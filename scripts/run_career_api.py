"""The career pilot via the Gemini API (the user, 2026-10-16: a quick look without Colab). Same design as notebook 16:
one Deutsche Bank agent, the 8 early chats of 2007-2010 once (shared by every version), the management briefing with
the first update of 7 Jan 2011, then trading 7 and 12 Jan, all in one sustained conversation (sim/career.py).

The API serves Gemma 4, not the Gemma 3 12B of notebooks 14-16, so this is a first look at behaviour, not the main run.
Same call settings as the other API runs (temperature 0.7, thinking minimal, API filter off).

Usage (the key is read from the GEMINI_API_KEY environment variable, never printed):
    python scripts/run_career_api.py --out outputs/rd2_api/career_pilot
Run the same command again to resume: the early history is kept, finished careers are skipped.
"""
import argparse, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sim"))
os.chdir(ROOT)
from briefing import BARE_REPLIES, MODE, chats_version, load_briefings
from career import EARLY_BARE, Career, briefing_message, career_opening, chat_text, early_events
from mountain import load_chat_setups

API = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
p = argparse.ArgumentParser()
p.add_argument("--model", default="gemma-4-26b-a4b-it")
p.add_argument("--versions", default="neutral,loss,gain,loss + you,gain + you")
p.add_argument("--days", default="2011-01-07,2011-01-12")
p.add_argument("--runs", type=int, default=1)
p.add_argument("--temperature", type=float, default=0.7)
p.add_argument("--max-tokens", type=int, default=300)
p.add_argument("--gap", type=float, default=4.0, help="seconds between calls (pacing for rate limits)")
p.add_argument("--out", default="outputs/rd2_api/career_pilot")
args = p.parse_args()
VERSIONS = [v.strip() for v in args.versions.split(",")]
TRADING = [d.strip() for d in args.days.split(",")]
OUT = ROOT / args.out
for sub in ("days", "careers", "early"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
KEY = os.environ.get("GEMINI_API_KEY")
assert KEY, "Set the GEMINI_API_KEY environment variable"
SAFETY = [{"category": c, "threshold": "OFF"} for c in
          ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
_last = [0.0]


def generate(turns):
    """One reply to [{role, content}] turns; the same call as scripts/run_mountain_api.py."""
    body = {"contents": [{"role": "model" if t["role"] == "assistant" else "user", "parts": [{"text": t["content"]}]}
                         for t in turns if t["role"] != "system"],
            "systemInstruction": {"parts": [{"text": turns[0]["content"]}]},
            "safetySettings": SAFETY,
            "generationConfig": {"temperature": args.temperature, "maxOutputTokens": args.max_tokens,
                                 "thinkingConfig": {"thinkingLevel": "minimal"}}}
    for attempt in range(8):
        wait = args.gap - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = requests.post(API.format(args.model), headers={"x-goog-api-key": KEY}, json=body, timeout=180)
        except requests.RequestException as e:
            print(f"   network error ({type(e).__name__}), retrying", flush=True)
            time.sleep(min(60, 5 * 2 ** attempt))
            continue
        if r.status_code == 429:
            err = json.dumps(r.json().get("error", {}))
            if "PerDay" in err:
                sys.exit("Daily API quota reached: run the same command again tomorrow to continue")
            m = re.search(r'"retryDelay": "(\d+)', err)
            time.sleep(int(m.group(1)) + 2 if m else 30 * (attempt + 1))
            continue
        if r.status_code >= 500:
            time.sleep(min(120, 5 * 2 ** attempt))
            continue
        if not r.ok:
            sys.exit(f"API error {r.status_code}: {r.text[:300]}")
        j = r.json()
        cand = (j.get("candidates") or [{}])[0]
        text = "".join(x.get("text", "") for x in cand.get("content", {}).get("parts", []) if not x.get("thought")).strip()
        generate.finish = cand.get("finishReason") or str(j.get("promptFeedback", {}).get("blockReason"))
        generate.context = (j.get("usageMetadata") or {}).get("promptTokenCount", 0)
        generate.most = max(getattr(generate, "most", 0), generate.context or 0)
        return text
    raise RuntimeError("gave up after 8 attempts")


B, SETUPS = load_briefings(), load_chat_setups()
FRAMED = json.load(open("data/silver/framed_chats_75.json"))["results"]
EARLY, OPENING = early_events(FRAMED), career_opening()
SET_ID = "ca" + hashlib.md5(json.dumps(
    [open(f).read() for f in ["sim/mountain.py", "sim/chat_market.py", "sim/silver_day.py", "sim/briefing.py", "sim/career.py",
                              "data/silver/chat_market_pilot.json", "data/silver/framed_chats_75.json",
                              "data/silver/desk_briefings.json"]]
    + [OPENING] + [chat_text(e) for e in EARLY] + [sorted(BARE_REPLIES), sorted(EARLY_BARE), MODE, TRADING,
                                                     args.model, args.temperature, args.max_tokens]).encode()).hexdigest()[:8]
done = {(c["version"], c["run"]) for c in (json.load(open(f)) for f in (OUT / "careers").glob("*.json")) if c["set"] == SET_ID}
print(f"Career pilot via the API: {args.model} | {len(EARLY)} early chats, then {TRADING} | {len(VERSIONS)} versions x "
      f"{args.runs} run | {len(done)} careers done | {SET_ID}", flush=True)
t0 = time.time()
for k in range(args.runs):
    early_path = OUT / "early" / f"r{k}.json"
    base = Career(generate, OPENING)
    if early_path.exists():
        saved = json.load(open(early_path))
        assert saved["set"] == SET_ID, f"{early_path} is from other settings: use another --out"
        base.history, base.records = saved["history"], saved["records"]
    else:
        for e in EARLY:
            reply = base.chat(e)
            print(f"{e['date']} {e['id']}: {reply[:160]!r}", flush=True)
        json.dump({"set": SET_ID, "model": args.model, "run": k, "history": base.history, "records": base.records},
                  open(early_path, "w"), indent=1)
    for v in VERSIONS:
        if (v, k) in done:
            continue
        c = base.fork()
        generate.most = 0
        for date in TRADING:
            day, finishes = c.trade_day(date, v, FRAMED, SETUPS, briefing=briefing_message(v, B) if date == TRADING[0] else None)
            steps = [{**{x: r.get(x) for x in ("time", "price_seen", "observation", "reply", "status", "problem", "target",
                                               "traded", "chat", "quote", "joined", "rival_traded", "stop_fills", "delivered",
                                               "price_after", "valued_at", "position", "over_limit", "pnl", "corrections")},
                      "finish": f} for r, f in zip(day.log, finishes)]
            name = f"{v.replace(' + ', '_plus_').replace(' ', '_')}_r{k}_{date}"
            row = {"version": v, "run": k, "mode": MODE, "chats": chats_version(v), "briefing": B["versions"][v], "date": date,
                   "model": args.model, "precision": "API", "set": SET_ID, "career": True, "summary": day.summary(),
                   "diary": day.diary(), "finishes": finishes, "memory_days": len(EARLY) + TRADING.index(date), "steps": steps}
            json.dump(row, open(OUT / "days" / f"{name}.json", "w"))
            s = row["summary"]
            print(f"{v} | {date} | P&L ${s['pnl']:+,.0f} | went along {[ch for ch, m in s['chats'].items() if m['joined']] or 'no'} | "
                  f"{(time.time() - t0) / 60:.0f} min", flush=True)
        json.dump({"set": SET_ID, "model": args.model, "version": v, "run": k, "context_tokens_most": generate.most,
                   "history": c.history, "records": c.records}, open(OUT / "careers" / f"{name.rsplit('_', 1)[0]}.json", "w"))
print(subprocess.run([sys.executable, "designs/rd2/analysis/briefing_pilot.py", str(OUT)], capture_output=True, text=True).stdout)
