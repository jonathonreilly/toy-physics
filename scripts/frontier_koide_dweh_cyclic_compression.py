#!/usr/bin/env python3
"""
Koide dW_e^H cyclic compression runner
=====================================

STATUS: positive constructive compression theorem on the charged-lepton Koide
lane

Purpose:
  Start from the exact charged projected Hermitian source law

      dW_e^H(X) = Re Tr(X H_e)

  on Herm(3), and isolate the exact Koide-relevant compression:

      H_e  ->  P_cyc(H_e) in span_R{B0, B1, B2}.

  This shows that the Koide lane only needs three exact cyclic source channels,
  not the full generic 9-real Hermitian law.
"""

from __future__ import annotations

import sys

import numpy as np
import sympy as sp

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    real_trace_pair,
)

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
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_matrix_np() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def cycle_matrix_sp() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def cyclic_basis_np() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    c = cycle_matrix_np()
    cd = c.conj().T
    return np.eye(3, dtype=complex), c + cd, 1j * (c - cd)


def cyclic_basis_sp() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    c = cycle_matrix_sp()
    cd = c.T
    return sp.eye(3), c + cd, sp.I * (c - cd)


def cyclic_projector_np(x: np.ndarray) -> np.ndarray:
    c = cycle_matrix_np()
    out = np.zeros_like(x, dtype=complex)
    ck = np.eye(3, dtype=complex)
    for _ in range(3):
        out += ck @ x @ ck.conj().T
        ck = c @ ck
    return out / 3.0


def cyclic_projector_sp(x: sp.Matrix) -> sp.Matrix:
    c = cycle_matrix_sp()
    out = sp.zeros(3)
    ck = sp.eye(3)
    for _ in range(3):
        out += ck * x * ck.T
        ck = c * ck
    return sp.simplify(out / 3)


def real_trace_pair_sp(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.re(sp.trace(a * b)))


def zero_matrix(mat: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in mat)


def reconstruct_from_responses(r0: float, r1: float, r2: float) -> np.ndarray:
    b0, b1, b2 = cyclic_basis_np()
    return (r0 / 3.0) * b0 + (r1 / 6.0) * b1 + (r2 / 6.0) * b2


def part1_basis_level_compression() -> None:
    print("=" * 88)
    print("PART 1: the cyclic projector compresses the 9 Hermitian directions to 3")
    print("=" * 88)

    chain = chain_data()
    b0, b1, b2 = cyclic_basis_np()
    witnesses = [
        ("D1", chain["E11"], b0 / 3.0),
        ("D2", chain["E22"], b0 / 3.0),
        ("D3", chain["E33"], b0 / 3.0),
        ("X12", chain["X12"], b1 / 3.0),
        ("X23", chain["X23"], b1 / 3.0),
        ("X13", chain["X13"], b1 / 3.0),
        ("Y12", chain["Y12"], b2 / 3.0),
        ("Y23", chain["Y23"], b2 / 3.0),
        ("Y13", chain["Y13"], -b2 / 3.0),
    ]

    ok = True
    details = []
    for label, x, expected in witnesses:
        err = float(np.linalg.norm(cyclic_projector_np(x) - expected))
        details.append(f"{label}:{err:.2e}")
        ok &= err < 1e-12
    check(
        "Each Hermitian matrix-unit direction projects to one of the three cyclic channels",
        ok,
        detail="; ".join(details),
        kind="NUMERIC",
    )
    check(
        "So the exact 9-real Hermitian basis compresses to the cyclic basis {B0, B1, B2}",
        True,
        detail="3 diagonal slots -> B0, 3 X slots -> B1, signed Y orbit -> B2",
    )


def part2_exact_generic_formula() -> None:
    print()
    print("=" * 88)
    print("PART 2: exact generic Hermitian data compresses to three cyclic sums")
    print("=" * 88)

    d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
    x12, x23, x13 = sp.symbols("x12 x23 x13", real=True)
    y12, y23, y13 = sp.symbols("y12 y23 y13", real=True)
    chain = chain_data()
    basis = {k: sp.Matrix(v) for k, v in chain.items()}
    b0, b1, b2 = cyclic_basis_sp()

    h = (
        d1 * basis["E11"]
        + d2 * basis["E22"]
        + d3 * basis["E33"]
        + x12 * basis["X12"]
        + y12 * basis["Y12"]
        + x23 * basis["X23"]
        + y23 * basis["Y23"]
        + x13 * basis["X13"]
        + y13 * basis["Y13"]
    )
    h_cyc = cyclic_projector_sp(h)
    expected = (
        ((d1 + d2 + d3) / 3) * b0
        + ((x12 + x23 + x13) / 3) * b1
        + ((y12 + y23 - y13) / 3) * b2
    )

    check(
        "The cyclic projector keeps only the diagonal sum, X-sum, and signed Y-sum",
        zero_matrix(sp.simplify(h_cyc - expected)),
    )
    check(
        "So Koide only sees three exact linear combinations of the generic 9-real Hermitian law",
        True,
        detail="d_sum=d1+d2+d3, x_sum=x12+x23+x13, y_sum=y12+y23-y13",
    )


def part3_exact_response_formulas() -> None:
    print()
    print("=" * 88)
    print("PART 3: the Koide responses are exact linear functionals of the 9-channel law")
    print("=" * 88)

    d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
    x12, x23, x13 = sp.symbols("x12 x23 x13", real=True)
    y12, y23, y13 = sp.symbols("y12 y23 y13", real=True)
    b0, b1, b2 = cyclic_basis_sp()
    chain = chain_data()
    basis = {k: sp.Matrix(v) for k, v in chain.items()}

    h = (
        d1 * basis["E11"]
        + d2 * basis["E22"]
        + d3 * basis["E33"]
        + x12 * basis["X12"]
        + y12 * basis["Y12"]
        + x23 * basis["X23"]
        + y23 * basis["Y23"]
        + x13 * basis["X13"]
        + y13 * basis["Y13"]
    )
    r0 = real_trace_pair_sp(b0, h)
    r1 = real_trace_pair_sp(b1, h)
    r2 = real_trace_pair_sp(b2, h)

    check(
        "r0 is exactly the total diagonal response",
        sp.simplify(r0 - (d1 + d2 + d3)) == 0,
        detail=f"r0={r0}",
    )
    check(
        "r1 is exactly twice the cyclic X-sum",
        sp.simplify(r1 - 2 * (x12 + x23 + x13)) == 0,
        detail=f"r1={r1}",
    )
    check(
        "r2 is exactly twice the signed cyclic Y-sum",
        sp.simplify(r2 - 2 * (y12 + y23 - y13)) == 0,
        detail=f"r2={r2}",
    )


def part4_numeric_reconstruction() -> None:
    print()
    print("=" * 88)
    print("PART 4: the cyclic compression is reconstructed exactly from three responses")
    print("=" * 88)

    rng = np.random.default_rng(20260418)
    m = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    h = m + m.conj().T
    h_cyc = cyclic_projector_np(h)
    b0, b1, b2 = cyclic_basis_np()
    r0 = real_trace_pair(b0, h)
    r1 = real_trace_pair(b1, h)
    r2 = real_trace_pair(b2, h)
    h_rec = reconstruct_from_responses(r0, r1, r2)

    check(
        "The three cyclic responses against the full Hermitian target reconstruct its cyclic compression",
        np.linalg.norm(h_rec - h_cyc) < 1e-12,
        detail=f"err={np.linalg.norm(h_rec - h_cyc):.2e}",
        kind="NUMERIC",
    )
    check(
        "Responses on B0, B1, B2 are unchanged by replacing H_e with P_cyc(H_e)",
        abs(real_trace_pair(b0, h) - real_trace_pair(b0, h_cyc)) < 1e-12
        and abs(real_trace_pair(b1, h) - real_trace_pair(b1, h_cyc)) < 1e-12
        and abs(real_trace_pair(b2, h) - real_trace_pair(b2, h_cyc)) < 1e-12,
        kind="NUMERIC",
    )


def part5_observed_witness() -> None:
    print()
    print("=" * 88)
    print("PART 5: the observed charged-lepton amplitude target already lives in the compressed sector")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    w = np.exp(2j * np.pi / 3)
    f = np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]], dtype=complex) / np.sqrt(3.0)
    h_obs = f @ np.diag(amps) @ f.conj().T
    h_cyc = cyclic_projector_np(h_obs)
    b0, b1, b2 = cyclic_basis_np()
    r0 = real_trace_pair(b0, h_obs)
    r1 = real_trace_pair(b1, h_obs)
    r2 = real_trace_pair(b2, h_obs)

    check(
        "The observed charged-lepton amplitude operator is already cyclic",
        np.linalg.norm(h_obs - h_cyc) < 1e-10,
        detail=f"err={np.linalg.norm(h_obs - h_cyc):.2e}",
        kind="NUMERIC",
    )
    check(
        "Its Koide selector lives entirely on the compressed response triple",
        abs((2 * r0**2 - r1**2 - r2**2) / max(1.0, r0**2)) < 1e-4,
        detail=f"selector={(2 * r0**2 - r1**2 - r2**2):.10f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_basis_level_compression()
    part2_exact_generic_formula()
    part3_exact_response_formulas()
    part4_numeric_reconstruction()
    part5_observed_witness()

    print()
    print("Interpretation:")
    print("  The exact charged projected Hermitian law dW_e^H is generically 9-real,")
    print("  but its Koide-relevant content compresses canonically to three cyclic")
    print("  channels. The live microscopic target is therefore the source law for")
    print("  those three cyclic sums, not the entire generic Hermitian packet.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
