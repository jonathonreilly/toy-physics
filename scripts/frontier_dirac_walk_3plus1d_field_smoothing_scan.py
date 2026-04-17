#!/usr/bin/env python3
"""Dirac 3+1D field smoothing scan.

This probe compares the current localized inverse-distance mass profile against
broader matched-strength alternatives on the same 4-component Dirac walk:

    m(r) = m0 * (1 + strength * kernel(r))

The baseline kernel is the current localized profile from the v4 convergence
lane, kernel(r) = 1 / (r + 0.1). Two broader controls are included:

    - softened inverse-distance: 1 / (r + 1.0)
    - Gaussian: exp(-r^2 / (2 sigma^2)), sigma = 3.0

Each candidate is rescaled so that the integrated kernel strength matches the
baseline approximately exactly on the same lattice and source placement.

The scan evaluates:
    1. monotonicity over N at n=29, source offset=3
    2. offset-distance law at n=29, N=16

The goal is to see whether broadening the source field improves the remaining
gravity failures in the current Dirac harness.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

import numpy as np


gamma0 = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ],
    dtype=complex,
)

gamma1 = np.array(
    [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, -1, 0, 0],
        [-1, 0, 0, 0],
    ],
    dtype=complex,
)

gamma2 = np.array(
    [
        [0, 0, 0, -1j],
        [0, 0, 1j, 0],
        [0, 1j, 0, 0],
        [-1j, 0, 0, 0],
    ],
    dtype=complex,
)

gamma3 = np.array(
    [
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
    ],
    dtype=complex,
)


def projectors(gp: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(gp)
    p_plus = sum(
        np.outer(evecs[:, i], evecs[:, i].conj())
        for i in range(4)
        if evals[i] > 0
    )
    p_minus = sum(
        np.outer(evecs[:, i], evecs[:, i].conj())
        for i in range(4)
        if evals[i] < 0
    )
    return p_plus, p_minus


PX_P, PX_M = projectors(gamma0 @ gamma1)
PY_P, PY_M = projectors(gamma0 @ gamma2)
PZ_P, PZ_M = projectors(gamma0 @ gamma3)


def coin_step(psi: np.ndarray, mass_field: np.ndarray) -> np.ndarray:
    cm = np.cos(mass_field)
    sm = np.sin(mass_field)
    out = np.zeros_like(psi)
    out[0] = (cm + 1j * sm) * psi[0]
    out[1] = (cm + 1j * sm) * psi[1]
    out[2] = (cm - 1j * sm) * psi[2]
    out[3] = (cm - 1j * sm) * psi[3]
    return out


def _shift_piece(piece: np.ndarray, axis: int, direction: int) -> np.ndarray:
    out = np.zeros_like(piece)
    src = [slice(None)] * 3
    dst = [slice(None)] * 3
    if direction > 0:
        src[axis] = slice(0, -1)
        dst[axis] = slice(1, None)
    else:
        src[axis] = slice(1, None)
        dst[axis] = slice(0, -1)
    out[tuple(dst)] = piece[tuple(src)]
    return out


def shift_dir(psi: np.ndarray, axis: int) -> np.ndarray:
    out = np.zeros_like(psi)
    if axis == 0:
        p_plus, p_minus = PX_P, PX_M
    elif axis == 1:
        p_plus, p_minus = PY_P, PY_M
    elif axis == 2:
        p_plus, p_minus = PZ_P, PZ_M
    else:
        raise ValueError(f"invalid axis: {axis}")

    for c in range(4):
        pp = sum(p_plus[c, d] * psi[d] for d in range(4))
        pm = sum(p_minus[c, d] * psi[d] for d in range(4))
        out[c] += _shift_piece(pp, axis, +1)
        out[c] += _shift_piece(pm, axis, -1)
    return out


def step_dirac(psi: np.ndarray, mass_field: np.ndarray) -> np.ndarray:
    psi = coin_step(psi, mass_field)
    psi = shift_dir(psi, 0)
    psi = shift_dir(psi, 1)
    psi = shift_dir(psi, 2)
    return psi


def density(psi: np.ndarray) -> tuple[np.ndarray, float]:
    rho = np.sum(np.abs(psi) ** 2, axis=0)
    total = float(np.sum(rho))
    if total > 1e-30:
        rho = rho / total
    return rho, total


def min_image_dist(n: int, pos: tuple[int, int, int]) -> np.ndarray:
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - pos[0])
    dx = np.minimum(dx, n - dx)
    dy = np.abs(c[None, :, None] - pos[1])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, None, :] - pos[2])
    dz = np.minimum(dz, n - dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def profile_kernel(n: int, source: tuple[int, int, int], family: str, param: float) -> np.ndarray:
    r = min_image_dist(n, source)
    if family == "inverse":
        return 1.0 / (r + param)
    if family == "gaussian":
        return np.exp(-0.5 * (r / param) ** 2)
    raise ValueError(f"unknown family: {family}")


def build_mass_field(
    n: int,
    mass0: float,
    strength: float,
    source: tuple[int, int, int],
    family: str,
    param: float,
    target_kernel_sum: float | None = None,
) -> tuple[np.ndarray, float, float]:
    kernel = profile_kernel(n, source, family, param)
    kernel_sum = float(np.sum(kernel))
    if target_kernel_sum is None:
        matched_strength = strength
    else:
        matched_strength = strength * target_kernel_sum / kernel_sum
    mass_field = mass0 * (1.0 + matched_strength * kernel)
    return mass_field, matched_strength, kernel_sum


def evolve(
    n: int,
    n_layers: int,
    mass0: float,
    strength: float,
    source: tuple[int, int, int] | None,
    family: str | None,
    param: float | None,
    target_kernel_sum: float | None = None,
) -> tuple[np.ndarray, float, float]:
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c = n // 2
    for k in range(4):
        psi[k, c, c, c] = 0.5

    if source is None or family is None or param is None or strength <= 0:
        mass_field = np.full((n, n, n), mass0, dtype=float)
        matched_strength = 0.0
        kernel_sum = 0.0
    else:
        mass_field, matched_strength, kernel_sum = build_mass_field(
            n,
            mass0,
            strength,
            source,
            family,
            param,
            target_kernel_sum=target_kernel_sum,
        )

    for _ in range(n_layers):
        psi = step_dirac(psi, mass_field)
    return psi, matched_strength, kernel_sum


def readout_bias(rho_field: np.ndarray, rho_free: np.ndarray, n: int, offset: int) -> tuple[float, float, float]:
    c = n // 2
    toward = float(np.sum(rho_field[c, c, c + 1 : c + offset + 1] - rho_free[c, c, c + 1 : c + offset + 1]))
    away = float(np.sum(rho_field[c, c, c - offset : c] - rho_free[c, c, c - offset : c]))
    return toward, away, toward - away


def fit_power_law(offsets: list[int], biases: list[float]) -> tuple[float, float]:
    arr = np.array(biases, dtype=float)
    signs = np.sign(arr)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        return float("nan"), 0.0
    x = np.log10(np.array(offsets, dtype=float))
    y = np.log10(np.abs(arr))
    coeffs = np.polyfit(x, y, 1)
    pred = np.polyval(coeffs, x)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coeffs[0]), r2


@dataclass
class SweepResult:
    family: str
    param: float
    matched_strength: float
    kernel_sum: float
    n_biases: list[float]
    n_monotone: bool
    offset_biases: list[float]
    toward_count: int
    offset_alpha: float
    offset_r2: float


def run_case(
    n: int,
    mass0: float,
    strength: float,
    family: str,
    param: float,
    source_offset: int,
    N_values: list[int],
    offsets: list[int],
    offset_layers: int,
) -> SweepResult:
    c = n // 2
    source = (c, c, c + source_offset)
    base_kernel = profile_kernel(n, source, "inverse", 0.1)
    target_kernel_sum = float(np.sum(base_kernel))

    free_cache: dict[int, np.ndarray] = {}

    def free_density_for_layers(layers: int) -> np.ndarray:
        if layers not in free_cache:
            psi_free, _, _ = evolve(n, layers, mass0, 0.0, None, None, None)
            free_cache[layers] = density(psi_free)[0]
        return free_cache[layers]

    n_biases: list[float] = []
    matched_strength = float("nan")
    kernel_sum = float("nan")
    for layers in N_values:
        rho_free = free_density_for_layers(layers)
        psi_field, matched_strength, kernel_sum = evolve(
            n,
            layers,
            mass0,
            strength,
            source,
            family,
            param,
            target_kernel_sum=target_kernel_sum,
        )
        rho_field = density(psi_field)[0]
        _, _, bias = readout_bias(rho_field, rho_free, n, source_offset)
        n_biases.append(bias)

    n_monotone = all(n_biases[i] <= n_biases[i + 1] for i in range(len(n_biases) - 1)) and all(
        b > 0 for b in n_biases
    )

    rho_free = free_density_for_layers(offset_layers)
    offset_biases: list[float] = []
    for off in offsets:
        source_off = (c, c, c + off)
        psi_field, matched_strength, kernel_sum = evolve(
            n,
            offset_layers,
            mass0,
            strength,
            source_off,
            family,
            param,
            target_kernel_sum=target_kernel_sum,
        )
        rho_field = density(psi_field)[0]
        _, _, bias = readout_bias(rho_field, rho_free, n, off)
        offset_biases.append(bias)

    toward_count = sum(1 for b in offset_biases if b > 0)
    alpha, r2 = fit_power_law(offsets, offset_biases)
    return SweepResult(
        family=family,
        param=param,
        matched_strength=matched_strength,
        kernel_sum=kernel_sum,
        n_biases=n_biases,
        n_monotone=n_monotone,
        offset_biases=offset_biases,
        toward_count=toward_count,
        offset_alpha=alpha,
        offset_r2=r2,
    )


def fmt_bias_list(values: list[float]) -> str:
    return "[" + ", ".join(f"{v:+.4e}" for v in values) + "]"


def main() -> None:
    parser = argparse.ArgumentParser(description="Dirac 3+1D field smoothing scan")
    parser.add_argument("--n", type=int, default=29)
    parser.add_argument("--mass0", type=float, default=0.10)
    parser.add_argument("--strength", type=float, default=5e-4)
    parser.add_argument("--source-offset", type=int, default=3)
    parser.add_argument("--offset-layers", type=int, default=16)
    args = parser.parse_args()

    n = args.n
    mass0 = args.mass0
    strength = args.strength
    source_offset = args.source_offset
    offset_layers = args.offset_layers
    N_values = [8, 10, 12, 14, 16, 18, 20, 22, 24]
    offsets = [2, 3, 4, 5, 6]

    families = [
        ("localized_inverse", "inverse", 0.1),
        ("soft_inverse", "inverse", 1.0),
        ("gaussian_sigma3", "gaussian", 3.0),
    ]

    start = time.time()
    results: list[SweepResult] = []

    print("=" * 78)
    print("DIRAC 3+1D FIELD SMOOTHING SCAN")
    print("=" * 78)
    print(f"n={n}, mass0={mass0:.3f}, strength={strength:.1e}, source_offset={source_offset}")
    print(f"N sweep: {N_values}")
    print(f"offset sweep: {offsets} at N={offset_layers}")
    print()

    for label, family, param in families:
        result = run_case(
            n=n,
            mass0=mass0,
            strength=strength,
            family=family,
            param=param,
            source_offset=source_offset,
            N_values=N_values,
            offsets=offsets,
            offset_layers=offset_layers,
        )
        results.append(result)
        print(f"[{label}]")
        print(f"  kernel param: {param}")
        print(f"  matched strength: {result.matched_strength:.6e}")
        print(f"  kernel sum: {result.kernel_sum:.6f}")
        print(f"  N biases: {fmt_bias_list(result.n_biases)}")
        print(f"  monotone increasing TOWARD bias over N: {'YES' if result.n_monotone else 'NO'}")
        print(f"  offset biases: {fmt_bias_list(result.offset_biases)}")
        print(f"  TOWARD count: {result.toward_count}/{len(offsets)}")
        if np.isnan(result.offset_alpha):
            print("  offset power law: not available (sign mix or zero values)")
        else:
            print(f"  offset power law: alpha={result.offset_alpha:.3f}, R^2={result.offset_r2:.4f}")
        print()

    baseline = results[0]
    best_n = max(results, key=lambda r: (r.n_monotone, r.toward_count, r.offset_r2))
    print("SUMMARY")
    print(
        f"  baseline localized_inverse: N-monotone={'YES' if baseline.n_monotone else 'NO'}, "
        f"offset TOWARD={baseline.toward_count}/{len(offsets)}, "
        f"offset R^2={baseline.offset_r2:.4f}"
    )
    print(
        f"  best profile by simple rank: {best_n.family} (param={best_n.param}) "
        f"N-monotone={'YES' if best_n.n_monotone else 'NO'}, "
        f"offset TOWARD={best_n.toward_count}/{len(offsets)}, "
        f"offset R^2={best_n.offset_r2:.4f}"
    )
    print(f"  runtime: {time.time() - start:.1f}s")


if __name__ == "__main__":
    main()
