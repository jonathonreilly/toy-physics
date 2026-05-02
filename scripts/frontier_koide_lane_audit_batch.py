#!/usr/bin/env python3
"""Koide-lane audit batch verification."""

import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "KOIDE_LANE_AUDIT_BATCH_NOTE_2026-05-02.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label, ok, detail=""):
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS (A)" if ok else "FAIL (A)"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


section("Part 1: audit batch structure")
note_text = NOTE_PATH.read_text()
required = [
    "Koide Lane Audit Batch",
    "charged_lepton_koide_ratio_source_selector_firewall_note_2026-04-27",
    "koide_berry_phase_theorem_note_2026-04-19",
    "charged_lepton_koide_cone_algebraic_equivalence_note",
    "Cluster observation",
    "fourth instance",
    "lattice → physical",  # multiline-wrapped phrase
]
for s in required:
    check(f"contains: {s!r}", s in note_text)


section("Part 2: re-verify the two passing runners")
runners = [
    ("frontier_charged_lepton_koide_ratio_source_selector_firewall.py", "PASS=35"),
    ("frontier_koide_berry_phase_theorem.py", "PASS=24"),
]
for runner, expected_pass in runners:
    runner_path = ROOT / "scripts" / runner
    if not runner_path.exists():
        check(f"{runner} exists", False, detail=f"path = {runner_path}")
        continue
    try:
        result = subprocess.run(
            ["python3", str(runner_path)],
            capture_output=True, text=True, timeout=120,
            cwd=str(ROOT),
            env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "scripts")},
        )
        out = result.stdout + result.stderr
        if expected_pass in out:
            check(f"{runner} re-verified {expected_pass}", True,
                  detail="re-run passed")
        else:
            check(f"{runner} re-verified {expected_pass}", False,
                  detail=f"output last 100 chars: {out[-100:].strip()!r}")
    except subprocess.TimeoutExpired:
        check(f"{runner} timeout", False, detail="120s")
    except Exception as e:
        check(f"{runner} exception", False, detail=str(e))


section("Part 3: confirm 3rd note's runner missing")
missing_runner = ROOT / "scripts" / "frontier_charged_lepton_koide_cone_algebraic_equivalence.py"
check("third Koide note's runner is missing (as documented)",
      not missing_runner.exists(),
      detail=f"path = {missing_runner}")


section("Part 4: cluster cross-references")
cluster_refs = ["cycle 5", "cycle 9", "cycle 11", "cycle 13", "#260", "#268", "#271", "#274"]
for c in cluster_refs:
    check(f"cluster ref: {c}", c in note_text)


print(f"\n{'='*88}\n  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}\n{'='*88}")
sys.exit(1 if FAIL_COUNT > 0 else 0)
