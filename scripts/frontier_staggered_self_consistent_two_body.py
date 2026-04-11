#!/usr/bin/env python3
"""
Staggered Self-Consistent Two-Body Channel on an Open 3D Lattice
=================================================================

Goal:
  Test a genuine self-consistent two-body channel on the primary staggered
  architecture, beyond the external-source Newton reproduction.

Design:
  - two separate staggered orbitals on an open 3D cubic lattice
  - shared self-consistent scalar field:
        rho_total = |psi_A|^2 + |psi_B|^2
        (L + mu^2 I) Phi = G * rho_total
  - self-only controls:
        psi_A evolves under Phi_A sourced by |psi_A|^2
        psi_B evolves under Phi_B sourced by |psi_B|^2
  - parity-correct staggered coupling:
        H_diag = (m + Phi) * epsilon(x)

Retained observables:
  1. exact partner-force channel on each orbital
  2. blocked-centroid mutual channel as a trajectory diagnostic

Interpretation rule:
  - if the exact partner-force channel is clean and Newton-compatible but the
    blocked trajectory channel remains noisy, the staggered self-consistent
    two-body lane is real but still force-led rather than trajectory-led
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
N_STEPS = 6
G = 50.0
# A narrower packet is needed here; broad packets wash the partner-force law
# from ~d^-2 to ~d^-1.6 on this self-consistent surface.
SIGMA = 0.80
SIDES = (12, 14, 16)
DISTANCES = (3, 4, 5, 6, 7)


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

    def gaussian(self, center: tuple[float, float, float], sigma: float = SIGMA) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma**2).astype(complex)
        return psi / np.linalg.norm(psi)

    def solve_phi(self, rho: np.ndarray, G_val: float = G) -> np.ndarray:
        if np.allclose(rho, 0.0):
            return np.zeros(self.n_sites)
        op = (self.laplacian + (MU2 + REG) * speye(self.n_sites, format="csr")).tocsc()
        return spsolve(op, G_val * rho).real

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
                        grad[i] = phi[self.index(x + 1, y, z)] - phi[i]
                    elif x == self.side - 1:
                        grad[i] = phi[i] - phi[self.index(x - 1, y, z)]
                    else:
                        grad[i] = 0.5 * (
                            phi[self.index(x + 1, y, z)] - phi[self.index(x - 1, y, z)]
                        )
        return grad

    def force_x(self, psi: np.ndarray, grad_x: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        rho = rho / np.sum(rho)
        return float(-np.sum(rho * grad_x))

    def blocked_centroid_x(self, psi: np.ndarray, *, left: bool) -> float:
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
                    if left and xc >= center:
                        continue
                    if not left and xc <= center:
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


def run_case(side: int, distance: int) -> dict[str, float]:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    packet_a_center = (center - distance / 2.0, center, center)
    packet_b_center = (center + distance / 2.0, center, center)

    psi_a_shared = lat.gaussian(packet_a_center)
    psi_b_shared = lat.gaussian(packet_b_center)
    psi_a_self = psi_a_shared.copy()
    psi_b_self = psi_b_shared.copy()

    phi_a0 = lat.solve_phi(np.abs(psi_a_shared) ** 2)
    phi_b0 = lat.solve_phi(np.abs(psi_b_shared) ** 2)
    # Define "toward positive":
    #   A sits on the left, so positive means +x
    #   B sits on the right, so positive means -x
    force_a_t0 = -lat.force_x(psi_a_shared, lat.gradient_x(phi_b0))
    force_b_t0 = lat.force_x(psi_b_shared, lat.gradient_x(phi_a0))

    force_a_hist = []
    force_b_hist = []
    dx_a_hist = []
    dx_b_hist = []

    for _ in range(N_STEPS):
        phi_a = lat.solve_phi(np.abs(psi_a_shared) ** 2)
        phi_b = lat.solve_phi(np.abs(psi_b_shared) ** 2)
        phi_shared = phi_a + phi_b

        force_a_hist.append(-lat.force_x(psi_a_shared, lat.gradient_x(phi_b)))
        force_b_hist.append(lat.force_x(psi_b_shared, lat.gradient_x(phi_a)))

        h_shared = lat.build_hamiltonian(phi_shared)
        lu_shared, am_shared = lat.make_stepper(h_shared)

        h_a_self = lat.build_hamiltonian(phi_a)
        h_b_self = lat.build_hamiltonian(phi_b)
        lu_a_self, am_a_self = lat.make_stepper(h_a_self)
        lu_b_self, am_b_self = lat.make_stepper(h_b_self)

        psi_a_shared = lat.step(psi_a_shared, lu_shared, am_shared)
        psi_b_shared = lat.step(psi_b_shared, lu_shared, am_shared)
        psi_a_self = lat.step(psi_a_self, lu_a_self, am_a_self)
        psi_b_self = lat.step(psi_b_self, lu_b_self, am_b_self)

        dx_a_hist.append(
            lat.blocked_centroid_x(psi_a_shared, left=True)
            - lat.blocked_centroid_x(psi_a_self, left=True)
        )
        dx_b_hist.append(
            lat.blocked_centroid_x(psi_b_self, left=False)
            - lat.blocked_centroid_x(psi_b_shared, left=False)
        )

    early = slice(0, 4)
    block_inward = 0.5 * (np.mean(dx_a_hist[early]) + np.mean(dx_b_hist[early]))
    return {
        "side": float(side),
        "distance": float(distance),
        "force_a_t0": force_a_t0,
        "force_b_t0": force_b_t0,
        "force_early": 0.5 * (
            float(np.mean(force_a_hist[early])) + float(np.mean(force_b_hist[early]))
        ),
        "dx_a_final": float(dx_a_hist[-1]),
        "dx_b_final": float(dx_b_hist[-1]),
        "block_inward_early": float(block_inward),
    }


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("STAGGERED SELF-CONSISTENT TWO-BODY CHANNEL (OPEN 3D)")
    print("=" * 96)
    print(
        f"MASS={MASS}, G={G}, mu2={MU2}, dt={DT}, steps={N_STEPS}, sigma={SIGMA}, "
        f"sides={SIDES}, distances={DISTANCES}"
    )
    print("Observable hierarchy: exact partner force first, blocked trajectory second.")
    print()

    rows: list[dict[str, float]] = []
    for side in SIDES:
        print(f"side={side}")
        print("-" * 96)
        print(
            f"{'d':>3s} | {'F_A(t0)':>11s} {'F_B(t0)':>11s} {'F_early':>11s} | "
            f"{'dxA_mut':>11s} {'dxB_mut':>11s} {'block_early':>12s}"
        )
        print("-" * 96)
        side_rows = []
        for distance in DISTANCES:
            row = run_case(side, distance)
            rows.append(row)
            side_rows.append(row)
            print(
                f"{distance:3d} | "
                f"{row['force_a_t0']:+11.4e} {row['force_b_t0']:+11.4e} {row['force_early']:+11.4e} | "
                f"{row['dx_a_final']:+11.4e} {row['dx_b_final']:+11.4e} {row['block_inward_early']:+12.4e}"
            )

        t0_exp, t0_r2 = power_law_fit(
            [r["distance"] for r in side_rows], [0.5 * (r["force_a_t0"] + r["force_b_t0"]) for r in side_rows]
        )
        early_exp, early_r2 = power_law_fit(
            [r["distance"] for r in side_rows], [r["force_early"] for r in side_rows]
        )
        print()
        print(f"  |F_partner(t0)|    ~ d^{t0_exp:.3f}   (R^2={t0_r2:.4f})")
        print(f"  |F_partner(early)| ~ d^{early_exp:.3f}   (R^2={early_r2:.4f})")
        print()

    global_t0_exp, global_t0_r2 = power_law_fit(
        [r["distance"] for r in rows], [0.5 * (r["force_a_t0"] + r["force_b_t0"]) for r in rows]
    )
    global_early_exp, global_early_r2 = power_law_fit(
        [r["distance"] for r in rows], [r["force_early"] for r in rows]
    )
    positive_force_rows = sum(1 for r in rows if r["force_a_t0"] > 0 and r["force_b_t0"] > 0)
    positive_block_rows = sum(1 for r in rows if r["block_inward_early"] > 0)

    print("=" * 96)
    print("SUMMARY")
    print("=" * 96)
    print(f"partner-force attractive rows: {positive_force_rows}/{len(rows)}")
    print(f"blocked inward rows:           {positive_block_rows}/{len(rows)}")
    print(f"global |F_partner(t0)|    ~ d^{global_t0_exp:.3f}   (R^2={global_t0_r2:.4f})")
    print(f"global |F_partner(early)| ~ d^{global_early_exp:.3f}   (R^2={global_early_r2:.4f})")
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
