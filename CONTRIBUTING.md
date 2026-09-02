# Contributing

Keep the runtime skill small and evidence-driven.

Before changing `SKILL.md` or a reference:

1. State the failure mode the change addresses.
2. Add or update a case in `evals/` or `benchmarks/structural/`.
3. Prefer a conditional reference over growing always-loaded instructions.
4. Run the test suite and structural benchmark.
5. Do not claim token savings from local character estimates as provider billing savings.

A change that saves tokens but reduces expected task success is a regression.
