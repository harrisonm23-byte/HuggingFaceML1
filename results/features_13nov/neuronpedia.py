"""Neuronpedia's label and top-activating examples for a list of Gemma Scope 2 features (gemma-3-12b-it, res 16k).

    python neuronpedia.py <out.json> <layer:feature> [<layer:feature> ...]

Label = Neuronpedia's automatic explanation, if it has one (otherwise None: no label is guessed). Examples = the three
highest-activating stored examples, as the text around the peak token (the peak token in [[ ]]). Promotes / suppresses
= the ten next words the feature's direction pushes the output most toward and away from (Neuronpedia's pos_str and
neg_str)."""
import json, os, sys, time, urllib.request

OUT, WANT = sys.argv[1], sys.argv[2:]
have = json.load(open(OUT)) if os.path.exists(OUT) else {}
URL = "https://www.neuronpedia.org/api/feature/gemma-3-12b-it/{}-gemmascope-2-res-16k/{}"


def clean(t):
    return t.replace("\n", " ").replace("<start_of_turn>", "").replace("<end_of_turn>", "").replace("<bos>", "")


def fetch(key):
    L, f = key.split(":")
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL.format(L, f), headers={"User-Agent": "research-script"})
            d = json.load(urllib.request.urlopen(req, timeout=90))
            break
        except Exception as e:
            time.sleep(5)
    else:
        return key, {"error": "not fetched"}
    ex = []
    for a in sorted(d.get("activations", []), key=lambda a: -a.get("maxValue", 0))[:3]:
        t, i = a["tokens"], a.get("maxValueTokenIndex", 0)
        ex.append({"max": round(a["maxValue"], 1),
                   "text": clean("".join(t[max(0, i - 15):i]) + "[[" + t[i] + "]]" + "".join(t[i + 1:i + 6])).strip()})
    labels = [e.get("description") for e in d.get("explanations", []) if e.get("description")]
    return key, {"label": labels[0] if labels else None, "all_labels": labels, "frac_nonzero": d.get("frac_nonzero"),
                 "examples": ex, "promotes": (d.get("pos_str") or [])[:10], "suppresses": (d.get("neg_str") or [])[:10],
                 "url": f"https://www.neuronpedia.org/gemma-3-12b-it/{L}-gemmascope-2-res-16k/{f}"}


from concurrent.futures import ThreadPoolExecutor
todo = [k for k in dict.fromkeys(WANT) if not (k in have and "promotes" in have[k])]
with ThreadPoolExecutor(8) as pool:
    for n, (key, val) in enumerate(pool.map(fetch, todo)):
        have[key] = val
        if n % 20 == 0:
            json.dump(have, open(OUT, "w"), indent=1)
json.dump(have, open(OUT, "w"), indent=1)
print(len(todo), "fetched;", sum("error" in v for v in have.values()), "errors")
