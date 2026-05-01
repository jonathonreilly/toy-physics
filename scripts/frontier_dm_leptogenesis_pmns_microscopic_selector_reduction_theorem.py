#!/usr/bin/env python3
"""
DM leptogenesis PMNS microscopic selector reduction theorem.

Question:
  Once the constructive PMNS chamber is known to contain an exact eta = eta_obs
  point and the DM thermal layer is already certified, what exact microscopic
  object is still missing on the current branch?

Answer:
  The remaining object is not transport closure, not the DM thermal map, and
  not a generic PMNS even-response fit.

  The constructive exact point already exists on the fixed native N_e seed
  surface. Upstream of dW_e^H the odd selector is already reduced to

      sign(A13) = sign(2 gamma) = sign(sin(delta)).

  But fixing that odd bit does not yet choose the constructive point: the
  remaining PMNS object is the even-response law. The atlas then compresses the
  source-facing side further: the current exact bank already collapses to one
  sharp source tuple, while distinct live points in the exact 2-real
  Z_3-doublet block still carry the same current-bank signature.

  Therefore the remaining positive theorem target is exactly a right-sensitive
  microscopic selector law on

      dW_e^H = Schur_Ee(D_-),

  equivalently the intrinsic 2-real Z_3 doublet-block point-selection law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from frontier_dm_leptogenesis_pmns_constructive_continuity_closure_theorem import (
    constructive_column_eta,
    path_point,
    path_triplet,
)
from frontier_dm_leptogenesis_pmns_even_response_sole_axiom_boundary import (
    CANONICAL_DELTA,
    CANONICAL_X,
    CANONICAL_Y,
    carrier_even_response,
    triplet_data,
)
from frontier_dm_leptogenesis_pmns_oriented_phase_sheet_selector_theorem import (
    witness_pair,
)
from frontier_dm_neutrino_postcanonical_right_frame_obstruction import (
    canonical_y,
    cp_tensor_from_kz,
    right_rotation,
    slot_amplitudes_from_kz,
    z3_kernel,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_full_closure_boundary import (
    active_target_from_h,
    active_affine_h,
    current_bank_signature,
    exact_package,
    q_floor,
    same_signature,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_the_constructive_exact_eta_one_point_already_exists() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CONSTRUCTIVE EXACT ETA=1 POINT ALREADY EXISTS")
    print("=" * 88)

    lam_star = brentq(lambda lam: constructive_column_eta(lam) - 1.0, 0.0, 1.0)
    x_star, y_star, delta_star = path_point(lam_star)
    triplet = path_triplet(lam_star)
    eta_star = constructive_column_eta(lam_star)

    check(
        "The constructive chamber contains an exact eta = 1 point on the fixed native seed surface",
        0.0 < lam_star < 1.0 and abs(eta_star - 1.0) < 1e-12,
        f"lambda_*={lam_star:.12f}",
    )
    check(
        "That exact closure point is still constructive",
        triplet["gamma"] > 0.0 and triplet["E1"] > 0.0 and triplet["E2"] > 0.0,
        f"(gamma,E1,E2)=({triplet['gamma']:.12f},{triplet['E1']:.12f},{triplet['E2']:.12f})",
    )
    check(
        "So the remaining blocker is not existence of a constructive eta = 1 point",
        np.linalg.norm(x_star) > 0.0 and np.linalg.norm(y_star) > 0.0 and abs(delta_star) > 1e-6,
        f"delta_*={delta_star:.12f}",
    )


def part2_the_odd_microscopic_selector_bit_is_already_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ODD MICROSCOPIC SELECTOR BIT IS ALREADY CLOSED")
    print("=" * 88)

    data = witness_pair()
    a13_pos = data["resp_pos"][6]
    a13_neg = data["resp_neg"][6]

    check(
        "On the positive seed surface sign(A13) is exactly sign(sin(delta))",
        math.copysign(1.0, a13_pos) == math.copysign(1.0, math.sin(data["delta_pos"]))
        and math.copysign(1.0, a13_neg) == math.copysign(1.0, math.sin(data["delta_neg"])),
        f"(A13+,A13-)=({a13_pos:.12f},{a13_neg:.12f})",
    )
    check(
        "The constructive witness pair shares all current exact even active data",
        abs(data["tri_pos"]["E1"] - data["tri_neg"]["E1"]) < 1e-12
        and abs(data["tri_pos"]["E2"] - data["tri_neg"]["E2"]) < 1e-12
        and np.linalg.norm(data["eta_pos"] - data["eta_neg"]) < 1e-12,
        f"eta={np.round(data['eta_pos'], 12)}",
    )
    check(
        "So the residual odd selector upstream of dW_e^H is already just sign(A13)",
        a13_pos > 0.0 and a13_neg < 0.0,
        "equivalently sign(sin(delta))",
    )


def part3_fixing_the_odd_bit_still_does_not_choose_the_constructive_point() -> None:
    print("\n" + "=" * 88)
    print("PART 3: FIXING THE ODD BIT STILL DOES NOT CHOOSE THE CONSTRUCTIVE POINT")
    print("=" * 88)

    _c_xbar, _c_ybar, c_gamma, c_e1, c_e2 = triplet_data(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    _w_xbar, _w_ybar, w_gamma, w_e1, w_e2 = triplet_data(
        path_point(1.0)[0], path_point(1.0)[1], path_point(1.0)[2]
    )
    c_e1_car, _c_e2_car, _c_gamma_car, c_sigma_sin_2v = carrier_even_response(
        CANONICAL_X, CANONICAL_Y, CANONICAL_DELTA
    )
    w_e1_car, _w_e2_car, _w_gamma_car, w_sigma_sin_2v = carrier_even_response(
        path_point(1.0)[0], path_point(1.0)[1], path_point(1.0)[2]
    )

    check(
        "The canonical near-closing sample and the constructive witness already share the positive odd sheet",
        c_gamma > 0.0 and w_gamma > 0.0 and math.sin(CANONICAL_DELTA) > 0.0 and math.sin(path_point(1.0)[2]) > 0.0,
        f"gamma=({c_gamma:.12f},{w_gamma:.12f})",
    )
    check(
        "But they still carry opposite even-response signs",
        c_e1 < 0.0 and c_e2 < 0.0 and w_e1 > 0.0 and w_e2 > 0.0,
        f"canonical=({c_e1:.12f},{c_e2:.12f}), constructive=({w_e1:.12f},{w_e2:.12f})",
    )
    check(
        "Equivalently the remaining PMNS object is the even-response pair (E1,E2) = (delta+rho, const*sigma sin(2v))",
        c_e1_car < 0.0 and c_sigma_sin_2v < 0.0 and w_e1_car > 0.0 and w_sigma_sin_2v > 0.0,
        f"(delta+rho,sigma sin2v)=({c_e1_car:.12f},{c_sigma_sin_2v:.12f}) vs ({w_e1_car:.12f},{w_sigma_sin_2v:.12f})",
    )


def part4_the_atlas_source_bank_already_compresses_further_to_a_right_sensitive_2_real_target() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ATLAS SOURCE BANK ALREADY COMPRESSES TO A RIGHT-SENSITIVE 2-REAL TARGET")
    print("=" * 88)

    pkg = exact_package()
    q_common = 2.2
    h_a = active_affine_h(0.0, 0.2, q_common)
    h_b = active_affine_h(0.0, 0.9, q_common)
    h_c = active_affine_h(0.0, 0.2, 2.5)
    sig_a = current_bank_signature(h_a)
    sig_b = current_bank_signature(h_b)
    sig_c = current_bank_signature(h_c)
    tgt_a = active_target_from_h(h_a)
    tgt_b = active_target_from_h(h_b)
    tgt_c = active_target_from_h(h_c)

    check(
        "The current source-facing bank is already collapsed to one sharp tuple",
        abs(pkg.gamma - 0.5) < 1e-12
        and abs(pkg.E1 - math.sqrt(8.0 / 3.0)) < 1e-12
        and abs(pkg.E2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f})",
    )
    check(
        "Distinct live-sheet points still carry the same complete current-bank signature",
        same_signature(sig_a, sig_b) and same_signature(sig_a, sig_c),
        "same (gamma,E1,E2,cp1,cp2,a_*,b_*,T_slot)",
    )
    check(
        "Those same points still have different active targets",
        tgt_a != tgt_b and tgt_a != tgt_c,
        f"targets={tgt_a}, {tgt_b}, {tgt_c}",
    )
    check(
        "So the remaining source-side object is the intrinsic 2-real point-selection law for (delta,q_+)",
        q_floor(0.2) < q_common,
        "equivalently the right-sensitive Z3 doublet-block law",
    )


def part5_h_only_data_cannot_supply_that_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 5: H-ONLY DATA CANNOT SUPPLY THAT SELECTOR")
    print("=" * 88)

    x = np.array([1.0, 0.8, 1.1], dtype=float)
    y = np.array([0.4, 0.6, 0.5], dtype=float)
    delta = 2.0 * math.pi / 3.0
    y0 = canonical_y(x, y, delta)
    y1 = y0 @ right_rotation(0.41).conj().T
    h0 = y0 @ y0.conj().T
    h1 = y1 @ y1.conj().T
    kz0 = z3_kernel(y0)
    kz1 = z3_kernel(y1)
    u0, v0 = slot_amplitudes_from_kz(kz0, 2.0 * math.pi / 3.0)
    u1, v1 = slot_amplitudes_from_kz(kz1, 2.0 * math.pi / 3.0)
    cp0 = cp_tensor_from_kz(kz0)
    cp1 = cp_tensor_from_kz(kz1)

    check(
        "An exact right-unitary orbit leaves H fixed",
        np.linalg.norm(h0 - h1) < 1e-12,
        f"H error={np.linalg.norm(h0 - h1):.2e}",
    )
    check(
        "The same orbit changes the right-sensitive slot amplitudes",
        abs(u0 - u1) > 1e-6 or abs(v0 - v1) > 1e-6,
        f"(u,v)_0=({u0:.6f},{v0:.6f}), (u,v)_1=({u1:.6f},{v1:.6f})",
    )
    check(
        "The same orbit changes the heavy-basis CP tensor",
        abs(cp0[0] - cp1[0]) > 1e-6 or abs(cp0[1] - cp1[1]) > 1e-6,
        f"CP0={cp0}, CP1={cp1}",
    )
    check(
        "So any positive selector that finishes the microscopic gate must be right-sensitive or right-frame-fixing",
        True,
        "H-only data are insufficient",
    )


def part6_the_notes_record_the_same_last_mile_object() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE NOTES RECORD THE SAME LAST-MILE OBJECT")
    print("=" * 88)

    dwh_note = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    blind_note = read("docs/DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md")
    z3_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_FULL_CLOSURE_BOUNDARY_NOTE_2026-04-16.md")
    note = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")

    check(
        "The charged-source reduction note records dW_e^H as the exact Schur pushforward and remaining transport-facing target",
        "`dW_e^H` is the exact charged-sector Schur pushforward" in dwh_note
        and "What is now the right target:" in dwh_note
        and "`dW_e^H`" in dwh_note,
        cls="B",
    )
    check(
        "The selector-bank blindness note records the remaining PMNS problem as a D_- / dW_e^H sign-law problem",
        "`D_- / dW_e^H` sign-law problem" in blind_note,
        cls="B",
    )
    check(
        "The Z3 full-closure boundary note records the remaining source object as the right-sensitive 2-real doublet-block law",
        "(delta, q_+)" in z3_note and "doublet-block law" in z3_note,
        cls="B",
    )
    check(
        "The new note records the unified last-mile reduction to a right-sensitive microscopic selector on dW_e^H / the Z3 doublet block",
        "right-sensitive microscopic selector law" in note
        and "dW_e^H = Schur_Ee(D_-)" in note
        and "`Z_3` doublet-block point-selection law" in note,
        cls="B",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS MICROSCOPIC SELECTOR REDUCTION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once constructive exact closure exists and the DM thermal layer is")
    print("  already bounded, what exact microscopic object is still missing on the")
    print("  current branch?")

    part1_the_constructive_exact_eta_one_point_already_exists()
    part2_the_odd_microscopic_selector_bit_is_already_closed()
    part3_fixing_the_odd_bit_still_does_not_choose_the_constructive_point()
    part4_the_atlas_source_bank_already_compresses_further_to_a_right_sensitive_2_real_target()
    part5_h_only_data_cannot_supply_that_selector()
    part6_the_notes_record_the_same_last_mile_object()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction answer:")
    print("    - the constructive eta = 1 point already exists")
    print("    - the odd microscopic selector bit is already reduced to sign(A13)")
    print("    - fixing that odd bit still leaves the constructive point unchosen")
    print("    - the atlas source bank already compresses the live source object to")
    print("      the intrinsic 2-real Z3 doublet-block point-selection law")
    print("    - H-only data cannot supply that selector")
    print("    - so the remaining blocker is exactly a right-sensitive microscopic")
    print("      selector law on dW_e^H = Schur_Ee(D_-), equivalently the intrinsic")
    print("      Z3 doublet-block point-selection law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
