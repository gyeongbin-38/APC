# Reddit launch draft — r/AI_Agents

## Title

I tested an adaptive prompt-engineering skill against a monolithic one — the main win was avoiding overprompting

## Body

I kept running into the same failure mode with prompt-engineering skills: they inject the same large checklist into a one-line creative task, a coding task, and a multi-hour agent workflow.

So I built **Adaptive Prompt Compiler**, a portable Agent Skill that keeps the top-level `SKILL.md` small and conditionally loads only the references a task needs.

The current deterministic structural stress test uses 1,000 synthetic task cards across simple, rewrite, coding, research, long-running, handoff, and constraint-heavy cases with routing noise injected across 100 seeded runs.

Current result:

- 97.9% required-module coverage
- 2.0% overprompt rate
- 99.0% hard-constraint support proxy
- ~41% less active instruction payload than the monolithic candidate

These are **not model accuracy numbers**. The benchmark is intentionally a cheap architecture filter before spending API tokens. The repo also contains clean-context bare-vs-skill eval fixtures for model-backed testing.

The interesting design choice was that neither extreme won:

- monolithic: great coverage, huge irrelevant-context tax;
- many specialist skills: cheap when routing is perfect, fragile on mixed tasks;
- one thin skill + compact prompt IR + conditional references: best balance in the stress test.

Repo and benchmark code are public. I would especially like adversarial examples where the skill should *not* trigger, or mixed tasks where the module routing misses something important.

If you can break it, please send the failing case as an eval PR.
