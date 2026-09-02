# Agentic and Long-Running Prompts

Use these rules only for long-running, tool-heavy, or context-heavy work.

- Keep a bounded working state: objective, constraints, verified facts, decisions, current subgoal, blockers, next action, active artifacts/evidence refs.
- Retrieve because the next decision has an information gap, not merely because content is related.
- Reduce large logs/tool results deterministically: deduplicate, filter, aggregate, retain representative failures and exact refs.
- Keep raw backing data recoverable outside the active prompt when possible.
- Checkpoint at semantic boundaries such as completed subgoals, committed decisions, diagnosed failures, phase transitions, or explicit handoff.
- Do not carry discarded exploration or full transcripts by default.
- Verify completion; execution alone is not proof of success.
