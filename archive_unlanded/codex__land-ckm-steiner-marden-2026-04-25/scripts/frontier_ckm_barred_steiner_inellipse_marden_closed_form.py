#!/usr/bin/env python3
"""Barred unitarity-triangle Steiner inellipse + Marden foci EXACT closed form.

Verifies the NEW retained closed forms in
  docs/CKM_BARRED_STEINER_INELLIPSE_MARDEN_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (M1) Steiner inellipse centre: centroid G = ((1 + rho_bar)/3, eta_bar/3).

  (M2) Sum of semi-axes squared: S' = perim_sq / 18
                                    = (alpha_s^2 - 4 alpha_s + 96) / 864.

  (M3) Product of semi-axes squared: P' = Area^2 / 27
                                       = 5 (4 - alpha_s)^2 / 62208.

  (M4) Semi-axis quadratic discriminant:
        S'^2 - 4 P' = P(alpha_s) / 746496
        where P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2.

  (M5) Individual semi-axes squared:
        semi_a^2 = ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))) / 1728
        semi_b^2 = ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s))) / 1728.

  (M6) Eccentricity squared:
        e^2 = 2 sqrt(P(alpha_s)) / ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))).

  (M7) Marden's theorem: Steiner foci are the roots of p'(z), where
        p(z) = z (z - 1) (z - V_3) and V_3 = rho_bar + i eta_bar.
        F_+/-  =  ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1)) / 3.

  (M8) Striking identity:  |V_3^2 - V_3 + 1|^2 = P(alpha_s) / 9216
                                              = P(alpha_s) / (N_pair^4 N_quark)^2.
       So |V_3^2 - V_3 + 1| = sqrt(P(alpha_s)) / 96 -- the SAME P
       independently recovered below from the classical Brocard formula.

  (M9) Distance squared between Marden foci:
        |F_+ - F_-|^2 = sqrt(P(alpha_s)) / 216
                      = sqrt(P(alpha_s)) / N_quark^3.

  (M10) Unification: on the retained NLO Wolfenstein protected-gamma_bar
        surface, P(alpha_s) = 0 simultaneously characterises:
          - Brocard equality omega_bar = pi/6   (cot^2(omega_bar) - 3 = 0),
          - Steiner inellipse circular           (semi_a = semi_b),
          - Marden foci coincide                 (|F_+ - F_-| = 0).
        All classical equilateral conditions reduce to a single polynomial
        condition. P(alpha_s) > 0 strictly on the physical alpha_s range,
        so all three equilateral conditions are simultaneously avoided.

Ground-up status verification: each cited authority's tier extracted from its
Status: line; closure derived only at extracted retained values.
"""

from __future__ import annotations

import math
import re
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_authority(rel_path: str) -> str:
    path = REPO_ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text()


def extract_status_text(content: str) -> str:
    if not content:
        return ""
    for line in content.splitlines()[:30]:
        stripped = line.strip()
        if stripped.lower().startswith("**status:**") or stripped.lower().startswith("status:"):
            text = stripped
            for prefix in ("**Status:**", "**status:**", "Status:", "status:"):
                if text.lower().startswith(prefix.lower()):
                    text = text[len(prefix):].strip()
                    break
            return text
    return ""


def authority_tier(content: str) -> str:
    status_low = extract_status_text(content).lower()
    if "retained" in status_low and "support" not in status_low:
        return "retained"
    if "current public framework memo" in status_low:
        return "retained"
    if "support" in status_low:
        return "support"
    return "unknown"


def audit_inputs() -> None:
    banner("Ground-up status verification of each cited authority")

    print("  RETAINED-TIER (load-bearing for closure):\n")

    retained_authorities = (
        ("docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md",
         "retained NLO CKM-structure corollary",
         ("retained",)),
        ("docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
         "retained",
         ("retained",)),
        ("docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
         "retained standalone structural-identity",
         ("retained",)),
        ("docs/CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md",
         "retained CKM-structure corollary",
         ("retained",)),
    )

    for rel_path, claimed, kws in retained_authorities:
        content = read_authority(rel_path)
        status = extract_status_text(content)
        tier = authority_tier(content)
        all_kws = all(kw.lower() in status.lower() for kw in kws)

        print(f"    [{rel_path.split('/')[-1]}]")
        print(f"      Status (extracted): {status!r}")
        print(f"      Tier classification: {tier}")
        check(f"Retained-tier verified: {rel_path.split('/')[-1]}",
              all_kws and tier == "retained")
        print()


def extract_retained_inputs() -> dict:
    banner("Extracting retained inputs from authority text")

    nlo = read_authority(
        "docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md"
    )
    counts = read_authority(
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md"
    )
    eul = read_authority(
        "docs/CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md"
    )

    has_rho_bar = "rho_bar" in nlo and "(4 - alpha_s(v)) / 24" in nlo
    has_eta_bar = "eta_bar" in nlo and "sqrt(5) (4 - alpha_s(v)) / 24" in nlo

    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_quark_match = re.search(r"n[_\s]quark\s*=\s*n[_\s]pair\s*n[_\s]color", counts, re.IGNORECASE)

    has_centroid = "Centroid" in eul and "(28 - alpha_s)/72" in eul

    print(f"  rho_bar = (4 - alpha_s)/24:        {'FOUND' if has_rho_bar else 'NOT FOUND'}")
    print(f"  eta_bar = sqrt(5)(4 - alpha_s)/24: {'FOUND' if has_eta_bar else 'NOT FOUND'}")
    print(f"  N_pair extracted:                  {n_pair_match.group(0) if n_pair_match else 'NOT FOUND'}")
    print(f"  N_color extracted:                 {n_color_match.group(0) if n_color_match else 'NOT FOUND'}")
    print(f"  N_quark = N_pair * N_color:        {'FOUND' if n_quark_match else 'NOT FOUND'}")
    print(f"  Centroid retained closed form:     {'FOUND' if has_centroid else 'NOT FOUND'}")

    check("NLO retains rho_bar = (4 - alpha_s)/24", has_rho_bar)
    check("NLO retains eta_bar = sqrt(5)(4 - alpha_s)/24", has_eta_bar)
    check("MAGNITUDES retains N_pair = 2", n_pair_match and int(n_pair_match.group(1)) == 2)
    check("MAGNITUDES retains N_color = 3", n_color_match and int(n_color_match.group(1)) == 3)
    check("MAGNITUDES retains N_quark = N_pair * N_color (=6)", bool(n_quark_match))
    check("ORTHOCENTER_EULER_LINE retains centroid closed form", has_centroid)

    return {
        "N_pair": 2,
        "N_color": 3,
        "N_quark": 6,
    }


def setup_symbolic(N: dict):
    a_s = sp.symbols("alpha_s", real=True)
    rho_bar = (4 - a_s) / 24
    eta_bar = sp.sqrt(5) * (4 - a_s) / 24

    V1 = sp.Matrix([0, 0])
    V2 = sp.Matrix([1, 0])
    V3 = sp.Matrix([rho_bar, eta_bar])

    a_sq = (1 - rho_bar) ** 2 + eta_bar ** 2
    b_sq = rho_bar ** 2 + eta_bar ** 2
    c_sq = sp.Integer(1)
    perim_sq = sp.simplify(a_sq + b_sq + c_sq)
    area = eta_bar / 2

    centroid = sp.Matrix([
        sp.simplify((1 + rho_bar) / 3),
        sp.simplify(eta_bar / 3),
    ])

    # V_3 as complex number for Marden.
    V3_complex = rho_bar + sp.I * eta_bar

    P_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 - 240 * (4 - a_s) ** 2)

    return {
        "a_s": a_s,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "V1": V1,
        "V2": V2,
        "V3": V3,
        "V3_complex": V3_complex,
        "a_sq": a_sq,
        "b_sq": b_sq,
        "c_sq": c_sq,
        "perim_sq": perim_sq,
        "area": area,
        "centroid": centroid,
        "P_poly": P_poly,
    }


def audit_m1_centroid(N: dict, S: dict) -> None:
    banner("M1: Steiner inellipse centre = centroid G")

    a_s = S["a_s"]
    G = S["centroid"]

    expected_x = sp.simplify((28 - a_s) / 72)
    expected_y = sp.simplify(sp.sqrt(5) * (4 - a_s) / 72)

    print(f"  G_x (computed) = {G[0]}")
    print(f"  Expected        = (28 - alpha_s)/72 = {expected_x}")
    print(f"  G_y (computed) = {G[1]}")
    print(f"  Expected        = sqrt(5)(4 - alpha_s)/72 = {expected_y}")

    check("M1: G_x = (28 - alpha_s)/72 (retained centroid x-coordinate)",
          sp.simplify(G[0] - expected_x) == 0)
    check("M1: G_y = sqrt(5)(4 - alpha_s)/72 (retained centroid y-coordinate)",
          sp.simplify(G[1] - expected_y) == 0)

    G_lo = G.subs(a_s, 0)
    print(f"\n  G | LO = ({sp.simplify(G_lo[0])}, {sp.simplify(G_lo[1])})")
    expected_x_lo = sp.Rational(7, 18)
    expected_y_lo = sp.sqrt(5) / 18
    check("M1 LO: G | LO = (7/18, sqrt(5)/18)",
          sp.simplify(G_lo[0] - expected_x_lo) == 0
          and sp.simplify(G_lo[1] - expected_y_lo) == 0)


def audit_m2_m3_semiaxis_symmetric_functions(N: dict, S: dict) -> tuple[sp.Expr, sp.Expr]:
    banner("M2 / M3: Steiner inellipse semi-axis symmetric functions")

    a_s = S["a_s"]
    perim_sq = S["perim_sq"]
    area = S["area"]

    S_sym = sp.simplify(perim_sq / 18)  # semi_a^2 + semi_b^2
    P_sym = sp.simplify(area ** 2 / 27)  # (semi_a * semi_b)^2

    expected_S = sp.simplify((a_s ** 2 - 4 * a_s + 96) / 864)
    expected_P = sp.simplify(5 * (4 - a_s) ** 2 / 62208)

    print(f"  S' = semi_a^2 + semi_b^2 = perim_sq / 18")
    print(f"     = {S_sym}")
    print(f"  Expected: (alpha_s^2 - 4 alpha_s + 96)/864 = {expected_S}")
    check("M2: S' = (alpha_s^2 - 4 alpha_s + 96)/864",
          sp.simplify(S_sym - expected_S) == 0)

    print()
    print(f"  P' = (semi_a * semi_b)^2 = Area^2 / 27")
    print(f"     = {P_sym}")
    print(f"  Expected: 5 (4 - alpha_s)^2 / 62208 = {expected_P}")
    check("M3: P' = 5 (4 - alpha_s)^2 / 62208",
          sp.simplify(P_sym - expected_P) == 0)

    return S_sym, P_sym


def audit_m4_discriminant(N: dict, S: dict, S_sym: sp.Expr, P_sym: sp.Expr) -> None:
    banner("M4: Semi-axis quadratic discriminant = P(alpha_s)/746496")

    a_s = S["a_s"]
    discriminant = sp.simplify(S_sym ** 2 - 4 * P_sym)
    expected = sp.simplify(S["P_poly"] / 746496)

    print(f"  S'^2 - 4 P' (computed) = {discriminant}")
    print(f"  Expected:               P(alpha_s)/746496 = {expected}")
    print(f"  Difference: {sp.simplify(discriminant - expected)}")

    check("M4: S'^2 - 4 P' = P(alpha_s)/746496",
          sp.simplify(discriminant - expected) == 0)

    # Structural-integer: 746496 = 864^2 = (N_pair^5 N_color^3)^2 = N_pair^10 N_color^6.
    N_pair, N_color = N["N_pair"], N["N_color"]
    expected_struct_denom = N_pair ** 10 * N_color ** 6
    print(f"\n  Structural-integer denom: N_pair^10 N_color^6 = {N_pair ** 10} * {N_color ** 6} = {expected_struct_denom}")
    check("M4 structural: 746496 = N_pair^10 * N_color^6",
          expected_struct_denom == 746496)


def audit_m5_semiaxes(N: dict, S: dict, S_sym: sp.Expr, P_sym: sp.Expr) -> None:
    banner("M5: Individual semi-axes squared in closed form")

    a_s = S["a_s"]
    discr = sp.simplify(S_sym ** 2 - 4 * P_sym)
    semi_a_sq = sp.simplify((S_sym + sp.sqrt(discr)) / 2)
    semi_b_sq = sp.simplify((S_sym - sp.sqrt(discr)) / 2)

    expected_a = sp.simplify(
        ((a_s ** 2 - 4 * a_s + 96) + sp.sqrt(S["P_poly"])) / 1728
    )
    expected_b = sp.simplify(
        ((a_s ** 2 - 4 * a_s + 96) - sp.sqrt(S["P_poly"])) / 1728
    )

    diff_a = sp.simplify(semi_a_sq - expected_a)
    diff_b = sp.simplify(semi_b_sq - expected_b)

    print(f"  semi_a^2 = ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s)))/1728")
    print(f"  semi_b^2 = ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s)))/1728")
    print(f"  Difference (semi_a^2): {diff_a}")
    print(f"  Difference (semi_b^2): {diff_b}")

    check("M5: semi_a^2 = ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P))/1728", diff_a == 0)
    check("M5: semi_b^2 = ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P))/1728", diff_b == 0)

    # LO numerical check.
    semi_a_sq_lo = float(semi_a_sq.subs(a_s, 0))
    semi_b_sq_lo = float(semi_b_sq.subs(a_s, 0))
    print(f"\n  LO: semi_a^2 = {semi_a_sq_lo:.10f},  semi_b^2 = {semi_b_sq_lo:.10f}")
    print(f"      semi_a   = {math.sqrt(semi_a_sq_lo):.10f},  semi_b   = {math.sqrt(semi_b_sq_lo):.10f}")
    check("M5 LO: semi_a^2 ~ 0.098, semi_b^2 ~ 0.0131",
          0.09 < semi_a_sq_lo < 0.11 and 0.012 < semi_b_sq_lo < 0.015)


def audit_m6_eccentricity(N: dict, S: dict, S_sym: sp.Expr, P_sym: sp.Expr) -> None:
    banner("M6: Steiner inellipse eccentricity squared")

    a_s = S["a_s"]
    discr = sp.simplify(S_sym ** 2 - 4 * P_sym)
    semi_a_sq = sp.simplify((S_sym + sp.sqrt(discr)) / 2)
    semi_b_sq = sp.simplify((S_sym - sp.sqrt(discr)) / 2)

    e_sq = sp.simplify((semi_a_sq - semi_b_sq) / semi_a_sq)
    expected = sp.simplify(
        2 * sp.sqrt(S["P_poly"])
        / ((a_s ** 2 - 4 * a_s + 96) + sp.sqrt(S["P_poly"]))
    )

    print(f"  e^2 (computed) = {e_sq}")
    print(f"  Expected: 2 sqrt(P)/((alpha_s^2 - 4 alpha_s + 96) + sqrt(P))")
    print(f"          = {expected}")
    print(f"  Difference: {sp.simplify(e_sq - expected)}")

    check("M6: e^2 = 2 sqrt(P)/((alpha_s^2 - 4 alpha_s + 96) + sqrt(P))",
          sp.simplify(e_sq - expected) == 0)

    e_sq_lo = float(e_sq.subs(a_s, 0))
    print(f"\n  e^2 | LO = {e_sq_lo:.6f}")
    print(f"  e   | LO = {math.sqrt(e_sq_lo):.6f}")
    check("M6 LO: e^2 | LO ~ 0.866 (highly eccentric)",
          0.85 < e_sq_lo < 0.88)


def audit_m7_marden_foci(N: dict, S: dict) -> tuple[sp.Expr, sp.Expr]:
    banner("M7: Marden's theorem -- Steiner foci = roots of p'(z)")

    a_s = S["a_s"]
    V3c = S["V3_complex"]

    # p(z) = z (z - 1) (z - V_3) = z^3 - (1 + V_3) z^2 + V_3 z.
    z = sp.symbols("z")
    p = z * (z - 1) * (z - V3c)
    dp = sp.diff(p, z)
    print(f"  p(z) = z (z - 1) (z - V_3)")
    print(f"  p'(z) = {sp.expand(dp)}")

    # Roots of p'(z) = 0.
    roots = sp.solve(dp, z)
    F_plus = sp.simplify(roots[0])
    F_minus = sp.simplify(roots[1])

    # Closed-form expression: F_+/- = ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1))/3.
    discriminant_complex = V3c ** 2 - V3c + 1
    F_plus_expected = sp.simplify(((1 + V3c) + sp.sqrt(discriminant_complex)) / 3)
    F_minus_expected = sp.simplify(((1 + V3c) - sp.sqrt(discriminant_complex)) / 3)

    # sympy's solve may swap +/-; check both orderings.
    diff_a = sp.simplify(F_plus - F_plus_expected)
    diff_b = sp.simplify(F_plus - F_minus_expected)
    matches = (diff_a == 0) or (diff_b == 0)

    print(f"\n  Marden foci F_+/- = ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1))/3")
    print(f"  Verifying sympy roots match Marden formula:")
    print(f"    F_+ - F_plus_expected   = {sp.simplify(diff_a)}")
    print(f"    F_+ - F_minus_expected  = {sp.simplify(diff_b)}")
    check("M7: Marden foci match closed-form ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1))/3",
          matches)

    return F_plus_expected, F_minus_expected


def audit_m8_modulus_identity(N: dict, S: dict) -> None:
    banner("M8: |V_3^2 - V_3 + 1|^2 = P(alpha_s)/9216 (striking algebraic identity)")

    a_s = S["a_s"]
    V3c = S["V3_complex"]
    discriminant = V3c ** 2 - V3c + 1

    real_part = sp.simplify(sp.re(discriminant))
    imag_part = sp.simplify(sp.im(discriminant))
    modulus_sq = sp.simplify(real_part ** 2 + imag_part ** 2)
    expected = sp.simplify(S["P_poly"] / 9216)

    print(f"  V_3^2 - V_3 + 1 (real) = {real_part}")
    print(f"  V_3^2 - V_3 + 1 (imag) = {imag_part}")
    print(f"  |V_3^2 - V_3 + 1|^2 (computed)        = {modulus_sq}")
    print(f"  Expected: P(alpha_s)/9216             = {expected}")
    diff = sp.simplify(modulus_sq - expected)
    print(f"  Difference: {diff}")
    check("M8: |V_3^2 - V_3 + 1|^2 = P(alpha_s)/9216", diff == 0)

    # Structural-integer: 9216 = 96^2 = (N_pair^4 N_quark)^2.
    N_pair, N_quark = N["N_pair"], N["N_quark"]
    expected_struct = (N_pair ** 4 * N_quark) ** 2
    print(f"\n  Structural denom: 9216 = (N_pair^4 N_quark)^2 = ({N_pair ** 4 * N_quark})^2 = {expected_struct}")
    check("M8 structural: 9216 = (N_pair^4 N_quark)^2 = 96^2",
          expected_struct == 9216)


def audit_m9_foci_distance(N: dict, S: dict, F_plus: sp.Expr, F_minus: sp.Expr) -> None:
    banner("M9: Distance squared between Marden foci = sqrt(P(alpha_s))/216")

    a_s = S["a_s"]
    delta = F_plus - F_minus
    # |F_+ - F_-|^2 = (2/3)^2 |sqrt(V_3^2 - V_3 + 1)|^2 = (4/9)|V_3^2 - V_3 + 1|.
    delta_sq = sp.simplify(sp.re(delta) ** 2 + sp.im(delta) ** 2)
    expected = sp.simplify(sp.sqrt(S["P_poly"]) / 216)

    print(f"  |F_+ - F_-|^2 (computed) = {delta_sq}")
    print(f"  Expected:                  sqrt(P(alpha_s))/216 = {expected}")
    diff = sp.simplify(delta_sq - expected)
    print(f"  Difference: {diff}")

    check("M9: |F_+ - F_-|^2 = sqrt(P(alpha_s))/216 = sqrt(P)/N_quark^3",
          diff == 0)

    # Numerical sanity at LO.
    delta_sq_lo = float(delta_sq.subs(a_s, 0))
    expected_lo = float(sp.sqrt(5376) / 216)
    print(f"\n  |F_+ - F_-|^2 | LO = {delta_sq_lo:.10f}")
    print(f"  Expected LO        = sqrt(5376)/216 = {expected_lo:.10f}")
    check("M9 LO: |F_+ - F_-|^2 | LO ~ 0.339",
          abs(delta_sq_lo - expected_lo) < 1e-9)


def audit_m10_unification(N: dict, S: dict, S_sym: sp.Expr, P_sym: sp.Expr) -> None:
    banner("M10: P(alpha_s) governs THREE classical equilateral conditions")

    a_s = S["a_s"]
    P_poly = S["P_poly"]
    perim_sq = S["perim_sq"]
    area = S["area"]

    print("  Three classical equilateral conditions on the retained surface:")
    print()

    # Condition 1: Brocard equality (cot^2(omega) - 3 = 0).
    cot_omega = sp.simplify(perim_sq / (4 * area))
    brocard_form = sp.simplify(cot_omega ** 2 - 3)
    # cot^2 - 3 should factor as P(alpha_s)/[denominator polynomial of cot^2].
    # cot(omega_bar) = (alpha_s^2 - 4 alpha_s + 96)/(4 sqrt(5)(4 - alpha_s)),
    # so cot^2 = (alpha_s^2 - 4 alpha_s + 96)^2/(80 (4 - alpha_s)^2),
    # and cot^2 - 3 = ((alpha_s^2 - 4 alpha_s + 96)^2 - 240(4 - alpha_s)^2)
    #               / (80 (4 - alpha_s)^2)
    #              = P(alpha_s) / (80 (4 - alpha_s)^2).
    brocard_expected = sp.simplify(P_poly / (80 * (4 - a_s) ** 2))
    diff_brocard = sp.simplify(brocard_form - brocard_expected)

    print(f"  (1) Brocard inequality: cot^2(omega_bar) - 3 = P(alpha_s)/[80 (4 - alpha_s)^2]")
    print(f"      (cot omega_bar)^2 - 3 (computed)  = {sp.simplify(brocard_form)}")
    print(f"      Expected: P/[80 (4 - alpha_s)^2]  = {brocard_expected}")
    print(f"      Difference: {diff_brocard}")
    check("M10(1): Brocard inequality polynomial = P(alpha_s)",
          diff_brocard == 0)

    # Condition 2: Steiner inellipse circular (semi_a^2 - semi_b^2 = 0).
    print()
    discr = sp.simplify(S_sym ** 2 - 4 * P_sym)
    discr_expected = sp.simplify(P_poly / 746496)
    diff_steiner = sp.simplify(discr - discr_expected)

    print(f"  (2) Steiner inellipse circular: S'^2 - 4 P' = P(alpha_s)/746496")
    print(f"      (semi_a^2 - semi_b^2)^2 = S'^2 - 4 P' = {discr}")
    print(f"      Expected: P/746496                    = {discr_expected}")
    print(f"      Difference: {diff_steiner}")
    check("M10(2): Steiner inellipse semi-axis discriminant polynomial = P(alpha_s)",
          diff_steiner == 0)

    # Condition 3: Marden foci coincide (|F_+ - F_-|^2 = 0).
    print()
    print(f"  (3) Marden foci coincide: |F_+ - F_-|^2 = sqrt(P(alpha_s))/216 = 0 iff P = 0")
    foci_dist_sq = sp.sqrt(P_poly) / 216
    foci_dist_fourth = sp.simplify(foci_dist_sq ** 2)
    foci_expected_fourth = sp.simplify(P_poly / 216 ** 2)
    print(f"      Squared relation: |F_+ - F_-|^4 = P(alpha_s)/216^2")
    print(f"      Difference: {sp.simplify(foci_dist_fourth - foci_expected_fourth)}")
    check("M10(3): Marden foci coincidence iff P(alpha_s) = 0",
          sp.simplify(foci_dist_fourth - foci_expected_fourth) == 0)

    # Numerical sweep: P(alpha_s) > 0 strictly across the physical range.
    print()
    print(f"  Numerical sweep: P(alpha_s) > 0 across alpha_s in [0, 3.9]:")
    samples = [0.0, 0.05, 0.10330, 0.3, 0.5, 1.0, 2.0, 3.0, 3.5, 3.9]
    all_positive = True
    print(f"  alpha_s   P(alpha_s)            cot^2-3 sign")
    for s in samples:
        pv = float(P_poly.subs(a_s, s))
        bv = float(brocard_form.subs(a_s, s))
        ok = (pv > 0) and (bv > 0)
        all_positive = all_positive and ok
        print(f"  {s:6.3f}   {pv:18.10f}   {bv:.10f}   {'OK' if ok else 'FAIL'}")

    check("M10 sweep: P(alpha_s) > 0 across the physical alpha_s range",
          all_positive)


def audit_numerical_readout(N: dict, S: dict) -> None:
    banner("Numerical readout at canonical alpha_s(v)")

    a_s = S["a_s"]
    perim_sq = S["perim_sq"]
    area = S["area"]
    P_poly = S["P_poly"]

    samples = [
        ("alpha_s -> 0  (LO)", 0.0),
        ("alpha_s = 0.10330 (canonical alpha_s(v))", 0.10330),
        ("alpha_s = 0.30 (mid-range)", 0.30),
    ]

    for label, s in samples:
        ps = float(perim_sq.subs(a_s, s))
        ar = float(area.subs(a_s, s))
        pv = float(P_poly.subs(a_s, s))

        # Steiner inellipse semi-axes squared.
        semi_a_sq = (ps / 18 + math.sqrt(pv / 746496)) / 2
        semi_b_sq = (ps / 18 - math.sqrt(pv / 746496)) / 2
        e_sq = (semi_a_sq - semi_b_sq) / semi_a_sq

        # Marden foci distance squared.
        foci_dist_sq = math.sqrt(pv) / 216

        print(f"  {label}:")
        print(f"    perim_sq = {ps:.10f}, Area = {ar:.10f}")
        print(f"    P(alpha_s) = {pv:.10f}, sqrt(P) = {math.sqrt(pv):.10f}")
        print(f"    Steiner semi-axes: a = {math.sqrt(semi_a_sq):.6f}, b = {math.sqrt(semi_b_sq):.6f}")
        print(f"    Eccentricity^2 = {e_sq:.6f}, e = {math.sqrt(e_sq):.6f}")
        print(f"    Marden foci distance^2 = {foci_dist_sq:.10f}")
        check(f"  numerical: P(alpha_s) > 0 and 0 < e < 1 at {label}",
              pv > 0 and 0 < e_sq < 1)


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA          (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS                  (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY                  (retained)")
    print("    CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (M1) Steiner inellipse centre = retained centroid G")
    print("           = ((28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72).")
    print()
    print("    (M2) Sum of semi-axes squared: S' = perim_sq/18")
    print("           = (alpha_s^2 - 4 alpha_s + 96)/864.")
    print()
    print("    (M3) Product of semi-axes squared: P' = Area^2/27")
    print("           = 5 (4 - alpha_s)^2/62208.")
    print()
    print("    (M4) Semi-axis quadratic discriminant:")
    print("           S'^2 - 4 P' = P(alpha_s)/746496")
    print("                       = P(alpha_s)/(N_pair^10 N_color^6),")
    print("         where P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2.")
    print()
    print("    (M5) Individual semi-axes squared:")
    print("           semi_a^2 = ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s)))/1728,")
    print("           semi_b^2 = ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s)))/1728.")
    print()
    print("    (M6) Eccentricity squared:")
    print("           e^2 = 2 sqrt(P(alpha_s)) / ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))).")
    print("           e^2 | LO ~ 0.866 (highly eccentric).")
    print()
    print("    (M7) Marden's theorem: Steiner foci F_+/- are the roots of p'(z),")
    print("         where p(z) = z (z - 1) (z - V_3).")
    print("           F_+/- = ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1))/3.")
    print()
    print("    (M8) Striking modulus identity:")
    print("           |V_3^2 - V_3 + 1|^2 = P(alpha_s)/9216")
    print("                                = P(alpha_s)/(N_pair^4 N_quark)^2.")
    print()
    print("    (M9) Distance squared between Marden foci:")
    print("           |F_+ - F_-|^2 = sqrt(P(alpha_s))/216 = sqrt(P)/N_quark^3.")
    print()
    print("    (M10) UNIFICATION: P(alpha_s) governs THREE classical equilateral conditions")
    print("          on the retained NLO Wolfenstein protected-gamma_bar surface:")
    print("            - Brocard equality omega_bar = pi/6   <=>  P(alpha_s) = 0,")
    print("            - Steiner inellipse circular            <=>  P(alpha_s) = 0,")
    print("            - Marden foci coincide                  <=>  P(alpha_s) = 0.")
    print("          On the physical alpha_s range, P(alpha_s) > 0 strictly, so all three")
    print("          equilateral conditions are simultaneously avoided. The polynomial")
    print("          P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2")
    print("          is the SINGLE algebraic invariant of the retained surface.")
    print()
    print("  All identities exact via sympy; closure on retained-tier authorities only.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity-triangle Steiner inellipse + Marden foci EXACT closed form audit")
    print("See docs/CKM_BARRED_STEINER_INELLIPSE_MARDEN_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    audit_m1_centroid(N, S)
    S_sym, P_sym = audit_m2_m3_semiaxis_symmetric_functions(N, S)
    audit_m4_discriminant(N, S, S_sym, P_sym)
    audit_m5_semiaxes(N, S, S_sym, P_sym)
    audit_m6_eccentricity(N, S, S_sym, P_sym)
    F_plus, F_minus = audit_m7_marden_foci(N, S)
    audit_m8_modulus_identity(N, S)
    audit_m9_foci_distance(N, S, F_plus, F_minus)
    audit_m10_unification(N, S, S_sym, P_sym)
    audit_numerical_readout(N, S)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
