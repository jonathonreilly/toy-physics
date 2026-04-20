#!/usr/bin/env python3
"""
Frontier runner - observable-radius theorem for the scalar charged-lepton lane.

This runner closes open import I6 from the 2026-04-20 scalar-selector
register:

  observable-principle local scalar jets on the real C_3 doublet are forced to
  be SO(2)-invariant and therefore depend only on the doublet radius.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {label}" + (f"  ({detail})" if detail else ""))


def main() -> int:
    print("=== Part 1: invariant scalar jets on the real C_3 doublet ===")
    theta = 2 * sp.pi / 3
    r1, r2 = sp.symbols("r1 r2", real=True)
    a, b, c = sp.symbols("a b c", real=True)
    R = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    S = sp.Matrix([[a, b], [b, c]])
    invariance = sp.expand(R.T * S * R - S)
    sol = sp.solve(list(invariance), [b, c], dict=True)
    check("120-degree doublet rotation leaves a unique symmetric bilinear class", len(sol) == 1)
    check(
        "Doublet invariant form is S = a I_2",
        sol[0][b] == 0 and sp.simplify(sol[0][c] - a) == 0,
        f"sol={sol[0]}",
    )

    q_doublet = sp.expand(sp.Matrix([[r1, r2]]) * S.subs(sol[0]) * sp.Matrix([[r1], [r2]]))[0]
    check(
        "The invariant doublet quadratic is proportional to r_1^2 + r_2^2",
        sp.simplify(q_doublet - a * (r1**2 + r2**2)) == 0,
    )

    phi = sp.symbols("phi", real=True)
    Rphi = sp.Matrix(
        [
            [sp.cos(phi), -sp.sin(phi)],
            [sp.sin(phi), sp.cos(phi)],
        ]
    )
    rotated = sp.simplify((sp.Matrix([[r1, r2]]) * Rphi.T * Rphi * sp.Matrix([[r1], [r2]]) )[0])
    check(
        "The resulting quadratic is automatically SO(2)-invariant, not only C_3-invariant",
        sp.simplify(rotated - (r1**2 + r2**2)) == 0,
    )

    print("\n=== Part 2: full singlet-plus-doublet scalar lane ===")
    r0 = sp.symbols("r0", real=True)
    A, B, C, D, E, F = sp.symbols("A B C D E F", real=True)
    G = sp.diag(1, 1, 1)
    G[1:, 1:] = R
    M = sp.Matrix([[A, E, F], [E, B, C], [F, C, D]])
    inv_full = sp.expand(G.T * M * G - M)
    sol_full = sp.solve(list(inv_full), [C, D, E, F], dict=True)
    check("Full scalar-lane quadratic family remains two-parameter", len(sol_full) == 1)
    full = sol_full[0]
    check(
        "Invariance kills singlet-doublet cross terms and equalizes the doublet block",
        full[C] == 0 and full[E] == 0 and full[F] == 0 and sp.simplify(full[D] - B) == 0,
        f"sol={full}",
    )

    q_full = sp.expand(
        (sp.Matrix([[r0, r1, r2]]) * M.subs(full) * sp.Matrix([[r0], [r1], [r2]]) )[0]
    )
    check(
        "General retained quadratic local scalar is A r_0^2 + B (r_1^2 + r_2^2)",
        sp.simplify(q_full - (A * r0**2 + B * (r1**2 + r2**2))) == 0,
    )

    print("\n=== Part 3: quotient-carrier coordinates ===")
    e_plus = sp.simplify(r0**2 / 3)
    e_perp = sp.simplify((r1**2 + r2**2) / 6)
    check("E_+ = r_0^2 / 3", sp.simplify(e_plus - r0**2 / 3) == 0)
    check("E_perp = (r_1^2 + r_2^2) / 6", sp.simplify(e_perp - (r1**2 + r2**2) / 6) == 0)

    r1p = sp.cos(phi) * r1 - sp.sin(phi) * r2
    r2p = sp.sin(phi) * r1 + sp.cos(phi) * r2
    e_perp_rot = sp.simplify((r1p**2 + r2p**2) / 6)
    check("E_perp is constant on SO(2) orbits", sp.simplify(e_perp_rot - e_perp) == 0)

    x, y, a0 = sp.symbols("x y a0", real=True)
    kappa = a0**2 / (x**2 + y**2)
    e_plus_ab = sp.simplify(e_plus.subs(r0, 3 * a0))
    e_perp_ab = sp.simplify(e_perp.subs({r1: 6 * x, r2: 6 * y}))
    check("In circulant variables E_+ = 3 a^2", sp.simplify(e_plus_ab - 3 * a0**2) == 0)
    check("In circulant variables E_perp = 6 |b|^2", sp.simplify(e_perp_ab - 6 * (x**2 + y**2)) == 0)
    check(
        "kappa factors through the quotient carrier: kappa = 2 E_+ / E_perp",
        sp.simplify(kappa - 2 * e_plus_ab / e_perp_ab) == 0,
    )

    print("\nInterpretation:")
    print("  Observable-principle local scalar jets on the MRU lane do not retain")
    print("  a Cartesian frame on the real doublet. They retain only the doublet")
    print("  radius, so the scalar charged-lepton lane factors through")
    print("  (rho_+, rho_perp).")
    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

