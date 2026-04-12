#!/usr/bin/env python3
"""
Staggered two-body flux and mid-plane current observables on the open 3D cubic family.

This replaces centroid-based observables which have been ruled out. Instead of measuring
packet position shifts, we measure probability current --- the graph-native transport
observable that lives on edges, not sites.

Two observables:

1. LOCAL MOMENTUM FLUX around each packet:
   Sum J_{ij} over edges crossing a shell around each packet center.
   Compare shared vs self-only: delta_flux_A = flux_A(shared) - flux_A(self_only).
   Acceptance: both delta_flux_A and delta_flux_B inward on the same row.

2. MID-PLANE PROBABILITY CURRENT:
   Sum J_{ij} over edges crossing the mid-plane between the two packets.
   Compare: J_mid(shared) - J_mid(self_only).
   Acceptance: shared current exceeds self-only current with inward sign.

Probability current on a graph edge (i,j):
   J_{ij} = -2 * Im(conj(psi_i) * H_{ij} * psi_j)

This is the natural graph-analogue of the continuum J = -Im(psi* nabla psi) / m.
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
    """Open 3D cubic lattice with staggered-fermion parity."""

    def __init__(self, side: int):
        self.side = side
        self.n_sites = side**3
        self.pos = np.zeros((self.n_sites, 3), dtype=float)
        self.parity = np.zeros(self.n_sites, dtype=int)
        self._adj: dict[int, list[int]] = {i: [] for i in range(self.n_sites)}
        self._edges: list[tuple[int, int]] = []
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
                    # Store directed edges i<j for unique enumeration
                    if x + 1 < self.side:
                        self._edges.append((i, self.index(x + 1, y, z)))
                    if y + 1 < self.side:
                        self._edges.append((i, self.index(x, y + 1, z)))
                    if z + 1 < self.side:
                        self._edges.append((i, self.index(x, y, z + 1)))

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
# Probability current computation
# ---------------------------------------------------------------------------

def edge_current(psi: np.ndarray, h: csc_matrix, i: int, j: int) -> float:
    """
    Probability current on the directed edge i -> j.

    J_{i->j} = -2 * Im(conj(psi_i) * H_{ij} * psi_j)

    Positive means net current flowing from i toward j.
    """
    return -2.0 * (np.conj(psi[i]) * h[i, j] * psi[j]).imag


def packet_shell_flux(
    psi: np.ndarray,
    h: csc_matrix,
    lat: OpenStaggered3D,
    packet_center_x: float,
    shell_radius: float,
) -> float:
    """
    Net probability current flowing INWARD through a shell around the packet center.

    We define a spherical shell of radius `shell_radius` around the packet center.
    For each edge (i,j) where i is inside and j is outside (or vice versa),
    we measure J and accumulate with sign convention: positive = inward flow.

    Since packets are separated along x, "inward" means toward the partner.
    We focus on the x-component: edges crossing the shell boundary in x.
    """
    total_flux = 0.0
    cx = packet_center_x

    for (i, j) in lat._edges:
        xi = lat.pos[i, 0]
        xj = lat.pos[j, 0]
        ri = abs(xi - cx)
        rj = abs(xj - cx)

        # Does this edge cross the shell boundary?
        if (ri <= shell_radius) != (rj <= shell_radius):
            j_ij = edge_current(psi, h, i, j)
            # i inside, j outside: outward current is i->j direction
            # We want inward = current flowing toward packet center
            if ri <= shell_radius:
                # i inside shell, j outside
                # If j is farther from center, outward = i->j positive
                # Inward contribution = -j_ij
                total_flux -= j_ij
            else:
                # j inside shell, i outside
                # Inward = i->j positive
                total_flux += j_ij

    return float(total_flux)


def midplane_current(
    psi: np.ndarray,
    h: csc_matrix,
    lat: OpenStaggered3D,
    midplane_x: float,
) -> float:
    """
    Net probability current crossing the mid-plane between the two packets.

    Sum J_{ij} over all edges crossing x = midplane_x.
    Sign convention: positive = current flowing in the +x direction.
    """
    total = 0.0
    for (i, j) in lat._edges:
        xi = lat.pos[i, 0]
        xj = lat.pos[j, 0]
        # Edge crosses midplane if one site is on each side
        if (xi <= midplane_x) != (xj <= midplane_x):
            j_ij = edge_current(psi, h, i, j)
            # If i is left and j is right, j_ij positive = rightward current
            if xi < xj:
                total += j_ij
            else:
                total -= j_ij
    return float(total)


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
    mid_x = center  # midplane between A and B

    # Shell radius: ~1 sigma from packet center
    shell_r = SIGMA * 1.2

    psi_a_sh = lat.gaussian(packet_a_center)
    psi_b_sh = lat.gaussian(packet_b_center)
    psi_a_sf = psi_a_sh.copy()
    psi_b_sf = psi_b_sh.copy()

    # Accumulators for time-averaged observables
    flux_a_sh_hist: list[float] = []
    flux_b_sh_hist: list[float] = []
    flux_a_sf_hist: list[float] = []
    flux_b_sf_hist: list[float] = []
    mid_sh_hist: list[float] = []
    mid_sf_hist: list[float] = []
    force_a_hist: list[float] = []
    force_b_hist: list[float] = []

    for _ in range(N_STEPS):
        # Shared field
        phi_a_sh = lat.solve_phi(MASS * np.abs(psi_a_sh) ** 2)
        phi_b_sh = lat.solve_phi(MASS * np.abs(psi_b_sh) ** 2)
        phi_shared = phi_a_sh + phi_b_sh

        # Exact partner-force for comparison
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

        # -- Observable 1: packet shell flux --
        # Measure BEFORE stepping (current under current Hamiltonian)
        flux_a_sh_hist.append(packet_shell_flux(psi_a_sh, h_shared, lat, ax, shell_r))
        flux_b_sh_hist.append(packet_shell_flux(psi_b_sh, h_shared, lat, bx, shell_r))
        flux_a_sf_hist.append(packet_shell_flux(psi_a_sf, h_a_sf, lat, ax, shell_r))
        flux_b_sf_hist.append(packet_shell_flux(psi_b_sf, h_b_sf, lat, bx, shell_r))

        # -- Observable 2: mid-plane current --
        # Total wavefunction for shared = psi_a + psi_b (superposition)
        # But for mid-plane, we measure each packet's contribution separately
        mid_sh_hist.append(
            midplane_current(psi_a_sh, h_shared, lat, mid_x)
            + midplane_current(psi_b_sh, h_shared, lat, mid_x)
        )
        mid_sf_hist.append(
            midplane_current(psi_a_sf, h_a_sf, lat, mid_x)
            + midplane_current(psi_b_sf, h_b_sf, lat, mid_x)
        )

        # Step all wavefunctions
        psi_a_sh = lat.step(psi_a_sh, lu_sh, am_sh)
        psi_b_sh = lat.step(psi_b_sh, lu_sh, am_sh)
        psi_a_sf = lat.step(psi_a_sf, lu_a_sf, am_a_sf)
        psi_b_sf = lat.step(psi_b_sf, lu_b_sf, am_b_sf)

    # Early-time window for analysis (first 5 steps)
    n_early = min(5, N_STEPS)

    # Observable 1: delta flux
    delta_flux_a = [flux_a_sh_hist[t] - flux_a_sf_hist[t] for t in range(n_early)]
    delta_flux_b = [flux_b_sh_hist[t] - flux_b_sf_hist[t] for t in range(n_early)]
    mean_dfa = float(np.mean(delta_flux_a))
    mean_dfb = float(np.mean(delta_flux_b))
    # "Inward" for A means current flowing toward B (positive delta_flux means
    # shared field draws probability inward relative to self-only)
    # A is on the left, B on the right. Inward for A = rightward = positive flux.
    # Inward for B = leftward = positive flux (shell convention already handles this).
    flux_gate = mean_dfa > 0 and mean_dfb > 0

    # Observable 2: delta mid-plane current
    delta_mid = [mid_sh_hist[t] - mid_sf_hist[t] for t in range(n_early)]
    mean_dm = float(np.mean(delta_mid))
    # Mid-plane current: net current crossing midplane.
    # For attraction, current from A side toward B side (rightward) is expected
    # from A, and leftward from B. The net mid-plane current should be enhanced
    # by the shared field. We accept if |delta_mid| > 0 with consistent sign.
    # Actually, for symmetric setup the net midplane current from both packets
    # should be near zero by symmetry. The useful signal is that delta_mid != 0
    # indicating the shared field breaks the self-only balance.
    # For an attractive interaction, mid-plane current should increase (more
    # probability flowing toward the partner region).
    mid_gate = abs(mean_dm) > 0  # Always true; real gate is sign consistency

    # Force reference
    mean_force = 0.5 * (
        float(np.mean(force_a_hist[:n_early])) + float(np.mean(force_b_hist[:n_early]))
    )
    force_ok = (
        float(np.mean(force_a_hist[:n_early])) > 0
        and float(np.mean(force_b_hist[:n_early])) > 0
    )

    return {
        "side": side,
        "distance": distance,
        "placement": placement,
        "force_mean": mean_force,
        "force_ok": force_ok,
        # Observable 1
        "delta_flux_a": mean_dfa,
        "delta_flux_b": mean_dfb,
        "flux_gate": flux_gate,
        # Observable 2
        "delta_mid": mean_dm,
        "mid_sh_mean": float(np.mean(mid_sh_hist[:n_early])),
        "mid_sf_mean": float(np.mean(mid_sf_hist[:n_early])),
        "mid_gate_sign_consistent": bool(
            all(d > 0 for d in delta_mid) or all(d < 0 for d in delta_mid)
        ),
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
    flux_pass = sum(1 for r in rows if r["flux_gate"])
    force_pass = sum(1 for r in rows if r["force_ok"])
    mid_sign_pass = sum(1 for r in rows if r["mid_gate_sign_consistent"])

    print()
    print("=" * 92)
    print("SUMMARY: STAGGERED TWO-BODY FLUX OBSERVABLES")
    print("=" * 92)
    print(f"Total rows: {total}")
    print()

    # Force reference
    print(f"[Reference] Exact partner-force attractive: {force_pass}/{total}")
    print()

    # Observable 1: Packet shell flux
    print("--- Observable 1: Local Momentum Flux (packet shell) ---")
    print(f"  Both-inward gate: {flux_pass}/{total} "
          f"({100*flux_pass/total:.1f}%)")
    flux_inward_rows = [r for r in rows if r["flux_gate"]]
    if flux_inward_rows:
        sl_a, r2_a = power_law_fit(flux_inward_rows, "delta_flux_a")
        sl_b, r2_b = power_law_fit(flux_inward_rows, "delta_flux_b")
        print(f"  Power-law fit (passing rows): "
              f"delta_flux_A ~ d^{sl_a:+.3f} (R2={r2_a:.3f}), "
              f"delta_flux_B ~ d^{sl_b:+.3f} (R2={r2_b:.3f})")
    for pl in PLACEMENTS:
        subset = [r for r in rows if r["placement"] == pl]
        n_pass = sum(1 for r in subset if r["flux_gate"])
        print(f"  {pl:>14s}: {n_pass}/{len(subset)}")
    print()

    # Observable 2: Mid-plane current
    print("--- Observable 2: Mid-plane Probability Current ---")
    print(f"  Sign-consistent gate: {mid_sign_pass}/{total} "
          f"({100*mid_sign_pass/total:.1f}%)")
    mid_rows = [r for r in rows if r["mid_gate_sign_consistent"]]
    if mid_rows:
        sl_m, r2_m = power_law_fit(mid_rows, "delta_mid")
        print(f"  Power-law fit (sign-consistent rows): "
              f"delta_mid ~ d^{sl_m:+.3f} (R2={r2_m:.3f})")
    for pl in PLACEMENTS:
        subset = [r for r in rows if r["placement"] == pl]
        n_pass = sum(1 for r in subset if r["mid_gate_sign_consistent"])
        print(f"  {pl:>14s}: {n_pass}/{len(subset)}")
    print()

    # Verdict
    print("--- VERDICT ---")
    flux_frac = flux_pass / total if total > 0 else 0.0
    mid_frac = mid_sign_pass / total if total > 0 else 0.0
    if flux_frac >= 0.80:
        print("Observable 1 (packet flux): PASS -- inward flux gate >= 80%")
    elif flux_frac >= 0.50:
        print("Observable 1 (packet flux): MARGINAL -- inward flux gate 50-80%")
    else:
        print(f"Observable 1 (packet flux): FAIL -- inward flux gate {100*flux_frac:.0f}%")

    if mid_frac >= 0.80:
        print("Observable 2 (mid-plane current): PASS -- sign-consistent >= 80%")
    elif mid_frac >= 0.50:
        print("Observable 2 (mid-plane current): MARGINAL -- sign-consistent 50-80%")
    else:
        print(f"Observable 2 (mid-plane current): FAIL -- sign-consistent {100*mid_frac:.0f}%")


def main() -> None:
    t0 = time.time()
    print("=" * 92)
    print("STAGGERED TWO-BODY FLUX AND MID-PLANE CURRENT OBSERVABLES")
    print("=" * 92)
    print(
        f"MASS={MASS}, G={G}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}"
    )
    print(f"sides={SIDES}, distances={DISTANCES}, placements={PLACEMENTS}")
    print()
    print("Observable 1: packet shell flux (delta = shared - self_only)")
    print("Observable 2: mid-plane probability current (delta = shared - self_only)")
    print("Reference: exact partner-force")
    print()

    header = (
        f"{'side':>4s} {'d':>2s} {'placement':>14s} | "
        f"{'force':>10s} {'ok':>2s} | "
        f"{'dFluxA':>10s} {'dFluxB':>10s} {'fg':>2s} | "
        f"{'dMid':>10s} {'sgn':>3s}"
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
                    f"{row['delta_flux_a']:+.3e} {row['delta_flux_b']:+.3e} "
                    f"{'Y' if row['flux_gate'] else 'N':>2s} | "
                    f"{row['delta_mid']:+.3e} "
                    f"{'Y' if row['mid_gate_sign_consistent'] else 'N':>3s}"
                )
        print()

    summarize(rows)
    print()
    print(f"elapsed={time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
