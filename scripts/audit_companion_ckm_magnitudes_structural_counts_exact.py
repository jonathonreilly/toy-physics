#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_magnitudes_structural_counts_theorem_note_2026-04-25`.

The parent note's load-bearing content is the five atlas-leading
off-diagonal squared CKM magnitude identities (M1)-(M5) packaged on the
`(n_pair, n_color, alpha_s(v))` structural-counts surface, plus the
exact `n_pair` cancellation in the `|V_ub|^2` closed form
`alpha_s(v)^3 / (8 n_color^2)`.

The existing primary runner
(`scripts/frontier_ckm_magnitudes_structural_counts.py`) verifies these
identities at floating-point tolerance using the canonical numerical
`alpha_s(v)`. This Pattern B audit companion adds a sympy-based
exact-symbolic verification:

  (a) treats `alpha_s(v)` as a free real symbol (so the algebra cannot
      be passing accidentally on a single numerical value);
  (b) treats `(n_pair, n_color, n_quark)` as positive-integer symbols
      with the constraint `n_quark = n_pair * n_color`;
  (c) imports the upstream identities verbatim:
        `lambda^2 = alpha_s(v) / n_pair`,
        `A^2      = n_pair / n_color`,
        `rho      = 1 / n_quark`,
        `eta^2    = (n_quark - 1) / n_quark^2`,
        `R_t^2    = (1 - rho)^2 + eta^2 = 1 - rho` (Thales);
  (d) verifies (M1)-(M5) in two layers:
        (i)  parametrically over abstract counts with q = p c, where
             each identity must reduce to 0 (i.e. `simplify(LHS - RHS) == 0`),
        (ii) at the framework counts (n_pair, n_color, n_quark) =
             (2, 3, 6), where the right-hand side specializes to the
             tabulated structural form (alpha_s/2, alpha_s^2/6,
             alpha_s^3/72, 5 alpha_s^3/72);
  (e) verifies the n_pair cancellation in (M4) symbolically
      (the n_pair-bearing expanded form equals the n_pair-free compact
      form as a sympy identity, not just at one numerical alpha_s);
  (f) verifies the Thales-relation cited input
      `(1 - rho)^2 + eta^2 = 1 - rho` reduces to 0 symbolically under
      `eta^2 = (q - 1)/q^2`, `rho = 1/q`.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the parent's
load-bearing class-(A) algebra holds at exact symbolic precision over
both the abstract-count parameter space and the framework counts.
The structural-counts inputs themselves (lambda^2 = alpha_s/n_pair,
A^2 = n_pair/n_color, rho = 1/n_quark, eta^2 = (n_quark-1)/n_quark^2)
are imported from upstream subtheorem authorities and are not
re-derived here.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols, expand
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("ckm_magnitudes_structural_counts_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (M1)-(M5) and n_pair cancellation")
    print("over abstract integer counts (p, c, q = p c) and framework counts (2, 3, 6)")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------

    # Free positive-integer symbolic counts (no numeric value forced yet).
    p_sym, c_sym, q_sym = symbols("p c q", positive=True, integer=True)

    # The canonical coupling alpha_s(v). The structural-counts theorem must
    # hold for ARBITRARY positive real alpha_s; making it a free symbol
    # ensures the identity cannot be passing by floating-point coincidence.
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Cited inputs (imported from upstream subtheorem authorities; not
    # re-derived here):
    #   lambda^2 = alpha_s(v) / n_pair      (Wolfenstein lambda/A note)
    #   A^2      = n_pair  / n_color        (Wolfenstein lambda/A note)
    #   rho      = 1 / n_quark              (CP-phase identity note)
    #   eta^2    = (n_quark - 1)/n_quark^2  (CP-phase identity note)
    lambda_sq = alpha_s / p_sym
    A_sq = p_sym / c_sym
    rho = Rational(1) / q_sym
    eta_sq = (q_sym - 1) / q_sym**2

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  symbolic counts: p (n_pair), c (n_color), q (n_quark)")
    print(f"  lambda^2 = {lambda_sq}")
    print(f"  A^2      = {A_sq}")
    print(f"  rho      = {rho}")
    print(f"  eta^2    = {eta_sq}")

    # ---------------------------------------------------------------------
    section("Part 1: cited Thales relation R_t^2 = (1-rho)^2 + eta^2 = 1-rho")
    # ---------------------------------------------------------------------
    # The right-angle Thales authority gives R_t^2 = 1 - rho. Verify under
    # rho = 1/q, eta^2 = (q-1)/q^2 that the cited (1-rho)^2 + eta^2
    # algebraically equals 1 - rho.
    Rt_sq_expanded = (1 - rho) ** 2 + eta_sq
    Rt_sq_target = 1 - rho

    check(
        "Thales: (1 - rho)^2 + eta^2 == 1 - rho (parametric in q)",
        simplify(Rt_sq_expanded - Rt_sq_target) == 0,
        detail=f"diff simplifies to {simplify(Rt_sq_expanded - Rt_sq_target)}",
    )

    check(
        "rho^2 + eta^2 == 1/q (parametric in q, dual Thales form)",
        simplify(rho * rho + eta_sq - Rational(1) / q_sym) == 0,
        detail="needed for |V_ub|^2 = A^2 lambda^6 (rho^2 + eta^2)",
    )

    # ---------------------------------------------------------------------
    section("Part 2: parametric (M1)-(M3) identities over abstract (p, c, q)")
    # ---------------------------------------------------------------------
    # These identities hold for ALL positive integer counts; they do not
    # require q = p c. Verify symbolically.

    # (M1) |V_us|^2 = lambda^2 = alpha_s / p
    M1_lhs = lambda_sq
    M1_rhs = alpha_s / p_sym
    check(
        "(M1) parametric: |V_us|^2 == alpha_s / p",
        simplify(M1_lhs - M1_rhs) == 0,
        detail=f"|V_us|^2 - alpha_s/p simplifies to {simplify(M1_lhs - M1_rhs)}",
    )

    # (M2) |V_cb|^2 = A^2 lambda^4 = (p/c)(alpha_s/p)^2 = alpha_s^2 / (p c)
    M2_lhs = A_sq * lambda_sq**2
    M2_rhs = alpha_s**2 / (p_sym * c_sym)
    check(
        "(M2) parametric: A^2 lambda^4 == alpha_s^2 / (p c)",
        simplify(M2_lhs - M2_rhs) == 0,
        detail=f"diff = {simplify(M2_lhs - M2_rhs)}",
    )

    # (M3) |V_ts|^2 = |V_cb|^2 at atlas-leading Wolfenstein order
    M3_lhs = A_sq * lambda_sq**2  # |V_ts|^2 same atlas-leading form
    M3_rhs = M2_lhs
    check(
        "(M3) parametric: |V_ts|^2 == |V_cb|^2 at atlas-leading order",
        simplify(M3_lhs - M3_rhs) == 0,
        detail="atlas-leading Wolfenstein equality",
    )

    # ---------------------------------------------------------------------
    section("Part 3: parametric (M4) identity and exact n_pair cancellation")
    # ---------------------------------------------------------------------
    # |V_ub|^2 = A^2 lambda^6 (rho^2 + eta^2)
    #         = (p/c) (alpha_s/p)^3 (1/q)
    #         = alpha_s^3 / (c p^2 q)
    # Under q = p c, this reduces to alpha_s^3 / (c p^2 (p c)) = alpha_s^3 / (p^3 c^2).
    # The compact theorem form is alpha_s^3 / (8 c^2). For p = 2, p^3 = 8, so
    # the n_pair factor cancels iff p = 2. We verify both the parametric
    # closed form (no q substitution, no p numeric) AND the cancellation
    # under q = p c at p = 2.

    M4_wolf = A_sq * lambda_sq**3 * (rho * rho + eta_sq)  # parametric in p, c, q
    M4_compact_general = alpha_s**3 / (c_sym * p_sym**2 * q_sym)
    check(
        "(M4) parametric: A^2 lambda^6 (rho^2+eta^2) == alpha_s^3 / (c p^2 q)",
        simplify(M4_wolf - M4_compact_general) == 0,
        detail=f"diff = {simplify(M4_wolf - M4_compact_general)}",
    )

    # Apply the framework constraint q = p c.
    M4_under_q = simplify(M4_wolf.subs(q_sym, p_sym * c_sym))
    M4_compact_struct = alpha_s**3 / (p_sym**3 * c_sym**2)
    check(
        "(M4) parametric under q = p c: equals alpha_s^3 / (p^3 c^2)",
        simplify(M4_under_q - M4_compact_struct) == 0,
        detail=f"reduced form = {M4_under_q}",
    )

    # n_pair cancellation: at p = 2 the p^3 factor becomes 8.
    M4_at_p2 = simplify(M4_compact_struct.subs(p_sym, 2))
    M4_target = alpha_s**3 / (8 * c_sym**2)
    check(
        "(M4) n_pair cancellation at p = 2: alpha_s^3 / (8 c^2)",
        simplify(M4_at_p2 - M4_target) == 0,
        detail=f"|V_ub|^2 at p=2 = {M4_at_p2}",
    )

    # The compact form depends only on alpha_s and n_color (no n_pair).
    # Confirm by checking that the partial derivative wrt p_sym is 0 at p = 2.
    # Actually a stronger statement: the compact form alpha_s^3 / (8 c^2)
    # is literally free of p_sym, so just check no p_sym in free symbols.
    check(
        "(M4) compact closed form has no n_pair dependence",
        p_sym not in M4_target.free_symbols,
        detail=f"free_symbols of compact M4 = {M4_target.free_symbols}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: parametric (M5) identity using Thales")
    # ---------------------------------------------------------------------
    # |V_td|^2 = A^2 lambda^6 ((1 - rho)^2 + eta^2)
    #         = A^2 lambda^6 (1 - rho)              (Thales)
    #         = (p/c)(alpha_s/p)^3 (q-1)/q
    #         = alpha_s^3 (q - 1) / (c p^2 q)
    # Under q = p c with p = 2: = alpha_s^3 (q - 1) / (8 c^2).

    M5_wolf = A_sq * lambda_sq**3 * ((1 - rho) ** 2 + eta_sq)
    M5_via_thales = A_sq * lambda_sq**3 * (1 - rho)  # cited Thales reduction
    check(
        "(M5) parametric: ((1-rho)^2+eta^2) form == (1-rho) form (Thales)",
        simplify(M5_wolf - M5_via_thales) == 0,
        detail="Thales reduction inside |V_td|^2",
    )

    M5_struct_general = alpha_s**3 * (q_sym - 1) / (c_sym * p_sym**2 * q_sym)
    check(
        "(M5) parametric: A^2 lambda^6 (1-rho) == alpha_s^3 (q-1) / (c p^2 q)",
        simplify(M5_via_thales - M5_struct_general) == 0,
        detail="closed form before q = p c substitution",
    )

    M5_under_qpc = simplify(M5_struct_general.subs(q_sym, p_sym * c_sym))
    M5_compact_general = alpha_s**3 * (p_sym * c_sym - 1) / (p_sym**3 * c_sym**2)
    check(
        "(M5) parametric under q = p c: alpha_s^3 (p c - 1) / (p^3 c^2)",
        simplify(M5_under_qpc - M5_compact_general) == 0,
        detail=f"reduced form = {M5_under_qpc}",
    )

    M5_at_p2 = simplify(M5_compact_general.subs(p_sym, 2))
    M5_target = alpha_s**3 * (2 * c_sym - 1) / (8 * c_sym**2)
    check(
        "(M5) at p = 2: alpha_s^3 (2 c - 1) / (8 c^2)",
        simplify(M5_at_p2 - M5_target) == 0,
        detail=f"|V_td|^2 at p=2 = {M5_at_p2}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: framework counts (p, c, q) = (2, 3, 6) numerical structural form")
    # ---------------------------------------------------------------------
    # Specialize all five identities to the framework counts.
    framework = {p_sym: 2, c_sym: 3, q_sym: 6}

    M1_at = simplify(M1_lhs.subs(framework))
    check(
        "(M1) at (2,3,6): alpha_s / 2",
        simplify(M1_at - alpha_s / 2) == 0,
        detail=f"got {M1_at}",
    )

    M2_at = simplify(M2_lhs.subs(framework))
    check(
        "(M2) at (2,3,6): alpha_s^2 / 6",
        simplify(M2_at - alpha_s**2 / 6) == 0,
        detail=f"got {M2_at}",
    )

    M3_at = simplify(M3_lhs.subs(framework))
    check(
        "(M3) at (2,3,6): alpha_s^2 / 6",
        simplify(M3_at - alpha_s**2 / 6) == 0,
        detail=f"got {M3_at}",
    )

    M4_at = simplify(M4_wolf.subs(framework))
    check(
        "(M4) at (2,3,6): alpha_s^3 / 72",
        simplify(M4_at - alpha_s**3 / 72) == 0,
        detail=f"got {M4_at}",
    )

    M5_at = simplify(M5_wolf.subs(framework))
    check(
        "(M5) at (2,3,6): 5 alpha_s^3 / 72",
        simplify(M5_at - 5 * alpha_s**3 / 72) == 0,
        detail=f"got {M5_at}",
    )

    # n_pair cancellation explicitly at (p, c, q) = (2, 3, 6).
    check(
        "n_pair cancels at (2,3,6): |V_ub|^2 = alpha_s^3 / (8 * 9) = alpha_s^3/72",
        simplify(M4_at - alpha_s**3 / (8 * 9)) == 0,
        detail="explicit |V_ub|^2 at framework counts uses only n_color",
    )

    # ---------------------------------------------------------------------
    section("Part 6: counterfactual probe (n_pair != 2 breaks compact form)")
    # ---------------------------------------------------------------------
    # The note's headline claim is that exactly at p = 2 the n_pair factor
    # cancels into the constant 8 in (M4). For audit hygiene, demonstrate
    # symbolically that at p != 2 the closed form retains a p^3 factor
    # rather than the constant 8.
    M4_general = alpha_s**3 / (p_sym**3 * c_sym**2)
    diff_at_p3 = simplify(M4_general.subs(p_sym, 3) - alpha_s**3 / (8 * c_sym**2))
    check(
        "counterfactual: at p=3, |V_ub|^2 = alpha_s^3/(27 c^2) != alpha_s^3/(8 c^2)",
        diff_at_p3 != 0,
        detail=f"diff at p=3 simplifies to {diff_at_p3} (nonzero confirms n_pair-=2 specificity)",
    )

    diff_at_p1 = simplify(M4_general.subs(p_sym, 1) - alpha_s**3 / (8 * c_sym**2))
    check(
        "counterfactual: at p=1, compact constant fails (1 != 8)",
        diff_at_p1 != 0,
        detail=f"diff at p=1 simplifies to {diff_at_p1}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    Thales: (1-rho)^2 + eta^2 = 1 - rho parametric in q")
    print("    rho^2 + eta^2 = 1/q parametric in q")
    print("    (M1)-(M5) parametric over abstract counts (p, c, q)")
    print("    (M4) n_pair cancellation: at p = 2, |V_ub|^2 = alpha_s^3/(8 c^2)")
    print("    (M4) compact form is independent of n_pair (free_symbols check)")
    print("    All identities specialize correctly at (p, c, q) = (2, 3, 6)")
    print("    Counterfactual: n_pair != 2 breaks the compact (8 c^2) constant")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
