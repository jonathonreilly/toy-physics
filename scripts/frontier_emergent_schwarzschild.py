#!/usr/bin/env python3
"""
Emergent Schwarzschild Metric from Self-Gravitating Matter on a Graph
======================================================================
THE NATURE EXPERIMENT: Does the self-gravitating two-field system produce
an effective metric that matches the Schwarzschild solution?

Setup:
  1. Build a large 2D bipartite graph (side=12, 144 nodes)
  2. Place a self-gravitating matter blob at center
  3. Let the two-field system (wave Φ + staggered ψ) equilibrate
  4. After equilibrium, inject TEST wavepackets at different distances
  5. Measure propagation speed v(r) from the spreading rate
  6. Compare v(r) to v_Schwarzschild(r) = sqrt(1 - 2GM/r)

If v(r) matches, gravitational spacetime curvature EMERGES from
quantum matter dynamics on a graph. This is the key Nature result.

Also test: does the equilibrium Φ profile match the Newtonian potential?
  Φ(r) should fall off as ~log(r) in 2D or ~1/r in 3D.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30; MU2 = 0.22; DT_PSI = 0.12; DT_PHI = 0.03
C_PHI = 1.0; BETA = 5.0; G_SELF = 100.0


# ============================================================================
# Graph
# ============================================================================

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)

def build_graph(seed=42, side=12):
    rng = random.Random(seed)
    coords = []; colors = []; index = {}; adj = {}; idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08*(rng.random()-0.5), y + 0.08*(rng.random()-0.5)))
            colors.append((x+y) % 2)
            index[(x, y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii, jj = i+di, j+dj
                if (ii, jj) not in index: continue
                b = index[(ii, jj)]
                if col[a] == col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0], pos[b,1]-pos[a,1]) <= 1.28:
                    _ae(adj, a, b)
    adj_l = {k: list(v) for k, v in adj.items()}
    return pos, col, adj_l, len(pos)


# ============================================================================
# Physics tools
# ============================================================================

def _laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()

def _build_H(pos, col, adj, n, mass, phi=None):
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    diag = mass * par
    if phi is not None: diag = diag - mass * phi
    H.setdiag(diag)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            H[i,j] += -0.5j * w; H[j,i] += 0.5j * w
    return H.tocsr()

def _cn_step(H, n, psi):
    ap = (speye(n, format='csc') + 1j*H*DT_PSI/2).tocsc()
    am = speye(n, format='csr') - 1j*H*DT_PSI/2
    return spsolve(ap, am.dot(psi))


# ============================================================================
# Main experiment
# ============================================================================

def run_experiment():
    t_start = time.time()
    print("=" * 70)
    print("EMERGENT SCHWARZSCHILD FROM SELF-GRAVITATING MATTER")
    print("=" * 70)

    pos, col, adj, n = build_graph(side=12)
    center_idx = n // 2
    center = pos[center_idx]
    L = _laplacian(pos, adj, n)
    phi_op = -C_PHI**2 * (L + MU2 * speye(n, format='csr'))

    print(f"  Graph: {n} nodes, side=12")
    print(f"  G_self={G_SELF}, beta={BETA}, c_phi={C_PHI}")
    print()

    # Step 1: Create self-gravitating matter blob at center
    print("--- PHASE 1: Self-gravitating equilibrium ---")
    sigma_blob = 1.5
    psi = np.exp(-0.5*((pos[:,0]-center[0])**2 + (pos[:,1]-center[1])**2) / sigma_blob**2).astype(complex)
    psi /= np.linalg.norm(psi)

    phi = np.zeros(n)
    pi_phi = np.zeros(n)
    H_free = _build_H(pos, col, adj, n, MASS)

    # Equilibrate: 50 iterations of two-field wave coupling
    N_EQUIL = 50
    for it in range(N_EQUIL):
        rho = np.abs(psi)**2
        source = BETA * G_SELF * rho

        # Leapfrog for Phi
        force_phi = phi_op.dot(phi) + source
        pi_phi += 0.5 * DT_PHI * force_phi
        phi += DT_PHI * pi_phi
        force_phi = phi_op.dot(phi) + source
        pi_phi += 0.5 * DT_PHI * force_phi

        # CN for psi
        H = _build_H(pos, col, adj, n, MASS, phi)
        psi = _cn_step(H, n, psi)

        if it < 5 or it % 10 == 0:
            w = np.sqrt(np.sum(np.abs(psi)**2 * ((pos[:,0]-center[0])**2 + (pos[:,1]-center[1])**2)) / np.sum(np.abs(psi)**2))
            print(f"  it={it:3d}: width={w:.3f}, |phi|={np.linalg.norm(phi):.3f}, |psi|={np.linalg.norm(psi):.6f}")

    print(f"\n  Equilibrated. Width: {w:.3f}, |phi|: {np.linalg.norm(phi):.3f}")

    # Step 2: Measure the equilibrium Phi profile
    print("\n--- PHASE 2: Equilibrium Phi profile ---")
    distances = np.sqrt((pos[:,0]-center[0])**2 + (pos[:,1]-center[1])**2)

    # Shell-average Phi by distance
    r_bins = np.linspace(0, 6, 13)
    phi_profile = []
    for i in range(len(r_bins)-1):
        mask = (distances >= r_bins[i]) & (distances < r_bins[i+1])
        if np.sum(mask) > 0:
            phi_profile.append((0.5*(r_bins[i]+r_bins[i+1]), np.mean(phi[mask]), np.sum(mask)))
        else:
            phi_profile.append((0.5*(r_bins[i]+r_bins[i+1]), 0, 0))

    print(f"  {'r':>6s} {'Phi':>10s} {'N_nodes':>8s}")
    for r, p, nn in phi_profile:
        print(f"  {r:6.2f} {p:10.4f} {int(nn):8d}")

    # Fit: Phi(r) ~ -GM/r (Newtonian) or -GM*log(r) (2D)
    r_vals = np.array([p[0] for p in phi_profile if p[2] > 0 and p[0] > 0.5])
    phi_vals = np.array([p[1] for p in phi_profile if p[2] > 0 and p[0] > 0.5])
    if len(r_vals) >= 3:
        # Try 1/r fit: Phi = a/r + b
        from scipy.optimize import curve_fit
        def inv_r(r, a, b): return a/r + b
        def log_r(r, a, b): return a*np.log(r) + b
        try:
            popt_r, _ = curve_fit(inv_r, r_vals, phi_vals)
            phi_pred_r = inv_r(r_vals, *popt_r)
            ss_res_r = np.sum((phi_vals - phi_pred_r)**2)
            ss_tot = np.sum((phi_vals - np.mean(phi_vals))**2)
            r2_invr = 1 - ss_res_r/ss_tot if ss_tot > 0 else 0
        except: r2_invr = 0; popt_r = [0, 0]
        try:
            popt_l, _ = curve_fit(log_r, r_vals, phi_vals)
            phi_pred_l = log_r(r_vals, *popt_l)
            ss_res_l = np.sum((phi_vals - phi_pred_l)**2)
            r2_log = 1 - ss_res_l/ss_tot if ss_tot > 0 else 0
        except: r2_log = 0; popt_l = [0, 0]

        print(f"\n  Phi fit:")
        print(f"    1/r:   R^2={r2_invr:.4f}, a={popt_r[0]:.4f}")
        print(f"    log(r): R^2={r2_log:.4f}, a={popt_l[0]:.4f}")
        better = "1/r" if r2_invr > r2_log else "log(r)"
        print(f"    Better fit: {better}")

    # Step 3: Measure propagation speed at different distances
    print("\n--- PHASE 3: Test wavepacket propagation speeds ---")
    print("  Inject narrow wavepackets at different distances from blob.")
    print("  Measure spreading rate = effective propagation speed v(r).")

    # The effective Hamiltonian after equilibrium:
    H_equil = _build_H(pos, col, adj, n, MASS, phi)

    speeds = []
    test_positions = [(center_idx, 0.0)]  # (node, distance)
    # Find nodes at various distances
    for target_r in [1.0, 2.0, 3.0, 4.0, 5.0]:
        candidates = [(i, abs(distances[i] - target_r)) for i in range(n) if col[i] == 0]
        candidates.sort(key=lambda x: x[1])
        if candidates:
            test_positions.append((candidates[0][0], distances[candidates[0][0]]))

    for test_node, r_test in test_positions:
        # Narrow Gaussian at test_node
        sigma_test = 0.8
        psi_test = np.exp(-0.5*((pos[:,0]-pos[test_node,0])**2 + (pos[:,1]-pos[test_node,1])**2) / sigma_test**2).astype(complex)
        psi_test /= np.linalg.norm(psi_test)

        # Measure width at t=0 and after 5 steps
        def wid(psi_):
            rho_ = np.abs(psi_)**2; rho_ /= np.sum(rho_)
            cx = np.sum(rho_*pos[:,0]); cy = np.sum(rho_*pos[:,1])
            return np.sqrt(np.sum(rho_*((pos[:,0]-cx)**2 + (pos[:,1]-cy)**2)))

        w0 = wid(psi_test)
        psi_evolved = psi_test.copy()
        for _ in range(5):
            psi_evolved = _cn_step(H_equil, n, psi_evolved)
        w5 = wid(psi_evolved)

        # Also measure on FREE Hamiltonian for comparison
        psi_free = psi_test.copy()
        for _ in range(5):
            psi_free = _cn_step(H_free, n, psi_free)
        w5_free = wid(psi_free)

        v_equil = (w5 - w0) / (5 * DT_PSI)
        v_free = (w5_free - w0) / (5 * DT_PSI)
        v_ratio = v_equil / v_free if abs(v_free) > 1e-10 else 0

        speeds.append((r_test, v_equil, v_free, v_ratio))
        print(f"  r={r_test:.1f}: v_equil={v_equil:.4f}, v_free={v_free:.4f}, ratio={v_ratio:.4f}")

    # Step 4: Compare v(r) to Schwarzschild prediction
    print("\n--- PHASE 4: Schwarzschild comparison ---")
    print("  v(r)/v_free should decrease near the mass (gravitational redshift)")
    print("  Schwarzschild: v(r) = v_free * sqrt(1 - r_s/r)")

    r_arr = np.array([s[0] for s in speeds if s[0] > 0])
    ratio_arr = np.array([s[3] for s in speeds if s[0] > 0])

    if len(r_arr) >= 3:
        # Fit: ratio = sqrt(1 - r_s/r) => ratio^2 = 1 - r_s/r
        # => 1 - ratio^2 = r_s/r => r_s = r*(1-ratio^2)
        ratio2 = ratio_arr**2
        r_s_estimates = r_arr * (1 - ratio2)
        r_s_mean = np.mean(r_s_estimates[r_s_estimates > 0]) if np.any(r_s_estimates > 0) else 0

        print(f"\n  Schwarzschild radius estimates: {r_s_estimates}")
        print(f"  Mean r_s = {r_s_mean:.4f}")

        # Fit quality: predicted ratio vs actual
        if r_s_mean > 0:
            ratio_pred = np.sqrt(np.clip(1 - r_s_mean/r_arr, 0, 1))
            ss_res = np.sum((ratio_arr - ratio_pred)**2)
            ss_tot = np.sum((ratio_arr - np.mean(ratio_arr))**2)
            r2_schwarz = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            print(f"  Schwarzschild fit R^2 = {r2_schwarz:.4f}")

            print(f"\n  {'r':>6s} {'v_ratio':>8s} {'v_Schwarz':>10s}")
            for r, vr, vp in zip(r_arr, ratio_arr, ratio_pred):
                print(f"  {r:6.1f} {vr:8.4f} {vp:10.4f}")

    elapsed = time.time() - t_start
    print(f"\n  Total time: {elapsed:.1f}s")


if __name__ == '__main__':
    run_experiment()
