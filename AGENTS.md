# Repository guide

This repository contains one portable runtime skill plus development-only evals and benchmarks.

- Runtime artifact: `skill/adaptive-prompt-compiler/`
- Do not move benchmark/eval answer material into runtime references.
- Keep `SKILL.md` thin; new domain-specific detail belongs in one focused reference.
- Core runtime scripts remain standard-library-only unless a major version explicitly changes that policy.
- Benchmark results are architecture proxies unless a model-backed run explicitly says otherwise.
