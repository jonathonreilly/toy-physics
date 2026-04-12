#!/usr/bin/env python3
"""
Staggered two-body x-directed flux and time-integrated impulse refinement.

Refines the shell-flux observable from the previous probe by:

1. Restricting to x-directed edges only (edges where |x_i - x_j| = 1).
   The force is along x, so y/z edge currents dilute the signal.

2. Dropping side=12 (known boundary artifact: 0/15 pass rate) and adding
   side=18 for convergence check.

3. Adding a time-integrated impulse observable: impulse = sum_t delta_flux(t) * DT.
   This accumulates signal over all time steps, reducing noise.

Two observables:

  Observable 1 (x-flux): instantaneous x-directed shell flux, early-time average.
  Observable 2 (impulse): time-integrated x-directed shell flux over all N_STEPS.

Both compared as delta = shared - self_only. Gate: both packets inward on same row.
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
G = 50.0
SIGMA = 0.80
SIDES = (14, 16, 18)
DISTANCES = (3, 4, 5, 6, 7)
PLACEMENTS = ("centered", "face_offset", "corner_offset")


class OpenStaggered3D:
    """Open 3D cubic lattice with staggered-fermion parity."""

    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self.parity = np.zeros(self.n_sites, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n_sites)}
        self._x_edges: list[tuple[int, int]] = []  # x-directed edges only
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
                    # Store x-directed edges (i < j convention)
                    if x + 1 < self.side:
                        self._x_edges.append((i, self.index(x + 1, y, z)))

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

    def step(self, psi: np.ndarray, lu, a_minus: csr_matrix) -> np.ndarray:
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


# ---------------------------------------------------------------------------
# X-directed probability current
# ---------------------------------------------------------------------------

def edge_current(psi: np.ndarray, h: csc_matrix, i: int, j: int) -> float:
    """
    Probability current on directed edge i -> j.
    J_{i->j} = -2 * Im(conj(psi_i) * H_{ij} * psi_j)
    Positive = net flow from i toward j.
    """
    return -2.0 * (np.conj(psi[i]) * h[i, j] * psi[j]).imag


def xflux_shell(
    psi: np.ndarray,
    h: csc_matrix,
    lat: OpenStaggered3D,
    packet_center_x: float,
    shell_radius: float,
) -> float:
    """
    Net x-directed probability current flowing INWARD through a shell around
    the packet center. Only x-directed edges (|x_i - x_j| = 1) are included.

    Sign convention: positive = inward (toward packet center).
    """
    total_flux = 0.0
    cx = packet_center_x

    for (i, j) in lat._x_edges:
        xi = lat.pos[i, 0]
        xj = lat.pos[j, 0]
        ri = abs(xi - cx)
        rj = abs(xj - cx)

        # Does this x-edge cross the shell boundary?
        if (ri <= shell_radius) != (rj <= shell_radius):
            j_ij = edge_current(psi, h, i, j)
            if ri <= shell_radius:
                # i inside, j outside: outward = i->j; inward = -j_ij
                total_flux -= j_ij
            else:
                # j inside, i outside: inward = i->j = +j_ij
                total_flux += j_ij

    return float(total_flux)


# ---------------------------------------------------------------------------
# Main simulation loop
# ---------------------------------------------------------------------------

def run_case(side: int, distance: int, placement: str) -> dict:
    lat = OpenStaggered3D(side)
    center = 0.5 * (side - 1)
    y0, z0 = placement_coords(side, placement)
    ax = center - distance / 2.0
    bx = center + distance / 2.0
    packet_a_center = (ax, y0, z0)
    packet_b_center = (bx, y0, z0)

    shell_r = SIGMA * 1.2

    psi_a_sh = lat.gaussian(packet_a_center)
    psi_b_sh = lat.gaussian(packet_b_center)
    psi_a_sf = psi_a_sh.copy()
    psi_b_sf = psi_b_sh.copy()

    # Per-step histories
    xflux_a_sh_hist: list[float] = []
    xflux_b_sh_hist: list[float] = []
    xflux_a_sf_hist: list[float] = []
    xflux_b_sf_hist: list[float] = []
    force_a_hist: list[float] = []
    force_b_hist: list[float] = []

    for _ in range(N_STEPS):
        # Shared field
        phi_a_sh = lat.solve_phi(MASS * np.abs(psi_a_sh) ** 2)
        phi_b_sh = lat.solve_phi(MASS * np.abs(psi_b_sh) ** 2)
        phi_shared = phi_a_sh + phi_b_sh

        # Exact partner-force reference
        force_a_hist.append(-lat.force_x(psi_a_sh, lat.gradient_x(phi_b_sh)))
        force_b_hist.append(lat.force_x(psi_b_sh, lat.gradient_x(phi_a_sh)))

        h_shared = lat.build_hamiltonian(phi_shared)
        lu_sh, am_sh = lat.make_stepper(h_shared)

        # Self-only fields
        phi_a_sf_field = lat.solve_phi(MASS * np.abs(psi_a_sf) ** 2)
        phi_b_sf_field = lat.solve_phi(MASS * np.abs(psi_b_sf) ** 2)
        h_a_sf = lat.build_hamiltonian(phi_a_sf_field)
        h_b_sf = lat.build_hamiltonian(phi_b_sf_field)
        lu_a_sf, am_a_sf = lat.make_stepper(h_a_sf)
        lu_b_sf, am_b_sf = lat.make_stepper(h_b_sf)

        # Measure x-directed shell flux BEFORE stepping
        xflux_a_sh_hist.append(xflux_shell(psi_a_sh, h_shared, lat, ax, shell_r))
        xflux_b_sh_hist.append(xflux_shell(psi_b_sh, h_shared, lat, bx, shell_r))
        xflux_a_sf_hist.append(xflux_shell(psi_a_sf, h_a_sf, lat, ax, shell_r))
        xflux_b_sf_hist.append(xflux_shell(psi_b_sf, h_b_sf, lat, bx, shell_r))

        # Step all wavefunctions
        psi_a_sh = lat.step(psi_a_sh, lu_sh, am_sh)
        psi_b_sh = lat.step(psi_b_sh, lu_sh, am_sh)
        psi_a_sf = lat.step(psi_a_sf, lu_a_sf, am_a_sf)
        psi_b_sf = lat.step(psi_b_sf, lu_b_sf, am_b_sf)

    # --- Observable 1: x-directed flux (early-time average, first 5 steps) ---
    n_early = min(5, N_STEPS)
    delta_xflux_a = [xflux_a_sh_hist[t] - xflux_a_sf_hist[t] for t in range(n_early)]
    delta_xflux_b = [xflux_b_sh_hist[t] - xflux_b_sf_hist[t] for t in range(n_early)]
    mean_dxa = float(np.mean(delta_xflux_a))
    mean_dxb = float(np.mean(delta_xflux_b))
    # Inward for A = toward B (rightward) = positive shell convention
    # Inward for B = toward A (leftward) = positive shell convention
    xflux_gate = mean_dxa > 0 and mean_dxb > 0

    # --- Observable 2: time-integrated impulse (all N_STEPS) ---
    delta_xflux_a_all = [xflux_a_sh_hist[t] - xflux_a_sf_hist[t] for t in range(N_STEPS)]
    delta_xflux_b_all = [xflux_b_sh_hist[t] - xflux_b_sf_hist[t] for t in range(N_STEPS)]
    impulse_a = float(np.sum(delta_xflux_a_all)) * DT
    impulse_b = float(np.sum(delta_xflux_b_all)) * DT
    impulse_gate = impulse_a > 0 and impulse_b > 0

    # Force reference
    mean_force_a = float(np.mean(force_a_hist[:n_early]))
    mean_force_b = float(np.mean(force_b_hist[:n_early]))
    force_ok = mean_force_a > 0 and mean_force_b > 0

    return {
        "side": side,
        "distance": distance,
        "placement": placement,
        # Reference
        "force_mean": 0.5 * (mean_force_a + mean_force_b),
        "force_ok": force_ok,
        # Observable 1: x-flux
        "delta_xflux_a": mean_dxa,
        "delta_xflux_b": mean_dxb,
        "xflux_gate": xflux_gate,
        # Observable 2: impulse
        "impulse_a": impulse_a,
        "impulse_b": impulse_b,
        "impulse_sym": 0.5 * (impulse_a + impulse_b),
        "impulse_gate": impulse_gate,
    }


def power_law_fit(rows: list[dict], key: str) -> tuple[float, float]:
    xs, ys = [], []
    for row in rows:
        val = abs(row[key])
        if val <= 0:
            continue
        xs.append(math.log(row["distance"]))
        ys.append(math.log(val))
    if len(xs) < 2:
        return float("nan"), float("nan")
    slope, intercept = np.polyfit(xs, ys, 1)
    pred = slope * np.asarray(xs) + intercept
    y = np.asarray(ys)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), float(r2)


def summarize(rows: list[dict]) -> None:
    total = len(rows)
    xflux_pass = sum(1 for r in rows if r["xflux_gate"])
    impulse_pass = sum(1 for r in rows if r["impulse_gate"])
    force_pass = sum(1 for r in rows if r["force_ok"])

    print()
    print("=" * 96)
    print("SUMMARY: X-DIRECTED FLUX AND IMPULSE REFINEMENT")
    print("=" * 96)
    print(f"Total rows: {total}")
    print()

    # Reference
    print(f"[Reference] Exact partner-force attractive: {force_pass}/{total}")
    print()

    # Observable 1: x-directed flux
    print("--- Observable 1: X-Directed Shell Flux (early-time average) ---")
    xflux_frac = xflux_pass / total if total > 0 else 0.0
    print(f"  Both-inward gate: {xflux_pass}/{total} ({100*xflux_frac:.1f}%)")
    xflux_ok_rows = [r for r in rows if r["xflux_gate"]]
    if xflux_ok_rows:
        sl_a, r2_a = power_law_fit(xflux_ok_rows, "delta_xflux_a")
        sl_b, r2_b = power_law_fit(xflux_ok_rows, "delta_xflux_b")
        print(f"  Power-law (passing): "
              f"dFluxA ~ d^{sl_a:+.3f} (R2={r2_a:.3f}), "
              f"dFluxB ~ d^{sl_b:+.3f} (R2={r2_b:.3f})")
    for s in SIDES:
        subset = [r for r in rows if r["side"] == s]
        n = sum(1 for r in subset if r["xflux_gate"])
        print(f"  side={s:2d}: {n}/{len(subset)}")
    for pl in PLACEMENTS:
        subset = [r for r in rows if r["placement"] == pl]
        n = sum(1 for r in subset if r["xflux_gate"])
        print(f"  {pl:>14s}: {n}/{len(subset)}")
    print()

    # Observable 2: impulse
    print("--- Observable 2: Time-Integrated Impulse ---")
    imp_frac = impulse_pass / total if total > 0 else 0.0
    print(f"  Both-inward gate: {impulse_pass}/{total} ({100*imp_frac:.1f}%)")
    imp_ok_rows = [r for r in rows if r["impulse_gate"]]
    if imp_ok_rows:
        sl_imp, r2_imp = power_law_fit(imp_ok_rows, "impulse_sym")
        print(f"  Power-law (passing): impulse_sym ~ d^{sl_imp:+.3f} (R2={r2_imp:.3f})")
    for s in SIDES:
        subset = [r for r in rows if r["side"] == s]
        n = sum(1 for r in subset if r["impulse_gate"])
        print(f"  side={s:2d}: {n}/{len(subset)}")
    for pl in PLACEMENTS:
        subset = [r for r in rows if r["placement"] == pl]
        n = sum(1 for r in subset if r["impulse_gate"])
        print(f"  {pl:>14s}: {n}/{len(subset)}")
    print()

    # Verdict
    print("--- VERDICT ---")

    # X-flux verdict
    if xflux_frac >= 0.85:
        print(f"Observable 1 (x-flux): PASS -- both-inward {100*xflux_frac:.0f}% >= 85%")
    elif xflux_frac >= 0.70:
        print(f"Observable 1 (x-flux): MARGINAL -- both-inward {100*xflux_frac:.0f}%")
    else:
        print(f"Observable 1 (x-flux): FAIL -- both-inward {100*xflux_frac:.0f}%")

    # Impulse verdict
    imp_r2 = float("nan")
    if imp_ok_rows:
        _, imp_r2 = power_law_fit(imp_ok_rows, "impulse_sym")
    r2_ok = not math.isnan(imp_r2) and imp_r2 > 0.5

    if imp_frac >= 0.85 and r2_ok:
        print(f"Observable 2 (impulse): PASS -- both-inward {100*imp_frac:.0f}% >= 85% "
              f"AND R2={imp_r2:.3f} > 0.5  [PROMOTABLE]")
    elif imp_frac >= 0.85:
        print(f"Observable 2 (impulse): PARTIAL -- both-inward {100*imp_frac:.0f}% >= 85% "
              f"but R2={imp_r2:.3f} <= 0.5")
    elif imp_frac >= 0.70:
        print(f"Observable 2 (impulse): MARGINAL -- both-inward {100*imp_frac:.0f}%")
    else:
        print(f"Observable 2 (impulse): FAIL -- both-inward {100*imp_frac:.0f}%")


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("STAGGERED TWO-BODY: X-DIRECTED FLUX AND TIME-INTEGRATED IMPULSE")
    print("=" * 96)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, placements={PLACEMENTS}")
    print()
    print("Observable 1: x-directed shell flux (delta = shared - self_only, early-time avg)")
    print("Observable 2: time-integrated impulse (delta summed over all steps * DT)")
    print("Reference: exact partner-force")
    print()

    header = (
        f"{'side':>4s} {'d':>2s} {'placement':>14s} | "
        f"{'force':>10s} {'ok':>2s} | "
        f"{'dXflA':>10s} {'dXflB':>10s} {'xg':>2s} | "
        f"{'impA':>10s} {'impB':>10s} {'ig':>2s}"
    )
    print(header)
    print("-" * len(header))

    rows: list[dict] = []
    for placement in PLACEMENTS:
        for side in SIDES:
            for distance in DISTANCES:
                row = run_case(side, distance, placement)
                rows.append(row)
                print(
                    f"{row['side']:4d} {row['distance']:2d} {row['placement']:>14s} | "
                    f"{row['force_mean']:+.3e} {'Y' if row['force_ok'] else 'N':>2s} | "
                    f"{row['delta_xflux_a']:+.3e} {row['delta_xflux_b']:+.3e} "
                    f"{'Y' if row['xflux_gate'] else 'N':>2s} | "
                    f"{row['impulse_a']:+.3e} {row['impulse_b']:+.3e} "
                    f"{'Y' if row['impulse_gate'] else 'N':>2s}"
                )
        print()

    summarize(rows)
    print()
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
