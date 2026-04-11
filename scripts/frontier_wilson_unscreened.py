#!/usr/bin/env python3
"""
Frontier Wilson 3D: Does removing Yukawa screening recover Newton's 1/r^2?

The exponent -3.15 was caused by mu^2=0.22 (screening length 2.13 sites).
At measurement distances d=3-7, we were deep in the exponential Yukawa tail.

Fix: use mu^2=0.001 (screening length 31.6) so measurements are well within
the unscreened regime.

Configs:
  1) side=15, mu^2=0.001  -> expect exponent ~ -2.1
  2) side=15, mu^2=0.22   -> expect exponent ~ -3.15 (control)
  3) side=20, mu^2=0.001  -> expect exponent ~ -2.0 (cleaner Newton)
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, expm_multiply
from scipy.stats import linregress
import time

# ── Parameters ────────────────────────────────────────────────────────────────
G = 5.0
WILSON_R = 1.0
MASS = 0.30
DT = 0.08
N_STEPS = 15
SIGMA = 1.0


def build_adjacency_open(side):
    """Build adjacency list for 3D cubic lattice with OPEN boundaries."""
    N = side ** 3
    rows, cols = [], []
    for x in range(side):
        for y in range(side):
            for z in range(side):
                i = x * side**2 + y * side + z
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    nx_, ny_, nz_ = x + dx, y + dy, z + dz
                    if 0 <= nx_ < side and 0 <= ny_ < side and 0 <= nz_ < side:
                        j = nx_ * side**2 + ny_ * side + nz_
                        rows.append(i)
                        cols.append(j)
    data = np.ones(len(rows))
    adj = sparse.csr_matrix((data, (rows, cols)), shape=(N, N))
    return adj


def build_graph_laplacian(adj, N):
    """Graph Laplacian L = D - A (positive semi-definite convention)."""
    degrees = np.array(adj.sum(axis=1)).flatten()
    D = sparse.diags(degrees)
    L = D - adj
    return L


def build_wilson_hamiltonian(adj, N, phi):
    """
    Wilson 3D Hamiltonian with potential phi on each site.
    H[i,j] = (-0.5j_hop + WILSON_R/2) for neighbors  [note: j_hop is imaginary unit]
    H[i,i] = MASS + phi[i] + WILSON_R * n_neighbors / 2

    For real-valued Wilson fermion on lattice (no gauge field):
    H = MASS*I + phi_diag + (WILSON_R/2)*L + hopping
    where hopping contribution: -1/(2) * A  (from kinetic term)
    and Wilson term: (WILSON_R/2) * L
    Combined: H = (MASS + phi)*I + (WILSON_R/2 - 1/2) * A_neighbors
    Wait -- let's be precise with Wilson fermion discretization:

    H_wilson = MASS*I + diag(phi) + sum_mu [ (WILSON_R/2) * (2I - S_mu - S_mu^dag) ]
             = MASS*I + diag(phi) + WILSON_R * (n_dim * I - A/2 ... no)

    Standard Wilson: for each direction mu,
      H_mu = -0.5*(1 - WILSON_R) * T_mu - 0.5*(1 + WILSON_R) * T_mu^dag  (for 1D)
    In 3D isotropic with T_mu = shift operator (real lattice, no gauge):
      Kinetic = -0.5 * A  (hopping)
      Wilson  = (WILSON_R/2) * L = (WILSON_R/2) * (D - A)
      Diagonal = (MASS + phi) * I

    So: H = (MASS + phi)*I + (WILSON_R/2)*(D - A) + (-0.5)*A
          = (MASS + phi)*I + (WILSON_R/2)*D - (WILSON_R/2 + 0.5)*A

    Let's use this form.
    """
    degrees = np.array(adj.sum(axis=1)).flatten()
    diag_vals = MASS + phi + (WILSON_R / 2.0) * degrees
    H_diag = sparse.diags(diag_vals)
    hop_coeff = -(WILSON_R / 2.0 + 0.5)
    H = H_diag + hop_coeff * adj
    return H


def gaussian_packet(side, center, sigma):
    """3D Gaussian wavepacket centered at (cx, cy, cz)."""
    N = side ** 3
    cx, cy, cz = center
    psi = np.zeros(N)
    for x in range(side):
        for y in range(side):
            for z in range(side):
                i = x * side**2 + y * side + z
                r2 = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
                psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi


def centroid(psi, side):
    """Compute expectation value of position for wavepacket."""
    prob = np.abs(psi)**2
    prob /= prob.sum()
    cx = cy = cz = 0.0
    for x in range(side):
        for y in range(side):
            for z in range(side):
                i = x * side**2 + y * side + z
                cx += x * prob[i]
                cy += y * prob[i]
                cz += z * prob[i]
    return np.array([cx, cy, cz])


def run_hartree(side, mu2, separations, label=""):
    """
    Run Hartree evolution for two Gaussian packets at various separations.
    Returns dict of separation -> mutual_acceleration.
    """
    N = side ** 3
    mid = side / 2.0

    print(f"\n{'='*60}")
    print(f"Config: {label}")
    print(f"  side={side}, N={N}, mu2={mu2}, screening_length={1/np.sqrt(mu2):.1f}")
    print(f"  G={G}, WILSON_R={WILSON_R}, MASS={MASS}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"  separations={separations}")
    print(f"{'='*60}")

    # Build lattice
    t0 = time.time()
    adj = build_adjacency_open(side)
    L = build_graph_laplacian(adj, N)

    # Poisson operator: (L + mu2 * I)
    poisson_op = (L + mu2 * sparse.eye(N)).tocsc()

    print(f"  Lattice built in {time.time()-t0:.2f}s")

    results = {}

    for d in separations:
        # Place packets along x-axis, centered in y,z
        center_A = (mid - d/2.0, mid, mid)
        center_B = (mid + d/2.0, mid, mid)

        psi_A = gaussian_packet(side, center_A, SIGMA)
        psi_B = gaussian_packet(side, center_B, SIGMA)

        # Track centroids
        centroids_shared_A = []
        centroids_shared_B = []
        centroids_self_A = []
        centroids_self_B = []

        # Make copies for self-only evolution
        psi_A_self = psi_A.copy()
        psi_B_self = psi_B.copy()
        psi_A_shared = psi_A.copy()
        psi_B_shared = psi_B.copy()

        for step in range(N_STEPS):
            # ── SHARED potential (both packets contribute) ──
            rho_shared = np.abs(psi_A_shared)**2 + np.abs(psi_B_shared)**2
            phi_shared = spsolve(poisson_op, G * rho_shared)

            H_shared = build_wilson_hamiltonian(adj, N, phi_shared)
            # Imaginary-time-like evolution: psi -> exp(-i H dt) psi
            # Use expm_multiply for sparse matrix exponential
            psi_A_shared = expm_multiply(-1j * DT * H_shared, psi_A_shared)
            psi_B_shared = expm_multiply(-1j * DT * H_shared, psi_B_shared)
            psi_A_shared /= np.linalg.norm(psi_A_shared)
            psi_B_shared /= np.linalg.norm(psi_B_shared)

            centroids_shared_A.append(centroid(psi_A_shared, side))
            centroids_shared_B.append(centroid(psi_B_shared, side))

            # ── SELF-ONLY potential (each packet sees only itself) ──
            rho_A_only = np.abs(psi_A_self)**2
            phi_A_only = spsolve(poisson_op, G * rho_A_only)
            rho_B_only = np.abs(psi_B_self)**2
            phi_B_only = spsolve(poisson_op, G * rho_B_only)

            H_A_self = build_wilson_hamiltonian(adj, N, phi_A_only)
            H_B_self = build_wilson_hamiltonian(adj, N, phi_B_only)

            psi_A_self = expm_multiply(-1j * DT * H_A_self, psi_A_self)
            psi_B_self = expm_multiply(-1j * DT * H_B_self, psi_B_self)
            psi_A_self /= np.linalg.norm(psi_A_self)
            psi_B_self /= np.linalg.norm(psi_B_self)

            centroids_self_A.append(centroid(psi_A_self, side))
            centroids_self_B.append(centroid(psi_B_self, side))

        # Compute mutual acceleration from early steps (1-5)
        # Separation trajectory
        seps_shared = [np.linalg.norm(centroids_shared_A[i] - centroids_shared_B[i])
                       for i in range(N_STEPS)]
        seps_self = [np.linalg.norm(centroids_self_A[i] - centroids_self_B[i])
                     for i in range(N_STEPS)]

        # Mutual = difference in separation change
        # Use steps 0-4 (early time) for acceleration estimate
        # a = d^2(sep)/dt^2 approximated by finite difference
        early = min(5, N_STEPS - 2)

        # Acceleration of separation for shared
        dsep_shared = np.array(seps_shared[:early+2])
        a_shared = np.diff(dsep_shared, 2) / DT**2  # second derivative

        dsep_self = np.array(seps_self[:early+2])
        a_self = np.diff(dsep_self, 2) / DT**2

        # Mutual acceleration = shared - self (average over early steps)
        a_mutual_arr = a_shared - a_self
        a_mutual = np.mean(a_mutual_arr[:early])

        # Also compute simpler metric: velocity of approach
        # v_approach = (sep[0] - sep[T]) / (T * DT) for shared vs self
        T_meas = 5
        v_shared = (seps_shared[0] - seps_shared[T_meas]) / (T_meas * DT)
        v_self = (seps_self[0] - seps_self[T_meas]) / (T_meas * DT)
        v_mutual = v_shared - v_self

        results[d] = {
            'a_mutual': a_mutual,
            'v_mutual': v_mutual,
            'seps_shared': seps_shared,
            'seps_self': seps_self,
        }

        print(f"  d={d:2d}: a_mutual={a_mutual:+.6f}, v_mutual={v_mutual:+.6f}, "
              f"sep_shared[0]={seps_shared[0]:.4f}, sep_shared[5]={seps_shared[4]:.4f}")

    return results


def fit_power_law(results, label):
    """Fit log|signal| vs log(d) to extract exponent."""
    ds = sorted(results.keys())

    print(f"\n--- Power law fits: {label} ---")

    for metric_name, metric_key in [("mutual_accel", "a_mutual"), ("mutual_velocity", "v_mutual")]:
        vals = [results[d][metric_key] for d in ds]
        # Use absolute value, check sign consistency
        signs = [np.sign(v) for v in vals]
        abs_vals = [abs(v) for v in vals]

        # Filter out zeros/tiny values
        valid = [(d, av) for d, av in zip(ds, abs_vals) if av > 1e-12]
        if len(valid) < 3:
            print(f"  {metric_name}: too few valid points ({len(valid)}), skipping")
            continue

        log_d = np.log([v[0] for v in valid])
        log_a = np.log([v[1] for v in valid])

        slope, intercept, r_value, p_value, std_err = linregress(log_d, log_a)

        print(f"  {metric_name}:")
        print(f"    exponent = {slope:.3f} +/- {std_err:.3f}  (R^2 = {r_value**2:.4f})")
        print(f"    signs: {signs}")
        print(f"    |values|: {[f'{v:.2e}' for v in abs_vals]}")

    return


def main():
    print("=" * 70)
    print("FRONTIER: Wilson 3D Unscreened Gravity Test")
    print("Does removing Yukawa screening recover Newton's 1/r^2 law?")
    print("=" * 70)

    # ── Config 1: side=15, mu^2=0.001 (unscreened) ──
    t0 = time.time()
    seps_15 = [3, 4, 5, 6, 7, 8, 9, 10]
    results_1 = run_hartree(15, 0.001, seps_15,
                            label="side=15, mu2=0.001 (unscreened)")
    fit_power_law(results_1, "Config 1: side=15, mu2=0.001")
    t1 = time.time()
    print(f"\n  Config 1 total time: {t1-t0:.1f}s")

    # ── Config 2: side=15, mu^2=0.22 (control — should reproduce -3.15) ──
    results_2 = run_hartree(15, 0.22, seps_15,
                            label="side=15, mu2=0.22 (screened control)")
    fit_power_law(results_2, "Config 2: side=15, mu2=0.22")
    t2 = time.time()
    print(f"\n  Config 2 total time: {t2-t1:.1f}s")

    # ── Config 3: side=20, mu^2=0.001 (larger lattice) ──
    # Check timing - if Config 1 took too long, skip
    time_per_step_15 = (t1 - t0) / (len(seps_15) * N_STEPS)
    estimated_20 = time_per_step_15 * (20/15)**3 * 6 * N_STEPS  # rough scaling
    print(f"\n  Estimated Config 3 time: {estimated_20:.0f}s")

    if estimated_20 < 300:  # 5 minute cutoff
        seps_20 = [5, 7, 9, 11, 13, 15]
        results_3 = run_hartree(20, 0.001, seps_20,
                                label="side=20, mu2=0.001 (larger lattice)")
        fit_power_law(results_3, "Config 3: side=20, mu2=0.001")
        t3 = time.time()
        print(f"\n  Config 3 total time: {t3-t2:.1f}s")
    else:
        print(f"  SKIPPING Config 3 (estimated {estimated_20:.0f}s > 300s limit)")
        t3 = t2

    # ── Summary ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total runtime: {t3-t0:.1f}s")
    print()
    print("Predictions vs Results:")
    print("  Config 1 (mu2=0.001): expect ~ -2.1 to -2.2")
    print("  Config 2 (mu2=0.22):  expect ~ -3.15")
    print("  Config 3 (mu2=0.001, side=20): expect ~ -2.0 to -2.1")
    print()
    print("If Config 1 exponent ~ -2.0, Newton's law is recovered")
    print("and the -3.15 was purely a Yukawa screening artifact.")


if __name__ == "__main__":
    main()
