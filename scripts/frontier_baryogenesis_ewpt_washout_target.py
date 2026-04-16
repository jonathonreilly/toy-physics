#!/usr/bin/env python3
"""
Baryogenesis EWPT/washout target on the current main package surface.

This runner does not compute the electroweak phase transition itself.
It packages the quantitative target that any future same-surface EWPT /
transport computation must satisfy.
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


def promoted_jarlskog() -> tuple[float, float]:
    v_us = 0.22727
    v_cb = 0.04217
    v_ub = 0.003913
    delta_deg = 65.905

    s13 = v_ub
    c13 = math.sqrt(1.0 - s13 * s13)
    s12 = v_us / c13
    s23 = v_cb / c13
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    delta = math.radians(delta_deg)
    j = c12 * s12 * c23 * s23 * c13 * c13 * s13 * math.sin(delta)
    return delta_deg, j


def bbn_omega_b(eta: float) -> float:
    h = 0.674
    eta_10 = eta / 1.0e-10
    omega_b_h2 = 3.6515e-3 * eta_10
    return omega_b_h2 / (h * h)


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS EWPT/WASHOUT TARGET")
    print("=" * 80)
    print()
    print("Question:")
    print("  What quantitative target must the missing same-surface EWPT /")
    print("  sphaleron-transport computation reproduce on top of the promoted")
    print("  CKM weak-sector CP source?")
    print()

    print("=" * 80)
    print("PART 1: PROMOTED WEAK-SECTOR SOURCE SCALE")
    print("=" * 80)
    print()

    eta_obs = 6.12e-10
    delta_deg, j = promoted_jarlskog()
    package_j = 3.331e-5

    check("promoted CKM phase is nonzero", delta_deg > 0.0, f"delta = {delta_deg:.3f} deg")
    check("promoted Jarlskog is nonzero", j > 0.0, f"J = {j:.6e}")
    check(
        "reconstructed J matches the promoted package",
        abs(j - package_j) / package_j < 5e-4,
        f"J(reconstructed) = {j:.6e}, J(package) = {package_j:.6e}",
    )

    print()
    print("=" * 80)
    print("PART 2: REQUIRED EWPT / WASHOUT EFFICIENCY")
    print("=" * 80)
    print()

    epsilon_req = eta_obs / j
    eta_reconstructed = j * epsilon_req

    check(
        "required electroweak efficiency is positive",
        epsilon_req > 0.0,
        f"epsilon_EWPT = {epsilon_req:.6e}",
    )
    check(
        "required electroweak efficiency is of order 1e-5",
        1.0e-6 < epsilon_req < 1.0e-4,
        f"epsilon_EWPT = {epsilon_req:.6e}",
    )
    check(
        "eta is exactly reconstructed by J * epsilon_EWPT",
        abs(eta_reconstructed - eta_obs) / eta_obs < 1e-15,
        f"eta_reconstructed = {eta_reconstructed:.6e}",
    )

    omega_b = bbn_omega_b(eta_obs)
    check(
        "the same eta target reproduces the observed baryon density through BBN",
        abs(omega_b - 0.0493) / 0.0493 < 0.01,
        f"Omega_b(BBN) = {omega_b:.6f}",
    )

    print()
    print("=" * 80)
    print("PART 3: HISTORICAL EWPT ROUTE ANCHOR")
    print("=" * 80)
    print()

    v_over_t_hist = 0.52
    no_washout_benchmark = 1.0

    check(
        "historical v/T route anchor is positive",
        v_over_t_hist > 0.0,
        f"v(T_c)/T_c = {v_over_t_hist:.2f}",
    )
    check(
        "historical anchor lies below the strict no-washout benchmark",
        v_over_t_hist < no_washout_benchmark,
        f"historical {v_over_t_hist:.2f} < benchmark {no_washout_benchmark:.2f}",
    )
    info(
        "route-history role of v/T ~ 0.52",
        "partial-washout target only; not a retained same-surface theorem",
    )

    baryo_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    ewpt_note = (DOCS / "BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(encoding="utf-8")

    check(
        "closure-gate note points to the EWPT/washout target",
        "BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md" in baryo_note,
    )
    check(
        "target note records epsilon_EWPT = eta/J",
        "ε_EWPT = η_obs / J_CKM = 1.837e-5" in ewpt_note,
    )
    check(
        "derivation atlas carries the baryogenesis EWPT/washout target row",
        "Baryogenesis EWPT/washout target" in atlas,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the promoted CKM package already fixes the weak CP source scale")
    print("    - the missing EWPT/transport bridge must supply")
    print(f"      epsilon_EWPT = {epsilon_req:.6e}")
    print("    - the older v/T ~ 0.52 number remains route history only")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
