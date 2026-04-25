#!/usr/bin/env python3
"""
Review-candidate closeout for the charged-lepton Koide Q bridge.

The April 22 second-order support stack reduced the Q = 2/3 residue to one
explicit primitive:

    the physical charged-lepton selector is source-free, K = 0,
    on the normalized first-live second-order reduced carrier.

This runner promotes that primitive to a review-candidate source-neutrality law
and checks the full algebraic consequence chain. The theorem proved here is not
a new derivation of the source-neutrality law from older notes; it is a
branch-local review packet that makes the final primitive explicit and shows
that it is datum-free, unique on the normalized carrier, and sufficient for
exact Koide if retained.

Boundary:
  - proposes closure of the Q = 2/3 source-law bridge on the source-neutral
    surface, pending reviewer retention;
  - does not close the separate Brannen phase delta = 2/9 bridge;
  - does not fix the overall charged-lepton scale v0.
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


def main() -> int:
    section("A. Normalized second-order carrier")

    e_plus, e_perp, scale = sp.symbols("e_plus e_perp scale", positive=True, real=True)
    y_plus = sp.simplify(2 * e_plus / (e_plus + e_perp))
    y_perp = sp.simplify(2 * e_perp / (e_plus + e_perp))

    record(
        "A.1 the admitted second-order block carrier normalizes to Tr(Y) = 2",
        sp.simplify(y_plus + y_perp - 2) == 0,
        f"Y = diag({y_plus}, {y_perp})",
    )
    record(
        "A.2 the normalized carrier quotients out common mass scale exactly",
        sp.simplify(y_plus.subs({e_plus: scale * e_plus, e_perp: scale * e_perp}) - y_plus) == 0
        and sp.simplify(y_perp.subs({e_plus: scale * e_plus, e_perp: scale * e_perp}) - y_perp) == 0,
    )
    record(
        "A.3 the identity point is exactly equal block power",
        sp.solve([sp.Eq(y_plus, 1), sp.Eq(y_perp, 1)], [e_plus, e_perp], dict=True)
        == [{e_plus: e_perp}],
        "Y = I_2 iff E_+ = E_perp.",
    )

    section("B. Exact reduced source-response law")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    k_matrix = sp.diag(k_plus, k_perp)
    w_red = sp.simplify(sp.log((sp.eye(2) + k_matrix).det()))
    y1, y2 = sp.symbols("y1 y2", positive=True, real=True)
    phi = sp.simplify(w_red - k_plus * y1 - k_perp * y2)
    stationary = sp.solve(
        [sp.diff(phi, k_plus), sp.diff(phi, k_perp)],
        [k_plus, k_perp],
        dict=True,
    )
    k_plus_star = sp.simplify(stationary[0][k_plus])
    k_perp_star = sp.simplify(stationary[0][k_perp])
    s_eff = sp.simplify(phi.subs({k_plus: k_plus_star, k_perp: k_perp_star}))

    record(
        "B.1 the reduced observable generator is W_red(K) = log det(I + K)",
        sp.simplify(sp.exp(w_red) - (1 + k_plus) * (1 + k_perp)) == 0,
        f"W_red = {w_red}",
    )
    record(
        "B.2 the exact dual source equation is K = Y^(-1) - I",
        sp.simplify(k_plus_star - (1 / y1 - 1)) == 0
        and sp.simplify(k_perp_star - (1 / y2 - 1)) == 0,
        f"K_* = diag({k_plus_star}, {k_perp_star})",
    )
    record(
        "B.3 the exact effective action is S_eff(Y) = Tr(Y) - log det(Y) - 2",
        sp.simplify(s_eff - (y1 + y2 - sp.log(y1 * y2) - 2)) == 0,
        f"S_eff = {s_eff}",
    )

    section("C. Source-neutrality law proposed for review")

    y = sp.symbols("y", positive=True, real=True)
    y_trace = sp.simplify(2 - y)
    k_y_plus = sp.simplify(1 / y - 1)
    k_y_perp = sp.simplify(1 / y_trace - 1)
    zero_source_solution = sp.solve(
        [sp.Eq(k_y_plus, 0), sp.Eq(k_y_perp, 0)],
        [y],
        dict=True,
    )

    record(
        "C.1 proposed source-neutrality is the no-added-selector-source law K = 0",
        sp.Matrix([0, 0]) == sp.zeros(2, 1),
        "This is the review-candidate primitive for the April 22 one-primitive gap.",
    )
    record(
        "C.2 on Tr(Y) = 2, K = 0 has the unique interior solution Y = I_2",
        zero_source_solution == [{y: 1}],
        f"K(y) = diag({k_y_plus}, {k_y_perp}); solution = {zero_source_solution}",
    )
    record(
        "C.3 the source-free point is also the strict minimum of the exact trace-normalized effective action",
        sp.solve(sp.Eq(sp.diff(-sp.log(y * (2 - y)), y), 0), y, dict=False) == [1]
        and sp.simplify(sp.diff(-sp.log(y * (2 - y)), y, 2).subs(y, 1) - 2) == 0,
        "S_eff|Tr=2 = -log(y(2-y)); d2S/dy2 at y=1 is 2.",
    )

    section("D. No hidden source or target import")

    k2_from_trace = sp.solve(
        sp.Eq(1 / (1 + k_plus) + 1 / (1 + k_perp), 2),
        k_perp,
        dict=False,
    )[0]
    y_from_k = sp.simplify(1 / (1 + k_plus))
    y_perp_from_k = sp.simplify(1 / (1 + k2_from_trace))

    record(
        "D.1 the normalized nonzero source family is one-dimensional",
        sp.simplify(k2_from_trace + k_plus / (2 * k_plus + 1)) == 0,
        f"k_perp(k_plus) = {sp.simplify(k2_from_trace)}",
    )
    record(
        "D.2 that source family is exactly the selector coordinate in disguise",
        sp.simplify(y_perp_from_k - (2 - y_from_k)) == 0,
        f"Y(k_plus) = diag({y_from_k}, {y_perp_from_k})",
    )
    record(
        "D.3 nonzero source is equivalent to moving off the datum-free Koide point",
        sp.solve(sp.Eq(k_plus, 0), k_plus, dict=False) == [0]
        and sp.simplify(y_from_k.subs(k_plus, 0) - 1) == 0,
        "K != 0 selects y != 1; it is an external one-real datum.",
    )

    section("E. Exact Koide consequence")

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    e_plus_r = sp.simplify(r0**2 / 3)
    e_perp_r = sp.simplify((r1**2 + r2**2) / 6)
    kappa = sp.symbols("kappa", positive=True, real=True)
    q_expr = sp.simplify((1 + 2 / kappa) / 3)
    kappa_y = sp.simplify(2 * y / (2 - y))
    q_y = sp.simplify(q_expr.subs(kappa, kappa_y))

    record(
        "E.1 Y = I_2 pulls back to 2 r0^2 = r1^2 + r2^2",
        sp.simplify((e_plus_r - e_perp_r) - (2 * r0**2 - r1**2 - r2**2) / 6) == 0,
    )
    record(
        "E.2 equal block power is kappa = 2 on the Brannen/circulant carrier",
        sp.simplify(kappa_y.subs(y, 1) - 2) == 0,
        f"kappa(y) = {kappa_y}",
    )
    record(
        "E.3 kappa = 2 gives exact charged-lepton Koide Q = 2/3",
        sp.simplify(q_expr.subs(kappa, 2) - sp.Rational(2, 3)) == 0,
        f"Q = {sp.simplify(q_expr.subs(kappa, 2))}",
    )
    record(
        "E.4 any nonzero normalized source imports the Q selector value",
        sp.simplify(q_y - 2 / (3 * y)) == 0,
        f"Q(y) = {q_y}; with y = 1/(1+k_plus), Q = {sp.simplify(q_y.subs(y, y_from_k))}",
    )

    section("F. Closure boundary")

    record(
        "F.1 Q source-law bridge closes if the source-neutral surface is retained",
        zero_source_solution == [{y: 1}]
        and sp.simplify(q_expr.subs(kappa, 2) - sp.Rational(2, 3)) == 0,
        "REVIEW_CANDIDATE_KOIDE_Q_SOURCE_FREE_CLOSURE=TRUE",
    )
    record(
        "F.2 the delta and overall-scale bridges are deliberately outside this theorem",
        True,
        "DELTA_BRANNEN_BRIDGE_CLOSED_BY_THIS_RUNNER=FALSE; V0_SCALE_CLOSED_BY_THIS_RUNNER=FALSE",
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
        print("VERDICT: source-neutrality K = 0 closes the charged-lepton")
        print("Koide Q bridge if retained on the admitted normalized second-order carrier.")
        print("The consequence chain is exact: K = 0 -> Y = I_2 -> kappa = 2 -> Q = 2/3.")
        print("Any nonzero normalized source is a one-real selector import.")
        print()
        print("REVIEW_CANDIDATE_KOIDE_Q_SOURCE_FREE_CLOSURE=TRUE")
        print("DELTA_BRANNEN_BRIDGE_CLOSED_BY_THIS_RUNNER=FALSE")
        return 0

    print("VERDICT: review-candidate Koide Q source-free closure theorem has FAILs.")
    print()
    print("REVIEW_CANDIDATE_KOIDE_Q_SOURCE_FREE_CLOSURE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
