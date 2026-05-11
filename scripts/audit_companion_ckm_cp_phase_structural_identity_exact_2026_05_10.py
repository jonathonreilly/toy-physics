#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_cp_phase_structural_identity_theorem_note_2026-04-24` (parent row)
via the narrow theorem
`CKM_CP_PHASE_STRUCTURAL_IDENTITY_NARROW_THEOREM_NOTE_2026-05-10.md`.

The narrow theorem's load-bearing content is the algebraic substitution
that, given projector weights `w_A1 = 1/n_quark`, `w_perp = (n_quark - 1)/
n_quark`, the cited bright/tensor CP radius `r^2 = 1/n_quark`, and the
Wolfenstein hypotheses `lambda^2 = alpha_s/n_pair`, `A^2 = n_pair/n_color`,
the CP-plane coordinates and CKM phase identities are forced

  (C1)  rho                =  1 / n_quark
  (C2)  eta                =  sqrt(n_quark - 1) / n_quark
  (C3)  rho^2 + eta^2      =  1 / n_quark
  (C4)  cos^2(delta_CKM)   =  1 / n_quark
  (C5)  sin^2(delta_CKM)   =  (n_quark - 1) / n_quark
  (C6)  tan(delta_CKM)     =  sqrt(n_quark - 1)
  (J)   J_0                =  alpha_s^3 sqrt(n_quark - 1)
                              / (n_pair^2 n_color n_quark)
  (Jq)  J_0  under q=pc    =  alpha_s^3 sqrt(n_quark - 1)
                              / (n_pair^3 n_color^2)

This Pattern B audit companion verifies each identity at exact sympy
precision over abstract counts (p, c, q with q = p c) and at the
framework counts (p, c, q) = (2, 3, 6), plus a non-framework instance
(p, c, q) = (3, 4, 12).

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the load-bearing
class-(A) algebra of the narrow theorem holds at exact symbolic
precision. Status remains owned by the audit pipeline.
"""

from __future__ import annotations
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols, sqrt, Integer, cos, sin, atan, acos
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
    print("Audit companion (exact-symbolic) for narrow theorem on parent")
    print("ckm_cp_phase_structural_identity_theorem_note_2026-04-24")
    print("Goal: sympy-symbolic verification of (C1)-(C7), (J), (Jq)")
    print("over abstract integer counts (p, c, q = p c) and framework counts (2, 3, 6)")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------
    p_sym, c_sym, q_sym = symbols("p c q", positive=True, integer=True)
    alpha_s = Symbol("alpha_s", positive=True, real=True)
    r_sym = Symbol("r", positive=True, real=True)

    # Imported parametric inputs
    w_A1 = Rational(1) / q_sym
    w_perp = (q_sym - 1) / q_sym
    r_sq = Rational(1) / q_sym
    lambda_sq = alpha_s / p_sym
    A_sq = p_sym / c_sym

    print(f"  symbolic alpha_s   = {alpha_s}")
    print(f"  symbolic counts:    p (n_pair), c (n_color), q (n_quark)")
    print(f"  w_A1               = {w_A1}")
    print(f"  w_perp             = {w_perp}")
    print(f"  r^2                = {r_sq}")
    print(f"  lambda^2           = {lambda_sq}")
    print(f"  A^2                = {A_sq}")

    # ---------------------------------------------------------------------
    section("Part 1: PSUM tautology w_A1 + w_perp == 1")
    # ---------------------------------------------------------------------
    check(
        "PSUM: w_A1 + w_perp == 1 (parametric in q)",
        simplify(w_A1 + w_perp - 1) == 0,
        detail=f"diff simplifies to {simplify(w_A1 + w_perp - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (C1) rho = 1/n_quark and (C2) eta = sqrt(q-1)/q")
    # ---------------------------------------------------------------------
    # rho^2 = r^2 * w_A1
    rho_sq = r_sq * w_A1
    rho_sq_target = Rational(1) / q_sym**2
    check(
        "(C1) rho^2 == 1/q^2  (parametric in q)",
        simplify(rho_sq - rho_sq_target) == 0,
        detail=f"diff = {simplify(rho_sq - rho_sq_target)}",
    )

    # Take positive square root => rho = 1/q
    rho = Rational(1) / q_sym
    check(
        "(C1) rho == 1/q  (positive branch)",
        simplify(sympy.sqrt(rho_sq_target) - rho) == 0,
        detail=f"sqrt(1/q^2) - 1/q simplifies to {simplify(sympy.sqrt(rho_sq_target) - rho)}",
    )

    # eta^2 = r^2 * w_perp
    eta_sq = r_sq * w_perp
    eta_sq_target = (q_sym - 1) / q_sym**2
    check(
        "(C2) eta^2 == (q-1)/q^2  (parametric in q)",
        simplify(eta_sq - eta_sq_target) == 0,
        detail=f"diff = {simplify(eta_sq - eta_sq_target)}",
    )

    eta = sqrt(q_sym - 1) / q_sym
    check(
        "(C2) eta == sqrt(q-1)/q  (positive branch)",
        simplify(sympy.sqrt(eta_sq_target) - eta) == 0,
        detail=f"sqrt((q-1)/q^2) - sqrt(q-1)/q simplifies to {simplify(sympy.sqrt(eta_sq_target) - eta)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (C3) rho^2 + eta^2 = 1/q")
    # ---------------------------------------------------------------------
    sum_sq = rho_sq + eta_sq
    target_C3 = Rational(1) / q_sym
    check(
        "(C3) rho^2 + eta^2 == 1/q  (parametric in q)",
        simplify(sum_sq - target_C3) == 0,
        detail=f"diff = {simplify(sum_sq - target_C3)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (C4),(C5) cos^2/sin^2 of delta_CKM")
    # ---------------------------------------------------------------------
    cos2_delta = rho_sq / (rho_sq + eta_sq)
    sin2_delta = eta_sq / (rho_sq + eta_sq)

    check(
        "(C4) cos^2(delta_CKM) == 1/q  (parametric in q)",
        simplify(cos2_delta - Rational(1) / q_sym) == 0,
        detail=f"diff = {simplify(cos2_delta - Rational(1) / q_sym)}",
    )

    check(
        "(C5) sin^2(delta_CKM) == (q-1)/q  (parametric in q)",
        simplify(sin2_delta - (q_sym - 1) / q_sym) == 0,
        detail=f"diff = {simplify(sin2_delta - (q_sym - 1) / q_sym)}",
    )

    # Trigonometric identity cos^2 + sin^2 = 1
    check(
        "cos^2 + sin^2 == 1  (parametric in q)",
        simplify(cos2_delta + sin2_delta - 1) == 0,
        detail="trigonometric identity preservation",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (C6) tan(delta_CKM) = sqrt(q - 1)")
    # ---------------------------------------------------------------------
    tan2_delta = sin2_delta / cos2_delta
    check(
        "(C6) tan^2(delta_CKM) == q - 1  (parametric in q)",
        simplify(tan2_delta - (q_sym - 1)) == 0,
        detail=f"diff = {simplify(tan2_delta - (q_sym - 1))}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (J) Jarlskog factor J_0")
    # ---------------------------------------------------------------------
    # J_0 = lambda^6 A^2 eta
    J0 = lambda_sq**3 * A_sq * eta
    J0_target = alpha_s**3 * sqrt(q_sym - 1) / (p_sym**2 * c_sym * q_sym)
    check(
        "(J) J_0 == alpha_s^3 sqrt(q-1) / (p^2 c q)  (parametric in p, c, q)",
        simplify(J0 - J0_target) == 0,
        detail=f"diff = {simplify(J0 - J0_target)}",
    )

    # Under q = p c
    J0_under_qpc = simplify(J0_target.subs(q_sym, p_sym * c_sym))
    J0_compact = alpha_s**3 * sqrt(p_sym * c_sym - 1) / (p_sym**3 * c_sym**2)
    check(
        "(Jq) J_0 under q=p*c == alpha_s^3 sqrt(p c - 1) / (p^3 c^2)",
        simplify(J0_under_qpc - J0_compact) == 0,
        detail=f"reduced form = {J0_under_qpc}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: framework counts (p, c, q) = (2, 3, 6)")
    # ---------------------------------------------------------------------
    framework = {p_sym: 2, c_sym: 3, q_sym: 6}

    rho_at = simplify(rho.subs(framework))
    check(
        "(C1) at (2,3,6): rho == 1/6",
        simplify(rho_at - Rational(1, 6)) == 0,
        detail=f"got {rho_at}",
    )

    eta_at = simplify(eta.subs(framework))
    check(
        "(C2) at (2,3,6): eta == sqrt(5)/6",
        simplify(eta_at - sqrt(5) / 6) == 0,
        detail=f"got {eta_at}",
    )

    rho2eta2_at = simplify((rho_sq + eta_sq).subs(framework))
    check(
        "(C3) at (2,3,6): rho^2 + eta^2 == 1/6",
        simplify(rho2eta2_at - Rational(1, 6)) == 0,
        detail=f"got {rho2eta2_at}",
    )

    cos2_at = simplify(cos2_delta.subs(framework))
    check(
        "(C4) at (2,3,6): cos^2(delta_CKM) == 1/6",
        simplify(cos2_at - Rational(1, 6)) == 0,
        detail=f"got {cos2_at}",
    )

    sin2_at = simplify(sin2_delta.subs(framework))
    check(
        "(C5) at (2,3,6): sin^2(delta_CKM) == 5/6",
        simplify(sin2_at - Rational(5, 6)) == 0,
        detail=f"got {sin2_at}",
    )

    tan2_at = simplify(tan2_delta.subs(framework))
    check(
        "(C6) at (2,3,6): tan^2(delta_CKM) == 5  (tan = sqrt(5))",
        simplify(tan2_at - 5) == 0,
        detail=f"got {tan2_at}",
    )

    J0_at = simplify(J0.subs(framework))
    check(
        "(J) at (2,3,6): J_0 == alpha_s^3 sqrt(5)/72",
        simplify(J0_at - alpha_s**3 * sqrt(5) / 72) == 0,
        detail=f"got {J0_at}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: non-framework instance (p, c, q) = (3, 4, 12)")
    # ---------------------------------------------------------------------
    other = {p_sym: 3, c_sym: 4, q_sym: 12}

    rho_o = simplify(rho.subs(other))
    check(
        "(C1) at (3,4,12): rho == 1/12",
        simplify(rho_o - Rational(1, 12)) == 0,
        detail=f"got {rho_o}",
    )

    eta_o = simplify(eta.subs(other))
    check(
        "(C2) at (3,4,12): eta == sqrt(11)/12",
        simplify(eta_o - sqrt(11) / 12) == 0,
        detail=f"got {eta_o}",
    )

    cos2_o = simplify(cos2_delta.subs(other))
    check(
        "(C4) at (3,4,12): cos^2(delta_CKM) == 1/12",
        simplify(cos2_o - Rational(1, 12)) == 0,
        detail=f"got {cos2_o}",
    )

    J0_o = simplify(J0.subs(other))
    # J_0 under (3,4,12) = alpha_s^3 sqrt(11) / (9 * 4 * 12) = alpha_s^3 sqrt(11)/432
    J0_target_o = alpha_s**3 * sqrt(11) / 432
    check(
        "(J) at (3,4,12): J_0 == alpha_s^3 sqrt(11)/432",
        simplify(J0_o - J0_target_o) == 0,
        detail=f"got {J0_o}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: derivable corollaries")
    # ---------------------------------------------------------------------
    # tan(delta) eta / rho = (q-1)
    # use tan^2 form
    coro1 = simplify(tan2_delta * eta_sq / rho_sq)
    # tan^2 = (q-1), eta^2/rho^2 = (q-1), product = (q-1)^2
    check(
        "corollary: tan^2(delta) * eta^2 / rho^2 == (q - 1)^2  (parametric)",
        simplify(coro1 - (q_sym - 1) ** 2) == 0,
        detail=f"got {coro1}",
    )

    # cos^2(delta) * q == 1
    coro2 = simplify(cos2_delta * q_sym - 1)
    check(
        "corollary: cos^2(delta) * q == 1  (parametric)",
        coro2 == 0,
        detail=f"diff = {coro2}",
    )

    # J_0 / alpha_s^3 under q=pc == sqrt(pc-1)/(p^3 c^2)
    coro3 = simplify(J0_compact / alpha_s**3)
    coro3_target = sqrt(p_sym * c_sym - 1) / (p_sym**3 * c_sym**2)
    check(
        "corollary: J_0 / alpha_s^3 == sqrt(pc-1) / (p^3 c^2)  (under q=pc)",
        simplify(coro3 - coro3_target) == 0,
        detail=f"got {coro3}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    PSUM tautology w_A1 + w_perp = 1")
    print("    (C1) rho parametric in q")
    print("    (C2) eta parametric in q")
    print("    (C3) rho^2 + eta^2 = 1/q parametric in q")
    print("    (C4),(C5) cos^2 and sin^2 of delta_CKM parametric in q")
    print("    cos^2 + sin^2 = 1 trigonometric identity preserved")
    print("    (C6) tan^2(delta) = q - 1 parametric in q")
    print("    (J) J_0 parametric in (p, c, q); (Jq) under q = p c")
    print("    All identities specialise correctly at (p, c, q) = (2, 3, 6)")
    print("    Non-framework (3, 4, 12) reproduces the corresponding closed forms")
    print("    Three derivable corollary identities hold parametrically")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
