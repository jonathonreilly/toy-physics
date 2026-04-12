#!/usr/bin/env python3
"""
CRITICAL CONTROL: Does random disorder on the Wilson lattice also produce
a -2.0 distance exponent?

If yes: the -2.02 exponent is just the lattice Green's function gradient,
reproducible by any smooth positive potential -- not specifically self-consistent
gravity.

Three conditions tested:
  1. SELF-CONSISTENT (Hartree): standard two-body with backreaction
  2. ANDERSON: Poisson-smoothed random potential (same spatial smoothness as
     gravity, but NOT self-consistent). 5 random seeds for error bars.
  3. FROZEN: self-consistent Phi from t=0, held fixed (no backreaction)

Key discriminator:
  - ANDERSON ~ -2 exponent => the -2 is from Poisson Green's function, not gravity
  - ANDERSON != -2         => self-consistency matters for the distance law
  - FROZEN   ~ SELF-CONSISTENT => backreaction doesn't affect the distance law
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

# ── parameters ───────────────────────────────────────────────────────────
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
MU2 = 0.001
G = 5.0
N_SIDE = 20
N = N_SIDE**3  # 8000
N_STEPS = 15
SIGMA = 1.0
REG = 1e-6  # tiny regulariser for solver stability


# ── open-boundary lattice ────────────────────────────────────────────────
class OpenLattice:
    """3D cubic lattice with open (Dirichlet) boundary conditions."""

    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        rows, cols, vals = [], [], []
        self._adj = [[] for _ in range(self.n)]

        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = x * side * side + y * side + z
                    self.pos[i] = [x, y, z]
                    n_nbrs = 0
                    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            j = nx * side * side + ny * side + nz
                            self._adj[i].append(j)
                            rows.append(i); cols.append(j); vals.append(1.0)
                            n_nbrs += 1
                    rows.append(i); cols.append(i); vals.append(-float(n_nbrs))

        self.lap = sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))
        # Poisson operator: (Lap - mu2*I) with small regulariser
        self.poisson_op = (self.lap - MU2 * sparse.eye(self.n) - REG * sparse.eye(self.n)).tocsc()

    def gaussian(self, center, sigma=SIGMA):
        cx, cy, cz = center
        dx = self.pos[:, 0] - cx
        dy = self.pos[:, 1] - cy
        dz = self.pos[:, 2] - cz
        r2 = dx**2 + dy**2 + dz**2
        psi = np.exp(-r2 / (2 * sigma**2)).astype(complex)
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho, g_val):
        rhs = -4.0 * np.pi * g_val * rho
        return spsolve(self.poisson_op, rhs).real

    def build_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for j in self._adj[i]:
                if j <= i:
                    continue
                rows.append(i); cols.append(j); vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j); cols.append(i); vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self._adj[i])
            rows.append(i); cols.append(i); vals.append(diag)
        return sparse.csc_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def cn_step(self, psi, H):
        """Crank-Nicolson: (I + iH dt/2) psi_new = (I - iH dt/2) psi."""
        half = 1j * H * (DT / 2.0)
        eye = sparse.eye(self.n, format='csc')
        lhs = (eye + half).tocsc()
        rhs_vec = (eye - half).dot(psi)
        psi_new = spsolve(lhs, rhs_vec)
        psi_new /= np.linalg.norm(psi_new)
        return psi_new

    def com_x(self, psi):
        rho = np.abs(psi)**2
        return float(np.sum(rho * self.pos[:, 0]))


# ── acceleration from separation trajectory ──────────────────────────────
def acceleration(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


# ── run one two-body configuration ───────────────────────────────────────
def run_two_body(lat, mode, center_a, center_b, phi_ext=None):
    """
    Modes:
      SELF_CONSISTENT - Hartree: phi from total density each step
      SELF_ONLY       - each orbital sees only its own potential
      FROZEN          - phi_ext held fixed for all steps
      ANDERSON        - phi_ext held fixed (random potential)
      FREE            - phi = 0
    """
    psi_a = lat.gaussian(center_a)
    psi_b = lat.gaussian(center_b)
    seps = np.zeros(N_STEPS + 1)
    seps[0] = lat.com_x(psi_b) - lat.com_x(psi_a)

    # For FROZEN: compute phi from initial density, then hold fixed
    if mode == 'FROZEN':
        rho0 = np.abs(psi_a)**2 + np.abs(psi_b)**2
        phi_ext = lat.solve_poisson(rho0, G)

    for t in range(N_STEPS):
        if mode == 'FREE':
            phi_a = np.zeros(lat.n)
            phi_b = np.zeros(lat.n)
        elif mode == 'SELF_CONSISTENT':
            rho_tot = np.abs(psi_a)**2 + np.abs(psi_b)**2
            phi = lat.solve_poisson(rho_tot, G)
            phi_a = phi
            phi_b = phi
        elif mode == 'SELF_ONLY':
            phi_a = lat.solve_poisson(np.abs(psi_a)**2, G)
            phi_b = lat.solve_poisson(np.abs(psi_b)**2, G)
        elif mode in ('FROZEN', 'ANDERSON'):
            phi_a = phi_ext
            phi_b = phi_ext

        H_a = lat.build_hamiltonian(phi_a)
        H_b = lat.build_hamiltonian(phi_b)
        psi_a = lat.cn_step(psi_a, H_a)
        psi_b = lat.cn_step(psi_b, H_b)
        seps[t + 1] = lat.com_x(psi_b) - lat.com_x(psi_a)

    return seps


# ── power law fit ────────────────────────────────────────────────────────
def power_law_fit(d_arr, a_arr, label=""):
    abs_a = np.abs(a_arr)
    mask = abs_a > 1e-14
    if mask.sum() < 3:
        print(f"  {label}: insufficient data ({mask.sum()} points)")
        return np.nan, np.nan
    log_d = np.log(d_arr[mask])
    log_a = np.log(abs_a[mask])
    coeffs = np.polyfit(log_d, log_a, 1)
    slope = coeffs[0]
    pred = np.polyval(coeffs, log_d)
    ss_res = np.sum((log_a - pred)**2)
    ss_tot = np.sum((log_a - log_a.mean())**2)
    r2 = 1 - ss_res / (ss_tot + 1e-30)
    sign = "negative" if np.mean(a_arr[mask]) < 0 else "positive"
    print(f"  {label}: |a| ~ d^{slope:.3f}  R^2={r2:.4f}  (sign: {sign})")
    return slope, r2


# ═══════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 80)
    print("NEWTON CONTROL: Does random disorder also give exponent -2.0?")
    print("=" * 80)
    print(f"Wilson 3D open BC: side={N_SIDE}, N={N}")
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, MU2={MU2}, G={G}")
    print(f"N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print()

    print("Building lattice ...", flush=True)
    t0 = time.time()
    lat = OpenLattice(N_SIDE)
    print(f"  Done in {time.time()-t0:.1f}s", flush=True)

    mid = N_SIDE // 2  # = 10
    d_vals = [5, 7, 9, 11, 13, 15]

    # ─── CONDITION 1: SELF-CONSISTENT REFERENCE ──────────────────────────
    print()
    print("=" * 80)
    print("CONDITION 1: SELF-CONSISTENT (Hartree) — the gravity signal")
    print("=" * 80)

    sc_results = {}
    for d in d_vals:
        xa = mid - d // 2
        xb = xa + d
        ca = (xa, mid, mid)
        cb = (xb, mid, mid)
        print(f"\n  d={d:2d}  A@x={xa}, B@x={xb}", flush=True)
        t0 = time.time()

        sep_sc = run_two_body(lat, 'SELF_CONSISTENT', ca, cb)
        sep_so = run_two_body(lat, 'SELF_ONLY', ca, cb)

        a_sc = acceleration(sep_sc)
        a_so = acceleration(sep_so)
        a_mut = a_sc - a_so
        early = slice(2, 8)
        mean = float(np.mean(a_mut[early]))
        std = float(np.std(a_mut[early]))
        snr = abs(mean) / (std + 1e-12)

        sc_results[d] = {'mean': mean, 'std': std, 'snr': snr}
        tag = "ATTRACT" if mean < -1e-8 else ("REPEL" if mean > 1e-8 else "NULL")
        print(f"    a_mutual = {mean:+.10f} +/- {std:.10f}  SNR={snr:.2f}  [{tag}]"
              f"  ({time.time()-t0:.1f}s)", flush=True)

    print("\n  --- Self-Consistent Distance Law ---")
    d_sc = np.array(d_vals, dtype=float)
    a_sc_arr = np.array([sc_results[d]['mean'] for d in d_vals])
    slope_sc, r2_sc = power_law_fit(d_sc, a_sc_arr, "SELF-CONSISTENT")

    # ─── CONDITION 2: ANDERSON CONTROL ───────────────────────────────────
    print()
    print("=" * 80)
    print("CONDITION 2: ANDERSON — Poisson-smoothed random potential (static)")
    print("=" * 80)
    print("  Phi_random = |spsolve((Lap - mu2*I), G * rho_random)| ")
    print("  where rho_random is random positive with same norm as gravity rho")
    print("  This has the SAME spatial smoothness as gravity (Poisson kernel)")
    print()

    n_seeds = 5
    anderson_results = {d: [] for d in d_vals}

    for seed in range(n_seeds):
        rng = np.random.default_rng(seed + 100)
        print(f"  --- Seed {seed} ---", flush=True)

        for d in d_vals:
            xa = mid - d // 2
            xb = xa + d
            ca = (xa, mid, mid)
            cb = (xb, mid, mid)

            # Make random source with same total norm as two Gaussians
            psi_a_ref = lat.gaussian(ca)
            psi_b_ref = lat.gaussian(cb)
            rho_ref = np.abs(psi_a_ref)**2 + np.abs(psi_b_ref)**2

            # Random positive density, Poisson-smoothed
            rho_rand = np.abs(rng.normal(0, 1, lat.n))
            rho_rand *= rho_ref.sum() / (rho_rand.sum() + 1e-30)
            phi_rand = lat.solve_poisson(rho_rand, G)

            t0 = time.time()
            sep_and = run_two_body(lat, 'ANDERSON', ca, cb, phi_ext=phi_rand)
            sep_free = run_two_body(lat, 'FREE', ca, cb)
            a_and = acceleration(sep_and)
            a_free = acceleration(sep_free)
            a_diff = a_and - a_free  # potential-induced acceleration
            early = slice(2, 8)
            mean = float(np.mean(a_diff[early]))
            anderson_results[d].append(mean)
            print(f"    d={d:2d}  a_pot = {mean:+.10f}  ({time.time()-t0:.1f}s)", flush=True)

    print("\n  --- Anderson Distance Law (mean over seeds) ---")
    d_and = np.array(d_vals, dtype=float)
    a_and_means = np.array([np.mean(anderson_results[d]) for d in d_vals])
    a_and_stds = np.array([np.std(anderson_results[d]) for d in d_vals])
    slope_and, r2_and = power_law_fit(d_and, a_and_means, "ANDERSON (mean)")

    print(f"\n  {'d':>3s}  {'a_pot mean':>14s}  {'a_pot std':>12s}")
    print("  " + "-" * 35)
    for i, d in enumerate(d_vals):
        print(f"  {d:3d}  {a_and_means[i]:+14.10f}  {a_and_stds[i]:12.10f}")

    # ─── CONDITION 3: FROZEN CONTROL ─────────────────────────────────────
    print()
    print("=" * 80)
    print("CONDITION 3: FROZEN — self-consistent Phi from t=0, held fixed")
    print("=" * 80)

    frz_results = {}
    for d in d_vals:
        xa = mid - d // 2
        xb = xa + d
        ca = (xa, mid, mid)
        cb = (xb, mid, mid)
        print(f"\n  d={d:2d}", flush=True)
        t0 = time.time()

        sep_frz = run_two_body(lat, 'FROZEN', ca, cb)
        sep_so = run_two_body(lat, 'SELF_ONLY', ca, cb)

        a_frz = acceleration(sep_frz)
        a_so = acceleration(sep_so)
        a_mut = a_frz - a_so
        early = slice(2, 8)
        mean = float(np.mean(a_mut[early]))
        std = float(np.std(a_mut[early]))

        frz_results[d] = {'mean': mean, 'std': std}
        tag = "ATTRACT" if mean < -1e-8 else ("REPEL" if mean > 1e-8 else "NULL")
        print(f"    a_mutual = {mean:+.10f}  [{tag}]  ({time.time()-t0:.1f}s)", flush=True)

    print("\n  --- Frozen Distance Law ---")
    d_frz = np.array(d_vals, dtype=float)
    a_frz_arr = np.array([frz_results[d]['mean'] for d in d_vals])
    slope_frz, r2_frz = power_law_fit(d_frz, a_frz_arr, "FROZEN")

    # ═══════════════════════════════════════════════════════════════════════
    # COMPARISON TABLE
    # ═══════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    print(f"\n  {'d':>3s}  {'SELF-CONSIST':>14s}  {'ANDERSON':>14s}  {'FROZEN':>14s}")
    print("  " + "-" * 52)
    for d in d_vals:
        sc_val = sc_results[d]['mean']
        and_val = np.mean(anderson_results[d])
        frz_val = frz_results[d]['mean']
        print(f"  {d:3d}  {sc_val:+14.10f}  {and_val:+14.10f}  {frz_val:+14.10f}")

    print(f"\n  Exponent fits:")
    print(f"    SELF-CONSISTENT: slope = {slope_sc:.3f}  R^2 = {r2_sc:.4f}")
    print(f"    ANDERSON:        slope = {slope_and:.3f}  R^2 = {r2_and:.4f}")
    print(f"    FROZEN:          slope = {slope_frz:.3f}  R^2 = {r2_frz:.4f}")

    # ═══════════════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Check if Anderson also gives -2
    if not np.isnan(slope_and) and not np.isnan(slope_sc):
        if abs(slope_and - slope_sc) < 0.5 and r2_and > 0.7:
            print("  WARNING: Anderson control gives SIMILAR exponent to self-consistent.")
            print(f"    SC slope = {slope_sc:.2f}, Anderson slope = {slope_and:.2f}")
            print("  => The -2 exponent is likely from the Poisson Green's function,")
            print("     NOT from self-consistent gravitational backreaction.")
            print("  => The distance law is a LATTICE ARTIFACT, not emergent gravity.")
        elif r2_and < 0.5:
            print("  Anderson control does NOT show a clean power law (R^2 < 0.5).")
            print(f"    SC slope = {slope_sc:.2f} (R^2={r2_sc:.3f})")
            print(f"    Anderson slope = {slope_and:.2f} (R^2={r2_and:.3f})")
            print("  => Self-consistency MATTERS for the distance law.")
            print("  => The -2 exponent is NOT just a Green's function artifact.")
        else:
            print(f"  Anderson exponent = {slope_and:.2f} differs from SC = {slope_sc:.2f}")
            print("  => Self-consistency modifies the distance law.")

    # Check frozen vs self-consistent
    if not np.isnan(slope_frz) and not np.isnan(slope_sc):
        if abs(slope_frz - slope_sc) < 0.3:
            print(f"\n  Frozen matches self-consistent (slopes within 0.3):")
            print(f"    SC = {slope_sc:.2f}, Frozen = {slope_frz:.2f}")
            print("  => Backreaction does NOT change the distance law at early times.")
        else:
            print(f"\n  Frozen DIFFERS from self-consistent:")
            print(f"    SC = {slope_sc:.2f}, Frozen = {slope_frz:.2f}")
            print("  => Backreaction MATTERS for the distance law.")

    # Sign consistency check
    sc_signs = [sc_results[d]['mean'] < 0 for d in d_vals]
    and_signs = [np.mean(anderson_results[d]) < 0 for d in d_vals]
    print(f"\n  Self-consistent attraction (all d negative): {all(sc_signs)}")
    print(f"  Anderson sign consistency: {sum(and_signs)}/{len(d_vals)} negative")


if __name__ == "__main__":
    main()
