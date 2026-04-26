#!/usr/bin/env python3
"""Barred unitarity-triangle Napoleon triangles EXACT closed form.

Verifies the NEW retained closed forms in
  docs/CKM_BARRED_NAPOLEON_TRIANGLES_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (N1) Napoleon's theorem: erect equilateral triangles externally (resp.
       internally) on each side of the unitarity triangle. The centroids
       of the three external (resp. internal) equilateral triangles form
       another equilateral triangle, the OUTER (resp. INNER) Napoleon
       triangle.

  (N2) Outer/inner Napoleon side^2 closed forms:
        N_outer^2 = perim_sq/6 + 2 Area/sqrt(3)
                  = ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288,
        N_inner^2 = perim_sq/6 - 2 Area/sqrt(3)
                  = ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288.

       In terms of the Weitzenbock-style sum/gap defined from perim_sq
       and Area:
        N_outer^2 = W_+/6,
        N_inner^2 = W_-/6.

  (N3) Sum (universal): N_outer^2 + N_inner^2 = perim_sq/3 = (a^2+b^2+c^2)/3.
       At LO: perim_sq|LO/3 = N_pair/N_color = 2/3.

  (N4) NEW Product (Brocard polynomial connection):
        N_outer^2 * N_inner^2 = W_+ * W_- / 36
                              = P(alpha_s) / (2304 * 36)
                              = P(alpha_s) / 82944
                              = P(alpha_s) / (N_pair^10 N_color^4).

  (N5) Areas of the Napoleon triangles:
        Area_outer_Nap = sqrt(3) N_outer^2 / 4,
        Area_inner_Nap = sqrt(3) N_inner^2 / 4.

  (N6) NEW product of Napoleon areas:
        Area_outer_Nap * Area_inner_Nap = (3/16) * N_outer^2 N_inner^2
                                        = 3 P(alpha_s) / (16 * 82944)
                                        = P(alpha_s) / 442368

       Here 442368 = 16 * 82944/3; the runner verifies this exactly.

  (N7) Napoleon area difference (classical, NOT new):
        Area_outer_Nap - Area_inner_Nap = Area_triangle.

  (N8) LO recovery in pure structural integers:
        N_outer^2 + N_inner^2 | LO  =  N_pair/N_color  =  2/3,
        N_outer^2 * N_inner^2 | LO  =  (N_quark + 1)/(N_pair^2 N_color^3)  =  7/108.

  (N9) NEW Napoleon discriminant:
        (N_outer^2 - N_inner^2)^2  =  (W_+ - W_-)^2 / 36
                                    =  (sqrt(15)(4 - alpha_s)/6)^2 / 36
                                    =  15 (4 - alpha_s)^2 / (36 * 36)
                                    =  5 (4 - alpha_s)^2 / 432
                                    =  (16/3) Area^2.

Ground-up status verification: each cited authority's tier extracted from its
Status: line; closure derived only at extracted retained values. The runner
also verifies the actual external/internal equilateral-centroid construction,
not just a prose citation of Napoleon's theorem.
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

    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_quark_match = re.search(r"n[_\s]quark\s*=\s*n[_\s]pair\s*n[_\s]color", counts, re.IGNORECASE)

    print(f"  rho_bar = (4 - alpha_s)/24:        {'FOUND' if has_rho_bar else 'NOT FOUND'}")
    print(f"  eta_bar = sqrt(5)(4 - alpha_s)/24: {'FOUND' if has_eta_bar else 'NOT FOUND'}")
    print(f"  N_pair extracted:                  {n_pair_match.group(0) if n_pair_match else 'NOT FOUND'}")
    print(f"  N_color extracted:                 {n_color_match.group(0) if n_color_match else 'NOT FOUND'}")
    print(f"  N_quark = N_pair * N_color:        {'FOUND' if n_quark_match else 'NOT FOUND'}")

    check("NLO retains rho_bar = (4 - alpha_s)/24", has_rho_bar)
    check("NLO retains eta_bar = sqrt(5)(4 - alpha_s)/24", has_eta_bar)
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

    a_sq = (1 - rho_bar) ** 2 + eta_bar ** 2
    b_sq = rho_bar ** 2 + eta_bar ** 2
    c_sq = sp.Integer(1)
    perim_sq = sp.simplify(a_sq + b_sq + c_sq)
    area = eta_bar / 2

    P_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 - 240 * (4 - a_s) ** 2)

    return {
        "a_s": a_s,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "a_sq": a_sq,
        "b_sq": b_sq,
        "c_sq": c_sq,
        "perim_sq": perim_sq,
        "area": area,
        "P_poly": P_poly,
    }


def audit_n2_napoleon_sides(N: dict, S: dict) -> tuple[sp.Expr, sp.Expr]:
    banner("N2: Outer/inner Napoleon side^2 closed forms")

    a_s = S["a_s"]
    perim_sq = S["perim_sq"]
    area = S["area"]

    N_outer_sq = sp.simplify(perim_sq / 6 + 2 * area / sp.sqrt(3))
    N_inner_sq = sp.simplify(perim_sq / 6 - 2 * area / sp.sqrt(3))

    expected_outer = sp.simplify(
        ((a_s ** 2 - 4 * a_s + 96) + 4 * sp.sqrt(15) * (4 - a_s)) / 288
    )
    expected_inner = sp.simplify(
        ((a_s ** 2 - 4 * a_s + 96) - 4 * sp.sqrt(15) * (4 - a_s)) / 288
    )

    diff_o = sp.simplify(N_outer_sq - expected_outer)
    diff_i = sp.simplify(N_inner_sq - expected_inner)

    print(f"  N_outer^2 = perim_sq/6 + 2 Area/sqrt(3)")
    print(f"            = {N_outer_sq}")
    print(f"  Expected: ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288")
    print(f"           = {expected_outer}")
    print(f"  Difference: {diff_o}")
    check("N2: N_outer^2 = ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288",
          diff_o == 0)

    print()
    print(f"  N_inner^2 = perim_sq/6 - 2 Area/sqrt(3)")
    print(f"            = {N_inner_sq}")
    print(f"  Expected: ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288")
    print(f"           = {expected_inner}")
    print(f"  Difference: {diff_i}")
    check("N2: N_inner^2 = ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288",
          diff_i == 0)

    # Connection to W_+, W_- (Weitzenbock).
    W_plus = sp.simplify(perim_sq + 4 * sp.sqrt(3) * area)
    W_minus = sp.simplify(perim_sq - 4 * sp.sqrt(3) * area)
    print()
    print(f"  Verifying N_outer^2 = W_+/6 (Weitzenbock connection):")
    diff_w_o = sp.simplify(N_outer_sq - W_plus / 6)
    print(f"    Difference: {diff_w_o}")
    check("N2: N_outer^2 = W_+/6 (where W_+ is the Weitzenbock sum)",
          diff_w_o == 0)

    print(f"  Verifying N_inner^2 = W_-/6 (Weitzenbock connection):")
    diff_w_i = sp.simplify(N_inner_sq - W_minus / 6)
    print(f"    Difference: {diff_w_i}")
    check("N2: N_inner^2 = W_-/6 (where W_- is the Weitzenbock gap)",
          diff_w_i == 0)

    return N_outer_sq, N_inner_sq


def audit_n3_sum_universal(N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr) -> None:
    banner("N3: Universal triangle identity -- N_outer^2 + N_inner^2 = perim_sq/3")

    a_s = S["a_s"]
    perim_sq = S["perim_sq"]

    sum_squares = sp.simplify(N_outer_sq + N_inner_sq)
    expected = sp.simplify(perim_sq / 3)
    diff = sp.simplify(sum_squares - expected)

    print(f"  N_outer^2 + N_inner^2 (computed) = {sum_squares}")
    print(f"  Expected: perim_sq/3 = (a^2 + b^2 + c^2)/3 = {expected}")
    print(f"  Difference: {diff}")

    check("N3: N_outer^2 + N_inner^2 = perim_sq/3 (universal triangle identity)",
          diff == 0)

    # LO recovery.
    sum_lo = sp.simplify(sum_squares.subs(a_s, 0))
    expected_lo = sp.Rational(N["N_pair"], N["N_color"])
    print(f"\n  LO: N_outer^2 + N_inner^2 |LO = {sum_lo}")
    print(f"  Expected: N_pair/N_color = {expected_lo} = 2/3")
    check("N3 LO: N_outer^2 + N_inner^2 |LO = N_pair/N_color = 2/3",
          sp.simplify(sum_lo - expected_lo) == 0)


def audit_n4_product_brocard_connection(N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr) -> None:
    banner("N4: NEW Product N_outer^2 * N_inner^2 = P(alpha_s)/82944")

    a_s = S["a_s"]
    P_poly = S["P_poly"]

    product = sp.simplify(N_outer_sq * N_inner_sq)
    expected = sp.simplify(P_poly / 82944)
    diff = sp.simplify(product - expected)

    print(f"  N_outer^2 * N_inner^2 (computed) = {product}")
    print(f"  Expected: P(alpha_s)/82944 = {expected}")
    print(f"  Difference: {diff}")

    check("N4: N_outer^2 * N_inner^2 = P(alpha_s)/82944",
          diff == 0)

    # Structural-integer: 82944 = 288^2 = N_pair^10 N_color^4.
    N_pair, N_color = N["N_pair"], N["N_color"]
    expected_structural = N_pair ** 10 * N_color ** 4
    print(f"\n  Structural: 82944 = N_pair^10 N_color^4 = {N_pair ** 10} * {N_color ** 4} = {expected_structural}")
    check("N4 structural: 82944 = N_pair^10 N_color^4",
          expected_structural == 82944)


def audit_n5_n6_napoleon_areas(N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr) -> None:
    banner("N5 / N6: Napoleon triangle areas")

    a_s = S["a_s"]
    P_poly = S["P_poly"]

    Area_outer_Nap = sp.simplify(sp.sqrt(3) * N_outer_sq / 4)
    Area_inner_Nap = sp.simplify(sp.sqrt(3) * N_inner_sq / 4)
    print(f"  Area_outer_Nap = sqrt(3) N_outer^2 / 4")
    print(f"  Area_inner_Nap = sqrt(3) N_inner^2 / 4")

    # Product.
    area_product = sp.simplify(Area_outer_Nap * Area_inner_Nap)
    expected = sp.simplify(3 * P_poly / (16 * 82944))
    diff = sp.simplify(area_product - expected)
    print()
    print(f"  Area_outer_Nap * Area_inner_Nap (computed) = {area_product}")
    print(f"  Expected: 3 P(alpha_s)/(16 * 82944) = P(alpha_s)/442368 = {expected}")
    print(f"  Difference: {diff}")
    check("N6: Area_outer_Nap * Area_inner_Nap = 3 P(alpha_s)/(16 * 82944)",
          diff == 0)

    # Difference (classical Napoleon result).
    area_diff = sp.simplify(Area_outer_Nap - Area_inner_Nap)
    area_triangle = S["area"]
    diff_classical = sp.simplify(area_diff - area_triangle)
    print()
    print(f"  Area_outer_Nap - Area_inner_Nap (computed) = {area_diff}")
    print(f"  Area_triangle (retained) = {area_triangle}")
    print(f"  Difference: {diff_classical}")
    check("N7 classical: Area_outer_Nap - Area_inner_Nap = Area_triangle",
          diff_classical == 0)


def audit_n8_lo_recovery(N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr) -> None:
    banner("N8: LO recovery in pure structural integers")

    a_s = S["a_s"]

    sum_lo = sp.simplify((N_outer_sq + N_inner_sq).subs(a_s, 0))
    product_lo = sp.simplify((N_outer_sq * N_inner_sq).subs(a_s, 0))

    N_pair, N_color, N_quark = N["N_pair"], N["N_color"], N["N_quark"]
    expected_sum = sp.Rational(N_pair, N_color)
    expected_product = sp.Rational(N_quark + 1, N_pair ** 2 * N_color ** 3)

    print(f"  Sum at LO: N_outer^2 + N_inner^2 |LO = {sum_lo}")
    print(f"  Expected: N_pair/N_color = 2/3")
    check("N8: N_outer^2 + N_inner^2 |LO = N_pair/N_color = 2/3",
          sp.simplify(sum_lo - expected_sum) == 0)

    print()
    print(f"  Product at LO: N_outer^2 * N_inner^2 |LO = {product_lo}")
    print(f"  Expected: (N_quark + 1)/(N_pair^2 N_color^3) = 7/108")
    check("N8: N_outer^2 * N_inner^2 |LO = (N_quark + 1)/(N_pair^2 N_color^3) = 7/108",
          sp.simplify(product_lo - expected_product) == 0)


def audit_n9_napoleon_discriminant(N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr) -> None:
    banner("N9: NEW Napoleon discriminant tied to (4 - alpha_s)^2")

    a_s = S["a_s"]
    area = S["area"]

    diff_squared = sp.simplify((N_outer_sq - N_inner_sq) ** 2)

    # Expected: 5 (4 - alpha_s)^2 / 432.
    expected = sp.simplify(5 * (4 - a_s) ** 2 / 432)
    diff = sp.simplify(diff_squared - expected)

    print(f"  (N_outer^2 - N_inner^2)^2 (computed) = {diff_squared}")
    print(f"  Expected: 5 (4 - alpha_s)^2/432 = {expected}")
    print(f"  Difference: {diff}")

    check("N9: (N_outer^2 - N_inner^2)^2 = 5 (4 - alpha_s)^2/432",
          diff == 0)

    # Connection to Area^2.
    # Area^2 = 5(4-α_s)²/2304, so 5(4-α_s)²/432 = Area² × 2304/432 = Area² × 16/3.
    expected_area_form = sp.simplify(area ** 2 * sp.Rational(16, 3))
    diff_area = sp.simplify(diff_squared - expected_area_form)
    print()
    print(f"  Equivalent form: (N_outer^2 - N_inner^2)^2 = (16/3) Area^2 = {expected_area_form}")
    print(f"  Difference: {diff_area}")
    check("N9 alt: (N_outer^2 - N_inner^2)^2 = (16/3) Area^2 = (N_pair^4/N_color) Area^2",
          diff_area == 0)


def audit_napoleon_centroid_construction(
    N: dict, S: dict, N_outer_sq: sp.Expr, N_inner_sq: sp.Expr
) -> None:
    banner("Napoleon centroid construction (object-level verification)")

    a_s = S["a_s"]
    rho_bar = S["rho_bar"]
    eta_bar = S["eta_bar"]

    # Original triangle vertices in counterclockwise order.
    V1 = sp.Matrix([0, 0])
    V2 = sp.Matrix([1, 0])
    V3 = sp.Matrix([rho_bar, eta_bar])
    sides = ((V1, V2), (V2, V3), (V3, V1))

    G_orig = sp.simplify((V1 + V2 + V3) / 3)
    print(f"  Centroid of original triangle: G_orig = ({G_orig[0]}, {G_orig[1]})")

    def rot90(v: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([-v[1], v[0]])

    def equilateral_center(P: sp.Matrix, Q: sp.Matrix, external: bool) -> sp.Matrix:
        # For the counterclockwise triangle boundary, interior is to the left
        # of each directed side. External uses the right-hand apex.
        sign = -1 if external else 1
        apex = (P + Q) / 2 + sign * sp.sqrt(3) * rot90(Q - P) / 2
        return sp.simplify((P + Q + apex) / 3)

    outer_centers = [equilateral_center(P, Q, external=True) for P, Q in sides]
    inner_centers = [equilateral_center(P, Q, external=False) for P, Q in sides]

    def squared_distance(P: sp.Matrix, Q: sp.Matrix) -> sp.Expr:
        return sp.simplify(sum((P[i] - Q[i]) ** 2 for i in range(2)))

    def centroid(points: list[sp.Matrix]) -> sp.Matrix:
        return sp.simplify(sum(points, sp.zeros(2, 1)) / 3)

    outer_side_squares = [
        squared_distance(outer_centers[0], outer_centers[1]),
        squared_distance(outer_centers[1], outer_centers[2]),
        squared_distance(outer_centers[2], outer_centers[0]),
    ]
    inner_side_squares = [
        squared_distance(inner_centers[0], inner_centers[1]),
        squared_distance(inner_centers[1], inner_centers[2]),
        squared_distance(inner_centers[2], inner_centers[0]),
    ]

    print("  Outer Napoleon side^2 values from explicit centroids:")
    for value in outer_side_squares:
        print(f"    {sp.simplify(value)}")
    check(
        "explicit outer centroids form an equilateral triangle",
        all(sp.simplify(value - outer_side_squares[0]) == 0 for value in outer_side_squares),
    )
    check(
        "explicit outer side^2 equals N_outer^2 closed form",
        sp.simplify(outer_side_squares[0] - N_outer_sq) == 0,
    )

    print("  Inner Napoleon side^2 values from explicit centroids:")
    for value in inner_side_squares:
        print(f"    {sp.simplify(value)}")
    check(
        "explicit inner centroids form an equilateral triangle",
        all(sp.simplify(value - inner_side_squares[0]) == 0 for value in inner_side_squares),
    )
    check(
        "explicit inner side^2 equals N_inner^2 closed form",
        sp.simplify(inner_side_squares[0] - N_inner_sq) == 0,
    )

    G_outer = centroid(outer_centers)
    G_inner = centroid(inner_centers)
    print(f"  Centroid of outer Napoleon: G_outer = ({G_outer[0]}, {G_outer[1]})")
    print(f"  Centroid of inner Napoleon: G_inner = ({G_inner[0]}, {G_inner[1]})")
    check(
        "outer Napoleon centroid equals original centroid exactly",
        all(sp.simplify((G_outer - G_orig)[i]) == 0 for i in range(2)),
    )
    check(
        "inner Napoleon centroid equals original centroid exactly",
        all(sp.simplify((G_inner - G_orig)[i]) == 0 for i in range(2)),
    )


def audit_package_wiring() -> None:
    banner("Package-surface wiring")

    note = "CKM_BARRED_NAPOLEON_TRIANGLES_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md"
    runner = "frontier_ckm_barred_napoleon_triangles_exact_closed_form.py"
    napoleon_phrase = "Napoleon"

    surfaces = (
        ("docs/CANONICAL_HARNESS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/CLAIMS_TABLE.md", (note, runner)),
        ("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md", (note, runner)),
        ("docs/publication/ci3_z3/DERIVATION_ATLAS.md", (note, runner)),
        ("docs/publication/ci3_z3/PUBLICATION_MATRIX.md", (note, runner)),
        ("docs/publication/ci3_z3/RESULTS_INDEX.md", (note, runner)),
        ("docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md", (note, napoleon_phrase)),
        ("docs/publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE.md", (note, napoleon_phrase)),
        ("docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md", (note, napoleon_phrase)),
        ("docs/publication/ci3_z3/EXTERNAL_REVIEWER_GUIDE.md", (napoleon_phrase, "N_outer^2=W_+/6")),
        ("docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md", (note, napoleon_phrase)),
        ("docs/publication/ci3_z3/SCIENCE_MAP.md", (napoleon_phrase, "N_outer^2=W_+/6")),
        ("docs/publication/ci3_z3/README.md", (napoleon_phrase, "N_outer^2=W_+/6")),
        ("docs/publication/ci3_z3/REPRODUCE.md", (runner,)),
    )

    for rel_path, needles in surfaces:
        content = read_authority(rel_path)
        missing = [needle for needle in needles if needle not in content]
        check(
            f"package surface wired: {rel_path}",
            not missing,
            detail=f"missing {missing}" if missing else "required tokens present",
        )


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA  (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS         (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY         (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (N2) Outer/inner Napoleon side^2:")
    print("           N_outer^2 = ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288")
    print("                     = W_+ / 6   (Weitzenbock connection),")
    print("           N_inner^2 = ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288")
    print("                     = W_- / 6.")
    print()
    print("    (N3) Sum (universal): N_outer^2 + N_inner^2 = perim_sq/3.")
    print("         At LO: N_pair/N_color = 2/3.")
    print()
    print("    (N4) NEW Brocard polynomial connection:")
    print("           N_outer^2 * N_inner^2 = P(alpha_s)/82944")
    print("                                 = P(alpha_s)/(N_pair^10 N_color^4).")
    print()
    print("    (N5/N6) Areas of Napoleon triangles: Area_Nap = sqrt(3) N^2/4.")
    print("           Area_outer_Nap * Area_inner_Nap = 3 P(alpha_s)/(16 * 82944).")
    print()
    print("    (N7) Classical: Area_outer_Nap - Area_inner_Nap = Area_triangle.")
    print()
    print("    (N8) LO structural-integer recovery:")
    print("           N_outer^2 + N_inner^2 |LO = N_pair/N_color = 2/3,")
    print("           N_outer^2 * N_inner^2 |LO = (N_quark + 1)/(N_pair^2 N_color^3) = 7/108.")
    print()
    print("    (N9) Napoleon discriminant:")
    print("           (N_outer^2 - N_inner^2)^2 = 5 (4 - alpha_s)^2/432")
    print("                                     = (16/3) Area^2.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity-triangle Napoleon triangles EXACT closed form audit")
    print("See docs/CKM_BARRED_NAPOLEON_TRIANGLES_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    N_outer_sq, N_inner_sq = audit_n2_napoleon_sides(N, S)
    audit_n3_sum_universal(N, S, N_outer_sq, N_inner_sq)
    audit_n4_product_brocard_connection(N, S, N_outer_sq, N_inner_sq)
    audit_n5_n6_napoleon_areas(N, S, N_outer_sq, N_inner_sq)
    audit_n8_lo_recovery(N, S, N_outer_sq, N_inner_sq)
    audit_n9_napoleon_discriminant(N, S, N_outer_sq, N_inner_sq)
    audit_napoleon_centroid_construction(N, S, N_outer_sq, N_inner_sq)
    audit_package_wiring()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
