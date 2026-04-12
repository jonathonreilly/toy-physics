#!/usr/bin/env python3
"""
Staggered two-body mid-plane link-current probe on the open 3D cubic family.

This is the transport-observable redesign requested for the staggered
self-consistent two-body lane after the detector-side transfer observable
failed. The readout is a genuine bond-current across the mid-plane between the
packets:

  J_plane = sum_{x = mid_left, y, z} J_{(x,y,z)->(x+1,y,z)}

where positive sign means left-to-right flow across the packet bisector.

The observable is compared between SHARED and SELF_ONLY evolutions, and the
packet-wise inward current is defined by the sign-adjusted plane current:

  packet A (left):  +J_plane
  packet B (right): -J_plane

This stays on the same audited open-cubic surface used by the prior staggered
two-body notes.
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
N_STEPS = 8
G = 50.0
SIGMA = 0.80
SIDES = (12, 14, 16)
DISTANCES = (3, 4, 5, 6, 7)
PLACEMENTS = ("centered", "face_offset", "corner_offset")


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

    def index(self, x: int, y: int, z: int) -> int:
        return x * self.side * self.side + y * self.side + z

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

    def solve_phi(self, rho: np.ndarray, g_val: float = G) -> np.ndarray:
        if np.allclose(rho, 0.0):
            return np.zeros(self.n_sites)
        op = (self.laplacian + (MU2 + REG) * speye(self.n_sites, format="csr")).tocsc()
        return spsolve(op, g_val * rho).real

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
        rho /= np.sum(rho)
        return float(-np.sum(rho * grad_x))

    def plane_current_x(self, psi: np.ndarray) -> float:
        """
        Net probability current across the mid-plane.

        Positive sign means left -> right flow across x = side/2 - 0.5.
        """

        if self.side < 2:
            return 0.0
        x_left = self.side // 2 - 1
        x_right = x_left + 1
        total = 0.0
        for y in range(self.side):
            for z in range(self.side):
                i = self.index(x_left, y, z)
                j = self.index(x_right, y, z)
                hij = -0.5j
                # Continuity-equation sign convention: positive means left -> right.
                total += -2.0 * np.imag(np.conj(psi[i]) * hij * psi[j])
        return float(total)


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


def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), float(intercept), r2


def power_law_fit(rows: list[dict[str, float]], key: str) -> tuple[float, float]:
    xs = []
    ys = []
    for row in rows:
        value = row[key]
        if value <= 0.0:
            continue
        xs.append(math.log(row["distance"]))
        ys.append(math.log(value))
    if len(xs) < 2:
        return float("nan"), float("nan")
    slope, intercept = np.polyfit(xs, ys, 1)
    pred = slope * np.asarray(xs) + intercept
    arr = np.asarray(ys)
    ss_res = float(np.sum((arr - pred) ** 2))
    ss_tot = float(np.sum((arr - np.mean(arr)) ** 2))
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

    current_a_hist: list[float] = []
    current_b_hist: list[float] = []
    force_a_hist: list[float] = []
    force_b_hist: list[float] = []

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

        current_a_hist.append(
            lat.plane_current_x(psi_a_shared) - lat.plane_current_x(psi_a_self)
        )
        current_b_hist.append(
            -lat.plane_current_x(psi_b_shared) + lat.plane_current_x(psi_b_self)
        )

        psi_a_shared = lat.step(psi_a_shared, lu_shared, am_shared)
        psi_b_shared = lat.step(psi_b_shared, lu_shared, am_shared)
        psi_a_self = lat.step(psi_a_self, lu_a_self, am_a_self)
        psi_b_self = lat.step(psi_b_self, lu_b_self, am_b_self)

    early = slice(0, min(6, len(current_a_hist)))
    a_fit = np.asarray(current_a_hist[early])
    b_fit = np.asarray(current_b_hist[early])
    t = DT * np.arange(1, len(a_fit) + 1)

    a_slope, a_int, r2_a = linear_fit(t.tolist(), a_fit.tolist())
    b_slope, b_int, r2_b = linear_fit(t.tolist(), b_fit.tolist())

    current_early = 0.5 * (float(np.mean(a_fit)) + float(np.mean(b_fit)))
    inward = float(np.mean(a_fit)) > 0.0 and float(np.mean(b_fit)) > 0.0

    return {
        "side": float(side),
        "distance": float(distance),
        "placement": placement,
        "force_early": 0.5 * (float(np.mean(force_a_hist[early])) + float(np.mean(force_b_hist[early]))),
        "force_ok": float(np.mean(force_a_hist[early]) > 0.0 and np.mean(force_b_hist[early]) > 0.0),
        "current_a_mean": float(np.mean(a_fit)),
        "current_b_mean": float(np.mean(b_fit)),
        "current_sym_mean": current_early,
        "inward": float(inward),
        "a_slope": a_slope,
        "b_slope": b_slope,
        "a_r2": r2_a,
        "b_r2": r2_b,
        "a_int": a_int,
        "b_int": b_int,
    }


def summarize(rows: list[dict[str, float]]) -> None:
    total = len(rows)
    force_rows = sum(int(row["force_ok"]) for row in rows)
    inward_rows = sum(int(row["inward"]) for row in rows)
    slope, r2 = power_law_fit([row for row in rows if row["inward"] > 0.0], "current_sym_mean")

    print()
    print("=" * 88)
    print("SUMMARY")
    print("=" * 88)
    print(f"rows={total}")
    print(f"force attractive: {force_rows}/{total}")
    print(f"mid-plane current inward: {inward_rows}/{total}")
    print(f"current fit (inward rows only): <J_in> ~ d^{slope:+.3f}, R^2={r2:.4f}")

    for placement in PLACEMENTS:
        subset = [row for row in rows if row["placement"] == placement]
        count = sum(int(row["inward"]) for row in subset)
        slope_p, r2_p = power_law_fit([row for row in subset if row["inward"] > 0.0], "current_sym_mean")
        print(
            f"{placement:>13s}: inward {count}/{len(subset)}, "
            f"fit={slope_p:+.3f} (R^2={r2_p:.4f})"
        )


def main() -> None:
    t0 = time.time()
    print("=" * 92)
    print("STAGGERED TWO-BODY MID-PLANE LINK-CURRENT PROBE")
    print("=" * 92)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, "
        f"SIGMA={SIGMA}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, placements={PLACEMENTS}")
    print("Readout: mid-plane bond current relative to self-only")
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
                    f"current=({row['current_a_mean']:+.3e},{row['current_b_mean']:+.3e}) "
                    f"sym={row['current_sym_mean']:+.3e} "
                    f"a={row['a_slope']:+.3e} r2={row['a_r2']:.4f}"
                )
        print()

    summarize(rows)
    print()
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
