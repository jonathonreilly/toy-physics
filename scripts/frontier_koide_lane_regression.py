#!/usr/bin/env python3
"""
Koide lane — support regression verification

Runs the expanded Koide support batch in sequence and verifies the expected
PASS counts. This is a reviewer-facing aggregation runner for the current
charged-lepton support package, not a proof that Koide is fully closed.

Usage:
    python3 scripts/frontier_koide_lane_regression.py

Expected output: all listed support runners pass with their current totals.
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
    ("frontier_koide_brannen_route3_geometry_support.py", 30),
    ("frontier_koide_brannen_dirac_support.py", 11),
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
    ("frontier_koide_pointed_origin_exhaustion_theorem.py", 15),
    ("frontier_koide_dimensionless_objection_closure_review.py", 21),
    ("frontier_koide_q_background_zero_z_erasure_criterion.py", 25),
    ("frontier_koide_q_onsite_source_domain_no_go_synthesis.py", 23),
    ("frontier_koide_q_source_domain_canonical_descent.py", 55),
    ("frontier_koide_a1_radian_bridge_irreducibility_audit.py", 36),
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
        print("VERDICT: all Koide-lane support runners pass. Support batch verified.")
        print()
        print("Support-batch summary:")
        print("  - M_Pl, α_LM      : retained primitives")
        print("  - (7/8)^(1/4)      : Stefan-Boltzmann fermion/boson (textbook)")
        print("  - 16 = 2^4         : taste doublers in 4D staggered (structural)")
        print("  - v_EW             : M_Pl · (7/8)^(1/4) · α_LM^16, PDG match 0.025%")
        print("  - Z_3 (1, 2)       : structurally unique on V_3")
        print("  - |η_AS| = 2/9     : ambient APS value fixed exactly")
        print("  - zero-mode / APS  : strengthened candidate bridge to physical δ")
        print("  - Brannen geometry : exact selected-line rotation / octahedral-domain")
        print("                      support on the retained first branch")
        print("  - finite-lattice   : explicit L=3 Wilson-Dirac descent illustration")
        print("                      for the ambient 2/9 value")
        print("  - C_τ = 1 route    : explicit radiative/Yukawa support calculation")
        print("  - Q = 2/3 support  : exact identities, A1 audits, bridge candidates")
        print("  - positive-parent, selected-line, and set-equality tools")
        print("                      : added as support diagnostics and atlas tools")
        print("  - pointed-origin    : exhaustion theorem shows origin-free retained data")
        print("                      cannot select the closing representative")
        print("  - objection review  : source-domain closure demoted to conditional")
        print("                      support with explicit Q and delta residuals")
        print("  - Q Z-erasure       : exact criterion K=0 <=> Z-erasure <=> Q=2/3")
        print("                      on the admitted reduced carrier")
        print("  - Q source domain   : onsite C3 scalar sources erase Z conditionally,")
        print("                      but retained commutant/projected sources still admit Z")
        print("  - Q descent         : unique trace-preserving onsite descent is diagonal")
        print("                      compression and erases reduced Z modulo common scalar")
        print("  - A1/radian audit   : retained phase sources remain q*pi; Type-B")
        print("                      rational-to-radian readout remains primitive")
        print()
        print("Open package status is unchanged:")
        print("  - physical source-domain / source-free reduced-carrier selection behind Q = 2/3 remains open")
        print("  - selected-line local boundary source plus based endpoint behind δ = 2/9 remains open")
        print("  - Type-B rational-to-radian readout behind δ = 2/9 remains open")
        print("  - overall scale lane v_0 remains separate support")
        return 0
    else:
        print("VERDICT: regression has FAILs. Investigate specific runner(s) above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
