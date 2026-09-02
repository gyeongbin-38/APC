import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BenchmarkTests(unittest.TestCase):
    def test_benchmark_runs_and_current_architecture_wins(self):
        p=subprocess.run([sys.executable,str(ROOT/'benchmarks/structural/run_benchmark.py')],capture_output=True,text=True,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data['cases'],1000)
        self.assertEqual(data['results'][0]['candidate'],'adaptive-compiler')
if __name__=='__main__': unittest.main()
