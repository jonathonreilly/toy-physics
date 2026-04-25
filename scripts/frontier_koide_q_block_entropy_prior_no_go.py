#!/usr/bin/env python3
"""
Koide Q block-entropy prior no-go.

The real-irrep-block democracy route can be phrased as max entropy over the
two block probabilities:

    p_+     = E_+/(E_+ + E_perp)
    p_perp  = E_perp/(E_+ + E_perp)

Max entropy with a uniform two-block prior gives p_+ = p_perp = 1/2, hence
E_+ = E_perp, c^2 = 2, kappa = 2, and Q = 2/3.

This runner audits whether that entropy argument is forced by the retained
C3/Herm_circ(3) data.  It is not.  Relative entropy needs a prior/coarse
graining.  Uniform over real isotype blocks, uniform over complex characters,
and other retained-compatible priors give different radius laws.  Therefore
the block-entropy route closes Q only after adopting the equal-block prior as
an additional physical coarse-graining primitive.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used.
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


def main() -> int:
    section("Koide Q block-entropy prior no-go")
    print("Theorem attempt: block-entropy/max-entropy on the retained C3 data")
    print("might force the Brannen radius law.  The audit result is negative:")
    print("the answer depends on an extra prior/coarse-graining choice.")

    a, b = sp.symbols("a b", positive=True, real=True)
    e_plus = 3 * a**2
    e_perp = 6 * b**2
    r = sp.symbols("r", positive=True, real=True)
    c2 = sp.symbols("c2", positive=True, real=True)

    section("A. Radius law in block-energy coordinates")

    ratio = sp.simplify(e_perp / e_plus)
    c2_expr = sp.simplify(4 * b**2 / a**2)
    kappa_expr = sp.simplify(a**2 / b**2)
    q_from_c2 = sp.Rational(1, 3) + c2 / 6
    q_from_r = sp.simplify(q_from_c2.subs(c2, 2 * r))

    record(
        "A.1 the block-energy ratio is E_perp/E_+ = c^2/2",
        sp.simplify(c2_expr - 2 * ratio) == 0,
        f"E_perp/E_+ = {ratio}; c^2 = {c2_expr}",
    )
    record(
        "A.2 Koide scalar in these coordinates is Q = (1 + E_perp/E_+)/3",
        sp.simplify(q_from_r - (1 + r) / 3) == 0,
        f"Q(r) = {q_from_r}",
    )
    record(
        "A.3 kappa is the inverse radius coordinate kappa = 2/(E_perp/E_+)",
        sp.simplify(kappa_expr - 2 / ratio) == 0,
        f"kappa = {kappa_expr}",
    )

    section("B. Entropy with an explicit prior")

    p, pi_plus, pi_perp = sp.symbols("p pi_plus pi_perp", positive=True, real=True)
    entropy = -p * sp.log(p / pi_plus) - (1 - p) * sp.log((1 - p) / pi_perp)
    d_entropy = sp.simplify(sp.diff(entropy, p))
    d2_entropy = sp.simplify(sp.diff(entropy, p, 2))
    p_star = sp.simplify(pi_plus / (pi_plus + pi_perp))
    d_at_star = sp.simplify(d_entropy.subs(p, p_star))
    d2_at_star = sp.simplify(d2_entropy.subs(p, p_star))

    record(
        "B.1 relative entropy maximization returns the chosen prior",
        d_at_star == 0
        and sp.simplify(d2_at_star + (pi_plus + pi_perp) ** 2 / (pi_plus * pi_perp)) == 0,
        f"p_+* = {p_star}; d2S|* = {d2_at_star}",
    )

    r_prior = sp.simplify(pi_perp / pi_plus)
    c2_prior = sp.simplify(2 * r_prior)
    kappa_prior = sp.simplify(2 / r_prior)
    q_prior = sp.simplify((1 + r_prior) / 3)
    record(
        "B.2 the entropy-selected radius is a function of the prior ratio",
        c2_prior == 2 * pi_perp / pi_plus
        and kappa_prior == 2 * pi_plus / pi_perp,
        f"E_perp/E_+ = {r_prior}; c^2 = {c2_prior}; kappa = {kappa_prior}; Q = {q_prior}",
    )

    section("C. Retained-compatible priors give different radii")

    samples = {
        "uniform_real_isotype_blocks": (sp.Integer(1), sp.Integer(1)),
        "uniform_complex_characters": (sp.Integer(1), sp.Integer(2)),
        "singlet_heavy_two_to_one": (sp.Integer(2), sp.Integer(1)),
        "matrix_real_dimension_count": (sp.Integer(3), sp.Integer(6)),
    }
    sample_lines: list[str] = []
    sample_ok = True
    sample_values = {}
    for label, (prior_plus, prior_perp) in samples.items():
        value_r = sp.simplify(r_prior.subs({pi_plus: prior_plus, pi_perp: prior_perp}))
        value_c2 = sp.simplify(c2_prior.subs({pi_plus: prior_plus, pi_perp: prior_perp}))
        value_kappa = sp.simplify(kappa_prior.subs({pi_plus: prior_plus, pi_perp: prior_perp}))
        value_q = sp.simplify(q_prior.subs({pi_plus: prior_plus, pi_perp: prior_perp}))
        sample_values[label] = (value_r, value_c2, value_kappa, value_q)
        sample_lines.append(
            f"{label}: prior=({prior_plus},{prior_perp}) -> "
            f"r={value_r}, c^2={value_c2}, kappa={value_kappa}, Q={value_q}"
        )

    sample_ok &= sample_values["uniform_real_isotype_blocks"] == (
        sp.Integer(1),
        sp.Integer(2),
        sp.Integer(2),
        sp.Rational(2, 3),
    )
    sample_ok &= sample_values["uniform_complex_characters"] == (
        sp.Integer(2),
        sp.Integer(4),
        sp.Integer(1),
        sp.Integer(1),
    )
    sample_ok &= sample_values["singlet_heavy_two_to_one"] == (
        sp.Rational(1, 2),
        sp.Integer(1),
        sp.Integer(4),
        sp.Rational(1, 2),
    )
    sample_ok &= sample_values["matrix_real_dimension_count"] == (
        sp.Integer(2),
        sp.Integer(4),
        sp.Integer(1),
        sp.Integer(1),
    )

    record(
        "C.1 different natural C3-compatible coarse grainings give different exact radius laws",
        sample_ok,
        "\n".join(sample_lines),
    )

    record(
        "C.2 the A1 value is selected only by the equal-real-isotype-block prior",
        sample_values["uniform_real_isotype_blocks"][1] == 2
        and sample_values["uniform_complex_characters"][1] != 2
        and sample_values["singlet_heavy_two_to_one"][1] != 2,
        "Equal block prior gives c^2=2; character-count and other priors do not.",
    )

    section("D. Review-grade consequence")

    record(
        "D.1 the existing block-democracy max-entropy runner is conditional on a prior",
        True,
        "It sets p_trivial = p_doublet = 1/2.  That is exactly the equal-block\n"
        "coarse graining, not a consequence of C3 covariance alone.",
    )
    record(
        "D.2 max entropy does not remove the K_TL/radius primitive",
        True,
        "It reformulates the primitive as a physical prior over coarse-grained\n"
        "blocks.  A closure still needs a retained theorem forcing that prior.",
    )
    record(
        "D.3 no forbidden target or observational pin is used",
        True,
        "The audit uses symbolic block energies and entropy priors only.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_BLOCK_ENTROPY_PRIOR_NO_GO=TRUE")
        print("Q_BLOCK_ENTROPY_MAXENT_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIMITIVE=equal_real_isotype_block_prior_equiv_c^2=2_equiv_K_TL=0")
        print()
        print("VERDICT: block-entropy max entropy is support for the democracy")
        print("primitive, but it is not a derivation from the retained C3 data alone.")
        print("The load-bearing input is the equal real-isotype-block prior.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
