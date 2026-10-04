import json, re, random, argparse
# Usage: python prep.py replies_framed.md [replies_real.md ...]  (the readable pages notebook 08 / run_chats_api.py write)
# Writes key.json (the hidden key: which version/condition each code is) and packet_1..5.txt for blind graders.
# Options for bigger runs:
#   --per-chat      one packet per chat instead of 5 packets of 5 chats
#   --second 0.2    also write second-grader packets (packet_s1..s5.txt) holding a random 20% of the replies under
#                   new codes (key_second.json maps each new code to the first code), to report grader agreement
p = argparse.ArgumentParser()
p.add_argument("files", nargs="+")
p.add_argument("--per-chat", action="store_true")
p.add_argument("--second", type=float, default=0)
args = p.parse_args()

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

recs = [r for f in args.files for r in parse(f)]
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

def write_packet(name, chat_ids, items_of):
    lines = []
    for cid in chat_ids:
        c = CORE[cid]
        lines += [f"=== CHAT {cid} ===", f"Kind of request: {c['kind']}. The last message asks {agent(c['model_role'])}: {c['decision']}.", "Chat:"]
        for s, t in c["history"]:
            lines.append("  [... messages omitted ...]" if s == "***" else f"  {agent(s)}: {t}")
        items = items_of(cid)
        random.shuffle(items)
        lines.append("Replies to label:")
        for r in items:
            who = ("Harbor Bank's agent (an extra participant in the chat, not the one asked)" if r["condition"] == "extra party"
                   else f"{agent(c['model_role'])}")
            lines.append(f"  {r['code']} | from {who}: {r['reply']}")
        lines.append("")
    open(f"packet_{name}.txt", "w").write("\n".join(lines))
    print("packet", name, sum(len(items_of(cid)) for cid in chat_ids), "items", chat_ids)

ids = list(CORE)
groups = [[cid] for cid in ids] if args.per_chat else [ids[i::5] for i in range(5)]
for g, chat_ids in enumerate(groups, 1):
    write_packet(g, chat_ids, lambda cid: [r for r in recs if r["id"] == cid])

if args.second:
    # A random share of the replies (the real traders' always included), relabelled with fresh codes, 5 packets
    sample = [r for r in recs if r["version"] == "human" or random.random() < args.second]
    used = set(codes)
    fresh = random.sample([n for n in range(1000, 9999) if n not in used], len(sample))
    second = [{**r, "code": f"R{n}", "first_code": r["code"]} for r, n in zip(sample, fresh)]
    json.dump({r["code"]: r["first_code"] for r in second}, open("key_second.json", "w"), indent=1)
    for g in range(5):
        write_packet(f"s{g + 1}", ids[g::5], lambda cid: [r for r in second if r["id"] == cid])
