#!/usr/bin/env python3
"""Audit the finite-order Cl(3) spinor-phase no-go honestly."""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_CL3_SPINOR_PHASE_QUANTUM_NO_GO_THEOREM_2026-04-23.md"


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

    print("Planck Cl(3) spinor-phase quantum no-go audit")
    print("=" * 78)

    section("PART 1: CUBIC ROTATION HALF-ANGLES")
    so3_angles = [math.pi, 2.0 * math.pi / 3.0, math.pi / 2.0]
    spinor_quanta = [a / 2.0 for a in so3_angles]
    q_min = min(spinor_quanta)
    for theta, q in zip(so3_angles, spinor_quanta):
        print(f"  theta = {theta:.6f}  ->  q = theta/2 = {q:.6f}")
    p = check(
        "smallest nonzero cubic spinorial phase quantum is pi/4",
        abs(q_min - math.pi / 4.0) < 1e-15,
        f"q_min = {q_min:.6f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT-PLANCK REQUIREMENT")
    eps_values = [0.1, 1.0, math.pi, 1.99 * math.pi]
    upper_bounds_ok = True
    for eps in eps_values:
        q_req = eps / (8.0 * math.pi)
        print(f"  eps = {eps:.6f}  ->  q_required = eps/(8pi) = {q_req:.6f}")
        upper_bounds_ok &= (0.0 < q_req < 0.25)
    p = check(
        "local positive hinge defects require q_* < 1/4 for exact Planck",
        upper_bounds_ok,
        "because exact a=l_P implies q_* = eps_*/(8pi) and 0 < eps_* < 2pi",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: NO-GO INEQUALITY")
    p = check(
        "pi/4 is strictly larger than 1/4",
        (math.pi / 4.0) > 0.25,
        f"pi/4 = {math.pi/4.0:.6f} > 0.25",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "therefore finite-order cubic spinorial holonomy cannot force exact Planck",
        q_min > 0.25,
        "the smallest available nonzero cubic spinor-phase quantum already violates the exact coefficient bound",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE VERDICT")
    p = check(
        "note states the finite-order cubic holonomy route is dead",
        "naive finite-order cubic spinorial-holonomy route cannot close the planck coefficient" in note,
        "the note must state the no-go clearly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note preserves narrower surviving action-phase possibilities",
        "what survives is narrower" in note and "non-finite-order" in note,
        "this is a route reduction, not a universal spinorial no-go",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Finite-order cubic Cl(3) spinorial holonomy alone cannot deliver "
        "exact a=l_P. Any surviving action-quantum theorem must use something "
        "subtler than the smallest nonzero cubic spinor phase."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
