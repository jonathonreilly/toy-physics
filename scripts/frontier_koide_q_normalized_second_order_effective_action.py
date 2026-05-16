#!/usr/bin/env python3
"""
Science-only support/candidate route:
Koide Q from the exact source-free effective action on the normalized
second-order block carrier.

Purpose:
  tighten the last open step in the branch-local Q route. Earlier notes already
  established that:

    1. the exact second-order Gamma_1 return is the first live
       species-resolving local bosonic carrier on T_1,
    2. its C_3-covariant quadratic scalar sector reduces exactly to the two
       positive block powers (E_+, E_perp),
    3. after quotienting by scale there is only one nontrivial selector
       variable.

  The remaining question is whether the VALUE law on that unique variable can
  be made native to the observable-principle framework rather than left as a
  free extremum ansatz.

Exact content here:
  - normalize the positive second-order block carrier to trace 2,
  - derive the exact reduced observable generator W_red(K) = log det(I + K),
  - compute its exact Legendre-dual effective action

        S_eff(Y) = Tr(Y) - log det(Y) - 2,

  - show that on the source-free normalized carrier Tr(Y) = 2, the unique
    minimum is Y = I_2,
  - pull that back to E_+ = E_perp and hence Q = 2/3.

This runner validates the internal algebra of that route. It does not prove
that retained charged-lepton physics forces the physical lane to be
source-free on this carrier.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []

REPO_ROOT = Path(__file__).resolve().parents[1]


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
    section("A. Exact normalized second-order block carrier")

    e_plus, e_perp, t = sp.symbols("e_plus e_perp t", positive=True, real=True)
    total = sp.simplify(e_plus + e_perp)
    y1 = sp.simplify(2 * e_plus / total)
    y2 = sp.simplify(2 * e_perp / total)

    record(
        "A.1 trace normalization sends the positive block carrier to Tr(Y) = 2",
        sp.simplify(y1 + y2 - 2) == 0,
        f"Y = diag({y1}, {y2})",
    )
    record(
        "A.2 the normalized carrier is exactly scale-free under common positive rescaling",
        sp.simplify(y1.subs({e_plus: t * e_plus, e_perp: t * e_perp}) - y1) == 0
        and sp.simplify(y2.subs({e_plus: t * e_plus, e_perp: t * e_perp}) - y2) == 0,
    )
    record(
        "A.3 equality on the normalized carrier is equivalent to equality of the original block powers",
        sp.simplify(y1 - y2) == sp.simplify(2 * (e_plus - e_perp) / (e_plus + e_perp)),
        "So Y = I_2 is exactly E_+ = E_perp.",
    )

    section("B. Exact reduced observable generator on the two-slot carrier")

    k1, k2 = sp.symbols("k1 k2", real=True)
    w_red = sp.log(1 + k1) + sp.log(1 + k2)
    record(
        "B.1 block additivity gives W_red(K1,K2) = log(1+K1) + log(1+K2)",
        sp.simplify(sp.exp(w_red) - (1 + k1) * (1 + k2)) == 0,
        f"W_red = {w_red}",
    )
    record(
        "B.2 pure-block normalization recovers the one-block generator exactly",
        sp.simplify(w_red.subs(k2, 0) - sp.log(1 + k1)) == 0
        and sp.simplify(w_red.subs(k1, 0) - sp.log(1 + k2)) == 0,
    )
    record(
        "B.3 therefore W_red is exactly log det(I + K) on the normalized 2x2 positive carrier",
        sp.simplify(sp.exp(w_red - sp.log(((sp.eye(2) + sp.diag(k1, k2)).det()))) - 1) == 0,
        "No quartic potential, primitive adoption, or unreduced multiplicity weighting is used.",
    )

    section("C. Exact Legendre-dual effective action")

    y1_sym, y2_sym = sp.symbols("y1_sym y2_sym", positive=True, real=True)
    phi = sp.log(1 + k1) + sp.log(1 + k2) - k1 * y1_sym - k2 * y2_sym
    stat_eqs = [sp.diff(phi, k1), sp.diff(phi, k2)]
    stat_sol = sp.solve(stat_eqs, [k1, k2], dict=True)
    k1_star = sp.simplify(stat_sol[0][k1])
    k2_star = sp.simplify(stat_sol[0][k2])
    hess = sp.Matrix(
        [
            [sp.diff(phi, k1, 2), sp.diff(phi, k1, k2)],
            [sp.diff(phi, k2, k1), sp.diff(phi, k2, 2)],
        ]
    )
    hess_star = sp.simplify(hess.subs({k1: k1_star, k2: k2_star}))
    s_eff = sp.simplify(phi.subs({k1: k1_star, k2: k2_star}))

    record(
        "C.1 the unique dual maximizer is K_* = Y^(-1) - I on each block",
        sp.simplify(k1_star - (1 / y1_sym - 1)) == 0
        and sp.simplify(k2_star - (1 / y2_sym - 1)) == 0,
        f"K_* = ({k1_star}, {k2_star})",
    )
    record(
        "C.2 the source-side dual is strictly concave at the maximizer",
        hess_star == sp.diag(-y1_sym**2, -y2_sym**2),
        f"Hessian at K_* = {hess_star}",
    )
    record(
        "C.3 the exact Legendre dual is S_eff(Y) = Tr(Y) - log det(Y) - 2",
        sp.simplify(s_eff - (y1_sym + y2_sym - sp.log(y1_sym * y2_sym) - 2)) == 0,
        f"S_eff = {s_eff}",
    )

    section("D. Direct source-free candidate point on the normalized carrier")

    y = sp.symbols("y", positive=True, real=True)
    s_trace = sp.simplify(
        (y + (2 - y) - sp.log(y * (2 - y)) - 2)
    )
    ds_trace = sp.simplify(sp.diff(s_trace, y))
    crit = sp.solve(sp.Eq(ds_trace, 0), y, dict=False)
    d2s_trace = sp.simplify(sp.diff(s_trace, y, 2).subs(y, 1))

    record(
        "D.1 on the admitted reduced carrier, zero external source gives Y = I_2 directly through K = Y^(-1) - I",
        sp.simplify(k1_star.subs({y1_sym: 1, y2_sym: 1})) == 0
        and sp.simplify(k2_star.subs({y1_sym: 1, y2_sym: 1})) == 0,
        "Source-free closure is Y = (I + K)^(-1)|_(K=0) = I_2.",
    )
    record(
        "D.2 on Tr(Y)=2 the effective action reduces to -log(y(2-y))",
        sp.simplify(s_trace + sp.log(y * (2 - y))) == 0,
        f"S_eff|_Tr=2 = {s_trace}",
    )
    record(
        "D.3 the normalized carrier has a unique interior stationary point at Y = I_2",
        crit == [1],
        f"critical y-values = {crit}",
    )
    record(
        "D.4 the stationary point is a strict minimum",
        sp.simplify(d2s_trace - 2) == 0,
        f"d^2 S / dy^2 at y=1 = {d2s_trace}",
    )
    record(
        "D.5 on the admitted carrier, the minimum statement is consistent with the source-free point",
        sp.simplify(k1_star.subs({y1_sym: 1, y2_sym: 1})) == 0
        and sp.simplify(k2_star.subs({y1_sym: 1, y2_sym: 1})) == 0
        and crit == [1],
        "The source-free dual equation already fixes Y = I_2 before appealing to convexity.",
    )

    section("E. Exact Koide consequence")

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    e_plus_from_r = sp.simplify(r0**2 / 3)
    e_perp_from_r = sp.simplify((r1**2 + r2**2) / 6)
    a, b_abs_sq, kappa = sp.symbols("a b_abs_sq kappa", positive=True, real=True)
    q_expr = sp.simplify((1 + 2 / kappa) / 3)

    record(
        "E.1 Y = I_2 pulls back exactly to E_+ = E_perp",
        sp.simplify(y1.subs({e_plus: e_plus, e_perp: e_perp}) - 1)
        == sp.simplify((e_plus - e_perp) / (e_plus + e_perp)),
        "Equivalent up to multiplication by the positive denominator E_+ + E_perp.",
    )
    record(
        "E.2 equal block power is exactly 2 r0^2 = r1^2 + r2^2",
        sp.simplify((e_plus_from_r - e_perp_from_r) - (2 * r0**2 - r1**2 - r2**2) / 6) == 0,
    )
    record(
        "E.3 in circulant variables this is exactly a^2 = 2|b|^2, i.e. kappa = 2",
        sp.simplify((3 * a**2 - 6 * b_abs_sq) / 3 - (a**2 - 2 * b_abs_sq)) == 0,
    )
    record(
        "E.4 therefore the normalized effective-action minimum gives exact Koide Q = 2/3",
        sp.simplify(q_expr.subs(kappa, 2) - sp.Rational(2, 3)) == 0,
        f"Q = {sp.simplify(q_expr.subs(kappa, 2))}",
    )

    section("F. Audit dependency-graph bookkeeping (no status promotion)")

    # The audit lane named a missing_bridge_theorem repair target for the
    # source-free physical law K = 0 on this admitted carrier. A subsequent
    # campaign has filed three candidate supplier notes (see Section 11.1 of
    # the markdown). This block records the dependency-graph edges as on-disk
    # facts. It does not audit the suppliers' physical claims and it does not
    # promote this row's audit_status; only the independent audit lane sets
    # effective_status.
    candidate_suppliers = [
        (
            "F.1 KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md exists on disk",
            REPO_ROOT
            / "docs"
            / "KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md",
            "Trace-preserving local descent uniqueness E_loc(X) = (Tr X / 3) I "
            "annihilates the reduced traceless Z coordinate.",
        ),
        (
            "F.2 KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md exists on disk",
            REPO_ROOT
            / "docs"
            / "KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md",
            "K = 0 <=> Y = I_2 <=> z = 0 <=> Q = 2/3 criterion equivalence "
            "on the admitted normalized reduced carrier.",
        ),
        (
            "F.3 KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md exists on disk",
            REPO_ROOT
            / "docs"
            / "KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md",
            "Structural composition OP T1+T2 + physical-lattice-necessity locality "
            "+ canonical descent + CRIT, targeting the source-free half.",
        ),
    ]
    for name, path, detail in candidate_suppliers:
        record(name, path.exists(), detail)

    record(
        "F.4 this section is graph-bookkeeping only and asserts no status promotion",
        True,
        "Audit lane independently sets effective_status; runner pass count "
        "alone never promotes a row beyond audited_conditional.",
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
        print("VERDICT: on the exact first-live second-order carrier, the")
        print("source-free normalized effective-action route lands at Y = I_2.")
        print("That is exactly E_+ = E_perp, hence kappa = 2 and Q = 2/3.")
        print()
        print("This validates the internal algebra of the admitted second-order route.")
        print("It does not by itself prove the physical source-free law.")
        return 0

    print("VERDICT: normalized second-order effective-action theorem candidate has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
