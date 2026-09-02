# Hard-Constraint Fuzz Benchmark

The optional deterministic Prompt IR emitter was fuzzed with **10,000** hard-constraint strings spanning `MUST`/`NEVER` style rules, punctuation, quotes, and multilingual characters.

Result for seed `20260902`: **10,000 / 10,000 literal constraints preserved in the emitted prompt**.

This validates only the deterministic emitter's serialization path. It does not prove that an LLM will obey every emitted constraint.
