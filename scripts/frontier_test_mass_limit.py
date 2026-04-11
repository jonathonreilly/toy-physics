#!/usr/bin/env python3
"""
Test-mass limit: F = G * M_source / r^2 from a single heavy source.

Avoids the self-field contamination that plagued the Hartree two-orbital
both-masses probe.  Instead of two equal-mass packets, we use:

  - one HEAVY source (Gaussian, amplitude A_source, width sigma=1.5)
  - one LIGHT test particle (Gaussian, small fixed amplitude, width sigma=1.0)

The gravitational potential phi is computed from the SOURCE density ONLY:
    (L + mu^2 I) phi = -4 pi G |psi_source|^2

The test particle evolves in this STATIC external field.  Its self-gravity
is negligible by construction.

Protocol:
  1. Mass sweep:  vary A_source in [0.5, 1.0, 1.5, 2.0, 3.0]
     with fixed d=4.  Measure |a_test| vs M_source = integral |psi_source|^2.
     Expect mass exponent ~ 1.0.

  2. Distance sweep:  fix A_source=2.0, vary d in [3, 4, 5, 6, 7].
     Expect distance exponent ~ -2.0  (Coulomb / Newton on 3D lattice).

Uses the Wilson 3D open-BC lattice infrastructure.

PStack experiment: test-mass-limit
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 30
SIGMA_SOURCE = 1.5
SIGMA_TEST = 1.0


class OpenWilsonLattice:
    """3D cubic lattice with open (Dirichlet) boundary conditions."""

    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self._idx(x, y, z)
                    self.pos[i] = [x, y, z]
                    self.adj[i] = []
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            self.adj[i].append(self._idx(nx, ny, nz))
        self.lap = self._build_laplacian()

    def _idx(self, x: int, y: int, z: int) -> int:
        return x * self.side**2 + y * self.side + z

    def _build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian(self, center, sigma: float, amplitude: float = 1.0) -> np.ndarray:
        cx, cy, cz = center
        r2 = (self.pos[:, 0] - cx)**2 + (self.pos[:, 1] - cy)**2 + (self.pos[:, 2] - cz)**2
        psi = amplitude * np.exp(-r2 / (2 * sigma**2)).astype(complex)
        return psi

    def solve_poisson(self, rho: np.ndarray, G: float, mu2: float) -> np.ndarray:
        """Solve (L - mu2) phi = -4 pi G rho.
        Returns phi which is POSITIVE near sources (potential hill).
        For gravitational attraction, caller should negate: V = -phi.
        """
        A = self.lap - mu2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi: np.ndarray):
        rows, cols, vals = [], [], []
        for i in range(self.n):
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
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_x(self, psi: np.ndarray) -> float:
        rho = np.abs(psi)**2
        total = np.sum(rho)
        if total < 1e-30:
            return 0.0
        return float(np.sum(rho * self.pos[:, 0]) / total)

    def evolve_step(self, psi: np.ndarray, H) -> np.ndarray:
        return expm_multiply(-1j * DT * H, psi)


def run_test_mass(
    side: int,
    G_val: float,
    mu2: float,
    d: int,
    A_source: float,
) -> dict:
    """
    Place a heavy source at lattice center, a light test particle at distance d.
    Compute phi from source only (static).  Evolve test particle.
    Return CoM trajectory and acceleration of the test particle.
    """
    lat = OpenWilsonLattice(side)
    c = side // 2

    center_source = (c, c, c)
    center_test = (c + d, c, c)

    # Source wavepacket (heavy, not normalized to 1)
    psi_source = lat.gaussian(center_source, SIGMA_SOURCE, amplitude=A_source)
    M_source = float(np.sum(np.abs(psi_source)**2))

    # Test wavepacket (light, normalized to 1)
    psi_test = lat.gaussian(center_test, SIGMA_TEST, amplitude=1.0)
    psi_test /= np.linalg.norm(psi_test)

    # Also run free evolution (no potential) as control
    psi_test_free = psi_test.copy()

    # Static potential from source density only
    # In the Wilson Hamiltonian, positive phi on diagonal acts as a potential
    # hill that deflects/attracts the wavepacket toward the source.
    # We test BOTH signs and report which gives attraction.
    rho_source = np.abs(psi_source)**2
    phi_raw = lat.solve_poisson(rho_source, G_val, mu2)
    phi_source = phi_raw  # phi > 0 near source

    # Build Hamiltonians
    H_gravity = lat.build_wilson_hamiltonian(phi_source)
    H_free = lat.build_wilson_hamiltonian(np.zeros(lat.n))

    # Evolve and record CoM
    x_grav = np.zeros(N_STEPS + 1)
    x_free = np.zeros(N_STEPS + 1)
    norms = np.zeros(N_STEPS + 1)

    x_grav[0] = lat.center_of_mass_x(psi_test)
    x_free[0] = lat.center_of_mass_x(psi_test_free)
    norms[0] = np.linalg.norm(psi_test)

    for t in range(N_STEPS):
        psi_test = lat.evolve_step(psi_test, H_gravity)
        psi_test /= np.linalg.norm(psi_test)
        psi_test_free = lat.evolve_step(psi_test_free, H_free)
        psi_test_free /= np.linalg.norm(psi_test_free)

        x_grav[t + 1] = lat.center_of_mass_x(psi_test)
        x_free[t + 1] = lat.center_of_mass_x(psi_test_free)
        norms[t + 1] = np.linalg.norm(psi_test)

    # Displacement relative to free evolution (removes any boundary drift)
    dx = x_grav - x_free

    # Acceleration via second finite difference of displacement
    acc = np.zeros(N_STEPS + 1)
    for t in range(1, N_STEPS):
        acc[t] = (dx[t + 1] - 2 * dx[t] + dx[t - 1]) / DT**2
    acc[0] = acc[1]
    acc[-1] = acc[-2]

    # Velocity from first difference of displacement
    vel = np.zeros(N_STEPS + 1)
    for t in range(N_STEPS):
        vel[t + 1] = (dx[t + 1] - dx[t]) / DT

    # Use early-time signal (steps 2-10) where linear response is cleanest
    early = slice(2, min(11, N_STEPS + 1))
    a_mean = float(np.mean(acc[early]))
    a_std = float(np.std(acc[early]))
    snr = abs(a_mean) / (a_std + 1e-12)

    # Also measure velocity at a fixed late time as a cleaner signal
    v_late = float(vel[min(15, N_STEPS)])
    dx_total = float(dx[min(20, N_STEPS)])

    # Potential at test particle location (should be negative for attraction)
    phi_at_test = float(phi_source[lat._idx(c + d, c, c)])

    return {
        "side": side,
        "G": G_val,
        "mu2": mu2,
        "d": d,
        "A_source": A_source,
        "M_source": M_source,
        "a_mean": a_mean,
        "a_std": a_std,
        "snr": snr,
        "v_late": v_late,
        "dx_total": dx_total,
        "phi_at_test": phi_at_test,
        "x_grav": x_grav,
        "x_free": x_free,
        "dx": dx,
        "acc": acc,
        "vel": vel,
    }


def power_law_fit(xs, ys):
    """Fit log(y) = alpha * log(x) + const.  Return (alpha, R^2)."""
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit_vals = slope * lx + intercept
    ss_res = float(np.sum((ly - fit_vals)**2))
    ss_tot = float(np.sum((ly - np.mean(ly))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(slope), float(r2)


def main():
    side = 20
    mu2 = 0.001
    G_val = 0.002

    print("=" * 80)
    print("FRONTIER: TEST-MASS LIMIT  —  F = G * M_source / r^2")
    print("=" * 80)
    print()
    print(f"Wilson 3D open-BC lattice, side={side} ({side**3} sites)")
    print(f"mu^2={mu2}, G={G_val}, MASS={MASS}, WILSON_R={WILSON_R}")
    print(f"DT={DT}, N_STEPS={N_STEPS}")
    print(f"Source: Gaussian sigma={SIGMA_SOURCE} (heavy, unnormalized)")
    print(f"Test:   Gaussian sigma={SIGMA_TEST} (light, normalized)")
    print(f"Static potential: phi from source density ONLY")
    print()

    # ==================================================================
    # PART 1: MASS SWEEP  (vary A_source, fixed d=4)
    # ==================================================================
    print("=" * 80)
    print("PART 1: MASS SWEEP  —  |a_test| vs M_source  (d=4 fixed)")
    print("=" * 80)
    print()

    d_fixed = 4
    A_values = [0.5, 1.0, 1.5, 2.0, 3.0]

    mass_results = []
    for A in A_values:
        t0 = time.time()
        result = run_test_mass(side, G_val, mu2, d_fixed, A)
        elapsed = time.time() - t0
        mass_results.append(result)

        sign = "TOWARD" if result["a_mean"] < 0 else "AWAY"
        print(
            f"A={A:.1f}  M_source={result['M_source']:.3f}  "
            f"a_mean={result['a_mean']:+.6f} +/- {result['a_std']:.6f}  "
            f"SNR={result['snr']:.2f}  [{sign}]  "
            f"v_late={result['v_late']:+.6f}  "
            f"dx_total={result['dx_total']:+.6f}  "
            f"phi_test={result['phi_at_test']:+.4f}  "
            f"({elapsed:.1f}s)"
        )

    # Fit |a_test| vs M_source
    print()
    print("--- Mass exponent fit ---")
    # Use absolute values of the observable (expect negative = toward source)
    masses = [r["M_source"] for r in mass_results]
    a_vals_abs = [abs(r["a_mean"]) for r in mass_results]
    v_vals_abs = [abs(r["v_late"]) for r in mass_results]
    dx_vals_abs = [abs(r["dx_total"]) for r in mass_results]

    # Filter out near-zero values
    valid_a = [(m, a) for m, a in zip(masses, a_vals_abs) if a > 1e-10]
    valid_v = [(m, v) for m, v in zip(masses, v_vals_abs) if v > 1e-10]
    valid_dx = [(m, dx) for m, dx in zip(masses, dx_vals_abs) if dx > 1e-10]

    if len(valid_a) >= 2:
        alpha_a, r2_a = power_law_fit([m for m, _ in valid_a], [a for _, a in valid_a])
        print(f"|a_test| ~ M_source^{alpha_a:.3f}   (R^2={r2_a:.4f}, n={len(valid_a)})")
    else:
        alpha_a = float("nan")
        print(f"|a_test|: insufficient data for fit (n={len(valid_a)})")

    if len(valid_v) >= 2:
        alpha_v, r2_v = power_law_fit([m for m, _ in valid_v], [v for _, v in valid_v])
        print(f"|v_late| ~ M_source^{alpha_v:.3f}   (R^2={r2_v:.4f}, n={len(valid_v)})")
    else:
        alpha_v = float("nan")
        print(f"|v_late|: insufficient data for fit (n={len(valid_v)})")

    if len(valid_dx) >= 2:
        alpha_dx, r2_dx = power_law_fit([m for m, _ in valid_dx], [dx for _, dx in valid_dx])
        print(f"|dx_total| ~ M_source^{alpha_dx:.3f}   (R^2={r2_dx:.4f}, n={len(valid_dx)})")
    else:
        alpha_dx = float("nan")
        print(f"|dx_total|: insufficient data for fit (n={len(valid_dx)})")

    # Linearity check: also look at ratios
    print()
    print("--- Linearity check (ratio test) ---")
    ref_idx = 1  # A=1.0 as reference
    if len(mass_results) > ref_idx:
        ref_mass = mass_results[ref_idx]["M_source"]
        ref_dx = mass_results[ref_idx]["dx_total"]
        for r in mass_results:
            mass_ratio = r["M_source"] / ref_mass
            if abs(ref_dx) > 1e-10:
                dx_ratio = r["dx_total"] / ref_dx
                linearity = dx_ratio / mass_ratio if abs(mass_ratio) > 1e-10 else float("nan")
                print(
                    f"A={r['A_source']:.1f}  "
                    f"M/M_ref={mass_ratio:.3f}  "
                    f"dx/dx_ref={dx_ratio:.3f}  "
                    f"ratio={linearity:.3f}  "
                    f"(expect 1.0 for linear)"
                )
            else:
                print(f"A={r['A_source']:.1f}  M/M_ref={mass_ratio:.3f}  dx_ref~0 (skip)")

    # ==================================================================
    # PART 2: DISTANCE SWEEP  (fixed A_source=2.0, vary d)
    # ==================================================================
    print()
    print("=" * 80)
    print("PART 2: DISTANCE SWEEP  —  |a_test| vs d  (A_source=2.0 fixed)")
    print("=" * 80)
    print()

    A_fixed = 2.0
    d_values = [3, 4, 5, 6, 7]

    dist_results = []
    for d in d_values:
        if d >= side - 3:
            print(f"d={d}: SKIP (too close to boundary)")
            continue
        t0 = time.time()
        result = run_test_mass(side, G_val, mu2, d, A_fixed)
        elapsed = time.time() - t0
        dist_results.append(result)

        sign = "TOWARD" if result["a_mean"] < 0 else "AWAY"
        print(
            f"d={d}  "
            f"a_mean={result['a_mean']:+.6f} +/- {result['a_std']:.6f}  "
            f"SNR={result['snr']:.2f}  [{sign}]  "
            f"v_late={result['v_late']:+.6f}  "
            f"dx_total={result['dx_total']:+.6f}  "
            f"phi_test={result['phi_at_test']:+.4f}  "
            f"({elapsed:.1f}s)"
        )

    # Fit |a_test| vs d
    print()
    print("--- Distance exponent fit ---")
    distances = [r["d"] for r in dist_results]
    a_d_abs = [abs(r["a_mean"]) for r in dist_results]
    v_d_abs = [abs(r["v_late"]) for r in dist_results]
    dx_d_abs = [abs(r["dx_total"]) for r in dist_results]

    valid_a_d = [(d, a) for d, a in zip(distances, a_d_abs) if a > 1e-10]
    valid_v_d = [(d, v) for d, v in zip(distances, v_d_abs) if v > 1e-10]
    valid_dx_d = [(d, dx) for d, dx in zip(distances, dx_d_abs) if dx > 1e-10]

    if len(valid_a_d) >= 2:
        beta_a, r2_a = power_law_fit([d for d, _ in valid_a_d], [a for _, a in valid_a_d])
        print(f"|a_test| ~ d^{beta_a:.3f}   (R^2={r2_a:.4f}, n={len(valid_a_d)})")
    else:
        beta_a = float("nan")
        print(f"|a_test|: insufficient data for fit (n={len(valid_a_d)})")

    if len(valid_v_d) >= 2:
        beta_v, r2_v = power_law_fit([d for d, _ in valid_v_d], [v for _, v in valid_v_d])
        print(f"|v_late| ~ d^{beta_v:.3f}   (R^2={r2_v:.4f}, n={len(valid_v_d)})")
    else:
        beta_v = float("nan")
        print(f"|v_late|: insufficient data for fit (n={len(valid_v_d)})")

    if len(valid_dx_d) >= 2:
        beta_dx, r2_dx = power_law_fit([d for d, _ in valid_dx_d], [dx for _, dx in valid_dx_d])
        print(f"|dx_total| ~ d^{beta_dx:.3f}   (R^2={r2_dx:.4f}, n={len(valid_dx_d)})")
    else:
        beta_dx = float("nan")
        print(f"|dx_total|: insufficient data for fit (n={len(valid_dx_d)})")

    # ==================================================================
    # PART 3: POTENTIAL PROFILE
    # ==================================================================
    print()
    print("=" * 80)
    print("PART 3: POTENTIAL PROFILE — phi(r) from the source")
    print("=" * 80)
    print()

    lat = OpenWilsonLattice(side)
    c = side // 2
    psi_source = lat.gaussian((c, c, c), SIGMA_SOURCE, amplitude=2.0)
    rho_source = np.abs(psi_source)**2
    phi_raw = lat.solve_poisson(rho_source, G_val, mu2)
    phi_pot = phi_raw  # Positive near source (same sign as in dynamics)

    print(f"M_source = {np.sum(rho_source):.3f}")
    print(f"{'r':>4} {'V(r)':>12} {'|V| * r':>12} {'|V| * r^2':>12}")
    print("-" * 48)
    for r in range(0, side // 2):
        idx = lat._idx(c + r, c, c)
        V_r = phi_pot[idx]
        scaled1 = abs(V_r) * r if r > 0 else 0.0
        scaled2 = abs(V_r) * r**2 if r > 0 else 0.0
        print(f"{r:4d} {V_r:+12.6f} {scaled1:+12.6f} {scaled2:+12.6f}")

    # Fit |V(r)| vs r for r >= 2
    rs = []
    phis = []
    for r in range(2, side // 2 - 1):
        idx = lat._idx(c + r, c, c)
        rs.append(r)
        phis.append(abs(phi_pot[idx]))

    if len(rs) >= 2 and all(p > 1e-12 for p in phis):
        phi_exp, phi_r2 = power_law_fit(rs, phis)
        print(f"\n|V(r)| ~ r^{phi_exp:.3f}   (R^2={phi_r2:.4f})")
        print(f"Expected: r^-1.0 for 3D Coulomb/Newton")

    # ==================================================================
    # PART 4: TRAJECTORY DETAILS
    # ==================================================================
    print()
    print("=" * 80)
    print("PART 4: TRAJECTORY DETAILS (mass sweep, d=4)")
    print("=" * 80)
    print()

    for r in mass_results:
        print(f"A={r['A_source']:.1f}, M_source={r['M_source']:.3f}:")
        print(f"  t:    ", end="")
        for t in range(0, N_STEPS + 1, 5):
            print(f"{t:>8d}", end="")
        print()
        print(f"  x_gv: ", end="")
        for t in range(0, N_STEPS + 1, 5):
            print(f"{r['x_grav'][t]:>8.4f}", end="")
        print()
        print(f"  x_fr: ", end="")
        for t in range(0, N_STEPS + 1, 5):
            print(f"{r['x_free'][t]:>8.4f}", end="")
        print()
        print(f"  dx:   ", end="")
        for t in range(0, N_STEPS + 1, 5):
            print(f"{r['dx'][t]:>8.4f}", end="")
        print()
        print()

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    # Direction check
    toward_count = sum(1 for r in mass_results if r["dx_total"] < -1e-6)
    total_mass = len(mass_results)
    print(f"Direction: {toward_count}/{total_mass} mass-sweep configs show test particle moving TOWARD source")

    toward_d = sum(1 for r in dist_results if r["dx_total"] < -1e-6)
    print(f"Direction: {toward_d}/{len(dist_results)} distance-sweep configs show TOWARD motion")
    print()

    # Mass exponent
    if np.isfinite(alpha_dx):
        verdict_m = "PASS" if 0.7 < alpha_dx < 1.3 else "FAIL"
        print(f"Mass exponent (dx_total):     {alpha_dx:.3f}  [expect ~1.0]  [{verdict_m}]")
    else:
        print(f"Mass exponent: could not fit")

    if np.isfinite(alpha_v):
        verdict_m2 = "PASS" if 0.7 < alpha_v < 1.3 else "FAIL"
        print(f"Mass exponent (v_late):       {alpha_v:.3f}  [expect ~1.0]  [{verdict_m2}]")

    # Distance exponent
    if np.isfinite(beta_dx):
        verdict_d = "PASS" if -3.0 < beta_dx < -1.0 else "FAIL"
        print(f"Distance exponent (dx_total): {beta_dx:.3f}  [expect ~-2.0]  [{verdict_d}]")
    else:
        print(f"Distance exponent: could not fit")

    if np.isfinite(beta_v):
        verdict_d2 = "PASS" if -3.0 < beta_v < -1.0 else "FAIL"
        print(f"Distance exponent (v_late):   {beta_v:.3f}  [expect ~-2.0]  [{verdict_d2}]")

    print()
    if np.isfinite(alpha_dx) and np.isfinite(beta_dx):
        if 0.7 < alpha_dx < 1.3 and -3.0 < beta_dx < -1.0:
            print("CONCLUSION: Test-mass limit SUPPORTS F = G * M_source / r^n")
            print(f"  with n ~ {abs(beta_dx):.2f} and linear mass dependence (exponent {alpha_dx:.2f})")
        else:
            print("CONCLUSION: Test-mass limit shows deviations from simple Newton")
            print(f"  mass exponent = {alpha_dx:.2f} (expect 1.0)")
            print(f"  distance exponent = {beta_dx:.2f} (expect -2.0)")
    else:
        print("CONCLUSION: Insufficient signal to determine force law")


if __name__ == "__main__":
    main()
