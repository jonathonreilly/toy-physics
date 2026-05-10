#!/usr/bin/env python3
"""Verify the CKM CP-phase structural trigonometric narrow theorem.

The narrow theorem note
`CKM_CP_PHASE_STRUCTURAL_TRIG_NARROW_THEOREM_NOTE_2026-05-10.md`
states a purely abstract two-coordinate trigonometric and
monomial-algebraic theorem on:

  - abstract real `(rho, eta)` with `rho > 0`, `eta >= 0`, defining
    `delta := atan2(eta, rho)` on the principal branch;
  - abstract real `(lambda, A, eta)` with `lambda > 0`, defining
    `J := lambda^6 A^2 eta`.

Conclusions:

  (T1) cos^2(delta) = rho^2 / (rho^2 + eta^2);
  (T2) sin^2(delta) = eta^2 / (rho^2 + eta^2);
  (T3) tan(delta)   = eta / rho                     (rho > 0);
  (T4) weight-form rephasing with w_A1, w_perp;
  (T5) lambda^6 A^2 eta = (lambda^2)^3 A^2 eta      (monomial);
  (T6) arctan(eta/rho) = arccos(rho/sqrt(rho^2+eta^2));
  (T7) explicit non-trivial points on the identity surface, including
       the parent-atlas readout point (rho, eta) = (1/6, sqrt(5)/6).

This runner exhibits each conclusion symbolically (exact rational /
real symbol algebra via sympy) and verifies numerical instances at
exact precision. No framework / audit / lattice module is imported;
only sympy.
"""

from __future__ import annotations

import sympy as sp
from sympy import (
    atan,
    atan2,
    acos,
    cos,
    sin,
    tan,
    sqrt,
    Rational,
    Symbol,
    pi,
    simplify,
    trigsimp,
)


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
    s = simplify(expr)
    if s == 0:
        return True
    s2 = trigsimp(s)
    return s2 == 0


def main() -> int:
    print("CKM CP-phase structural trigonometric narrow theorem check")
    print()

    # ------------------------------------------------------------------
    # Setup: abstract symbols on the open principal-branch quadrant
    # rho > 0, eta >= 0; lambda > 0; A real
    # ------------------------------------------------------------------
    rho = Symbol("rho", positive=True, real=True)
    eta = Symbol("eta", positive=True, real=True)
    lam = Symbol("lambda", positive=True, real=True)
    A = Symbol("A", real=True)

    delta = atan2(eta, rho)  # principal branch, in (0, pi/2) for rho, eta > 0
    r_sq = rho ** 2 + eta ** 2
    r = sqrt(r_sq)

    # ------------------------------------------------------------------
    # (T1) cos^2(delta) = rho^2 / (rho^2 + eta^2)
    # ------------------------------------------------------------------
    t1 = cos(delta) ** 2 - rho ** 2 / r_sq
    check("(1) (T1) cos^2(delta) = rho^2 / (rho^2 + eta^2)", is_zero(t1))

    # ------------------------------------------------------------------
    # (T2) sin^2(delta) = eta^2 / (rho^2 + eta^2)
    # ------------------------------------------------------------------
    t2 = sin(delta) ** 2 - eta ** 2 / r_sq
    check("(2) (T2) sin^2(delta) = eta^2 / (rho^2 + eta^2)", is_zero(t2))

    # ------------------------------------------------------------------
    # (T3) tan(delta) = eta / rho     (rho > 0)
    # ------------------------------------------------------------------
    t3 = tan(delta) - eta / rho
    check("(3) (T3) tan(delta) = eta / rho", is_zero(t3))

    # Cross-check: cos^2 + sin^2 = 1
    pythag = cos(delta) ** 2 + sin(delta) ** 2 - 1
    check("(3a) cos^2(delta) + sin^2(delta) = 1", is_zero(pythag))

    # ------------------------------------------------------------------
    # (T4) weight-form rephasing
    #     w_A1 := rho^2/r^2,  w_perp := eta^2/r^2
    # ------------------------------------------------------------------
    w_A1 = rho ** 2 / r_sq
    w_perp = eta ** 2 / r_sq

    t4a = w_A1 + w_perp - 1
    check("(4) (T4a) w_A1 + w_perp = 1", is_zero(t4a))

    t4b = cos(delta) ** 2 - w_A1
    check("(5) (T4b) cos^2(delta) = w_A1", is_zero(t4b))

    t4c = sin(delta) ** 2 - w_perp
    check("(6) (T4c) sin^2(delta) = w_perp", is_zero(t4c))

    t4d = tan(delta) ** 2 - w_perp / w_A1
    check("(7) (T4d) tan^2(delta) = w_perp / w_A1", is_zero(t4d))

    # ------------------------------------------------------------------
    # (T5) Jarlskog monomial factorisation: lam^6 A^2 eta = (lam^2)^3 A^2 eta
    # ------------------------------------------------------------------
    j_full = lam ** 6 * A ** 2 * eta
    j_factored = (lam ** 2) ** 3 * A ** 2 * eta
    t5 = j_full - j_factored
    check(
        "(8) (T5) lambda^6 A^2 eta = (lambda^2)^3 A^2 eta",
        is_zero(t5),
        "monomial exponent identity (x^a)^b = x^(a*b) for x>0, a,b in Z",
    )

    # Variant: J = lambda^6 A^2 eta = lambda^4 * lambda^2 * A^2 * eta
    t5b = j_full - (lam ** 4 * lam ** 2 * A ** 2 * eta)
    check(
        "(8a) (T5 variant) lambda^6 A^2 eta = lambda^4 * lambda^2 * A^2 * eta",
        is_zero(t5b),
    )

    # ------------------------------------------------------------------
    # (T6) Principal-branch equivalence
    #     arctan(eta/rho) = arccos(rho / sqrt(rho^2+eta^2))
    # ------------------------------------------------------------------
    # On rho>0, eta>=0, atan2(eta, rho) = atan(eta/rho).
    # Compare via cos/sin of both sides on open quadrant via series-
    # equivalent symbolic forms.
    lhs = atan(eta / rho)
    rhs = acos(rho / r)
    # Differences are unstable to compare directly with simplify because
    # sympy keeps both as transcendental forms; check via cos and sin:
    cos_diff = cos(lhs) - cos(rhs)
    sin_diff = sin(lhs) - sin(rhs)
    check(
        "(9) (T6) cos(arctan(eta/rho)) = cos(arccos(rho/r))",
        is_zero(cos_diff),
    )
    check(
        "(9a) (T6) sin(arctan(eta/rho)) = sin(arccos(rho/r))",
        is_zero(sin_diff),
    )

    # ------------------------------------------------------------------
    # (T7) Non-trivial substitutions
    # ------------------------------------------------------------------
    # Instance A: parent-atlas readout (rho, eta) = (1/6, sqrt(5)/6)
    inst_rho = Rational(1, 6)
    inst_eta = sqrt(Rational(5)) / 6
    inst_r_sq = inst_rho ** 2 + inst_eta ** 2
    check(
        "(10) (T7-A) r^2 = 1/6 at (rho, eta) = (1/6, sqrt(5)/6)",
        simplify(inst_r_sq - Rational(1, 6)) == 0,
        f"r^2 = {sp.nsimplify(inst_r_sq)}",
    )

    inst_delta = atan2(inst_eta, inst_rho)
    inst_cos_sq = simplify(cos(inst_delta) ** 2)
    check(
        "(11) (T7-A) cos^2(delta) = 1/6 at instance",
        inst_cos_sq == Rational(1, 6),
        f"cos^2 = {inst_cos_sq}",
    )
    inst_sin_sq = simplify(sin(inst_delta) ** 2)
    check(
        "(12) (T7-A) sin^2(delta) = 5/6 at instance",
        inst_sin_sq == Rational(5, 6),
        f"sin^2 = {inst_sin_sq}",
    )
    inst_tan = simplify(tan(inst_delta))
    check(
        "(13) (T7-A) tan(delta) = sqrt(5) at instance",
        simplify(inst_tan - sqrt(Rational(5))) == 0,
        f"tan = {inst_tan}",
    )
    inst_acos = acos(1 / sqrt(Rational(6)))
    inst_atan = atan(sqrt(Rational(5)))
    # Sympy's simplify() does not fold (acos(x) - atan(y)) to zero even
    # when both lie in [0, pi/2] and are equal; verify equality via the
    # injective trigonometric forms cos and tan instead. Both functions
    # are injective on [0, pi/2], so equality of cos and tan on that
    # branch implies equality of the angles.
    cos_eq = simplify(cos(inst_acos) - cos(inst_atan))
    tan_eq = simplify(tan(inst_acos) - tan(inst_atan))
    check(
        "(14) (T7-A) delta = arccos(1/sqrt(6)) = arctan(sqrt(5))",
        cos_eq == 0 and tan_eq == 0,
        f"cos(acos)-cos(atan) = {cos_eq}, tan(acos)-tan(atan) = {tan_eq}",
    )
    # Numerical readout (informational; exact match also covered)
    inst_deg = sp.N(sp.deg(inst_acos), 15)
    check(
        "(15) (T7-A) numerical delta in degrees ~ 65.9051574...",
        abs(float(inst_deg) - 65.9051574478893) < 1e-10,
        f"delta = {inst_deg} deg",
    )

    # Instance B: boundary (rho, eta) = (1, 0): delta = 0
    rho_b = Rational(1)
    eta_b = Rational(0)
    delta_b = atan2(eta_b, rho_b)
    check(
        "(16) (T7-B) (rho, eta) = (1, 0): delta = 0",
        simplify(delta_b) == 0,
    )
    check(
        "(17) (T7-B) (rho, eta) = (1, 0): cos^2(delta) = 1",
        simplify(cos(delta_b) ** 2) == 1,
    )
    check(
        "(18) (T7-B) (rho, eta) = (1, 0): tan(delta) = 0",
        simplify(tan(delta_b)) == 0,
    )

    # Instance C: boundary (rho, eta) = (0, 1): delta = pi/2
    # (T3)/(T6) excluded (rho = 0), but (T1), (T2) still hold.
    rho_c = Rational(0)
    eta_c = Rational(1)
    delta_c = atan2(eta_c, rho_c)
    check(
        "(19) (T7-C) (rho, eta) = (0, 1): delta = pi/2",
        simplify(delta_c - pi / 2) == 0,
    )
    check(
        "(20) (T7-C) (rho, eta) = (0, 1): cos^2(delta) = 0",
        simplify(cos(delta_c) ** 2) == 0,
    )
    check(
        "(21) (T7-C) (rho, eta) = (0, 1): sin^2(delta) = 1",
        simplify(sin(delta_c) ** 2) == 1,
    )

    # Instance D: a generic (rho, eta) = (3, 4): r = 5
    rho_d = Rational(3)
    eta_d = Rational(4)
    delta_d = atan2(eta_d, rho_d)
    check(
        "(22) (T7-D) (rho, eta) = (3, 4): cos^2(delta) = 9/25",
        simplify(cos(delta_d) ** 2 - Rational(9, 25)) == 0,
    )
    check(
        "(23) (T7-D) (rho, eta) = (3, 4): sin^2(delta) = 16/25",
        simplify(sin(delta_d) ** 2 - Rational(16, 25)) == 0,
    )
    check(
        "(24) (T7-D) (rho, eta) = (3, 4): tan(delta) = 4/3",
        simplify(tan(delta_d) - Rational(4, 3)) == 0,
    )

    # ------------------------------------------------------------------
    # (T5) numerical: lambda = 1/sqrt(2), A = sqrt(2/3), eta = sqrt(5)/6
    # gives J = lam^6 A^2 eta = (1/8) * (2/3) * sqrt(5)/6 = sqrt(5)/72
    # ------------------------------------------------------------------
    lam_p = 1 / sqrt(Rational(2))
    A_p = sqrt(Rational(2, 3))
    eta_p = sqrt(Rational(5)) / 6
    j_inst_full = simplify(lam_p ** 6 * A_p ** 2 * eta_p)
    j_inst_fact = simplify((lam_p ** 2) ** 3 * A_p ** 2 * eta_p)
    check(
        "(25) (T5 instance) full and factored evaluate equal",
        simplify(j_inst_full - j_inst_fact) == 0,
        f"J = {j_inst_full}",
    )
    j_target = sqrt(Rational(5)) / 72
    check(
        "(26) (T5 instance) value = sqrt(5)/72",
        simplify(j_inst_full - j_target) == 0,
        f"J = {j_inst_full}, target = {j_target}",
    )

    # ------------------------------------------------------------------
    # Forbidden imports check (programmatic)
    # ------------------------------------------------------------------
    import sys
    framework_modules = [
        m for m in sys.modules
        if m.startswith("toy_") or "audit" in m.lower() or "lattice" in m.lower()
    ]
    check(
        "(27) no framework / audit / lattice modules imported",
        not framework_modules,
        f"forbidden={framework_modules}" if framework_modules else "",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
