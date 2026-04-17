#!/usr/bin/env python3
"""
Staggered Newton Reproduction on an Open 3D Lattice
===================================================

Goal:
  Test whether the primary staggered architecture can support a Newton-
  compatible distance law with a trajectory-level observable once the readout
  is coarse-grained to suppress sublattice oscillation.

Protocol:
  - open 3D staggered lattice
  - literature-correct scalar/parity coupling: (m + V) * epsilon(x)
  - external attractive source displaced along +z
  - compare free vs gravitating evolution of the same packet
  - report:
      * exact force on the evolved state
      * raw centroid shift (known pathology probe)
      * 2x2x2 blocked-centroid shift
      * early-time blocked acceleration fit vs source distance

Interpretation rule:
  - if the blocked observable is clean and follows ~ d^-2 on the audited
    surface, the staggered architecture supports a bounded Newton-compatible
    trajectory law on that surface
  - if exact force is clean but blocked trajectory is not, the trajectory
    observable still fails even though the force law survives
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import csc_matrix, csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu


MASS = 0.30
DT = 0.10
N_STEPS = 12
SOURCE_STRENGTH = 5e-4
G = 50.0
# A slightly broader packet suppresses sublattice-scale beating in the blocked
# readout without changing the exact-force law.
SIGMA = 1.30
SIDES = (12, 14, 16)
# d=2 is a near-field/regularization point and contaminates the distance fit.
DISTANCES = (3, 4, 5, 6)


class OpenStaggered3D:
    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self._fill_positions()
        self._aplus_cache: dict[bytes, splu] = {}

    def _fill_positions(self) -> None:
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    self.pos[self.index(x, y, z)] = (x, y, z)

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

    def gaussian(self, center: tuple[float, float, float], sigma: float = SIGMA) -> np.ndarray:
        rel = self.pos - np.asarray(center, dtype=float)
        psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma**2).astype(complex)
        return psi / np.linalg.norm(psi)

    def build_potential(self, source: tuple[float, float, float], strength: float = SOURCE_STRENGTH) -> np.ndarray:
        rel = self.pos - np.asarray(source, dtype=float)
        r = np.sqrt(np.sum(rel * rel, axis=1))
        return -MASS * G * strength / np.maximum(r, 0.35)

    def build_hamiltonian(self, V: np.ndarray | None = None) -> csr_matrix:
        H = lil_matrix((self.n_sites, self.n_sites), dtype=complex)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if x + 1 < self.side:
                        j = self.index(x + 1, y, z)
                        H[i, j] += -0.5j
                        H[j, i] += 0.5j
                    eta_y = (-1) ** x
                    if y + 1 < self.side:
                        j = self.index(x, y + 1, z)
                        H[i, j] += eta_y * (-0.5j)
                        H[j, i] += eta_y * (0.5j)
                    eta_z = (-1) ** (x + y)
                    if z + 1 < self.side:
                        j = self.index(x, y, z + 1)
                        H[i, j] += eta_z * (-0.5j)
                        H[j, i] += eta_z * (0.5j)
                    eps = (-1) ** (x + y + z)
                    phi = 0.0 if V is None else float(V[i])
                    H[i, i] += (MASS + phi) * eps
        return H.tocsr()

    def evolve(self, H: csr_matrix, psi0: np.ndarray, n_steps: int = N_STEPS, dt: float = DT) -> list[np.ndarray]:
        key = H.data.tobytes()
        lu = self._aplus_cache.get(key)
        if lu is None:
            aplus = (speye(self.n_sites, format="csc") + 1j * H * dt / 2).tocsc()
            lu = splu(aplus)
            self._aplus_cache[key] = lu
        aminus = speye(self.n_sites, format="csr") - 1j * H * dt / 2
        psi = psi0.copy()
        out = [psi.copy()]
        for _ in range(n_steps):
            psi = lu.solve(aminus.dot(psi))
            psi = psi / np.linalg.norm(psi)
            out.append(psi.copy())
        return out

    def raw_centroid_z(self, psi: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        return float(np.sum(rho * self.pos[:, 2]) / np.sum(rho))

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
                    zc = min(z0 + 0.5, self.side - 1)
                    total += weight
                    moment += weight * zc
        return float(moment / total)

    def dV_dz(self, V: np.ndarray) -> np.ndarray:
        dV = np.zeros(self.n_sites, dtype=float)
        for x in range(self.side):
            for y in range(self.side):
                for z in range(self.side):
                    i = self.index(x, y, z)
                    if z == 0:
                        vp = V[self.index(x, y, z + 1)]
                        vm = V[i]
                        dV[i] = vp - vm
                    elif z == self.side - 1:
                        vp = V[i]
                        vm = V[self.index(x, y, z - 1)]
                        dV[i] = vp - vm
                    else:
                        vp = V[self.index(x, y, z + 1)]
                        vm = V[self.index(x, y, z - 1)]
                        dV[i] = 0.5 * (vp - vm)
        return dV

    def exact_force(self, psi: np.ndarray, dV: np.ndarray) -> float:
        rho = np.abs(psi) ** 2
        rho = rho / np.sum(rho)
        return float(-np.sum(rho * dV))


def fit_early_accel(times: np.ndarray, delta: np.ndarray) -> tuple[float, float]:
    # delta(t) ~ a0 + v0 t + 0.5 a t^2 on the first few steps.
    X = np.column_stack([np.ones_like(times), times, 0.5 * times * times])
    coeffs, *_ = np.linalg.lstsq(X, delta, rcond=None)
    pred = X @ coeffs
    ss_res = float(np.sum((delta - pred) ** 2))
    ss_tot = float(np.sum((delta - np.mean(delta)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[2]), r2


def run_case(side: int, distance: int) -> dict[str, float]:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    packet_center = (center, center, center)
    source_center = (center, center, center + distance)

    psi0 = lat.gaussian(packet_center)
    V = lat.build_potential(source_center)
    dV = lat.dV_dz(V)
    H_free = lat.build_hamiltonian(None)
    H_grav = lat.build_hamiltonian(V)

    free_hist = lat.evolve(H_free, psi0)
    grav_hist = lat.evolve(H_grav, psi0)

    raw_free = np.array([lat.raw_centroid_z(psi) for psi in free_hist])
    raw_grav = np.array([lat.raw_centroid_z(psi) for psi in grav_hist])
    block_free = np.array([lat.blocked_centroid_z(psi) for psi in free_hist])
    block_grav = np.array([lat.blocked_centroid_z(psi) for psi in grav_hist])

    delta_raw = raw_grav - raw_free
    delta_block = block_grav - block_free
    times = DT * np.arange(len(delta_block))
    accel_block, accel_r2 = fit_early_accel(times[1:6], delta_block[1:6])
    accel_raw, raw_r2 = fit_early_accel(times[1:6], delta_raw[1:6])
    force_t0 = lat.exact_force(psi0, dV)
    force_tfinal = lat.exact_force(grav_hist[-1], dV)

    return {
        "side": float(side),
        "distance": float(distance),
        "force_t0": force_t0,
        "force_tfinal": force_tfinal,
        "delta_raw_final": float(delta_raw[-1]),
        "delta_block_final": float(delta_block[-1]),
        "accel_raw": accel_raw,
        "accel_raw_r2": raw_r2,
        "accel_block": accel_block,
        "accel_block_r2": accel_r2,
    }


def fit_distance_law(rows: list[dict[str, float]], key: str) -> tuple[float, float]:
    xs = []
    ys = []
    for row in rows:
        value = abs(row[key])
        if value <= 0:
            continue
        xs.append(math.log(row["distance"]))
        ys.append(math.log(value))
    if len(xs) < 2:
        return float("nan"), float("nan")
    coeffs = np.polyfit(xs, ys, 1)
    pred = np.polyval(coeffs, xs)
    y = np.asarray(ys)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[0]), r2


def main() -> None:
    t0 = time.time()
    print("=" * 88)
    print("STAGGERED NEWTON REPRODUCTION: OPEN 3D TRAJECTORY TEST")
    print("=" * 88)
    print(f"MASS={MASS}, G={G}, SOURCE_STRENGTH={SOURCE_STRENGTH}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print("Observable hierarchy: exact force, raw centroid delta, blocked 2x2x2 centroid delta.")
    print()

    rows: list[dict[str, float]] = []
    for side in SIDES:
        print(f"side={side}")
        print("-" * 88)
        for distance in DISTANCES:
            row = run_case(side, distance)
            rows.append(row)
            print(
                f"d={distance:2d} "
                f"F0={row['force_t0']:+.4e} Ff={row['force_tfinal']:+.4e} "
                f"raw_dz={row['delta_raw_final']:+.4e} raw_a={row['accel_raw']:+.4e} (R2={row['accel_raw_r2']:.3f}) "
                f"block_dz={row['delta_block_final']:+.4e} block_a={row['accel_block']:+.4e} (R2={row['accel_block_r2']:.3f})"
            )
        print()

    print("Distance-law fits")
    print("-" * 88)
    for side in SIDES:
        subset = [row for row in rows if int(row["side"]) == side]
        slope_force, r2_force = fit_distance_law(subset, "force_t0")
        slope_block, r2_block = fit_distance_law(subset, "accel_block")
        slope_raw, r2_raw = fit_distance_law(subset, "accel_raw")
        print(
            f"side={side}: "
            f"|F0|~d^{slope_force:+.3f} (R2={r2_force:.4f})  "
            f"|a_block|~d^{slope_block:+.3f} (R2={r2_block:.4f})  "
            f"|a_raw|~d^{slope_raw:+.3f} (R2={r2_raw:.4f})"
        )

    slope_force, r2_force = fit_distance_law(rows, "force_t0")
    slope_block, r2_block = fit_distance_law(rows, "accel_block")
    slope_raw, r2_raw = fit_distance_law(rows, "accel_raw")
    all_block_toward = all(row["accel_block"] > 0 for row in rows)
    all_force_toward = all(row["force_t0"] > 0 and row["force_tfinal"] > 0 for row in rows)
    all_raw_toward = all(row["accel_raw"] > 0 for row in rows)

    print()
    print("Summary")
    print("-" * 88)
    print(f"force toward: {all_force_toward}")
    print(f"raw accel toward: {all_raw_toward}")
    print(f"blocked accel toward: {all_block_toward}")
    print(f"global |F0| exponent = {slope_force:+.3f} (R2={r2_force:.4f})")
    print(f"global |a_block| exponent = {slope_block:+.3f} (R2={r2_block:.4f})")
    print(f"global |a_raw| exponent = {slope_raw:+.3f} (R2={r2_raw:.4f})")
    print(f"time = {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
