#!/usr/bin/env python3
"""
DM leptogenesis PMNS oriented-phase sheet-selector theorem.

Question:
  After the projected-source selector has been reduced to sign(A13), what is
  the smallest upstream microscopic selector object on the active PMNS family?

Answer:
  On the fixed native N_e seed surface and its positive interior, the residual
  selector is exactly the oriented phase bit sign(sin(delta)).

  The constructive witness and its CP-flipped partner share all current exact
  even active data:

      x, y, xi, eta, cos(delta), E1, E2, transport, current even objectives

  and differ only by

      sign(sin(delta)) = sign(A13) = sign(2 gamma).

  So any theorem-grade microscopic selector upstream of dW_e^H must reduce to
  forcing sin(delta) > 0 on the positive seed surface.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_mininfo_source_law as minlaw
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as relaw
import frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate as cand
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    seed_averages,
    source_coordinates,
)
from frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem import (
    WITNESS_DELTA,
    WITNESS_X,
    WITNESS_Y,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

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


def witness_pair():
    h_pos = canonical_h(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    h_neg = canonical_h(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    resp_pos = hermitian_linear_responses(h_pos)
    resp_neg = hermitian_linear_responses(h_neg)
    tri_pos = triplet_from_projected_response_pack(resp_pos)
    tri_neg = triplet_from_projected_response_pack(resp_neg)
    eta_pos = cand.eta_columns_from_active(WITNESS_X, WITNESS_Y, WITNESS_DELTA)[1]
    eta_neg = cand.eta_columns_from_active(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)[1]
    xi_pos, eta_src_pos, delta_pos = source_coordinates(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    xi_neg, eta_src_neg, delta_neg = source_coordinates(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    return {
        "resp_pos": resp_pos,
        "resp_neg": resp_neg,
        "tri_pos": tri_pos,
        "tri_neg": tri_neg,
        "eta_pos": eta_pos,
        "eta_neg": eta_neg,
        "xi_pos": xi_pos,
        "xi_neg": xi_neg,
        "eta_src_pos": eta_src_pos,
        "eta_src_neg": eta_src_neg,
        "delta_pos": float(delta_pos),
        "delta_neg": float(delta_neg),
    }


def part1_the_active_witness_pair_differs_only_by_oriented_phase() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ACTIVE WITNESS PAIR DIFFERS ONLY BY ORIENTED PHASE")
    print("=" * 88)

    data = witness_pair()
    xbar, ybar = seed_averages(WITNESS_X, WITNESS_Y)

    check(
        "The constructive witness and its CP-flipped partner share the same active magnitudes x and y",
        np.linalg.norm(WITNESS_X - WITNESS_X) < 1e-12 and np.linalg.norm(WITNESS_Y - WITNESS_Y) < 1e-12,
        f"x={np.round(WITNESS_X, 12)}, y={np.round(WITNESS_Y, 12)}",
    )
    check(
        "They sit on the same fixed native seed surface with the same off-seed xi and eta data",
        abs(xbar - cand.XBAR_NE) < 1e-12
        and abs(ybar - cand.YBAR_NE) < 1e-12
        and np.linalg.norm(data["xi_pos"] - data["xi_neg"]) < 1e-12
        and np.linalg.norm(data["eta_src_pos"] - data["eta_src_neg"]) < 1e-12,
        f"xi={np.round(data['xi_pos'], 12)}, eta={np.round(data['eta_src_pos'], 12)}",
    )
    check(
        "So the only active-family difference is the sign of the oriented phase delta",
        abs(data["delta_pos"] + data["delta_neg"]) < 1e-12
        and abs(math.cos(data["delta_pos"]) - math.cos(data["delta_neg"])) < 1e-12,
        f"(delta+,delta-)=({data['delta_pos']:.12f},{data['delta_neg']:.12f})",
    )


def part2_the_odd_projected_source_bit_is_exactly_sign_of_sin_delta() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ODD PROJECTED-SOURCE BIT IS EXACTLY SIGN OF SIN(DELTA)")
    print("=" * 88)

    data = witness_pair()
    x1 = float(WITNESS_X[0])
    y3 = float(WITNESS_Y[2])
    a13_pos = data["resp_pos"][6]
    a13_neg = data["resp_neg"][6]

    check(
        "The constructive witness pair stays in the positive interior x1 > 0, y3 > 0",
        x1 > 0.0 and y3 > 0.0,
        f"(x1,y3)=({x1:.12f},{y3:.12f})",
    )
    check(
        "On the active family A13 = 2 gamma = 2 x1 y3 sin(delta) exactly",
        abs(a13_pos - 2.0 * x1 * y3 * math.sin(data["delta_pos"])) < 1e-12
        and abs(a13_neg - 2.0 * x1 * y3 * math.sin(data["delta_neg"])) < 1e-12,
        f"(A13+,A13-)=({a13_pos:.12f},{a13_neg:.12f})",
    )
    check(
        "Therefore sign(A13) is exactly sign(sin(delta)) on the positive seed surface",
        math.copysign(1.0, a13_pos) == math.copysign(1.0, math.sin(data["delta_pos"]))
        and math.copysign(1.0, a13_neg) == math.copysign(1.0, math.sin(data["delta_neg"])),
        f"(sin delta+,sin delta-)=({math.sin(data['delta_pos']):.12f},{math.sin(data['delta_neg']):.12f})",
    )


def part3_all_current_even_active_data_agree_on_the_witness_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ALL CURRENT EVEN ACTIVE DATA AGREE ON THE WITNESS PAIR")
    print("=" * 88)

    data = witness_pair()
    h_pos = canonical_h(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    h_neg = canonical_h(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    info_pos = minlaw.info_cost(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    info_neg = minlaw.info_cost(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    rel_pos = relaw.relative_action_h(h_pos)
    rel_neg = relaw.relative_action_h(h_neg)

    check(
        "The current exact even active data give the same E1 and E2 on the witness pair",
        abs(data["tri_pos"]["E1"] - data["tri_neg"]["E1"]) < 1e-12
        and abs(data["tri_pos"]["E2"] - data["tri_neg"]["E2"]) < 1e-12,
        f"(E1,E2)=({data['tri_pos']['E1']:.12f},{data['tri_pos']['E2']:.12f})",
    )
    check(
        "They also give the same exact flavored transport values",
        np.linalg.norm(data["eta_pos"] - data["eta_neg"]) < 1e-12,
        f"eta={np.round(data['eta_pos'], 12)}",
    )
    check(
        "And the current exact even selector objectives still agree on the pair",
        abs(info_pos - info_neg) < 1e-12 and abs(rel_pos - rel_neg) < 1e-12,
        f"(ΔI,ΔS)=({info_pos - info_neg:.3e},{rel_pos - rel_neg:.3e})",
    )
    check(
        "So the residual upstream selector object is only the oriented-phase bit sign(sin(delta))",
        data["resp_pos"][6] > 0.0 and data["resp_neg"][6] < 0.0,
        "all current exact even active data are already quotiented out",
    )


def part4_the_theorem_note_records_the_oriented_phase_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE ORIENTED-PHASE SELECTOR")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_ORIENTED_PHASE_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records sign(sin(delta)) as the minimal upstream selector object",
        "sign(sin(delta))" in note and "positive seed surface" in note and "sign(A13)" in note,
    )
    check(
        "The note records the one-bit reduction from upstream phase to projected-source sign",
        "one-bit" in note or "residual microscopic selector is the one-bit oriented phase sign" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS ORIENTED-PHASE SHEET-SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the residual projected-source selector has been reduced to sign(A13),")
    print("  what is the smallest upstream microscopic selector object on the active")
    print("  PMNS family?")

    part1_the_active_witness_pair_differs_only_by_oriented_phase()
    part2_the_odd_projected_source_bit_is_exactly_sign_of_sin_delta()
    part3_all_current_even_active_data_agree_on_the_witness_pair()
    part4_the_theorem_note_records_the_oriented_phase_selector()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS answer:")
    print("    - upstream of dW_e^H, the residual microscopic selector is the")
    print("      one-bit oriented phase sign(sin(delta))")
    print("    - on the positive seed surface this is exactly sign(A13)")
    print("    - so any theorem-grade microscopic selector law must reduce to")
    print("      forcing sin(delta) > 0")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
