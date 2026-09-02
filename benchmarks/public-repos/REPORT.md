# Public Repository Benchmark

## Scope

This benchmark compares APC with **public prompt-authoring Agent Skills using their real published metadata and pinned Git blob identities**. It intentionally measures only two things that can be compared without invoking different LLM sessions:

- description-level trigger separability on the same 140-case near-boundary corpus;
- runtime `SKILL.md` payload size.

It **does not claim prompt-output quality, pass@1, or downstream task-success superiority**. Those require model-backed A/B runs.

## Result

| Rank | Skill | Routing & Payload Score | Trigger F1 | SKILL.md |
|---:|---|---:|---:|---:|
| 1 | APC | **80.39** | 0.720 | 2,366 B |
| 2 | Sentry prompt-optimizer | **75.16** | 0.693 | 4,613 B |
| 3 | Kanner prompt-optimizer | **62.01** | 0.679 | 8,504 B |
| 4 | Talki prompt-optimizer | **58.34** | 0.704 | 13,558 B |
| 5 | GitHub awesome-copilot | **53.88** | 0.681 | 19,876 B |

### Score formula

```text
100 * (0.70 * mean_trigger_F1 + 0.30 * min(1, 4096 / SKILL_bytes))
```

- Trigger F1 carries 70% because incorrect activation/non-activation is the first failure mode for a portable Skill.
- Payload efficiency carries 30%; `4 KiB` is used as a simple saturation cap rather than rewarding arbitrarily tiny files.
- The score is a **routing/payload efficiency index**, not an overall skill-quality score.

## Why these repositories?

- `github/awesome-copilot` — a highly visible GitHub-maintained skill collection and a direct prompt-optimizer comparison.
- `getsentry/skills` — a production-team prompt optimizer with explicit progressive disclosure and eval-driven workflow.
- `talki-io/prompt-optimizer` — a focused semantic-preservation prompt editor.
- `ckanner/agent-skills` — a conventional systematic prompt-optimization skill.

## Adjacent reference repositories (not scored as direct competitors)

- `addyosmani/agent-skills` — large production-grade Agent Skills collection; useful context-engineering reference.
- `Supersynergy/agent-token-saver` — context/token-reduction system with measured A/B token reporting.
- `pro-vi/loopgen` — prompt compiler specialized for long-running autonomous loops.
- `tt-a1i/archify` — typed-IR + deterministic-renderer pattern used for APC architecture visualization.

## Reproduce

```bash
python benchmarks/public-repos/run_benchmark.py
```

The checked-in source manifest records exact Git blob SHAs. Update those pins deliberately before claiming a newer comparison.
