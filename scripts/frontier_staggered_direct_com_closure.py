#!/usr/bin/env python3
"""
Staggered direct-CoM closure probe on an open 3D lattice.

This is the strongest honest follow-up to the retained staggered self-consistent
two-body lane. The exact partner-force channel is already known to be clean on a
bounded open-cubic surface. The unresolved question is whether a parity-aware
direct-CoM readout can survive on that same surface.

Readout used here:
  - coarse-grain the staggered density into 2x2x2 taste cells
  - build a packet-local x-profile around each packet's initial cell
  - estimate translation by template matching against the initial local envelope
  - compare SHARED vs SELF_ONLY packet shifts

This is still an early-time bounded observable. It is not a full trajectory-law
claim unless the sign and fitted exponent survive across the audited surface.
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
WINDOW_BLOCKS = 3
SHIFT_MAX = 0.25
SHIFT_STEP = 0.001


class OpenStaggered3D:
    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.nbx = side // 2
        self.nby = side // 2
        self.nbz = side // 2
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

    def block_tensor(self, psi: np.ndarray) -> np.ndarray:
        rho = np.abs(psi) ** 2
        tensor = np.zeros((self.nbx, self.nby, self.nbz), dtype=float)
        for bx in range(self.nbx):
            x0 = 2 * bx
            for by in range(self.nby):
                y0 = 2 * by
                for bz in range(self.nbz):
                    z0 = 2 * bz
                    weight = 0.0
                    for dx in (0, 1):
                        for dy in (0, 1):
                            for dz in (0, 1):
                                weight += rho[self.index(x0 + dx, y0 + dy, z0 + dz)]
                    tensor[bx, by, bz] = weight
        return tensor

    def local_block_profile_x(
        self,
        psi: np.ndarray,
        center: tuple[float, float, float],
        radius_blocks: int = WINDOW_BLOCKS,
    ) -> tuple[np.ndarray, np.ndarray]:
        bx0 = int(np.clip(round((center[0] - 0.5) / 2.0), 0, self.nbx - 1))
        by0 = int(np.clip(round((center[1] - 0.5) / 2.0), 0, self.nby - 1))
        bz0 = int(np.clip(round((center[2] - 0.5) / 2.0), 0, self.nbz - 1))
        bx_l = max(0, bx0 - radius_blocks)
        bx_r = min(self.nbx, bx0 + radius_blocks + 1)
        by_l = max(0, by0 - radius_blocks)
        by_r = min(self.nby, by0 + radius_blocks + 1)
        bz_l = max(0, bz0 - radius_blocks)
        bz_r = min(self.nbz, bz0 + radius_blocks + 1)

        tensor = self.block_tensor(psi)
        local = tensor[bx_l:bx_r, by_l:by_r, bz_l:bz_r]
        profile = local.sum(axis=(1, 2))
        centers = 2.0 * np.arange(bx_l, bx_r, dtype=float) + 0.5
        return centers, profile


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


def estimate_shift(centers: np.ndarray, template: np.ndarray, current: np.ndarray) -> float:
    if template.sum() <= 0 or current.sum() <= 0:
        return 0.0
    x = centers.astype(float)
    template = template.astype(float) / float(template.sum())
    current = current.astype(float) / float(current.sum())
    best_shift = 0.0
    best_err = float("inf")
    for shift in np.arange(-SHIFT_MAX, SHIFT_MAX + 0.5 * SHIFT_STEP, SHIFT_STEP):
        shifted = np.interp(x, x - shift, current, left=0.0, right=0.0)
        err = float(np.sum((template - shifted) ** 2))
        if err < best_err:
            best_err = err
            best_shift = float(shift)
    return best_shift


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

    centers_a, _ = lat.local_block_profile_x(psi_a_shared, packet_a_center)
    centers_b, _ = lat.local_block_profile_x(psi_b_shared, packet_b_center)

    force_a_hist: list[float] = []
    force_b_hist: list[float] = []
    shift_a_hist: list[float] = []
    shift_b_hist: list[float] = []

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

        _, prof_a_shared = lat.local_block_profile_x(psi_a_shared, packet_a_center)
        _, prof_b_shared = lat.local_block_profile_x(psi_b_shared, packet_b_center)
        _, prof_a_self = lat.local_block_profile_x(psi_a_self, packet_a_center)
        _, prof_b_self = lat.local_block_profile_x(psi_b_self, packet_b_center)

        # A sits on the left: inward means the shared profile is shifted right
        # relative to self-only. B sits on the right: inward means the shared
        # profile is shifted left relative to self-only.
        shift_a_hist.append(estimate_shift(centers_a, prof_a_self, prof_a_shared))
        shift_b_hist.append(-estimate_shift(centers_b, prof_b_self, prof_b_shared))

        psi_a_shared = lat.step(psi_a_shared, lu_shared, am_shared)
        psi_b_shared = lat.step(psi_b_shared, lu_shared, am_shared)
        psi_a_self = lat.step(psi_a_self, lu_a_self, am_a_self)
        psi_b_self = lat.step(psi_b_self, lu_b_self, am_b_self)

    t = DT * np.arange(1, min(6, len(shift_a_hist)) + 1)
    shift_a_fit = np.asarray(shift_a_hist[: len(t)])
    shift_b_fit = np.asarray(shift_b_hist[: len(t)])

    a_a, r2_a = fit_early_accel(t, shift_a_fit)
    a_b, r2_b = fit_early_accel(t, shift_b_fit)

    early = slice(0, len(t))
    force_early = 0.5 * (
        float(np.mean(force_a_hist[early])) + float(np.mean(force_b_hist[early]))
    )
    inward = float(np.mean(shift_a_fit)) > 0.0 and float(np.mean(shift_b_fit)) > 0.0
    shift_sym_mean = 0.5 * (float(np.mean(shift_a_fit)) + float(np.mean(shift_b_fit)))
    a_sym = 0.5 * (a_a + a_b)

    return {
        "side": float(side),
        "distance": float(distance),
        "placement": placement,
        "force_early": force_early,
        "force_ok": float(force_early > 0.0),
        "shift_a_mean": float(np.mean(shift_a_fit)),
        "shift_b_mean": float(np.mean(shift_b_fit)),
        "shift_sym_mean": shift_sym_mean,
        "inward": float(inward),
        "a_sym": a_sym,
        "a_r2": 0.5 * (r2_a + r2_b),
    }


def summarize(rows: list[dict[str, float]]) -> None:
    total = len(rows)
    force_rows = sum(int(row["force_ok"]) for row in rows)
    inward_rows = sum(int(row["inward"]) for row in rows)
    slope, r2 = power_law_fit([row for row in rows if row["inward"] > 0.0], "shift_sym_mean")

    print()
    print("=" * 88)
    print("SUMMARY")
    print("=" * 88)
    print(f"rows={total}")
    print(f"force attractive: {force_rows}/{total}")
    print(f"template-shift inward: {inward_rows}/{total}")
    print(
        f"template-shift fit (inward rows only): <dx_mut> ~ d^{slope:+.3f}, "
        f"R^2={r2:.4f}"
    )

    for placement in PLACEMENTS:
        subset = [row for row in rows if row["placement"] == placement]
        count = sum(int(row["inward"]) for row in subset)
        slope_p, r2_p = power_law_fit(
            [row for row in subset if row["inward"] > 0.0], "shift_sym_mean"
        )
        print(
            f"{placement:>13s}: inward {count}/{len(subset)}, "
            f"fit={slope_p:+.3f} (R^2={r2_p:.4f})"
        )


def main() -> None:
    t0 = time.time()
    print("=" * 88)
    print("STAGGERED DIRECT-COM CLOSURE PROBE")
    print("=" * 88)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, "
        f"SIGMA={SIGMA}, WINDOW_BLOCKS={WINDOW_BLOCKS}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, placements={PLACEMENTS}")
    print("Readout: 2x2x2 cell-envelope template shift vs self-only")
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
                    f"shift=({row['shift_a_mean']:+.3e},{row['shift_b_mean']:+.3e}) "
                    f"sym={row['shift_sym_mean']:+.3e} "
                    f"a={row['a_sym']:+.3e} r2={row['a_r2']:.4f}"
                )
        print()

    summarize(rows)
    print()
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
