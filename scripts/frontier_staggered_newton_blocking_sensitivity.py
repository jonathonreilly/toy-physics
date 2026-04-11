#!/usr/bin/env python3
"""
Blocking sensitivity on the open-cubic staggered Newton reproduction surface.

Question:
  Does the Newton-compatible distance exponent on the open 3D staggered lane
  depend delicately on the current 2x2x2 blocked readout, or does it survive
  sensible coarse-grained trajectory observables and lattice sizes?

Scope:
  - same external-source open 3D staggered surface as
    frontier_staggered_newton_reproduction.py
  - no self-consistent two-body closure here
  - only trajectory readout / blocking sensitivity
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import splu


MASS = 0.30
DT = 0.10
N_STEPS = 12
SOURCE_STRENGTH = 5e-4
G = 50.0
SIGMA = 1.30
SIDES = (12, 14, 16)
DISTANCES = (3, 4, 5, 6)
SCHEMES = (
    ("raw", (1, 1, 1)),
    ("z2", (1, 1, 2)),
    ("cube2", (2, 2, 2)),
    ("cube4", (4, 4, 4)),
)


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

    def build_potential(
        self, source: tuple[float, float, float], strength: float = SOURCE_STRENGTH
    ) -> np.ndarray:
        rel = self.pos - np.asarray(source, dtype=float)
        r = np.sqrt(np.sum(rel * rel, axis=1))
        return -MASS * G * strength / np.maximum(r, 0.35)

    def build_hamiltonian(self, V: np.ndarray | None = None) -> csr_matrix:
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
                    phi = 0.0 if V is None else float(V[i])
                    h[i, i] += (MASS + phi) * eps
        return h.tocsr()

    def evolve(self, H: csr_matrix, psi0: np.ndarray, n_steps: int = N_STEPS) -> list[np.ndarray]:
        key = H.data.tobytes()
        lu = self._aplus_cache.get(key)
        if lu is None:
            aplus = (speye(self.n_sites, format="csc") + 1j * H * DT / 2).tocsc()
            lu = splu(aplus)
            self._aplus_cache[key] = lu
        aminus = speye(self.n_sites, format="csr") - 1j * H * DT / 2
        psi = psi0.copy()
        out = [psi.copy()]
        for _ in range(n_steps):
            psi = lu.solve(aminus.dot(psi))
            psi = psi / np.linalg.norm(psi)
            out.append(psi.copy())
        return out

    def blocked_centroid_z(self, psi: np.ndarray, block: tuple[int, int, int]) -> float:
        if block == (1, 1, 1):
            rho = np.abs(psi) ** 2
            return float(np.sum(rho * self.pos[:, 2]) / np.sum(rho))

        bx, by, bz = block
        rho = np.abs(psi) ** 2
        total = 0.0
        moment = 0.0
        for x0 in range(0, self.side, bx):
            for y0 in range(0, self.side, by):
                for z0 in range(0, self.side, bz):
                    weight = 0.0
                    for dx in range(bx):
                        for dy in range(by):
                            for dz in range(bz):
                                x = x0 + dx
                                y = y0 + dy
                                z = z0 + dz
                                if x < self.side and y < self.side and z < self.side:
                                    weight += rho[self.index(x, y, z)]
                    zc = min(z0 + 0.5 * (bz - 1), self.side - 1)
                    total += weight
                    moment += weight * zc
        return float(moment / total)


def fit_early_accel(times: np.ndarray, delta: np.ndarray) -> tuple[float, float]:
    X = np.column_stack([np.ones_like(times), times, 0.5 * times * times])
    coeffs, *_ = np.linalg.lstsq(X, delta, rcond=None)
    pred = X @ coeffs
    ss_res = float(np.sum((delta - pred) ** 2))
    ss_tot = float(np.sum((delta - np.mean(delta)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[2]), r2


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


def run_case(side: int, distance: int, scheme_name: str, block: tuple[int, int, int]) -> dict[str, float]:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    packet_center = (center, center, center)
    source_center = (center, center, center + distance)

    psi0 = lat.gaussian(packet_center)
    V = lat.build_potential(source_center)
    H_free = lat.build_hamiltonian(None)
    H_grav = lat.build_hamiltonian(V)

    free_hist = lat.evolve(H_free, psi0)
    grav_hist = lat.evolve(H_grav, psi0)

    obs_free = np.array([lat.blocked_centroid_z(psi, block) for psi in free_hist])
    obs_grav = np.array([lat.blocked_centroid_z(psi, block) for psi in grav_hist])
    delta = obs_grav - obs_free
    times = DT * np.arange(len(delta))
    accel, r2 = fit_early_accel(times[1:6], delta[1:6])

    return {
        "side": float(side),
        "distance": float(distance),
        "accel": accel,
        "accel_r2": r2,
        "delta_final": float(delta[-1]),
        "scheme": scheme_name,
    }


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("STAGGERED NEWTON BLOCKING SENSITIVITY: OPEN 3D EXTERNAL-SOURCE SURFACE")
    print("=" * 96)
    print(
        f"MASS={MASS}, G={G}, SOURCE_STRENGTH={SOURCE_STRENGTH}, DT={DT}, "
        f"N_STEPS={N_STEPS}, SIGMA={SIGMA}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}")
    print("schemes: raw, z2, cube2, cube4")
    print()

    all_rows: list[dict[str, float]] = []

    for scheme_name, block in SCHEMES:
        print(f"{scheme_name} block={block}")
        print("-" * 96)
        scheme_rows: list[dict[str, float]] = []
        for side in SIDES:
            for distance in DISTANCES:
                row = run_case(side, distance, scheme_name, block)
                scheme_rows.append(row)
                all_rows.append(row)
                print(
                    f"side={side:2d} d={distance:d} "
                    f"accel={row['accel']:+.6e} "
                    f"delta_final={row['delta_final']:+.6e} "
                    f"fitR2={row['accel_r2']:.4f}"
                )
        slope_global, r2_global = fit_distance_law(scheme_rows, "accel")
        all_toward = all(row["accel"] > 0 for row in scheme_rows)
        slopes = []
        for side in SIDES:
            side_rows = [row for row in scheme_rows if int(row["side"]) == side]
            slope_side, r2_side = fit_distance_law(side_rows, "accel")
            slopes.append(slope_side)
            print(f"  side={side}: |a| ~ d^{slope_side:.3f}  R^2={r2_side:.4f}")
        print(
            f"  global: |a| ~ d^{slope_global:.3f}  R^2={r2_global:.4f}  "
            f"all_toward={all_toward}  side_span={max(slopes)-min(slopes):.3f}"
        )
        print()

    print("=" * 96)
    print("SUMMARY")
    print("=" * 96)
    for scheme_name, _block in SCHEMES:
        scheme_rows = [row for row in all_rows if row["scheme"] == scheme_name]
        slope_global, r2_global = fit_distance_law(scheme_rows, "accel")
        slopes = [
            fit_distance_law([row for row in scheme_rows if int(row["side"]) == side], "accel")[0]
            for side in SIDES
        ]
        print(
            f"{scheme_name:>5s}: exponent={slope_global:+.3f}  R^2={r2_global:.4f}  "
            f"all_toward={all(row['accel'] > 0 for row in scheme_rows)}  "
            f"side_span={max(slopes)-min(slopes):.3f}"
        )

    print()
    print(f"runtime={time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
