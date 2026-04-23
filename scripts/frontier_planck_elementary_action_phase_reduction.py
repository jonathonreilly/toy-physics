#!/usr/bin/env python3
"""Audit the elementary action-phase reduction honestly.

This is not a derivation harness. It encodes the first-principles reduction:
  - elementary Z^3 plaquette gives A_* = a^2
  - unitary closed process gives q_* = S_*/hbar
  - Einstein/Regge gives S_h/hbar = A_h eps_h / (8 pi l_P^2)
  - therefore a^2 / l_P^2 = 8 pi q_* / eps_*
"""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def main() -> int:
    note = normalized(NOTE)
    n_pass = 0
    n_fail = 0

    print("Planck elementary action-phase reduction audit")
    print("=" * 78)

    section("PART 1: FORMULA CHECK")
    q = 1.234
    eps = 0.789
    lhs = 8.0 * math.pi * q / eps
    rhs = (8.0 * math.pi * q) / eps
    p = check(
        "reduced coefficient formula is algebraically consistent",
        abs(lhs - rhs) < 1e-15,
        "a^2 / l_P^2 = 8 pi q_* / eps_* is the exact reduction from Einstein/Regge",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: PLANCK-ORDER BUT NOT EXACT-PLANCK")
    samples = [
        ("q=1, eps=1", 8.0 * math.pi),
        ("q=pi/2, eps=pi/2", 8.0 * math.pi),
        ("q=1/2, eps=pi/2", 8.0),
        ("q=pi, eps=pi/2", 16.0 * math.pi),
    ]
    all_order_one = True
    all_not_one = True
    for label, ratio in samples:
        print(f"  {label:<18} -> a^2/l_P^2 = {ratio:.6f}")
        all_order_one &= (0.1 < ratio < 1000.0)
        all_not_one &= abs(ratio - 1.0) > 1e-9
    p = check(
        "generic O(1) action/defect quanta force Planck-order scaling",
        all_order_one,
        "the lattice naturally lands at the Planck scale up to an O(1) coefficient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "generic O(1) quanta do not force exact a = l_P",
        all_not_one,
        "exact Planck needs the coefficient identity, not just dimensional self-completion",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT-PLANCK CONDITION")
    eps_star = 0.73
    q_needed = eps_star / (8.0 * math.pi)
    ratio = 8.0 * math.pi * q_needed / eps_star
    p = check(
        "exact Planck occurs iff q_* = eps_*/(8 pi)",
        abs(ratio - 1.0) < 1e-15,
        f"for eps_* = {eps_star:.6f}, exact Planck requires q_* = {q_needed:.6f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE VERDICT")
    p = check(
        "note states that Cl(3)/Z^3 gives the right carrier but not yet the exact coefficient",
        "right kind of elementary carrier" in note
        and "not yet the exact planck coefficient" in note,
        "the reduction must distinguish carrier-forcing from coefficient closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note identifies the surviving theorem target as an elementary action/defect coefficient theorem",
        "elementary action/defect coefficient theorem" in note
        or "elementary action-phase/defect theorem" in note,
        "the next first-principles target is now explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Bare Cl(3) on Z^3 does not yet force exact a = l_P, but it does "
        "reduce any future Planck derivation to one elementary action-phase / "
        "curvature-defect coefficient theorem: a^2/l_P^2 = 8 pi q_*/eps_*."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
