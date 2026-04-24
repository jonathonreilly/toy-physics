#!/usr/bin/env python3
"""
Shapiro Delay on Graphs — Mass-Gap Time Dilation
==================================================
Under parity coupling H = (m + Φ)·ε(x), positive Φ widens the mass gap.
Wider gap → smaller group velocity → probability wavefront arrives later
at distant nodes. This is the graph analog of gravitational time dilation
(Shapiro delay).

Protocol:
1. Build graph with an external gravitational source at one side
2. Initialize a sharp wavepacket on the opposite side
3. Measure time-to-threshold at nodes near the source
4. Compare with and without the source (free propagation)
5. Repeat with inverted Φ (−Φ should SPEED UP propagation)

Sign-selective if: +Φ delays arrival AND −Φ accelerates arrival.
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from collections import deque

MASS = 0.30
MU2 = 0.22
DT = 0.05  # smaller dt for time-resolution
G_EXT = 15.0
N_STEPS = 200  # enough for wavefront to traverse graph
THRESHOLD = 1e-4  # probability threshold for "arrival"


def _ae(adj, a, b):
    adj.setdefault(a, set()).add(b)
    adj.setdefault(b, set()).add(a)


def make_random_geometric(seed=42, side=10):
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08*(rng.random()-0.5), y + 0.08*(rng.random()-0.5)))
            colors.append((x+y) % 2); index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1)):
                ii,jj = i+di, j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a] == col[b]: continue
                _ae(adj, a, b)
    return "random_geometric", pos, col, {k:list(v) for k,v in adj.items()}


def make_layered(seed=42, layers=12, width=6):
    rng = random.Random(seed)
    coords, colors, layer_nodes = [], [], []; idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            coords.append((float(layer), float(k)+0.05*(rng.random()-0.5)))
            colors.append(layer%2); this_layer.append(idx); idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords); col = np.array(colors, dtype=int); n = len(pos)
    adj = {i: set() for i in range(n)}
    for layer in range(layers-1):
        curr = layer_nodes[layer]; nxt = layer_nodes[layer+1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos%len(nxt)]; adj[i].add(j1); adj[j1].add(i)
            j2 = nxt[(i_pos+1)%len(nxt)]
            if j2 != j1: adj[i].add(j2); adj[j2].add(i)
    return "layered", pos, col, {k:list(v) for k,v in adj.items()}, layer_nodes


def _min_image_hypot(pos, i, j):
    """Minimum-image Euclidean distance between sites i and j.

    Detects per-axis period from the extent of pos; applies
    min(|d|, period - |d|) when period > 1. Collapses to raw hypot on axes
    with only one distinct coordinate, so it is safe for 1D/2D/open and
    periodic configurations alike. Fixes the 2026-04-11 wraparound bug on
    the 1D periodic ring path (run_shapiro("1d_lattice", ...)).
    """
    dsq = 0.0
    for ax in range(pos.shape[1]):
        lo = int(round(float(pos[:, ax].min())))
        hi = int(round(float(pos[:, ax].max())))
        period = hi - lo + 1
        d = abs(pos[j, ax] - pos[i, ax])
        if period > 1:
            d = min(d, period - d)
        dsq += d * d
    return math.sqrt(dsq)


def _build_L(pos, adj, n):
    L = lil_matrix((n,n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = _min_image_hypot(pos, i, j)
            w = 1./max(d, 0.5); L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()


def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = _min_image_hypot(pos, i, j)
            w = 1./max(d, 0.5); H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
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


def run_shapiro(name, pos, col, adj, start_nodes, detect_nodes, source_node):
    """Measure arrival time at detector nodes with +Φ, −Φ, and free."""
    n = len(pos)
    L = _build_L(pos, adj, n)

    # External potential from source
    rho_ext = np.zeros(n); rho_ext[source_node] = 1.0
    phi_ext = spsolve((L + MU2*speye(n,format='csr')).tocsc(), G_EXT * rho_ext)

    # Initial wavepacket: localized at start nodes
    psi0 = np.zeros(n, dtype=complex)
    for s in start_nodes:
        psi0[s] = 1.0
    psi0 /= np.linalg.norm(psi0)

    results = {}
    for label, phi in [("attract", phi_ext), ("repulse", -phi_ext), ("free", np.zeros(n))]:
        H = _build_H(pos, col, adj, n, phi)
        psi = psi0.copy()

        # Track arrival at detector nodes
        arrival_times = {d: None for d in detect_nodes}
        total_prob_history = []

        for step in range(N_STEPS):
            psi = _cn_step(H, psi, DT)
            rho = np.abs(psi)**2

            # Cumulative probability at detector
            det_prob = sum(rho[d] for d in detect_nodes)
            total_prob_history.append(det_prob)

            # Record first time threshold is crossed
            for d in detect_nodes:
                if arrival_times[d] is None and rho[d] > THRESHOLD:
                    arrival_times[d] = step

        # Mean arrival time across detector nodes
        arrived = [t for t in arrival_times.values() if t is not None]
        mean_arrival = np.mean(arrived) if arrived else N_STEPS
        frac_arrived = len(arrived) / len(detect_nodes)

        # Half-max time: when does cumulative probability at detector reach half its max?
        prob_arr = np.array(total_prob_history)
        half_max = 0.5 * np.max(prob_arr) if np.max(prob_arr) > 0 else 0
        half_max_time = N_STEPS
        for step, p in enumerate(prob_arr):
            if p >= half_max:
                half_max_time = step
                break

        results[label] = {
            "mean_arrival": mean_arrival,
            "half_max_time": half_max_time,
            "frac_arrived": frac_arrived,
            "max_det_prob": float(np.max(prob_arr)),
            "norm": np.linalg.norm(psi),
        }

    # Shapiro delay: attract should arrive LATER than free, repulse EARLIER
    delay_attract = results["attract"]["half_max_time"] - results["free"]["half_max_time"]
    delay_repulse = results["repulse"]["half_max_time"] - results["free"]["half_max_time"]

    # Sign-selective: +Φ delays (>0), −Φ accelerates (<0)
    sign_selective = delay_attract > 0 and delay_repulse < 0

    return {
        "name": name,
        "t_attract": results["attract"]["half_max_time"],
        "t_repulse": results["repulse"]["half_max_time"],
        "t_free": results["free"]["half_max_time"],
        "delay_attract": delay_attract,
        "delay_repulse": delay_repulse,
        "sign_selective": sign_selective,
        "frac_a": results["attract"]["frac_arrived"],
        "frac_r": results["repulse"]["frac_arrived"],
        "norm_a": results["attract"]["norm"],
        "norm_r": results["repulse"]["norm"],
    }


if __name__ == '__main__':
    t0 = time.time()
    print("=" * 78)
    print("SHAPIRO DELAY ON GRAPHS — MASS-GAP TIME DILATION")
    print("=" * 78)
    print(f"G_EXT={G_EXT}, DT={DT}, N_STEPS={N_STEPS}, THRESHOLD={THRESHOLD}")
    print(f"+Φ widens mass gap → slower propagation → delayed arrival")
    print(f"−Φ narrows mass gap → faster propagation → early arrival")
    print()

    # ── Test 1: Layered graph (cleanest geometry) ───────────────────
    print("--- LAYERED GRAPH (12 layers × 6 width) ---")
    print("Source at middle layer, wavepacket starts at layer 0, detect at last layer")
    print()

    for seed in [42, 43, 44]:
        name, pos, col, adj, layer_nodes = make_layered(seed=seed, layers=12, width=6)
        n = len(pos)

        start_nodes = layer_nodes[0]  # first layer
        detect_nodes = layer_nodes[-1]  # last layer
        source_node = layer_nodes[6][3]  # middle layer, middle node

        r = run_shapiro(name, pos, col, adj, start_nodes, detect_nodes, source_node)
        print(f"  seed={seed}: t_free={r['t_free']:3d}  t_attract={r['t_attract']:3d} (Δ={r['delay_attract']:+3d})  "
              f"t_repulse={r['t_repulse']:3d} (Δ={r['delay_repulse']:+3d})  "
              f"{'SIGN-SEL' if r['sign_selective'] else 'no':>8s}  norm={r['norm_a']:.6f}")

    # ── Test 2: Random geometric ────────────────────────────────────
    print()
    print("--- RANDOM GEOMETRIC (10×10) ---")
    print("Source at center, wavepacket starts at corner, detect at opposite corner")
    print()

    for seed in [42, 43, 44]:
        name, pos, col, adj = make_random_geometric(seed=seed, side=10)
        n = len(pos)

        # Start: nodes near (0,0)
        dists_start = np.sqrt(pos[:,0]**2 + pos[:,1]**2)
        start_nodes = list(np.argsort(dists_start)[:5])

        # Detect: nodes near (9,9)
        dists_detect = np.sqrt((pos[:,0]-9)**2 + (pos[:,1]-9)**2)
        detect_nodes = list(np.argsort(dists_detect)[:5])

        # Source: node nearest center
        dists_center = np.sqrt((pos[:,0]-4.5)**2 + (pos[:,1]-4.5)**2)
        source_node = int(np.argmin(dists_center))

        r = run_shapiro(name, pos, col, adj, start_nodes, detect_nodes, source_node)
        print(f"  seed={seed}: t_free={r['t_free']:3d}  t_attract={r['t_attract']:3d} (Δ={r['delay_attract']:+3d})  "
              f"t_repulse={r['t_repulse']:3d} (Δ={r['delay_repulse']:+3d})  "
              f"{'SIGN-SEL' if r['sign_selective'] else 'no':>8s}  norm={r['norm_a']:.6f}")

    # ── Test 3: 1D lattice reference (should show clean delay) ─────
    print()
    print("--- 1D LATTICE REFERENCE (n=61) ---")
    print("Source at center, wavepacket starts at left end, detect at right end")
    print()

    n = 61; c = n//2
    pos_1d = np.array([(float(x), 0.0) for x in range(n)])
    col_1d = np.array([x%2 for x in range(n)], dtype=int)
    adj_1d = {x: [((x+1)%n), ((x-1)%n)] for x in range(n)}

    start_nodes_1d = [0, 1, 2]
    detect_nodes_1d = [n-3, n-2, n-1]
    source_1d = c

    r = run_shapiro("1d_lattice", pos_1d, col_1d, adj_1d, start_nodes_1d, detect_nodes_1d, source_1d)
    print(f"  1D ref: t_free={r['t_free']:3d}  t_attract={r['t_attract']:3d} (Δ={r['delay_attract']:+3d})  "
          f"t_repulse={r['t_repulse']:3d} (Δ={r['delay_repulse']:+3d})  "
          f"{'SIGN-SEL' if r['sign_selective'] else 'no':>8s}  norm={r['norm_a']:.6f}")

    print(f"\nTotal time: {time.time()-t0:.1f}s")
