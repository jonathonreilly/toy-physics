#!/usr/bin/env python3
"""
Open-Wilson both-masses follow-up with antisymmetrized early accelerations.

Why this exists:
  The earlier `frontier_newton_both_masses.py` runner used early-time momentum
  transfer from velocity residuals:

      P_A^mut = M_A * <v_A^shared - v_A^self>
      P_B^mut = M_B * <v_B^self - v_B^shared>

  That residual failed once both inertial masses varied because the common
  Wilson-gap slowdown dominated the integrated velocity shift.

This runner switches to a cleaner short-time observable on the same Wilson lane:
  - open 3D Wilson lattice
  - weak screening mu^2 = 0.001
  - side = 20 (same clean surface as the recent open-Wilson attraction run)
  - two separate orbitals at fixed separation d = 8
  - both source and inertial masses varied independently
  - retained observables are inward-positive early accelerations

      a_A^mut = +(a_A^shared - a_A^self)
      a_B^mut = -(a_B^shared - a_B^self)

  and the associated force-balance proxy

      F_A = M_A * a_A^mut
      F_B = M_B * a_B^mut

What this can close:
  - whether A's inward acceleration is linear in partner mass M_B
  - whether B's inward acceleration is linear in partner mass M_A
  - whether the equal-and-opposite force proxy survives on this surface

What it still cannot prove:
  - a many-body Newton closure
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

    def center_of_mass_x(self, psi):
        rho = np.abs(psi) ** 2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))

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


def run_pair(lat, mode, center_a, center_b, mass_a, mass_b):
    psi_a = lat.gaussian_wavepacket(center_a)
    psi_b = lat.gaussian_wavepacket(center_b)

    cx_a = np.zeros(N_STEPS + 1)
    cx_b = np.zeros(N_STEPS + 1)
    cx_a[0] = lat.center_of_mass_x(psi_a)
    cx_b[0] = lat.center_of_mass_x(psi_b)

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
        cx_a[t + 1] = lat.center_of_mass_x(psi_a)
        cx_b[t + 1] = lat.center_of_mass_x(psi_b)

    return cx_a, cx_b


def main():
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    lat = OpenWilsonLattice(SIDE)

    print("=" * 98)
    print("OPEN WILSON BOTH-MASSES ANTISYMMETRIZED ACCELERATION TEST")
    print("=" * 98)
    print(f"Surface: side={SIDE}, d={D_SEP}, G={G_VAL}, mu2={MU2}, sigma={SIGMA}, N_STEPS={N_STEPS}")
    print(f"Mass grid: {MASS_VALUES}")
    print()
    print("Observables:")
    print("  a_A^mut = +(a_A^shared - a_A^self)   inward positive")
    print("  a_B^mut = -(a_B^shared - a_B^self)   inward positive")
    print("  F_A = M_A * a_A^mut")
    print("  F_B = M_B * a_B^mut")
    print()

    results = {}
    header = (
        f"{'M_A':>5s} {'M_B':>5s} | "
        f"{'a_A^mut':>11s} {'a_B^mut':>11s} {'a_close':>11s} | "
        f"{'F_A':>11s} {'F_B':>11s} {'relΔF':>9s}"
    )
    print(header)
    print("-" * len(header))

    t0 = time.time()
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

    print(f"\nGrid time: {time.time() - t0:.1f}s")

    print()
    print("=" * 98)
    print("ANCHOR SLICE 1: a_A^mut vs M_B  (M_A = 1.0)")
    print("=" * 98)
    mb_vals = []
    a_a_vals = []
    for mass_b in MASS_VALUES:
        value = results[(1.0, mass_b)]["a_a_mut"]
        mb_vals.append(mass_b)
        a_a_vals.append(value)
        print(f"  M_B={mass_b:.1f}: a_A^mut = {value:+.6e}")
    slope_a, intercept_a, r2_a = linear_fit(mb_vals, a_a_vals)
    print(f"  fit: a_A^mut = {slope_a:+.6e} * M_B + {intercept_a:+.6e}   R^2={r2_a:.6f}")

    print()
    print("=" * 98)
    print("ANCHOR SLICE 2: a_B^mut vs M_A  (M_B = 1.0)")
    print("=" * 98)
    ma_vals = []
    a_b_vals = []
    for mass_a in MASS_VALUES:
        value = results[(mass_a, 1.0)]["a_b_mut"]
        ma_vals.append(mass_a)
        a_b_vals.append(value)
        print(f"  M_A={mass_a:.1f}: a_B^mut = {value:+.6e}")
    slope_b, intercept_b, r2_b = linear_fit(ma_vals, a_b_vals)
    print(f"  fit: a_B^mut = {slope_b:+.6e} * M_A + {intercept_b:+.6e}   R^2={r2_b:.6f}")

    print()
    print("=" * 98)
    print("FULL-GRID NORMALIZATION CHECKS")
    print("=" * 98)
    a_a_norm = [row["a_a_per_mb"] for row in results.values()]
    a_b_norm = [row["a_b_per_ma"] for row in results.values()]
    cv_a, mean_a, std_a = coefficient_of_variation(a_a_norm)
    cv_b, mean_b, std_b = coefficient_of_variation(a_b_norm)
    print(f"  a_A^mut / M_B: mean={mean_a:+.6e}, std={std_a:.6e}, CV={cv_a:.3%}")
    print(f"  a_B^mut / M_A: mean={mean_b:+.6e}, std={std_b:.6e}, CV={cv_b:.3%}")

    print()
    print("=" * 98)
    print("FORCE-BALANCE CHECK")
    print("=" * 98)
    rel_vals = [row["rel_df"] for row in results.values()]
    print(f"  mean relative |F_A - F_B| / (|F_A| + |F_B|) = {np.mean(rel_vals):.3%}")
    print(f"  max relative |F_A - F_B| / (|F_A| + |F_B|) = {np.max(rel_vals):.3%}")

    print()
    ok_slice_a = r2_a > 0.98
    ok_slice_b = r2_b > 0.98
    ok_cv = cv_a < 0.15 and cv_b < 0.15
    ok_force = np.mean(rel_vals) < 0.15

    print("=" * 98)
    print("VERDICT")
    print("=" * 98)
    print(f"1. A-side partner-mass slice linear: {'YES' if ok_slice_a else 'NO'} (R^2={r2_a:.4f})")
    print(f"2. B-side partner-mass slice linear: {'YES' if ok_slice_b else 'NO'} (R^2={r2_b:.4f})")
    print(f"3. Grid-normalized accelerations stable: {'YES' if ok_cv else 'NO'} (CVs {cv_a:.2%}, {cv_b:.2%})")
    print(f"4. Force balance survives: {'YES' if ok_force else 'NO'} (mean relΔF {np.mean(rel_vals):.2%})")

    if ok_slice_a and ok_slice_b and ok_cv and ok_force:
        print("\nOVERALL: bounded both-masses closure survives on this fixed Wilson surface.")
    else:
        print("\nOVERALL: both-masses closure still fails on this fixed Wilson surface.")
        if not ok_slice_a or not ok_slice_b:
            print("  - partner-mass linearity is not strong enough on both anchor slices")
        if not ok_cv:
            print("  - normalized per-partner accelerations drift too much across the grid")
        if not ok_force:
            print("  - equal-and-opposite force balance does not hold cleanly")


if __name__ == "__main__":
    main()
