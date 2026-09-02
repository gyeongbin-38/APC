import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "adaptive-prompt-compiler" / "SKILL.md"
SOURCES = ROOT / "benchmarks" / "public-repos" / "sources.json"
RESULTS = ROOT / "benchmarks" / "public-repos" / "results.json"


class PublicRepoBenchmarkTests(unittest.TestCase):
    def test_apc_manifest_matches_runtime_skill(self):
        text = SKILL.read_text(encoding="utf-8")
        manifest = json.loads(SOURCES.read_text(encoding="utf-8"))
        apc = manifest["APC"]
        description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE).group(1).strip()
        self.assertEqual(apc["size_bytes"], len(text.encode("utf-8")))
        self.assertEqual(apc["description"], description)

    def test_checked_in_result_has_expected_scope(self):
        result = json.loads(RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(result["cases"], 140)
        self.assertIn("does not measure model answer quality", result["scope"].lower())
        self.assertEqual(result["rows"][0]["name"], "APC")
        self.assertGreaterEqual(len(result["rows"]), 5)


if __name__ == "__main__":
    unittest.main()
