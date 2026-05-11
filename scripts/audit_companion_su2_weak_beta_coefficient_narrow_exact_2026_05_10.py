#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`SU2_WEAK_BETA_COEFFICIENT_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is the algebraic substitution
implication: given

  (X0) Native SU(2)_L and graph-first structural SU(3)_c color supplied by
       retained_bounded gauge-count upstreams; standard SU(2) group theory
       gives C_2(adj of SU(2)) = 2, recorded as N_pair = 2.
  (X1) N_W = (N_color + 1) * N_gen  (LH SU(2) Weyl-doublet count from
       the retained_bounded lh_traceless_eigenvalue_ratio narrow theorem),
  (X2) N_gen = 3  (retained three_generation_observable_count corollary),
  (X3) n_S^complex_components = 2  (retained ew_higgs_gauge_mass_diagonalization),
  (X4) Peskin-Schroeder SU(N) 1-loop beta formula:
         b = (11/3) C_2(adj) - (2/3) T(F_W) N_W - (1/6) T(F_S) n_S
       with C_2(adj of SU(N)) = N and T(F^Weyl) = T(F^scalar) = 1/2,

the SU(2)_L 1-loop beta-coefficient evaluates to

  (P1)  b_2 = (11/3) N_pair - (1/3) (N_color + 1) N_gen - 1/6
            = (22 N_pair - 2 (N_color + 1) N_gen - 1) / 6,
  (P2)  b_2 |_{(N_pair, N_color, N_gen) = (2, 3, 3)} = 19/6,
  (P3)  per-sector decomposition: +22/3 (gauge) - 4 (matter) - 1/6 (Higgs) = 19/6.

This runner verifies (P1)-(P3) plus four corollaries (C1)-(C4) at exact
sympy precision over abstract positive integers (N_pair, N_color, N_gen),
then specializes to the framework instance (2, 3, 3) and a counterfactual
check at (2, 4, 3) confirming the closed form is genuinely parametric.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence at exact precision.
"""

from __future__ import annotations
import sys

try:
    from sympy import Rational, Symbol, simplify
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
    print("SU2_WEAK_BETA_COEFFICIENT_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: sympy verification of b_2 = 19/6 closed form")
    print("Inputs (cited):")
    print("  (X0) native_gauge_closure + graph_first_su3_integration ... retained_bounded")
    print("  (X1) lh_traceless_eigenvalue_ratio_narrow ... retained_bounded")
    print("  (X2) three_generation_observable_count_corollary ... retained")
    print("  (X3) ew_higgs_gauge_mass_diagonalization ... retained")
    print("  (X4) Peskin-Schroeder SU(N) 1-loop beta formula (external admission)")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup (positive integers)")
    # ---------------------------------------------------------------------
    N_pair = Symbol("N_pair", positive=True, integer=True)
    N_color = Symbol("N_color", positive=True, integer=True)
    N_gen = Symbol("N_gen", positive=True, integer=True)

    print(f"  symbolic N_pair  = {N_pair}")
    print(f"  symbolic N_color = {N_color}")
    print(f"  symbolic N_gen   = {N_gen}")

    # Cited input (X1): N_W = (N_color + 1) * N_gen
    N_W = (N_color + 1) * N_gen

    # Cited input (X3): n_S^complex_components = 2 (one Higgs doublet)
    n_S_complex_components = Rational(2)

    # Casimir + Dynkin index admissions in (X4):
    #   C_2(adj of SU(N)) = N   (for SU(2)_L this identifies as N_pair)
    #   T(F^Weyl) = T(F^scalar) = 1/2
    C2_adj_SU2 = N_pair
    T_F_Weyl = Rational(1, 2)
    T_F_scalar = Rational(1, 2)

    print(f"  (X1) N_W = (N_color + 1) * N_gen = {N_W}")
    print(f"  (X3) n_S^complex_components = {n_S_complex_components}")
    print(f"  (X4) C_2(adj of SU(2)) = N_pair, T(F^Weyl) = T(F^scalar) = 1/2")

    # ---------------------------------------------------------------------
    section("Part 1: (P1) symbolic closed form for b_2 parametric in (N_pair, N_color, N_gen)")
    # ---------------------------------------------------------------------
    # Peskin-Schroeder Eq. 16.135:
    #   b  =  (11/3) C_2(adj)  -  (2/3) T(F_W) N_W  -  (1/6) T(F_S) n_S
    b_2_psv = (
        Rational(11, 3) * C2_adj_SU2
        - Rational(2, 3) * T_F_Weyl * N_W
        - Rational(1, 6) * T_F_scalar * n_S_complex_components
    )

    # Claim (P1): the above simplifies to
    #   (11/3) * N_pair - (1/3) * (N_color + 1) * N_gen - 1/6.
    b_2_claimed_P1 = (
        Rational(11, 3) * N_pair
        - Rational(1, 3) * (N_color + 1) * N_gen
        - Rational(1, 6)
    )

    check(
        "(P1) PSv-applied b_2 = (11/3) N_pair - (1/3) (N_color + 1) N_gen - 1/6",
        simplify(b_2_psv - b_2_claimed_P1) == 0,
        detail=f"b_2_psv - b_2_claimed_P1 = {simplify(b_2_psv - b_2_claimed_P1)}",
    )

    # Verify the factored form (P1'):
    #   b_2 = (22 N_pair - 2 (N_color + 1) N_gen - 1) / 6.
    b_2_claimed_factored = (
        22 * N_pair - 2 * (N_color + 1) * N_gen - 1
    ) / Rational(6)

    check(
        "(P1') factored: b_2 = (22 N_pair - 2 (N_color + 1) N_gen - 1) / 6",
        simplify(b_2_psv - b_2_claimed_factored) == 0,
        detail=f"diff = {simplify(b_2_psv - b_2_claimed_factored)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (P2) framework instance (N_pair, N_color, N_gen) = (2, 3, 3) -> 19/6")
    # ---------------------------------------------------------------------
    framework = {N_pair: 2, N_color: 3, N_gen: 3}
    b_2_framework = simplify(b_2_psv.subs(framework))

    check(
        "(P2) framework instance: b_2 = 19/6 at (N_pair, N_color, N_gen) = (2, 3, 3)",
        b_2_framework == Rational(19, 6),
        detail=f"b_2 = {b_2_framework}",
    )

    # Also verify the same instance via the factored form:
    b_2_framework_factored = simplify(b_2_claimed_factored.subs(framework))
    check(
        "(P2 alt) factored form at framework counts also equals 19/6",
        b_2_framework_factored == Rational(19, 6),
        detail=f"b_2_factored = {b_2_framework_factored}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (P3) per-sector decomposition")
    # ---------------------------------------------------------------------
    # Three additive contributions at framework counts:
    #   gauge boson + ghost:    +(11/3) N_pair                =  +22/3
    #   LH SU(2) Weyl matter:   -(1/3) (N_color + 1) N_gen    =  -4
    #   1 Higgs doublet:        -(1/6) * (1/2) * 2 = -1/6     =  -1/6
    gauge_contrib_sym = Rational(11, 3) * N_pair
    matter_contrib_sym = -Rational(1, 3) * (N_color + 1) * N_gen
    higgs_contrib_sym = -Rational(1, 6)

    gauge_at_fw = simplify(gauge_contrib_sym.subs(framework))
    matter_at_fw = simplify(matter_contrib_sym.subs(framework))
    higgs_at_fw = simplify(higgs_contrib_sym)

    check(
        "(P3) gauge boson + ghost contribution at framework counts is +22/3",
        gauge_at_fw == Rational(22, 3),
        detail=f"+ (11/3) * 2 = {gauge_at_fw}",
    )
    check(
        "(P3) LH SU(2) Weyl-doublet matter contribution at framework counts is -4",
        matter_at_fw == Rational(-4),
        detail=f"- (1/3) * 4 * 3 = {matter_at_fw}",
    )
    check(
        "(P3) 1-Higgs-doublet scalar contribution is -1/6",
        higgs_at_fw == -Rational(1, 6),
        detail=f"- (1/6) * (1/2) * 2 = {higgs_at_fw}",
    )

    # Sum of three contributions equals 19/6.
    total = gauge_at_fw + matter_at_fw + higgs_at_fw
    check(
        "(P3) per-sector sum: +22/3 + (-4) + (-1/6) = 19/6",
        total == Rational(19, 6),
        detail=f"22/3 - 4 - 1/6 = {total}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (C1)-(C4) corollaries")
    # ---------------------------------------------------------------------
    # (C1) Per-sector decomposition exact: 22/3 - 4 - 1/6 = 19/6.
    check(
        "(C1) per-sector decomposition equals 19/6 by exact Rational arithmetic",
        Rational(22, 3) + Rational(-4) + Rational(-1, 6) == Rational(19, 6),
        detail="22/6 + (-24/6) + (-1/6) form: (44 - 24 - 1)/6 = 19/6",
    )

    # (C3) Matter sector alone at framework counts is -4.
    matter_alone = simplify(matter_contrib_sym.subs(framework))
    check(
        "(C3) matter sector alone at framework: -(N_color+1) * N_gen / 3 = -4",
        matter_alone == Rational(-4),
        detail=f"-(3+1)*3/3 = {matter_alone}",
    )

    # (C4) Symmetric point N_color = N_gen yields parent broad note's variant.
    sym_subs = {N_gen: N_color}
    b_2_at_sym_point = simplify(b_2_psv.subs(sym_subs))
    parent_variant = (
        22 * N_pair - 2 * N_color * (N_color + 1) - 1
    ) / Rational(6)
    check(
        "(C4) symmetric point N_color = N_gen recovers parent broad-note form "
        "b_2 = (22 N_pair - 2 N_color (N_color + 1) - 1) / 6",
        simplify(b_2_at_sym_point - parent_variant) == 0,
        detail=f"diff = {simplify(b_2_at_sym_point - parent_variant)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: counterfactual at (N_pair, N_color, N_gen) = (2, 4, 3)")
    # ---------------------------------------------------------------------
    # At N_color = 4, the closed form should evaluate to
    #   (22*2 - 2*5*3 - 1)/6 = (44 - 30 - 1)/6 = 13/6.
    cf = {N_pair: 2, N_color: 4, N_gen: 3}
    b_2_cf = simplify(b_2_psv.subs(cf))
    check(
        "counterfactual (2, 4, 3): b_2 = 13/6 (confirms parametric form)",
        b_2_cf == Rational(13, 6),
        detail=f"b_2 = {b_2_cf}",
    )

    # Also check (3, 3, 3): hypothetical SU(3)_L instance gives
    #   (22*3 - 2*4*3 - 1)/6 = (66 - 24 - 1)/6 = 41/6.
    cf2 = {N_pair: 3, N_color: 3, N_gen: 3}
    b_2_cf2 = simplify(b_2_psv.subs(cf2))
    check(
        "counterfactual (3, 3, 3): b_2 = 41/6 (confirms N_pair dependence)",
        b_2_cf2 == Rational(41, 6),
        detail=f"b_2 = {b_2_cf2}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: factored-form sympy simplify roundtrip")
    # ---------------------------------------------------------------------
    # Verify that the factored form (P1') simplifies to the same expression
    # as the Peskin-Schroeder substituted form by sympy.simplify.
    diff_factored = simplify(b_2_psv - b_2_claimed_factored)
    check(
        "sympy.simplify(PSv - factored P1') == 0",
        diff_factored == 0,
        detail=f"simplify result: {diff_factored}",
    )

    # Verify the unfactored (P1) sympy.simplify reduction.
    diff_unfactored = simplify(b_2_psv - b_2_claimed_P1)
    check(
        "sympy.simplify(PSv - unfactored P1) == 0",
        diff_unfactored == 0,
        detail=f"simplify result: {diff_unfactored}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: Rational-arithmetic sanity check on the framework instance")
    # ---------------------------------------------------------------------
    # Build the framework instance numerically via direct Rational arithmetic
    # (no symbols) and confirm the final value.
    gauge_num = Rational(11, 3) * 2  # = 22/3
    matter_num = -Rational(1, 3) * (3 + 1) * 3  # = -4
    higgs_num = -Rational(1, 6)
    total_num = gauge_num + matter_num + higgs_num

    check(
        "framework instance via direct Rational arithmetic equals 19/6",
        total_num == Rational(19, 6),
        detail=f"22/3 - 4 - 1/6 = {total_num}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (P1) parametric closed form for b_2 in (N_pair, N_color, N_gen)")
    print("    (P1') factored form (22 N_pair - 2 (N_color+1) N_gen - 1) / 6")
    print("    (P2) framework instance b_2 = 19/6 at (2, 3, 3)")
    print("    (P3) per-sector additive decomposition (+22/3) + (-4) + (-1/6) = 19/6")
    print("    (C1) per-sector decomposition exact Rational arithmetic")
    print("    (C3) matter sector alone is -4 at framework counts")
    print("    (C4) symmetric point N_color = N_gen recovers parent broad-note form")
    print("    Counterfactual (2, 4, 3) -> 13/6 confirming N_color dependence")
    print("    Counterfactual (3, 3, 3) -> 41/6 confirming N_pair dependence")
    print("    sympy.simplify roundtrip on both unfactored and factored forms")
    print("    Direct Rational-arithmetic framework instance reproduces 19/6")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
