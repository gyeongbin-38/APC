# Structural Benchmark Report

Method: deterministic structural stress benchmark; no model calls

| Candidate | Score | Coverage | Overprompt | Constraint support | Active instruction proxy |
|---|---:|---:|---:|---:|---:|
| adaptive-compiler | 93.42 | 0.9787 | 0.0197 | 0.9903 | 1027.3 |
| typed-ir-router | 91.81 | 0.9574 | 0.0400 | 0.9809 | 999.8 |
| thin-router | 89.71 | 0.9226 | 0.0695 | 0.9647 | 844.2 |
| monolithic | 81.49 | 1.0000 | 0.6570 | 1.0000 | 1696.8 |
| specialist-pack | 73.97 | 0.6966 | 0.0521 | 0.8130 | 470.3 |
| no-skill | 36.99 | 0.1410 | 0.0000 | 0.6093 | 0.0 |

The token proxy is UTF-8 characters / 4, not provider billing. This benchmark is structural and does not measure model pass@1.

The benchmark is deterministic across Python hash seeds; CI includes a regression test for this property.
