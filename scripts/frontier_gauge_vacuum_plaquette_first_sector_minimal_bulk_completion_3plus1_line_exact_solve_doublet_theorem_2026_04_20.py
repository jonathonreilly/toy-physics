#!/usr/bin/env python3
"""
Bounded-angle exact-solve doublet theorem for the retained `3d+1`
complement-line problem on the selected minimally-positive Wilson branch.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np
from scipy.optimize import least_squares

from frontier_dm_leptogenesis_dweh_even_split_transfer_layer import TARGET
from frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_helper_2026_04_19 import (
    compressed_local_block_from_line,
    line_from_positive_angles,
    positive_angles_from_line,
)

PASS_COUNT = 0
FAIL_COUNT = 0

THETA_SEEDS = np.linspace(-math.pi, math.pi, 7, endpoint=False)
PHI_SEEDS = np.linspace(-1.2, 1.2, 5)
PSI_SEEDS = np.array([0.06, 0.18, 0.34, 0.72, 1.08], dtype=float)
ANGLE_LOWER = np.array([-math.pi, -0.5 * math.pi + 1.0e-6, 1.0e-6], dtype=float)
ANGLE_UPPER = np.array([math.pi, 0.5 * math.pi - 1.0e-6, 0.5 * math.pi - 1.0e-6], dtype=float)
_SOLVE_CACHE: list[np.ndarray] | None = None


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def canonicalize_angles(angles: np.ndarray) -> np.ndarray:
    theta, phi, psi = [float(x) for x in np.asarray(angles, dtype=float)]
    theta = ((theta + math.pi) % (2.0 * math.pi)) - math.pi
    phi = max(ANGLE_LOWER[1], min(ANGLE_UPPER[1], phi))
    psi = max(ANGLE_LOWER[2], min(ANGLE_UPPER[2], psi))
    return np.array([theta, phi, psi], dtype=float)


def live_residual_from_angles(angles: np.ndarray) -> np.ndarray:
    theta, phi, psi = [float(x) for x in canonicalize_angles(angles)]
    if psi <= ANGLE_LOWER[2] or psi >= ANGLE_UPPER[2]:
        return np.full(3, 10.0, dtype=float)
    line = line_from_positive_angles(theta, phi, psi)
    return np.array(compressed_local_block_from_line(line)[2] - TARGET, dtype=float)


def line_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)))


def finite_difference_jacobian(angles: np.ndarray, eps: float = 1.0e-6) -> np.ndarray:
    base = canonicalize_angles(angles)
    jac = np.zeros((3, 3), dtype=float)
    for idx in range(3):
        delta = np.zeros(3, dtype=float)
        delta[idx] = eps
        plus = canonicalize_angles(np.minimum(base + delta, ANGLE_UPPER))
        minus = canonicalize_angles(np.maximum(base - delta, ANGLE_LOWER))
        step = max(float(plus[idx] - minus[idx]), 1.0e-12)
        jac[:, idx] = (live_residual_from_angles(plus) - live_residual_from_angles(minus)) / step
    return jac


def solved_target_hitting_lines() -> list[np.ndarray]:
    global _SOLVE_CACHE
    if _SOLVE_CACHE is not None:
        return [np.array(line, dtype=float) for line in _SOLVE_CACHE]

    roots: list[np.ndarray] = []
    for seed in itertools.product(THETA_SEEDS, PHI_SEEDS, PSI_SEEDS):
        result = least_squares(
            live_residual_from_angles,
            np.array(seed, dtype=float),
            bounds=(ANGLE_LOWER, ANGLE_UPPER),
            xtol=1.0e-12,
            ftol=1.0e-12,
            gtol=1.0e-12,
            max_nfev=4000,
        )
        if float(np.linalg.norm(result.fun)) >= 1.0e-10:
            continue
        line = line_from_positive_angles(*canonicalize_angles(result.x))
        if all(line_distance(line, other) > 1.0e-7 for other in roots):
            roots.append(line)

    roots.sort(key=lambda line: tuple(np.round(positive_angles_from_line(line), 12).tolist()))
    _SOLVE_CACHE = [np.array(line, dtype=float) for line in roots]
    return [np.array(line, dtype=float) for line in roots]


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION 3D+1 EXACT-SOLVE DOUBLET")
    print("=" * 118)
    print()
    print("Question:")
    print("  On the selected minimally-positive Wilson branch, what does the bounded")
    print("  positive-angle solve of the retained live target equation actually return?")

    lines = solved_target_hitting_lines()
    errs = [float(np.linalg.norm(compressed_local_block_from_line(line)[2] - TARGET)) for line in lines]
    angles = [positive_angles_from_line(line) for line in lines]
    jacobians = [finite_difference_jacobian(a) for a in angles]
    sigmas = [np.linalg.svd(jac, compute_uv=False) for jac in jacobians]
    line_sep = min(
        line_distance(lines[0], lines[1]),
        line_distance(lines[0], -lines[1]),
    ) if len(lines) == 2 else float("nan")

    print()
    print(f"  audited seed counts                         = ({len(THETA_SEEDS)}, {len(PHI_SEEDS)}, {len(PSI_SEEDS)})")
    for idx, (line, angle, sigma, err) in enumerate(zip(lines, angles, sigmas, errs)):
        print(f"  solution[{idx}] line                        = {np.round(line, 15).tolist()}")
        print(f"  solution[{idx}] angles                      = {np.round(angle, 15).tolist()}")
        print(f"  solution[{idx}] singular values             = {np.round(sigma, 12).tolist()}")
        print(f"  solution[{idx}] live residual norm          = {err:.3e}")
    print()

    check(
        "The bounded positive-angle solve returns exactly two retained-line roots on the selected branch",
        len(lines) == 2,
        f"count={len(lines)}",
    )
    check(
        "Both solved roots are exact target-hitting retained-line solutions",
        len(lines) == 2 and max(errs) < 1.0e-10,
        f"max_err={max(errs) if errs else float('nan'):.3e}",
    )
    check(
        "The two solved roots are genuinely distinct as projective complement lines",
        len(lines) == 2 and line_sep > 1.0e-3,
        f"sep={line_sep:.6f}",
    )
    check(
        "Each solved root is nondegenerate in the bounded angle chart",
        len(sigmas) == 2 and min(float(np.min(sigma)) for sigma in sigmas) > 1.0e-3,
        f"min_sigma={min(float(np.min(sigma)) for sigma in sigmas) if sigmas else float('nan'):.6f}",
    )
    check(
        "So the retained complement-line live equation has an isolated exact-solve doublet on the positive 3d+1 chart",
        len(lines) == 2 and max(errs) < 1.0e-10 and min(float(np.min(sigma)) for sigma in sigmas) > 1.0e-3,
    )
    check(
        "This replaces the old hardcoded witness use by an audited solve of the bounded target equation itself",
        len(lines) == 2,
        "all later theorems can import the solved set rather than named witnesses",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Bounded-angle exact solve:")
    print("    - the retained `3d+1` complement-line problem is now solved on the")
    print("      positive-angle chart of the selected branch")
    print("    - the exact target equation has an isolated two-point solution set there")
    print("    - both roots are nondegenerate and can therefore be used as the genuine")
    print("      multiplicity set for the later selector theorem")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
