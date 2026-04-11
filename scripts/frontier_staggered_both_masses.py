#!/usr/bin/env python3
"""
Staggered both-masses test on the open 3D cubic surface.

Goal:
  Test whether the blocked 2x2x2 staggered trajectory observable can support
  a genuine both-masses law on the same open cubic surface where the external-
  source staggered Newton reproduction succeeds.

Protocol:
  - open 3D staggered lattice
  - literature-correct parity coupling (m + Phi) * epsilon(x)
  - two separate orbitals placed along +z / -z
  - compare SHARED and SELF_ONLY evolutions
  - measure inward-positive early accelerations from the blocked centroid

Retained question:
  Does the blocked staggered observable support partner-mass linearity and
  force-balance well enough to call this a retained both-masses law?
"""

from __future__ import annotations

import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve


SIDE = 14
DT = 0.10
N_STEPS = 10
SIGMA = 1.30
G = 50.0
MU2 = 0.001
REG = 1e-3
SOURCE_SCALE = 5e-4
DISTANCE = 4
EARLY = slice(1, 6)
MASS_VALUES = (0.20, 0.30, 0.40)


class OpenStaggered3D:
    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self._fill_positions()
        self.lap = self._build_laplacian()

    def _fill_positions(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    self.pos[self.index(x, y, z)] = (x, y, z)

    def _build_laplacian(self) -> csc_matrix:
        lap = lil_matrix((self.n_sites, self.n_sites), dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    deg = 0
                    for dx, dy, dz in (
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < self.side and 0 <= ny < self.side and 0 <= nz < self.side:
                            j = self.index(nx, ny, nz)
                            lap[i, j] = -1.0
                            deg += 1
                    lap[i, i] = float(deg)
        return lap.tocsc()

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def gaussian(self, center: tuple[float, float, float], sigma: float = SIGMA) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma**2).astype(complex)
        return psi / np.linalg.norm(psi)

    def solve_potential(self, rho: np.ndarray) -> np.ndarray:
        op = self.lap + (MU2 + REG) * speye(self.n_sites, format="csc")
        rhs = G * SOURCE_SCALE * rho
        return -spsolve(op, rhs).real

    def build_hamiltonian(self, mass: float, phi: np.ndarray | None = None) -> csr_matrix:
        h = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x + 1 < self.side:
                        j = self.index(x + 1, y, z)
                        h[i, j] += -0.5j
                        h[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self.index(x, y + 1, z)
                        h[i, j] += eta_y * (-0.5j)
                        h[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self.index(x, y, z + 1)
                        h[i, j] += eta_z * (-0.5j)
                        h[j, i] += eta_z * (0.5j)
                    eps = (-1) ** (x + y + z)
                    phi_i = 0.0 if phi is None else float(phi[i])
                    h[i, i] += (mass + phi_i) * eps
        return h.tocsr()

    def evolve_step(self, h: csr_matrix, psi: np.ndarray) -> np.ndarray:
        aplus = (speye(self.n_sites, format="csc") + 1j * h * DT / 2).tocsc()
        aminus = speye(self.n_sites, format="csr") - 1j * h * DT / 2
        lu = splu(aplus)
        out = lu.solve(aminus.dot(psi))
        return out / np.linalg.norm(out)

    def blocked_centroid_z(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = 0.0
        moment = 0.0
        for x0 in range(0, self.side, 2):
            for y0 in range(0, self.side, 2):
                for z0 in range(0, self.side, 2):
                    weight = 0.0
                    for dx in (0, 1):
                        for dy in (0, 1):
                            for dz in (0, 1):
                                x = x0 + dx
                                y = y0 + dy
                                z = z0 + dz
                                if x < self.side and y < self.side and z < self.side:
                                    weight += rho[self.index(x, y, z)]
                    xc = min(z0 + 0.5, self.side - 1)
                    total += weight
                    moment += weight * xc
        return float(moment / total)


def acceleration(series: np.ndarray) -> np.ndarray:
    out = np.zeros_like(series)
    out[1:-1] = (series[2:] - 2 * series[1:-1] + series[:-2]) / DT**2
    out[0] = out[1]
    out[-1] = out[-2]
    return out


def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), float(intercept), r2


def coefficient_of_variation(values: list[float]) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=float)
    mean = float(np.mean(arr))
    std = float(np.std(arr))
    cv = abs(std / mean) if abs(mean) > 1e-30 else float("inf")
    return cv, mean, std


def run_pair(lat: OpenStaggered3D, mode: str, center_a, center_b, mass_a: float, mass_b: float):
    psi_a = lat.gaussian(center_a)
    psi_b = lat.gaussian(center_b)

    cx_a = np.zeros(N_STEPS + 1)
    cx_b = np.zeros(N_STEPS + 1)
    cx_a[0] = lat.blocked_centroid_z(psi_a)
    cx_b[0] = lat.blocked_centroid_z(psi_b)

    for t in range(N_STEPS):
        if mode == "SHARED":
            rho_total = mass_a * np.abs(psi_a) ** 2 + mass_b * np.abs(psi_b) ** 2
            phi = lat.solve_potential(rho_total)
            h_a = lat.build_hamiltonian(mass_a, phi)
            h_b = lat.build_hamiltonian(mass_b, phi)
        elif mode == "SELF_ONLY":
            phi_a = lat.solve_potential(mass_a * np.abs(psi_a) ** 2)
            phi_b = lat.solve_potential(mass_b * np.abs(psi_b) ** 2)
            h_a = lat.build_hamiltonian(mass_a, phi_a)
            h_b = lat.build_hamiltonian(mass_b, phi_b)
        else:
            raise ValueError(mode)

        psi_a = lat.evolve_step(h_a, psi_a)
        psi_b = lat.evolve_step(h_b, psi_b)
        cx_a[t + 1] = lat.blocked_centroid_z(psi_a)
        cx_b[t + 1] = lat.blocked_centroid_z(psi_b)

    return cx_a, cx_b


def main() -> None:
    t0 = time.time()
    center = 0.5 * (SIDE - 1)
    center_a = (center, center, center - DISTANCE / 2)
    center_b = (center, center, center + DISTANCE / 2)
    lat = OpenStaggered3D(SIDE)

    print("=" * 98)
    print("STAGGERED BOTH-MASSES TEST: BLOCKED 2x2x2 OPEN 3D SURFACE")
    print("=" * 98)
    print(
        f"side={SIDE}, d={DISTANCE}, G={G}, mu2={MU2}, source_scale={SOURCE_SCALE}, "
        f"dt={DT}, N_STEPS={N_STEPS}, sigma={SIGMA}"
    )
    print(f"mass grid={MASS_VALUES}")
    print("observable: a_A^mut = +(a_A^shared - a_A^self), a_B^mut = -(a_B^shared - a_B^self)")
    print("axis: blocked centroid along z (same clean axis as staggered Newton reproduction)")
    print()

    results: dict[tuple[float, float], dict[str, float]] = {}
    header = (
        f"{'M_A':>5s} {'M_B':>5s} | "
        f"{'a_A^mut':>11s} {'a_B^mut':>11s} {'a_close':>11s} | "
        f"{'F_A':>11s} {'F_B':>11s} {'relΔF':>9s}"
    )
    print(header)
    print("-" * len(header))

    for mass_a in MASS_VALUES:
        for mass_b in MASS_VALUES:
            cx_a_sh, cx_b_sh = run_pair(lat, "SHARED", center_a, center_b, mass_a, mass_b)
            cx_a_so, cx_b_so = run_pair(lat, "SELF_ONLY", center_a, center_b, mass_a, mass_b)

            a_a_sh = acceleration(cx_a_sh)
            a_b_sh = acceleration(cx_b_sh)
            a_a_so = acceleration(cx_a_so)
            a_b_so = acceleration(cx_b_so)

            a_a_mut = float(np.mean((a_a_sh - a_a_so)[EARLY]))
            a_b_mut = float(np.mean(-(a_b_sh - a_b_so)[EARLY]))
            a_close = 0.5 * (a_a_mut + a_b_mut)
            f_a = mass_a * a_a_mut
            f_b = mass_b * a_b_mut
            rel_df = abs(f_a - f_b) / max(abs(f_a) + abs(f_b), 1e-30)

            results[(mass_a, mass_b)] = {
                "a_a_mut": a_a_mut,
                "a_b_mut": a_b_mut,
                "a_close": a_close,
                "f_a": f_a,
                "f_b": f_b,
                "rel_df": rel_df,
                "a_a_per_mb": a_a_mut / mass_b,
                "a_b_per_ma": a_b_mut / mass_a,
            }

            print(
                f"{mass_a:5.1f} {mass_b:5.1f} | "
                f"{a_a_mut:+11.6e} {a_b_mut:+11.6e} {a_close:+11.6e} | "
                f"{f_a:+11.6e} {f_b:+11.6e} {rel_df:8.2%}"
            )

    print()
    print("Anchor fits")
    print("-" * 98)
    xs_mb = list(MASS_VALUES)
    ys_a = [results[(0.3, mb)]["a_a_mut"] for mb in MASS_VALUES]
    slope_a, intercept_a, r2_a = linear_fit(xs_mb, ys_a)
    print(
        "a_A^mut vs M_B at M_A=0.3: "
        f"a_A^mut = {slope_a:+.6e} * M_B + {intercept_a:+.6e}, R^2={r2_a:.6f}"
    )
    xs_ma = list(MASS_VALUES)
    ys_b = [results[(ma, 0.3)]["a_b_mut"] for ma in MASS_VALUES]
    slope_b, intercept_b, r2_b = linear_fit(xs_ma, ys_b)
    print(
        "a_B^mut vs M_A at M_B=0.3: "
        f"a_B^mut = {slope_b:+.6e} * M_A + {intercept_b:+.6e}, R^2={r2_b:.6f}"
    )
    xs_sum = [mass_a + mass_b for mass_a in MASS_VALUES for mass_b in MASS_VALUES]
    ys_close = [results[(mass_a, mass_b)]["a_close"] for mass_a in MASS_VALUES for mass_b in MASS_VALUES]
    slope_sum, intercept_sum, r2_sum = linear_fit(xs_sum, ys_close)
    print(
        "a_close vs (M_A + M_B): "
        f"a_close = {slope_sum:+.6e} * (M_A+M_B) + {intercept_sum:+.6e}, R^2={r2_sum:.6f}"
    )

    cv_a, mean_a, std_a = coefficient_of_variation([val["a_a_per_mb"] for val in results.values()])
    cv_b, mean_b, std_b = coefficient_of_variation([val["a_b_per_ma"] for val in results.values()])
    rel_dfs = [val["rel_df"] for val in results.values()]

    print()
    print("Full-grid normalization")
    print("-" * 98)
    print(f"a_A^mut / M_B: mean={mean_a:+.6e}, std={std_a:.6e}, CV={cv_a:.3%}")
    print(f"a_B^mut / M_A: mean={mean_b:+.6e}, std={std_b:.6e}, CV={cv_b:.3%}")
    print(
        "force-balance proxy: "
        f"mean relΔF={float(np.mean(rel_dfs)):.3%}, max relΔF={float(np.max(rel_dfs)):.3%}"
    )

    all_inward = all(val["a_a_mut"] > 0 and val["a_b_mut"] > 0 for val in results.values())
    print()
    print("Summary")
    print("-" * 98)
    print(f"all inward: {all_inward}")
    print(f"runtime={time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
