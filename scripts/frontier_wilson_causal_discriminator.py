#!/usr/bin/env python3
"""
Wilson causal-discriminator probe on the open 3D cubic family.

This is a different discriminator from the failed SHARED/SELF_ONLY/FROZEN_SOURCE
comparison. Instead of asking whether a frozen field can mimic the signal, this
probe asks whether the mutual channel changes when the source refresh is delayed
by one or two time steps on the same open Wilson surface.

Modes:
  - SHARED_NOW: source is updated from the current total density each step
  - LAG1: source is updated from the previous step's total density
  - LAG2: source is updated from two steps back

The discriminator is the early-time mutual acceleration of the packet
separation. If the lagged modes track SHARED_NOW too closely, the causal timing
is not isolated on this surface. If they split cleanly, the shared backreaction
is temporally discriminated.
"""

from __future__ import annotations

import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import expm_multiply, splu, spsolve


MASS = 0.30
WILSON_R = 1.0
MU2 = 0.001
REG = 1e-6
DT = 0.08
N_STEPS = 15
G = 5.0
SIGMA = 1.0
SIDE = 20
SEPARATION = 8
PLACEMENT = "centered"
N_SEEDS = 5
SEEDS = tuple(range(N_SEEDS))
EARLY = slice(2, 8)


class OpenWilsonLattice:
    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = x * side**2 + y * side + z
                    self.pos[i] = [x, y, z]
                    nbrs: list[int] = []
                    for dx, dy, dz in (
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            nbrs.append(nx * side**2 + ny * side + nz)
                    self.adj[i] = nbrs
        self.lap = self._build_laplacian()

    def _build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return csc_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian_wavepacket(self, center, rng=None):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * SIGMA**2))
        if rng is not None:
            phases = rng.uniform(0.0, 0.1, self.n)
            psi *= np.exp(1j * phases)
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho):
        op = self.lap - MU2 * speye(self.n, format="csc") - REG * speye(self.n, format="csc")
        rhs = -4.0 * np.pi * G * rho
        return spsolve(op, rhs).real

    def build_wilson_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def evolve_step(self, psi, hamiltonian):
        return expm_multiply(-1j * DT * hamiltonian, psi)

    def center_of_mass_x(self, psi):
        rho = np.abs(psi) ** 2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))


def acceleration(series):
    out = np.zeros(len(series))
    out[1:-1] = (series[2:] - 2 * series[1:-1] + series[:-2]) / DT**2
    out[0] = out[1]
    out[-1] = out[-2]
    return out


def linear_fit(xs, ys):
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), float(intercept), r2


def placement_coords(side: int) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    center = 0.5 * (side - 1)
    x_a = center - SEPARATION / 2.0
    x_b = center + SEPARATION / 2.0
    return (x_a, center, center), (x_b, center, center)


def run_mode(lat: OpenWilsonLattice, mode: str, seed: int):
    center_a, center_b = placement_coords(lat.side)
    rng_a = np.random.default_rng(10_000 + seed * 2 + 1)
    rng_b = np.random.default_rng(10_000 + seed * 2 + 2)
    psi_a = lat.gaussian_wavepacket(center_a, rng=rng_a)
    psi_b = lat.gaussian_wavepacket(center_b, rng=rng_b)

    rho_hist: list[np.ndarray] = []
    sep = np.zeros(N_STEPS + 1)
    sep[0] = lat.center_of_mass_x(psi_b) - lat.center_of_mass_x(psi_a)

    for t in range(N_STEPS):
        rho_now = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
        rho_hist.append(rho_now.copy())

        if mode == "SHARED_NOW":
            rho_source = rho_now
        elif mode == "LAG1":
            rho_source = rho_hist[-2] if len(rho_hist) >= 2 else rho_now
        elif mode == "LAG2":
            rho_source = rho_hist[-3] if len(rho_hist) >= 3 else rho_now
        else:
            raise ValueError(mode)

        phi = lat.solve_poisson(rho_source)
        h = lat.build_wilson_hamiltonian(phi)
        psi_a = lat.evolve_step(psi_a, h)
        psi_b = lat.evolve_step(psi_b, h)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        sep[t + 1] = lat.center_of_mass_x(psi_b) - lat.center_of_mass_x(psi_a)

    a = acceleration(sep)
    mean = float(np.mean(a[EARLY]))
    std = float(np.std(a[EARLY]))
    return {
        "mode": mode,
        "seed": seed,
        "sep0": float(sep[0]),
        "sep1": float(sep[-1]),
        "a_mean": mean,
        "a_std": std,
        "snr": abs(mean) / (std + 1e-12),
        "series": a,
    }


def summarize(rows: list[dict[str, float]]) -> None:
    modes = ("SHARED_NOW", "LAG1", "LAG2")
    summary = {}
    for mode in modes:
        sub = [r for r in rows if r["mode"] == mode]
        means = np.array([r["a_mean"] for r in sub], dtype=float)
        summary[mode] = {
            "mean": float(np.mean(means)),
            "std": float(np.std(means)),
            "snr_mean": float(np.mean([r["snr"] for r in sub])),
        }

    gap1 = np.array([r["a_mean"] for r in rows if r["mode"] == "LAG1"]) - np.array(
        [r["a_mean"] for r in rows if r["mode"] == "SHARED_NOW"]
    )
    gap2 = np.array([r["a_mean"] for r in rows if r["mode"] == "LAG2"]) - np.array(
        [r["a_mean"] for r in rows if r["mode"] == "SHARED_NOW"]
    )

    print()
    print("=" * 92)
    print("SUMMARY")
    print("=" * 92)
    for mode in modes:
        print(
            f"{mode:>10s}: mean a={summary[mode]['mean']:+.6e} "
            f"std={summary[mode]['std']:.6e} mean SNR={summary[mode]['snr_mean']:.2f}"
        )
    print(f"LAG1 - SHARED_NOW: mean={np.mean(gap1):+.6e} std={np.std(gap1):.6e}")
    print(f"LAG2 - SHARED_NOW: mean={np.mean(gap2):+.6e} std={np.std(gap2):.6e}")

    gap1_abs = abs(np.mean(gap1)) / max(abs(summary["SHARED_NOW"]["mean"]), 1e-30)
    gap2_abs = abs(np.mean(gap2)) / max(abs(summary["SHARED_NOW"]["mean"]), 1e-30)
    print(f"Relative lag1 gap: {gap1_abs:.2%}")
    print(f"Relative lag2 gap: {gap2_abs:.2%}")

    shared = [r["a_mean"] for r in rows if r["mode"] == "SHARED_NOW"]
    lag1 = [r["a_mean"] for r in rows if r["mode"] == "LAG1"]
    lag2 = [r["a_mean"] for r in rows if r["mode"] == "LAG2"]
    if len(shared) >= 2:
        s1, i1, r2_1 = linear_fit(range(len(shared)), shared)
        s2, i2, r2_2 = linear_fit(range(len(lag1)), lag1)
        print(f"shared drift fit: slope={s1:+.3e}, R^2={r2_1:.4f}")
        print(f"lag1 drift fit:   slope={s2:+.3e}, R^2={r2_2:.4f}")

    lag1_consistent = np.all(gap1 > 0) or np.all(gap1 < 0)
    lag2_consistent = np.all(gap2 > 0) or np.all(gap2 < 0)
    small_gap = abs(np.mean(gap1)) < 0.05 * max(abs(summary["SHARED_NOW"]["mean"]), 1e-30)

    print()
    print("=" * 92)
    print("VERDICT")
    print("=" * 92)
    if lag1_consistent and lag2_consistent and not small_gap:
        print(
            "Lagged source refresh cleanly separates the mutual channel from the current shared update."
        )
        print(
            "This would support a genuine causal timing discriminator on this fixed Wilson surface."
        )
    else:
        print(
            "Lagged source refresh does not cleanly separate the mutual channel on this surface."
        )
        print(
            "The response is too adiabatic / too close to the shared update to promote as a causal proof."
        )


def main() -> None:
    t0 = time.time()
    print("=" * 92)
    print("WILSON CAUSAL DISCRIMINATOR")
    print("=" * 92)
    print(f"surface: open 3D Wilson, side={SIDE}, d={SEPARATION}, placement={PLACEMENT}")
    print(f"G={G}, mu2={MU2}, mass={MASS}, sigma={SIGMA}, dt={DT}, N_STEPS={N_STEPS}")
    print("modes: SHARED_NOW vs LAG1 vs LAG2")
    print("observable: early-time mutual acceleration of the packet separation")
    print()

    lat = OpenWilsonLattice(SIDE)
    rows: list[dict[str, float]] = []
    for seed in SEEDS:
        for mode in ("SHARED_NOW", "LAG1", "LAG2"):
            row = run_mode(lat, mode, seed)
            rows.append(row)
            print(
                f"seed={seed:2d} mode={mode:10s} "
                f"a_mean={row['a_mean']:+.6e} a_std={row['a_std']:.6e} "
                f"SNR={row['snr']:.2f} sep0={row['sep0']:.4f} sep1={row['sep1']:.4f}"
            )
        print()

    summarize(rows)
    print(f"\nelapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
