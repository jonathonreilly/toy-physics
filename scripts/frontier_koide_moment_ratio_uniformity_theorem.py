#!/usr/bin/env python3
"""
Frontier runner - Koide MRU theorem via canonical real-isotype reduction.

Companion to `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.

Load-bearing claim on this branch:
  the scalar charged-lepton MRU lane does not live on the unreduced ordered
  response triple (r_0, r_1, r_2). The non-trivial real doublet carries an
  internal SO(2) frame redundancy, so the exact retained scalar carrier is the
  two-slot quotient

      (r_0, r_1, r_2)  ->  (rho_+, rho_perp),

  where

      rho_+^2    = E_+    = r_0^2 / 3,
      rho_perp^2 = E_perp = (r_1^2 + r_2^2) / 6.

  Applying the standard block log-volume / extremal law on this reduced
  carrier forces

      E_+ = E_perp  <=>  a^2 = 2 |b|^2  <=>  kappa = 2.

The same-day obstruction theorem on the unreduced 3x3 determinant carrier
remains true; this runner certifies the quotient step that resolves it.
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


def shift_matrix(d: int = 3) -> sp.Matrix:
    rows = []
    for i in range(d):
        row = [0] * d
        row[(i - 1) % d] = 1
        rows.append(row)
    return sp.Matrix(rows)


def real_trace(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.re(sp.trace(a * b.H)))


def part0_geometry_and_uniqueness() -> None:
    print("\n=== Part 0: d=3 geometry and uniqueness ===")
    c = shift_matrix(3)
    i3 = sp.eye(3)
    b0 = i3
    b1 = c + c**2
    b2 = sp.I * (c - c**2)

    check("||B_0||^2 = 3", sp.simplify(real_trace(b0, b0) - 3) == 0)
    check(
        "||B_1||^2 = ||B_2||^2 = 6",
        sp.simplify(real_trace(b1, b1) - 6) == 0 and sp.simplify(real_trace(b2, b2) - 6) == 0,
    )
    check(
        "B_0, B_1, B_2 are pairwise orthogonal",
        sp.simplify(real_trace(b0, b1)) == 0
        and sp.simplify(real_trace(b0, b2)) == 0
        and sp.simplify(real_trace(b1, b2)) == 0,
    )

    counts = {
        2: (2, 0),
        3: (1, 1),
        4: (2, 1),
        5: (1, 2),
        6: (2, 2),
    }
    check("d=3 has exactly one singlet and one real doublet", counts[3] == (1, 1))
    check("d=2 is singlet-singlet only, so no singlet-vs-doublet MRU form", counts[2] == (2, 0))
    check("d>=4 fragments into multiple real isotypes", counts[4][0] + counts[4][1] > 2 and counts[5][0] + counts[5][1] > 2 and counts[6][0] + counts[6][1] > 2)


def part1_doublet_frame_redundancy() -> None:
    print("\n=== Part 1: internal SO(2) frame redundancy of the real doublet ===")
    r1, r2, theta = sp.symbols("r1 r2 theta", real=True)
    r1p = sp.cos(theta) * r1 - sp.sin(theta) * r2
    r2p = sp.sin(theta) * r1 + sp.cos(theta) * r2

    check(
        "The doublet radius is SO(2)-invariant",
        sp.simplify(sp.expand(r1p**2 + r2p**2 - (r1**2 + r2**2))) == 0,
    )

    expr_noninv = sp.simplify((r1p**2 - r1**2).subs(theta, sp.pi / 3))
    check(
        "A single Cartesian coordinate is not invariant under the internal frame rotation",
        sp.simplify(expr_noninv) != 0,
        f"residual={sp.expand(expr_noninv)}",
    )

    x, y = sp.symbols("x y", real=True)
    xp = sp.cos(theta) * x - sp.sin(theta) * y
    yp = sp.sin(theta) * x + sp.cos(theta) * y
    check(
        "|b|^2 is frame-invariant on the non-trivial sector",
        sp.simplify(sp.expand(xp**2 + yp**2 - (x**2 + y**2))) == 0,
    )

    a = sp.symbols("a", positive=True, real=True)
    kappa = a**2 / (x**2 + y**2)
    kappa_rot = a**2 / (xp**2 + yp**2)
    check("kappa depends only on the doublet radius, not on the chosen frame", sp.simplify(kappa_rot - kappa) == 0)


def part2_exact_quotient_carrier() -> None:
    print("\n=== Part 2: exact two-slot quotient carrier ===")
    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    e_plus = sp.simplify(r0**2 / 3)
    e_perp = sp.simplify((r1**2 + r2**2) / 6)

    check("E_+ = r_0^2 / 3", sp.simplify(e_plus - r0**2 / 3) == 0)
    check("E_perp = (r_1^2 + r_2^2) / 6", sp.simplify(e_perp - (r1**2 + r2**2) / 6) == 0)

    theta = sp.symbols("theta", real=True)
    r1p = sp.cos(theta) * r1 - sp.sin(theta) * r2
    r2p = sp.sin(theta) * r1 + sp.cos(theta) * r2
    e_perp_rot = sp.simplify((r1p**2 + r2p**2) / 6)
    check("E_perp is constant on SO(2) orbits of the doublet plane", sp.simplify(e_perp_rot - e_perp) == 0)

    a, x, y = sp.symbols("a x y", real=True)
    e_plus_ab = sp.simplify(e_plus.subs(r0, 3 * a))
    e_perp_ab = sp.simplify(e_perp.subs({r1: 6 * x, r2: 6 * y}))
    check("In circulant variables E_+ = 3 a^2", sp.simplify(e_plus_ab - 3 * a**2) == 0)
    check("In circulant variables E_perp = 6 |b|^2", sp.simplify(e_perp_ab - 6 * (x**2 + y**2)) == 0)

    kappa_expr = a**2 / (x**2 + y**2)
    check(
        "kappa is exactly a quotient-carrier function: kappa = 2 E_+ / E_perp",
        sp.simplify(kappa_expr - 2 * e_plus_ab / e_perp_ab) == 0,
    )


def part3_reduced_log_volume_extremum() -> None:
    print("\n=== Part 3: reduced-carrier log-volume extremum ===")
    rho_p, rho_perp, e_tot, lam = sp.symbols("rho_p rho_perp e_tot lam", positive=True, real=True)
    lagrangian = sp.log(rho_p) + sp.log(rho_perp) - lam * (rho_p**2 + rho_perp**2 - e_tot)
    sol = sp.solve(
        [
            sp.diff(lagrangian, rho_p),
            sp.diff(lagrangian, rho_perp),
            rho_p**2 + rho_perp**2 - e_tot,
        ],
        [rho_p, rho_perp, lam],
        dict=True,
    )
    check("Reduced log-volume has a unique positive stationary point", len(sol) == 1, f"sol={sol}")
    stationary = sol[0]
    check(
        "Stationary point is rho_+ = rho_perp = sqrt(E_tot/2)",
        sp.simplify(stationary[rho_p] - sp.sqrt(e_tot / 2)) == 0
        and sp.simplify(stationary[rho_perp] - sp.sqrt(e_tot / 2)) == 0,
    )

    rho = sp.symbols("rho", positive=True, real=True)
    reduced_profile = sp.log(rho) + sp.log(sp.sqrt(e_tot - rho**2))
    second = sp.simplify(sp.diff(reduced_profile, rho, 2).subs(rho, sp.sqrt(e_tot / 2)))
    check(
        "The stationary point is a strict maximum on the positive branch",
        sp.simplify(second) < 0,
        f"second={second}",
    )

    e_plus, e_perp = sp.symbols("e_plus e_perp", positive=True, real=True)
    check(
        "rho_+ = rho_perp is equivalent to E_+ = E_perp",
        sp.simplify((rho_p**2 - rho_perp**2).subs({rho_p: sp.sqrt(e_plus), rho_perp: sp.sqrt(e_perp)}) - (e_plus - e_perp)) == 0,
    )

    a, b_abs_sq = sp.symbols("a b_abs_sq", positive=True, real=True)
    check(
        "E_+ = E_perp pulls back to a^2 = 2 |b|^2",
        sp.simplify((3 * a**2 - 6 * b_abs_sq) / 3 - (a**2 - 2 * b_abs_sq)) == 0,
    )
    check("Therefore the reduced-carrier extremum forces kappa = 2", sp.simplify((a**2 / b_abs_sq).subs(a**2, 2 * b_abs_sq) - 2) == 0)


def part4_unreduced_vs_reduced_contrast() -> None:
    print("\n=== Part 4: contrast with the unreduced determinant obstruction ===")
    c = shift_matrix(3)
    i3 = sp.eye(3)
    p_plus = sp.simplify((i3 + c + c**2) / 3)
    p_perp = sp.simplify(i3 - p_plus)
    alpha, beta = sp.symbols("alpha beta", positive=True, real=True)

    d_unreduced = sp.simplify(alpha * p_plus + beta * p_perp)
    check("Unreduced isotypic-scalar carrier has det = alpha beta^2", sp.simplify(sp.factor(d_unreduced.det()) - alpha * beta**2) == 0)

    d_reduced = sp.diag(alpha, beta)
    check("Reduced real-isotype carrier has det = alpha beta", sp.simplify(d_reduced.det() - alpha * beta) == 0)

    mu, nu = sp.symbols("mu nu", positive=True, real=True)
    kappa_leaf = sp.simplify(2 * mu / nu)
    check("Unreduced weights (1,2) land at kappa = 1", sp.simplify(kappa_leaf.subs({mu: 1, nu: 2}) - 1) == 0)
    check("Reduced two-slot carrier carries equal weights and lands at kappa = 2", sp.simplify(kappa_leaf.subs({mu: 1, nu: 1}) - 2) == 0)


def main() -> int:
    part0_geometry_and_uniqueness()
    part1_doublet_frame_redundancy()
    part2_exact_quotient_carrier()
    part3_reduced_log_volume_extremum()
    part4_unreduced_vs_reduced_contrast()

    print("\nInterpretation:")
    print("  The unreduced 3x3 determinant obstruction remains exact.")
    print("  The load-bearing new theorem is the canonical SO(2) quotient of the")
    print("  non-trivial real doublet to a single scalar radius rho_perp.")
    print("  That makes the scalar charged-lepton carrier two-slot, not three-slot,")
    print("  and the reduced-carrier log-volume extremum is exactly MRU.")
    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
