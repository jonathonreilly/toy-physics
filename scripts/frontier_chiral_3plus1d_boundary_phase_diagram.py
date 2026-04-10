#!/usr/bin/env python3
"""3+1D chiral boundary-condition phase diagram.

This scan asks whether the 3+1D gravity-sign windows are mostly recurrence /
torus artifacts or whether they survive when the boundary conditions change.

It keeps the underlying 3+1D factorized chiral walk fixed and varies:
  - boundary type: periodic, reflecting, open/absorbing
  - dimensionless propagation ratio lambda = L / n
  - dimensionless mass offset ratio delta = offset / n

For periodic boundaries, the primary observable is torus-aware:
  signed minimum-image displacement toward the mass.

For reflecting/open boundaries, the primary observable is non-periodic:
  the raw z-centroid shift.

The scan compares coherent, classical, and phase-kill propagation on the same
boundary class and reports whether TOWARD / AWAY sign windows persist.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable

import numpy as np


THETA0 = 0.3
STRENGTH = 5e-4
SIZES = (21, 31)
LAMBDA_TARGETS = (0.48, 0.57, 0.67, 0.76, 0.86)
DELTA_TARGETS = (0.10, 0.14, 0.19, 0.24, 0.29)
BOUNDARIES = ("periodic", "reflecting", "open")
MODES = ("coherent", "classical", "phase-kill")


@dataclass(frozen=True)
class Case:
    n: int
    layers: int
    offset: int
    lambda_ratio: float
    delta_ratio: float


def clamp_offset(offset: int, n: int) -> int:
    return max(1, min(offset, n // 2 - 1))


def make_case(n: int, lambda_target: float, delta_target: float) -> Case:
    layers = max(1, int(round(lambda_target * n)))
    offset = clamp_offset(int(round(delta_target * n)), n)
    return Case(
        n=n,
        layers=layers,
        offset=offset,
        lambda_ratio=layers / n,
        delta_ratio=offset / n,
    )


def make_field(n: int, center: int, mass: tuple[int, int, int], boundary: str) -> np.ndarray:
    y, z, w = np.meshgrid(
        np.arange(n, dtype=float),
        np.arange(n, dtype=float),
        np.arange(n, dtype=float),
        indexing="ij",
    )
    my, mz, mw = mass

    if boundary == "periodic":
        dy = np.minimum(np.abs(y - my), n - np.abs(y - my))
        dz = np.minimum(np.abs(z - mz), n - np.abs(z - mz))
        dw = np.minimum(np.abs(w - mw), n - np.abs(w - mw))
    else:
        dy = np.abs(y - my)
        dz = np.abs(z - mz)
        dw = np.abs(w - mw)

    r = np.sqrt(dy**2 + dz**2 + dw**2)
    return STRENGTH / (r + 0.1)


def init_coherent_state(n: int) -> np.ndarray:
    state = np.zeros((n, n, n, 6), dtype=np.complex128)
    center = n // 2
    state[center, center, center, :] = 1.0 / np.sqrt(6.0)
    return state


def init_classical_state(n: int) -> np.ndarray:
    state = np.zeros((n, n, n, 6), dtype=float)
    center = n // 2
    state[center, center, center, :] = 1.0 / 6.0
    return state


def coin_coherent(state: np.ndarray, field: np.ndarray) -> np.ndarray:
    flat = state.reshape(-1, 6)
    theta = THETA0 * (1.0 - field.reshape(-1))
    ct = np.cos(theta)
    st = 1j * np.sin(theta)

    for a, b in ((0, 1), (2, 3), (4, 5)):
        plus = flat[:, a].copy()
        minus = flat[:, b].copy()
        flat[:, a] = ct * plus + st * minus
        flat[:, b] = st * plus + ct * minus

    return flat.reshape(state.shape)


def coin_classical(prob: np.ndarray, field: np.ndarray) -> np.ndarray:
    flat = prob.reshape(-1, 6)
    theta = THETA0 * (1.0 - field.reshape(-1))
    c2 = np.cos(theta) ** 2
    s2 = np.sin(theta) ** 2

    for a, b in ((0, 1), (2, 3), (4, 5)):
        plus = flat[:, a].copy()
        minus = flat[:, b].copy()
        flat[:, a] = c2 * plus + s2 * minus
        flat[:, b] = s2 * plus + c2 * minus

    return flat.reshape(prob.shape)


def shift_periodic(state: np.ndarray) -> np.ndarray:
    out = np.zeros_like(state)
    out[:, :, :, 0] = np.roll(state[:, :, :, 0], 1, axis=0)
    out[:, :, :, 1] = np.roll(state[:, :, :, 1], -1, axis=0)
    out[:, :, :, 2] = np.roll(state[:, :, :, 2], 1, axis=1)
    out[:, :, :, 3] = np.roll(state[:, :, :, 3], -1, axis=1)
    out[:, :, :, 4] = np.roll(state[:, :, :, 4], 1, axis=2)
    out[:, :, :, 5] = np.roll(state[:, :, :, 5], -1, axis=2)
    return out


def shift_reflecting(state: np.ndarray) -> np.ndarray:
    out = np.zeros_like(state)

    # y-axis pair
    out[1:, :, :, 0] += state[:-1, :, :, 0]
    out[-1, :, :, 1] += state[-1, :, :, 0]
    out[:-1, :, :, 1] += state[1:, :, :, 1]
    out[0, :, :, 0] += state[0, :, :, 1]

    # z-axis pair
    out[:, 1:, :, 2] += state[:, :-1, :, 2]
    out[:, -1, :, 3] += state[:, -1, :, 2]
    out[:, :-1, :, 3] += state[:, 1:, :, 3]
    out[:, 0, :, 2] += state[:, 0, :, 3]

    # w-axis pair
    out[:, :, 1:, 4] += state[:, :, :-1, 4]
    out[:, :, -1, 5] += state[:, :, -1, 4]
    out[:, :, :-1, 5] += state[:, :, 1:, 5]
    out[:, :, 0, 4] += state[:, :, 0, 5]

    return out


def shift_open(state: np.ndarray) -> np.ndarray:
    out = np.zeros_like(state)

    # y-axis pair
    out[1:, :, :, 0] += state[:-1, :, :, 0]
    out[:-1, :, :, 1] += state[1:, :, :, 1]

    # z-axis pair
    out[:, 1:, :, 2] += state[:, :-1, :, 2]
    out[:, :-1, :, 3] += state[:, 1:, :, 3]

    # w-axis pair
    out[:, :, 1:, 4] += state[:, :, :-1, 4]
    out[:, :, :-1, 5] += state[:, :, 1:, 5]

    return out


def site_prob(state: np.ndarray, classical: bool) -> np.ndarray:
    if classical:
        return np.sum(state, axis=-1)
    return np.sum(np.abs(state) ** 2, axis=-1)


def z_marginal(prob: np.ndarray) -> np.ndarray:
    return np.sum(prob, axis=(0, 2))


def raw_z_expectation(prob: np.ndarray) -> float:
    total = float(np.sum(prob))
    if total <= 1e-30:
        return 0.0
    zs = np.arange(prob.shape[1], dtype=float)
    return float(np.dot(zs, z_marginal(prob)) / total)


def torus_z_expectation(prob: np.ndarray, center: int) -> float:
    total = float(np.sum(prob))
    if total <= 1e-30:
        return 0.0
    zs = np.arange(prob.shape[1], dtype=float) - float(center)
    half = prob.shape[1] // 2
    zs[zs > half] -= prob.shape[1]
    zs[zs < -half] += prob.shape[1]
    return float(np.dot(zs, z_marginal(prob)) / total)


def evolve(boundary: str, mode: str, n: int, layers: int, offset: int) -> tuple[np.ndarray, float]:
    center = n // 2
    mass = (center, center + offset, center)
    field = make_field(n, center, mass, boundary)

    if mode == "classical":
        state = init_classical_state(n)
    else:
        state = init_coherent_state(n)

    for _ in range(layers):
        if mode == "classical":
            state = coin_classical(state, field)
        else:
            state = coin_coherent(state, field)

        if boundary == "periodic":
            state = shift_periodic(state)
        elif boundary == "reflecting":
            state = shift_reflecting(state)
        else:
            state = shift_open(state)

        if mode == "phase-kill":
            state = np.abs(state).astype(np.complex128)

    prob = site_prob(state, classical=(mode == "classical"))
    return prob, float(np.sum(prob))


def sign(delta: float) -> str:
    return "T" if delta > 0.0 else "A"


def aggregate_sign(values: Iterable[float]) -> str:
    vals = list(values)
    if not vals:
        return "."
    signs = {sign(v) for v in vals}
    if len(signs) == 1:
        return next(iter(signs))
    return "M"


def run_case(boundary: str, mode: str, n: int, layers: int, offset: int) -> dict[str, float]:
    center = n // 2
    free_prob, free_norm = evolve(boundary, mode, n, layers, 0)
    mass_prob, mass_norm = evolve(boundary, mode, n, layers, offset)

    if boundary == "periodic":
        free_obs = torus_z_expectation(free_prob, center)
        mass_obs = torus_z_expectation(mass_prob, center)
        free_raw = raw_z_expectation(free_prob)
        mass_raw = raw_z_expectation(mass_prob)
    else:
        free_obs = raw_z_expectation(free_prob)
        mass_obs = raw_z_expectation(mass_prob)
        free_raw = free_obs
        mass_raw = mass_obs

    return {
        "delta_obs": mass_obs - free_obs,
        "delta_raw": mass_raw - free_raw,
        "free_norm": free_norm,
        "mass_norm": mass_norm,
    }


def build_grid(boundary: str, mode: str) -> dict[tuple[float, float], list[tuple[float, float, float, float]]]:
    grid: dict[tuple[float, float], list[tuple[float, float, float, float]]] = {}
    for n in SIZES:
        for lambda_target in LAMBDA_TARGETS:
            case_layers = max(1, int(round(lambda_target * n)))
            lambda_ratio = case_layers / n
            for delta_target in DELTA_TARGETS:
                case_offset = clamp_offset(int(round(delta_target * n)), n)
                delta_ratio = case_offset / n
                result = run_case(boundary, mode, n, case_layers, case_offset)
                grid.setdefault((delta_target, lambda_target), []).append(
                    (
                        delta_ratio,
                        lambda_ratio,
                        result["delta_obs"],
                        result["delta_raw"],
                    )
                )
    return grid


def summarize_grid(grid: dict[tuple[float, float], list[tuple[float, float, float, float]]],
                   periodic: bool) -> tuple[list[str], int, int, int]:
    rows = []
    toward = away = mixed = 0
    for delta_target in DELTA_TARGETS:
        cells = []
        for lambda_target in LAMBDA_TARGETS:
            vals = grid[(delta_target, lambda_target)]
            obs_vals = [v[2] for v in vals]
            if periodic:
                raw_vals = [v[3] for v in vals]
                obs_cell = aggregate_sign(obs_vals)
                raw_cell = aggregate_sign(raw_vals)
                cell = f"{obs_cell}/{raw_cell}"
                if obs_cell == "T":
                    toward += 1
                elif obs_cell == "A":
                    away += 1
                else:
                    mixed += 1
            else:
                cell = aggregate_sign(obs_vals)
                if cell == "T":
                    toward += 1
                elif cell == "A":
                    away += 1
                else:
                    mixed += 1
            cells.append(cell)
        rows.append(" ".join(f"{cell:^7s}" for cell in cells))
    return rows, toward, away, mixed


def print_grid(boundary: str, mode: str, rows: list[str]) -> None:
    header = "delta \\ lambda | " + " | ".join(f"{lam:>6.2f}" for lam in LAMBDA_TARGETS)
    print(f"\n[{boundary.upper()}] mode={mode}")
    print(header)
    print("-" * len(header))
    for delta_target, row in zip(DELTA_TARGETS, rows):
        print(f"{delta_target:>12.2f} | {row}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--boundary",
        choices=BOUNDARIES + ("all",),
        default="all",
        help="Restrict the scan to one boundary class.",
    )
    parser.add_argument(
        "--mode",
        choices=MODES + ("all",),
        default="all",
        help="Restrict the scan to one propagation mode.",
    )
    args = parser.parse_args()

    boundaries = BOUNDARIES if args.boundary == "all" else (args.boundary,)
    modes = MODES if args.mode == "all" else (args.mode,)

    print("=" * 86)
    print("FRONTIER: 3+1D CHIRAL BOUNDARY-PHASE DIAGRAM")
    print("=" * 86)
    print(f"theta0={THETA0}, strength={STRENGTH}")
    print(f"sizes={SIZES}")
    print(f"lambda targets={LAMBDA_TARGETS}")
    print(f"delta targets={DELTA_TARGETS}")
    print("periodic uses torus-aware z expectation; others use raw z centroid")
    print()

    total_cases = 0
    boundary_away: dict[tuple[str, str], int] = {}
    periodic_torus_sensitive = 0

    for boundary in boundaries:
        for mode in modes:
            grid = build_grid(boundary, mode)
            rows, toward, away, mixed = summarize_grid(grid, periodic=(boundary == "periodic"))
            print_grid(boundary, mode, rows)

            total = len(DELTA_TARGETS) * len(LAMBDA_TARGETS)
            total_cases += total * len(SIZES)
            if boundary == "periodic":
                print(
                    f"  consensus cells: T={toward}, A={away}, mixed={mixed} "
                    f"out of {total} ratio cells (each cell aggregates {len(SIZES)} sizes)"
                )
                torus_mismatch = 0
                for key, vals in grid.items():
                    obs_vals = [v[2] for v in vals]
                    raw_vals = [v[3] for v in vals]
                    if aggregate_sign(obs_vals) != aggregate_sign(raw_vals):
                        torus_mismatch += 1
                periodic_torus_sensitive += torus_mismatch
                print(f"  torus-sensitive cells (torus vs raw sign mismatch): {torus_mismatch}")
            else:
                print(
                    f"  consensus cells: T={toward}, A={away}, mixed={mixed} "
                    f"out of {total} ratio cells (each cell aggregates {len(SIZES)} sizes)"
                )

            away_cells = [
                (delta_target, lambda_target)
                for delta_target in DELTA_TARGETS
                for lambda_target in LAMBDA_TARGETS
                if aggregate_sign([v[2] for v in grid[(delta_target, lambda_target)]]) == "A"
            ]
            boundary_away[(boundary, mode)] = len(away_cells)
            print(f"  AWAY consensus cells: {away_cells or 'none'}")

    print("\n" + "=" * 86)
    print("SUMMARY")
    print("=" * 86)
    for boundary in boundaries:
        for mode in modes:
            print(
                f"{boundary:>10s} / {mode:>10s}: "
                f"AWAY consensus cells = {boundary_away[(boundary, mode)]}"
            )
    if "periodic" in boundaries:
        print(f"periodic torus-sensitive cells = {periodic_torus_sensitive}")
    print(
        "Interpretation: AWAY windows that vanish under reflecting/open boundaries "
        "or disappear when the periodic observable is torus-aware are consistent "
        "with recurrence artifacts; AWAY windows that persist across all three "
        "boundary classes are structural."
    )
    print(f"Total raw cases evaluated: {total_cases}")


if __name__ == "__main__":
    main()
