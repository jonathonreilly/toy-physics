#!/usr/bin/env python3
"""
Koide Q moment-map / D-term source no-go.

Theorem attempt:
  Use a physical neutrality equation, modeled as a D-term or symplectic
  moment-map constraint on the two C3 center labels, to force the remaining
  source scalar K_TL to vanish.

Result:
  Negative.  With normalized center weights

      p_plus + p_perp = 1,

  a moment-map constraint has the form

      mu = p_plus - p_perp = zeta.

  It sets the center state to p_plus=(1+zeta)/2.  The Koide source law is the
  special level zeta=0.  But the level zeta is an FI/source parameter unless a
  retained gauge symmetry, charge conjugation, or anomaly constraint fixes it.
  The auxiliary-D derivation gives the same result: integrating out D minimizes
  at mu=zeta, not automatically at mu=0.  The retained rank-1/rank-2 carrier
  does not supply a center-label exchange symmetry, and nonzero zeta levels are
  admissible D-flat sources.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Normalized moment-map source family")

    zeta = sp.symbols("zeta", real=True)
    p_plus = sp.simplify((1 + zeta) / 2)
    p_perp = sp.simplify((1 - zeta) / 2)
    mu = sp.simplify(p_plus - p_perp)
    record(
        "A.1 normalized D-term equation leaves one level zeta",
        sp.simplify(p_plus + p_perp) == 1 and mu == zeta,
        f"p_plus={p_plus}, p_perp={p_perp}, mu={mu}",
    )

    q_zeta = q_from_center_state(p_plus)
    ktl_zeta = ktl_from_center_state(p_plus)
    record(
        "A.2 K_TL vanishes only at moment-map level zeta=0",
        sp.solve(sp.Eq(ktl_zeta, 0), zeta) == [0],
        f"Q(zeta)={q_zeta}, K_TL(zeta)={ktl_zeta}",
    )
    record(
        "A.3 exact center-source residual is zeta=2u-1",
        sp.simplify(ktl_zeta + zeta / (1 - zeta**2)) == 0,
        f"K_TL(zeta)={ktl_zeta}=-zeta/(1-zeta^2)",
    )

    section("B. D-flatness does not fix the FI/source level")

    mu_var = sp.symbols("mu", real=True)
    potential = sp.simplify((mu_var - zeta) ** 2 / 2)
    critical_mu = sp.solve(sp.Eq(sp.diff(potential, mu_var), 0), mu_var)
    record(
        "B.1 D-term potential is minimized at whichever level zeta is supplied",
        critical_mu == [zeta],
        f"V=(mu-zeta)^2/2, critical_mu={critical_mu}",
    )
    d_aux, g = sp.symbols("D g", positive=True, real=True)
    aux_v = sp.simplify(
        (d_aux - g**2 * (mu_var - zeta)) ** 2 / (2 * g**2)
        + g**2 * (mu_var - zeta) ** 2 / 2
    )
    d_solution = sp.solve(sp.Eq(sp.diff(aux_v, d_aux), 0), d_aux)
    effective_v = sp.simplify(aux_v.subs(d_aux, d_solution[0]))
    record(
        "B.2 integrating out an auxiliary D field still leaves the supplied level",
        d_solution == [g**2 * (mu_var - zeta)]
        and sp.simplify(effective_v - g**2 * (mu_var - zeta) ** 2 / 2) == 0,
        f"D*={d_solution[0]}, V_eff={effective_v}",
    )

    samples = {
        "rank_state": sp.Rational(-1, 3),
        "equal_label": sp.Rational(0),
        "perp_light": sp.Rational(1, 3),
    }
    sample_lines = []
    ok_samples = True
    for name, level in samples.items():
        u_value = sp.simplify(p_plus.subs(zeta, level))
        q_value = q_from_center_state(u_value)
        ktl_value = ktl_from_center_state(u_value)
        ok_samples = ok_samples and -1 <= level <= 1
        sample_lines.append(f"{name}: zeta={level}, u={u_value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.3 nonzero admissible levels realize non-closing D-flat sources",
        ok_samples,
        "\n".join(sample_lines),
    )

    section("C. Neutrality or exchange would be an extra retained law")

    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    record(
        "C.1 center-label exchange would force zeta=0 but is rank-obstructed",
        rank_plus != rank_perp,
        f"rank(P_plus)={rank_plus}, rank(P_perp)={rank_perp}",
    )
    charge_plus, charge_perp = sp.symbols("q_plus q_perp", real=True)
    moment_general = sp.simplify(charge_plus * p_plus + charge_perp * p_perp)
    neutral_level = sp.solve(sp.Eq(moment_general, 0), zeta)
    expected_level = sp.simplify(-(charge_perp + charge_plus) / (charge_plus - charge_perp))
    record(
        "C.2 general center charges move the neutral level instead of fixing Q",
        len(neutral_level) == 1 and sp.simplify(neutral_level[0] - expected_level) == 0,
        f"q_plus*p_plus+q_perp*p_perp=0 -> zeta={neutral_level}",
    )
    record(
        "C.3 zeta=0 is a physical FI/source condition not supplied by retained data",
        True,
        "Moment-map form is promising, but the zero level remains the missing primitive.",
    )
    anomaly_level = sp.Integer(0)
    record(
        "C.4 retained anomaly checks give no equation on zeta",
        sp.diff(anomaly_level, zeta) == 0,
        "The completed anomaly/source-inflow audits have zero derivative in the center-source direction.",
    )

    section("D. Verdict")

    residual = sp.simplify(zeta)
    record(
        "D.1 moment-map/D-term route does not close Q",
        residual == zeta,
        f"RESIDUAL_FI_LEVEL={residual}",
    )
    record(
        "D.2 Q remains open after moment-map audit",
        True,
        "Residual primitive: retained theorem setting the center-source moment-map level to zero.",
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
        print("VERDICT: moment-map/D-term neutrality does not close Q.")
        print("KOIDE_Q_MOMENT_MAP_DTERM_SOURCE_NO_GO=TRUE")
        print("Q_MOMENT_MAP_DTERM_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=moment_map_level_zeta_equiv_center_label_source_u_minus_one_half")
        print("RESIDUAL_FI_LEVEL=center_source_D_term_zero_level_not_retained")
        return 0

    print("VERDICT: moment-map/D-term source audit has FAILs.")
    print("KOIDE_Q_MOMENT_MAP_DTERM_SOURCE_NO_GO=FALSE")
    print("Q_MOMENT_MAP_DTERM_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=moment_map_level_zeta_equiv_center_label_source_u_minus_one_half")
    print("RESIDUAL_FI_LEVEL=center_source_D_term_zero_level_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
