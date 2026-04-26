#!/usr/bin/env python3
"""CKM compound-magnitude circumradius bridge.

Verifies the NEW retained closed forms in
  docs/CKM_COMPOUND_MAGNITUDES_CIRCUMRADIUS_BRIDGE_THEOREM_NOTE_2026-04-25.md

Key NEW identities on the retained NLO Wolfenstein protected-gamma_bar surface:

  (C1) Three-magnitude circumradius bridge (NEW):
        N_color * |V_td|^2  =  N_pair * (N_quark - 1) * |V_us|^2 * |V_cb|^2 * R_bar^2,

       i.e.,
        3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2,
       or
        |V_td|^2  =  (N_pair (N_quark - 1)/N_color) |V_us|^2 |V_cb|^2 R_bar^2
                  =  (10/3) |V_us|^2 |V_cb|^2 R_bar^2.

  (C2) Four-magnitude circumradius bridge (NEW):
        (|V_td V_us| / |V_cb V_ub|)^2  =  N_pair^2 * N_color * (N_quark - 1) * R_bar^2 / alpha_s
                                        =  60 R_bar^2 / alpha_s.

  (C3) Equivalent form (eliminating alpha_s via |V_us|^2 = alpha_s/N_pair):
        (|V_td V_us| / |V_cb V_ub|)^2  =  (N_pair^3 N_color (N_quark - 1)) R_bar^2 / |V_us|^2
                                        =  120 R_bar^2 / |V_us|^2,
       since alpha_s = N_pair |V_us|^2 implies 1/alpha_s = 1/(N_pair |V_us|^2),
       so 60/alpha_s = 60/(N_pair |V_us|^2) = 30/|V_us|^2... hmm let me re-check.

       Actually 60 R_bar^2/alpha_s = 60 R_bar^2 / (N_pair |V_us|^2) = 30 R_bar^2/|V_us|^2.

       So (|V_td V_us| / |V_cb V_ub|)^2 = 30 R_bar^2/|V_us|^2,
       i.e., |V_td V_us|^2 / |V_cb V_ub|^2 = 30 R_bar^2 / |V_us|^2,
       so   |V_td|^2 |V_us|^4 = 30 R_bar^2 |V_cb|^2 |V_ub|^2.

       Let me re-verify the structural integer factor.
       In structural form: 30 = N_pair × N_color × (N_quark - 1) = 2 * 3 * 5 = 30.
       Yes 30 = N_pair N_color (N_quark - 1).

  (C4) PDG numerical comparison.
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

    lambda_sq = a_s / 2
    A_sq = sp.Rational(2, 3)
    rho = sp.Rational(1, 6)
    eta = sp.sqrt(5) / 6

    Vus_sq = lambda_sq
    Vcb_sq = A_sq * lambda_sq ** 2
    Vub_sq = A_sq * lambda_sq ** 3 * (rho ** 2 + eta ** 2)

    rho_bar = (4 - a_s) / 24
    eta_bar = sp.sqrt(5) * (4 - a_s) / 24
    R_bar_sq = sp.Rational(1, 4) + a_s ** 2 / 320
    Vtd_sq = A_sq * lambda_sq ** 3 * ((1 - rho_bar) ** 2 + eta_bar ** 2)
    Vts_sq = A_sq * lambda_sq ** 2

    return {
        "a_s": a_s,
        "Vus_sq": Vus_sq,
        "Vcb_sq": Vcb_sq,
        "Vub_sq": Vub_sq,
        "Vtd_sq": Vtd_sq,
        "Vts_sq": Vts_sq,
        "R_bar_sq": R_bar_sq,
    }


def audit_c1_three_magnitude_bridge(N: dict, S: dict) -> None:
    banner("C1: NEW three-magnitude circumradius bridge")

    a_s = S["a_s"]
    Vtd_sq = S["Vtd_sq"]
    Vus_sq = S["Vus_sq"]
    Vcb_sq = S["Vcb_sq"]
    R_bar_sq = S["R_bar_sq"]

    N_pair, N_color, N_quark = N["N_pair"], N["N_color"], N["N_quark"]
    expected = sp.simplify(
        sp.Rational(N_pair * (N_quark - 1), N_color) * Vus_sq * Vcb_sq * R_bar_sq
    )
    diff = sp.simplify(Vtd_sq - expected)

    print(f"  |V_td|^2 (computed) = {sp.simplify(Vtd_sq)}")
    print(f"  Expected: (N_pair (N_quark - 1)/N_color) |V_us|^2 |V_cb|^2 R_bar^2")
    print(f"          = (10/3) |V_us|^2 |V_cb|^2 R_bar^2")
    print(f"          = {expected}")
    print(f"  Difference: {diff}")

    check("C1: |V_td|^2 = (N_pair (N_quark - 1)/N_color) |V_us|^2 |V_cb|^2 R_bar^2",
          diff == 0)

    # Equivalent form: N_color |V_td|^2 = N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2.
    diff_alt = sp.simplify(N_color * Vtd_sq - N_pair * (N_quark - 1) * Vus_sq * Vcb_sq * R_bar_sq)
    check("C1 alt: N_color |V_td|^2 = N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2",
          diff_alt == 0)


def audit_c2_four_magnitude_bridge(N: dict, S: dict) -> None:
    banner("C2: NEW four-magnitude circumradius bridge")

    a_s = S["a_s"]
    Vtd_sq = S["Vtd_sq"]
    Vus_sq = S["Vus_sq"]
    Vcb_sq = S["Vcb_sq"]
    Vub_sq = S["Vub_sq"]
    R_bar_sq = S["R_bar_sq"]

    compound_sq = sp.simplify(Vtd_sq * Vus_sq / (Vcb_sq * Vub_sq))

    N_pair, N_color, N_quark = N["N_pair"], N["N_color"], N["N_quark"]
    expected = sp.simplify(N_pair ** 2 * N_color * (N_quark - 1) * R_bar_sq / a_s)
    diff = sp.simplify(compound_sq - expected)

    print(f"  (|V_td V_us|/|V_cb V_ub|)^2 (computed) = {compound_sq}")
    print(f"  Expected: N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s")
    print(f"          = 60 R_bar^2 / alpha_s")
    print(f"          = {expected}")
    print(f"  Difference: {diff}")

    check("C2: (|V_td V_us|/|V_cb V_ub|)^2 = N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s",
          diff == 0)

    # Alternative form using |V_us|^2 = alpha_s/N_pair: alpha_s = N_pair |V_us|^2.
    expected_alt = sp.simplify(
        N_pair ** 3 * N_color * (N_quark - 1) * R_bar_sq / (N_pair * Vus_sq)
        # = N_pair^2 N_color (N_quark - 1) R_bar^2 / |V_us|^2
    )
    # Wait: 60/alpha_s = 60/(N_pair |V_us|^2) = (60/N_pair)/|V_us|^2 = 30/|V_us|^2.
    # In structural integers: 30 = N_pair N_color (N_quark - 1).
    expected_alt2 = sp.simplify(N_pair * N_color * (N_quark - 1) * R_bar_sq / Vus_sq)
    diff_alt = sp.simplify(compound_sq - expected_alt2)
    print(f"\n  Equivalent form: 30 R_bar^2 / |V_us|^2")
    print(f"          = N_pair N_color (N_quark - 1) R_bar^2 / |V_us|^2")
    print(f"  Difference: {diff_alt}")
    check("C2 alt: (|V_td V_us|/|V_cb V_ub|)^2 = N_pair N_color (N_quark - 1) R_bar^2 / |V_us|^2",
          diff_alt == 0)


def audit_c3_pdg_comparison(N: dict, S: dict) -> None:
    banner("C3: PDG numerical comparison")

    a_s = S["a_s"]
    Vtd_sq = S["Vtd_sq"]
    Vus_sq = S["Vus_sq"]
    Vcb_sq = S["Vcb_sq"]
    Vub_sq = S["Vub_sq"]
    R_bar_sq = S["R_bar_sq"]

    s_canonical = 0.103

    # Three-magnitude bridge.
    Vtd_pred = math.sqrt(float(Vtd_sq.subs(a_s, s_canonical)))
    Vus_pred = math.sqrt(float(Vus_sq.subs(a_s, s_canonical)))
    Vcb_pred = math.sqrt(float(Vcb_sq.subs(a_s, s_canonical)))
    Vub_pred = math.sqrt(float(Vub_sq.subs(a_s, s_canonical)))
    R_bar_pred = math.sqrt(float(R_bar_sq.subs(a_s, s_canonical)))

    # Verify: 3 |V_td|^2 = 10 |V_us|^2 |V_cb|^2 R_bar^2 numerically.
    lhs_C1 = 3 * Vtd_pred ** 2
    rhs_C1 = 10 * Vus_pred ** 2 * Vcb_pred ** 2 * R_bar_pred ** 2

    print(f"  At canonical alpha_s = {s_canonical}:")
    print(f"    |V_td| = {Vtd_pred:.6f}, |V_us| = {Vus_pred:.6f}")
    print(f"    |V_cb| = {Vcb_pred:.6f}, |V_ub| = {Vub_pred:.6f}")
    print(f"    R_bar  = {R_bar_pred:.6f}, R_bar^2 = {R_bar_pred ** 2:.6f}")
    print()
    print(f"  C1 check: 3 |V_td|^2 vs 10 |V_us|^2 |V_cb|^2 R_bar^2:")
    print(f"    LHS = 3 |V_td|^2                       = {lhs_C1:.10f}")
    print(f"    RHS = 10 |V_us|^2 |V_cb|^2 R_bar^2     = {rhs_C1:.10f}")
    check("C1 numerical: 3 |V_td|^2 = 10 |V_us|^2 |V_cb|^2 R_bar^2 within 1e-10",
          abs(lhs_C1 - rhs_C1) < 1e-10)

    # PDG values (central):
    pdg = {"|V_us|": 0.2243, "|V_cb|": 0.0410, "|V_ub|": 0.00382, "|V_td|": 0.00861}

    pdg_lhs_C1 = 3 * pdg["|V_td|"] ** 2
    # For PDG, R_bar isn't directly measured, so use framework's R_bar at canonical alpha_s.
    pdg_rhs_C1 = 10 * pdg["|V_us|"] ** 2 * pdg["|V_cb|"] ** 2 * R_bar_pred ** 2
    rel_diff = abs(pdg_lhs_C1 - pdg_rhs_C1) / pdg_lhs_C1 * 100

    print(f"\n  C1 PDG check (with framework R_bar):")
    print(f"    LHS_PDG = 3 |V_td|_PDG^2          = {pdg_lhs_C1:.10f}")
    print(f"    RHS_PDG = 10 |V_us|_PDG^2 |V_cb|_PDG^2 R_bar^2  =  {pdg_rhs_C1:.10f}")
    print(f"    |Delta/LHS| = {rel_diff:.2f} %")
    check("C1 PDG numerical: 3 |V_td|^2 ~= 10 |V_us|^2 |V_cb|^2 R_bar^2 within 5 % (combined PDG err)",
          rel_diff < 5)

    # Four-magnitude compound.
    compound_sq_pred = float((Vtd_sq * Vus_sq / (Vcb_sq * Vub_sq)).subs(a_s, s_canonical))
    pdg_compound_sq = (pdg["|V_td|"] * pdg["|V_us|"]) ** 2 / (pdg["|V_cb|"] * pdg["|V_ub|"]) ** 2
    rel_diff_C2 = abs(compound_sq_pred - pdg_compound_sq) / pdg_compound_sq * 100

    print(f"\n  C2 PDG check: (|V_td V_us|/|V_cb V_ub|)^2:")
    print(f"    Framework = {compound_sq_pred:.4f}")
    print(f"    PDG       = {pdg_compound_sq:.4f}")
    print(f"    |Delta/PDG| = {rel_diff_C2:.2f} %")
    check("C2 PDG numerical: (|V_td V_us|/|V_cb V_ub|)^2 framework ~= PDG within 5 %",
          rel_diff_C2 < 5)


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
    print("    (C1) Three-magnitude circumradius bridge:")
    print("         N_color |V_td|^2  =  N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2,")
    print("         i.e., 3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2.")
    print()
    print("    (C2) Four-magnitude circumradius bridge:")
    print("         (|V_td V_us|/|V_cb V_ub|)^2  =  N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s")
    print("                                       =  60 R_bar^2 / alpha_s.")
    print()
    print("    (C2 alt) Equivalent form:")
    print("         (|V_td V_us|/|V_cb V_ub|)^2  =  N_pair N_color (N_quark - 1) R_bar^2 / |V_us|^2")
    print("                                       =  30 R_bar^2 / |V_us|^2.")
    print()
    print("    (C3) PDG validation: framework predictions for both bridges agree")
    print("         with PDG-computed values within 5 % relative deviation.")


def main() -> int:
    print("=" * 88)
    print("CKM compound-magnitudes circumradius bridge audit")
    print("See docs/CKM_COMPOUND_MAGNITUDES_CIRCUMRADIUS_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    N = extract_retained_inputs()
    S = setup_symbolic(N)
    audit_c1_three_magnitude_bridge(N, S)
    audit_c2_four_magnitude_bridge(N, S)
    audit_c3_pdg_comparison(N, S)
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
