#!/usr/bin/env python3
"""Moduli-only 3x3 unitarity/Jarlskog area certificate audit.

Verifies the theorem note:
  docs/CKM_MODULI_ONLY_UNITARITY_JARLSKOG_AREA_CERTIFICATE_THEOREM_NOTE_2026-04-26.md

The audit checks:
  - exact Fourier-unitary row/column Heron certificates and Jarlskog magnitude;
  - Heron side-square area identity;
  - symbolic third-row modulus recovery in the constructive 3x3 converse;
  - a nondegenerate numeric bistochastic lift from one closing row triangle;
  - status/scope boundaries from the note itself.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0
REPO_ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def heron_radicand(side_squares):
    x1, x2, x3 = side_squares
    return 2 * (x1 * x2 + x2 * x3 + x3 * x1) - (x1**2 + x2**2 + x3**2)


def row_certificate(B: np.ndarray, a: int, b: int) -> float:
    return heron_radicand([B[a, i] * B[b, i] for i in range(3)])


def col_certificate(B: np.ndarray, i: int, j: int) -> float:
    return heron_radicand([B[a, i] * B[a, j] for a in range(3)])


def jarlskog(V: np.ndarray, a: int = 0, b: int = 1, i: int = 0, j: int = 1) -> float:
    return float(np.imag(V[a, i] * V[b, j] * np.conjugate(V[a, j]) * np.conjugate(V[b, i])))


def audit_note_status() -> None:
    banner("Status and scope extraction")

    rel = "docs/CKM_MODULI_ONLY_UNITARITY_JARLSKOG_AREA_CERTIFICATE_THEOREM_NOTE_2026-04-26.md"
    text = (REPO_ROOT / rel).read_text()
    status_match = re.search(r"\*\*Status:\*\*\s*(.+?)(?:\n\n|$)", text, re.DOTALL)
    status = " ".join(status_match.group(1).split()) if status_match else ""

    print(f"  Status (extracted): {status!r}")
    check("note is scoped as standalone positive CKM theorem", "standalone positive ckm theorem" in status.lower())
    check("note explicitly avoids retained-lane promotion", "does not modify, promote, or close" in status.lower())
    check("note declares no new numerical CKM prediction", "any new numerical ckm prediction" in text.lower())


def audit_exact_fourier_unitary() -> None:
    banner("Exact Fourier-unitary certificate")

    sqrt3 = sp.sqrt(3)
    omega = -sp.Rational(1, 2) + sp.I * sqrt3 / 2
    V = sp.Matrix(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ]
    ) / sqrt3
    B = sp.Matrix([[sp.simplify(abs(V[r, c]) ** 2) for c in range(3)] for r in range(3)])

    expected_B = sp.Matrix([[sp.Rational(1, 3)] * 3] * 3)
    check("Fourier squared-moduli table is exactly flat bistochastic", B == expected_B)

    row_rads = []
    col_rads = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        row_rads.append(sp.simplify(heron_radicand([B[a, i] * B[b, i] for i in range(3)])))
    for i, j in ((0, 1), (0, 2), (1, 2)):
        col_rads.append(sp.simplify(heron_radicand([B[a, i] * B[a, j] for a in range(3)])))

    J = sp.im(V[0, 0] * V[1, 1] * sp.conjugate(V[0, 1]) * sp.conjugate(V[1, 0]))
    expected = sp.simplify(4 * J**2)
    print(f"  row certificates: {row_rads}")
    print(f"  col certificates: {col_rads}")
    print(f"  4J^2: {expected}")

    check("all six Heron certificates equal 4J^2 exactly",
          all(sp.simplify(r - expected) == 0 for r in row_rads + col_rads))
    check("Fourier area equals |J|/2 exactly",
          sp.simplify(sp.sqrt(row_rads[0]) / 4 - abs(J) / 2) == 0)


def audit_heron_identity() -> None:
    banner("Heron side-square identity")

    a, b, c = sp.symbols("a b c", positive=True)
    s = (a + b + c) / 2
    heron_area_sq = sp.expand(s * (s - a) * (s - b) * (s - c))
    side_square_form = sp.expand(
        (2 * (a**2 * b**2 + b**2 * c**2 + c**2 * a**2) - (a**4 + b**4 + c**4)) / 16
    )
    diff = sp.factor(heron_area_sq - side_square_form)
    print(f"  Heron difference: {diff}")
    check("16 Area^2 side-square formula is symbolic identity", diff == 0)


def audit_constructive_converse_symbolic() -> None:
    banner("Symbolic constructive converse: third-row moduli")

    a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2")
    a3 = 1 - a1 - a2
    b3 = 1 - b1 - b2
    c1 = 1 - a1 - b1
    c2 = 1 - a2 - b2
    c3 = 1 - a3 - b3

    # From the closing side triangle, for component 1:
    # a1*b1 = a2*b2 + a3*b3 + 2 sqrt(a2*b2*a3*b3) cos(theta3-theta2).
    # Substitute that relation into |t1|^2.
    t1_sq = sp.expand(a2 * b3 + a3 * b2 - (a1 * b1 - a2 * b2 - a3 * b3))
    t2_sq = sp.expand(a1 * b3 + a3 * b1 - (a2 * b2 - a1 * b1 - a3 * b3))
    t3_sq = sp.expand(a1 * b2 + a2 * b1 - (a3 * b3 - a1 * b1 - a2 * b2))

    print(f"  |t1|^2 - c1 = {sp.factor(t1_sq - c1)}")
    print(f"  |t2|^2 - c2 = {sp.factor(t2_sq - c2)}")
    print(f"  |t3|^2 - c3 = {sp.factor(t3_sq - c3)}")

    check("constructed row component 1 has target modulus", sp.factor(t1_sq - c1) == 0)
    check("constructed row component 2 has target modulus", sp.factor(t2_sq - c2) == 0)
    check("constructed row component 3 has target modulus", sp.factor(t3_sq - c3) == 0)


def build_numeric_lift(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    lengths = np.sqrt(a * b)
    l1, l2, l3 = lengths
    # Place side 1 on the real axis and solve for a closed triangle.
    cos_phi = (l3**2 - l1**2 - l2**2) / (2 * l1 * l2)
    cos_phi = max(-1.0, min(1.0, float(cos_phi)))
    phi = math.acos(cos_phi)
    z1 = l1
    z2 = l2 * np.exp(1j * phi)
    z3 = -(z1 + z2)
    z = np.array([z1, z2, z3], dtype=complex)
    # z_i = sqrt(a_i b_i) exp(-i theta_i), so theta_i = -arg(z_i).
    theta = -np.angle(z)

    r = np.sqrt(a).astype(complex)
    s = np.sqrt(b).astype(complex) * np.exp(1j * theta)
    t = np.conjugate(np.cross(r, s))
    return np.vstack([r, s, t])


def audit_numeric_constructive_lift() -> None:
    banner("Numeric nondegenerate bistochastic lift")

    a = np.array([0.50, 0.30, 0.20])
    b = np.array([0.30, 0.40, 0.30])
    c = 1.0 - a - b
    B_target = np.vstack([a, b, c])
    V = build_numeric_lift(a, b)
    B_lift = np.abs(V) ** 2
    unit_err = np.max(np.abs(V @ np.conjugate(V.T) - np.eye(3)))
    mod_err = np.max(np.abs(B_lift - B_target))

    row_rads = [row_certificate(B_lift, *pair) for pair in ((0, 1), (0, 2), (1, 2))]
    col_rads = [col_certificate(B_lift, *pair) for pair in ((0, 1), (0, 2), (1, 2))]
    J = jarlskog(V)

    print(f"  max unitarity error: {unit_err:.3e}")
    print(f"  max modulus-table error: {mod_err:.3e}")
    print(f"  row certificates: {[f'{x:.12g}' for x in row_rads]}")
    print(f"  col certificates: {[f'{x:.12g}' for x in col_rads]}")
    print(f"  4J^2: {4 * J * J:.12g}")

    check("constructed lift is unitary", unit_err < 1e-12)
    check("constructed lift has requested squared moduli", mod_err < 1e-12)
    check("all six certificates match 4J^2 numerically",
          max(abs(x - 4 * J * J) for x in row_rads + col_rads) < 1e-12)
    check("positive radicand gives CP-violating interior", min(row_rads + col_rads) > 0.0)


def main() -> int:
    print("=" * 88)
    print("CKM moduli-only unitarity/Jarlskog area certificate audit")
    print("=" * 88)

    audit_note_status()
    audit_exact_fourier_unitary()
    audit_heron_identity()
    audit_constructive_converse_symbolic()
    audit_numeric_constructive_lift()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
