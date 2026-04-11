#!/usr/bin/env python3
"""
Emergent Geometry — Multi-Size Confirmation + Displacement Test
================================================================
Two questions:

Q1: Does the G=100 unanimous ROBUST_TOWARD hold at multiple graph sizes?
    Sizes: n=60, 80, 100, 120, 150. Seeds: 42-46. G=100.
    If ROBUST_TOWARD is size-stable, the emergent geometry lane is real.

Q2: Wavepacket displacement test (graph-native directional observable).
    Initialize wavepacket at graph center. Evolve under self-gravity
    with parity coupling. Measure centroid displacement toward/away from
    the density peak. This is a DYNAMICAL response, not a field-shape
    proxy — it directly measures whether the wavepacket moves toward
    the self-generated potential minimum.

    Positive displacement (toward density peak) = attraction.
    This closes the "no graph-native directional observable" blocker.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_EVOLVE = 3
K_CONNECT = 4


def grow_graph(n_final, G_self, n_evolve=N_EVOLVE, seed=42):
    rng = random.Random(seed)
    coords = [(0,0),(1,0),(0,1),(1,1),(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)]
    colors = [0,1,1,0,1,0,0,1]
    n_seed = len(coords)
    adj = {i: set() for i in range(n_seed)}
    for i in range(n_seed):
        for j in range(i+1, n_seed):
            if colors[i] != colors[j]:
                d = math.sqrt(sum((a-b)**2 for a,b in zip(coords[i],coords[j])))
                if d < 1.2:
                    adj[i].add(j); adj[j].add(i)
    pos = list(coords); col = list(colors); cur = n_seed
    psi = np.ones(n_seed, dtype=complex)
    pos_arr = np.array(pos)
    center_seed = np.mean(pos_arr, axis=0)
    for i in range(n_seed):
        r2 = (pos_arr[i,0]-center_seed[0])**2 + (pos_arr[i,1]-center_seed[1])**2
        psi[i] = np.exp(-0.5*r2/0.8**2)
    psi /= np.linalg.norm(psi)

    while cur < n_final:
        n = len(pos); pos_arr = np.array(pos); col_arr = np.array(col, dtype=int)
        adj_l = {k: list(v) for k, v in adj.items()}
        L = lil_matrix((n,n), dtype=float)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.sqrt((pos_arr[j,0]-pos_arr[i,0])**2 + (pos_arr[j,1]-pos_arr[i,1])**2)
                w = 1./max(d, 0.3)
                L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
        L = L.tocsr()
        rho = np.abs(psi)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)
        H = lil_matrix((n,n), dtype=complex)
        par = np.where(col_arr==0, 1., -1.)
        H.setdiag((MASS + phi) * par)
        for i, nbs in adj_l.items():
            for j in nbs:
                if i >= j: continue
                d = math.sqrt((pos_arr[j,0]-pos_arr[i,0])**2 + (pos_arr[j,1]-pos_arr[i,1])**2)
                w = 1./max(d, 0.3)
                H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
        H = H.tocsr()
        ap = (speye(n,format='csc') + 1j*H*DT/2).tocsc()
        am = speye(n,format='csr') - 1j*H*DT/2
        for _ in range(n_evolve):
            psi = spsolve(ap, am.dot(psi))
        rho = np.abs(psi)**2; rho_n = rho / np.sum(rho)
        nc = cur % 2
        parent = rng.choices(range(n), weights=rho_n, k=1)[0]
        new_pos = (pos_arr[parent,0] + 0.3*(rng.random()-0.5),
                   pos_arr[parent,1] + 0.3*(rng.random()-0.5))
        pos.append(new_pos); col.append(nc); adj[cur] = set()
        dists = [(math.sqrt((new_pos[0]-pos_arr[i,0])**2+(new_pos[1]-pos_arr[i,1])**2), i)
                 for i in range(n) if col[i] != nc]
        dists.sort()
        for _, j in dists[:min(K_CONNECT, len(dists))]:
            adj[cur].add(j); adj[j].add(cur)
        psi_new = np.zeros(cur+1, dtype=complex)
        psi_new[:n] = psi; psi_new[cur] = 0.01*psi[parent]
        psi /= np.linalg.norm(psi_new); psi = psi_new / np.linalg.norm(psi_new)
        cur += 1

    return np.array(pos), np.array(col, dtype=int), {k: list(v) for k,v in adj.items()}, psi


def _build_physics(pos, col, adj, n):
    """Build Laplacian and Hamiltonian infrastructure for a graph."""
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.sqrt((pos[j,0]-pos[i,0])**2 + (pos[j,1]-pos[i,1])**2)
            w = 1./max(d, 0.3)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.sqrt((pos[j,0]-pos[i,0])**2 + (pos[j,1]-pos[i,1])**2)
            w = 1./max(d, 0.3)
            H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j*H*dt/2).tocsc()
    am = speye(n, format='csr') - 1j*H*dt/2
    return spsolve(ap, am.dot(psi))


def _bfs_depth(adj, src, n):
    depth = np.full(n, np.inf); depth[src] = 0; q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf: depth[j] = depth[i] + 1; q.append(j)
    return depth


def force_battery(pos, col, adj, psi, G_self):
    """Three force measures on grown graph."""
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))
    src = np.argmin(dists_c)
    L = _build_physics(pos, col, adj, n)
    rho = np.abs(psi)**2
    phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)
    depth = _bfs_depth(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d <= 0:
        return {"shell_mean": 0., "shell_prob": 0., "edge_radial": 0., "robust": False}

    ps = np.zeros(max_d+1); rs = np.zeros(max_d+1); P_shell = np.zeros(max_d+1)
    cnt = np.zeros(max_d+1)
    rho_n = rho / np.sum(rho)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]; rs[d_] += rho[i]; P_shell[d_] += rho_n[i]; cnt[d_] += 1
    for d_ in range(max_d+1):
        if cnt[d_] > 0: ps[d_] /= cnt[d_]; rs[d_] /= cnt[d_]

    grad = np.zeros(max_d+1)
    for d_ in range(max_d+1):
        if d_ == 0: grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d: grad[d_] = ps[d_-1] - ps[d_]
        else: grad[d_] = 0.5*(ps[d_-1] - ps[d_+1])

    shell_mean = float(np.sum(rs * grad))
    shell_prob = float(np.sum(P_shell * grad))

    edge_radial = 0.0
    for i, nbs in adj.items():
        if not np.isfinite(depth[i]): continue
        for j in nbs:
            if j <= i or not np.isfinite(depth[j]): continue
            d_ij = math.sqrt((pos[j,0]-pos[i,0])**2 + (pos[j,1]-pos[i,1])**2)
            w = 1./max(d_ij, 0.3)
            dphi = phi[j] - phi[i]
            ri = pos[i] - pos[src]; rj = pos[j] - pos[src]
            edge_vec = pos[j] - pos[i]
            r_mid = 0.5*(ri + rj)
            r_norm = np.linalg.norm(r_mid)
            if r_norm < 1e-10: continue
            r_hat = r_mid / r_norm
            cos_theta = np.dot(edge_vec, r_hat) / max(d_ij, 1e-10)
            edge_radial += 0.5*(rho_n[i]+rho_n[j]) * w * dphi * (-cos_theta)

    robust = shell_mean > 0 and shell_prob > 0 and edge_radial > 0
    return {"shell_mean": shell_mean, "shell_prob": shell_prob,
            "edge_radial": float(edge_radial), "robust": robust}


def displacement_test(pos, col, adj, G_self, n_steps=30):
    """Graph-native directional observable: wavepacket displacement under self-gravity.

    1. Initialize a Gaussian wavepacket centered on the graph.
    2. Run n_steps of self-gravitating CN evolution (parity coupling).
    3. Measure whether the centroid moved TOWARD the density peak.

    Compare against a FREE evolution (no self-gravity) to isolate the
    gravitational contribution. Positive delta = attraction.
    """
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))

    # Initial wavepacket: Gaussian at center
    psi0 = np.exp(-0.5 * dists_c**2 / 1.0**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    L = _build_physics(pos, col, adj, n)

    def centroid(psi_):
        rho_ = np.abs(psi_)**2; rho_ /= np.sum(rho_)
        return np.array([np.sum(rho_ * pos[:,0]), np.sum(rho_ * pos[:,1])])

    def width(psi_):
        rho_ = np.abs(psi_)**2; rho_ /= np.sum(rho_)
        cx = np.sum(rho_ * pos[:,0]); cy = np.sum(rho_ * pos[:,1])
        return np.sqrt(np.sum(rho_ * ((pos[:,0]-cx)**2 + (pos[:,1]-cy)**2)))

    c0 = centroid(psi0)
    w0 = width(psi0)

    # Self-gravitating evolution
    psi_grav = psi0.copy()
    for step in range(n_steps):
        rho = np.abs(psi_grav)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_self*rho)
        H = _build_H(pos, col, adj, n, phi)
        psi_grav = _cn_step(H, psi_grav, DT)

    c_grav = centroid(psi_grav)
    w_grav = width(psi_grav)

    # Free evolution (no gravity)
    psi_free = psi0.copy()
    phi_zero = np.zeros(n)
    H_free = _build_H(pos, col, adj, n, phi_zero)
    for step in range(n_steps):
        psi_free = _cn_step(H_free, psi_free, DT)

    c_free = centroid(psi_free)
    w_free = width(psi_free)

    # The density peak is where rho is highest after self-gravity
    rho_final = np.abs(psi_grav)**2
    peak_node = np.argmax(rho_final)
    peak_pos = pos[peak_node]

    # Displacement: how much closer did the centroid get to the density peak
    # compared to the free evolution?
    dist_to_peak_grav = np.linalg.norm(c_grav - peak_pos)
    dist_to_peak_free = np.linalg.norm(c_free - peak_pos)
    delta_dist = dist_to_peak_free - dist_to_peak_grav  # positive = closer = attraction

    # Width contraction
    contraction = w_grav / w0
    free_spread = w_free / w0

    norm_grav = np.linalg.norm(psi_grav)
    norm_free = np.linalg.norm(psi_free)

    return {
        "delta_dist": delta_dist,
        "attracted": delta_dist > 0,
        "contraction": contraction,
        "free_spread": free_spread,
        "norm_grav": norm_grav,
        "norm_free": norm_free,
    }


def measure_d_eff(pos, adj, n):
    """Effective dimension from BFS shell volumes."""
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))
    src = np.argmin(dists_c)
    depth = _bfs_depth(adj, src, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    if max_d < 3:
        return float('nan'), 0.0
    shells = np.zeros(max_d + 1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            shells[d_] += 1
    cum = np.cumsum(shells)
    valid = (cum > 0) & (np.arange(max_d+1) > 0)
    if np.sum(valid) < 3:
        return float('nan'), 0.0
    r = np.arange(max_d+1)[valid].astype(float)
    v = cum[valid]
    lr = linregress(np.log(r), np.log(v))
    return lr.slope, lr.rvalue**2


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("EMERGENT GEOMETRY — MULTI-SIZE CONFIRMATION + DISPLACEMENT TEST")
    print("=" * 78)
    print(f"G=100, seeds=42-46, sizes=60,80,100,120,150")
    print()

    G = 100
    sizes = [60, 80, 100, 120, 150]
    seeds = [42, 43, 44, 45, 46]

    # ── Q1: Multi-size force battery ────────────────────────────────
    print("=" * 78)
    print("Q1: FORCE BATTERY ACROSS GRAPH SIZES (G=100)")
    print("=" * 78)
    print()

    size_results = {}
    for n_target in sizes:
        robust_count = 0
        results_n = []
        for seed in seeds:
            pos, col, adj, psi = grow_graph(n_target, G_self=G, seed=seed)
            fb = force_battery(pos, col, adj, psi, G)
            results_n.append(fb)
            if fb["robust"]:
                robust_count += 1
        size_results[n_target] = (robust_count, results_n)

        sm_avg = np.mean([r["shell_mean"] for r in results_n])
        sp_avg = np.mean([r["shell_prob"] for r in results_n])
        er_avg = np.mean([r["edge_radial"] for r in results_n])
        print(f"  n={n_target:4d}: {robust_count}/5 ROBUST_TOWARD  "
              f"sm={sm_avg:+.3e}  sp={sp_avg:+.3e}  er={er_avg:+.3e}")

    print()
    print("Size-stability summary:")
    all_robust = all(count >= 4 for count, _ in size_results.values())
    all_unanimous = all(count == 5 for count, _ in size_results.values())
    print(f"  All sizes >=4/5 robust: {'YES' if all_robust else 'NO'}")
    print(f"  All sizes  5/5 robust: {'YES' if all_unanimous else 'NO'}")

    # ── Q2: Displacement test (graph-native directional observable) ─
    print()
    print("=" * 78)
    print("Q2: WAVEPACKET DISPLACEMENT TEST (G=100)")
    print("=" * 78)
    print()
    print("Does the wavepacket centroid move TOWARD the self-generated")
    print("density peak compared to free evolution? Positive delta = attraction.")
    print()

    disp_results = {}
    for n_target in sizes:
        attracted_count = 0
        results_d = []
        for seed in seeds:
            pos, col, adj, psi = grow_graph(n_target, G_self=G, seed=seed)
            dr = displacement_test(pos, col, adj, G_self=G, n_steps=30)
            results_d.append(dr)
            if dr["attracted"]:
                attracted_count += 1
        disp_results[n_target] = (attracted_count, results_d)

        dd_avg = np.mean([r["delta_dist"] for r in results_d])
        ct_avg = np.mean([r["contraction"] for r in results_d])
        fs_avg = np.mean([r["free_spread"] for r in results_d])
        print(f"  n={n_target:4d}: {attracted_count}/5 ATTRACTED  "
              f"delta={dd_avg:+.4f}  contraction={ct_avg:.4f}  free_spread={fs_avg:.4f}  "
              f"norm={np.mean([r['norm_grav'] for r in results_d]):.6f}")

    print()
    print("Displacement summary:")
    all_attracted = all(count >= 4 for count, _ in disp_results.values())
    all_unan_disp = all(count == 5 for count, _ in disp_results.values())
    print(f"  All sizes >=4/5 attracted: {'YES' if all_attracted else 'NO'}")
    print(f"  All sizes  5/5 attracted: {'YES' if all_unan_disp else 'NO'}")

    # ── Q3: d_eff across sizes ──────────────────────────────────────
    print()
    print("=" * 78)
    print("Q3: EFFECTIVE DIMENSION ACROSS SIZES")
    print("=" * 78)
    print()

    for n_target in sizes:
        deffs = []
        for seed in seeds:
            pos, col, adj, psi = grow_graph(n_target, G_self=G, seed=seed)
            d_eff, r2 = measure_d_eff(pos, adj, len(pos))
            deffs.append(d_eff)
        print(f"  n={n_target:4d}: d_eff = {np.mean(deffs):.3f} +/- {np.std(deffs):.3f}")

    # ── Final verdict ───────────────────────────────────────────────
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    force_ok = all(count >= 4 for count, _ in size_results.values())
    disp_ok = all(count >= 4 for count, _ in disp_results.values())

    if force_ok and disp_ok:
        print("EMERGENT GEOMETRY IS SIZE-STABLE AND DYNAMICALLY ATTRACTIVE.")
        print("Both the force battery and displacement test pass across all sizes.")
        print("This is a candidate for promotion to retained status.")
    elif force_ok:
        print("Force battery passes but displacement test is unstable.")
        print("The field-shape measures agree, but the dynamical response is noisy.")
    elif disp_ok:
        print("Displacement test passes but force battery is unstable.")
        print("The dynamical response is attractive, but proxy measures disagree.")
    else:
        print("Neither test is size-stable. Emergent geometry remains exploratory.")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
