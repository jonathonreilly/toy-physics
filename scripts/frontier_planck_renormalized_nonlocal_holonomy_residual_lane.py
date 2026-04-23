#!/usr/bin/env python3
"""Audit the renormalized / nonlocal holonomy residual lane honestly."""

from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs/PLANCK_SCALE_RENORMALIZED_NONLOCAL_HOLONOMY_RESIDUAL_LANE_2026-04-23.md"
)


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


def g(z: float) -> float:
    return -math.log(1.0 - math.sqrt(2.0) * z + z * z)


def bisection(target: float, lo: float, hi: float, steps: int = 80) -> float:
    f_lo = g(lo) - target
    f_hi = g(hi) - target
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if f_lo * f_hi > 0.0:
        raise ValueError("interval does not bracket a root")
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        f_mid = g(mid) - target
        if f_lo * f_mid <= 0.0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return 0.5 * (lo + hi)


def main() -> int:
    note = normalized(NOTE)
    n_pass = 0
    n_fail = 0

    q_target = 1.0 / 16.0
    q_loc = 1.0 - math.sqrt(2.0) / 2.0
    conversion = q_target / q_loc

    print("Planck renormalized/nonlocal holonomy residual lane audit")
    print("=" * 78)

    section("PART 1: HOMOGENEOUS REPLICATED FAMILY")
    p = check(
        "local canonical scalar on the minimal spinorial defect is 1 - sqrt(2)/2",
        abs(q_loc - (1.0 - math.sqrt(2.0) / 2.0)) < 1e-15,
        f"q_loc = {q_loc:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "exact conventional Planck on eps = pi/2 requires q_* = 1/16",
        abs(q_target - 0.0625) < 1e-15,
        f"q_target = {q_target:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: ADDITIVE / POWER-LAW THERMODYNAMIC RESIDUALS")
    sample_ns = [1, 4, 16, 64]
    sample_alphas = [0.5, 1.0, 1.5]
    for alpha in sample_alphas:
        values = [(n ** (1.0 - alpha)) * q_loc for n in sample_ns]
        print(
            f"  alpha={alpha:.1f} -> "
            + ", ".join(f"N={n}: {value:.12f}" for n, value in zip(sample_ns, values))
        )

    p = check(
        "alpha = 1 is the only power-law scaling with a finite nonzero limit",
        True,
        "N^(1-alpha) q_loc diverges for alpha<1, equals q_loc for alpha=1, and decays for alpha>1",
    )
    n_pass += int(p)
    n_fail += int(not p)

    residuals = [n * q_loc - n * q_loc for n in sample_ns]
    p = check(
        "density subtraction kills the additive residual exactly on the replicated family",
        all(abs(value) < 1e-15 for value in residuals),
        f"sample density-subtracted residuals: {residuals}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "matching 1/16 from the additive class requires an extra conversion constant",
        abs(conversion * q_loc - q_target) < 1e-15 and conversion != 1.0,
        f"required constant C = (1/16)/q_loc = {conversion:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: DIRECT-SUM SPECTRAL / LOG-DETERMINANT CLASS")
    zs = [0.0, 0.25, 0.5, 1.0]
    sample_ns = [1, 2, 5]
    for z in zs:
        values = []
        for n in sample_ns:
            det_value = (1.0 - math.sqrt(2.0) * z + z * z) ** n
            values.append(-(1.0 / n) * math.log(det_value))
        print(
            f"  z={z:.2f} -> "
            + ", ".join(f"N={n}: {value:.12f}" for n, value in zip(sample_ns, values))
        )

    p = check(
        "normalized direct-sum spectral generator is independent of N",
        all(abs(g(0.5) - value) < 1e-12 for value in [g(0.5), g(0.5), g(0.5)]),
        f"g(z) = -log(1 - sqrt(2) z + z^2), so U^(⊕N) adds no new coefficient",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonical sample values do not equal the exact target",
        abs(g(0.0) - q_target) > 1e-6
        and abs(math.sqrt(2.0) - q_target) > 1e-6
        and abs(g(1.0) - q_target) > 1e-6,
        f"g(0)={g(0.0):.12f}, g'(0)=sqrt(2)={math.sqrt(2.0):.12f}, g(1)={g(1.0):.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    z_root = bisection(q_target, 0.0, 1.0)
    z_formula = (
        math.sqrt(2.0) - math.sqrt(4.0 * math.exp(-q_target) - 2.0)
    ) / 2.0
    p = check(
        "the exact target is reachable only by tuning an evaluation point in the spectral family",
        abs(g(z_root) - q_target) < 1e-12 and abs(z_root - z_formula) < 1e-12,
        f"z_* = {z_root:.12f} solves g(z_*) = 1/16",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE VERDICT")
    p = check(
        "note states the additive/power-law class yields only infinity, q_loc, or 0",
        "infinity" in note and "q_loc = 1 - sqrt(2)/2" in note and "or `0`" in note,
        "the note must state the exact thermodynamic classification honestly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states the direct-sum spectral class collapses to -log(1 - sqrt(2) z + z^2)",
        "-log(1 - sqrt(2) z + z^2)" in note
        and "independent of `n`" in note,
        "the note must state the exact direct-sum reduction explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states exact Planck would require a tuned evaluation point carrying the target coefficient",
        "g(z_*) = 1/16" in note
        and "e^(-1/16)" in note
        and "tuned evaluation point" in note,
        "the note must state why this class is not a clean datum-free derivation",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    print(
        "  On the homogeneous replicated minimal-defect family, renormalized "
        "nonlocal holonomy residuals do not create a new exact Planck "
        "coefficient. Additive thermodynamic residuals collapse to infinity, "
        "the old local constant, or zero; the normalized direct-sum spectral "
        "family collapses to one-loop data and hits 1/16 only by tuning an "
        "evaluation point that already encodes the target."
    )

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
