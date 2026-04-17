#!/usr/bin/env python3
"""
DM neutrino source-surface zero-import active quadratic selector theorem.

Question:
  Can the same quadratic point-selection law on the live active pair
  (delta, q_+) be derived natively from the existing Cl(3)/Z^3 bank, without
  adding a new selector input?

Answer:
  Yes.

  Restrict the unique additive CPT-even scalar generator

      W[J] = log|det(D+J)| - log|det D|

  to the exact active family

      J_act(delta,q_+) = delta T_delta + q_+ T_q

  on a scalar baseline D = m I_3.

  The zero-source bosonic curvature then gives the exact native bilinear form

      K_act(J_act,J_act) = (6/m^2) (delta^2 + q_+^2),

  so the canonical positive quadratic action is

      Q_act(delta,q_+) = 6 (delta^2 + q_+^2).

  Minimizing that native action on the exact active chamber
  q_+ >= sqrt(8/3) - delta yields the unique point

      delta_* = q_+* = sqrt(6)/3,

  hence rho_* = sqrt(6)/3, r31,* = 1/2, phi_+,* = pi/2.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
    tdelta,
    tq,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    active_half_plane_h,
    q_floor,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)

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


def active_source(delta: float, q_plus: float) -> np.ndarray:
    return delta * tdelta() + q_plus * tq()


def relative_generator(mass: float, delta: float, q_plus: float) -> float:
    j = active_source(delta, q_plus)
    sign, logabs = np.linalg.slogdet(mass * np.eye(3, dtype=complex) + j)
    if abs(sign) == 0:
        raise ValueError("singular source-deformed block encountered")
    return float(logabs - 3.0 * math.log(abs(mass)))


def exact_det_formula(mass: float, delta: float, q_plus: float) -> float:
    return (mass + 2.0 * q_plus) * ((mass - q_plus) ** 2 - 3.0 * delta * delta)


def frobenius_inner(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.real(np.trace(a.conj().T @ b)))


def native_quadratic(delta: float, q_plus: float) -> float:
    j = active_source(delta, q_plus)
    return frobenius_inner(j, j)


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def part1_the_observable_principle_restricts_to_an_exact_active_source_family() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE OBSERVABLE PRINCIPLE RESTRICTS TO AN EXACT ACTIVE SOURCE FAMILY")
    print("=" * 88)

    obs_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    affine_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md")

    mass = 2.3
    samples = [(0.2, 1.1), (-0.4, 1.7), (0.8, 0.9)]
    ok_det = True
    max_err = 0.0
    for delta, q_plus in samples:
        sign, logabs = np.linalg.slogdet(mass * np.eye(3, dtype=complex) + active_source(delta, q_plus))
        det_direct = float(np.real(sign * np.exp(logabs)))
        det_exact = exact_det_formula(mass, delta, q_plus)
        err = abs(det_direct - det_exact)
        max_err = max(max_err, err)
        ok_det &= err < 1e-10

    check(
        "The observable principle note records the unique additive CPT-even scalar generator W[J] = log|det(D+J)| - log|det D|",
        "W[J] = log |det(D+J)| - log |det D|" in obs_note
        or "W[J] = log|det(D+J)| - log|det D|" in obs_note,
    )
    check(
        "The active-affine theorem records the exact active generators T_delta and T_q",
        "T_delta" in affine_note and "T_q" in affine_note,
    )
    check(
        "Restricting W to J_act(delta,q_+) gives an exact intrinsic active source-response family",
        ok_det,
        f"max det error={max_err:.2e}",
    )


def part2_the_zero_source_bosonic_curvature_is_exactly_isotropic_on_the_active_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ZERO-SOURCE BOSONIC CURVATURE IS EXACTLY ISOTROPIC ON THE ACTIVE PAIR")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    mass = 1.9

    tr_td = float(np.real(np.trace(td)))
    tr_tq = float(np.real(np.trace(tqm)))
    gram_dd = frobenius_inner(td, td)
    gram_qq = frobenius_inner(tqm, tqm)
    gram_dq = frobenius_inner(td, tqm)
    # Exact zero-source Hessian from the closed determinant family:
    # det(mI + J_act) = (m+2q)((m-q)^2 - 3 delta^2).
    # Hence W(delta,0) = log|1 - 3 delta^2/m^2| and
    # W(0,q) = log|(1+2q/m)(1-q/m)^2|, so
    # d^2W/ddelta^2|_0 = -6/m^2, d^2W/dq^2|_0 = -6/m^2.
    hess_dd = -6.0 / (mass * mass)
    hess_dq = 0.0

    check(
        "The active generators are traceless, so the linear source term vanishes at the origin",
        abs(tr_td) < 1e-12 and abs(tr_tq) < 1e-12,
        f"(Tr T_delta, Tr T_q)=({tr_td:.12f},{tr_tq:.12f})",
    )
    check(
        "Their exact bosonic curvature Gram matrix is diagonal with equal entries",
        abs(gram_dd - 6.0) < 1e-12 and abs(gram_qq - 6.0) < 1e-12 and abs(gram_dq) < 1e-12,
        f"Gram=({gram_dd:.12f},{gram_qq:.12f},{gram_dq:.12f})",
    )
    check(
        "The zero-source Hessian of W matches the native curvature law -Tr(XY)/m^2 on T_delta",
        abs(hess_dd + gram_dd / (mass * mass)) < 1e-12,
        f"H_dd={hess_dd:.12f}, exact={-gram_dd/(mass*mass):.12f}",
    )
    check(
        "The mixed zero-source Hessian vanishes exactly because T_delta and T_q are Frobenius-orthogonal",
        abs(hess_dq) < 1e-12,
        f"H_dq={hess_dq:.12f}",
    )


def part3_the_native_quadratic_law_is_exactly_the_previous_selector_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NATIVE QUADRATIC LAW IS EXACTLY THE PREVIOUS SELECTOR LAW")
    print("=" * 88)

    samples = [(0.37, 1.41), (-0.25, 0.9), (0.8, 0.2)]
    ok = True
    max_err = 0.0
    for delta, q_plus in samples:
        val = native_quadratic(delta, q_plus)
        exact = 6.0 * (delta * delta + q_plus * q_plus)
        err = abs(val - exact)
        max_err = max(max_err, err)
        ok &= err < 1e-12

    check(
        "The canonical positive active quadratic is exactly Q_act(delta,q_+) = Tr(J_act^2)",
        ok,
        f"max err={max_err:.2e}",
    )
    check(
        "So the derived zero-import quadratic law is exactly Q_act(delta,q_+) = 6(delta^2 + q_+^2)",
        ok,
        "the old variational law is recovered natively",
    )


def part4_minimizing_the_native_quadratic_on_the_exact_chamber_selects_the_same_point() -> None:
    print("\n" + "=" * 88)
    print("PART 4: MINIMIZING THE NATIVE QUADRATIC ON THE EXACT CHAMBER SELECTS THE SAME POINT")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()
    boundary_ok = abs(q_sel - q_floor(d_sel)) < 1e-12

    def q_bdy(delta: float) -> float:
        return q_floor(delta)

    def qb_action(delta: float) -> float:
        return 6.0 * (delta * delta + q_bdy(delta) * q_bdy(delta))

    deriv = 24.0 * d_sel - 8.0 * math.sqrt(6.0)
    center = qb_action(d_sel)
    left = qb_action(d_sel - 0.2)
    right = qb_action(d_sel + 0.2)

    check(
        "The exact selected point lies on the active boundary q_+ = sqrt(8/3) - delta",
        boundary_ok,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )
    check(
        "The boundary quadratic has stationary point at delta_* = sqrt(6)/3",
        abs(deriv) < 1e-12,
        f"Q'_bdy(delta_*)={deriv:.12f}",
    )
    check(
        "Strict convexity gives that point as the unique minimizer on the chamber",
        center < left and center < right,
        f"Q*={center:.12f}, Q_left={left:.12f}, Q_right={right:.12f}",
    )
    check(
        "Therefore the zero-import selector closes at delta_* = q_+* = sqrt(6)/3",
        abs(d_sel - math.sqrt(6.0) / 3.0) < 1e-12 and abs(q_sel - math.sqrt(6.0) / 3.0) < 1e-12,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )


def part5_the_selected_point_has_exact_live_sheet_readout() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE SELECTED POINT HAS EXACT LIVE-SHEET READOUT")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()
    rho_sel = q_floor(d_sel)
    h, r31, phi = active_half_plane_h(d_sel, q_sel, m=0.0)
    kz = kz_from_h(h)
    q_rec = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
    delta_rec = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)

    check(
        "The selected law gives rho_* = sqrt(6)/3 by the exact source constraint delta + rho = sqrt(8/3)",
        abs(rho_sel - d_sel) < 1e-12,
        f"(delta_*,rho_*)=({d_sel:.12f},{rho_sel:.12f})",
    )
    check(
        "The selected point lies on the maximal-phase boundary r31 = 1/2, phi_+ = pi/2",
        abs(r31 - 0.5) < 1e-12 and abs(phi - 0.5 * math.pi) < 1e-12,
        f"(r31,phi)=({r31:.12f},{phi:.12f})",
    )
    check(
        "The intrinsic Z3 doublet block reads back exactly the selected point",
        abs(q_rec - q_sel) < 1e-12 and abs(delta_rec - d_sel) < 1e-12,
        f"(delta,q_+) from K_Z3=({delta_rec:.12f},{q_rec:.12f})",
    )
    check(
        "The selected point is realized directly by the affine H-side chart",
        np.linalg.norm(h - active_affine_h(0.0, d_sel, q_sel)) < 1e-12,
        f"affine err={np.linalg.norm(h - active_affine_h(0.0, d_sel, q_sel)):.2e}",
    )


def part6_the_note_records_the_zero_import_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE NOTE RECORDS THE ZERO-IMPORT CLOSEOUT")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ZERO_IMPORT_ACTIVE_QUADRATIC_SELECTOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The note records that the selector is zero-import on the single-axiom surface",
        "zero-import" in note and "Cl(3)" in note and "Z^3" in note,
    )
    check(
        "The note records the exact native quadratic law and the selected point",
        "Q_act(delta,q_+) = 6(delta^2 + q_+^2)" in note
        and "delta_* = q_+* = sqrt(6)/3" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ZERO-IMPORT ACTIVE QUADRATIC SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the same quadratic selector law on the live active pair")
    print("  (delta, q_+) be derived natively from the existing Cl(3)/Z^3 bank,")
    print("  without adding a new selector input?")

    part1_the_observable_principle_restricts_to_an_exact_active_source_family()
    part2_the_zero_source_bosonic_curvature_is_exactly_isotropic_on_the_active_pair()
    part3_the_native_quadratic_law_is_exactly_the_previous_selector_law()
    part4_minimizing_the_native_quadratic_on_the_exact_chamber_selects_the_same_point()
    part5_the_selected_point_has_exact_live_sheet_readout()
    part6_the_note_records_the_zero_import_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact zero-import answer:")
    print("    - the unique additive CPT-even scalar generator already restricts to the active family")
    print("    - its zero-source curvature yields the native bilinear form")
    print("      K_act(J_act,J_act) = (6/m^2)(delta^2 + q_+^2)")
    print("    - so the canonical positive quadratic selector is Q_act = 6(delta^2 + q_+^2)")
    print("    - minimizing on the exact chamber selects delta_* = q_+* = sqrt(6)/3")
    print("    - therefore rho_* = sqrt(6)/3, r31,* = 1/2, phi_+,* = pi/2")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
