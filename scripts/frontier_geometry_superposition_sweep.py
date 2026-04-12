#!/usr/bin/env python3
"""
Geometry Superposition Sweep
=============================
Comprehensive parameter sweep extending the geometry superposition result
(TV=0.37 on 2D side=8 G=10) across:

1. G sweep on 2D lattice (side=8): G = 0.5, 1, 2, 5, 10, 20, 50
2. Size sweep on 2D lattice (G=5): side = 6, 8, 10, 12, 14
3. Irregular graph families (G=5 and G=10):
   - Random geometric, Growing, Layered cycle
4. Multiple source positions on 2D lattice (side=10, G=5)

TV > 0: geometries produce distinguishable detector states
dphi > 0: real phase difference (gravitational phase shift)
TV_quantum > 0: quantum superposition differs from classical mixture
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
N_STEPS = 30


# ---------------------------------------------------------------------------
# Graph builders
# ---------------------------------------------------------------------------

def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_lattice_2d(side):
    coords, colors, adj = [], [], {}
    idx = 0; index = {}
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]; adj[a] = []
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                adj[a].append(index[((x + dx) % side, (y + dy) % side)])
    return pos, col, adj


def make_random_geometric(seed=42, side=8):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}; idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5),
                           y + 0.08 * (rng.random() - 0.5)))
            colors.append((x + y) % 2); index[(x, y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index:
                    continue
                b = index[(ii, jj)]
                if col[a] == col[b]:
                    continue
                if math.hypot(pos[b, 0] - pos[a, 0], pos[b, 1] - pos[a, 1]) <= 1.28:
                    _ae(adj, a, b)
    return pos, col, {k: list(v) for k, v in adj.items()}


def make_growing(seed=42, n_target=64):
    rng = random.Random(seed)
    coords = [(0., 0.), (1., 0.)]; colors = [0, 1]
    adj = {0: {1}, 1: {0}}; cur = 2
    while cur < n_target:
        px = rng.uniform(-3, 3); py = rng.uniform(-3, 3); nc = cur % 2
        coords.append((px, py)); colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = [(math.hypot(px - coords[i][0], py - coords[i][1]), i) for i in opp]
            ds.sort()
            for _, j in ds[:min(4, len(ds))]:
                _ae(adj, cur, j)
        cur += 1
    return np.array(coords), np.array(colors, dtype=int), {k: list(v) for k, v in adj.items()}


def make_layered_cycle(seed=42, layers=8, width=8):
    rng = random.Random(seed)
    coords, colors, layer_nodes = [], [], []; idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            coords.append((float(layer), float(k) + 0.05 * (rng.random() - 0.5)))
            colors.append(layer % 2); this_layer.append(idx); idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords); col = np.array(colors, dtype=int); n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]; nxt = layer_nodes[layer + 1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos % len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2 = nxt[(i_pos + 1) % len(nxt)]
            if j2 != j1:
                adj[i].add(j2); adj[j2].add(i)
    return pos, col, {k: list(v) for k, v in adj.items()}


# ---------------------------------------------------------------------------
# Physics primitives
# ---------------------------------------------------------------------------

def _build_L(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1. / max(d, 0.5)
            L[i, j] -= w; L[j, i] -= w; L[i, i] += w; L[j, j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1. / max(d, 0.5)
            H[i, j] += -0.5j * w; H[j, i] += 0.5j * w
    return H.tocsr()


def _cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def _bfs_depth(adj, start, n):
    """BFS depth from start node. Returns depth array."""
    depth = np.full(n, -1, dtype=int)
    depth[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj.get(u, []):
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                queue.append(v)
    return depth


def run_geometry_test(pos, col, adj, n, G, source_idx, detector_indices):
    """Run geometry superposition test on arbitrary graph.

    Returns dict with TV, dphi, TVq, overlap.
    """
    L = _build_L(pos, adj, n)
    rho_ext = np.zeros(n); rho_ext[source_idx] = G
    phi_B = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), rho_ext)

    # Initial state: Gaussian centered on graph center
    center = np.mean(pos, axis=0)
    dists = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    psi0 = np.exp(-0.5 * dists ** 2 / 1.5 ** 2).astype(complex)
    psi0 /= np.linalg.norm(psi0)

    # Evolve on flat (A) and curved (B)
    H_A = _build_H(pos, col, adj, n, np.zeros(n))
    psi_A = psi0.copy()
    for _ in range(N_STEPS):
        psi_A = _cn_step(H_A, psi_A, DT)

    H_B = _build_H(pos, col, adj, n, phi_B)
    psi_B = psi0.copy()
    for _ in range(N_STEPS):
        psi_B = _cn_step(H_B, psi_B, DT)

    det = detector_indices

    # TV distance at detector
    rA = np.abs(psi_A[det]) ** 2; rB = np.abs(psi_B[det]) ** 2
    PA = rA / max(np.sum(rA), 1e-20); PB = rB / max(np.sum(rB), 1e-20)
    TV = 0.5 * np.sum(np.abs(PA - PB))

    # Phase difference
    mask = (np.abs(psi_A[det]) > 1e-10) & (np.abs(psi_B[det]) > 1e-10)
    dphi = (np.mean(np.abs(np.angle(psi_A[det][mask]) - np.angle(psi_B[det][mask])))
            if np.sum(mask) > 0 else 0.0)

    # Quantum vs classical
    psi_s = (psi_A + psi_B); psi_s /= np.linalg.norm(psi_s)
    rmix = 0.5 * (np.abs(psi_A) ** 2 + np.abs(psi_B) ** 2)
    rsup = np.abs(psi_s) ** 2
    Pm = rmix[det] / max(np.sum(rmix[det]), 1e-20)
    Ps = rsup[det] / max(np.sum(rsup[det]), 1e-20)
    TVq = 0.5 * np.sum(np.abs(Ps - Pm))

    overlap = np.abs(np.conj(psi_A) @ psi_B) ** 2
    return {"TV": TV, "dphi": dphi, "TVq": TVq, "overlap": overlap}


# ---------------------------------------------------------------------------
# Sweep helpers
# ---------------------------------------------------------------------------

def run_2d_lattice(side, G, source_idx=None):
    """Run on 2D periodic lattice. Default source at n//4."""
    pos, col, adj = make_lattice_2d(side)
    n = side * side
    if source_idx is None:
        source_idx = n // 4
    det = list(range(3 * n // 4, n))
    return run_geometry_test(pos, col, adj, n, G, source_idx, det)


def run_irregular(builder_fn, G, **kwargs):
    """Run on irregular graph. Source = farthest from center, detector = far half."""
    pos, col, adj = builder_fn(**kwargs)
    n = len(pos)
    center = np.mean(pos, axis=0)
    dists_to_center = np.sqrt(np.sum((pos - center) ** 2, axis=1))
    source_idx = int(np.argmax(dists_to_center))

    # BFS depth from center node
    center_node = int(np.argmin(dists_to_center))
    depth = _bfs_depth(adj, center_node, n)
    max_depth = int(np.max(depth[depth >= 0]))
    det = [i for i in range(n) if depth[i] > max_depth // 2]
    if len(det) < 2:
        det = list(range(n // 2, n))

    return run_geometry_test(pos, col, adj, n, G, source_idx, det)


def print_row(label, r):
    print(f"  {label:<35s}  TV={r['TV']:.4f}  dphi={r['dphi']:.3f}  "
          f"TVq={r['TVq']:.4f}  overlap={r['overlap']:.4f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("GEOMETRY SUPERPOSITION SWEEP")
    print("=" * 78)
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")

    # ---- Sweep 1: G sweep on 2D lattice side=8 ----
    print("\n" + "-" * 78)
    print("SWEEP 1: G sweep on 2D lattice (side=8)")
    print("-" * 78)
    g_values = [0.5, 1, 2, 5, 10, 20, 50]
    for G in g_values:
        r = run_2d_lattice(8, G)
        print_row(f"side=8  G={G:<5.1f}", r)

    # ---- Sweep 2: Size sweep on 2D lattice G=5 ----
    print("\n" + "-" * 78)
    print("SWEEP 2: Size sweep on 2D lattice (G=5)")
    print("-" * 78)
    for side in [6, 8, 10, 12, 14]:
        r = run_2d_lattice(side, 5.0)
        print_row(f"side={side:<3d} G=5", r)

    # ---- Sweep 3: Irregular graph families ----
    print("\n" + "-" * 78)
    print("SWEEP 3: Irregular graph families")
    print("-" * 78)
    for G in [5.0, 10.0]:
        print(f"\n  G = {G:.1f}:")
        for seed in [42, 43, 44]:
            r = run_irregular(make_random_geometric, G, seed=seed, side=8)
            print_row(f"  random_geometric seed={seed}", r)
        for seed in [42, 43, 44]:
            r = run_irregular(make_growing, G, seed=seed, n_target=64)
            print_row(f"  growing n=64 seed={seed}", r)
        for seed in [42, 43, 44]:
            r = run_irregular(make_layered_cycle, G, seed=seed, layers=8, width=8)
            print_row(f"  layered_cycle 8x8 seed={seed}", r)

    # ---- Sweep 4: Source position on 2D lattice ----
    print("\n" + "-" * 78)
    print("SWEEP 4: Source position sweep (side=10, G=5)")
    print("-" * 78)
    side = 10
    positions = {"(2,5)": 2 * side + 5, "(5,2)": 5 * side + 2,
                 "(5,5)": 5 * side + 5, "(7,5)": 7 * side + 5}
    for label, src in positions.items():
        pos, col, adj = make_lattice_2d(side)
        n = side * side
        det = list(range(3 * n // 4, n))
        r = run_geometry_test(pos, col, adj, n, 5.0, src, det)
        print_row(f"source={label}", r)

    # ---- Summary ----
    elapsed = time.time() - t0
    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("TV:      geometry distinguishability (0=identical, 1=orthogonal)")
    print("dphi:    mean phase difference at detector (gravitational phase shift)")
    print("TVq:     quantum superposition vs classical mixture distinguishability")
    print("overlap: state fidelity |<psi_A|psi_B>|^2")
    print(f"\nTotal time: {elapsed:.1f}s")
