#!/usr/bin/env python3
"""
Wilson both-masses follow-up: packet-local antisymmetrized force-balance probe.

Why this exists:
  `frontier_wilson_both_masses_accel.py` established that the old integrated
  momentum residual was the wrong observable and that early mutual
  accelerations recover clean partner-mass linearity on anchor slices.
  What still failed was global force balance:

      F_A = M_A * a_A^mut
      F_B = M_B * a_B^mut

  with mean relative mismatch about 28%.

  That remaining failure may still be contaminated by a common slowdown mode
  because the observable uses whole-packet centroids. This runner keeps the
  same open Wilson surface but switches to packet-local centroids with fixed
  Gaussian windows anchored to the initial packet centers. The shared-self
  subtraction is unchanged; only the readout is localized.

What this tests:
  - whether local inward mutual response remains linear in the partner mass
  - whether a packet-local force-balance proxy is cleaner than the global one

What it does not test:
  - many-body Newton closure
  - cross-geometry robustness
  - architecture-independent universality
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


WILSON_R = 1.0
DT = 0.08
N_STEPS = 15
G_VAL = 5.0
MU2 = 0.001
REG = 1e-3
SIGMA = 1.0
SIDE = 20
D_SEP = 8
MASS_VALUES = (0.5, 1.0, 1.5, 2.0)
EARLY = slice(2, 8)
WINDOW_SIGMA = 1.5


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
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * sigma**2))
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho):
        op = self.lap - MU2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G_VAL * rho
        return spsolve(op.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi, inertial_mass):
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
            diag = inertial_mass + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def evolve_step(self, psi, hamiltonian):
        return expm_multiply(-1j * DT * hamiltonian, psi)


def acceleration(series):
    out = np.zeros(len(series))
    out[1:-1] = (series[2:] - 2 * series[1:-1] + series[:-2]) / DT**2
    out[0] = out[1]
    out[-1] = out[-2]
    return out


def linear_fit(xs, ys):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(xs, ys, 1)
    fit = slope * xs + intercept
    ss_res = float(np.sum((ys - fit) ** 2))
    ss_tot = float(np.sum((ys - np.mean(ys)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def coefficient_of_variation(values):
    values = np.asarray(values, dtype=float)
    mean = float(np.mean(values))
    std = float(np.std(values))
    if abs(mean) < 1e-30:
        return float("inf"), mean, std
    return abs(std / mean), mean, std


def make_window(lat: OpenWilsonLattice, center, sigma):
    cx, cy, cz = center
    dx = lat.pos[:, 0] - cx
    dy = lat.pos[:, 1] - cy
    dz = lat.pos[:, 2] - cz
    return np.exp(-(dx * dx + dy * dy + dz * dz) / (2.0 * sigma**2))


def local_centroid_x(lat: OpenWilsonLattice, psi: np.ndarray, window: np.ndarray):
    rho = np.abs(psi) ** 2
    weight = rho * window
    norm = float(np.sum(weight))
    return float(np.sum(weight * lat.pos[:, 0]) / max(norm, 1e-30))


def run_pair(lat, mode, center_a, center_b, window_a, window_b, mass_a, mass_b):
    psi_a = lat.gaussian_wavepacket(center_a)
    psi_b = lat.gaussian_wavepacket(center_b)

    xloc_a = np.zeros(N_STEPS + 1)
    xloc_b = np.zeros(N_STEPS + 1)
    xloc_a[0] = local_centroid_x(lat, psi_a, window_a)
    xloc_b[0] = local_centroid_x(lat, psi_b, window_b)

    for t in range(N_STEPS):
        if mode == "SHARED":
            rho_total = mass_a * np.abs(psi_a) ** 2 + mass_b * np.abs(psi_b) ** 2
            phi = lat.solve_poisson(rho_total)
            h_a = lat.build_wilson_hamiltonian(phi, mass_a)
            h_b = lat.build_wilson_hamiltonian(phi, mass_b)
        elif mode == "SELF_ONLY":
            phi_a = lat.solve_poisson(mass_a * np.abs(psi_a) ** 2)
            phi_b = lat.solve_poisson(mass_b * np.abs(psi_b) ** 2)
            h_a = lat.build_wilson_hamiltonian(phi_a, mass_a)
            h_b = lat.build_wilson_hamiltonian(phi_b, mass_b)
        else:
            raise ValueError(mode)

        psi_a = lat.evolve_step(psi_a, h_a)
        psi_b = lat.evolve_step(psi_b, h_b)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        xloc_a[t + 1] = local_centroid_x(lat, psi_a, window_a)
        xloc_b[t + 1] = local_centroid_x(lat, psi_b, window_b)

    return xloc_a, xloc_b


def main():
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    lat = OpenWilsonLattice(SIDE)
    window_a = make_window(lat, center_a, WINDOW_SIGMA)
    window_b = make_window(lat, center_b, WINDOW_SIGMA)

    print("=" * 104)
    print("OPEN WILSON BOTH-MASSES LOCAL ANTISYMMETRIZED FORCE-BALANCE TEST")
    print("=" * 104)
    print(
        f"Surface: side={SIDE}, d={D_SEP}, G={G_VAL}, mu2={MU2}, sigma={SIGMA}, "
        f"N_STEPS={N_STEPS}, window_sigma={WINDOW_SIGMA}"
    )
    print(f"Mass grid: {MASS_VALUES}")
    print()
    print("Local observables:")
    print("  x_A^loc, x_B^loc = packet-local x centroids in fixed Gaussian windows")
    print("  a_A^loc = +(x_A^loc,shared - x_A^loc,self)''   inward positive")
    print("  a_B^loc = -(x_B^loc,shared - x_B^loc,self)''   inward positive")
    print("  F_A^loc = M_A * a_A^loc")
    print("  F_B^loc = M_B * a_B^loc")
    print()

    results = {}
    header = (
        f"{'M_A':>5s} {'M_B':>5s} | "
        f"{'a_A^loc':>11s} {'a_B^loc':>11s} {'a_sym':>11s} | "
        f"{'F_A^loc':>11s} {'F_B^loc':>11s} {'relΔF':>9s}"
    )
    print(header)
    print("-" * len(header))

    t0 = time.time()
    for mass_a in MASS_VALUES:
        for mass_b in MASS_VALUES:
            x_a_sh, x_b_sh = run_pair(lat, "SHARED", center_a, center_b, window_a, window_b, mass_a, mass_b)
            x_a_so, x_b_so = run_pair(lat, "SELF_ONLY", center_a, center_b, window_a, window_b, mass_a, mass_b)

            a_a_loc = float(np.mean(acceleration(x_a_sh - x_a_so)[EARLY]))
            a_b_loc = float(np.mean(acceleration(-(x_b_sh - x_b_so))[EARLY]))
            a_sym = 0.5 * (a_a_loc + a_b_loc)
            f_a_loc = mass_a * a_a_loc
            f_b_loc = mass_b * a_b_loc
            rel_df = abs(f_a_loc - f_b_loc) / max(abs(f_a_loc) + abs(f_b_loc), 1e-30)

            results[(mass_a, mass_b)] = {
                "a_a_loc": a_a_loc,
                "a_b_loc": a_b_loc,
                "a_sym": a_sym,
                "f_a_loc": f_a_loc,
                "f_b_loc": f_b_loc,
                "rel_df": rel_df,
                "a_a_per_mb": a_a_loc / mass_b,
                "a_b_per_ma": a_b_loc / mass_a,
            }

            print(
                f"{mass_a:5.1f} {mass_b:5.1f} | "
                f"{a_a_loc:+11.6e} {a_b_loc:+11.6e} {a_sym:+11.6e} | "
                f"{f_a_loc:+11.6e} {f_b_loc:+11.6e} {rel_df:8.2%}"
            )

    grid_time = time.time() - t0
    print(f"\nGrid time: {grid_time:.1f}s")

    print()
    print("=" * 104)
    print("ANCHOR SLICE 1: a_A^loc vs M_B  (M_A = 1.0)")
    print("=" * 104)
    mb_vals = []
    a_a_vals = []
    for mass_b in MASS_VALUES:
        value = results[(1.0, mass_b)]["a_a_loc"]
        mb_vals.append(mass_b)
        a_a_vals.append(value)
        print(f"  M_B={mass_b:.1f}: a_A^loc = {value:+.6e}")
    slope_a, intercept_a, r2_a = linear_fit(mb_vals, a_a_vals)
    print(f"  fit: a_A^loc = {slope_a:+.6e} * M_B + {intercept_a:+.6e}   R^2={r2_a:.6f}")

    print()
    print("=" * 104)
    print("ANCHOR SLICE 2: a_B^loc vs M_A  (M_B = 1.0)")
    print("=" * 104)
    ma_vals = []
    a_b_vals = []
    for mass_a in MASS_VALUES:
        value = results[(mass_a, 1.0)]["a_b_loc"]
        ma_vals.append(mass_a)
        a_b_vals.append(value)
        print(f"  M_A={mass_a:.1f}: a_B^loc = {value:+.6e}")
    slope_b, intercept_b, r2_b = linear_fit(ma_vals, a_b_vals)
    print(f"  fit: a_B^loc = {slope_b:+.6e} * M_A + {intercept_b:+.6e}   R^2={r2_b:.6f}")

    print()
    print("=" * 104)
    print("FULL-GRID NORMALIZATION CHECKS")
    print("=" * 104)
    a_a_norm = [row["a_a_per_mb"] for row in results.values()]
    a_b_norm = [row["a_b_per_ma"] for row in results.values()]
    cv_a, mean_a, std_a = coefficient_of_variation(a_a_norm)
    cv_b, mean_b, std_b = coefficient_of_variation(a_b_norm)
    print(f"  a_A^loc / M_B: mean={mean_a:+.6e}, std={std_a:.6e}, CV={cv_a:.3%}")
    print(f"  a_B^loc / M_A: mean={mean_b:+.6e}, std={std_b:.6e}, CV={cv_b:.3%}")

    print()
    print("=" * 104)
    print("LOCAL FORCE-BALANCE CHECK")
    print("=" * 104)
    rel_vals = [row["rel_df"] for row in results.values()]
    print(f"  mean relative |F_A^loc - F_B^loc| / (|F_A^loc| + |F_B^loc|) = {np.mean(rel_vals):.3%}")
    print(f"  max relative |F_A^loc - F_B^loc| / (|F_A^loc| + |F_B^loc|) = {np.max(rel_vals):.3%}")

    print()
    ok_slice_a = r2_a > 0.98
    ok_slice_b = r2_b > 0.98
    ok_cv = cv_a < 0.15 and cv_b < 0.15
    ok_force = np.mean(rel_vals) < 0.15

    print("=" * 104)
    print("VERDICT")
    print("=" * 104)
    print(f"1. A-side partner-mass slice linear: {'YES' if ok_slice_a else 'NO'} (R^2={r2_a:.4f})")
    print(f"2. B-side partner-mass slice linear: {'YES' if ok_slice_b else 'NO'} (R^2={r2_b:.4f})")
    print(f"3. Grid-normalized local responses stable: {'YES' if ok_cv else 'NO'} (CVs {cv_a:.2%}, {cv_b:.2%})")
    print(f"4. Local force balance survives: {'YES' if ok_force else 'NO'} (mean relΔF {np.mean(rel_vals):.2%})")

    if ok_slice_a and ok_slice_b and ok_cv and ok_force:
        print("\nOVERALL: bounded both-masses closure survives on this fixed Wilson surface.")
    else:
        print("\nOVERALL: both-masses closure still fails on this fixed Wilson surface.")
        if not ok_slice_a or not ok_slice_b:
            print("  - partner-mass linearity is not strong enough on both anchor slices")
        if not ok_cv:
            print("  - normalized local responses drift too much across the grid")
        if not ok_force:
            print("  - equal-and-opposite local force balance does not hold cleanly")


if __name__ == "__main__":
    main()
