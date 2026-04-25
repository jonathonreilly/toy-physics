#!/usr/bin/env python3
"""
Koide Q Gaussian/equipartition covariance no-go.

Theorem attempt:
  A retained Gaussian maximum-entropy, covariance-whitening, or equipartition
  principle on the first-live C3 carrier might force equal total singlet and
  doublet block powers, hence K_TL = 0.

Result:
  Negative.  C3 invariance reduces a positive covariance to

      Sigma = x P_plus + y P_perp,

  with block energies E_plus=x and E_perp=2y.  Trace/determinant
  normalization leaves the ratio R=E_perp/E_plus free.  Microdegree Gaussian
  entropy/equipartition selects x=y, i.e. R=2, not the Koide leaf R=1.
  Equal total block powers require a block-label entropy/equipartition weight
  alpha=1 rather than the retained microdimension weight alpha=2.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    return sp.simplify((1 + sp.sympify(r)) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    r = sp.sympify(r)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. C3-invariant Gaussian covariance")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = J / 3
    P_perp = I3 - P_plus
    x, y, n = sp.symbols("x y n", positive=True, real=True)
    sigma = sp.simplify(x * P_plus + y * P_perp)

    record(
        "A.1 P_plus and P_perp are the retained singlet/doublet projectors",
        sp.simplify(P_plus**2 - P_plus) == sp.zeros(3, 3)
        and sp.simplify(P_perp**2 - P_perp) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3)
        and P_plus.rank() == 1
        and P_perp.rank() == 2,
        f"ranks=({P_plus.rank()},{P_perp.rank()})",
    )
    record(
        "A.2 Sigma=xP_plus+yP_perp is C3-invariant with one free anisotropy",
        sp.simplify(C * sigma - sigma * C) == sp.zeros(3, 3)
        and sigma.has(x)
        and sigma.has(y),
        f"Sigma={sigma}",
    )

    section("B. Block energies and Koide scalar")

    e_plus = sp.simplify(sp.trace(P_plus * sigma))
    e_perp = sp.simplify(sp.trace(P_perp * sigma))
    ratio = sp.simplify(e_perp / e_plus)
    record(
        "B.1 block energies are E_plus=x and E_perp=2y",
        e_plus == x and e_perp == 2 * y and ratio == 2 * y / x,
        f"E_plus={e_plus}, E_perp={e_perp}, R={ratio}",
    )
    record(
        "B.2 source neutrality is the special anisotropy x=2y",
        sp.solve(sp.Eq(ratio, 1), x) == [2 * y]
        and ktl_from_ratio(ratio).subs(x, 2 * y) == 0,
        f"Q(R)={q_from_ratio(ratio)}, K_TL(R)={ktl_from_ratio(ratio)}",
    )

    section("C. Normalization does not select the anisotropy")

    trace_condition = sp.Eq(sp.trace(sigma), n)
    trace_solutions = sp.solve(trace_condition, x)
    det_sigma = sp.simplify(sigma.det())
    record(
        "C.1 trace normalization leaves y, hence R, free",
        trace_solutions == [n - 2 * y],
        f"trace(Sigma)=x+2y=n -> x={trace_solutions}",
    )
    record(
        "C.2 determinant normalization leaves a one-parameter positive family",
        det_sigma == x * y**2,
        f"det(Sigma)={det_sigma}; det=const fixes x as const/y^2, not y",
    )

    sample_lines = []
    sample_values = []
    for label, substitutions in {
        "rank_equipartition": {x: 1, y: 1},
        "source_neutral": {x: 2, y: 1},
        "doublet_cold": {x: 4, y: 1},
    }.items():
        r_value = sp.simplify(ratio.subs(substitutions))
        sample_values.append(r_value)
        sample_lines.append(
            f"{label}: x={substitutions[x]}, y={substitutions[y]}, "
            f"R={r_value}, Q={q_from_ratio(r_value)}, K_TL={ktl_from_ratio(r_value)}"
        )
    record(
        "C.3 retained C3-positive covariance family realizes off-Koide values",
        sample_values == [2, 1, sp.Rational(1, 2)],
        "\n".join(sample_lines),
    )

    section("D. Entropy/equipartition selects microdegree weights, not Koide")

    # Gaussian entropy is log det Sigma up to constants.  With trace budget
    # x+2y=n, the stationary equations select x=y.
    entropy = sp.log(x) + 2 * sp.log(y)
    lam = sp.symbols("lam", real=True)
    lagrangian = entropy - lam * (x + 2 * y - n)
    stat_x = sp.Eq(sp.diff(lagrangian, x), 0)
    stat_y = sp.Eq(sp.diff(lagrangian, y), 0)
    micro_solution = sp.solve([stat_x, stat_y, trace_condition], [x, y, lam], dict=True)
    record(
        "D.1 microdegree Gaussian maximum entropy gives x=y=n/3",
        micro_solution == [{x: n / 3, y: n / 3, lam: 3 / n}],
        f"stationary solution={micro_solution}",
    )
    micro_ratio = sp.simplify(ratio.subs({x: n / 3, y: n / 3}))
    record(
        "D.2 microdegree equipartition is off the Koide/source-neutral leaf",
        micro_ratio == 2
        and q_from_ratio(micro_ratio) == 1
        and ktl_from_ratio(micro_ratio) == sp.Rational(3, 8),
        f"R={micro_ratio}, Q={q_from_ratio(micro_ratio)}, K_TL={ktl_from_ratio(micro_ratio)}",
    )

    alpha = sp.symbols("alpha", positive=True, real=True)
    e_plus_sym, e_perp_sym, total = sp.symbols(
        "e_plus_sym e_perp_sym total", positive=True, real=True
    )
    block_entropy = sp.log(e_plus_sym) + alpha * sp.log(e_perp_sym)
    block_lagrangian = block_entropy - lam * (e_plus_sym + e_perp_sym - total)
    block_solution = sp.solve(
        [
            sp.Eq(sp.diff(block_lagrangian, e_plus_sym), 0),
            sp.Eq(sp.diff(block_lagrangian, e_perp_sym), 0),
            sp.Eq(e_plus_sym + e_perp_sym, total),
        ],
        [e_plus_sym, e_perp_sym, lam],
        dict=True,
    )
    block_ratio = sp.simplify(block_solution[0][e_perp_sym] / block_solution[0][e_plus_sym])
    record(
        "D.3 weighted block entropy selects the supplied block weight alpha",
        block_ratio == alpha,
        f"E_perp/E_plus={block_ratio}; alpha=1 is equal blocks, alpha=2 is microdimension.",
    )

    section("E. Verdict")

    record(
        "E.1 Gaussian/equipartition structure does not derive K_TL=0",
        True,
        "Standard covariance entropy counts microdegrees and selects R=2; equal block totals require alpha=1.",
    )
    record(
        "E.2 Q remains open after Gaussian covariance audit",
        True,
        "Residual primitive: a retained law choosing block-label equipartition alpha=1 over microdegree alpha=2.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: Gaussian/equipartition covariance route does not close Q.")
        print("KOIDE_Q_GAUSSIAN_EQUIPARTITION_NO_GO=TRUE")
        print("Q_GAUSSIAN_EQUIPARTITION_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=block_entropy_weight_alpha_minus_1_equiv_K_TL")
        print("RESIDUAL_WEIGHT=block_entropy_weight_alpha_minus_1_equiv_K_TL")
        return 0

    print("VERDICT: Gaussian/equipartition covariance audit has FAILs.")
    print("KOIDE_Q_GAUSSIAN_EQUIPARTITION_NO_GO=FALSE")
    print("Q_GAUSSIAN_EQUIPARTITION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=block_entropy_weight_alpha_minus_1_equiv_K_TL")
    print("RESIDUAL_WEIGHT=block_entropy_weight_alpha_minus_1_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
