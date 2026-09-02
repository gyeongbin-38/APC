import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class EvalTests(unittest.TestCase):
    def test_evals(self):
        data=json.loads((ROOT/'evals/evals.json').read_text())
        self.assertEqual(data['skill_name'],'adaptive-prompt-compiler')
        self.assertGreaterEqual(len(data['evals']),20)
        ids=[x['id'] for x in data['evals']]
        self.assertEqual(len(ids),len(set(ids)))
        for x in data['evals']:
            self.assertTrue(x['prompt']); self.assertTrue(x['expected_output']); self.assertTrue(x['expectations'])
    def test_trigger_set_has_both_classes(self):
        d=json.loads((ROOT/'evals/trigger_set.json').read_text())
        self.assertGreaterEqual(sum(x['should_trigger'] for x in d),30)
        self.assertGreaterEqual(sum(not x['should_trigger'] for x in d),25)
if __name__=='__main__': unittest.main()
