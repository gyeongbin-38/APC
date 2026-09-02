import re, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skill/adaptive-prompt-compiler/SKILL.md'
class LayoutTests(unittest.TestCase):
    def test_skill_frontmatter_and_size(self):
        text=SKILL.read_text(encoding='utf-8'); self.assertTrue(text.startswith('---\n'))
        m=re.match(r'^---\n(.*?)\n---\n',text,re.S); self.assertIsNotNone(m); fm=m.group(1)
        name=re.search(r'^name:\s*(.+)$',fm,re.M).group(1).strip(); desc=re.search(r'^description:\s*(.+)$',fm,re.M).group(1).strip()
        self.assertEqual(name,SKILL.parent.name); self.assertRegex(name,r'^[a-z0-9]+(?:-[a-z0-9]+)*$'); self.assertLessEqual(len(name),64); self.assertLessEqual(len(desc),1024); self.assertLessEqual(len(text.splitlines()),500)
    def test_reference_paths_exist(self):
        text=SKILL.read_text(encoding='utf-8'); refs=re.findall(r'`(references/[^`]+\.md)`',text); self.assertTrue(refs)
        for ref in refs: self.assertTrue((SKILL.parent/ref).exists(),ref)
if __name__=='__main__': unittest.main()
