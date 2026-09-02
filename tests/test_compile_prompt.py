import importlib.util
import json
import random
import string
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skill/adaptive-prompt-compiler/scripts/compile_prompt.py'
spec=importlib.util.spec_from_file_location('compile_prompt',SCRIPT)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class CompileTests(unittest.TestCase):
    def test_example_compiles(self):
        ir=json.loads((ROOT/'examples/ir-coding.json').read_text())
        out=mod.compile_ir(ir)
        self.assertIn('Fix the checkout regression',out)
        self.assertIn('Do not change the public API.',out)
    def test_rejects_missing_objective(self):
        self.assertTrue(mod.validate({'complexity':'simple'}))
    def test_hard_constraint_roundtrip_250(self):
        r=random.Random(20260902)
        for i in range(250):
            marker='HC-'+''.join(r.choice(string.ascii_letters+string.digits+'-_:/ ') for _ in range(28)).strip()
            ir={'objective':'Test exact constraint preservation','hard_constraints':[marker], 'complexity':'structured'}
            out=mod.compile_ir(ir)
            self.assertIn(marker,out)
if __name__=='__main__': unittest.main()
