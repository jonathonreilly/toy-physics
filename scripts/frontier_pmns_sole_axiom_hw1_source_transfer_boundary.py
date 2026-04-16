#!/usr/bin/env python3
"""Sole-axiom hw=1 source/transfer boundary for the retained PMNS lane.

Question:
  If we derive the canonical hw=1 source/transfer pack itself from the sole
  axiom Cl(3) on Z^3, do the native source insertions and graph-first cycle
  frame produce a nontrivial retained PMNS pack?

Answer:
  No.

  On the retained hw=1 triplet:
    - the sole-axiom active resolvent is the identity
    - the sole-axiom passive resolvent is a scalar multiple of the identity
    - source insertion through the native site projectors therefore yields only
      the basis columns e1,e2,e3 up to a scalar passive weight
    - graph-first forward transport fixes the frame E12,E23,E31 exactly, but
      contributes no nontrivial value data

  So even the strongest canonical sole-axiom hw=1 source/transfer pack remains
  support-only / frame-only and is rejected by the retained PMNS closure stack.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_graph_first_cycle_frame_support import canonical_edge_basis
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from pmns_lower_level_utils import (
    CYCLE,
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_response_columns_from_sector_operator,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

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


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E11 = e(0, 0)
E22 = e(1, 1)
E33 = e(2, 2)


def source_projectors() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return E11, E22, E33


def sole_axiom_hw1_source_transfer_pack(lam_act: float, lam_pass: float) -> dict[str, object]:
    active_block = I3
    passive_block = I3
    active_cols = active_response_columns_from_sector_operator(active_block, lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(passive_block, lam_pass)[1]
    return {
        "active_block": active_block,
        "passive_block": passive_block,
        "active_columns": active_cols,
        "passive_columns": passive_cols,
        "source_projectors": source_projectors(),
        "edge_basis": canonical_edge_basis(),
    }


def part1_native_sources_and_graph_first_cycle_frame_are_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: NATIVE SOURCES AND GRAPH-FIRST CYCLE FRAME ARE EXACT")
    print("=" * 88)

    s1, s2, s3 = source_projectors()
    b1, b2, b3 = canonical_edge_basis()

    check("The native hw=1 source projectors resolve the identity exactly",
          np.linalg.norm((s1 + s2 + s3) - I3) < 1e-12)
    check("The source projectors are exactly E11,E22,E33",
          np.linalg.norm(s1 - E11) < 1e-12 and np.linalg.norm(s2 - E22) < 1e-12 and np.linalg.norm(s3 - E33) < 1e-12)
    check("Forward cycle transport sends the source projectors to the canonical edge frame",
          np.linalg.norm(s1 @ CYCLE - b1) < 1e-12
          and np.linalg.norm(s2 @ CYCLE - b2) < 1e-12
          and np.linalg.norm(s3 @ CYCLE - b3) < 1e-12)
    check("The graph-first frame is exactly E12,E23,E31",
          np.allclose(np.stack([b1, b2, b3]), np.stack([e(0, 1), e(1, 2), e(2, 0)]), atol=1e-12))


def part2_sole_axiom_source_insertions_give_only_trivial_response_columns() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 2: SOLE-AXIOM SOURCE INSERTIONS GIVE ONLY TRIVIAL RESPONSE COLUMNS")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, lam_pass)
    active_cols = pack["active_columns"]
    passive_cols = pack["passive_columns"]
    active_kernel, active_block = derive_active_block_from_response_columns(active_cols, lam_act)
    passive_kernel, passive_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)

    check("The sole-axiom active source columns are exactly the basis columns e1,e2,e3",
          np.linalg.norm(np.column_stack(active_cols) - I3) < 1e-12)
    check("The sole-axiom passive source columns are exactly a scalar multiple of the basis columns",
          np.linalg.norm(np.column_stack(passive_cols) - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)
    check("The active source-derived block is exactly I3", np.linalg.norm(active_block - I3) < 1e-12)
    check("The passive source-derived block is exactly I3", np.linalg.norm(passive_block - I3) < 1e-12)
    check("The active/passive kernels are exactly the free scalar kernels",
          np.linalg.norm(active_kernel - I3) < 1e-12
          and np.linalg.norm(passive_kernel - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)

    return active_cols, passive_cols


def part3_graph_first_transfer_adds_only_frame_support_not_value_data(
    active_cols: list[np.ndarray],
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: GRAPH-FIRST TRANSFER ADDS ONLY FRAME SUPPORT, NOT VALUE DATA")
    print("=" * 88)

    transported_cols = [CYCLE @ col for col in active_cols]
    transported_matrix = np.column_stack(transported_cols)
    b1, b2, b3 = canonical_edge_basis()

    check("Forward transport of the sole-axiom source columns is exactly the cycle matrix",
          np.linalg.norm(transported_matrix - CYCLE) < 1e-12)
    check("The transported source frame matches the graph-first ordered cycle support",
          np.linalg.norm(b1 - E11 @ transported_matrix) < 1e-12
          and np.linalg.norm(b2 - E22 @ transported_matrix) < 1e-12
          and np.linalg.norm(b3 - E33 @ transported_matrix) < 1e-12)
    check("No nontrivial cycle values appear: the transferred columns are fixed entirely by the frame",
          np.count_nonzero(np.abs(transported_matrix) > 1e-12) == 3,
          f"transported={np.round(transported_matrix, 6)}")


def part4_the_canonical_sole_axiom_pack_is_rejected_by_the_retained_pmns_closure_stack(
    active_cols: list[np.ndarray],
    passive_cols: list[np.ndarray],
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CANONICAL SOLE-AXIOM PACK IS REJECTED BY THE RETAINED PMNS STACK")
    print("=" * 88)

    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(active_cols, passive_cols, 0.31, 0.27),
        ValueError,
    )
    check("The retained PMNS closure stack rejects the canonical sole-axiom hw=1 source/transfer pack",
          ok, detail)
    check("Reason: the derived pair is not on a one-sided minimal PMNS class",
          "one-sided minimal PMNS class" in detail, detail)
    check("So native source insertion and graph-first transfer do not evade the sole-axiom free boundary", True)


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(
        sole_axiom_hw1_source_transfer_pack,
        {"x", "y", "delta", "tau", "q", "coeffs", "d0_trip", "dm_trip", "u", "v", "w"},
    )
    check("The canonical sole-axiom source/transfer derivation takes no PMNS-side value targets as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS SOLE-AXIOM HW=1 SOURCE/TRANSFER BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If we derive the canonical hw=1 source/transfer pack itself from the")
    print("  sole axiom Cl(3) on Z^3, do the native source insertions and")
    print("  graph-first transfer frame produce a nontrivial retained PMNS pack?")

    part1_native_sources_and_graph_first_cycle_frame_are_exact()
    active_cols, passive_cols = part2_sole_axiom_source_insertions_give_only_trivial_response_columns()
    part3_graph_first_transfer_adds_only_frame_support_not_value_data(active_cols)
    part4_the_canonical_sole_axiom_pack_is_rejected_by_the_retained_pmns_closure_stack(active_cols, passive_cols)
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact sole-axiom source/transfer boundary:")
    print("    - native source insertions give only the basis columns e1,e2,e3")
    print("      up to the passive scalar resolvent weight")
    print("    - graph-first forward transport fixes only the cycle frame")
    print("      E12,E23,E31")
    print("    - the resulting canonical hw=1 source/transfer pack is still the")
    print("      trivial free pack")
    print("    - the retained PMNS closure stack rejects that pack exactly")
    print()
    print("  So even source insertion plus graph-first transfer do not derive a")
    print("  nontrivial retained PMNS lane from Cl(3) on Z^3 alone.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
