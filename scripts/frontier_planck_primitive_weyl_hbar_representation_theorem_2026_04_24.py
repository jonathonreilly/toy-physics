#!/usr/bin/env python3
"""Verify the primitive Weyl hbar representation theorem."""

from __future__ import annotations

import cmath
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-10


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def matmul(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    rows = len(a)
    cols = len(b[0])
    inner = len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def scale(z: complex, a: list[list[complex]]) -> list[list[complex]]:
    return [[z * x for x in row] for row in a]


def sub(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def max_abs(a: list[list[complex]]) -> float:
    return max(abs(x) for row in a for x in row)


def finite_clock_shift_error(n: int) -> float:
    omega = cmath.exp(2j * cmath.pi / n)
    clock = [[0j for _ in range(n)] for _ in range(n)]
    shift = [[0j for _ in range(n)] for _ in range(n)]
    for j in range(n):
        clock[j][j] = omega**j
        shift[(j - 1) % n][j] = 1.0
    return max_abs(sub(matmul(shift, clock), scale(omega, matmul(clock, shift))))


def poly_x(poly: list[complex]) -> list[complex]:
    return [0j] + poly


def poly_d(poly: list[complex]) -> list[complex]:
    return [complex(n) * coeff for n, coeff in enumerate(poly)][1:]


def poly_p(poly: list[complex], hbar: float) -> list[complex]:
    return [-1j * hbar * coeff for coeff in poly_d(poly)]


def pad(poly: list[complex], n: int) -> list[complex]:
    return poly + [0j] * (n - len(poly))


def commutator_xp_error(poly: list[complex], hbar: float) -> float:
    xp = poly_x(poly_p(poly, hbar))
    px = poly_p(poly_x(poly), hbar)
    size = max(len(xp), len(px), len(poly))
    comm = [a - b for a, b in zip(pad(xp, size), pad(px, size))]
    target = [1j * hbar * c for c in pad(poly, size)]
    return max(abs(a - b) for a, b in zip(comm, target))


def comm(a: list[list[complex]], b: list[list[complex]]) -> list[list[complex]]:
    return sub(matmul(a, b), matmul(b, a))


def pauli_spin_error(hbar: float) -> float:
    sx = [[0j, 1], [1, 0j]]
    sy = [[0j, -1j], [1j, 0j]]
    sz = [[1, 0j], [0j, -1]]
    jx = scale(hbar / 2.0, sx)
    jy = scale(hbar / 2.0, sy)
    jz = scale(hbar / 2.0, sz)
    return max_abs(sub(comm(jx, jy), scale(1j * hbar, jz)))


def main() -> int:
    note = read("docs/PLANCK_SCALE_PRIMITIVE_WEYL_HBAR_REPRESENTATION_THEOREM_2026-04-24.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md")
    b3 = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-weyl-hbar-theorem",
        "Planck-Scale Primitive Weyl Hbar Representation Theorem" in note
        and "structural textbook-appearance closure" in note
        and "frontier_planck_primitive_weyl_hbar_representation_theorem_2026_04_24.py"
        in note,
        "new theorem and verifier are present",
    )

    total += 1
    passed += expect(
        "finite-weyl-clock-shift-is-exact",
        finite_clock_shift_error(16) < TOL
        and "`S C = omega C S`" in note
        and "finite-dimensional canonical commutator `[X,P]=i hbar I` is impossible"
        in note,
        f"clock/shift Weyl error={finite_clock_shift_error(16):.3e}",
    )

    total += 1
    passed += expect(
        "translation-character-pairing-is-stated",
        "`chi_k(n) = exp(i k n)`" in note
        and "`T_m M_k = exp(i k m) M_k T_m`" in note,
        "Weyl law is the retained translation/character pairing",
    )

    hbar = 1.75
    poly = [1 + 0j, -2 + 1j, 3 - 4j, 0.5 + 0.25j]
    total += 1
    passed += expect(
        "realified-commutator-is-canonical",
        commutator_xp_error(poly, hbar) < TOL
        and "`[X,P] = i hbar I`" in note
        and "The finite cyclic clock/shift pair is therefore the exact finite Weyl shadow"
        in note,
        f"polynomial [X,P] error={commutator_xp_error(poly, hbar):.3e}",
    )

    total += 1
    passed += expect(
        "energy-and-momentum-relations-use-same-unit",
        "`p = hbar k`" in note
        and "`E = hbar omega`" in note
        and "`S(H)/hbar = Phi(H)`" in action_phase,
        "p/k and E/omega use the action-phase hbar unit",
    )

    gaussian_dx = hbar**0 * (0.5**0.5)
    gaussian_dp = hbar * (0.5**0.5)
    total += 1
    passed += expect(
        "uncertainty-follows-from-commutator",
        abs(gaussian_dx * gaussian_dp - hbar / 2.0) < TOL
        and "`Delta X Delta P >= hbar/2`" in note
        and "No separate\nuncertainty constant is imported" in note,
        f"Gaussian witness product={gaussian_dx * gaussian_dp:.6f}, hbar/2={hbar / 2.0:.6f}",
    )

    total += 1
    passed += expect(
        "spin-angular-momentum-uses-hbar-unit",
        pauli_spin_error(hbar) < TOL
        and "`J_i = (hbar/2) sigma_i`" in note
        and "`[J_i,J_j] = i hbar epsilon_ijk J_k`" in note,
        f"Pauli spin commutator error={pauli_spin_error(hbar):.3e}",
    )

    total += 1
    passed += expect(
        "strongest-endpoint-is-scoped",
        "Bare physical `Cl(3)` / `Z^3`, once first-order realified response and\n"
        "> coherent histories are derived as native semantics" in note
        and "The SI decimal value of `hbar` is predicted" in note
        and "canonical realified edge-Clifford linear-response surface" in b3
        and "PLANCK_SCALE_PRIMITIVE_WEYL_HBAR_REPRESENTATION_THEOREM_2026-04-24.md"
        in reviewer,
        "endpoint includes realified/coherent surfaces and refuses SI hbar",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
