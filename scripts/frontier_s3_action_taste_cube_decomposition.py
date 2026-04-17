#!/usr/bin/env python3
"""
Exact S_3 axis-permutation decomposition of the taste cube C^8.

Safe statement:
  Under the tensor-position permutation action of S_3 on C^8 = (C^2)^{otimes 3},
  the representation decomposes as 4*A_1 + 2*E, with no copy of A_2.
  Each of the hw=1 and hw=2 sectors is the standard permutation carrier
  A_1 + E.
"""

from __future__ import annotations

import itertools
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


S3_ELEMENTS = {
    "e": (0, 1, 2),
    "(12)": (1, 0, 2),
    "(23)": (0, 2, 1),
    "(13)": (2, 1, 0),
    "(123)": (1, 2, 0),
    "(132)": (2, 0, 1),
}


def basis_index(alpha: tuple[int, int, int]) -> int:
    return alpha[0] * 4 + alpha[1] * 2 + alpha[2]


def build_s3_unitary(perm: tuple[int, int, int]) -> np.ndarray:
    perm_inv = [0, 0, 0]
    for idx, value in enumerate(perm):
        perm_inv[value] = idx

    unitary = np.zeros((8, 8), dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        new_alpha = tuple(alpha[perm_inv[idx]] for idx in range(3))
        unitary[basis_index(new_alpha), basis_index(alpha)] = 1.0
    return unitary


def hw_projector(hw: int) -> np.ndarray:
    projector = np.zeros((8, 8), dtype=complex)
    for alpha in itertools.product([0, 1], repeat=3):
        if sum(alpha) == hw:
            projector[basis_index(alpha), basis_index(alpha)] = 1.0
    return projector


def sector_indices(hw: int) -> list[int]:
    return [basis_index(alpha) for alpha in itertools.product([0, 1], repeat=3) if sum(alpha) == hw]


def part1_representation() -> dict[str, np.ndarray]:
    print("\n" + "=" * 72)
    print("PART 1: S_3 unitary representation on C^8")
    print("=" * 72)

    unitaries = {name: build_s3_unitary(perm) for name, perm in S3_ELEMENTS.items()}
    for name, unitary in unitaries.items():
        check(f"U({name}) is unitary", np.allclose(unitary @ unitary.conj().T, np.eye(8)))

    check("U(e) = I", np.allclose(unitaries["e"], np.eye(8)))
    for name in ["(12)", "(23)", "(13)"]:
        check(f"U({name})^2 = I", np.allclose(unitaries[name] @ unitaries[name], np.eye(8)))
    for name in ["(123)", "(132)"]:
        check(
            f"U({name})^3 = I",
            np.allclose(np.linalg.matrix_power(unitaries[name], 3), np.eye(8)),
        )

    lhs = unitaries["(12)"] @ unitaries["(23)"] @ unitaries["(12)"]
    check("(12)(23)(12) = (13)", np.allclose(lhs, unitaries["(13)"]))
    return unitaries


def part2_hamming_weight(unities: dict[str, np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Hamming-weight preservation and orbit structure")
    print("=" * 72)

    for name, unitary in unities.items():
        for hw in range(4):
            projector = hw_projector(hw)
            check(
                f"[U({name}), P_hw={hw}] = 0",
                np.allclose(unitary @ projector, projector @ unitary),
            )

    all_alphas = list(itertools.product([0, 1], repeat=3))
    visited: set[tuple[int, int, int]] = set()
    orbit_sizes: list[int] = []
    for alpha in all_alphas:
        if alpha in visited:
            continue
        orbit = set()
        for perm in S3_ELEMENTS.values():
            perm_inv = [0, 0, 0]
            for idx, value in enumerate(perm):
                perm_inv[value] = idx
            orbit.add(tuple(alpha[perm_inv[idx]] for idx in range(3)))
        visited.update(orbit)
        orbit_sizes.append(len(orbit))
    check("Orbit sizes are {1, 1, 3, 3}", sorted(orbit_sizes) == [1, 1, 3, 3], f"got {sorted(orbit_sizes)}")


def part3_characters(unities: dict[str, np.ndarray]) -> dict[str, float]:
    print("\n" + "=" * 72)
    print("PART 3: Class characters")
    print("=" * 72)

    chars = {name: float(np.real(np.trace(unitary))) for name, unitary in unities.items()}
    check("chi(e) = 8", abs(chars["e"] - 8.0) < 1e-10)
    check("all 2-cycles have character 4", all(abs(chars[name] - 4.0) < 1e-10 for name in ["(12)", "(23)", "(13)"]))
    check("all 3-cycles have character 2", all(abs(chars[name] - 2.0) < 1e-10 for name in ["(123)", "(132)"]))
    return {"e": chars["e"], "2c": chars["(12)"], "3c": chars["(123)"]}


def part4_decomposition(chars: dict[str, float]) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Multiplicity calculation")
    print("=" * 72)

    size = 6.0
    multiplicities = {
        "A_1": (chars["e"] + 3 * chars["2c"] + 2 * chars["3c"]) / size,
        "A_2": (chars["e"] - 3 * chars["2c"] + 2 * chars["3c"]) / size,
        "E": (2 * chars["e"] - 2 * chars["3c"]) / size,
    }

    check("mult(A_1) = 4", abs(multiplicities["A_1"] - 4.0) < 1e-10, f"got {multiplicities['A_1']:.6f}")
    check("mult(A_2) = 0", abs(multiplicities["A_2"]) < 1e-10, f"got {multiplicities['A_2']:.6f}")
    check("mult(E) = 2", abs(multiplicities["E"] - 2.0) < 1e-10, f"got {multiplicities['E']:.6f}")
    total_dim = multiplicities["A_1"] + multiplicities["A_2"] + 2.0 * multiplicities["E"]
    check("dimension matches 8", abs(total_dim - 8.0) < 1e-10, f"got {total_dim:.6f}")


def part5_sector_characters(unities: dict[str, np.ndarray]) -> None:
    print("\n" + "=" * 72)
    print("PART 5: hw-sector decomposition")
    print("=" * 72)

    for hw in [1, 2]:
        indices = sector_indices(hw)
        expected = {"e": 3.0, "(12)": 1.0, "(23)": 1.0, "(13)": 1.0, "(123)": 0.0, "(132)": 0.0}
        for name, unitary in unities.items():
            restricted = unitary[np.ix_(indices, indices)]
            char = float(np.real(np.trace(restricted)))
            check(
                f"hw={hw} character chi({name}) = {expected[name]:.0f}",
                abs(char - expected[name]) < 1e-10,
                f"got {char:.6f}",
            )


def main() -> int:
    print("=" * 72)
    print("S_3 TASTE-CUBE DECOMPOSITION")
    print("=" * 72)
    unitaries = part1_representation()
    part2_hamming_weight(unitaries)
    chars = part3_characters(unitaries)
    part4_decomposition(chars)
    part5_sector_characters(unitaries)
    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
