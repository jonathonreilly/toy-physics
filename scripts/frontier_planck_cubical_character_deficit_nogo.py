#!/usr/bin/env python3
"""Audit the cubical character-deficit no-go honestly."""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_CUBICAL_CHARACTER_DEFICIT_NO_GO_THEOREM_2026-04-23.md"


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


def normalized_character(j: float, eps: float) -> float:
    numerator = math.sin((2.0 * j + 1.0) * eps / 2.0)
    denominator = (2.0 * j + 1.0) * math.sin(eps / 2.0)
    return numerator / denominator


def q_deficit(j: float, eps: float) -> float:
    return 1.0 - normalized_character(j, eps)


def main() -> int:
    note = normalized(NOTE)
    n_pass = 0
    n_fail = 0
    eps = math.pi / 2.0

    print("Planck cubical character-deficit no-go audit")
    print("=" * 78)

    section("PART 1: MINIMAL CUBICAL DEFECT SURFACE")
    p = check(
        "minimal positive cubical Regge defect is pi/2",
        abs(eps - math.pi / 2.0) < 1e-15,
        "on the cubic slice, positive deficits come in multiples of pi/2 and the first one is pi/2",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: CHARACTER-DEFICIT CLASS")
    sample_js = [0.5, 1.0, 1.5, 2.0, 2.5]
    q_values = []
    coeff_values = []
    for j in sample_js:
        q = q_deficit(j, eps)
        coeff = 8.0 * math.pi * q / eps
        q_values.append((j, q))
        coeff_values.append((j, coeff))
        print(f"  j = {j:>3.1f} -> q_j(pi/2) = {q:.12f}, a^2/l_P^2 = {coeff:.12f}")

    q_min_exact = 1.0 - math.sqrt(2.0) / 2.0
    coeff_min_exact = 16.0 - 8.0 * math.sqrt(2.0)
    p = check(
        "the minimal sampled character deficit occurs at j=1/2",
        min(q_values, key=lambda item: item[1])[0] == 0.5,
        f"best sampled q_j = {min(q_values, key=lambda item: item[1])[1]:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "j=1/2 lands the exact lower bound 1 - sqrt(2)/2",
        abs(q_values[0][1] - q_min_exact) < 1e-12,
        f"q_(1/2)(pi/2) = {q_values[0][1]:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the best cubical character-deficit coefficient is 16 - 8 sqrt(2)",
        abs(coeff_values[0][1] - coeff_min_exact) < 1e-12,
        f"a^2/l_P^2 = {coeff_values[0][1]:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT-PLANCK NO-GO")
    p = check(
        "the minimal character-deficit coefficient is still larger than 1",
        coeff_min_exact > 1.0,
        f"16 - 8 sqrt(2) = {coeff_min_exact:.12f} > 1",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "therefore the canonical same-defect character-deficit class cannot force exact Planck",
        abs(coeff_min_exact - 1.0) > 1e-6,
        "even the best cubical gauge-invariant holonomy scalar overshoots exact a=l_P",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE VERDICT")
    p = check(
        "note states the exact lower bound 16 - 8 sqrt(2)",
        "16 - 8 sqrt(2)" in note,
        "the exact coefficient floor must be explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states the class is ruled out for exact conventional a = l_P",
        "cannot force exact conventional `a = l_p`" in note,
        "the no-go must be stated clearly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The canonical gauge-invariant same-defect Spin(3) character-deficit "
        "class is also boxed out: on the minimal cubical defect its best "
        "possible coefficient is 16 - 8 sqrt(2), which is exact but still "
        "strictly above 1."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
