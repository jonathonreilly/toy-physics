#!/usr/bin/env python3
"""
Frontier runner - asymptotic pure-source no-go for additional DM PMNS basins.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np
from scipy.optimize import minimize

from frontier_sigma_hier_uniqueness_theorem import T_M, T_DELTA, T_Q


PASS = 0
FAIL = 0

TARGET_S12SQ = 0.307
TARGET_S13SQ = 0.0218
TARGET_S23SQ = 0.545


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {label}" + (f"  ({detail})" if detail else ""))


def standard_pmns(delta_cp: float) -> np.ndarray:
    s12 = math.sqrt(TARGET_S12SQ)
    c12 = math.sqrt(1.0 - TARGET_S12SQ)
    s13 = math.sqrt(TARGET_S13SQ)
    c13 = math.sqrt(1.0 - TARGET_S13SQ)
    s23 = math.sqrt(TARGET_S23SQ)
    c23 = math.sqrt(1.0 - TARGET_S23SQ)
    e = complex(math.cos(delta_cp), math.sin(delta_cp))
    em = complex(math.cos(-delta_cp), math.sin(-delta_cp))
    return np.array(
        [
            [c12 * c13, s12 * c13, s13 * em],
            [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
            [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13],
        ],
        dtype=complex,
    ).real


def family_constraints(mat: np.ndarray) -> np.ndarray:
    return np.array(
        [
            mat[1, 1] + mat[2, 2],
            mat[0, 2] - mat[0, 1] - 2.0 * mat[1, 1],
            2.0 * mat[0, 0] - 2.0 * mat[1, 2] + mat[0, 1] + mat[0, 2],
        ],
        dtype=float,
    )


def asymptotic_observables(point: tuple[float, float, float], perm: tuple[int, int, int]) -> tuple[float, float, float]:
    h = point[0] * T_M + point[1] * T_DELTA + point[2] * T_Q
    w, v = np.linalg.eigh(h)
    order = np.argsort(np.real(w))
    v = v[:, order]
    p = v[list(perm), :]
    s13sq = abs(p[0, 2]) ** 2
    c13sq = max(1.0 - s13sq, 1e-18)
    s12sq = abs(p[0, 1]) ** 2 / c13sq
    s23sq = abs(p[1, 2]) ** 2 / c13sq
    return s12sq, s13sq, s23sq


def asymptotic_chi2(point: tuple[float, float, float], perm: tuple[int, int, int]) -> float:
    s12sq, s13sq, s23sq = asymptotic_observables(point, perm)
    return (
        (s12sq - TARGET_S12SQ) ** 2
        + (s13sq - TARGET_S13SQ) ** 2
        + (s23sq - TARGET_S23SQ) ** 2
    )


def main() -> int:
    print("=== Part 1: linear-algebra no-go at infinity ===")
    for delta_cp in (0.0, math.pi):
        u0 = standard_pmns(delta_cp)
        for perm in itertools.permutations(range(3)):
            u = u0[list(perm), :]
            a = np.column_stack(
                [family_constraints(np.outer(u[:, i], u[:, i])) for i in range(3)]
            )
            svals = np.linalg.svd(a, compute_uv=False)
            check(
                f"({perm}, delta_CP={delta_cp / math.pi:.0f} pi): constraint matrix has full rank",
                np.linalg.matrix_rank(a, tol=1e-10) == 3,
                f"min singular value={svals[-1]:.6f}",
            )
            check(
                f"({perm}, delta_CP={delta_cp / math.pi:.0f} pi): only lambda=0 solves A lambda = 0",
                svals[-1] > 1e-8,
                f"min singular value={svals[-1]:.6f}",
            )

    print("\n=== Part 2: numerical asymptotic chamber-sphere floor ===")
    best_value = float("inf")
    best_perm = None
    best_dir = None

    def direction_from_angles(x: np.ndarray) -> tuple[float, float, float]:
        u, v = x
        return (
            math.cos(u) * math.cos(v),
            math.cos(u) * math.sin(v),
            math.sin(u),
        )

    for perm in itertools.permutations(range(3)):
        for u0 in np.linspace(-1.4, 1.4, 9):
            for v0 in np.linspace(-math.pi, math.pi, 17):
                def objective(x: np.ndarray, perm: tuple[int, int, int] = perm) -> float:
                    point = direction_from_angles(x)
                    if point[1] + point[2] < 1e-8:
                        return 1e3 + (1e-8 - (point[1] + point[2])) * 1e3
                    return asymptotic_chi2(point, perm)

                res = minimize(
                    objective,
                    x0=np.array([u0, v0]),
                    method="Nelder-Mead",
                    options={"maxiter": 4000, "xatol": 1e-10, "fatol": 1e-12},
                )
                if res.fun < best_value:
                    best_value = float(res.fun)
                    best_perm = perm
                    best_dir = direction_from_angles(res.x)

    check(
        "Pure-source chamber-sphere minimum stays strictly above zero",
        best_value > 1e-4,
        f"best chi^2_inf={best_value:.9f} at perm={best_perm}, dir={best_dir}",
    )
    check(
        "The asymptotic floor is near the observed 1e-3 scale, not numerical zero",
        5e-4 < best_value < 5e-3,
        f"best chi^2_inf={best_value:.9f}",
    )

    print("\nInterpretation:")
    print("  No exact PMNS-fit basin can escape to infinity, because the")
    print("  pure-source limit admits no nonzero solution with the target angles.")
    print("  The remaining basin-enumeration problem is therefore compact.")
    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
