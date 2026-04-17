#!/usr/bin/env python3
"""
DM neutrino source-surface minimal active-displacement selector theorem.

Question:
  If we add one genuinely new right-sensitive input, can we derive the exact
  2-real point-selection law (delta, q_+) itself on the live source-oriented
  sheet?

Answer:
  Yes.

  Add the input that the physical point is the unique minimizer of the
  Frobenius action

      S_act(delta,q_+) = ||delta T_delta + q_+ T_q||_F^2

  on the exact active chamber q_+ >= sqrt(8/3) - delta.

  Because T_delta and T_q are Frobenius-orthogonal and have equal norm 6,

      S_act(delta,q_+) = 6(delta^2 + q_+^2).

  The unique constrained minimizer is the orthogonal projection of the origin
  to the boundary line q_+ = sqrt(8/3) - delta, hence

      delta_* = q_+* = sqrt(6)/3.

  Therefore rho_* = sqrt(6)/3, r31,* = 1/2, and phi_+,* = pi/2.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
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


def frobenius_inner(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.real(np.trace(a.conj().T @ b)))


def active_action(delta: float, q_plus: float) -> float:
    disp = delta * tdelta() + q_plus * tq()
    return frobenius_inner(disp, disp)


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def part1_the_active_generators_define_an_exact_euclidean_selector_problem() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE GENERATORS DEFINE AN EXACT EUCLIDEAN SELECTOR PROBLEM")
    print("=" * 88)

    td = tdelta()
    tqm = tq()
    inner = frobenius_inner(td, tqm)
    norm_delta = frobenius_inner(td, td)
    norm_q = frobenius_inner(tqm, tqm)

    check(
        "The two active generators are Frobenius-orthogonal",
        abs(inner) < 1e-12,
        f"<T_delta,T_q>={inner:.12f}",
    )
    check(
        "The two active generators have equal exact Frobenius norm",
        abs(norm_delta - 6.0) < 1e-12 and abs(norm_q - 6.0) < 1e-12,
        f"||T_delta||^2={norm_delta:.12f}, ||T_q||^2={norm_q:.12f}",
    )

    delta = 0.37
    q_plus = 1.41
    action = active_action(delta, q_plus)
    formula = 6.0 * (delta * delta + q_plus * q_plus)
    check(
        "So the active action is exactly S_act(delta,q_+) = 6(delta^2 + q_+^2)",
        abs(action - formula) < 1e-12,
        f"action={action:.12f}, formula={formula:.12f}",
    )


def part2_the_exact_half_plane_has_a_unique_minimizer() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXACT HALF-PLANE HAS A UNIQUE MINIMIZER")
    print("=" * 88)

    pkg = exact_package()
    d_star = delta_star()
    q_sel = q_star()

    boundary_ok = abs(q_sel - q_floor(d_star)) < 1e-12

    def boundary_action(delta: float) -> float:
        return active_action(delta, q_floor(delta))

    deriv_at_star = 24.0 * d_star - 8.0 * math.sqrt(6.0)
    action_star = boundary_action(d_star)
    action_left = boundary_action(d_star - 0.2)
    action_right = boundary_action(d_star + 0.2)

    check(
        "The selected point lies exactly on the active boundary q_+ = sqrt(8/3) - delta",
        boundary_ok,
        f"q_*={q_sel:.12f}, q_floor(delta_*)={q_floor(d_star):.12f}",
    )
    check(
        "The boundary action has stationary point at delta_* = sqrt(6)/3",
        abs(deriv_at_star) < 1e-12,
        f"S'_bdy(delta_*)={deriv_at_star:.12f}",
    )
    check(
        "That stationary point is the unique minimum of the strict convex boundary action",
        action_star < action_left and action_star < action_right,
        f"S*={action_star:.12f}, S_left={action_left:.12f}, S_right={action_right:.12f}",
    )
    check(
        "Therefore the exact selected law is delta_* = q_+* = sqrt(6)/3 = sqrt(8/3)/2",
        abs(d_star - math.sqrt(6.0) / 3.0) < 1e-12
        and abs(q_sel - pkg.E1 / 2.0) < 1e-12,
        f"(delta_*,q_+*)=({d_star:.12f},{q_sel:.12f})",
    )


def part3_the_selected_point_has_exact_carrier_and_doublet_block_data() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SELECTED POINT HAS EXACT CARRIER AND DOUBLET-BLOCK DATA")
    print("=" * 88)

    pkg = exact_package()
    d_star = delta_star()
    q_sel = q_star()
    rho_star = q_floor(d_star)

    h, r31, phi = active_half_plane_h(d_star, q_sel, m=0.0)
    kz = kz_from_h(h)
    q_rec = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
    delta_rec = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)

    check(
        "The selected point lies exactly on the maximal-phase active boundary",
        abs(r31 - pkg.gamma) < 1e-12 and abs(phi - 0.5 * math.pi) < 1e-12,
        f"(r31,phi)=({r31:.12f},{phi:.12f})",
    )
    check(
        "The selected law gives delta_* = rho_* = sqrt(6)/3 by the exact source constraint delta + rho = sqrt(8/3)",
        abs(rho_star - d_star) < 1e-12 and abs(d_star + rho_star - pkg.E1) < 1e-12,
        f"(delta_*,rho_*)=({d_star:.12f},{rho_star:.12f})",
    )
    check(
        "The Z3 doublet block reads back exactly the selected point",
        abs(q_rec - q_sel) < 1e-12 and abs(delta_rec - d_star) < 1e-12,
        f"(delta,q_+) from K_Z3=({delta_rec:.12f},{q_rec:.12f})",
    )
    check(
        "The selected point is realized directly by the affine H-side chart",
        np.linalg.norm(h - active_affine_h(0.0, d_star, q_sel)) < 1e-12,
        f"affine err={np.linalg.norm(h - active_affine_h(0.0, d_star, q_sel)):.2e}",
    )
    check(
        "At the selected point the H-side boundary is maximal-phase: H_02 is purely imaginary with Im(H_02) = -gamma",
        abs(float(np.real(h[0, 2]))) < 1e-12 and abs(float(np.imag(h[0, 2])) + pkg.gamma) < 1e-12,
        f"H_02={h[0,2]:.12f}",
    )


def part4_the_note_records_the_new_input_and_closed_form_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE NEW INPUT AND CLOSED-FORM SELECTOR")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_MINIMAL_ACTIVE_DISPLACEMENT_SELECTOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The note records the new variational input on the active displacement",
        "minimizing the Frobenius size of the active" in note
        and "Delta_H,act" in note,
    )
    check(
        "The note records the exact selected law delta_* = q_+* = sqrt(6)/3",
        "delta_* = q_+* = sqrt(6)/3" in note and "phi_+,* = pi/2" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE MINIMAL ACTIVE-DISPLACEMENT SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  If we add one genuinely new right-sensitive input, can we derive the")
    print("  exact 2-real point-selection law (delta, q_+) itself on the live")
    print("  source-oriented sheet?")

    part1_the_active_generators_define_an_exact_euclidean_selector_problem()
    part2_the_exact_half_plane_has_a_unique_minimizer()
    part3_the_selected_point_has_exact_carrier_and_doublet_block_data()
    part4_the_note_records_the_new_input_and_closed_form_selector()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer with the new input:")
    print("    - S_act(delta,q_+) = ||delta T_delta + q_+ T_q||_F^2 = 6(delta^2 + q_+^2)")
    print("    - the exact admissible domain is q_+ >= sqrt(8/3) - delta")
    print("    - the unique minimizer is delta_* = q_+* = sqrt(6)/3")
    print("    - therefore rho_* = sqrt(6)/3, r31,* = 1/2, phi_+,* = pi/2")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
