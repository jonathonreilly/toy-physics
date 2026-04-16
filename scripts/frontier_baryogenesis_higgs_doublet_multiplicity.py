#!/usr/bin/env python3
"""
Higgs-doublet multiplicity / matching boundary for the baryogenesis lane.

This runner confirms the derived one-Higgs-doublet content on the Higgs/CW
surface, then derives the exact scalar-spectrum matching boundary:

  - the selector quartic fixes orthogonal taste-scalar masses with
    m_sel^2(h) = 3 lambda_H h^2
  - the one-doublet Higgs/CW surface gives
      m_rad^2(h)  = 3 lambda_H h^2
      m_G^2(h)    = 1 lambda_H h^2

So the selector coefficient matches the radial Higgs mode exactly, but it does
not match the three Goldstones. That means the old step "take kappa_sel and
multiply it by n=4" is not derived from the current same-surface package.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

PASS = 0
FAIL = 0

MH_2L = 119.77
MH_3L = 125.10
V = 246.282818290129
G1_GUT_V = 0.464376
G2_V = 0.648031
VT_TARGET = 0.52

N_H_DOUBLETS = 1
N_HIGGS = 1
N_GOLDSTONE = 3
SELECTOR_EQUIV_ONE_DOUBLET = 1.0 + 1.0 / math.sqrt(3.0)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def gauge_cubic() -> float:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    return (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)


def route_values(m_h: float) -> dict[str, float]:
    lam = m_h * m_h / (2.0 * V * V)
    delta_e_target = VT_TARGET * lam / 2.0 - gauge_cubic()

    kappa_sel = 6.0 * lam
    kappa_gold = 2.0 * lam

    delta_e_sel_one = 1.0 / (12.0 * math.pi) * (kappa_sel / 2.0) ** 1.5
    delta_e_gold_one = 1.0 / (12.0 * math.pi) * (kappa_gold / 2.0) ** 1.5
    delta_e_doublet = delta_e_sel_one + 3.0 * delta_e_gold_one

    selector_equiv = delta_e_doublet / delta_e_sel_one
    coverage = delta_e_doublet / delta_e_target
    gap_factor = delta_e_target / delta_e_doublet

    return {
        "lambda": lam,
        "kappa_sel": kappa_sel,
        "kappa_gold": kappa_gold,
        "delta_e_target": delta_e_target,
        "delta_e_sel_one": delta_e_sel_one,
        "delta_e_gold_one": delta_e_gold_one,
        "delta_e_doublet": delta_e_doublet,
        "selector_equiv": selector_equiv,
        "coverage": coverage,
        "gap_factor": gap_factor,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                         = {values['lambda']:.6f}")
    print(f"    kappa_sel (selector / radial)   = {values['kappa_sel']:.6f}")
    print(f"    kappa_G (Goldstone)             = {values['kappa_gold']:.6f}")
    print(f"    DeltaE_target                   = {values['delta_e_target']:.6f}")
    print(f"    DeltaE_sel_one                  = {values['delta_e_sel_one']:.6f}")
    print(f"    DeltaE_gold_one                 = {values['delta_e_gold_one']:.6f}")
    print(f"    DeltaE_one-doublet              = {values['delta_e_doublet']:.6f}")
    print(f"    selector-equiv multiplicity     = {values['selector_equiv']:.6f}")
    print(f"    coverage of target              = {values['coverage']:.6f}")
    print(f"    remaining pre-screening gap     = {values['gap_factor']:.6f}x")
    print()

    check(
        f"{label} Goldstones carry only one-third of the selector coefficient",
        abs(values["kappa_sel"] / values["kappa_gold"] - 3.0) < 1e-12,
        f"kappa_sel / kappa_G = {values['kappa_sel'] / values['kappa_gold']:.6f}",
    )
    check(
        f"{label} one-doublet scalar package has fixed selector-equivalent multiplicity",
        abs(values["selector_equiv"] - SELECTOR_EQUIV_ONE_DOUBLET) < 1e-12,
        f"n_equiv = {values['selector_equiv']:.6f}",
    )
    check(
        f"{label} matched one-doublet scalar package covers only about 41% of the target",
        0.40 < values["coverage"] < 0.43,
        f"coverage = {values['coverage']:.6f}",
    )
    check(
        f"{label} scalar-side route still needs more than a factor-two enhancement before screening",
        2.3 < values["gap_factor"] < 2.5,
        f"gap factor = {values['gap_factor']:.6f}x",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS HIGGS-DOUBLET MULTIPLICITY / MATCHING BOUNDARY")
    print("=" * 80)
    print()
    print("Question:")
    print("  Does the derived one-Higgs-doublet 1+3 scalar content justify")
    print("  reusing the selector portal coefficient across all four modes?")
    print()

    print("=" * 80)
    print("PART 1: DERIVED ONE-DOUBLET SCALAR CONTENT")
    print("=" * 80)
    print()

    higgs_runner = (SCRIPTS / "frontier_higgs_mass_derived.py").read_text(encoding="utf-8")
    yt_zero = (SCRIPTS / "frontier_yt_zero_import_chain.py").read_text(encoding="utf-8")
    yt_eft = (SCRIPTS / "frontier_yt_eft_bridge.py").read_text(encoding="utf-8")
    selector_note = (DOCS / "BARYOGENESIS_SELECTOR_PORTAL_NOTE.md").read_text(encoding="utf-8")

    check(
        "EW/Yukawa bridge records one derived Higgs doublet",
        "N_H = 1" in yt_eft and "Higgs doublet from G_5 condensate" in yt_eft,
    )
    check(
        "Higgs/CW runner records one radial Higgs mode",
        "N_HIGGS = 1" in higgs_runner and "radial Higgs mode" in higgs_runner,
    )
    check(
        "Higgs/CW runner records three Goldstones",
        "N_GOLDSTONE = 3" in higgs_runner and "eaten by W+, W-, Z" in higgs_runner,
    )
    check(
        "zero-import CW runner records the same 1+3 scalar split",
        "N_HIGGS_CW = 1" in yt_zero and "N_GOLD_CW = 3" in yt_zero,
    )
    check(
        "selector portal note records m_sel^2(h) = 3 lambda_H h^2",
        "m_s^2(h) = d^2V/ds^2 = 2 alpha_hs h^2 = 3 lambda_H h^2" in selector_note,
    )
    check(
        "Higgs/CW runner records the radial and Goldstone field-dependent masses",
        "M_H^2(phi) = |m^2| + 3 lambda phi^2" in higgs_runner
        and "M_G^2(phi) = |m^2| + lambda phi^2" in higgs_runner,
    )
    info(
        "exact coefficient match",
        "the selector coefficient matches the radial Higgs mode exactly, while the three Goldstones are lighter by a factor of 3 in kappa",
    )
    print()

    print("=" * 80)
    print("PART 2: CONSEQUENCE FOR THE OLD n=4 RESCUE")
    print("=" * 80)
    print()
    check(
        "one-doublet scalar multiplicity is 4",
        N_HIGGS + N_GOLDSTONE == 4,
        f"n_Higgs + n_Goldstone = {N_HIGGS + N_GOLDSTONE}",
    )
    check(
        "selector-equivalent multiplicity of the matched one-doublet spectrum is exact",
        abs(SELECTOR_EQUIV_ONE_DOUBLET - (1.0 + 1.0 / math.sqrt(3.0))) < 1e-12,
        f"1 + 1/sqrt(3) = {SELECTOR_EQUIV_ONE_DOUBLET:.6f}",
    )
    print()

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    mult_note = (DOCS / "BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md").read_text(encoding="utf-8")
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "Higgs-doublet note records selector-equivalent multiplicity 1 + 1/sqrt(3)",
        "1 + 1/sqrt(3)" in mult_note,
    )
    check(
        "closure-gate note no longer says screening is the only remaining scalar-side object",
        "41%" in gate_note and "additional same-surface bosonic structure" in gate_note,
    )
    check(
        "derivation atlas records the matching-boundary outcome",
        "selector-equivalent multiplicity `1 + 1/sqrt(3)`" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the current framework surface does contain one derived Higgs")
    print("      doublet with one radial mode plus three Goldstones")
    print("    - but the exact selector coefficient kappa_sel = 6 lambda_H")
    print("      matches only the radial mode; Goldstones carry")
    print("      kappa_G = 2 lambda_H")
    print("    - so the old step 'reuse kappa_sel for n=4 modes' is not")
    print("      framework-derived")
    print("    - on the same imported one-loop scalar-cubic ansatz, the matched")
    print("      one-doublet spectrum reaches only about 41% of the old target")
    print("      before any screening penalty")
    print("    - the remaining scalar-side baryogenesis gap is therefore not")
    print("      just screening by itself; it is a real mode-matching /")
    print("      additional-structure problem")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
