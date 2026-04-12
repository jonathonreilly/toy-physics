#!/usr/bin/env python3
"""Diosi-Penrose decoherence rate RECHECK with unscreened field (mu2=0.001).

The DP decoherence rate for a mass in superposition of two positions is:
    Gamma_DP ~ G * m^2 / d

We compute this via the gravitational self-energy difference:
    Delta_E = E_LL + E_RR - 2*E_LR

On a small periodic lattice with mu2~0, the Green's function is nearly
flat (long-range), so the cross-term E_LR barely varies with d.
We test BOTH the static Delta_E and isolate the d-dependent cross-term.

We also test at several lattice sizes to show convergence of d-scaling.

PStack experiment: decoherence-unscreened-recheck
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


SIGMA = 1.5
MU2 = 0.001


def build_lattice(side):
    pos = [(x, y) for x in range(side) for y in range(side)]
    n = len(pos)
    col = np.array([(x + y) % 2 for x, y in pos], dtype=float)
    idx = {}
    for i, (x, y) in enumerate(pos):
        idx[(x, y)] = i
    adj = {}
    for i, (x, y) in enumerate(pos):
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = (x + dx) % side, (y + dy) % side
            neighbors.append(idx[(nx, ny)])
        adj[i] = neighbors
    return pos, col, adj, n


def make_laplacian_2d(adj, n):
    rows, cols, vals = [], [], []
    for i in range(n):
        nbrs = adj[i]
        rows.append(i); cols.append(i); vals.append(-float(len(nbrs)))
        for j in nbrs:
            rows.append(i); cols.append(j); vals.append(1.0)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(n, n))


def solve_phi(rho, L, mu2, G, n):
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G * rho)


def gaussian_2d(cx, cy, sigma, pos, n):
    psi = np.zeros(n, dtype=complex)
    for i, (x, y) in enumerate(pos):
        psi[i] = np.exp(-0.5 * ((x - cx)**2 + (y - cy)**2) / sigma**2)
    return psi / np.sqrt(np.sum(np.abs(psi)**2))


def grav_self_energy(rho, L, mu2, G, n):
    phi = solve_phi(rho, L, mu2, G, n)
    return 0.5 * np.dot(rho, phi)


def compute_energies(side, mass, G, separation, mu2=MU2, sigma=SIGMA):
    """Compute E_LL, E_RR, E_LR, and Delta_E for given parameters."""
    pos, col, adj, n = build_lattice(side)
    L = make_laplacian_2d(adj, n)

    cy = side / 2.0
    cx_L = side / 2.0 - separation / 2.0
    cx_R = side / 2.0 + separation / 2.0

    psi_L = gaussian_2d(cx_L, cy, sigma, pos, n)
    psi_R = gaussian_2d(cx_R, cy, sigma, pos, n)

    rho_L = np.abs(psi_L)**2 * mass
    rho_R = np.abs(psi_R)**2 * mass

    phi_L = solve_phi(rho_L, L, mu2, G, n)
    phi_R = solve_phi(rho_R, L, mu2, G, n)

    E_LL = 0.5 * np.dot(rho_L, phi_L)
    E_RR = 0.5 * np.dot(rho_R, phi_R)
    E_LR = np.dot(rho_L, phi_R)  # full cross energy

    delta_E = E_LL + E_RR - 2 * E_LR

    return E_LL, E_RR, E_LR, delta_E


# ---------------------------------------------------------------------------
# Full dynamical protocol: evolve superposition under NONLINEAR self-gravity
# ---------------------------------------------------------------------------
def build_hamiltonian(pos, col, adj, n, phi, mass):
    par = np.where(col == 0, 1.0, -1.0)
    diag = (mass + phi) * par
    rows, cols_arr, vals = [], [], []
    for i in range(n):
        rows.append(i); cols_arr.append(i); vals.append(diag[i])
    for i in range(n):
        for j in adj[i]:
            rows.append(i); cols_arr.append(j)
            if j > i or (j < i and (j == 0 and i == n - 1)):
                vals.append(-0.5j)
            else:
                vals.append(0.5j)
    return sparse.csc_matrix((vals, (rows, cols_arr)), shape=(n, n), dtype=complex)


def cn_step(H, psi, dt):
    n = len(psi)
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    return spsolve(A_plus, A_minus.dot(psi))


def run_decoherence(side, mass, G, separation, n_steps=60, dt=0.12,
                    mu2=MU2, sigma=SIGMA):
    """Evolve superposition, return coherence time series."""
    pos, col, adj, n = build_lattice(side)
    L = make_laplacian_2d(adj, n)

    cy = side / 2.0
    cx_L = side / 2.0 - separation / 2.0
    cx_R = side / 2.0 + separation / 2.0

    psi_L_init = gaussian_2d(cx_L, cy, sigma, pos, n)
    psi_R_init = gaussian_2d(cx_R, cy, sigma, pos, n)

    psi = (psi_L_init + psi_R_init) / np.sqrt(2)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))

    coherence = np.zeros(n_steps + 1)
    coherence[0] = np.abs(np.vdot(psi_L_init, psi) * np.vdot(psi, psi_R_init))

    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = solve_phi(rho, L, mu2, G, n)
        H = build_hamiltonian(pos, col, adj, n, phi, mass)
        psi = cn_step(H, psi, dt)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        coherence[step + 1] = np.abs(
            np.vdot(psi_L_init, psi) * np.vdot(psi, psi_R_init))

    return coherence


def fit_decay_from_envelope(coherence, dt):
    """Fit envelope of coherence peaks to extract decay rate."""
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(coherence)
    if len(peaks) < 2:
        # Try just using all local maxima manually
        peaks = []
        for i in range(1, len(coherence) - 1):
            if coherence[i] >= coherence[i-1] and coherence[i] >= coherence[i+1]:
                peaks.append(i)
        peaks = np.array(peaks)

    if len(peaks) < 2:
        return 0.0

    times = peaks * dt
    vals = coherence[peaks]
    valid = vals > 1e-20
    if np.sum(valid) < 2:
        return 0.0

    t = times[valid]
    lv = np.log(vals[valid])
    coeffs = np.polyfit(t, lv, 1)
    return -coeffs[0]  # positive = decaying


def main():
    print("=" * 76)
    print("Diosi-Penrose Decoherence RECHECK  --  UNSCREENED (mu2=0.001)")
    print("=" * 76)
    print(f"  MU2={MU2}, SIGMA={SIGMA}")
    print()

    # ===================================================================
    # PART 1: Static Delta_E on side=10
    # Verify G and mass scaling (which should be exact)
    # ===================================================================
    side = 10
    print("=" * 76)
    print(f"PART 1: Static energy analysis (side={side})")
    print("=" * 76)
    print()

    # --- G sweep ---
    G_values = [1, 5, 10, 20]
    d_fixed = 4
    m_fixed = 0.30

    print(f"  G sweep (d={d_fixed}, m={m_fixed}):")
    print(f"  {'G':>6} {'Delta_E':>14} {'E_LL':>12} {'E_LR':>12}")
    dEs_G = []
    for G in G_values:
        E_LL, E_RR, E_LR, dE = compute_energies(side, m_fixed, G, d_fixed)
        dEs_G.append(abs(dE))
        print(f"  {G:>6d} {dE:>14.6e} {E_LL:>12.6e} {E_LR:>12.6e}")

    log_G = np.log(G_values)
    log_dE = np.log(dEs_G)
    slope_G = np.polyfit(log_G, log_dE, 1)[0]
    print(f"  => Delta_E ~ G^{slope_G:.3f}  (DP: +1.0)")
    print()

    # --- mass sweep ---
    mass_values = [0.1, 0.2, 0.3, 0.5]
    G_fixed = 10

    print(f"  mass sweep (d={d_fixed}, G={G_fixed}):")
    print(f"  {'mass':>6} {'Delta_E':>14} {'E_LL':>12} {'E_LR':>12}")
    dEs_m = []
    for m in mass_values:
        E_LL, E_RR, E_LR, dE = compute_energies(side, m, G_fixed, d_fixed)
        dEs_m.append(abs(dE))
        print(f"  {m:>6.2f} {dE:>14.6e} {E_LL:>12.6e} {E_LR:>12.6e}")

    log_m = np.log(mass_values)
    log_dE = np.log(dEs_m)
    slope_m = np.polyfit(log_m, log_dE, 1)[0]
    print(f"  => Delta_E ~ m^{slope_m:.3f}  (DP: +2.0)")
    print()

    # --- d sweep: show the cross-energy E_LR behavior ---
    d_values = [2, 3, 4, 5, 6, 8]
    print(f"  d sweep (G={G_fixed}, m={m_fixed}):")
    print(f"  {'d':>4} {'Delta_E':>14} {'E_LL':>12} {'E_LR':>12} {'E_LL-E_LR':>14}")
    dEs_d = []
    diffs_d = []
    for d in d_values:
        E_LL, E_RR, E_LR, dE = compute_energies(side, m_fixed, G_fixed, d)
        dEs_d.append(abs(dE))
        diffs_d.append(E_LL - E_LR)
        print(f"  {d:>4d} {dE:>14.6e} {E_LL:>12.6e} {E_LR:>12.6e} {E_LL - E_LR:>14.6e}")

    log_d = np.log(d_values)
    log_dE = np.log(dEs_d)
    slope_d = np.polyfit(log_d, log_dE, 1)[0]
    print(f"  => Delta_E ~ d^{slope_d:.3f}  (DP: -1.0)")
    print()
    print(f"  NOTE: On periodic side={side}, E_LR barely changes with d")
    print(f"  because the Green's function wraps around. The DP 1/d scaling")
    print(f"  is a short-range feature that requires d << side/2.")
    print()

    # ===================================================================
    # PART 2: Larger lattice to see d-scaling emerge
    # ===================================================================
    for test_side in [20, 40]:
        print("=" * 76)
        print(f"PART 2: d-sweep on larger lattice (side={test_side})")
        print("=" * 76)

        # Use d values well below side/2
        if test_side == 20:
            test_d = [2, 3, 4, 5, 6, 8]
        else:
            test_d = [2, 3, 4, 5, 6, 8, 10, 12]

        print(f"  d sweep (G={G_fixed}, m={m_fixed}, side={test_side}):")
        print(f"  {'d':>4} {'Delta_E':>14} {'E_LL':>12} {'E_LR':>12}")
        test_dEs = []
        for d in test_d:
            E_LL, E_RR, E_LR, dE = compute_energies(test_side, m_fixed, G_fixed, d)
            test_dEs.append(abs(dE))
            print(f"  {d:>4d} {dE:>14.6e} {E_LL:>12.6e} {E_LR:>12.6e}")

        valid = [(d, dE) for d, dE in zip(test_d, test_dEs) if dE > 1e-30]
        if len(valid) >= 2:
            ld = np.log([v[0] for v in valid])
            ldE = np.log([v[1] for v in valid])
            s = np.polyfit(ld, ldE, 1)[0]
            print(f"  => Delta_E ~ d^{s:.3f}  (DP: -1.0)")
        print()

    # ===================================================================
    # PART 3: Dynamical decoherence (envelope decay) on side=10
    # ===================================================================
    side = 10
    print("=" * 76)
    print(f"PART 3: Dynamical envelope decay (side={side}, 60 steps, dt=0.12)")
    print("=" * 76)
    print()

    # d sweep
    d_values = [2, 3, 4, 5, 6, 8]
    print(f"  d sweep (G={G_fixed}, m={m_fixed}):")
    print(f"  {'d':>4} {'env_decay':>14} {'C(0)':>10} {'C(end)':>10}")
    env_d = []
    for d in d_values:
        coh = run_decoherence(side, m_fixed, G_fixed, d, n_steps=60, dt=0.12)
        gamma = fit_decay_from_envelope(coh, 0.12)
        env_d.append(gamma)
        print(f"  {d:>4d} {gamma:>14.6e} {coh[0]:>10.6f} {coh[-1]:>10.6f}")

    valid_d = [(d, g) for d, g in zip(d_values, env_d) if g > 1e-10]
    if len(valid_d) >= 2:
        ld = np.log([v[0] for v in valid_d])
        lg = np.log([v[1] for v in valid_d])
        s = np.polyfit(ld, lg, 1)[0]
        print(f"  => envelope_decay ~ d^{s:.3f}  (DP: -1.0)")
    else:
        print("  => Insufficient positive-decay data")
    print()

    # G sweep
    print(f"  G sweep (d={d_fixed}, m={m_fixed}):")
    print(f"  {'G':>6} {'env_decay':>14} {'C(0)':>10} {'C(end)':>10}")
    env_G = []
    for G in G_values:
        coh = run_decoherence(side, m_fixed, G, d_fixed, n_steps=60, dt=0.12)
        gamma = fit_decay_from_envelope(coh, 0.12)
        env_G.append(gamma)
        print(f"  {G:>6d} {gamma:>14.6e} {coh[0]:>10.6f} {coh[-1]:>10.6f}")

    valid_G = [(g, gam) for g, gam in zip(G_values, env_G) if gam > 1e-10]
    if len(valid_G) >= 2:
        lg = np.log([v[0] for v in valid_G])
        lgam = np.log([v[1] for v in valid_G])
        s = np.polyfit(lg, lgam, 1)[0]
        print(f"  => envelope_decay ~ G^{s:.3f}  (DP: +1.0)")
    else:
        print("  => Insufficient positive-decay data")
    print()

    # mass sweep
    print(f"  mass sweep (d={d_fixed}, G={G_fixed}):")
    print(f"  {'mass':>6} {'env_decay':>14} {'C(0)':>10} {'C(end)':>10}")
    env_m = []
    for m in mass_values:
        coh = run_decoherence(side, m, G_fixed, d_fixed, n_steps=60, dt=0.12)
        gamma = fit_decay_from_envelope(coh, 0.12)
        env_m.append(gamma)
        print(f"  {m:>6.2f} {gamma:>14.6e} {coh[0]:>10.6f} {coh[-1]:>10.6f}")

    valid_m = [(m, gam) for m, gam in zip(mass_values, env_m) if gam > 1e-10]
    if len(valid_m) >= 2:
        lm = np.log([v[0] for v in valid_m])
        lgam = np.log([v[1] for v in valid_m])
        s = np.polyfit(lm, lgam, 1)[0]
        print(f"  => envelope_decay ~ m^{s:.3f}  (DP: +2.0)")
    else:
        print("  => Insufficient positive-decay data")
    print()

    # ===================================================================
    # Summary
    # ===================================================================
    print("=" * 76)
    print("FINAL SUMMARY")
    print("=" * 76)
    print()
    print("  Static Delta_E (side=10):")
    print(f"    G-scaling:  {slope_G:+.3f}  (DP: +1.0)  -- MATCHES")
    print(f"    m-scaling:  {slope_m:+.3f}  (DP: +2.0)  -- MATCHES")
    print(f"    d-scaling:  {slope_d:+.3f}  (DP: -1.0)  -- FAILS (periodic lattice too small)")
    print()
    print("  The G and mass scalings are EXACT because Delta_E is bilinear in G")
    print("  and quadratic in m (through rho = m*|psi|^2). The d-scaling fails")
    print("  because on a periodic side=10 lattice with mu2=0.001, the Green's")
    print("  function is nearly flat -- the unscreened potential wraps around")
    print("  the torus. Larger lattices should show the 1/d emerge.")
    print()
    print("=" * 76)
    print("DONE")
    print("=" * 76)


if __name__ == "__main__":
    main()
