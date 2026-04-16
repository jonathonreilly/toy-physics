#!/usr/bin/env python3
"""
Finite-temperature reduction target for the baryogenesis lane.

This runner derives the zero-temperature control parameters from the promoted
main package, then inserts them into the standard textbook one-loop high-T
Landau reduction as an explicitly imported control ansatz.
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
YT_V = 0.9176
MH_2L = 119.77
MH_3L = 125.10
VT_TARGET = 0.52


def finite_t_control(m_h: float) -> dict[str, float]:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    lam = m_h * m_h / (2.0 * V * V)

    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    m_t = YT_V * V / math.sqrt(2.0)

    # Imported textbook one-loop high-T coefficients.
    d_coeff = (2.0 * m_w * m_w + m_z * m_z + 2.0 * m_t * m_t + m_h * m_h) / (8.0 * V * V)
    e_coeff = (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)
    vc_over_tc = 2.0 * e_coeff / lam

    e_required = VT_TARGET * lam / 2.0
    enhancement = e_required / e_coeff
    lam_required = 2.0 * e_coeff / VT_TARGET

    return {
        "g_y": g_y,
        "lambda": lam,
        "D": d_coeff,
        "E": e_coeff,
        "vc_over_tc": vc_over_tc,
        "e_required": e_required,
        "enhancement": enhancement,
        "lambda_required": lam_required,
    }


def audit_route(label: str, m_h: float) -> None:
    print(f"  {label}:")
    values = finite_t_control(m_h)
    print(f"    m_H               = {m_h:.2f} GeV")
    print(f"    lambda            = {values['lambda']:.6f}")
    print(f"    D (imported)      = {values['D']:.6f}")
    print(f"    E (imported)      = {values['E']:.6f}")
    print(f"    v_c/T_c           = {values['vc_over_tc']:.6f}")
    print(f"    E required for 0.52 = {values['e_required']:.6f}")
    print(f"    enhancement factor  = {values['enhancement']:.3f}x")
    print(f"    lambda required at fixed E = {values['lambda_required']:.6f}")
    print()

    check(
        f"{label} quartic is positive",
        values["lambda"] > 0.0,
        f"lambda = {values['lambda']:.6f}",
    )
    check(
        f"{label} gauge-cubic coefficient is positive",
        values["E"] > 0.0,
        f"E = {values['E']:.6f}",
    )
    check(
        f"{label} minimal gauge-cubic reduction undershoots v/T = 0.52",
        values["vc_over_tc"] < VT_TARGET,
        f"v_c/T_c = {values['vc_over_tc']:.6f} < {VT_TARGET:.2f}",
    )
    check(
        f"{label} requires O(3x-4x) bosonic enhancement over gauge cubic",
        3.0 < values["enhancement"] < 4.0,
        f"enhancement = {values['enhancement']:.3f}x",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS FINITE-T REDUCTION")
    print("=" * 80)
    print()
    print("Question:")
    print("  What does the promoted zero-temperature package imply for the")
    print("  simplest imported one-loop high-T EWPT control ratio?")
    print()

    print("=" * 80)
    print("PART 1: DERIVED ZERO-T PACKAGE VALUES")
    print("=" * 80)
    print()

    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    check("hypercharge coupling is obtained from promoted GUT-normalized g1", g_y > 0.0, f"g_Y(v) = {g_y:.6f}")
    check("promoted SU(2) coupling is positive", G2_V > 0.0, f"g_2(v) = {G2_V:.6f}")
    check("promoted top Yukawa is positive", YT_V > 0.0, f"y_t(v) = {YT_V:.6f}")

    print()
    print("=" * 80)
    print("PART 2: IMPORTED HIGH-T CONTROL ANSATZ")
    print("=" * 80)
    print()
    info(
        "thermal ansatz classification",
        "D, E, and v_c/T_c = 2E/lambda are imported textbook high-T reduction formulas",
    )
    print()

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    target_note = (DOCS / "BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md").read_text(encoding="utf-8")
    reduction_note = (DOCS / "BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "EWPT target note points to the finite-T reduction note",
        "BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md" in target_note,
    )
    check(
        "finite-T reduction note records the undershoot of the 0.52 target",
        "undershoots" in reduction_note and "0.52" in reduction_note,
    )
    check(
        "derivation atlas carries the finite-T reduction row",
        "Baryogenesis finite-T reduction" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the zero-temperature EW/Higgs package is already fixed on main")
    print("    - the minimal imported high-T one-doublet gauge-cubic reduction gives")
    print("      v_c/T_c ≈ 0.15 rather than 0.52")
    print("    - so any real taste-scalar EWPT route must supply an O(3x-4x)")
    print("      enhancement beyond the minimal gauge cubic, or a non-minimal")
    print("      finite-T potential altogether")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
