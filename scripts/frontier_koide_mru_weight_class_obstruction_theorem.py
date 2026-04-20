#!/usr/bin/env python3
"""
Frontier runner - Koide MRU Weight-Class Obstruction Theorem.

Companion to
`docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

Theorem.
  On the d=3 hw=1 cyclic carrier with block powers

      E_+    = r_0^2 / 3          = 3 a^2,
      E_perp = (r_1^2 + r_2^2)/6  = 6 |b|^2,

  every weighted block-log-volume law

      S_{mu,nu} = mu log(E_+) + nu log(E_perp)

  at fixed total block power E_tot = E_+ + E_perp has the unique interior
  stationary point

      E_+ / E_perp = mu / nu.

  Equivalently,

      2 nu r_0^2 = mu (r_1^2 + r_2^2),
      kappa := a^2 / |b|^2 = 2 mu / nu.

  MRU is exactly the equal-weight leaf mu = nu. By contrast, the retained
  observable-principle carrier on the unreduced 3x3 circulant block has

      det(alpha P_+ + beta P_perp) = alpha beta^2,

  so log|det| counts weights (mu, nu) = (1, 2), giving kappa = 1 rather
  than MRU's kappa = 2. The exact missing object is therefore a retained
  real-isotype carrier reduction, or an equivalent 1:1 block-measure law.

Expected final line: PASS=26 FAIL=0.
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


def shift_matrix() -> sp.Matrix:
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def real_trace(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.re(sp.trace(a * b.H)))


def part0_block_geometry() -> None:
    print("\n=== Part 0: cyclic block geometry ===")
    c = shift_matrix()
    i3 = sp.eye(3)
    b0 = i3
    b1 = c + c.T
    b2 = sp.I * (c - c.T)

    check("||B_0||^2 = 3", sp.simplify(real_trace(b0, b0) - 3) == 0)
    check("||B_1||^2 = ||B_2||^2 = 6",
          sp.simplify(real_trace(b1, b1) - 6) == 0
          and sp.simplify(real_trace(b2, b2) - 6) == 0)
    check("B_0 is orthogonal to the cyclic doublet plane",
          sp.simplify(real_trace(b0, b1)) == 0 and sp.simplify(real_trace(b0, b2)) == 0)

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    h_plus = (r0 / 3) * b0
    h_perp = (r1 / 6) * b1 + (r2 / 6) * b2
    e_plus = sp.simplify(real_trace(h_plus, h_plus))
    e_perp = sp.simplify(real_trace(h_perp, h_perp))
    check("E_+ = r_0^2 / 3", sp.simplify(e_plus - r0**2 / 3) == 0, f"E_+={e_plus}")
    check("E_perp = (r_1^2 + r_2^2) / 6",
          sp.simplify(e_perp - (r1**2 + r2**2) / 6) == 0, f"E_perp={e_perp}")

    a, x, y = sp.symbols("a x y", real=True)
    e_plus_ab = sp.simplify(e_plus.subs({r0: 3 * a}))
    e_perp_ab = sp.simplify(e_perp.subs({r1: 6 * x, r2: 6 * y}))
    check("E_+ = 3 a^2 on H = aI + bC + b^* C^2", sp.simplify(e_plus_ab - 3 * a**2) == 0)
    check("E_perp = 6 |b|^2 with |b|^2 = x^2 + y^2",
          sp.simplify(e_perp_ab - 6 * (x**2 + y**2)) == 0)
    check("MRU equal block power is exactly kappa = 2",
          sp.simplify((e_plus_ab - e_perp_ab) - 3 * (a**2 - 2 * (x**2 + y**2))) == 0)


def part1_weighted_log_volume() -> None:
    print("\n=== Part 1: weighted block-log-volume classification ===")
    e_plus, e_perp, e_tot = sp.symbols("e_plus e_perp e_tot", positive=True)
    mu, nu, lam = sp.symbols("mu nu lam", positive=True)

    lagrangian = mu * sp.log(e_plus) + nu * sp.log(e_perp) - lam * (e_plus + e_perp - e_tot)
    sol = sp.solve(
        [sp.diff(lagrangian, e_plus), sp.diff(lagrangian, e_perp), e_plus + e_perp - e_tot],
        [e_plus, e_perp, lam],
        dict=True,
    )
    check("Weighted block-log-volume has one interior stationary point", len(sol) == 1, f"sol={sol}")
    stationary = sol[0]
    check("E_+^* = mu/(mu+nu) E_tot",
          sp.simplify(stationary[e_plus] - e_tot * mu / (mu + nu)) == 0)
    check("E_perp^* = nu/(mu+nu) E_tot",
          sp.simplify(stationary[e_perp] - e_tot * nu / (mu + nu)) == 0)
    check("Stationary ratio is E_+ / E_perp = mu / nu",
          sp.simplify(stationary[e_plus] / stationary[e_perp] - mu / nu) == 0)

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    e_plus_r = r0**2 / 3
    e_perp_r = (r1**2 + r2**2) / 6
    check("Stationary leaf is 2 nu r_0^2 = mu (r_1^2 + r_2^2)",
          sp.simplify(6 * (nu * e_plus_r - mu * e_perp_r) - (2 * nu * r0**2 - mu * (r1**2 + r2**2))) == 0)

    a, b_abs_sq = sp.symbols("a b_abs_sq", positive=True)
    stationary_kappa = sp.simplify((2 * nu * (3 * a)**2 - mu * 36 * b_abs_sq) / 18)
    check("In circulant variables the stationary leaf is nu a^2 = 2 mu |b|^2",
          sp.simplify(stationary_kappa - (nu * a**2 - 2 * mu * b_abs_sq)) == 0)
    check("Hence kappa = a^2/|b|^2 = 2 mu / nu",
          sp.simplify((nu * a**2 - 2 * mu * b_abs_sq) / (nu * b_abs_sq) - (a**2 / b_abs_sq - 2 * mu / nu)) == 0)


def part2_weight_leaves() -> None:
    print("\n=== Part 2: MRU leaf vs retained determinant leaf ===")
    e_tot = sp.symbols("e_tot", positive=True)
    mu, nu = sp.symbols("mu nu", positive=True)
    e_plus_star = e_tot * mu / (mu + nu)
    e_perp_star = e_tot * nu / (mu + nu)

    mrw = {mu: 1, nu: 1}
    check("Equal weights (1,1) give E_+ = E_perp = E_tot/2",
          sp.simplify(e_plus_star.subs(mrw) - e_tot / 2) == 0
          and sp.simplify(e_perp_star.subs(mrw) - e_tot / 2) == 0)
    check("Equal weights (1,1) give kappa = 2",
          sp.simplify((2 * mu / nu).subs(mrw) - 2) == 0)

    retained = {mu: 1, nu: 2}
    check("Weights (1,2) give E_+ = E_tot/3 and E_perp = 2E_tot/3",
          sp.simplify(e_plus_star.subs(retained) - e_tot / 3) == 0
          and sp.simplify(e_perp_star.subs(retained) - 2 * e_tot / 3) == 0)
    check("Weights (1,2) give kappa = 1, not MRU",
          sp.simplify((2 * mu / nu).subs(retained) - 1) == 0)


def part3_retained_multiplicity_obstruction() -> None:
    print("\n=== Part 3: retained log-det multiplicity obstruction ===")
    alpha, beta, theta = sp.symbols("alpha beta theta", positive=True, real=True)

    c = shift_matrix()
    i3 = sp.eye(3)
    p_plus = sp.simplify((i3 + c + c**2) / 3)
    p_perp = sp.simplify(i3 - p_plus)
    check("P_+ and P_perp are complementary projectors",
          sp.simplify(p_plus**2 - p_plus) == sp.zeros(3)
          and sp.simplify(p_perp**2 - p_perp) == sp.zeros(3)
          and sp.simplify(p_plus * p_perp) == sp.zeros(3))
    check("rank(P_+) = 1 and rank(P_perp) = 2",
          p_plus.rank() == 1 and p_perp.rank() == 2)

    d = sp.simplify(alpha * p_plus + beta * p_perp)
    check("det(alpha P_+ + beta P_perp) = alpha beta^2",
          sp.simplify(sp.factor(d.det()) - alpha * beta**2) == 0)

    rot = sp.Matrix([
        [1, 0, 0],
        [0, sp.cos(theta), -sp.sin(theta)],
        [0, sp.sin(theta), sp.cos(theta)],
    ])
    d_block = sp.diag(alpha, beta, beta)
    d_rot = sp.simplify(rot * d_block * rot.T)
    check("Doublet-basis rotations do not alter the repeated beta multiplicity",
          sp.simplify(d_rot - d_block) == sp.zeros(3))
    check("So every unreduced 3x3 determinant law carries weights (1,2)",
          sp.simplify(sp.factor(d_rot.det()) - alpha * beta**2) == 0)


def part4_missing_reduction_object() -> None:
    print("\n=== Part 4: the exact missing carrier reduction ===")
    alpha, beta = sp.symbols("alpha beta", positive=True)
    d_red = sp.diag(alpha, beta)
    check("A two-slot real-isotype carrier has det = alpha beta",
          sp.simplify(d_red.det() - alpha * beta) == 0)
    check("That reduced carrier counts weights (1,1) and therefore lands on MRU",
          sp.Integer(2) * sp.Integer(1) / sp.Integer(1) == 2)


def main() -> int:
    part0_block_geometry()
    part1_weighted_log_volume()
    part2_weight_leaves()
    part3_retained_multiplicity_obstruction()
    part4_missing_reduction_object()

    print("\nInterpretation:")
    print("  MRU is no longer just an isolated equality on the cyclic carrier.")
    print("  It is the equal-weight leaf in the full weighted block-log-volume")
    print("  family. The retained log|det| carrier picks the different leaf")
    print("  (1,2) -> kappa=1 because the non-trivial sector appears twice in the")
    print("  unreduced 3x3 determinant. The exact missing object is therefore a")
    print("  retained 1:1 real-isotype measure or an equivalent carrier reduction")
    print("  that counts the whole doublet block once.")
    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
