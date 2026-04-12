#!/usr/bin/env python3
"""
Wilson fermion two-body test on 3D cubic lattice.

Staggered fermions have parity oscillation noise from epsilon(x) = (-1)^{x+y+z}.
Wilson fermions have NO parity oscillation — test whether they give a CLEAN
mutual attraction signal.

Protocol: Hartree two-orbital on 3D cubic lattice (side=9, N=729)
Four modes: SHARED, SELF_ONLY, FREE, FROZEN
Observable: separation, velocity, acceleration, mutual acceleration
Sweeps: G, mu2, separation
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
import itertools
import time

# ── lattice ──────────────────────────────────────────────────────────────
N_SIDE = 9
N = N_SIDE ** 3

def site_index(x, y, z):
    return x * N_SIDE**2 + y * N_SIDE + z

def site_coords(i):
    x = i // (N_SIDE**2)
    r = i % (N_SIDE**2)
    y = r // N_SIDE
    z = r % N_SIDE
    return x, y, z

# positions and adjacency (periodic boundary)
pos = np.zeros((N, 3))
adj = {}
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            i = site_index(x, y, z)
            pos[i] = [x, y, z]
            adj[i] = []
            for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                nx = (x + dx) % N_SIDE
                ny = (y + dy) % N_SIDE
                nz = (z + dz) % N_SIDE
                adj[i].append(site_index(nx, ny, nz))

# ── parameters ───────────────────────────────────────────────────────────
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 30

# ── Gaussian wavepacket ──────────────────────────────────────────────────
def gaussian_wavepacket(center, sigma=1.0):
    """Gaussian on the lattice, periodic-aware, normalized."""
    psi = np.zeros(N, dtype=complex)
    cx, cy, cz = center
    for i in range(N):
        x, y, z = pos[i]
        # minimum-image distance for periodic lattice
        dx = x - cx; dx -= N_SIDE * round(dx / N_SIDE)
        dy = y - cy; dy -= N_SIDE * round(dy / N_SIDE)
        dz = z - cz; dz -= N_SIDE * round(dz / N_SIDE)
        r2 = dx**2 + dy**2 + dz**2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi

# ── Poisson solver (lattice Laplacian) ───────────────────────────────────
def build_lattice_laplacian():
    """Sparse lattice Laplacian for Poisson equation."""
    rows, cols, vals = [], [], []
    for i in range(N):
        rows.append(i); cols.append(i); vals.append(-len(adj[i]))
        for j in adj[i]:
            rows.append(i); cols.append(j); vals.append(1.0)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))

LAP = build_lattice_laplacian()

def solve_poisson(rho, G, mu2):
    """Solve (Lap - mu2) phi = -4 pi G rho with regularization."""
    # In Fourier space this is straightforward, but we use direct sparse solve
    # with regularization for the zero mode
    A = LAP - mu2 * sparse.eye(N) - REG * sparse.eye(N)
    rhs = -4.0 * np.pi * G * rho
    # Remove mean from rhs to help convergence
    rhs -= rhs.mean()
    from scipy.sparse.linalg import spsolve
    phi = spsolve(A, rhs)
    return phi.real

# ── Wilson Hamiltonian ───────────────────────────────────────────────────
def build_wilson_hamiltonian(phi):
    """Build sparse Wilson fermion Hamiltonian with gravitational potential."""
    rows, cols, vals = [], [], []
    for i in range(N):
        # Off-diagonal: hopping + Wilson term
        for j in adj[i]:
            if j <= i:
                continue
            # Kinetic: -i/2; Wilson: +r/2
            val_ij = -0.5j + WILSON_R * 0.5
            val_ji = +0.5j + WILSON_R * 0.5
            rows.append(i); cols.append(j); vals.append(val_ij)
            rows.append(j); cols.append(i); vals.append(val_ji)
        # Diagonal: mass + phi + Wilson mass correction
        coord_num = len(adj[i])
        wilson_diag = WILSON_R * coord_num / 2.0  # = r * coordination / 2
        diag_val = MASS + phi[i] + wilson_diag
        rows.append(i); cols.append(i); vals.append(diag_val)
    H = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))
    return H

# ── center of mass ───────────────────────────────────────────────────────
def center_of_mass_x(psi):
    """x-component of center of mass, periodic-aware."""
    rho = np.abs(psi)**2
    # Use circular mean for periodic lattice
    angles = 2 * np.pi * pos[:, 0] / N_SIDE
    sin_mean = np.sum(rho * np.sin(angles))
    cos_mean = np.sum(rho * np.cos(angles))
    theta = np.arctan2(sin_mean, cos_mean)
    if theta < 0:
        theta += 2 * np.pi
    return theta * N_SIDE / (2 * np.pi)

# ── time evolution ───────────────────────────────────────────────────────
def evolve_step(psi, H):
    """One step of Crank-Nicolson-like evolution via expm_multiply."""
    return expm_multiply(-1j * DT * H, psi)

# ── run one configuration ────────────────────────────────────────────────
def run_mode(mode, G_val, mu2_val, center_A, center_B, sigma=1.0):
    """
    Run two-orbital Hartree dynamics.
    mode: 'SHARED', 'SELF_ONLY', 'FREE', 'FROZEN'
    Returns: array of separations over time
    """
    psi_A = gaussian_wavepacket(center_A, sigma)
    psi_B = gaussian_wavepacket(center_B, sigma)

    seps = np.zeros(N_STEPS + 1)
    cx_A = center_of_mass_x(psi_A)
    cx_B = center_of_mass_x(psi_B)
    seps[0] = cx_B - cx_A

    # For FROZEN mode, compute initial shared potential
    if mode == 'FROZEN':
        rho_total = np.abs(psi_A)**2 + np.abs(psi_B)**2
        phi_frozen = solve_poisson(rho_total, G_val, mu2_val)

    for t in range(N_STEPS):
        if mode == 'FREE':
            phi_A = np.zeros(N)
            phi_B = np.zeros(N)
        elif mode == 'SHARED':
            rho_total = np.abs(psi_A)**2 + np.abs(psi_B)**2
            phi_shared = solve_poisson(rho_total, G_val, mu2_val)
            phi_A = phi_shared
            phi_B = phi_shared
        elif mode == 'SELF_ONLY':
            rho_A = np.abs(psi_A)**2
            rho_B = np.abs(psi_B)**2
            phi_A = solve_poisson(rho_A, G_val, mu2_val)
            phi_B = solve_poisson(rho_B, G_val, mu2_val)
        elif mode == 'FROZEN':
            phi_A = phi_frozen
            phi_B = phi_frozen

        H_A = build_wilson_hamiltonian(phi_A)
        H_B = build_wilson_hamiltonian(phi_B)

        psi_A = evolve_step(psi_A, H_A)
        psi_B = evolve_step(psi_B, H_B)

        # Renormalize (expm_multiply should preserve norm, but be safe)
        psi_A /= np.linalg.norm(psi_A)
        psi_B /= np.linalg.norm(psi_B)

        cx_A = center_of_mass_x(psi_A)
        cx_B = center_of_mass_x(psi_B)
        seps[t + 1] = cx_B - cx_A

    return seps

# ── finite differences ───────────────────────────────────────────────────
def velocity(sep):
    """Central difference velocity."""
    v = np.zeros(len(sep))
    v[1:-1] = (sep[2:] - sep[:-2]) / (2 * DT)
    v[0] = (sep[1] - sep[0]) / DT
    v[-1] = (sep[-1] - sep[-2]) / DT
    return v

def acceleration(sep):
    """Second-order finite difference acceleration."""
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2*sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a

# ── sweep ────────────────────────────────────────────────────────────────
def main():
    print("=" * 80)
    print("WILSON FERMION TWO-BODY TEST")
    print("=" * 80)
    print(f"Lattice: {N_SIDE}^3 = {N} sites")
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, REG={REG}")
    print(f"N_STEPS={N_STEPS}")
    print()

    G_vals = [5, 10, 20, 50, 100]
    mu2_vals = [0.0, 0.22]
    d_vals = [3, 4, 5, 6]

    center_y, center_z = 4, 4

    results = {}

    total_runs = len(G_vals) * len(mu2_vals) * len(d_vals)
    run_idx = 0

    for G_val in G_vals:
        for mu2_val in mu2_vals:
            for d in d_vals:
                run_idx += 1
                # Place orbitals symmetrically around center (4)
                xA = center_y - d // 2
                xB = center_y + (d - d // 2)
                center_A = (xA, center_y, center_z)
                center_B = (xB, center_y, center_z)

                print(f"[{run_idx}/{total_runs}] G={G_val}, mu2={mu2_val}, d={d} "
                      f"(A@x={xA}, B@x={xB})")
                t0 = time.time()

                seps = {}
                for mode in ['SHARED', 'SELF_ONLY', 'FREE', 'FROZEN']:
                    seps[mode] = run_mode(mode, G_val, mu2_val, center_A, center_B)

                elapsed = time.time() - t0

                # Compute mutual acceleration
                a_shared = acceleration(seps['SHARED'])
                a_self = acceleration(seps['SELF_ONLY'])
                a_mutual = a_shared - a_self

                # Early-time mean mutual acceleration (steps 2-10)
                early_slice = slice(2, min(11, N_STEPS + 1))
                a_mutual_early = a_mutual[early_slice].mean()

                # Check if signal is clean (low oscillation)
                a_mutual_std = a_mutual[early_slice].std()
                snr = abs(a_mutual_early) / (a_mutual_std + 1e-12)

                # Separation change
                dsep_shared = seps['SHARED'][-1] - seps['SHARED'][0]
                dsep_free = seps['FREE'][-1] - seps['FREE'][0]

                results[(G_val, mu2_val, d)] = {
                    'seps': seps,
                    'a_mutual': a_mutual,
                    'a_mutual_early_mean': a_mutual_early,
                    'a_mutual_early_std': a_mutual_std,
                    'snr': snr,
                    'dsep_shared': dsep_shared,
                    'dsep_free': dsep_free,
                }

                # Is attraction present? (negative a_mutual = closing)
                attract = "ATTRACT" if a_mutual_early < -1e-6 else ("REPEL" if a_mutual_early > 1e-6 else "NULL")
                clean = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")

                print(f"  a_mutual_early = {a_mutual_early:+.6f} +/- {a_mutual_std:.6f} "
                      f"(SNR={snr:.2f}) [{attract}] [{clean}]")
                print(f"  dsep: SHARED={dsep_shared:+.4f}, FREE={dsep_free:+.4f} "
                      f"({elapsed:.1f}s)")
                print()

    # ── summary table ────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'G':>5s} {'mu2':>6s} {'d':>3s} | {'a_mut_early':>12s} {'std':>10s} "
          f"{'SNR':>6s} {'signal':>8s} {'quality':>8s} | {'dsep_SH':>9s} {'dsep_FR':>9s}")
    print("-" * 90)

    for G_val in G_vals:
        for mu2_val in mu2_vals:
            for d in d_vals:
                r = results[(G_val, mu2_val, d)]
                ae = r['a_mutual_early_mean']
                astd = r['a_mutual_early_std']
                snr = r['snr']
                attract = "ATTRACT" if ae < -1e-6 else ("REPEL" if ae > 1e-6 else "NULL")
                clean = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")
                print(f"{G_val:5d} {mu2_val:6.2f} {d:3d} | {ae:+12.6f} {astd:10.6f} "
                      f"{snr:6.2f} {attract:>8s} {clean:>8s} | "
                      f"{r['dsep_shared']:+9.4f} {r['dsep_free']:+9.4f}")

    # ── detailed trajectories for best cases ─────────────────────────────
    print()
    print("=" * 80)
    print("DETAILED TRAJECTORIES (best SNR cases)")
    print("=" * 80)

    # Find top 5 by SNR
    sorted_keys = sorted(results.keys(), key=lambda k: results[k]['snr'], reverse=True)
    for k in sorted_keys[:5]:
        G_val, mu2_val, d = k
        r = results[k]
        print(f"\nG={G_val}, mu2={mu2_val}, d={d} (SNR={r['snr']:.2f})")
        print(f"  {'t':>4s}  {'sep_SH':>8s} {'sep_SELF':>8s} {'sep_FR':>8s} {'sep_FZ':>8s} "
              f"{'a_mutual':>10s}")
        for t in range(N_STEPS + 1):
            line = f"  {t:4d}  "
            line += f"{r['seps']['SHARED'][t]:8.4f} "
            line += f"{r['seps']['SELF_ONLY'][t]:8.4f} "
            line += f"{r['seps']['FREE'][t]:8.4f} "
            line += f"{r['seps']['FROZEN'][t]:8.4f} "
            line += f"{r['a_mutual'][t]:+10.6f}"
            print(line)

    # ── comparison note ──────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("WILSON vs STAGGERED COMPARISON NOTES")
    print("=" * 80)
    n_attract = sum(1 for r in results.values() if r['a_mutual_early_mean'] < -1e-6)
    n_clean = sum(1 for r in results.values() if r['snr'] > 2.0)
    n_total = len(results)
    print(f"Total configurations: {n_total}")
    print(f"Attraction signal: {n_attract}/{n_total} ({100*n_attract/n_total:.0f}%)")
    print(f"Clean (SNR>2): {n_clean}/{n_total} ({100*n_clean/n_total:.0f}%)")
    print()
    print("Key question: Does removing staggered epsilon oscillation")
    print("produce cleaner mutual acceleration signal?")
    print("Look for: consistent sign of a_mutual, higher SNR, smooth trajectories.")


if __name__ == "__main__":
    main()
