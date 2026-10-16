"""The 12 UBS chats of the briefing design, as the agent sees them, for make_chats_doc.js (2026-10-16).

    python designs/rd2/book/export_chats12.py chats12.json && node designs/rd2/book/make_chats_doc.js chats12.json out.docx

"What the agent sees" is read from the agent's own updates in the simulator, so it cannot drift from the design."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "sim"))
os.chdir(ROOT)
from mountain import TIMES, DAYS, load_chat_setups, ME
from chat_market import chat_for
from briefing import briefing_day, load_frames, BARE_REPLIES

FR = json.load(open("data/silver/framed_chats_75.json"))["results"]
S, F = load_chat_setups(), load_frames()["chats"]
WANTS = {"up": "push the price up", "down": "push the price down"}
out = []
for date in DAYS:
    d, obs = briefing_day(date, "neutral", FR, S), {}

    def agent(o, dd):
        if "New chat messages:" in o:
            obs[dd.now()] = [l.strip() for l in o.split("New chat messages:")[1].strip().splitlines()]
        return "HOLD"
    d.run(agent)
    for cid, at in TIMES[date]:
        sees = obs.get(at, [])
        rows = []
        for sp, t in chat_for(cid, "real", FR):
            if sp == "***":
                rows.append(["", "[messages omitted in the court record]",
                             'shown as "[... messages omitted ...]"' if "[... messages omitted ...]" in sees else "not shown"])
            elif sp == ME:
                rows.append(["Deutsche Bank", t, "removed (Deutsche Bank's line)"])
            elif (cid, t) in BARE_REPLIES:
                rows.append(["UBS", t, "removed (it answered a removed line)"])
            else:
                rows.append(["UBS", t, "shown"])
        assert [l.split(": ", 1)[1] for l in sees if l.startswith("UBS")] == [r[1] for r in rows if r[2] == "shown"], cid
        out.append({"id": cid, "date": date, "time": at, "ask": WANTS.get(S[cid]["wants"], F[cid]["what"].split(", ", 1)[1]),
                    "push": S[cid]["wants"] in WANTS, "pilot": date in DAYS[:2], "real": rows, "sees": sees,
                    "frames": [[k, F[cid][k]] for k in ("loss", "gain", "loss + you", "gain + you")]})
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(out), "chats written to", sys.argv[1])
