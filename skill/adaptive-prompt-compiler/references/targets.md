# Target Adaptation

Adapt only when the target is known.

- **General chat model:** outcome-first, concise instructions, only necessary context.
- **Coding agent:** include repository inspection, edit scope, verification, and final diff/report expectations.
- **Research agent:** include source/evidence requirements and uncertainty handling.
- **Reviewer/verifier:** provide original objective, candidate result, acceptance criteria, and a bounded verdict contract; do not give execution authority unless needed.
- **Image/audio/media model:** specify desired observable output rather than coding/repository machinery.
- **APC-aware target or shared policy:** emit only the task-specific delta (objective, constraints, evidence/context refs, success criteria, current state, required output). Do not restate APC's compiler policy or generic guidance the target already inherits.

Do not invent unsupported target capabilities.
