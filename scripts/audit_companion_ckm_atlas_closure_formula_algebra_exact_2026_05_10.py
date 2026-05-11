#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_atlas_axiom_closure_note` (legacy parent row) via the narrow theorem
`CKM_ATLAS_CLOSURE_FORMULA_ALGEBRA_NARROW_THEOREM_NOTE_2026-05-10.md`.

The narrow theorem isolates three algebraic blocks from the parent's
"Closure Formulas" section that are reducible to pure substitution under the
parametric input identities `(I1)-(Iq)` plus the imported magnitudes
`(M1)-(M5)` from the magnitudes narrow theorem:

  Block (U):  atlas-leading unitarity-row completion identities
              (U1) |V_ud|^2 = 1 - alpha_s/p - alpha_s^3/(p^3 c^2)
              (U2) |V_cs|^2 = 1 - alpha_s/p - alpha_s^2/(p c)
              (U3) |V_tb|^2 = 1 - (q-1) alpha_s^3/(p^3 c^2) - alpha_s^2/(p c)

  Block (IS): CKM inverse-square structural reading on counts
              (IS2) rho A^2 = 1/c^2  (parametric in p, c under q = p c)
              (IS1), (IS3), (IS4) at framework counts (p, c) = (2, 3)

  Block (BM): CKM Bernoulli moment/variance corollary
              (BM1) V(N) = M(N)/N  (parametric in N)
              (BM2) M(N) + 1/N = 1  (parametric in N)
              framework Bernoulli table at (p, c, q) = (2, 3, 6)
              (parametric only when p = c - 1; framework satisfies this)

This Pattern B audit companion verifies each identity at exact sympy
precision over abstract counts (p, c, q with q = p c, and abstract N for
Bernoulli identities) and at the framework counts.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the load-bearing
class-(A) algebra of the narrow theorem holds at exact symbolic
precision. Status remains owned by the audit pipeline.
"""

from __future__ import annotations
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols, sqrt
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
    print("Audit companion (exact-symbolic) for CKM atlas closure-formula algebra")
    print("legacy parent: ckm_atlas_axiom_closure_note")
    print("Goal: sympy-symbolic verification of blocks (U), (IS), (BM)")
    print("over abstract integer counts (p, c, q = p c) and framework counts (2, 3, 6)")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------
    p_sym, c_sym, q_sym = symbols("p c q", positive=True, integer=True)
    N_sym = symbols("N", positive=True, real=True)
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Imported parametric inputs (I1)-(I4)
    lambda_sq = alpha_s / p_sym
    A_sq = p_sym / c_sym
    rho = Rational(1) / q_sym
    eta_sq = (q_sym - 1) / q_sym**2

    # Imported magnitudes (M1)-(M5) from magnitudes narrow theorem
    V_us_sq = alpha_s / p_sym
    V_cb_sq = alpha_s**2 / (p_sym * c_sym)
    V_ts_sq = alpha_s**2 / (p_sym * c_sym)
    V_ub_sq = alpha_s**3 / (p_sym**3 * c_sym**2)  # under q = p c
    V_td_sq = (q_sym - 1) * alpha_s**3 / (p_sym**3 * c_sym**2)  # under q = p c (use q_sym for clarity)

    # Atlas-leading second-row identity: |V_cd|^2 = |V_us|^2 at leading order
    V_cd_sq = V_us_sq

    print(f"  symbolic alpha_s = {alpha_s}, counts p, c, q = symbolic positive integers")
    print(f"  Imported (M1)-(M5) at q = p c:")
    print(f"    |V_us|^2 = {V_us_sq}")
    print(f"    |V_cb|^2 = {V_cb_sq}")
    print(f"    |V_ts|^2 = {V_ts_sq}")
    print(f"    |V_ub|^2 = {V_ub_sq}")
    print(f"    |V_td|^2 = {V_td_sq}")

    # ---------------------------------------------------------------------
    section("Part 1: Block (U) unitarity-row completion identities")
    # ---------------------------------------------------------------------
    # (U1) |V_ud|^2 = 1 - |V_us|^2 - |V_ub|^2
    V_ud_sq = 1 - V_us_sq - V_ub_sq
    V_ud_target = 1 - alpha_s / p_sym - alpha_s**3 / (p_sym**3 * c_sym**2)
    check(
        "(U1) |V_ud|^2 == 1 - alpha_s/p - alpha_s^3/(p^3 c^2)  (parametric in p, c)",
        simplify(V_ud_sq - V_ud_target) == 0,
        detail=f"diff = {simplify(V_ud_sq - V_ud_target)}",
    )

    # (U2) |V_cs|^2 = 1 - |V_cd|^2 - |V_cb|^2 with V_cd^2 = V_us^2
    V_cs_sq = 1 - V_cd_sq - V_cb_sq
    V_cs_target = 1 - alpha_s / p_sym - alpha_s**2 / (p_sym * c_sym)
    check(
        "(U2) |V_cs|^2 == 1 - alpha_s/p - alpha_s^2/(p c)  (parametric in p, c)",
        simplify(V_cs_sq - V_cs_target) == 0,
        detail=f"diff = {simplify(V_cs_sq - V_cs_target)}",
    )

    # (U3) |V_tb|^2 = 1 - |V_td|^2 - |V_ts|^2
    V_tb_sq = 1 - V_td_sq - V_ts_sq
    V_tb_target = 1 - (q_sym - 1) * alpha_s**3 / (p_sym**3 * c_sym**2) - alpha_s**2 / (p_sym * c_sym)
    check(
        "(U3) |V_tb|^2 == 1 - (q-1) alpha_s^3/(p^3 c^2) - alpha_s^2/(p c)  (parametric)",
        simplify(V_tb_sq - V_tb_target) == 0,
        detail=f"diff = {simplify(V_tb_sq - V_tb_target)}",
    )

    # Sanity: row sums == 1
    check(
        "row-U sum: |V_ud|^2 + |V_us|^2 + |V_ub|^2 == 1  (parametric)",
        simplify(V_ud_sq + V_us_sq + V_ub_sq - 1) == 0,
        detail="atlas-leading first row unitarity",
    )

    check(
        "row-C sum: |V_cd|^2 + |V_cs|^2 + |V_cb|^2 == 1  (parametric)",
        simplify(V_cd_sq + V_cs_sq + V_cb_sq - 1) == 0,
        detail="atlas-leading second row unitarity",
    )

    check(
        "row-T sum: |V_td|^2 + |V_ts|^2 + |V_tb|^2 == 1  (parametric)",
        simplify(V_td_sq + V_ts_sq + V_tb_sq - 1) == 0,
        detail="atlas-leading third row unitarity",
    )

    # ---------------------------------------------------------------------
    section("Part 2: Block (IS) inverse-square structural reading")
    # ---------------------------------------------------------------------
    # (IS2): rho A^2 = (1/q)(p/c) = p/(c q). Under q = p c: = p/(c * p c) = 1/c^2
    rho_Asq = rho * A_sq
    rho_Asq_under_q = simplify(rho_Asq.subs(q_sym, p_sym * c_sym))
    check(
        "(IS2) rho A^2 under q = p c: == 1 / c^2  (parametric in p, c)",
        simplify(rho_Asq_under_q - 1 / c_sym**2) == 0,
        detail=f"reduced = {rho_Asq_under_q}",
    )

    # (IS1) at framework counts: eta^2 = 1/p^2 - 1/c^2 at p=2, c=3, q=6
    # eta^2 at framework
    eta_sq_at_framework = eta_sq.subs(q_sym, 6)
    inv_sq_at_framework = Rational(1) / 4 - Rational(1) / 9  # 1/p^2 - 1/c^2 at p=2, c=3
    check(
        "(IS1) at (p,c,q)=(2,3,6): eta^2 == 1/p^2 - 1/c^2 == 5/36",
        simplify(eta_sq_at_framework - inv_sq_at_framework) == 0
        and simplify(eta_sq_at_framework - Rational(5, 36)) == 0,
        detail=f"eta^2={eta_sq_at_framework}, 1/p^2 - 1/c^2 = {inv_sq_at_framework}",
    )

    # (IS3) at framework: eta^2 + rho A^2 = 1/p^2 = 1/4
    eta_sq_plus_rho_Asq_fw = (eta_sq + rho_Asq).subs({p_sym: 2, c_sym: 3, q_sym: 6})
    check(
        "(IS3) at (p,c,q)=(2,3,6): eta^2 + rho A^2 == 1/p^2 == 1/4",
        simplify(eta_sq_plus_rho_Asq_fw - Rational(1, 4)) == 0,
        detail=f"got {simplify(eta_sq_plus_rho_Asq_fw)}",
    )

    # (IS4) at framework: eta^2 + 2 rho A^2 = 1/p^2 + 1/c^2 = 13/36
    eta_sq_plus_2_rho_Asq_fw = (eta_sq + 2 * rho_Asq).subs({p_sym: 2, c_sym: 3, q_sym: 6})
    check(
        "(IS4) at (p,c,q)=(2,3,6): eta^2 + 2 rho A^2 == 1/p^2 + 1/c^2 == 13/36",
        simplify(eta_sq_plus_2_rho_Asq_fw - Rational(13, 36)) == 0,
        detail=f"got {simplify(eta_sq_plus_2_rho_Asq_fw)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: Block (BM) Bernoulli moment/variance identities")
    # ---------------------------------------------------------------------
    # (BM1) V(N) = M(N)/N where M(N) = 1 - 1/N, V(N) = (N-1)/N^2
    M_N = 1 - Rational(1) / N_sym
    V_N = (N_sym - 1) / N_sym**2

    check(
        "(BM1) V(N) == M(N)/N  (parametric in N)",
        simplify(V_N - M_N / N_sym) == 0,
        detail=f"diff = {simplify(V_N - M_N / N_sym)}",
    )

    # (BM2) M(N) + 1/N == 1
    check(
        "(BM2) M(N) + 1/N == 1  (parametric in N)",
        simplify(M_N + Rational(1) / N_sym - 1) == 0,
        detail=f"diff = {simplify(M_N + Rational(1) / N_sym - 1)}",
    )

    # Framework Bernoulli table (requires n_pair = n_color - 1, satisfied at p=2, c=3)
    # M(N_pair) = 1 - 1/2 = 1/2
    M_npair = M_N.subs(N_sym, 2)
    check(
        "framework: M(N_pair=2) == 1/2",
        simplify(M_npair - Rational(1, 2)) == 0,
        detail=f"got {M_npair}",
    )

    # M(N_color) = 1 - 1/3 = 2/3 (matches A^2 = 2/3 at framework)
    M_ncolor = M_N.subs(N_sym, 3)
    A_sq_at_framework = A_sq.subs({p_sym: 2, c_sym: 3})
    check(
        "framework: M(N_color=3) == A^2 == 2/3 (requires n_pair = n_color - 1)",
        simplify(M_ncolor - A_sq_at_framework) == 0
        and simplify(M_ncolor - Rational(2, 3)) == 0,
        detail=f"M(3)={M_ncolor}, A^2={A_sq_at_framework}",
    )

    # M(N_quark) = 1 - 1/6 = 5/6 = 1 - rho at framework
    M_nquark = M_N.subs(N_sym, 6)
    one_minus_rho_at_framework = (1 - rho).subs(q_sym, 6)
    check(
        "framework: M(N_quark=6) == 1 - rho == 5/6",
        simplify(M_nquark - one_minus_rho_at_framework) == 0
        and simplify(M_nquark - Rational(5, 6)) == 0,
        detail=f"got {M_nquark}",
    )

    # V(N_pair) = 1/4
    V_npair = V_N.subs(N_sym, 2)
    check(
        "framework: V(N_pair=2) == 1/4",
        simplify(V_npair - Rational(1, 4)) == 0,
        detail=f"got {V_npair}",
    )

    # V(N_color) = 2/9
    V_ncolor = V_N.subs(N_sym, 3)
    check(
        "framework: V(N_color=3) == 2/9",
        simplify(V_ncolor - Rational(2, 9)) == 0,
        detail=f"got {V_ncolor}",
    )

    # V(N_quark) = 5/36 = eta^2 at framework
    V_nquark = V_N.subs(N_sym, 6)
    eta_sq_at_framework2 = eta_sq.subs(q_sym, 6)
    check(
        "framework: V(N_quark=6) == eta^2 == 5/36",
        simplify(V_nquark - eta_sq_at_framework2) == 0
        and simplify(V_nquark - Rational(5, 36)) == 0,
        detail=f"got {V_nquark}",
    )

    # rho = V(N_pair) M(N_color) at framework
    rho_via_BM = V_npair * M_ncolor
    rho_at_framework = rho.subs(q_sym, 6)
    check(
        "framework: rho == V(N_pair) M(N_color) == 1/6",
        simplify(rho_via_BM - rho_at_framework) == 0
        and simplify(rho_via_BM - Rational(1, 6)) == 0,
        detail=f"got {rho_via_BM}",
    )

    # A^2 rho == V(N_color) M(N_pair) == 1/9
    Asq_rho_via_BM = V_ncolor * M_npair
    Asq_rho_at_framework = (A_sq * rho).subs({p_sym: 2, c_sym: 3, q_sym: 6})
    check(
        "framework: A^2 rho == V(N_color) M(N_pair) == 1/9",
        simplify(Asq_rho_via_BM - Asq_rho_at_framework) == 0
        and simplify(Asq_rho_via_BM - Rational(1, 9)) == 0,
        detail=f"got {Asq_rho_via_BM}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: framework numerical specialisations of (U1)-(U3)")
    # ---------------------------------------------------------------------
    framework = {p_sym: 2, c_sym: 3, q_sym: 6}

    V_ud_fw = simplify(V_ud_sq.subs(framework))
    V_ud_fw_target = 1 - alpha_s / 2 - alpha_s**3 / 72
    check(
        "(U1) at (2,3,6): |V_ud|^2 == 1 - alpha_s/2 - alpha_s^3/72",
        simplify(V_ud_fw - V_ud_fw_target) == 0,
        detail=f"got {V_ud_fw}",
    )

    V_cs_fw = simplify(V_cs_sq.subs(framework))
    V_cs_fw_target = 1 - alpha_s / 2 - alpha_s**2 / 6
    check(
        "(U2) at (2,3,6): |V_cs|^2 == 1 - alpha_s/2 - alpha_s^2/6",
        simplify(V_cs_fw - V_cs_fw_target) == 0,
        detail=f"got {V_cs_fw}",
    )

    V_tb_fw = simplify(V_tb_sq.subs(framework))
    V_tb_fw_target = 1 - 5 * alpha_s**3 / 72 - alpha_s**2 / 6
    check(
        "(U3) at (2,3,6): |V_tb|^2 == 1 - 5 alpha_s^3/72 - alpha_s^2/6",
        simplify(V_tb_fw - V_tb_fw_target) == 0,
        detail=f"got {V_tb_fw}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: counterfactual probe for (IS1) at non-framework counts")
    # ---------------------------------------------------------------------
    # (IS1) eta^2 = 1/p^2 - 1/c^2 is a framework-counts identity. At
    # (p, c, q) = (3, 4, 12) it does NOT hold parametrically.
    other = {p_sym: 3, c_sym: 4, q_sym: 12}
    eta_sq_at_other = simplify(eta_sq.subs(other))
    inv_sq_at_other = Rational(1) / 9 - Rational(1) / 16
    check(
        "(IS1) counterfactual: at (3,4,12), eta^2 != 1/p^2 - 1/c^2",
        simplify(eta_sq_at_other - inv_sq_at_other) != 0,
        detail=f"eta^2={eta_sq_at_other}, 1/p^2 - 1/c^2 = {inv_sq_at_other} (different)",
    )

    # Show that the corresponding Bernoulli M(N_color) = A^2 identity also breaks
    # at (p, c) = (3, 4): A^2 = 3/4, M(N_color) = 1 - 1/4 = 3/4, so it HAPPENS to hold
    # only when p = c - 1 (which is 3 = 4-1 = 3, also yes!) -- both (2,3) and (3,4)
    # satisfy p = c - 1. Let's use a true counterfactual (p, c) = (2, 4).
    M_4 = M_N.subs(N_sym, 4)
    A_sq_at_other_cf = A_sq.subs({p_sym: 2, c_sym: 4})  # p=2, c=4: A^2 = 1/2, M(4) = 3/4
    check(
        "Bernoulli counterfactual: at (p, c) = (2, 4) where p != c - 1, M(N_color) != A^2",
        simplify(M_4 - A_sq_at_other_cf) != 0,
        detail=f"M(4)={M_4}, A^2(p=2,c=4)={A_sq_at_other_cf}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    Block (U): (U1)-(U3) row-completion identities parametric in p, c, q")
    print("    Row sums |V_ij|^2 = 1 for all three rows parametric in p, c, q")
    print("    Block (IS): (IS2) parametric in p, c under q = p c")
    print("    Block (IS): (IS1), (IS3), (IS4) at framework counts (2, 3, 6)")
    print("    Block (BM): (BM1), (BM2) parametric in N")
    print("    Framework Bernoulli table: 1/2, 2/3, 5/6, 1/4, 2/9, 5/36")
    print("    rho = V(N_pair) M(N_color) and A^2 rho = V(N_color) M(N_pair) at framework")
    print("    All (U1)-(U3) specialise correctly at (p, c, q) = (2, 3, 6)")
    print("    Counterfactuals: (IS1) and (BM-A^2) require specific count tuples")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
