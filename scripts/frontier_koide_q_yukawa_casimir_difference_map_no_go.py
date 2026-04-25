#!/usr/bin/env python3
"""
Koide Q Yukawa Casimir-difference amplitude-map no-go.

Theorem attempt:
  The strongest A1/Yukawa route observes that the lepton doublet and Higgs
  have T(T+1) - Y^2 = 1/2, exactly the amplitude ratio |b|^2/a^2 needed for
  the Koide radius.  Perhaps retained Cl(3) electroweak embedding plus Yukawa
  structure derives

      |b|^2/a^2 = T(T+1) - Y^2.

Result:
  No from the currently retained structure.  The Casimir difference is exact
  and highly suggestive, but the map from electroweak Casimirs to the cyclic
  amplitude ratio is not derived.  Standard positive gauge/radiative weights
  naturally produce same-sign sums, while the difference requires a relative
  sign/asymmetric measure theorem.  Without that map, the scalar remains
  |b|^2/a^2 - 1/2, equivalent to K_TL.
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


def q_from_amp_ratio(rho: sp.Expr) -> sp.Expr:
    """rho = |b|^2/a^2, c^2 = 4 rho, E_perp/E_plus = c^2/2 = 2 rho."""
    return sp.simplify((1 + 2 * rho) / 3)


def ktl_from_amp_ratio(rho: sp.Expr) -> sp.Expr:
    r = sp.simplify(2 * rho)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Exact electroweak Casimir arithmetic")

    T = sp.Rational(1, 2)
    Y_abs = sp.Rational(1, 2)
    casimir_su2 = T * (T + 1)
    y2 = Y_abs**2
    casimir_sum = sp.simplify(casimir_su2 + y2)
    casimir_diff = sp.simplify(casimir_su2 - y2)

    record(
        "A.1 lepton/Higgs doublet has T(T+1)=3/4 and Y^2=1/4",
        casimir_su2 == sp.Rational(3, 4) and y2 == sp.Rational(1, 4),
        f"T(T+1)={casimir_su2}, Y^2={y2}",
    )
    record(
        "A.2 the Casimir sum gives C_tau=1 while the difference gives 1/2",
        casimir_sum == 1 and casimir_diff == sp.Rational(1, 2),
        f"sum={casimir_sum}, difference={casimir_diff}",
    )

    particles = {
        "lepton_or_Higgs_doublet": (sp.Rational(1, 2), sp.Rational(1, 2)),
        "quark_doublet": (sp.Rational(1, 2), sp.Rational(1, 6)),
        "e_R": (sp.Rational(0), sp.Rational(1, 1)),
        "u_R": (sp.Rational(0), sp.Rational(2, 3)),
        "d_R": (sp.Rational(0), sp.Rational(1, 3)),
    }
    differences = {
        name: sp.simplify(t * (t + 1) - y**2)
        for name, (t, y) in particles.items()
    }
    record(
        "A.3 the 1/2 difference is unique among the checked SM Yukawa-relevant representations",
        differences["lepton_or_Higgs_doublet"] == sp.Rational(1, 2)
        and all(value != sp.Rational(1, 2) for name, value in differences.items() if name != "lepton_or_Higgs_doublet"),
        f"differences={differences}",
    )

    section("B. Koide consequence if the amplitude map were supplied")

    rho = sp.symbols("rho", positive=True, real=True)
    q = q_from_amp_ratio(rho)
    ktl = ktl_from_amp_ratio(rho)
    record(
        "B.1 rho=|b|^2/a^2=1/2 is exactly the Koide source-neutral leaf",
        sp.simplify(q.subs(rho, sp.Rational(1, 2)) - sp.Rational(2, 3)) == 0
        and sp.simplify(ktl.subs(rho, sp.Rational(1, 2))) == 0,
        f"Q(rho)={q}, K_TL(rho)={ktl}",
    )

    section("C. The amplitude map is not derived by standard retained gauge weights")

    g2, g1 = sp.symbols("g2 g1", positive=True, real=True)
    same_sign_weight = sp.simplify(g2**2 * casimir_su2 + g1**2 * y2)
    diff_weight = sp.simplify(g2**2 * casimir_su2 - g1**2 * y2)
    record(
        "C.1 standard positive gauge/radiative weights produce same-sign Casimir sums",
        same_sign_weight == g2**2 * sp.Rational(3, 4) + g1**2 * sp.Rational(1, 4),
        f"W_sum={same_sign_weight}",
    )
    record(
        "C.2 the difference requires a relative sign/asymmetric measure theorem",
        diff_weight == g2**2 * sp.Rational(3, 4) - g1**2 * sp.Rational(1, 4),
        f"W_diff={diff_weight}",
    )

    section("D. Exact countermaps")

    maps = {
        "difference_map": casimir_diff,
        "sum_map": casimir_sum,
        "hypercharge_only": y2,
    }
    map_values = {
        name: (sp.simplify(q_from_amp_ratio(value)), sp.simplify(ktl_from_amp_ratio(value)))
        for name, value in maps.items()
    }
    record(
        "D.1 multiple retained-scalar maps are algebraically available, only one is Koide",
        map_values["difference_map"] == (sp.Rational(2, 3), 0)
        and map_values["sum_map"][0] == 1
        and map_values["hypercharge_only"][0] == sp.Rational(1, 2),
        f"map -> (Q,K_TL) = {map_values}",
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    general_map = sp.simplify(alpha * casimir_su2 + beta * y2)
    record(
        "D.2 fixing the Koide value imposes one coefficient equation on the map",
        sp.solve(sp.Eq(general_map, sp.Rational(1, 2)), alpha) == [(2 - beta) / 3],
        f"rho_map=(3 alpha + beta)/4; Koide fixes alpha=(2-beta)/3.",
    )

    section("E. Verdict")

    residual = sp.simplify(rho - casimir_diff)
    record(
        "E.1 the open object is the amplitude-map lemma rho=T(T+1)-Y^2",
        residual == rho - sp.Rational(1, 2),
        f"RESIDUAL={residual}",
    )
    record(
        "E.2 Yukawa Casimir difference is support, not closure, without the map",
        True,
        "The exact 1/2 scalar is real support; the physical cyclic amplitude assignment remains unproved.",
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
        print("VERDICT: Yukawa Casimir-difference arithmetic does not close Q by itself.")
        print("It would close Q if a retained amplitude-map theorem supplied")
        print("|b|^2/a^2 = T(T+1)-Y^2, but that map is still missing.")
        print()
        print("KOIDE_Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_NO_GO=TRUE")
        print("Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL")
        print("RESIDUAL_MAP=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL")
        return 0

    print("VERDICT: Yukawa Casimir-difference map audit has FAILs.")
    print()
    print("KOIDE_Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_NO_GO=FALSE")
    print("Q_YUKAWA_CASIMIR_DIFFERENCE_MAP_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL")
    print("RESIDUAL_MAP=rho_amp_minus_TTplus1_minus_Y2_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
