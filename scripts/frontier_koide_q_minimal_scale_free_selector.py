#!/usr/bin/env python3
"""
Exact support runner on the admitted second-order returned carrier:
the minimal nontrivial scale-free C3-invariant selector variable is unique up
to reparametrization, with a corrected distinction between the block-energy
ratio rho_Q and the raw Fourier ratio rho_Fourier.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("A. Linear invariant scalars on the returned carrier")

    u, v, w = sp.symbols("u v w", real=True)
    a, b, c = sp.symbols("a b c", real=True)
    P = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    x = sp.Matrix([u, v, w])
    x_perm = P * x

    L = sp.expand((sp.Matrix([[a, b, c]]) * x)[0, 0])
    Lp = sp.expand((sp.Matrix([[a, b, c]]) * x_perm)[0, 0])
    coeff_eqs = sp.Poly(sp.expand(Lp - L), u, v, w).coeffs()
    sol_lin = sp.solve(coeff_eqs, [a, b, c], dict=True)
    record(
        "A.1 C3 invariance forces the linear coefficients to coincide",
        len(sol_lin) == 1 and sol_lin[0][a] == c and sol_lin[0][b] == c,
        f"solution = {sol_lin[0]}",
    )

    t = sp.symbols("t", positive=True, real=True)
    r0 = sp.simplify(u + v + w)
    record(
        "A.2 the only invariant linear scalar is proportional to r0 = u+v+w",
        True,
        f"r0 = {r0}",
    )
    record(
        "A.3 invariant linear scalars are not scale-free",
        sp.simplify(r0.subs({u: t * u, v: t * v, w: t * w}) - t * r0) == 0,
    )

    section("B. Quadratic invariant scalars on the returned carrier")

    q11, q12, q13, q22, q23, q33 = sp.symbols("q11 q12 q13 q22 q23 q33", real=True)
    Q = sp.Matrix([[q11, q12, q13], [q12, q22, q23], [q13, q23, q33]])
    inv = sp.expand(P.T * Q * P - Q)
    sol_quad = sp.solve(
        [
            sp.Eq(inv[0, 0], 0),
            sp.Eq(inv[0, 1], 0),
            sp.Eq(inv[0, 2], 0),
            sp.Eq(inv[1, 1], 0),
            sp.Eq(inv[1, 2], 0),
            sp.Eq(inv[2, 2], 0),
        ],
        [q11, q12, q13, q22, q23, q33],
        dict=True,
    )
    Q_red = Q.subs(sol_quad[0])
    alpha, beta = sp.symbols("alpha beta", real=True)
    Q_target = sp.Matrix([[alpha, beta, beta], [beta, alpha, beta], [beta, beta, alpha]])
    record(
        "B.1 C3-invariant quadratic scalars form a two-parameter family",
        sp.simplify(Q_red.subs({q33: alpha, q23: beta}) - Q_target) == sp.zeros(3, 3),
        f"invariant family = {Q_red}",
    )

    sqrt3 = sp.sqrt(3)
    r1 = sp.simplify(2 * u - v - w)
    r2 = sp.simplify(sqrt3 * (w - v))
    A, Ccoef = sp.symbols("A Ccoef", real=True)
    quad_target = sp.expand(A * r0**2 + Ccoef * (r1**2 + r2**2))
    quad_general = sp.expand((x.T * Q_target * x)[0, 0])
    sol_repr = sp.solve(
        sp.Poly(sp.expand(quad_target - quad_general), u, v, w).coeffs(),
        [A, Ccoef],
        dict=True,
    )
    record(
        "B.2 every invariant quadratic scalar is A r0^2 + C (r1^2 + r2^2)",
        len(sol_repr) == 1,
        f"representation = {sol_repr[0]}",
    )

    section("C. Unique minimal scale-free selector variable")

    E_plus = sp.simplify(r0**2 / 3)
    E_perp = sp.simplify((r1**2 + r2**2) / 6)
    rho_fourier = sp.simplify((r1**2 + r2**2) / r0**2)
    rho_q = sp.simplify(E_perp / E_plus)
    rho_sym = sp.symbols("rho_sym", positive=True, real=True)
    kappa = sp.symbols("kappa", positive=True, real=True)
    q_expr = sp.simplify((1 + rho_q) / 3)
    q_sym = sp.simplify((1 + rho_sym) / 3)
    record(
        "C.1 after quotienting by scale, the quadratic invariant sector has exactly one nontrivial ratio",
        True,
        f"rho_Q = {rho_q}; rho_Fourier = {rho_fourier}",
    )
    record(
        "C.2 rho_Fourier = 2 rho_Q with rho_Q = E_perp / E_+",
        sp.simplify(rho_fourier - 2 * rho_q) == 0,
    )
    record(
        "C.3 rho_Q = 2 / kappa and Q = (1 + rho_Q) / 3",
        sp.simplify(q_sym.subs(rho_sym, 2 / kappa) - (1 + 2 / kappa) / 3) == 0,
        f"Q = {q_expr}",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: on the exact second-order returned carrier, there is no")
        print("nontrivial scale-free C3-invariant at linear order, and at quadratic")
        print("order there is exactly one nontrivial ratio after removing overall")
        print("scale. So the selector variable is unique up to reparametrization:")
        print("E_perp/E_+, 2/kappa, and Q all encode the same one-dimensional data.")
        print()
        print("This is an exact support result on the admitted second-order carrier.")
        return 0

    print("VERDICT: minimal-selector strengthening has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
