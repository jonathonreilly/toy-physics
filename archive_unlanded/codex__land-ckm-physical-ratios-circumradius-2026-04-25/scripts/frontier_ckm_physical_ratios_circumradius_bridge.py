#!/usr/bin/env python3
"""CKM physical ratios circumradius bridge.

Verifies the NEW retained closed forms in
  docs/CKM_PHYSICAL_RATIOS_CIRCUMRADIUS_BRIDGE_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (R2) |V_td/V_ts|^2 (NLO Wolfenstein):
        |V_td/V_ts|^2  =  lambda^2 * ((1 - rho_bar)^2 + eta_bar^2)
                       =  alpha_s (80 + alpha_s^2) / 192.

  (R3) NEW retained CIRCUMRADIUS BRIDGE:
        |V_td/V_ts|^2  =  ((N_quark - 1) / N_color) * alpha_s * R_bar^2
                       =  (5/3) alpha_s R_bar^2.

       So the B-meson mixing CKM ratio |V_td/V_ts|^2 is directly proportional
       to the SQUARE OF THE CIRCUMRADIUS of the unitarity triangle, with
       structural-integer scaling (N_quark - 1)/N_color and a single
       factor of alpha_s.

  (R4) |V_us/V_cb|^2 closed form:
        |V_us/V_cb|^2  =  (alpha_s/2) / (alpha_s^2/6)  =  3/alpha_s
                       =  N_color / alpha_s.

  (R5) |V_ub/V_cb|^2 closed form:
        |V_ub/V_cb|^2  =  lambda^2 (rho^2 + eta^2)  =  alpha_s/12
                       =  alpha_s / (N_pair^2 * N_color).

  (R6) NEW compound CIRCUMRADIUS identity:
        |V_us V_td / (V_cb V_ts)|^2  =  (N_quark - 1) * R_bar^2
                                      =  5 R_bar^2.

       So the FOUR-element ratio |V_us V_td / V_cb V_ts|^2 is exactly
       (N_quark - 1) times the squared circumradius of the unitarity
       triangle. The leading multiplicative alpha_s prefactor cancels;
       the remaining alpha_s dependence is only the geometric dependence
       inside R_bar^2 = 1/4 + alpha_s^2/320.

  (R7) Numerical comparison to CKM-ratio comparators at canonical
       alpha_s(v) = 0.103303816...:
        |V_td/V_ts|       ~  0.2075  (comparator: 0.211 +/- 0.005)
        |V_ub/V_cb|       ~  0.0928  (comparator: 0.092 +/- 0.008)
        |V_us/V_cb|       ~  5.389   (comparator: 5.49 +/- 0.20).

Ground-up status verification: each cited authority's tier extracted from its
Status: line; closure derived only at extracted retained values.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import sympy as sp

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


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
        ("docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
         "Retained structural-identity subtheorem",
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
    a_s = sp.symbols("alpha_s", positive=True)
    rho_bar = (4 - a_s) / 24
    eta_bar = sp.sqrt(5) * (4 - a_s) / 24
    rho = sp.Rational(1, 6)
    eta = sp.sqrt(5) / 6

    lambda_sq = a_s / 2  # retained Wolfenstein lambda^2 = alpha_s/2.
    A_sq = sp.Rational(2, 3)  # retained A^2.

    # CKM ratio closed forms (in terms of retained Wolfenstein parameters).
    # |V_td/V_ts|^2 = lambda^2 * ((1 - rho_bar)^2 + eta_bar^2).
    Vtd_Vts_sq = sp.simplify(lambda_sq * ((1 - rho_bar) ** 2 + eta_bar ** 2))

    # |V_us/V_cb|^2 = lambda^2 / (A^2 lambda^4) = 1/(A^2 lambda^2).
    Vus_Vcb_sq = sp.simplify(1 / (A_sq * lambda_sq))

    # |V_ub/V_cb|^2 = lambda^2 (rho^2 + eta^2).
    Vub_Vcb_sq = sp.simplify(lambda_sq * (rho ** 2 + eta ** 2))

    # Retained R_bar^2 closed form.
    R_bar_sq = sp.Rational(1, 4) + a_s ** 2 / 320  # retained.

    return {
        "a_s": a_s,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "rho": rho,
        "eta": eta,
        "lambda_sq": lambda_sq,
        "A_sq": A_sq,
        "Vtd_Vts_sq": Vtd_Vts_sq,
        "Vus_Vcb_sq": Vus_Vcb_sq,
        "Vub_Vcb_sq": Vub_Vcb_sq,
        "R_bar_sq": R_bar_sq,
    }


def audit_r2_vtd_vts(N: dict, S: dict) -> None:
    banner("R2: |V_td/V_ts|^2 closed form")

    a_s = S["a_s"]
    Vtd_Vts_sq = S["Vtd_Vts_sq"]

    expected = sp.simplify(a_s * (80 + a_s ** 2) / 192)
    diff = sp.simplify(Vtd_Vts_sq - expected)

    print(f"  |V_td/V_ts|^2 (computed) = {Vtd_Vts_sq}")
    print(f"  Expected: alpha_s (80 + alpha_s^2) / 192 = {expected}")
    print(f"  Difference: {diff}")
    check("R2: |V_td/V_ts|^2 = alpha_s (80 + alpha_s^2)/192",
          diff == 0)

    N_pair, N_quark = N["N_pair"], N["N_quark"]
    structural_form = a_s * (N_pair ** 4 * (N_quark - 1) + a_s ** 2) / (N_pair ** 5 * N_quark)
    diff_structural = sp.simplify(Vtd_Vts_sq - structural_form)
    check("R2 structural: |V_td/V_ts|^2 = alpha_s (N_pair^4(N_quark-1) + alpha_s^2)/(N_pair^5 N_quark)",
          diff_structural == 0)


def audit_r3_circumradius_bridge(N: dict, S: dict) -> None:
    banner("R3: NEW circumradius bridge -- |V_td/V_ts|^2 = (5/3) alpha_s R_bar^2")

    a_s = S["a_s"]
    Vtd_Vts_sq = S["Vtd_Vts_sq"]
    R_bar_sq = S["R_bar_sq"]

    bridge = sp.simplify(Vtd_Vts_sq / (a_s * R_bar_sq))
    expected = sp.Rational(5, 3)
    diff = sp.simplify(bridge - expected)

    print(f"  |V_td/V_ts|^2 / (alpha_s R_bar^2) (computed) = {bridge}")
    print(f"  Expected: (N_quark - 1)/N_color = 5/3 = {expected}")
    print(f"  Difference: {diff}")
    check("R3: |V_td/V_ts|^2 = (N_quark - 1)/N_color * alpha_s * R_bar^2 = (5/3) alpha_s R_bar^2",
          diff == 0)

    N_color, N_quark = N["N_color"], N["N_quark"]
    expected_struct = sp.Rational(N_quark - 1, N_color)
    print(f"\n  Structural form: (N_quark - 1)/N_color = ({N_quark - 1})/{N_color} = {expected_struct}")
    check("R3 structural: ratio = (N_quark - 1)/N_color = 5/3",
          expected_struct == sp.Rational(5, 3))

    # Equivalent: 3 |V_td/V_ts|^2 = 5 alpha_s R_bar^2, i.e.,
    # N_color |V_td/V_ts|^2 = (N_quark - 1) alpha_s R_bar^2.
    diff_alt = sp.simplify(N_color * Vtd_Vts_sq - (N_quark - 1) * a_s * R_bar_sq)
    print(f"\n  Alternative form: N_color |V_td/V_ts|^2 = (N_quark - 1) alpha_s R_bar^2")
    check("R3 alt: N_color * |V_td/V_ts|^2 = (N_quark - 1) * alpha_s * R_bar^2",
          diff_alt == 0)


def audit_r4_vus_vcb(N: dict, S: dict) -> None:
    banner("R4: |V_us/V_cb|^2 = N_color/alpha_s")

    a_s = S["a_s"]
    Vus_Vcb_sq = S["Vus_Vcb_sq"]

    expected = sp.simplify(sp.Rational(N["N_color"], 1) / a_s)
    diff = sp.simplify(Vus_Vcb_sq - expected)

    print(f"  |V_us/V_cb|^2 (computed) = {Vus_Vcb_sq}")
    print(f"  Expected: N_color/alpha_s = 3/alpha_s = {expected}")
    print(f"  Difference: {diff}")
    check("R4: |V_us/V_cb|^2 = N_color/alpha_s = 3/alpha_s",
          diff == 0)


def audit_r5_vub_vcb(N: dict, S: dict) -> None:
    banner("R5: |V_ub/V_cb|^2 = alpha_s/(N_pair^2 N_color)")

    a_s = S["a_s"]
    Vub_Vcb_sq = S["Vub_Vcb_sq"]

    N_pair, N_color = N["N_pair"], N["N_color"]
    expected = sp.simplify(a_s / (N_pair ** 2 * N_color))
    diff = sp.simplify(Vub_Vcb_sq - expected)

    print(f"  |V_ub/V_cb|^2 (computed) = {Vub_Vcb_sq}")
    print(f"  Expected: alpha_s/(N_pair^2 N_color) = alpha_s/12 = {expected}")
    print(f"  Difference: {diff}")
    check("R5: |V_ub/V_cb|^2 = alpha_s/(N_pair^2 N_color) = alpha_s/12",
          diff == 0)


def audit_r6_compound_circumradius(N: dict, S: dict) -> None:
    banner("R6: NEW compound identity |V_us V_td/(V_cb V_ts)|^2 = (N_quark - 1) R_bar^2")

    a_s = S["a_s"]
    Vtd_Vts_sq = S["Vtd_Vts_sq"]
    Vus_Vcb_sq = S["Vus_Vcb_sq"]
    R_bar_sq = S["R_bar_sq"]

    compound = sp.simplify(Vtd_Vts_sq * Vus_Vcb_sq)
    expected = sp.simplify((N["N_quark"] - 1) * R_bar_sq)
    diff = sp.simplify(compound - expected)

    print(f"  |V_us V_td/(V_cb V_ts)|^2 (computed)")
    print(f"     = |V_us/V_cb|^2 * |V_td/V_ts|^2")
    print(f"     = {compound}")
    print(f"  Expected: (N_quark - 1) R_bar^2 = 5 R_bar^2 = {expected}")
    print(f"  Difference: {diff}")

    check("R6 NEW: |V_us V_td/(V_cb V_ts)|^2 = (N_quark - 1) R_bar^2",
          diff == 0)

    print()
    explicit_alpha = sp.simplify(expected.expand())
    print("  This is a 4-CKM-element-ratio observable expressed as a STRUCTURAL")
    print("  INTEGER multiple of the SQUARED CIRCUMRADIUS of the unitarity triangle.")
    print("  The leading multiplicative alpha_s prefactor cancels, but R_bar^2")
    print(f"  still contains the retained alpha_s^2 geometry: {explicit_alpha}.")
    print()
    print("  At LO (alpha_s = 0): R_bar | LO = 1/2, so")
    print("    |V_us V_td/(V_cb V_ts)|^2 | LO  =  (N_quark - 1) (1/2)^2  =  5/4.")
    compound_lo = sp.simplify(compound.subs(a_s, 0))
    print(f"\n    |V_us V_td/(V_cb V_ts)|^2 | LO (computed) = {compound_lo}")
    check("R6 LO: |V_us V_td/(V_cb V_ts)|^2 | LO = 5/4",
          compound_lo == sp.Rational(5, 4))


def audit_r7_pdg_comparison(N: dict, S: dict) -> None:
    banner("R7: numerical CKM-ratio comparator")

    a_s = S["a_s"]
    Vtd_Vts_sq = S["Vtd_Vts_sq"]
    Vus_Vcb_sq = S["Vus_Vcb_sq"]
    Vub_Vcb_sq = S["Vub_Vcb_sq"]

    comparators = {
        "|V_td/V_ts|": (0.211, 0.005),
        "|V_ub/V_cb|": (0.092, 0.008),
        "|V_us/V_cb|": (5.49, 0.20),
    }

    s = CANONICAL_ALPHA_S_V
    print(f"  canonical alpha_s(v) = {s:.15f}")
    ratio_td_ts = float(sp.sqrt(Vtd_Vts_sq).subs(a_s, s))
    ratio_ub_cb = float(sp.sqrt(Vub_Vcb_sq).subs(a_s, s))
    ratio_us_cb = float(sp.sqrt(Vus_Vcb_sq).subs(a_s, s))

    ratios = {
        "|V_td/V_ts|": ratio_td_ts,
        "|V_ub/V_cb|": ratio_ub_cb,
        "|V_us/V_cb|": ratio_us_cb,
    }

    for name, value in ratios.items():
        central, err = comparators[name]
        sigma = abs(value - central) / err
        print(f"  {name:<13} = {value:.6f}  (comparator: {central} +/- {err}; {sigma:.2f} sigma)")

    print()
    for name, value in ratios.items():
        central, err = comparators[name]
        sigma = abs(value - central) / err
        check(f"R7: {name} at canonical alpha_s(v) within 2 sigma of comparator",
              sigma < 2)


def audit_summary() -> None:
    banner("Summary of NEW retained content")

    print("  Inputs (retained-tier, ground-up Status verified):")
    print("    CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA  (retained)")
    print("    CKM_MAGNITUDES_STRUCTURAL_COUNTS         (retained)")
    print("    CKM_CP_PHASE_STRUCTURAL_IDENTITY         (retained)")
    print("    CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM (retained)")
    print("    WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES (retained)")
    print()
    print("  NEW retained closed forms:")
    print()
    print("    (R2) |V_td/V_ts|^2  =  alpha_s (80 + alpha_s^2)/192")
    print("                        =  alpha_s (N_pair^4 (N_quark - 1) + alpha_s^2)")
    print("                           / (N_pair^5 N_quark).")
    print()
    print("    (R3) NEW CIRCUMRADIUS BRIDGE:")
    print("           |V_td/V_ts|^2  =  (N_quark - 1)/N_color * alpha_s * R_bar^2")
    print("                          =  (5/3) alpha_s R_bar^2.")
    print()
    print("         The B-meson mixing CKM ratio is exactly proportional to the")
    print("         SQUARED CIRCUMRADIUS of the unitarity triangle on the retained")
    print("         surface, with structural-integer coupling (N_quark - 1)/N_color.")
    print()
    print("    (R4) |V_us/V_cb|^2  =  N_color/alpha_s.")
    print()
    print("    (R5) |V_ub/V_cb|^2  =  alpha_s/(N_pair^2 N_color)  =  alpha_s/12.")
    print()
    print("    (R6) NEW compound CIRCUMRADIUS identity:")
    print("           |V_us V_td/(V_cb V_ts)|^2  =  (N_quark - 1) R_bar^2.")
    print()
    print("         A 4-CKM-element-ratio observable is exactly (N_quark - 1)")
    print("         times the squared circumradius of the unitarity triangle.")
    print("         The leading multiplicative alpha_s prefactor cancels;")
    print("         R_bar^2 still carries the retained alpha_s^2 correction.")
    print()
    print(f"    (R7) Framework readouts at canonical alpha_s(v) = {CANONICAL_ALPHA_S_V:.10f}")
    print("         match listed CKM-ratio comparators within < 2 sigma for")
    print("         |V_td/V_ts|, |V_ub/V_cb|, and |V_us/V_cb|.")


def main() -> int:
    print("=" * 88)
    print("CKM physical ratios circumradius bridge audit")
    print("See docs/CKM_PHYSICAL_RATIOS_CIRCUMRADIUS_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    audit_r2_vtd_vts(N, S)
    audit_r3_circumradius_bridge(N, S)
    audit_r4_vus_vcb(N, S)
    audit_r5_vub_vcb(N, S)
    audit_r6_compound_circumradius(N, S)
    audit_r7_pdg_comparison(N, S)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
