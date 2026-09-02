# Handoff Prompts

Use when work moves between agents, models, sessions, or roles.

Prefer a small explicit state packet:

```yaml
objective:
hard_constraints: []
verified_state: []
decisions: []
completed: []
blockers: []
next_action:
active_files_or_artifacts: []
evidence_refs: []
verification:
```

Keep binding constraints and unresolved blockers explicit. Do not forward the entire prior conversation unless it is genuinely required.
