# APC Usage Guide

APC — **Adaptive Prompt Compiler** — is meant to sit between rough intent and the AI or agent that will execute the work.

## 1. Install the skill

With the open `skills` CLI:

```bash
npx skills add gyeongbin-38/APC --skill adaptive-prompt-compiler
```

Or copy the skill package into a client-supported skill directory:

```bash
mkdir -p .agents/skills
cp -R skill/adaptive-prompt-compiler .agents/skills/
```

## 2. Use it naturally

Once the host supports Agent Skills, ask for an actual reusable prompt or agent instruction.

```text
Create a prompt for Codex to fix this failing checkout test without changing the public API or refactoring unrelated code.
```

```text
Rewrite this research-agent prompt so it checks primary sources, preserves exact dates, and reports uncertainty.
```

```text
Shorten this system prompt without weakening any MUST/NEVER constraints.
```

APC should keep trivial tasks short and progressively add structure only when the task earns it.

## 3. Explicit invocation when needed

If your host does not automatically select skills, make the intent explicit:

```text
Use adaptive-prompt-compiler to turn the following requirements into a prompt for a coding agent: ...
```

The skill is still expected to emit the prompt itself, not a long explanation of APC.

## 4. Before → after example

### Rough request

```text
Make me a prompt for Codex. Fix the checkout test. Don't change the public API and don't refactor unrelated code. Check the repo first and prove the fix works.
```

### Representative APC output shape

```text
Task: Fix the failing checkout test.

Constraints:
- Do not change the public API.
- Do not refactor unrelated code.

Execution:
1. Inspect repository instructions and the smallest relevant code/test surface first.
2. Identify the failure from exact code and test evidence; expand context only if needed.
3. Implement the smallest correct fix.
4. Run the narrow relevant tests, then the repository-required validation gates.

Success:
- The checkout failure is fixed.
- Relevant tests pass.
- No unrelated behavior or public API changed.

Return:
- Root cause
- Files changed
- Verification results
- Remaining uncertainty, if any
```

The exact wording can vary by target and task. The invariant is **minimum-sufficient structure with hard constraints preserved**.

## 5. Deterministic Prompt IR path

Hosts with code execution can use the optional compiler directly:

```bash
python skill/adaptive-prompt-compiler/scripts/compile_prompt.py examples/ir-coding.json
```

A minimal Prompt IR looks like:

```json
{
  "objective": "Fix the failing checkout test",
  "target": "coding agent",
  "hard_constraints": ["Do not change the public API"],
  "success_criteria": ["Relevant tests pass"],
  "complexity": "structured"
}
```

Use the deterministic path when exact field/literal preservation matters or when you want a reproducible compiler surface. It does not replace model reasoning.

## 6. Agent-to-agent handoff

When the receiving agent already has APC or an equivalent shared prompt policy, do **not** restate the whole policy. Send only the task-specific delta: objective, constraints, evidence/context references, success criteria, current state, and required output.

This avoids paying the same instruction overhead at every hop.

## 7. When APC should not activate

APC is not for ordinary questions or direct work unless the user asks for a reusable AI prompt/instruction.

```text
What is prompt engineering?
Review this Python function directly.
Summarize this document.
Write a friendly text message.
```

Those should stay ordinary tasks rather than being wrapped in another prompt.

## Design goal

APC does **not** optimize for the shortest possible prompt.

It optimizes for the smallest prompt that preserves equivalent expected task success, hard constraints, and required evidence/verification behavior.
