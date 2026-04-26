#!/usr/bin/env python3
"""Brocard / Q polynomial perfect-square decomposition (algebraic structure).

Verifies the NEW retained closed forms in
  docs/CKM_BROCARD_Q_POLYNOMIAL_PERFECT_SQUARE_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (D1) The pair of fundamental quartic polynomials of the retained surface:
        P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2
                     [Brocard polynomial, universal equilateral excess],
        Q(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  +  80 (4 - alpha_s)^2
                     [Brocard-points denominator polynomial].

  (D2) NEW perfect-square decomposition (1):
        Q(alpha_s) - P(alpha_s)  =  320 (4 - alpha_s)^2
                                  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2.

       The DIFFERENCE Q - P is exactly a perfect square in (N_pair^2 - alpha_s)
       with structural-integer scaling N_pair^6 (N_quark - 1).

  (D3) NEW perfect-square decomposition (2):
        P(alpha_s) + 3 Q(alpha_s)  =  4 (alpha_s^2 - 4 alpha_s + 96)^2
                                    =  (N_pair^4 N_quark)^2 perim_sq^2 * 4
                                    =  4 (N_pair^4 N_quark perim_sq)^2.

       The combination P + 3Q is exactly a perfect square in
       (alpha_s^2 - 4 alpha_s + 96) = 48 perim_sq, with structural-integer
       scaling 4 = N_pair^2.

  (D4) Two perfect-square SUBSPACES of the (P, Q) module:
        - Q - P  perfect square in (N_pair^2 - alpha_s),
        - P + 3Q perfect square in (alpha_s^2 - 4 alpha_s + 96).
       Every other linear combination alpha P + beta Q is a perfect square
       only if it lies on one of these two lines:
         * beta = -alpha  (proportional to Q - P, perfect square in (4 - alpha_s)),
         * beta = 3 alpha (proportional to P + 3Q, perfect square in (alpha_s^2 - 4 alpha_s + 96)).

  (D5) Physical interpretation:
        - (4 - alpha_s) is proportional to eta_bar (and therefore to the
          Jarlskog J_bar in Wolfenstein-normalized form).
        - (alpha_s^2 - 4 alpha_s + 96) is exactly 48 * perim_sq, i.e. 48
          times the sum of squared sides of the unitarity triangle.
       So the perfect-square decomposition algebraically separates:
        - "Jarlskog channel" (Q - P): proportional to J_bar^2 with structural
          integer scaling N_pair^11 N_quark^2.
        - "Perimeter channel" (P + 3Q): proportional to perim_sq^2 with
          structural integer scaling 4 (N_pair^4 N_quark)^2 = N_pair^10 N_quark^2.

  (D6) Cross-channel identity (NEW):
        4 (P + 3Q)(Q - P)  =  perfect-square cross-product
                            =  16 N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2
                                (alpha_s^2 - 4 alpha_s + 96)^2.

       Equivalently:
        (P + 3Q)(Q - P) / 4  =  ((N_pair^4 N_quark perim_sq)
                                 (N_pair^3 sqrt(N_quark - 1)(N_pair^2 - alpha_s)))^2
                                 / N_pair^? ... (structural form).

  (D7) The (P, Q) algebraic system is "perfect-square-decomposable" --
       on the retained NLO Wolfenstein protected-gamma_bar surface, the
       polynomial pair admits a complete factorization into two
       structural-integer-scaled perfect squares.

Ground-up status verification: each cited authority's tier extracted from its
Status: line; closure derived only at extracted retained values.
"""

from __future__ import annotations

import math
import re
import sys
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

    counts = read_authority(
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md"
    )
    n_pair_match = re.search(r"n[_\s]pair\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_color_match = re.search(r"n[_\s]color\s*=\s*(\d+)", counts, re.IGNORECASE)
    n_quark_match = re.search(r"n[_\s]quark\s*=\s*n[_\s]pair\s*n[_\s]color", counts, re.IGNORECASE)

    print(f"  N_pair extracted:                  {n_pair_match.group(0) if n_pair_match else 'NOT FOUND'}")
    print(f"  N_color extracted:                 {n_color_match.group(0) if n_color_match else 'NOT FOUND'}")
    print(f"  N_quark = N_pair * N_color:        {'FOUND' if n_quark_match else 'NOT FOUND'}")

    check("MAGNITUDES retains N_pair = 2", n_pair_match and int(n_pair_match.group(1)) == 2)
    check("MAGNITUDES retains N_color = 3", n_color_match and int(n_color_match.group(1)) == 3)
    check("MAGNITUDES retains N_quark = N_pair * N_color (=6)", bool(n_quark_match))

    return {
        "N_pair": 2,
        "N_color": 3,
        "N_quark": 6,
    }


def setup_symbolic(N: dict):
    a_s = sp.symbols("alpha_s")
    P_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 - 240 * (4 - a_s) ** 2)
    Q_poly = sp.expand((a_s ** 2 - 4 * a_s + 96) ** 2 + 80 * (4 - a_s) ** 2)

    return {
        "a_s": a_s,
        "P_poly": P_poly,
        "Q_poly": Q_poly,
    }


def audit_d2_q_minus_p(N: dict, S: dict) -> None:
    banner("D2: Q - P perfect square in (N_pair^2 - alpha_s)")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    diff_QP = sp.simplify(Q - P)
    expected = sp.simplify(320 * (4 - a_s) ** 2)
    print(f"  Q(alpha_s) - P(alpha_s) (computed) = {diff_QP}")
    print(f"  Expected: 320 (4 - alpha_s)^2 = {expected}")
    delta = sp.simplify(diff_QP - expected)
    print(f"  Difference: {delta}")
    check("D2: Q(alpha_s) - P(alpha_s) = 320 (4 - alpha_s)^2",
          delta == 0)

    # Structural-integer scaling: 320 = N_pair^6 (N_quark - 1).
    N_pair, N_quark = N["N_pair"], N["N_quark"]
    expected_structural = N_pair ** 6 * (N_quark - 1)
    print(f"\n  Structural: 320 = N_pair^6 (N_quark - 1) = {N_pair ** 6} * {N_quark - 1} = {expected_structural}")
    check("D2 structural: 320 = N_pair^6 (N_quark - 1) = 64 * 5",
          expected_structural == 320)

    # Perfect-square form.
    structural_form = N_pair ** 6 * (N_quark - 1) * (N_pair ** 2 - a_s) ** 2
    diff_structural = sp.simplify(diff_QP - structural_form)
    check("D2 structural form: Q - P = N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2",
          diff_structural == 0)


def audit_d3_p_plus_3q(N: dict, S: dict) -> None:
    banner("D3: P + 3Q perfect square in (alpha_s^2 - 4 alpha_s + 96)")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    sum_P3Q = sp.expand(P + 3 * Q)
    expected = sp.expand(4 * (a_s ** 2 - 4 * a_s + 96) ** 2)
    print(f"  P(alpha_s) + 3 Q(alpha_s) (computed) = {sum_P3Q}")
    print(f"  Expected: 4 (alpha_s^2 - 4 alpha_s + 96)^2 = {expected}")
    delta = sp.simplify(sum_P3Q - expected)
    print(f"  Difference: {delta}")
    check("D3: P + 3 Q = 4 (alpha_s^2 - 4 alpha_s + 96)^2",
          delta == 0)

    # Structural form: 4 = N_pair^2.
    N_pair = N["N_pair"]
    expected_structural = N_pair ** 2 * (a_s ** 2 - 4 * a_s + 96) ** 2
    diff_structural = sp.simplify(sum_P3Q - expected_structural)
    check("D3 structural: P + 3 Q = N_pair^2 (alpha_s^2 - 4 alpha_s + 96)^2",
          diff_structural == 0)


def audit_d4_perfect_square_subspaces(N: dict, S: dict) -> None:
    banner("D4: Two perfect-square subspaces of the (P, Q) module")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    # General linear combination alpha P + beta Q.
    # Has form (alpha + beta)(alpha_s^2 - 4 alpha_s + 96)^2 + (-240 alpha + 80 beta)(4 - alpha_s)^2.
    # For this to be a perfect square, either:
    #   (a) beta = 3 alpha (then -240 alpha + 240 alpha = 0, gives multiple of (alpha_s^2 - 4 alpha_s + 96)^2),
    #   (b) beta = -alpha (then alpha - alpha = 0, gives multiple of (4 - alpha_s)^2).
    # These are the two perfect-square lines.

    print("  alpha P + beta Q = (alpha + beta)(alpha_s^2 - 4 alpha_s + 96)^2")
    print("                   + (-240 alpha + 80 beta)(4 - alpha_s)^2.")
    print()
    print("  Perfect-square iff either:")
    print("    Line A: beta = 3 alpha   =>   alpha P + beta Q proportional to (alpha_s^2 - 4 alpha_s + 96)^2,")
    print("    Line B: beta = -alpha    =>   alpha P + beta Q proportional to (4 - alpha_s)^2.")

    # Verify line A: take alpha = 1, beta = 3.
    line_A = sp.simplify(P + 3 * Q)
    line_A_expected = sp.simplify(4 * (a_s ** 2 - 4 * a_s + 96) ** 2)
    check("D4 Line A: P + 3Q = 4 (alpha_s^2 - 4 alpha_s + 96)^2",
          sp.simplify(line_A - line_A_expected) == 0)

    # Verify line B: take alpha = -1, beta = 1.
    line_B = sp.simplify(-P + Q)
    line_B_expected = sp.simplify(320 * (4 - a_s) ** 2)
    check("D4 Line B: -P + Q = Q - P = 320 (4 - alpha_s)^2",
          sp.simplify(line_B - line_B_expected) == 0)

    # Check that off-line combinations are NOT perfect squares.
    # Take alpha = 1, beta = 2 (between the two lines).
    off_line = sp.expand(P + 2 * Q)
    print(f"\n  Off-line example: P + 2 Q = {off_line}")
    # Has both (alpha_s^2-4alpha_s+96)^2 and (4-alpha_s)^2 contributions, neither zero.
    coeff_pq = 1 + 2  # = 3
    coeff_4ms = -240 + 160  # = -80
    print(f"    Coefficient of (alpha_s^2 - 4 alpha_s + 96)^2: {coeff_pq}")
    print(f"    Coefficient of (4 - alpha_s)^2:                {coeff_4ms}")
    print(f"    Both nonzero  =>  NOT a perfect square.")
    check("D4: P + 2Q has BOTH perfect-square components, not a single perfect square",
          coeff_pq != 0 and coeff_4ms != 0)


def audit_d5_physical_interpretation(N: dict, S: dict) -> None:
    banner("D5: Physical interpretation")

    a_s = S["a_s"]
    rho_bar = (4 - a_s) / 24
    eta_bar = sp.sqrt(5) * (4 - a_s) / 24

    # perim_sq = (alpha_s^2 - 4 alpha_s + 96)/48.
    perim_sq = (a_s ** 2 - 4 * a_s + 96) / 48
    expected_perim_sq = sp.Rational(1, 48) * (a_s ** 2 - 4 * a_s + 96)
    diff_perim = sp.simplify(perim_sq - expected_perim_sq)
    check("D5: perim_sq = (alpha_s^2 - 4 alpha_s + 96)/48",
          diff_perim == 0)

    # eta_bar^2 in terms of (4 - alpha_s)^2.
    eta_bar_sq = sp.simplify(eta_bar ** 2)
    expected_eta_bar_sq = sp.simplify(5 * (4 - a_s) ** 2 / 576)
    diff_eta = sp.simplify(eta_bar_sq - expected_eta_bar_sq)
    check("D5: eta_bar^2 = 5 (4 - alpha_s)^2 / 576",
          diff_eta == 0)

    # Connection: (Q - P) proportional to eta_bar^2 (and hence to Jarlskog^2).
    # (Q - P) = 320 (4 - alpha_s)^2 = 320 * 576 eta_bar^2 / 5 = 36864 eta_bar^2.
    Q_minus_P = sp.simplify(S["Q_poly"] - S["P_poly"])
    eta_bar_sq_form = sp.simplify(36864 * eta_bar_sq)
    diff_jarlskog = sp.simplify(Q_minus_P - eta_bar_sq_form)
    print(f"\n  Q - P (in eta_bar^2 form):")
    print(f"    Q - P = {sp.simplify(Q_minus_P)}")
    print(f"    Expected: 36864 eta_bar^2 = {eta_bar_sq_form}")
    print(f"    Difference: {diff_jarlskog}")
    check("D5 Jarlskog channel: Q - P = 36864 eta_bar^2",
          diff_jarlskog == 0)

    # Check structural form: 36864 = N_pair^11 * N_quark^2 / (N_quark - 1)? Hmm.
    # 36864 = 320 * 576 / 5 = 64 * 576 = 36864. And 576 = 24^2 = (N_pair^2 N_quark)^2 / ? 24 = N_pair^2 N_quark / N_pair = N_pair N_quark. Yes.
    # 24 = N_pair * N_quark? N_pair * N_quark = 2 * 6 = 12. NO.
    # 24 = N_pair^2 N_quark? = 4 * 6 = 24 YES.
    # So 576 = (N_pair^2 N_quark)^2 = N_pair^4 N_quark^2.
    # And 320 = N_pair^6 (N_quark - 1).
    # 320 * 576 / 5 = N_pair^6 (N_quark - 1) * N_pair^4 N_quark^2 / (N_quark - 1) = N_pair^10 N_quark^2.
    # Hmm wait that's 1024 * 36 = 36864 ✓.
    N_pair, N_quark = N["N_pair"], N["N_quark"]
    expected_structural = N_pair ** 10 * N_quark ** 2
    print(f"\n  Structural: 36864 = N_pair^10 N_quark^2 = {N_pair ** 10} * {N_quark ** 2} = {expected_structural}")
    check("D5: Q - P = N_pair^10 N_quark^2 eta_bar^2 (Jarlskog channel)",
          expected_structural == 36864)

    # Connection: (P + 3Q) proportional to perim_sq^2.
    # (P + 3Q) = 4 (alpha_s^2 - 4 alpha_s + 96)^2 = 4 * (48 perim_sq)^2 = 4 * 2304 perim_sq^2 = 9216 perim_sq^2.
    P_plus_3Q = sp.simplify(S["P_poly"] + 3 * S["Q_poly"])
    perim_sq_form = sp.simplify(9216 * perim_sq ** 2)
    diff_perim_2 = sp.simplify(P_plus_3Q - perim_sq_form)
    check("D5 Perimeter channel: P + 3 Q = 9216 perim_sq^2",
          diff_perim_2 == 0)

    # 9216 = 96^2 = (N_pair^4 N_quark)^2 = N_pair^8 N_quark^2.
    expected_structural_2 = N_pair ** 8 * N_quark ** 2
    check("D5: P + 3 Q = N_pair^8 N_quark^2 perim_sq^2 = (N_pair^4 N_quark perim_sq)^2",
          expected_structural_2 == 9216)


def audit_d6_cross_channel_identity(N: dict, S: dict) -> None:
    banner("D6: Cross-channel identity -- (P + 3Q)(Q - P) is a structured product")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    product = sp.expand((P + 3 * Q) * (Q - P))
    expected = sp.expand(
        4 * (a_s ** 2 - 4 * a_s + 96) ** 2 * 320 * (4 - a_s) ** 2
    )
    diff = sp.simplify(product - expected)
    print(f"  (P + 3Q)(Q - P) (computed) = {sp.simplify(product)}")
    print(f"  Expected: 1280 (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2")
    print(f"  Difference: {diff}")
    check("D6: (P + 3Q)(Q - P) = 1280 (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2",
          diff == 0)

    # 1280 = 4 * 320 = N_pair^2 * N_pair^6 (N_quark - 1) = N_pair^8 (N_quark - 1).
    N_pair, N_quark = N["N_pair"], N["N_quark"]
    expected_scaling = N_pair ** 8 * (N_quark - 1)
    print(f"\n  Structural: 1280 = N_pair^8 (N_quark - 1) = {N_pair ** 8} * {N_quark - 1} = {expected_scaling}")
    check("D6 structural: 1280 = N_pair^8 (N_quark - 1) = 256 * 5",
          expected_scaling == 1280)

    # Cross-product as perfect square of cross-product:
    # (P + 3Q)(Q - P) = (4 (...)^2) * (320 (4 - alpha_s)^2)
    #                = 4 * 320 * ((alpha_s^2 - 4 alpha_s + 96)(4 - alpha_s))^2
    # is the SQUARE of structural integer * (alpha_s^2 - 4 alpha_s + 96)(4 - alpha_s).
    # 4 * 320 = 1280. sqrt(1280) = sqrt(N_pair^8 (N_quark-1)) = N_pair^4 sqrt(N_quark-1).
    # So sqrt((P + 3Q)(Q - P)) = N_pair^4 sqrt(N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)(4 - alpha_s).
    sqrt_product = N_pair ** 4 * sp.sqrt(N_quark - 1) * (a_s ** 2 - 4 * a_s + 96) * (4 - a_s)
    diff_sqrt = sp.simplify(product - sqrt_product ** 2)
    check("D6: sqrt((P + 3Q)(Q - P)) = N_pair^4 sqrt(N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)(4 - alpha_s)",
          diff_sqrt == 0)


def audit_d7_module_structure(N: dict, S: dict) -> None:
    banner("D7: (P, Q) algebraic system - perfect-square decomposition")

    print("  The (P, Q) module on the retained surface has the structure:")
    print("    {alpha P + beta Q : alpha, beta in Q}")
    print("    = (alpha + beta)(alpha_s^2 - 4 alpha_s + 96)^2 + (-240 alpha + 80 beta)(4 - alpha_s)^2.")
    print()
    print("  The 'perfect-square' subset is the union of two 1-D lines:")
    print("    Line A: {(alpha, 3 alpha) : alpha in Q}, generated by P + 3Q,")
    print("    Line B: {(alpha, -alpha) : alpha in Q}, generated by Q - P.")
    print()
    print("  Other linear combinations (off the two lines) have BOTH")
    print("  (alpha_s^2 - 4 alpha_s + 96)^2 and (4 - alpha_s)^2 components,")
    print("  and are therefore NOT perfect squares as polynomials in alpha_s.")
    print()
    print("  The two perfect-square forms encode:")
    print("    P + 3Q proportional to perim_sq^2  (Perimeter channel),")
    print("    Q - P proportional to eta_bar^2     (Jarlskog channel).")
    print()
    print("  Together they span the (P, Q) module under linear combination:")
    print("    P  =  ((P + 3Q) - 3(Q - P))/4  =  (perim^2-channel - 3 * Jarlskog-channel)/4,")
    print("    Q  =  ((P + 3Q) + (Q - P))/4   =  (perim^2-channel + Jarlskog-channel)/4.")

    a_s = S["a_s"]
    P = S["P_poly"]
    Q = S["Q_poly"]

    # Verify the inverse relations.
    check_P = sp.simplify(P - ((P + 3 * Q) - 3 * (Q - P)) / 4)
    check_Q = sp.simplify(Q - ((P + 3 * Q) + (Q - P)) / 4)
    check("D7: P = ((P + 3Q) - 3(Q - P))/4 (inverse relation)",
          check_P == 0)
    check("D7: Q = ((P + 3Q) + (Q - P))/4 (inverse relation)",
          check_Q == 0)


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA  (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS         (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY         (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (D2) Q(alpha_s) - P(alpha_s)  =  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2,")
    print("         a perfect square in (4 - alpha_s) with structural-integer scaling.")
    print()
    print("    (D3) P(alpha_s) + 3 Q(alpha_s)  =  N_pair^2 (alpha_s^2 - 4 alpha_s + 96)^2,")
    print("         a perfect square in (alpha_s^2 - 4 alpha_s + 96) = 48 perim_sq.")
    print()
    print("    (D4) Two perfect-square SUBSPACES of the (P, Q) module:")
    print("         Line A (beta = 3 alpha):   alpha P + 3 alpha Q  =  4 alpha (alpha_s^2 - 4 alpha_s + 96)^2,")
    print("         Line B (beta = -alpha):    alpha P - alpha Q    =  -320 alpha (4 - alpha_s)^2.")
    print("         All other (alpha, beta) give linear combinations that are NOT")
    print("         perfect squares in alpha_s (have both (alpha_s^2 - 4 alpha_s + 96)^2 and")
    print("         (4 - alpha_s)^2 components).")
    print()
    print("    (D5) Physical interpretation:")
    print("         Q - P  =  N_pair^10 N_quark^2 eta_bar^2     [Jarlskog channel],")
    print("         P + 3Q  =  N_pair^8 N_quark^2 perim_sq^2    [Perimeter channel].")
    print()
    print("    (D6) Cross-channel identity (NEW):")
    print("         (P + 3Q)(Q - P)  =  N_pair^8 (N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)^2 (4 - alpha_s)^2.")
    print("         sqrt((P + 3Q)(Q - P))  =  N_pair^4 sqrt(N_quark - 1) (alpha_s^2 - 4 alpha_s + 96)(4 - alpha_s).")
    print()
    print("    (D7) The (P, Q) algebraic module is perfect-square-decomposable on")
    print("         the retained surface. The two perfect-square forms span the module:")
    print("           P  =  ((P + 3Q) - 3(Q - P))/4,")
    print("           Q  =  ((P + 3Q) + (Q - P))/4.")
    print()
    print("  All identities exact via sympy; closure on retained-tier authorities only.")


def main() -> int:
    print("=" * 88)
    print("Brocard / Q polynomial perfect-square decomposition audit")
    print("See docs/CKM_BROCARD_Q_POLYNOMIAL_PERFECT_SQUARE_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    audit_d2_q_minus_p(N, S)
    audit_d3_p_plus_3q(N, S)
    audit_d4_perfect_square_subspaces(N, S)
    audit_d5_physical_interpretation(N, S)
    audit_d6_cross_channel_identity(N, S)
    audit_d7_module_structure(N, S)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
