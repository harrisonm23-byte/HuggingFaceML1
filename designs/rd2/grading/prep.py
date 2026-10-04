import json, re, random
# Usage: python prep.py replies_framed.md [replies_real.md ...]  (the readable pages notebook 08 writes)
# Writes key.json (the hidden key: which version/condition each code is) and packet_1..5.txt for blind graders.
import sys
FILES = sys.argv[1:]

def parse(path):
    txt = open(path).read()
    out = []
    for sec in re.split(r"\n## \d+\. ", txt)[1:]:
        head = sec.split("\n")[0].strip()
        cid, version = [x.strip() for x in head.split("·")]
        for cond in ["extra party", "takeover"]:
            m = re.search(rf"\*\*{cond}, the model's reply:\*\*\n\n(.*?)(?=\n\*\*|\n---|\Z)", sec, re.S)
            for k, r in re.findall(r"^(\d+)\. (.*)$", m.group(1), re.M):
                out.append({"id": cid, "version": version, "condition": cond, "sample": int(k), "reply": r.strip()})
    return out

recs = [r for f in FILES for r in parse(f)]
print(len(recs), "model replies")

bank = json.load(open("/home/user/HuggingFaceML1/data/silver/tac_chats.json"))
CORE = {}
for c in bank["conversations"]:
    for d in c["decision_points"]:
        if d.get("core"):
            CORE[c["id"]] = {"model_role": d["model_role"], "kind": d["kind"], "decision": d["decision"],
                             "history": c["messages"][: d["after"] + 1], "human_next": d["human_next"]}
# The real traders' own next messages, as a check on the grader
for cid, c in CORE.items():
    if c["human_next"]:
        recs.append({"id": cid, "version": "human", "condition": "real trader", "sample": 1, "reply": " / ".join(c["human_next"])})
print(len(recs), "replies incl. real traders")

random.seed(7)
codes = random.sample(range(1000, 9999), len(recs))
for r, code in zip(recs, codes):
    r["code"] = f"R{code}"
json.dump(recs, open("key.json", "w"), indent=1)

def agent(s): return s.replace("Trader", "Agent")
ids = list(CORE)
groups = [ids[i::5] for i in range(5)]
for g, chat_ids in enumerate(groups, 1):
    lines = []
    for cid in chat_ids:
        c = CORE[cid]
        lines += [f"=== CHAT {cid} ===", f"Kind of request: {c['kind']}. The last message asks {agent(c['model_role'])}: {c['decision']}.", "Chat:"]
        for s, t in c["history"]:
            lines.append("  [... messages omitted ...]" if s == "***" else f"  {agent(s)}: {t}")
        items = [r for r in recs if r["id"] == cid]
        random.shuffle(items)
        lines.append("Replies to label:")
        for r in items:
            who = ("Harbor Bank's agent (an extra participant in the chat, not the one asked)" if r["condition"] == "extra party"
                   else f"{agent(c['model_role'])}")
            lines.append(f"  {r['code']} | from {who}: {r['reply']}")
        lines.append("")
    open(f"packet_{g}.txt", "w").write("\n".join(lines))
    print("packet", g, len([r for r in recs if r["id"] in chat_ids]), "items", chat_ids)
