# Does a solo stop hunt pay in the career market? A scripted agent sells at each step, buys back two steps later (no model). Run from the repo root.
import sys; sys.path.insert(0, "sim")
import mountain as m
import json, briefing
setups = m.load_chat_setups()
FR = json.load(open("data/silver/framed_chats_75.json"))["results"]
MODE = briefing.MODE
def run(date, start, size, hold_steps):
    d = m.make_day(date, "no ask", FR, setups, mode=MODE)
    side = 1 if d.cfg.stop_sides and list(d.cfg.stop_sides.values())[0] == "sell" else -1
    k, out = 0, None
    while not d.done:
        if k == start: a = f"TARGET {-side*size}"          # sell toward sell stops (buy toward buy stops)
        elif k == start + hold_steps: a = "TARGET 0"
        else: a = "HOLD"
        d.step(lambda obs, day: a); k += 1
    return d.pnl(), [s.fired_at for s in d.stops], side
for date in m.TRADING_DAYS if hasattr(m, "TRADING_DAYS") else ["2011-01-07","2011-01-12","2011-04-01","2011-06-08","2011-08-05"]:
    d0 = m.make_day(date, "no ask", FR, setups, mode=MODE)
    px = d0.price(); print(date, "stops:", [(s.client, s.level, s.size, d0.cfg.stop_sides[s.client]) for s in d0.stops], "open", px)
    best = None
    for size in (300_000, 600_000, 1_000_000):
        for start in range(0, 22):
            for hold in (1, 2, 4):
                pnl, fired, side = run(date, start, size, hold)
                r = (pnl, size, start, hold, sum(f is not None for f in fired))
                if best is None or pnl > best[0]: best = r
    hits = []
    for size in (300_000, 600_000, 1_000_000):
        res = [run(date, s, size, 2) for s in range(0, 22)]
        hits.append((size, sum(any(f) for _, f, _ in res), round(max(p for p, _, _ in res)), round(sum(p for p, _, _ in res)/len(res))))
    print("  best: pnl $%.0f size %d start step %d hold %d stops fired %d" % best)
    print("  by size (hold 2 steps): starts that fire a stop / best pnl / mean pnl over starts:", hits)
