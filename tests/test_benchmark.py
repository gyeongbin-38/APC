import json, os, subprocess, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'benchmarks/structural/run_benchmark.py'

class BenchmarkTests(unittest.TestCase):
    def test_benchmark_runs_and_current_architecture_wins(self):
        p=subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data['cases'],1000)
        self.assertEqual(data['results'][0]['candidate'],'adaptive-compiler')

    def test_benchmark_is_stable_across_python_hash_seeds(self):
        outputs=[]
        for hash_seed in ('1','777'):
            env=os.environ.copy()
            env['PYTHONHASHSEED']=hash_seed
            p=subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True,check=True,env=env)
            outputs.append(json.loads(p.stdout))
        self.assertEqual(outputs[0],outputs[1])

if __name__=='__main__': unittest.main()
