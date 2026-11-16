"""Data for the two Word booklets (2026-10-15): every framed chat, and every reply of the agent at UBS's asks.

    python designs/rd2/book/make_booklets.py <out.json>
    NODE_PATH=<folder with docx installed>/node_modules node designs/rd2/book/booklets.js <out.json> <out folder>
"""
import collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, os.path.join(ROOT, "sim"))
from chat_market import SIGN          # noqa: E402
from mountain import TIMES, WINDOW    # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "outputs/booklets/booklets.json"
FOLDER = os.path.join(ROOT, "results/mountain_gemma-3-12b-it_4bit")
GRADES = os.path.join(HERE, "..", "results_final_round_12b")
VERSIONS = ["real", "loss", "gain", "loss + you", "gain + you", "no ask"]
MODES = {"takeover 5 days": "Full takeover", "takeover 1 day": "One line"}
STEP = {f"{8 + k // 4:02d}:{15 * (k % 4):02d}": k for k in range(24)}
SHARE = {"p315_tell_me_stops": "where the desk's clients' stop orders sit",
         "p277_chinese_buying": "what the desk's clients are doing",
         "p278_give_me_a_call": "the desk's own position",
         "p279_last_price_chinese_paid": "the price a client paid the desk",
         "p240_just_quote_wider": "a wider quote to the desk's client",
         "p362_everything_stays_here": "to keep the chat between them"}
used_order = [cid for pairs in TIMES.values() for cid, _ in pairs]

# ---- the framed chats (all 73 that are run) ----
framed = json.load(open(os.path.join(ROOT, "data/silver/framed_chats_75.json")))
notes = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data/silver/frames_75.json")))["chats"]}
tac = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data/silver/tac_chats.json")))["conversations"]}
by = collections.defaultdict(dict)
for r in framed["results"]:
    by[r["id"]][r["frame"] + (" + you" if r["owner"] else "")] = r
chats = []
for cid, vs in by.items():
    r0 = vs["loss"]
    chats.append({"id": cid, "para": tac[cid]["paragraph"], "date": tac[cid]["date"], "name": cid.split("_", 1)[1].replace("_", " "),
                  "kind": r0["kind"], "decision": r0["decision"], "role": r0["model_role"], "context": notes[cid]["context"],
                  "used": cid in used_order, "real": r0["real_history"],
                  "versions": {v: vs[v]["history_all"] for v in ["loss", "gain", "loss + you", "gain + you"]}})
chats.sort(key=lambda c: (not c["used"], used_order.index(c["id"]) if c["used"] else 0, c["date"] or "9999", c["id"]))

# ---- the agent's replies at each ask ----
def grades(kind, pattern):
    key = {}
    for f in glob.glob(os.path.join(GRADES, kind, "key*.json")):
        key.update(json.load(open(f)))
    out = {}
    for f in sorted(glob.glob(os.path.join(GRADES, kind, pattern))):
        for code, lab in json.load(open(f)).items():
            k = key[code]
            out.setdefault((k["version"], k["mode"], k["run"], k["date"], k["time"]), lab)
    return out
named = grades("flags", "flag_labels_1.json")
shown = grades("disclosure", "disclosure_labels_[0-9].json")

def order(steps, i):
    s, before = steps[i], steps[i - 1]["position"] if i else 0
    if s["status"] == "trade":
        what = f"TARGET {s['target']:+,}: " + (("bought " if s["traded"] > 0 else "sold ") + f"{abs(s['traded']):,} oz" if s["traded"] else "no change")
    elif s["status"] == "hold":
        what = "HOLD: no trade"
    elif s["status"] == "quote only":
        what = "quote only: no trade"
    else:
        what = "unreadable reply: nothing traded"
    if s["quote"] is not None:
        what += f"; quoted the client {s['quote']} cents"
    what += f"; position {before:+,} -> {s['position']:+,} oz"
    if s["rival_traded"]:
        what += f"; UBS {'sold' if s['rival_traded'] < 0 else 'bought'} {abs(s['rival_traded']):,} oz"
    return what

days = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(FOLDER, "days", "*.json")))]
reps = {}
for v in VERSIONS:
    for m in MODES:
        for n, r in enumerate(sorted({d["run"] for d in days if d["version"] == v and d["mode"] == m})):
            reps[(v, m, r)] = n + 1
asks = []
for date, pairs in TIMES.items():
    for cid, at in pairs:
        c0 = next(d for d in days if d["date"] == date)["summary"]["chats"][cid]
        push = bool(SIGN[c0["wants"]])
        w = STEP[WINDOW.get(cid, at)]
        idx = sorted({STEP[at], w, w + 1}) if push else [STEP[at]]
        entry = {"date": date, "at": at, "id": cid, "name": cid.split("_", 1)[1].replace("oclock", "o'clock").replace("_", " "),
                 "push": push, "wants": c0["wants"], "share": SHARE.get(cid), "versions": []}
        for v in VERSIONS:
            if v == "no ask" and not push:
                continue
            ds = sorted((d for d in days if d["version"] == v and d["date"] == date),
                        key=lambda d: (list(MODES).index(d["mode"]), d["run"]))
            full = next(d for d in ds if d["mode"] == "takeover 5 days")
            said = [["UBS" if not x["inherited"] else "Deutsche Bank (2011 line)", x["text"]] for x in full["steps"][STEP[at]]["delivered"]]
            runs = []
            for d in ds:
                sm = d["summary"]["chats"][cid]
                steps = []
                for i in idx:
                    s = d["steps"][i]
                    k = (v, d["mode"], d["run"], date, s["time"])
                    steps.append({"t": s["time"], "reply": s["reply"] or "", "chat": s["chat"], "order": order(d["steps"], i),
                                  "joined": bool(s["joined"]), "named": named.get(k), "shown": shown.get(k) if s["chat"] else None})
                runs.append({"mode": MODES[d["mode"]], "rep": reps[(v, d["mode"], d["run"])],
                             "joined": bool(sm["joined"]) if push else None, "quote": sm.get("quote"), "steps": steps})
            entry["versions"].append({"version": v, "said": said, "runs": runs})
        asks.append(entry)

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
json.dump({"chats": chats, "asks": asks}, open(OUT, "w"))
print(f"{len(chats)} framed chats; {len(asks)} asks; {sum(len(r['steps']) for a in asks for v in a['versions'] for r in v['runs'])} replies -> {OUT}")
