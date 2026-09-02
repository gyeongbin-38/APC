# Adaptive Prompt Compiler

A portable Agent Skill that turns rough intent into the **smallest prompt that still preserves task quality**.

Instead of applying one giant prompt-engineering template to every request, Adaptive Prompt Compiler classifies task complexity and loads only the guidance the task actually needs.

```text
rough intent
   ↓
compact prompt IR
   ↓
complexity + risk classification
   ↓
load only relevant references
   ↓
target-aware prompt
```

## Why

Modern models often need *less* prompt scaffolding than prompt-engineering folklore suggests, while complex coding/research/agent tasks still benefit from explicit constraints, evidence rules, and verification. The skill therefore optimizes for **tokens per successful task**, not minimum tokens in isolation.

### Design goals

- **Portable:** follows the Agent Skills folder format.
- **Progressive:** thin `SKILL.md`; detailed guidance lives in on-demand references.
- **Adaptive:** simple tasks stay simple; agentic tasks get stronger context/verification rules.
- **Constraint-safe:** hard constraints are kept distinct from preferences and non-goals.
- **Target-aware:** coding, research, review, and general-model prompts are emitted differently.
- **Eval-first:** public eval cases and structural benchmarks live outside the runtime skill.
- **Zero dependency at runtime:** the skill works without scripts; optional emitters use Python stdlib only.

## Install

After the GitHub repository is published, the open `skills` CLI can install the skill directly:

```bash
npx skills add gyeongbin-38/adaptive-prompt-compiler --skill adaptive-prompt-compiler
```

Or copy `skill/adaptive-prompt-compiler/` into a skills directory supported by your client:

```bash
mkdir -p .agents/skills
cp -R skill/adaptive-prompt-compiler .agents/skills/
```

Exact installation paths vary by client. The skill itself stays platform-neutral.

## Use

Ask naturally:

```text
Create a prompt for a coding agent to fix this bug without refactoring unrelated code.
```

```text
Rewrite this research prompt so the agent checks primary sources and reports uncertainty.
```

```text
Make this system prompt shorter without losing any hard constraints.
```

The skill should **not** activate for ordinary questions such as:

```text
What is prompt engineering?
```

unless the user also asks for an actual reusable prompt.

## Architecture

The runtime skill is intentionally small:

```text
skill/adaptive-prompt-compiler/
├── SKILL.md
├── references/
│   ├── coding.md
│   ├── research.md
│   ├── agentic.md
│   ├── handoff.md
│   ├── constraints.md
│   └── targets.md
├── scripts/
│   ├── compile_prompt.py
│   └── validate_ir.py
└── assets/
    └── prompt-ir.schema.json
```

`SKILL.md` performs routing and compilation. References are loaded only when relevant. The scripts are optional deterministic helpers for hosts that support code execution.

## Prompt IR

The model-native compiler uses a compact conceptual IR. Only material fields should exist:

```json
{
  "objective": "Fix the failing checkout test",
  "target": "coding agent",
  "hard_constraints": ["Do not change the public API"],
  "success_criteria": ["Relevant tests pass"],
  "complexity": "structured"
}
```

The optional deterministic emitter can compile a JSON IR:

```bash
python skill/adaptive-prompt-compiler/scripts/compile_prompt.py examples/ir-coding.json
```

## What is different from other prompt compilers?

This project is deliberately narrower than prompt-management platforms and broader than long-running-loop generators.

It focuses on one reusable primitive:

> **Given a request to create instructions for another AI, compile only the prompt structure that task earns.**

It does not require an API key, model router, database, prompt marketplace, autonomous loop runtime, or proprietary format.

## Evaluation

There are two evaluation layers:

1. `evals/` — realistic behavior/trigger cases for real model runs.
2. `benchmarks/structural/` — deterministic structural tests for routing cost, module coverage, constraint preservation, and prompt overhead.

The structural benchmark is **not** an LLM pass@1 benchmark. It exists to compare architecture choices before spending API tokens.

Run local checks:

```bash
python -m unittest discover -s tests -v
python benchmarks/structural/run_benchmark.py
```

For model-backed evaluation, use the supplied `evals/evals.json` with an Agent Skills eval runner, promptfoo, SkillsBench, or another clean-context with-skill/without-skill harness.

## Current benchmark conclusion

The current structural benchmark favors a **thin unified skill + typed prompt IR + condition-gated references** over:

- one monolithic universal prompt skill;
- many overlapping specialist prompt skills;
- always-on context/token optimization.

See `benchmarks/structural/REPORT.md` for methods and limitations.

### Current structural result

| Candidate | Score | Coverage | Overprompt | Constraint support | Active instruction proxy |
|---|---:|---:|---:|---:|---:|
| **adaptive-compiler** | **93.53** | **97.86%** | **1.98%** | **99.03%** | 934 |
| typed-ir-router | 91.66 | 95.77% | 4.04% | 98.06% | 961 |
| monolithic | 81.49 | 100% | 65.70% | 100% | 1,579 |
| specialist-pack | 74.00 | 69.74% | 5.20% | 81.52% | 453 |

The active-instruction metric is a `UTF-8 characters / 4` payload proxy, not provider billing. The adaptive candidate uses about **41% less active instruction payload** than the monolithic candidate in this benchmark while preserving high required-module coverage.

A second 140-case trigger-boundary benchmark tests description separability against near misses. The current description ranked first among four candidates, but this is also a lexical proxy—not real router accuracy. See `benchmarks/trigger-boundary/REPORT.md`.

### Real model A/B

No independent model-success uplift is claimed yet. Clean-context bare-vs-skill fixtures and a Promptfoo/Codex example live in `evals/model-backed/`. The build environment used for v0.1.1 had no provider credentials or Codex executable, so model-backed numbers are intentionally left pending rather than inferred from structural scores.

## Principles

1. Quality first; token savings second.
2. Remove irrelevant context before compressing critical context.
3. Hard constraints never become optional because a prompt was shortened.
4. Simple tasks should not inherit agentic machinery.
5. Exact evidence beats generic semantic similarity for decision-critical facts.
6. Execution is not verification.
7. Public benchmark claims must label estimates separately from provider-reported tokens.

## License

MIT. See [LICENSE](LICENSE).
