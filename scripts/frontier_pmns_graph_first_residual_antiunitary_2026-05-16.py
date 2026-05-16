#!/usr/bin/env python3
"""Narrow bridge theorem: graph-first residual antiunitary on the oriented cycle channel.

Closes one of the two missing_bridge_theorem clauses named by the
audit verdict on pmns_oriented_cycle_selection_structure_note, namely:

  "the graph-first residual antiunitary condition ... within the
  restricted dependency chain."

Setting:
  - P_23 = [[1,0,0],[0,0,1],[0,1,0]] is the residual Z_2 swap of axes
    2 and 3 (the graph-first axis-stabilizer for the selected axis).
  - The oriented forward-cycle channel is
        A_fwd(c_1, c_2, c_3) = c_1 E_12 + c_2 E_23 + c_3 E_31.
  - The graph-first residual antiunitary map is
        R[A] = P_23 @ A^dagger @ P_23.

Theorem (class A finite-dimensional algebra):

  (1) R carries the cycle channel into itself with coordinate action
      (c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1)).
  (2) R is conjugate-linear (antiunitary on the channel).
  (3) R is an involution: R o R = id.
  (4) The fixed locus is exactly c_1 = conj(c_3), c_2 real
      (a 3-real-parameter subfamily).
  (5) A generic triple is not fixed.

This runner exercises only finite-dimensional algebra; it does not
derive the carrier or the axis-stabilizer-equals-P_23 step.  Those are
imported from cited one-hop authorities (PMNS_GRAPH_FIRST_AXIS_-
ALIGNMENT_NOTE.md and Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md).
"""

from __future__ import annotations

import sys

import numpy as np

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


P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)


def E(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E12 = E(0, 1)
E23 = E(1, 2)
E31 = E(2, 0)
E21 = E(1, 0)
E32 = E(2, 1)
E13 = E(0, 2)


def cycle_block(c1: complex, c2: complex, c3: complex) -> np.ndarray:
    return c1 * E12 + c2 * E23 + c3 * E31


def R(a: np.ndarray) -> np.ndarray:
    return P23 @ a.conj().T @ P23


SAMPLE_TRIPLES = [
    (1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j),
    (0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j),
    (0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j),
    (0.7 - 0.3j, 0.4 + 0.0j, 0.7 + 0.3j),
    (1.0 + 0.2j, -0.3 + 0.7j, 0.5 - 0.4j),
    (0.41 + 0.32j, 0.28 + 0.07j, 0.33 - 0.11j),
]


def part1_matrix_unit_conjugation_under_P23() -> None:
    print("\n" + "=" * 88)
    print("PART 1: matrix-unit conjugation under P_23")
    print("=" * 88)
    check(
        "P_23 @ E_21 @ P_23 == E_31",
        np.linalg.norm(P23 @ E21 @ P23 - E31) < 1e-12,
    )
    check(
        "P_23 @ E_32 @ P_23 == E_23",
        np.linalg.norm(P23 @ E32 @ P23 - E23) < 1e-12,
    )
    check(
        "P_23 @ E_13 @ P_23 == E_12",
        np.linalg.norm(P23 @ E13 @ P23 - E12) < 1e-12,
    )
    check("P_23 is self-adjoint (P_23 == P_23^dagger)", np.linalg.norm(P23 - P23.conj().T) < 1e-12)
    check("P_23 is an involution (P_23 @ P_23 == I_3)", np.linalg.norm(P23 @ P23 - np.eye(3, dtype=complex)) < 1e-12)


def part2_coordinate_action_on_the_cycle_channel() -> None:
    print("\n" + "=" * 88)
    print("PART 2: coordinate action  (c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1))")
    print("=" * 88)
    for c1, c2, c3 in SAMPLE_TRIPLES:
        a = cycle_block(c1, c2, c3)
        b = R(a)
        expected = cycle_block(np.conj(c3), np.conj(c2), np.conj(c1))
        check(
            f"R[A_fwd({c1},{c2},{c3})] = A_fwd(conj(c_3), conj(c_2), conj(c_1))",
            np.linalg.norm(b - expected) < 1e-12,
        )


def part3_channel_preservation() -> None:
    print("\n" + "=" * 88)
    print("PART 3: R preserves the oriented forward-cycle channel")
    print("=" * 88)
    cycle_support = (np.abs(E12) + np.abs(E23) + np.abs(E31)) > 0
    for c1, c2, c3 in SAMPLE_TRIPLES:
        a = cycle_block(c1, c2, c3)
        b = R(a)
        out_of_channel = np.linalg.norm(b[~cycle_support])
        check(
            f"R[A_fwd({c1},{c2},{c3})] has support inside cycle channel",
            out_of_channel < 1e-12,
            f"||off-channel|| = {out_of_channel:.2e}",
        )


def part4_antiunitarity() -> None:
    print("\n" + "=" * 88)
    print("PART 4: R is conjugate-linear  (antiunitary on the channel)")
    print("=" * 88)
    a = cycle_block(0.7 - 0.3j, 0.4 + 0.0j, 0.7 + 0.3j)
    for alpha in [2.0 + 0.0j, 1.0 - 1.0j, -3.5 + 2.1j]:
        lhs = R(alpha * a)
        rhs = np.conj(alpha) * R(a)
        check(
            f"R[alpha * A] = conj(alpha) * R[A]  for alpha = {alpha}",
            np.linalg.norm(lhs - rhs) < 1e-12,
        )


def part5_involution() -> None:
    print("\n" + "=" * 88)
    print("PART 5: R is an involution  (R o R = id  on the cycle channel)")
    print("=" * 88)
    for c1, c2, c3 in SAMPLE_TRIPLES:
        a = cycle_block(c1, c2, c3)
        check(
            f"R[R[A_fwd({c1},{c2},{c3})]] == A_fwd({c1},{c2},{c3})",
            np.linalg.norm(R(R(a)) - a) < 1e-12,
        )


def part6_fixed_locus() -> None:
    print("\n" + "=" * 88)
    print("PART 6: fixed locus is exactly  c_1 = conj(c_3),  c_2 real")
    print("=" * 88)
    fixed_examples = [
        (1.0 + 0.0j, 0.5 + 0.0j, 1.0 + 0.0j),
        (0.7 - 0.3j, 0.0 + 0.0j, 0.7 + 0.3j),
        (0.41 + 0.32j, 0.28 + 0.0j, 0.41 - 0.32j),
        (-2.0 + 1.5j, -0.7 + 0.0j, -2.0 - 1.5j),
    ]
    for c1, c2, c3 in fixed_examples:
        a = cycle_block(c1, c2, c3)
        check(
            f"on the fixed locus  c_1={c1}, c_2={c2}, c_3={c3}:  R[A] = A",
            np.linalg.norm(R(a) - a) < 1e-12,
        )
    not_fixed_examples = [
        (0.41 + 0.32j, 0.28 + 0.07j, 0.33 - 0.11j),  # c2 not real
        (1.0 + 0.5j, 0.0 + 0.0j, 1.0 + 0.5j),         # c1 != conj(c3)
        (1.0 + 0.0j, 0.5 + 0.1j, 1.0 + 0.0j),         # c2 has imaginary part
    ]
    for c1, c2, c3 in not_fixed_examples:
        a = cycle_block(c1, c2, c3)
        diff = np.linalg.norm(R(a) - a)
        check(
            f"off fixed locus  c_1={c1}, c_2={c2}, c_3={c3}:  R[A] != A",
            diff > 1e-6,
            f"||R[A] - A|| = {diff:.4f}",
        )


def part7_fixed_locus_real_dimension_is_three() -> None:
    print("\n" + "=" * 88)
    print("PART 7: fixed locus is a 3-real-parameter family")
    print("=" * 88)
    rng = np.random.default_rng(20260516)
    samples_in = 0
    for _ in range(64):
        c1 = rng.standard_normal() + 1j * rng.standard_normal()
        c2 = rng.standard_normal() + 0.0j
        c3 = np.conj(c1)
        a = cycle_block(c1, c2, c3)
        if np.linalg.norm(R(a) - a) < 1e-12:
            samples_in += 1
    check(
        "64 random points in c_1=conj(c_3), c_2 real are all fixed",
        samples_in == 64,
        f"in-locus fixed count = {samples_in}/64",
    )
    samples_out = 0
    for _ in range(64):
        c1 = rng.standard_normal() + 1j * rng.standard_normal()
        c2 = rng.standard_normal() + 1j * rng.standard_normal()
        c3 = rng.standard_normal() + 1j * rng.standard_normal()
        if abs(c2.imag) < 1e-3 and abs(c1 - np.conj(c3)) < 1e-3:
            continue
        a = cycle_block(c1, c2, c3)
        if np.linalg.norm(R(a) - a) > 1e-6:
            samples_out += 1
    check(
        "generic random triples are not fixed (negative control)",
        samples_out >= 60,
        f"not-fixed count = {samples_out}/64",
    )


def part8_result() -> None:
    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Graph-first residual antiunitary narrow bridge theorem:")
    print("    R[A] = P_23 @ A^dagger @ P_23")
    print("    coordinate action: (c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1))")
    print("    antiunitary and involutive on the oriented cycle channel")
    print("    fixed locus: c_1 = conj(c_3),  c_2 real  (3 real parameters)")
    print("  closes the load-bearing step in")
    print("    docs/PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md")
    print("  that asserts  'A_fwd = P_23 A_fwd^dagger P_23 fixes")
    print("  c_1 = conjugate(c_3), c_2 real'.")
    print("  Carrier identification and axis-stabilizer-equals-P_23")
    print("  are out of scope and remain with the cited one-hop authorities.")


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-FIRST RESIDUAL ANTIUNITARY NARROW BRIDGE THEOREM")
    print("=" * 88)
    print()
    print("Setting:")
    print("  P_23 = swap of axes 2 and 3  (graph-first axis stabilizer)")
    print("  A_fwd(c_1, c_2, c_3) = c_1 E_12 + c_2 E_23 + c_3 E_31")
    print("  R[A] = P_23 @ A^dagger @ P_23")

    part1_matrix_unit_conjugation_under_P23()
    part2_coordinate_action_on_the_cycle_channel()
    part3_channel_preservation()
    part4_antiunitarity()
    part5_involution()
    part6_fixed_locus()
    part7_fixed_locus_real_dimension_is_three()
    part8_result()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
