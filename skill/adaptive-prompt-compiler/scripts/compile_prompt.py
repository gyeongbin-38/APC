#!/usr/bin/env python3
"""Deterministic optional emitter for Adaptive Prompt Compiler IR.

The skill does not require this script. It is useful when an Agent Skills host can
execute Python and a reproducible IR -> prompt emission path is desired.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ALLOWED_COMPLEXITY = {"simple", "structured", "agentic"}
LIST_FIELDS = ("hard_constraints", "preferences", "non_goals", "context", "success_criteria", "verification")
SCALAR_FIELDS = ("objective", "target", "deliverable")
ALLOWED_FIELDS = set(SCALAR_FIELDS) | set(LIST_FIELDS) | {"complexity"}
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_STRING_CHARS = 65_536
MAX_LIST_ITEMS = 256


def validate(ir: dict) -> list[str]:
    errors = []
    if not isinstance(ir, dict):
        return ["IR must be a JSON object"]
    unknown = sorted(set(ir) - ALLOWED_FIELDS)
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")
    for field in SCALAR_FIELDS:
        if field in ir and not isinstance(ir[field], str):
            errors.append(f"{field} must be a string")
        elif isinstance(ir.get(field), str) and len(ir[field]) > MAX_STRING_CHARS:
            errors.append(f"{field} exceeds {MAX_STRING_CHARS} characters")
    if not isinstance(ir.get("objective"), str) or not ir.get("objective", "").strip():
        errors.append("objective must be a non-empty string")
    c = ir.get("complexity")
    if c is not None and c not in ALLOWED_COMPLEXITY:
        errors.append(f"complexity must be one of {sorted(ALLOWED_COMPLEXITY)}")
    for field in LIST_FIELDS:
        if field not in ir:
            continue
        if not isinstance(ir[field], list) or not all(isinstance(x, str) for x in ir[field]):
            errors.append(f"{field} must be an array of strings")
            continue
        if len(ir[field]) > MAX_LIST_ITEMS:
            errors.append(f"{field} exceeds {MAX_LIST_ITEMS} items")
        if any(len(x) > MAX_STRING_CHARS for x in ir[field]):
            errors.append(f"{field} contains an item exceeding {MAX_STRING_CHARS} characters")
    return errors


def bullets(title: str, values: list[str]) -> list[str]:
    if not values:
        return []
    return [f"## {title}", *[f"- {x}" for x in values], ""]


def compile_ir(ir: dict) -> str:
    errors = validate(ir)
    if errors:
        raise ValueError("; ".join(errors))
    complexity = ir.get("complexity", "structured")
    out = ["# Task", "", ir["objective"].strip(), ""]
    if ir.get("target"):
        out += ["## Target", ir["target"].strip(), ""]
    if ir.get("deliverable"):
        out += ["## Deliverable", ir["deliverable"].strip(), ""]
    out += bullets("Hard constraints", ir.get("hard_constraints", []))
    if complexity != "simple":
        out += bullets("Success criteria", ir.get("success_criteria", []))
        out += bullets("Context", ir.get("context", []))
    out += bullets("Preferences", ir.get("preferences", []))
    out += bullets("Out of scope", ir.get("non_goals", []))
    if complexity != "simple":
        out += bullets("Verification", ir.get("verification", []))
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path, help="JSON Prompt IR")
    p.add_argument("-o", "--output", type=Path)
    args = p.parse_args()
    try:
        size = args.input.stat().st_size
    except OSError as e:
        print(f"invalid IR input: {e}", file=sys.stderr)
        return 2
    if size > MAX_INPUT_BYTES:
        print(f"invalid IR: input exceeds {MAX_INPUT_BYTES} bytes", file=sys.stderr)
        return 2
    try:
        ir = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as e:
        print(f"invalid IR input: {e}", file=sys.stderr)
        return 2
    try:
        prompt = compile_ir(ir)
    except ValueError as e:
        print(f"invalid IR: {e}", file=sys.stderr)
        return 2
    if args.output:
        args.output.write_text(prompt, encoding="utf-8")
    else:
        sys.stdout.write(prompt)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
