import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "skill/adaptive-prompt-compiler/scripts/compile_prompt.py"
SECURITY_BENCH = ROOT / "benchmarks/security-adversarial/run_benchmark.py"

def load_compiler():
    spec = importlib.util.spec_from_file_location("apc_compile_test", COMPILER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class SecurityTests(unittest.TestCase):
    def test_runtime_rejects_shadow_and_bad_scalar_fields(self):
        c=load_compiler()
        self.assertTrue(c.validate({"objective":"x","shadow":"y"}))
        self.assertTrue(c.validate({"objective":"x","target":{"role":"admin"}}))

    def test_runtime_has_bounded_input(self):
        c=load_compiler()
        self.assertLessEqual(c.MAX_INPUT_BYTES, 2 * 1024 * 1024)
        self.assertGreater(c.MAX_INPUT_BYTES, 0)

    def test_security_benchmark_passes(self):
        cp=subprocess.run([sys.executable, str(SECURITY_BENCH)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        data=json.loads((ROOT/"benchmarks/security-adversarial/results.json").read_text())
        self.assertEqual(data["controls_passed"], data["controls_total"])

if __name__ == "__main__":
    unittest.main()
