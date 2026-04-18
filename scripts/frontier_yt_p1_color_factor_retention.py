#!/usr/bin/env python3
"""
Frontier runner: P1 color-factor retention.

Status
------
STRUCTURAL RETENTION of the three-channel color-tensor decomposition of
the 1-loop Ward-ratio correction Delta_R = delta_y - delta_g on the
retained Cl(3)/Z^3 framework surface:

    Delta_R  =  C_F * Delta_1  +  C_A * Delta_2  +  T_F * n_f * Delta_3

with exact SU(3) prefactors C_F = 4/3, C_A = 3, T_F * n_f = 3 at n_f = 6.

The runner does NOT derive the per-channel integrals Delta_1, Delta_2,
Delta_3; those are treated in separate BZ-computation sub-theorems.
It verifies:

  1. C_F = 4/3 exactly at SU(3) (from D7 + S1);
  2. C_A = 3 exactly at SU(3) (from D7);
  3. T_F * n_f = 3 exactly at SU(3), n_f = 6 (from D7 + S1 + SM flavor
     count at M_Pl);
  4. three-channel decomposition identity is structurally exact
     (symbolic reassembly matches the Rep-A - Rep-B subtraction
     channel-by-channel);
  5. consistency with the Rep-A/Rep-B decomposition: the net C_F, C_A,
     T_F n_f channel coefficients after the 2 C_F * I_leg external-Z_psi
     cancellation reproduce the retained per-channel formulae.

Authority
---------
  - docs/YT_EW_COLOR_PROJECTION_THEOREM.md            (SU(3) C_F, C_A, T_F)
  - docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md (gauge-group uniqueness)
  - docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md
    (diagrammatic catalog from which the three-channel color structure follows)

Self-contained: sympy + stdlib only.
"""

from __future__ import annotations

import sys

import sympy as sp


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
# Retained SU(3) Casimir algebra (exact)
# ---------------------------------------------------------------------------

N_C = sp.Integer(3)
C_F = (N_C ** 2 - 1) / (2 * N_C)          # = 4/3
T_F = sp.Rational(1, 2)
C_A = N_C                                   # = 3
N_F = sp.Integer(6)                         # SM flavor count at M_Pl


# ---------------------------------------------------------------------------
# PART A: Exact SU(3) Casimir values at n_f = 6
# ---------------------------------------------------------------------------

def part_a_casimir_values() -> None:
    print("\n" + "=" * 72)
    print("PART A: Retained SU(3) Casimir prefactors at n_f = 6")
    print("=" * 72)

    print(f"\n  C_F           = {sp.nsimplify(C_F)}  = {float(C_F):.10f}")
    print(f"  C_A           = {sp.nsimplify(C_A)}  = {float(C_A):.10f}")
    print(f"  T_F           = {sp.nsimplify(T_F)}  = {float(T_F):.10f}")
    print(f"  n_f           = {sp.nsimplify(N_F)}")
    print(f"  T_F * n_f     = {sp.nsimplify(T_F * N_F)}  = {float(T_F * N_F):.10f}")

    check(
        "C_F = 4/3 exactly at SU(3)",
        C_F == sp.Rational(4, 3),
        f"value = {sp.nsimplify(C_F)}",
    )
    check(
        "C_A = 3 exactly at SU(3)",
        C_A == sp.Integer(3),
        f"value = {sp.nsimplify(C_A)}",
    )
    check(
        "T_F * n_f = 3 exactly at SU(3), n_f = 6",
        T_F * N_F == sp.Integer(3),
        f"value = {sp.nsimplify(T_F * N_F)}",
    )


# ---------------------------------------------------------------------------
# PART B: Three-channel decomposition identity
# ---------------------------------------------------------------------------

def part_b_decomposition_identity() -> None:
    """
    Verify that the three-channel decomposition
        Delta_R = C_F * Delta_1 + C_A * Delta_2 + T_F * n_f * Delta_3
    reproduces the Rep-A minus Rep-B subtraction channel-by-channel.

    From docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md:

      delta_g  =  2 (C_F - C_A/2) * I_v_gauge
                 + (5/3 C_A - 4/3 T_F n_f) * I_SE
                 + 2 C_F * I_leg                           [Rep-A]

      delta_y  =  2 C_F * I_v_scalar
                 + (-6 C_F)                                 [scalar op anom dim]
                 + 2 C_F * I_leg                           [Rep-B]

    Delta_R = delta_y - delta_g splits as:

      C_F channel      :  2 (I_v_scalar - I_v_gauge) - 6
      C_A channel      :  I_v_gauge - (5/3) I_SE^{gluonic}
      T_F n_f channel  :  (4/3) I_SE^{fermion}

    The 2 C_F * I_leg piece cancels exactly on the ratio.
    """
    print("\n" + "=" * 72)
    print("PART B: Three-channel decomposition identity")
    print("=" * 72)

    # Symbolic integrals appearing in the two reps.
    I_v_scalar, I_v_gauge, I_SE_g, I_SE_f, I_leg = sp.symbols(
        "I_v_scalar I_v_gauge I_SE_g I_SE_f I_leg", real=True
    )

    # Rep-A: vertex (non-abelian decomposed into 2 C_F - C_A), gluon SE
    # (gluonic + fermion-loop pieces), external Z_psi.
    delta_g = (
        (2 * C_F - C_A) * I_v_gauge       # vertex C_F + C_A piece
        + sp.Rational(5, 3) * C_A * I_SE_g
        - sp.Rational(4, 3) * T_F * N_F * I_SE_f
        + 2 * C_F * I_leg
    )

    # Rep-B: scalar vertex, operator anomalous dimension, external Z_psi.
    delta_y = (
        2 * C_F * I_v_scalar
        - 6 * C_F
        + 2 * C_F * I_leg
    )

    Delta_R = sp.expand(delta_y - delta_g)

    # Per-channel formulae (as claimed in the note, §3.3):
    Delta_1 = 2 * (I_v_scalar - I_v_gauge) - 6
    Delta_2 = I_v_gauge - sp.Rational(5, 3) * I_SE_g
    Delta_3 = sp.Rational(4, 3) * I_SE_f

    Delta_R_reconstructed = sp.expand(
        C_F * Delta_1 + C_A * Delta_2 + T_F * N_F * Delta_3
    )

    print("\n  Delta_R (from Rep-A - Rep-B):")
    print(f"    {Delta_R}")
    print("\n  Delta_R (three-channel assembly C_F*D1 + C_A*D2 + T_F n_f*D3):")
    print(f"    {Delta_R_reconstructed}")

    # Exact symbolic identity: the two expressions should match.
    residual = sp.simplify(Delta_R - Delta_R_reconstructed)
    check(
        "Three-channel decomposition matches Rep-A - Rep-B subtraction exactly",
        residual == 0,
        f"residual = {residual}",
    )

    # Verify the external Z_psi cancellation explicitly.
    leg_coeff_in_delta_R = Delta_R.coeff(I_leg)
    check(
        "External quark Z_psi (I_leg) cancels exactly on the ratio",
        sp.simplify(leg_coeff_in_delta_R) == 0,
        f"coeff of I_leg in Delta_R = {sp.simplify(leg_coeff_in_delta_R)}",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("P1 color-factor retention -- runner")
    print("Date: 2026-04-17")
    print("Authority: YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md")
    print("=" * 72)

    part_a_casimir_values()
    part_b_decomposition_identity()

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print("\n(C_F, C_A, T_F*n_f prefactors retained framework-native at SU(3).")
    print(" Three-channel decomposition structurally exact from Rep-A vs Rep-B.")
    print(" Per-channel integrals Delta_1, Delta_2, Delta_3 live outside this")
    print(" note's scope; they are cited / computed in the three dedicated BZ")
    print(" sub-theorems.)")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
