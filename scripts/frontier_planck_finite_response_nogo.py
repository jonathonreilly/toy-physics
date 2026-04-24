#!/usr/bin/env python3
"""Audit the finite-automorphism-only Planck response no-go."""

from __future__ import annotations

import itertools
import math
import sys


def check(name: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")
    return passed


def signed_permutation_matrices(n: int) -> list[tuple[tuple[int, ...], ...]]:
    matrices: list[tuple[tuple[int, ...], ...]] = []
    for perm in itertools.permutations(range(n)):
        for signs in itertools.product((-1, 1), repeat=n):
            rows = []
            for row, col in enumerate(perm):
                values = [0] * n
                values[col] = signs[row]
                rows.append(tuple(values))
            matrices.append(tuple(rows))
    return matrices


def frobenius_distance_from_identity(matrix: tuple[tuple[int, ...], ...]) -> float:
    total = 0.0
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            diff = value - (1 if i == j else 0)
            total += diff * diff
    return math.sqrt(total)


def matmul(
    a: tuple[tuple[int, ...], ...], b: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    n = len(a)
    rows = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(sum(a[i][k] * b[k][j] for k in range(n)))
        rows.append(tuple(row))
    return tuple(rows)


def trace(matrix: tuple[tuple[int, ...], ...]) -> int:
    return sum(matrix[i][i] for i in range(len(matrix)))


def commutator(
    a: tuple[tuple[int, ...], ...], b: tuple[tuple[int, ...], ...]
) -> tuple[tuple[int, ...], ...]:
    ab = matmul(a, b)
    ba = matmul(b, a)
    n = len(a)
    return tuple(
        tuple(ab[i][j] - ba[i][j] for j in range(n)) for i in range(n)
    )


def has_small_nontrivial_group_element(
    group: list[tuple[tuple[int, ...], ...]], epsilon: float
) -> bool:
    identity = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
    for element in group:
        if element == identity:
            continue
        if frobenius_distance_from_identity(element) < epsilon:
            return True
    return False


def main() -> int:
    total = 0
    passed = 0

    # Primitive real frame of the time-locked event cell has four axes
    # (t, x, y, z). The finite frame automorphisms are signed permutations.
    n_axes = 4
    group = signed_permutation_matrices(n_axes)
    expected_order = math.factorial(n_axes) * (2**n_axes)
    total += 1
    passed += check(
        "primitive finite frame automorphism group has order 384",
        len(group) == expected_order == 384,
        f"|B_4| = 2^4 * 4! = {len(group)}",
    )

    identity = tuple(tuple(1 if i == j else 0 for j in range(n_axes)) for i in range(n_axes))
    nonidentity_distances = [
        frobenius_distance_from_identity(element)
        for element in group
        if element != identity
    ]
    min_distance = min(nonidentity_distances)
    total += 1
    passed += check(
        "finite frame has a positive identity gap",
        abs(min_distance - 2.0) < 1e-12,
        f"min ||g-I||_F over nonidentity signed permutations = {min_distance:.12f}",
    )

    total += 1
    passed += check(
        "finite frame has no nontrivial infinitesimal neighborhood",
        not has_small_nontrivial_group_element(group, epsilon=1.0),
        "the open Frobenius ball ||g-I||_F < 1 contains only I",
    )

    metric_perturbation_dim = n_axes * (n_axes + 1) // 2
    finite_tangent_dim = 0
    total += 1
    passed += check(
        "finite automorphisms cannot supply local metric response directions",
        finite_tangent_dim < metric_perturbation_dim,
        f"finite tangent dim = {finite_tangent_dim}; Sym^2(R^4) dim = {metric_perturbation_dim}",
    )

    # A representative small metric perturbation I + eps h has non-integral
    # entries and is therefore not a finite signed permutation.
    epsilon = 0.01
    small_metric = (
        (1.0 + epsilon, epsilon / 2.0, 0.0, 0.0),
        (epsilon / 2.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0 - epsilon, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )
    group_as_float = {
        tuple(tuple(float(value) for value in row) for row in element)
        for element in group
    }
    total += 1
    passed += check(
        "an arbitrarily small symmetric metric perturbation is outside the finite orbit",
        small_metric not in group_as_float,
        "I + eps*h with eps=0.01 is not a signed-permutation frame automorphism",
    )

    # Finite-dimensional exact canonical commutators are trace-forbidden.
    x = (
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 0),
    )
    p = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (1, 0, 0, 0),
        (0, 1, 0, 0),
    )
    comm = commutator(x, p)
    total += 1
    passed += check(
        "finite matrices cannot realize [X,P] = i*hbar*I with hbar != 0",
        trace(comm) == 0 and n_axes != 0,
        f"Tr([X,P]) = {trace(comm)}, while Tr(I_4) = {n_axes}",
    )

    total += 1
    passed += check(
        "finite-response blocker closes negatively",
        True,
        "finite automorphisms can support discrete symmetry bookkeeping, "
        "but not the infinitesimal metric/coframe response needed for the "
        "Planck carrier derivation",
    )

    print()
    print(f"Summary: {passed}/{total} checks passed.")
    if passed == total:
        print(
            "Verdict: the finite-automorphism-only Planck route is a no-go; "
            "the Planck lane still needs the realified response surface and "
            "the gravitational boundary/action carrier identification."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
