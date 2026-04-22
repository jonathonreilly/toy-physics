#!/usr/bin/env python3
"""
Master closure runner for the Casimir-Difference Lemma derivation track.

Re-executes every step runner on the branch and produces an aggregate
PASS/FAIL summary. Returns 0 iff every step runner returns 0.

Used as the canonical "did this whole track close?" check.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"

STEP_RUNNERS = [
    "frontier_koide_a1_casimir_difference_lemma_skeleton.py",
    "frontier_koide_a1_casimir_difference_o1a_c3_plancherel.py",
    "frontier_koide_a1_casimir_difference_o1b_hw1_s3_alignment.py",
    "frontier_koide_a1_casimir_difference_o1c_mass_matrix_split.py",
    "frontier_koide_a1_casimir_difference_o2a_sum_enumeration.py",
    "frontier_koide_a1_casimir_difference_o2b_trivial_weight.py",
    "frontier_koide_a1_casimir_difference_o2c_constant_pin.py",
    "frontier_koide_a1_casimir_difference_o3a_offdiag_enumeration.py",
    "frontier_koide_a1_casimir_difference_o3b_same_loop.py",
    "frontier_koide_a1_casimir_difference_o3c_same_c.py",
    "frontier_koide_a1_casimir_difference_x1_uniqueness_sweep.py",
    "frontier_koide_a1_casimir_difference_x2_perturbation_test.py",
    "frontier_koide_a1_casimir_difference_x3_iff.py",
    "frontier_koide_a1_casimir_difference_x4_compose_hw1_theorem1.py",
    "frontier_koide_a1_casimir_difference_x5_no_go_evasion.py",
    "frontier_koide_a1_casimir_difference_x6_brannen_corollary.py",
    "frontier_koide_a1_casimir_difference_x7_existing_runner_consistency.py",
]


def run_one(name: str) -> tuple[int, int, int]:
    """Return (returncode, passes, total)."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / name)],
        capture_output=True, text=True, timeout=60,
    )
    m = re.search(r"PASSED:\s+(\d+)/(\d+)", proc.stdout)
    if not m:
        return proc.returncode, 0, 0
    return proc.returncode, int(m.group(1)), int(m.group(2))


def main() -> int:
    print("=" * 88)
    print("Master closure runner — Casimir-Difference Lemma derivation track")
    print("=" * 88)
    print()
    print(f"  {'Runner':<58}{'rc':>4}{'PASS':>8}{'TOTAL':>8}")
    print("  " + "-" * 78)
    total_p = 0
    total_t = 0
    bad = []
    for name in STEP_RUNNERS:
        rc, p, t = run_one(name)
        marker = "✓" if (rc == 0 and p == t and t > 0) else "✗"
        # Strip the long prefix for display
        short = name.replace("frontier_koide_a1_casimir_difference_", "*")
        print(f"  {marker} {short:<56}{rc:>4}{p:>8}{t:>8}")
        total_p += p
        total_t += t
        if rc != 0 or p != t:
            bad.append(name)
    print("  " + "-" * 78)
    print(f"  TOTAL{'':>53}     {total_p:>8}/{total_t}")
    print()
    if not bad:
        print(f"VERDICT: ALL {len(STEP_RUNNERS)} step runners PASS — track closes ({total_p}/{total_t}).")
        return 0
    print(f"VERDICT: {len(bad)} step runner(s) FAILED:")
    for name in bad:
        print(f"  - {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
