"""Blind packets for the careers with a document's state on (state_careers_words.py reads the labels).

    python designs/rd2/analysis/state_careers_words_prep.py

The 22 Oct packet's code was not kept; this rebuilds it and first checks that it gives every one of the 90 items in
results/state_careers_words/key.json exactly (same text, wants, joined). Then every push request in the layer-22 x2 and
no-state careers not yet in the key goes into a new packet (packet_2.txt), shuffled, with 20 of the old items mixed in
blind as a check that the new graders read the rubric as the old ones did; key.json gains the new items.
Each item: the agent's reasoning and chat message at the request and 15 minutes later, its orders (TARGET, HOLD, QUOTE lines after the reasoning) and arm
hidden, under one line saying which way UBS wants the price.
"""
import glob, json, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HERE = os.path.join(ROOT, "results", "state_careers_words")
PUSH = ["p344_i_can_hunt_with_u", "p316_bust_through_it", "p252_screw_other_people_harder", "p250_grow_our_mafia",
        "p317_stop_busters", "p253_11_oclock_rule"]
ARM = re.compile(r"^(none|(random|gain|credit|loss|blame)_x2_L22)_r\d+$")
WANTS = {"down": "UBS wants the silver price pushed down.", "up": "UBS wants the silver price pushed up."}


def minutes(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def step_text(st):
    reasoning = re.split(r"\n+(?:TARGET|HOLD|QUOTE)\b", st["reply"])[0].strip()   # an order opening the reply stays
    out = f"[{st['time']}] Reasoning: {reasoning}"
    return out + (f"\n  Message to UBS/chat: {st['chat']}" if st["chat"] else "")


def items(folder):
    wording = os.path.basename(folder).split("state_careers_")[1].replace("_plus_you", " + you").replace("_v2", "")
    wording = wording or "v2"                                   # the neutral folder (state_careers_v2), as the key has it
    for path in sorted(glob.glob(os.path.join(folder, "days", "*.json"))):
        d = json.load(open(path))
        arm = f"{d['arm'] if d['arm'] != 'none' else 'none'}"
        name = os.path.basename(path)[:-len("_2011-01-07.json")]
        if not ARM.match(name):
            continue
        for cid in PUSH:
            ch = d["summary"]["chats"].get(cid)
            if not ch:
                continue
            at = minutes(ch["at"])
            steps = [st for st in d["steps"] if at <= minutes(st["time"]) <= at + 15]
            yield {"wording": wording, "arm": name, "date": d["date"], "chat": cid, "wants": ch["wants"],
                   "joined": bool(ch["joined"]), "text": "\n".join(step_text(st) for st in steps)}


folders = sorted(glob.glob(os.path.join(ROOT, "results", "full_career_gemma-3-12b-it_4bit_state_careers*_v2")))
found = [it for f in folders for it in items(f)]
ident = lambda it: (it["wording"], it["arm"], it["date"], it["chat"])
by = {ident(it): it for it in found}
assert len(by) == len(found)
key = json.load(open(os.path.join(HERE, "key.json")))
bad = [k["id"] for k in key if ident(k) not in by or any(by[ident(k)][f] != k[f] for f in ("text", "wants", "joined"))]
assert not bad, f"rebuilt items differ from the 22 Oct key: {bad[:10]} ({len(bad)})"
print(f"the 22 Oct key rebuilt exactly: {len(key)} of {len(key)} items")
old = {ident(k) for k in key}
new = [it for it in found if ident(it) not in old]
if any(k.get("packet") == 2 for k in key):
    raise SystemExit("packet 2 already made")
rng = random.Random(20261030)
rng.shuffle(new)
for i, it in enumerate(new):
    it.update(id=f"S{len(key) + i:03d}", packet=2)
check = rng.sample(key, 20)
packet = new + check
rng.shuffle(packet)
open(os.path.join(HERE, "packet_2.txt"), "w").write(
    "\n".join(f"### {it['id']}\n{WANTS[it['wants']]}\n{it['text']}\n" for it in packet))
json.dump(key + new, open(os.path.join(HERE, "key.json"), "w"), indent=1)
json.dump(sorted(it["id"] for it in check), open(os.path.join(HERE, "packet_2_check_ids.json"), "w"))
print(f"{len(new)} new items (S{len(key):03d}-S{len(key) + len(new) - 1:03d}) and 20 old ones in packet_2.txt")
