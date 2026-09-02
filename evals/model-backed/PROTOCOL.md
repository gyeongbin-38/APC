# Model-Backed Evaluation Protocol

Status: **protocol only — results are not yet claimed**.

This protocol defines how APC should be compared on real model/task outcomes without allowing routing proxies or prompt-size proxies to masquerade as answer quality.

## Primary question

Does APC improve downstream task success, constraint retention, or success-normalized token efficiency relative to the same model receiving the user's rough request directly?

## Evaluation arms

### Primary A/B

- **Bare:** original user request, no APC skill or APC-derived prompt.
- **APC:** same original request compiled through the pinned APC version.

### Secondary public-skill comparison

When reproducible and license-compatible, add independently pinned arms for public prompt-authoring skills such as the Sentry or GitHub prompt-optimizer examples used in `benchmarks/public-repos/`.

Do not mix multiple optimizer skills in one arm.

## Experimental controls

For a paired case, hold constant whenever the provider permits it:

- model and model snapshot/version
- temperature and sampling settings
- tool availability and permissions
- repository/files/source corpus
- system/developer instructions unrelated to the skill under test
- maximum output budget
- starting conversation state

Each arm must start from a **clean context**. Never let one arm see another arm's generated prompt, output, grader feedback, or hidden notes.

## Corpus

Use a stratified task set covering at least:

1. simple prompt-authoring tasks
2. coding/repository tasks
3. research/evidence tasks
4. long-running/tool-heavy tasks
5. agent/session handoffs
6. hard-constraint-heavy tasks
7. negative/near-miss cases where APC should not be used

Prefer real or realistically constructed tasks with deterministic acceptance checks where possible.

## Required metrics

Primary:

- `task_success`
- `hard_constraint_pass`
- `tokens_per_successful_task`

Secondary:

- prompt-generation input/output tokens
- downstream target input/output tokens
- tool-result/context tokens when observable
- latency
- cost when observable
- unnecessary-context / overprompt incidents
- hallucinated-assumption incidents
- verification completeness

Report provider token accounting separately from local character-based proxies.

## Judging

Prefer deterministic tests, compilers, linters, exact-match contracts, or source-backed checks over subjective grading.

When model judging is required:

- blind the grader to arm identity
- randomize presentation order
- provide the original task and explicit acceptance criteria
- prevent the grader from seeing benchmark labels or expected winner
- separate correctness from style/preferences

Human review may be added for ambiguous cases, but disagreements and adjudication rules must be recorded.

## Statistics

Use paired analysis because each task is run across the same arms.

At minimum report:

- number of tasks
- success count/rate per arm
- paired win/loss/tie counts
- bootstrap confidence interval for the primary delta
- mean and median tokens per successful task

Do not promote a small single-model difference into a general claim without replication.

## Reproducibility record

Every published run should pin:

```yaml
apc_commit:
skill_version:
competitor_repo_and_blob_sha:
model_provider:
model_id:
model_version_or_snapshot:
sampling_settings:
tool_configuration:
corpus_commit:
run_date:
random_seed:
grader_model_or_method:
```

Store raw outputs outside the headline summary when large, but keep stable references/hashes so results remain auditable.

## Claim gate

APC may claim a model-backed improvement only when:

1. the full protocol and corpus are public or otherwise inspectable;
2. the comparison uses clean independent contexts;
3. task success does not materially regress on important task families;
4. the reported improvement includes uncertainty/confidence information;
5. proxy metrics are clearly separated from provider/model measurements.

Until then, README status remains **Model-backed task success: Pending**.

## Recommended first experiment

Start small and paired:

```text
30–50 tasks
× 2 arms (Bare vs APC)
× one pinned model
× clean context per run
```

Only after the harness is stable should the experiment expand to multiple models and public competitor skills.
