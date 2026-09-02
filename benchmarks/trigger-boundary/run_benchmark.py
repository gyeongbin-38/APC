#!/usr/bin/env python3
"""Metadata trigger-boundary proxy benchmark.

No LLM calls. Uses TF-IDF similarity only as a cheap separability proxy for skill
metadata. It must not be interpreted as an actual Agent Skills router accuracy.
"""
from __future__ import annotations
import json, random, statistics
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT=Path(__file__).resolve().parents[2]
base=json.loads((ROOT/'evals/trigger_set.json').read_text(encoding='utf-8'))
extra=[]
def add(q,y): extra.append({'query':q,'should_trigger':y})
POSITIVES=[
"Turn these messy requirements into instructions I can paste into an AI coding agent.","Give me a reusable instruction block for Gemini to compare these PDFs.","Make this agent brief less verbose without dropping any NEVER rules.","I want exact instructions for another model to review a legal memo with citations.","Structure these notes as a system message for an AI tutor.","Create something I can paste into an image generator for this scene.","Convert this task into a concise brief for an autonomous research agent.","Refine the following LLM instructions and preserve the JSON output contract.","Make an AI handoff that preserves blockers, decisions, and next action.","Write reusable instructions for Codex to inspect only the relevant files.","이 요구사항을 코덱스에 넣을 구현 프롬프트로 만들어줘.","다른 AI에게 줄 시스템 프롬프트로 정리해줘.","이 프롬프트 짧게 줄이되 MUST 조건은 하나도 빼지 마.","리서치 에이전트에게 넘길 지시문 만들어줘. 최신 출처와 정확한 날짜가 필요해.","클로드에 붙여넣을 코드리뷰 지침 만들어줘.","이미지 생성 모델용 프롬프트로 바꿔줘.","긴 작업을 다른 에이전트가 이어받을 수 있게 handoff prompt 만들어줘.","대충 적은 요구사항인데 AI가 잘 수행하도록 프롬프트로 컴파일해줘.","이 작업을 GPT에 맡기기 좋은 재사용 지시문으로 바꿔줘.","시스템 메시지 개선해줘. 보안 규칙은 절대 약화하면 안 돼."
]
NEGATIVES=[
"Explain this prompt to me but don't rewrite it.","What does the phrase 'system prompt' mean?","Summarize the prompt engineering article I attached.","Write a friendly text message to my teammate.","Review this Python function for bugs directly.","Research the latest prompt injection attacks and summarize them.","Give me ideas for prompts I could ask in an interview, not AI prompts.","The shell prompt looks weird after installing zsh. How do I fix it?","What are some good writing prompts for a fiction class?","Evaluate whether this existing prompt worked; do not produce a replacement.","프롬프트 엔지니어링이 뭐야? 설명만 해줘.","이 이메일 문장 자연스럽게 고쳐줘.","이 파이썬 오류 직접 해결해줘. 프롬프트는 필요 없어.","AI 프롬프트 관련 최신 논문을 조사해줘.","이 프롬프트가 왜 안 좋은지 분석만 해줘. 새 프롬프트는 만들지 마.","소설 글쓰기 프롬프트 아이디어 10개 줘.","터미널 프롬프트 색깔을 바꾸는 법 알려줘.","내 코드 리뷰해줘.","이 문서 요약해줘.","ChatGPT에 시스템 프롬프트가 왜 중요한지 설명해줘."
]
for q in POSITIVES: add(q,True)
for q in NEGATIVES: add(q,False)
true_stems=[("Make a reusable AI prompt to {task}.",["review a PR","compare two papers","debug a repository","extract facts from files","generate a product image"]),("Turn my notes into instructions for another AI to {task}.",["write tests","research a law","summarize evidence","plan an experiment","grade answers"]),("Rewrite these agent instructions so they {task}.",["stay concise","preserve constraints","use tools only when needed","return strict JSON","leave a resumable handoff"])]
false_stems=[("Explain {task} without creating a new prompt.",["prompt injection","system prompts","few-shot prompting","agent skills","context windows"]),("Do {task} directly; I do not need instructions for another AI.",["the code review","the research","the rewrite","the summary","the calculation"]),("Give me {task} prompts for humans, not LLM prompts.",["journal","interview","fiction-writing","class discussion","icebreaker"])]
for stem,vals in true_stems:
    for v in vals: add(stem.format(task=v),True)
for stem,vals in false_stems:
    for v in vals: add(stem.format(task=v),False)
cases=base+extra
DESCRIPTIONS={
"current":"Compiles rough intent into a task-appropriate prompt for another AI or agent while preserving hard constraints and avoiding unnecessary prompt overhead. Use when the user asks to create, draft, rewrite, improve, optimize, structure, or shorten a prompt, system prompt, agent instruction, task brief, or AI handoff. Do not use for ordinary writing requests or general questions about prompt engineering unless the user wants an actual reusable prompt.",
"broad":"Use for prompt engineering, prompts, AI instructions, writing, coding, research, system prompts, agents, optimization, rewriting, summarization, and improving requests to AI.",
"ultra-short":"Create, rewrite, and optimize prompts and instructions for AI models and agents.",
"explicit-boundary":"Create or improve reusable instructions that the user intends to give to another AI, model, or agent. Trigger for prompts, system prompts, AI task briefs, and agent handoffs even when the word prompt is omitted. Do not trigger when the user wants the task performed directly, asks only about prompt engineering, or means human writing prompts, shell prompts, or ordinary prose rewriting."
}
texts=[c['query'] for c in cases]+list(DESCRIPTIONS.values())
word=TfidfVectorizer(lowercase=True,ngram_range=(1,2),min_df=1).fit_transform(texts)
char=TfidfVectorizer(lowercase=True,analyzer='char_wb',ngram_range=(3,5),min_df=1).fit_transform(texts)
n=len(cases); labels=[bool(c['should_trigger']) for c in cases]
def sims_for(desc_idx):
    wi=n+desc_idx
    return (cosine_similarity(word[:n],word[wi]).ravel()+cosine_similarity(char[:n],char[wi]).ravel())/2
def metrics(pred,truth):
    tp=sum(p and y for p,y in zip(pred,truth)); fp=sum(p and not y for p,y in zip(pred,truth)); fn=sum((not p) and y for p,y in zip(pred,truth)); tn=sum((not p) and (not y) for p,y in zip(pred,truth))
    precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0; f1=2*precision*recall/(precision+recall) if precision+recall else 0; acc=(tp+tn)/len(truth)
    return precision,recall,f1,acc
results=[]
for di,name in enumerate(DESCRIPTIONS):
    sims=sims_for(di); split_rows=[]
    for seed in range(200):
        r=random.Random(88000+seed); pos=[i for i,y in enumerate(labels) if y]; neg=[i for i,y in enumerate(labels) if not y]; r.shuffle(pos); r.shuffle(neg)
        train=pos[:len(pos)//2]+neg[:len(neg)//2]; test=pos[len(pos)//2:]+neg[len(neg)//2:]
        best=(0,None); vals=sorted({float(sims[i]) for i in train}); thresholds=[0.0]+[(a+b)/2 for a,b in zip(vals,vals[1:])]+[1.0]
        for t in thresholds:
            m=metrics([sims[i]>=t for i in train],[labels[i] for i in train])
            if m[2]>best[0]: best=(m[2],t)
        t=best[1]; p,rcl,f1,acc=metrics([sims[i]>=t for i in test],[labels[i] for i in test]); split_rows.append((p,rcl,f1,acc,t))
    results.append({'description':name,'precision':round(statistics.mean(x[0] for x in split_rows),4),'recall':round(statistics.mean(x[1] for x in split_rows),4),'f1':round(statistics.mean(x[2] for x in split_rows),4),'accuracy':round(statistics.mean(x[3] for x in split_rows),4),'threshold_mean':round(statistics.mean(x[4] for x in split_rows),4)})
out={'method':'TF-IDF word+char description separability proxy; no LLM router calls','cases':len(cases),'positive':sum(labels),'negative':len(labels)-sum(labels),'splits':200,'warning':'This measures lexical metadata separability, not real Agent Skills router accuracy.','results':sorted(results,key=lambda x:x['f1'],reverse=True)}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
