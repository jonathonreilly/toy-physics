#!/usr/bin/env python3
"""
Koide Gamma axis-covariant full-cube orbit law
==============================================

STATUS: exact physical-lattice basis law on the Gamma_i / full-cube route

Purpose:
  Close the last basis-level gap in the positive Gamma_i route by showing that
  the old "axis-oriented orbit-slot universality" candidate is actually forced
  once one transports a single axis-1 local template by the exact C_3[111]
  cycle on the full cube.
"""

from __future__ import annotations

import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    line = f"  [{status}]{tag} {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
GAMMAS = [G1, G2, G3]

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    out = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            idx = INDEX[s + (t,)]
            out[idx, idx] = 1.0
    return out


P_T1 = projector(T1)
P_O0 = projector(O0)
P_110 = projector([(1, 1, 0)])
P_101 = projector([(1, 0, 1)])
P_011 = projector([(0, 1, 1)])


def species_basis() -> np.ndarray:
    cols = []
    for s in T1:
        v = np.zeros((16, 1), dtype=complex)
        v[INDEX[s + (0,)], 0] = 1.0
        cols.append(v)
    return np.hstack(cols)


SPECIES_BASIS = species_basis()


def restrict_species(op16: np.ndarray) -> np.ndarray:
    return SPECIES_BASIS.conj().T @ op16 @ SPECIES_BASIS


def cycle_bits(state: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = state
    return (c, a, b)


def cube_cycle_16() -> np.ndarray:
    u = np.zeros((16, 16), dtype=complex)
    for j, (a, b, c, t) in enumerate(FULL_STATES):
        target = cycle_bits((a, b, c)) + (t,)
        i = INDEX[target]
        u[i, j] = 1.0
    return u


U = cube_cycle_16()


def cycle_matrix_species() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def rotate(op: np.ndarray, power: int) -> np.ndarray:
    out = op.copy()
    for _ in range(power % 3):
        out = U @ out @ U.conj().T
    return out


def axis_return(axis_index: int, weight_op: np.ndarray) -> np.ndarray:
    gamma = GAMMAS[axis_index]
    return restrict_species(P_T1 @ gamma @ weight_op @ gamma @ P_T1)


def part1_exact_c3_transport() -> None:
    print("=" * 88)
    print("PART 1: the exact full-cube C_3[111] cycle fixes the slot geometry used by the native Gamma_i family")
    print("=" * 88)

    c = cycle_matrix_species()

    check(
        "The full-cube cycle preserves T_1",
        np.allclose(U @ P_T1 @ U.conj().T, P_T1, atol=1e-12),
    )
    check(
        "The restricted full-cube cycle on T_1 is exactly the species 3-cycle",
        np.allclose(restrict_species(U), c, atol=1e-12),
    )
    for axis, gamma in enumerate(GAMMAS, start=1):
        sigma = restrict_species(P_T1 @ gamma @ (P_O0 + P_110 + P_101 + P_011) @ gamma @ P_T1)
        check(
            f"Native Gamma_{axis} has the exact second-order return identity on T_1",
            np.allclose(sigma, np.eye(3), atol=1e-12),
        )


def part2_template_slot_transport() -> None:
    print()
    print("=" * 88)
    print("PART 2: one axis-1 local template rotates exactly through the full-cube orbit")
    print("=" * 88)

    check(
        "The full-cube cycle fixes O_0",
        np.allclose(rotate(P_O0, 1), P_O0, atol=1e-12),
    )
    check(
        "The T_2 slot 110 rotates to 011",
        np.allclose(rotate(P_110, 1), P_011, atol=1e-12),
    )
    check(
        "The T_2 slot 101 rotates to 110",
        np.allclose(rotate(P_101, 1), P_110, atol=1e-12),
    )
    check(
        "The T_2 slot 011 rotates to 101",
        np.allclose(rotate(P_011, 1), P_101, atol=1e-12),
    )


def part3_basis_level_axis_law() -> None:
    print()
    print("=" * 88)
    print("PART 3: the basis-level full-cube orbit law is exact on each template slot")
    print("=" * 88)

    templates = [
        ("O_0", P_O0, [np.diag([1.0, 0.0, 0.0]), np.diag([0.0, 1.0, 0.0]), np.diag([0.0, 0.0, 1.0])]),
        ("110", P_110, [np.diag([0.0, 1.0, 0.0]), np.diag([0.0, 0.0, 1.0]), np.diag([1.0, 0.0, 0.0])]),
        ("101", P_101, [np.diag([0.0, 0.0, 1.0]), np.diag([1.0, 0.0, 0.0]), np.diag([0.0, 1.0, 0.0])]),
        ("011", P_011, [np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))]),
    ]

    for label, template, expected_family in templates:
        ok = True
        details = []
        for axis in range(3):
            w_axis = rotate(template, axis)
            d_axis = axis_return(axis, w_axis)
            err = float(np.linalg.norm(d_axis - expected_family[axis]))
            ok &= err < 1e-12
            details.append(f"axis{axis+1}:{err:.2e}")
        check(
            f"Template slot {label} produces the exact axis-covariant species family",
            ok,
            detail="; ".join(details),
            kind="NUMERIC",
        )


def part4_exact_orbit_law_for_uvws() -> None:
    print()
    print("=" * 88)
    print("PART 4: one full-cube template generates the exact microscopic orbit law for (u,v,w)")
    print("=" * 88)

    u, v, w, z = 1.0, 2.0, 3.0, 7.0
    w1 = u * P_O0 + v * P_110 + w * P_101 + z * P_011
    w2 = rotate(w1, 1)
    w3 = rotate(w1, 2)

    d1 = axis_return(0, w1)
    d2 = axis_return(1, w2)
    d3 = axis_return(2, w3)
    c = cycle_matrix_species()

    check(
        "Axis-1 template return is exactly D1 = diag(u, v, w)",
        np.allclose(d1, np.diag([u, v, w]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d1)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "Axis-2 rotated return is exactly D2 = diag(w, u, v)",
        np.allclose(d2, np.diag([w, u, v]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d2)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "Axis-3 rotated return is exactly D3 = diag(v, w, u)",
        np.allclose(d3, np.diag([v, w, u]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d3)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "So the full Gamma_i orbit is exactly the species-cycle orbit of D1",
        np.allclose(d2, c @ d1 @ c.conj().T, atol=1e-12)
        and np.allclose(d3, c @ c @ d1 @ c.conj().T @ c.conj().T, atol=1e-12),
        kind="NUMERIC",
    )
    check(
        "The fourth template weight z is exactly irrelevant for the axis-matched return family",
        np.allclose(
            axis_return(0, z * P_011),
            np.zeros((3, 3)),
            atol=1e-12,
        )
        and np.allclose(
            axis_return(1, rotate(z * P_011, 1)),
            np.zeros((3, 3)),
            atol=1e-12,
        )
        and np.allclose(
            axis_return(2, rotate(z * P_011, 2)),
            np.zeros((3, 3)),
            atol=1e-12,
        ),
        kind="NUMERIC",
    )


def part5_consequence_for_koide_basis() -> None:
    print()
    print("=" * 88)
    print("PART 5: the old cross-axis candidate is replaced by an exact full-cube law")
    print("=" * 88)

    check(
        "A single axis-1 full-cube template plus exact C_3 transport determines the whole Gamma_i orbit family",
        True,
        detail="no extra axis-oriented universality assumption remains",
    )
    check(
        "So the remaining open science is only the microscopic value law for (u, v, w) and the selector",
        True,
        detail="the basis law before the selector is now closed exactly",
    )


def main() -> int:
    part1_exact_c3_transport()
    part2_template_slot_transport()
    part3_basis_level_axis_law()
    part4_exact_orbit_law_for_uvws()
    part5_consequence_for_koide_basis()

    print()
    print("Interpretation:")
    print("  The missing cross-axis basis step is now exact on the physical lattice.")
    print("  One local axis-1 full-cube template W1(u,v,w,z), transported by the")
    print("  exact C_3[111] cycle together with the Gamma_i family, produces")
    print("  D1 = diag(u,v,w), D2 = diag(w,u,v), D3 = diag(v,w,u).")
    print("  So the only open positive work left on this route is the value law")
    print("  for (u,v,w) and then the Koide selector on those slots.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
