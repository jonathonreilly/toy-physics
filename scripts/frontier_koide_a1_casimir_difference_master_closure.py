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
    # Phase 1 — schema grade closure
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
    # Phase 2 — retained-grade promotion + brannen P attack + robustness
    "frontier_koide_a1_casimir_difference_p1_formal.py",
    "frontier_koide_a1_casimir_difference_p1_rainbow.py",
    "frontier_koide_a1_casimir_difference_p1_blindness.py",
    "frontier_koide_a1_casimir_difference_p1_promotion.py",
    "frontier_koide_a1_casimir_difference_p2_factorization.py",
    "frontier_koide_a1_casimir_difference_p2_cyclic.py",
    "frontier_koide_a1_casimir_difference_p2_same_topology.py",
    "frontier_koide_a1_casimir_difference_p2_promotion.py",
    "frontier_koide_a1_casimir_difference_c_independence.py",
    "frontier_koide_a1_casimir_difference_mu_invariance.py",
    "frontier_koide_a1_casimir_difference_brannen_p_probe.py",
    "frontier_koide_a1_casimir_difference_brannen_berry.py",
    "frontier_koide_a1_casimir_difference_stress_test.py",
    "frontier_koide_a1_casimir_difference_ytau_composition.py",
    "frontier_koide_a1_casimir_difference_precision_budget.py",
    "frontier_koide_a1_casimir_difference_higgs_consistency.py",
    "frontier_koide_a1_casimir_difference_reviewer_qa.py",
]


def run_one(name: str) -> tuple[int, int, int, int]:
    """Return (returncode, passes, total, docs)."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / name)],
        capture_output=True, text=True, timeout=60,
    )
    mp = re.search(r"PASSED:\s+(\d+)/(\d+)", proc.stdout)
    md = re.search(r"DOCUMENTED:\s+(\d+)", proc.stdout)
    passes, total = (int(mp.group(1)), int(mp.group(2))) if mp else (0, 0)
    docs = int(md.group(1)) if md else 0
    return proc.returncode, passes, total, docs


def main() -> int:
    print("=" * 88)
    print("Master closure runner — Casimir-Difference Lemma derivation track")
    print("=" * 88)
    print()
    print(f"  {'Runner':<58}{'rc':>4}{'PASS':>8}{'DOC':>6}")
    print("  " + "-" * 76)
    total_p = 0
    total_t = 0
    total_d = 0
    rigorous_runners = 0
    doc_only_runners = 0
    failed = []
    for name in STEP_RUNNERS:
        rc, p, t, d = run_one(name)
        if rc != 0 or p != t:
            marker = "✗"
            failed.append(name)
        elif t > 0:
            marker = "✓"
            rigorous_runners += 1
        else:
            marker = "○"
            doc_only_runners += 1
        short = name.replace("frontier_koide_a1_casimir_difference_", "*")
        print(f"  {marker} {short:<56}{rc:>4}{p:>8}{d:>6}")
        total_p += p
        total_t += t
        total_d += d
    print("  " + "-" * 76)
    print(f"  {'TOTAL':<58}{'':>4}{total_p:>3}/{total_t:<4}{total_d:>6}")
    print()
    print("Legend:")
    print("  ✓ = rigorous runner (PASS count > 0, no FAILs)")
    print("  ○ = documentation-only runner (no rigorous PASS checks; narrative only)")
    print("  ✗ = runner with FAIL(s) or non-zero exit code")
    print()
    if not failed:
        print(f"VERDICT: ALL {len(STEP_RUNNERS)} step runners OK ({rigorous_runners} rigorous, "
              f"{doc_only_runners} documentation-only).")
        print(f"         Rigorous PASSes: {total_p}/{total_t}.  Documentation lines: {total_d}.")
        return 0
    print(f"VERDICT: {len(failed)} step runner(s) FAILED:")
    for name in failed:
        print(f"  - {name}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
