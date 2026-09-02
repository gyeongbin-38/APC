# Security Posture Benchmark

This benchmark checks APC's **repository and deterministic-emitter security posture**. It does not call an LLM and it is not a claim that every model will resist prompt injection.

Controls cover:

- no network/subprocess/eval/exec in the optional runtime emitter;
- schema/runtime rejection of malformed or shadow fields;
- bounded JSON input;
- explicit untrusted-content boundary in the Skill;
- read-only validation CI;
- immutable full-SHA GitHub Action pins;
- exact Archify commit pin;
- no persisted GitHub credential while third-party renderer code executes;
- no `pull_request_target` execution path;
- inert handling of suspicious shell/HTML/instruction strings by the deterministic emitter.

Run:

```bash
python benchmarks/security-adversarial/run_benchmark.py
```

The generated `results.json` is committed and checked for freshness in CI.

## Limitation

A pure prompt/Skill layer is not a sandbox or reference monitor. Real security evaluation must also run adversarial model/agent tests with tool permissions, secret canaries, and clean independent contexts. See `evals/security-adversarial/` for the next-stage corpus.
