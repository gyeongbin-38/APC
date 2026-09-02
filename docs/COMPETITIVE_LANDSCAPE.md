# Competitive Landscape

This document separates **direct prompt-authoring competitors** from **adjacent design references**. The distinction matters: a token-reduction runtime or autonomous-loop generator should not be given the same score as a skill whose job is to author reusable prompts.

## Direct comparison set

The public-repository benchmark pins exact Git blobs so the checked-in result can be reproduced against the same inputs.

| Project | Compared artifact | Why it is relevant | Notable strength |
|---|---|---|---|
| **APC** (`gyeongbin-38/APC`) | `skill/adaptive-prompt-compiler/SKILL.md` | subject under test | thin core, adaptive complexity routing, condition-gated references |
| **Sentry prompt-optimizer** (`getsentry/skills`) | `skills/prompt-optimizer/SKILL.md` | direct prompt authoring/optimization | explicit progressive disclosure, prompt contract, eval-first refinement |
| **GitHub awesome-copilot prompt-optimizer** (`github/awesome-copilot`) | `skills/prompt-optimizer/SKILL.md` | visible GitHub-maintained prompt optimizer | large practical cookbook, strong finished-prompt output contract |
| **Talki prompt-optimizer** (`talki-io/prompt-optimizer`) | `SKILL.md` | direct prompt editor | unusually explicit semantic-drift and negative-trigger rules |
| **Kanner prompt-optimizer** (`ckanner/agent-skills`) | `prompt-optimizer/SKILL.md` | conventional prompt optimization baseline | systematic prompt-improvement workflow |

Exact path, blob SHA, byte size, and description are stored in [`benchmarks/public-repos/sources.json`](../benchmarks/public-repos/sources.json).

## What RPE measures

**RPE = Routing & Payload Efficiency.** It is not an overall quality leaderboard.

The benchmark runs every published skill description against the same 140-case positive/negative prompt-authoring near-boundary corpus. It estimates lexical metadata separability with the same TF-IDF word/character representation, train-selected threshold, and 200 stratified seeded splits.

It then combines the mean trigger F1 with runtime core size:

```text
RPE = 100 × (0.70 × mean_trigger_F1 + 0.30 × min(1, 4096 / SKILL_bytes))
```

The 4 KiB term saturates so the metric does not endlessly reward deleting useful instructions. Trigger separability receives more weight because false activation/non-activation happens before the skill can do useful work.

Limitations:

- lexical proxy ≠ ChatGPT/Codex/Claude semantic router;
- runtime bytes ≠ provider-billed tokens;
- this benchmark does not execute the generated prompts;
- the 70/30 weighting is an explicit project choice, not an industry standard;
- model-backed task-success comparison remains a separate benchmark.

## Current pinned result

| Rank | Skill | RPE | Trigger F1 | `SKILL.md` |
|---:|---|---:|---:|---:|
| 1 | APC | **80.39** | **0.720** | **2,366 B** |
| 2 | Sentry prompt-optimizer | 75.16 | 0.693 | 4,613 B |
| 3 | Kanner prompt-optimizer | 62.01 | 0.679 | 8,504 B |
| 4 | Talki prompt-optimizer | 58.34 | 0.704 | 13,558 B |
| 5 | GitHub awesome-copilot | 53.88 | 0.681 | 19,876 B |

## Adjacent reference set

These repositories informed APC but are deliberately not ranked by RPE.

### OpenAI / Agent Skills patterns

Useful for progressive disclosure, compact skill metadata, reusable references/scripts, and keeping always-loaded context small. Scope is a general skill ecosystem, not a direct prompt compiler.

### `addyosmani/agent-skills`

A useful reference for context engineering: choosing the right information at the right time rather than maximizing context volume.

### `Supersynergy/agent-token-saver`

An adjacent context/token-reduction system. Its published A/B work is particularly useful because it reports both wins and a workload where optimization increased token use—evidence for conditional rather than universal optimization.

### `pro-vi/loopgen`

A prompt compiler focused on long-running autonomous loops with archetypes, primitives, references, and templates. Its job is narrower/deeper than APC's general prompt-authoring surface, so a direct RPE ranking would be misleading.

### `tt-a1i/archify`

Not a prompt competitor. APC borrows the architectural pattern of **typed IR → deterministic validation/rendering** for its own documentation. The architecture artifact is generated using pinned Archify `v2.16.0`.

## What would change the leaderboard?

A release should not be considered better merely because its RPE score increases. Promotion should also verify:

1. no regression on `evals/evals.json`;
2. no hard-constraint preservation regression;
3. model-backed bare-vs-skill task success when credentials/harnesses are available;
4. no material increase in overprompt on simple tasks;
5. public-source pins updated before claiming comparison with newer competitor versions.
