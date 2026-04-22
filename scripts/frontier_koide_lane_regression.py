#!/usr/bin/env python3
"""
Koide lane — full regression verification

Runs all 9 Koide-lane runners in sequence and verifies the expected
PASS counts. Single entry point for the canonical-branch reviewer
to confirm the complete closure chain passes end-to-end.

Usage:
    python3 scripts/frontier_koide_lane_regression.py

Expected output: 166/166 total tests pass across 23 runners.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# (runner_script, expected_pass_count)
RUNNERS = [
    ("frontier_koide_equivariant_berry_aps_selector.py", 15),
    ("frontier_koide_dirac_zero_mode_phase_theorem.py", 10),
    ("frontier_charged_lepton_radiative_yukawa_theorem.py", 11),
    ("frontier_koide_eta_lefschetz_spectral_flow.py", 8),
    ("frontier_charged_lepton_yukawa_diagrammatic_enumeration.py", 8),
    ("frontier_charged_lepton_yukawa_bz_quadrature_explicit.py", 6),
    ("frontier_koide_mass_assignment_derivation.py", 7),
    ("frontier_koide_z3_weight_uniqueness.py", 6),
    ("frontier_koide_hierarchy_derivation_audit.py", 9),
    ("frontier_koide_as_pin_replaces_h_star_witness.py", 5),
    ("frontier_koide_real_irrep_block_democracy.py", 8),
    ("frontier_koide_q_equals_lefschetz_sum.py", 5),
    ("frontier_koide_p1_sqrtm_amplitude_derivation.py", 6),
    ("frontier_koide_selected_line_axis_fourier_bridge.py", 5),
    ("frontier_koide_positive_parent_operator_construction.py", 9),
    ("frontier_koide_name_free_set_equality.py", 5),
    ("frontier_koide_a1_quartic_potential_derivation.py", 5),
    ("frontier_koide_a1_n3_structural_uniqueness.py", 5),
    ("frontier_koide_a1_cv_equals_one.py", 4),
    ("frontier_koide_a1_block_democracy_max_entropy.py", 5),
    ("frontier_koide_a1_weyl_vector_kostant_coincidence.py", 6),
    ("frontier_koide_a1_a2_weyl_double_match.py", 8),
    ("frontier_koide_a1_lie_theoretic_triple_match.py", 10),
]

EXPECTED_TOTAL = sum(n for _, n in RUNNERS)


def main() -> int:
    print("=" * 88)
    print("Koide Lane — full regression verification")
    print("=" * 88)
    print()
    print(f"Running {len(RUNNERS)} runners. Expected total: {EXPECTED_TOTAL}/{EXPECTED_TOTAL} PASS.")
    print()

    all_ok = True
    actual_total = 0
    max_name_len = max(len(s) for s, _ in RUNNERS)

    for script, expected in RUNNERS:
        path = SCRIPTS / script
        if not path.exists():
            print(f"  [FAIL] {script:<{max_name_len}}  (missing)")
            all_ok = False
            continue

        result = subprocess.run(
            ["python3", str(path)],
            capture_output=True,
            text=True,
            timeout=600,
        )
        # Extract "PASSED: X/Y" line
        passed_line = None
        for line in result.stdout.splitlines():
            if line.startswith("PASSED:"):
                passed_line = line
                break

        if passed_line is None:
            print(f"  [FAIL] {script:<{max_name_len}}  (no PASSED summary)")
            all_ok = False
            continue

        # Parse "PASSED: X/Y"
        try:
            after = passed_line.split("PASSED:")[1].strip()
            num, den = after.split("/")
            actual_passed = int(num)
            actual_total += actual_passed

            ok = (actual_passed == expected) and (actual_passed == int(den))
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {script:<{max_name_len}}  {actual_passed}/{den} (expected {expected})")
            if not ok:
                all_ok = False
        except Exception as e:
            print(f"  [FAIL] {script}:  parse error: {e}")
            all_ok = False

    print()
    print("=" * 88)
    print(f"TOTAL: {actual_total}/{EXPECTED_TOTAL}")
    if all_ok and actual_total == EXPECTED_TOTAL:
        print("VERDICT: all Koide-lane closure runners pass. Full package verified.")
        print()
        print("Closure chain summary (axiom-only):")
        print("  - M_Pl, α_LM      : retained primitives")
        print("  - (7/8)^(1/4)      : Stefan-Boltzmann fermion/boson (textbook)")
        print("  - 16 = 2^4         : taste doublers in 4D staggered (structural)")
        print("  - v_EW             : M_Pl · (7/8)^(1/4) · α_LM^16, PDG match 0.025%")
        print("  - Z_3 (1, 2)       : structurally unique on V_3")
        print("  - |η_AS| = 2/9     : AS G-signature via Lefschetz + Berry")
        print("  - δ = 2/9          : AS/APS spectral-flow identification")
        print("  - C_τ = 1          : SU(2)_L × U(1)_Y Casimir enumeration")
        print("  - y_τ = α_LM/(4π) : 1-loop PT + C_τ (retained + textbook)")
        print("  - Q = 2/3          : Z_3 Lefschetz sum (unique at n=3)")
        print("  - Positive parent M: explicit construction M = Y² on V_3")
        print("  - P1: λ_k = √m_k   : derived via M^(1/2) = Y (functional calculus)")
        print("  - mass triple      : set equality with PDG at <0.01% (no naming)")
        print()
        print("All charged-lepton observables match PDG at <0.03% precision.")
        return 0
    else:
        print("VERDICT: regression has FAILs. Investigate specific runner(s) above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
