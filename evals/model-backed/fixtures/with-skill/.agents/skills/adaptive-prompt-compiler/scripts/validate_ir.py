#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from compile_prompt import validate
p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
try: ir=json.loads(a.input.read_text(encoding="utf-8"))
except Exception as e: print(f"invalid JSON: {e}",file=sys.stderr); raise SystemExit(2)
errors=validate(ir)
if errors:
    for e in errors: print(e,file=sys.stderr)
    raise SystemExit(1)
print("OK")
