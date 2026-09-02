#!/usr/bin/env python3
"""Fail when deterministic benchmark outputs differ semantically from committed evidence."""
from __future__ import annotations

import difflib
import json
import subprocess
from pathlib import Path

FILES = [
    "benchmarks/structural/results.json",
    "benchmarks/trigger-boundary/results.json",
    "benchmarks/constraint-fuzz/results.json",
    "benchmarks/public-repos/results.json",
    "benchmarks/security-adversarial/results.json",
    "benchmarks/security-efficiency/results.json",
]


def load_committed(path: str):
    raw = subprocess.check_output(["git", "show", f"HEAD:{path}"], text=True)
    return json.loads(raw)


def normalized(value) -> list[str]:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).splitlines()


def main() -> int:
    stale = []
    for path in FILES:
        expected = load_committed(path)
        actual = json.loads(Path(path).read_text(encoding="utf-8"))
        if expected != actual:
            stale.append(path)
            print(f"STALE benchmark evidence: {path}")
            for line in difflib.unified_diff(normalized(expected), normalized(actual), fromfile=f"committed/{path}", tofile=f"regenerated/{path}", lineterm=""):
                print(line)
    if stale:
        print("\nRegenerate and commit the changed benchmark results before merging.")
        return 1
    print("Benchmark evidence is fresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
