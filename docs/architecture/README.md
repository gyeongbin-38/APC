# APC Architecture Map

This directory contains the source for the **Archify** view of APC.

- `apc.architecture.json` — typed Archify architecture IR.
- `apc.html` — generated interactive artifact (created by CI from the pinned Archify release).

The rendering workflow pins **`tt-a1i/archify@v2.16.0`** rather than following its moving default branch.

## Re-render locally

```bash
git clone --branch v2.16.0 --depth 1 https://github.com/tt-a1i/archify.git /tmp/archify
node /tmp/archify/archify/bin/archify.mjs deliver \
  architecture \
  docs/architecture/apc.architecture.json \
  docs/architecture/apc.html \
  --quality standard \
  --repo-root "$PWD" \
  --json
```

Archify is an independent MIT-licensed project by `tt-a1i`; APC does not vendor or fork its renderer.
