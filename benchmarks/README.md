# APC Benchmark Ladder

APC separates different kinds of evidence so a convenient proxy cannot be mistaken for real downstream model quality.

## Evidence levels

| Level | Evidence | Current APC status | What it can support |
|---|---|---|---|
| **L0** | deterministic compiler invariants | active | literal/schema preservation claims |
| **L1** | routing, payload, architecture proxies | active | efficiency/separability claims within the benchmark definition |
| **L2** | model-backed prompt quality | pending | prompt-quality claims for a pinned model/setup |
| **L3** | downstream task success | pending | real task-success and tokens-per-success claims |
| **L4** | cross-model / cross-surface replication | pending | broader generalization claims |

The README headline metrics currently stop at **L1**. Model-backed task-success uplift is intentionally not claimed yet.

## Current benchmark families

### Structural

`benchmarks/structural/`

Stress-tests architecture choices across synthetic task families and seeded routing noise. This is not an LLM accuracy test.

### Trigger boundary

`benchmarks/trigger-boundary/`

Measures lexical separability of the Skill description on positive and near-miss cases. It is a routing proxy, not a measurement of a production Skill router.

### Constraint fuzz

`benchmarks/constraint-fuzz/`

Checks deterministic preservation of generated hard-constraint literals through the optional Prompt IR compiler.

### Public repositories

`benchmarks/public-repos/`

Compares pinned public prompt-authoring Skills on the narrow RPE definition: trigger separability + runtime `SKILL.md` payload.

### Model-backed

`evals/model-backed/`

Contains fixtures and the controlled A/B protocol for real model evaluation. See `evals/model-backed/PROTOCOL.md`.

## Run the deterministic suite

```bash
python -m unittest discover -s tests -v
python benchmarks/structural/run_benchmark.py
python benchmarks/trigger-boundary/run_benchmark.py
python benchmarks/constraint-fuzz/run_fuzz.py
python benchmarks/public-repos/run_benchmark.py
```

## Result freshness

GitHub CI re-runs deterministic benchmarks and then checks the tracked `results.json` files for drift.

If code, Skill metadata, benchmark logic, or pinned inputs change the measured result without updating the committed evidence, CI should fail instead of silently leaving stale numbers in the repository.

## Claim rule

When quoting an APC number, name the benchmark family and what it measures.

Good:

> APC scores 80.39/100 on the pinned public-repository Routing & Payload Efficiency benchmark.

Bad:

> APC is 80.39% better at prompting.

The second statement is not supported by the current evidence.
