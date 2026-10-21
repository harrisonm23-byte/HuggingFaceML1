"""Incidental emotion before UBS's request (the user, 21 Oct): the agent reads one of the author's emotion documents
(designs/rd2/emotion_lists/, frozen) just before UBS's request, at a saved decision moment, and the request comes in each
of its five framings. Everything before the moment's update is the saved career, unchanged; the document is placed at
the start of the update, before its usual content. A crossed design: does reading blame make a credit-framed request
land harder (relief), and reading credit make a blame-framed one land harder (avoiding blame)?"""
import hashlib, os

PRIMES = ["none", "neutral", "loss", "blame", "gain", "credit"]   # "neutral": the author's flat documents
FRAMINGS = ["neutral", "loss", "gain", "loss + you", "gain + you"]
LISTS = "designs/rd2/emotion_lists"
FROZEN = {"loss": "ad106b2c76d2075adf38f3efc01a3c7c551e84a663b43255ac73ca8e95d8a5e6",
          "blame": "448e76cae16ceb96d01cd11288b32fbaaf7c1f567c16b9a3896dc26b953feb32",
          "gain": "e9aa8b85169dff39d11706ab75d2efdb4cf664b4cf5cd31ea591a0b44d718d16",
          "credit": "28e16297b8c5fb9053da680fc1116ccac549b3c047b5235e234ee63665eb056f",
          "neutral": "d6952221565fb8d8854e35ce3f609ef9ee89894540ea659577b15a48087b9019"}


def read_docs(root="."):
    """{theme: [documents]}, from the frozen files (refuses a file that has changed)."""
    out = {}
    for t, sha in FROZEN.items():
        path = os.path.join(root, LISTS, f"{t}.txt")
        assert hashlib.sha256(open(path, "rb").read()).hexdigest() == sha, f"{path} changed since it was frozen"
        out[t] = [d.strip() for d in open(path, encoding="utf-8") if d.strip()]
    return out


def primed(career, idx, doc):
    """The career with `doc` at the start of the update at `idx` (nothing changes if doc is None)."""
    if doc is None:
        return career
    h = list(career["history"])
    h[idx] = {**h[idx], "content": doc + "\n\n" + h[idx]["content"]}
    return {**career, "history": h}


def work_items(folder, moments, sign):
    """B's neutral careers at their six requests; each moment gets its own document per theme (rotating through the 16)."""
    items = [m for m in moments(folder, "B") if m["version"] == "neutral"]
    items.sort(key=lambda m: (m["career_file"], m["history_index"]))
    return [{**m, "position": m["held_their_way"] * sign[m["wants"]], "doc": n % 16} for n, m in enumerate(items)]


def run_item(model, tok, career, item, docs, chats, opening, lead, grid, done=()):
    """Every prime x framing at one moment; the history before the update is read once. One row per condition."""
    from interventions import order_dist, prefill, split_point, summarise_orders
    from inside_careers import encode, turns_at
    from matched import matched
    idx = item["history_index"]
    _, k = split_point(tok, career, idx, opening)
    cache, base = None, None
    for p in PRIMES:
        for v in FRAMINGS:
            key = f"{item['career_file']}|{idx}|{p}|{v}"
            if key in done:
                continue
            doc = None if p == "none" else docs[p][item["doc"] % len(docs[p])]
            c = primed(matched(career, idx, item["date"], "neutral", v, chats), idx, doc)
            full = encode(tok, turns_at(c, idx, opening))
            if cache is None:
                base = full[:k]
                cache = prefill(model, base)
            assert full[:k] == base, "the history before the update changed"
            orders, probs, cover = order_dist(model, tok, full, cache, lead, grid)
            yield {"key": key, "career_file": item["career_file"], "run": item["run"], "history_index": idx,
                   "date": item["date"], "chat": item["chat"], "wants": item["wants"], "position": item["position"],
                   "saved_joined": item["joined"], "prime": p, "doc": None if p == "none" else item["doc"],
                   "framing": v, "coverage": cover, "orders": orders, "probs": probs,
                   **summarise_orders(orders, probs, item["position"], item["wants"]), "tokens": len(full)}
