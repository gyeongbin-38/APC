# Trigger Boundary Benchmark — v0.1.1

This benchmark tests whether the `SKILL.md` **description text is lexically separable** from nearby requests. It does **not** call an Agent Skills router or an LLM.

## Dataset

140 prompts:

- 75 should trigger;
- 65 should not trigger;
- includes English, Korean, near-miss wording, omitted use of the word `prompt`, human writing prompts, shell prompts, ordinary writing, direct task execution, and prompt-engineering explanation requests.

For each candidate description, a hybrid word/character TF-IDF similarity score is threshold-calibrated on half of the positive/negative examples and tested on the held-out half across 200 seeded splits.

## Result

| Description | Precision | Recall | F1 | Accuracy |
|---|---:|---:|---:|---:|
| current | 0.643 | 0.823 | **0.718** | **0.657** |
| explicit-boundary | 0.602 | **0.868** | 0.708 | 0.618 |
| ultra-short | 0.599 | 0.825 | 0.690 | 0.604 |
| broad | 0.580 | 0.855 | 0.688 | 0.586 |

## Interpretation

The current description is the best of the four cheap lexical proxies. The broader variants gain some recall but create more false positives. This supports keeping one narrow, explicit top-level skill rather than widening its trigger surface.

## Limitation

This is **not real skill-router accuracy**. Modern Agent Skills clients use richer semantic routing than TF-IDF. Run model-backed routing evals before making any router-accuracy claim.
