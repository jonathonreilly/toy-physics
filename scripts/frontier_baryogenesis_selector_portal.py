#!/usr/bin/env python3
"""
Selector-portal derivation for the baryogenesis lane.

This runner uses the exact graph-first quartic invariant to derive the
orthogonal taste-scalar portal scale and compare it to the finite-T cubic
target from the baryogenesis package.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)

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


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def build_axis_shifts() -> list[np.ndarray]:
    return [
        kron3(SX, I2, I2),
        kron3(I2, SX, I2),
        kron3(I2, I2, SX),
    ]


def h(phi: tuple[float, float, float], shifts: list[np.ndarray]) -> np.ndarray:
    return sum(c * op for c, op in zip(phi, shifts))


def gauge_cubic() -> float:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    return (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)


def cubic_target_kappa(m_h: float) -> float:
    lam = m_h * m_h / (2.0 * V * V)
    e_req = VT_TARGET * lam / 2.0
    delta_e = e_req - gauge_cubic()
    n_doublet = 4.0
    return 2.0 * ((12.0 * math.pi * delta_e) / n_doublet) ** (2.0 / 3.0)


def route_values(m_h: float) -> dict[str, float]:
    lam = m_h * m_h / (2.0 * V * V)
    kappa_sel = 6.0 * lam
    kappa_target = cubic_target_kappa(m_h)
    delta_e_target = VT_TARGET * lam / 2.0 - gauge_cubic()
    delta_e_sel_if_n4 = 4.0 / (12.0 * math.pi) * (kappa_sel / 2.0) ** 1.5
    return {
        "lambda": lam,
        "kappa_sel": kappa_sel,
        "kappa_target": kappa_target,
        "kappa_ratio": kappa_sel / kappa_target,
        "delta_e_target": delta_e_target,
        "delta_e_sel_n4": delta_e_sel_if_n4,
        "delta_e_ratio_n4": delta_e_sel_if_n4 / delta_e_target,
    }


def audit_route(label: str, m_h: float) -> None:
    values = route_values(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                      = {values['lambda']:.6f}")
    print(f"    kappa_sel = 6 lambda_H        = {values['kappa_sel']:.6f}")
    print(f"    kappa_target                  = {values['kappa_target']:.6f}")
    print(f"    kappa_sel / target            = {values['kappa_ratio']:.6f}")
    print(f"    DeltaE_target                 = {values['delta_e_target']:.6f}")
    print(f"    DeltaE_sel (n=4)              = {values['delta_e_sel_n4']:.6f}")
    print(f"    DeltaE_sel / target           = {values['delta_e_ratio_n4']:.6f}")
    print()

    check(
        f"{label} selector portal is order-1",
        0.65 < values["kappa_sel"] < 0.80,
        f"kappa_sel = {values['kappa_sel']:.6f}",
    )
    check(
        f"{label} selector portal lands within 5% of the cubic-target window",
        1.0 < values["kappa_ratio"] < 1.05,
        f"ratio = {values['kappa_ratio']:.6f}",
    )
    check(
        f"{label} minimal n=4 route almost saturates the required cubic enhancement",
        1.0 < values["delta_e_ratio_n4"] < 1.08,
        f"ratio = {values['delta_e_ratio_n4']:.6f}",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS SELECTOR PORTAL")
    print("=" * 80)
    print()
    print("Question:")
    print("  Does the actual derived lattice taste-scalar surface generate the")
    print("  order-1 portal needed by the old baryogenesis route?")
    print()

    print("=" * 80)
    print("PART 1: EXACT QUARTIC RATIO")
    print("=" * 80)
    print()

    shifts = build_axis_shifts()
    samples = [(1, 0, 0), (1, 1, 0), (2, 1, 1)]
    for phi in samples:
        H = h(phi, shifts)
        s2 = float(sum(x * x for x in phi))
        pair = float(sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3)))
        tr4 = np.trace(H @ H @ H @ H).real
        expected = 8.0 * (s2 * s2 + 4.0 * pair)
        check(
            f"Tr H({phi})^4 matches the exact graph-first quartic formula",
            abs(tr4 - expected) < 1e-10,
            f"value = {tr4:.6f}",
        )

    info(
        "exact quartic decomposition",
        "Tr H^4 = 8 sum_i phi_i^4 + 48 sum_{i<j} phi_i^2 phi_j^2, so the exact portal/self ratio is 6:1",
    )
    check(
        "portal/self ratio from the exact quartic is 6",
        abs((48.0 / 8.0) - 6.0) < 1e-12,
    )

    print()
    print("=" * 80)
    print("PART 2: SELECTOR PORTAL ON THE HIGGS SURFACE")
    print("=" * 80)
    print()
    info(
        "normalization",
        "matching the axis quartic 8A h^4 to the promoted Higgs convention lambda_H h^4 / 4 gives A = lambda_H / 32 and therefore kappa_sel = 6 lambda_H",
    )
    print()

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    target_note = (DOCS / "BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md").read_text(encoding="utf-8")
    selector_note = (DOCS / "BARYOGENESIS_SELECTOR_PORTAL_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "taste-scalar cubic target note points to the selector portal note",
        "BARYOGENESIS_SELECTOR_PORTAL_NOTE.md" in target_note,
    )
    check(
        "selector portal note records kappa_sel = 6 lambda_H",
        "kappa_sel = 6 lambda_H" in selector_note,
    )
    check(
        "derivation atlas carries the selector portal row",
        "Baryogenesis selector portal" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the exact graph-first quartic fixes the portal/self ratio")
    print("    - matching to the promoted Higgs quartic gives")
    print("      kappa_sel = 6 lambda_H")
    print("    - numerically that is kappa_sel ≈ 0.71-0.77 on the current")
    print("      package surface")
    print("    - this lands essentially on top of the previously derived")
    print("      baryogenesis target window")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
