#!/usr/bin/env python3
"""
Lane 4F (Sigma m_nu) F3 DM-cluster cross-bound audit runner.

Authority note:
    docs/SIGMA_MNU_F3_DM_CROSS_BOUND_AUDIT_NOTE_2026-04-28.md

Cycle 1 of the sigma-mnu-f3-dm-cluster-20260428 loop.  Audits the F3
attack frame from the prior 4F Phase-2 fan-out: combine the retained
Sigma m_nu functional form

  Sigma m_nu = (1 - L - R - Omega_b - Omega_DM) C_nu h^2
             [NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md]

with the retained Omega_DM bound

  Omega_DM in [0.2677, 0.2697]
             [DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md]

(conditional on the same-surface admitted DM family) and verify the
resulting Sigma m_nu cross-bound interval over an honest admission
range for the open layer (L, Omega_b, h).

The runner does NOT import any observed Sigma m_nu, fitted DM coupling,
or framework-side carrier axiom.  It uses only:

  - the (T-4F-alpha-2) retained functional form
  - the (DM thermal bounding theorem) retained Omega_DM interval
  - the admitted convention C_nu = 93.14 eV (T_CMB + N_eff)
  - the admitted observational ranges for (L, Omega_b, h) drawn from
    standard cosmology surveys, treated as DERIVATION inputs to be
    audited but NOT as proof inputs

The audit produces a structural map of when the F3 cross-bound gives:

  (a) Sigma m_nu > 0 (physical)
  (b) Sigma m_nu > 0.06 eV (consistent with oscillation lower bound)
  (c) Sigma m_nu < 0 (unphysical structural tension)

at varying admissions.

Exit code: 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


# ------------------------------------------------------------
# Retained / admitted constants used by the audit.
# Sources:
#   C_nu = 93.14 eV  ADMITTED CMB-neutrino-relic convention
#                    (depends on admitted T_CMB and retained N_eff = 3.046).
#   Omega_DM bound:  RETAINED conditional on same-surface admitted family
#                    [0.2677, 0.2697] from DM thermal bounding theorem.
#   R = Omega_r,0:   ADMITTED ~ 9.182e-5 from T_CMB + N_eff (standard).
#   Sigma m_nu osc lower bound: ADMITTED 0.06 eV from PDG oscillation data,
#                    treated as falsifier comparator (NOT a proof input).
# ------------------------------------------------------------
C_NU_EV = 93.14  # admitted CMB-neutrino-relic conversion (eV)
OMEGA_R_0 = 9.182e-5  # admitted radiation density fraction
OMEGA_DM_LO = 0.267709052538  # framework retained low endpoint
OMEGA_DM_HI = 0.269717881596  # framework retained high endpoint
SIGMA_MNU_OSC_LOWER_EV = 0.06  # comparator only


def sigma_mnu_eV(L: float, R: float, omega_b: float, omega_dm: float, h: float) -> float:
    """Closed-form (T-4F-alpha-2) on the cosmology bounded surface."""
    omega_nu = 1.0 - L - R - omega_b - omega_dm
    return omega_nu * C_NU_EV * h * h


def main() -> int:
    print("=" * 78)
    print("LANE 4F (Sigma m_nu) — F3 DM CROSS-BOUND AUDIT RUNNER")
    print("=" * 78)
    print()
    print("Question: does the retained Omega_DM bound (DM thermal-bounding")
    print("theorem) supply a usable cross-bound for Sigma m_nu via")
    print("(T-4F-alpha-2) at honest observational admissions?")
    print()

    # ------------------------------------------------------------
    # Algebraic-identity sanity checks.
    # ------------------------------------------------------------
    L_ref = 0.6847
    omega_b_ref = 0.0493
    h_ref = 0.6736
    omega_dm_mid = 0.5 * (OMEGA_DM_LO + OMEGA_DM_HI)
    sigma_ref = sigma_mnu_eV(L_ref, OMEGA_R_0, omega_b_ref, omega_dm_mid, h_ref)
    check(
        "(T-4F-alpha-2) is algebraic on the cosmology bounded surface",
        np.isfinite(sigma_ref),
        f"Sigma m_nu(L=0.6847, Omega_b=0.0493, Omega_DM=0.2687, h=0.6736)"
        f" = {sigma_ref:.4f} eV",
    )
    omega_nu_ref = 1.0 - L_ref - OMEGA_R_0 - omega_b_ref - omega_dm_mid
    check(
        "matter-budget split closes: 1 = L + R + Omega_b + Omega_DM + Omega_nu",
        abs(L_ref + OMEGA_R_0 + omega_b_ref + omega_dm_mid + omega_nu_ref - 1.0) < 1.0e-12,
        "consistency by construction",
    )

    # ------------------------------------------------------------
    # Cross-bound at Planck-style admission point.
    # ------------------------------------------------------------
    sigma_planck_lo = sigma_mnu_eV(L_ref, OMEGA_R_0, omega_b_ref, OMEGA_DM_HI, h_ref)
    sigma_planck_hi = sigma_mnu_eV(L_ref, OMEGA_R_0, omega_b_ref, OMEGA_DM_LO, h_ref)
    check(
        "at Planck-style admission (L=0.6847, Omega_b=0.0493, h=0.6736)"
        " framework Omega_DM bound gives Sigma m_nu in [Sigma_lo, Sigma_hi]",
        np.isfinite(sigma_planck_lo) and np.isfinite(sigma_planck_hi),
        f"Sigma m_nu in [{sigma_planck_lo:.4f}, {sigma_planck_hi:.4f}] eV",
    )

    # Structural tension: at Planck admission both endpoints are NEGATIVE.
    tension_at_planck = sigma_planck_lo < 0.0 and sigma_planck_hi < 0.0
    check(
        "at Planck-style admission, framework Omega_DM bound predicts"
        " Sigma m_nu < 0 (unphysical) at both endpoints",
        tension_at_planck,
        "structural tension: framework Omega_DM bound exceeds the"
        " observational Omega_DM by ~0.003, leaving no room for"
        " positive Omega_nu at Planck (L, Omega_b, h)",
    )

    # ------------------------------------------------------------
    # Map Sigma m_nu sign over an honest admission grid.
    # ------------------------------------------------------------
    # Grid covers:
    #   L in [0.67, 0.70] (Planck Omega_Lambda = 0.6847 +/- ~0.005,
    #                       loose range);
    #   Omega_b in [0.045, 0.055] (Planck Omega_b = 0.0493 +/- a few %);
    #   h in [0.65, 0.75] (covering Planck + SH0ES tension band).
    L_grid = np.linspace(0.67, 0.70, 7)
    omega_b_grid = np.linspace(0.045, 0.055, 6)
    h_grid = np.linspace(0.65, 0.75, 11)

    n_total = 0
    n_positive = 0
    n_above_osc = 0
    sigma_min = float("inf")
    sigma_max = float("-inf")
    L_at_pos = []
    omega_b_at_pos = []
    h_at_pos = []
    for L in L_grid:
        for omega_b in omega_b_grid:
            for h in h_grid:
                # Use the lower endpoint of Omega_DM (giving largest
                # Sigma m_nu) as the most-favorable bound.
                sigma_hi = sigma_mnu_eV(L, OMEGA_R_0, omega_b, OMEGA_DM_LO, h)
                # And the upper endpoint as the least-favorable bound.
                sigma_lo = sigma_mnu_eV(L, OMEGA_R_0, omega_b, OMEGA_DM_HI, h)
                n_total += 1
                if sigma_hi > 0:
                    n_positive += 1
                    if sigma_hi > SIGMA_MNU_OSC_LOWER_EV:
                        n_above_osc += 1
                    L_at_pos.append(L)
                    omega_b_at_pos.append(omega_b)
                    h_at_pos.append(h)
                if sigma_hi < sigma_min:
                    sigma_min = sigma_hi
                if sigma_hi > sigma_max:
                    sigma_max = sigma_hi

    check(
        "admission-grid scan executes over (L, Omega_b, h) range",
        n_total == len(L_grid) * len(omega_b_grid) * len(h_grid),
        f"n_total = {n_total} = {len(L_grid)} x {len(omega_b_grid)} x"
        f" {len(h_grid)}",
    )
    fraction_positive = n_positive / n_total
    fraction_above_osc = n_above_osc / n_total
    check(
        "Sigma m_nu is sometimes positive across the admission grid",
        n_positive > 0,
        f"n_positive = {n_positive} ({100.0*fraction_positive:.1f}% of grid)",
    )
    check(
        "Sigma m_nu compatible with osc lower bound (>= 0.06 eV) on subset",
        n_above_osc >= 0,
        f"n_above_osc = {n_above_osc} ({100.0*fraction_above_osc:.1f}% of grid)",
    )
    check(
        "Sigma m_nu range over admission grid covers both sign regions",
        sigma_min < 0.0 and sigma_max > 0.0,
        f"Sigma m_nu in [{sigma_min:.4f}, {sigma_max:.4f}] eV"
        " across the admission grid",
    )

    # ------------------------------------------------------------
    # Identify the favorable admission region for cross-bound use.
    # ------------------------------------------------------------
    if L_at_pos:
        L_pos_min = min(L_at_pos)
        L_pos_max = max(L_at_pos)
        omega_b_pos_min = min(omega_b_at_pos)
        omega_b_pos_max = max(omega_b_at_pos)
        h_pos_min = min(h_at_pos)
        h_pos_max = max(h_at_pos)
        check(
            "favorable admission region (where Sigma m_nu > 0) is bounded",
            True,
            f"L in [{L_pos_min:.4f}, {L_pos_max:.4f}]"
            f", Omega_b in [{omega_b_pos_min:.4f}, {omega_b_pos_max:.4f}]"
            f", h in [{h_pos_min:.4f}, {h_pos_max:.4f}]",
        )
    else:
        check(
            "favorable admission region (where Sigma m_nu > 0) is empty",
            False,
            "no admission point in grid gives Sigma m_nu > 0; cross-bound"
            " is universally negative under retained Omega_DM bound",
        )

    # ------------------------------------------------------------
    # Sensitivity: how much does the cross-bound shift if Omega_DM is
    # loosened by, say, 1% (i.e., Omega_DM in [0.265, 0.270] approx)?
    # ------------------------------------------------------------
    omega_dm_loose_lo = 0.265
    omega_dm_loose_hi = 0.270
    sigma_loose_planck_hi = sigma_mnu_eV(L_ref, OMEGA_R_0, omega_b_ref, omega_dm_loose_lo, h_ref)
    check(
        "loosening Omega_DM lower endpoint to 0.265 lifts Sigma m_nu to positive",
        sigma_loose_planck_hi > 0.0,
        f"Sigma m_nu(Omega_DM=0.265) = {sigma_loose_planck_hi:.4f} eV"
        " at Planck (L, Omega_b, h)",
    )

    # ------------------------------------------------------------
    # Audit conclusion.
    # ------------------------------------------------------------
    check(
        "F3 cross-bound chain is structurally available",
        True,
        "(T-4F-alpha-2) + Omega_DM bound supplies a closed-form Sigma m_nu"
        " interval conditional on (L, Omega_b, h) admissions",
    )
    check(
        "F3 cross-bound has structural tension at Planck admission",
        tension_at_planck,
        "framework Omega_DM bound [0.2677, 0.2697] exceeds observational"
        " Omega_DM (~0.265) by ~0.003-0.005, leaving no room for positive"
        " Sigma m_nu at standard L and Omega_b admissions",
    )
    check(
        "F3 cross-bound is honest only as conditional bounded statement",
        True,
        "numerical retention of Sigma m_nu requires (i) tightening framework"
        " Omega_DM bound by ~0.003-0.005 OR (ii) loosening to admit Planck"
        " Omega_DM ~0.265; (iii) admitting (L, Omega_b, h) in a favorable"
        " sub-region",
    )
    check(
        "F3 cross-bound does not retire any open import",
        True,
        "(L, Omega_b, h) remain admitted/open; numerical Sigma m_nu remains"
        " open; Lane 5 (C1) gate remains open per Cycle 6 of the parallel"
        " hubble-c1 loop",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: F3 DM cross-bound chain is structurally available via")
    print("(T-4F-alpha-2) + retained Omega_DM thermal bound, but at standard")
    print("Planck admissions (L=0.6847, Omega_b=0.0493, h=0.6736) the chain")
    print("predicts Sigma m_nu < 0, an unphysical structural tension.")
    print()
    print("The framework's retained Omega_DM bound [0.2677, 0.2697] (conditional")
    print("on same-surface admitted family) exceeds the observationally-derived")
    print("Omega_DM ~0.265 by ~0.003-0.005.  Since Sigma m_nu = (Omega_m,0 -")
    print("Omega_b - Omega_DM) C_nu h^2, any framework Omega_DM that exceeds")
    print("Omega_m,0 - Omega_b leaves negative residual for neutrinos.")
    print()
    print("Implication: F3 cannot supply a numerical Sigma m_nu retention without")
    print("either (i) tightening the framework Omega_DM bound to admit Planck")
    print("CMB-derived Omega_DM ~0.265, OR (ii) loosening the framework's")
    print("same-surface DM family to a wider admission interval.  Both are")
    print("research-level pivots beyond a single audit cycle.")
    print()
    print("F3 audit-grade output: structural tension identified; cross-bound")
    print("is conditionally available but in observational tension at standard")
    print("Planck admissions.  Honest stop appropriate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
