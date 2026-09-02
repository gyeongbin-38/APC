#!/usr/bin/env python3
"""Deterministic fuzz test for hard-constraint literal preservation."""
from __future__ import annotations
import importlib.util, json, random, string
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'skill/adaptive-prompt-compiler/scripts/compile_prompt.py'
spec=importlib.util.spec_from_file_location('compile_prompt',SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
SEED=20260902
N=10000
r=random.Random(SEED)
alphabet=string.ascii_letters+string.digits+" -_:/[](){}.,!?=+@#%&'\""+"한글제약조건禁止必須"
failed=[]
for i in range(N):
    prefix=r.choice(['MUST ','NEVER ','REQUIRED ','금지: ','필수: ',''])
    body=''.join(r.choice(alphabet) for _ in range(r.randint(8,100))).strip() or 'constraint'
    c=f'{prefix}{body}'
    ir={'objective':'Fuzz hard-constraint preservation','hard_constraints':[c], 'complexity':r.choice(['simple','structured','agentic'])}
    out=mod.compile_ir(ir)
    if c not in out:
        failed.append({'index':i,'constraint':c})
        if len(failed)>=10: break
result={'method':'deterministic literal-preservation fuzz; optional emitter only','seed':SEED,'cases':N,'failures':len(failed),'examples':failed,'pass_rate':1-(len(failed)/N)}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
