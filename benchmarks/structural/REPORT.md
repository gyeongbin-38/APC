# Structural Benchmark Report — v0.1.0

## Result

The current **adaptive-compiler** architecture ranked first in the deterministic structural stress test.

| Candidate | Mean proxy score | Coverage | Overprompt | Constraint support | Avg active instruction token proxy |
|---|---:|---:|---:|---:|---:|
| adaptive-compiler | 93.53 | 0.9786 | 0.0198 | 0.9903 | 933.9 |
| typed-ir-router | 91.66 | 0.9577 | 0.0404 | 0.9806 | 960.5 |
| thin-router | 89.68 | 0.9234 | 0.0682 | 0.9649 | 805.9 |
| monolithic | 81.49 | 1.0000 | 0.6570 | 1.0000 | 1578.5 |
| specialist-pack | 74.00 | 0.6974 | 0.0520 | 0.8152 | 453.2 |

## Conditions

1,000 synthetic task cards were generated across ten conditions:

- simple one-shot
- prompt rewrite/compression
- creative/media prompt
- structured general work
- coding
- research
- long-running coding
- long-running research
- handoff
- constraint-heavy

Each architecture was evaluated over 100 seeded routing-noise runs.

## What the score means

It is a **structural architecture proxy**, not model accuracy. The score weights:

- required module coverage;
- irrelevant module loading;
- active instruction payload;
- hard-constraint support;
- multi-module composition robustness.

The routing noise values are simulation parameters, not measured ChatGPT router error rates.

## Token metric

`UTF-8 character count / 4` is used only as a stable relative payload proxy. It is not a tokenizer and must not be presented as provider billing.

## Interpretation

### Monolithic

Perfect rule coverage, but a large irrelevant-context tax. It performs better on complex long tasks than on simple tasks, which is exactly why it should not be the universal default.

### Specialist pack

Cheap when it selects the right narrow workflow. It breaks down on mixed tasks such as long coding handoffs that require several concerns at once. Real Agent Skills routers may perform better or worse; the public trigger suite exists to measure that separately.

### Thin router

Good efficiency but more fragile when multiple concerns are active.

### Typed IR router

Better composition and constraint retention at moderate overhead.

### Adaptive compiler

Best balance in this structural benchmark: one discoverable skill, compact IR, conditional references, and explicit handling for constraints and long-task composition.

## Required next evidence

Before claiming a real task-success improvement, run `evals/evals.json` in clean contexts:

1. without the skill;
2. with the skill;
3. ideally across multiple models/surfaces;
4. record provider-reported input/output/cache tokens separately from local estimates;
5. grade assertions blind to the arm when possible.
