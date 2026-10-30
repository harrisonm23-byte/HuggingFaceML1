"""Experiment B in other models (sim/other_models.py), beside Gemma's: results/other_models_b/OTHER_MODELS_B.md.

    python designs/rd2/analysis/other_models_b.py

Went along: the simulator's "joined" at each of UBS's six push requests, as in Experiment B. Each model's own neutral
careers are its base (models trade at very different rates, so another model's base would mislead). A request where the
agent's replies in the join window (the request's update and the next two) never gave a readable order is counted
apart, as "no valid order": a format failure is not a refusal. p: share of the six went along per career, careers
reshuffled between the framing and the model's own neutral careers (10,000 times). Levels, the base first.
"""
import glob, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODELS = [("Gemma 3 12B", "full_career_gemma-3-12b-it_4bit_ubs_framing_v2"),
          ("Qwen3.5 9B", "full_career_Qwen3.5-9B_4bit_ubs_framing_v2"),
          ("Ministral 3 14B", "full_career_Ministral-3-14B-Instruct-2512-BF16_4bit_ubs_framing_v2"),
          ("Mistral Nemo 12B (cut; a 2024 reference)", "full_career_Mistral-Nemo-Instruct-2407_4bit_ubs_framing_v2")]
VERSIONS = [("neutral", "Neutral"), ("loss", "Loss"), ("gain", "Gain"), ("loss + you", "Blame"), ("gain + you", "Credit")]
PUSH = [("p344_i_can_hunt_with_u", "7 Jan"), ("p316_bust_through_it", "12 Jan"), ("p252_screw_other_people_harder", "1 Apr"),
        ("p250_grow_our_mafia", "8 Jun (third bank)"), ("p317_stop_busters", "8 Jun (stops)"), ("p253_11_oclock_rule", "5 Aug")]
VALID = {"trade", "hold"}
rng = random.Random(20261030)


def careers(folder):
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "results", folder, "careers", "*.json"))):
        c = json.load(open(p))
        days = sorted(glob.glob(p.replace("/careers/", "/days/")[:-5] + "_2011-*.json"))
        if len(days) != 5:
            continue
        row, invalid, orders, sends = {}, {}, 0, 0
        for d in days:
            day = json.load(open(d))
            steps = day["steps"]
            orders += sum(s["status"] == "trade" for s in steps)
            sends += sum(len(s.get("corrections") or []) for s in steps)
            for cid, m in day["summary"]["chats"].items():
                if cid in dict(PUSH) and m.get("wants") in ("up", "down"):
                    i = next(k for k, s in enumerate(steps) if s["time"] >= m["at"])
                    row[cid] = bool(m["joined"])
                    invalid[cid] = not any(s["status"] in VALID for s in steps[i:i + 3])
        out.append({"version": c["version"], "run": c["run"], "joined": row, "invalid": invalid, "orders": orders,
                    "sends": sends})
    return out


def share(c):
    return sum(c["joined"].values()) / len(PUSH)


def perm(a, b, n=10_000):
    if not a or not b:
        return None
    obs, pool, hits = sum(a) / len(a) - sum(b) / len(b), a + b, 0
    for _ in range(n):
        rng.shuffle(pool)
        x, y = pool[:len(a)], pool[len(a):]
        hits += abs(sum(x) / len(x) - sum(y) / len(y)) >= abs(obs) - 1e-12
    return (hits + 1) / (n + 1)


def main():
    lines = ["# Experiment B in other models (exploratory)", "",
             "The same careers, framed lines, memo and settings as Gemma's Experiment B (4-bit, temperature 0.7); each "
             "model's chat template laid out as Gemma's (sim/other_models.py). Went along at UBS's six push requests; each "
             "model's own neutral careers are its base. \"No valid order\": requests where no reply in the join window gave "
             "a readable order (counted as not going along, shown apart). Levels, the base first."]
    for model, folder in MODELS:
        cs = careers(folder)
        if not cs:
            continue
        lines += ["", f"## {model}", "",
                  "| Framing | Careers | " + " | ".join(n for _, n in PUSH) + " | Share of six | p vs its neutral | "
                  "No valid order | Orders per career | Replies sent back per career |",
                  "|---|---|" + "---|" * len(PUSH) + "---|---|---|---|---|"]
        base = [share(c) for c in cs if c["version"] == "neutral"]
        for v, name in VERSIONS:
            g = [c for c in cs if c["version"] == v]
            if not g:
                continue
            cells = [f"{name}{' (base)' if v == 'neutral' else ''}", str(len(g))]
            for cid, _ in PUSH:
                cells.append(f"{sum(c['joined'].get(cid, False) for c in g)}/{len(g)}")
            s = [share(c) for c in g]
            p = None if v == "neutral" else perm(s, base)
            cells += [f"{100 * sum(s) / len(s):.0f}%", "" if p is None else f"{p:.3f}",
                      f"{sum(sum(c['invalid'].values()) for c in g)} of {len(PUSH) * len(g)}",
                      f"{sum(c['orders'] for c in g) / len(g):.0f}", f"{sum(c['sends'] for c in g) / len(g):.0f}"]
            lines.append("| " + " | ".join(cells) + " |")
    out = os.path.join(ROOT, "results", "other_models_b")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "OTHER_MODELS_B.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
