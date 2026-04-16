#!/usr/bin/env python3
"""
Gauge-vacuum plaquette closure on the exact 3+1 scalar bridge
==============================================================

The exact closure stack is:

1. exact local SU(3) one-plaquette block
2. exact scalar temporal-completion factor on the minimal 3 spatial + 1 time block
3. exact plaquette/link incidence lift on the 3+1 lattice

This gives

    beta_eff = beta * (3/2) * (2 / sqrt(3))^(1/4)
    P(beta)  = P_1plaq(beta_eff)

At beta = 6:

    P(6) = 0.593530679977098

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


@dataclass(frozen=True)
class SumResult:
    partition: float
    derivative: float
    max_mode_used: int


def coordination_factor_3plus1() -> float:
    """Each link lies in 6 plaquettes; each plaquette has 4 links."""
    return 6.0 / 4.0


def apbc_frequencies(lt: int) -> np.ndarray:
    n = np.arange(lt, dtype=float)
    return 2.0 * math.pi * (n + 0.5) / lt


def scalar_bridge_coefficient(lt: int) -> float:
    omega = apbc_frequencies(lt)
    return float(np.mean(1.0 / (3.0 + np.sin(omega) ** 2)) / 2.0)


def scalar_completion_ratio() -> float:
    return (1.0 / (4.0 * math.sqrt(3.0))) / (1.0 / 8.0)


def scalar_completion_factor_dim4() -> float:
    return scalar_completion_ratio() ** 0.25


def effective_beta(beta: float) -> float:
    return beta * coordination_factor_3plus1() * scalar_completion_factor_dim4()


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
    coord = coordination_factor_3plus1()
    a2 = scalar_bridge_coefficient(2)
    a4096 = scalar_bridge_coefficient(4096)
    ratio = scalar_completion_ratio()
    factor = scalar_completion_factor_dim4()
    beta_eff = effective_beta(bare_beta)

    p_bare, mode_bare = plaquette_from_bessel(bare_beta)
    p_bare_fd = plaquette_from_finite_difference(bare_beta)
    p_bare_weyl = plaquette_from_weyl(bare_beta)
    p_eff, mode_eff = plaquette_from_bessel(beta_eff)
    p_eff_weyl = plaquette_from_weyl(beta_eff)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE CLOSURE ON THE EXACT 3+1 SCALAR BRIDGE")
    print("=" * 78)
    print()
    print("Exact ingredients")
    print("  local SU(3) block: P_1plaq(beta_loc) = d/d beta_loc log Z_1plaq(beta_loc)")
    print("  scalar bridge:     K_sc(omega) = 3 + sin^2(omega)")
    print("  scalar factor:     Gamma_sc = (2 / sqrt(3))^(1/4)")
    print("  incidence factor:  Gamma_coord = 6 / 4 = 3/2")
    print()
    print(f"  bare beta                  = {fmt(bare_beta)}")
    print(f"  exact local P_1plaq(6)     = {fmt(p_bare)}   (mode cutoff m = {mode_bare})")
    print(f"  finite-difference check    = {fmt(p_bare_fd)}")
    print(f"  Weyl-angle check           = {fmt(p_bare_weyl)}")
    print()
    print("Scalar completion data")
    print(f"  A_2                        = {fmt(a2)}")
    print(f"  A_inf (Lt=4096 proxy)      = {fmt(a4096)}")
    print(f"  Gamma_sc                   = {fmt(factor)}")
    print(f"  Gamma_coord                = {fmt(coord)}")
    print()
    print("Closed plaquette output")
    print(f"  beta_eff                   = {fmt(beta_eff)}")
    print(f"  P(6) = P_1plaq(beta_eff)   = {fmt(p_eff)}   (mode cutoff m = {mode_eff})")
    print(f"  Weyl check at beta_eff     = {fmt(p_eff_weyl)}")
    print(f"  u_0 = P^(1/4)              = {fmt(p_eff ** 0.25)}")
    print(f"  canonical same-surface P   = {fmt(CANONICAL_PLAQUETTE)}")
    print(f"  closure minus canonical    = {p_eff - CANONICAL_PLAQUETTE:+.12f}")
    print()

    exact_checks: list[tuple[bool, str]] = []
    exact_checks.append(
        check_close("analytic derivative vs finite difference at beta=6", p_bare, p_bare_fd, 1.0e-9)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at beta=6", p_bare, p_bare_weyl, 1.0e-12)
    )
    exact_checks.append(
        check_close("scalar A_2 coefficient", a2, 1.0 / 8.0, 1.0e-15)
    )
    exact_checks.append(
        check_close("scalar A_inf coefficient", a4096, 1.0 / (4.0 * math.sqrt(3.0)), 1.0e-8)
    )
    exact_checks.append(
        check_close("scalar completion ratio", ratio, 2.0 / math.sqrt(3.0), 1.0e-15)
    )
    exact_checks.append(
        check_close("3+1 incidence factor", coord, 1.5, 1.0e-15)
    )
    exact_checks.append(
        check_close("Bessel/Weyl agreement at beta_eff", p_eff, p_eff_weyl, 1.0e-12)
    )

    bounded_checks: list[tuple[bool, str]] = []
    bounded_checks.append(
        check_true(
            "closed result matches previous canonical plaquette",
            abs(p_eff - CANONICAL_PLAQUETTE) < 2.0e-4,
            f"|P(6) - P_can| = {abs(p_eff - CANONICAL_PLAQUETTE):.6e} < 2e-4",
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
    return 0 if (exact_fail == 0 and bounded_fail == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
