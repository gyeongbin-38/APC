# Constraint Preservation

Use when failure to preserve constraints would materially harm the result.

Classify constraints as:

- **hard**: must be satisfied; never silently weakened;
- **preference**: optimize when compatible with hard constraints;
- **non-goal**: explicitly out of scope.

For hard constraints, make verification observable when possible. Examples: exact output syntax, forbidden files, unchanged architecture boundary, required citations, maximum scope, safety boundaries, or tests that must pass.

When constraints conflict, surface the conflict instead of silently choosing one.
