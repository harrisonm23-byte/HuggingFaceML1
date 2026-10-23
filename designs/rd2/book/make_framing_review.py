"""A review page for every framed chat: the real chat and its four framed versions side by side (2026-10-15).

    python designs/rd2/book/make_framing_review.py <out.html>

Reads data/silver/framed_chats_75.json (the 73 chats that are run), frames_75.json (context notes) and tac_chats.json
(dates), marks the 12 chats the final round used, and writes framing_review_template.html with the data built in.
The user's marks and notes are kept in the page's own store (the artifact's db), not in this repository.
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, os.path.join(ROOT, "sim"))
from mountain import TIMES    # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "outputs/framing_review.html"
VERSIONS = [("loss", None), ("gain", None), ("loss", "you"), ("gain", "you")]
NAMES = ["loss", "gain", "loss + you", "gain + you"]
framed = json.load(open(os.path.join(ROOT, "data/silver/framed_chats_75.json")))
notes = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data/silver/frames_75.json")))["chats"]}
tac = {c["id"]: c for c in json.load(open(os.path.join(ROOT, "data/silver/tac_chats.json")))["conversations"]}
used = {cid for pairs in TIMES.values() for cid, _ in pairs}

by = collections.defaultdict(dict)
for r in framed["results"]:
    by[r["id"]][(r["frame"], r["owner"])] = r
chats = []
for cid, vs in by.items():
    r0 = vs[VERSIONS[0]]
    real = r0["real_history"]
    lines = {"real": real}
    for key, nm in zip(VERSIONS, NAMES):
        h = vs[key]["history_all"]
        assert len(h) == len(real) and all(a[0] == b[0] for a, b in zip(h, real)), cid
        lines[nm] = h
    t = tac[cid]
    chats.append({"id": cid, "para": t["paragraph"], "date": t["date"], "name": cid.split("_", 1)[1].replace("_", " "),
                  "kind": r0["kind"], "decision": r0["decision"], "role": r0["model_role"], "set": notes[cid]["set"],
                  "context": notes[cid]["context"], "offer_framed": r0["offer_framed"], "used": cid in used, "lines": lines})
chats.sort(key=lambda c: (c["date"] or "9999", int(c["para"].split("-")[0]), c["id"]))   # p310 has no date in the complaint
assert len(chats) == 73 and sum(c["used"] for c in chats) == 12
data = json.dumps({"made": framed["rewriter"], "chats": chats}, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
html = open(os.path.join(HERE, "framing_review_template.html")).read().replace("/*DATA*/null", data)
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(html)
print(f"{len(chats)} chats ({sum(c['used'] for c in chats)} in the final round) -> {OUT}: {len(html) / 1e3:.0f} KB")
