#!/usr/bin/env python3
"""Dirac 3+1D source smoothing scan.

This is a narrow follow-up to the historical Dirac walk v3/v4 harnesses.
It keeps the current best mass point fixed at m0=0.10 and asks a single
question:

    Does smoothing the initial source packet improve the remaining gravity
    failures?

The scan compares a point-like source against Gaussian source widths and
reports the exact signed readouts for:

  - N-growth at fixed offset
  - distance-law offsets at fixed N

The observables reuse the same periodic 3+1D Dirac walk structure as the
v3/v4 harnesses:

  - 4-component Dirac coin
  - periodic conditional shifts
  - spatially varying mass field m(r) = m0 * (1 + f(r))
  - signed side-band readout around the source
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np


GAMMA0 = np.diag([1, 1, -1, -1]).astype(complex)
GAMMA1 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, -1, 0, 0], [-1, 0, 0, 0]], dtype=complex)
GAMMA2 = np.array([[0, 0, 0, -1j], [0, 0, 1j, 0], [0, 1j, 0, 0], [-1j, 0, 0, 0]], dtype=complex)
GAMMA3 = np.array([[0, 0, 1, 0], [0, 0, 0, -1], [-1, 0, 0, 0], [0, 1, 0, 0]], dtype=complex)


def get_projectors(gp: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(gp)
    p_plus = sum(np.outer(evecs[:, i], evecs[:, i].conj()) for i in range(4) if evals[i] > 0)
    p_minus = sum(np.outer(evecs[:, i], evecs[:, i].conj()) for i in range(4) if evals[i] < 0)
    return p_plus, p_minus


PX_P, PX_M = get_projectors(GAMMA0 @ GAMMA1)
PY_P, PY_M = get_projectors(GAMMA0 @ GAMMA2)
PZ_P, PZ_M = get_projectors(GAMMA0 @ GAMMA3)


def coin_step(psi: np.ndarray, mass_field: np.ndarray) -> np.ndarray:
    cm = np.cos(mass_field)
    sm = np.sin(mass_field)
    out = np.zeros_like(psi)
    out[0] = (cm + 1j * sm) * psi[0]
    out[1] = (cm + 1j * sm) * psi[1]
    out[2] = (cm - 1j * sm) * psi[2]
    out[3] = (cm - 1j * sm) * psi[3]
    return out


def shift_dir(psi: np.ndarray, p_plus: np.ndarray, p_minus: np.ndarray, axis: int) -> np.ndarray:
    out = np.zeros_like(psi)
    for c in range(4):
        pp = sum(p_plus[c, d] * psi[d] for d in range(4))
        pm = sum(p_minus[c, d] * psi[d] for d in range(4))
        out[c] += np.roll(pp, -1, axis=axis)
        out[c] += np.roll(pm, +1, axis=axis)
    return out


def step_dirac(psi: np.ndarray, mass_field: np.ndarray) -> np.ndarray:
    psi = coin_step(psi, mass_field)
    psi = shift_dir(psi, PX_P, PX_M, 0)
    psi = shift_dir(psi, PY_P, PY_M, 1)
    psi = shift_dir(psi, PZ_P, PZ_M, 2)
    return psi


def min_image_dist(n: int, mass_pos: tuple[int, int, int]) -> np.ndarray:
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - mass_pos[0])
    dx = np.minimum(dx, n - dx)
    dy = np.abs(c[None, :, None] - mass_pos[1])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, None, :] - mass_pos[2])
    dz = np.minimum(dz, n - dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def make_mass_field(
    n: int,
    mass0: float,
    strength: float,
    mass_positions: list[tuple[int, int, int]] | None,
) -> np.ndarray:
    mf = np.full((n, n, n), mass0, dtype=float)
    if not mass_positions or strength <= 0:
        return mf

    total_f = np.zeros((n, n, n), dtype=float)
    for mp in mass_positions:
        total_f += strength / (min_image_dist(n, mp) + 0.1)
    return mass0 * (1.0 + total_f)


def normalize_state(psi: np.ndarray) -> np.ndarray:
    norm = float(np.sqrt(np.sum(np.abs(psi) ** 2)))
    return psi if norm <= 0 else psi / norm


def make_source_state(n: int, sigma: float) -> np.ndarray:
    """Create the initial source packet.

    sigma <= 0 is the point-like baseline used by the old harnesses.
    """
    center = n // 2
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    if sigma <= 0:
        psi[:, center, center, center] = 0.5
        return psi

    x, y, z = np.indices((n, n, n), dtype=float)
    dx = x - center
    dy = y - center
    dz = z - center
    env = np.exp(-0.5 * (dx**2 + dy**2 + dz**2) / (sigma**2))
    for comp in range(4):
        psi[comp] = 0.5 * env
    return normalize_state(psi)


def evolve(
    psi0: np.ndarray,
    mass0: float,
    strength: float,
    mass_positions: list[tuple[int, int, int]] | None,
    n_layers: int,
) -> np.ndarray:
    psi = np.array(psi0, dtype=np.complex128, copy=True)
    mf = make_mass_field(psi.shape[1], mass0, strength, mass_positions)
    for _ in range(n_layers):
        psi = step_dirac(psi, mf)
    return psi


def density(psi: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(psi) ** 2, axis=0)


def signed_sideband_readout(
    rho_field: np.ndarray,
    rho_free: np.ndarray,
    offset: int,
) -> tuple[float, float, float]:
    n = rho_field.shape[0]
    c = n // 2
    toward = float(np.sum(rho_field[c, c, c + 1 : c + offset + 1] - rho_free[c, c, c + 1 : c + offset + 1]))
    away = float(np.sum(rho_field[c, c, c - offset : c] - rho_free[c, c, c - offset : c]))
    return toward, away, toward - away


def fit_power_law(xs: Iterable[int], ys: Iterable[float]) -> tuple[float, float]:
    xs_arr = np.asarray(list(xs), dtype=float)
    ys_arr = np.asarray(list(ys), dtype=float)
    mask = ys_arr > 0
    if np.sum(mask) < 3:
        return float("nan"), 0.0
    lx = np.log(xs_arr[mask])
    ly = np.log(ys_arr[mask])
    coeffs = np.polyfit(lx, ly, 1)
    pred = np.polyval(coeffs, lx)
    ss_res = float(np.sum((ly - pred) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coeffs[0]), r2


def monotone_non_decreasing(values: list[float]) -> bool:
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


@dataclass(frozen=True)
class SweepResult:
    label: str
    sigma: float
    n_toward: int
    n_total: int
    n_grows: bool
    n_alpha: float
    n_r2: float
    offset_toward: int
    offset_total: int
    offset_alpha: float
    offset_r2: float
    n_rows: list[tuple[int, float, float, float]]
    offset_rows: list[tuple[int, float, float, float]]


def run_source_case(
    label: str,
    sigma: float,
    mass0: float,
    strength: float,
    n_growth: int,
    growth_layers: tuple[int, ...],
    growth_offset: int,
    n_distance: int,
    distance_layers: int,
    distance_offsets: tuple[int, ...],
) -> SweepResult:
    psi0_growth = make_source_state(n_growth, sigma)
    psi0_distance = make_source_state(n_distance, sigma)

    c_growth = n_growth // 2
    c_distance = n_distance // 2

    free_growth_cache: dict[int, np.ndarray] = {}
    field_growth_cache: dict[int, np.ndarray] = {}
    growth_rows: list[tuple[int, float, float, float]] = []

    for layers in growth_layers:
        rho_free = density(evolve(psi0_growth, mass0, 0.0, None, layers))
        rho_field = density(evolve(psi0_growth, mass0, strength, [(c_growth, c_growth, c_growth + growth_offset)], layers))
        toward, away, net = signed_sideband_readout(rho_field, rho_free, growth_offset)
        growth_rows.append((layers, toward, away, net))
        free_growth_cache[layers] = rho_free
        field_growth_cache[layers] = rho_field

    growth_nets = [row[3] for row in growth_rows]
    growth_toward = sum(net > 0 for net in growth_nets)
    growth_alpha = float("nan")
    growth_r2 = 0.0
    if growth_toward == len(growth_nets):
        growth_alpha, growth_r2 = fit_power_law(growth_layers, [abs(net) for net in growth_nets])

    offset_rows: list[tuple[int, float, float, float]] = []
    offset_nets: list[float] = []
    for offset in distance_offsets:
        rho_free = density(evolve(psi0_distance, mass0, 0.0, None, distance_layers))
        rho_field = density(evolve(psi0_distance, mass0, strength, [(c_distance, c_distance, c_distance + offset)], distance_layers))
        toward, away, net = signed_sideband_readout(rho_field, rho_free, offset)
        offset_rows.append((offset, toward, away, net))
        offset_nets.append(net)

    offset_toward = sum(net > 0 for net in offset_nets)
    offset_alpha = float("nan")
    offset_r2 = 0.0
    if offset_toward == len(offset_nets):
        offset_alpha, offset_r2 = fit_power_law(distance_offsets, [abs(net) for net in offset_nets])

    return SweepResult(
        label=label,
        sigma=sigma,
        n_toward=growth_toward,
        n_total=len(growth_nets),
        n_grows=monotone_non_decreasing([abs(net) for net in growth_nets]),
        n_alpha=growth_alpha,
        n_r2=growth_r2,
        offset_toward=offset_toward,
        offset_total=len(offset_nets),
        offset_alpha=offset_alpha,
        offset_r2=offset_r2,
        n_rows=growth_rows,
        offset_rows=offset_rows,
    )


def format_float(value: float) -> str:
    return f"{value:+.6e}"


def print_case(result: SweepResult) -> None:
    print()
    print("=" * 72)
    print(f"SOURCE CASE: {result.label} (sigma={result.sigma:.2f})")
    print("=" * 72)
    print("N-growth sweep")
    print("  N     toward         away           net        sign")
    for layers, toward, away, net in result.n_rows:
        sign = "TOWARD" if net > 0 else "AWAY"
        print(f"  {layers:2d}  {format_float(toward):>12s}  {format_float(away):>12s}  {format_float(net):>12s}  {sign}")
    print(
        "  summary: "
        f"{result.n_toward}/{result.n_total} TOWARD, "
        f"|net| monotone={ 'YES' if result.n_grows else 'NO' }, "
        f"power-law={result.n_alpha:.3f} (R^2={result.n_r2:.4f})"
        if result.n_toward == result.n_total
        else
        "  summary: "
        f"{result.n_toward}/{result.n_total} TOWARD, "
        f"|net| monotone={ 'YES' if result.n_grows else 'NO' }, "
        "power-law=n/a"
    )

    print("Distance-law offset sweep")
    print("  off    toward         away           net        sign")
    for offset, toward, away, net in result.offset_rows:
        sign = "TOWARD" if net > 0 else "AWAY"
        print(f"  {offset:3d}  {format_float(toward):>12s}  {format_float(away):>12s}  {format_float(net):>12s}  {sign}")
    print(
        "  summary: "
        f"{result.offset_toward}/{result.offset_total} TOWARD, "
        f"power-law={result.offset_alpha:.3f} (R^2={result.offset_r2:.4f})"
        if result.offset_toward == result.offset_total
        else
        "  summary: "
        f"{result.offset_toward}/{result.offset_total} TOWARD, power-law=n/a"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Dirac 3+1D source smoothing")
    parser.add_argument("--mass", type=float, default=0.10, help="fixed mass point (current note default)")
    parser.add_argument("--strength", type=float, default=5e-4, help="gravity strength")
    parser.add_argument("--growth-layers", default="6,8,10,12,14", help="comma-separated N values for the N-growth sweep")
    parser.add_argument("--growth-offset", type=int, default=3, help="mass offset for the N-growth sweep")
    parser.add_argument("--distance-layers", type=int, default=10, help="layers for the distance-law sweep")
    parser.add_argument("--distance-offsets", default="2,3,4,5", help="comma-separated offsets for the distance-law sweep")
    parser.add_argument(
        "--widths",
        default="point,0.75,1.25,2.00",
        help="comma-separated source widths; use point for the point-like baseline",
    )
    args = parser.parse_args()

    growth_layers = tuple(int(item.strip()) for item in args.growth_layers.split(",") if item.strip())
    distance_offsets = tuple(int(item.strip()) for item in args.distance_offsets.split(",") if item.strip())
    width_specs = [item.strip() for item in args.widths.split(",") if item.strip()]

    cases: list[tuple[str, float]] = []
    for item in width_specs:
        if item.lower() == "point":
            cases.append(("point", 0.0))
        else:
            cases.append((f"gaussian_{item}", float(item)))

    print("=" * 72)
    print("DIRAC 3+1D SOURCE SMOOTHING SCAN")
    print("=" * 72)
    print(f"fixed mass point m0={args.mass:.2f}")
    print(f"strength={args.strength:.1e}")
    print(f"N-growth sweep layers={growth_layers}, offset={args.growth_offset}")
    print(f"distance-law layers={args.distance_layers}, offsets={distance_offsets}")
    print(f"source widths={', '.join(name for name, _ in cases)}")

    results = [
        run_source_case(
            label=label,
            sigma=sigma,
            mass0=args.mass,
            strength=args.strength,
            n_growth=17,
            growth_layers=growth_layers,
            growth_offset=args.growth_offset,
            n_distance=21,
            distance_layers=args.distance_layers,
            distance_offsets=distance_offsets,
        )
        for label, sigma in cases
    ]

    for result in results:
        print_case(result)

    print()
    print("=" * 72)
    print("COMPARISON")
    print("=" * 72)
    print("label           sigma   N TOWARD   N mono   off TOWARD   off power-law")
    print("-" * 72)
    for result in results:
        n_alpha = "n/a" if math.isnan(result.n_alpha) else f"{result.n_alpha:+.3f}"
        off_alpha = "n/a" if math.isnan(result.offset_alpha) else f"{result.offset_alpha:+.3f}"
        print(
            f"{result.label:<14s}  {result.sigma:5.2f}   "
            f"{result.n_toward:>2d}/{result.n_total:<2d}     "
            f"{'YES' if result.n_grows else 'NO ':>3s}      "
            f"{result.offset_toward:>2d}/{result.offset_total:<2d}      "
            f"{n_alpha}/{off_alpha}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
