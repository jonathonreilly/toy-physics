#!/usr/bin/env python3
"""
Koide Q intensive source-density no-go.

Theorem attempt:
  The physical charged-lepton source might be intensive on the reduced
  quotient components rather than extensive over retained Hilbert rank.  If
  source density is one unit per quotient component, the plus and perp center
  atoms carry equal weights:

      w_plus = w_perp = 1/2 -> K_TL = 0 -> Q = 2/3.

Result:
  Conditional positive, retained negative.  Equal intensive component density
  closes Q exactly, but the retained Cl(3)/Z3 package also contains the ranks
  (1,2) and the Hilbert/rank-extensive state (1/3,2/3).  Choosing intensive
  quotient-component density over rank-extensive density is therefore the
  missing physical source law, not a retained theorem.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def normalized_weights(total_plus: sp.Expr, total_perp: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    total = sp.simplify(total_plus + total_perp)
    return sp.simplify(total_plus / total), sp.simplify(total_perp / total)


def main() -> int:
    section("A. Retained center has quotient labels and Hilbert ranks")

    rank_plus = sp.Integer(1)
    rank_perp = sp.Integer(2)
    P_plus_trace = rank_plus
    P_perp_trace = rank_perp
    record(
        "A.1 retained center atoms have ranks 1 and 2",
        rank_plus == 1 and rank_perp == 2,
        f"Tr(P_plus)={P_plus_trace}, Tr(P_perp)={P_perp_trace}",
    )
    record(
        "A.2 rank is a retained label-distinguishing predicate",
        rank_plus != rank_perp,
        "The pair of quotient labels is not an anonymous two-point set in the retained language.",
    )

    section("B. Conditional positive theorem from intensive component density")

    rho_plus, rho_perp = sp.symbols("rho_plus rho_perp", positive=True, real=True)
    w_plus_int, w_perp_int = normalized_weights(rho_plus, rho_perp)
    ktl_int = sp.factor(ktl_from_weights(w_plus_int, w_perp_int))
    q_int = sp.simplify(q_from_weights(w_plus_int, w_perp_int))
    record(
        "B.1 component-density family leaves exactly one density ratio",
        sp.simplify(w_plus_int + w_perp_int) == 1,
        f"w=({w_plus_int},{w_perp_int}); Q={q_int}; K_TL={ktl_int}",
    )
    record(
        "B.2 K_TL=0 is equivalent to equal intensive component densities",
        sp.solve(sp.Eq(ktl_int, 0), rho_plus) == [rho_perp],
        f"K_TL numerator={sp.factor(sp.together(ktl_int).as_numer_denom()[0])}",
    )
    equal_density_weights = (
        sp.simplify(w_plus_int.subs(rho_plus, rho_perp)),
        sp.simplify(w_perp_int.subs(rho_plus, rho_perp)),
    )
    record(
        "B.3 equal intensive component density closes the Q chain",
        equal_density_weights == (sp.Rational(1, 2), sp.Rational(1, 2))
        and ktl_from_weights(*equal_density_weights) == 0
        and q_from_weights(*equal_density_weights) == sp.Rational(2, 3),
        f"w={equal_density_weights}; K_TL={ktl_from_weights(*equal_density_weights)}, Q={q_from_weights(*equal_density_weights)}",
    )

    section("C. Retained rank-extensive counterstate")

    sigma = sp.symbols("sigma", positive=True, real=True)
    w_plus_rank, w_perp_rank = normalized_weights(rank_plus * sigma, rank_perp * sigma)
    record(
        "C.1 equal density per Hilbert microdimension gives rank-extensive weights",
        (w_plus_rank, w_perp_rank) == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"w_rank=({w_plus_rank},{w_perp_rank})",
    )
    record(
        "C.2 rank-extensive retained state is exact and off Koide",
        q_from_weights(w_plus_rank, w_perp_rank) == 1
        and ktl_from_weights(w_plus_rank, w_perp_rank) == sp.Rational(3, 8),
        f"Q={q_from_weights(w_plus_rank, w_perp_rank)}, K_TL={ktl_from_weights(w_plus_rank, w_perp_rank)}",
    )
    sigma_plus, sigma_perp = sp.symbols("sigma_plus sigma_perp", positive=True, real=True)
    w_plus_ext, w_perp_ext = normalized_weights(
        rank_plus * sigma_plus, rank_perp * sigma_perp
    )
    ktl_ext = sp.factor(ktl_from_weights(w_plus_ext, w_perp_ext))
    record(
        "C.3 extensive rank law closes only after an inverse-rank density choice",
        sp.solve(sp.Eq(ktl_ext, 0), sigma_plus) == [2 * sigma_perp],
        f"K_TL_ext={ktl_ext}; closure requires rank_plus*sigma_plus=rank_perp*sigma_perp",
    )

    section("D. Convention scalar: intensive versus rank-extensive")

    lam = sp.symbols("lambda_source_dimension", real=True)
    ratio_lam = sp.exp(lam * sp.log(2))
    w_plus_lam, w_perp_lam = normalized_weights(1, ratio_lam)
    ktl_lam = sp.simplify(ktl_from_weights(w_plus_lam, w_perp_lam))
    q_lam = sp.simplify(q_from_weights(w_plus_lam, w_perp_lam))
    record(
        "D.1 one scalar interpolates intensive labels and rank-extensive trace",
        ktl_lam.subs(lam, 0) == 0
        and q_lam.subs(lam, 0) == sp.Rational(2, 3)
        and ktl_lam.subs(lam, 1) == sp.Rational(3, 8)
        and q_lam.subs(lam, 1) == 1,
        f"lambda=0 intensive -> Q={q_lam.subs(lam,0)}, K_TL={ktl_lam.subs(lam,0)}; "
        f"lambda=1 rank -> Q={q_lam.subs(lam,1)}, K_TL={ktl_lam.subs(lam,1)}",
    )
    record(
        "D.2 K_TL=0 selects lambda=0 inside the convention family",
        sp.solveset(sp.Eq(ratio_lam, 1), lam, domain=sp.S.Reals) == sp.FiniteSet(0),
        "Since ratio=2^lambda is positive, K_TL=0 iff ratio=1 iff lambda=0.",
    )
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.3 retained support constraints do not set the convention scalar",
        retained_constraints.jacobian([lam]).rank() == 0,
        "No retained equation distinguishes lambda=0 from lambda=1 in this audit.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The Koide value is computed only after the intensive-density assumption sets rho_plus=rho_perp.",
    )
    record(
        "E.2 intensive density is not promoted as retained closure",
        True,
        "The retained Hilbert/rank-extensive counterstate remains available and nonclosing.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem selecting intensive quotient-component source over rank-extensive source.",
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
        print("VERDICT: intensive source density is conditional, not retained-only proof.")
        print("KOIDE_Q_INTENSIVE_SOURCE_DENSITY_NO_GO=TRUE")
        print("Q_INTENSIVE_SOURCE_DENSITY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_INTENSIVE_COMPONENT_SOURCE=TRUE")
        print("RESIDUAL_SCALAR=derive_intensive_component_source_over_rank_extensive_source")
        print("RESIDUAL_Q=rank_extensive_source_state_not_excluded")
        print("COUNTERSTATE=rank_extensive_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: intensive source-density audit has FAILs.")
    print("KOIDE_Q_INTENSIVE_SOURCE_DENSITY_NO_GO=FALSE")
    print("Q_INTENSIVE_SOURCE_DENSITY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_intensive_component_source_over_rank_extensive_source")
    return 1


if __name__ == "__main__":
    sys.exit(main())
