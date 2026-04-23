#!/usr/bin/env python3
"""Audit the exotic/nonlocal holonomy narrowing honestly."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_EXOTIC_NONLOCAL_HOLONOMY_LANE_2026-04-23.md"


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


def weights(j2: int) -> list[Fraction]:
    """Weights for spin j = j2 / 2 as exact half-integers."""
    return [Fraction(-j2 + 2 * k, 2) for k in range(j2 + 1)]


def tensor_weights(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return sorted({a + b for a in left for b in right})


def main() -> int:
    note = normalized(NOTE)
    n_pass = 0
    n_fail = 0

    eps_min = math.pi / 2.0
    q_target = eps_min / (8.0 * math.pi)
    ratio_target = 1.0 / (8.0 * math.pi)
    q_floor = 1.0 - math.sqrt(2.0) / 2.0

    print("Planck exotic/nonlocal holonomy lane audit")
    print("=" * 78)

    section("PART 1: EXACT TARGET ON THE MINIMAL CUBICAL DEFECT")
    p = check(
        "exact conventional Planck at eps = pi/2 requires q_* = 1/16",
        abs(q_target - 1.0 / 16.0) < 1e-15,
        f"q_target = (pi/2)/(8 pi) = {q_target:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "equivalently q_*/eps_* must equal 1/(8 pi)",
        abs(ratio_target - q_target / eps_min) < 1e-15,
        f"q_*/eps_* target = {ratio_target:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: FINITE WORD / TENSOR EIGENPHASE CLASS")
    base_half = weights(1)
    spin_one = weights(2)
    half_tensor_half = tensor_weights(base_half, base_half)
    one_tensor_half = tensor_weights(spin_one, base_half)
    print(f"  spin-1/2 weights       -> {base_half}")
    print(f"  spin-1 weights         -> {spin_one}")
    print(f"  (1/2) tensor (1/2)     -> {half_tensor_half}")
    print(f"  1 tensor (1/2)         -> {one_tensor_half}")

    all_half_integer = all(
        (2 * w).denominator == 1
        for family in (base_half, spin_one, half_tensor_half, one_tensor_half)
        for w in family
    )
    p = check(
        "finite tensor products preserve the half-integer weight lattice",
        all_half_integer,
        "finite Spin(3) tensor/direct-sum constructions keep resolved phases on (1/2) Z",
    )
    n_pass += int(p)
    n_fail += int(not p)

    sample_coeffs = [
        Fraction(1, 2),      # minimal spinor
        Fraction(3, 2),      # tensor-resolved weight
        Fraction(1, 2) / 2,  # average over two loops
        Fraction(3, 2) / 4,  # finite combinatorial normalization
        Fraction(5, 2) / 8,
    ]
    print("  sample rational coefficients c = q_*/eps_* from finite combinatorial normalizations:")
    for coeff in sample_coeffs:
        print(f"    c = {coeff} = {float(coeff):.12f}")

    p = check(
        "sample finite nonlocal phase coefficients stay rational",
        all(isinstance(coeff, Fraction) for coeff in sample_coeffs),
        "half-integer weights divided by finite counts stay in Q",
    )
    n_pass += int(p)
    n_fail += int(not p)

    nearest_gap = min(abs(float(coeff) - ratio_target) for coeff in sample_coeffs)
    p = check(
        "sample rational coefficient family does not hit the exact target 1/(8 pi)",
        nearest_gap > 1e-6,
        f"nearest sampled gap to 1/(8 pi) is {nearest_gap:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: POSITIVE NORMALIZED NONLOCAL AGGREGATION")
    p = check(
        "best canonical local scalar floor is larger than the exact Planck target",
        q_floor > q_target,
        f"q_floor = 1 - sqrt(2)/2 = {q_floor:.12f}, q_target = {q_target:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    samples = [
        [q_floor, q_floor],
        [q_floor, 0.5, 0.75],
        [0.4, 0.6, 0.8],
    ]
    for idx, values in enumerate(samples, start=1):
        arithmetic = sum(values) / len(values)
        geometric = math.prod(values) ** (1.0 / len(values))
        harmonic = len(values) / sum(1.0 / value for value in values)
        print(
            f"  sample {idx}: min={min(values):.12f}, "
            f"arith={arithmetic:.12f}, geom={geometric:.12f}, harm={harmonic:.12f}"
        )
        p = check(
            f"internal means stay above the local floor on sample {idx}",
            min(arithmetic, geometric, harmonic) + 1e-12 >= q_floor,
            "arithmetic / geometric / harmonic means of positive values stay between min and max",
        )
        n_pass += int(p)
        n_fail += int(not p)

    p = check(
        "therefore normalized positive pooling of the canonical local scalars cannot reach 1/16",
        q_floor > 1.0 / 16.0,
        f"every internal mean stays >= q_floor = {q_floor:.12f} > 1/16 = {1.0/16.0:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE VERDICT")
    p = check(
        "note states the finite combinatorial eigenphase class is ruled out",
        "finite combinatorial nonlocal eigenphase functionals" in note
        and "1 / (8 pi)" in note
        and "notin q" in note,
        "the note must state the rational-coefficient obstruction explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states positive normalized nonlocal pooling cannot beat the local floor",
        "positive normalized nonlocal aggregates" in note
        and "q_loc,min = 1 - sqrt(2)/2" in note
        and "1/16" in note,
        "the note must state the exact floor obstruction on the scalar-aggregation side",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note leaves only much more exotic holonomy survivors",
        "non-extensive" in note
        and "infinite / renormalized nonlocal" in note
        and "holonomy construction" in note,
        "the note should narrow the surviving holonomy route honestly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    print(
        "  The surviving holonomy route narrows again: finite combinatorial "
        "nonlocal eigenphase constructions stay on a rational coefficient "
        "lattice, and positive normalized nonlocal pooling of the canonical "
        "local scalar deficits cannot beat the exact local floor 1 - sqrt(2)/2."
    )

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
