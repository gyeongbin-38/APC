# Changelog

## 0.1.2 — Security hardening

- Added an explicit untrusted-content boundary to the always-on Skill core.
- Hardened the deterministic Prompt IR emitter with unknown-field/type/size validation and graceful input errors.
- Pinned GitHub Actions and Archify execution to immutable commit SHAs.
- Removed persisted repository credentials while external Archify code executes.
- Added a 15-control security posture benchmark and adversarial model-eval corpus.
- Added benchmark freshness and determinism regression coverage.

## 0.1.0 — 2026-09-02

- Initial public experimental release.
- Thin Agent Skills-compatible router.
- Compact prompt IR.
- Conditional coding, research, agentic, handoff, constraint, and target references.
- Optional stdlib-only deterministic IR emitter.
- Public eval corpus and structural benchmark.

## 0.1.1 - 2026-09-02

- Added 140-case adversarial trigger-boundary benchmark with multilingual/near-miss cases.
- Added clean bare-vs-skill model-backed eval fixtures and Promptfoo Codex example.
- Added launch-plan and community-post drafts.
- Added `npx skills add` installation path for the future public GitHub repository.
- Kept model-success claims explicitly separate from structural proxy metrics.
