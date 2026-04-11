#!/usr/bin/env python3
"""
Open-boundary Wilson two-body mutual-channel probe.

Goal:
  remove periodic-image contamination from frontier_wilson_two_body.py
  and test whether the clean G=5 mutual-attraction window survives on a
  larger open 3D Wilson lattice.

Protocol:
  - two separate orbitals
  - SHARED, SELF_ONLY, FREE, FROZEN controls
  - early mutual acceleration from separation(t)
  - symmetric placement around the lattice center to suppress boundary drift
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 20
SIGMA = 1.0


class OpenWilsonLattice:
    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self.site_index(x, y, z)
                    self.pos[i] = [x, y, z]
                    self.adj[i] = []
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
                            self.adj[i].append(self.site_index(nx, ny, nz))
        self.lap = self.build_laplacian()

    def site_index(self, x: int, y: int, z: int):
        return x * self.side**2 + y * self.side + z

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * sigma**2))
        psi /= np.linalg.norm(psi)
        return psi

    def build_laplacian(self):
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

    def solve_poisson(self, rho, G, mu2):
        A = self.lap - mu2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

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
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_x(self, psi):
        rho = np.abs(psi) ** 2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)

    def run_mode(
        self,
        mode,
        G_val,
        mu2_val,
        center_a,
        center_b,
        sigma=SIGMA,
        source_mass_a=1.0,
        source_mass_b=1.0,
    ):
        psi_a = self.gaussian_wavepacket(center_a, sigma)
        psi_b = self.gaussian_wavepacket(center_b, sigma)

        seps = np.zeros(N_STEPS + 1)
        seps[0] = self.center_of_mass_x(psi_b) - self.center_of_mass_x(psi_a)

        phi_frozen = None
        if mode == "FROZEN":
            rho_total = source_mass_a * np.abs(psi_a) ** 2 + source_mass_b * np.abs(psi_b) ** 2
            phi_frozen = self.solve_poisson(rho_total, G_val, mu2_val)

        for t in range(N_STEPS):
            if mode == "FREE":
                phi_a = np.zeros(self.n)
                phi_b = np.zeros(self.n)
            elif mode == "SHARED":
                rho_total = source_mass_a * np.abs(psi_a) ** 2 + source_mass_b * np.abs(psi_b) ** 2
                phi_shared = self.solve_poisson(rho_total, G_val, mu2_val)
                phi_a = phi_shared
                phi_b = phi_shared
            elif mode == "SELF_ONLY":
                phi_a = self.solve_poisson(source_mass_a * np.abs(psi_a) ** 2, G_val, mu2_val)
                phi_b = self.solve_poisson(source_mass_b * np.abs(psi_b) ** 2, G_val, mu2_val)
            else:
                phi_a = phi_frozen
                phi_b = phi_frozen

            H_a = self.build_wilson_hamiltonian(phi_a)
            H_b = self.build_wilson_hamiltonian(phi_b)
            psi_a = self.evolve_step(psi_a, H_a)
            psi_b = self.evolve_step(psi_b, H_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            seps[t + 1] = self.center_of_mass_x(psi_b) - self.center_of_mass_x(psi_a)

        return seps


def acceleration(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def run_config(side: int, G_val: float, mu2_val: float, d: int, source_mass_a: float = 1.0, source_mass_b: float = 1.0):
    lat = OpenWilsonLattice(side)
    center = side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    seps = {}
    for mode in ("SHARED", "SELF_ONLY", "FREE", "FROZEN"):
        seps[mode] = lat.run_mode(
            mode,
            G_val,
            mu2_val,
            center_a,
            center_b,
            source_mass_a=source_mass_a,
            source_mass_b=source_mass_b,
        )

    a_mut = acceleration(seps["SHARED"]) - acceleration(seps["SELF_ONLY"])
    early = slice(2, min(11, N_STEPS + 1))
    mean = float(np.mean(a_mut[early]))
    std = float(np.std(a_mut[early]))
    snr = abs(mean) / (std + 1e-12)
    return {
        "side": side,
        "G": G_val,
        "mu2": mu2_val,
        "d": d,
        "source_mass_a": source_mass_a,
        "source_mass_b": source_mass_b,
        "a_mutual_early_mean": mean,
        "a_mutual_early_std": std,
        "snr": snr,
        "dsep_shared": float(seps["SHARED"][-1] - seps["SHARED"][0]),
        "dsep_self": float(seps["SELF_ONLY"][-1] - seps["SELF_ONLY"][0]),
        "dsep_free": float(seps["FREE"][-1] - seps["FREE"][0]),
    }


def label(mean, snr):
    signal = "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL")
    quality = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")
    return signal, quality


def main():
    print("=" * 88)
    print("OPEN-BOUNDARY WILSON TWO-BODY TEST")
    print("=" * 88)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, REG={REG}, N_STEPS={N_STEPS}")
    print("Test surface: side in {11,13}, G=5, mu2=0.22, d in {3,4,5,6}")
    print()

    rows = []
    for side in (11, 13):
        for d in (3, 4, 5, 6):
            t0 = time.time()
            row = run_config(side, 5, 0.22, d)
            elapsed = time.time() - t0
            signal, quality = label(row["a_mutual_early_mean"], row["snr"])
            rows.append(row)
            print(
                f"side={side:2d} d={d}: "
                f"a_mut={row['a_mutual_early_mean']:+.6f} +/- {row['a_mutual_early_std']:.6f} "
                f"(SNR={row['snr']:.2f}) [{signal}] [{quality}] "
                f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f} "
                f"({elapsed:.1f}s)"
            )

    print("\nSummary")
    print("-" * 88)
    clean = [r for r in rows if r["snr"] > 2.0]
    attract = [r for r in rows if r["a_mutual_early_mean"] < -1e-6]
    print(f"configs={len(rows)} attract={len(attract)}/{len(rows)} clean={len(clean)}/{len(rows)}")


if __name__ == "__main__":
    main()
