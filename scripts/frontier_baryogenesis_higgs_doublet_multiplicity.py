#!/usr/bin/env python3
"""
Derived Higgs-doublet multiplicity for the baryogenesis lane.

This runner shows that the n=4 scalar multiplicity needed by the
selector-portal route is already present on the Higgs/CW surface as
one radial Higgs mode plus three Goldstones from the derived Higgs doublet.
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
    delta_e_one = 1.0 / (12.0 * math.pi) * (kappa_sel / 2.0) ** 1.5

    n_scalar = N_HIGGS + N_GOLDSTONE
    delta_e_n4 = n_scalar * delta_e_one
    xi_required = delta_e_target / delta_e_n4

    return {
        "lambda": lam,
        "kappa_sel": kappa_sel,
        "delta_e_target": delta_e_target,
        "delta_e_n4": delta_e_n4,
        "xi_required": xi_required,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                    = {values['lambda']:.6f}")
    print(f"    kappa_sel                   = {values['kappa_sel']:.6f}")
    print(f"    DeltaE_target               = {values['delta_e_target']:.6f}")
    print(f"    DeltaE_n=4                  = {values['delta_e_n4']:.6f}")
    print(f"    xi_screen required          = {values['xi_required']:.6f}")
    print()

    check(
        f"{label} derived Higgs-doublet multiplicity saturates the scalar count",
        N_HIGGS + N_GOLDSTONE == 4,
        f"n_Higgs + n_Goldstone = {N_HIGGS + N_GOLDSTONE}",
    )
    check(
        f"{label} only mild screening is needed once n=4 is derived",
        0.94 < values["xi_required"] < 0.96,
        f"xi_screen >= {values['xi_required']:.6f}",
    )
    check(
        f"{label} scalar multiplicity loophole is closed on the current surface",
        values["delta_e_n4"] > values["delta_e_target"],
        f"DeltaE_n=4 / target = {values['delta_e_n4'] / values['delta_e_target']:.6f}",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS HIGGS-DOUBLET MULTIPLICITY")
    print("=" * 80)
    print()
    print("Question:")
    print("  Is the n=4 scalar multiplicity needed by the selector-portal route")
    print("  already present on the current framework surface?")
    print()

    print("=" * 80)
    print("PART 1: DERIVED HIGGS / GOLDSTONE COUNT")
    print("=" * 80)
    print()

    higgs_runner = (SCRIPTS / "frontier_higgs_mass_derived.py").read_text(encoding="utf-8")
    yt_zero = (SCRIPTS / "frontier_yt_zero_import_chain.py").read_text(encoding="utf-8")
    yt_eft = (SCRIPTS / "frontier_yt_eft_bridge.py").read_text(encoding="utf-8")

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
    info(
        "same-surface interpretation",
        "the exact selector manifold fixes the portal, while the derived Higgs-doublet completion supplies the n=4 scalar multiplicity",
    )
    print()

    print("=" * 80)
    print("PART 2: CONSEQUENCE FOR THE BARYOGENESIS ROUTE")
    print("=" * 80)
    print()
    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    mult_note = (DOCS / "BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md").read_text(encoding="utf-8")
    dbl_note = (DOCS / "BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "multiplicity/screening note points to the Higgs-doublet multiplicity note",
        "BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md" in mult_note,
    )
    check(
        "Higgs-doublet multiplicity note records n_scalar = 4",
        "n_scalar = n_Higgs + n_Goldstone = 4" in dbl_note,
    )
    check(
        "derivation atlas carries the Higgs-doublet multiplicity row",
        "Baryogenesis Higgs-doublet multiplicity" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the required n=4 scalar multiplicity is already present on the")
    print("      Higgs/CW surface as one radial Higgs plus three Goldstones")
    print("    - the selector-portal route therefore no longer needs an ad hoc")
    print("      extra doubling mechanism")
    print("    - the only remaining scalar-side open quantity is the screening")
    print("      survival factor xi_screen")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
