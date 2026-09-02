# Research and design references

This project intentionally combines a small set of patterns rather than cloning one existing prompt framework.

## Agent Skills standard

- Agent Skills specification: https://github.com/agentskills/agentskills
- Progressive disclosure: metadata -> `SKILL.md` -> references/scripts/assets.
- Description quality matters because description is the discovery-time trigger surface.

Design impact: keep one cohesive top-level skill and move conditional detail into references.

## OpenAI Skills guidance

- https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- https://openai.com/academy/skills/

Design impact: skills are best for repeatable workflows. The compiler is a reusable method for prompt-authoring requests rather than an always-on replacement for normal ChatGPT behavior.

## agent-token-saver

- https://github.com/Supersynergy/agent-token-saver

Useful pattern: exact evidence -> deterministic projection -> selective skill/context loading. Its published Codex A/B also shows an important negative result: one task used more tokens even though the aggregate saved tokens. That supports workload-conditional optimization rather than universal compression.

## loopgen

- https://github.com/pro-vi/loopgen

Useful pattern: classify task shape, compose from primitives/archetypes, emit stable artifacts, make long-running state explicit. Adaptive Prompt Compiler generalizes only the classification/composition idea; it does not adopt loopgen's autonomous-loop runtime or artifact set for ordinary users.

## Intent/prompt compiler projects

Examples:
- https://github.com/PantheraLabs/IntentCompiler
- https://github.com/CyberFFarm/Prompt-Compiler

Design impact: avoid requiring a separate web app, provider API keys, model router, or prompt database for the core use case. The public skill must remain useful as a folder copied into any compatible Agent Skills host.

## Evaluation ecosystem

- Agent Skills eval guidance: https://agentskills.io/skill-creation/evaluating-skills
- promptfoo: https://github.com/promptfoo/promptfoo
- SkillsBench: https://github.com/benchflow-ai/skillsbench

Design impact: separate runtime skill content from public eval/development artifacts and compare with-skill vs without-skill in clean contexts. Structural token estimates are not provider billing or task-success claims.
