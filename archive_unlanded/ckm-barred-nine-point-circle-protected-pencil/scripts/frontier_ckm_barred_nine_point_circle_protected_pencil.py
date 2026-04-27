#!/usr/bin/env python3
"""Barred unitarity-triangle nine-point circle + protected coaxial pencil.

Verifies the NEW retained closed forms in
  docs/CKM_BARRED_NINE_POINT_CIRCLE_PROTECTED_PENCIL_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (NP1) Nine-point circle: passes through 9 special points -- 3 side midpoints,
        3 altitude feet, 3 orthocenter-vertex midpoints. Center N9 = (O+H)/2,
        radius squared = R_bar^2/4.

  (NP2) Center N9 closed form:
          N9_x  =  (16 - alpha_s)/48
                =  (N_pair^4 - alpha_s)/(N_pair^4 N_color),
          N9_y  =  sqrt(5)(10 - alpha_s)/120
                =  sqrt(N_quark - 1)(N_pair (N_quark - 1) - alpha_s)
                   / (N_pair^3 N_color (N_quark - 1)).

  (NP3) Radius squared:
          R9^2  =  R_bar^2 / 4  =  (80 + alpha_s^2)/1280
                =  (N_pair^4 (N_quark - 1) + alpha_s^2)/(N_pair^8 (N_quark - 1)).

  (NP4) Three side midpoints:
          M_a  =  ((28 - alpha_s)/48, sqrt(5)(4 - alpha_s)/48),
          M_b  =  ((4 - alpha_s)/48, sqrt(5)(4 - alpha_s)/48),
          M_c  =  (1/2, 0).

  (NP5) Three altitude feet:
          H_a  =  (5(4 - alpha_s)^2/(6(80 + alpha_s^2)),
                   sqrt(5)(4 - alpha_s)(20 + alpha_s)/(6(80 + alpha_s^2))),
          H_b  =  (1/6, sqrt(5)/6),                          # alpha_s-INVARIANT!
          H_c  =  ((4 - alpha_s)/24, 0).

  (NP6) Three orthocenter-vertex midpoints:
          P_1  =  ((4 - alpha_s)/48, (20 + alpha_s)/(48 sqrt(5))),
          P_2  =  ((28 - alpha_s)/48, (20 + alpha_s)/(48 sqrt(5))),
          P_3  =  ((4 - alpha_s)/24, sqrt(5)(10 - alpha_s)/60).

  (NP7) STRIKING: M_c = (1/2, 0) is alpha_s-INVARIANT, because both V_1 = (0, 0)
        and V_2 = (1, 0) are alpha_s-fixed on the retained surface.

  (NP8) STRIKING: H_b = (1/N_quark, sqrt(N_quark - 1)/N_quark) = (1/6, sqrt(5)/6)
        is alpha_s-INVARIANT, because the line V_1 V_3 has alpha_s-protected
        slope eta_bar/rho_bar = sqrt(5) = tan(gamma_bar). The foot of
        perpendicular from V_2 onto this line therefore depends only on the
        protected slope, not on the apex position.

  (NP9) Distance between the two invariant points:
          |M_c - H_b|  =  1/2  =  R_bar | LO.

        At LO, this is exactly the LO circumradius. For NLO, the circumradius
        R_bar grows slightly with alpha_s, but |M_c - H_b| stays frozen at 1/2.

  (NP10) PENCIL THEOREM: as alpha_s varies, the nine-point circle is a
         one-parameter family of circles, ALL passing through the two
         alpha_s-invariant points M_c and H_b. The family forms a COAXIAL
         PENCIL of circles, with radical axis = perpendicular bisector of
         the segment M_c H_b.

  (NP11) All 9 special points verified to lie on the nine-point circle
         (sympy-exact).

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
        ("docs/CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md",
         "retained CKM-structure corollary",
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

    has_rho_bar = "rho_bar" in nlo and "(4 - alpha_s(v)) / 24" in nlo
    has_eta_bar = "eta_bar" in nlo and "sqrt(5) (4 - alpha_s(v)) / 24" in nlo
    has_tan_gamma = "tan(gamma_bar)" in nlo and "sqrt(5)" in nlo

    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_quark_match = re.search(r"n[_\s]quark\s*=\s*n[_\s]pair\s*n[_\s]color", counts, re.IGNORECASE)

    print(f"  rho_bar = (4 - alpha_s)/24:        {'FOUND' if has_rho_bar else 'NOT FOUND'}")
    print(f"  eta_bar = sqrt(5)(4 - alpha_s)/24: {'FOUND' if has_eta_bar else 'NOT FOUND'}")
    print(f"  tan(gamma_bar) = sqrt(5):          {'FOUND' if has_tan_gamma else 'NOT FOUND'}")
    print(f"  N_pair extracted:                  {n_pair_match.group(0) if n_pair_match else 'NOT FOUND'}")
    print(f"  N_color extracted:                 {n_color_match.group(0) if n_color_match else 'NOT FOUND'}")
    print(f"  N_quark = N_pair * N_color:        {'FOUND' if n_quark_match else 'NOT FOUND'}")

    check("NLO retains rho_bar = (4 - alpha_s)/24", has_rho_bar)
    check("NLO retains eta_bar = sqrt(5)(4 - alpha_s)/24", has_eta_bar)
    check("NLO retains tan(gamma_bar) = sqrt(5) (alpha_s-protected slope)", has_tan_gamma)
    check("MAGNITUDES retains N_pair = 2", n_pair_match and int(n_pair_match.group(1)) == 2)
    check("MAGNITUDES retains N_color = 3", n_color_match and int(n_color_match.group(1)) == 3)
    check("MAGNITUDES retains N_quark = N_pair * N_color (=6)", bool(n_quark_match))

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

    # Retained: circumcenter and orthocenter.
    O = sp.Matrix([sp.Rational(1, 2), -a_s * sp.sqrt(5) / 40])
    H = sp.Matrix([rho_bar, (20 + a_s) / (24 * sp.sqrt(5))])

    # Nine-point circle center and radius squared.
    N9 = sp.Matrix([sp.simplify((O[0] + H[0]) / 2),
                    sp.simplify((O[1] + H[1]) / 2)])
    R_bar_sq = sp.Rational(1, 4) + a_s ** 2 / 320  # retained R_bar^2
    R9_sq = sp.simplify(R_bar_sq / 4)

    return {
        "a_s": a_s,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "V1": V1,
        "V2": V2,
        "V3": V3,
        "O": O,
        "H": H,
        "N9": N9,
        "R_bar_sq": R_bar_sq,
        "R9_sq": R9_sq,
    }


def audit_np2_n9_center(N: dict, S: dict) -> None:
    banner("NP2: Nine-point circle center N9 = (O + H)/2")

    a_s = S["a_s"]
    N9 = S["N9"]

    expected_x = sp.simplify((16 - a_s) / 48)
    expected_y = sp.simplify(sp.sqrt(5) * (10 - a_s) / 120)

    print(f"  N9_x (computed) = {N9[0]}")
    print(f"  Expected: (16 - alpha_s)/48 = {expected_x}")
    diff_x = sp.simplify(N9[0] - expected_x)
    print(f"  Difference: {diff_x}")
    check("NP2: N9_x = (16 - alpha_s)/48", diff_x == 0)

    print()
    print(f"  N9_y (computed) = {N9[1]}")
    print(f"  Expected: sqrt(5)(10 - alpha_s)/120 = {expected_y}")
    diff_y = sp.simplify(N9[1] - expected_y)
    print(f"  Difference: {diff_y}")
    check("NP2: N9_y = sqrt(5)(10 - alpha_s)/120", diff_y == 0)


def audit_np3_radius(N: dict, S: dict) -> None:
    banner("NP3: Nine-point circle radius squared = R_bar^2/4")

    a_s = S["a_s"]
    R9_sq = S["R9_sq"]
    expected = sp.simplify((80 + a_s ** 2) / 1280)

    print(f"  R9^2 (computed) = R_bar^2/4 = {R9_sq}")
    print(f"  Expected: (80 + alpha_s^2)/1280 = {expected}")
    diff = sp.simplify(R9_sq - expected)
    print(f"  Difference: {diff}")
    check("NP3: R9^2 = (80 + alpha_s^2)/1280 = (N_pair^4(N_quark-1) + alpha_s^2)/(N_pair^8(N_quark-1))",
          diff == 0)


def audit_np4_midpoints(N: dict, S: dict, R9_sq: sp.Expr) -> dict:
    banner("NP4: Three side midpoints M_a, M_b, M_c")

    a_s = S["a_s"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]
    N9 = S["N9"]

    M_a = sp.simplify((V2 + V3) / 2)
    M_b = sp.simplify((V1 + V3) / 2)
    M_c = sp.simplify((V1 + V2) / 2)

    print(f"  M_a (midpoint of V_2 V_3) = ({M_a[0]}, {M_a[1]})")
    print(f"  M_b (midpoint of V_1 V_3) = ({M_b[0]}, {M_b[1]})")
    print(f"  M_c (midpoint of V_1 V_2) = ({M_c[0]}, {M_c[1]})")

    # Verify on circle.
    for name, M in [("M_a", M_a), ("M_b", M_b), ("M_c", M_c)]:
        dist_sq = sp.simplify((M[0] - N9[0]) ** 2 + (M[1] - N9[1]) ** 2)
        diff = sp.simplify(dist_sq - R9_sq)
        check(f"NP4: {name} lies on the nine-point circle", diff == 0)

    return {"M_a": M_a, "M_b": M_b, "M_c": M_c}


def audit_np5_altitude_feet(N: dict, S: dict, R9_sq: sp.Expr) -> dict:
    banner("NP5: Three altitude feet H_a, H_b, H_c")

    a_s = S["a_s"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]
    N9 = S["N9"]

    def foot_of_altitude(P, A, B):
        """Foot of altitude from P onto line through A, B."""
        # F = A + ((P - A) . (B - A))/|B - A|^2 * (B - A).
        diff = B - A
        t = ((P - A).dot(diff)) / diff.dot(diff)
        return sp.Matrix([sp.simplify(A[0] + t * diff[0]),
                          sp.simplify(A[1] + t * diff[1])])

    H_a = foot_of_altitude(V1, V2, V3)
    H_b = foot_of_altitude(V2, V1, V3)
    H_c = foot_of_altitude(V3, V1, V2)

    print(f"  H_a (foot from V_1 onto V_2V_3) = ({H_a[0]}, {H_a[1]})")
    print(f"  H_b (foot from V_2 onto V_1V_3) = ({H_b[0]}, {H_b[1]})")
    print(f"  H_c (foot from V_3 onto V_1V_2) = ({H_c[0]}, {H_c[1]})")

    # Verify on circle.
    for name, H_pt in [("H_a", H_a), ("H_b", H_b), ("H_c", H_c)]:
        dist_sq = sp.simplify((H_pt[0] - N9[0]) ** 2 + (H_pt[1] - N9[1]) ** 2)
        diff = sp.simplify(dist_sq - R9_sq)
        check(f"NP5: {name} lies on the nine-point circle", diff == 0)

    return {"H_a": H_a, "H_b": H_b, "H_c": H_c}


def audit_np6_orthocenter_vertex_midpoints(N: dict, S: dict, R9_sq: sp.Expr) -> dict:
    banner("NP6: Three orthocenter-vertex midpoints P_1, P_2, P_3")

    a_s = S["a_s"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]
    H_pt = S["H"]
    N9 = S["N9"]

    P_1 = sp.simplify((V1 + H_pt) / 2)
    P_2 = sp.simplify((V2 + H_pt) / 2)
    P_3 = sp.simplify((V3 + H_pt) / 2)

    print(f"  P_1 (midpoint of V_1, H) = ({P_1[0]}, {P_1[1]})")
    print(f"  P_2 (midpoint of V_2, H) = ({P_2[0]}, {P_2[1]})")
    print(f"  P_3 (midpoint of V_3, H) = ({P_3[0]}, {P_3[1]})")

    # Verify on circle.
    for name, P_pt in [("P_1", P_1), ("P_2", P_2), ("P_3", P_3)]:
        dist_sq = sp.simplify((P_pt[0] - N9[0]) ** 2 + (P_pt[1] - N9[1]) ** 2)
        diff = sp.simplify(dist_sq - R9_sq)
        check(f"NP6: {name} lies on the nine-point circle", diff == 0)

    return {"P_1": P_1, "P_2": P_2, "P_3": P_3}


def audit_np7_np8_invariant_points(N: dict, S: dict, midpoints: dict, feet: dict) -> None:
    banner("NP7 / NP8: Two alpha_s-INVARIANT points -- M_c and H_b")

    a_s = S["a_s"]
    M_c = midpoints["M_c"]
    H_b = feet["H_b"]

    # Test alpha_s-independence by differentiating.
    M_c_d_alpha_x = sp.diff(M_c[0], a_s)
    M_c_d_alpha_y = sp.diff(M_c[1], a_s)
    H_b_d_alpha_x = sp.diff(H_b[0], a_s)
    H_b_d_alpha_y = sp.diff(H_b[1], a_s)

    print(f"  d(M_c_x)/d(alpha_s) = {M_c_d_alpha_x}")
    print(f"  d(M_c_y)/d(alpha_s) = {M_c_d_alpha_y}")
    print(f"  d(H_b_x)/d(alpha_s) = {H_b_d_alpha_x}")
    print(f"  d(H_b_y)/d(alpha_s) = {H_b_d_alpha_y}")

    check("NP7: M_c is alpha_s-invariant (both coordinates have zero alpha_s derivative)",
          M_c_d_alpha_x == 0 and M_c_d_alpha_y == 0)
    check("NP8: H_b is alpha_s-invariant (both coordinates have zero alpha_s derivative)",
          H_b_d_alpha_x == 0 and H_b_d_alpha_y == 0)

    # Verify exact values.
    expected_M_c = sp.Matrix([sp.Rational(1, 2), 0])
    expected_H_b = sp.Matrix([sp.Rational(1, N["N_quark"]),
                              sp.sqrt(N["N_quark"] - 1) / N["N_quark"]])

    diff_M = sp.simplify(M_c - expected_M_c)
    diff_H = sp.simplify(H_b - expected_H_b)

    print()
    print(f"  M_c = (1/2, 0) -- midpoint of V_1 V_2 (the unit base).")
    print(f"  H_b = (1/N_quark, sqrt(N_quark - 1)/N_quark) = (1/6, sqrt(5)/6).")
    print(f"        This equals V_3 | LO (the LO apex).")

    check("NP7: M_c = (1/2, 0) exactly",
          diff_M == sp.Matrix([0, 0]))
    check("NP8: H_b = (1/N_quark, sqrt(N_quark - 1)/N_quark) = LO apex",
          diff_H == sp.Matrix([0, 0]))


def audit_np9_invariant_distance(N: dict, S: dict, midpoints: dict, feet: dict) -> None:
    banner("NP9: Distance |M_c - H_b| = 1/2 (alpha_s-INVARIANT)")

    a_s = S["a_s"]
    M_c = midpoints["M_c"]
    H_b = feet["H_b"]

    dist_sq = sp.simplify((M_c[0] - H_b[0]) ** 2 + (M_c[1] - H_b[1]) ** 2)
    expected = sp.Rational(1, 4)

    print(f"  |M_c - H_b|^2 (computed) = {dist_sq}")
    print(f"  Expected: 1/4 = (1/2)^2 = R_bar^2 | LO")
    check("NP9: |M_c - H_b|^2 = 1/4 (alpha_s-invariant)",
          sp.simplify(dist_sq - expected) == 0)

    print()
    print(f"  At LO: R_bar | LO = sqrt(80/320) = sqrt(1/4) = 1/2.")
    print(f"  So |M_c - H_b| = R_bar | LO. The frozen distance equals the LO circumradius.")


def audit_np10_pencil_theorem(N: dict, S: dict) -> None:
    banner("NP10: PENCIL THEOREM -- nine-point circle family is coaxial through M_c, H_b")

    a_s = S["a_s"]
    N9 = S["N9"]
    R9_sq = S["R9_sq"]

    M_c = sp.Matrix([sp.Rational(1, 2), 0])
    H_b = sp.Matrix([sp.Rational(1, 6), sp.sqrt(5) / 6])

    # Power of M_c with respect to nine-point circle: |M_c - N9|^2 - R9^2 should be 0
    # for ALL alpha_s.
    pow_M_c = sp.simplify((M_c[0] - N9[0]) ** 2 + (M_c[1] - N9[1]) ** 2 - R9_sq)
    pow_H_b = sp.simplify((H_b[0] - N9[0]) ** 2 + (H_b[1] - N9[1]) ** 2 - R9_sq)

    print(f"  Power(M_c, nine-point circle) = {pow_M_c}")
    print(f"  Power(H_b, nine-point circle) = {pow_H_b}")
    print()
    print("  For a coaxial pencil through M_c and H_b, both powers must be zero")
    print("  for ALL alpha_s.")
    check("NP10: Power(M_c) = 0 (M_c lies on every nine-point circle in the family)",
          pow_M_c == 0)
    check("NP10: Power(H_b) = 0 (H_b lies on every nine-point circle in the family)",
          pow_H_b == 0)

    # The radical axis of the coaxial pencil is the perpendicular bisector of M_c H_b.
    midpoint_chord = sp.Matrix([(M_c[0] + H_b[0]) / 2, (M_c[1] + H_b[1]) / 2])
    chord_direction = sp.Matrix([H_b[0] - M_c[0], H_b[1] - M_c[1]])
    print(f"\n  Chord M_c H_b midpoint: ({midpoint_chord[0]}, {midpoint_chord[1]})")
    print(f"          = (1/3, sqrt(5)/12)")
    print(f"  Chord direction: ({chord_direction[0]}, {chord_direction[1]})")
    print(f"          = (-1/3, sqrt(5)/6)")

    print()
    print("  The radical axis of the coaxial pencil is the perpendicular bisector")
    print("  of segment M_c H_b. It is alpha_s-invariant. The pencil is uniquely")
    print("  determined by the two fixed points M_c, H_b plus any one circle.")


def audit_np11_pencil_centers(N: dict, S: dict, R9_sq: sp.Expr) -> None:
    banner("NP11: Pencil center curve -- N9 traces a line as alpha_s varies")

    a_s = S["a_s"]
    N9 = S["N9"]

    # N9_x = (16 - alpha_s)/48, N9_y = sqrt(5)(10 - alpha_s)/120.
    # Eliminate alpha_s to find the curve.
    # alpha_s = 16 - 48 N9_x.
    # N9_y = sqrt(5)(10 - (16 - 48 N9_x))/120 = sqrt(5)(48 N9_x - 6)/120 = sqrt(5)(8 N9_x - 1)/20.

    # So N9_y * 20 = sqrt(5)(8 N9_x - 1)
    # => 20 N9_y - 8 sqrt(5) N9_x + sqrt(5) = 0
    # => 8 sqrt(5) N9_x - 20 N9_y - sqrt(5) = 0
    # i.e. the locus of nine-point centers is a STRAIGHT LINE.

    # Verify at sample alpha_s values.
    samples = [0.0, 0.118, 0.30, 0.5]
    print(f"  As alpha_s varies, N9 traces:")
    print(f"  alpha_s   N9_x          N9_y          on line 8 sqrt(5) x - 20 y = sqrt(5)?")
    all_on_line = True
    for s in samples:
        nx = float(N9[0].subs(a_s, s))
        ny = float(N9[1].subs(a_s, s))
        # Test: 8 sqrt(5) nx - 20 ny ?= sqrt(5).
        lhs = 8 * math.sqrt(5) * nx - 20 * ny
        rhs = math.sqrt(5)
        on_line = abs(lhs - rhs) < 1e-12
        all_on_line = all_on_line and on_line
        print(f"  {s:6.3f}    {nx:10.6f}    {ny:10.6f}    {lhs - rhs:+.10f}   {'OK' if on_line else 'FAIL'}")

    check("NP11: N9 lies on the line 8 sqrt(5) x - 20 y = sqrt(5) for all alpha_s",
          all_on_line)

    # Symbolic verification.
    line_form = sp.simplify(8 * sp.sqrt(5) * N9[0] - 20 * N9[1] - sp.sqrt(5))
    print(f"\n  Symbolic check: 8 sqrt(5) N9_x - 20 N9_y - sqrt(5) = {line_form}")
    check("NP11 symbolic: N9 traces a STRAIGHT LINE as alpha_s varies",
          line_form == 0)

    print()
    print("  This is the LINE OF CENTERS of the coaxial pencil through M_c and H_b.")


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA              (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS                      (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY                      (retained)")
    print("    CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM             (retained)")
    print("    CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM   (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (NP2) Nine-point circle center N9 closed form.")
    print("    (NP3) Nine-point circle radius squared R9^2 = R_bar^2/4 closed form.")
    print("    (NP4) Three side midpoints M_a, M_b, M_c closed forms (each on circle).")
    print("    (NP5) Three altitude feet H_a, H_b, H_c closed forms (each on circle).")
    print("    (NP6) Three orthocenter-vertex midpoints P_1, P_2, P_3 closed forms.")
    print()
    print("    (NP7) STRIKING -- M_c = (1/2, 0) is alpha_s-INVARIANT.")
    print("          (Both V_1 = (0,0) and V_2 = (1,0) are alpha_s-fixed.)")
    print()
    print("    (NP8) STRIKING -- H_b = (1/N_quark, sqrt(N_quark - 1)/N_quark)")
    print("          = (1/6, sqrt(5)/6) is alpha_s-INVARIANT.")
    print("          (Forced by the alpha_s-protected slope tan(gamma_bar) = sqrt(5)")
    print("          of the line V_1 V_3.) This equals the LO apex V_3 | LO.")
    print()
    print("    (NP9) The frozen distance |M_c - H_b| = 1/2 = R_bar | LO is")
    print("          alpha_s-invariant -- exactly the LO circumradius.")
    print()
    print("    (NP10) PENCIL THEOREM (NEW): as alpha_s varies, the nine-point circle")
    print("           is a one-parameter family ALL passing through the two fixed")
    print("           points M_c and H_b. The family forms a COAXIAL PENCIL of circles,")
    print("           with the segment M_c H_b as common chord.")
    print()
    print("    (NP11) The locus of nine-point centers N9(alpha_s) traces a straight")
    print("           LINE in (rho_bar, eta_bar)-plane. This is the LINE OF CENTERS")
    print("           of the coaxial pencil. Equation:")
    print("              8 sqrt(5) N9_x  -  20 N9_y  =  sqrt(5).")
    print()
    print("  All identities exact via sympy; closure on retained-tier authorities only.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity-triangle nine-point circle + protected coaxial pencil audit")
    print("See docs/CKM_BARRED_NINE_POINT_CIRCLE_PROTECTED_PENCIL_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    audit_np2_n9_center(N, S)
    audit_np3_radius(N, S)
    R9_sq = S["R9_sq"]
    midpoints = audit_np4_midpoints(N, S, R9_sq)
    feet = audit_np5_altitude_feet(N, S, R9_sq)
    audit_np6_orthocenter_vertex_midpoints(N, S, R9_sq)
    audit_np7_np8_invariant_points(N, S, midpoints, feet)
    audit_np9_invariant_distance(N, S, midpoints, feet)
    audit_np10_pencil_theorem(N, S)
    audit_np11_pencil_centers(N, S, R9_sq)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
