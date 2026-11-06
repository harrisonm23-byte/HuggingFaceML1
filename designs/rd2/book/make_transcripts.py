"""Plain-text transcripts (2026-10-16): the real 2011 chats, and every step of every final-round run as the agent
saw and answered it. No formatting, no grades.

    python designs/rd2/book/make_transcripts.py <out folder>
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, os.path.join(ROOT, "sim"))
from mountain import opening, TIMES    # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "outputs/transcripts"
os.makedirs(OUT, exist_ok=True)
RULE = "=" * 78

# 1. The real chats, as quoted in the complaint
tac = json.load(open(os.path.join(ROOT, "data/silver/tac_chats.json")))
used = {cid for pairs in TIMES.values() for cid, _ in pairs}
lines = ["REAL SILVER CHATS, 2011 AND EARLIER (as quoted in the Third Amended Complaint, In re London Silver Fixing,",
         "No. 14-md-2573, Dkt. 258). Allegations in a complaint, quoted as filed. *** = messages the complaint left out.",
         "[FINAL ROUND] marks the chats the trading agent saw.", ""]
for c in sorted(tac["conversations"], key=lambda c: (c["date"] or "9999", c["id"])):
    lines += [RULE, f"{c['date'] or 'date not given'}  ¶{c['paragraph']}  {c['id']}" + ("  [FINAL ROUND]" if c["id"] in used else ""), RULE]
    for speaker, text in c["messages"]:
        lines.append("***" if speaker == "***" else f"{speaker}: {text}")
    lines.append("")
open(os.path.join(OUT, "Real silver chats (court record).txt"), "w").write("\n".join(lines))

# 2. The final round, one file per version
days = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(ROOT, "results/mountain_gemma-3-12b-it_4bit/days/*.json")))]
MODES = {"takeover 5 days": "FULL TAKEOVER", "takeover 1 day": "ONE LINE"}
for v in ["real", "loss", "gain", "loss + you", "gain + you", "no ask"]:
    ds = sorted((d for d in days if d["version"] == v), key=lambda d: (list(MODES).index(d["mode"]), d["run"], d["date"]))
    out = [f"FINAL ROUND TRANSCRIPTS, VERSION: {v.upper()}",
           f"Model {ds[0]['model']} ({ds[0]['precision']}), setup {ds[0]['set']}. Every 15-minute step: what the agent was shown,",
           "then its reply word for word. Earlier days reached the agent through the desk diary (shown at the end of each day).", "",
           RULE, "THE AGENT'S INSTRUCTIONS (the same in every run)", RULE, opening(), ""]
    reps = {}
    for d in ds:
        reps.setdefault((d["mode"], d["run"]), len([k for k in reps if k[0] == d["mode"]]) + 1)
    for d in ds:
        out += ["", RULE, f"{MODES[d['mode']]} RUN {reps[(d['mode'], d['run'])]}  |  {d['date']}  |  version: {v}", RULE]
        for s in d["steps"]:
            out += ["", f"----- {s['time']} UTC -----", "[SHOWN TO THE AGENT]", s["observation"]]
            for rejected, note in s["corrections"]:
                out += ["[AGENT REPLY, SENT BACK]", rejected, "[CORRECTION SHOWN TO THE AGENT]", note]
            out += ["[AGENT REPLY]", s["reply"] or "(empty)"]
        out += ["", "[DESK DIARY ENTRY KEPT FROM THIS DAY]", d["diary"] or "(none)"]
    open(os.path.join(OUT, f"Final round transcripts - {v}.txt"), "w").write("\n".join(out))
print("\n".join(f"{f}: {os.path.getsize(os.path.join(OUT, f)) / 1e6:.1f} MB" for f in sorted(os.listdir(OUT))))
