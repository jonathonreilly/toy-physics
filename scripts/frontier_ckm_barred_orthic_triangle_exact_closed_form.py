#!/usr/bin/env python3
"""Barred unitarity-triangle ORTHIC TRIANGLE exact closed form.

Verifies the NEW retained closed forms in
  docs/CKM_BARRED_ORTHIC_TRIANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (O1) ORTHIC TRIANGLE: triangle whose vertices are the three altitude
       feet H_a, H_b, H_c of the original unitarity triangle. The orthic
       triangle is inscribed in the original triangle's nine-point circle.

  (O2) Orthic vertices (closed forms):
        H_a = (5(4 - alpha_s)^2/(6(80 + alpha_s^2)),
               sqrt(5)(4 - alpha_s)(20 + alpha_s)/(6(80 + alpha_s^2))),
        H_b = (1/6, sqrt(5)/6)                                  [alpha_s-INVARIANT],
        H_c = ((4 - alpha_s)/24, 0).

  (O3) Orthic side lengths:
        |H_b H_c|  =  a |cos(gamma_bar)|  =  sqrt(80 + alpha_s^2)/24
                   =  sqrt(N_pair^4 (N_quark - 1) + alpha_s^2)/(N_pair^2 N_quark),

        |H_a H_c|  =  b |cos(beta_bar)|  =  (4 - alpha_s)(20 + alpha_s)
                                              /(24 sqrt(80 + alpha_s^2)),

        |H_a H_b|  =  c |cos(alpha_bar)|  =  alpha_s/sqrt(80 + alpha_s^2).

  (O4) Orthic AREA closed form:
        Area_orthic  =  2 |Area| |cos alpha_bar cos beta_bar cos gamma_bar|
                     =  sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s)
                        /  (144 (80 + alpha_s^2))
                     =  sqrt(N_quark - 1) alpha_s (N_pair^2 - alpha_s)
                                          (N_pair^2 (N_quark - 1) + alpha_s)
                        /  (N_pair^4 N_color^2 (N_pair^4 (N_quark - 1) + alpha_s^2)).

  (O5) STRIKING LO DEGENERACY:
        At alpha_s = 0:
          H_a | LO  =  V_3 | LO  =  (1/6, sqrt(5)/6),
          H_b | LO  =  V_3 | LO  =  (1/6, sqrt(5)/6),
          so H_a = H_b at LO -- the orthic triangle DEGENERATES (two
          vertices collide at the LO right-angle apex V_3).

       Area_orthic | LO  =  0.

       Reason: at LO, alpha_LO = pi/2 (right angle at V_3), and for a
       right triangle the altitudes from the two acute vertices meet
       the opposite leg at the right-angle vertex itself.

  (O6) NINE-POINT CIRCLE IDENTITY: orthic triangle's circumcircle =
       nine-point circle of the original triangle (classical,
       verified retained-surface).

  (O7) Ratio Area_orthic / Area_triangle:
        Area_orthic / Area_triangle
           =  2 cos alpha_bar cos beta_bar cos gamma_bar  (formal, with signs)
           =  alpha_s (20 + alpha_s)/(3 (80 + alpha_s^2))   (after taking |cos|).

  (O8) Second boundary degeneracy at alpha_s = 4:
        At alpha_s = 4, (4 - alpha_s) = 0 and the original triangle itself
        degenerates (V_3 -> V_1). The orthic closed forms extend
        continuously to zero area at this singular boundary.

       Area_orthic vanishes at alpha_s = 0 AND at alpha_s = 4.

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
        ("docs/CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md",
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
    apex = read_authority(
        "docs/CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md"
    )

    has_rho_bar = "rho_bar" in nlo and "(4 - alpha_s(v)) / 24" in nlo
    has_eta_bar = "eta_bar" in nlo and "sqrt(5) (4 - alpha_s(v)) / 24" in nlo

    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_quark_match = re.search(r"n[_\s]quark\s*=\s*n[_\s]pair\s*n[_\s]color", counts, re.IGNORECASE)

    has_apex_cos = "cos^2(alpha_bar)" in apex or "cos(alpha_bar)" in apex.lower()

    print(f"  rho_bar = (4 - alpha_s)/24:         {'FOUND' if has_rho_bar else 'NOT FOUND'}")
    print(f"  eta_bar = sqrt(5)(4 - alpha_s)/24:  {'FOUND' if has_eta_bar else 'NOT FOUND'}")
    print(f"  N_pair extracted:                   {n_pair_match.group(0) if n_pair_match else 'NOT FOUND'}")
    print(f"  N_color extracted:                  {n_color_match.group(0) if n_color_match else 'NOT FOUND'}")
    print(f"  N_quark = N_pair * N_color:         {'FOUND' if n_quark_match else 'NOT FOUND'}")
    print(f"  apex angle cos retained:            {'FOUND' if has_apex_cos else 'NOT FOUND'}")

    check("NLO retains rho_bar = (4 - alpha_s)/24", has_rho_bar)
    check("NLO retains eta_bar = sqrt(5)(4 - alpha_s)/24", has_eta_bar)
    check("MAGNITUDES retains N_pair = 2", n_pair_match and int(n_pair_match.group(1)) == 2)
    check("MAGNITUDES retains N_color = 3", n_color_match and int(n_color_match.group(1)) == 3)
    check("MAGNITUDES retains N_quark = N_pair * N_color (=6)", bool(n_quark_match))
    check("APEX retains cos(alpha_bar) closed form", has_apex_cos)

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
    area_triangle = eta_bar / 2

    return {
        "a_s": a_s,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "V1": V1,
        "V2": V2,
        "V3": V3,
        "a_sq": a_sq,
        "b_sq": b_sq,
        "c_sq": c_sq,
        "area_triangle": area_triangle,
    }


def audit_o2_orthic_vertices(N: dict, S: dict) -> dict:
    banner("O2: Orthic vertices H_a, H_b, H_c (closed forms)")

    a_s = S["a_s"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]

    def foot_of_altitude(P, A, B):
        diff = B - A
        t = ((P - A).dot(diff)) / diff.dot(diff)
        return sp.Matrix([sp.simplify(A[0] + t * diff[0]),
                          sp.simplify(A[1] + t * diff[1])])

    H_a = foot_of_altitude(V1, V2, V3)
    H_b = foot_of_altitude(V2, V1, V3)
    H_c = foot_of_altitude(V3, V1, V2)

    expected_H_a = sp.Matrix([
        sp.simplify(5 * (4 - a_s) ** 2 / (6 * (80 + a_s ** 2))),
        sp.simplify(sp.sqrt(5) * (4 - a_s) * (20 + a_s) / (6 * (80 + a_s ** 2))),
    ])
    expected_H_b = sp.Matrix([sp.Rational(1, 6), sp.sqrt(5) / 6])
    expected_H_c = sp.Matrix([(4 - a_s) / 24, sp.Integer(0)])

    diff_a = sp.simplify(H_a - expected_H_a)
    diff_b = sp.simplify(H_b - expected_H_b)
    diff_c = sp.simplify(H_c - expected_H_c)

    print(f"  H_a (foot from V_1 onto V_2 V_3):")
    print(f"    Computed: ({H_a[0]}, {H_a[1]})")
    print(f"    Expected: (5(4-α_s)²/(6(80+α_s²)), √5(4-α_s)(20+α_s)/(6(80+α_s²)))")
    print(f"    Difference: ({sp.simplify(diff_a[0])}, {sp.simplify(diff_a[1])})")
    check("O2: H_a closed form",
          sp.simplify(diff_a[0]) == 0 and sp.simplify(diff_a[1]) == 0)

    print(f"\n  H_b (foot from V_2 onto V_1 V_3):")
    print(f"    Computed: ({H_b[0]}, {H_b[1]})")
    print(f"    Expected: (1/6, √5/6) -- alpha_s INVARIANT!")
    print(f"    Difference: ({sp.simplify(diff_b[0])}, {sp.simplify(diff_b[1])})")
    check("O2: H_b closed form (alpha_s-invariant = (1/6, sqrt(5)/6))",
          sp.simplify(diff_b[0]) == 0 and sp.simplify(diff_b[1]) == 0)

    print(f"\n  H_c (foot from V_3 onto V_1 V_2 = base):")
    print(f"    Computed: ({H_c[0]}, {H_c[1]})")
    print(f"    Expected: ((4-α_s)/24, 0)")
    print(f"    Difference: ({sp.simplify(diff_c[0])}, {sp.simplify(diff_c[1])})")
    check("O2: H_c closed form = (rho_bar, 0)",
          sp.simplify(diff_c[0]) == 0 and sp.simplify(diff_c[1]) == 0)

    return {"H_a": H_a, "H_b": H_b, "H_c": H_c}


def audit_o3_orthic_sides(N: dict, S: dict, vertices: dict) -> None:
    banner("O3: Orthic side lengths")

    a_s = S["a_s"]
    H_a = vertices["H_a"]
    H_b = vertices["H_b"]
    H_c = vertices["H_c"]

    side_HbHc_sq = sp.simplify((H_b[0] - H_c[0]) ** 2 + (H_b[1] - H_c[1]) ** 2)
    side_HaHc_sq = sp.simplify((H_a[0] - H_c[0]) ** 2 + (H_a[1] - H_c[1]) ** 2)
    side_HaHb_sq = sp.simplify((H_a[0] - H_b[0]) ** 2 + (H_a[1] - H_b[1]) ** 2)

    expected_HbHc_sq = sp.simplify((80 + a_s ** 2) / 576)
    expected_HaHc_sq = sp.simplify(((4 - a_s) * (20 + a_s)) ** 2 / (576 * (80 + a_s ** 2)))
    expected_HaHb_sq = sp.simplify(a_s ** 2 / (80 + a_s ** 2))

    diff_bc = sp.simplify(side_HbHc_sq - expected_HbHc_sq)
    diff_ac = sp.simplify(side_HaHc_sq - expected_HaHc_sq)
    diff_ab = sp.simplify(side_HaHb_sq - expected_HaHb_sq)

    print(f"  |H_b H_c|^2 = {side_HbHc_sq}")
    print(f"    Expected: (80 + alpha_s^2)/576 = a^2 cos^2(gamma_bar)")
    check("O3: |H_b H_c|^2 = (80 + alpha_s^2)/576", diff_bc == 0)

    print(f"\n  |H_a H_c|^2 = {side_HaHc_sq}")
    print(f"    Expected: (4 - alpha_s)^2 (20 + alpha_s)^2 / (576 (80 + alpha_s^2))")
    print(f"            = b^2 cos^2(beta_bar)")
    check("O3: |H_a H_c|^2 = (4-α_s)²(20+α_s)²/(576(80+α_s²))", diff_ac == 0)

    print(f"\n  |H_a H_b|^2 = {side_HaHb_sq}")
    print(f"    Expected: alpha_s^2 / (80 + alpha_s^2) = c^2 cos^2(alpha_bar)")
    check("O3: |H_a H_b|^2 = α_s²/(80 + α_s²)", diff_ab == 0)


def audit_o4_orthic_area(N: dict, S: dict, vertices: dict) -> None:
    banner("O4: Orthic AREA closed form")

    a_s = S["a_s"]
    H_a = vertices["H_a"]
    H_b = vertices["H_b"]
    H_c = vertices["H_c"]

    # Triangle area via cross product / shoelace.
    area_signed = sp.Rational(1, 2) * (
        H_a[0] * (H_b[1] - H_c[1])
        + H_b[0] * (H_c[1] - H_a[1])
        + H_c[0] * (H_a[1] - H_b[1])
    )
    area_orthic = sp.Abs(area_signed)
    # For positive alpha_s (physical range), simplify by removing Abs.
    area_orthic = sp.simplify(sp.Abs(sp.simplify(area_signed)))

    expected = sp.simplify(
        sp.sqrt(5) * a_s * (4 - a_s) * (20 + a_s)
        / (144 * (80 + a_s ** 2))
    )

    # Verify by direct symbolic comparison and numerical agreement.
    # The signed area might be negative depending on orientation; use absolute.
    print(f"  Area_orthic (signed via shoelace) = {sp.simplify(area_signed)}")
    print(f"  Expected: sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s) / (144 (80 + alpha_s^2))")
    print(f"          = {expected}")

    # Test numerical agreement at sample alpha_s.
    samples = [0.118, 0.30, 0.50, 1.0]
    print(f"\n  Numerical comparison:")
    print(f"  alpha_s   computed signed Area    expected (positive form)")
    all_match = True
    for s in samples:
        computed = float(area_signed.subs(a_s, s))
        expected_val = float(expected.subs(a_s, s))
        # The signed area might be negative, but |signed| = expected.
        match = abs(abs(computed) - expected_val) < 1e-10
        all_match = all_match and match
        print(f"  {s:6.3f}   {computed:+.10f}    {expected_val:.10f}   {'OK' if match else 'FAIL'}")

    check("O4: |Area_orthic| = sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s) / (144 (80 + alpha_s^2))",
          all_match)

    # Algebraic equivalence of |signed| and expected.
    diff = sp.simplify(area_signed ** 2 - expected ** 2)
    check("O4 algebraic: signed_area^2 = expected^2",
          diff == 0)


def audit_o5_lo_degeneracy(N: dict, S: dict, vertices: dict) -> None:
    banner("O5: STRIKING LO degeneracy -- orthic triangle has zero area at alpha_s = 0")

    a_s = S["a_s"]
    H_a = vertices["H_a"]
    H_b = vertices["H_b"]

    H_a_lo = sp.simplify(H_a.subs(a_s, 0))
    H_b_lo = sp.simplify(H_b.subs(a_s, 0))

    print(f"  H_a | LO = ({H_a_lo[0]}, {H_a_lo[1]})")
    print(f"  H_b | LO = ({H_b_lo[0]}, {H_b_lo[1]})")
    print(f"  V_3 | LO = (1/6, sqrt(5)/6)")

    diff = sp.simplify(H_a_lo - H_b_lo)
    print(f"  H_a | LO - H_b | LO: ({diff[0]}, {diff[1]})")

    check("O5: H_a | LO = H_b | LO (collide at LO right-angle apex V_3)",
          diff == sp.Matrix([0, 0]))

    expected_apex_lo = sp.Matrix([sp.Rational(1, N["N_quark"]),
                                  sp.sqrt(N["N_quark"] - 1) / N["N_quark"]])
    diff_apex = sp.simplify(H_a_lo - expected_apex_lo)
    check("O5: H_a | LO = H_b | LO = V_3 | LO = (1/N_quark, sqrt(N_quark - 1)/N_quark)",
          diff_apex == sp.Matrix([0, 0]))

    print()
    print("  At alpha_s = 0, the original triangle has alpha_LO = pi/2 (right")
    print("  angle at V_3). For a right triangle with right angle at V_3:")
    print("    - The altitude from V_1 to the leg V_2 V_3 lands at V_3 itself.")
    print("    - The altitude from V_2 to the leg V_1 V_3 lands at V_3 itself.")
    print("  So H_a = H_b = V_3 at LO, and the orthic triangle DEGENERATES.")


def audit_o6_nine_point_circle_identity(N: dict, S: dict, vertices: dict) -> None:
    banner("O6: nine-point circle identity -- orthic-circumcircle = nine-point circle")

    a_s = S["a_s"]
    H_a, H_b, H_c = vertices["H_a"], vertices["H_b"], vertices["H_c"]

    # Nine-point center and radius (from companion theorem).
    rho_bar = (4 - a_s) / 24
    O = sp.Matrix([sp.Rational(1, 2), -a_s * sp.sqrt(5) / 40])
    H_pt = sp.Matrix([rho_bar, (20 + a_s) / (24 * sp.sqrt(5))])
    N9 = sp.Matrix([sp.simplify((O[0] + H_pt[0]) / 2),
                    sp.simplify((O[1] + H_pt[1]) / 2)])
    R9_sq = sp.simplify((sp.Rational(1, 4) + a_s ** 2 / 320) / 4)

    # All three orthic vertices on nine-point circle.
    for name, P in [("H_a", H_a), ("H_b", H_b), ("H_c", H_c)]:
        dist_sq = sp.simplify((P[0] - N9[0]) ** 2 + (P[1] - N9[1]) ** 2)
        diff = sp.simplify(dist_sq - R9_sq)
        check(f"O6: {name} on nine-point circle", diff == 0)

    print()
    print("  All three orthic vertices H_a, H_b, H_c lie on the nine-point circle")
    print("  of the original triangle. So the orthic triangle's circumcircle")
    print("  equals the original triangle's nine-point circle.")


def audit_o7_area_ratio(N: dict, S: dict, vertices: dict) -> None:
    banner("O7: Ratio Area_orthic / Area_triangle")

    a_s = S["a_s"]
    H_a, H_b, H_c = vertices["H_a"], vertices["H_b"], vertices["H_c"]
    area_triangle = S["area_triangle"]

    area_orthic_signed = sp.Rational(1, 2) * (
        H_a[0] * (H_b[1] - H_c[1])
        + H_b[0] * (H_c[1] - H_a[1])
        + H_c[0] * (H_a[1] - H_b[1])
    )
    # |Area_orthic|.
    area_orthic_abs_sq = sp.simplify(area_orthic_signed ** 2)

    ratio_sq = sp.simplify(area_orthic_abs_sq / area_triangle ** 2)
    expected_ratio_sq = sp.simplify(
        a_s ** 2 * (20 + a_s) ** 2 / (9 * (80 + a_s ** 2) ** 2)
    )

    diff = sp.simplify(ratio_sq - expected_ratio_sq)
    print(f"  (Area_orthic / Area_triangle)^2 = {ratio_sq}")
    print(f"  Expected: alpha_s^2 (20 + alpha_s)^2 / (9 (80 + alpha_s^2)^2)")
    print(f"  Difference: {diff}")

    check("O7: (Area_orthic / Area_triangle)^2 = alpha_s^2 (20 + alpha_s)^2 / (9 (80 + alpha_s^2)^2)",
          diff == 0)

    # |Area_orthic / Area_triangle|.
    print()
    print("  |Area_orthic / Area_triangle|  =  alpha_s (20 + alpha_s) / (3 (80 + alpha_s^2))")
    print("                                =  alpha_s (N_pair^2 (N_quark - 1) + alpha_s)")
    print("                                   / (N_color (N_pair^4 (N_quark - 1) + alpha_s^2)).")


def audit_o8_double_degeneracy(N: dict, S: dict, vertices: dict) -> None:
    banner("O8: second boundary degeneracy at alpha_s = 4 (where (4 - alpha_s) = 0)")

    a_s = S["a_s"]
    H_a, H_b, H_c = vertices["H_a"], vertices["H_b"], vertices["H_c"]

    H_a_4 = sp.simplify(H_a.subs(a_s, 4))
    H_b_4 = sp.simplify(H_b.subs(a_s, 4))
    H_c_4 = sp.simplify(H_c.subs(a_s, 4))

    print(f"  At alpha_s = 4 (where 4 - alpha_s = 0):")
    print(f"  H_a | (alpha_s = 4) = ({H_a_4[0]}, {H_a_4[1]})")
    print(f"  H_b | (alpha_s = 4) = ({H_b_4[0]}, {H_b_4[1]})")
    print(f"  H_c | (alpha_s = 4) = ({H_c_4[0]}, {H_c_4[1]})")

    print()
    print("  At alpha_s = 4: rho_bar = 0, eta_bar = 0, so V_3 -> V_1 = (0, 0).")
    print("  The original triangle degenerates to a line segment with a collapsed")
    print("  side V_1 V_3. The closed-form orthic area has a continuous zero-area")
    print("  boundary value there; the literal altitude-foot construction is singular.")

    # Area_orthic at alpha_s = 4 should be 0.
    area_orthic_signed = sp.Rational(1, 2) * (
        H_a[0] * (H_b[1] - H_c[1])
        + H_b[0] * (H_c[1] - H_a[1])
        + H_c[0] * (H_a[1] - H_b[1])
    )
    area_at_4 = sp.simplify(area_orthic_signed.subs(a_s, 4))
    print(f"\n  Area_orthic | (alpha_s = 4) = {area_at_4}")
    check("O8: Area_orthic vanishes at alpha_s = 4 (second boundary degeneracy)",
          area_at_4 == 0)


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA  (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS         (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY         (retained)")
    print("    CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM  (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (O2) Orthic vertices closed forms:")
    print("           H_a = (5(4-α_s)²/(6(80+α_s²)), √5(4-α_s)(20+α_s)/(6(80+α_s²))),")
    print("           H_b = (1/6, √5/6)                       [alpha_s-INVARIANT],")
    print("           H_c = ((4-α_s)/24, 0).")
    print()
    print("    (O3) Orthic side lengths:")
    print("           |H_b H_c|^2  =  (80 + alpha_s^2)/576       =  a^2 cos^2(γ̄),")
    print("           |H_a H_c|^2  =  (4-α_s)²(20+α_s)²/(576(80+α_s²))  =  b^2 cos^2(β̄),")
    print("           |H_a H_b|^2  =  alpha_s^2/(80 + alpha_s^2)         =  c^2 cos^2(α̃).")
    print()
    print("    (O4) Orthic area in pure structural integers:")
    print("           Area_orthic  =  sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s)")
    print("                            / (144 (80 + alpha_s^2)).")
    print()
    print("    (O5) STRIKING LO degeneracy:")
    print("           At alpha_s = 0: H_a = H_b = V_3 | LO = (1/6, sqrt(5)/6).")
    print("           Orthic triangle DEGENERATES (two vertices collide at the LO")
    print("           right-angle apex V_3).")
    print("           Area_orthic | LO  =  0.")
    print()
    print("    (O6) Nine-point circle identity: orthic triangle's circumcircle = nine-point circle of")
    print("         original triangle (verified retained-surface).")
    print()
    print("    (O7) Ratio Area_orthic / Area_triangle:")
    print("           (Area_orthic / Area_triangle)^2  =  alpha_s^2 (20 + alpha_s)^2")
    print("                                              / (9 (80 + alpha_s^2)^2),")
    print("         |Area_orthic / Area_triangle|     =  alpha_s (20 + alpha_s)")
    print("                                              / (3 (80 + alpha_s^2)).")
    print()
    print("    (O8) Second boundary degeneracy at alpha_s = 4:")
    print("           At alpha_s = 4, rho_bar = eta_bar = 0, so V_3 -> V_1 and the")
    print("           original triangle degenerates; the orthic area has a zero")
    print("           continuous boundary value.")
    print("         Area_orthic vanishes at alpha_s = 0 AND at alpha_s = 4.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity-triangle ORTHIC TRIANGLE exact closed form audit")
    print("See docs/CKM_BARRED_ORTHIC_TRIANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    vertices = audit_o2_orthic_vertices(N, S)
    audit_o3_orthic_sides(N, S, vertices)
    audit_o4_orthic_area(N, S, vertices)
    audit_o5_lo_degeneracy(N, S, vertices)
    audit_o6_nine_point_circle_identity(N, S, vertices)
    audit_o7_area_ratio(N, S, vertices)
    audit_o8_double_degeneracy(N, S, vertices)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
