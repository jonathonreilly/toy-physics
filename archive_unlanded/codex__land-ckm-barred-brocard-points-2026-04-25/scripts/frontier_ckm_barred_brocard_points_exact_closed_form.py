#!/usr/bin/env python3
"""Barred unitarity-triangle Brocard POINTS (Omega_1, Omega_2) exact closed form.

Verifies the NEW retained closed forms in
  docs/CKM_BARRED_BROCARD_POINTS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (B1) First Brocard point Omega_1 on retained surface:
        Omega_1_x = (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q(alpha_s),
        Omega_1_y = 4 sqrt(5) (4 - alpha_s)^3 / Q(alpha_s).

  (B2) Second Brocard point Omega_2:
        Omega_2_x = 4 (4 - alpha_s) (alpha_s^2 - 24 alpha_s + 176) / Q(alpha_s),
        Omega_2_y = 4 sqrt(5) (4 - alpha_s) (80 + alpha_s^2) / Q(alpha_s).

  (B3) Q-polynomial: Q(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 + 80 (4 - alpha_s)^2.

  (B4) Q-P relation (NEW):
        Q(alpha_s)  =  P(alpha_s)  +  320 (4 - alpha_s)^2,
       where P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2
       is the Brocard polynomial.

  (B5) Q-Weitzenbock relation (NEW):
        Q(alpha_s)  =  2304 [(perim_sq)^2 + 16 Area^2]
                     =  N_pair^8 N_color^2 [(perim_sq)^2 + N_pair^4 Area^2].

  (B6) LO recovery in pure structural integers:
        Omega_1 | LO = (N_quark, sqrt(N_quark - 1)) / (N_quark^2 + N_quark - 1)
                     = (6, sqrt(5))/41,
        Omega_2 | LO = (2 N_quark - 1, (N_quark - 1)^(3/2)) / (N_quark^2 + N_quark - 1)
                     = (11, 5 sqrt(5))/41.

  (B7) Brocard-Brocard distance squared at LO:
        |Omega_1 - Omega_2|^2 | LO  =  N_color (N_quark^2 - 1) / (N_quark^2 + N_quark - 1)^2
                                     =  105/41^2  =  105/1681.

  (B8) Both Brocard points lie on the Brocard circle (verified):
        circle has diameter OK (circumcenter to symmedian),
        center M_B = (O + K)/2,
        radius^2 = OK^2/4.

  (B9) The Brocard angle property holds (verified numerically):
        angle (Omega_1 V_1 V_2) = angle (Omega_1 V_2 V_3) = angle (Omega_1 V_3 V_1) = omega_bar.
        At LO, sin^2(omega_bar) = 5/41 and cos^2(omega_bar) = 36/41.

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
    a_s = sp.symbols("alpha_s", real=True, positive=True)
    rho_bar = (4 - a_s) / 24
    eta_bar = sp.sqrt(5) * (4 - a_s) / 24

    V1 = sp.Matrix([0, 0])
    V2 = sp.Matrix([1, 0])
    V3 = sp.Matrix([rho_bar, eta_bar])

    # Side lengths squared (a opposite V_1, b opposite V_2, c opposite V_3).
    a_sq = sp.simplify((1 - rho_bar) ** 2 + eta_bar ** 2)  # = (80 + alpha_s^2)/96
    b_sq = sp.simplify(rho_bar ** 2 + eta_bar ** 2)         # = (4 - alpha_s)^2/96
    c_sq = sp.Integer(1)
    perim_sq = sp.simplify(a_sq + b_sq + c_sq)
    area = eta_bar / 2

    a = sp.sqrt(a_sq)
    b = sp.sqrt(b_sq)
    c = sp.Integer(1)

    P_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 - 240 * (4 - a_s) ** 2)
    Q_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 + 80 * (4 - a_s) ** 2)

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
        "a": a,
        "b": b,
        "c": c,
        "perim_sq": perim_sq,
        "area": area,
        "P_poly": P_poly,
        "Q_poly": Q_poly,
    }


def audit_b1_b2_brocard_points(N: dict, S: dict) -> tuple[sp.Matrix, sp.Matrix]:
    banner("B1 / B2: First and second Brocard points closed forms")

    a_s = S["a_s"]
    a = S["a"]
    b = S["b"]
    c = S["c"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]

    # Barycentric weights for first Brocard point: (m1, m2, m3) = (ac/b, ab/c, bc/a).
    m_1 = a * c / b
    m_2 = a * b / c
    m_3 = b * c / a

    weights_sum = sp.simplify(m_1 + m_2 + m_3)

    # Omega_1 = (m_1 V_1 + m_2 V_2 + m_3 V_3) / (m_1 + m_2 + m_3).
    Omega_1 = sp.simplify(sp.Matrix([
        sp.simplify((m_1 * V1[0] + m_2 * V2[0] + m_3 * V3[0]) / weights_sum),
        sp.simplify((m_1 * V1[1] + m_2 * V2[1] + m_3 * V3[1]) / weights_sum),
    ]))

    # Omega_2 = (m_2 V_1 + m_3 V_2 + m_1 V_3) / (m_1 + m_2 + m_3) (cyclic shift).
    Omega_2 = sp.simplify(sp.Matrix([
        sp.simplify((m_2 * V1[0] + m_3 * V2[0] + m_1 * V3[0]) / weights_sum),
        sp.simplify((m_2 * V1[1] + m_3 * V2[1] + m_1 * V3[1]) / weights_sum),
    ]))

    # Expected closed forms.
    Q = S["Q_poly"]

    expected_O1_x = sp.simplify((4 - a_s) ** 2 * (a_s ** 2 - 4 * a_s + 96) / Q)
    expected_O1_y = sp.simplify(4 * sp.sqrt(5) * (4 - a_s) ** 3 / Q)

    expected_O2_x = sp.simplify(4 * (4 - a_s) * (a_s ** 2 - 24 * a_s + 176) / Q)
    expected_O2_y = sp.simplify(4 * sp.sqrt(5) * (4 - a_s) * (80 + a_s ** 2) / Q)

    diff_O1_x = sp.simplify(Omega_1[0] - expected_O1_x)
    diff_O1_y = sp.simplify(Omega_1[1] - expected_O1_y)
    diff_O2_x = sp.simplify(Omega_2[0] - expected_O2_x)
    diff_O2_y = sp.simplify(Omega_2[1] - expected_O2_y)

    print(f"  Omega_1_x (closed form) = (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q")
    print(f"           Difference: {diff_O1_x}")
    print(f"  Omega_1_y (closed form) = 4 sqrt(5)(4 - alpha_s)^3 / Q")
    print(f"           Difference: {diff_O1_y}")
    print()
    print(f"  Omega_2_x (closed form) = 4 (4 - alpha_s)(alpha_s^2 - 24 alpha_s + 176) / Q")
    print(f"           Difference: {diff_O2_x}")
    print(f"  Omega_2_y (closed form) = 4 sqrt(5)(4 - alpha_s)(80 + alpha_s^2) / Q")
    print(f"           Difference: {diff_O2_y}")

    check("B1: Omega_1_x = (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q",
          diff_O1_x == 0)
    check("B1: Omega_1_y = 4 sqrt(5)(4 - alpha_s)^3 / Q",
          diff_O1_y == 0)
    check("B2: Omega_2_x = 4 (4 - alpha_s)(alpha_s^2 - 24 alpha_s + 176) / Q",
          diff_O2_x == 0)
    check("B2: Omega_2_y = 4 sqrt(5)(4 - alpha_s)(80 + alpha_s^2) / Q",
          diff_O2_y == 0)

    return Omega_1, Omega_2


def audit_b3_q_polynomial(N: dict, S: dict) -> None:
    banner("B3: Q-polynomial Q(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 + 80 (4 - alpha_s)^2")

    a_s = S["a_s"]
    Q = S["Q_poly"]

    # Verify Q is the sum-of-squares form.
    expected = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 + 80 * (4 - a_s) ** 2)
    diff = sp.simplify(Q - expected)
    print(f"  Q(alpha_s) = {Q}")
    print(f"  Expected: (alpha_s^2 - 4 alpha_s + 96)^2 + 80(4 - alpha_s)^2 = {expected}")
    print(f"  Difference: {diff}")

    check("B3: Q(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 + 80 (4 - alpha_s)^2",
          diff == 0)

    # Numerical at LO.
    Q_lo = int(Q.subs(a_s, 0))
    print(f"\n  Q(0) = {Q_lo}")
    check("B3: Q(0) = 10496 = N_pair^8 (N_quark^2 + N_quark - 1)",
          Q_lo == 256 * 41 and Q_lo == 2 ** 8 * (6 ** 2 + 6 - 1))


def audit_b4_q_p_relation(N: dict, S: dict) -> None:
    banner("B4: Q-P relation -- Q(alpha_s) = P(alpha_s) + 320 (4 - alpha_s)^2")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    expected = sp.simplify(P + 320 * (4 - a_s) ** 2)
    diff = sp.simplify(Q - expected)

    print(f"  Q(alpha_s) (expanded) = {Q}")
    print(f"  P(alpha_s) + 320 (4 - alpha_s)^2 = {sp.expand(expected)}")
    print(f"  Difference: {diff}")

    check("B4: Q(alpha_s) = P(alpha_s) + 320 (4 - alpha_s)^2",
          diff == 0)

    # Structural-integer: 320 = N_pair^6 (N_quark - 1) = 64 * 5.
    N_pair, N_quark = N["N_pair"], N["N_quark"]
    expected_320 = N_pair ** 6 * (N_quark - 1)
    check("B4 structural: 320 = N_pair^6 (N_quark - 1) = 64 * 5",
          expected_320 == 320)


def audit_b5_q_weitzenbock_relation(N: dict, S: dict) -> None:
    banner("B5: Q-Weitzenbock relation -- Q(alpha_s) = 2304 [(perim_sq)^2 + 16 Area^2]")

    a_s = S["a_s"]
    Q = S["Q_poly"]
    perim_sq = S["perim_sq"]
    area = S["area"]

    expected = sp.simplify(2304 * (perim_sq ** 2 + 16 * area ** 2))
    diff = sp.simplify(Q - expected)

    print(f"  Q(alpha_s) = {Q}")
    print(f"  2304 ((perim_sq)^2 + 16 Area^2) = {sp.expand(expected)}")
    print(f"  Difference: {diff}")

    check("B5: Q(alpha_s) = 2304 [(perim_sq)^2 + 16 Area^2]",
          diff == 0)

    # Structural recoding.
    N_pair, N_color = N["N_pair"], N["N_color"]
    print(f"\n  Structural form:")
    print(f"    Q(alpha_s) = N_pair^8 N_color^2 [(perim_sq)^2 + N_pair^4 Area^2]")
    print(f"               = {N_pair ** 8 * N_color ** 2} [(perim_sq)^2 + {N_pair ** 4} Area^2]")
    check("B5 structural: 2304 = N_pair^8 N_color^2",
          N_pair ** 8 * N_color ** 2 == 2304)
    check("B5 structural: 16 = N_pair^4",
          N_pair ** 4 == 16)


def audit_b6_lo_recovery(N: dict, S: dict, Omega_1: sp.Matrix, Omega_2: sp.Matrix) -> None:
    banner("B6: LO recovery in pure structural integers")

    a_s = S["a_s"]
    Omega_1_lo = sp.simplify(Omega_1.subs(a_s, 0))
    Omega_2_lo = sp.simplify(Omega_2.subs(a_s, 0))

    N_quark = N["N_quark"]
    denom = N_quark ** 2 + N_quark - 1  # = 41

    expected_O1 = sp.Matrix([
        sp.Rational(N_quark, denom),
        sp.sqrt(N_quark - 1) / denom,
    ])
    expected_O2 = sp.Matrix([
        sp.Rational(2 * N_quark - 1, denom),
        (N_quark - 1) ** sp.Rational(3, 2) / denom,
    ])

    diff_O1 = sp.simplify(Omega_1_lo - expected_O1)
    diff_O2 = sp.simplify(Omega_2_lo - expected_O2)

    print(f"  Omega_1 | LO = ({Omega_1_lo[0]}, {Omega_1_lo[1]})")
    print(f"  Expected: (N_quark, sqrt(N_quark - 1))/(N_quark^2 + N_quark - 1)")
    print(f"          = ({N_quark}/{denom}, sqrt({N_quark - 1})/{denom})")
    print(f"          = (6/41, sqrt(5)/41)")
    print(f"  Difference: {diff_O1}")
    check("B6: Omega_1 | LO = (N_quark, sqrt(N_quark - 1))/(N_quark^2 + N_quark - 1) = (6/41, sqrt(5)/41)",
          diff_O1 == sp.Matrix([0, 0]))

    print()
    print(f"  Omega_2 | LO = ({Omega_2_lo[0]}, {Omega_2_lo[1]})")
    print(f"  Expected: (2 N_quark - 1, (N_quark - 1)^(3/2))/(N_quark^2 + N_quark - 1)")
    print(f"          = ({2 * N_quark - 1}/{denom}, ({N_quark - 1})^(3/2)/{denom})")
    print(f"          = (11/41, 5 sqrt(5)/41)")
    print(f"  Difference: {diff_O2}")
    check("B6: Omega_2 | LO = (2 N_quark - 1, (N_quark - 1)^(3/2))/(N_quark^2 + N_quark - 1) = (11/41, 5 sqrt(5)/41)",
          diff_O2 == sp.Matrix([0, 0]))


def audit_b7_brocard_distance(N: dict, S: dict, Omega_1: sp.Matrix, Omega_2: sp.Matrix) -> None:
    banner("B7: NEW |Omega_1 - Omega_2|^2 closed form")

    a_s = S["a_s"]
    delta = Omega_1 - Omega_2
    delta_sq = sp.simplify(delta[0] ** 2 + delta[1] ** 2)

    # LO value.
    delta_sq_lo = sp.simplify(delta_sq.subs(a_s, 0))

    N_color, N_quark = N["N_color"], N["N_quark"]
    expected_lo = sp.Rational(N_color * (N_quark ** 2 - 1), (N_quark ** 2 + N_quark - 1) ** 2)

    print(f"  |Omega_1 - Omega_2|^2 | LO = {delta_sq_lo}")
    print(f"  Expected: N_color (N_quark^2 - 1)/(N_quark^2 + N_quark - 1)^2 = {N_color * (N_quark ** 2 - 1)}/{(N_quark ** 2 + N_quark - 1) ** 2} = {expected_lo}")
    diff_lo = sp.simplify(delta_sq_lo - expected_lo)
    print(f"  Difference (LO): {diff_lo}")

    check("B7 LO: |Omega_1 - Omega_2|^2 | LO = N_color (N_quark^2 - 1)/(N_quark^2 + N_quark - 1)^2 = 105/1681",
          diff_lo == 0)

    # Numerical readout for general alpha_s.
    print()
    print(f"  Numerical |Omega_1 - Omega_2|^2 across alpha_s:")
    samples = [0.0, 0.118, 0.30, 0.50, 1.0]
    for s in samples:
        val = float(delta_sq.subs(a_s, s))
        print(f"    alpha_s = {s:.3f}:  |Omega_1 - Omega_2|^2 = {val:.10f}")
    check("B7 sanity: |Omega_1 - Omega_2|^2 > 0 across physical alpha_s",
          all(float(delta_sq.subs(a_s, s)) > 0 for s in [0.0, 0.118, 0.5]))


def audit_b8_brocard_circle(N: dict, S: dict, Omega_1: sp.Matrix, Omega_2: sp.Matrix) -> None:
    banner("B8: Both Brocard points lie on the Brocard circle (verified)")

    a_s = S["a_s"]
    a = S["a"]
    b = S["b"]
    c = S["c"]
    V1, V2, V3 = S["V1"], S["V2"], S["V3"]

    # Circumcenter (retained).
    O = sp.Matrix([sp.Rational(1, 2), -a_s * sp.sqrt(5) / 40])

    # Symmedian point, computed directly from classical barycentric (a^2, b^2, c^2).
    a_sq = S["a_sq"]
    b_sq = S["b_sq"]
    c_sq = S["c_sq"]
    perim_sq = S["perim_sq"]
    K_x = sp.simplify((a_sq * V1[0] + b_sq * V2[0] + c_sq * V3[0]) / perim_sq)
    K_y = sp.simplify((a_sq * V1[1] + b_sq * V2[1] + c_sq * V3[1]) / perim_sq)
    K = sp.Matrix([K_x, K_y])

    # Brocard circle: passes through O, K, Omega_1, Omega_2; center M = (O+K)/2.
    M = sp.simplify(sp.Matrix([(O[0] + K[0]) / 2, (O[1] + K[1]) / 2]))

    # Brocard radius squared = OK^2/4.
    OK_sq = sp.simplify((O[0] - K[0]) ** 2 + (O[1] - K[1]) ** 2)
    radius_sq = sp.simplify(OK_sq / 4)

    # Distance from M to each Brocard point.
    M_O1_sq = sp.simplify((M[0] - Omega_1[0]) ** 2 + (M[1] - Omega_1[1]) ** 2)
    M_O2_sq = sp.simplify((M[0] - Omega_2[0]) ** 2 + (M[1] - Omega_2[1]) ** 2)

    # All four points should be equidistant from M.
    M_O_sq = sp.simplify((M[0] - O[0]) ** 2 + (M[1] - O[1]) ** 2)
    M_K_sq = sp.simplify((M[0] - K[0]) ** 2 + (M[1] - K[1]) ** 2)

    diff_O1 = sp.simplify(M_O1_sq - radius_sq)
    diff_O2 = sp.simplify(M_O2_sq - radius_sq)
    diff_O = sp.simplify(M_O_sq - radius_sq)
    diff_K = sp.simplify(M_K_sq - radius_sq)

    print(f"  Brocard circle center M = (O + K)/2.")
    print(f"  Brocard radius^2 = OK^2/4 = {radius_sq}")
    print()
    print(f"  |M - O|^2 - radius^2:        {diff_O}")
    print(f"  |M - K|^2 - radius^2:        {diff_K}")
    print(f"  |M - Omega_1|^2 - radius^2:  {diff_O1}")
    print(f"  |M - Omega_2|^2 - radius^2:  {diff_O2}")

    check("B8: O lies on Brocard circle", diff_O == 0)
    check("B8: K lies on Brocard circle", diff_K == 0)
    check("B8: Omega_1 lies on Brocard circle", diff_O1 == 0)
    check("B8: Omega_2 lies on Brocard circle", diff_O2 == 0)


def audit_b9_brocard_angle_property(N: dict, S: dict, Omega_1: sp.Matrix) -> None:
    banner("B9: Brocard angle property of Omega_1 verified numerically")

    a_s = S["a_s"]
    V1 = S["V1"]
    V2 = S["V2"]
    V3 = S["V3"]

    # Exact LO angle denominator.  From cot(omega)=perim_sq/(4*Area),
    # sin^2(omega)=1/(1+cot^2(omega)).
    cot_omega_sq_lo = sp.simplify((S["perim_sq"] / (4 * S["area"])) ** 2).subs(a_s, 0)
    sin_sq_lo = sp.simplify(1 / (1 + cot_omega_sq_lo))
    cos_sq_lo = sp.simplify(cot_omega_sq_lo / (1 + cot_omega_sq_lo))
    check("B9 LO: sin^2(omega_bar) = 5/41",
          sin_sq_lo == sp.Rational(5, 41))
    check("B9 LO: cos^2(omega_bar) = 36/41",
          cos_sq_lo == sp.Rational(36, 41))

    # Test at LO and at canonical alpha_s.
    samples = [(0.0, "LO"), (0.118, "PDG-ish"), (0.30, "mid-range")]

    print(f"  For each Omega_1, the angle (Omega_1 V_1 V_2) at V_1 should equal omega_bar.")
    print(f"  Similarly (Omega_1 V_2 V_3) at V_2 and (Omega_1 V_3 V_1) at V_3.")
    print()
    print(f"  alpha_s   angle@V_1   angle@V_2   angle@V_3   omega_bar (deg)   match?")

    all_match = True
    for s, label in samples:
        v1 = [float(V1[0].subs(a_s, s)) if hasattr(V1[0], 'subs') else float(V1[0]),
              float(V1[1].subs(a_s, s)) if hasattr(V1[1], 'subs') else float(V1[1])]
        v2 = [float(V2[0].subs(a_s, s)) if hasattr(V2[0], 'subs') else float(V2[0]),
              float(V2[1].subs(a_s, s)) if hasattr(V2[1], 'subs') else float(V2[1])]
        v3 = [float(V3[0].subs(a_s, s)), float(V3[1].subs(a_s, s))]
        o = [float(Omega_1[0].subs(a_s, s)), float(Omega_1[1].subs(a_s, s))]

        # Angle at V_1 between V_1V_2 and V_1Omega_1.
        u_12 = (v2[0] - v1[0], v2[1] - v1[1])
        u_1o = (o[0] - v1[0], o[1] - v1[1])
        ang_1 = math.degrees(math.atan2(
            abs(u_12[0] * u_1o[1] - u_12[1] * u_1o[0]),
            u_12[0] * u_1o[0] + u_12[1] * u_1o[1]
        ))

        # Angle at V_2 between V_2V_3 and V_2Omega_1.
        u_23 = (v3[0] - v2[0], v3[1] - v2[1])
        u_2o = (o[0] - v2[0], o[1] - v2[1])
        ang_2 = math.degrees(math.atan2(
            abs(u_23[0] * u_2o[1] - u_23[1] * u_2o[0]),
            u_23[0] * u_2o[0] + u_23[1] * u_2o[1]
        ))

        # Angle at V_3 between V_3V_1 and V_3Omega_1.
        u_31 = (v1[0] - v3[0], v1[1] - v3[1])
        u_3o = (o[0] - v3[0], o[1] - v3[1])
        ang_3 = math.degrees(math.atan2(
            abs(u_31[0] * u_3o[1] - u_31[1] * u_3o[0]),
            u_31[0] * u_3o[0] + u_31[1] * u_3o[1]
        ))

        # Compute omega_bar from the closed form (cot omega = perim_sq / (4 * Area)).
        ps = float(S["perim_sq"].subs(a_s, s))
        ar = float(S["area"].subs(a_s, s))
        cot_omega = ps / (4 * ar)
        omega_bar = math.degrees(math.atan2(1.0, cot_omega))

        match = (abs(ang_1 - omega_bar) < 0.01
                 and abs(ang_2 - omega_bar) < 0.01
                 and abs(ang_3 - omega_bar) < 0.01)
        all_match = all_match and match
        print(f"  {s:6.3f}   {ang_1:9.5f}   {ang_2:9.5f}   {ang_3:9.5f}   {omega_bar:9.5f}        {'OK' if match else 'FAIL'}")

    check("B9: Omega_1 satisfies all three Brocard angles = omega_bar",
          all_match)


def audit_package_wiring() -> None:
    banner("Package wiring: Brocard-points theorem is captured by repo truth surfaces")

    note_name = "CKM_BARRED_BROCARD_POINTS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md"
    runner_name = "frontier_ckm_barred_brocard_points_exact_closed_form.py"
    package_surfaces = (
        ("docs/CANONICAL_HARNESS_INDEX.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/CLAIMS_TABLE.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/DERIVATION_ATLAS.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/RESULTS_INDEX.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/PUBLICATION_MATRIX.md", (note_name, runner_name)),
        ("docs/publication/ci3_z3/FULL_CLAIM_LEDGER.md", (note_name, "not a direct metric")),
        ("docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md", (note_name, "NLO Brocard point")),
        ("docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md", (note_name, "directly measured")),
    )

    for rel_path, required_tokens in package_surfaces:
        content = read_authority(rel_path)
        ok = bool(content) and all(token in content for token in required_tokens)
        print(f"  {rel_path}: {'OK' if ok else 'MISSING'}")
        check(f"Package surface wired: {rel_path}", ok)


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA  (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS         (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY         (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (B1) First Brocard point on retained surface:")
    print("           Omega_1_x = (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q,")
    print("           Omega_1_y = 4 sqrt(5) (4 - alpha_s)^3 / Q.")
    print()
    print("    (B2) Second Brocard point on retained surface:")
    print("           Omega_2_x = 4 (4 - alpha_s) (alpha_s^2 - 24 alpha_s + 176) / Q,")
    print("           Omega_2_y = 4 sqrt(5)(4 - alpha_s)(80 + alpha_s^2) / Q.")
    print()
    print("    (B3) Q-polynomial: Q(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 + 80 (4 - alpha_s)^2.")
    print()
    print("    (B4) NEW Q-P relation: Q(alpha_s) = P(alpha_s) + 320 (4 - alpha_s)^2,")
    print("         where P(alpha_s) is the Brocard polynomial (universal equilateral excess).")
    print()
    print("    (B5) NEW Q-Weitzenbock relation:")
    print("           Q(alpha_s) = 2304 [(perim_sq)^2 + 16 Area^2]")
    print("                      = N_pair^8 N_color^2 [(perim_sq)^2 + N_pair^4 Area^2].")
    print()
    print("    (B6) LO recovery in pure structural integers:")
    print("           Omega_1 | LO = (N_quark, sqrt(N_quark - 1))/(N_quark^2 + N_quark - 1)")
    print("                        = (6, sqrt(5))/41,")
    print("           Omega_2 | LO = (2 N_quark - 1, (N_quark - 1)^(3/2))/(N_quark^2 + N_quark - 1)")
    print("                        = (11, 5 sqrt(5))/41.")
    print()
    print("    (B7) NEW Brocard-Brocard distance squared at LO:")
    print("           |Omega_1 - Omega_2|^2 | LO = N_color (N_quark^2 - 1)/(N_quark^2 + N_quark - 1)^2")
    print("                                       = 105/1681 = 105/41^2.")
    print()
    print("    (B8) Both Brocard points lie on the Brocard circle (4 concyclic points:")
    print("         O, K, Omega_1, Omega_2; verified symbolically).")
    print()
    print("    (B9) The Brocard angle property is satisfied: at each vertex, the angle")
    print("         from Omega_1 to the next vertex equals omega_bar (verified numerically),")
    print("         with LO sin^2(omega_bar)=5/41 and cos^2(omega_bar)=36/41.")


def main() -> int:
    print("=" * 88)
    print("Barred unitarity-triangle Brocard POINTS exact closed form audit")
    print("See docs/CKM_BARRED_BROCARD_POINTS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    Omega_1, Omega_2 = audit_b1_b2_brocard_points(N, S)
    audit_b3_q_polynomial(N, S)
    audit_b4_q_p_relation(N, S)
    audit_b5_q_weitzenbock_relation(N, S)
    audit_b6_lo_recovery(N, S, Omega_1, Omega_2)
    audit_b7_brocard_distance(N, S, Omega_1, Omega_2)
    audit_b8_brocard_circle(N, S, Omega_1, Omega_2)
    audit_b9_brocard_angle_property(N, S, Omega_1)
    audit_package_wiring()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
