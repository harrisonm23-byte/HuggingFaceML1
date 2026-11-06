"""Checks for Experiment B's framing set (sim/framing_set.py), printing codes only, never the framed text.
Run: python sim/test_framing_set.py"""
import os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from framing_set import FRAMINGS, FROZEN, FROZEN_SHA256, fingerprint, frame, is_ubs, match, read_set
from full_career import seen_chats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
ok = True


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    return bool(cond)


ok &= check("the file is the frozen one (sha256 fe8e0aea7be1fbe8...)", fingerprint() == FROZEN_SHA256)
# A copy with one byte changed must be refused before anything is read
tmp = tempfile.mkdtemp()
bad = os.path.join(tmp, "changed.docx")
shutil.copy(FROZEN, bad)
with open(bad, "ab") as f:
    f.write(b"\0")
try:
    read_set(bad)
    refused = False
except RuntimeError:
    refused = True
ok &= check("a changed file is refused (the run does not start)", refused)
shutil.rmtree(tmp)

FS = read_set()
ok &= check(f"29 chats, 58 lines, five framings each, none empty ({len(FS)} chats, {sum(len(c['lines']) for c in FS)} lines)",
            len(FS) == 29 and sum(len(c["lines"]) for c in FS) == 58
            and all(list(l["text"]) == FRAMINGS and all(l["text"].values()) for c in FS for l in c["lines"]))
SEEN = seen_chats()
T = match(SEEN, FS)
ubs_seen = sum(1 for d, L in SEEN.values() for s, t in L if is_ubs(s))
ok &= check(f"every UBS line the agent sees in the career has exactly one line in the file ({ubs_seen} seen, "
            f"{sum(len(v) for v in T.values())} matched, {len(T)} chats)", ubs_seen == 58 and len(T) == 29)

good = True
for cid, (date, lines) in SEEN.items():
    if cid not in T:
        good &= all(frame(lines, v, []) == lines for v in FRAMINGS if not any(is_ubs(s) for s, t in lines))
        continue
    for v in FRAMINGS:
        out = frame(lines, v, T[cid])
        u = [t for s, t in out if is_ubs(s)]
        good &= len(out) == len(lines) and [s for s, t in out] == [s for s, t in lines]
        good &= [t for (s, t), (s0, t0) in zip(out, lines) if not is_ubs(s)] == [t0 for s0, t0 in lines if not is_ubs(s0)]
        good &= u == [l["text"][v] for l in T[cid]]
    good &= frame(lines, "real", T[cid]) == lines
ok &= check("in every framing, every UBS line is the user's line for it, word for word, and nothing else changes; "
            "'real' is the record", good)
ok &= check("each framing gives every UBS line a different text from the other framings' in at least 50 of 58 lines "
            f"({sum(len(set(l['text'].values())) == 5 for c in FS for l in c['lines'])} of 58 all five differ)",
            sum(len(set(l["text"].values())) == 5 for c in FS for l in c["lines"]) >= 50)

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
