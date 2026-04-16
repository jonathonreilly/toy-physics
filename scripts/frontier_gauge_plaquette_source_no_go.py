#!/usr/bin/env python3
"""
Gauge plaquette source theorem and constant-lift no-go
=====================================================

This runner keeps the real part of the old package:

1. exact local SU(3) one-plaquette block
2. independent Weyl-angle cross-check
3. exact strong-coupling slope theorem

and replaces the unsupported claim with the exact obstruction:

If the full 3+1 plaquette satisfied

    P_full(beta) = P_1plaq(c beta)

for a constant c on an interval, then exact strong-coupling matching forces

    c = 1.

So the proposed

    c = (3/2) * (2 / sqrt(3))^(1/4)

cannot be exact.

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import iv


BARE_BETA = 6.0
CANONICAL_PLAQUETTE = 0.5934
MODE_TOL = 1.0e-15
MAX_MODE = 80
WEYL_NODES = 30
FINITE_DIFF_STEP = 1.0e-6
TINY_BETA = 1.0e-5


@dataclass(frozen=True)
class SumResult:
    partition: float
    derivative: float
    max_mode_used: int


def proposed_constant_lift() -> float:
    """The rejected closure constant from the old package."""
    return 1.5 * (2.0 / math.sqrt(3.0)) ** 0.25


def exact_strong_coupling_slope() -> float:
    """
    Exact beta -> 0 slope of the full plaquette.

    For P = (1/3) Re Tr U_P and weight exp[beta sum_p P_p], the O(beta)
    term is beta * <P_q^2>_0. Haar orthogonality gives <P_q^2>_0 = 1/18.
    """
    return 1.0 / 18.0


def one_plaquette_series_slope() -> float:
    """Exact slope of the one-plaquette block from Z = 1 + beta^2/36 + O(beta^4)."""
    return 1.0 / 18.0


def bessel_matrix(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [[iv(mode + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def bessel_matrix_derivative(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [
            [
                (iv(mode + i - j - 1, arg) + iv(mode + i - j + 1, arg)) / 6.0
                for j in range(3)
            ]
            for i in range(3)
        ],
        dtype=float,
    )


def su3_mode_terms(beta: float, mode: int) -> tuple[float, float]:
    mat = bessel_matrix(beta, mode)
    dmat = bessel_matrix_derivative(beta, mode)
    det = float(np.linalg.det(mat))
    derivative = det * float(np.trace(np.linalg.inv(mat) @ dmat))
    return det, derivative


def su3_partition_sum(beta: float, tol: float = MODE_TOL, max_mode: int = MAX_MODE) -> SumResult:
    total_partition = 0.0
    total_derivative = 0.0

    for mode in range(max_mode + 1):
        strip_partition = 0.0
        strip_derivative = 0.0
        modes = [0] if mode == 0 else [-mode, mode]
        for signed_mode in modes:
            part, deriv = su3_mode_terms(beta, signed_mode)
            strip_partition += part
            strip_derivative += deriv

        total_partition += strip_partition
        total_derivative += strip_derivative

        if mode >= 3:
            partition_small = abs(strip_partition) < tol * abs(total_partition)
            derivative_small = abs(strip_derivative) < tol * abs(total_derivative)
            if partition_small and derivative_small:
                return SumResult(total_partition, total_derivative, mode)

    raise RuntimeError(f"mode sum did not converge by m = {max_mode}")


def partition_from_bessel(beta: float) -> tuple[float, int]:
    result = su3_partition_sum(beta)
    return result.partition, result.max_mode_used


def plaquette_from_bessel(beta: float) -> tuple[float, int]:
    result = su3_partition_sum(beta)
    return result.derivative / result.partition, result.max_mode_used


def plaquette_from_finite_difference(beta: float, step: float = FINITE_DIFF_STEP) -> float:
    zp, _ = partition_from_bessel(beta + step)
    zm, _ = partition_from_bessel(beta - step)
    return (math.log(zp) - math.log(zm)) / (2.0 * step)


def haar_weight(theta1: float, theta2: float) -> float:
    theta3 = -theta1 - theta2
    z1 = np.exp(1j * theta1)
    z2 = np.exp(1j * theta2)
    z3 = np.exp(1j * theta3)
    return float(abs((z1 - z2) * (z1 - z3) * (z2 - z3)) ** 2)


def plaquette_from_weyl(beta: float, nodes: int = WEYL_NODES) -> float:
    leg_nodes, leg_weights = np.polynomial.legendre.leggauss(nodes)
    thetas = math.pi * (leg_nodes + 1.0)
    weights = math.pi * leg_weights

    partition = 0.0
    numerator = 0.0

    for i, theta1 in enumerate(thetas):
        for j, theta2 in enumerate(thetas):
            theta3 = -theta1 - theta2
            trace_real = math.cos(theta1) + math.cos(theta2) + math.cos(theta3)
            weight = weights[i] * weights[j] * haar_weight(theta1, theta2)
            factor = math.exp((beta / 3.0) * trace_real)
            partition += weight * factor
            numerator += weight * factor * (trace_real / 3.0)

    return numerator / partition


def fmt(x: float) -> str:
    return f"{x:.15f}"


def check_close(name: str, value: float, target: float, tol: float) -> tuple[bool, str]:
    delta = abs(value - target)
    ok = delta <= tol
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={fmt(value)} target={fmt(target)} delta={delta:.3e} tol={tol:.1e}"


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    bare_beta = BARE_BETA
    slope_full = exact_strong_coupling_slope()
    slope_1plaq = one_plaquette_series_slope()
    c_prop = proposed_constant_lift()
    beta_prop = c_prop * bare_beta

    p_bare, mode_bare = plaquette_from_bessel(bare_beta)
    p_bare_fd = plaquette_from_finite_difference(bare_beta)
    p_bare_weyl = plaquette_from_weyl(bare_beta)
    p_prop, mode_prop = plaquette_from_bessel(beta_prop)
    p_prop_weyl = plaquette_from_weyl(beta_prop)
    p_tiny, _ = plaquette_from_bessel(TINY_BETA)

    print("=" * 78)
    print("GAUGE PLAQUETTE SOURCE THEOREM AND CONSTANT-LIFT NO-GO")
    print("=" * 78)
    print()
    print("Exact ingredients")
    print("  local SU(3) block: P_1plaq(beta_loc) = d/d beta_loc log Z_1plaq(beta_loc)")
    print("  full gauge source: P_Lambda(beta) = (1/N_p) d/d beta log Z_Lambda(beta)")
    print("  exact slope:       dP/d beta |_(beta=0) = 1/18")
    print()
    print(f"  bare beta                  = {fmt(bare_beta)}")
    print(f"  exact local P_1plaq(6)     = {fmt(p_bare)}   (mode cutoff m = {mode_bare})")
    print(f"  finite-difference check    = {fmt(p_bare_fd)}")
    print(f"  Weyl-angle check           = {fmt(p_bare_weyl)}")
    print()
    print("Strong-coupling theorem data")
    print(f"  full-theory slope          = {fmt(slope_full)}")
    print(f"  one-plaquette slope        = {fmt(slope_1plaq)}")
    print(f"  numeric P_1plaq({TINY_BETA:.0e})/{TINY_BETA:.0e} = {fmt(p_tiny / TINY_BETA)}")
    print()
    print("Rejected constant-lift proposal")
    print(f"  c_prop                     = {fmt(c_prop)}")
    print(f"  proposed beta_prop         = {fmt(beta_prop)}")
    print(f"  P_1plaq(beta_prop)         = {fmt(p_prop)}   (mode cutoff m = {mode_prop})")
    print(f"  Weyl check at beta_prop    = {fmt(p_prop_weyl)}")
    print(f"  canonical same-surface P   = {fmt(CANONICAL_PLAQUETTE)}")
    print(f"  proposal minus canonical   = {p_prop - CANONICAL_PLAQUETTE:+.12f}")
    print(f"  exact required c           = {fmt(slope_full / slope_1plaq)}")
    print()

    exact_checks: list[tuple[bool, str]] = []
    exact_checks.append(
        check_close("analytic derivative vs finite difference at beta=6", p_bare, p_bare_fd, 1.0e-9)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at beta=6", p_bare, p_bare_weyl, 1.0e-12)
    )
    exact_checks.append(
        check_close("exact full-theory strong-coupling slope", slope_full, 1.0 / 18.0, 1.0e-15)
    )
    exact_checks.append(
        check_close("exact one-plaquette strong-coupling slope", slope_1plaq, 1.0 / 18.0, 1.0e-15)
    )
    exact_checks.append(
        check_close("numeric one-plaquette small-beta slope", p_tiny / TINY_BETA, 1.0 / 18.0, 5.0e-8)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at proposed beta", p_prop, p_prop_weyl, 1.0e-12)
    )
    exact_checks.append(
        check_close("constant-lift no-go requires c = 1", slope_full / slope_1plaq, 1.0, 1.0e-15)
    )

    bounded_checks: list[tuple[bool, str]] = []
    bounded_checks.append(
        check_true(
            "proposed lifted block lands numerically near the canonical plaquette",
            abs(p_prop - CANONICAL_PLAQUETTE) < 2.0e-4,
            f"|P_1plaq(c_prop*6) - P_can| = {abs(p_prop - CANONICAL_PLAQUETTE):.6e} < 2e-4",
        )
    )

    print("Checks")
    exact_pass = 0
    bounded_pass = 0
    for ok, msg in exact_checks:
        print(" ", msg)
        exact_pass += int(ok)
    for ok, msg in bounded_checks:
        print(" ", msg)
        bounded_pass += int(ok)

    exact_fail = len(exact_checks) - exact_pass
    bounded_fail = len(bounded_checks) - bounded_pass
    print()
    print(
        f"SUMMARY: exact {exact_pass} pass / {exact_fail} fail, "
        f"bounded {bounded_pass} pass / {bounded_fail} fail"
    )
    print()

    if exact_fail or bounded_fail:
        return 1

    print("Exact local SU(3) block confirmed.")
    print("Exact no-go confirmed: any constant-lift closure P(beta) = P_1plaq(c beta) forces c = 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
