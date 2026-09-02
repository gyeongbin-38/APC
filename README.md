<div align="center">

# APC
### Adaptive Prompt Compiler

**Prompt engineering as a compiler pass.**<br>
Write rough intent. APC adds only the prompt structure the task actually earns.

[![CI](https://github.com/gyeongbin-38/APC/actions/workflows/validate.yml/badge.svg)](https://github.com/gyeongbin-38/APC/actions/workflows/validate.yml)
![Agent Skill](https://img.shields.io/badge/Agent-Skill-7C3AED?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)
![Structural](https://img.shields.io/badge/structural-93.42%2F100-0891b2?style=flat-square)
![RPE](https://img.shields.io/badge/RPE-80.39%2F100-f59e0b?style=flat-square)

**APC = Adaptive Prompt Compiler**

[Quick start](#quick-start) · [Usage guide](docs/USAGE.md) · [How it works](#how-it-works) · [Benchmarks](#benchmarks) · [Evidence ladder](benchmarks/README.md) · [Archify map](docs/architecture/README.md)

</div>

---

APC is a portable Agent Skill that turns a request for another AI into the **minimum-sufficient prompt** for that task.

A simple task stays simple. A coding, research, handoff, or long-running task can progressively load stronger guidance without making every prompt inherit one giant checklist.

```text
rough intent
    ↓
thin skill core
    ↓
compact Prompt IR
    ↓
complexity + risk gate
    ↓
load only relevant guidance
    ↓
target-aware prompt
```

> **Quality first. Token savings second.** APC removes irrelevant prompt overhead before it considers compressing anything decision-critical.

## Benchmark snapshot

| Evidence | Current result | What it measures |
|---|---:|---|
| **Structural architecture score** | **93.42 / 100** | coverage, overprompt, constraint support, active payload across 1,000 synthetic tasks × 100 routing-noise runs |
| **RPE score — public repos** | **80.39 / 100** | metadata trigger separability + runtime `SKILL.md` payload against four public prompt-optimizer Skills |
| **Trigger boundary** | **0.720 F1** | 140-case lexical near-miss routing proxy |
| **Constraint fuzz** | **10,000 / 10,000** | literal preservation through the optional deterministic Prompt IR emitter |
| **Security posture** | **15 / 15 controls** | static supply-chain/runtime/trust-boundary controls + inert payload checks; not a model jailbreak score |
| **Model-backed task success** | **Pending** | clean-context bare-vs-skill A/B; no pass@1 uplift is claimed yet |

**Important:** the first five are deterministic/proxy benchmarks, not LLM accuracy. See the linked reports before quoting the numbers.

## Quick start

Install with the open `skills` CLI:

```bash
npx skills add gyeongbin-38/APC --skill adaptive-prompt-compiler
```

Or copy the skill directory into a client-supported skills folder:

```bash
mkdir -p .agents/skills
cp -R skill/adaptive-prompt-compiler .agents/skills/
```

Then ask naturally:

```text
Create a prompt for a coding agent to fix this bug without refactoring unrelated code.
```

```text
Rewrite this research prompt so the agent checks primary sources and reports uncertainty.
```

```text
Make this system prompt shorter without losing any hard constraints.
```

APC should **not** activate for ordinary requests such as `What is prompt engineering?` unless the user actually wants a reusable prompt or AI instruction.

## How it works

APC uses a deliberately small runtime core and progressively loads task-specific references.

```text
User Intent
    │
    ▼
┌────────────────────┐
│ Thin SKILL.md Core │  classify only what matters
└─────────┬──────────┘
          ▼
     ┌───────────┐
     │ Prompt IR │  objective · hard constraints · success
     └─────┬─────┘
           │
       ┌───┴───────────────┐
       │ condition-gated   │
       ▼                   ▼
  JIT references     optional emitter
       │                   │
       └────────┬──────────┘
                ▼
        Target-aware Prompt
                │
                ▼
            Target AI
```

For the deeper interactive system view, open the **[Archify architecture map](docs/architecture/README.md)**. The diagram is generated from typed JSON IR and validated with pinned Archify `v2.16.0`.

### Runtime package

```text
skill/adaptive-prompt-compiler/
├── SKILL.md                 # ~2.6 KB runtime router/compiler
├── references/
│   ├── coding.md
│   ├── research.md
│   ├── agentic.md
│   ├── handoff.md
│   ├── constraints.md
│   └── targets.md
├── scripts/
│   ├── compile_prompt.py    # optional deterministic path
│   └── validate_ir.py
└── assets/
    └── prompt-ir.schema.json
```

The core does not load a reference merely because it exists.

### Prompt IR

Only material fields need to exist:

```json
{
  "objective": "Fix the failing checkout test",
  "target": "coding agent",
  "hard_constraints": ["Do not change the public API"],
  "success_criteria": ["Relevant tests pass"],
  "complexity": "structured"
}
```

Hosts with code execution can optionally compile JSON IR deterministically:

```bash
python skill/adaptive-prompt-compiler/scripts/compile_prompt.py examples/ir-coding.json
```

## Benchmarks

APC keeps different claims in separate benchmark families so a convenient proxy cannot masquerade as model quality.

### 1. Structural architecture benchmark

1,000 synthetic task cards across simple, rewrite, creative, coding, research, long-running, handoff, and constraint-heavy conditions are evaluated over 100 seeded routing-noise runs.

| Candidate | Score | Coverage | Overprompt | Constraint support | Active instruction proxy |
|---|---:|---:|---:|---:|---:|
| **adaptive-compiler** | **93.42** | **97.87%** | **1.97%** | **99.03%** | 1,027 |
| typed-ir-router | 91.81 | 95.74% | 4.00% | 98.09% | 1,000 |
| monolithic | 81.49 | 100% | 65.70% | 100% | 1,697 |
| specialist-pack | 73.97 | 69.66% | 5.21% | 81.30% | 470 |

In this benchmark, APC uses about **39% less active instruction payload** than the monolithic candidate while retaining high required-module coverage. The payload metric is `UTF-8 characters / 4`, not provider billing.

[Methodology and limitations →](benchmarks/structural/REPORT.md)

### 2. Public repository benchmark

The **RPE score (Routing & Payload Efficiency)** compares APC with public prompt-authoring Agent Skills using their actual published descriptions, runtime Skill sizes, and pinned Git blob identities.

| Rank | Public Skill | RPE score | Trigger F1 | Runtime `SKILL.md` |
|---:|---|---:|---:|---:|
| 1 | **APC** | **80.39** | **0.720** | **2,579 B** |
| 2 | Sentry `prompt-optimizer` | 75.16 | 0.693 | 4,613 B |
| 3 | Kanner `prompt-optimizer` | 62.01 | 0.679 | 8,504 B |
| 4 | Talki `prompt-optimizer` | 58.34 | 0.704 | 13,558 B |
| 5 | GitHub `awesome-copilot` prompt optimizer | 53.88 | 0.681 | 19,876 B |

RPE is intentionally narrow:

```text
100 × (0.70 × trigger_F1 + 0.30 × min(1, 4096 / SKILL_bytes))
```

It measures **activation-boundary separability and runtime payload efficiency only**. It does **not** say APC produces better answers than Sentry, GitHub, Talki, or Kanner. Sentry in particular is a strong architecture reference because its public Skill also uses progressive disclosure and eval-driven optimization.

[Reproduce the public-repo benchmark →](benchmarks/public-repos/REPORT.md)

### 3. Constraint fuzz

The optional deterministic compiler preserves **10,000 / 10,000** generated hard-constraint literals in the current fuzz corpus. This proves compiler preservation—not downstream LLM compliance.

[Constraint fuzz report →](benchmarks/constraint-fuzz/REPORT.md)

### 4. Security posture benchmark

A deterministic security suite checks 15 repository/runtime controls: no network/subprocess/eval/exec in the optional emitter, strict IR validation and size bounds, an explicit untrusted-content boundary, immutable Action/Archify pins, read-only validation CI, no `pull_request_target`, credential isolation during third-party rendering, and inert handling of suspicious payload strings.

Current result: **15 / 15 controls pass**. This is a static/deterministic posture check, **not** proof of model-level jailbreak resistance. A separate adversarial model corpus is included under `evals/security-adversarial/`.

[Security benchmark →](benchmarks/security-adversarial/REPORT.md) · [Security policy →](SECURITY.md)

### 5. Model-backed A/B

Real answer-quality claims are deliberately kept separate. `evals/model-backed/` contains clean-context **bare vs with-skill** fixtures for model-backed evaluation.

Until those runs are completed across models/surfaces, APC does **not** claim a measured pass@1 or task-success uplift. See the controlled **[model-backed evaluation protocol](evals/model-backed/PROTOCOL.md)** for the planned paired A/B methodology.

## Public repository comparison

The direct comparison set is intentionally limited to repositories that expose a reusable prompt-authoring/optimization Skill. Famous adjacent projects are used as design references but are not forced into an unfair single score.

### Direct prompt-authoring competitors

| Project | Strongest public characteristic | APC difference |
|---|---|---|
| `getsentry/skills` · prompt-optimizer | progressive disclosure, contract capture, eval loop | smaller core + explicit complexity gating + public routing/payload benchmark |
| `github/awesome-copilot` · prompt-optimizer | extensive chat-prompt cookbook and finished-output rules | APC keeps the always-loaded core much smaller and condition-gates detailed guidance |
| `talki-io/prompt-optimizer` | very explicit semantic-preservation/editor boundary | APC also authors new prompts and handles agentic/handoff cases conditionally |
| `ckanner/agent-skills` · prompt-optimizer | conventional systematic optimization workflow | APC emphasizes adaptive complexity and minimum-sufficient prompt structure |

### Famous / adjacent reference repositories

These influence the design but are **not ranked by RPE because their jobs differ**:

- `openai/skills` / Agent Skills patterns — progressive disclosure and reusable skill packaging.
- `addyosmani/agent-skills` — production-oriented context engineering patterns.
- `Supersynergy/agent-token-saver` — measured token/context reduction and evidence that optimization can regress on some workloads.
- `pro-vi/loopgen` — prompt compilation for long-running autonomous loops.
- `tt-a1i/archify` — typed IR + deterministic renderer pattern used for APC's architecture visualization.

The exact competitive sources and immutable blob pins are documented in **[Competitive Landscape](docs/COMPETITIVE_LANDSCAPE.md)** and `benchmarks/public-repos/sources.json`.

## Why APC instead of one giant prompt template?

A universal checklist maximizes rule coverage by paying an irrelevant-context tax on every task. APC instead treats prompting more like compilation:

1. capture the task contract;
2. classify complexity and material risk;
3. construct a compact Prompt IR;
4. load only the references that resolve real needs;
5. emit a target-appropriate prompt;
6. verify hard constraints and success criteria proportionally.

The goal is not the shortest prompt. It is the **smallest prompt with equivalent expected task success**.

## Evaluation layout

```text
evals/                          real-model cases / trigger corpus
benchmarks/structural/          architecture stress test
benchmarks/trigger-boundary/    metadata near-miss proxy
benchmarks/constraint-fuzz/     deterministic constraint preservation
benchmarks/public-repos/        pinned public competitor comparison
benchmarks/security-adversarial/ security posture and inert-payload controls
```

Run the deterministic suite locally:

```bash
python -m unittest discover -s tests -v
python benchmarks/structural/run_benchmark.py
python benchmarks/trigger-boundary/run_benchmark.py
python benchmarks/constraint-fuzz/run_fuzz.py
python benchmarks/public-repos/run_benchmark.py
python benchmarks/security-adversarial/run_benchmark.py
```

## Design principles

1. **Quality first; token savings second.**
2. Remove irrelevant context before compressing critical context.
3. Hard constraints never become optional because a prompt was shortened.
4. Simple tasks should not inherit agentic machinery.
5. Exact evidence beats generic similarity for decision-critical facts.
6. Execution is not verification.
7. Public benchmark claims label proxies separately from provider/model measurements.

## Contributing

Adversarial trigger cases, failed prompts, model-backed A/B results, and competing public Skill examples are especially useful. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
