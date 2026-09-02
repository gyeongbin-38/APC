# Security-vs-Efficiency Pareto Benchmark

This benchmark tests **where APC's trust-boundary instruction should live**. It does not call an LLM and does not measure jailbreak resistance.

## Strategies

| Strategy | Behavior | Added policy payload |
|---|---|---:|
| `no_guard` | no APC-layer trust-boundary instruction | 0 token-proxy |
| `lazy_short_guard` | load the short trust boundary only when a risk router fires | 53.25 when active |
| **`always_short_guard`** | current APC design: keep one short trust boundary in `SKILL.md` | **53.25 every prompt-authoring activation** |
| `always_full_policy` | inject the entire `SECURITY.md` | 741.25 every activation |

Token-proxy is UTF-8 bytes / 4, not provider billing.

## Risk-router stress test

The lazy strategy is evaluated on **200 paired risky/benign near-boundary cases** using 20 repeated 5-fold `StratifiedGroupKFold` runs. Template families are held out by group so the router cannot win merely by memorizing one phrasing family.

Base lexical risk-router result:

| Metric | Result |
|---|---:|
| Risk recall | **98.60%** |
| Benign false activation | 40.65% |
| Precision | 70.93% |
| F1 | 82.47% |
| Accuracy | 78.97% |

Then independent decision-flip noise is applied analytically.

### Example at 5% risky workload

| Added routing noise | Lazy guard coverage on risky tasks | Lazy added token-proxy | Always-short coverage | Always-short tokens | Full-policy tokens |
|---:|---:|---:|---:|---:|---:|
| 0% | **98.60%** | 23.19 | **100%** | 53.25 | 741.25 |
| 5% | 93.74% | 23.53 | **100%** | 53.25 | 741.25 |
| 10% | 88.88% | 23.88 | **100%** | 53.25 | 741.25 |
| 20% | 79.16% | 24.56 | **100%** | 53.25 | 741.25 |
| 30% | 69.44% | 25.25 | **100%** | 53.25 | 741.25 |

## Conditional winner

There is no single winner if security requirements differ.

- If a deployment accepts **90% guard-presence coverage** and the risk router is nearly perfect, lazy loading is cheaper.
- At a **95% minimum**, lazy wins only at zero added routing noise in this benchmark.
- At a **99% minimum**, the current **always-on short boundary wins even at zero added noise** because the held-out lexical router reaches 98.6% recall.
- The full policy is dominated by the short always-on boundary on this proxy: both give 100% guard-presence coverage, but the full policy costs about **13.9×** more prompt payload.

## Decision for APC

For a portable public Skill, the compiler cannot safely assume that risky quoted/retrieved/tool/handoff content will be recognized before that content is processed. APC therefore keeps a **short trust boundary always on** and leaves the detailed security policy outside the normal prompt.

That is a deliberate security/efficiency trade:

- the security hardening moved the structural architecture score from **93.53 → 93.42**;
- the one-line boundary adds about **53 token-proxy**;
- it avoids making trust-boundary presence depend on a fallible risk-routing step.

## Limitations

- "Security coverage" here means **the APC trust-boundary rule is present**, not that the downstream model obeys it.
- The 200-case corpus is synthetic and English-heavy.
- The lexical router is a proxy, not ChatGPT/Codex/Claude's production skill router.
- Real attack success, false refusals, tool misuse, and secret-canary access require the separate model-backed adversarial eval in `evals/security-adversarial/`.

Reproduce:

```bash
python benchmarks/security-efficiency/run_benchmark.py
```
