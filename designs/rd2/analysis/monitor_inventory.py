"""State monitor, Phase 1, Step 0: what is saved for the monitor (DESIGN: designs/rd2/MONITOR.md).

    python designs/rd2/analysis/monitor_inventory.py <folder holding the downloaded <exp>_bf16 state folders>

Reads every saved decision-state file (rd2-states v2/<exp>_bf16/*.npz: the residual stream at every layer, at the last
token before the agent's reply, at each push request of each career), checks each moment against the career as saved in
results/ (same reply, same "joined" label), and counts requests, going along (the paper's trade measure, "joined") and
the words labels (results/words_all, results/words_b) per experiment and condition. Writes
results/monitor_heldout/INVENTORY.md and inventory.json.
"""
import collections, glob, json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
from inside_careers import moments

STATES = sys.argv[1]
OUT = os.path.join(ROOT, "results", "monitor_heldout")
FOLDERS = {"A": "career_book_neutral_lines_v2", "B": "ubs_framing_v2", "C": "takeover_ladder_v2",
           "C2": "takeover_ladder_real_lines_v2", "D": "memo_and_ubs_framing_v2", "E": "memo_ubs_bank_c_v2",
           "F": "peer_same_frame_v2"}
WHAT = {"A": "the memo and morning book; UBS's lines neutral", "B": "UBS's framing", "C": "the takeover ladder",
        "C2": "the takeover ladder, UBS's real lines", "D": "memo and UBS share the framing", "E": "B plus Bank C",
        "F": "memo, UBS and Bank C share the framing"}
os.makedirs(OUT, exist_ok=True)

# ---------------- the saved states
rows, shapes = [], collections.Counter()
for exp in FOLDERS:
    for p in sorted(glob.glob(os.path.join(STATES, f"{exp}_bf16", "*.npz"))):
        z = np.load(p)
        meta = json.loads(str(z["meta"]))
        shapes[(exp, z["states"].shape[1:])] += 1
        assert len(meta) == z["states"].shape[0], p
        for i, m in enumerate(meta):
            rows.append({**m, "exp": exp, "file": os.path.basename(p), "index": i})

# ---------------- check each moment against the career as saved in results/
mismatch, checked = collections.Counter(), collections.Counter()
for exp, folder in FOLDERS.items():
    path = os.path.join(ROOT, "results", f"full_career_gemma-3-12b-it_4bit_{folder}")
    if not os.path.isdir(path):
        continue
    saved = {(m["career_file"], m["chat"]): m for m in moments(path, exp)}
    for r in rows:
        if r["exp"] != exp:
            continue
        s = saved.get((r["career_file"], r["chat"]))
        checked[exp] += 1
        if s is None or s["joined"] != r["joined"] or s["reply"] != r["reply"] or s["asked"] != r["asked"]:
            mismatch[exp] += 1

# ---------------- words labels at the push requests
words = collections.Counter()
key = json.load(open(os.path.join(ROOT, "results", "words_all", "key.json")))
for m in key.values():
    if m["push_request"] and m["experiment"] in FOLDERS and m["experiment"] != "B":
        words[(m["experiment"], m["version"])] += 1
for m in json.load(open(os.path.join(ROOT, "results", "words_b", "key.json"))).values():
    if m.get("push_request"):
        words[("B", m["version"])] += 1

# ---------------- the table
NAME = {"neutral": "neutral", "loss": "loss", "gain": "gain", "loss + you": "blame", "gain + you": "credit",
        "no ask": "no ask", "clean": "clean", "first line": "first line", "up to 7 Jan": "up to 7 Jan",
        "whole career": "whole career"}
out = ["# State monitor, Step 0: the inventory\n",
       "Produced by `designs/rd2/analysis/monitor_inventory.py`. One row per experiment and condition. \"Requests\": push "
       "requests UBS actually made (Experiment A's \"no ask\" careers have the same moments with no request; they are "
       "listed but cannot be labelled going along). \"Went along\": the paper's trade measure (the simulator's "
       "\"joined\"). States: the residual stream at all 48 layers at the last token before the reply (rd2-states "
       "v2/<exp>_bf16). \"Checked\": each saved moment matched against the career as saved in results/ (same reply, "
       "same label).\n",
       "| Experiment | Condition | Careers | Requests | Went along | 7 Jan requests | Went along on 7 Jan | Words labels | "
       "States saved | Checked |", "|---|---|---|---|---|---|---|---|---|---|"]
summary = {"by_condition": [], "by_experiment": {}}
for exp in FOLDERS:
    rs = [r for r in rows if r["exp"] == exp]
    if not rs:
        out.append(f"| {exp} | (no states saved) | | | | | | | no | |")
        continue
    versions = sorted({r["version"] for r in rs}, key=lambda v: list(NAME).index(v) if v in NAME else 99)
    for v in versions:
        g = [r for r in rs if r["version"] == v]
        asked = [r for r in g if r["asked"]]
        jan7 = [r for r in asked if r["date"] == "2011-01-07"]
        row = {"experiment": exp, "condition": v, "careers": len({r["career_file"] for r in g}), "moments": len(g),
               "requests": len(asked), "went_along": sum(r["joined"] for r in asked), "jan7": len(jan7),
               "went_along_jan7": sum(r["joined"] for r in jan7), "words": words.get((exp, v), 0)}
        summary["by_condition"].append(row)
        out.append(f"| {exp} | {NAME.get(v, v)} | {row['careers']} | {row['requests']} | {row['went_along']} | "
                   f"{row['jan7']} | {row['went_along_jan7']} | {row['words']} | yes | |")
    asked = [r for r in rs if r["asked"]]
    e = {"careers": len({(r['version'], r['career_file']) for r in rs}), "requests": len(asked),
         "went_along": sum(r["joined"] for r in asked),
         "careers_with_any": len({(r['version'], r['career_file']) for r in asked if r["joined"]}),
         "checked": checked[exp], "mismatch": mismatch[exp]}
    summary["by_experiment"][exp] = e
    out.append(f"| **{exp} total** | {WHAT[exp]} | {e['careers']} | {e['requests']} | {e['went_along']} | | | "
               f"{sum(w for (x, _), w in words.items() if x == exp)} | yes | "
               f"{e['checked'] - e['mismatch']} of {e['checked']} |")
asked = [r for r in rows if r["asked"]]
out.append(f"| **All** | | {len({(r['exp'], r['version'], r['career_file']) for r in rows})} | {len(asked)} | "
           f"{sum(r['joined'] for r in asked)} | {sum(r['date'] == '2011-01-07' for r in asked)} | "
           f"{sum(r['joined'] for r in asked if r['date'] == '2011-01-07')} | {sum(words.values())} | | |")
out += ["\n**Careers that went along at least once**, per experiment (the unit the folds split on): " +
        ", ".join(f"{x} {e['careers_with_any']} of {e['careers']}" for x, e in summary["by_experiment"].items()) + ".",
        "\n**State files:** " + ", ".join(f"{e}: {n} files of {s[0]} layers x {s[1]}" for (e, s), n in shapes.items()) + "."]
open(os.path.join(OUT, "INVENTORY.md"), "w").write("\n".join(out) + "\n")
json.dump(summary, open(os.path.join(OUT, "inventory.json"), "w"), indent=1)
print("\n".join(out))
