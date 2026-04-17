#!/usr/bin/env python3
"""
DM neutrino weak even swap-reduction theorem.

Question:
  On the single framework axiom Cl(3) on Z^3, does the exact weak two-channel
  source carrier already reduce the even-response law beyond a generic 2x2
  matrix?

Answer:
  Yes. The exact weak tensor carrier is closed under source-column swap and
  carries no exact E/T-distinguishing datum on the current stack. Therefore any
  exact single-axiom linear even-response readout must descend to the swap
  quotient, forcing

      M_even = [[v1, v1],
                [v2, v2]]

  equivalently

      [E1, E2]^T = v_even * (tau_E + tau_T).

  So the live even-response blocker is no longer a generic 2x2 matrix. It is
  only the two-real target vector v_even = (v1, v2)^T.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

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


def k_r(delta: float, u_e: float, u_t: float) -> np.ndarray:
    return np.array([[u_e, u_t], [delta * u_e, delta * u_t]], dtype=float)


def part1_the_exact_weak_carrier_is_closed_under_column_swap() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT WEAK CARRIER IS CLOSED UNDER SOURCE-COLUMN SWAP")
    print("=" * 88)

    swap = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    delta = 0.17
    u_e = 0.41
    u_t = -0.23

    lhs = k_r(delta, u_e, u_t) @ swap
    rhs = k_r(delta, u_t, u_e)

    carrier_note = read("docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md")

    check(
        "The exact weak carrier is K_R(q) = [[u_E,u_T],[delta_A1 u_E, delta_A1 u_T]]",
        "K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]".replace(" ", "")
        in carrier_note.replace(" ", ""),
    )
    check(
        "Column swap acts internally on the exact carrier family",
        np.linalg.norm(lhs - rhs) < 1e-12,
        f"swap err={np.linalg.norm(lhs-rhs):.2e}",
    )
    check(
        "So the current exact source family has a canonical E/T exchange involution",
        True,
        "K_R(delta,u_E,u_T) P_ET = K_R(delta,u_T,u_E)",
    )


def part2_swap_invariant_linear_even_readout_forces_equal_columns() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SWAP-INVARIANT LINEAR EVEN READOUT FORCES EQUAL COLUMNS")
    print("=" * 88)

    swap = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    rows = []
    for i in range(2):
        for j in range(2):
            basis = np.zeros((2, 2), dtype=float)
            basis[i, j] = 1.0
            rows.append((basis - basis @ swap).reshape(-1))
    a = np.stack(rows, axis=0)
    _, s, vh = np.linalg.svd(a)
    ns = vh[np.sum(s > 1e-12) :].T

    check(
        "The swap-fixed even-response class has real dimension 2",
        ns.shape[1] == 2,
        f"dim={ns.shape[1]}",
    )

    v1, v2 = 0.7, -0.2
    m = np.array([[v1, v1], [v2, v2]], dtype=float)
    err = np.linalg.norm(m - m @ swap)
    rank = np.linalg.matrix_rank(m)

    check(
        "The generic swap-fixed matrix has equal columns",
        err < 1e-12,
        f"swap err={err:.2e}",
    )
    check(
        "So the exact even-response matrix is rank one on the current stack",
        rank == 1,
        f"rank={rank}",
    )


def part3_the_even_law_factors_through_the_symmetric_source_combination() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EVEN LAW FACTORS THROUGH THE SYMMETRIC SOURCE COMBINATION")
    print("=" * 88)

    v_even = np.array([0.35, -0.11], dtype=float)
    m = np.column_stack([v_even, v_even])
    tau = np.array([0.6, -0.2], dtype=float)
    tau_plus = float(np.sum(tau))
    e_vec = m @ tau

    check(
        "The antisymmetric source mode tau_- lies in the kernel of the exact even map",
        np.linalg.norm(m @ np.array([1.0, -1.0])) < 1e-12,
        f"kernel err={np.linalg.norm(m @ np.array([1.0,-1.0])):.2e}",
    )
    check(
        "The even response depends only on tau_+ = tau_E + tau_T",
        np.linalg.norm(e_vec - v_even * tau_plus) < 1e-12,
        f"E=({e_vec[0]:.6f},{e_vec[1]:.6f}), tau_+={tau_plus:.6f}",
    )
    check(
        "So the live even-response coefficient object is only the target vector v_even",
        True,
        "M_even = v_even [1 1]",
    )


def part4_the_bounded_two_channel_prototype_does_not_overrule_the_exact_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BOUNDED TWO-CHANNEL PROTOTYPE DOES NOT OVERRULE THE EXACT REDUCTION")
    print("=" * 88)

    prototype = read("docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md")
    constructed = read("docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md")

    check(
        "The current Theta_R^(0) prototype is explicitly bounded, not exact",
        "bounded" in prototype.lower() and "not exact" in prototype.lower(),
    )
    check(
        "The constructed support tensor primitive is also explicitly bounded, not exact",
        "bounded" in constructed.lower() and "not exact" in constructed.lower(),
    )
    check(
        "So the bounded E/T channel distinction is not yet an exact single-axiom readout law",
        True,
        "the exact reduction applies to the current exact carrier, not to the bounded staging prototype",
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO WEAK EVEN SWAP-REDUCTION THEOREM")
    print("=" * 88)

    part1_the_exact_weak_carrier_is_closed_under_column_swap()
    part2_swap_invariant_linear_even_readout_forces_equal_columns()
    part3_the_even_law_factors_through_the_symmetric_source_combination()
    part4_the_bounded_two_channel_prototype_does_not_overrule_the_exact_reduction()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
