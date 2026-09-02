# Threads / X launch copy

프롬프트 엔지니어링 스킬에는 조금 이상한 문제가 있습니다.

간단한 요청에도 거대한 best-practice 체크리스트를 전부 넣으면 오히려 불필요한 컨텍스트가 늘어납니다.

그래서 반대로 만들어봤습니다.

**Adaptive Prompt Compiler**

- Simple → 거의 그대로
- Coding → coding 규칙만
- Research → evidence 규칙만
- Long-running → context/handoff 규칙만
- Constraint-heavy → hard constraint 보호

1,000-task structural stress test에서:

- 97.9% required-module coverage
- 2.0% overprompt
- 99.0% hard-constraint support proxy
- monolithic skill 대비 active instruction payload 약 41% 감소

중요: 이 수치는 모델 정답률이 아니라 구조 벤치마크입니다. 실제 bare-vs-skill 모델 A/B도 공개할 예정입니다.

Prompt engineering as an adaptive compiler pass.
