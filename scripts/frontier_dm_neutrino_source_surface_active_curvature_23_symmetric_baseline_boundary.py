#!/usr/bin/env python3
"""
DM neutrino source-surface active-curvature 23-symmetric baseline boundary.

Question:
  For positive diagonal baselines D = diag(A,B,C), when does the observable-
  principle zero-source curvature on the live active pair (T_delta,T_q)
  become Euclidean up to scale?

Answer:
  Exactly when the diagonal baseline is 23-symmetric:

      D = diag(A,B,B).

  The scalar line D = m I_3 is only the special case A = B.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    tdelta,
    tq,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def diagonal_curvature(diagonal: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    dinv = np.diag(1.0 / diagonal)
    return float(np.real(np.trace(dinv @ x @ dinv @ y)))


def kdd_formula(a: float, b: float, c: float) -> float:
    return (a * (b * b + c * c) + 2.0 * b * c * (b + c)) / (a * b * b * c * c)


def kqq_formula(a: float, b: float, c: float) -> float:
    return 2.0 * (a + b + c) / (a * b * c)


def kdq_formula(a: float, b: float, c: float) -> float:
    return 2.0 * (b - c) / (a * b * c)


def boundary_prefactor(a: float, b: float) -> float:
    return 2.0 * (a + 2.0 * b) / (a * b * b)


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def part1_the_diagonal_baseline_curvature_has_exact_closed_form() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE DIAGONAL-BASELINE CURVATURE HAS EXACT CLOSED FORM")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    samples = [
        (1.0, 2.0, 3.0),
        (2.5, 0.7, 0.7),
        (3.2, 1.1, 2.4),
    ]
    ok = True
    details = []
    for a, b, c in samples:
        diagonal = np.array([a, b, c], dtype=float)
        kdd = diagonal_curvature(diagonal, td, td)
        kqq = diagonal_curvature(diagonal, tqm, tqm)
        kdq = diagonal_curvature(diagonal, td, tqm)
        err = max(
            abs(kdd - kdd_formula(a, b, c)),
            abs(kqq - kqq_formula(a, b, c)),
            abs(kdq - kdq_formula(a, b, c)),
        )
        ok &= err < 1e-12
        details.append(f"({a:.1f},{b:.1f},{c:.1f}):err={err:.2e}")

    check(
        "The diagonal-baseline active curvature matches the exact closed formulas",
        ok,
        "; ".join(details),
    )


def part2_mixed_term_and_isotropy_are_equivalent_to_23_symmetry() -> None:
    print("\n" + "=" * 88)
    print("PART 2: MIXED TERM AND ISOTROPY ARE EQUIVALENT TO 23 SYMMETRY")
    print("=" * 88)

    td = tdelta()
    tqm = tq()

    diag_sym = np.array([2.0, 1.3, 1.3], dtype=float)
    diag_asym = np.array([1.0, 2.0, 3.0], dtype=float)

    kdq_sym = diagonal_curvature(diag_sym, td, tqm)
    kdd_sym = diagonal_curvature(diag_sym, td, td)
    kqq_sym = diagonal_curvature(diag_sym, tqm, tqm)

    kdq_asym = diagonal_curvature(diag_asym, td, tqm)
    kdd_asym = diagonal_curvature(diag_asym, td, td)
    kqq_asym = diagonal_curvature(diag_asym, tqm, tqm)

    a, b, c = diag_asym
    exact_gap = (b - c) ** 2 / (b * b * c * c)

    check(
        "The mixed term vanishes exactly on the 23-symmetric family B = C",
        abs(kdq_sym) < 1e-12 and abs(kdq_asym - kdq_formula(a, b, c)) < 1e-12,
        f"Kdq(sym)={kdq_sym:.12f}, Kdq(asym)={kdq_asym:.12f}",
    )
    check(
        "The curvature is isotropic exactly on the same 23-symmetric family",
        abs(kdd_sym - kqq_sym) < 1e-12 and abs((kdd_asym - kqq_asym) - exact_gap) < 1e-12,
        f"Kdd-Kqq(asym)={kdd_asym-kqq_asym:.12f}, exact={exact_gap:.12f}",
    )
    check(
        "The reviewer counterexample diag(1,2,3) is genuinely non-Euclidean on the active pair",
        abs(kdq_asym + 1.0 / 3.0) < 1e-12
        and abs(kdd_asym - 2.0277777777777777) < 1e-12
        and abs(kqq_asym - 2.0) < 1e-12,
        f"(Kdd,Kqq,Kdq)=({kdd_asym:.12f},{kqq_asym:.12f},{kdq_asym:.12f})",
    )


def part3_the_23_symmetric_family_has_the_same_chamber_minimizer() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE 23-SYMMETRIC FAMILY HAS THE SAME CHAMBER MINIMIZER")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()

    def boundary_action(prefactor: float, delta: float) -> float:
        q_plus = q_floor(delta)
        return prefactor * (delta * delta + q_plus * q_plus)

    samples = [
        (1.0, 1.0),
        (1.0, 2.0),
        (4.0, 0.5),
    ]
    ok_prefactor = True
    ok_min = True
    details = []
    for a, b in samples:
        pref = boundary_prefactor(a, b)
        deriv = pref * (4.0 * d_sel - 2.0 * math.sqrt(8.0 / 3.0))
        center = boundary_action(pref, d_sel)
        left = boundary_action(pref, d_sel - 0.2)
        right = boundary_action(pref, d_sel + 0.2)
        ok_prefactor &= pref > 0.0
        ok_min &= abs(deriv) < 1e-12 and center < left and center < right
        details.append(f"(A,B)=({a:.1f},{b:.1f}) pref={pref:.12f}")

    check(
        "Every 23-symmetric positive diagonal baseline gives a positive Euclidean prefactor",
        ok_prefactor,
        "; ".join(details),
    )
    check(
        "So every 23-symmetric positive diagonal baseline picks the same chamber minimizer delta_* = q_+* = sqrt(6)/3",
        ok_min and abs(q_sel - q_floor(d_sel)) < 1e-12,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )


def part4_the_note_records_the_honest_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE HONEST BOUNDARY")
    print("=" * 88)

    note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md"
    )

    check(
        "The note records the exact diagonal-baseline curvature formulas",
        "K(T_delta,T_delta)" in note and "K(T_delta,T_q)" in note and "K(T_q,T_q)" in note,
    )
    check(
        "The note records that isotropy holds exactly on the 23-symmetric family, not just the scalar line",
        "`23`-symmetric positive family" in note and "scalar baselines as a special case" in note,
    )
    check(
        "The note explicitly says this does not close the DM selector lane",
        "does **not** close the DM selector lane" in note and "not a selector-closeout theorem" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ACTIVE-CURVATURE 23-SYMMETRIC BASELINE BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  For positive diagonal baselines D = diag(A,B,C), when does the")
    print("  observable-principle zero-source curvature on the live active pair")
    print("  become Euclidean up to scale?")

    part1_the_diagonal_baseline_curvature_has_exact_closed_form()
    part2_mixed_term_and_isotropy_are_equivalent_to_23_symmetry()
    part3_the_23_symmetric_family_has_the_same_chamber_minimizer()
    part4_the_note_records_the_honest_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - for D = diag(A,B,C), the active curvature is diagonal/isotropic iff B = C")
    print("    - the scalar baseline is only the special case A = B = C")
    print("    - the full Euclidean diagonal family is D = diag(A,B,B)")
    print("    - every such baseline gives the same chamber minimizer delta_* = q_+* = sqrt(6)/3")
    print("    - this is still a boundary theorem for the diagnostic route, not selector closure")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
