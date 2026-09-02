# Launch Plan

## Release gate

Publish widely only after:

- public GitHub repository exists;
- `npx skills add <owner>/<repo> --skill adaptive-prompt-compiler` is tested from a clean directory;
- CI is green;
- structural benchmark is reproducible;
- model-backed A/B results are either published or explicitly marked pending.

## Claim hierarchy

### Safe now

- 1,000-task deterministic structural stress benchmark;
- 97.9% required-module coverage;
- 2.0% overprompt rate;
- 99.0% hard-constraint support proxy;
- ~41% smaller active instruction payload proxy than the monolithic candidate;
- 140-case trigger-boundary lexical benchmark, with explicit proxy disclaimer.

### Do not claim yet

- real model accuracy uplift;
- pass@1 improvement;
- provider token-cost reduction;
- actual Agent Skills router accuracy.

## Sequence

1. GitHub public release.
2. Verify `npx skills add` install from GitHub.
3. Run clean-context model A/B on at least one supported agent; ideally 2–3 model families.
4. Update README with real A/B table.
5. Soft launch on Threads/X.
6. Post technical write-up to r/AI_Agents.
7. Show HN after the repo is immediately runnable.
8. Post to LocalLLaMA after an open-weight model benchmark exists.

## Positioning

Primary:

> Prompt engineering as an adaptive compiler pass.

Secondary:

> Write rough intent. Load only the prompt structure the task actually earns.

Avoid positioning it as a generic "token saver". The project optimizes tokens per successful task, not token count in isolation.
