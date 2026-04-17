#!/usr/bin/env python3
"""
Bounded staggered test-mass / source-mass companion on an open 3D lattice.

Goal:
  Mirror the retained Wilson weak-field companion as closely as possible on the
  primary open-cubic staggered architecture, without pretending to close a
  both-masses or self-consistent two-body law.

Design:
  - open 3D cubic staggered lattice
  - parity-correct scalar coupling: H_diag = (m + Phi) * epsilon(x)
  - one STATIC source packet, not evolved
  - one normalized test packet evolved in the source-only field
  - free control subtraction for the blocked-envelope trajectory readout

Retained observables:
  1. exact inward force on the test packet from the source-only Phi
  2. early-time blocked-envelope acceleration relative to free evolution

Boundary:
  This is a source-mass companion only. It does not close both-masses scaling,
  self-consistent two-body closure, or a standalone distance-law claim.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve


MASS = 0.30
MU2 = 0.001
REG = 1e-6
DT = 0.08
N_STEPS = 10
G = 0.005
SIGMA_SOURCE = 1.30
SIGMA_TEST = 1.10
SIDES = (14, 16, 18)
DISTANCES = (4, 5, 6)
SOURCE_AMPLITUDES = (0.4, 0.6, 0.8, 1.0, 1.2)


class OpenStaggered3D:
    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self.parity = np.zeros(self.n_sites, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n_sites)}
        self._fill_geometry()
        self.laplacian = self._build_laplacian()
        self.eye_csc = speye(self.n_sites, format="csc")
        self.eye_csr = speye(self.n_sites, format="csr")

    def _fill_geometry(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    self.pos[i] = (x, y, z)
                    self.parity[i] = (x + y + z) % 2
                    for dx, dy, dz in (
                        (1, 0, 0),
                        (-1, 0, 0),
                        (0, 1, 0),
                        (0, -1, 0),
                        (0, 0, 1),
                        (0, 0, -1),
                    ):
                        xx, yy, zz = x + dx, y + dy, z + dz
                        if 0 <= xx < self.side and 0 <= yy < self.side and 0 <= zz < self.side:
                            self._adj[i].append(self.index(xx, yy, zz))

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csr_matrix:
        lap = lil_matrix((self.n_sites, self.n_sites), dtype=float)
        for i, nbrs in self._adj.items():
            for j in nbrs:
                if i >= j:
                    continue
                lap[i, j] -= 1.0
                lap[j, i] -= 1.0
                lap[i, i] += 1.0
                lap[j, j] += 1.0
        return lap.tocsr()

    def gaussian(
        self,
        center: tuple[float, float, float],
        sigma: float,
        *,
        amplitude: float = 1.0,
        normalize: bool = True,
    ) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = amplitude * np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma**2).astype(complex)
        if normalize:
            psi /= np.linalg.norm(psi)
        return psi

    def solve_phi(self, rho: np.ndarray) -> np.ndarray:
        op = (self.laplacian + (MU2 + REG) * speye(self.n_sites, format="csr")).tocsc()
        return spsolve(op, G * rho).real

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        h = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        eps = np.where(self.parity == 0, 1.0, -1.0)
        h.setdiag((MASS + phi) * eps)

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

        return h.tocsc()

    def make_stepper(self, hamiltonian: csc_matrix):
        a_plus = (self.eye_csc + 1j * hamiltonian * DT / 2).tocsc()
        a_minus = self.eye_csr - 1j * hamiltonian * DT / 2
        return splu(a_plus), a_minus

    def step(self, psi: np.ndarray, lu: splu, a_minus: csr_matrix) -> np.ndarray:
        psi = lu.solve(a_minus.dot(psi))
        return psi / np.linalg.norm(psi)

    def gradient_x(self, phi: np.ndarray) -> np.ndarray:
        grad = np.zeros(self.n_sites, dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x == 0:
                        grad[i] = phi[self.index(1, y, z)] - phi[i]
                    elif x == self.side - 1:
                        grad[i] = phi[i] - phi[self.index(x - 1, y, z)]
                    else:
                        grad[i] = 0.5 * (
                            phi[self.index(x + 1, y, z)] - phi[self.index(x - 1, y, z)]
                        )
        return grad

    def force_x(self, psi: np.ndarray, grad_x: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        rho /= np.sum(rho)
        return float(-np.sum(rho * grad_x))

    def blocked_centroid_x(self, psi: np.ndarray, *, right: bool) -> float:
        rho = np.abs(psi) ** 2
        total = 0.0
        moment = 0.0
        center = 0.5 * (self.side - 1)
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
                    xc = min(x0 + 0.5, self.side - 1)
                    if right and xc <= center:
                        continue
                    total += weight
                    moment += weight * xc
        return float(moment / max(total, 1e-30))


def power_law_fit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    log_x = np.log(np.asarray(xs, dtype=float))
    log_y = np.log(np.abs(np.asarray(ys, dtype=float)))
    slope, intercept = np.polyfit(log_x, log_y, 1)
    pred = slope * log_x + intercept
    ss_res = float(np.sum((log_y - pred) ** 2))
    ss_tot = float(np.sum((log_y - np.mean(log_y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), r2


def run_case(side: int, distance: int, amplitude: float) -> dict[str, float]:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    source_center = (center - distance / 2.0, center, center)
    test_center = (center + distance / 2.0, center, center)

    psi_source = lat.gaussian(
        source_center,
        SIGMA_SOURCE,
        amplitude=amplitude,
        normalize=False,
    )
    rho_source = np.abs(psi_source) ** 2
    source_mass = float(np.sum(rho_source))
    phi = lat.solve_phi(rho_source)
    grad_x = lat.gradient_x(phi)

    psi = lat.gaussian(test_center, SIGMA_TEST, normalize=True)
    psi_free = psi.copy()
    h_grav = lat.build_hamiltonian(phi)
    h_free = lat.build_hamiltonian(np.zeros(lat.n_sites, dtype=float))
    lu_grav, am_grav = lat.make_stepper(h_grav)
    lu_free, am_free = lat.make_stepper(h_free)

    force_hist = []
    x_hist = []
    x_free_hist = []
    for _ in range(N_STEPS + 1):
        # Test packet is on the right. Positive "toward" means leftward motion.
        force_hist.append(lat.force_x(psi, grad_x))
        x_hist.append(lat.blocked_centroid_x(psi, right=True))
        x_free_hist.append(lat.blocked_centroid_x(psi_free, right=True))
        psi = lat.step(psi, lu_grav, am_grav)
        psi_free = lat.step(psi_free, lu_free, am_free)

    x_hist = np.asarray(x_hist, dtype=float)
    x_free_hist = np.asarray(x_free_hist, dtype=float)
    dx_mut = x_free_hist - x_hist
    acc_mut = np.zeros_like(dx_mut)
    acc_mut[1:-1] = (dx_mut[2:] - 2 * dx_mut[1:-1] + dx_mut[:-2]) / DT**2
    early = slice(2, 7)

    return {
        "side": float(side),
        "distance": float(distance),
        "amplitude": float(amplitude),
        "source_mass": source_mass,
        "phi_peak": float(np.max(phi)),
        "force_toward_early": float(np.mean(force_hist[early])),
        "block_accel_early": float(np.mean(acc_mut[early])),
        "block_shift_final": float(dx_mut[-1]),
    }


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("STAGGERED TEST-MASS / SOURCE-MASS COMPANION (OPEN 3D)")
    print("=" * 96)
    print(
        f"MASS={MASS}, G={G}, mu2={MU2}, dt={DT}, steps={N_STEPS}, "
        f"sigma_source={SIGMA_SOURCE}, sigma_test={SIGMA_TEST}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, amplitudes={SOURCE_AMPLITUDES}")
    print("Static source only. Source-mass companion, not both-masses closure.")
    print()

    rows: list[dict[str, float]] = []
    fit_rows: list[dict[str, float]] = []

    for side in SIDES:
        print(f"side={side}")
        print("-" * 96)
        print(
            f"{'d':>2s} {'A':>4s} | {'M_source':>9s} {'phi_peak':>9s} | "
            f"{'F_toward':>11s} {'a_block':>11s} {'dx_final':>11s}"
        )
        print("-" * 96)
        side_rows = []
        for distance in DISTANCES:
            row_group = []
            for amplitude in SOURCE_AMPLITUDES:
                row = run_case(side, distance, amplitude)
                rows.append(row)
                side_rows.append(row)
                row_group.append(row)
                print(
                    f"{distance:2d} {amplitude:4.1f} | "
                    f"{row['source_mass']:9.4f} {row['phi_peak']:9.4e} | "
                    f"{row['force_toward_early']:+11.4e} {row['block_accel_early']:+11.4e} {row['block_shift_final']:+11.4e}"
                )
            force_exp, force_r2 = power_law_fit(
                [r["source_mass"] for r in row_group],
                [r["force_toward_early"] for r in row_group],
            )
            accel_exp, accel_r2 = power_law_fit(
                [r["source_mass"] for r in row_group],
                [r["block_accel_early"] for r in row_group],
            )
            fit_rows.append(
                {
                    "side": float(side),
                    "distance": float(distance),
                    "force_exp": force_exp,
                    "force_r2": force_r2,
                    "accel_exp": accel_exp,
                    "accel_r2": accel_r2,
                }
            )
            print(
                f"  fit d={distance}: "
                f"|F_toward| ~ M_source^{force_exp:.4f} (R^2={force_r2:.6f}), "
                f"|a_block| ~ M_source^{accel_exp:.4f} (R^2={accel_r2:.6f})"
            )
        print()

    force_exps = [row["force_exp"] for row in fit_rows]
    accel_exps = [row["accel_exp"] for row in fit_rows]
    all_force_positive = sum(row["force_toward_early"] > 0 for row in rows)
    all_accel_positive = sum(row["block_accel_early"] > 0 for row in rows)

    print("=" * 96)
    print("GLOBAL SUMMARY")
    print("=" * 96)
    print(f"rows: {len(rows)}")
    print(f"inward exact-force rows: {all_force_positive}/{len(rows)}")
    print(f"inward blocked-accel rows: {all_accel_positive}/{len(rows)}")
    print(
        f"force exponent range: {min(force_exps):.4f} .. {max(force_exps):.4f} "
        f"(mean={np.mean(force_exps):.4f})"
    )
    print(
        f"blocked accel exponent range: {min(accel_exps):.4f} .. {max(accel_exps):.4f} "
        f"(mean={np.mean(accel_exps):.4f})"
    )
    print(
        f"phi_peak range: {min(row['phi_peak'] for row in rows):.4e} .. "
        f"{max(row['phi_peak'] for row in rows):.4e}"
    )
    print()
    print("Interpretation:")
    print("  - This closes a bounded source-mass companion on the primary staggered surface.")
    print("  - It does not close both-masses scaling or a self-consistent two-body mass law.")
    print("  - The exact-force readout is the clean theory companion; the blocked acceleration")
    print("    is the bounded trajectory companion on this same weak-field surface.")
    print()
    print(f"elapsed={time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
