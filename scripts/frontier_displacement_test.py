#!/usr/bin/env python3
"""
Wavepacket Displacement Test on Fixed Admissible Graph Families
================================================================
Graph-native directional observable: does the wavepacket centroid move
TOWARD the external source under self-gravity, compared to free evolution?

This is the dynamical response test that shell/edge-radial proxies fail
to provide. If it works on fixed graphs, it closes the "no graph-native
directional observable" blocker for the existing batteries.

Tests:
  D1: External-source displacement (source at one end, wavepacket at center)
      - Evolve under parity-coupled gravity: does centroid shift toward source?
      - Compare against free evolution (Phi=0)
      - TOWARD if centroid-to-source distance decreases more than free
  D2: Self-gravity contraction (no external source)
      - Evolve under self-gravity: does wavepacket width decrease?
      - Compare against free evolution
      - CONTRACT if width ratio (grav/free) < 1
  D3: Sign test — run with +Phi (standard) and -Phi (inverted)
      - If parity coupling is sign-selective, +Phi should attract, -Phi repel
      - This is the graph-native analog of the exact-lattice well/hill test

Graph families: random geometric, growing, layered cycle (all bipartite).
Multiple seeds per family.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.12
G_EXT = 8.0
G_SELF = 50.0
N_STEPS = 40


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08*(rng.random()-0.5), y + 0.08*(rng.random()-0.5)))
            colors.append((x+y) % 2)
            index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj = i+di, j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a] == col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0], pos[b,1]-pos[a,1]) <= 1.28:
                    _ae(adj, a, b)
    return "random_geometric", pos, col, {k: list(v) for k,v in adj.items()}


def make_growing(seed=42, n_target=64):
    rng = random.Random(seed)
    coords = [(0.0,0.0),(1.0,0.0)]; colors = [0,1]
    adj = {0: {1}, 1: {0}}; cur = 2
    while cur < n_target:
        px = rng.uniform(-3,3); py = rng.uniform(-3,3); nc = cur%2
        coords.append((px,py)); colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = [(math.hypot(px-coords[i][0],py-coords[i][1]),i) for i in opp]
            ds.sort()
            for _,j in ds[:min(4,len(ds))]: _ae(adj, cur, j)
        cur += 1
    return "growing", np.array(coords), np.array(colors,dtype=int), {k:list(v) for k,v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
    rng = random.Random(seed)
    coords, colors, layer_nodes = [], [], []; idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            coords.append((float(layer), float(k)+0.05*(rng.random()-0.5)))
            colors.append(layer % 2)
            this_layer.append(idx); idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords); col = np.array(colors,dtype=int); n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers-1):
        curr = layer_nodes[layer]; nxt = layer_nodes[layer+1]
        for i_pos,i in enumerate(curr):
            j1 = nxt[i_pos % len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2 = nxt[(i_pos+1) % len(nxt)]
            if j2 != j1: adj[i].add(j2); adj[j2].add(i)
    return "layered_cycle", pos, col, {k:list(v) for k,v in adj.items()}


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5)
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
            if depth[j] == np.inf: depth[j] = depth[i]+1; q.append(j)
    return depth


def _centroid(psi, pos):
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    return np.array([np.sum(rho*pos[:,0]), np.sum(rho*pos[:,1])])


def _width(psi, pos):
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    cx = np.sum(rho*pos[:,0]); cy = np.sum(rho*pos[:,1])
    return np.sqrt(np.sum(rho*((pos[:,0]-cx)**2 + (pos[:,1]-cy)**2)))


def run_displacement(name, pos, col, adj):
    """D1: External-source displacement test.

    Place source at one corner, wavepacket at center. Evolve with and without
    gravity. Measure whether gravity pulls the centroid toward the source.
    """
    n = len(pos)
    L = _build_L(pos, adj, n)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))

    # Source: node farthest from center (one corner)
    src = np.argmax(dists_c)
    src_pos = pos[src]

    # External potential from source
    rho_ext = np.zeros(n); rho_ext[src] = 1.0
    phi_ext = spsolve((L + MU2*speye(n, format='csr')).tocsc(), G_EXT * rho_ext)

    # Initial wavepacket at center
    psi0 = np.exp(-0.5 * dists_c**2 / 1.2**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    c0 = _centroid(psi0, pos)
    d0_to_src = np.linalg.norm(c0 - src_pos)

    # Gravitating evolution
    H_grav = _build_H(pos, col, adj, n, phi_ext)
    psi_grav = psi0.copy()
    for _ in range(N_STEPS):
        psi_grav = _cn_step(H_grav, psi_grav, DT)
    c_grav = _centroid(psi_grav, pos)
    d_grav = np.linalg.norm(c_grav - src_pos)

    # Free evolution
    H_free = _build_H(pos, col, adj, n, np.zeros(n))
    psi_free = psi0.copy()
    for _ in range(N_STEPS):
        psi_free = _cn_step(H_free, psi_free, DT)
    c_free = _centroid(psi_free, pos)
    d_free = np.linalg.norm(c_free - src_pos)

    # delta > 0 means gravity brought centroid closer to source than free
    delta = d_free - d_grav
    toward = delta > 0

    return {
        "delta": delta,
        "toward": toward,
        "d0": d0_to_src,
        "d_grav": d_grav,
        "d_free": d_free,
        "norm": np.linalg.norm(psi_grav),
    }


def run_self_gravity_contraction(name, pos, col, adj):
    """D2: Self-gravity contraction test."""
    n = len(pos)
    L = _build_L(pos, adj, n)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))

    psi0 = np.exp(-0.5 * dists_c**2 / 1.2**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)
    w0 = _width(psi0, pos)

    # Self-gravitating
    psi_grav = psi0.copy()
    for _ in range(N_STEPS):
        rho = np.abs(psi_grav)**2
        phi = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_SELF*rho)
        H = _build_H(pos, col, adj, n, phi)
        psi_grav = _cn_step(H, psi_grav, DT)

    # Free
    psi_free = psi0.copy()
    H_free = _build_H(pos, col, adj, n, np.zeros(n))
    for _ in range(N_STEPS):
        psi_free = _cn_step(H_free, psi_free, DT)

    w_grav = _width(psi_grav, pos)
    w_free = _width(psi_free, pos)

    return {
        "w_grav_ratio": w_grav / w0,
        "w_free_ratio": w_free / w0,
        "relative_contraction": w_grav / w_free,
        "contracts": w_grav < w_free,
        "norm": np.linalg.norm(psi_grav),
    }


def run_sign_test(name, pos, col, adj):
    """D3: Sign test — +Phi vs -Phi under parity coupling.

    If sign-selective: +Phi should attract (centroid toward source),
    -Phi should repel (centroid away from source).
    """
    n = len(pos)
    L = _build_L(pos, adj, n)
    center = np.mean(pos, axis=0)
    dists_c = np.sqrt(np.sum((pos - center)**2, axis=1))
    src = np.argmax(dists_c)
    src_pos = pos[src]

    rho_ext = np.zeros(n); rho_ext[src] = 1.0
    phi_pos = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_EXT * rho_ext)
    phi_neg = -phi_pos

    psi0 = np.exp(-0.5 * dists_c**2 / 1.2**2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    results = {}
    for label, phi in [("positive", phi_pos), ("negative", phi_neg)]:
        H = _build_H(pos, col, adj, n, phi)
        psi = psi0.copy()
        for _ in range(N_STEPS):
            psi = _cn_step(H, psi, DT)
        c = _centroid(psi, pos)
        d_to_src = np.linalg.norm(c - src_pos)
        results[label] = d_to_src

    # Free baseline
    H_free = _build_H(pos, col, adj, n, np.zeros(n))
    psi_free = psi0.copy()
    for _ in range(N_STEPS):
        psi_free = _cn_step(H_free, psi_free, DT)
    d_free = np.linalg.norm(_centroid(psi_free, pos) - src_pos)

    delta_pos = d_free - results["positive"]  # >0 = attracted
    delta_neg = d_free - results["negative"]  # <0 = repelled

    sign_selective = delta_pos > 0 and delta_neg < 0
    return {
        "delta_pos": delta_pos,
        "delta_neg": delta_neg,
        "sign_selective": sign_selective,
        "d_free": d_free,
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("WAVEPACKET DISPLACEMENT TEST ON FIXED ADMISSIBLE GRAPHS")
    print("=" * 78)
    print(f"G_ext={G_EXT}, G_self={G_SELF}, N_steps={N_STEPS}, DT={DT}")
    print()

    families = [
        make_random_geometric(seed=42, side=8),
        make_growing(seed=42, n_target=64),
        make_layered_cycle(seed=42, layers=8, width=8),
    ]

    seeds_rg = [make_random_geometric(seed=s, side=8) for s in [42,43,44]]
    seeds_gr = [make_growing(seed=s, n_target=64) for s in [42,43,44]]
    seeds_lc = [make_layered_cycle(seed=s, layers=8, width=8) for s in [42,43,44]]

    all_families = [
        ("random_geometric", seeds_rg),
        ("growing", seeds_gr),
        ("layered_cycle", seeds_lc),
    ]

    # ── D1: External-source displacement ────────────────────────────
    print("=" * 78)
    print("D1: EXTERNAL-SOURCE DISPLACEMENT")
    print("=" * 78)
    print(f"{'family':<20s} {'seed':>5s} {'delta':>10s} {'d_grav':>8s} {'d_free':>8s} {'toward':>8s} {'norm':>10s}")
    print("-" * 75)

    d1_results = {}
    for fam_name, fam_seeds in all_families:
        tw_count = 0
        for fname, pos, col, adj in fam_seeds:
            r = run_displacement(fname, pos, col, adj)
            tw_count += int(r["toward"])
            print(f"{fname:<20s} {'':>5s} {r['delta']:+10.4f} {r['d_grav']:8.4f} {r['d_free']:8.4f} "
                  f"{'TOWARD' if r['toward'] else 'AWAY':>8s} {r['norm']:10.6f}")
        d1_results[fam_name] = tw_count
        print(f"  → {fam_name}: {tw_count}/3 TOWARD")
        print()

    # ── D2: Self-gravity contraction ────────────────────────────────
    print("=" * 78)
    print("D2: SELF-GRAVITY CONTRACTION (vs free evolution)")
    print("=" * 78)
    print(f"{'family':<20s} {'w_grav':>8s} {'w_free':>8s} {'grav/free':>10s} {'contracts':>10s} {'norm':>10s}")
    print("-" * 75)

    d2_results = {}
    for fam_name, fam_seeds in all_families:
        ct_count = 0
        for fname, pos, col, adj in fam_seeds:
            r = run_self_gravity_contraction(fname, pos, col, adj)
            ct_count += int(r["contracts"])
            print(f"{fname:<20s} {r['w_grav_ratio']:8.4f} {r['w_free_ratio']:8.4f} "
                  f"{r['relative_contraction']:10.4f} "
                  f"{'CONTRACT' if r['contracts'] else 'EXPAND':>10s} {r['norm']:10.6f}")
        d2_results[fam_name] = ct_count
        print(f"  → {fam_name}: {ct_count}/3 CONTRACT")
        print()

    # ── D3: Sign test (+Phi vs -Phi) ───────────────────────────────
    print("=" * 78)
    print("D3: SIGN TEST (+Phi vs -Phi)")
    print("=" * 78)
    print(f"{'family':<20s} {'delta_pos':>10s} {'delta_neg':>10s} {'selective':>10s}")
    print("-" * 60)

    d3_results = {}
    for fam_name, fam_seeds in all_families:
        sel_count = 0
        for fname, pos, col, adj in fam_seeds:
            r = run_sign_test(fname, pos, col, adj)
            sel_count += int(r["sign_selective"])
            print(f"{fname:<20s} {r['delta_pos']:+10.4f} {r['delta_neg']:+10.4f} "
                  f"{'YES' if r['sign_selective'] else 'NO':>10s}")
        d3_results[fam_name] = sel_count
        print(f"  → {fam_name}: {sel_count}/3 sign-selective")
        print()

    # ── Verdict ─────────────────────────────────────────────────────
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    print("D1 External displacement:")
    for fam, count in d1_results.items():
        print(f"  {fam}: {count}/3 TOWARD")

    print("D2 Self-gravity contraction:")
    for fam, count in d2_results.items():
        print(f"  {fam}: {count}/3 CONTRACT")

    print("D3 Sign selection (+Phi vs -Phi):")
    for fam, count in d3_results.items():
        print(f"  {fam}: {count}/3 sign-selective")

    d1_pass = all(c >= 2 for c in d1_results.values())
    d2_pass = all(c >= 2 for c in d2_results.values())
    d3_pass = all(c >= 2 for c in d3_results.values())

    print()
    if d1_pass and d2_pass and d3_pass:
        print("ALL THREE TESTS PASS on fixed admissible graph families.")
        print("The graph-native directional observable blocker is CLOSED.")
    elif d3_pass:
        print("Sign test passes — parity coupling is sign-selective on irregular graphs.")
        if d2_pass:
            print("Self-gravity contraction also passes.")
        if not d1_pass:
            print("External displacement is noisy — needs stronger source or more steps.")
    else:
        print("Sign test does NOT pass cleanly on irregular graphs.")
        print("The graph-native directional observable blocker remains OPEN.")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
