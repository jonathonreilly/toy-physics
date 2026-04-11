#!/usr/bin/env python3
"""
frontier_bmv_prediction.py

Quantitative prediction for the Bose-Marletto-Vedral (BMV) experiment
using our Wilson-fermion lattice model.

BMV setup:
  Two masses m1, m2 separated by distance d. One mass (A) is placed in a
  spatial superposition of two locations (delta_x apart). The gravitational
  interaction with mass B accumulates a differential phase between the two
  branches. After time T:

    delta_phi = G * m1 * m2 * T * delta_x / (hbar * d^2)

  The resulting entanglement entropy is:
    S = H_binary( (1 + cos(delta_phi)) / 2 )

Our lattice protocol:
  1. Particle A in superposition at (center-1, center, center) and
     (center+1, center, center), so delta_x = 2 lattice units.
  2. Particle B at (center, center+d, center) for d = 3,4,5,6,7.
  3. Each branch: B's Poisson field evaluated at A's location gives a
     different potential. The wavefunction evolves under this potential.
  4. Phase difference between branches grows with T.
  5. Extract effective G from the lattice data.

Wilson 3D, side=15, mu2=0.001, open BC.

Hypothesis: delta_phi grows linearly in T and scales as 1/d^2 (Newton).
Falsification: nonlinear T-dependence or wrong d-scaling.
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve

# ── lattice parameters ──────────────────────────────────────────────────
SIDE = 15
N = SIDE ** 3
CENTER = SIDE // 2  # = 7

MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
G_VAL = 5.0
MU2 = 0.001
SIGMA = 1.0

N_STEPS_MAX = 20
DELTA_X = 2  # superposition separation in lattice units
DISTANCES = [3, 4, 5, 6, 7]


# ── lattice infrastructure ──────────────────────────────────────────────
def site_index(x, y, z):
    return x * SIDE ** 2 + y * SIDE + z


class OpenLattice:
    def __init__(self):
        self.n = N
        self.pos = np.zeros((N, 3))
        self.adj = [[] for _ in range(N)]
        for x in range(SIDE):
            for y in range(SIDE):
                for z in range(SIDE):
                    i = site_index(x, y, z)
                    self.pos[i] = [x, y, z]
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < SIDE and 0 <= ny < SIDE and 0 <= nz < SIDE:
                            self.adj[i].append(site_index(nx, ny, nz))
        self.lap = self._build_laplacian()
        self.poisson_op = (self.lap - MU2 * sparse.eye(N) - REG * sparse.eye(N)).tocsc()

    def _build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(N):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))

    def solve_poisson(self, rho):
        rhs = -4.0 * np.pi * G_VAL * rho
        return spsolve(self.poisson_op, rhs).real

    def build_wilson_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(N):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))

    def gaussian_wavepacket(self, center):
        psi = np.zeros(N, dtype=complex)
        cx, cy, cz = center
        for i in range(N):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * SIGMA ** 2))
        psi /= np.linalg.norm(psi)
        return psi

    def evolve(self, psi, H):
        psi_new = expm_multiply(-1j * DT * H, psi)
        psi_new /= np.linalg.norm(psi_new)
        return psi_new


def binary_entropy(p):
    """H_binary(p) = -p log2 p - (1-p) log2 (1-p)."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


# ── BMV simulation ──────────────────────────────────────────────────────
def run_bmv(lat, d):
    """
    Run BMV protocol for separation d.

    Branch L: A at (center - 1, center, center), B at (center, center + d, center)
    Branch R: A at (center + 1, center, center), B at (center, center + d, center)

    In each branch, B sources a gravitational potential. A evolves in that potential.
    The phase difference between the branches is the BMV signal.

    Returns: (delta_phi[T], entropy[T]) arrays of length N_STEPS_MAX+1.
    """
    # Positions
    pos_A_left = (CENTER - 1, CENTER, CENTER)
    pos_A_right = (CENTER + 1, CENTER, CENTER)
    pos_B = (CENTER, CENTER + d, CENTER)

    # B's wavepacket (same in both branches)
    psi_B = lat.gaussian_wavepacket(pos_B)
    rho_B = np.abs(psi_B) ** 2

    # Solve for B's gravitational potential (static source approximation)
    phi_B = lat.solve_poisson(rho_B)

    # Build Hamiltonian from B's field
    H_B_field = lat.build_wilson_hamiltonian(phi_B)

    # Also build free Hamiltonian (no gravitational field) for reference
    H_free = lat.build_wilson_hamiltonian(np.zeros(N))

    # Initialize A in each branch
    psi_A_left = lat.gaussian_wavepacket(pos_A_left)
    psi_A_right = lat.gaussian_wavepacket(pos_A_right)

    # Track phases
    delta_phi = np.zeros(N_STEPS_MAX + 1)
    entropy = np.zeros(N_STEPS_MAX + 1)

    # Also track free evolution for comparison
    psi_A_left_free = psi_A_left.copy()
    psi_A_right_free = psi_A_right.copy()

    # Initial phase difference (should be ~0)
    phase_left = np.angle(np.vdot(lat.gaussian_wavepacket(pos_A_left), psi_A_left))
    phase_right = np.angle(np.vdot(lat.gaussian_wavepacket(pos_A_right), psi_A_right))
    delta_phi[0] = phase_left - phase_right

    for t in range(N_STEPS_MAX):
        # Evolve both branches under B's gravitational field
        psi_A_left = lat.evolve(psi_A_left, H_B_field)
        psi_A_right = lat.evolve(psi_A_right, H_B_field)

        # Evolve free references
        psi_A_left_free = lat.evolve(psi_A_left_free, H_free)
        psi_A_right_free = lat.evolve(psi_A_right_free, H_free)

        # Phase accumulated relative to free evolution:
        # The gravitational phase for each branch is the phase of the overlap
        # <psi_free | psi_grav>
        overlap_left = np.vdot(psi_A_left_free, psi_A_left)
        overlap_right = np.vdot(psi_A_right_free, psi_A_right)

        grav_phase_left = np.angle(overlap_left)
        grav_phase_right = np.angle(overlap_right)

        dphi = grav_phase_left - grav_phase_right
        delta_phi[t + 1] = dphi

        # Entanglement entropy from phase
        p = 0.5 * (1 + np.cos(dphi))
        entropy[t + 1] = binary_entropy(p)

    return delta_phi, entropy


def main():
    print("=" * 80)
    print("BMV EXPERIMENT PREDICTION FROM WILSON-FERMION LATTICE MODEL")
    print("=" * 80)
    print(f"Lattice: {SIDE}^3 = {N} sites, open BC")
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, G={G_VAL}, mu2={MU2}")
    print(f"SIGMA={SIGMA}, delta_x={DELTA_X} (superposition separation)")
    print(f"Distances: {DISTANCES}")
    print(f"Time steps: 0..{N_STEPS_MAX}")
    print()

    t0_total = time.time()
    print("Building lattice...", flush=True)
    lat = OpenLattice()
    print(f"  Lattice built in {time.time() - t0_total:.1f}s")
    print()

    # ── collect results ─────────────────────────────────────────────────
    all_dphi = {}
    all_entropy = {}

    for d in DISTANCES:
        t0 = time.time()
        print(f"Running BMV for d={d}...", flush=True)
        dphi, ent = run_bmv(lat, d)
        elapsed = time.time() - t0
        all_dphi[d] = dphi
        all_entropy[d] = ent
        print(f"  d={d}: delta_phi(T=5)={dphi[5]:.6f}, delta_phi(T=10)={dphi[10]:.6f}, "
              f"delta_phi(T=20)={dphi[20]:.6f}  ({elapsed:.1f}s)")

    # ── unwrap phase for continuity ────────────────────────────────────
    for d in DISTANCES:
        all_dphi[d] = np.unwrap(all_dphi[d])

    # Recompute entropy from unwrapped phases
    for d in DISTANCES:
        for t in range(N_STEPS_MAX + 1):
            p = 0.5 * (1 + np.cos(all_dphi[d][t]))
            all_entropy[d][t] = binary_entropy(p)

    # ── results table ───────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("PHASE ACCUMULATION: delta_phi(T, d)")
    print("=" * 80)
    header = f"{'T':>3s}"
    for d in DISTANCES:
        header += f"  {'d=' + str(d):>12s}"
    print(header)
    print("-" * (3 + 14 * len(DISTANCES)))
    for t in range(N_STEPS_MAX + 1):
        line = f"{t:3d}"
        for d in DISTANCES:
            line += f"  {all_dphi[d][t]:12.6f}"
        print(line)

    # ── entropy table ───────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("ENTANGLEMENT ENTROPY: S(T, d)")
    print("=" * 80)
    header = f"{'T':>3s}"
    for d in DISTANCES:
        header += f"  {'d=' + str(d):>12s}"
    print(header)
    print("-" * (3 + 14 * len(DISTANCES)))
    for t in range(N_STEPS_MAX + 1):
        line = f"{t:3d}"
        for d in DISTANCES:
            line += f"  {all_entropy[d][t]:12.6f}"
        print(line)

    # ── linearity check ─────────────────────────────────────────────────
    # Phase grows as ~T^2 at early times (acceleration from rest) then
    # linearizes once the wavepacket is fully in the potential gradient.
    # Use late window (steps 5..18) for the linear fit.
    print()
    print("=" * 80)
    print("LINEARITY CHECK: delta_phi vs T")
    print("=" * 80)
    print("Fit delta_phi(T) = slope * T + intercept over steps 5..18")
    print()

    slopes = {}
    for d in DISTANCES:
        t_arr = np.arange(5, 19)
        dphi_arr = all_dphi[d][5:19]
        coeffs = np.polyfit(t_arr, dphi_arr, 1)
        slope = coeffs[0]
        intercept = coeffs[1]
        pred = np.polyval(coeffs, t_arr)
        ss_res = np.sum((dphi_arr - pred) ** 2)
        ss_tot = np.sum((dphi_arr - dphi_arr.mean()) ** 2)
        r2 = 1 - ss_res / (ss_tot + 1e-30) if ss_tot > 1e-30 else 1.0
        slopes[d] = slope
        print(f"  d={d}: slope = {slope:.8f}/step, intercept = {intercept:.6f}, R^2 = {r2:.6f}")

    # ── distance law check ──────────────────────────────────────────────
    print()
    print("=" * 80)
    print("DISTANCE LAW: slope(d) ~ 1/d^alpha")
    print("=" * 80)

    d_arr = np.array(DISTANCES, dtype=float)
    slope_arr = np.array([slopes[d] for d in DISTANCES])
    abs_slope = np.abs(slope_arr)

    mask = abs_slope > 1e-15
    if mask.sum() >= 2:
        log_d = np.log(d_arr[mask])
        log_s = np.log(abs_slope[mask])
        coeffs_d = np.polyfit(log_d, log_s, 1)
        alpha = coeffs_d[0]
        pred_d = np.polyval(coeffs_d, log_d)
        ss_res_d = np.sum((log_s - pred_d) ** 2)
        ss_tot_d = np.sum((log_s - log_s.mean()) ** 2)
        r2_d = 1 - ss_res_d / (ss_tot_d + 1e-30) if ss_tot_d > 1e-30 else 1.0

        print(f"  Power law fit: |slope| ~ d^{alpha:.3f}")
        print(f"  R^2 = {r2_d:.6f}")
        print(f"  Newton predicts: alpha = -2.0")
        print(f"  Deviation from Newton: {alpha - (-2.0):+.3f}")
    else:
        alpha = float("nan")
        r2_d = float("nan")
        print("  Insufficient data for power law fit")

    # ── extract effective G ─────────────────────────────────────────────
    print()
    print("=" * 80)
    print("EFFECTIVE GRAVITATIONAL COUPLING")
    print("=" * 80)
    print()
    print("Continuum BMV prediction: delta_phi = G * m^2 * T * delta_x / (hbar * d^2)")
    print("In lattice units (hbar=1, m=1): delta_phi / T = G_eff * delta_x / d^2")
    print(f"With delta_x = {DELTA_X}:")
    print()

    g_eff_values = {}
    for d in DISTANCES:
        # G_eff = slope * d^2 / delta_x
        g_eff = slopes[d] * d ** 2 / DELTA_X
        g_eff_values[d] = g_eff
        print(f"  d={d}: slope={slopes[d]:+.8f}, G_eff = {g_eff:.8f}")

    g_eff_mean = np.mean(list(g_eff_values.values()))
    g_eff_std = np.std(list(g_eff_values.values()))
    print(f"\n  G_eff (mean over d) = {g_eff_mean:.8f} +/- {g_eff_std:.8f}")
    print(f"  Consistency (std/mean) = {abs(g_eff_std / g_eff_mean) * 100:.1f}%"
          if abs(g_eff_mean) > 1e-15 else "  (signal too weak)")

    # ── concrete BMV numbers ────────────────────────────────────────────
    print()
    print("=" * 80)
    print("CONCRETE BMV PREDICTION (lattice units)")
    print("=" * 80)
    print()
    print(f"For a BMV experiment with two unit masses, superposition delta_x={DELTA_X}:")
    print()
    print(f"  {'d':>3s}  {'dphi/T':>14s}  {'dphi(T=10)':>14s}  {'dphi(T=20)':>14s}  {'S(T=20)':>10s}")
    print("  " + "-" * 62)
    for d in DISTANCES:
        rate = slopes[d]
        dphi10 = all_dphi[d][10]
        dphi20 = all_dphi[d][20]
        s20 = all_entropy[d][20]
        print(f"  {d:3d}  {rate:+14.8f}  {dphi10:+14.8f}  {dphi20:+14.8f}  {s20:10.6f}")

    # ── phase rate vs 1/d^2 plot data ───────────────────────────────────
    print()
    print("=" * 80)
    print("SCALING VERIFICATION: slope vs 1/d^2")
    print("=" * 80)
    print()
    print(f"  {'d':>3s}  {'1/d^2':>10s}  {'slope':>14s}  {'slope*d^2':>14s}")
    print("  " + "-" * 46)
    for d in DISTANCES:
        inv_d2 = 1.0 / d ** 2
        product = slopes[d] * d ** 2
        print(f"  {d:3d}  {inv_d2:10.6f}  {slopes[d]:+14.8f}  {product:+14.8f}")

    # ── verdict ─────────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Check linearity in T (same window as fit)
    t_arr_check = np.arange(5, 19)
    r2_vals = []
    for d in DISTANCES:
        dphi_check = all_dphi[d][5:19]
        coeffs_check = np.polyfit(t_arr_check, dphi_check, 1)
        pred_check = np.polyval(coeffs_check, t_arr_check)
        ss_r = np.sum((dphi_check - pred_check) ** 2)
        ss_t = np.sum((dphi_check - dphi_check.mean()) ** 2)
        r2_check = 1 - ss_r / (ss_t + 1e-30) if ss_t > 1e-30 else 1.0
        r2_vals.append(r2_check)

    min_r2_linear = min(r2_vals)
    print(f"  Linear phase growth (delta_phi ~ T): min R^2 = {min_r2_linear:.6f}",
          "PASS" if min_r2_linear > 0.95 else "FAIL")

    if not np.isnan(alpha):
        print(f"  Distance law (slope ~ 1/d^alpha):    alpha = {alpha:.3f} (Newton: -2.0), R^2 = {r2_d:.4f}",
              "PASS" if abs(alpha - (-2.0)) < 0.5 and r2_d > 0.9 else "MARGINAL")

    print(f"  Effective G (lattice units):          G_eff = {g_eff_mean:.6f} +/- {g_eff_std:.6f}")

    has_signal = any(abs(slopes[d]) > 1e-8 for d in DISTANCES)
    print()
    if has_signal and min_r2_linear > 0.9:
        print("  BMV PREDICTION: The model predicts a measurable gravitational phase.")
        print(f"  At d=3: delta_phi accumulates at rate {slopes[3]:+.6f} per time step.")
        print(f"  After T=20 steps: delta_phi = {all_dphi[3][20]:+.6f}, "
              f"entanglement entropy S = {all_entropy[3][20]:.6f} bits.")
        print(f"  The effective coupling G_eff = {g_eff_mean:.6f} in lattice units.")
    else:
        print("  BMV PREDICTION: Signal is weak or nonlinear — further investigation needed.")

    total_time = time.time() - t0_total
    print(f"\n  Total runtime: {total_time:.1f}s")


if __name__ == "__main__":
    main()
