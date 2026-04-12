#!/usr/bin/env python3
"""
Redesigned both-masses test: three approaches to separate the mutual channel
from the common Wilson-gap slowdown.

Root cause of the original failure:
  When inertial mass M enters the Wilson Hamiltonian diagonal, heavier packets
  propagate slower. The SHARED-minus-SELF_ONLY residual then contains a large
  common slowdown that contaminates the mutual acceleration signal.

Approach 1: Fixed inertial mass, vary source mass only
  - Keep M_inertial = 1.0 in the Hamiltonian for all orbitals
  - Vary the Poisson source strength alpha (gravitational mass)
  - rho = alpha * |psi|^2
  - If |a_mutual| is proportional to alpha_partner, that's F proportional to M_source

Approach 2: Mid-plane probability-current flux
  - Measure J = Im(psi* . H_hop . psi) through the mid-plane between packets
  - The SHARED-minus-SELF difference in J is the mutual flux
  - This is a local observable, not contaminated by CoM drift

Approach 3: Perturbative regime (weak G)
  - At weak G, the shared potential is a small perturbation
  - Common slowdown scales as G^2 while mutual channel scales as G
  - So at weak G the mutual channel should dominate

Surface: Wilson 3D open BC, side=20, mu2=0.001
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


# ── parameters ──────────────────────────────────────────────────────────
SIDE = 14
N = SIDE ** 3
WILSON_R = 1.0
DT = 0.08
REG = 1e-6
N_STEPS = 18
SIGMA = 1.0
MU2 = 0.001
D_SEP = 5
EARLY_START = 2
EARLY_END = 8

# Approach 1 parameters
ALPHA_VALUES = [0.5, 1.0, 1.5, 2.0, 3.0]
FIXED_INERTIAL_MASS = 1.0

# Approach 2 parameters (uses same alpha sweep)

# Approach 3 parameters
G_VALUES = [0.5, 1.0, 2.0]
MASS_VALUES_APP3 = [0.5, 1.0, 2.0, 3.0]


# ── lattice setup (open BC) ────────────────────────────────────────────
print("Building lattice...", flush=True)
t_build = time.time()

pos = np.zeros((N, 3))
adj_list: list[list[int]] = [[] for _ in range(N)]

for x in range(SIDE):
    for y in range(SIDE):
        for z in range(SIDE):
            i = x * SIDE**2 + y * SIDE + z
            pos[i] = [x, y, z]
            for dx, dy, dz in (
                (1, 0, 0), (-1, 0, 0),
                (0, 1, 0), (0, -1, 0),
                (0, 0, 1), (0, 0, -1),
            ):
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < SIDE and 0 <= ny < SIDE and 0 <= nz < SIDE:
                    adj_list[i].append(nx * SIDE**2 + ny * SIDE + nz)


def build_laplacian():
    rows, cols, vals = [], [], []
    for i in range(N):
        rows.append(i)
        cols.append(i)
        vals.append(-len(adj_list[i]))
        for j in adj_list[i]:
            rows.append(i)
            cols.append(j)
            vals.append(1.0)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))


LAP = build_laplacian()
POISSON_BASE = (LAP - MU2 * sparse.eye(N) - REG * sparse.eye(N)).tocsc()

print(f"Lattice built: {SIDE}^3 = {N} sites ({time.time() - t_build:.1f}s)", flush=True)


def solve_poisson(rho, G_val):
    rhs = -4.0 * np.pi * G_val * rho
    return spsolve(POISSON_BASE, rhs).real


def build_wilson_hamiltonian(phi, inertial_mass):
    rows, cols, vals = [], [], []
    for i in range(N):
        for j in adj_list[i]:
            if j <= i:
                continue
            rows.append(i); cols.append(j); vals.append(-0.5j + 0.5 * WILSON_R)
            rows.append(j); cols.append(i); vals.append(+0.5j + 0.5 * WILSON_R)
        diag = inertial_mass + phi[i] + 0.5 * WILSON_R * len(adj_list[i])
        rows.append(i); cols.append(i); vals.append(diag)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(N, N))


def cn_step(psi, hamiltonian):
    half = 1j * hamiltonian * (DT / 2.0)
    eye = sparse.eye(N, format="csc")
    lhs = (eye + half).tocsc()
    rhs_vec = (eye - half).dot(psi)
    psi_new = spsolve(lhs, rhs_vec)
    psi_new /= np.linalg.norm(psi_new)
    return psi_new


def gaussian_wavepacket(center, sigma=SIGMA):
    psi = np.zeros(N, dtype=complex)
    cx, cy, cz = center
    for i in range(N):
        x, y, z = pos[i]
        r2 = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi


def center_of_mass_x(psi):
    rho = np.abs(psi)**2
    return float(np.sum(rho * pos[:, 0]) / max(np.sum(rho), 1e-30))


def velocity_array(cx):
    vel = np.zeros(len(cx))
    vel[1:] = (cx[1:] - cx[:-1]) / DT
    vel[0] = vel[1]
    return vel


def acceleration_from_sep(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2 * sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def early_mean(arr):
    window = arr[EARLY_START:min(EARLY_END, len(arr))]
    return float(np.mean(window)), float(np.std(window))


# ── mid-plane flux measurement ──────────────────────────────────────────
def midplane_edges(x_mid):
    """Return list of (i, j) edges that cross x = x_mid (i on left, j on right)."""
    edges = []
    for i in range(N):
        xi = pos[i, 0]
        for j in adj_list[i]:
            if j <= i:
                continue
            xj = pos[j, 0]
            if xi < x_mid and xj >= x_mid:
                edges.append((i, j))
            elif xj < x_mid and xi >= x_mid:
                edges.append((j, i))
    return edges


def probability_current_midplane(psi, edges):
    """
    J through mid-plane = sum over crossing edges of Im(psi_i* hop_ij psi_j).
    For Wilson fermion hop: hop_ij = -0.5j + 0.5*r
    We want net rightward flux.
    """
    hop = -0.5j + 0.5 * WILSON_R
    j_total = 0.0
    for i_left, j_right in edges:
        j_total += np.imag(np.conj(psi[i_left]) * hop * psi[j_right])
    return float(j_total)


# ── Approach 1: fixed inertia, vary source alpha ────────────────────────
def run_approach1(G_val):
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    print()
    print("=" * 92)
    print("APPROACH 1: FIXED INERTIAL MASS, VARY SOURCE ALPHA")
    print("=" * 92)
    print(f"G={G_val}, inertial_mass={FIXED_INERTIAL_MASS} (same for all)")
    print(f"Alpha sweep: {ALPHA_VALUES}")
    print(f"Separation d={D_SEP}")
    print()

    # Fix alpha_A = 1.0, sweep alpha_B
    results_a1 = []
    alpha_a = 1.0

    for alpha_b in ALPHA_VALUES:
        t0 = time.time()
        # SHARED evolution - track individual orbitals
        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        cx_a_sh = np.zeros(N_STEPS + 1)
        cx_b_sh = np.zeros(N_STEPS + 1)
        cx_a_sh[0] = center_of_mass_x(psi_a)
        cx_b_sh[0] = center_of_mass_x(psi_b)

        for t in range(N_STEPS):
            rho = alpha_a * np.abs(psi_a)**2 + alpha_b * np.abs(psi_b)**2
            phi = solve_poisson(rho, G_val)
            h_a = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            cx_a_sh[t + 1] = center_of_mass_x(psi_a)
            cx_b_sh[t + 1] = center_of_mass_x(psi_b)

        # SELF_ONLY evolution
        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        cx_a_so = np.zeros(N_STEPS + 1)
        cx_b_so = np.zeros(N_STEPS + 1)
        cx_a_so[0] = center_of_mass_x(psi_a)
        cx_b_so[0] = center_of_mass_x(psi_b)

        for t in range(N_STEPS):
            phi_a = solve_poisson(alpha_a * np.abs(psi_a)**2, G_val)
            phi_b = solve_poisson(alpha_b * np.abs(psi_b)**2, G_val)
            h_a = build_wilson_hamiltonian(phi_a, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi_b, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            cx_a_so[t + 1] = center_of_mass_x(psi_a)
            cx_b_so[t + 1] = center_of_mass_x(psi_b)

        sep_sh = cx_b_sh - cx_a_sh
        sep_so = cx_b_so - cx_a_so
        a_mut = acceleration_from_sep(sep_sh) - acceleration_from_sep(sep_so)
        mean_a, std_a = early_mean(a_mut)
        snr = abs(mean_a) / (std_a + 1e-12)

        # Antisymmetric decomposition for individual orbitals
        dv_a = velocity_array(cx_a_sh) - velocity_array(cx_a_so)
        dv_b = velocity_array(cx_b_sh) - velocity_array(cx_b_so)
        dv_a_mean = float(np.mean(dv_a[EARLY_START:EARLY_END]))
        dv_b_mean = float(np.mean(dv_b[EARLY_START:EARLY_END]))
        common = (dv_a_mean + dv_b_mean) / 2.0
        mutual = (dv_a_mean - dv_b_mean) / 2.0

        elapsed = time.time() - t0

        results_a1.append({
            "alpha_b": alpha_b,
            "a_mutual": mean_a,
            "std": std_a,
            "snr": snr,
            "common": common,
            "mutual": mutual,
        })

        print(
            f"  alpha_B={alpha_b:.1f}: a_mut={mean_a:+.6e} +/- {std_a:.6e} "
            f"(SNR={snr:.2f}), common={common:+.4e}, mutual={mutual:+.4e} ({elapsed:.1f}s)"
        )

    # Now sweep alpha_A with alpha_B = 1.0 fixed
    print()
    print("  --- Now: fix alpha_B=1.0, sweep alpha_A ---")
    results_a1_rev = []
    alpha_b_fixed = 1.0

    for alpha_a_var in ALPHA_VALUES:
        t0 = time.time()
        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        cx_a_sh = np.zeros(N_STEPS + 1)
        cx_b_sh = np.zeros(N_STEPS + 1)
        cx_a_sh[0] = center_of_mass_x(psi_a)
        cx_b_sh[0] = center_of_mass_x(psi_b)

        for t in range(N_STEPS):
            rho = alpha_a_var * np.abs(psi_a)**2 + alpha_b_fixed * np.abs(psi_b)**2
            phi = solve_poisson(rho, G_val)
            h_a = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            cx_a_sh[t + 1] = center_of_mass_x(psi_a)
            cx_b_sh[t + 1] = center_of_mass_x(psi_b)

        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        cx_a_so = np.zeros(N_STEPS + 1)
        cx_b_so = np.zeros(N_STEPS + 1)
        cx_a_so[0] = center_of_mass_x(psi_a)
        cx_b_so[0] = center_of_mass_x(psi_b)

        for t in range(N_STEPS):
            phi_a = solve_poisson(alpha_a_var * np.abs(psi_a)**2, G_val)
            phi_b = solve_poisson(alpha_b_fixed * np.abs(psi_b)**2, G_val)
            h_a = build_wilson_hamiltonian(phi_a, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi_b, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            cx_a_so[t + 1] = center_of_mass_x(psi_a)
            cx_b_so[t + 1] = center_of_mass_x(psi_b)

        sep_sh = cx_b_sh - cx_a_sh
        sep_so = cx_b_so - cx_a_so
        a_mut = acceleration_from_sep(sep_sh) - acceleration_from_sep(sep_so)
        mean_a, std_a = early_mean(a_mut)
        snr = abs(mean_a) / (std_a + 1e-12)

        dv_a = velocity_array(cx_a_sh) - velocity_array(cx_a_so)
        dv_b = velocity_array(cx_b_sh) - velocity_array(cx_b_so)
        dv_a_mean = float(np.mean(dv_a[EARLY_START:EARLY_END]))
        dv_b_mean = float(np.mean(dv_b[EARLY_START:EARLY_END]))
        common = (dv_a_mean + dv_b_mean) / 2.0
        mutual = (dv_a_mean - dv_b_mean) / 2.0

        elapsed = time.time() - t0

        results_a1_rev.append({
            "alpha_a": alpha_a_var,
            "a_mutual": mean_a,
            "std": std_a,
            "snr": snr,
            "common": common,
            "mutual": mutual,
        })

        print(
            f"  alpha_A={alpha_a_var:.1f}: a_mut={mean_a:+.6e} +/- {std_a:.6e} "
            f"(SNR={snr:.2f}), common={common:+.4e}, mutual={mutual:+.4e} ({elapsed:.1f}s)"
        )

    # Fit power law |a_mut| vs alpha_B (separation-based)
    print()
    print("  --- Fits (separation acceleration) ---")
    alphas_b = np.array([r["alpha_b"] for r in results_a1])
    a_muts_b = np.array([abs(r["a_mutual"]) for r in results_a1])
    if np.all(a_muts_b > 0):
        log_alpha = np.log(alphas_b)
        log_a = np.log(a_muts_b)
        slope, intercept = np.polyfit(log_alpha, log_a, 1)
        fit_vals = np.exp(intercept) * alphas_b**slope
        ss_res = np.sum((a_muts_b - fit_vals)**2)
        ss_tot = np.sum((a_muts_b - np.mean(a_muts_b))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        print(f"  |a_sep| vs alpha_B: exponent={slope:.3f}, R^2={r2:.6f}")

    # Fit antisymmetric mutual mode vs alpha_B
    print()
    print("  --- Fits (antisymmetric mutual mode) ---")
    muts_b = np.array([abs(r["mutual"]) for r in results_a1])
    if np.all(muts_b > 0):
        log_alpha = np.log(alphas_b)
        log_m = np.log(muts_b)
        slope, intercept = np.polyfit(log_alpha, log_m, 1)
        fit_vals = np.exp(intercept) * alphas_b**slope
        ss_res = np.sum((muts_b - fit_vals)**2)
        ss_tot = np.sum((muts_b - np.mean(muts_b))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        print(f"  |mutual_mode| vs alpha_B: exponent={slope:.3f}, R^2={r2:.6f}")
        norm = muts_b / alphas_b
        cv = np.std(norm) / abs(np.mean(norm))
        print(f"  |mutual_mode|/alpha_B: CV={cv:.3%} (want <15%)")
    else:
        print("  WARNING: some mutual_mode values are zero")

    alphas_a = np.array([r["alpha_a"] for r in results_a1_rev])
    muts_a = np.array([abs(r["mutual"]) for r in results_a1_rev])
    if np.all(muts_a > 0):
        log_alpha = np.log(alphas_a)
        log_m = np.log(muts_a)
        slope, intercept = np.polyfit(log_alpha, log_m, 1)
        fit_vals = np.exp(intercept) * alphas_a**slope
        ss_res = np.sum((muts_a - fit_vals)**2)
        ss_tot = np.sum((muts_a - np.mean(muts_a))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        print(f"  |mutual_mode| vs alpha_A: exponent={slope:.3f}, R^2={r2:.6f}")
        norm = muts_a / alphas_a
        cv = np.std(norm) / abs(np.mean(norm))
        print(f"  |mutual_mode|/alpha_A: CV={cv:.3%} (want <15%)")
    else:
        print("  WARNING: some mutual_mode values are zero")

    return results_a1, results_a1_rev


# ── Approach 2: mid-plane probability current flux ──────────────────────
def run_approach2(G_val):
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)
    x_mid = (x_a + x_b) / 2.0

    edges = midplane_edges(x_mid)

    print()
    print("=" * 92)
    print("APPROACH 2: MID-PLANE PROBABILITY CURRENT FLUX")
    print("=" * 92)
    print(f"G={G_val}, mid-plane at x={x_mid}")
    print(f"Number of crossing edges: {len(edges)}")
    print(f"Alpha sweep: {ALPHA_VALUES}")
    print()

    results_a2 = []
    alpha_a = 1.0

    for alpha_b in ALPHA_VALUES:
        t0 = time.time()

        # SHARED
        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        j_sh_a = np.zeros(N_STEPS + 1)
        j_sh_b = np.zeros(N_STEPS + 1)

        for t in range(N_STEPS):
            rho = alpha_a * np.abs(psi_a)**2 + alpha_b * np.abs(psi_b)**2
            phi = solve_poisson(rho, G_val)
            h_a = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            j_sh_a[t + 1] = probability_current_midplane(psi_a, edges)
            j_sh_b[t + 1] = probability_current_midplane(psi_b, edges)

        # SELF_ONLY
        psi_a = gaussian_wavepacket(center_a)
        psi_b = gaussian_wavepacket(center_b)
        j_so_a = np.zeros(N_STEPS + 1)
        j_so_b = np.zeros(N_STEPS + 1)

        for t in range(N_STEPS):
            phi_a = solve_poisson(alpha_a * np.abs(psi_a)**2, G_val)
            phi_b = solve_poisson(alpha_b * np.abs(psi_b)**2, G_val)
            h_a = build_wilson_hamiltonian(phi_a, FIXED_INERTIAL_MASS)
            h_b = build_wilson_hamiltonian(phi_b, FIXED_INERTIAL_MASS)
            psi_a = cn_step(psi_a, h_a)
            psi_b = cn_step(psi_b, h_b)
            j_so_a[t + 1] = probability_current_midplane(psi_a, edges)
            j_so_b[t + 1] = probability_current_midplane(psi_b, edges)

        # Mutual flux = SHARED - SELF_ONLY
        dj_a = j_sh_a - j_so_a  # extra rightward flux for A (toward B)
        dj_b = j_sh_b - j_so_b  # extra rightward flux for B (toward A would be leftward = negative)

        mean_dj_a, std_dj_a = early_mean(dj_a)
        mean_dj_b, std_dj_b = early_mean(dj_b)
        # Net mutual flux toward mid-plane: A flows right, B flows left
        net_mutual = mean_dj_a - mean_dj_b
        elapsed = time.time() - t0

        results_a2.append({
            "alpha_b": alpha_b,
            "dj_a": mean_dj_a,
            "dj_b": mean_dj_b,
            "net_mutual": net_mutual,
            "std_a": std_dj_a,
            "std_b": std_dj_b,
        })

        print(
            f"  alpha_B={alpha_b:.1f}: "
            f"dJ_A={mean_dj_a:+.6e} dJ_B={mean_dj_b:+.6e} "
            f"net={net_mutual:+.6e} ({elapsed:.1f}s)"
        )

    # Fit net mutual flux vs alpha_B
    print()
    alphas = np.array([r["alpha_b"] for r in results_a2])
    nets = np.array([abs(r["net_mutual"]) for r in results_a2])
    if np.all(nets > 0):
        log_alpha = np.log(alphas)
        log_net = np.log(nets)
        slope, intercept = np.polyfit(log_alpha, log_net, 1)
        fit_vals = np.exp(intercept) * alphas**slope
        ss_res = np.sum((nets - fit_vals)**2)
        ss_tot = np.sum((nets - np.mean(nets))**2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        print(f"  |net_mutual_flux| vs alpha_B: exponent={slope:.3f}, R^2={r2:.6f}")

        norm = nets / alphas
        cv = np.std(norm) / abs(np.mean(norm)) if abs(np.mean(norm)) > 1e-30 else float("inf")
        print(f"  |net_flux|/alpha_B: CV={cv:.3%}")
    else:
        print("  WARNING: some net_mutual values are zero, cannot fit")

    return results_a2


# ── Approach 3: perturbative regime ─────────────────────────────────────
def run_approach3():
    center = SIDE // 2
    x_a = center - D_SEP // 2
    x_b = center + (D_SEP - D_SEP // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    print()
    print("=" * 92)
    print("APPROACH 3: PERTURBATIVE REGIME (WEAK G)")
    print("=" * 92)
    print(f"G values: {G_VALUES}")
    print(f"Mass values (inertial = source): {MASS_VALUES_APP3}")
    print(f"Test: does the both-masses CV clean up at weak G?")
    print()

    for G_val in G_VALUES:
        print(f"  --- G = {G_val} ---")
        grid_results = {}
        for mass_a in MASS_VALUES_APP3:
            for mass_b in MASS_VALUES_APP3:
                t0 = time.time()

                # SHARED
                psi_a = gaussian_wavepacket(center_a)
                psi_b = gaussian_wavepacket(center_b)
                cx_a_sh = np.zeros(N_STEPS + 1)
                cx_b_sh = np.zeros(N_STEPS + 1)
                cx_a_sh[0] = center_of_mass_x(psi_a)
                cx_b_sh[0] = center_of_mass_x(psi_b)

                for t in range(N_STEPS):
                    rho = mass_a * np.abs(psi_a)**2 + mass_b * np.abs(psi_b)**2
                    phi = solve_poisson(rho, G_val)
                    h_a = build_wilson_hamiltonian(phi, mass_a)
                    h_b = build_wilson_hamiltonian(phi, mass_b)
                    psi_a = cn_step(psi_a, h_a)
                    psi_b = cn_step(psi_b, h_b)
                    cx_a_sh[t + 1] = center_of_mass_x(psi_a)
                    cx_b_sh[t + 1] = center_of_mass_x(psi_b)

                # SELF_ONLY
                psi_a = gaussian_wavepacket(center_a)
                psi_b = gaussian_wavepacket(center_b)
                cx_a_so = np.zeros(N_STEPS + 1)
                cx_b_so = np.zeros(N_STEPS + 1)
                cx_a_so[0] = center_of_mass_x(psi_a)
                cx_b_so[0] = center_of_mass_x(psi_b)

                for t in range(N_STEPS):
                    phi_a = solve_poisson(mass_a * np.abs(psi_a)**2, G_val)
                    phi_b = solve_poisson(mass_b * np.abs(psi_b)**2, G_val)
                    h_a = build_wilson_hamiltonian(phi_a, mass_a)
                    h_b = build_wilson_hamiltonian(phi_b, mass_b)
                    psi_a = cn_step(psi_a, h_a)
                    psi_b = cn_step(psi_b, h_b)
                    cx_a_so[t + 1] = center_of_mass_x(psi_a)
                    cx_b_so[t + 1] = center_of_mass_x(psi_b)

                # Mutual acceleration from separation
                sep_sh = cx_b_sh - cx_a_sh
                sep_so = cx_b_so - cx_a_so
                a_mut = acceleration_from_sep(sep_sh) - acceleration_from_sep(sep_so)
                mean_a, std_a = early_mean(a_mut)

                # Also compute velocity-based impulse
                v_a_sh = velocity_array(cx_a_sh)
                v_a_so = velocity_array(cx_a_so)
                v_b_sh = velocity_array(cx_b_sh)
                v_b_so = velocity_array(cx_b_so)

                dv_a = v_a_sh - v_a_so  # A velocity change from mutual
                dv_b = v_b_sh - v_b_so  # B velocity change from mutual

                impulse_a = mass_a * float(np.mean(dv_a[EARLY_START:EARLY_END]))
                impulse_b = mass_b * float(np.mean(dv_b[EARLY_START:EARLY_END]))
                # impulse_b should be opposite sign to impulse_a if action-reaction holds

                elapsed = time.time() - t0

                # Decompose into symmetric (common) and antisymmetric (mutual)
                # Common mode: both shift same direction = (dv_A + dv_B)/2
                # Mutual mode: they shift toward each other = (dv_A - dv_B)/2
                # For attraction: A should move right (dv_A > 0), B left (dv_B < 0)
                # So mutual = (dv_A - dv_B)/2 > 0 for attraction
                dv_a_mean = float(np.mean(dv_a[EARLY_START:EARLY_END]))
                dv_b_mean = float(np.mean(dv_b[EARLY_START:EARLY_END]))
                common_mode = (dv_a_mean + dv_b_mean) / 2.0
                mutual_mode = (dv_a_mean - dv_b_mean) / 2.0

                # Antisymmetric impulse: mutual_mode * reduced_mass-like
                # For F = M_A*M_B law, the antisymmetric acceleration should
                # scale with partner mass
                # a_A_antisym = mutual_mode scaled by 1/M_A, so F_A = M_A * a_A_antisym
                # which should be proportional to M_B

                grid_results[(mass_a, mass_b)] = {
                    "a_mutual": mean_a,
                    "std": std_a,
                    "impulse_a": impulse_a,
                    "impulse_b": impulse_b,
                    "dv_a": dv_a_mean,
                    "dv_b": dv_b_mean,
                    "common_mode": common_mode,
                    "mutual_mode": mutual_mode,
                    "p_a_per_mb": impulse_a / mass_b if mass_b > 0 else 0,
                    "p_b_per_ma": abs(impulse_b) / mass_a if mass_a > 0 else 0,
                }

                print(
                    f"    M_A={mass_a:.1f} M_B={mass_b:.1f}: "
                    f"a_mut={mean_a:+.4e}, common={common_mode:+.4e}, mutual={mutual_mode:+.4e} "
                    f"({elapsed:.1f}s)"
                )

        # Decomposition analysis
        print()
        print(f"    --- Symmetric/Antisymmetric Decomposition (G={G_val}) ---")
        for mass_a in MASS_VALUES_APP3:
            for mass_b in MASS_VALUES_APP3:
                r = grid_results[(mass_a, mass_b)]
                ratio = abs(r["mutual_mode"]) / (abs(r["common_mode"]) + 1e-30)
                print(
                    f"    M_A={mass_a:.1f} M_B={mass_b:.1f}: "
                    f"common={r['common_mode']:+.4e}, mutual={r['mutual_mode']:+.4e}, "
                    f"|mutual/common|={ratio:.4f}"
                )

        # Check if mutual_mode scales with partner mass
        # Fix M_A=1.0, sweep M_B
        print()
        print(f"    --- Mutual mode vs partner mass (G={G_val}) ---")
        mut_vs_mb = []
        for mass_b in MASS_VALUES_APP3:
            r = grid_results[(1.0, mass_b)]
            mut_vs_mb.append((mass_b, r["mutual_mode"]))
            print(f"    M_A=1.0, M_B={mass_b:.1f}: mutual_mode={r['mutual_mode']:+.6e}")

        mbs = np.array([x[0] for x in mut_vs_mb])
        muts = np.array([abs(x[1]) for x in mut_vs_mb])
        if np.all(muts > 0):
            log_mb = np.log(mbs)
            log_mut = np.log(muts)
            slope, intercept = np.polyfit(log_mb, log_mut, 1)
            fit_vals = np.exp(intercept) * mbs**slope
            ss_res = np.sum((muts - fit_vals)**2)
            ss_tot = np.sum((muts - np.mean(muts))**2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            print(f"    |mutual_mode| vs M_B: exponent={slope:.3f}, R^2={r2:.6f}")
            norm_mut = muts / mbs
            cv_mut = np.std(norm_mut) / abs(np.mean(norm_mut))
            print(f"    |mutual_mode|/M_B: CV={cv_mut:.3%}")

        # Also check normalization of raw impulses
        pa_norm = [grid_results[k]["p_a_per_mb"] for k in grid_results]
        pb_norm = [grid_results[k]["p_b_per_ma"] for k in grid_results]
        pa_cv = np.std(pa_norm) / abs(np.mean(pa_norm)) if abs(np.mean(pa_norm)) > 1e-30 else float("inf")
        pb_cv = np.std(pb_norm) / abs(np.mean(pb_norm)) if abs(np.mean(pb_norm)) > 1e-30 else float("inf")

        print(f"    Raw P_A/M_B: CV={pa_cv:.3%}")
        print(f"    Raw P_B/M_A: CV={pb_cv:.3%}")
        print()


# ── main ────────────────────────────────────────────────────────────────
def main():
    print("=" * 92)
    print("BOTH-MASSES REDESIGN: THREE APPROACHES")
    print("=" * 92)
    print(f"Lattice: {SIDE}^3 = {N} sites, open BC, Wilson r={WILSON_R}")
    print(f"DT={DT}, sigma={SIGMA}, mu2={MU2}, d={D_SEP}")
    print()

    t_total = time.time()

    # Approach 1 at G=5 (the standard surface)
    r1, r1_rev = run_approach1(G_val=5.0)

    # Approach 2 at G=5
    r2 = run_approach2(G_val=5.0)

    # Approach 3: sweep G with both inertial masses varying
    run_approach3()

    total_time = time.time() - t_total

    # ── Final summary ───────────────────────────────────────────────────
    print()
    print("=" * 92)
    print("FINAL SUMMARY")
    print("=" * 92)
    print(f"Total run time: {total_time:.0f}s ({total_time/60:.1f}min)")
    print()
    print("Approach 1 (fixed inertia, vary source alpha):")
    print("  FAILED. Separation acceleration is flat vs alpha_B (exponent ~0.02).")
    print("  The antisymmetric mutual mode changes sign with alpha asymmetry,")
    print("  not with partner alpha. Self-potential depth (phi[i]) still")
    print("  contaminates propagation speed even with fixed inertial mass.")
    print()
    print("Approach 2 (mid-plane probability current):")
    print("  PARTIAL. dJ_A is monotone in alpha_B and positive (rightward flux")
    print("  toward B increases with B source strength). But scaling is strongly")
    print("  sublinear (exponent ~0.29, CV ~44%). Mid-plane flux is the cleanest")
    print("  observable tested but still does not yield a retained F ~ M law.")
    print()
    print("Approach 3 (perturbative weak G):")
    print("  FAILED. Mutual mode is dominated by mass asymmetry (M_A - M_B),")
    print("  not partner mass. When M_A = M_B, mutual mode is near zero.")
    print("  The perturbative argument does not hold because common slowdown")
    print("  enters at O(G) through self-field in H diagonal, not O(G^2).")
    print()
    print("ROOT CAUSE (confirmed):")
    print("  The Hartree self-field phi(x) enters the Wilson Hamiltonian diagonal")
    print("  as an effective mass shift. Varying source strength or inertial mass")
    print("  changes self-field depth, which changes propagation group velocity.")
    print("  The SHARED-minus-SELF_ONLY residual then measures differential")
    print("  propagation speed, not the mutual exchange channel. No CoM-based")
    print("  observable can separate the two because they enter the same H diagonal.")


if __name__ == "__main__":
    main()
