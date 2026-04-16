#!/usr/bin/env python3
"""
Taste-scalar cubic target for the baryogenesis lane.

This runner converts the finite-T reduction gap into an explicit one-loop
scalar-cubic target relation for any 2HDM-like taste-scalar completion.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0


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


V = 246.282818290129
G1_GUT_V = 0.464376
G2_V = 0.648031
VT_TARGET = 0.52
MH_2L = 119.77
MH_3L = 125.10


def gauge_cubic() -> float:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    return (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)


def route_values(m_h: float) -> dict[str, float]:
    lam = m_h * m_h / (2.0 * V * V)
    e_g = gauge_cubic()
    e_req = VT_TARGET * lam / 2.0
    delta_e = e_req - e_g
    scalar_target = 12.0 * math.pi * delta_e

    # One extra complex SU(2) doublet = 4 real bosonic degrees of freedom.
    n_doublet = 4.0
    kappa_doublet = 2.0 * (scalar_target / n_doublet) ** (2.0 / 3.0)

    e_from_higgs_quartic_doublet = n_doublet / (12.0 * math.pi) * (lam / 2.0) ** 1.5
    frac_from_higgs_quartic = e_from_higgs_quartic_doublet / delta_e
    n_required_at_higgs_quartic = scalar_target / ((lam / 2.0) ** 1.5)

    return {
        "lambda": lam,
        "E_gauge": e_g,
        "E_required": e_req,
        "delta_E": delta_e,
        "scalar_target": scalar_target,
        "kappa_doublet": kappa_doublet,
        "quartic_fraction": frac_from_higgs_quartic,
        "n_required_at_lambda": n_required_at_higgs_quartic,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    m_H                        = {m_h:.2f} GeV")
    print(f"    lambda_H                   = {values['lambda']:.6f}")
    print(f"    E_gauge                    = {values['E_gauge']:.6f}")
    print(f"    E_required(0.52)           = {values['E_required']:.6f}")
    print(f"    delta_E                    = {values['delta_E']:.6f}")
    print(f"    scalar target 12pi*delta_E = {values['scalar_target']:.6f}")
    print(f"    kappa for one extra doublet = {values['kappa_doublet']:.6f}")
    print(f"    quartic-scale fraction      = {values['quartic_fraction']:.3%}")
    print(f"    n required at kappa=lambda  = {values['n_required_at_lambda']:.3f}")
    print()

    check(
        f"{label} requires positive extra scalar cubic strength",
        values["delta_E"] > 0.0,
        f"delta_E = {values['delta_E']:.6f}",
    )
    check(
        f"{label} scalar-cubic target is O(1)",
        0.75 < values["scalar_target"] < 0.95,
        f"12pi*delta_E = {values['scalar_target']:.6f}",
    )
    check(
        f"{label} one-extra-doublet interpretation needs order-1 portal",
        0.6 < values["kappa_doublet"] < 0.8,
        f"kappa = {values['kappa_doublet']:.6f}",
    )
    check(
        f"{label} Higgs-quartic-scale coupling cannot carry the route by itself",
        values["quartic_fraction"] < 0.10,
        f"fraction = {values['quartic_fraction']:.3%}",
    )
    check(
        f"{label} multiplicity-only rescue at kappa=lambda is implausibly large",
        values["n_required_at_lambda"] > 50.0,
        f"n_required = {values['n_required_at_lambda']:.3f}",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS TASTE-SCALAR CUBIC TARGET")
    print("=" * 80)
    print()
    print("Question:")
    print("  If the old taste-scalar EWPT route is real, what exact extra")
    print("  one-loop scalar cubic coefficient must it supply?")
    print()

    print("=" * 80)
    print("PART 1: MISSING CUBIC STRENGTH")
    print("=" * 80)
    print()
    info(
        "imported scalar-cubic ansatz",
        "for m_s^2(phi) = (kappa/2) phi^2, one-loop high-T reduction gives E_s = n_s/(12pi) * (kappa/2)^(3/2)",
    )
    print()

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 2: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    closure_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    reduction_note = (DOCS / "BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md").read_text(encoding="utf-8")
    cubic_note = (DOCS / "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "closure-gate note points to the taste-scalar cubic target",
        "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md" in closure_note,
    )
    check(
        "finite-T reduction note points to the taste-scalar cubic target",
        "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md" in reduction_note,
    )
    check(
        "cubic target note records the one-extra-doublet portal window",
        "κ ~= 0.69 - 0.74" in cubic_note and "0.685" in cubic_note and "0.744" in cubic_note,
    )
    check(
        "derivation atlas carries the taste-scalar cubic target row",
        "Baryogenesis taste-scalar cubic target" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the missing finite-T enhancement can be written as an exact")
    print("      scalar-cubic target relation")
    print("    - the old 2HDM-like route only works if the extra taste-scalar")
    print("      sector supplies an order-1 portal, kappa ≈ 0.69-0.74")
    print("    - a Higgs-quartic-scale scalar coupling is far too small")
    print("    - thermal screening would make the required portal larger, not")
    print("      smaller")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
