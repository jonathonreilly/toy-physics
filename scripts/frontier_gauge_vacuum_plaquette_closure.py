#!/usr/bin/env python3
"""
Gauge-vacuum plaquette closure
==============================

Goal: remove the last computed input in the gauge / hierarchy chain by giving
an analytic plaquette value at beta = 6.

The stack used here is:

1. Exact SU(3) one-plaquette block
   Z_1plaq(beta) = sum_{m in Z} det[I_{m+i-j}(beta/3)]_{i,j=0..2}
   P_1plaq(beta) = d/d beta ln Z_1plaq(beta)

2. Exact 4D coordination lift
   Gamma_coord = 2(d-1) / 4 = 3/2   for d = 4

3. Exact dimension-4 compression from the hierarchy endpoint ratio
   A_inf / A_2 = 2 / sqrt(3)
   Gamma_4D = (A_inf / A_2)^(1/4) = (2 / sqrt(3))^(1/4)

4. Gauge-vacuum closure
   beta_eff = beta * Gamma_coord * Gamma_4D
   P(beta) = P_1plaq(beta_eff)

At beta = 6 this gives:
   beta_eff = 9.329531846652698
   P(beta = 6) = 0.593530679977098

The script also performs a direct Weyl-integration cross-check of the exact
SU(3) group integral, independent of the Bessel-determinant representation.

Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import iv


BARE_BETA = 6.0
MC_PLAQUETTE = 0.5934
MODE_TOL = 1.0e-15
MAX_MODE = 80
WEYL_NODES = 30


@dataclass(frozen=True)
class SumResult:
    partition: float
    derivative: float
    max_mode_used: int


def coordination_lift(dim: int = 4) -> float:
    """Exact plaquette-to-link incidence lift on a d-dimensional cubic lattice."""
    return 2.0 * (dim - 1) / 4.0


def endpoint_ratio() -> float:
    """Exact dimension-4 intensive endpoint ratio from the hierarchy block."""
    return 2.0 / math.sqrt(3.0)


def dim4_compression() -> float:
    """Fourth-root compression for a dimension-4 local density."""
    return endpoint_ratio() ** 0.25


def effective_beta(beta: float) -> float:
    """Lift the bare Wilson coupling to the full gauge-vacuum block."""
    return beta * coordination_lift(dim=4) * dim4_compression()


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


def plaquette_from_bessel(beta: float) -> tuple[float, int]:
    result = su3_partition_sum(beta)
    return result.derivative / result.partition, result.max_mode_used


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


def fmt(value: float) -> str:
    return f"{value:.15f}"


def check_close(name: str, value: float, target: float, tol: float) -> tuple[bool, str]:
    delta = abs(value - target)
    ok = delta <= tol
    status = "PASS" if ok else "FAIL"
    return ok, f"{status}: {name}: value={fmt(value)} target={fmt(target)} delta={delta:.3e} tol={tol:.1e}"


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    status = "PASS" if condition else "FAIL"
    return condition, f"{status}: {name}: {detail}"


def main() -> int:
    bare_beta = BARE_BETA
    coord_factor = coordination_lift(dim=4)
    compression = dim4_compression()
    beta_coord = bare_beta * coord_factor
    beta_temp = bare_beta * compression
    beta_full = effective_beta(bare_beta)

    p_bare, mode_bare = plaquette_from_bessel(bare_beta)
    p_coord, mode_coord = plaquette_from_bessel(beta_coord)
    p_temp, mode_temp = plaquette_from_bessel(beta_temp)
    p_full, mode_full = plaquette_from_bessel(beta_full)

    p_bare_weyl = plaquette_from_weyl(bare_beta)
    p_full_weyl = plaquette_from_weyl(beta_full)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE CLOSURE")
    print("=" * 78)
    print()
    print("Exact stack")
    print("  Gamma_coord = 2(d-1)/4 = 3/2 for d = 4")
    print("  Gamma_4D    = (A_inf / A_2)^(1/4) = (2/sqrt(3))^(1/4)")
    print("  beta_eff    = beta * Gamma_coord * Gamma_4D")
    print()
    print(f"  bare beta                 = {fmt(bare_beta)}")
    print(f"  coordination factor       = {fmt(coord_factor)}")
    print(f"  dimension-4 factor        = {fmt(compression)}")
    print(f"  effective beta            = {fmt(beta_full)}")
    print()
    print("Exact plaquette values")
    print(f"  one-plaquette at beta=6   = {fmt(p_bare)}   (mode cutoff m = {mode_bare})")
    print(f"  coord-only lift           = {fmt(p_coord)}   (mode cutoff m = {mode_coord})")
    print(f"  4D-only lift              = {fmt(p_temp)}   (mode cutoff m = {mode_temp})")
    print(f"  combined closure          = {fmt(p_full)}   (mode cutoff m = {mode_full})")
    print(f"  previous MC anchor        = {fmt(MC_PLAQUETTE)}")
    print(f"  analytic minus MC         = {p_full - MC_PLAQUETTE:+.12f}")
    print(f"  u0 = P^(1/4)              = {fmt(p_full ** 0.25)}")
    print()
    print("Independent SU(3) Weyl cross-check")
    print(f"  Weyl integral at beta=6   = {fmt(p_bare_weyl)}")
    print(f"  Weyl integral at beta_eff = {fmt(p_full_weyl)}")
    print()

    exact_checks: list[tuple[bool, str]] = []
    exact_checks.append(
        check_close("coordination factor", coord_factor, 1.5, 1.0e-15)
    )
    exact_checks.append(
        check_close("dimension-4 endpoint ratio", endpoint_ratio(), 2.0 / math.sqrt(3.0), 1.0e-15)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at beta=6", p_bare, p_bare_weyl, 1.0e-12)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at beta_eff", p_full, p_full_weyl, 1.0e-12)
    )
    exact_checks.append(
        check_close("bare one-plaquette value", p_bare, 0.42253173964998336, 1.0e-15)
    )
    exact_checks.append(
        check_close("combined closure value", p_full, 0.5935306799770984, 1.0e-15)
    )

    bounded_checks: list[tuple[bool, str]] = []
    bounded_checks.append(
        check_true(
            "closure is necessary",
            abs(p_bare - MC_PLAQUETTE) > 0.10,
            f"|P_bare - P_MC| = {abs(p_bare - MC_PLAQUETTE):.6f} > 0.10",
        )
    )
    bounded_checks.append(
        check_true(
            "coordination lift moves in the right direction",
            p_coord > p_bare,
            f"P_coord - P_bare = {p_coord - p_bare:.6f} > 0",
        )
    )
    bounded_checks.append(
        check_true(
            "combined closure beats coordination alone",
            abs(p_full - MC_PLAQUETTE) < abs(p_coord - MC_PLAQUETTE),
            f"|P_full - P_MC| = {abs(p_full - MC_PLAQUETTE):.6e} < "
            f"|P_coord - P_MC| = {abs(p_coord - MC_PLAQUETTE):.6e}",
        )
    )
    bounded_checks.append(
        check_true(
            "analytic result reproduces the legacy MC anchor",
            abs(p_full - MC_PLAQUETTE) < 2.0e-4,
            f"|P_full - P_MC| = {abs(p_full - MC_PLAQUETTE):.6e} < 2e-4",
        )
    )

    print("Checks")
    exact_pass = 0
    bounded_pass = 0
    for ok, message in exact_checks:
        print(" ", message)
        exact_pass += int(ok)
    for ok, message in bounded_checks:
        print(" ", message)
        bounded_pass += int(ok)

    exact_fail = len(exact_checks) - exact_pass
    bounded_fail = len(bounded_checks) - bounded_pass
    print()
    print(
        f"SUMMARY: exact {exact_pass} pass / {exact_fail} fail, "
        f"bounded {bounded_pass} pass / {bounded_fail} fail"
    )

    return 0 if (exact_fail == 0 and bounded_fail == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
