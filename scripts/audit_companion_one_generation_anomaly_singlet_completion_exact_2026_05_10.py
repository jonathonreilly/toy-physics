#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ONE_GENERATION_ANOMALY_SINGLET_COMPLETION_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is:

  (R1) Y_uR  = a + 1     = (n_color + 1) / n_color   under b = -1, a = 1/n_color
  (R2) Y_dR  = a - 1     = (1 - n_color) / n_color   under b = -1
  (R3) Y_eR  = b - 1     = -2                         under b = -1
  (R4) Y_nuR = b + 1     = 0 under b = -1, by neutral-branch convention

derived under the standard singlet charge-readout / Y-shift assignment plus
the color, mixed gauge-gravity, and cubic anomaly equations.

The runner verifies that these closed forms satisfy the three anomaly
equations parametric in n_color and a (with b = -n_color a from the
sister LH-trace narrow theorem), then specializes to the framework
n_color = 3 instance and to a non-framework n_color = 5 sanity check.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow note's
load-bearing class-A algebra holds at exact sympy precision.
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
    print("ONE_GENERATION_ANOMALY_SINGLET_COMPLETION_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: verify (R1)-(R4) closed forms satisfy anomaly equations")
    print("parametric in n_color, plus framework n_color=3 sanity")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------
    # n_color: abstract positive integer
    # a, b: LH eigenvalues with trace constraint b = -n_color * a
    # The four RH hypercharges are the unknowns.
    nc = Symbol("n_color", positive=True, integer=True)
    a, b = symbols("a b", real=True)

    # LH trace constraint imported from sister narrow theorem:
    b_constraint = -nc * a

    # Closed-form proposals for RH hypercharges from (R1)-(R4) under
    # the standard singlet charge-readout / Y-shift assignment:
    Y_uR = a + 1
    Y_dR = a - 1
    Y_eR = b - 1
    Y_nuR = b + 1  # neutral branch gives Y_nuR = 0 when b = -1

    # Under the neutral-branch convention with b = -1:
    # Substituting b = -1 gives Y_nuR = 0 directly.
    print(f"  symbolic n_color = {nc}, a, b = LH eigenvalues")
    print(f"  LH trace constraint (imported from sister narrow): b = -n_color * a")
    print(f"  (R1) Y_uR  = a + 1")
    print(f"  (R2) Y_dR  = a - 1")
    print(f"  (R3) Y_eR  = b - 1")
    print(f"  (R4) Y_nuR = b + 1 (neutral branch gives Y_nuR = 0 at b = -1)")

    # ---------------------------------------------------------------------
    section("Part 1: color SU(3)_c anomaly under closed forms")
    # ---------------------------------------------------------------------
    # Color anomaly: 2 n_color Y_QL - n_color Y_uR - n_color Y_dR = 0
    # Equivalent: 2 a - (Y_uR + Y_dR) = 0
    color_anom = 2 * nc * a - nc * Y_uR - nc * Y_dR
    A2_simplified = simplify(color_anom)
    check(
        "color SU(3)_c anomaly vanishes identically",
        A2_simplified == 0,
        detail=f"color anomaly simplifies to {A2_simplified}",
    )

    A2_div_nc = 2 * a - (Y_uR + Y_dR)
    check(
        "color anomaly /n_color form: 2a - (Y_uR + Y_dR) = 0",
        simplify(A2_div_nc) == 0,
        detail=f"2a - (Y_uR + Y_dR) simplifies to {simplify(A2_div_nc)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: mixed gauge-gravity anomaly under closed forms")
    # ---------------------------------------------------------------------
    # Mixed gauge-gravity anomaly:
    # 2 n_color Y_QL + 2 Y_LL - n_color Y_uR - n_color Y_dR - Y_eR - Y_nuR = 0
    grav_anom = (
        2 * nc * a
        + 2 * b
        - nc * Y_uR
        - nc * Y_dR
        - Y_eR
        - Y_nuR
    )
    A3_simplified = simplify(grav_anom)
    check(
        "gauge-gravity anomaly vanishes before LH trace substitution",
        A3_simplified == simplify(2 * nc * a + 2 * b - 2 * nc * a - 2 * b),
        detail=f"gauge-gravity anomaly simplifies to {A3_simplified}",
    )
    # Under the LH trace constraint b = -n_color a:
    A3_under_trace = simplify(grav_anom.subs(b, b_constraint))
    check(
        "gauge-gravity anomaly under LH trace b = -n_color a: vanishes identically",
        A3_under_trace == 0,
        detail=f"grav_anom under trace = {A3_under_trace}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: cubic [U(1)_Y]^3 anomaly under closed forms")
    # ---------------------------------------------------------------------
    # Cubic anomaly: 2 n_color Y_QL^3 + 2 Y_LL^3 - n_color Y_uR^3 - n_color Y_dR^3
    #       - Y_eR^3 - Y_nuR^3 = 0
    cubic_anom = (
        2 * nc * a**3
        + 2 * b**3
        - nc * Y_uR**3
        - nc * Y_dR**3
        - Y_eR**3
        - Y_nuR**3
    )
    A4_under_trace = simplify(cubic_anom.subs(b, b_constraint))
    check(
        "cubic anomaly under LH trace b = -n_color a: vanishes identically",
        A4_under_trace == 0,
        detail=f"cubic_anom under trace = {A4_under_trace}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (R1)-(R4) framework instance n_color = 3, b = -1, a = 1/3")
    # ---------------------------------------------------------------------
    framework = {nc: 3, a: Rational(1, 3), b: -1}

    Y_uR_at = simplify(Y_uR.subs(framework))
    Y_dR_at = simplify(Y_dR.subs(framework))
    Y_eR_at = simplify(Y_eR.subs(framework))
    Y_nuR_at = simplify(Y_nuR.subs(framework))

    check(
        "framework n_color=3: Y_uR = 4/3",
        simplify(Y_uR_at - Rational(4, 3)) == 0,
        detail=f"Y_uR = {Y_uR_at}",
    )
    check(
        "framework n_color=3: Y_dR = -2/3",
        simplify(Y_dR_at + Rational(2, 3)) == 0,
        detail=f"Y_dR = {Y_dR_at}",
    )
    check(
        "framework n_color=3: Y_eR = -2",
        simplify(Y_eR_at + 2) == 0,
        detail=f"Y_eR = {Y_eR_at}",
    )
    check(
        "framework n_color=3: Y_nuR = 0 (neutral branch under b=-1)",
        simplify(Y_nuR_at) == 0,
        detail=f"Y_nuR = {Y_nuR_at}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: anomalies vanish numerically at framework n_color = 3")
    # ---------------------------------------------------------------------
    A2_at = simplify(color_anom.subs(framework))
    A3_at = simplify(grav_anom.subs(framework))
    A4_at = simplify(cubic_anom.subs(framework))
    check(
        "framework n_color=3: (COLOR_ANOM) SU(3)_c anomaly = 0",
        A2_at == 0,
        detail=f"color_anom at framework = {A2_at}",
    )
    check(
        "framework n_color=3: (GRAV_ANOM) gauge-gravity anomaly = 0",
        A3_at == 0,
        detail=f"grav_anom at framework = {A3_at}",
    )
    check(
        "framework n_color=3: (CUBIC_ANOM) cubic [U(1)_Y]^3 anomaly = 0",
        A4_at == 0,
        detail=f"cubic_anom at framework = {A4_at}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: broad-note hypercharge readouts at n_color = 3")
    # ---------------------------------------------------------------------
    # Broad note subscripts in (1,3)_{+4/3}, (1,3)_{-2/3}, (1,1)_{-2}, (1,1)_0
    # use the same Q = T_3 + Y/2 hypercharge convention. Verify these match.
    check(
        "broad-note readout at framework n_color=3: Y_uR = 4/3",
        simplify(Y_uR_at - Rational(4, 3)) == 0,
        detail=f"Y_uR = {Y_uR_at}; broad note uses (1,3)_{{+4/3}}",
    )
    check(
        "broad-note readout at framework n_color=3: Y_dR = -2/3",
        simplify(Y_dR_at + Rational(2, 3)) == 0,
        detail=f"Y_dR = {Y_dR_at}; broad note uses (1,3)_{{-2/3}}",
    )
    check(
        "broad-note readout at framework n_color=3: Y_eR = -2",
        simplify(Y_eR_at + 2) == 0,
        detail=f"Y_eR = {Y_eR_at}; broad note uses (1,1)_{{-2}}",
    )
    check(
        "broad-note readout at framework n_color=3: Y_nuR = 0",
        simplify(Y_nuR_at) == 0,
        detail=f"Y_nuR = {Y_nuR_at}; broad note uses (1,1)_{{0}}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: non-framework instance n_color = 5, b = -1, a = 1/5")
    # ---------------------------------------------------------------------
    nonframework = {nc: 5, a: Rational(1, 5), b: -1}

    Y_uR_nf = simplify(Y_uR.subs(nonframework))
    Y_dR_nf = simplify(Y_dR.subs(nonframework))
    Y_eR_nf = simplify(Y_eR.subs(nonframework))
    Y_nuR_nf = simplify(Y_nuR.subs(nonframework))

    check(
        "non-framework n_color=5: Y_uR = 6/5",
        simplify(Y_uR_nf - Rational(6, 5)) == 0,
        detail=f"Y_uR = {Y_uR_nf}",
    )
    check(
        "non-framework n_color=5: Y_dR = -4/5",
        simplify(Y_dR_nf + Rational(4, 5)) == 0,
        detail=f"Y_dR = {Y_dR_nf}",
    )
    check(
        "non-framework n_color=5: Y_eR = -2 (independent of n_color)",
        simplify(Y_eR_nf + 2) == 0,
        detail=f"Y_eR = {Y_eR_nf}",
    )
    check(
        "non-framework n_color=5: Y_nuR = 0 (independent of n_color, neutral branch)",
        simplify(Y_nuR_nf) == 0,
        detail=f"Y_nuR = {Y_nuR_nf}",
    )

    # All anomalies vanish at non-framework instance too:
    A2_nf = simplify(color_anom.subs(nonframework))
    A3_nf = simplify(grav_anom.subs(nonframework))
    A4_nf = simplify(cubic_anom.subs(nonframework))
    check(
        "non-framework n_color=5: all three anomalies vanish",
        A2_nf == 0 and A3_nf == 0 and A4_nf == 0,
        detail=f"(color_anom, grav_anom, cubic_anom) = ({A2_nf}, {A3_nf}, {A4_nf})",
    )

    # ---------------------------------------------------------------------
    section("Part 8: discrete e_R <-> nu_R relabelling branch is anomaly-consistent")
    # ---------------------------------------------------------------------
    # The relabelled branch swaps Y_eR <-> Y_nuR. Under b = -1 that gives
    # Y_eR = 0 (the previously-neutral slot) and Y_nuR = -2. Check that the
    # anomaly equations still vanish.
    Y_eR_swap = b + 1  # was Y_nuR
    Y_nuR_swap = b - 1  # was Y_eR

    A2_swap = 2 * nc * a - nc * Y_uR - nc * Y_dR  # unchanged: quark-only
    A3_swap = (
        2 * nc * a
        + 2 * b
        - nc * Y_uR
        - nc * Y_dR
        - Y_eR_swap
        - Y_nuR_swap
    )
    A4_swap = (
        2 * nc * a**3
        + 2 * b**3
        - nc * Y_uR**3
        - nc * Y_dR**3
        - Y_eR_swap**3
        - Y_nuR_swap**3
    )
    A3_swap_under_trace = simplify(A3_swap.subs(b, b_constraint))
    A4_swap_under_trace = simplify(A4_swap.subs(b, b_constraint))

    check(
        "discrete branch e_R <-> nu_R: (GRAV_ANOM) still vanishes",
        A3_swap_under_trace == 0,
        detail=f"A3_swap = {A3_swap_under_trace}",
    )
    check(
        "discrete branch e_R <-> nu_R: (CUBIC_ANOM) still vanishes",
        A4_swap_under_trace == 0,
        detail=f"A4_swap = {A4_swap_under_trace}",
    )

    # At framework n_color = 3, b = -1:
    framework_swap = {nc: 3, a: Rational(1, 3), b: -1}
    Y_eR_swap_at = simplify(Y_eR_swap.subs(framework_swap))
    Y_nuR_swap_at = simplify(Y_nuR_swap.subs(framework_swap))
    check(
        "discrete branch at framework n_color=3: Y_eR_swap = 0, Y_nuR_swap = -2",
        simplify(Y_eR_swap_at) == 0 and simplify(Y_nuR_swap_at + 2) == 0,
        detail=f"swap: Y_eR = {Y_eR_swap_at}, Y_nuR = {Y_nuR_swap_at}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: (C1) sum of all hypercharges (gravitational trace) vanishes")
    # ---------------------------------------------------------------------
    # 2 n_color Y_QL + 2 Y_LL - n_color Y_uR - n_color Y_dR - Y_eR - Y_nuR
    # = mixed gauge-gravity anomaly. Already verified to vanish under LH trace;
    # record (C1) check.
    check(
        "(C1) gravitational-trace sum vanishes identically",
        simplify(grav_anom.subs(b, b_constraint)) == 0,
        detail="confirms mixed gauge-gravity anomaly is gravitational-trace identity (C1)",
    )

    # ---------------------------------------------------------------------
    section("Part 10: (C2) sum of right-handed Y under (R1)-(R4)")
    # ---------------------------------------------------------------------
    sum_RH = Y_uR + Y_dR + Y_eR + Y_nuR
    sum_RH_under_trace = simplify(sum_RH.subs(b, b_constraint))
    # Should equal 2a + 2b under the closed forms, simplifying further:
    # (a+1) + (a-1) + (b-1) + (b+1) = 2a + 2b.
    # Under b = -n_color a: = 2a + 2(-n_color a) = 2a(1 - n_color).
    target_C2 = 2 * a * (1 - nc)
    check(
        "(C2) sum_{R} Y_R = 2a + 2b = 2a(1 - n_color)",
        simplify(sum_RH_under_trace - target_C2) == 0,
        detail=f"sum_RH under trace = {sum_RH_under_trace}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (R1)-(R4) closed forms for Y_uR, Y_dR, Y_eR, Y_nuR")
    print("    Color SU(3)_c anomaly vanishes identically")
    print("    Gauge-gravity anomaly vanishes under LH trace b = -n_color a")
    print("    Cubic [U(1)_Y]^3 anomaly vanishes under LH trace")
    print("    Framework n_color=3: (Y_uR, Y_dR, Y_eR, Y_nuR) = (4/3, -2/3, -2, 0)")
    print("    Hypercharge readouts match broad-note rep-literal subscripts at n_color=3")
    print("    Non-framework n_color=5: (Y_uR, Y_dR, Y_eR, Y_nuR) = (6/5, -4/5, -2, 0)")
    print("    Discrete e_R <-> nu_R relabelling branch is anomaly-consistent")
    print("    (C1), (C2) corollaries verified")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
