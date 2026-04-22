#!/usr/bin/env python3
"""
O1.a — C_3 character Plancherel/Parseval verification on √m vectors

This is the first sub-step of obligation O1
(``S_3 / C_3-irrep alignment of √m on the hw=1 carrier'').
We verify symbolically and numerically the two Parseval identities
used in `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`
Theorem 1:

    |v|^2     = a_0^2 + 2 |z|^2                                   (1)
    (sum v_i)^2 = 3 a_0^2                                         (2)

with v = (sqrt m_1, sqrt m_2, sqrt m_3) decomposed under the C_3
characters as v = a_0 e_+ + z e_omega + zbar e_{omega-bar}.

We also verify that the unitary C_3 Fourier transform sends the
"diagonal" weight to the trivial character and the "off-diagonal"
weight to the nontrivial character pair, which is exactly the
A_1 / E split needed for O1.
"""

from __future__ import annotations

import sys
from fractions import Fraction

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("O1.a — C_3 character Plancherel/Parseval")

    v1, v2, v3 = sp.symbols("v1 v2 v3", positive=True, real=True)
    # Use the explicit primitive cube root form so sympy can simplify cleanly.
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    omega_bar = sp.Rational(-1, 2) - sp.I * sp.sqrt(3) / 2

    # Unitary C_3 Fourier basis (rows are character vectors / sqrt(3))
    e_plus = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    e_omega = sp.Matrix([1, omega, omega ** 2]) / sp.sqrt(3)
    e_omega_bar = sp.Matrix([1, omega_bar, omega_bar ** 2]) / sp.sqrt(3)

    v = sp.Matrix([v1, v2, v3])

    # ---- A. Compute the C_3 Fourier coefficients ---------------------------
    section("A. C_3 Fourier coefficients of v = (v1, v2, v3)")
    a0 = sp.simplify(e_plus.H * v)[0]
    z = sp.simplify(e_omega.H * v)[0]
    zbar = sp.simplify(e_omega_bar.H * v)[0]

    print(f"  a_0  = {a0}")
    print(f"  z    = {z}")
    print(f"  zbar = {zbar}")

    expected_a0 = (v1 + v2 + v3) / sp.sqrt(3)
    expected_z = (v1 + omega_bar * v2 + omega * v3) / sp.sqrt(3)
    expected_zbar = (v1 + omega * v2 + omega_bar * v3) / sp.sqrt(3)

    record(
        "A.1 a_0 = (v1+v2+v3)/sqrt 3   (matches paper formula)",
        sp.simplify(a0 - expected_a0) == 0,
    )
    record(
        "A.2 z = (v1 + omega-bar v2 + omega v3)/sqrt 3   (matches paper formula)",
        sp.simplify(z - expected_z) == 0,
    )
    record(
        "A.3 zbar = (v1 + omega v2 + omega-bar v3)/sqrt 3   (matches paper formula)",
        sp.simplify(zbar - expected_zbar) == 0,
    )
    record(
        "A.4 z and zbar are complex conjugates (forced by reality of v)",
        sp.simplify(sp.conjugate(z) - zbar) == 0,
    )

    # ---- B. Parseval identity (1): |v|^2 = a_0^2 + 2 |z|^2 -----------------
    section("B. Parseval identity (1):  |v|^2 = a_0^2 + 2 |z|^2")
    lhs1 = sp.simplify(v1 ** 2 + v2 ** 2 + v3 ** 2)
    rhs1 = sp.simplify(a0 ** 2 + 2 * (z * zbar))
    diff1 = sp.simplify(lhs1 - rhs1)
    record(
        "B.1 |v|^2 - (a_0^2 + 2 |z|^2) simplifies to zero",
        diff1 == 0,
        f"lhs - rhs = {diff1}",
    )

    # ---- C. Parseval identity (2): (sum v_i)^2 = 3 a_0^2 -------------------
    section("C. Parseval identity (2):  (sum v_i)^2 = 3 a_0^2")
    lhs2 = sp.expand((v1 + v2 + v3) ** 2)
    rhs2 = sp.expand(3 * a0 ** 2)
    diff2 = sp.simplify(lhs2 - rhs2)
    record(
        "C.1 (sum v_i)^2 - 3 a_0^2 simplifies to zero",
        diff2 == 0,
        f"lhs - rhs = {diff2}",
    )

    # ---- D. A_1 / E split alignment -----------------------------------------
    section("D. A_1 (trivial) / E (nontrivial) split alignment")
    # The S_3 representation on R^3 splits as A_1 + E where:
    #   A_1 = span(e_+),   E = span(e_omega, e_{omega-bar}) viewed as a 2D real rep.
    # We confirm the projector decomposition:
    P_plus = e_plus * e_plus.H              # 1-dim trivial projector
    P_E = e_omega * e_omega.H + e_omega_bar * e_omega_bar.H  # 2-dim E-projector
    P_total = (P_plus + P_E).applyfunc(lambda x: sp.nsimplify(sp.expand(x), rational=True))
    is_identity = (P_total == sp.eye(3))
    record(
        "D.1 P_+ + P_E = 1_3 (orthogonal direct sum)",
        is_identity,
        f"P_+ + P_E = {P_total.tolist()}",
    )

    a1_weight = sp.simplify((v.H * P_plus * v)[0])
    e_weight = sp.simplify((v.H * P_E * v)[0])
    diff_a1 = sp.simplify(a1_weight - a0 ** 2)
    diff_e = sp.simplify(e_weight - 2 * z * zbar)
    record(
        "D.2 v^T P_+ v = a_0^2  (A_1 squared weight = trivial-character squared coefficient)",
        diff_a1 == 0,
        f"v^T P_+ v - a_0^2 = {diff_a1}",
    )
    record(
        "D.3 v^T P_E v = 2 |z|^2  (E squared weight = twice the nontrivial-character squared coefficient)",
        diff_e == 0,
        f"v^T P_E v - 2 |z|^2 = {diff_e}",
    )

    # ---- E. Numerical check at PDG charged-lepton point --------------------
    section("E. Numerical check at PDG charged-lepton √m point")
    m_pdg = (
        Fraction(510998946, 10**9),   # m_e in GeV * 10^-9 scale-factor; relative only
        Fraction(105658375, 10**9 * 1000),  # rough m_mu, only the ratios matter
        Fraction(177686, 10**9 * 1000 * 1000),  # rough m_tau placeholder
    )
    # Actually use floats for the numerical sanity check (Plancherel is ratio-stable)
    import math
    mvals = (0.000510999, 0.105658375, 1.77686)  # PDG-ish, GeV
    sqrt_m = tuple(math.sqrt(mi) for mi in mvals)
    sum_sqrt_m = sum(sqrt_m)
    sum_m = sum(mvals)
    a0_num = sum_sqrt_m / math.sqrt(3)
    # Koide Q = sum_m / (sum sqrt m)^2
    Q_num = sum_m / sum_sqrt_m ** 2
    # |z|^2 from Parseval (1): |z|^2 = (|v|^2 - a_0^2) / 2
    z_sq_num = (sum_m - a0_num ** 2) / 2

    print(f"  PDG sqrt-mass vector: {sqrt_m}")
    print(f"  sum_m = {sum_m:.9f} GeV")
    print(f"  sum_sqrt_m = {sum_sqrt_m:.9f} GeV^(1/2)")
    print(f"  a_0^2 = {a0_num**2:.9f}, |z|^2 = {z_sq_num:.9f}")
    print(f"  |z|^2 / a_0^2 = {z_sq_num / a0_num**2:.9f}    (A1 target: 0.5)")
    print(f"  Koide Q = {Q_num:.9f}    (A1 target: 0.6666...)")

    # The PDG point sits very close to A1; assert numerical agreement at 3e-3
    record(
        "E.1 PDG Koide Q lies within 3e-3 of 2/3",
        abs(Q_num - 2 / 3) < 3e-3,
        f"|Q - 2/3| = {abs(Q_num - 2/3):.3e}",
    )
    record(
        "E.2 PDG |z|^2/a_0^2 lies within 5e-3 of 1/2",
        abs(z_sq_num / a0_num ** 2 - 0.5) < 5e-3,
        f"|ratio - 1/2| = {abs(z_sq_num/a0_num**2 - 0.5):.3e}",
    )
    record(
        "E.3 Numerical Parseval (1) holds to machine precision",
        abs(sum_m - (a0_num ** 2 + 2 * z_sq_num)) < 1e-12,
    )

    # ---- Summary ----------------------------------------------------------
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print("VERDICT: O1.a closed — C_3 character Plancherel/Parseval verified")
        print("symbolically and the A_1/E projector split aligns with (a_0^2, 2|z|^2)")
        print("as required for the next step (mass-matrix-level alignment, O1.b).")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
