# Model-backed A/B evaluation

The deterministic benchmarks in this repository are architecture filters. They do **not** establish real task-success uplift.

The release-quality comparison is:

1. same task;
2. same model and permissions;
3. clean working directory/session;
4. `bare` fixture without the skill;
5. `with-skill` fixture with only `adaptive-prompt-compiler` installed;
6. repeat nondeterministic runs;
7. score task quality first, routing/cost/latency second.

Promptfoo's current Agent Skills guide supports Codex SDK skill discovery from `.agents/skills/`, `skill-used` assertions, cost/latency signals, repeats, and trace evidence.

## Fixture layout

```text
fixtures/
├── bare/
│   └── .agents/skills/
└── with-skill/
    └── .agents/skills/adaptive-prompt-compiler/
```

## Suggested run

Use `promptfooconfig.codex.example.yaml` as a starting point and replace the placeholder task assertions with the project eval corpus in `../evals.json`.

```bash
npx promptfoo@latest eval \
  -c evals/model-backed/promptfooconfig.codex.example.yaml \
  --repeat 5 \
  --no-cache \
  -o evals/model-backed/results.json
```

Record provider-reported input/output/cache tokens separately from local estimates. Do not publish an uplift claim from a single run.

## Status in the build environment

The repository build used to prepare v0.1.1 had no OpenAI, Anthropic, or Gemini API credentials and no Codex executable, so no independent model-backed A/B result is included. This is deliberate: the project does not fabricate model results from structural proxies.
