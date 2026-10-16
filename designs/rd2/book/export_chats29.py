"""The 29 UBS chats in the Deutsche Bank career, each with UBS's added line per framing, for make_chats29_doc.js
(RD2, 2026-10-16).

    python designs/rd2/book/export_chats29.py chats29.json && node designs/rd2/book/make_chats29_doc.js chats29.json out.docx

The 12 on trading days take their lines from data/silver/ubs_frames.json, the 17 chat-only ones from
data/silver/ubs_frames_chat_only.json (both drafts the user is reviewing)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
os.chdir(ROOT)
from briefing import BARE_REPLIES
from career import EARLY_BARE, early_events
from mountain import DAYS

FR = json.load(open("data/silver/framed_chats_75.json"))["results"]
ROWS = {r["id"]: r for r in FR}
TAC = {c["id"]: c for c in json.load(open("data/silver/tac_chats.json"))["conversations"]}
TRADING = json.load(open("data/silver/ubs_frames.json"))["chats"]
CHAT_ONLY = json.load(open("data/silver/ubs_frames_chat_only.json"))["chats"]
out = []
for e in early_events(FR, before="2099"):
    if not any(s.startswith("UBS") for s, t in e["lines"]):
        continue
    r, cid = ROWS[e["id"]], e["id"]
    frames = TRADING.get(cid) or CHAT_ONLY[cid]
    rows = []
    for sp, t in r["real_history"]:
        if sp == "***":
            rows.append(["", "[messages omitted in the court record]", "gap"])
        elif sp == r["model_role"]:
            rows.append(["Deutsche Bank", t, "removed"])            # the agent writes its own lines
        elif (cid, t) in BARE_REPLIES | EARLY_BARE:
            rows.append([sp.split(" [")[0], t, "bare"])              # answered a removed line
        else:
            rows.append([sp.split(" [")[0], t, "shown"])
    full = [tuple(m) for m in TAC[cid]["messages"]]
    hist = [tuple(m) for m in r["real_history"]]
    dp = next((p for p in TAC[cid]["decision_points"] if full[:p["after"] + 1] == hist), None)
    after = []
    if dp:
        for sp, t in full[dp["after"] + 1:]:
            who = "" if sp == "***" else "Deutsche Bank" if sp == r["model_role"] else sp.split(" [")[0]
            after.append([who, "[messages omitted in the court record]" if sp == "***" else t])
    out.append({"id": cid, "date": e["date"], "trading": e["date"] in DAYS, "ask": frames["what"].split(", ", 1)[1],
                "decision": e["decision"], "real_did": (dp or {}).get("human_choice", ""), "rows": rows, "after": after,
                "frames": [[k, frames[k]] for k in ("loss", "gain", "loss + you", "gain + you")]})
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out), "chats,", sum(c["trading"] for c in out), "on trading days, written to", sys.argv[1])
