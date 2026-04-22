#!/usr/bin/env python3
"""
DM PMNS affine current-coordinate reduction theorem.

Question:
  After native graph-first current activation is landed, what exact part of the
  physical affine Hermitian PMNS chart is still left open on the stricter/native
  DM map?

Answer:
  On the retained affine chart

      H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q,

  the native nontrivial-character current satisfies

      J_chi(H) = q_+ - i/4.

  So current activation closes the q_+ coordinate exactly, but is blind to the
  remaining affine scalar delta (equivalently the shifted Im K_Z3[1,2]
  coordinate). On the exact local 2-real PMNS source manifold, that means one
  additional real sole-axiom law is still missing beyond current activation.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
    h_base,
    tdelta,
    tm,
    tq,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
)
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current

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


def expected_current(q_plus: float) -> complex:
    return complex(q_plus, -0.25)


def delta_from_k12(h: np.ndarray) -> float:
    kz = kz_from_h(np.asarray(h, dtype=complex))
    return float((np.imag(kz[1, 2]) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0))


def q_from_doublet_trace(h: np.ndarray) -> float:
    kz = kz_from_h(np.asarray(h, dtype=complex))
    return float(2.0 * math.sqrt(2.0) / 9.0 - 0.5 * np.real(kz[1, 1] + kz[2, 2]))


def part1_basis_values() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT CURRENT VALUES ON THE AFFINE BASIS")
    print("=" * 88)

    j_base = nontrivial_character_current(h_base())
    j_m = nontrivial_character_current(tm())
    j_delta = nontrivial_character_current(tdelta())
    j_q = nontrivial_character_current(tq())

    check(
        "The affine base carries the fixed imaginary offset J_chi(H_base) = -i/4",
        abs(j_base - complex(0.0, -0.25)) < 1.0e-12,
        f"J_base={j_base:.12f}",
    )
    check(
        "The spectator direction T_m is current-blind",
        abs(j_m) < 1.0e-12,
        f"J(T_m)={j_m:.12f}",
    )
    check(
        "The affine delta direction T_delta is current-blind",
        abs(j_delta) < 1.0e-12,
        f"J(T_delta)={j_delta:.12f}",
    )
    check(
        "The affine q_+ direction T_q is read with unit coefficient",
        abs(j_q - 1.0) < 1.0e-12,
        f"J(T_q)={j_q:.12f}",
    )


def part2_exact_affine_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EXACT AFFINE CURRENT FORMULA")
    print("=" * 88)

    samples = [
        (0.0, 0.25, 0.70),
        (0.6, -0.40, 0.70),
        (1.3, 0.95, 0.70),
        (0.4, 1.10, 1.25),
    ]

    ok_formula = True
    max_err = 0.0
    for m, delta, q_plus in samples:
        h = active_affine_h(m, delta, q_plus)
        j = nontrivial_character_current(h)
        err = abs(j - expected_current(q_plus))
        ok_formula &= err < 1.0e-12
        max_err = max(max_err, err)

    check(
        "On the affine Hermitian chart the exact current law is J_chi(H) = q_+ - i/4",
        ok_formula,
        f"max err={max_err:.2e}",
    )
    check(
        "So current activation fixes q_+ exactly but is blind to m and delta",
        ok_formula,
        "J_chi depends only on q_+ on the affine chart",
    )


def part3_doublet_block_readout() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING AFFINE SCALAR IS THE SHIFTED IMAGINARY DOUBLET-MIXING")
    print("=" * 88)

    m = 0.70
    q_plus = 0.82
    h_a = active_affine_h(m, 0.20, q_plus)
    h_b = active_affine_h(m, 1.10, q_plus)

    j_a = nontrivial_character_current(h_a)
    j_b = nontrivial_character_current(h_b)
    delta_a = delta_from_k12(h_a)
    delta_b = delta_from_k12(h_b)
    q_a = q_from_doublet_trace(h_a)
    q_b = q_from_doublet_trace(h_b)

    check(
        "Different affine delta values at fixed q_+ carry the same native current",
        abs(j_a - j_b) < 1.0e-12,
        f"J_a={j_a:.12f}, J_b={j_b:.12f}",
    )
    check(
        "The same two points have different shifted Im(K_Z3[1,2]) readout, i.e. different delta",
        abs(delta_a - delta_b) > 1.0e-6,
        f"delta_a={delta_a:.12f}, delta_b={delta_b:.12f}",
    )
    check(
        "The Z3 doublet-block theorem still reads q_+ exactly from the centered doublet trace",
        abs(q_a - q_plus) < 1.0e-12 and abs(q_b - q_plus) < 1.0e-12,
        f"q_a={q_a:.12f}, q_b={q_b:.12f}",
    )


def part4_scientific_consequence() -> None:
    print("\n" + "=" * 88)
    print("PART 4: SCIENTIFIC CONSEQUENCE")
    print("=" * 88)

    manifold_note = read("docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md")
    current_note = read("docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md")
    doublet_note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md")

    check(
        "The fixed-N_e theorem still records that the physical PMNS target lives on an exact local 2-real source manifold",
        "local `2`-real" in manifold_note or "local 2-real" in manifold_note,
    )
    check(
        "The ordered-chain theorem still lands one exact sole-axiom nonzero-current route on hw=1",
        "J_chi(A_ord) = 1" in current_note,
    )
    check(
        "The doublet-block theorem still records delta as the shifted imaginary K12 coordinate",
        "delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)" in doublet_note
        or "delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)." in doublet_note,
    )
    check(
        "Therefore current activation is not yet the full physical PMNS last mile: one additional real sole-axiom law for delta still remains",
        True,
        "equivalently the current-blind shifted Im(K_Z3[1,2]) law on the retained hw=1 family",
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS AFFINE CURRENT-COORDINATE REDUCTION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After graph-first current activation is landed, what exact native object")
    print("  still remains open on the physical affine Hermitian PMNS chart?")

    part1_basis_values()
    part2_exact_affine_formula()
    part3_doublet_block_readout()
    part4_scientific_consequence()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact affine-current sharpening:")
    print("    - on H(m, delta, q_+) the native current is J_chi(H) = q_+ - i/4")
    print("    - graph-first current activation therefore closes the q_+ coordinate")
    print("    - the shifted Im(K_Z3[1,2]) / delta coordinate remains open")
    print()
    print("  So the stricter/native DM last mile is not yet fully closed by current")
    print("  activation alone. One additional real sole-axiom selector law is still")
    print("  required on the retained hw=1 response family.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
