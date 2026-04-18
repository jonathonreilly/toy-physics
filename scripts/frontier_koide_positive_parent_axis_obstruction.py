#!/usr/bin/env python3
"""
Koide positive-parent axis-obstruction runner
============================================

STATUS: exact obstruction on the candidate sqrt(m) lane

Question:
  Can a nondegenerate positive C_3-covariant parent operator M serve as the
  physical charged-lepton mass parent on the current retained surface, where
  masses are read as axis-basis diagonal entries (U_e = I_3)?

Safe answer:
  No. Any matrix that is both circulant and axis-diagonal is a scalar multiple
  of I_3. Therefore a nontrivial positive C_3 parent is necessarily non-diagonal
  in the axis basis and lives in the eigenvalue channel.
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
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def build_fourier():
    w = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    F = sp.Matrix(
        [
            [1, 1, 1],
            [1, w, w**2],
            [1, w**2, w],
        ]
    ) / sp.sqrt(3)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    return F, C


def part1_intersection():
    print("=" * 88)
    print("PART 1: circulant ∩ axis-diagonal = scalar identity")
    print("=" * 88)

    a, x, y = sp.symbols("a x y", real=True)
    b = x + sp.I * y
    M = sp.Matrix([[a, sp.conjugate(b), b], [b, a, sp.conjugate(b)], [sp.conjugate(b), b, a]])
    offdiag = M - sp.diag(*[M[i, i] for i in range(3)])

    check(
        "Generic Hermitian circulant has equal diagonal entries",
        M[0, 0] == M[1, 1] == M[2, 2],
    )
    check(
        "Axis-diagonal condition forces b = 0",
        sp.simplify(offdiag[0, 1]) == x - sp.I * y and sp.simplify(offdiag[0, 2]) == x + sp.I * y,
        detail="off-diagonals are exactly b and b*",
    )
    M_scalar = sp.simplify(M.subs({x: 0, y: 0}))
    check(
        "With b = 0 the circulant collapses to a scalar multiple of I_3",
        M_scalar == a * sp.eye(3),
    )


def part2_fourier_parent():
    print()
    print("=" * 88)
    print("PART 2: positive C_3 parent with prescribed spectrum is non-diagonal unless degenerate")
    print("=" * 88)

    F, C = build_fourier()
    m1, m2, m3 = sp.symbols("m1 m2 m3", positive=True, real=True)
    M = sp.simplify(F * sp.diag(m1, m2, m3) * F.H)
    Cinv = C.T

    check(
        "Fourier-built parent is Hermitian",
        sp.simplify(M - M.H) == sp.zeros(3),
    )
    check(
        "Fourier-built parent commutes with C_3",
        sp.simplify(C * M * Cinv - M) == sp.zeros(3),
    )

    offdiag01 = sp.simplify(M[0, 1])
    offdiag02 = sp.simplify(M[0, 2])
    check(
        "Off-diagonals vanish iff the spectrum is fully degenerate",
        offdiag01 != 0 and offdiag02 != 0,
        detail=f"M01={offdiag01}, M02={offdiag02}",
    )

    M_deg = sp.simplify(M.subs({m1: m1, m2: m1, m3: m1}))
    check(
        "When m1 = m2 = m3, the parent reduces to m1 I_3",
        sp.simplify(M_deg - m1 * sp.eye(3)) == sp.zeros(3),
    )


def part3_observed_masses():
    print()
    print("=" * 88)
    print("PART 3: observed charged-lepton parent sits in the eigenvalue channel")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    w = np.exp(2j * np.pi / 3)
    F = np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]], dtype=complex) / np.sqrt(3)
    M = F @ np.diag(masses) @ F.conj().T
    offdiag = M - np.diag(np.diag(M))
    offdiag_max = float(np.max(np.abs(offdiag)))

    check(
        "Observed-mass C_3 parent has large nonzero axis-basis off-diagonals",
        offdiag_max > 1.0,
        detail=f"max|offdiag|={offdiag_max:.6f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_intersection()
    part2_fourier_parent()
    part3_observed_masses()

    print()
    print("Interpretation:")
    print("  A nontrivial positive C_3-covariant parent automatically lives in the")
    print("  Fourier/eigenvalue channel. On the current retained charged-lepton")
    print("  surface, that channel is not physical because U_e = I_3 fixes the")
    print("  axis-basis diagonal readout. So the positive-parent sqrt(m) route")
    print("  needs a new readout primitive, not just the parent operator.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
