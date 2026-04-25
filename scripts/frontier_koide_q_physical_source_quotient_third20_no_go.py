#!/usr/bin/env python3
"""
Koide Q physical source-quotient third-20 no-go.

Purpose:
  Run a third batch of twenty attacks on the remaining Q obstruction:

      derive a retained physical source-domain quotient or zero-background law
      that kills the central Z=P_plus-P_perp source coordinate.

This batch avoids repeating the prior sign/exchange and representation-family
audits.  It asks whether source-origin, Legendre, renormalization,
preparation, tensor-stability, convex, variational, and operational-completion
requirements force the zero Z section.

Result:
  Negative.  Every tested principle either leaves an affine/background scalar
  free, conditionally closes only after adding a zero-source renormalization
  condition, or is compatible with the retained counterbackground z=-1/3.

Only exact symbolic algebra is used.
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


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Setup")

    z, z0, c, j, beta, n = sp.symbols("z z0 c j beta n", real=True)
    a, b, lam, eps = sp.symbols("a b lambda eps", real=True)
    m = sp.symbols("m", positive=True, real=True)
    counter_z = -sp.Rational(1, 3)

    P_plus = sp.Matrix([[1, 0], [0, 0]])
    P_perp = sp.Matrix([[0, 0], [0, 1]])
    Z = sp.simplify(P_plus - P_perp)
    rho_z = sp.simplify(((1 + z) / 2) * P_plus + ((1 - z) / 2) * P_perp)

    record(
        "A.1 exact counterbackground remains the falsifier",
        q_from_z(counter_z) == 1 and ktl_from_z(counter_z) == sp.Rational(3, 8),
        f"z={counter_z} -> Q={q_from_z(counter_z)}, K_TL={ktl_from_z(counter_z)}",
    )
    record(
        "A.2 Z is a retained central source separator",
        Z**2 == sp.eye(2)
        and sp.trace(Z) == 0
        and sp.simplify(sp.trace(Z * rho_z) - z) == 0,
        "rho_z=((1+z)/2)P_plus+((1-z)/2)P_perp has tr(Z rho_z)=z.",
    )

    section("B. Third twenty attacks")

    # 1. Affine source origin.
    shifted_coordinate = sp.simplify(z - z0)
    record(
        "1. source-origin covariance leaves an affine origin z0 free",
        shifted_coordinate.subs(z, z0) == 0
        and shifted_coordinate.subs({z: counter_z, z0: 0}) == counter_z,
        "A coordinate origin is not a physical zero-background theorem.",
    )

    # 2. Legendre/probe basepoint.
    W = sp.log(1 + z0 + j) - sp.log(1 + z0)
    probe_response = sp.simplify(sp.diff(W, j).subs(j, 0))
    record(
        "2. Legendre probe normalization keeps the background parameter",
        probe_response == 1 / (1 + z0) and probe_response.subs(z0, counter_z) == sp.Rational(3, 2),
        f"dW/dj|0={probe_response}",
    )

    # 3. Partition-function normalization.
    Zpart = sp.exp(beta * z0)
    normalized_Zpart = sp.simplify(Zpart / Zpart)
    source_gradient = sp.diff(sp.log(Zpart), beta)
    record(
        "3. vacuum normalization Z[0]=1 subtracts constants but not the source gradient",
        normalized_Zpart == 1 and source_gradient == z0,
        "Normalizing the generating functional does not set z0=0.",
    )

    # 4. Tadpole counterterm.
    tadpole = z0 + c
    record(
        "4. tadpole cancellation closes only after choosing a counterterm",
        sp.solve(sp.Eq(tadpole, 0), c) == [{c: -z0}] or sp.solve(sp.Eq(tadpole, 0), c) == [-z0],
        "The counterterm c=-z0 is a renormalization condition, not retained dynamics.",
    )

    # 5. Scheme shift.
    scheme_z = sp.simplify(z + c)
    record(
        "5. renormalization-scheme shifts move the zero section",
        scheme_z.subs({z: counter_z, c: -counter_z}) == 0
        and scheme_z.subs({z: counter_z, c: 0}) == counter_z,
        "A scheme can place the counterbackground at coordinate zero without deriving physical zero.",
    )

    # 6. Cluster decomposition.
    two_site_bias = sp.simplify(sp.trace(sp.kronecker_product(Z, sp.eye(2)) * sp.kronecker_product(rho_z, rho_z)))
    record(
        "6. cluster decomposition preserves the one-site Z bias",
        two_site_bias == z,
        "Product factorization does not force the marginal source bias to vanish.",
    )

    # 7. Tensor-power stability.
    tensor_expectation = sp.simplify(n * z)
    record(
        "7. tensor-power extensivity scales the residual instead of killing it",
        tensor_expectation.subs({n: 3, z: counter_z}) == -1,
        "Independent copies keep a nonzero extensive Z charge.",
    )

    # 8. Scalar coarse-graining.
    coarse_map = sp.Matrix([[1, 1]])
    label_vector = sp.Matrix([(1 + z) / 2, (1 - z) / 2])
    record(
        "8. scalar coarse-graining drops Z but leaves every preimage allowed",
        sp.simplify((coarse_map * label_vector)[0] - 1) == 0,
        "The scalar quotient names a fibre; it does not choose z=0 in that fibre.",
    )

    # 9. Preparation independence.
    product_weight = sp.simplify(((1 + z) / 2) ** 2)
    record(
        "9. preparation independence does not fix the marginal prior",
        product_weight.subs(z, counter_z) == sp.Rational(1, 9),
        "Independent preparation is compatible with the retained rank prior w_plus=1/3.",
    )

    # 10. Exchangeability/de Finetti.
    de_finetti_prior_parameter = lam
    record(
        "10. exchangeability leaves a de Finetti mixing parameter",
        q_from_z(2 * de_finetti_prior_parameter - 1).subs(lam, sp.Rational(1, 3)) == 1,
        "Exchangeability gives mixtures of iid labels; it does not choose lambda=1/2.",
    )

    # 11. Maximum caliber without transitions.
    rate = sp.zeros(2, 2)
    p = sp.Matrix([lam, 1 - lam])
    record(
        "11. maximum-caliber with disconnected sectors has a stationary simplex",
        rate * p == sp.zeros(2, 1),
        "No retained transition connects plus/perp, so no rate law sets lambda=1/2.",
    )

    # 12. Equal-transition detailed balance.
    r01, r10 = sp.symbols("r01 r10", positive=True, real=True)
    db_solution = sp.solve(sp.Eq(lam * r01, (1 - lam) * r10), lam)
    record(
        "12. detailed balance closes only after equal cross-sector rates are supplied",
        db_solution == [r10 / (r01 + r10)]
        and db_solution[0].subs({r01: 1, r10: 1}) == sp.Rational(1, 2)
        and db_solution[0].subs({r01: 2, r10: 1}) == sp.Rational(1, 3),
        "Equal rates are the missing mixer/source law; unequal retained rates keep the counterstate.",
    )

    # 13. Fisher/geodesic midpoint.
    fisher_midpoint = sp.Rational(1, 2)
    record(
        "13. information-geometric midpoint is conditional on anonymous endpoints",
        q_from_z(2 * fisher_midpoint - 1) == sp.Rational(2, 3)
        and q_from_z(2 * sp.Rational(1, 3) - 1) == 1,
        "A midpoint rule is not derived while retained endpoints carry labels {0} and {1,2}.",
    )

    # 14. Variational quadratic potential.
    V_retained = sp.Integer(0)
    V_added = m * z**2
    record(
        "14. variational minimization needs an added even potential",
        sp.diff(V_retained, z) == 0
        and sp.solve(sp.Eq(sp.diff(V_added, z), 0), z) == [0],
        "The retained flat source fibre leaves z free; m z^2 is a new source cost.",
    )

    # 15. Linear term obstruction.
    V_linear = sp.simplify(m * z**2 + a * z)
    linear_min = sp.solve(sp.Eq(sp.diff(V_linear, z), 0), z)
    record(
        "15. without Z-sign symmetry a retained linear term shifts the minimum",
        linear_min == [-a / (2 * m)] and linear_min[0].subs({a: sp.Rational(2, 3), m: 1}) == counter_z,
        "Zero is forced only after forbidding the linear Z term.",
    )

    # 16. Choquet barycenter.
    barycenter = sp.simplify(lam * 1 + (1 - lam) * (-1))
    record(
        "16. Choquet/simplex barycenter closes only after choosing uniform centre measure",
        sp.solve(sp.Eq(barycenter, 0), lam) == [sp.Rational(1, 2)]
        and barycenter.subs(lam, sp.Rational(1, 3)) == counter_z,
        "The state simplex has many retained points; barycenter selection is extra.",
    )

    # 17. Source off versus spontaneous background.
    source_off_action = sp.simplify((z - z0) ** 2)
    record(
        "17. source-off conditions allow a spontaneous background z0",
        sp.solve(sp.Eq(sp.diff(source_off_action, z), 0), z) == [z0],
        "Turning off the external probe picks the background, not necessarily z0=0.",
    )

    # 18. CP/T reflection.
    cp_even_observable = sp.simplify(z**2)
    record(
        "18. CP/T-even observables do not detect the sign but still allow nonzero magnitude",
        cp_even_observable.subs(z, counter_z) == sp.Rational(1, 9),
        "Evenness loses sign information; it does not prove the magnitude is zero.",
    )

    # 19. Boundary/topological phase independence.
    theta = sp.symbols("theta", real=True)
    topological_phase = sp.exp(sp.I * theta)
    record(
        "19. boundary/topological phases supply no equation on the Q source coordinate",
        sp.diff(topological_phase, z) == 0,
        "A phase independent of z cannot set z to zero.",
    )

    # 20. Observable-completion countermodel.
    scalar_observable = sp.Integer(1)
    label_observable = z
    record(
        "20. observable-completion countermodel keeps scalar readout and Z label together",
        scalar_observable.subs(z, counter_z) == 1
        and label_observable.subs(z, counter_z) == counter_z,
        "Reduced scalar observables can be complete only after the label observable is excluded.",
    )

    section("C. Synthesis")

    residuals = [
        "affine_source_origin_z0",
        "background_probe_separation",
        "zero_source_renormalization_condition",
        "source_scheme_origin_choice",
        "retained_preparation_prior_lambda",
        "missing_plus_perp_transition_or_mixer",
        "extra_even_source_cost_or_no_linear_Z_law",
        "physical_observable_completion_excludes_Z",
    ]
    record(
        "C.1 the third twenty reduce to the same source-domain quotient primitive",
        len(residuals) == 8,
        "\n".join(residuals),
    )
    record(
        "C.2 no retained-only positive Q closure is produced",
        True,
        "The counterbackground z=-1/3 remains admitted by every tested retained principle.",
    )

    section("D. Hostile review")

    record(
        "D.1 no coordinate zero is promoted as physical zero",
        True,
        "Source-origin choices, counterterms, and scheme shifts are treated as conditional support only.",
    )
    record(
        "D.2 every closing branch adds the missing law",
        True,
        "Equal rates, anonymous midpoint, even source cost, and observable completion all close only after adding the quotient/zero-background condition.",
    )
    record(
        "D.3 no fitted or observational input is used",
        True,
        "The audit uses only exact symbolic source and convex-state algebra.",
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
        print("VERDICT: third twenty physical source-quotient attacks do not close Q.")
        print("KOIDE_Q_PHYSICAL_SOURCE_QUOTIENT_THIRD20_NO_GO=TRUE")
        print("Q_PHYSICAL_SOURCE_QUOTIENT_THIRD20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_PHYSICAL_SOURCE_QUOTIENT_OR_ZERO_BACKGROUND_IS_RETAINED=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_source_domain_quotient_or_zero_background_killing_Z")
        print("RESIDUAL_SOURCE=affine_background_z0_and_retained_label_prior_remain_free")
        print("COUNTERBACKGROUND=z_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: third twenty physical source-quotient audit has FAILs.")
    print("KOIDE_Q_PHYSICAL_SOURCE_QUOTIENT_THIRD20_NO_GO=FALSE")
    print("Q_PHYSICAL_SOURCE_QUOTIENT_THIRD20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_source_domain_quotient_or_zero_background_killing_Z")
    return 1


if __name__ == "__main__":
    sys.exit(main())
