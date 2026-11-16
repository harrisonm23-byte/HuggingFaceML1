"""The book of the final round: every day's chat, the agent's replies and its trading, as one page (2026-10-15).

    python designs/rd2/book/make_book.py results/mountain_gemma-3-12b-it_4bit <out.html>

Reads the saved days (results/<folder>/days/*.json) and the blind grades (results_final_round_12b/flags and
disclosure), and writes book_template.html with the data built in. Nothing is recomputed except the measures the
analysis already uses (joined, the ask's window); the observations are left out to keep the page small.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "sim"))
from chat_market import SIGN          # noqa: E402
from mountain import TIMES, WINDOW    # noqa: E402

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "results/mountain_gemma-3-12b-it_4bit"
OUT = sys.argv[2] if len(sys.argv) > 2 else "outputs/mountain_book.html"
GRADES = os.path.join(HERE, "..", "results_final_round_12b")
VERSIONS = ["real", "loss", "gain", "loss + you", "gain + you", "no ask"]
MODES = {"takeover 5 days": "full", "takeover 1 day": "one"}
STEP = {f"{8 + k // 4:02d}:{15 * (k % 4):02d}": k for k in range(24)}
SHARE = {"p315_tell_me_stops": "where the desk's clients' stop orders sit",
         "p277_chinese_buying": "what the desk's clients are doing",
         "p278_give_me_a_call": "the desk's own position",
         "p279_last_price_chinese_paid": "the price a client paid the desk",
         "p240_just_quote_wider": "a wider quote to the desk's client",
         "p362_everything_stays_here": "to keep the chat between them"}


def name(cid):
    # p253_11_oclock_rule -> "11 o'clock rule"
    return cid.split("_", 1)[1].replace("oclock", "o'clock").replace("_", " ")


def grades(kind, pattern):
    # Grader 1's label for each (version, mode, run, date, time); the second grader's where there is one
    key = {}
    for f in glob.glob(os.path.join(GRADES, kind, "key*.json")):
        key.update(json.load(open(f)))
    first, second = {}, {}
    for f in sorted(glob.glob(os.path.join(GRADES, kind, pattern))):
        target = second if kind == "flags" and f.endswith("_2.json") else first
        target.update(json.load(open(f)))
    out = {}
    for code, lab in first.items():
        k = key[code]
        out[(k["version"], k["mode"], k["run"], k["date"], k["time"])] = [lab, second.get(code)]
    return out


flags = grades("flags", "flag_labels_*.json")
disclosure = grades("disclosure", "disclosure_labels_[0-9].json")

days = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(FOLDER, "days", "*.json")))]
assert len(days) == 300 and len({d["set"] for d in days}) == 1
reps = {}
for v in VERSIONS:
    for m in MODES:
        for n, r in enumerate(sorted({d["run"] for d in days if d["version"] == v and d["mode"] == m})):
            reps[(v, m, r)] = n + 1

book = []
for d in sorted(days, key=lambda d: (VERSIONS.index(d["version"]), list(MODES).index(d["mode"]), d["run"], d["date"])):
    sm, steps = d["summary"], d["steps"]
    rep = reps[(d["version"], d["mode"], d["run"])]
    asks = []
    for cid, at in TIMES[d["date"]]:
        c = sm["chats"][cid]
        w = STEP[WINDOW.get(cid, at)]
        asks.append({"id": cid, "name": name(cid), "at": at, "wants": c["wants"], "push": bool(SIGN[c["wants"]]),
                     "share": SHARE.get(cid), "win": [steps[i]["time"] for i in range(w, min(w + 2, len(steps)))],
                     "joined": bool(c["joined"]) if SIGN[c["wants"]] else None, "quote": c.get("quote")})
    out_steps = []
    for s in steps:
        k = (d["version"], d["mode"], d["run"], d["date"], s["time"])
        out_steps.append({"t": s["time"], "p": s["price_seen"], "pa": s["price_after"], "tg": s["target"],
                          "tr": s["traded"], "pos": s["position"], "st": s["status"], "r": s["reply"],
                          "c": s["chat"], "q": s["quote"], "j": s["joined"], "u": s["rival_traded"],
                          "sf": [[f["client"], f["at"], f["fill"], f["size"]] for f in s["stop_fills"]],
                          "dl": [["D" if x["inherited"] else "U", x["text"]] for x in s["delivered"]],
                          "co": s["corrections"], "pnl": s["pnl"], "fl": flags.get(k), "ds": disclosure.get(k)})
    book.append({"id": "-".join([d["version"].replace(" + ", "-").replace(" ", "-"), MODES[d["mode"]], str(rep), d["date"]]),
                 "v": d["version"], "m": MODES[d["mode"]], "rep": rep, "run": d["run"], "date": d["date"],
                 "pnl": sm["pnl"], "harm": sm["client_harm"], "stops": sm["book_stops"],
                 "fired": [[f["client"], f["at"], f["fill"], f["pushed"], f["harm"]] for f in sm["stops_fired"]],
                 "book": sm["book_lines"], "asks": asks, "close": sm["closeout"], "diary": d["diary"], "s": out_steps})

# Every chat as the agent saw it (the full takeover run; identical in every run), side by side across the wordings
chats = []
for date, pairs in TIMES.items():
    for cid, at in pairs:
        seen = {}
        for v in VERSIONS[:-1]:
            d = next(d for d in days if d["version"] == v and d["mode"] == "takeover 5 days" and d["date"] == date)
            seen[v] = [["D" if x["inherited"] else "U", x["text"]] for x in next(s for s in d["steps"] if s["time"] == at)["delivered"]]
        assert all(len(x) == len(seen["real"]) for x in seen.values()), cid
        c = days[0]["summary"]["chats"].get(cid) or next(d["summary"]["chats"][cid] for d in days if cid in d["summary"]["chats"])
        chats.append({"date": date, "at": at, "id": cid, "name": name(cid), "wants": c["wants"], "push": bool(SIGN[c["wants"]]),
                      "share": SHARE.get(cid), "lines": seen})

meta = {"model": days[0]["model"], "precision": days[0].get("precision"), "set": days[0]["set"], "days": len(days)}
missing = len(flags) - sum(s["fl"] is not None for b in book for s in b["s"])
assert missing == 0 and sum(s["ds"] is not None for b in book for s in b["s"]) == len(disclosure), "grades not placed"
push = [(b["v"], a["joined"]) for b in book for a in b["asks"] if a["push"]]
print(f"{len(book)} days; asked joined {sum(j for v, j in push if v != 'no ask')}/{sum(v != 'no ask' for v, j in push)}; "
      f"no ask {sum(j for v, j in push if v == 'no ask')}/{sum(v == 'no ask' for v, j in push)}; "
      f"{len(flags)} graded wrongdoing replies, {len(disclosure)} graded messages placed")
data = json.dumps({"meta": meta, "days": book, "chats": chats}, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
html = open(os.path.join(HERE, "book_template.html")).read().replace("/*DATA*/null", data)
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(html)
print(f"{OUT}: {len(html) / 1e6:.1f} MB")
