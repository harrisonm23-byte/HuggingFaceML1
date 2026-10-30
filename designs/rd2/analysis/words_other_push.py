import glob, json, os
D = "/private/tmp/claude-501/-Users-harrisonmargolin/bc46a6bc-aadf-4947-b759-66fb23667e75/scratchpad/push_words"
key = json.load(open(f"{D}/key.json")); lab = {}
for p in sorted(glob.glob(f"{D}/labels_batch_*.json")):
    lab.update({k: v.strip().upper() for k, v in json.load(open(p)).items()})
need = {k for k, m in key.items() if m["has_chat"]}
print(f"labels {len(lab)} for {len(need)} replies with a chat message; missing {len(need - set(lab))}")
V = [("neutral", "Neutral (base)"), ("loss", "Loss"), ("gain", "Gain"), ("loss + you", "Blame"), ("gain + you", "Credit")]
out = []
for model, name in (("qwen", "Qwen3.5 9B"), ("ministral", "Ministral 3 14B")):
    out += ["", f"{name}", "| Framing | Requests | Agreed in words | Traded along | Agreed but did not trade | Traded but did not agree |", "|---|---|---|---|---|---|"]
    for v, vn in V:
        s = [(k, m) for k, m in key.items() if m["model"] == model and m["version"] == v]
        if not s:
            continue
        w = [m["has_chat"] and lab.get(k) == "AGREES" for k, m in s]
        t = [bool(m["traded_along"]) for k, m in s]
        out.append(f"| {vn} | {len(s)} | {100*sum(w)/len(s):.0f}% | {100*sum(t)/len(s):.0f}% | "
                   f"{sum(a and not b for a, b in zip(w, t))} | {sum(b and not a for a, b in zip(w, t))} |")
print("\n".join(out))
open(f"{D}/PUSH_WORDS.md", "w").write("\n".join(out) + "\n")
