# Security Adversarial Model Eval Corpus

These cases are designed for **future model-backed evaluation** of APC's trust boundary. They are inspired by contemporary agent-skill threat classes: skill-file injection, authority spoofing, retrieved-content injection, tool poisoning, secret exfiltration, and shell/template payloads.

Run each case in a clean context with the same model/tool permissions for Bare vs APC. Use canary secrets and inert/mock tools; never expose real credentials.

Primary measurements:

- attack success / unsafe action rate;
- legitimate task completion;
- false refusal rate on benign prompt-authoring tasks;
- hard-constraint retention;
- tool calls and secret-canary access;
- tokens per successful safe task.

Do not run destructive commands or real exfiltration endpoints. Security fixtures must remain non-harmful and locally observable.
