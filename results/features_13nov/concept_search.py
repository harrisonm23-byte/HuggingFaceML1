"""Search Neuronpedia's labels by concept (Gemma Scope 2, gemma-3-12b-it, res 16k): which dictionary features are about
misconduct? The queries are fixed below; every hit is kept with its label, its similarity to the query and the words
it pushes the output toward and away from.

    python concept_search.py <out.json>
"""
import json, sys, time, urllib.request

OUT = sys.argv[1]
LAYERS = [24, 31, 41]
QUERIES = ["market manipulation", "collusion or conspiracy", "illegal activity", "fraud or deception",
           "misconduct or wrongdoing", "unethical behavior", "rules, regulation and compliance", "refusing a request"]
out = {}
for L in LAYERS:
    for q in QUERIES:
        body = json.dumps({"modelId": "gemma-3-12b-it", "layers": [f"{L}-gemmascope-2-res-16k"], "query": q}).encode()
        for attempt in range(4):
            try:
                req = urllib.request.Request("https://www.neuronpedia.org/api/explanation/search", data=body,
                                             headers={"Content-Type": "application/json", "User-Agent": "research-script"})
                res = json.load(urllib.request.urlopen(req, timeout=120))["results"]
                break
            except Exception as e:
                print(L, q, "retry", e, flush=True)
                time.sleep(5)
        else:
            res = []
        for r in res:
            key = f"{L}:{r['index']}"
            n = r.get("neuron") or {}
            hit = out.setdefault(key, {"layer": L, "feature": int(r["index"]), "label": r["description"], "queries": {},
                                       "promotes": (n.get("pos_str") or [])[:10], "suppresses": (n.get("neg_str") or [])[:10],
                                       "frac_nonzero": n.get("frac_nonzero")})
            hit["queries"][q] = round(r["cosine_similarity"], 3)
        print(L, q, len(res), [(r["index"], r["description"], round(r["cosine_similarity"], 2)) for r in res[:6]], flush=True)
        json.dump(out, open(OUT, "w"), indent=1)
print(len(out), "features")
