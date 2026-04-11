#!/usr/bin/env python3
"""
3D Staggered Self-Gravity Contraction / Sign Probe
==================================================

Primary-architecture single-packet self-gravity on an open 3D cubic staggered
lattice. This lane is intentionally separate from the active both-masses and
self-consistent two-body workers.

Question:
  - Does the primary staggered architecture show a genuine 3D trajectory-level
    self-gravity contraction on an open cubic lattice?
  - If we flip the self-source sign in a matched control, do blocked trajectory
    observables separate cleanly, or does sign closure still fail?

Observables:
  - blocked 2x2x2 envelope width ratio vs free evolution
  - central-core probability excess vs free evolution
  - blocked-centroid drift (sanity check for symmetry)
  - shell-averaged potential gradient sign (field-side sign control)
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np
from scipy.sparse import csc_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu


MASS = 0.30
DT = 0.10
G_SELF = 50.0
MU2 = 0.001
SIGMA = 1.35
N_STEPS = 20
SIDES = (9, 11, 13)


@dataclass(frozen=True)
class RunSummary:
    side: int
    sign_label: str
    width_ratio: float
    core_excess: float
    drift_max: float
    drift_final: float
    grad_positive: int
    grad_total: int
    grad_mean: float
    norm_drift: float


class OpenStaggered3DSelfGravity:
    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self.parity = np.zeros(self.n_sites, dtype=float)
        self._fill_geometry()
        self.laplacian = self._build_laplacian()
        self.poisson_lu = splu((self.laplacian + MU2 * speye(self.n_sites, format="csc")).tocsc())
        self.h_free = self._build_free_hamiltonian()
        self.identity = speye(self.n_sites, format="csc")
        self.center = np.array([0.5 * (side - 1)] * 3, dtype=float)
        self.site_radius = np.sqrt(np.sum((self.pos - self.center) ** 2, axis=1))
        self.core_mask = self.site_radius <= 2.5
        self.shell0_mask = self.site_radius < 1.5
        self.shell1_mask = (self.site_radius >= 1.5) & (self.site_radius < 3.0)
        self.blocks = self._build_blocks()
        self._free_lu = splu((self.identity + 0.5j * DT * self.h_free).tocsc())
        self._free_b = self.identity - 0.5j * DT * self.h_free

    def _fill_geometry(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    self.pos[i] = (x, y, z)
                    self.parity[i] = 1.0 if (x + y + z) % 2 == 0 else -1.0

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def _build_laplacian(self) -> csc_matrix:
        lap = lil_matrix((self.n_sites, self.n_sites), dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                        xx = x + dx
                        yy = y + dy
                        zz = z + dz
                        if xx >= self.side or yy >= self.side or zz >= self.side:
                            continue
                        j = self.index(xx, yy, zz)
                        lap[i, j] -= 1.0
                        lap[j, i] -= 1.0
                        lap[i, i] += 1.0
                        lap[j, j] += 1.0
        return lap.tocsc()

    def _build_free_hamiltonian(self) -> csc_matrix:
        ham = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x + 1 < self.side:
                        j = self.index(x + 1, y, z)
                        ham[i, j] += -0.5j
                        ham[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self.index(x, y + 1, z)
                        ham[i, j] += eta_y * (-0.5j)
                        ham[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self.index(x, y, z + 1)
                        ham[i, j] += eta_z * (-0.5j)
                        ham[j, i] += eta_z * (0.5j)
        ham.setdiag(ham.diagonal() + MASS * self.parity)
        return ham.tocsc()

    def _build_blocks(self) -> list[tuple[np.ndarray, np.ndarray]]:
        blocks: list[tuple[np.ndarray, np.ndarray]] = []
        for x0 in range(0, self.side, 2):
            for y0 in range(0, self.side, 2):
                for z0 in range(0, self.side, 2):
                    idxs: list[int] = []
                    for dx in (0, 1):
                        for dy in (0, 1):
                            for dz in (0, 1):
                                x = x0 + dx
                                y = y0 + dy
                                z = z0 + dz
                                if x < self.side and y < self.side and z < self.side:
                                    idxs.append(self.index(x, y, z))
                    center = np.array(
                        [min(x0 + 0.5, self.side - 1), min(y0 + 0.5, self.side - 1), min(z0 + 0.5, self.side - 1)],
                        dtype=float,
                    )
                    blocks.append((np.array(idxs, dtype=int), center))
        return blocks

    def gaussian_state(self) -> np.ndarray:
        rel = self.pos - self.center
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / SIGMA**2).astype(complex)
        return psi / np.linalg.norm(psi)

    def blocked_width(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = float(np.sum(rho))
        moment = 0.0
        for idxs, center in self.blocks:
            weight = float(np.sum(rho[idxs]))
            moment += weight * float(np.sum((center - self.center) ** 2))
        return math.sqrt(moment / total)

    def blocked_centroid_z(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        total = float(np.sum(rho))
        moment = 0.0
        for idxs, center in self.blocks:
            weight = float(np.sum(rho[idxs]))
            moment += weight * center[2]
        return moment / total

    def core_probability(self, psi: np.ndarray) -> float:
        return float(np.sum(np.abs(psi[self.core_mask]) ** 2))

    def solve_phi(self, rho: np.ndarray, sign: float) -> np.ndarray:
        return self.poisson_lu.solve(sign * G_SELF * rho)

    def build_hamiltonian(self, phi: np.ndarray) -> csc_matrix:
        ham = self.h_free.copy().tolil()
        ham.setdiag(np.asarray(ham.diagonal()) + phi * self.parity)
        return ham.tocsc()

    def step(self, ham: csc_matrix, psi: np.ndarray) -> np.ndarray:
        lu = splu((self.identity + 0.5j * DT * ham).tocsc())
        bmat = self.identity - 0.5j * DT * ham
        nxt = lu.solve(bmat @ psi)
        return nxt / np.linalg.norm(nxt)

    def free_step(self, psi: np.ndarray) -> np.ndarray:
        nxt = self._free_lu.solve(self._free_b @ psi)
        return nxt / np.linalg.norm(nxt)


def run_case(side: int, sign: float) -> RunSummary:
    lat = OpenStaggered3DSelfGravity(side)
    psi = lat.gaussian_state()
    psi_free = psi.copy()
    center_z = lat.center[2]

    grad_series: list[float] = []
    drift_series: list[float] = [lat.blocked_centroid_z(psi) - center_z]
    norm_series: list[float] = [float(np.linalg.norm(psi))]

    for _ in range(N_STEPS):
        rho = np.abs(psi) ** 2
        phi = lat.solve_phi(rho, sign=sign)
        grad = float(np.mean(phi[lat.shell0_mask]) - np.mean(phi[lat.shell1_mask]))
        grad_series.append(grad)
        psi = lat.step(lat.build_hamiltonian(phi), psi)
        psi_free = lat.free_step(psi_free)
        drift_series.append(lat.blocked_centroid_z(psi) - center_z)
        norm_series.append(float(np.linalg.norm(psi)))

    sign_label = "attract" if sign > 0 else "repulse"
    width_ratio = lat.blocked_width(psi) / lat.blocked_width(psi_free)
    core_excess = lat.core_probability(psi) - lat.core_probability(psi_free)
    grad_positive = int(sum(g > 0 for g in grad_series))
    grad_mean = float(np.mean(grad_series))
    drift_max = float(np.max(np.abs(drift_series)))
    drift_final = float(drift_series[-1])
    norm_drift = float(np.max(np.abs(np.asarray(norm_series) - 1.0)))

    return RunSummary(
        side=side,
        sign_label=sign_label,
        width_ratio=width_ratio,
        core_excess=core_excess,
        drift_max=drift_max,
        drift_final=drift_final,
        grad_positive=grad_positive,
        grad_total=len(grad_series),
        grad_mean=grad_mean,
        norm_drift=norm_drift,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("3D STAGGERED SELF-GRAVITY CONTRACTION / SIGN PROBE")
    print("=" * 96)
    print(f"MASS={MASS}, G_SELF={G_SELF}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print("Open cubic staggered lattice, centered packet, blocked 2x2x2 envelope observables.")
    print()
    print(
        f"{'side':>4}  {'sign':>7}  {'w_self/w_free':>13}  {'core_excess':>12}  "
        f"{'grad+':>6}  {'grad_mean':>12}  {'drift_max':>12}  {'drift_final':>12}  {'norm_drift':>11}"
    )
    print("-" * 96)
    rows: list[RunSummary] = []
    for side in SIDES:
        for sign in (+1.0, -1.0):
            row = run_case(side, sign)
            rows.append(row)
            print(
                f"{row.side:4d}  {row.sign_label:>7s}  {row.width_ratio:13.6f}  {row.core_excess:12.6f}  "
                f"{row.grad_positive:2d}/{row.grad_total:<3d}  {row.grad_mean:+12.6e}  "
                f"{row.drift_max:12.6e}  {row.drift_final:+12.6e}  {row.norm_drift:11.3e}"
            )

    print("\nAggregate checks")
    print("-" * 96)
    for side in SIDES:
        a = next(r for r in rows if r.side == side and r.sign_label == "attract")
        r = next(rw for rw in rows if rw.side == side and rw.sign_label == "repulse")
        print(
            f"side={side}: contraction both signs={'YES' if a.width_ratio < 1.0 and r.width_ratio < 1.0 else 'NO'}; "
            f"|Δ width ratio|={abs(a.width_ratio - r.width_ratio):.6e}; "
            f"shell-gradient sign split={a.grad_positive}/{a.grad_total} vs {r.grad_positive}/{r.grad_total}"
        )

    print(f"\nElapsed: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
