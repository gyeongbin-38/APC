import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TriggerBoundaryTests(unittest.TestCase):
    def test_trigger_boundary_proxy(self):
        p=subprocess.run([sys.executable,str(ROOT/'benchmarks/trigger-boundary/run_benchmark.py')],cwd=ROOT,capture_output=True,text=True,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data['results'][0]['description'],'current')
        self.assertGreaterEqual(data['cases'],100)
        self.assertIn('no LLM',data['method'])
if __name__=='__main__': unittest.main()
