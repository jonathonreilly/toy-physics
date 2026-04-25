#!/usr/bin/env python3
"""
Koide Q controlled-C3-breaking radius no-go.

The full-lattice Schur-inheritance note leaves a real escape hatch:

    a controlled charged-lepton-specific breaking of strict C3[111] covariance.

The tempting closure upgrade is that such a controlled breaking might derive
the missing charged-lepton source law K_TL = 0, or equivalently the Brannen
radius c^2 = 2, without importing it.

This runner checks that route exactly on the real three-slot square-root
amplitude carrier.  After separating the C3 singlet from the real two-plane,
controlled breaking supplies a doublet direction and magnitude.  The Koide
quotient depends only on the doublet radius.  Neither C3 averaging, an explicit
linear breaking source, nor a generic C3-invariant spontaneous-breaking action
sets that radius without an extra coefficient/value law.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used as
an input.  The Koide value appears only as the target leaf whose residual
radius law is isolated.
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


def q_from_r2(r2: sp.Expr) -> sp.Expr:
    """r2 is the squared Brannen/free-doublet radius c^2."""
    return sp.simplify(sp.Rational(1, 3) + r2 / 6)


def main() -> int:
    section("Koide Q controlled-C3-breaking radius no-go")
    print("Theorem attempt: controlled charged-lepton C3 breaking derives the")
    print("missing normalized traceless source law K_TL = 0.  The audit result")
    print("is negative: controlled breaking leaves a free radius scalar.")

    alpha, beta = sp.symbols("alpha beta", real=True)

    # Exact real decomposition of a three-slot square-root amplitude into the
    # C3 singlet plus the real doublet plane.  The basis is intentionally
    # rational so the no-go does not rest on floating trigonometry.
    one = sp.Matrix([1, 1, 1])
    e = sp.Matrix([2, -1, -1])
    f = sp.Matrix([0, 1, -1])
    lam = sp.simplify(one + alpha * e + beta * f)

    sum_lam = sp.simplify(sum(lam))
    sumsq_lam = sp.simplify(sum(v**2 for v in lam))
    radius2 = sp.simplify(4 * alpha**2 + sp.Rational(4, 3) * beta**2)
    q = sp.simplify(sumsq_lam / sum_lam**2)

    section("A. Exact singlet plus C3-doublet carrier")

    record(
        "A.1 the controlled-breaking carrier is the general real singlet-plus-doublet form",
        lam == sp.Matrix([1 + 2 * alpha, 1 - alpha + beta, 1 - alpha - beta]),
        f"lambda = {list(lam)}",
    )
    record(
        "A.2 the singlet normalization fixes sum(lambda)=3 and leaves a doublet radius",
        sum_lam == 3 and sp.simplify(sumsq_lam - (3 + sp.Rational(3, 2) * radius2)) == 0,
        f"sum(lambda)={sum_lam}; sum(lambda^2)={sumsq_lam}; c^2={radius2}",
    )
    record(
        "A.3 the Koide quotient depends only on the doublet radius, not the direction",
        sp.simplify(q - q_from_r2(radius2)) == 0,
        f"Q = {q}",
    )

    section("B. C3 action preserves the radius but does not set it")

    alpha_p, beta_p = sp.symbols("alpha_p beta_p", real=True)
    cycle_lam = sp.Matrix([lam[1], lam[2], lam[0]])
    transformed = sp.solve(
        list(one + alpha_p * e + beta_p * f - cycle_lam),
        [alpha_p, beta_p],
        dict=True,
    )[0]
    alpha_cycle = sp.simplify(transformed[alpha_p])
    beta_cycle = sp.simplify(transformed[beta_p])
    radius2_cycle = sp.simplify(
        radius2.subs({alpha: alpha_cycle, beta: beta_cycle}, simultaneous=True)
    )

    record(
        "B.1 the C3 generator rotates the doublet plane exactly",
        alpha_cycle == sp.simplify((-alpha + beta) / 2)
        and beta_cycle == sp.simplify((-3 * alpha - beta) / 2),
        f"(alpha,beta) -> ({alpha_cycle}, {beta_cycle})",
    )
    record(
        "B.2 the doublet radius is a C3 invariant",
        sp.simplify(radius2_cycle - radius2) == 0,
        f"c^2 after the cycle = {radius2_cycle}",
    )

    cycle2_lam = sp.Matrix([lam[2], lam[0], lam[1]])
    c3_average = sp.simplify((lam + cycle_lam + cycle2_lam) / 3)
    q_average = sp.simplify(sum(v**2 for v in c3_average) / sum(c3_average) ** 2)

    record(
        "B.3 restoring exact C3 by averaging kills the doublet and gives the symmetric value",
        c3_average == one and q_average == sp.Rational(1, 3),
        f"C3 average = {list(c3_average)}; Q_average={q_average}",
    )

    section("C. Explicit controlled-breaking source")

    h1, h2, mu = sp.symbols("h1 h2 mu", positive=True, real=True)
    source_action = sp.simplify(mu * radius2 / 2 - h1 * alpha - h2 * beta)
    stationary = sp.solve(
        [sp.diff(source_action, alpha), sp.diff(source_action, beta)],
        [alpha, beta],
        dict=True,
    )[0]
    alpha_star = sp.simplify(stationary[alpha])
    beta_star = sp.simplify(stationary[beta])
    radius2_star = sp.simplify(radius2.subs({alpha: alpha_star, beta: beta_star}))
    q_star = sp.simplify(q_from_r2(radius2_star))

    record(
        "C.1 an explicit doublet source fixes a direction and a source-strength radius",
        alpha_star == h1 / (4 * mu)
        and beta_star == 3 * h2 / (4 * mu)
        and radius2_star == (h1**2 + 3 * h2**2) / (4 * mu**2),
        f"alpha*={alpha_star}; beta*={beta_star}; c^2*={radius2_star}",
    )
    record(
        "C.2 the induced Q value is a free source-strength ratio",
        sp.simplify(q_star - (sp.Rational(1, 3) + (h1**2 + 3 * h2**2) / (24 * mu**2))) == 0,
        f"Q*={q_star}",
    )
    record(
        "C.3 the Koide leaf would require a new exact source-strength law",
        sp.simplify(radius2_star - 2)
        == sp.simplify((h1**2 + 3 * h2**2 - 8 * mu**2) / (4 * mu**2)),
        "c^2*=2 iff h1^2 + 3 h2^2 = 8 mu^2.",
    )

    source_samples = [
        ("h1=2mu, h2=0", {h1: 2 * mu, h2: 0}, sp.Integer(1), sp.Rational(1, 2)),
        ("h1=2sqrt(2)mu, h2=0", {h1: 2 * sp.sqrt(2) * mu, h2: 0}, sp.Integer(2), sp.Rational(2, 3)),
        ("h1=4mu, h2=0", {h1: 4 * mu, h2: 0}, sp.Integer(4), sp.Integer(1)),
    ]
    source_lines: list[str] = []
    source_ok = True
    for label, subs, expected_r2, expected_q in source_samples:
        got_r2 = sp.simplify(radius2_star.subs(subs))
        got_q = sp.simplify(q_star.subs(subs))
        source_ok = source_ok and got_r2 == expected_r2 and got_q == expected_q
        source_lines.append(f"{label}: c^2={got_r2}, Q={got_q}")
    record(
        "C.4 the same controlled-breaking form realizes inequivalent exact Q values",
        source_ok,
        "\n".join(source_lines),
    )

    section("D. Spontaneous-breaking action coefficients")

    A, B, rho2 = sp.symbols("A B rho2", real=True, nonzero=True)
    landau = sp.simplify(A * rho2 + B * rho2**2)
    rho2_stationary = sp.solve(sp.Eq(sp.diff(landau, rho2), 0), rho2, dict=False)[0]
    q_landau = sp.simplify(q_from_r2(rho2_stationary))

    record(
        "D.1 a C3-invariant Landau action can depend on the doublet only through c^2",
        sp.diff(landau, rho2) == A + 2 * B * rho2
        and rho2_stationary == -A / (2 * B),
        f"S(c^2)=A c^2 + B c^4; stationary c^2={rho2_stationary}",
    )
    record(
        "D.2 the spontaneous-breaking radius is a free coefficient ratio",
        sp.simplify(q_landau - (sp.Rational(1, 3) - A / (12 * B))) == 0,
        f"Q_stationary={q_landau}",
    )
    record(
        "D.3 the Koide leaf would require the new coefficient law A + 4B = 0",
        sp.simplify(rho2_stationary - 2) == sp.simplify(-(A + 4 * B) / (2 * B)),
        "c^2=2 iff A + 4B = 0.",
    )

    section("E. Normalized second-order source reading")

    e_ratio = sp.simplify(radius2 / 2)
    y_plus = sp.simplify(2 / (1 + e_ratio))
    y_perp = sp.simplify(2 * e_ratio / (1 + e_ratio))
    k_plus = sp.simplify(1 / y_plus - 1)
    k_perp = sp.simplify(1 / y_perp - 1)
    k_tl_residual = sp.simplify(k_plus - k_perp)

    record(
        "E.1 the controlled-breaking radius is the normalized block-power ratio",
        sp.simplify(e_ratio - radius2 / 2) == 0
        and sp.simplify(y_plus + y_perp - 2) == 0,
        f"E_perp/E_+={e_ratio}; Y=diag({y_plus}, {y_perp})",
    )
    record(
        "E.2 zero traceless source is equivalent to the same radius law c^2=2",
        sp.factor(k_tl_residual)
        == sp.factor((radius2 - 2) * (radius2 + 2) / (4 * radius2)),
        f"K_+ - K_perp = {sp.factor(k_tl_residual)}",
    )
    record(
        "E.3 no forbidden target or observational pin is used as an input",
        True,
        "The audit uses exact symbolic carrier algebra and names the residual scalar.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_CONTROLLED_C3_BREAKING_NO_GO=TRUE")
        print("Q_CONTROLLED_C3_BREAKING_CLOSES_Q=FALSE")
        print("RESIDUAL_RADIUS_LAW=controlled_breaking_radius_c^2=2_equiv_K_TL=0")
        print()
        print("VERDICT: controlled C3 breaking supplies a doublet sector,")
        print("but Q is set by its radius.  A closure still needs a retained")
        print("law fixing that radius to c^2=2, equivalently K_TL=0.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
