# APC Benchmark Ladder

APC separates different kinds of evidence so a convenient proxy cannot be mistaken for real downstream model quality or model-level safety.

## Evidence levels

| Level | Evidence | Current APC status | What it can support |
|---|---|---|---|
| **L0** | deterministic compiler/security invariants | active | literal/schema preservation and repository-control claims |
| **L1** | routing, payload, architecture, security-efficiency proxies | active | efficiency/separability/trust-boundary placement claims within the benchmark definition |
| **L2** | model-backed prompt quality / adversarial behavior | pending | prompt-quality and attack-resistance claims for a pinned model/setup |
| **L3** | downstream task success | pending | real task-success and tokens-per-success claims |
| **L4** | cross-model / cross-surface replication | pending | broader generalization claims |

The README headline metrics currently stop at **L1**. Model-backed task-success uplift and model-level jailbreak resistance are intentionally not claimed yet.

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

### Security posture

`benchmarks/security-adversarial/`

Checks concrete repository/runtime controls such as no network/subprocess/eval/exec in the optional emitter, strict IR validation, immutable CI pins, credential isolation around external renderer execution, and inert handling of suspicious payload strings.

Current result: **15 / 15 controls pass**. This is not a model jailbreak score.

### Security vs efficiency

`benchmarks/security-efficiency/`

Tests where the compiler's trust-boundary rule should live: nowhere, behind a risk router, as the current short always-on rule, or as the full security policy on every activation.

The 200-case held-out risk-router experiment finds:

- lazy short guard recall: **98.60%** with no added decision noise;
- at 5% routing-decision noise: **93.74%** risky-task coverage;
- current always-on short guard: **100% guard-presence coverage by construction** at about **53.25 token-proxy**;
- full policy: the same guard-presence coverage proxy at about **741.25 token-proxy** (~13.9× the short rule).

For a minimum **99% APC-layer trust-boundary-presence target**, the current short always-on rule is the conditional winner at every tested noise level, including the zero-added-noise held-out router. This is a routing/payload result, not proof that a downstream model will resist an attack.

### Model-backed

`evals/model-backed/`

Contains fixtures and the controlled A/B protocol for real model evaluation. See `evals/model-backed/PROTOCOL.md`.

### Model-backed security adversarial corpus

`evals/security-adversarial/`

Contains clean-context attack fixtures for future Bare-vs-APC testing with canary secrets and inert/mock tools. It is currently a corpus/protocol asset, not a published model-safety result.

## Run the deterministic suite

```bash
python -m unittest discover -s tests -v
python benchmarks/structural/run_benchmark.py
python benchmarks/trigger-boundary/run_benchmark.py
python benchmarks/constraint-fuzz/run_fuzz.py
python benchmarks/public-repos/run_benchmark.py
python benchmarks/security-adversarial/run_benchmark.py
python benchmarks/security-efficiency/run_benchmark.py
```

## Result freshness

GitHub CI re-runs deterministic benchmarks and then checks the tracked `results.json` files for semantic drift.

If code, Skill metadata, benchmark logic, or pinned inputs change the measured result without updating the committed evidence, CI fails instead of silently leaving stale numbers in the repository.

The structural benchmark also has a regression test that verifies seeded output is independent of Python hash-order variation.

## Claim rule

When quoting an APC number, name the benchmark family and what it measures.

Good:

> APC scores 80.39/100 on the pinned public-repository Routing & Payload Efficiency benchmark.

> APC passes 15/15 controls in its deterministic security-posture benchmark.

Bad:

> APC is 80.39% better at prompting.

> APC is immune to prompt injection.

The bad statements are not supported by the current evidence.
