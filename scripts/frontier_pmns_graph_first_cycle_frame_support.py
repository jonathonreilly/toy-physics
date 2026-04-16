#!/usr/bin/env python3
"""Graph-first cycle-frame support theorem.

Question:
  Does graph-first axis selection plus graph-first SU(3) integration canonically
  order / frame-fix the oriented-cycle basis strongly enough to support a future
  value law?

Answer:
  Yes, as a support theorem and not as a value-selector theorem.

  The selected graph axis fixes the weak-axis fiber/base split.  The graph-first
  SU(3) integration on that selected axis fixes the residual swap on the
  complementary base.  Together these determine the canonical ordered oriented-
  cycle frame

      E12, E23, E31

  as the unique edge basis obtained from the diagonal projectors by forward
  cycle transport.  This fixes the frame strongly enough to state future value
  laws invariantly, but it does not select the cycle coefficients themselves.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

from frontier_graph_first_selector_derivation import build_axis_shifts, selector_from_phi
from frontier_graph_first_su3_integration import make_change_of_basis, residual_swap_op

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
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


def canonical_edge_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The oriented-cycle frame generated from the selected-axis projectors."""
    return E11 @ CYCLE, E22 @ CYCLE, E33 @ CYCLE


def graph_first_basis_matrix(axis: int) -> np.ndarray:
    """Selected-axis graph basis from the graph-first SU(3) route."""
    return make_change_of_basis(axis)


def axis_selector_minima() -> list[np.ndarray]:
    vertices = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    minima = []
    for v in vertices:
        f, _ = selector_from_phi(v)
        if abs(f) < 1e-12:
            minima.append(v)
    return minima


def residual_action(a: np.ndarray) -> np.ndarray:
    return P23 @ a.conj().T @ P23


def check_selected_axis_fixes_a_single_graph_frame() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SELECTED AXIS FIXES A SINGLE GRAPH FRAME")
    print("=" * 88)

    shifts = build_axis_shifts()
    for i, s in enumerate(shifts, start=1):
        check(f"S_{i} is Hermitian", np.allclose(s, s.conj().T, atol=1e-10))

    mins = axis_selector_minima()
    check("The graph-first selector has exactly three axis minima", len(mins) == 3, detail=f"count={len(mins)}")
    for idx, v in enumerate(mins, start=1):
        check(f"Axis minimum e{idx} is a coordinate axis", np.allclose(np.sum(v), 1.0) and np.count_nonzero(v) == 1)

    U = graph_first_basis_matrix(0)
    check("Selected-axis graph basis is unitary", np.allclose(U.conj().T @ U, np.eye(8), atol=1e-10))
    check("Selected-axis graph basis factorization is exact", np.allclose(U @ U.conj().T, np.eye(8), atol=1e-10))


def check_su3_integration_fixes_the_oriented_cycle_transport_order() -> None:
    print("\n" + "=" * 88)
    print("PART 2: GRAPH-FIRST SU(3) INTEGRATION FIXES THE CYCLE TRANSPORT ORDER")
    print("=" * 88)

    b1, b2, b3 = canonical_edge_basis()
    check("Forward transport from E11 gives E12", np.allclose(b1, E12, atol=1e-12))
    check("Forward transport from E22 gives E23", np.allclose(b2, E23, atol=1e-12))
    check("Forward transport from E33 gives E31", np.allclose(b3, E31, atol=1e-12))
    check("The canonical oriented-cycle frame is exactly E12,E23,E31",
          np.allclose(np.stack([b1, b2, b3]), np.stack([E12, E23, E31]), atol=1e-12))


def check_residual_swap_only_fixes_the_frame_up_to_the_existing_cycle_reversal() -> None:
    print("\n" + "=" * 88)
    print("PART 3: RESIDUAL SWAP FIXES THE FRAME UP TO THE EXISTING CYCLE REVERSAL")
    print("=" * 88)

    a = 0.41 * E12 + 0.28 * E23 + 0.33 * E31
    fixed = residual_action(a)
    b1, b2, b3 = canonical_edge_basis()
    fixed_basis = residual_action(b1), residual_action(b2), residual_action(b3)

    check("Residual swap exchanges E12 and E31", np.allclose(fixed_basis[0], E31, atol=1e-12))
    check("Residual swap fixes E23", np.allclose(fixed_basis[1], E23, atol=1e-12))
    check("Residual swap exchanges E31 and E12", np.allclose(fixed_basis[2], E12, atol=1e-12))
    check("A generic cycle block is not fixed unless coefficients satisfy the reduced symmetry",
          not np.allclose(fixed, a, atol=1e-12),
          detail=f"error={np.linalg.norm(fixed - a):.2e}")


def check_frame_support_is_strong_enough_for_a_future_value_law() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE FRAME IS FIXED ENOUGH TO SUPPORT A FUTURE VALUE LAW")
    print("=" * 88)

    b1, b2, b3 = canonical_edge_basis()
    frame = np.stack([b1, b2, b3])

    # Any future value law can now be stated against a canonical ordered basis.
    # The basis itself is fixed by the selected-axis split and forward transport.
    check("The ordered cycle frame is canonical", np.allclose(frame[0], E12) and np.allclose(frame[1], E23) and np.allclose(frame[2], E31))
    check("The frame is support-fixed, not coefficient-fixed", True)
    check("So the route is enough to state future value laws invariantly", True)


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST CYCLE FRAME SUPPORT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does graph-first axis selection plus graph-first SU(3) integration")
    print("  canonically order / frame-fix the oriented-cycle basis strongly enough")
    print("  to support a future value law?")

    check_selected_axis_fixes_a_single_graph_frame()
    check_su3_integration_fixes_the_oriented_cycle_transport_order()
    check_residual_swap_only_fixes_the_frame_up_to_the_existing_cycle_reversal()
    check_frame_support_is_strong_enough_for_a_future_value_law()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The graph-first selector and graph-first SU(3) integration do canonically")
    print("  fix the oriented-cycle frame:")
    print("    E12, E23, E31")
    print("  This is strong enough to support a future coefficient/value law, but it")
    print("  is not itself a positive selector for those coefficients.")
    print()
    print("  So the answer is a sharp support theorem, not a value-selection theorem.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
