#!/usr/bin/env python3
"""Exact native observable law for the oriented forward cycle channel.

Question:
  Can the remaining positive carrier on the retained PMNS active class be
  equipped with an exact axiom-native observable/value law?

Answer:
  Yes. On the `hw=1` triplet:

    - the exact coordinate-cycle unitary projects to the forward cycle matrix
      `C`
    - the projected scalar site projectors give the diagonal matrix units
    - their products give the canonical forward-cycle edge basis
      `E12, E23, E31`

  Therefore any canonical active block has an exact native oriented-cycle
  decomposition

      A_fwd = c1 E12 + c2 E23 + c3 E31

  with coefficient law

      (c1, c2, c3) = diag(A C^dagger)

  equivalently

      c_i = Tr((P_i C)^dagger A)

  and the same coefficients are read from a lower-level active response profile
  via the derived active block.
"""

from __future__ import annotations

import sys

import numpy as np

from pmns_lower_level_utils import (
    CYCLE,
    active_operator,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
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


def taste_vector(state: tuple[int, int, int]) -> np.ndarray:
    v = np.array([1.0, 0.0], dtype=complex) if state[0] == 0 else np.array([0.0, 1.0], dtype=complex)
    for idx in (1, 2):
        vk = np.array([1.0, 0.0], dtype=complex) if state[idx] == 0 else np.array([0.0, 1.0], dtype=complex)
        v = np.kron(v, vk)
    return v


def hw1_triplet_projector() -> np.ndarray:
    states = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    return np.column_stack([taste_vector(s) for s in states])


def c3_taste_unitary() -> np.ndarray:
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    u = np.zeros((8, 8), dtype=complex)
    for a in alphas:
        a1, a2, a3 = a
        b = (a3, a1, a2)
        eps = (-1) ** ((a1 + a2) * a3)
        u[alpha_idx[b], alpha_idx[a]] = eps
    return u


def site_projector(state: tuple[int, int, int]) -> np.ndarray:
    v = taste_vector(state)
    return np.outer(v, v.conj())


def projected_scalar_projectors() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = hw1_triplet_projector()
    q1 = p.conj().T @ site_projector((1, 0, 0)) @ p
    q2 = p.conj().T @ site_projector((0, 1, 0)) @ p
    q3 = p.conj().T @ site_projector((0, 0, 1)) @ p
    return q1, q2, q3


def projected_forward_cycle() -> np.ndarray:
    p = hw1_triplet_projector()
    u = c3_taste_unitary()
    return p.conj().T @ (u @ u) @ p


def oriented_cycle_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    q1, q2, q3 = projected_scalar_projectors()
    c = projected_forward_cycle()
    return q1 @ c, q2 @ c, q3 @ c


def forward_cycle_part(a: np.ndarray) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[0, 1] = a[0, 1]
    out[1, 2] = a[1, 2]
    out[2, 0] = a[2, 0]
    return out


def oriented_cycle_coeffs_from_block(a: np.ndarray) -> np.ndarray:
    return np.diag(a @ projected_forward_cycle().conj().T)


def oriented_cycle_coeffs_from_response_columns(response_columns: list[np.ndarray], lam: float) -> np.ndarray:
    _kernel, block = derive_active_block_from_response_columns(response_columns, lam)
    return oriented_cycle_coeffs_from_block(block)


def part1_the_exact_coordinate_cycle_projects_to_the_forward_cycle_operator() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT COORDINATE CYCLE PROJECTS TO THE FORWARD CYCLE OPERATOR")
    print("=" * 88)

    c = projected_forward_cycle()
    check("The projected coordinate-cycle unitary equals the forward cycle C", np.linalg.norm(c - CYCLE) < 1e-12,
          f"error={np.linalg.norm(c - CYCLE):.2e}")
    check("Its adjoint is the backward cycle C^2", np.linalg.norm(c.conj().T - (CYCLE @ CYCLE)) < 1e-12)


def part2_projected_scalar_projectors_supply_the_native_forward_cycle_edge_basis() -> None:
    print("\n" + "=" * 88)
    print("PART 2: PROJECTED SCALAR PROJECTORS SUPPLY THE FORWARD-CYCLE EDGE BASIS")
    print("=" * 88)

    q1, q2, q3 = projected_scalar_projectors()
    b1, b2, b3 = oriented_cycle_basis()

    check("The projected scalar site projectors are exactly E11, E22, E33",
          np.linalg.norm(q1 - E11) < 1e-12 and np.linalg.norm(q2 - E22) < 1e-12 and np.linalg.norm(q3 - E33) < 1e-12)
    check("Multiplying by the projected forward cycle gives E12", np.linalg.norm(b1 - E12) < 1e-12)
    check("Multiplying by the projected forward cycle gives E23", np.linalg.norm(b2 - E23) < 1e-12)
    check("Multiplying by the projected forward cycle gives E31", np.linalg.norm(b3 - E31) < 1e-12)


def part3_any_canonical_active_block_has_an_exact_native_oriented_cycle_value_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EXACT VALUE LAW FOR ANY CANONICAL ACTIVE BLOCK")
    print("=" * 88)

    a = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    b1, b2, b3 = oriented_cycle_basis()
    coeffs = oriented_cycle_coeffs_from_block(a)
    rebuilt = coeffs[0] * b1 + coeffs[1] * b2 + coeffs[2] * b3
    fwd = forward_cycle_part(a)

    check("The native coefficient law reads the three forward-cycle values exactly",
          np.linalg.norm(coeffs - np.array([a[0, 1], a[1, 2], a[2, 0]], dtype=complex)) < 1e-12,
          f"coeffs={np.round(coeffs, 6)}")
    check("The forward-cycle part rebuilds exactly from the native edge basis", np.linalg.norm(rebuilt - fwd) < 1e-12,
          f"error={np.linalg.norm(rebuilt - fwd):.2e}")
    check("The mean oriented-cycle amplitude matches the existing transport odd mode",
          abs(np.mean(coeffs) - (a[0, 1] + a[1, 2] + a[2, 0]) / 3.0) < 1e-12,
          f"sigma={np.mean(coeffs)}")


def part4_the_same_cycle_values_are_read_from_the_lower_level_active_response_profile() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE SAME VALUE LAW HOLDS ON THE ACTIVE RESPONSE PROFILE")
    print("=" * 88)

    lam = 0.31
    target = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    sector = sector_operator_fixture_from_effective_block(target, seed=4217)
    _block, columns = active_response_columns_from_sector_operator(sector, lam)
    coeffs = oriented_cycle_coeffs_from_response_columns(columns, lam)

    check("The lower-level active response profile recovers the same forward-cycle coefficients exactly",
          np.linalg.norm(coeffs - np.array([target[0, 1], target[1, 2], target[2, 0]], dtype=complex)) < 1e-12,
          f"coeffs={np.round(coeffs, 6)}")


def main() -> int:
    print("=" * 88)
    print("PMNS ORIENTED CYCLE CHANNEL VALUE LAW")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the remaining positive carrier on the retained PMNS active class")
    print("  be equipped with an exact axiom-native observable/value law?")

    part1_the_exact_coordinate_cycle_projects_to_the_forward_cycle_operator()
    part2_projected_scalar_projectors_supply_the_native_forward_cycle_edge_basis()
    part3_any_canonical_active_block_has_an_exact_native_oriented_cycle_value_law()
    part4_the_same_cycle_values_are_read_from_the_lower_level_active_response_profile()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact native oriented-cycle observable law:")
    print("    - the projected coordinate cycle gives the forward cycle operator C")
    print("    - projected scalar site projectors give the edge basis E12,E23,E31")
    print("    - the forward-cycle values are exactly diag(A C^dagger)")
    print("    - the same values are read from the lower-level active response profile")
    print()
    print("  This equips the remaining positive carrier with an exact native value law.")
    print("  It still does not select those values from the sole axiom alone.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
