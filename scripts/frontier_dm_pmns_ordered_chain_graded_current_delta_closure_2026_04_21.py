#!/usr/bin/env python3
"""
DM PMNS ordered-chain graded-current delta closure theorem.

Question:
  After native graph-first current activation closes q_+ on the physical
  affine Hermitian chart, is there an exact same-branch sole-axiom law for the
  remaining delta / Im(K_Z3[1,2]) direction on the retained hw=1 response
  family?

Answer:
  Yes.

  Let N = diag(1,2,3) be the canonical ordered-chain grading already fixed by
  the graph-first selector, cycle-frame support theorem, and adjacent-chain
  path algebra. Define the graded current

      J_N(H) := J_chi(i [N, H]).

  On the physical affine chart

      H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q

  this current satisfies the exact formula

      J_N(H) = -1/2 + i (E1/2 - delta/2 - 3 q_+/2),

  where E1 = sqrt(8/3).

  Since the affine current theorem already gives

      J_chi(H) = q_+ - i/4,

  the affine active pair is recovered exactly by

      q_+(H) = Re J_chi(H),
      delta(H) = E1 - 2 Im J_N(H) - 3 Re J_chi(H).

  The same formulas survive exactly after passage to the retained hw=1
  response columns. So the remaining strict/native DM scalar last mile is
  closed on the physical affine/source family.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
    h_base,
    tdelta,
    tm,
    tq,
)
from frontier_dm_pmns_graph_first_ordered_chain_nonzero_current_closure_2026_04_21 import (
    chain_number_operator,
)
from frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20 import (
    CHAMBER_ROOTS,
)
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from pmns_lower_level_utils import (
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
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


def graded_current(h: np.ndarray) -> complex:
    n = chain_number_operator()
    return nontrivial_character_current(1j * (n @ h - h @ n))


def expected_graded_current(m: float, delta: float, q_plus: float) -> complex:
    e1 = exact_package().E1
    return complex(-0.5, 0.5 * e1 - 0.5 * delta - 1.5 * q_plus)


def delta_from_currents(h: np.ndarray) -> float:
    e1 = exact_package().E1
    j = nontrivial_character_current(h)
    jn = graded_current(h)
    return float(e1 - 2.0 * np.imag(jn) - 3.0 * np.real(j))


def q_from_current(h: np.ndarray) -> float:
    return float(np.real(nontrivial_character_current(h)))


def part1_the_ordered_chain_grading_is_already_canonical() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ORDERED-CHAIN GRADING IS ALREADY CANONICAL")
    print("=" * 88)

    ordered_note = read(
        "docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md"
    )
    n = chain_number_operator()

    check(
        "The ordered-chain activation theorem records the canonical grading N = diag(1,2,3)",
        "N = diag(1,2,3)" in ordered_note or "N = diag(1, 2, 3)" in ordered_note,
    )
    check(
        "The graded-current route uses exactly that canonical ordered-chain grading",
        np.linalg.norm(n - np.diag([1.0, 2.0, 3.0]).astype(complex)) < 1e-12,
    )


def part2_basis_values_close_the_exact_graded_current_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 2: BASIS VALUES CLOSE THE EXACT GRADED-CURRENT FORMULA")
    print("=" * 88)

    e1 = exact_package().E1
    h0 = h_base()
    tm_mat = tm()
    td_mat = tdelta()
    tq_mat = tq()

    j_h0 = graded_current(h0)
    j_tm = graded_current(tm_mat)
    j_td = graded_current(td_mat)
    j_tq = graded_current(tq_mat)

    check(
        "On the affine base H_base the graded current is -1/2 + i E1/2",
        abs(j_h0 - complex(-0.5, 0.5 * e1)) < 1e-12,
        f"J_N(H_base)={j_h0:.12f}",
    )
    check(
        "The spectator generator T_m is graded-current blind",
        abs(j_tm) < 1e-12,
        f"J_N(T_m)={j_tm:.12f}",
    )
    check(
        "The delta generator contributes exactly -i/2",
        abs(j_td - complex(0.0, -0.5)) < 1e-12,
        f"J_N(T_delta)={j_td:.12f}",
    )
    check(
        "The q_+ generator contributes exactly -3 i / 2",
        abs(j_tq - complex(0.0, -1.5)) < 1e-12,
        f"J_N(T_q)={j_tq:.12f}",
    )

    samples = [
        (0.0, 0.2, 2.1),
        (0.5, 0.4, 1.0),
        (1.2, 0.9, 1.1),
        CHAMBER_ROOTS["Basin 1"],
    ]
    ok_formula = True
    max_err = 0.0
    for m, delta, q_plus in samples:
        h = active_affine_h(m, delta, q_plus)
        err = abs(graded_current(h) - expected_graded_current(m, delta, q_plus))
        ok_formula &= err < 1e-12
        max_err = max(max_err, float(err))

    check(
        "Affine linearity gives J_N(H) = -1/2 + i(E1/2 - delta/2 - 3 q_+/2)",
        ok_formula,
        f"max err={max_err:.2e}",
    )


def part3_the_pair_of_currents_recovers_the_full_affine_active_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE PAIR OF CURRENTS RECOVERS THE FULL AFFINE ACTIVE PAIR")
    print("=" * 88)

    same_q = [
        (0.5, 0.1, 1.0),
        (0.5, 1.2, 1.0),
    ]
    j_same = [nontrivial_character_current(active_affine_h(*p)) for p in same_q]
    jn_same = [graded_current(active_affine_h(*p)) for p in same_q]

    check(
        "Two affine points with the same q_+ have the same native current J_chi",
        abs(j_same[0] - j_same[1]) < 1e-12,
        f"J0={j_same[0]:.12f}, J1={j_same[1]:.12f}",
    )
    check(
        "The graded current separates those same-q_+ points by their different delta values",
        abs(jn_same[0] - jn_same[1]) > 1e-6,
        f"J_N0={jn_same[0]:.12f}, J_N1={jn_same[1]:.12f}",
    )

    samples = [
        (0.5, 0.1, 1.0),
        (0.5, 0.4, 1.0),
        (1.2, 0.9, 1.1),
        CHAMBER_ROOTS["Basin 1"],
        CHAMBER_ROOTS["Basin 2"],
        CHAMBER_ROOTS["Basin X"],
    ]
    ok_q = True
    ok_delta = True
    max_q_err = 0.0
    max_d_err = 0.0
    for m, delta, q_plus in samples:
        h = active_affine_h(m, delta, q_plus)
        q_err = abs(q_from_current(h) - q_plus)
        d_err = abs(delta_from_currents(h) - delta)
        ok_q &= q_err < 1e-12
        ok_delta &= d_err < 1e-12
        max_q_err = max(max_q_err, float(q_err))
        max_d_err = max(max_d_err, float(d_err))

    check(
        "The affine current theorem still recovers q_+ exactly as Re J_chi(H)",
        ok_q,
        f"max err={max_q_err:.2e}",
    )
    check(
        "The graded-current law recovers delta exactly as E1 - 2 Im J_N(H) - 3 Re J_chi(H)",
        ok_delta,
        f"max err={max_d_err:.2e}",
    )


def part4_the_current_pair_survives_exactly_on_the_retained_hw1_response_family() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT PAIR SURVIVES EXACTLY ON THE RETAINED HW=1 RESPONSE FAMILY")
    print("=" * 88)

    lam = 0.31
    samples = [
        CHAMBER_ROOTS["Basin 1"],
        (0.5, 0.4, 1.0),
        (1.2, 0.9, 1.1),
    ]

    ok_block = True
    ok_q = True
    ok_delta = True
    max_block = 0.0
    max_q_err = 0.0
    max_d_err = 0.0

    for idx, sample in enumerate(samples):
        h = active_affine_h(*sample)
        sector = sector_operator_fixture_from_effective_block(h, seed=4100 + idx)
        _ref, cols = active_response_columns_from_sector_operator(sector, lam)
        _ker, recovered = derive_active_block_from_response_columns(cols, lam)

        block_err = np.linalg.norm(recovered - h)
        q_err = abs(q_from_current(recovered) - sample[2])
        d_err = abs(delta_from_currents(recovered) - sample[1])

        ok_block &= block_err < 1e-12
        ok_q &= q_err < 1e-12
        ok_delta &= d_err < 1e-12
        max_block = max(max_block, float(block_err))
        max_q_err = max(max_q_err, float(q_err))
        max_d_err = max(max_d_err, float(d_err))

    check(
        "Active response-column reconstruction recovers the affine Hermitian block exactly",
        ok_block,
        f"max err={max_block:.2e}",
    )
    check(
        "On reconstructed hw=1 response blocks the native current still recovers q_+ exactly",
        ok_q,
        f"max err={max_q_err:.2e}",
    )
    check(
        "On reconstructed hw=1 response blocks the graded current still recovers delta exactly",
        ok_delta,
        f"max err={max_d_err:.2e}",
    )


def part5_strict_native_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 5: STRICT/NATIVE CLOSEOUT")
    print("=" * 88)

    reduction_note = read(
        "docs/DM_PMNS_NATIVE_CURRENT_LAST_MILE_REDUCTION_THEOREM_NOTE_2026-04-21.md"
    )
    affine_note = read(
        "docs/DM_PMNS_AFFINE_CURRENT_COORDINATE_REDUCTION_THEOREM_NOTE_2026-04-21.md"
    )

    check(
        "The prior reduction note records the remaining strict/native object as one additional real delta-law beyond current activation",
        "one additional real scalar law remains" in affine_note
        or "one additional real sole-axiom selector law" in affine_note,
    )
    check(
        "The same reduction note still records that q_+ was already closed by the native current",
        "J_chi(H) = q_+ - i/4" in reduction_note or "J_chi(H) = q_+ - i/4" in affine_note,
    )
    basin1 = CHAMBER_ROOTS["Basin 1"]
    h_phys = active_affine_h(*basin1)
    delta_phys = delta_from_currents(h_phys)

    check(
        "The ordered-chain graded current closes that remaining real affine coordinate on the physical chamber point",
        abs(delta_phys - basin1[1]) < 1e-12,
        f"delta_phys={delta_phys:.12f}",
    )
    check(
        "So the strict/native DM last mile now closes on the physical affine/source family",
        abs(delta_phys - basin1[1]) < 1e-12 and abs(q_from_current(h_phys) - basin1[2]) < 1e-12,
        "q_+ and delta both recovered natively",
    )


def part6_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CIRCULARITY GUARD")
    print("=" * 88)

    banned = {"u", "v", "w", "x", "y", "delta", "tau", "q", "d0_trip", "dm_trip"}
    ok_g, bad_g = circularity_guard(graded_current, banned)
    ok_d, bad_d = circularity_guard(delta_from_currents, banned)

    check(
        "The graded current takes no PMNS-side target values as inputs",
        ok_g,
        f"bad={bad_g}",
    )
    check(
        "The delta recovery law takes no PMNS-side target values as inputs",
        ok_d,
        f"bad={bad_d}",
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS ORDERED-CHAIN GRADED-CURRENT DELTA CLOSURE")
    print("=" * 88)
    print()
    print("Question:")
    print("  After native graph-first current activation closes q_+ on the physical")
    print("  affine Hermitian chart, is there an exact same-branch sole-axiom law")
    print("  for the remaining delta / Im(K_Z3[1,2]) direction on the retained")
    print("  hw=1 response family?")

    part1_the_ordered_chain_grading_is_already_canonical()
    part2_basis_values_close_the_exact_graded_current_formula()
    part3_the_pair_of_currents_recovers_the_full_affine_active_pair()
    part4_the_current_pair_survives_exactly_on_the_retained_hw1_response_family()
    part5_strict_native_closeout()
    part6_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact ordered-chain graded-current closure:")
    print("    - graph-first structure already fixes the canonical grading N = diag(1,2,3)")
    print("    - the graded current J_N(H) = J_chi(i[N,H]) reads the current-blind affine direction")
    print("    - together with J_chi(H) = q_+ - i/4, it recovers q_+ and delta exactly")
    print("    - the same two-current law survives exactly on the retained hw=1 response family")
    print()
    print("  So the stricter/native DM last mile is closed on the physical affine/source family.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
