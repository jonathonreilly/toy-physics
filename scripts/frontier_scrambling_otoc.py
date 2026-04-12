#!/usr/bin/env python3
"""Scrambling time of self-gravity-localized states via OTOC.

Measures the out-of-time-order correlator (OTOC) to determine whether
the Zeno-localized state scrambles information logarithmically in
system size (discrete black hole) or polynomially (integrable).

The single-particle OTOC:
  F(t) = |G(i,j,t)|^4  where G(i,j,t) = <i|exp(-iHt)|j>
  C(t) = 1 - F(t)/F(0)

For a black hole: C(t) ~ exp(lambda_L * t), scrambling time t* ~ log(N)/lambda_L
For integrable:   C(t) ~ t^alpha (power-law), t* ~ N^beta

Protocol:
  1. Build Zeno-localized state via 60 Zeno steps at G=100
  2. Construct self-gravitating Hamiltonian at that density profile
  3. Diagonalize H, compute propagator G(i,j,t)
  4. Measure C(t) for site pairs at distances r=1,2,3,4
  5. Fit early-time growth to extract Lyapunov exponent lambda_L
  6. Compare G=0 (free) vs G=100 (localized) across side=8,10,12

PStack experiment: scrambling-otoc
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Physical parameters (matching Zeno probe)
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
ZENO_STEPS = 60
SIGMA = 1.5

SIDES = [8, 10, 12]
G_COMPARE = [0, 100]
DISTANCES = [1, 2, 3, 4]
T_MAX_STEPS = 80
T_SAMPLE = np.arange(0, T_MAX_STEPS + 1)


# ---------------------------------------------------------------------------
# 2D periodic lattice (from Zeno probe)
# ---------------------------------------------------------------------------
def make_2d_periodic_lattice(side: int):
    n = side * side
    pos = np.zeros((n, 2))
    col = np.zeros(n, dtype=int)
    idx = {}

    for ix in range(side):
        for iy in range(side):
            i = ix * side + iy
            pos[i] = [ix, iy]
            col[i] = (ix + iy) % 2
            idx[(ix, iy)] = i

    adj = [[] for _ in range(n)]
    rows, cols_sp, vals = [], [], []

    for ix in range(side):
        for iy in range(side):
            i = idx[(ix, iy)]
            neighbors = [
                idx[((ix + 1) % side, iy)],
                idx[((ix - 1) % side, iy)],
                idx[(ix, (iy + 1) % side)],
                idx[(ix, (iy - 1) % side)],
            ]
            adj[i] = neighbors
            deg = len(neighbors)
            rows.append(i); cols_sp.append(i); vals.append(-float(deg))
            for j in neighbors:
                rows.append(i); cols_sp.append(j); vals.append(1.0)

    L = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n))
    return pos, col, L, adj, n, idx


# ---------------------------------------------------------------------------
# Operators (from Zeno probe)
# ---------------------------------------------------------------------------
def solve_phi(rho, L, mu2, G, n):
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G * rho)


def make_hamiltonian(phi, col, adj, n):
    par = np.where(col == 0, 1.0, -1.0)
    diag = (MASS + phi) * par

    rows, cols_sp, vals = [], [], []
    for i in range(n):
        rows.append(i); cols_sp.append(i); vals.append(diag[i])
        for j in adj[i]:
            if j > i:
                rows.append(i); cols_sp.append(j); vals.append(-0.5j)
                rows.append(j); cols_sp.append(i); vals.append(0.5j)

    H = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n), dtype=complex)
    return H


def cn_step(psi, H, dt, n):
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    rhs = A_minus.dot(psi)
    return spsolve(A_plus, rhs)


# ---------------------------------------------------------------------------
# Wavepacket utilities
# ---------------------------------------------------------------------------
def gaussian_2d(pos, center, sigma, n):
    dx = pos[:, 0] - center[0]
    dy = pos[:, 1] - center[1]
    psi = np.exp(-0.5 * (dx**2 + dy**2) / sigma**2)
    psi = psi.astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi


def width(psi, pos):
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dx = pos[:, 0] - cx
    dy = pos[:, 1] - cy
    return np.sqrt(np.sum(prob * (dx**2 + dy**2)))


# ---------------------------------------------------------------------------
# Prepare Zeno-localized state
# ---------------------------------------------------------------------------
def prepare_zeno_state(side, G, pos, col, L, adj, n):
    """Evolve a Gaussian under self-gravity for ZENO_STEPS to get localized state."""
    center = np.array([side / 2.0, side / 2.0])
    psi = gaussian_2d(pos, center, SIGMA, n)

    if G == 0:
        return psi

    for step in range(ZENO_STEPS):
        rho = np.abs(psi)**2
        phi = solve_phi(rho, L, MU2, G, n)
        H = make_hamiltonian(phi, col, adj, n)
        psi = cn_step(psi, H, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))

    return psi


# ---------------------------------------------------------------------------
# Build full Hamiltonian at frozen density profile
# ---------------------------------------------------------------------------
def build_frozen_hamiltonian(psi_loc, G, L, col, adj, n):
    """Build H with gravitational potential from the localized density."""
    rho = np.abs(psi_loc)**2
    if G > 0:
        phi = solve_phi(rho, L, MU2, G, n)
    else:
        phi = np.zeros(n)
    H = make_hamiltonian(phi, col, adj, n)
    return H


# ---------------------------------------------------------------------------
# Propagator via eigendecomposition
# ---------------------------------------------------------------------------
def compute_propagator_table(H_dense, n, t_steps, dt):
    """Compute G(i,j,t) = <i|exp(-iHt)|j> for all t in t_steps.

    Returns: propagator[t_idx, i, j] complex array
    """
    evals, evecs = np.linalg.eigh(H_dense)

    n_t = len(t_steps)
    # For each time, compute exp(-i * evals * t * dt) phase factors
    # G(i,j,t) = sum_k evecs[i,k] * conj(evecs[j,k]) * exp(-i*evals[k]*t*dt)
    propagator = np.zeros((n_t, n, n), dtype=complex)

    for t_idx, t in enumerate(t_steps):
        phases = np.exp(-1j * evals * t * dt)  # (n,)
        # G[i,j] = sum_k evecs[i,k] * phases[k] * conj(evecs[j,k])
        # = (evecs @ diag(phases) @ evecs^dag)[i,j]
        propagator[t_idx] = (evecs * phases[np.newaxis, :]) @ evecs.conj().T

    return propagator


# ---------------------------------------------------------------------------
# BFS distance on lattice
# ---------------------------------------------------------------------------
def bfs_distance(adj, src, n):
    dist = np.full(n, -1, dtype=int)
    dist[src] = 0
    queue = [src]
    head = 0
    while head < len(queue):
        u = queue[head]; head += 1
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


# ---------------------------------------------------------------------------
# Select site pairs at given distances
# ---------------------------------------------------------------------------
def select_pairs(adj, center_idx, n, distances, n_pairs=4):
    """Select site pairs (center_idx, j) at each distance r.

    Returns dict: {r: [(i, j), ...]} where i=center_idx.
    """
    dist = bfs_distance(adj, center_idx, n)
    pairs = {}
    for r in distances:
        candidates = np.where(dist == r)[0]
        if len(candidates) == 0:
            pairs[r] = []
            continue
        # Pick up to n_pairs evenly spaced
        step = max(1, len(candidates) // n_pairs)
        selected = candidates[::step][:n_pairs]
        pairs[r] = [(center_idx, int(j)) for j in selected]
    return pairs


# ---------------------------------------------------------------------------
# OTOC measurement
# ---------------------------------------------------------------------------
def measure_otoc(propagator, pairs_by_r, t_steps):
    """Compute C(t) = 1 - |G(i,j,t)|^4 / |G(i,j,0)|^4 for each (r, pair).

    Returns dict: {r: C(t) array averaged over pairs}
    """
    results = {}
    for r, pairs in pairs_by_r.items():
        if len(pairs) == 0:
            results[r] = np.zeros(len(t_steps))
            continue

        c_avg = np.zeros(len(t_steps))
        for (i, j) in pairs:
            g_0 = propagator[0, i, j]
            f_0 = np.abs(g_0)**4
            if f_0 < 1e-30:
                # G(i,j,0) = delta(i,j), so for i!=j, F(0)=0
                # Use |G(i,j,t)|^2 directly as the scrambling measure
                for t_idx in range(len(t_steps)):
                    g_t = propagator[t_idx, i, j]
                    c_avg[t_idx] += np.abs(g_t)**2
                continue

            for t_idx in range(len(t_steps)):
                g_t = propagator[t_idx, i, j]
                f_t = np.abs(g_t)**4
                c_avg[t_idx] += 1.0 - f_t / f_0

        c_avg /= len(pairs)
        results[r] = c_avg

    return results


def measure_otoc_spreading(propagator, pairs_by_r, t_steps):
    """For i != j where G(i,j,0) = 0: measure |G(i,j,t)|^2 as spreading.

    This is the probability of reaching site i starting from site j.
    Scrambling = how fast this probability grows.
    """
    results = {}
    for r, pairs in pairs_by_r.items():
        if len(pairs) == 0:
            results[r] = np.zeros(len(t_steps))
            continue

        c_avg = np.zeros(len(t_steps))
        for (i, j) in pairs:
            for t_idx in range(len(t_steps)):
                g_t = propagator[t_idx, i, j]
                c_avg[t_idx] += np.abs(g_t)**2

        c_avg /= len(pairs)
        results[r] = c_avg

    return results


# ---------------------------------------------------------------------------
# Fit Lyapunov exponent
# ---------------------------------------------------------------------------
def fit_lyapunov(t_arr, c_arr, dt):
    """Fit early-time exponential growth: C(t) ~ A * exp(lambda_L * t).

    Returns lambda_L and quality of fit (R^2).
    """
    times = t_arr * dt

    # Find the regime where C is growing and nonzero
    mask = (c_arr > 1e-8) & (c_arr < 0.5) & (times > 0)
    if np.sum(mask) < 3:
        return 0.0, 0.0

    t_fit = times[mask]
    c_fit = c_arr[mask]

    # Log-linear fit: log(C) = log(A) + lambda_L * t
    log_c = np.log(c_fit + 1e-30)

    try:
        coeffs = np.polyfit(t_fit, log_c, 1)
        lambda_L = coeffs[0]

        # R^2
        predicted = np.polyval(coeffs, t_fit)
        ss_res = np.sum((log_c - predicted)**2)
        ss_tot = np.sum((log_c - np.mean(log_c))**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        return lambda_L, r2
    except Exception:
        return 0.0, 0.0


def fit_power_law(t_arr, c_arr, dt):
    """Fit power-law growth: C(t) ~ A * t^alpha.

    Returns alpha and R^2.
    """
    times = t_arr * dt

    mask = (c_arr > 1e-8) & (c_arr < 0.5) & (times > 0)
    if np.sum(mask) < 3:
        return 0.0, 0.0

    t_fit = times[mask]
    c_fit = c_arr[mask]

    # Log-log fit: log(C) = log(A) + alpha * log(t)
    log_t = np.log(t_fit + 1e-30)
    log_c = np.log(c_fit + 1e-30)

    try:
        coeffs = np.polyfit(log_t, log_c, 1)
        alpha = coeffs[0]

        predicted = np.polyval(coeffs, log_t)
        ss_res = np.sum((log_c - predicted)**2)
        ss_tot = np.sum((log_c - np.mean(log_c))**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        return alpha, r2
    except Exception:
        return 0.0, 0.0


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("FRONTIER: Scrambling Time via OTOC")
    print("  Does the Zeno-localized state scramble like a black hole?")
    print("=" * 78)
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, ZENO_STEPS={ZENO_STEPS}")
    print(f"  Lattice sides: {SIDES}")
    print(f"  G values: {G_COMPARE}")
    print(f"  Distances: {DISTANCES}")
    print(f"  T_MAX_STEPS={T_MAX_STEPS} (t_max = {T_MAX_STEPS * DT:.1f})")
    print()

    # Store results for final analysis
    all_results = {}  # (side, G) -> {r: (lambda_L, r2_exp, alpha, r2_pow)}

    for side in SIDES:
        n = side * side
        print("=" * 78)
        print(f"LATTICE: side={side}, n={n}")
        print("=" * 78)

        pos, col, L, adj, _, idx = make_2d_periodic_lattice(side)
        center = np.array([side / 2.0, side / 2.0])
        center_idx = np.argmin(np.sum((pos - center)**2, axis=1))

        # Select site pairs at each distance from center
        pairs_by_r = select_pairs(adj, center_idx, n, DISTANCES)
        for r in DISTANCES:
            print(f"  r={r}: {len(pairs_by_r[r])} pairs")
        print()

        for G in G_COMPARE:
            print("-" * 78)
            print(f"  G={G}: ", end="")

            # Step 1: Prepare state
            psi_loc = prepare_zeno_state(side, G, pos, col, L, adj, n)
            w = width(psi_loc, pos)
            print(f"width={w:.4f}, ", end="")

            # Localization measure: IPR (inverse participation ratio)
            prob = np.abs(psi_loc)**2
            ipr = 1.0 / np.sum(prob**2)
            print(f"IPR={ipr:.1f} (of n={n})")

            # Step 2: Build frozen Hamiltonian
            H = build_frozen_hamiltonian(psi_loc, G, L, col, adj, n)
            H_dense = H.toarray()

            # Check Hermiticity
            herm_err = np.max(np.abs(H_dense - H_dense.conj().T))
            print(f"  Hermiticity error: {herm_err:.2e}")

            # Step 3: Eigendecomposition and propagator
            print(f"  Computing propagator ({n}x{n}, {len(T_SAMPLE)} time steps)...", end="", flush=True)
            propagator = compute_propagator_table(H_dense, n, T_SAMPLE, DT)
            print(" done")

            # Step 4: Measure OTOC (spreading measure for i != j)
            otoc = measure_otoc_spreading(propagator, pairs_by_r, T_SAMPLE)

            # Step 5: Fit and report
            print()
            print(f"  {'r':>3s}  {'lambda_L':>10s}  {'R2_exp':>8s}  {'alpha':>8s}  {'R2_pow':>8s}  {'best_fit':>10s}  {'C_max':>8s}")
            print("  " + "-" * 68)

            results_G = {}
            for r in DISTANCES:
                c_arr = otoc[r]
                lambda_L, r2_exp = fit_lyapunov(T_SAMPLE, c_arr, DT)
                alpha, r2_pow = fit_power_law(T_SAMPLE, c_arr, DT)
                c_max = np.max(c_arr)

                best = "EXP" if r2_exp > r2_pow else "POWER"
                results_G[r] = (lambda_L, r2_exp, alpha, r2_pow, c_max)

                print(f"  {r:>3d}  {lambda_L:>10.4f}  {r2_exp:>8.4f}  {alpha:>8.4f}  {r2_pow:>8.4f}  {best:>10s}  {c_max:>8.6f}")

            all_results[(side, G)] = results_G

            # Print time series for r=1 and r=2
            print()
            print(f"  C(t) time series (G={G}, every 10 steps):")
            header = f"  {'t_step':>6s}  {'t':>6s}"
            for r in DISTANCES:
                header += f"  {'r='+str(r):>10s}"
            print(header)
            print("  " + "-" * (14 + 12 * len(DISTANCES)))
            for t_idx in range(0, len(T_SAMPLE), 10):
                t = T_SAMPLE[t_idx]
                row = f"  {t:>6d}  {t*DT:>6.2f}"
                for r in DISTANCES:
                    row += f"  {otoc[r][t_idx]:>10.6f}"
                print(row)
            print()

    # =========================================================================
    # Analysis: Scrambling classification
    # =========================================================================
    print()
    print("=" * 78)
    print("SCRAMBLING ANALYSIS")
    print("=" * 78)

    # Compare lambda_L across system sizes at fixed G and r
    print()
    print("1. Lyapunov exponent lambda_L(side, G, r):")
    print("-" * 78)
    print(f"  {'side':>6s}  {'n':>6s}  {'G':>6s}  {'r':>3s}  {'lambda_L':>10s}  {'R2_exp':>8s}  {'alpha':>8s}  {'R2_pow':>8s}")
    print("  " + "-" * 68)

    for side in SIDES:
        n = side * side
        for G in G_COMPARE:
            for r in DISTANCES:
                if (side, G) in all_results and r in all_results[(side, G)]:
                    lam, r2e, alp, r2p, cmax = all_results[(side, G)][r]
                    print(f"  {side:>6d}  {n:>6d}  {G:>6d}  {r:>3d}  {lam:>10.4f}  {r2e:>8.4f}  {alp:>8.4f}  {r2p:>8.4f}")

    # Check fast scrambling criterion: t* ~ log(N)/lambda_L
    print()
    print("2. Scrambling time scaling: t* = log(N) / lambda_L")
    print("-" * 78)
    for G in G_COMPARE:
        print(f"\n  G={G}:")
        for r in [1, 2]:
            lambdas = []
            ns = []
            for side in SIDES:
                n = side * side
                if (side, G) in all_results and r in all_results[(side, G)]:
                    lam = all_results[(side, G)][r][0]
                    if lam > 0.01:
                        lambdas.append(lam)
                        ns.append(n)

            if len(lambdas) >= 2:
                t_stars = [np.log(n_val) / lam for n_val, lam in zip(ns, lambdas)]
                print(f"    r={r}: ", end="")
                for n_val, lam, ts in zip(ns, lambdas, t_stars):
                    print(f"N={n_val}: lambda_L={lam:.4f}, t*={ts:.2f}  ", end="")
                print()

                # Check if t* scales as log(N)
                # If lambda_L ~ const, then t* ~ log(N) -> fast scrambling
                # If lambda_L ~ 1/N^alpha, then t* ~ N^alpha * log(N) -> slow
                lam_ratio = lambdas[-1] / lambdas[0]
                n_ratio = ns[-1] / ns[0]
                print(f"    lambda_L ratio (largest/smallest N): {lam_ratio:.3f}")
                print(f"    N ratio: {n_ratio:.1f}")
                if lam_ratio > 0.5:
                    print(f"    -> lambda_L approximately constant: FAST scrambling (t* ~ log N)")
                else:
                    # Fit lambda_L vs N power law
                    log_n = np.log(ns)
                    log_lam = np.log(lambdas)
                    try:
                        coeffs = np.polyfit(log_n, log_lam, 1)
                        print(f"    -> lambda_L ~ N^{coeffs[0]:.2f}: SLOW scrambling")
                    except Exception:
                        print(f"    -> lambda_L decreases: SLOW scrambling")
            else:
                print(f"    r={r}: insufficient data (lambda_L too small or no growth)")

    # Final verdict
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    # Focus on G=100, r=1 for the key diagnostic
    g_key = 100
    r_key = 1
    fast_evidence = 0
    slow_evidence = 0

    for side in SIDES:
        if (side, g_key) in all_results and r_key in all_results[(side, g_key)]:
            lam, r2e, alp, r2p, cmax = all_results[(side, g_key)][r_key]
            if r2e > r2p and r2e > 0.7:
                fast_evidence += 1
            elif r2p > r2e:
                slow_evidence += 1

    # Compare G=0 vs G=100
    free_lam = []
    grav_lam = []
    for side in SIDES:
        if (side, 0) in all_results and r_key in all_results[(side, 0)]:
            free_lam.append(all_results[(side, 0)][r_key][0])
        if (side, g_key) in all_results and r_key in all_results[(side, g_key)]:
            grav_lam.append(all_results[(side, g_key)][r_key][0])

    print()
    if free_lam and grav_lam:
        avg_free = np.mean(free_lam)
        avg_grav = np.mean(grav_lam)
        print(f"  Mean lambda_L (G=0,  r={r_key}): {avg_free:.4f}  [free particle]")
        print(f"  Mean lambda_L (G={g_key}, r={r_key}): {avg_grav:.4f}  [Zeno-localized]")
        if avg_grav > avg_free * 1.5:
            print(f"  -> Self-gravity ENHANCES scrambling (ratio = {avg_grav/avg_free:.2f}x)")
        elif avg_grav < avg_free * 0.67:
            print(f"  -> Self-gravity SUPPRESSES scrambling (ratio = {avg_grav/avg_free:.2f}x)")
        else:
            print(f"  -> Similar scrambling rates (ratio = {avg_grav/avg_free:.2f}x)")
    print()

    if fast_evidence > slow_evidence:
        print("  CLASSIFICATION: FAST SCRAMBLER (exponential growth)")
        print("  -> Zeno-localized state behaves as a DISCRETE BLACK HOLE")
        print("  -> Scrambling time t* ~ log(N) / lambda_L")
    elif slow_evidence > fast_evidence:
        print("  CLASSIFICATION: SLOW SCRAMBLER (power-law growth)")
        print("  -> Zeno-localized state is integrable, NOT a black hole")
        print("  -> Scrambling time t* ~ N^alpha")
    else:
        print("  CLASSIFICATION: INCONCLUSIVE")
        print("  -> Need larger systems or longer evolution to determine")

    print()
    print("=" * 78)
    print("DONE")
    print("=" * 78)


if __name__ == "__main__":
    main()
