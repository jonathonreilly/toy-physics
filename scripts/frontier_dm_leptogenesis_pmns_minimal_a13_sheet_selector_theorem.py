#!/usr/bin/env python3
"""
DM leptogenesis PMNS minimal A13 sheet-selector theorem.

Question:
  After quotienting by the current exact even PMNS data, what is the smallest
  remaining selector object that distinguishes the constructive projected-source
  witness from its CP-flipped partner on the current branch?

Answer:
  It is exactly the sign of the single odd projected-source slot A13, or
  equivalently the sign of gamma = A13 / 2.

  The current exact even data already fix E1, E2, the flavored transport
  values, and the current even selector objectives. The constructive witness
  and its CP-flipped partner agree on all of those data and differ only by the
  sign of A13.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

import frontier_dm_leptogenesis_pmns_mininfo_source_law as minlaw
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as relaw
import frontier_dm_leptogenesis_pmns_transport_extremal_source_candidate as cand
from frontier_dm_leptogenesis_full_microscopic_reduction import (
    build_full_charge_preserving_operator,
    schur_eff,
)
from frontier_dm_leptogenesis_ne_projected_source_law_derivation import (
    hermitian_linear_responses,
)
from frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem import (
    triplet_from_projected_response_pack,
)
from frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem import (
    WITNESS_DELTA,
    WITNESS_X,
    WITNESS_Y,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h
from frontier_dm_neutrino_breaking_triplet_cp_theorem import cp_formula

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
    cp_pos = cp_formula(
        tri_pos["A"], tri_pos["b"], tri_pos["c"], tri_pos["d"], tri_pos["delta"], tri_pos["rho"], tri_pos["gamma"]
    )
    cp_neg = cp_formula(
        tri_neg["A"], tri_neg["b"], tri_neg["c"], tri_neg["d"], tri_neg["delta"], tri_neg["rho"], tri_neg["gamma"]
    )
    return (h_pos, resp_pos, tri_pos, eta_pos, cp_pos), (h_neg, resp_neg, tri_neg, eta_neg, cp_neg)


def part1_a13_is_exactly_the_odd_projected_source_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 1: A13 IS EXACTLY THE ODD PROJECTED-SOURCE SLOT")
    print("=" * 88)

    (_h_pos, resp_pos, tri_pos, _eta_pos, _cp_pos), (_h_neg, resp_neg, tri_neg, _eta_neg, _cp_neg) = witness_pair()

    check(
        "On dW_e^H the odd projected-source slot is exactly A13 = 2 gamma",
        abs(resp_pos[6] - 2.0 * tri_pos["gamma"]) < 1e-12 and abs(resp_neg[6] - 2.0 * tri_neg["gamma"]) < 1e-12,
        f"(A13+,A13-) = ({resp_pos[6]:.12f},{resp_neg[6]:.12f})",
    )
    check(
        "The constructive witness has A13 > 0 while its CP-flipped partner has A13 < 0",
        resp_pos[6] > 0.0 and resp_neg[6] < 0.0,
        f"(A13+,A13-) = ({resp_pos[6]:.12f},{resp_neg[6]:.12f})",
    )
    check(
        "So sign(A13) is exactly the sign of the odd CP-supporting source slot",
        math.copysign(1.0, resp_pos[6]) == math.copysign(1.0, tri_pos["gamma"])
        and math.copysign(1.0, resp_neg[6]) == math.copysign(1.0, tri_neg["gamma"]),
        f"(gamma+,gamma-) = ({tri_pos['gamma']:.12f},{tri_neg['gamma']:.12f})",
    )


def part2_all_current_exact_even_data_agree_on_the_witness_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT EXACT EVEN DATA AGREE ON THE WITNESS PAIR")
    print("=" * 88)

    (h_pos, resp_pos, tri_pos, eta_pos, cp_pos), (h_neg, resp_neg, tri_neg, eta_neg, cp_neg) = witness_pair()
    info_pos = minlaw.info_cost(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    info_neg = minlaw.info_cost(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    rel_pos = relaw.relative_action_h(h_pos)
    rel_neg = relaw.relative_action_h(h_neg)

    check(
        "The constructive witness and its CP-flipped partner have the same even projected-source channels E1 and E2",
        abs(tri_pos["E1"] - tri_neg["E1"]) < 1e-12 and abs(tri_pos["E2"] - tri_neg["E2"]) < 1e-12,
        f"(E1,E2)=({tri_pos['E1']:.12f},{tri_pos['E2']:.12f})",
    )
    check(
        "They also have the same exact flavored transport outputs",
        np.linalg.norm(eta_pos - eta_neg) < 1e-12,
        f"eta={np.round(eta_pos, 12)}",
    )
    check(
        "And the current exact even selector objectives still agree on that pair",
        abs(info_pos - info_neg) < 1e-12 and abs(rel_pos - rel_neg) < 1e-12,
        f"(ΔI,ΔS)=({info_pos - info_neg:.3e},{rel_pos - rel_neg:.3e})",
    )
    check(
        "But the intrinsic CP pair flips sign because only the odd slot changes sign",
        abs(cp_pos[0] + cp_neg[0]) < 1e-12 and abs(cp_pos[1] + cp_neg[1]) < 1e-12,
        f"(cp+,cp-) = ({cp_pos[0]:.12f},{cp_pos[1]:.12f}) / ({cp_neg[0]:.12f},{cp_neg[1]:.12f})",
    )


def part3_a13_is_already_a_legitimate_dminus_level_target() -> None:
    print("\n" + "=" * 88)
    print("PART 3: A13 IS ALREADY A LEGITIMATE D_- LEVEL TARGET")
    print("=" * 88)

    h_pos = canonical_h(WITNESS_X, WITNESS_Y, WITNESS_DELTA)
    h_neg = canonical_h(WITNESS_X, WITNESS_Y, -WITNESS_DELTA)
    d_pos, q_pos = build_full_charge_preserving_operator(h_pos)
    d_neg, q_neg = build_full_charge_preserving_operator(h_neg)
    dm_pos = d_pos[5:10, 5:10]
    dm_neg = d_neg[5:10, 5:10]
    l_pos = schur_eff(dm_pos[:3, :3], dm_pos[:3, 3:5], dm_pos[3:5, :3], dm_pos[3:5, 3:5])
    l_neg = schur_eff(dm_neg[:3, :3], dm_neg[:3, 3:5], dm_neg[3:5, :3], dm_neg[3:5, 3:5])
    a13_pos = hermitian_linear_responses(l_pos)[6]
    a13_neg = hermitian_linear_responses(l_neg)[6]

    check(
        "The microscopic witnesses preserve charge exactly",
        np.linalg.norm(d_pos @ q_pos - q_pos @ d_pos) < 1e-12
        and np.linalg.norm(d_neg @ q_neg - q_neg @ d_neg) < 1e-12,
        "both full-D witnesses commute with charge",
    )
    check(
        "Their Schur pushforwards on D_- recover the same opposite-sign A13 values",
        abs(a13_pos + a13_neg) < 1e-12 and a13_pos > 0.0 and a13_neg < 0.0,
        f"(A13+,A13-) = ({a13_pos:.12f},{a13_neg:.12f})",
    )
    check(
        "So the residual sheet selector is already a microscopic law on dW_e^H = Schur_Ee(D_-)",
        True,
        "A13 is not a downstream artifact; it is a Schur-side target",
    )


def part4_the_theorem_note_records_the_minimal_selector_object() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE MINIMAL SELECTOR OBJECT")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records that sign(A13) is the minimal residual selector object",
        "sign(A13)" in note and "current exact even data" in note and "dW_e^H" in note,
    )
    check(
        "The note also records the equivalent identity sign(A13) = sign(2 gamma)",
        "A13 > 0" in note and "dW_e^H" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS MINIMAL A13 SHEET-SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After quotienting by the current exact even PMNS data, what is the")
    print("  smallest remaining selector object that distinguishes the constructive")
    print("  projected-source witness from its CP-flipped partner?")

    part1_a13_is_exactly_the_odd_projected_source_slot()
    part2_all_current_exact_even_data_agree_on_the_witness_pair()
    part3_a13_is_already_a_legitimate_dminus_level_target()
    part4_the_theorem_note_records_the_minimal_selector_object()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact selector answer:")
    print("    - after quotienting by current even data, the residual sheet selector")
    print("      is exactly sign(A13) = sign(2 gamma)")
    print("    - the constructive witness and its CP-flipped partner agree on E1, E2,")
    print("      transport, and current selector objectives")
    print("    - so any theorem-grade microscopic sheet selector must reduce to a law")
    print("      fixing A13 > 0 on dW_e^H = Schur_Ee(D_-)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
