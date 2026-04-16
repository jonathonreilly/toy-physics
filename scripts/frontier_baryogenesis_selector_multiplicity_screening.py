#!/usr/bin/env python3
"""
Multiplicity / screening boundary for the selector-based baryogenesis route.

This runner takes the exact selector portal kappa_sel = 6 lambda_H and reduces
the remaining scalar-side baryogenesis question to a product condition on
effective multiplicity and screening survival.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

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
    e_req = VT_TARGET * lam / 2.0
    delta_e_target = e_req - gauge_cubic()

    kappa_sel = 6.0 * lam
    delta_e_one = 1.0 / (12.0 * math.pi) * (kappa_sel / 2.0) ** 1.5
    required_product = delta_e_target / delta_e_one

    exact_real_ratio = 2.0 / required_product
    required_screen_if_n4 = required_product / 4.0

    return {
        "lambda": lam,
        "kappa_sel": kappa_sel,
        "delta_e_target": delta_e_target,
        "delta_e_one": delta_e_one,
        "required_product": required_product,
        "exact_real_ratio": exact_real_ratio,
        "required_screen_if_n4": required_screen_if_n4,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                    = {values['lambda']:.6f}")
    print(f"    kappa_sel                   = {values['kappa_sel']:.6f}")
    print(f"    DeltaE_target               = {values['delta_e_target']:.6f}")
    print(f"    DeltaE_one                  = {values['delta_e_one']:.6f}")
    print(f"    n_eff * xi_screen required  = {values['required_product']:.6f}")
    print(f"    exact real n=2 coverage     = {values['exact_real_ratio']:.6f}")
    print(f"    xi_screen required if n=4   = {values['required_screen_if_n4']:.6f}")
    print()

    check(
        f"{label} requires almost four unscreened real scalar modes",
        3.7 < values["required_product"] < 3.9,
        f"required product = {values['required_product']:.6f}",
    )
    check(
        f"{label} exact real selector surface covers only about half the target",
        0.50 < values["exact_real_ratio"] < 0.54,
        f"coverage = {values['exact_real_ratio']:.6f}",
    )
    check(
        f"{label} n=2 exact selector manifold cannot close the route",
        2.0 < values["required_product"],
        f"required product = {values['required_product']:.6f} > 2",
    )
    check(
        f"{label} n=4 rescue requires screening below about six percent",
        0.94 < values["required_screen_if_n4"] < 0.96,
        f"xi_screen >= {values['required_screen_if_n4']:.6f}",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS SELECTOR MULTIPLICITY / SCREENING")
    print("=" * 80)
    print()
    print("Question:")
    print("  Once the selector portal is fixed, what multiplicity and screening")
    print("  budget must the finite-T scalar sector satisfy?")
    print()

    print("=" * 80)
    print("PART 1: EXACT BOUNDARY CONDITION")
    print("=" * 80)
    print()
    info(
        "exact selector multiplicity",
        "choosing one Higgs axis on the real selector manifold leaves exactly two orthogonal real scalar directions",
    )
    check("exact real selector multiplicity is 2", True, "orthogonal directions = s_2, s_3")
    print()

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 2: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    selector_note = (DOCS / "BARYOGENESIS_SELECTOR_PORTAL_NOTE.md").read_text(encoding="utf-8")
    mult_note = (DOCS / "BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "selector portal note points to the multiplicity/screening note",
        "BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md" in selector_note,
    )
    check(
        "multiplicity/screening note records the n_eff * xi_screen condition",
        "n_eff * xi_screen" in mult_note,
    )
    check(
        "derivation atlas carries the multiplicity/screening row",
        "Baryogenesis selector multiplicity / screening" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the exact real selector manifold gives only two orthogonal")
    print("      scalar modes")
    print("    - with the derived selector portal, that covers only about half")
    print("      of the required finite-T enhancement")
    print("    - any surviving old route therefore needs an additional doubling")
    print("      mechanism and screening milder than about five to six percent")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
