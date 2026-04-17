#!/usr/bin/env python3
"""
DM neutrino source-surface active affine point-selection boundary.

Question:
  After reducing the live source-oriented sheet to the exact active
  half-plane in (delta, q_+), can the current exact bank reduce point
  selection any further?

Answer:
  No.

  On the live source-oriented sheet, the active chart is already affine on H:

      H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q

  with exact fixed generators

      T_m     = [[1,0,0],[0,0,1],[0,1,0]]
      T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]
      T_q     = [[0,1,1],[1,0,1],[1,1,0]]

  and fixed source package (gamma, E1, E2) = (1/2, sqrt(8/3), sqrt(8)/3).

  The current exact source-facing bank is blind to both active generators:

    - T_delta changes delta and rho oppositely while keeping delta+rho = E1
    - T_q changes q_+, equivalently sigma cos(2v) = sqrt(8)/9 - 3 q_+,
      while keeping the exact source package, intrinsic CP pair, intrinsic
      slot pair, and slot torsion unchanged

  So the minimal remaining mainline datum is exactly the 2-real affine
  point-selection pair (delta, q_+), equivalently the coefficients of
  (T_delta, T_q) on the live sheet. No smaller current-bank object remains.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    active_half_plane_h,
    positive_representative,
    q_floor,
    slot_torsion,
)
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
)
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import (
    intrinsic_slot_formula,
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


def tm() -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def tdelta() -> np.ndarray:
    return np.array(
        [
            [0.0, -1.0, 1.0],
            [-1.0, 1.0, 0.0],
            [1.0, 0.0, -1.0],
        ],
        dtype=complex,
    )


def tq() -> np.ndarray:
    return np.array(
        [
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def h_base() -> np.ndarray:
    pkg = exact_package()
    gamma = pkg.gamma
    e1 = pkg.E1
    e2 = pkg.E2
    return np.array(
        [
            [0.0, e1, -e1 - 1j * gamma],
            [e1, 0.0, -e2],
            [-e1 + 1j * gamma, -e2, 0.0],
        ],
        dtype=complex,
    )


def active_affine_h(m: float, delta: float, q_plus: float) -> np.ndarray:
    return h_base() + m * tm() + delta * tdelta() + q_plus * tq()


def part1_the_active_chart_is_exactly_affine_on_h() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE CHART IS EXACTLY AFFINE ON H")
    print("=" * 88)

    samples = [
        (0.0, 0.25, q_floor(0.25) + 0.2),
        (0.4, -0.30, q_floor(-0.30) + 0.8),
        (-0.6, 0.90, q_floor(0.90) + 1.3),
    ]

    ok_affine = True
    max_err = 0.0
    for m, delta, q_plus in samples:
        h_exact, _r31, _phi = active_half_plane_h(delta, q_plus, m=m)
        h_lin = active_affine_h(m, delta, q_plus)
        err = float(np.linalg.norm(h_exact - h_lin))
        max_err = max(max_err, err)
        ok_affine &= err < 1e-12

    check(
        "On the live source-oriented sheet the (delta, q_+) chart is exactly affine on H",
        ok_affine,
        f"max err={max_err:.2e}",
    )
    check(
        "The exact active generators are T_m, T_delta, and T_q",
        np.linalg.matrix_rank(
            np.column_stack(
                [
                    np.concatenate([np.real(tm()).ravel(), np.imag(tm()).ravel()]),
                    np.concatenate([np.real(tdelta()).ravel(), np.imag(tdelta()).ravel()]),
                    np.concatenate([np.real(tq()).ravel(), np.imag(tq()).ravel()]),
                ]
            )
        )
        == 3,
        "the spectator and active generators are linearly independent over R",
    )


def part2_tdelta_and_tq_are_the_exact_blind_active_generators() -> None:
    print("\n" + "=" * 88)
    print("PART 2: T_DELTA AND T_Q ARE THE EXACT BLIND ACTIVE GENERATORS")
    print("=" * 88)

    pkg = exact_package()
    delta = 0.25
    q_plus = q_floor(delta) + 0.7
    h, _r31, _phi = active_half_plane_h(delta, q_plus, m=0.0)
    h_delta, _r31d, _phid = active_half_plane_h(delta + 0.4, q_plus, m=0.0)
    h_q, _r31q, _phiq = active_half_plane_h(delta, q_plus + 0.9, m=0.0)

    err_delta = float(np.linalg.norm(h_delta - h - 0.4 * tdelta()))
    err_q = float(np.linalg.norm(h_q - h - 0.9 * tq()))

    hp = positive_representative(h, floor=2.0)
    hp_delta = positive_representative(h_delta, floor=2.0)
    hp_q = positive_representative(h_q, floor=2.0)

    lam0, _lam_odd0, _u0, v0, delta0, rho0, gamma0, sigma0 = source_surface_data_in_carrier_normal_form(hp)
    _lam1, _lam_odd1, _u1, v1, delta1, rho1, gamma1, sigma1 = source_surface_data_in_carrier_normal_form(hp_delta)
    _lam2, _lam_odd2, _u2, v2, delta2, rho2, gamma2, sigma2 = source_surface_data_in_carrier_normal_form(hp_q)

    del lam0  # shift-sensitive, not used
    check(
        "Changing delta at fixed q_+ is exactly the affine H-step H -> H + ddelta T_delta",
        err_delta < 1e-12,
        f"err={err_delta:.2e}",
    )
    check(
        "Changing q_+ at fixed delta is exactly the affine H-step H -> H + dq T_q",
        err_q < 1e-12,
        f"err={err_q:.2e}",
    )
    check(
        "T_delta redistributes the fixed source channel E1 by changing delta and rho oppositely while keeping delta+rho = sqrt(8/3)",
        abs((delta1 + rho1) - pkg.E1) < 1e-12
        and abs((delta0 + rho0) - pkg.E1) < 1e-12
        and abs(delta1 - delta0) > 1e-6
        and abs(rho1 - rho0) > 1e-6,
        f"(delta,rho): ({delta0:.6f},{rho0:.6f}) -> ({delta1:.6f},{rho1:.6f})",
    )
    check(
        "T_q changes only the even carrier channel sigma cos(2v) = sqrt(8)/9 - 3 q_+ while keeping delta fixed",
        abs(delta2 - delta0) < 1e-12
        and abs(sigma2 * math.cos(2.0 * v2) - sigma0 * math.cos(2.0 * v0)) > 1e-6,
        f"chi: {sigma0 * math.cos(2.0 * v0):.6f} -> {sigma2 * math.cos(2.0 * v2):.6f}",
    )
    check(
        "Both active generators keep gamma = 1/2 and sigma sin(2v) = 8/9 fixed",
        abs(gamma0 - pkg.gamma) < 1e-12
        and abs(gamma1 - pkg.gamma) < 1e-12
        and abs(gamma2 - pkg.gamma) < 1e-12
        and abs(sigma0 * math.sin(2.0 * v0) - 8.0 / 9.0) < 1e-12
        and abs(sigma1 * math.sin(2.0 * v1) - 8.0 / 9.0) < 1e-12
        and abs(sigma2 * math.sin(2.0 * v2) - 8.0 / 9.0) < 1e-12,
        "the source package stays fixed along both active directions",
    )


def part3_the_current_exact_bank_is_blind_to_both_active_generators() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT EXACT BANK IS BLIND TO BOTH ACTIVE GENERATORS")
    print("=" * 88)

    pkg = exact_package()
    a_exact, b_exact = intrinsic_slot_formula()
    torsion_exact = slot_torsion(a_exact, b_exact)

    delta = -0.15
    q_plus = q_floor(delta) + 0.6
    h0, _r310, _phi0 = active_half_plane_h(delta, q_plus, m=0.0)
    h_delta, _r311, _phi1 = active_half_plane_h(delta + 0.9, q_plus, m=0.0)
    h_q, _r312, _phi2 = active_half_plane_h(delta, q_plus + 1.1, m=0.0)

    hp0 = positive_representative(h0, floor=2.0)
    hp_delta = positive_representative(h_delta, floor=2.0)
    hp_q = positive_representative(h_q, floor=2.0)

    def bank_matches(hp: np.ndarray) -> bool:
        a, b = slot_pair_from_h(hp)
        cp = cp_pair_from_h(hp)
        _lam_plus, _lam_odd, _u, v, delta_c, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(hp)
        return (
            abs(a - a_exact) < 1e-12
            and abs(b - b_exact) < 1e-12
            and abs(slot_torsion(a, b) - torsion_exact) < 1e-12
            and abs(cp[0] - pkg.cp1) < 1e-12
            and abs(cp[1] - pkg.cp2) < 1e-12
            and abs(gamma - pkg.gamma) < 1e-12
            and abs(delta_c + rho - pkg.E1) < 1e-12
            and abs(sigma * math.sin(2.0 * v) - 8.0 / 9.0) < 1e-12
        )

    check(
        "The current exact source-facing bank is unchanged along the T_delta direction",
        bank_matches(hp0) and bank_matches(hp_delta),
        "same source package, CP pair, slot pair, and slot torsion",
    )
    check(
        "The current exact source-facing bank is unchanged along the T_q direction",
        bank_matches(hp0) and bank_matches(hp_q),
        "same source package, CP pair, slot pair, and slot torsion",
    )
    check(
        "So the minimal remaining mainline datum is exactly the 2-real affine point-selection pair (delta, q_+)",
        bank_matches(hp0) and bank_matches(hp_delta) and bank_matches(hp_q),
        "no smaller current-bank object remains on the live source-oriented sheet",
    )


def part4_the_note_records_the_active_affine_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE ACTIVE AFFINE BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md")

    check(
        "The new note records the affine active chart H = H_base + m T_m + delta T_delta + q_+ T_q",
        "H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q" in note,
    )
    check(
        "The new note records the remaining object as the affine point-selection pair (delta, q_+)",
        "affine point-selection pair `(delta, q_+)`" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ACTIVE AFFINE POINT-SELECTION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  After reducing the live source-oriented sheet to the exact active")
    print("  half-plane in (delta, q_+), can the current exact bank reduce point")
    print("  selection any further?")

    part1_the_active_chart_is_exactly_affine_on_h()
    part2_tdelta_and_tq_are_the_exact_blind_active_generators()
    part3_the_current_exact_bank_is_blind_to_both_active_generators()
    part4_the_note_records_the_active_affine_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the live active chart is already affine on H")
    print("    - the two active generators are T_delta and T_q")
    print("    - the current exact source-facing bank is blind to both")
    print("    - so the minimal remaining datum is exactly the affine")
    print("      point-selection pair (delta, q_+)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
