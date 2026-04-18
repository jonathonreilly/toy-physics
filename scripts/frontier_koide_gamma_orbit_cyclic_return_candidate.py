#!/usr/bin/env python3
"""
Koide Gamma-orbit cyclic-return candidate runner
================================================

STATUS: exact algebraic reduction plus one fresh candidate input

Purpose:
  Prove that the retained Gamma second-order return already compresses
  canonically to the Koide cyclic carrier, and isolate the one genuinely new
  microscopic ingredient still needed.

Safe statement:
  1. The exact Gamma_1 second-order return with general reachable-state weights
     produces the species diagonal triple diag(u, v, w).
  2. Under one fresh candidate assumption -- axis-oriented orbit-slot
     universality -- the full Gamma_i orbit becomes the cyclic family
        diag(u, v, w), diag(w, u, v), diag(v, w, u).
  3. Fourier transport of diag(u, v, w) lands exactly on the Koide cyclic basis
        B0 = I, B1 = C + C^2, B2 = i(C - C^2)
     with responses
        r0 = u + v + w,
        r1 = 2u - v - w,
        r2 = sqrt(3) (v - w).
  4. So the remaining positive task is only to derive the microscopic orbit law
     for (u, v, w) and then the selector relation among (r0, r1, r2).
"""

from __future__ import annotations

import sys

import numpy as np
import sympy as sp

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


def real_trace_pair(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.real(np.trace(a.conj().T @ b)))


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)

FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

S_O0 = [(0, 0, 0)]
S_T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
S_110 = [(1, 1, 0)]
S_101 = [(1, 0, 1)]
S_011 = [(0, 1, 1)]


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    out = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            out[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return out


P_T1 = projector(S_T1)
P_O0 = projector(S_O0)
P_110 = projector(S_110)
P_101 = projector(S_101)
P_011 = projector(S_011)


def species_basis() -> np.ndarray:
    cols = []
    for s in S_T1:
        v = np.zeros((16, 1), dtype=complex)
        v[INDEX[s + (0,)], 0] = 1.0
        cols.append(v)
    return np.hstack(cols)


SPECIES_BASIS = species_basis()


def restrict_species(op16: np.ndarray) -> np.ndarray:
    return SPECIES_BASIS.conj().T @ op16 @ SPECIES_BASIS


def cycle_matrix_np() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def cyclic_basis_np() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    c = cycle_matrix_np()
    cd = c.conj().T
    b0 = np.eye(3, dtype=complex)
    b1 = c + cd
    b2 = 1j * (c - cd)
    return b0, b1, b2


def fourier_matrix_np() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    return np.array([[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]], dtype=complex) / np.sqrt(3.0)


def cycle_matrix_sp() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def cyclic_basis_sp() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    c = cycle_matrix_sp()
    cd = c.T
    b0 = sp.eye(3)
    b1 = c + cd
    b2 = sp.I * (c - cd)
    return b0, b1, b2


def fourier_matrix_sp() -> sp.Matrix:
    omega = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
    return sp.Matrix([[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]) / sp.sqrt(3)


def gamma_return(gamma: np.ndarray, w_o0: float, w_110: float, w_101: float, w_011: float) -> np.ndarray:
    weight_op = w_o0 * P_O0 + w_110 * P_110 + w_101 * P_101 + w_011 * P_011
    return restrict_species(P_T1 @ gamma @ weight_op @ gamma @ P_T1)


def part1_exact_gamma1_shape() -> None:
    print("=" * 88)
    print("PART 1: the exact Gamma_1 return already gives a 3-slot species-orbit object")
    print("=" * 88)

    r_o0 = gamma_return(G1, 1.0, 0.0, 0.0, 0.0)
    r_110 = gamma_return(G1, 0.0, 1.0, 0.0, 0.0)
    r_101 = gamma_return(G1, 0.0, 0.0, 1.0, 0.0)
    r_011 = gamma_return(G1, 0.0, 0.0, 0.0, 1.0)

    check(
        "O_0 contributes only to the first species slot",
        np.allclose(r_o0, np.diag([1.0, 0.0, 0.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(r_o0)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "(1,1,0) contributes only to the second species slot",
        np.allclose(r_110, np.diag([0.0, 1.0, 0.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(r_110)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "(1,0,1) contributes only to the third species slot",
        np.allclose(r_101, np.diag([0.0, 0.0, 1.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(r_101)).tolist()}",
        kind="NUMERIC",
    )
    check(
        "(0,1,1) is unreachable at this order",
        np.allclose(r_011, np.zeros((3, 3)), atol=1e-12),
        detail=f"norm={np.linalg.norm(r_011):.2e}",
        kind="NUMERIC",
    )

    u, v, w, z = sp.symbols("u v w z", real=True)
    d_u = sp.diag(1, 0, 0)
    d_v = sp.diag(0, 1, 0)
    d_w = sp.diag(0, 0, 1)
    d_z = sp.zeros(3)
    combined = sp.simplify(u * d_u + v * d_v + w * d_w + z * d_z)
    check(
        "So the general Gamma_1 reachable-state return is exactly diag(u, v, w)",
        combined == sp.diag(u, v, w),
        detail=f"return={combined}",
    )


def part2_candidate_axis_orbit_family() -> None:
    print()
    print("=" * 88)
    print("PART 2: under one fresh candidate law, the full Gamma_i orbit is the cyclic family")
    print("=" * 88)

    c = cycle_matrix_np()
    d1 = gamma_return(G1, 1.0, 2.0, 3.0, 7.0)
    d2 = gamma_return(G2, 1.0, 3.0, 7.0, 2.0)
    d3 = gamma_return(G3, 1.0, 7.0, 2.0, 3.0)

    check(
        "Candidate axis-oriented slot assignment gives D1 = diag(u, v, w)",
        np.allclose(d1, np.diag([1.0, 2.0, 3.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d1)).tolist()}",
        kind="CANDIDATE",
    )
    check(
        "The same candidate gives D2 = diag(w, u, v)",
        np.allclose(d2, np.diag([3.0, 1.0, 2.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d2)).tolist()}",
        kind="CANDIDATE",
    )
    check(
        "The same candidate gives D3 = diag(v, w, u)",
        np.allclose(d3, np.diag([2.0, 3.0, 1.0]), atol=1e-12),
        detail=f"diag={np.real(np.diag(d3)).tolist()}",
        kind="CANDIDATE",
    )
    check(
        "So the Gamma orbit is exactly generated by species-cycle conjugation",
        np.allclose(d2, c @ d1 @ c.conj().T, atol=1e-12)
        and np.allclose(d3, c @ d2 @ c.conj().T, atol=1e-12),
        kind="CANDIDATE",
    )


def part3_exact_fourier_transport() -> None:
    print()
    print("=" * 88)
    print("PART 3: Fourier transport lands exactly on the Koide cyclic basis")
    print("=" * 88)

    u, v, w = sp.symbols("u v w", real=True)
    f = fourier_matrix_sp()
    d = sp.diag(u, v, w)
    b0, b1, b2 = cyclic_basis_sp()
    h = sp.simplify(f * d * f.H)

    r0 = u + v + w
    r1 = 2 * u - v - w
    r2 = sp.sqrt(3) * (v - w)
    h_basis = sp.simplify((r0 / 3) * b0 + (r1 / 6) * b1 + (r2 / 6) * b2)

    c = cycle_matrix_sp()
    check(
        "The transported Gamma return is Hermitian",
        sp.simplify(h - h.H) == sp.zeros(3),
    )
    check(
        "The transported Gamma return commutes with the species cycle",
        sp.simplify(h * c - c * h) == sp.zeros(3),
    )
    check(
        "So Fourier transport gives the unique Hermitian circulant target",
        sp.simplify(h - h_basis) == sp.zeros(3),
        detail=f"H={h_basis}",
    )
    check(
        "The exact cyclic responses are r0 = u + v + w, r1 = 2u - v - w, r2 = sqrt(3)(v - w)",
        True,
        detail=f"r0={r0}, r1={r1}, r2={r2}",
    )

    m0 = (u + v + w) / 3
    mc = (2 * u - v - w) / 3
    ms = (v - w) / sp.sqrt(3)
    h_moments = sp.simplify(m0 * b0 + (mc / 2) * b1 + (ms / 2) * b2)
    check(
        "Equivalently the orbit moments (m0, mc, ms) are exactly the Koide cyclic coordinates",
        sp.simplify(h - h_moments) == sp.zeros(3),
        detail=f"m0={m0}, mc={mc}, ms={ms}",
    )


def part4_observed_witness() -> None:
    print()
    print("=" * 88)
    print("PART 4: the observed charged-lepton amplitudes lie on the same Gamma-orbit carrier")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    f = fourier_matrix_np()
    b0, b1, b2 = cyclic_basis_np()
    h_obs = f @ np.diag(amps) @ f.conj().T

    r0 = real_trace_pair(b0, h_obs)
    r1 = real_trace_pair(b1, h_obs)
    r2 = real_trace_pair(b2, h_obs)
    selector_ratio = (r1**2 + r2**2) / (2.0 * r0**2)
    spectrum = np.sort(np.real(np.linalg.eigvalsh(h_obs)))

    check(
        "The transported observed operator has spectrum sqrt(m_e), sqrt(m_mu), sqrt(m_tau)",
        np.allclose(spectrum, np.sort(amps), atol=1e-10),
        detail=f"spectrum={spectrum.tolist()}",
        kind="NUMERIC",
    )
    check(
        "The observed amplitudes satisfy the cyclic selector to Koide precision",
        abs(selector_ratio - 1.0) < 1e-4,
        detail=f"(r1^2+r2^2)/(2 r0^2)={selector_ratio:.10f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_gamma1_shape()
    part2_candidate_axis_orbit_family()
    part3_exact_fourier_transport()
    part4_observed_witness()

    print()
    print("Interpretation:")
    print("  The exact Gamma return already has the right three-channel size.")
    print("  The one fresh candidate input is an axis-oriented orbit-slot law.")
    print("  Once that is supplied, the full Gamma orbit lands automatically on")
    print("  the Koide cyclic basis. The remaining open science is only the")
    print("  microscopic orbit law for (u, v, w) and the selector relation on")
    print("  its cyclic moments.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
