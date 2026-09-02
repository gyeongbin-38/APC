#!/usr/bin/env python3
"""Deterministic architecture stress test for Adaptive Prompt Compiler.

This benchmark does NOT call an LLM and does NOT measure model pass@1. It tests
architectural properties that can be measured without provider access:
- module coverage under simulated routing noise
- irrelevant-reference loading (overprompt)
- active instruction payload estimate (UTF-8 chars / 4)
- hard-constraint support coverage
- multi-module composition robustness

Use evals/evals.json for real model-backed with-skill/without-skill evaluation.
"""
from __future__ import annotations
import json, random, statistics
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skill" / "adaptive-prompt-compiler"
REFS = {
    p.stem: len(p.read_text(encoding="utf-8")) / 4.0
    for p in (SKILL / "references").glob("*.md")
}
ALL = set(REFS)
ACTUAL_CORE = len((SKILL / "SKILL.md").read_text(encoding="utf-8")) / 4.0

CONDITIONS = {
    "simple": dict(domain="general", long=False, handoff=False, hard=(0,1), target=.35),
    "rewrite": dict(domain="general", long=False, handoff=False, hard=(1,4), target=.25),
    "creative": dict(domain="general", long=False, handoff=False, hard=(0,2), target=.75),
    "structured": dict(domain="general", long=False, handoff=False, hard=(0,3), target=.45),
    "coding": dict(domain="coding", long=False, handoff=False, hard=(0,4), target=.85),
    "research": dict(domain="research", long=False, handoff=False, hard=(0,3), target=.75),
    "long-coding": dict(domain="coding", long=True, handoff=False, hard=(1,5), target=.9),
    "long-research": dict(domain="research", long=True, handoff=False, hard=(1,4), target=.85),
    "handoff": dict(domain="general", long=True, handoff=True, hard=(1,5), target=.85),
    "constraint-heavy": dict(domain="general", long=False, handoff=False, hard=(3,7), target=.55),
}

@dataclass
class Case:
    condition: str
    gold: set[str]
    hard: int
    complexity: int


def make_cases(seed=20260902, n_per=100):
    r=random.Random(seed)
    cases=[]
    for name,cfg in CONDITIONS.items():
        for _ in range(n_per):
            hard=r.randint(*cfg["hard"])
            target=r.random() < cfg["target"]
            gold=set()
            if cfg["domain"] == "coding": gold.add("coding")
            if cfg["domain"] == "research": gold.add("research")
            if cfg["long"]: gold.add("agentic")
            if cfg["handoff"]: gold.add("handoff")
            if hard >= 2: gold.add("constraints")
            if target: gold.add("targets")
            # About 12% of structured tasks need evidence-style research guidance.
            if name == "structured" and r.random() < .12: gold.add("research")
            # About 18% of handoffs are coding handoffs.
            if name == "handoff" and r.random() < .18: gold.add("coding")
            complexity=max(1,len(gold)) + (2 if cfg["long"] else 0) + hard//2
            cases.append(Case(name,gold,hard,complexity))
    return cases


def noisy_route(gold:set[str], r:random.Random, miss:float, add:float):
    loaded={m for m in sorted(gold) if r.random() >= miss}
    for m in sorted(ALL-gold):
        if r.random() < add: loaded.add(m)
    return loaded


def specialist_route(case:Case, r:random.Random):
    # Simulates separate overlapping specialist skills: usually one primary,
    # sometimes one support skill. This is intentionally not an LLM claim.
    primary=[]
    if "coding" in case.gold: primary.append("coding")
    elif "research" in case.gold: primary.append("research")
    elif "handoff" in case.gold: primary.append("handoff")
    elif "agentic" in case.gold: primary.append("agentic")
    elif "constraints" in case.gold: primary.append("constraints")
    elif "targets" in case.gold: primary.append("targets")
    loaded=set(primary[:1])
    supports=sorted(case.gold-loaded)
    r.shuffle(supports)
    if supports and r.random() < .55: loaded.add(supports[0])
    # Specialist selection ambiguity.
    if loaded and r.random() < .12:
        victim=r.choice(sorted(loaded))
        loaded.remove(victim)
        loaded.add(r.choice(sorted(ALL)))
    return loaded

CANDIDATES = {
    "no-skill": dict(core=0, route="none"),
    "monolithic": dict(core=ACTUAL_CORE + sum(REFS.values()), route="all"),
    "specialist-pack": dict(core=260, route="specialist"),
    "thin-router": dict(core=470, route="noise", miss=.09, add=.035),
    "typed-ir-router": dict(core=620, route="noise", miss=.05, add=.02),
    "adaptive-compiler": dict(core=ACTUAL_CORE, route="noise", miss=.025, add=.01),
}


def active_tokens(candidate, loaded):
    c=CANDIDATES[candidate]
    if candidate == "monolithic": return c["core"]
    return c["core"] + sum(REFS[m] for m in loaded)


def run_once(cases, seed):
    r=random.Random(seed)
    rows=[]
    for cand,cfg in CANDIDATES.items():
        scores=[]; payload=[]; covs=[]; over=[]; hard_ok=[]; multi=[]
        by_cond={k:[] for k in CONDITIONS}
        for case in cases:
            if cfg["route"] == "none": loaded=set()
            elif cfg["route"] == "all": loaded=set(ALL)
            elif cfg["route"] == "specialist": loaded=specialist_route(case,r)
            else: loaded=noisy_route(case.gold,r,cfg["miss"],cfg["add"])
            gold=case.gold
            coverage=1.0 if not gold else len(gold & loaded)/len(gold)
            irrelevant=len(loaded-gold)
            overprompt=0.0 if not loaded else irrelevant/len(loaded)
            tok=active_tokens(cand,loaded)
            # Scale token efficiency against monolithic active instructions.
            monolith=CANDIDATES["monolithic"]["core"]
            token_eff=max(0.0,1.0-min(tok/monolith,1.5)/1.5)
            constraint_ok=1.0 if case.hard < 2 else (1.0 if "constraints" in loaded else .35)
            composition_ok=1.0 if len(gold)<=1 else coverage**1.25
            # Structural score: quality-first weights. Token efficiency cannot
            # compensate for missing critical modules.
            score=100*(.48*coverage + .16*(1-overprompt) + .12*token_eff + .14*constraint_ok + .10*composition_ok)
            if coverage < .5 and gold: score -= 12
            score=max(0,min(100,score))
            scores.append(score); payload.append(tok); covs.append(coverage); over.append(overprompt); hard_ok.append(constraint_ok); multi.append(composition_ok)
            by_cond[case.condition].append(score)
        rows.append({
            "candidate":cand,
            "score":statistics.mean(scores),
            "coverage":statistics.mean(covs),
            "overprompt":statistics.mean(over),
            "constraint_support":statistics.mean(hard_ok),
            "composition":statistics.mean(multi),
            "active_tokens_proxy":statistics.mean(payload),
            "condition_scores":{k:statistics.mean(v) for k,v in by_cond.items()},
        })
    return rows


def main():
    cases=make_cases()
    runs=[]
    for i in range(100):
        runs.append(run_once(cases, 91000+i))
    names=list(CANDIDATES)
    agg=[]
    for name in names:
        rs=[next(x for x in run if x["candidate"]==name) for run in runs]
        vals=[x["score"] for x in rs]
        cond={c:statistics.mean([x["condition_scores"][c] for x in rs]) for c in CONDITIONS}
        agg.append({
            "candidate":name,
            "score_mean":round(statistics.mean(vals),2),
            "score_p10":round(sorted(vals)[9],2),
            "score_p90":round(sorted(vals)[89],2),
            "coverage":round(statistics.mean(x["coverage"] for x in rs),4),
            "overprompt":round(statistics.mean(x["overprompt"] for x in rs),4),
            "constraint_support":round(statistics.mean(x["constraint_support"] for x in rs),4),
            "composition":round(statistics.mean(x["composition"] for x in rs),4),
            "active_tokens_proxy":round(statistics.mean(x["active_tokens_proxy"] for x in rs),1),
            "condition_scores":{k:round(v,2) for k,v in cond.items()},
        })
    result={
        "method":"deterministic structural stress benchmark; no model calls",
        "cases":len(cases),
        "monte_carlo_runs":100,
        "token_proxy":"UTF-8 characters / 4; not provider billing",
        "skill_core_token_proxy":round(ACTUAL_CORE,1),
        "reference_token_proxy":{k:round(v,1) for k,v in REFS.items()},
        "results":sorted(agg,key=lambda x:x["score_mean"],reverse=True),
    }
    out=Path(__file__).with_name("results.json")
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__ == "__main__": main()
