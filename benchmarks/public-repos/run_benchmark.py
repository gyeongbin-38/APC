#!/usr/bin/env python3
"""Compare public prompt-authoring Agent Skills on routing metadata + runtime payload.

This is intentionally NOT an LLM quality benchmark. It uses the same 140-case
near-boundary corpus as the APC trigger benchmark and exact published SKILL.md
sizes pinned in sources.json.
"""
from __future__ import annotations
import json, random, statistics
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sources=json.loads((OUT/'sources.json').read_text(encoding='utf-8'))
base=json.loads((ROOT/'evals/trigger_set.json').read_text(encoding='utf-8'))
extra=[]
def add(q,y): extra.append({'query':q,'should_trigger':y})
POSITIVES=[
"Turn these messy requirements into instructions I can paste into an AI coding agent.",
"Give me a reusable instruction block for Gemini to compare these PDFs.",
"Make this agent brief less verbose without dropping any NEVER rules.",
"I want exact instructions for another model to review a legal memo with citations.",
"Structure these notes as a system message for an AI tutor.",
"Create something I can paste into an image generator for this scene.",
"Convert this task into a concise brief for an autonomous research agent.",
"Refine the following LLM instructions and preserve the JSON output contract.",
"Make an AI handoff that preserves blockers, decisions, and next action.",
"Write reusable instructions for Codex to inspect only the relevant files.",
"이 요구사항을 코덱스에 넣을 구현 프롬프트로 만들어줘.",
"다른 AI에게 줄 시스템 프롬프트로 정리해줘.",
"이 프롬프트 짧게 줄이되 MUST 조건은 하나도 빼지 마.",
"리서치 에이전트에게 넘길 지시문 만들어줘. 최신 출처와 정확한 날짜가 필요해.",
"클로드에 붙여넣을 코드리뷰 지침 만들어줘.",
"이미지 생성 모델용 프롬프트로 바꿔줘.",
"긴 작업을 다른 에이전트가 이어받을 수 있게 handoff prompt 만들어줘.",
"대충 적은 요구사항인데 AI가 잘 수행하도록 프롬프트로 컴파일해줘.",
"이 작업을 GPT에 맡기기 좋은 재사용 지시문으로 바꿔줘.",
"시스템 메시지 개선해줘. 보안 규칙은 절대 약화하면 안 돼.",
]
NEGATIVES=[
"Explain this prompt to me but don't rewrite it.",
"What does the phrase 'system prompt' mean?",
"Summarize the prompt engineering article I attached.",
"Write a friendly text message to my teammate.",
"Review this Python function for bugs directly.",
"Research the latest prompt injection attacks and summarize them.",
"Give me ideas for prompts I could ask in an interview, not AI prompts.",
"The shell prompt looks weird after installing zsh. How do I fix it?",
"What are some good writing prompts for a fiction class?",
"Evaluate whether this existing prompt worked; do not produce a replacement.",
"프롬프트 엔지니어링이 뭐야? 설명만 해줘.",
"이 이메일 문장 자연스럽게 고쳐줘.",
"이 파이썬 오류 직접 해결해줘. 프롬프트는 필요 없어.",
"AI 프롬프트 관련 최신 논문을 조사해줘.",
"이 프롬프트가 왜 안 좋은지 분석만 해줘. 새 프롬프트는 만들지 마.",
"소설 글쓰기 프롬프트 아이디어 10개 줘.",
"터미널 프롬프트 색깔을 바꾸는 법 알려줘.",
"내 코드 리뷰해줘.",
"이 문서 요약해줘.",
"ChatGPT에 시스템 프롬프트가 왜 중요한지 설명해줘.",
]
for q in POSITIVES: add(q,True)
for q in NEGATIVES: add(q,False)
true_stems=[
("Make a reusable AI prompt to {task}.",["review a PR","compare two papers","debug a repository","extract facts from files","generate a product image"]),
("Turn my notes into instructions for another AI to {task}.",["write tests","research a law","summarize evidence","plan an experiment","grade answers"]),
("Rewrite these agent instructions so they {task}.",["stay concise","preserve constraints","use tools only when needed","return strict JSON","leave a resumable handoff"]),
]
false_stems=[
("Explain {task} without creating a new prompt.",["prompt injection","system prompts","few-shot prompting","agent skills","context windows"]),
("Do {task} directly; I do not need instructions for another AI.",["the code review","the research","the rewrite","the summary","the calculation"]),
("Give me {task} prompts for humans, not LLM prompts.",["journal","interview","fiction-writing","class discussion","icebreaker"]),
]
for stem,vals in true_stems:
    for v in vals: add(stem.format(task=v),True)
for stem,vals in false_stems:
    for v in vals: add(stem.format(task=v),False)
cases=base+extra
labels=[bool(x['should_trigger']) for x in cases]
texts=[x['query'] for x in cases]+[s['description'] for s in sources.values()]
word=TfidfVectorizer(lowercase=True,ngram_range=(1,2),min_df=1).fit_transform(texts)
char=TfidfVectorizer(lowercase=True,analyzer='char_wb',ngram_range=(3,5),min_df=1).fit_transform(texts)
n=len(cases)

def metrics(pred,truth):
    tp=sum(p and y for p,y in zip(pred,truth)); fp=sum(p and not y for p,y in zip(pred,truth))
    fn=sum((not p) and y for p,y in zip(pred,truth)); tn=sum((not p) and (not y) for p,y in zip(pred,truth))
    precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0
    accuracy=(tp+tn)/len(truth)
    return precision,recall,f1,accuracy

rows=[]
for di,(name,src) in enumerate(sources.items()):
    wi=n+di
    sims=(cosine_similarity(word[:n],word[wi]).ravel()+cosine_similarity(char[:n],char[wi]).ravel())/2
    samples=[]
    for seed in range(200):
        r=random.Random(88000+seed)
        pos=[i for i,y in enumerate(labels) if y]; neg=[i for i,y in enumerate(labels) if not y]
        r.shuffle(pos); r.shuffle(neg)
        train=pos[:len(pos)//2]+neg[:len(neg)//2]
        test=pos[len(pos)//2:]+neg[len(neg)//2:]
        vals=sorted({float(sims[i]) for i in train})
        thresholds=[0.0]+[(a+b)/2 for a,b in zip(vals,vals[1:])]+[1.0]
        best=(-1,None)
        for t in thresholds:
            f1=metrics([sims[i]>=t for i in train],[labels[i] for i in train])[2]
            if f1>best[0]: best=(f1,t)
        t=best[1]
        samples.append(metrics([sims[i]>=t for i in test],[labels[i] for i in test]))
    f1=statistics.mean(x[2] for x in samples)
    payload_eff=min(1.0,4096/src['size_bytes'])
    score=100*(0.70*f1+0.30*payload_eff)
    rows.append({
      'name':name,'repo':src['repo'],'blob_sha':src['blob_sha'],'skill_bytes':src['size_bytes'],
      'payload_proxy_chars_per_4':round(src['size_bytes']/4,1),
      'trigger_f1_mean':round(f1,4),'trigger_f1_sd':round(statistics.pstdev(x[2] for x in samples),4),
      'payload_efficiency_4k_cap':round(payload_eff,4),'routing_payload_score':round(score,2),
    })
rows.sort(key=lambda x:x['routing_payload_score'],reverse=True)
out={
 'benchmark':'Open Prompt Skill — Routing & Payload Benchmark v0.1',
 'date':'2026-09-02','cases':len(cases),'positive':sum(labels),'negative':len(labels)-sum(labels),'splits':200,
 'score_formula':'100 * (0.70 * mean_trigger_F1 + 0.30 * min(1, 4096 / SKILL_bytes))',
 'scope':'Measures metadata trigger separability and runtime SKILL.md payload only. It does not measure model answer quality or task-success uplift.',
 'rows':rows,
}
(OUT/'results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
