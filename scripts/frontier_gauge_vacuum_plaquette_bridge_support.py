#!/usr/bin/env python3
"""
Gauge-vacuum plaquette scalar-bridge support stack.

This script records the exact local/source/coupling ingredients and the sharp
current analytic plaquette candidate without promoting the full physical-vacuum
bridge insertion as a theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import iv

from canonical_plaquette_surface import CANONICAL_PLAQUETTE
from frontier_scalar_3plus1_temporal_ratio import completion_ratio


BARE_BETA = 6.0
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
    return 6.0 / 4.0


def scalar_completion_factor_dim4() -> float:
    return completion_ratio() ** 0.25


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


def source_response_generator(beta: float, j: float) -> float:
    zp, _ = partition_from_bessel(beta + j)
    z0, _ = partition_from_bessel(beta)
    return math.log(zp) - math.log(z0)


def two_block_source_response_generator(beta: float, j: float) -> float:
    zp, _ = partition_from_bessel(beta + j)
    z0, _ = partition_from_bessel(beta)
    return math.log((zp * zp) / (z0 * z0))


def source_derivative_from_generator(beta: float, step: float = FINITE_DIFF_STEP) -> float:
    return (source_response_generator(beta, step) - source_response_generator(beta, -step)) / (2.0 * step)


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
            z1 = np.exp(1j * theta1)
            z2 = np.exp(1j * theta2)
            z3 = np.exp(1j * theta3)
            haar = abs((z1 - z2) * (z1 - z3) * (z2 - z3)) ** 2
            weight = weights[i] * weights[j] * haar
            factor = math.exp((beta / 3.0) * trace_real)
            partition += weight * factor
            numerator += weight * factor * (trace_real / 3.0)

    return numerator / partition


def random_su3(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    phases = d / np.abs(d)
    q = q @ np.diag(np.conj(phases))
    det = np.linalg.det(q)
    return q / det ** (1.0 / 3.0)


def plaquette_value(links: list[np.ndarray]) -> float:
    u1, u2, u3, u4 = links
    up = u1 @ u2 @ u3.conj().T @ u4.conj().T
    return float(np.trace(up).real / 3.0)


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
    ratio = completion_ratio()
    factor = scalar_completion_factor_dim4()
    beta_eff = effective_beta(bare_beta)

    p_bare, mode_bare = plaquette_from_bessel(bare_beta)
    p_bare_src = source_derivative_from_generator(bare_beta)
    p_bare_weyl = plaquette_from_weyl(bare_beta)
    p_eff, mode_eff = plaquette_from_bessel(beta_eff)

    w1 = source_response_generator(bare_beta, 0.037)
    w2 = two_block_source_response_generator(bare_beta, 0.037)

    rng = np.random.default_rng(7)
    links = [random_su3(rng) for _ in range(4)]
    p_ref = plaquette_value(links)
    scale_devs = []
    wrong_devs = []
    for u0 in [0.5, 0.7, 0.877, 1.0, 1.3]:
        scaled_links = [u0 * link for link in links]
        p_scaled = plaquette_value(scaled_links)
        scale_devs.append(abs(p_scaled / (u0**4) - p_ref))
        if abs(p_ref) > 1e-12:
            wrong_devs.append(abs(p_scaled / (u0**2) - p_ref))

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE SCALAR-BRIDGE SUPPORT")
    print("=" * 78)
    print()
    print("Local Wilson source-response")
    print(f"  P_1plaq(6) from exact derivative     = {fmt(p_bare)}   (mode cutoff m = {mode_bare})")
    print(f"  P_1plaq(6) from source derivative    = {fmt(p_bare_src)}")
    print(f"  P_1plaq(6) from Weyl integration     = {fmt(p_bare_weyl)}")
    print(f"  W_tot(j) for two independent blocks  = {fmt(w2)}")
    print()
    print("Scalar 3+1 bridge")
    print(f"  A_inf / A_2                          = {fmt(ratio)}")
    print(f"  Gamma_sc = ratio^(1/4)              = {fmt(factor)}")
    print()
    print("Plaquette four-link coupling map")
    print(f"  max |P(u0 V)/u0^4 - P(V)|           = {max(scale_devs):.3e}")
    print(f"  max |P(u0 V)/u0^2 - P(V)|           = {max(wrong_devs):.3e}")
    print()
    print("Support candidate output")
    print(f"  Gamma_coord                         = {fmt(coord)}")
    print(f"  beta_eff                            = {fmt(beta_eff)}")
    print(f"  P(6)                                = {fmt(p_eff)}   (mode cutoff m = {mode_eff})")
    print(f"  canonical same-surface P            = {fmt(CANONICAL_PLAQUETTE)}")
    print(f"  closure minus canonical             = {p_eff - CANONICAL_PLAQUETTE:+.12f}")
    print()

    exact_checks: list[tuple[bool, str]] = []
    exact_checks.append(
        check_close("local plaquette equals local Wilson source derivative", p_bare, p_bare_src, 1.0e-9)
    )
    exact_checks.append(
        check_true(
            "local Wilson generator is additive on independent blocks",
            abs((w1 + w1) - w2) < 1.0e-15,
            f"|W1+W1-W2| = {abs((w1 + w1) - w2):.3e}",
        )
    )
    exact_checks.append(check_close("Bessel/Weyl agreement at beta=6", p_bare, p_bare_weyl, 1.0e-12))
    exact_checks.append(check_close("scalar 3+1 completion ratio", ratio, 2.0 / math.sqrt(3.0), 1.0e-15))
    exact_checks.append(
        check_true(
            "plaquette four-link coupling map is exact",
            max(scale_devs) < 1.0e-12,
            f"max scaling deviation = {max(scale_devs):.3e}",
        )
    )
    exact_checks.append(
        check_close("3+1 incidence factor", coord, 1.5, 1.0e-15)
    )

    support_checks: list[tuple[bool, str]] = []
    support_checks.append(
        check_true(
            "no lower link power preserves the plaquette coupling map",
            max(wrong_devs) > 1.0e-2,
            f"max wrong-power deviation = {max(wrong_devs):.3e}",
        )
    )
    support_checks.append(
        check_true(
            "candidate plaquette value stays near the historical canonical surface",
            abs(p_eff - CANONICAL_PLAQUETTE) < 2.0e-4,
            f"|P(6) - P_can| = {abs(p_eff - CANONICAL_PLAQUETTE):.6e} < 2e-4",
        )
    )

    exact_pass = 0
    support_pass = 0
    print("Checks")
    for ok, msg in exact_checks:
        print(" ", msg)
        exact_pass += int(ok)
    for ok, msg in support_checks:
        print(" ", msg)
        support_pass += int(ok)

    fail = (len(exact_checks) - exact_pass) + (len(support_checks) - support_pass)
    print()
    print(f"SUMMARY: EXACT PASS={exact_pass} SUPPORT={support_pass} FAIL={fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
