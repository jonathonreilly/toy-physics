#!/usr/bin/env python3
"""Verify the CKM inverse-square structural sum-rule narrow theorem.

The narrow theorem note
`CKM_INVERSE_SQUARE_STRUCTURAL_SUM_RULE_NARROW_THEOREM_NOTE_2026-05-10.md`
states a purely abstract polynomial-algebra theorem on:

  - abstract positive real symbols (n_pair, n_color), with algebraic
    quantities rho, A^2, and eta^2 satisfying the parametric input identities
      (H1)  rho   = 1 / (n_pair * n_color),
      (H2)  A^2   = n_pair / n_color,
      (H3)  eta^2 = 1 / n_pair^2 - 1 / n_color^2.

Conclusions:

  (T1) rho * A^2 = 1 / n_color^2;
  (T2) eta^2 + rho * A^2 = 1 / n_pair^2;
  (T3) eta^2 + 2 * rho * A^2 = 1 / n_pair^2 + 1 / n_color^2;
  (T4) real-eta gate: eta^2 > 0 iff n_color > n_pair;
  (C1) (T3) - (T2) = (T1) = 1 / n_color^2;
  (T5) explicit non-trivial points on the identity surface, including
       the parent-atlas framework readout (n_pair, n_color) = (2, 3).

This runner exhibits each conclusion symbolically (exact rational /
real symbol algebra via sympy) and verifies numerical instances at
exact precision. No framework / audit / lattice module is imported;
only sympy.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def is_zero(expr) -> bool:
    """Return True iff sympy can simplify `expr` to identically zero."""
    return simplify(expr) == 0


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


def main() -> int:
    print("CKM inverse-square structural sum-rule narrow theorem check")
    print()

    # ------------------------------------------------------------------
    # Setup: abstract positive n_pair,n_color symbols and parametric hypothesis system
    # ------------------------------------------------------------------
    n_pair = Symbol("n_pair", positive=True, real=True)
    n_color = Symbol("n_color", positive=True, real=True)

    # Hypotheses (defined as explicit expressions in n_pair, n_color)
    rho = 1 / (n_pair * n_color)              # (H1)
    A_sq = n_pair / n_color                    # (H2)
    eta_sq = 1 / n_pair**2 - 1 / n_color**2    # (H3)

    # ------------------------------------------------------------------
    section("Part 1: (T1) product identity rho * A^2 = 1 / n_color^2")
    # ------------------------------------------------------------------
    T1_lhs = rho * A_sq
    T1_rhs = 1 / n_color**2
    T1_diff = simplify(T1_lhs - T1_rhs)
    check(
        "(1) (T1) rho * A^2 = 1/n_color^2 symbolically",
        T1_diff == 0,
        detail=f"diff = {T1_diff}",
    )

    # ------------------------------------------------------------------
    section("Part 2: (T2) first sum-rule eta^2 + rho * A^2 = 1 / n_pair^2")
    # ------------------------------------------------------------------
    T2_lhs = eta_sq + rho * A_sq
    T2_rhs = 1 / n_pair**2
    T2_diff = simplify(T2_lhs - T2_rhs)
    check(
        "(2) (T2) eta^2 + rho * A^2 = 1/n_pair^2 symbolically",
        T2_diff == 0,
        detail=f"diff = {T2_diff}",
    )

    # ------------------------------------------------------------------
    section("Part 3: (T3) second sum-rule eta^2 + 2 rho A^2 = 1/n_pair^2 + 1/n_color^2")
    # ------------------------------------------------------------------
    T3_lhs = eta_sq + 2 * rho * A_sq
    T3_rhs = 1 / n_pair**2 + 1 / n_color**2
    T3_diff = simplify(T3_lhs - T3_rhs)
    check(
        "(3) (T3) eta^2 + 2*rho*A^2 = 1/n_pair^2 + 1/n_color^2 symbolically",
        T3_diff == 0,
        detail=f"diff = {T3_diff}",
    )

    # ------------------------------------------------------------------
    section("Part 4: (T4) real-eta gate eta^2 > 0 iff n_color > n_pair")
    # ------------------------------------------------------------------
    # eta^2 = (n_color^2 - n_pair^2) / (n_pair^2 n_color^2)
    #       = (n_color - n_pair)(n_color + n_pair) / (n_pair^2 n_color^2)
    eta_sq_factored = (
        (n_color - n_pair) * (n_color + n_pair) / (n_pair**2 * n_color**2)
    )
    T4_diff = simplify(eta_sq - eta_sq_factored)
    check(
        "(4) (T4) eta^2 factorizes as (n_color-n_pair)(n_color+n_pair) / (n_pair n_color)^2",
        T4_diff == 0,
        detail=f"diff = {T4_diff}",
    )
    # Denominator is positive (positive symbols), and (n_color + n_pair) is
    # positive. So sign(eta^2) = sign(n_color - n_pair).
    # We verify this on representative tuples (sign check):
    eta_sq_at_23 = eta_sq.subs({n_pair: Rational(2), n_color: Rational(3)})
    eta_sq_at_32 = eta_sq.subs({n_pair: Rational(3), n_color: Rational(2)})
    eta_sq_at_22 = eta_sq.subs({n_pair: Rational(2), n_color: Rational(2)})
    check(
        "(5) (T4) positivity at (2,3): eta^2 = 5/36 > 0 (n_color > n_pair)",
        simplify(eta_sq_at_23 - Rational(5, 36)) == 0 and eta_sq_at_23 > 0,
        detail=f"eta^2(2,3) = {eta_sq_at_23}",
    )
    check(
        "(6) (T4) negativity at (3,2): eta^2 = -5/36 < 0 (n_color < n_pair)",
        simplify(eta_sq_at_32 + Rational(5, 36)) == 0 and eta_sq_at_32 < 0,
        detail=f"eta^2(3,2) = {eta_sq_at_32}",
    )
    check(
        "(7) (T4) zero at (2,2): eta^2 = 0 (n_color = n_pair, boundary)",
        eta_sq_at_22 == 0,
        detail=f"eta^2(2,2) = {eta_sq_at_22}",
    )

    # ------------------------------------------------------------------
    section("Part 5: (C1) corollary (T3) - (T2) = (T1) = 1/n_color^2")
    # ------------------------------------------------------------------
    C1_lhs = T3_lhs - T2_lhs
    C1_rhs = T1_lhs
    C1_diff = simplify(C1_lhs - C1_rhs)
    check(
        "(8) (C1) (eta^2 + 2 rho*A^2) - (eta^2 + rho*A^2) = rho*A^2 symbolically",
        C1_diff == 0,
        detail=f"diff = {C1_diff}",
    )
    # Also verify it equals 1/n_color^2
    C1_alt = simplify(C1_lhs - 1 / n_color**2)
    check(
        "(9) (C1-alt) (T3) - (T2) = 1/n_color^2 symbolically",
        C1_alt == 0,
        detail=f"diff = {C1_alt}",
    )

    # ------------------------------------------------------------------
    section("Part 6: (T5-A) concrete framework instance (n_pair, n_color) = (2, 3)")
    # ------------------------------------------------------------------
    subs_23 = {n_pair: Rational(2), n_color: Rational(3)}
    rho_23 = rho.subs(subs_23)
    A_sq_23 = A_sq.subs(subs_23)
    eta_sq_23 = eta_sq.subs(subs_23)
    rhoA2_23 = simplify((rho * A_sq).subs(subs_23))
    T2_23 = simplify(T2_lhs.subs(subs_23))
    T3_23 = simplify(T3_lhs.subs(subs_23))
    check(
        "(10) (T5-A) (2,3): rho = 1/6",
        rho_23 == Rational(1, 6),
        detail=f"rho = {rho_23}",
    )
    check(
        "(11) (T5-A) (2,3): A^2 = 2/3",
        A_sq_23 == Rational(2, 3),
        detail=f"A^2 = {A_sq_23}",
    )
    check(
        "(12) (T5-A) (2,3): eta^2 = 5/36",
        eta_sq_23 == Rational(5, 36),
        detail=f"eta^2 = {eta_sq_23}",
    )
    check(
        "(13) (T5-A) (2,3): rho * A^2 = 1/9",
        rhoA2_23 == Rational(1, 9),
        detail=f"rho*A^2 = {rhoA2_23}",
    )
    check(
        "(14) (T5-A) (2,3): eta^2 + rho*A^2 = 1/4",
        T2_23 == Rational(1, 4),
        detail=f"T2-sum = {T2_23}",
    )
    check(
        "(15) (T5-A) (2,3): eta^2 + 2*rho*A^2 = 13/36",
        T3_23 == Rational(13, 36),
        detail=f"T3-sum = {T3_23}",
    )

    # ------------------------------------------------------------------
    section("Part 7: (T5-B) concrete non-framework instance (n_pair, n_color) = (3, 4)")
    # ------------------------------------------------------------------
    subs_34 = {n_pair: Rational(3), n_color: Rational(4)}
    rho_34 = rho.subs(subs_34)
    A_sq_34 = A_sq.subs(subs_34)
    eta_sq_34 = eta_sq.subs(subs_34)
    rhoA2_34 = simplify((rho * A_sq).subs(subs_34))
    T2_34 = simplify(T2_lhs.subs(subs_34))
    T3_34 = simplify(T3_lhs.subs(subs_34))
    check(
        "(16) (T5-B) (3,4): rho = 1/12",
        rho_34 == Rational(1, 12),
        detail=f"rho = {rho_34}",
    )
    check(
        "(17) (T5-B) (3,4): A^2 = 3/4",
        A_sq_34 == Rational(3, 4),
        detail=f"A^2 = {A_sq_34}",
    )
    check(
        "(18) (T5-B) (3,4): eta^2 = 7/144",
        eta_sq_34 == Rational(7, 144),
        detail=f"eta^2 = {eta_sq_34}",
    )
    check(
        "(19) (T5-B) (3,4): rho * A^2 = 1/16",
        rhoA2_34 == Rational(1, 16),
        detail=f"rho*A^2 = {rhoA2_34}",
    )
    check(
        "(20) (T5-B) (3,4): eta^2 + rho*A^2 = 1/9",
        T2_34 == Rational(1, 9),
        detail=f"T2-sum = {T2_34}",
    )
    check(
        "(21) (T5-B) (3,4): eta^2 + 2*rho*A^2 = 25/144",
        T3_34 == Rational(25, 144),
        detail=f"T3-sum = {T3_34}",
    )

    # ------------------------------------------------------------------
    section("Part 8: (T5-C) concrete extreme instance (n_pair, n_color) = (1, 2)")
    # ------------------------------------------------------------------
    subs_12 = {n_pair: Rational(1), n_color: Rational(2)}
    rho_12 = rho.subs(subs_12)
    A_sq_12 = A_sq.subs(subs_12)
    eta_sq_12 = eta_sq.subs(subs_12)
    rhoA2_12 = simplify((rho * A_sq).subs(subs_12))
    T2_12 = simplify(T2_lhs.subs(subs_12))
    T3_12 = simplify(T3_lhs.subs(subs_12))
    check(
        "(22) (T5-C) (1,2): rho = 1/2",
        rho_12 == Rational(1, 2),
        detail=f"rho = {rho_12}",
    )
    check(
        "(23) (T5-C) (1,2): A^2 = 1/2",
        A_sq_12 == Rational(1, 2),
        detail=f"A^2 = {A_sq_12}",
    )
    check(
        "(24) (T5-C) (1,2): eta^2 = 3/4",
        eta_sq_12 == Rational(3, 4),
        detail=f"eta^2 = {eta_sq_12}",
    )
    check(
        "(25) (T5-C) (1,2): rho * A^2 = 1/4",
        rhoA2_12 == Rational(1, 4),
        detail=f"rho*A^2 = {rhoA2_12}",
    )
    check(
        "(26) (T5-C) (1,2): eta^2 + rho*A^2 = 1",
        T2_12 == Rational(1),
        detail=f"T2-sum = {T2_12}",
    )
    check(
        "(27) (T5-C) (1,2): eta^2 + 2*rho*A^2 = 5/4",
        T3_12 == Rational(5, 4),
        detail=f"T3-sum = {T3_12}",
    )

    # ------------------------------------------------------------------
    section("Part 9: (T5-D) cross-instance independence check at non-integer (n_pair, n_color)")
    # ------------------------------------------------------------------
    # Even at non-integer positive reals (e.g. (sqrt(2), pi)), the
    # symbolic identities (T1)-(T3) hold by their universal substitution.
    subs_sym = {n_pair: sqrt(Rational(2)), n_color: Rational(7, 2)}
    T1_sym = simplify((rho * A_sq).subs(subs_sym) - (1 / n_color**2).subs(subs_sym))
    T2_sym = simplify(T2_lhs.subs(subs_sym) - T2_rhs.subs(subs_sym))
    T3_sym = simplify(T3_lhs.subs(subs_sym) - T3_rhs.subs(subs_sym))
    check(
        "(28) (T5-D) (sqrt(2), 7/2): T1 holds at non-integer tuple",
        T1_sym == 0,
        detail=f"T1 diff = {T1_sym}",
    )
    check(
        "(29) (T5-D) (sqrt(2), 7/2): T2 holds at non-integer tuple",
        T2_sym == 0,
        detail=f"T2 diff = {T2_sym}",
    )
    check(
        "(30) (T5-D) (sqrt(2), 7/2): T3 holds at non-integer tuple",
        T3_sym == 0,
        detail=f"T3 diff = {T3_sym}",
    )

    # ------------------------------------------------------------------
    section("Narrow theorem summary")
    # ------------------------------------------------------------------
    print(
        """
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let n_pair > 0 and n_color > 0 be abstract positive real symbols,
    with rho, A^2, and eta^2 satisfying
        (H1)  rho      = 1 / (n_pair * n_color),
        (H2)  A^2      = n_pair / n_color,
        (H3)  eta^2    = 1 / n_pair^2  -  1 / n_color^2.

  CONCLUSION:
    (T1)  rho * A^2  =  1 / n_color^2.
    (T2)  eta^2 + rho * A^2  =  1 / n_pair^2.
    (T3)  eta^2 + 2 * rho * A^2  =  1 / n_pair^2 + 1 / n_color^2.
    (T4)  Real-eta gate: eta^2 > 0  iff  n_color > n_pair.
    (C1)  (T3) - (T2) = (T1) = 1 / n_color^2.
    (T5)  Specific instances:
           (2,3): rho=1/6, A^2=2/3, eta^2=5/36, rho*A^2=1/9,
                  T2-sum=1/4, T3-sum=13/36;
           (3,4): rho=1/12, A^2=3/4, eta^2=7/144, rho*A^2=1/16,
                  T2-sum=1/9, T3-sum=25/144;
           (1,2): rho=1/2, A^2=1/2, eta^2=3/4, rho*A^2=1/4,
                  T2-sum=1, T3-sum=5/4.

  Audit-lane class:
    (A) — pure polynomial algebra over positive n_pair,n_color symbols.
    No physical Cl(3) local algebra, Z^3 spatial substrate, CKM atlas,
    projector split, alpha_s, Wolfenstein coordinate identification,
    charged-lepton, staggered-Dirac, PMNS, PDG observable, or specific
    count tuple is consumed.

  This narrow theorem isolates the polynomial-algebra inverse-square
  sum-rule from any physical CKM atlas / Wolfenstein / inverse-square
  upstream framing.
"""
    )

    print(f"\nTOTAL: PASS={PASS}, FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
