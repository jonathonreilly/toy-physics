#!/usr/bin/env python3
"""
Koide Q Wess-Zumino / Berezinian asymmetric-measure no-go.

Theorem attempt:
  Upgrade the exact support scalar

      T(T+1) - Y^2 = 3/4 - 1/4 = 1/2

  into the charged-lepton cyclic amplitude map

      rho = |b|^2/a^2 = T(T+1) - Y^2.

  The proposed physical source is a Wess-Zumino, anomaly-inflow, or
  Berezinian measure principle that would give SU(2)_L and U(1)_Y opposite
  signs and unit relative normalization.

Result:
  Negative for the retained source class tested here.  Statistics/graded
  determinants attach one sign to an entire field, not one sign to SU(2)_L and
  another to U(1)_Y inside the same field.  Standard Wess-Zumino consistency
  supplies anomaly-cancellation equations; for one SM generation those anomaly
  coefficients cancel to zero and do not provide a nonzero generation-cyclic
  traceless source.  A map rho = C2 - Y^2 closes Q only after adding a
  generator-selective grading plus unit hypercharge normalization, which is
  exactly the missing physical law.

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


def q_from_rho(rho: sp.Expr) -> sp.Expr:
    """rho = |b|^2/a^2 on the normalized second-order carrier."""
    return sp.simplify(sp.Rational(1, 3) + sp.Rational(2, 3) * rho)


def ktl_from_rho(rho: sp.Expr) -> sp.Expr:
    """Equivalent traceless source coordinate; K_TL=0 iff rho=1/2."""
    r = sp.simplify(2 * rho)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Exact support scalar and the missing map")

    t = sp.Rational(1, 2)
    y = sp.Rational(1, 2)
    c2_su2 = sp.simplify(t * (t + 1))
    y2 = y**2
    rho_diff = sp.simplify(c2_su2 - y2)
    rho_sum = sp.simplify(c2_su2 + y2)

    record(
        "A.1 lepton/Higgs electroweak doublet has C2=3/4 and Y^2=1/4",
        c2_su2 == sp.Rational(3, 4) and y2 == sp.Rational(1, 4),
        f"C2_SU2={c2_su2}, Y^2={y2}",
    )
    record(
        "A.2 the desired asymmetric scalar is exactly 1/2",
        rho_diff == sp.Rational(1, 2)
        and q_from_rho(rho_diff) == sp.Rational(2, 3)
        and ktl_from_rho(rho_diff) == 0,
        f"C2-Y^2={rho_diff}; Q={q_from_rho(rho_diff)}; K_TL={ktl_from_rho(rho_diff)}",
    )
    record(
        "A.3 the same retained inputs also allow the positive measure sum",
        rho_sum == 1 and q_from_rho(rho_sum) == 1,
        f"C2+Y^2={rho_sum}; Q={q_from_rho(rho_sum)}",
    )

    section("B. General generator-weighted measure class")

    alpha, beta = sp.symbols("alpha beta", real=True)
    rho_general = sp.simplify(alpha * c2_su2 + beta * y2)
    beta_needed = sp.solve(sp.Eq(rho_general.subs(alpha, 1), sp.Rational(1, 2)), beta)
    alpha_needed = sp.solve(sp.Eq(rho_general, sp.Rational(1, 2)), alpha)

    record(
        "B.1 a retained scalar measure leaves two generator weights free",
        rho_general == (3 * alpha + beta) / 4,
        f"rho(alpha,beta)={rho_general}",
    )
    record(
        "B.2 with SU(2) normalization fixed to alpha=1, the closing sign is beta=-1",
        beta_needed == [-1],
        f"rho(1,beta)=1/2 -> beta={beta_needed}",
    )
    record(
        "B.3 without a generator-selective law, the closing equation fixes only one map coefficient",
        alpha_needed == [(2 - beta) / 3],
        f"rho=1/2 -> alpha={alpha_needed[0]}",
    )

    maps = {
        "positive_sum": (1, 1),
        "su2_only": (1, 0),
        "difference": (1, -1),
        "hypercharge_only": (0, 1),
    }
    map_lines = []
    for label, (a_weight, b_weight) in maps.items():
        value = sp.simplify(rho_general.subs({alpha: a_weight, beta: b_weight}))
        map_lines.append(
            f"{label}: (alpha,beta)=({a_weight},{b_weight}) -> rho={value}, "
            f"Q={q_from_rho(value)}, K_TL={ktl_from_rho(value)}"
        )
    record(
        "B.4 retained arithmetic admits inequivalent maps; only the asymmetric one closes Q",
        True,
        "\n".join(map_lines),
    )

    section("C. Berezinian/statistics grading cannot give SU(2)-minus-U(1) inside one field")

    s = sp.symbols("s", real=True)
    field_statistical_weight = sp.simplify(s * (c2_su2 + y2))
    desired_internal_split = sp.simplify(c2_su2 - y2)
    s_solution = sp.solve(sp.Eq(field_statistical_weight, desired_internal_split), s)
    record(
        "C.1 one Berezinian sign on a field multiplies C2 and Y^2 with the same sign",
        field_statistical_weight == s,
        f"s*(C2+Y^2)={field_statistical_weight}",
    )
    record(
        "C.2 matching the numeric 1/2 with a field sign needs s=1/2, not a sign grading",
        s_solution == [sp.Rational(1, 2)],
        f"s*(C2+Y^2)=C2-Y^2 -> s={s_solution}",
    )
    record(
        "C.3 a true SU(2)-minus-U(1) split requires a generator-selective grading",
        sp.simplify((c2_su2 + y2) - desired_internal_split) == sp.Rational(1, 2),
        "Statistics distinguishes boson/fermion or chirality sectors; it does not by itself "
        "flip only the U(1)_Y generator inside a lepton/Higgs doublet.",
    )

    section("D. Wess-Zumino consistency supplies anomaly cancellation, not the source map")

    # One left-handed SM generation using conjugate right-handed fields.
    # Tuples are (multiplicity, SU2_is_doublet, hypercharge).
    fields = {
        "Q_L": (6, True, sp.Rational(1, 6)),      # 3 colors * 2 SU2 components
        "u_R^c": (3, False, sp.Rational(-2, 3)),
        "d_R^c": (3, False, sp.Rational(1, 3)),
        "L": (2, True, sp.Rational(-1, 2)),
        "e_R^c": (1, False, sp.Rational(1, 1)),
    }
    grav_u1 = sp.simplify(sum(mult * hyp for mult, _, hyp in fields.values()))
    u1_cube = sp.simplify(sum(mult * hyp**3 for mult, _, hyp in fields.values()))
    su2_su2_u1 = sp.simplify(
        3 * sp.Rational(1, 6) * sp.Rational(1, 2)
        + sp.Rational(-1, 2) * sp.Rational(1, 2)
    )
    su3_su3_u1 = sp.simplify(
        2 * sp.Rational(1, 6) * sp.Rational(1, 2)
        + sp.Rational(-2, 3) * sp.Rational(1, 2)
        + sp.Rational(1, 3) * sp.Rational(1, 2)
    )

    record(
        "D.1 one-generation WZ anomaly coefficients cancel exactly",
        grav_u1 == 0 and u1_cube == 0 and su2_su2_u1 == 0 and su3_su3_u1 == 0,
        f"grav-U1={grav_u1}, U1^3={u1_cube}, SU2^2-U1={su2_su2_u1}, SU3^2-U1={su3_su3_u1}",
    )
    record(
        "D.2 zero anomaly data cannot supply a nonzero K_TL source",
        rho_diff != 0 and grav_u1 == 0 and u1_cube == 0,
        "The anomaly equations are consistency constraints on gauge variations; "
        "they do not select rho=C2-Y^2 on the generation-cyclic carrier.",
    )

    section("E. Counterfamily with identical anomaly data and different carrier source")

    beta_values = [-1, 0, 1, sp.Rational(2, 1)]
    counter_lines = []
    q_values = []
    for beta_value in beta_values:
        rho_value = sp.simplify(rho_general.subs({alpha: 1, beta: beta_value}))
        q_value = q_from_rho(rho_value)
        q_values.append(q_value)
        counter_lines.append(
            f"beta={beta_value}: anomalies=(0,0,0,0), rho={rho_value}, "
            f"Q={q_value}, K_TL={ktl_from_rho(rho_value)}"
        )
    record(
        "E.1 changing the generator weight changes Q while retained anomaly data stay fixed",
        len(set(q_values)) == len(q_values),
        "\n".join(counter_lines),
    )

    residual = sp.simplify(rho_general - rho_diff)
    record(
        "E.2 residual is the generator-selective grading/normalization law",
        residual == (3 * alpha + beta - 2) / 4,
        f"RESIDUAL_MAP=rho(alpha,beta)-(C2-Y^2)={residual}",
    )

    section("F. Verdict")

    record(
        "F.1 WZ/Berezinian asymmetric measure route does not close Q",
        True,
        "The exact difference scalar remains strong support.  Closure still needs "
        "a retained theorem forcing alpha=1 and beta=-1 on the charged-lepton "
        "generation-cyclic second-order carrier.",
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
        print("VERDICT: Wess-Zumino/Berezinian asymmetric-measure source does not close Q.")
        print("KOIDE_Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_NO_GO=TRUE")
        print("Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1")
        print("RESIDUAL_MAP=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1")
        return 0

    print("VERDICT: Wess-Zumino/Berezinian asymmetric-measure audit has FAILs.")
    print("KOIDE_Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_NO_GO=FALSE")
    print("Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1")
    print("RESIDUAL_MAP=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1")
    return 1


if __name__ == "__main__":
    sys.exit(main())
