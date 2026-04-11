#!/usr/bin/env python3
"""
Bounded Staggered Two-Body Portability / Direct-CoM Closure Probe
=================================================================

Goal:
  Stress the primary staggered self-consistent two-body lane with a more local
  direct-CoM observable, without changing the underlying physics. The question
  is whether a packet-local, pair-blocked centroid survives side, separation,
  and placement-family variation better than the retained global blocked readout.

Design:
  - open 3D staggered lattice
  - two orbitals with shared self-consistent Phi and self-only controls
  - same parity-correct coupling as the retained main harness
  - compare:
      1. exact partner-force channel
      2. retained global blocked-half centroid channel
      3. new local pair-blocked direct-CoM channel

Interpretation:
  - if the local pair-blocked direct-CoM channel stays inward and near-Newton
    across the bounded audited surface, direct-CoM closure strengthens
  - if only the force channel stays clean, direct-CoM closure remains open
"""

from __future__ import annotations

import os
import math
import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu, spsolve


MASS = 0.30
MU2 = 0.001
REG = 1e-6
DT = 0.08
N_STEPS = 8
G = 50.0
SIGMA = 0.80
SIDES = (12, 14, 16)
DISTANCES = (3, 4, 5, 6, 7)
PLACEMENTS = ("centered", "face_offset", "corner_offset")
LOCAL_RADIUS_BLOCKS = int(os.environ.get("LOCAL_RADIUS_BLOCKS", "2"))


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

    def blocked_half_centroid_x(self, psi: np.ndarray, *, left: bool) -> float:
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

    def pair_block_local_centroid_x(
        self, psi: np.ndarray, center_x: float, radius_blocks: int = LOCAL_RADIUS_BLOCKS
    ) -> float:
        rho = np.abs(psi) ** 2
        profile = rho.reshape(self.side, self.side, self.side).sum(axis=(1, 2))
        block_weights = profile[0::2] + profile[1::2]
        block_centers = 2.0 * np.arange(len(block_weights)) + 0.5
        k0 = int(np.clip(round((center_x - 0.5) / 2.0), 0, len(block_weights) - 1))
        left = max(0, k0 - radius_blocks)
        right = min(len(block_weights), k0 + radius_blocks + 1)
        weights = block_weights[left:right]
        centers = block_centers[left:right]
        total = float(np.sum(weights))
        return float(np.sum(weights * centers) / max(total, 1e-30))


def placement_coords(side: int, placement: str) -> tuple[float, float]:
    center = 0.5 * (side - 1)
    offset = 2.5
    if placement == "centered":
        return center, center
    if placement == "face_offset":
        return offset, center
    if placement == "corner_offset":
        return offset, offset
    raise ValueError(f"unknown placement {placement}")


def fit_early_accel(times: np.ndarray, delta: np.ndarray) -> tuple[float, float]:
    X = np.column_stack([np.ones_like(times), times, 0.5 * times * times])
    coeffs, *_ = np.linalg.lstsq(X, delta, rcond=None)
    pred = X @ coeffs
    ss_res = float(np.sum((delta - pred) ** 2))
    ss_tot = float(np.sum((delta - np.mean(delta)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[2]), r2


def power_law_fit(rows: list[dict[str, float]], key: str) -> tuple[float, float]:
    xs = []
    ys = []
    for row in rows:
        value = row[key]
        if value <= 0:
            continue
        xs.append(math.log(row["distance"]))
        ys.append(math.log(value))
    if len(xs) < 2:
        return float("nan"), float("nan")
    slope, intercept = np.polyfit(xs, ys, 1)
    pred = slope * np.asarray(xs) + intercept
    y = np.asarray(ys)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), r2


def run_case(side: int, distance: int, placement: str) -> dict[str, float]:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    y0, z0 = placement_coords(side, placement)
    packet_a_center = (center - distance / 2.0, y0, z0)
    packet_b_center = (center + distance / 2.0, y0, z0)

    psi_a_shared = lat.gaussian(packet_a_center)
    psi_b_shared = lat.gaussian(packet_b_center)
    psi_a_self = psi_a_shared.copy()
    psi_b_self = psi_b_shared.copy()

    force_a_hist = []
    force_b_hist = []
    delta_a_global = []
    delta_b_global = []
    delta_a_local = []
    delta_b_local = []

    for _ in range(N_STEPS):
        phi_a_shared = lat.solve_phi(np.abs(psi_a_shared) ** 2)
        phi_b_shared = lat.solve_phi(np.abs(psi_b_shared) ** 2)
        phi_shared = phi_a_shared + phi_b_shared

        force_a_hist.append(-lat.force_x(psi_a_shared, lat.gradient_x(phi_b_shared)))
        force_b_hist.append(lat.force_x(psi_b_shared, lat.gradient_x(phi_a_shared)))

        h_shared = lat.build_hamiltonian(phi_shared)
        lu_shared, am_shared = lat.make_stepper(h_shared)

        phi_a_self = lat.solve_phi(np.abs(psi_a_self) ** 2)
        phi_b_self = lat.solve_phi(np.abs(psi_b_self) ** 2)
        h_a_self = lat.build_hamiltonian(phi_a_self)
        h_b_self = lat.build_hamiltonian(phi_b_self)
        lu_a_self, am_a_self = lat.make_stepper(h_a_self)
        lu_b_self, am_b_self = lat.make_stepper(h_b_self)

        delta_a_global.append(
            lat.blocked_half_centroid_x(psi_a_shared, left=True)
            - lat.blocked_half_centroid_x(psi_a_self, left=True)
        )
        delta_b_global.append(
            lat.blocked_half_centroid_x(psi_b_self, left=False)
            - lat.blocked_half_centroid_x(psi_b_shared, left=False)
        )
        delta_a_local.append(
            lat.pair_block_local_centroid_x(psi_a_shared, packet_a_center[0])
            - lat.pair_block_local_centroid_x(psi_a_self, packet_a_center[0])
        )
        delta_b_local.append(
            lat.pair_block_local_centroid_x(psi_b_self, packet_b_center[0])
            - lat.pair_block_local_centroid_x(psi_b_shared, packet_b_center[0])
        )

        psi_a_shared = lat.step(psi_a_shared, lu_shared, am_shared)
        psi_b_shared = lat.step(psi_b_shared, lu_shared, am_shared)
        psi_a_self = lat.step(psi_a_self, lu_a_self, am_a_self)
        psi_b_self = lat.step(psi_b_self, lu_b_self, am_b_self)

    t = DT * np.arange(1, min(6, len(delta_a_local)) + 1)
    delta_a_global_fit = np.asarray(delta_a_global[: len(t)])
    delta_b_global_fit = np.asarray(delta_b_global[: len(t)])
    delta_a_local_fit = np.asarray(delta_a_local[: len(t)])
    delta_b_local_fit = np.asarray(delta_b_local[: len(t)])

    a_ag, r2_ag = fit_early_accel(t, delta_a_global_fit)
    a_bg, r2_bg = fit_early_accel(t, delta_b_global_fit)
    a_al, r2_al = fit_early_accel(t, delta_a_local_fit)
    a_bl, r2_bl = fit_early_accel(t, delta_b_local_fit)

    early = slice(0, len(t))
    force_early = 0.5 * (
        float(np.mean(force_a_hist[early])) + float(np.mean(force_b_hist[early]))
    )
    inward_global = (
        float(np.mean(delta_a_global_fit)) > 0.0 and float(np.mean(delta_b_global_fit)) > 0.0
    )
    inward_local = (
        float(np.mean(delta_a_local_fit)) > 0.0 and float(np.mean(delta_b_local_fit)) > 0.0
    )
    a_global_sym = 0.5 * (a_ag + a_bg)
    a_local_sym = 0.5 * (a_al + a_bl)

    return {
        "side": float(side),
        "distance": float(distance),
        "placement": placement,
        "force_early": force_early,
        "force_ok": float(force_early > 0.0),
        "delta_a_global_mean": float(np.mean(delta_a_global_fit)),
        "delta_b_global_mean": float(np.mean(delta_b_global_fit)),
        "delta_a_local_mean": float(np.mean(delta_a_local_fit)),
        "delta_b_local_mean": float(np.mean(delta_b_local_fit)),
        "inward_global": float(inward_global),
        "inward_local": float(inward_local),
        "a_global_sym": a_global_sym,
        "a_local_sym": a_local_sym,
        "a_global_r2": 0.5 * (r2_ag + r2_bg),
        "a_local_r2": 0.5 * (r2_al + r2_bl),
    }


def summarize(rows: list[dict[str, float]]) -> None:
    total = len(rows)
    force_rows = sum(int(row["force_ok"]) for row in rows)
    global_rows = sum(int(row["inward_global"]) for row in rows)
    local_rows = sum(int(row["inward_local"]) for row in rows)
    both_rows = sum(int(row["inward_global"] and row["inward_local"]) for row in rows)

    print()
    print("=" * 88)
    print("SUMMARY")
    print("=" * 88)
    print(f"rows={total}")
    print(f"force attractive: {force_rows}/{total}")
    print(f"global blocked inward: {global_rows}/{total}")
    print(f"local pair-block inward: {local_rows}/{total}")
    print(f"both inward: {both_rows}/{total}")

    slope_g, r2_g = power_law_fit([r for r in rows if r["inward_global"] > 0.0], "a_global_sym")
    slope_l, r2_l = power_law_fit([r for r in rows if r["inward_local"] > 0.0], "a_local_sym")
    print(f"global blocked fit (inward rows only): a ~ d^{slope_g:+.3f}, R^2={r2_g:.4f}")
    print(f"local pair-block fit (inward rows only): a ~ d^{slope_l:+.3f}, R^2={r2_l:.4f}")

    for placement in PLACEMENTS:
        subset = [row for row in rows if row["placement"] == placement]
        count_g = sum(int(row["inward_global"]) for row in subset)
        count_l = sum(int(row["inward_local"]) for row in subset)
        slope_pl, r2_pl = power_law_fit(
            [row for row in subset if row["inward_local"] > 0.0], "a_local_sym"
        )
        print(
            f"{placement:>13s}: global {count_g}/{len(subset)}, "
            f"local {count_l}/{len(subset)}, local fit={slope_pl:+.3f} (R^2={r2_pl:.4f})"
        )


def main() -> None:
    t0 = time.time()
    print("=" * 88)
    print("STAGGERED TWO-BODY PORTABILITY / DIRECT-COM CLOSURE PROBE")
    print("=" * 88)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, "
        f"SIGMA={SIGMA}, LOCAL_RADIUS_BLOCKS={LOCAL_RADIUS_BLOCKS}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, placements={PLACEMENTS}")
    print()

    rows: list[dict[str, float]] = []
    for placement in PLACEMENTS:
        print(f"[placement={placement}]")
        for side in SIDES:
            for distance in DISTANCES:
                row = run_case(side, distance, placement)
                rows.append(row)
                print(
                    f"side={side:2d} d={distance} "
                    f"force={row['force_early']:+.4e} "
                    f"global=({row['delta_a_global_mean']:+.3e},{row['delta_b_global_mean']:+.3e}) "
                    f"local=({row['delta_a_local_mean']:+.3e},{row['delta_b_local_mean']:+.3e}) "
                    f"aG={row['a_global_sym']:+.3e} aL={row['a_local_sym']:+.3e}"
                )
        print()

    summarize(rows)
    print()
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
