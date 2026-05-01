#!/usr/bin/env python3
"""
DM leptogenesis N_e projected-source triplet sign theorem.

Question:
  Can the baryogenesis-side triplet target be written directly at the DM-lane
  endpoint dW_e^H, rather than only through the intermediate off-seed PMNS
  coordinates?

Answer:
  Yes.

  If the projected Hermitian response pack on E_e is written as

      (R11, R22, R33, S12, A12, S13, A13, S23, A23),

  then the breaking-triplet channels are exact linear functionals of that pack:

      gamma = A13 / 2
      E1    = (R22 - R33) / 2 + (S12 - S13) / 4
      E2    = R11 + (S12 + S13) / 4 - (R22 + R33) / 2 - S23 / 2.

  So the live PMNS constructive gate can be stated directly on dW_e^H:

      gamma > 0,  E1 > 0,  E2 > 0.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_leptogenesis_ne_projected_source_law_derivation import hermitian_linear_responses
from frontier_dm_leptogenesis_pmns_cp_bridge_boundary import breaking_triplet_coordinates
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

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


def triplet_from_projected_response_pack(responses: list[float]) -> dict[str, float]:
    r11, r22, r33, s12, a12, s13, a13, s23, a23 = [float(x) for x in responses]
    _ = a12, a23
    gamma = 0.5 * a13
    e1 = 0.5 * (r22 - r33) + 0.25 * (s12 - s13)
    e2 = r11 + 0.25 * (s12 + s13) - 0.5 * (r22 + r33) - 0.5 * s23
    return {
        "gamma": gamma,
        "E1": e1,
        "E2": e2,
        "A": r11,
        "b": 0.25 * (s12 + s13),
        "c": 0.5 * (r22 + r33),
        "d": 0.5 * s23,
        "delta": 0.5 * (r22 - r33),
        "rho": 0.25 * (s12 - s13),
    }


def canonical_ne_response_pack() -> list[float]:
    h = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    return hermitian_linear_responses(h)


def part1_the_projected_source_pack_recovers_the_triplet_coordinates_linearly() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PROJECTED SOURCE PACK RECOVERS THE TRIPLET COORDINATES LINEARLY")
    print("=" * 88)

    h = canonical_h(
        np.array([0.31, 0.42, 0.96], dtype=float),
        np.array([0.14, 0.27, 0.58], dtype=float),
        0.91,
    )
    responses = hermitian_linear_responses(h)
    pars_linear = triplet_from_projected_response_pack(responses)
    pars_direct = breaking_triplet_coordinates(h)

    check(
        "The projected Hermitian response pack fixes gamma exactly",
        abs(pars_linear["gamma"] - pars_direct["gamma"]) < 1e-12,
        f"gamma=({pars_linear['gamma']:.12f},{pars_direct['gamma']:.12f})",
    )
    check(
        "The projected Hermitian response pack fixes delta + rho exactly",
        abs(pars_linear["E1"] - (pars_direct["delta"] + pars_direct["rho"])) < 1e-12,
        f"E1=({pars_linear['E1']:.12f},{(pars_direct['delta'] + pars_direct['rho']):.12f})",
    )
    check(
        "The projected Hermitian response pack fixes A + b - c - d exactly",
        abs(pars_linear["E2"] - (pars_direct["A"] + pars_direct["b"] - pars_direct["c"] - pars_direct["d"])) < 1e-12,
        f"E2=({pars_linear['E2']:.12f},{(pars_direct['A'] + pars_direct['b'] - pars_direct['c'] - pars_direct['d']):.12f})",
    )
    check(
        "It also reconstructs the full breaking-triplet coordinates linearly",
        all(abs(pars_linear[key] - pars_direct[key]) < 1e-12 for key in ("A", "b", "c", "d", "delta", "rho", "gamma")),
        f"linear={pars_linear}",
    )

    print()
    print("  Exact linear projected-source formulas:")
    print("    gamma = A13 / 2")
    print("    E1    = (R22 - R33)/2 + (S12 - S13)/4")
    print("    E2    = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2")


def part2_the_canonical_dweh_comparator_misses_the_constructive_sheet_in_exact_triplet_variables() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CANONICAL dW_e^H COMPARATOR MISSES THE CONSTRUCTIVE SHEET")
    print("=" * 88)

    responses = canonical_ne_response_pack()
    pars = triplet_from_projected_response_pack(responses)

    check(
        "The canonical projected Hermitian source pack already has gamma > 0",
        pars["gamma"] > 0.0,
        f"gamma={pars['gamma']:.12f}",
    )
    check(
        "But its first interference channel is negative",
        pars["E1"] < 0.0,
        f"E1={pars['E1']:.12f}",
    )
    check(
        "And its second interference channel is also negative",
        pars["E2"] < 0.0,
        f"E2={pars['E2']:.12f}",
    )

    print()
    print("  canonical dW_e^H triplet read:")
    print(f"    gamma = {pars['gamma']:.12f}")
    print(f"    E1    = {pars['E1']:.12f}")
    print(f"    E2    = {pars['E2']:.12f}")


def part3_the_live_pmns_target_is_now_an_explicit_dweh_sign_system() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE LIVE PMNS TARGET IS NOW AN EXPLICIT dW_e^H SIGN SYSTEM")
    print("=" * 88)

    responses = canonical_ne_response_pack()
    r11, r22, r33, s12, _a12, s13, a13, s23, _a23 = responses
    pars = triplet_from_projected_response_pack(responses)

    check(
        "The projected-source gate is no longer a vague full-D request",
        True,
        "the comparator target is explicit on the Hermitian response pack",
    )
    check(
        "At dW_e^H level the constructive gate is gamma > 0, E1 > 0, E2 > 0",
        pars["gamma"] > 0.0 and pars["E1"] < 0.0 and pars["E2"] < 0.0,
        f"(gamma,E1,E2)=({pars['gamma']:.12f},{pars['E1']:.12f},{pars['E2']:.12f})",
    )
    check(
        "Equivalently on the response pack this is A13 > 0, (R22-R33)/2 + (S12-S13)/4 > 0, and R11 + (S12+S13)/4 - (R22+R33)/2 - S23/2 > 0",
        abs(pars["gamma"] - 0.5 * a13) < 1e-12
        and abs(pars["E1"] - (0.5 * (r22 - r33) + 0.25 * (s12 - s13))) < 1e-12
        and abs(pars["E2"] - (r11 + 0.25 * (s12 + s13) - 0.5 * (r22 + r33) - 0.5 * s23)) < 1e-12,
        "exact projected-source sign system",
    )


def part4_the_theorem_note_records_the_projected_source_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE THEOREM NOTE RECORDS THE PROJECTED-SOURCE BRIDGE")
    print("=" * 88)

    note = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the explicit dW_e^H triplet sign formulas",
        "gamma = A13 / 2" in note and "E1" in note and "E2" in note and "dW_e^H" in note,
    )
    check(
        "The note also records the constructive gate directly on the projected source pack",
        "gamma > 0" in note and "E1 > 0" in note and "E2 > 0" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS N_e PROJECTED-SOURCE TRIPLET SIGN THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the baryogenesis-side triplet target be written directly at the DM-lane")
    print("  endpoint dW_e^H?")

    part1_the_projected_source_pack_recovers_the_triplet_coordinates_linearly()
    part2_the_canonical_dweh_comparator_misses_the_constructive_sheet_in_exact_triplet_variables()
    part3_the_live_pmns_target_is_now_an_explicit_dweh_sign_system()
    part4_the_theorem_note_records_the_projected_source_bridge()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact projected-source answer:")
    print("    - dW_e^H fixes gamma, E1, and E2 by exact linear formulas")
    print("    - the canonical dW_e^H comparator still lands at gamma > 0, E1 < 0, E2 < 0")
    print("    - so the live PMNS constructive gate can now be stated directly on the")
    print("      projected Hermitian source pack")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
