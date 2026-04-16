#!/usr/bin/env python3
"""
Current-surface no-go for the old taste-scalar baryogenesis route.

This runner does not claim an axiom-level impossibility theorem.
Its statement is narrower and current-package exact:

  - the present authority surface derives exactly one Higgs doublet
  - the scalar-spectrum matching boundary shows that this one-doublet
    package contributes only about 41% of the old target before screening
  - earlier baryogenesis notes explicitly do not derive an extra
    taste-scalar doublet on the authority path

Therefore the old 2HDM-like taste-scalar EWPT route is not a live same-surface
route on current `main`. Reviving it would require genuinely new derived
finite-T bosonic structure or new thermal dynamics beyond the old ansatz.
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

    required_product = delta_e_target / delta_e_sel_one
    selector_equiv = delta_e_doublet / delta_e_sel_one
    coverage = delta_e_doublet / delta_e_target
    extra_equiv_needed = required_product - selector_equiv

    return {
        "lambda": lam,
        "required_product": required_product,
        "selector_equiv": selector_equiv,
        "coverage": coverage,
        "extra_equiv_needed": extra_equiv_needed,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                        = {values['lambda']:.6f}")
    print(f"    target selector-equiv strength = {values['required_product']:.6f}")
    print(f"    one-doublet selector-equiv     = {values['selector_equiv']:.6f}")
    print(f"    coverage of old target         = {values['coverage']:.6f}")
    print(f"    extra selector-equiv needed    = {values['extra_equiv_needed']:.6f}")
    print()

    check(
        f"{label} current one-doublet package is strictly weaker than the old target",
        values["selector_equiv"] < values["required_product"],
        f"{values['selector_equiv']:.6f} < {values['required_product']:.6f}",
    )
    check(
        f"{label} old route fails even before screening",
        values["coverage"] < 0.43,
        f"coverage = {values['coverage']:.6f}",
    )
    check(
        f"{label} reviving the old route would need more than two extra selector-equiv units",
        values["extra_equiv_needed"] > 2.1,
        f"extra needed = {values['extra_equiv_needed']:.6f}",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS OLD-ROUTE CURRENT-SURFACE NO-GO")
    print("=" * 80)
    print()
    print("Question:")
    print("  Is the old 2HDM-like taste-scalar EWPT route still a live")
    print("  same-surface route on the current package?")
    print()

    print("=" * 80)
    print("PART 1: CURRENT AUTHORITY SURFACE")
    print("=" * 80)
    print()

    yt_eft = (SCRIPTS / "frontier_yt_eft_bridge.py").read_text(encoding="utf-8")
    yt_zero = (SCRIPTS / "frontier_yt_zero_import_chain.py").read_text(encoding="utf-8")
    higgs_runner = (SCRIPTS / "frontier_higgs_mass_derived.py").read_text(encoding="utf-8")
    cubic_target_note = (DOCS / "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md").read_text(encoding="utf-8")
    matching_note = (DOCS / "BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md").read_text(encoding="utf-8")

    check(
        "EW/Yukawa bridge derives exactly one Higgs doublet",
        "N_H = 1" in yt_eft and "Higgs doublet from G_5 condensate" in yt_eft,
    )
    check(
        "zero-import Yukawa chain keeps the same one-doublet count",
        "N_H = 1" in yt_zero and "Higgs doublets (G_5 condensate)" in yt_zero,
    )
    check(
        "current scalar content on the Higgs/CW surface is 1 radial + 3 Goldstones",
        "N_HIGGS = 1" in higgs_runner and "N_GOLDSTONE = 3" in higgs_runner,
    )
    check(
        "current baryogenesis cubic-target note explicitly does not derive an extra doublet",
        "that an extra taste-scalar doublet is already derived on the authority path" in cubic_target_note,
    )
    check(
        "matching-boundary note records that the old n=4 reuse is not derived",
        "is not framework-derived" in matching_note,
    )
    info(
        "surface meaning",
        "the present package derives one Higgs doublet and does not currently derive a second same-surface taste-scalar doublet",
    )
    print()

    print("=" * 80)
    print("PART 2: CONSEQUENCE FOR THE OLD ROUTE")
    print("=" * 80)
    print()
    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    no_go_note = (DOCS / "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md").read_text(encoding="utf-8")
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    target_note = (DOCS / "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md").read_text(encoding="utf-8")
    mult_note = (DOCS / "BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")

    check(
        "no-go note states the old route is not live on current main",
        "old route is dead **on the present surface**" in no_go_note,
    )
    check(
        "closure-gate note points to the current-surface no-go",
        "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md" in gate_note,
    )
    check(
        "cubic-target note points to the current-surface no-go",
        "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md" in target_note,
    )
    check(
        "multiplicity/screening note points to the current-surface no-go",
        "BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md" in mult_note,
    )
    check(
        "derivation atlas carries the old-route no-go row",
        "Baryogenesis old-route current-surface no-go" in atlas,
    )
    check(
        "canonical harness index includes the old-route no-go runner",
        "frontier_baryogenesis_old_route_surface_no_go.py" in harness,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the current authority surface derives exactly one Higgs")
    print("      doublet, not a 2HDM-like scalar sector")
    print("    - the matched one-doublet scalar package reaches only about 41%")
    print("      of the old target before screening")
    print("    - so the old taste-scalar EWPT route is not a live same-surface")
    print("      route on current main")
    print("    - reviving it would require genuinely new derived finite-T")
    print("      bosonic structure or new thermal dynamics beyond the old ansatz")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
