# Coding and Repository Prompts

Use these rules only for coding or repository work.

- Start from current project/repository instructions and state.
- Retrieve exact owner/path/symbol/contract before broad semantic search.
- Expand to direct dependencies and relevant tests only when needed.
- Preserve exact APIs, schemas, invariants, error text, and decision-critical code; do not replace them with lossy summaries.
- Prefer the smallest compatible change; forbid unrelated refactors unless explicitly requested.
- Verify with narrow tests first, then relevant integration/regression/build/lint gates.
- For large repos, separate exploration from implementation: pass the solver a compact evidence packet rather than the explorer's full transcript.
