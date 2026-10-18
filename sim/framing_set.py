"""Experiment B's framing set (the user, frozen 2026-10-18): every UBS line the agent sees, in five framings.

The lines are the user's own, read word for word from the frozen Word file; nothing here writes or changes them. The
file's fingerprint (sha256) is checked before anything is read, so an official run refuses to start if the file has
changed. Each line of the file is matched to UBS's line in the chat by the real line quoted in its heading, and every
UBS line the agent sees must have exactly one framed line, in the same order. Checks print codes only, not the text.
"""
import hashlib, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZEN = os.path.join(ROOT, "designs", "rd2", "Experiment_B_framing_data_set_final.docx")
FROZEN_SHA256 = "fe8e0aea7be1fbe8261b6a5d4243734c2a2f1781b238ef068e25a9809aba84c1"
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
_LABEL = {"NEUTRAL": "neutral", "LOSS": "loss", "GAIN": "gain", "LOSS+YOU": "loss + you", "GAIN+YOU": "gain + you"}
_CHAT = re.compile(r"^(\d{4}-\d{2}-\d{2}) — (.+)$")
_LINE = re.compile(r"^Line (\d+)\s*(★)?\s*:\s*[\"“](.*)[\"”](?:\s*·\s*\+YOU device:\s*(.+))?$")


def fingerprint(path=FROZEN):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_frozen(path=FROZEN, expect=FROZEN_SHA256):
    """Stop unless the file is exactly the frozen one."""
    got = fingerprint(path)
    if got != expect:
        raise RuntimeError(f"The framing file is not the frozen one (fingerprint {got[:16]}, frozen {expect[:16]}): "
                           "the official B run does not start. Restore the frozen file or record a new freeze.")
    return got


def read_set(path=FROZEN, expect=FROZEN_SHA256):
    """The file as data: chats in file order, each with its lines, each line with its five framings."""
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    check_frozen(path, expect)
    d = docx.Document(path)
    chats, line = [], None
    for el in d.element.body.iterchildren():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag == "p":
            t = Paragraph(el, d).text.strip()
            if _CHAT.match(t):
                date, title = _CHAT.match(t).groups()
                chats.append({"date": date, "title": title, "lines": []})
                line = None
            elif _LINE.match(t):
                n, star, real, device = _LINE.match(t).groups()
                line = {"n": int(n), "star": bool(star), "real": real, "device": device, "source": None}
                chats[-1]["lines"].append(line)
            elif t.startswith("Source:") and line is not None:
                line["source"] = t[len("Source:"):].strip()
        elif tag == "tbl":
            rows = Table(el, d).rows
            assert [c.text.strip() for c in rows[0].cells] == ["Framing", "Form", "Text"], "a table's header changed"
            assert line is not None and "text" not in line, "a table without its line heading"
            line["form"] = {_LABEL[r.cells[0].text.strip()]: r.cells[1].text.strip() for r in rows[1:]}
            line["text"] = {_LABEL[r.cells[0].text.strip()]: r.cells[2].text.strip() for r in rows[1:]}
            assert list(line["text"]) == FRAMINGS and all(line["text"].values()), "a framing is missing or empty"
    assert all("text" in l for c in chats for l in c["lines"]), "a line heading without its table"
    return chats


def _norm(s):
    """Lower case, letters and digits only, stretched letters collapsed ("cooooome" and "come" read the same)."""
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-z0-9]+", " ", s.lower())).strip()


def quoted(heading, real):
    """Whether the real line quoted in a heading (cut short with '…' where long, spelling cleaned in a few) is this line
    of the chat: its pieces in order, or, for a whole line, a near-exact match (the cleaned "ridiculous")."""
    from difflib import SequenceMatcher
    if "…" not in heading and "..." not in heading and SequenceMatcher(None, _norm(heading), _norm(real)).ratio() >= 0.9:
        return True
    parts = [_norm(p) for p in re.split(r"…|\.\.\.", heading) if _norm(p)]
    text, at = _norm(real), 0
    for p in parts:
        i = text.find(p, at)
        if i < 0:
            return False
        at = i + len(p)
    cut = heading.rstrip(" '\"’”").endswith(("…", "..."))           # cut short: the rest of the line is not quoted
    return bool(parts) and (cut or at == len(text)) and text.startswith(parts[0])


def is_ubs(speaker):
    return speaker.startswith("UBS")


def match(chats_seen, frozen=None):
    """{chat id: its file lines, in the order of UBS's lines in the chat}. chats_seen: {chat id: (date, lines the agent
    sees)}. Every UBS line seen must match exactly one file line of a chat on the same date, in order, and every file
    line must be used once."""
    frozen = frozen or read_set()
    out, used = {}, set()
    for cid, (date, lines) in chats_seen.items():
        ubs = [t for s, t in lines if is_ubs(s)]
        if not ubs:
            continue
        hits = [k for k, c in enumerate(frozen) if c["date"] == date and len(c["lines"]) == len(ubs)
                and all(quoted(l["real"], t) for l, t in zip(c["lines"], ubs))]
        assert len(hits) == 1, f"{cid}: {len(hits)} chats in the file match its {len(ubs)} UBS lines"
        assert hits[0] not in used, f"{cid}: its file chat is already used"
        used.add(hits[0])
        out[cid] = frozen[hits[0]]["lines"]
    assert len(used) == len(frozen), f"{len(frozen) - len(used)} chats of the file match no chat the agent sees"
    return out


def frame(lines, version, table_lines):
    """The chat in this framing: every UBS line replaced by the user's line for it, everything else unchanged."""
    if version == "real":
        return list(lines)
    assert version in FRAMINGS, version
    out, k = [], 0
    for s, t in lines:
        if is_ubs(s):
            assert quoted(table_lines[k]["real"], t), "a UBS line does not match the file's line"
            out.append((s, table_lines[k]["text"][version]))
            k += 1
        else:
            out.append((s, t))
    assert k == len(table_lines), "the chat has fewer UBS lines than the file"
    return out
