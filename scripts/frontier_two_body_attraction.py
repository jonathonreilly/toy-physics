#!/usr/bin/env python3
"""
Two-body mutual gravitational attraction on Wilson 3D open-BC lattice.

Goal:
  Demonstrate unambiguous mutual attraction between two localized
  wavepackets using graph-native observables (center of mass of |psi|^2).
  The SHARED vs SELF_ONLY subtraction isolates the mutual channel,
  eliminating self-gravity contraction.

Protocol:
  - Place two Gaussian packets at separation d along x-axis
  - Evolve under SHARED potential (both contribute to rho)
  - Evolve under SELF_ONLY potential (each sees only its own rho)
  - Mutual acceleration = d''_shared(t) - d''_self(t)
  - If mutual accel < 0 (separation decreasing), that's ATTRACTION
  - Sweep separations d = [4, 6, 8, 10, 12]
  - Multiple seeds (random phase kicks on one fixed surface)
  - Report fraction attractive and |a_mutual| vs d power law

Surface caveat:
  This script tests ONE geometry (side-20 open cubic), ONE placement
  family (x-axis centered), with phase-jitter repeats only. The seeds
  add small random phase kicks to the initial Gaussians but do not vary
  the lattice, placement axis, or packet shape. Results demonstrate a
  deterministic signal on this surface but do not constitute cross-graph
  or cross-placement robustness.

Confirmed parameters from Newton -1.979 result:
  MASS=0.3, WILSON_R=1.0, DT=0.08, N_STEPS=15, G=5, mu2=0.001, side=20
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


# --- Physics parameters (from confirmed Newton exponent run) ---
MASS = 0.3
WILSON_R = 1.0
DT = 0.08
N_STEPS = 15
G_DEFAULT = 5.0
MU2 = 0.001
REG = 1e-3
SIGMA = 1.0
SIDE = 20

SEPARATIONS = [4, 6, 8, 10, 12]
G_VALUES = [2.0, 5.0, 10.0]
N_SEEDS = 5


class OpenWilsonLattice:
    """3D cubic lattice with open boundary conditions."""

    def __init__(self, side: int):
        self.side = side
        self.n = side**3
        self.pos = np.zeros((self.n, 3))
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = x * side**2 + y * side + z
                    self.pos[i] = [x, y, z]
                    self.adj[i] = []
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            self.adj[i].append(nx * side**2 + ny * side + nz)
        self.lap = self._build_laplacian()

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

    def gaussian_wavepacket(self, center, sigma=SIGMA, rng=None, phase_seed=None):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
            psi[i] = np.exp(-r2 / (2 * sigma**2))
        if phase_seed is not None:
            rng_phase = np.random.default_rng(phase_seed)
            phases = rng_phase.uniform(0, 0.1, self.n)
            psi *= np.exp(1j * phases)
        psi /= np.linalg.norm(psi)
        return psi

    def solve_poisson(self, rho, G, mu2):
        A = self.lap - mu2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi):
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

    def center_of_mass_x(self, psi):
        rho = np.abs(psi)**2
        return float(np.sum(rho * self.pos[:, 0]) / max(np.sum(rho), 1e-30))

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)


def acceleration(sep):
    """Second finite difference of separation time series."""
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def run_two_body(lat, G_val, mu2_val, d, seed=0):
    """Run SHARED and SELF_ONLY evolutions, return mutual acceleration."""
    center = lat.side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    results = {}
    for mode in ("SHARED", "SELF_ONLY", "FREE"):
        psi_a = lat.gaussian_wavepacket(center_a, phase_seed=seed * 1000 + 1)
        psi_b = lat.gaussian_wavepacket(center_b, phase_seed=seed * 1000 + 2)

        # Track individual CoM positions, not just separation
        com_a = np.zeros(N_STEPS + 1)
        com_b = np.zeros(N_STEPS + 1)
        com_a[0] = lat.center_of_mass_x(psi_a)
        com_b[0] = lat.center_of_mass_x(psi_b)

        for t in range(N_STEPS):
            if mode == "FREE":
                phi_a = np.zeros(lat.n)
                phi_b = np.zeros(lat.n)
            elif mode == "SHARED":
                rho_total = np.abs(psi_a)**2 + np.abs(psi_b)**2
                phi_shared = lat.solve_poisson(rho_total, G_val, mu2_val)
                phi_a = phi_shared
                phi_b = phi_shared
            else:  # SELF_ONLY
                phi_a = lat.solve_poisson(np.abs(psi_a)**2, G_val, mu2_val)
                phi_b = lat.solve_poisson(np.abs(psi_b)**2, G_val, mu2_val)

            H_a = lat.build_wilson_hamiltonian(phi_a)
            H_b = lat.build_wilson_hamiltonian(phi_b)
            psi_a = lat.evolve_step(psi_a, H_a)
            psi_b = lat.evolve_step(psi_b, H_b)
            psi_a /= np.linalg.norm(psi_a)
            psi_b /= np.linalg.norm(psi_b)
            com_a[t + 1] = lat.center_of_mass_x(psi_a)
            com_b[t + 1] = lat.center_of_mass_x(psi_b)

        results[mode] = {"com_a": com_a, "com_b": com_b, "sep": com_b - com_a}

    # Mutual acceleration from separation
    a_shared = acceleration(results["SHARED"]["sep"])
    a_self = acceleration(results["SELF_ONLY"]["sep"])
    a_mutual = a_shared - a_self

    # Also compute individual CoM mutual displacements
    # (packet A should move RIGHT, packet B should move LEFT if attractive)
    dx_a_shared = results["SHARED"]["com_a"] - results["SELF_ONLY"]["com_a"]
    dx_b_shared = results["SHARED"]["com_b"] - results["SELF_ONLY"]["com_b"]

    early = slice(2, min(11, N_STEPS + 1))
    a_mean = float(np.mean(a_mutual[early]))
    a_std = float(np.std(a_mutual[early]))
    snr = abs(a_mean) / (a_std + 1e-12)

    # Check individual packet motion directions at end of run
    # For attraction: A moves toward B (positive dx if B is to the right)
    #                 B moves toward A (negative dx if A is to the left)
    dx_a_final = float(dx_a_shared[-1])
    dx_b_final = float(dx_b_shared[-1])
    # Attractive if A moves right AND B moves left (mutual approach)
    individual_attract = dx_a_final > 0 and dx_b_final < 0

    return {
        "d": d,
        "G": G_val,
        "seed": seed,
        "a_mutual_mean": a_mean,
        "a_mutual_std": a_std,
        "snr": snr,
        "dsep_shared": float(results["SHARED"]["sep"][-1] - results["SHARED"]["sep"][0]),
        "dsep_self": float(results["SELF_ONLY"]["sep"][-1] - results["SELF_ONLY"]["sep"][0]),
        "dsep_free": float(results["FREE"]["sep"][-1] - results["FREE"]["sep"][0]),
        "dx_a_mutual": dx_a_final,
        "dx_b_mutual": dx_b_final,
        "individual_attract": individual_attract,
    }


def label(mean, snr):
    signal = "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL")
    quality = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")
    return signal, quality


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit)**2))
    ss_tot = float(np.sum((ly - np.mean(ly))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, r2


def main():
    t_start = time.time()

    print("=" * 92)
    print("TWO-BODY MUTUAL GRAVITATIONAL ATTRACTION")
    print("Wilson 3D open-BC lattice")
    print("=" * 92)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"SIGMA={SIGMA}, MU2={MU2}, REG={REG}, SIDE={SIDE}")
    print(f"Separations: {SEPARATIONS}")
    print(f"G values: {G_VALUES}")
    print(f"Seeds per config: {N_SEEDS}")
    print()

    # Build lattice once (side=20 is expensive)
    print(f"Building {SIDE}^3 = {SIDE**3} site lattice...", end=" ", flush=True)
    t0 = time.time()
    lat = OpenWilsonLattice(SIDE)
    print(f"done ({time.time() - t0:.1f}s)")
    print()

    # ================================================================
    # PHASE 1: Primary sweep at G=5.0 across all separations and seeds
    # ================================================================
    print("=" * 92)
    print("PHASE 1: Primary sweep (G=5.0)")
    print("=" * 92)

    all_rows = []
    for d in SEPARATIONS:
        for seed in range(N_SEEDS):
            t0 = time.time()
            row = run_two_body(lat, G_DEFAULT, MU2, d, seed=seed)
            elapsed = time.time() - t0
            signal, quality = label(row["a_mutual_mean"], row["snr"])
            all_rows.append(row)
            print(
                f"  d={d:2d} seed={seed}: "
                f"a_mut={row['a_mutual_mean']:+.6f} +/- {row['a_mutual_std']:.6f} "
                f"(SNR={row['snr']:.2f}) [{signal}] [{quality}] "
                f"dsep SH={row['dsep_shared']:+.5f} SELF={row['dsep_self']:+.5f} "
                f"dxA={row['dx_a_mutual']:+.5f} dxB={row['dx_b_mutual']:+.5f} "
                f"indiv={'YES' if row['individual_attract'] else 'no '} "
                f"({elapsed:.1f}s)"
            )
        print()

    # Summary for Phase 1
    print("-" * 92)
    print("PHASE 1 SUMMARY (G=5.0)")
    print("-" * 92)
    total = len(all_rows)
    n_attract = sum(1 for r in all_rows if r["a_mutual_mean"] < -1e-6)
    n_clean_attract = sum(
        1 for r in all_rows
        if r["a_mutual_mean"] < -1e-6 and r["snr"] > 2.0
    )
    n_indiv = sum(1 for r in all_rows if r["individual_attract"])
    print(f"  Total configs: {total}")
    print(f"  Attractive (a_mut < 0): {n_attract}/{total} = {n_attract / total:.1%}")
    print(f"  Clean attractive (SNR>2): {n_clean_attract}/{total} = {n_clean_attract / total:.1%}")
    print(f"  Individual CoM approach: {n_indiv}/{total} = {n_indiv / total:.1%}")
    print()

    # Per-distance summary
    print("  Per-distance breakdown:")
    distance_means = {}
    for d in SEPARATIONS:
        d_rows = [r for r in all_rows if r["d"] == d]
        a_vals = [r["a_mutual_mean"] for r in d_rows]
        n_att = sum(1 for v in a_vals if v < -1e-6)
        mean_a = np.mean(a_vals)
        std_a = np.std(a_vals)
        n_ind = sum(1 for r in d_rows if r["individual_attract"])
        distance_means[d] = (mean_a, std_a, n_att, len(d_rows), n_ind)
        print(
            f"    d={d:2d}: <a_mut>={mean_a:+.6f} +/- {std_a:.6f}  "
            f"attract={n_att}/{len(d_rows)}  "
            f"indiv_attract={n_ind}/{len(d_rows)}"
        )
    print()

    # Power law fit on seed-averaged |a_mutual|
    clean_ds = []
    clean_amps = []
    for d in SEPARATIONS:
        mean_a, std_a, n_att, n_tot, _ = distance_means[d]
        if mean_a < -1e-8 and n_att == n_tot:  # require ALL seeds attractive
            clean_ds.append(d)
            clean_amps.append(abs(mean_a))

    if len(clean_ds) >= 3:
        slope, r2 = power_law_fit(clean_ds, clean_amps)
        print(f"  Distance law: |<a_mut>| ~ d^{slope:.3f}  (R^2={r2:.4f})")
        print(f"    Newton prediction: -2.00")
        print(f"    Measured exponent: {slope:.3f}")
        print(f"    Deviation from Newton: {abs(slope - (-2.0)):.3f}")
    elif len(clean_ds) >= 2:
        slope, r2 = power_law_fit(clean_ds, clean_amps)
        print(f"  Distance law (2-point): |<a_mut>| ~ d^{slope:.3f}  (R^2={r2:.4f})")
    else:
        print("  Insufficient attractive separations for distance law fit")
    print()

    # ================================================================
    # PHASE 2: G-value sweep at fixed d=6
    # ================================================================
    print("=" * 92)
    print("PHASE 2: G-value sweep (d=6)")
    print("=" * 92)

    g_rows = []
    for G in G_VALUES:
        for seed in range(N_SEEDS):
            t0 = time.time()
            row = run_two_body(lat, G, MU2, 6, seed=seed)
            elapsed = time.time() - t0
            signal, quality = label(row["a_mutual_mean"], row["snr"])
            g_rows.append(row)
            print(
                f"  G={G:5.1f} seed={seed}: "
                f"a_mut={row['a_mutual_mean']:+.6f} "
                f"(SNR={row['snr']:.2f}) [{signal}] [{quality}] "
                f"indiv={'YES' if row['individual_attract'] else 'no '} "
                f"({elapsed:.1f}s)"
            )
        print()

    print("-" * 92)
    print("PHASE 2 SUMMARY (G sweep)")
    print("-" * 92)
    for G in G_VALUES:
        gr = [r for r in g_rows if r["G"] == G]
        a_vals = [r["a_mutual_mean"] for r in gr]
        n_att = sum(1 for v in a_vals if v < -1e-6)
        print(
            f"  G={G:5.1f}: <a_mut>={np.mean(a_vals):+.6f} +/- {np.std(a_vals):.6f}  "
            f"attract={n_att}/{len(gr)}"
        )
    print()

    # ================================================================
    # PHASE 3: Verify asymmetry (packet A moves RIGHT, B moves LEFT)
    # ================================================================
    print("=" * 92)
    print("PHASE 3: Individual packet motion verification")
    print("=" * 92)
    print("If attraction is real, packet A (left) should shift RIGHT")
    print("and packet B (right) should shift LEFT relative to SELF_ONLY.")
    print()

    for d in SEPARATIONS:
        d_rows = [r for r in all_rows if r["d"] == d]
        dx_a_vals = [r["dx_a_mutual"] for r in d_rows]
        dx_b_vals = [r["dx_b_mutual"] for r in d_rows]
        a_right = sum(1 for v in dx_a_vals if v > 1e-8)
        b_left = sum(1 for v in dx_b_vals if v < -1e-8)
        both = sum(1 for r in d_rows if r["individual_attract"])
        print(
            f"  d={d:2d}: "
            f"A_right={a_right}/{len(d_rows)}  "
            f"B_left={b_left}/{len(d_rows)}  "
            f"both={both}/{len(d_rows)}  "
            f"<dxA>={np.mean(dx_a_vals):+.6f}  "
            f"<dxB>={np.mean(dx_b_vals):+.6f}"
        )
    print()

    # ================================================================
    # FINAL VERDICT
    # ================================================================
    total_time = time.time() - t_start
    print("=" * 92)
    print("FINAL VERDICT")
    print("=" * 92)
    frac_attract = n_attract / total
    frac_indiv = n_indiv / total

    print(f"  Attractive rows on this fixed surface: {n_attract}/{total} = {frac_attract:.1%}")
    print(f"  Individual packet-approach rows:      {n_indiv}/{total} = {frac_indiv:.1%}")
    if len(clean_ds) >= 3:
        print(f"  Early-time all-attractive distance fit: alpha={slope:.3f}  (R^2={r2:.4f})")
    else:
        print("  Early-time all-attractive distance fit: insufficient clean separations")

    print()
    print("  >>> BOUNDED FIXED-SURFACE RESULT ONLY <<<")
    print("      - phase-jitter repeats on one open Wilson surface")
    print("      - not cross-placement or cross-size robustness")
    print("      - not both-masses closure")
    print("      - not a standalone promotion-to-main verdict")

    print(f"\n  Total runtime: {total_time:.0f}s")


if __name__ == "__main__":
    main()
