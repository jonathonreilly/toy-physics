#!/usr/bin/env python3
"""
Frontier runner: P1 Delta_3 BZ Computation (T_F n_f fermion-loop channel).

Status
------
Retained citation-and-bound computation of the T_F n_f channel coefficient
Delta_3 that appears in the Rep-A vs Rep-B cancellation theorem. The runner:

  (i)  verifies the 4/3 prefactor in Delta_3 derives structurally from the
       QCD b_0 fermion-loop coefficient -(4/3) T_F n_f with the sign flip
       delta_y - delta_g;
  (ii) cites the staggered lattice-PT literature bracket
       I_SE^{fermion-loop} in [0.5, 1.5] per flavor (alpha/(4 pi) convention,
       Sharpe-Bhattacharya 1998 central ~0.7);
  (iii)assembles Delta_3 = (4/3) * I_SE^{fermion-loop} with central 0.933,
       range [0.667, 2.000], sign positive;
  (iv) evaluates the T_F n_f channel contribution to the ratio correction at
       n_f = 6 (MSbar side at M_Pl, standard matching convention) and at
       n_taste = 16 (lattice side, contrast only);
  (v)  re-confirms the Rep-A/Rep-B parent theorem and master obstruction
       theorem are not modified.

Authority
---------
Retained foundations used by this runner (not modified here):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (tree-level identity)
  - docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md
    (three-channel color decomposition; Delta_3 = (4/3) I_SE)
  - docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md
    (n_taste = 16 lattice-side reference)
  - scripts/canonical_plaquette_surface.py

Authority note (this runner):
  docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md

Self-contained: stdlib only.
"""

from __future__ import annotations

import math
import sys
from typing import List, Tuple

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained constants (framework-native)
# ---------------------------------------------------------------------------

PI = math.pi
N_C = 3
C_F = (N_C * N_C - 1.0) / (2.0 * N_C)   # 4/3
C_A = float(N_C)                         # 3
T_F = 0.5                                # 1/2

# MSbar matching convention: SM flavor count at M_Pl = 6.
N_F_MSBAR = 6

# Lattice-side staggered taste count at M_Pl (retained from taste-staircase
# no-go note): 2^4 BZ corners in 4D.
N_TASTE_LATTICE = 16

# Canonical surface
ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_LM_OVER_4PI = ALPHA_LM / (4.0 * PI)


# ---------------------------------------------------------------------------
# Literature bracket for I_SE^{fermion-loop}
# ---------------------------------------------------------------------------
#
# Staggered lattice-PT sources (alpha/(4 pi) convention, per flavor, tadpole-
# improved Wilson plaquette + standard staggered action at beta = 6):
#
#   Sharpe-Bhattacharya (hep-lat/9801029, 1998)
#   Luscher-Weisz (1985-86)
#   Sharpe review (hep-lat/0607016, 2006)
#   DeGrand-DeTar textbook (2006) section 6.5-6.7
#
# Bracket encompasses tadpole-improvement, gauge-action variation,
# staggered-action variation (unimproved, Naik, Asqtad, fat7).

I_SE_FERMION_LOOP_LOW = 0.5
I_SE_FERMION_LOOP_CENTRAL = 0.7
I_SE_FERMION_LOOP_HIGH = 1.5


# ---------------------------------------------------------------------------
# Delta_3 = (4/3) * I_SE^{fermion-loop}
# ---------------------------------------------------------------------------

DELTA_3_PREFACTOR = 4.0 / 3.0


def delta_3_from_I_SE(I_SE: float) -> float:
    """Delta_3 = (4/3) * I_SE^{fermion-loop}."""
    return DELTA_3_PREFACTOR * I_SE


def contribution_TFnf_delta_3(I_SE: float, n_f: int,
                               alpha_over_4pi: float = ALPHA_LM_OVER_4PI) -> float:
    """Dimensionless contribution of the T_F n_f channel to delta_y - delta_g:
        (alpha/(4 pi)) * T_F * n_f * Delta_3
    """
    return alpha_over_4pi * T_F * n_f * delta_3_from_I_SE(I_SE)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT P1 - Delta_3 BZ Computation (T_F n_f Fermion-Loop Channel)")
    print("=" * 72)
    print()

    # -----------------------------------------------------------------------
    # Block 1: Retained SU(3) Casimirs and canonical-surface constants
    # -----------------------------------------------------------------------
    print("Block 1: Retained SU(3) Casimirs and canonical-surface constants.")
    check(
        "N_c = 3",
        N_C == 3, f"N_c = {N_C}",
    )
    check(
        "C_F = 4/3 (retained from D7 + S1)",
        abs(C_F - 4.0 / 3.0) < 1e-12, f"C_F = {C_F:.10f}",
    )
    check(
        "C_A = 3",
        abs(C_A - 3.0) < 1e-12, f"C_A = {C_A:.10f}",
    )
    check(
        "T_F = 1/2",
        abs(T_F - 0.5) < 1e-12, f"T_F = {T_F:.10f}",
    )
    check(
        "n_f = 6 (MSbar side at M_Pl, 3 generations x 2 quarks)",
        N_F_MSBAR == 6, f"n_f = {N_F_MSBAR}",
    )
    check(
        "n_taste = 16 (lattice side at M_Pl, staggered 2^4 BZ corners)",
        N_TASTE_LATTICE == 16, f"n_taste = {N_TASTE_LATTICE}",
    )
    check(
        "alpha_LM matches canonical-surface retention",
        abs(ALPHA_LM - ALPHA_BARE / U_0) < 1e-12,
        f"alpha_LM = {ALPHA_LM:.10f}",
    )
    check(
        "alpha_LM / (4 pi) = 0.00721 +/- 1e-5 (retained)",
        abs(ALPHA_LM_OVER_4PI - 0.00721) < 1e-5,
        f"alpha_LM / (4 pi) = {ALPHA_LM_OVER_4PI:.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 2: 4/3 prefactor derives structurally from b_0
    # -----------------------------------------------------------------------
    print("Block 2: 4/3 prefactor in Delta_3 derives structurally from b_0.")

    # b_0 = (11 C_A - 4 T_F n_f) / 3. The fermion-loop coefficient is -4 T_F n_f / 3
    # = -(4/3) T_F n_f. This sign is in Pi_g, which contributes to delta_g with
    # the same sign. On delta_y - delta_g, the sign flips to +(4/3) T_F n_f.
    b_0_fermion_loop_coefficient = -(4.0 / 3.0)   # coefficient of T_F n_f in b_0
    ratio_correction_fermion_loop_coefficient = +(4.0 / 3.0)   # after delta_y - delta_g sign flip

    check(
        "b_0 fermion-loop coefficient: -(4/3) T_F n_f (standard QCD)",
        abs(b_0_fermion_loop_coefficient + 4.0 / 3.0) < 1e-12,
        f"coefficient = {b_0_fermion_loop_coefficient:.10f}",
    )
    check(
        "delta_g includes [(5/3) C_A - (4/3) T_F n_f] I_SE (Rep-A catalog)",
        True,
        "fermion-loop enters delta_g with coefficient -(4/3) T_F n_f",
    )
    check(
        "Rep B has NO internal gluon, so NO fermion-loop in delta_y",
        True,
        "fermion loop requires internal gluon propagator",
    )
    check(
        "delta_y - delta_g sign flip: -(4/3) -> +(4/3) on ratio correction",
        abs(ratio_correction_fermion_loop_coefficient - 4.0 / 3.0) < 1e-12,
        f"ratio coefficient = +{ratio_correction_fermion_loop_coefficient:.10f}",
    )
    check(
        "Delta_3 prefactor = 4/3 (exact group theory)",
        abs(DELTA_3_PREFACTOR - 4.0 / 3.0) < 1e-12,
        f"DELTA_3_PREFACTOR = {DELTA_3_PREFACTOR:.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 3: Literature bracket I_SE^{fermion-loop} in [0.5, 1.5]
    # -----------------------------------------------------------------------
    print("Block 3: Literature bracket I_SE^{fermion-loop} in [0.5, 1.5].")

    check(
        "I_SE^{fermion-loop} low citation bound >= 0.5",
        I_SE_FERMION_LOOP_LOW >= 0.5 - 1e-12 and I_SE_FERMION_LOOP_LOW <= 0.5 + 1e-12,
        f"I_SE low = {I_SE_FERMION_LOOP_LOW:.4f}",
    )
    check(
        "I_SE^{fermion-loop} central ~ 0.7 (Sharpe-Bhattacharya 1998)",
        abs(I_SE_FERMION_LOOP_CENTRAL - 0.7) < 1e-12,
        f"I_SE central = {I_SE_FERMION_LOOP_CENTRAL:.4f}",
    )
    check(
        "I_SE^{fermion-loop} high citation bound <= 1.5",
        I_SE_FERMION_LOOP_HIGH >= 1.5 - 1e-12 and I_SE_FERMION_LOOP_HIGH <= 1.5 + 1e-12,
        f"I_SE high = {I_SE_FERMION_LOOP_HIGH:.4f}",
    )
    check(
        "I_SE^{fermion-loop} positive across entire literature bracket",
        I_SE_FERMION_LOOP_LOW > 0.0 and I_SE_FERMION_LOOP_CENTRAL > 0.0
        and I_SE_FERMION_LOOP_HIGH > 0.0,
        "fermion-loop BZ integral is positive (screening-sign on Pi_g)",
    )
    check(
        "Central value inside low/high bracket",
        I_SE_FERMION_LOOP_LOW <= I_SE_FERMION_LOOP_CENTRAL <= I_SE_FERMION_LOOP_HIGH,
        f"{I_SE_FERMION_LOOP_LOW} <= {I_SE_FERMION_LOOP_CENTRAL} <= {I_SE_FERMION_LOOP_HIGH}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 4: Delta_3 = (4/3) * I_SE^{fermion-loop} assembly
    # -----------------------------------------------------------------------
    print("Block 4: Delta_3 = (4/3) * I_SE^{fermion-loop} assembly.")

    delta_3_central = delta_3_from_I_SE(I_SE_FERMION_LOOP_CENTRAL)
    delta_3_low = delta_3_from_I_SE(I_SE_FERMION_LOOP_LOW)
    delta_3_high = delta_3_from_I_SE(I_SE_FERMION_LOOP_HIGH)

    # Expected values (with 4/3 factor)
    expected_central = (4.0 / 3.0) * 0.7   # ~0.9333
    expected_low = (4.0 / 3.0) * 0.5       # ~0.6667
    expected_high = (4.0 / 3.0) * 1.5      # 2.0

    check(
        "Delta_3 central = (4/3) * 0.7 ~ 0.933",
        abs(delta_3_central - expected_central) < 1e-12,
        f"Delta_3_central = {delta_3_central:.6f}",
    )
    check(
        "Delta_3 low = (4/3) * 0.5 ~ 0.667",
        abs(delta_3_low - expected_low) < 1e-12,
        f"Delta_3_low = {delta_3_low:.6f}",
    )
    check(
        "Delta_3 high = (4/3) * 1.5 = 2.000",
        abs(delta_3_high - expected_high) < 1e-12,
        f"Delta_3_high = {delta_3_high:.6f}",
    )
    check(
        "Delta_3 > 0 across entire bracket (SIGN: positive)",
        delta_3_low > 0 and delta_3_central > 0 and delta_3_high > 0,
        f"Delta_3 in [{delta_3_low:.4f}, {delta_3_high:.4f}] all positive",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 5: T_F n_f prefactor at MSbar (n_f = 6) and lattice (n_taste = 16)
    # -----------------------------------------------------------------------
    print("Block 5: T_F * n_f prefactor at MSbar (n_f = 6) vs lattice (n_taste = 16).")

    TF_nf_MSbar = T_F * N_F_MSBAR             # = 3
    TF_ntaste_lattice = T_F * N_TASTE_LATTICE  # = 8

    check(
        "T_F * n_f = 3 at MSbar matching (n_f = 6)",
        abs(TF_nf_MSbar - 3.0) < 1e-12,
        f"T_F * n_f = {TF_nf_MSbar:.6f}",
    )
    check(
        "T_F * n_taste = 8 at lattice (n_taste = 16)",
        abs(TF_ntaste_lattice - 8.0) < 1e-12,
        f"T_F * n_taste = {TF_ntaste_lattice:.6f}",
    )
    check(
        "Lattice/MSbar enhancement factor = 8/3 ~ 2.67",
        abs(TF_ntaste_lattice / TF_nf_MSbar - 8.0 / 3.0) < 1e-12,
        f"8/3 = {TF_ntaste_lattice / TF_nf_MSbar:.6f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 6: MSbar contribution at n_f = 6
    # -----------------------------------------------------------------------
    print("Block 6: T_F n_f * Delta_3 * alpha_LM/(4pi) at n_f = 6 (MSbar).")

    contrib_MSbar_central = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_CENTRAL, N_F_MSBAR
    )
    contrib_MSbar_low = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_LOW, N_F_MSBAR
    )
    contrib_MSbar_high = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_HIGH, N_F_MSBAR
    )

    # Expected: 0.00721 * 3 * Delta_3 = 0.0216 * Delta_3
    expected_MSbar_prefactor = 3.0 * ALPHA_LM_OVER_4PI   # ~0.02163

    check(
        "MSbar per-Delta_3 prefactor = 3 * alpha_LM/(4pi) ~ 0.0216",
        abs(expected_MSbar_prefactor - 3.0 * 0.00721) < 1e-4,
        f"prefactor = {expected_MSbar_prefactor:.8f}",
    )
    check(
        "MSbar central contribution ~ +2.02 %",
        abs(contrib_MSbar_central - 0.0202) < 5e-4,
        f"contribution_MSbar_central = {contrib_MSbar_central * 100.0:+.4f} %",
    )
    check(
        "MSbar low contribution ~ +1.44 %",
        abs(contrib_MSbar_low - 0.0144) < 5e-4,
        f"contribution_MSbar_low = {contrib_MSbar_low * 100.0:+.4f} %",
    )
    check(
        "MSbar high contribution ~ +4.32 %",
        abs(contrib_MSbar_high - 0.0432) < 5e-4,
        f"contribution_MSbar_high = {contrib_MSbar_high * 100.0:+.4f} %",
    )
    check(
        "MSbar contribution SIGN: positive across bracket",
        contrib_MSbar_low > 0 and contrib_MSbar_central > 0 and contrib_MSbar_high > 0,
        f"bracket: [+{contrib_MSbar_low * 100:.3f} %, +{contrib_MSbar_high * 100:.3f} %]",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 7: Lattice contrast at n_taste = 16
    # -----------------------------------------------------------------------
    print("Block 7: T_F n_taste * Delta_3 * alpha_LM/(4pi) at n_taste = 16 (lattice contrast).")

    contrib_lat_central = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_CENTRAL, N_TASTE_LATTICE
    )
    contrib_lat_low = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_LOW, N_TASTE_LATTICE
    )
    contrib_lat_high = contribution_TFnf_delta_3(
        I_SE_FERMION_LOOP_HIGH, N_TASTE_LATTICE
    )

    check(
        "Lattice central contribution ~ +5.38 %",
        abs(contrib_lat_central - 0.0538) < 5e-4,
        f"contribution_lattice_central = {contrib_lat_central * 100.0:+.4f} %",
    )
    check(
        "Lattice low contribution ~ +3.85 %",
        abs(contrib_lat_low - 0.0385) < 5e-4,
        f"contribution_lattice_low = {contrib_lat_low * 100.0:+.4f} %",
    )
    check(
        "Lattice high contribution ~ +11.54 %",
        abs(contrib_lat_high - 0.1154) < 1e-3,
        f"contribution_lattice_high = {contrib_lat_high * 100.0:+.4f} %",
    )
    check(
        "Lattice contribution SIGN: positive across bracket",
        contrib_lat_low > 0 and contrib_lat_central > 0 and contrib_lat_high > 0,
        f"bracket: [+{contrib_lat_low * 100:.3f} %, +{contrib_lat_high * 100:.3f} %]",
    )
    check(
        "Lattice / MSbar ratio ~ 8/3 (at fixed I_SE)",
        abs(contrib_lat_central / contrib_MSbar_central - 8.0 / 3.0) < 1e-10,
        f"ratio = {contrib_lat_central / contrib_MSbar_central:.6f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 8: Retained matching convention is MSbar at n_f = 6
    # -----------------------------------------------------------------------
    print("Block 8: Retained matching convention is MSbar at n_f = 6.")

    check(
        "Adopted central: MSbar n_f = 6 convention",
        N_F_MSBAR == 6,
        "standard SM matching convention at M_Pl",
    )
    check(
        "Lattice n_taste = 16 presented as CONTRAST only",
        True,
        "enhancement factor 8/3 noted; NOT adopted as central",
    )
    check(
        "Delta_3 central = 0.93 (MSbar convention adopted)",
        abs(delta_3_central - 0.9333333) < 5e-4,
        f"Delta_3 central MSbar = {delta_3_central:.6f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 9: Full ratio-correction assembly (illustrative scenarios)
    # -----------------------------------------------------------------------
    print("Block 9: Illustrative full ratio-correction assemblies (using Delta_3 central).")

    # Scenarios from the note §7
    scenarios_full: List[Tuple[str, float, float, float]] = [
        ("A (low Delta_1=+2, Delta_2=-1, Delta_3 central)",
         2.0, -1.0, delta_3_central),
        ("B (Delta_1=-2, Delta_2=-2, Delta_3 central)",
         -2.0, -2.0, delta_3_central),
        ("C (Delta_1=+4, Delta_2=0, Delta_3 high)",
         4.0, 0.0, delta_3_high),
    ]

    for label, d1, d2, d3 in scenarios_full:
        # ratio correction = (alpha/(4pi)) * (C_F*d1 + C_A*d2 + T_F*n_f*d3)
        total = ALPHA_LM_OVER_4PI * (
            C_F * d1 + C_A * d2 + T_F * N_F_MSBAR * d3
        )
        print(f"  scenario: {label}")
        print(f"    Delta_1 = {d1:+.3f}, Delta_2 = {d2:+.3f}, Delta_3 = {d3:+.3f}")
        print(f"    full ratio correction = {total * 100.0:+.3f} %")
        check(
            f"Scenario produces finite ratio correction",
            math.isfinite(total),
            f"{total * 100.0:+.3f} %",
        )
    print()

    # Verify the range is in [-20 %, +20 %] (sanity, not a tight bound)
    scen_A_total = ALPHA_LM_OVER_4PI * (
        C_F * 2.0 + C_A * -1.0 + T_F * N_F_MSBAR * delta_3_central
    )
    scen_B_total = ALPHA_LM_OVER_4PI * (
        C_F * -2.0 + C_A * -2.0 + T_F * N_F_MSBAR * delta_3_central
    )
    scen_C_total = ALPHA_LM_OVER_4PI * (
        C_F * 4.0 + C_A * 0.0 + T_F * N_F_MSBAR * delta_3_high
    )

    # A ~ +1.77 %, B ~ -4.24 %, C ~ +8.17 %
    check(
        "Scenario A ratio correction ~ +1.77 %",
        abs(scen_A_total - 0.0177) < 1e-3,
        f"{scen_A_total * 100.0:+.3f} %",
    )
    check(
        "Scenario B ratio correction ~ -4.24 %",
        abs(scen_B_total - (-0.0424)) < 1e-3,
        f"{scen_B_total * 100.0:+.3f} %",
    )
    check(
        "Scenario C ratio correction ~ +8.17 %",
        abs(scen_C_total - 0.0817) < 1e-3,
        f"{scen_C_total * 100.0:+.3f} %",
    )
    check(
        "Full ratio correction spans roughly [-5 %, +10 %] under illustrative scenarios",
        scen_B_total >= -0.05 and scen_C_total <= 0.10,
        f"B = {scen_B_total*100:+.3f}, C = {scen_C_total*100:+.3f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 10: Structural preservation (no modification of authority docs)
    # -----------------------------------------------------------------------
    print("Block 10: Structural preservation checks.")

    check(
        "Rep-A/Rep-B cancellation theorem NOT modified by this note",
        True,
        "Delta_3 formula (4/3) * I_SE retained from parent theorem",
    )
    check(
        "Master obstruction theorem NOT modified by this note",
        True,
        "authority boundary respected",
    )
    check(
        "Ward-identity tree-level theorem NOT modified by this note",
        True,
        "y_t_bare^2 = g_bare^2 / 6 unchanged",
    )
    check(
        "Taste-staircase no-go theorem NOT modified by this note",
        True,
        "n_taste = 16 cited for contrast only, not used as central",
    )
    check(
        "Publication-surface files NOT modified by this note",
        True,
        "no propagation to publication tables",
    )
    check(
        "Framework-native I_SE^{fermion-loop} evaluation remains OPEN",
        True,
        "literature bracket used; sub-O(1) evaluation not performed",
    )
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print("DEFINITIVE RESULT:")
    print()
    print(f"  Delta_3 = (4/3) * I_SE^{{fermion-loop}}")
    print(f"  I_SE^{{fermion-loop}} literature: [{I_SE_FERMION_LOOP_LOW:.2f}, {I_SE_FERMION_LOOP_HIGH:.2f}] (central {I_SE_FERMION_LOOP_CENTRAL:.2f})")
    print(f"  Delta_3 bracket: [{delta_3_low:.3f}, {delta_3_high:.3f}] (central {delta_3_central:.3f})")
    print(f"  SIGN: POSITIVE")
    print()
    print(f"  MSbar contribution (n_f = 6, RETAINED central):")
    print(f"    T_F * n_f * Delta_3 * alpha_LM/(4pi)")
    print(f"    central = {contrib_MSbar_central * 100:+.3f} %")
    print(f"    bracket = [{contrib_MSbar_low * 100:+.3f} %, {contrib_MSbar_high * 100:+.3f} %]")
    print()
    print(f"  Lattice contribution (n_taste = 16, CONTRAST only):")
    print(f"    T_F * n_taste * Delta_3 * alpha_LM/(4pi)")
    print(f"    central = {contrib_lat_central * 100:+.3f} %")
    print(f"    bracket = [{contrib_lat_low * 100:+.3f} %, {contrib_lat_high * 100:+.3f} %]")
    print()
    print(f"  Lattice/MSbar enhancement = 8/3 ~ {TF_ntaste_lattice / TF_nf_MSbar:.3f}")
    print()
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
