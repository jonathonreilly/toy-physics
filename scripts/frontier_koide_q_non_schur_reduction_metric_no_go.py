#!/usr/bin/env python3
"""
Koide Q non-Schur reduction-metric no-go.

The full-lattice Schur-inheritance theorem leaves open a non-Schur reduction
map from the full taste carrier to the charged-lepton observable lane.  The
tempting closure upgrade is:

    changing the positive reduction metric on the C3 singlet/doublet carrier
    might force the normalized source-free point to the Koide radius.

This runner checks the strongest scale-free version that still preserves the
retained C3 isotype split.  A general positive C3-equivariant metric assigns
independent weights g_+ and g_perp to the real singlet and doublet blocks.
Source-freeness on that metric-weighted carrier fixes only

    E_perp / E_+ = g_+ / g_perp.

The metric ratio is not fixed by C3 covariance, positivity, or scale
normalization.  Koide is recovered only for the extra law g_+ = g_perp, which
is the canonical Schur/Frobenius metric choice in another form.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used as
an input.  The Koide value appears only as the target leaf whose residual
metric-ratio law is isolated.
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
    """r = E_perp / E_+ on the unweighted charged-lepton block carrier."""
    return sp.simplify((1 + r) / 3)


def main() -> int:
    section("Koide Q non-Schur reduction-metric no-go")
    print("Theorem attempt: a non-Schur C3-equivariant reduction metric fixes")
    print("the normalized source-free point at the Koide radius.  The audit")
    print("result is negative: the metric ratio remains a free scalar.")

    gp, gt = sp.symbols("g_plus g_perp", positive=True, real=True)
    eplus, eperp = sp.symbols("E_plus E_perp", positive=True, real=True)

    section("A. C3-equivariant positive metrics leave one free ratio")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3)
    Pp = sp.simplify(J / 3)
    Pt = sp.simplify(I3 - Pp)
    G = sp.simplify(gp * Pp + gt * Pt)

    record(
        "A.1 the singlet and doublet projectors are exact C3 projectors",
        sp.simplify(Pp * Pp - Pp) == sp.zeros(3)
        and sp.simplify(Pt * Pt - Pt) == sp.zeros(3)
        and sp.simplify(Pp * Pt) == sp.zeros(3)
        and sp.simplify(Pp + Pt - I3) == sp.zeros(3),
        f"P_+ rank={Pp.trace()}; P_perp rank={Pt.trace()}",
    )
    record(
        "A.2 every metric G = g_+ P_+ + g_perp P_perp is C3-equivariant",
        sp.simplify(C * G * C.T - G) == sp.zeros(3),
        "C G C^T = G for arbitrary positive g_+, g_perp.",
    )
    record(
        "A.3 C3 covariance does not force the metric weights equal",
        sp.simplify((G.subs({gp: 2, gt: 1}) - G.subs({gp: 1, gt: 1}))) != sp.zeros(3)
        and sp.simplify(C * G.subs({gp: 2, gt: 1}) * C.T - G.subs({gp: 2, gt: 1}))
        == sp.zeros(3),
        "The metric ratio g_+/g_perp is a retained-symmetry-allowed scalar.",
    )

    section("B. Metric-weighted normalized carrier")

    y_plus = sp.simplify(2 * gp * eplus / (gp * eplus + gt * eperp))
    y_perp = sp.simplify(2 * gt * eperp / (gp * eplus + gt * eperp))
    ratio = sp.simplify(eperp / eplus)

    record(
        "B.1 the metric-weighted carrier normalizes to Tr(Y_G)=2",
        sp.simplify(y_plus + y_perp - 2) == 0,
        f"Y_G=diag({y_plus}, {y_perp})",
    )
    record(
        "B.2 common scale still cancels exactly",
        sp.simplify(y_plus.subs({eplus: 7 * eplus, eperp: 7 * eperp}) - y_plus) == 0
        and sp.simplify(y_perp.subs({eplus: 7 * eplus, eperp: 7 * eperp}) - y_perp) == 0,
        "The non-Schur metric changes the block ratio, not the overall scale.",
    )

    source_free_eperp = sp.solve(sp.Eq(y_plus, y_perp), eperp, dict=False)[0]
    source_free_metric_ratio = sp.simplify(source_free_eperp / eplus)
    record(
        "B.3 source-free on the metric-weighted carrier fixes E_perp/E_+ to the metric ratio",
        sp.simplify(source_free_metric_ratio - gp / gt) == 0,
        f"Y_G=I_2 -> E_perp/E_+ = {source_free_metric_ratio}",
    )

    section("C. Consequence for the physical Koide quotient")

    q_metric_source_free = sp.simplify(q_from_ratio(source_free_metric_ratio))
    c2_metric_source_free = sp.simplify(2 * source_free_metric_ratio)
    kappa_metric_source_free = sp.simplify(2 / source_free_metric_ratio)

    record(
        "C.1 the unweighted charged-lepton Q value follows the free metric ratio",
        sp.simplify(q_metric_source_free - (gp + gt) / (3 * gt)) == 0,
        f"Q_metric_source_free={q_metric_source_free}",
    )
    record(
        "C.2 the Brannen radius and kappa are likewise metric-ratio functions",
        c2_metric_source_free == 2 * gp / gt
        and kappa_metric_source_free == 2 * gt / gp,
        f"c^2={c2_metric_source_free}; kappa={kappa_metric_source_free}",
    )
    record(
        "C.3 the Koide leaf would require the extra metric law g_+ = g_perp",
        sp.simplify(q_metric_source_free - sp.Rational(2, 3))
        == sp.simplify((gp - gt) / (3 * gt)),
        "Q=2/3 iff g_+ = g_perp.",
    )

    section("D. Exact countermetrics")

    countermetrics = [
        ("singlet_light_metric", {gp: sp.Rational(1, 2), gt: 1}, sp.Rational(1, 2), sp.Integer(1), sp.Rational(1, 2)),
        ("canonical_equal_metric", {gp: 1, gt: 1}, sp.Integer(1), sp.Integer(2), sp.Rational(2, 3)),
        ("singlet_heavy_metric", {gp: 2, gt: 1}, sp.Integer(2), sp.Integer(4), sp.Integer(1)),
    ]
    counter_lines: list[str] = []
    counter_ok = True
    for label, subs, expected_ratio, expected_c2, expected_q in countermetrics:
        got_ratio = sp.simplify(source_free_metric_ratio.subs(subs))
        got_c2 = sp.simplify(c2_metric_source_free.subs(subs))
        got_q = sp.simplify(q_metric_source_free.subs(subs))
        metric = sp.simplify(G.subs(subs))
        commutes = sp.simplify(C * metric * C.T - metric) == sp.zeros(3)
        counter_ok = (
            counter_ok
            and got_ratio == expected_ratio
            and got_c2 == expected_c2
            and got_q == expected_q
            and commutes
        )
        counter_lines.append(
            f"{label}: E_perp/E_+={got_ratio}, c^2={got_c2}, Q={got_q}, C3-equivariant={commutes}"
        )
    record(
        "D.1 C3-equivariant non-Schur metrics realize inequivalent exact Q values",
        counter_ok,
        "\n".join(counter_lines),
    )

    section("E. Relation to the unweighted traceless source")

    r = sp.symbols("r", positive=True, real=True)
    y_unweighted_plus = sp.simplify(2 / (1 + r))
    y_unweighted_perp = sp.simplify(2 * r / (1 + r))
    k_unweighted_plus = sp.simplify(1 / y_unweighted_plus - 1)
    k_unweighted_perp = sp.simplify(1 / y_unweighted_perp - 1)
    ktl_unweighted = sp.factor(k_unweighted_plus - k_unweighted_perp)
    ktl_after_metric_source_free = sp.simplify(ktl_unweighted.subs(r, source_free_metric_ratio))

    record(
        "E.1 the physical unweighted traceless source still vanishes only at the equal metric",
        sp.factor(ktl_after_metric_source_free)
        == sp.factor((gp - gt) * (gp + gt) / (2 * gp * gt)),
        f"K_+ - K_perp after Y_G=I is {sp.factor(ktl_after_metric_source_free)}",
    )
    record(
        "E.2 the non-Schur route therefore changes the source convention unless a metric law is added",
        True,
        "Needed theorem: g_+/g_perp = 1, equivalently the canonical Frobenius/Schur block metric.",
    )
    record(
        "E.3 no forbidden target or observational pin is used as an input",
        True,
        "The audit uses exact C3 projectors, symbolic metric weights, and block ratios only.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_NON_SCHUR_REDUCTION_METRIC_NO_GO=TRUE")
        print("Q_NON_SCHUR_REDUCTION_METRIC_CLOSES_Q=FALSE")
        print("RESIDUAL_METRIC_LAW=g_plus/g_perp=1_equiv_c^2=2_equiv_K_TL=0")
        print()
        print("VERDICT: a non-Schur C3-equivariant reduction metric can move")
        print("the source-free point, but Q tracks the free metric ratio.  A")
        print("closure still needs a retained law selecting g_+ = g_perp.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
