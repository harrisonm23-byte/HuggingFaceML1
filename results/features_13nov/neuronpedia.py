"""Neuronpedia's label and top-activating examples for a list of Gemma Scope 2 features (gemma-3-12b-it, res 16k).

    python neuronpedia.py <out.json> <layer:feature> [<layer:feature> ...]

Label = Neuronpedia's automatic explanation, if it has one (otherwise None: no label is guessed). Examples = the three
highest-activating stored examples, as the text around the peak token (the peak token in [[ ]])."""
import json, os, sys, time, urllib.request

OUT, WANT = sys.argv[1], sys.argv[2:]
have = json.load(open(OUT)) if os.path.exists(OUT) else {}
URL = "https://www.neuronpedia.org/api/feature/gemma-3-12b-it/{}-gemmascope-2-res-16k/{}"


def clean(t):
    return t.replace("\n", " ").replace("<start_of_turn>", "").replace("<end_of_turn>", "").replace("<bos>", "")


for key in WANT:
    if key in have:
        continue
    L, f = key.split(":")
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL.format(L, f), headers={"User-Agent": "research-script"})
            d = json.load(urllib.request.urlopen(req, timeout=90))
            break
        except Exception as e:
            print(key, "retry", e, flush=True)
            time.sleep(5)
    else:
        have[key] = {"error": "not fetched"}
        continue
    ex = []
    for a in sorted(d.get("activations", []), key=lambda a: -a.get("maxValue", 0))[:3]:
        t, i = a["tokens"], a.get("maxValueTokenIndex", 0)
        ex.append({"max": round(a["maxValue"], 1),
                   "text": clean("".join(t[max(0, i - 15):i]) + "[[" + t[i] + "]]" + "".join(t[i + 1:i + 6])).strip()})
    labels = [e.get("description") for e in d.get("explanations", []) if e.get("description")]
    have[key] = {"label": labels[0] if labels else None, "all_labels": labels, "frac_nonzero": d.get("frac_nonzero"),
                 "examples": ex, "url": f"https://www.neuronpedia.org/gemma-3-12b-it/{L}-gemmascope-2-res-16k/{f}"}
    print(key, have[key]["label"], flush=True)
    json.dump(have, open(OUT, "w"), indent=1)
