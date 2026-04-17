#!/usr/bin/env python3
"""
Exact site-phase / cube-shift intertwiner on the BZ-corner subspace.

Safe statement:
  On the BZ-corner subspace of an even periodic lattice Z_L^3, the site-phase
  operators P_mu act as exact bit flips on the corner labels. Under the
  isometry Phi|alpha> = |X_alpha>, this gives Phi^dagger P_mu Phi = S_mu on
  C^8, where S_mu is the cube-shift on tensor slot mu.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def site_index(x: tuple[int, int, int], L: int) -> int:
    return ((x[0] % L) * L + (x[1] % L)) * L + (x[2] % L)


def bz_corner_state(alpha: tuple[int, int, int], L: int) -> np.ndarray:
    state = np.zeros(L**3, dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                phase = (-1) ** (alpha[0] * x1 + alpha[1] * x2 + alpha[2] * x3)
                state[site_index((x1, x2, x3), L)] = phase
    return state / math.sqrt(L**3)


def site_phase_operator(mu: int, L: int) -> np.ndarray:
    operator = np.zeros((L**3, L**3), dtype=complex)
    for x1 in range(L):
        for x2 in range(L):
            for x3 in range(L):
                x = (x1, x2, x3)
                operator[site_index(x, L), site_index(x, L)] = (-1) ** x[mu]
    return operator


def cube_shift(mu: int) -> np.ndarray:
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    ident = np.eye(2, dtype=complex)
    factors = [ident, ident, ident]
    factors[mu] = sigma_x
    return np.kron(np.kron(factors[0], factors[1]), factors[2])


def part1_bit_flip_on_bz_corners(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print(f"PART 1: P_mu |X_alpha> = |X_(alpha xor e_mu)> on Z_{L}^3")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))
    for mu in range(3):
        operator = site_phase_operator(mu, L)
        for alpha in alphas:
            result = operator @ bz_corner_state(alpha, L)
            target = list(alpha)
            target[mu] = 1 - target[mu]
            expected = bz_corner_state(tuple(target), L)
            check(
                f"P_{mu + 1} |X_{alpha}> = |X_{tuple(target)}>",
                np.allclose(result, expected, atol=1e-12),
                f"max|diff| = {np.max(np.abs(result - expected)):.2e}",
            )


def part2_intertwiner(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Phi^dagger P_mu Phi = S_mu on C^8")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))
    phi = np.zeros((L**3, 8), dtype=complex)
    for idx, alpha in enumerate(alphas):
        phi[:, idx] = bz_corner_state(alpha, L)

    gram = phi.conj().T @ phi
    check(
        "Phi is an isometry on the BZ-corner subspace",
        np.allclose(gram, np.eye(8), atol=1e-12),
        f"max|Phi^dagger Phi - I| = {np.max(np.abs(gram - np.eye(8))):.2e}",
    )

    for mu in range(3):
        pulled = phi.conj().T @ site_phase_operator(mu, L) @ phi
        expected = cube_shift(mu)
        check(
            f"Phi^dagger P_{mu + 1} Phi = S_{mu + 1}",
            np.allclose(pulled, expected, atol=1e-12),
            f"max|diff| = {np.max(np.abs(pulled - expected)):.2e}",
        )


def part3_joint_eigensystem_transfer(L: int = 4) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Joint P_mu eigensystem on the BZ-corner subspace")
    print("=" * 72)

    alphas = list(itertools.product([0, 1], repeat=3))
    for signs in itertools.product([+1, -1], repeat=3):
        psi = np.zeros(L**3, dtype=complex)
        for alpha in alphas:
            coefficient = np.prod([signs[mu] ** alpha[mu] for mu in range(3)])
            psi += coefficient * bz_corner_state(alpha, L)
        psi /= math.sqrt(8)

        norm_sq = float(np.real(np.vdot(psi, psi)))
        check(
            f"psi_{signs} has norm 1",
            abs(norm_sq - 1.0) < 1e-12,
            f"|psi|^2 = {norm_sq:.12f}",
        )

        for mu in range(3):
            result = site_phase_operator(mu, L) @ psi
            expected = signs[mu] * psi
            check(
                f"P_{mu + 1} psi_{signs} = {signs[mu]:+d} psi_{signs}",
                np.allclose(result, expected, atol=1e-12),
            )


def main() -> int:
    print("=" * 72)
    print("SITE-PHASE / CUBE-SHIFT INTERTWINER")
    print("=" * 72)
    part1_bit_flip_on_bz_corners()
    part2_intertwiner()
    part3_joint_eigensystem_transfer()
    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
