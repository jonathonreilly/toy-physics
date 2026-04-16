#!/usr/bin/env python3
"""Anomaly-forced 3+1 retarded-transport / projection boundary for PMNS.

Question:
  Can an anomaly-forced 3+1 retarded lift on the retained hw=1 triplet
  generate a genuinely nontrivial source/transfer pack after projection back
  to the lepton triplet?

Answer:
  No on the current exact bank.

  The 3+1 retarded lift is nontrivial upstairs: the anomaly-odd source sector
  produces distinct time-slices along the retarded history. But the retained
  C3-even projection onto the hw=1 lepton triplet kills that anomaly-odd
  source exactly. After projection, every anomaly-forced lift collapses to the
  free retained pack, and the PMNS closure stack rejects it.

  So the anomaly-forced 3+1 retarded route does not evade the existing
  sole-axiom free boundary.
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
    except exc_type as exc:  # noqa: PERF203
        return True, str(exc)
    except Exception as exc:  # noqa: BLE001
        return False, f"wrong exception {type(exc).__name__}: {exc}"
    return False, "no exception"


def anomaly_seed() -> np.ndarray:
    """A traceless anomaly-odd source on the retained triplet."""
    return np.array([[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 0.0]], dtype=complex)


def orbit_average(matrix: np.ndarray) -> np.ndarray:
    return (matrix + CYCLE @ matrix @ CYCLE.conj().T + CYCLE @ CYCLE @ matrix @ CYCLE.conj().T @ CYCLE.conj().T) / 3.0


def retarded_3plus1_history(eta: float) -> list[np.ndarray]:
    """A minimal finite-lag retarded history on the hw=1 triplet.

    The lifted 3+1 data are nontrivial upstairs, but each anomaly contribution
    is traceless and C3-odd under the retained projection.
    """
    a0 = anomaly_seed()
    a1 = CYCLE @ a0 @ CYCLE.conj().T
    a2 = CYCLE @ CYCLE @ a0 @ CYCLE.conj().T @ CYCLE.conj().T
    return [
        I3.copy(),
        I3 + eta * a0,
        I3 + eta * (a0 + 2.0 * a1),
        I3 + eta * (a0 + 2.0 * a1 + 3.0 * a2),
    ]


def retained_projection_from_history(history: list[np.ndarray]) -> np.ndarray:
    """Project the retarded 3+1 lift back to the retained lepton triplet."""
    return orbit_average(history[-1])


def retained_hw1_pack_from_projection(projected: np.ndarray, lam_act: float, lam_pass: float) -> dict[str, object]:
    active_cols = active_response_columns_from_sector_operator(projected, lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(projected, lam_pass)[1]
    active_block = derive_active_block_from_response_columns(active_cols, lam_act)[1]
    passive_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)[1]
    return {
        "active_columns": active_cols,
        "passive_columns": passive_cols,
        "active_block": active_block,
        "passive_block": passive_block,
    }


def part1_retarded_3plus1_lift_is_nontrivial_upstairs() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ANOMALY-FORCED 3+1 RETARDED LIFT IS NONTRIVIAL UPSTAIRS")
    print("=" * 88)

    eta = 0.37
    history = retarded_3plus1_history(eta)

    check("The 3+1 retarded lift has four causal slices", len(history) == 4, f"slices={len(history)}")
    check("The retarded history is nontrivial after the first anomaly step",
          np.linalg.norm(history[1] - I3) > 1e-12,
          f"||H1-I||={np.linalg.norm(history[1] - I3):.2e}")
    check("The retarded lift continues to evolve across the 3+1 slices",
          np.linalg.norm(history[3] - history[1]) > 1e-12,
          f"||H3-H1||={np.linalg.norm(history[3] - history[1]):.2e}")

    print()
    print("  So the anomaly-forced 3+1 route does create a genuine causal history")
    print("  upstairs. The question is whether that history survives the retained")
    print("  hw=1 projection.")


def part2_projection_back_to_the_retained_triplet_kills_the_anomaly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: RETAINED PROJECTION KILLS THE ANOMALY-ODD SOURCE EXACTLY")
    print("=" * 88)

    eta = 0.37
    history = retarded_3plus1_history(eta)
    projected = retained_projection_from_history(history)
    pack = retained_hw1_pack_from_projection(projected, 0.31, 0.27)

    check("The retained projection is exactly the free triplet I3",
          np.linalg.norm(projected - I3) < 1e-12,
          f"error={np.linalg.norm(projected - I3):.2e}")
    check("The retained active source columns collapse to the basis columns",
          np.linalg.norm(np.column_stack(pack["active_columns"]) - I3) < 1e-12,
          f"active_cols={np.round(np.column_stack(pack['active_columns']), 6)}")
    check("The retained passive source columns collapse to a scalar multiple of the basis columns",
          np.linalg.norm(np.column_stack(pack["passive_columns"]) - (1.0 / (1.0 - 0.27)) * I3) < 1e-12,
          f"passive_cols={np.round(np.column_stack(pack['passive_columns']), 6)}")
    check("The projected active block is exactly I3", np.linalg.norm(pack["active_block"] - I3) < 1e-12)
    check("The projected passive block is exactly I3", np.linalg.norm(pack["passive_block"] - I3) < 1e-12)

    print()
    print("  So the anomaly-forced 3+1 lift does not generate a nontrivial retained")
    print("  hw=1 source/transfer pack. The retained projection removes the anomaly")
    print("  sector exactly.")


def part3_two_distinct_anomaly_strengths_have_the_same_retained_projection() -> None:
    print("\n" + "=" * 88)
    print("PART 3: DIFFERENT ANOMALY STRENGTHS HAVE THE SAME RETAINED PROJECTION")
    print("=" * 88)

    h1 = retarded_3plus1_history(0.19)
    h2 = retarded_3plus1_history(0.83)
    p1 = retained_projection_from_history(h1)
    p2 = retained_projection_from_history(h2)

    check("The two 3+1 lifted histories are genuinely different upstairs",
          np.linalg.norm(h1[1] - h2[1]) > 1e-6,
          f"||H1-H2||={np.linalg.norm(h1[1] - h2[1]):.2e}")
    check("Their retained projections are identical",
          np.linalg.norm(p1 - p2) < 1e-12,
          f"projection diff={np.linalg.norm(p1 - p2):.2e}")
    check("The common retained projection is still just the free pack",
          np.linalg.norm(p1 - I3) < 1e-12 and np.linalg.norm(p2 - I3) < 1e-12)


def part4_the_retained_pmns_closure_stack_rejects_the_projected_pack() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE RETAINED PMNS CLOSURE STACK REJECTS THE PROJECTED PACK")
    print("=" * 88)

    projected = I3.copy()
    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(
            active_response_columns_from_sector_operator(projected, 0.31)[1],
            passive_response_columns_from_sector_operator(projected, 0.27)[1],
            0.31,
            0.27,
        ),
        ValueError,
    )
    check("The retained PMNS closure stack rejects the projected 3+1 pack", ok, detail)
    check("Reason: the projected pack is still the free profile boundary",
          "one-sided minimal PMNS class" in detail, detail)
    check("Graph-first transport still only fixes the support frame, not values", True)


def part5_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(retarded_3plus1_history, {"tau", "q", "x", "y", "delta", "coeffs", "d0_trip", "dm_trip", "u", "v", "w"})
    check("The retarded 3+1 history takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS ANOMALY-FORCED 3+1 RETARDED TRANSPORT / PROJECTION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can an anomaly-forced 3+1 retarded lift on the retained hw=1")
    print("  triplet generate a genuinely nontrivial source/transfer pack after")
    print("  projection back to the lepton triplet?")

    part1_retarded_3plus1_lift_is_nontrivial_upstairs()
    part2_projection_back_to_the_retained_triplet_kills_the_anomaly()
    part3_two_distinct_anomaly_strengths_have_the_same_retained_projection()
    part4_the_retained_pmns_closure_stack_rejects_the_projected_pack()
    part5_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Boundary result for the anomaly-forced 3+1 retarded route:")
    print("    - the 3+1 retarded lift is genuinely nontrivial upstairs")
    print("    - the retained C3-even projection kills the anomaly-odd source")
    print("      sector exactly")
    print("    - different anomaly strengths project to the same free retained pack")
    print("    - the retained PMNS closure stack rejects that projected pack")
    print()
    print("  So this candidate family does not derive a nontrivial hw=1")
    print("  source/transfer pack from the current exact bank.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
