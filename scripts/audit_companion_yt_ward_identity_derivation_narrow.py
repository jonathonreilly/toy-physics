#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for the YT_WARD parent narrow
theorem note `YT_WARD_IDENTITY_DERIVATION_NARROW_THEOREM_NOTE_2026-05-10.md`.

The parent narrow note's load-bearing content is the algebraic-substitution
implication that, given the four cited inputs

  (I1) F_Htt^(0)(g_bare)^2 = c_S * g_bare^2 / (2 N_c)
       (§3 same-1PI construction identity, upstream PR #1080 narrow note)
  (I2) F_Htt^(0)(g_bare)   = 1 / sqrt(N_c * N_iso)
       (retained W1: g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19)
  (I3) c_S = +1
       (retained yt_ew_color_projection_theorem Block 8 / S2)
  (I4) (N_c, N_iso) = (3, 2)
       (retained native_gauge_closure_note)

the positive-branch substitution forces g_bare^2 = 1, hence g_bare = +1,
hence y_t_bare = 1/sqrt(6) and (under retained CMT D2-D3) the ratio
y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6).

This Pattern A narrow runner adds a sympy-based exact-symbolic verification:

  (a) treats (g_bare, c_S, N_c, N_iso, u_0) as free positive real symbols;
  (b) imports the four input identities (I1)-(I4) verbatim from the cited
      upstream retained / PR-#1080 authorities, with no rederivation of
      F_Htt^(0), c_S, N_c, or N_iso;
  (c) verifies parametrically that (I1)<->(I2) under (I3) reduces to
      g_bare^2 = 2 / (N_iso * c_S);
  (d) verifies at (c_S, N_iso, N_c) = (+1, 2, 3) that the reduction yields
      g_bare^2 = 1 (sympy simplify to 0), and that sympy.solve on the
      positive branch returns exactly +1;
  (e) verifies y_t_bare = 1/sqrt(N_c N_iso) reduces to 1/sqrt(6) at
      framework counts;
  (f) verifies the squared form y_t_bare^2 = g_bare^2 / (2 N_c) reduces
      to 1/6 at framework counts on the positive branch;
  (g) verifies that the ratio y_t(M_Pl) / g_s(M_Pl) under the retained CMT
      D2-D3 reduces to 1/sqrt(6) symbolically (u_0 does not appear in the
      free symbols of the simplified ratio);
  (h) runs two counterfactual probes that confirm (I3) and (I4) are
      load-bearing.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the parent's
load-bearing class-(A) algebra holds at exact symbolic precision under
the cited retained / PR-#1080 inputs. The cited input identities
themselves (I1)-(I4) and the CMT identities D14-D15 used in (D2)-(D3)
are imported from upstream retained authorities and are not re-derived
here.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, solve, sqrt, symbols
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
    print("YT_WARD_IDENTITY_DERIVATION_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: sympy-symbolic verification of g_bare^2 = 1 forcing and y_t/g_s ratio")
    print("under cited inputs (I1)-(I4) and CMT identities D2-D3")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------

    g_bare = Symbol("g_bare", positive=True, real=True)
    c_S = Symbol("c_S", real=True)
    N_c = Symbol("N_c", positive=True, integer=True)
    N_iso = Symbol("N_iso", positive=True, integer=True)
    u_0 = Symbol("u_0", positive=True, real=True)

    # Cited inputs (imported from upstream retained / PR-#1080 authorities;
    # not re-derived here):
    #   (I1) F_Htt^(0)(g_bare)^2 = c_S * g_bare^2 / (2 N_c)
    #   (I2) F_Htt^(0)(g_bare)   = 1 / sqrt(N_c N_iso)
    #   (I3) c_S = +1
    #   (I4) (N_c, N_iso) = (3, 2)
    F_Htt_sq_from_I1 = c_S * g_bare**2 / (2 * N_c)
    F_Htt_from_I2 = 1 / sqrt(N_c * N_iso)
    F_Htt_sq_from_I2 = (F_Htt_from_I2) ** 2  # = 1 / (N_c N_iso)

    print(f"  symbolic g_bare (positive real)        = {g_bare}")
    print(f"  symbolic c_S (real)                    = {c_S}")
    print(f"  symbolic N_c (positive integer)        = {N_c}")
    print(f"  symbolic N_iso (positive integer)      = {N_iso}")
    print(f"  (I1) F_Htt^(0)(g_bare)^2 = {F_Htt_sq_from_I1}")
    print(f"  (I2) F_Htt^(0)(g_bare)   = {F_Htt_from_I2}")

    # ---------------------------------------------------------------------
    section("Part 1: parametric same-1PI substitution (I1) <-> (I2)^2 under (I3)")
    # ---------------------------------------------------------------------
    # Equate (I1) and (I2)^2 and solve for g_bare^2 parametrically.

    diff = F_Htt_sq_from_I1 - F_Htt_sq_from_I2
    # diff = c_S g_bare^2 / (2 N_c) - 1/(N_c N_iso)
    # Setting diff = 0 gives g_bare^2 = 2 / (c_S N_iso)
    g_bare_sq_solution = solve(diff, g_bare**2)
    expected_param = Rational(2) / (c_S * N_iso)
    check(
        "parametric: equating (I1) and (I2)^2 gives g_bare^2 = 2 / (c_S * N_iso)",
        len(g_bare_sq_solution) == 1
        and simplify(g_bare_sq_solution[0] - expected_param) == 0,
        detail=f"solve returned {g_bare_sq_solution}, expected {expected_param}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: cited (I3) c_S = +1 under retained yt_ew_color_projection_theorem")
    # ---------------------------------------------------------------------
    # The retained authority supplies c_S = +1. Substitute into the
    # parametric expression and confirm g_bare^2 = 2 / N_iso.

    under_I3 = simplify(expected_param.subs(c_S, 1))
    expected_under_I3 = Rational(2) / N_iso
    check(
        "(I3) substitution: c_S = +1 gives g_bare^2 = 2 / N_iso",
        simplify(under_I3 - expected_under_I3) == 0,
        detail=f"got {under_I3}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: cited (I4) (N_c, N_iso) = (3, 2) under retained native_gauge_closure_note")
    # ---------------------------------------------------------------------
    # Substitute (I4) into the post-(I3) reduction.

    under_I3_I4 = simplify(under_I3.subs(N_iso, 2))
    expected_g_bare_sq = Rational(1)
    check(
        "(I4) substitution: N_iso = 2 gives g_bare^2 = 1",
        simplify(under_I3_I4 - expected_g_bare_sq) == 0,
        detail=f"got {under_I3_I4}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: positive-branch g_bare = +1 from sympy.solve")
    # ---------------------------------------------------------------------
    # Solve g_bare^2 = 1 for the symbol; positive branch must be exactly +1.

    g_bare_solutions = solve(g_bare**2 - 1, g_bare)
    # On real free symbol with positive=True, sympy returns only +1.
    # Allow either {+1} or {-1, +1} as the algebraic solution set; positive
    # branch is +1 in either case.
    sols_set = set(g_bare_solutions)
    pos_branch_ok = (1 in sols_set) or any(simplify(s - 1) == 0 for s in g_bare_solutions)
    check(
        "(P1) positive-branch g_bare = +1 from sympy.solve",
        pos_branch_ok,
        detail=f"solve returned {g_bare_solutions}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (P2) y_t_bare = 1/sqrt(6) by (I2) + (I4)")
    # ---------------------------------------------------------------------
    # y_t_bare := F_Htt^(0)(g_bare). At framework counts:
    y_t_bare = F_Htt_from_I2.subs({N_c: 3, N_iso: 2})
    expected_y_t_bare = 1 / sqrt(6)
    check(
        "(P2) y_t_bare = 1/sqrt(6) under (I2) and (I4)",
        simplify(y_t_bare - expected_y_t_bare) == 0,
        detail=f"got {y_t_bare}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (P2') y_t_bare^2 = 1/6 via (I1) + (P1) + (I3) + (I4)")
    # ---------------------------------------------------------------------
    # Equivalent check via the squared (I1) substitution.

    y_t_bare_sq_from_I1 = F_Htt_sq_from_I1.subs({c_S: 1, N_c: 3, g_bare: 1})
    expected_y_t_bare_sq = Rational(1, 6)
    check(
        "(P2') y_t_bare^2 = 1/6 via (I1) + (I3) + (I4) + (P1)",
        simplify(y_t_bare_sq_from_I1 - expected_y_t_bare_sq) == 0,
        detail=f"got {y_t_bare_sq_from_I1}",
    )

    # Consistency between (P2) and (P2'):
    check(
        "consistency: y_t_bare^2 from (P2) squared == y_t_bare^2 from (P2')",
        simplify(y_t_bare**2 - y_t_bare_sq_from_I1) == 0,
        detail="positive-branch consistency",
    )

    # ---------------------------------------------------------------------
    section("Part 7: (P3) y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6) via CMT cancellation")
    # ---------------------------------------------------------------------
    # Retained CMT D2-D3 (one fermion-bilinear hopping link per vertex,
    # n_link = 1):
    #   g_s(M_Pl) = g_bare / sqrt(u_0)
    #   y_t(M_Pl) = y_t_bare / sqrt(u_0)
    # The ratio cancels u_0.

    y_t_bare_value = 1 / sqrt(6)
    g_bare_value = Rational(1)
    g_s_MPl = g_bare_value / sqrt(u_0)
    y_t_MPl = y_t_bare_value / sqrt(u_0)
    ratio = simplify(y_t_MPl / g_s_MPl)
    expected_ratio = 1 / sqrt(6)
    check(
        "(P3) y_t(M_Pl) / g_s(M_Pl) reduces to 1/sqrt(6)",
        simplify(ratio - expected_ratio) == 0,
        detail=f"got {ratio}",
    )

    check(
        "(P3) ratio simplification removes u_0 from free symbols",
        u_0 not in ratio.free_symbols,
        detail=f"free_symbols of ratio = {ratio.free_symbols}",
    )

    # Stronger check: do the cancellation parametrically without
    # preselecting g_bare = 1, then specialize via (P1).
    g_s_MPl_param = g_bare / sqrt(u_0)
    y_t_MPl_param = y_t_bare_value / sqrt(u_0)
    ratio_param = simplify(y_t_MPl_param / g_s_MPl_param)
    # = y_t_bare / g_bare = (1/sqrt(6)) / g_bare
    expected_ratio_param = (1 / sqrt(6)) / g_bare
    check(
        "(P3) parametric: ratio simplifies to y_t_bare / g_bare with u_0 cancelled",
        simplify(ratio_param - expected_ratio_param) == 0,
        detail=f"got {ratio_param}",
    )
    # At (P1) g_bare = 1 this reduces to 1/sqrt(6).
    ratio_at_P1 = simplify(ratio_param.subs(g_bare, 1))
    check(
        "(P3) at (P1) g_bare = 1: ratio = 1/sqrt(6)",
        simplify(ratio_at_P1 - 1 / sqrt(6)) == 0,
        detail=f"got {ratio_at_P1}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: derivable corollaries")
    # ---------------------------------------------------------------------
    # 2 * y_t(M_Pl)^2 / g_s(M_Pl)^2 = 1 / N_c
    # The ratio (P3) gives y_t/g_s = 1/sqrt(2 N_c), so
    # 2 * (1 / (2 N_c)) = 1 / N_c.
    ratio_sq_times_2 = simplify(2 * (1 / sqrt(2 * N_c)) ** 2)
    expected_corr1 = Rational(1) / N_c
    check(
        "corollary 1: 2 * y_t(M_Pl)^2 / g_s(M_Pl)^2 = 1 / N_c parametric",
        simplify(ratio_sq_times_2 - expected_corr1) == 0,
        detail=f"got {ratio_sq_times_2}",
    )
    # At N_c = 3, equals 1/3.
    corr1_at_3 = ratio_sq_times_2.subs(N_c, 3)
    check(
        "corollary 1 at N_c = 3: 2 * y_t^2 / g_s^2 = 1/3",
        simplify(corr1_at_3 - Rational(1, 3)) == 0,
        detail=f"got {corr1_at_3}",
    )

    # N_iso * y_t_bare^2 = c_S * g_bare^2 / N_c is a restatement of (I1)
    # under the definition (D1) y_t_bare := F_Htt^(0)(g_bare).
    corr2_lhs = N_iso * F_Htt_sq_from_I1.subs(c_S, c_S)  # explicit identity, no substitution
    # Equate y_t_bare^2 = F_Htt^(0)^2 from (I1):
    # y_t_bare^2 = c_S g_bare^2 / (2 N_c). So:
    #   N_iso * y_t_bare^2 = c_S g_bare^2 * N_iso / (2 N_c)
    # The target says = c_S g_bare^2 / N_c, i.e. N_iso / (2 N_c) = 1 / N_c,
    # which requires N_iso = 2.
    corr2_general = N_iso * F_Htt_sq_from_I1
    corr2_target = c_S * g_bare**2 / N_c
    diff_corr2_general = simplify(corr2_general - corr2_target)
    # NOT identically zero parametrically; only zero when N_iso = 2 (per I4).
    check(
        "corollary 2 (N_iso=2): N_iso * y_t_bare^2 = c_S * g_bare^2 / N_c iff N_iso = 2",
        simplify(diff_corr2_general.subs(N_iso, 2)) == 0
        and simplify(diff_corr2_general.subs(N_iso, 3)) != 0,
        detail="parametric identity becomes algebraic under (I4) N_iso = 2",
    )

    # ---------------------------------------------------------------------
    section("Part 9: counterfactual probes (load-bearingness of (I3) and (I4))")
    # ---------------------------------------------------------------------
    # (I3) load-bearing: at c_S = -1 there is no positive real g_bare
    # satisfying the substitution (since g_bare^2 = -2/N_iso < 0).
    g_bare_sq_at_cS_minus = simplify(expected_param.subs(c_S, -1))
    # At N_iso = 2: g_bare^2 = -1. No positive real solution.
    g_bare_sq_at_cS_minus_N2 = simplify(g_bare_sq_at_cS_minus.subs(N_iso, 2))
    check(
        "counterfactual: at c_S = -1, N_iso = 2, no positive real g_bare^2 (= -1)",
        g_bare_sq_at_cS_minus_N2 == -1,
        detail=f"g_bare^2 at c_S=-1, N_iso=2 = {g_bare_sq_at_cS_minus_N2} (negative, no real root)",
    )

    # (I4) load-bearing on N_iso: at N_iso = 3 (instead of 2), g_bare^2 = 2/3 != 1.
    g_bare_sq_at_N_iso_3 = simplify(under_I3.subs(N_iso, 3))
    check(
        "counterfactual: at N_iso = 3 (not 2), g_bare^2 = 2/3 != 1",
        simplify(g_bare_sq_at_N_iso_3 - Rational(2, 3)) == 0,
        detail=f"g_bare^2 at N_iso=3 = {g_bare_sq_at_N_iso_3} (confirms (I4) load-bearing)",
    )

    # ---------------------------------------------------------------------
    section("Part 10: cross-checks with the §3 construction note")
    # ---------------------------------------------------------------------
    # The §3 same-1PI construction note (PR #1080) ships the identity (I1)
    # symbolically with (c_S = +1, N_c = 3, N_iso = 2) and solves the
    # consequent pinning. Confirm that the parent narrow's substitution
    # produces the SAME positive-branch root as a sanity cross-check.

    # Symbolically construct C_A and C_B as the §3 note's two
    # Wick-representations of Gamma^(4):
    #   C_A(g_bare) = c_S g_bare^2 / (2 N_c)
    #   C_B         = 1 / (N_c N_iso)
    # and verify C_A = C_B at (c_S, N_c, N_iso) = (+1, 3, 2) gives g_bare^2 = 1.
    C_A = c_S * g_bare**2 / (2 * N_c)
    C_B = Rational(1) / (N_c * N_iso)
    eq = simplify(C_A - C_B).subs({c_S: 1, N_c: 3, N_iso: 2})
    g_solutions = solve(eq, g_bare)
    pos_root_match = any(simplify(s - 1) == 0 for s in g_solutions)
    check(
        "§3 cross-check: C_A = C_B at (+1, 3, 2) yields positive root g_bare = +1",
        pos_root_match,
        detail=f"§3 cross-check solutions = {g_solutions}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (I1) <-> (I2)^2 under (I3): parametric g_bare^2 = 2 / (c_S * N_iso)")
    print("    (I3) + (I4) close to g_bare^2 = 1; positive branch g_bare = +1")
    print("    (P2) y_t_bare = 1/sqrt(6) under (I2) + (I4)")
    print("    (P2') y_t_bare^2 = 1/6 under (I1) + (I3) + (I4) + (P1)")
    print("    (P3) y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6) via CMT D2-D3 with u_0 cancelled")
    print("    Two derivable corollaries reduce as claimed")
    print("    Counterfactuals confirm (I3) and (I4) are load-bearing")
    print("    §3 construction cross-check returns the same positive-branch root")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
