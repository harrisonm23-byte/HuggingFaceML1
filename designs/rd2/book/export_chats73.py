"""All 73 chats of the words study, whole, for make_chats73_doc.js (2026-10-16): who the agent plays, where it answers,
what the real trader did, and which chats are also in the trading run (12) and the pilot (2).

    python designs/rd2/book/export_chats73.py chats73.json && node designs/rd2/book/make_chats73_doc.js chats73.json out.docx
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
os.chdir(ROOT)
from mountain import TIMES, DAYS

T = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
R = {r["id"]: r for r in json.load(open("data/silver/framed_chats_75.json"))["results"]}
trading = [c for d in DAYS for c, _ in TIMES[d]]
pilot = [c for d in DAYS[:2] for c, _ in TIMES[d]]
KIND = {"join": "coordinate prices or trading", "share": "share confidential information", "conceal": "keep it hidden"}
out = []
for cid in sorted(R, key=lambda c: (T[c]["date"] or "9999", c)):
    r, c = R[cid], T[cid]
    msgs = [tuple(m) for m in c["messages"]]
    assert [tuple(m) for m in r["real_history"]] == msgs[:r["decision_after"] + 1], cid
    dp = next(p for p in c["decision_points"] if p["after"] == r["decision_after"] and p["model_role"] == r["model_role"])
    rows = []
    for i, (sp, t) in enumerate(msgs):
        if i == r["decision_after"] + 1:
            rows.append(["", f"THE AGENT ANSWERS HERE, as {r['model_role']}", "", "marker"])
        where = "before" if i <= r["decision_after"] else "after"
        rows.append(["" if sp == "***" else sp, "[messages omitted in the court record]" if sp == "***" else t, where,
                     "self" if sp == r["model_role"] else "gap" if sp == "***" else "other"])
    if r["decision_after"] + 1 >= len(msgs):
        rows.append(["", f"THE AGENT ANSWERS HERE, as {r['model_role']}", "", "marker"])
    out.append({"id": cid, "date": c["date"], "paragraph": c.get("paragraph"), "scheme": c.get("scheme"),
                "core": r["set"] == "core", "role": r["model_role"], "kind": KIND.get(r["kind"], r["kind"]),
                "decision": r["decision"], "real_did": dp.get("human_choice") or "", "note": c.get("note") or "",
                "trading": cid in trading, "pilot": cid in pilot, "rows": rows})
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out), "chats;", sum(x["trading"] for x in out), "in the trading run;", sum(x["pilot"] for x in out), "in the pilot")
