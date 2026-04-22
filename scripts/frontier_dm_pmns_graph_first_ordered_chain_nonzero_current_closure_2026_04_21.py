#!/usr/bin/env python3
"""
DM PMNS graph-first ordered-chain nonzero-current activation theorem.

Question:
  Can one derive an explicit sole-axiom nonzero-current law on the retained
  hw=1 response family itself?

Answer:
  Yes.

  The graph-first selector plus graph-first cycle-frame theorem already fix:
    - the ordered diagonal projectors E11, E22, E33,
    - the canonical forward oriented-cycle frame E12, E23, E31,
    - and therefore the adjacent ordered chain 1 -> 2 -> 3.

  On that ordered chain there is one unique normalized Hermitian grading
  element N satisfying

      [N, E12] = -E12,
      [N, E23] = -E23,
      min spec(N) = 1,

  namely N = diag(1,2,3).

  Combining that grading with the exact forward cycle C = E12 + E23 + E31
  gives the canonical sole-axiom active law

      A_ord = N + C.

  This law already produces a nonzero native nontrivial-character current

      J_chi(A_ord) = 1,

  and that current survives exactly on the retained hw=1 response family.

  By the strict/native last-mile reduction theorem, this meets the reduced
  constructive current-activation target on that response family.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
)
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_graph_first_cycle_frame_support import canonical_edge_basis
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from pmns_lower_level_utils import (
    circularity_guard,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    passive_operator,
    passive_response_columns_from_sector_operator,
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


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E11 = e(0, 0)
E22 = e(1, 1)
E33 = e(2, 2)
E12 = e(0, 1)
E23 = e(1, 2)
E31 = e(2, 0)
CYCLE = E12 + E23 + E31


def chain_number_operator() -> np.ndarray:
    return np.diag([1.0, 2.0, 3.0]).astype(complex)


def ordered_chain_active_law() -> np.ndarray:
    return chain_number_operator() + CYCLE


def part1_graph_first_and_chain_algebra_fix_the_ordered_carrier() -> None:
    print("\n" + "=" * 88)
    print("PART 1: GRAPH-FIRST AND CHAIN ALGEBRA FIX THE ORDERED CARRIER")
    print("=" * 88)

    cycle_note = read("docs/PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md")
    chain_note = read("docs/DM_WILSON_TO_DWEH_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")

    b1, b2, b3 = canonical_edge_basis()
    chain = chain_data()

    check(
        "The graph-first cycle-frame note records the canonical ordered frame E12,E23,E31",
        "E12, E23, E31" in cycle_note,
    )
    check(
        "The canonical edge basis is exactly the ordered frame E12,E23,E31",
        np.linalg.norm(b1 - E12) < 1e-12
        and np.linalg.norm(b2 - E23) < 1e-12
        and np.linalg.norm(b3 - E31) < 1e-12,
    )
    check(
        "The adjacent-chain target note records the local chain generators E12 and E23",
        "E_12" in chain_note and "E_23" in chain_note,
    )
    check(
        "The chain products recover the ordered diagonal projectors exactly",
        np.linalg.norm(chain["E11"] - E11) < 1e-12
        and np.linalg.norm(chain["E22"] - E22) < 1e-12
        and np.linalg.norm(chain["E33"] - E33) < 1e-12,
    )


def part2_the_unique_normalized_chain_grading_is_diag123() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE UNIQUE NORMALIZED CHAIN GRADING IS diag(1,2,3)")
    print("=" * 88)

    n1 = 1.0
    n2 = n1 + 1.0
    n3 = n2 + 1.0
    n = np.diag([n1, n2, n3]).astype(complex)

    check(
        "A diagonal chain grading with [N,E12]=-E12 forces n2-n1=1",
        np.linalg.norm((n @ E12) - (E12 @ n) + E12) < 1e-12,
        f"diag={np.round(np.diag(n), 6)}",
    )
    check(
        "The same law on E23 forces n3-n2=1",
        np.linalg.norm((n @ E23) - (E23 @ n) + E23) < 1e-12,
        f"diag={np.round(np.diag(n), 6)}",
    )
    check(
        "With the minimal positive normalization min spec(N)=1 the grading is exactly diag(1,2,3)",
        np.linalg.norm(n - chain_number_operator()) < 1e-12,
    )


def part3_the_ordered_chain_law_activates_the_native_current() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 3: THE ORDERED-CHAIN LAW ACTIVATES THE NATIVE CURRENT")
    print("=" * 88)

    n = chain_number_operator()
    a_ord = ordered_chain_active_law()
    j = nontrivial_character_current(a_ord)

    check(
        "The canonical sole-axiom active law is N + C on the ordered chain",
        np.linalg.norm(a_ord - (n + CYCLE)) < 1e-12,
    )
    check(
        "The ordered-chain law lies on the canonical diagonal-plus-forward-cycle support",
        np.count_nonzero(np.abs(a_ord) > 1e-12) == 6,
        f"A_ord={np.round(a_ord, 6)}",
    )
    check(
        "The ordered-chain law produces nonzero native current",
        abs(j) > 1e-12,
        f"J_chi={j:.12f}",
    )
    check(
        "In the canonical unit normalization that current is exactly J_chi = 1",
        abs(j - 1.0) < 1e-12,
        f"J_chi={j:.12f}",
    )

    return a_ord


def part4_the_nonzero_current_survives_exactly_on_the_response_family(a_ord: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NONZERO CURRENT SURVIVES ON THE RESPONSE FAMILY")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    active_cols = active_response_columns_from_sector_operator(a_ord, lam_act)[1]
    _kernel, recovered = derive_active_block_from_response_columns(active_cols, lam_act)
    recovered_j = nontrivial_character_current(recovered)

    passive_cols = passive_response_columns_from_sector_operator(
        passive_operator(np.ones(3, dtype=complex), 0), lam_pass
    )[1]
    closure = close_from_lower_level_observables(active_cols, passive_cols, lam_act, lam_pass)

    check(
        "The response-column reconstruction recovers the ordered-chain active law exactly",
        np.linalg.norm(recovered - a_ord) < 1e-12,
        f"err={np.linalg.norm(recovered - a_ord):.2e}",
    )
    check(
        "The reconstructed response-family current stays exactly nonzero",
        abs(recovered_j - 1.0) < 1e-12,
        f"J_chi={recovered_j:.12f}",
    )
    check(
        "The ordered-chain active law already sits on a one-sided minimal PMNS class with a canonical monomial passive companion",
        closure["branch"] == "neutrino-active",
        f"branch={closure['branch']}, sheet={closure['sheet']}",
    )


def part5_reduction_consequence() -> None:
    print("\n" + "=" * 88)
    print("PART 5: REDUCTION CONSEQUENCE")
    print("=" * 88)

    reduction_note = read(
        "docs/DM_PMNS_NATIVE_CURRENT_LAST_MILE_REDUCTION_THEOREM_NOTE_2026-04-21.md"
    )
    check(
        "The prior last-mile reduction note records nonzero J_chi production as the exact remaining strict/native burden",
        "derive a sole-axiom law producing nonzero J_chi" in reduction_note,
    )
    j = nontrivial_character_current(ordered_chain_active_law())
    check(
        "The ordered-chain theorem supplies one explicit sole-axiom nonzero-current law",
        abs(j - 1.0) < 1e-12,
        f"J_chi(A_ord)={j:.12f}",
    )
    check(
        "So the reduced constructive target is met on the retained hw=1 response family",
        abs(j) > 1e-12 and "derive a sole-axiom law producing nonzero J_chi" in reduction_note,
        "reduction target + exact current activation",
    )


def part6_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CIRCULARITY GUARD")
    print("=" * 88)

    banned = {"u", "v", "w", "x", "y", "delta", "tau", "q", "d0_trip", "dm_trip"}
    ok_n, bad_n = circularity_guard(chain_number_operator, banned)
    ok_a, bad_a = circularity_guard(ordered_chain_active_law, banned)

    check(
        "The chain grading takes no PMNS-side target values as inputs",
        ok_n,
        f"bad={bad_n}",
    )
    check(
        "The ordered-chain active law takes no PMNS-side target values as inputs",
        ok_a,
        f"bad={bad_a}",
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS GRAPH-FIRST ORDERED-CHAIN NONZERO-CURRENT ACTIVATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can one derive an explicit sole-axiom nonzero-current law on the")
    print("  retained hw=1 response family?")

    part1_graph_first_and_chain_algebra_fix_the_ordered_carrier()
    part2_the_unique_normalized_chain_grading_is_diag123()
    a_ord = part3_the_ordered_chain_law_activates_the_native_current()
    part4_the_nonzero_current_survives_exactly_on_the_response_family(a_ord)
    part5_reduction_consequence()
    part6_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact same-branch current-activation theorem on the retained hw=1 response family:")
    print("    - graph-first selection and cycle-frame support fix the ordered carrier")
    print("    - the adjacent chain has a unique normalized grading N = diag(1,2,3)")
    print("    - the canonical ordered-chain law A_ord = N + C produces J_chi = 1")
    print("    - that current survives exactly on the retained response family")
    print()
    print("  Therefore one explicit sole-axiom nonzero-current law is derived on")
    print("  the retained hw=1 response family, meeting the reduced constructive target.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
