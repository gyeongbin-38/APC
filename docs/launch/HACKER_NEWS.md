# Show HN launch draft

## Title

Show HN: Adaptive Prompt Compiler – an Agent Skill that loads only the prompt rules a task needs

## First comment

I built this after noticing a recurring failure mode in prompt-engineering skills: simple tasks get overprompted, while mixed long-running tasks often need several concerns at once.

The core is a small Agent Skill that first classifies the request as simple, structured, or agentic, then loads only relevant references such as coding, research, handoff, or hard-constraint guidance.

The repo includes the skill, an optional deterministic prompt-IR emitter, tests, eval cases, and benchmark source.

Current structural benchmark:

- 1,000 tasks across 10 conditions
- 97.9% required-module coverage
- 2.0% overprompt
- 99.0% hard-constraint support proxy
- ~41% smaller active instruction payload than the monolithic candidate

Those are structural proxy metrics, not model accuracy. I kept that distinction explicit because I don't want to turn a synthetic benchmark into a pass@1 claim. The repository includes clean bare-vs-skill model-eval fixtures as the next evidence layer.

The project follows the open Agent Skills format and has no runtime dependency; optional Python helpers use only the standard library.

I'd be particularly interested in cases where the routing boundary is wrong or where a modern model performs better with even less scaffolding.
