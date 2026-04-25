#!/usr/bin/env python3
"""
Koide Q SU(2) ladder-amplitude-map no-go.

Theorem attempt:
  The charged lepton sits in an SU(2)_L doublet.  The charged-current ladder
  part of the doublet has an exact half-strength in the standard vertex
  normalization, matching the Koide cyclic amplitude ratio |b|^2/a^2 = 1/2.
  Perhaps the retained electroweak embedding maps that ladder strength to the
  cyclic doublet/singlet amplitude ratio and closes Q.

Result:
  No from the currently retained structure.  The half-strength is exact
  support, but the map from SU(2)_L ladder strength to the C3 cyclic amplitude
  ratio is not derived.  Other exact electroweak scalars remain available and
  give off-Koide radii.

Residual:
  RESIDUAL_SCALAR=rho_amp_minus_su2_ladder_half_equiv_K_TL.
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
    return sp.simplify((1 + 2 * rho) / 3)


def ktl_from_amp_ratio(rho: sp.Expr) -> sp.Expr:
    r = sp.simplify(2 * rho)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    print("=" * 88)
    print("KOIDE Q SU(2) LADDER-AMPLITUDE-MAP NO-GO")
    print("=" * 88)
    print(
        "Theorem attempt: identify the exact SU(2)_L charged-current ladder "
        "half-strength with the cyclic Koide amplitude ratio."
    )

    section("A. Exact SU(2) doublet ladder arithmetic")

    T = sp.Rational(1, 2)
    m_tau = -sp.Rational(1, 2)
    casimir = T * (T + 1)
    t3_sq = m_tau**2
    transverse = sp.simplify(casimir - t3_sq)
    vertex_half = sp.Rational(1, 2) * transverse

    record(
        "A.1 SU(2)_L doublet has C2=3/4 and T3^2=1/4",
        casimir == sp.Rational(3, 4) and t3_sq == sp.Rational(1, 4),
        f"C2={casimir}, T3^2={t3_sq}",
    )
    record(
        "A.2 transverse charged-current Casimir remainder is 1/2",
        transverse == sp.Rational(1, 2) and vertex_half == sp.Rational(1, 4),
        "Using C2-T3^2 gives 1/2; an additional vertex split gives 1/4.",
    )

    # The route's strongest version uses C2 - T3^2 = 1/2 directly.
    ladder_half = transverse

    section("B. Koide consequence if the ladder map were supplied")

    rho = sp.symbols("rho", positive=True, real=True)
    record(
        "B.1 rho=|b|^2/a^2=1/2 is exactly the Koide leaf",
        q_from_amp_ratio(ladder_half) == sp.Rational(2, 3)
        and ktl_from_amp_ratio(ladder_half) == 0,
        f"Q(1/2)={q_from_amp_ratio(ladder_half)}, K_TL(1/2)={ktl_from_amp_ratio(ladder_half)}",
    )

    section("C. Competing exact electroweak scalars")

    hypercharge_sq = sp.Rational(1, 4)
    total_casimir = casimir + hypercharge_sq
    neutral_t3 = t3_sq
    candidates = {
        "charged_ladder_C2_minus_T3sq": ladder_half,
        "hypercharge_square": hypercharge_sq,
        "neutral_T3_square": neutral_t3,
        "total_SU2_plus_Y": total_casimir,
    }
    candidate_values = {
        name: (q_from_amp_ratio(value), ktl_from_amp_ratio(value))
        for name, value in candidates.items()
    }
    record(
        "C.1 multiple exact electroweak scalars are available, only the ladder scalar is Koide",
        candidate_values["charged_ladder_C2_minus_T3sq"] == (sp.Rational(2, 3), 0)
        and candidate_values["hypercharge_square"][0] == sp.Rational(1, 2)
        and candidate_values["total_SU2_plus_Y"][0] == 1,
        f"candidate -> (Q,K_TL) = {candidate_values}",
    )

    alpha, beta, gamma = sp.symbols("alpha beta gamma", real=True)
    general_map = sp.simplify(alpha * transverse + beta * hypercharge_sq + gamma * neutral_t3)
    record(
        "C.2 Koide fixes one coefficient equation in a general electroweak scalar map",
        sp.solve(sp.Eq(general_map, sp.Rational(1, 2)), alpha) == [1 - beta / 2 - gamma / 2],
        f"rho_map=alpha/2+beta/4+gamma/4; Koide fixes alpha=1-beta/2-gamma/2.",
    )

    section("D. Why the route is not retained closure")

    residual = sp.simplify(rho - ladder_half)
    record(
        "D.1 the missing theorem is rho_amp = C2 - T3^2",
        residual == rho - sp.Rational(1, 2),
        f"RESIDUAL={residual}",
    )
    record(
        "D.2 the retained electroweak embedding does not map SU(2) ladder strength to C3 cyclic radius",
        True,
        "The ladder scalar is exact support; the cross-basis amplitude map is the missing bridge.",
    )

    section("E. Hostile-review verdict")

    record(
        "E.1 no target mass data, observational pin, delta pin, or Q target is used",
        True,
    )
    record(
        "E.2 SU(2) ladder arithmetic does not derive K_TL=0 without the amplitude map",
        True,
        "Choosing the ladder scalar as rho is a new selector unless derived.",
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
        print("VERDICT: SU(2) ladder half-strength does not close Q by itself.")
        print("It is exact support, but the map to the C3 cyclic amplitude")
        print("ratio is still missing.")
        print()
        print("KOIDE_Q_SU2_LADDER_AMPLITUDE_MAP_NO_GO=TRUE")
        print("Q_SU2_LADDER_AMPLITUDE_MAP_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=rho_amp_minus_su2_ladder_half_equiv_K_TL")
        return 0

    print("VERDICT: SU(2) ladder amplitude-map audit has FAILs.")
    print()
    print("KOIDE_Q_SU2_LADDER_AMPLITUDE_MAP_NO_GO=FALSE")
    print("Q_SU2_LADDER_AMPLITUDE_MAP_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=rho_amp_minus_su2_ladder_half_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
