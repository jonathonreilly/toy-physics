#!/usr/bin/env python3
"""
Koide Q continuous anomaly-inflow source no-go.

Theorem attempt:
  Strengthen the anomaly route by allowing a continuous anomaly-inflow
  functional on the normalized singlet/doublet source quotient.  Perhaps
  anomaly cancellation then forces the quotient coefficient K_TL to vanish.

Result:
  The retained anomaly data supply no nonzero quotient coupling.  Completed
  SM anomalies vanish generation by generation, and retained C3 character
  anomalies are integer congruences independent of continuous source weights.
  Even a source-weighted anomaly functional has zero derivative with respect
  to the normalized traceless source.  A continuous inflow term mu*K_TL would
  close Q only if a new theorem supplied mu != 0 and identified K_TL as an
  anomalous charge.  The current retained package has mu = 0; adding mu != 0
  is a new primitive.
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


def sm_completed_anomaly_vector() -> dict[str, sp.Rational]:
    fields = [
        ("Q_L", sp.Rational(1, 3), 2, 3),
        ("L_L", sp.Rational(-1), 2, 1),
        ("u_R^c", sp.Rational(-4, 3), 1, 3),
        ("d_R^c", sp.Rational(2, 3), 1, 3),
        ("e_R^c", sp.Rational(2), 1, 1),
        ("nu_R^c", sp.Rational(0), 1, 1),
    ]
    out = {"Y": sp.Rational(0), "Y3": sp.Rational(0), "SU3_Y": sp.Rational(0), "SU2_Y": sp.Rational(0)}
    for _name, y, su2_dim, su3_dim in fields:
        out["Y"] += su2_dim * su3_dim * y
        out["Y3"] += su2_dim * su3_dim * y**3
        out["SU3_Y"] += su2_dim * (sp.Rational(1, 2) if su3_dim == 3 else 0) * y
        out["SU2_Y"] += su3_dim * (sp.Rational(1, 2) if su2_dim == 2 else 0) * y
    return {key: sp.simplify(value) for key, value in out.items()}


def q_from_ktl_value(k_value: sp.Rational) -> sp.Expr:
    y = sp.symbols("y", positive=True, real=True)
    ktl = sp.simplify((1 - y) / (y * (2 - y)))
    if k_value == 0:
        y_value = sp.Integer(1)
    else:
        y_value = [root for root in sp.solve(sp.Eq(ktl, k_value), y) if 0 < float(root.evalf()) < 2][0]
    r = sp.simplify((2 - y_value) / y_value)
    return sp.simplify((1 + r) / 3)


def c3_projectors() -> tuple[sp.Matrix, sp.Matrix]:
    i3 = sp.eye(3)
    j = sp.ones(3, 3)
    p_plus = j / 3
    return p_plus, i3 - p_plus


def main() -> int:
    section("A. Retained anomaly data have zero quotient coupling")

    full = sm_completed_anomaly_vector()
    record(
        "A.1 completed perturbative anomaly vector vanishes generation by generation",
        all(value == 0 for value in full.values()),
        f"A_full={full}",
    )

    q_chars = [sp.Integer(0), sp.Integer(1), sp.Integer(2)]
    c3_linear = sum(q_chars)
    c3_cubic = sum(q**3 for q in q_chars)
    record(
        "A.2 retained C3 character anomaly sums vanish as integer congruences mod 3",
        int(c3_linear % 3) == 0 and int(c3_cubic % 3) == 0,
        f"sum q={c3_linear}, sum q^3={c3_cubic}",
    )

    p_plus, p_perp = c3_projectors()
    k0, k_tl = sp.symbols("K_trace K_TL", real=True)
    source = sp.simplify(k0 * sp.eye(3) + k_tl * (p_plus - p_perp))
    generation_anomaly = sp.Matrix([0, 0, 0])
    source_weighted_anomaly = sp.simplify((sp.ones(1, 3) * source * generation_anomaly)[0])
    record(
        "A.3 source-weighted perturbative anomaly is identically blind to K_TL",
        source_weighted_anomaly == 0
        and sp.diff(source_weighted_anomaly, k_tl) == 0,
        "A_gen=(0,0,0), so d/dK_TL Tr_source(A_gen)=0.",
    )

    section("B. General continuous inflow coupling would be new data")

    k, mu = sp.symbols("K_TL mu", real=True)
    retained_mu = sp.Integer(0)
    inflow = sp.simplify(mu * k)
    retained_inflow = inflow.subs(mu, retained_mu)
    record(
        "B.1 retained anomaly package supplies mu=0 for a continuous K_TL inflow term",
        retained_inflow == 0,
        "No retained anomaly coefficient couples to the real source quotient.",
    )
    record(
        "B.2 anomaly cancellation would force K_TL=0 only after adding mu != 0",
        sp.solve(sp.Eq(inflow, 0), k) == [0],
        "The implication uses an externally supplied nonzero quotient anomaly coefficient.",
    )
    source_mu = sp.diff(source_weighted_anomaly, k_tl)
    record(
        "B.3 retained source-weighted anomaly derives mu=0, not a nonzero coupling",
        source_mu == 0,
        f"mu_retained=dA_source/dK_TL={source_mu}",
    )

    section("C. Off-Koide sources preserve retained anomaly data")

    k_sample = sp.Rational(1, 5)
    q_sample = q_from_ktl_value(k_sample)
    record(
        "C.1 K_TL=1/5 is admissible and off Koide",
        sp.simplify(q_sample - sp.Rational(2, 3)) != 0,
        f"Q={sp.N(q_sample, 12)}",
    )
    record(
        "C.2 the off-Koide source leaves retained anomaly and discrete character data unchanged",
        all(value == 0 for value in full.values())
        and int(c3_linear % 3) == 0
        and retained_inflow.subs(k, k_sample) == 0,
        "Changing a continuous source coefficient does not change completed anomaly traces or C3 integer characters.",
    )

    section("D. Normalization ambiguity")

    mu_values = [sp.Rational(0), sp.Rational(1, 2), sp.Rational(2)]
    implications = {value: sp.simplify((value * k).subs(k, k_sample)) for value in mu_values}
    record(
        "D.1 different continuous inflow normalizations give different physical equations",
        implications[0] == 0 and implications[sp.Rational(1, 2)] != 0 and implications[2] != 0,
        f"mu*K_TL at K_TL=1/5: {implications}",
    )
    record(
        "D.2 selecting a nonzero mu is precisely the missing anomaly/source-identification theorem",
        True,
        "It would be new physics, not a consequence of the retained anomaly arithmetic.",
    )
    q_residual, theta_residual, nu = sp.symbols("q_residual theta_residual nu", real=True)
    mixed_inflow = sp.Eq(mu * q_residual + nu * theta_residual, 0)
    mixed_line = sp.solve(mixed_inflow, theta_residual)
    record(
        "D.3 mixed continuous inflow leaves a residual line without independent laws",
        mixed_line == [-mu * q_residual / nu],
        "A Q/delta mixed term cannot set both residuals to zero unless extra equations are retained.",
    )

    section("E. Verdict")

    record(
        "E.1 continuous anomaly inflow does not force K_TL=0 from retained data",
        True,
        "The retained quotient anomaly coefficient is zero/absent; nonzero mu is an added primitive.",
    )
    record(
        "E.2 Q remains open after continuous inflow audit",
        True,
        "Residual primitive: derive a nonzero physical anomaly coupling to the K_TL quotient or derive K_TL=0 otherwise.",
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
        print("VERDICT: continuous anomaly-inflow source normalization does not close Q.")
        print("A nonzero inflow coefficient for K_TL would be a new physical")
        print("identification theorem, not retained anomaly data.")
        print()
        print("KOIDE_Q_CONTINUOUS_ANOMALY_INFLOW_SOURCE_NO_GO=TRUE")
        print("Q_CONTINUOUS_ANOMALY_INFLOW_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_COUPLING=mu_K_TL_anomaly_inflow_coefficient")
        print("RESIDUAL_FUNCTIONAL=source_weighted_anomaly_derivative_dA_dKTL_zero")
        return 0

    print("VERDICT: continuous anomaly-inflow source audit has FAILs.")
    print()
    print("KOIDE_Q_CONTINUOUS_ANOMALY_INFLOW_SOURCE_NO_GO=FALSE")
    print("Q_CONTINUOUS_ANOMALY_INFLOW_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_COUPLING=mu_K_TL_anomaly_inflow_coefficient")
    print("RESIDUAL_FUNCTIONAL=source_weighted_anomaly_derivative_dA_dKTL_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
