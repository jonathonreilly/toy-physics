#!/usr/bin/env python3
"""Quantum Zeno effect from self-gravity on a 2D periodic lattice.

Tests whether strong gravitational self-coupling freezes wavepacket
spreading (Zeno localization):
  - Weak G: width grows (quantum spreading)
  - Strong G: width freezes or shrinks (Zeno localization)
  - Find critical G_Zeno where transition occurs

Additional checks:
  1. Geodesic tracking: at critical G, does the localized packet
     centroid sit at a graph geodesic?
  2. Finite-size scaling: does G_Zeno depend on lattice size?
     (side=6,8,10,12 -> if G_Zeno ~ const, it's physical)
  3. Topology dependence: test on random geometric graph (side=8)

PStack experiment: quantum-zeno-self-gravity
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.spatial import Delaunay

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 60
SIGMA = 1.5           # narrow Gaussian (lattice units)

G_VALUES = [0, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
SIZE_SCAN = [6, 8, 10, 12]


# ---------------------------------------------------------------------------
# 2D periodic lattice
# ---------------------------------------------------------------------------
def make_2d_periodic_lattice(side: int):
    """Build a 2D periodic square lattice.

    Returns:
        pos: (n, 2) array of positions
        col: (n,) array of checkerboard coloring (0 or 1)
        L: (n, n) sparse Laplacian
        adj: list of neighbor lists
    """
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

    # Build adjacency and Laplacian
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
    return pos, col, L, adj, n


def make_random_geometric_graph(side: int, seed: int = 42):
    """Build a random geometric graph in a periodic box.

    Places side^2 points uniformly, connects via Delaunay triangulation.
    Returns same format as make_2d_periodic_lattice.
    """
    rng = np.random.RandomState(seed)
    n = side * side
    pos = rng.uniform(0, side, size=(n, 2))

    # Checkerboard coloring based on position
    col = np.array([(int(pos[i, 0]) + int(pos[i, 1])) % 2 for i in range(n)])

    # Delaunay triangulation for connectivity
    tri = Delaunay(pos)
    adj = [set() for _ in range(n)]
    for simplex in tri.simplices:
        for a in simplex:
            for b in simplex:
                if a != b:
                    adj[a].add(b)
                    adj[b].add(a)
    adj = [list(s) for s in adj]

    # Build Laplacian
    rows, cols_sp, vals = [], [], []
    for i in range(n):
        deg = len(adj[i])
        rows.append(i); cols_sp.append(i); vals.append(-float(deg))
        for j in adj[i]:
            rows.append(i); cols_sp.append(j); vals.append(1.0)

    L = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n))
    return pos, col, L, adj, n


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
def solve_phi(rho, L, mu2, G, n):
    """Screened Poisson: (L + mu^2 I) phi = G * rho."""
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G * rho)


def make_hamiltonian_2d(phi, col, adj, n):
    """2D staggered Hamiltonian with parity coupling.

    H[i,i] = (MASS + phi[i]) * par[i]   where par = +1 (even) / -1 (odd)
    H[i,j] = -i/2 for neighbors (antisymmetric hopping)
    """
    par = np.where(col == 0, 1.0, -1.0)
    diag = (MASS + phi) * par

    rows, cols_sp, vals = [], [], []
    for i in range(n):
        rows.append(i); cols_sp.append(i); vals.append(diag[i])
        for j in adj[i]:
            # Antisymmetric hopping: sign from parity structure
            if j > i:
                rows.append(i); cols_sp.append(j); vals.append(-0.5j)
                rows.append(j); cols_sp.append(i); vals.append(0.5j)

    H = sparse.csc_matrix((vals, (rows, cols_sp)), shape=(n, n), dtype=complex)
    return H


def cn_step(psi, H, dt, n):
    """Crank-Nicolson step: (I + iHdt/2) psi_new = (I - iHdt/2) psi_old."""
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    rhs = A_minus.dot(psi)
    return spsolve(A_plus, rhs)


# ---------------------------------------------------------------------------
# Wavepacket utilities
# ---------------------------------------------------------------------------
def gaussian_2d(pos, center, sigma, n):
    """Normalized 2D Gaussian centered at 'center'."""
    dx = pos[:, 0] - center[0]
    dy = pos[:, 1] - center[1]
    psi = np.exp(-0.5 * (dx**2 + dy**2) / sigma**2)
    psi = psi.astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi


def width(psi, pos):
    """RMS width of wavepacket."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dx = pos[:, 0] - cx
    dy = pos[:, 1] - cy
    return np.sqrt(np.sum(prob * (dx**2 + dy**2)))


def centroid(psi, pos):
    """Centroid of wavepacket."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    return np.array([cx, cy])


# ---------------------------------------------------------------------------
# Evolution with width tracking
# ---------------------------------------------------------------------------
def evolve_and_track(psi, G, L, col, adj, n, pos, n_steps=N_STEPS):
    """Evolve under self-gravity, return width trajectory."""
    psi = psi.copy().astype(complex)
    widths = [width(psi, pos)]
    centroids = [centroid(psi, pos)]

    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = solve_phi(rho, L, MU2, G, n) if G > 0 else np.zeros(n)
        H = make_hamiltonian_2d(phi, col, adj, n)
        psi = cn_step(psi, H, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        widths.append(width(psi, pos))
        centroids.append(centroid(psi, pos))

    return np.array(widths), np.array(centroids), psi


# ---------------------------------------------------------------------------
# G_Zeno identification
# ---------------------------------------------------------------------------
def find_g_zeno(G_values, final_widths, initial_width, threshold=0.05):
    """Find critical G where wavepacket stops spreading.

    Uses a relative threshold: if (w_final - w_init)/w_init < threshold,
    the packet is "frozen". G_Zeno is the crossover from spreading to frozen.
    """
    relative_spread = (np.array(final_widths) - initial_width) / initial_width
    frozen = relative_spread < threshold

    for i in range(len(frozen)):
        if frozen[i]:
            if i == 0:
                return G_values[0], 0
            # Log-linear interpolation between last spreading and first frozen
            g_lo, g_hi = G_values[i - 1], G_values[i]
            rs_lo, rs_hi = relative_spread[i - 1], relative_spread[i]
            if abs(rs_lo - rs_hi) < 1e-12:
                return g_lo, i
            # Interpolate where relative_spread = threshold
            frac = (threshold - rs_lo) / (rs_hi - rs_lo)
            if g_lo > 0 and g_hi > 0:
                # Log-space interpolation for G
                g_crit = np.exp(np.log(g_lo) + frac * (np.log(g_hi) - np.log(g_lo)))
            else:
                g_crit = g_lo + frac * (g_hi - g_lo)
            return g_crit, i
    return float("inf"), len(G_values)


# ---------------------------------------------------------------------------
# Geodesic tracking check
# ---------------------------------------------------------------------------
def geodesic_distance_from_center(pos, adj, center_idx, n):
    """BFS shortest-path distance from center node."""
    dist = np.full(n, np.inf)
    dist[center_idx] = 0
    queue = [center_idx]
    head = 0
    while head < len(queue):
        u = queue[head]; head += 1
        for v in adj[u]:
            if dist[v] == np.inf:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def check_geodesic_tracking(centroids, pos, adj, center_idx, n):
    """Check if centroid tracks the graph geodesic structure.

    Measure correlation between centroid displacement and geodesic distance.
    """
    geo_dist = geodesic_distance_from_center(pos, adj, center_idx, n)

    # For each timestep, find the node closest to centroid
    # and check if centroid stays near geodesic center
    centroid_drifts = []
    for c in centroids:
        dists_from_c = np.sqrt((pos[:, 0] - c[0])**2 + (pos[:, 1] - c[1])**2)
        nearest = np.argmin(dists_from_c)
        centroid_drifts.append(geo_dist[nearest])

    return np.array(centroid_drifts)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("FRONTIER: Quantum Zeno Effect from Self-Gravity")
    print("=" * 72)
    print(f"  MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print()

    # =======================================================================
    # Part 1: G sweep on side=10 lattice
    # =======================================================================
    side = 10
    print(f"[1] G sweep on {side}x{side} periodic lattice (n={side**2})")
    print("-" * 72)

    pos, col, L, adj, n = make_2d_periodic_lattice(side)
    center = np.array([side / 2.0, side / 2.0])
    psi0 = gaussian_2d(pos, center, SIGMA, n)
    w0 = width(psi0, pos)
    print(f"  Initial width: {w0:.4f}")
    print()

    print(f"{'G':>8s}  {'w_init':>8s}  {'w_final':>8s}  {'w_max':>8s}  {'w_min':>8s}  {'spread':>8s}")
    print("-" * 60)

    all_widths = {}
    all_centroids = {}
    final_widths = []
    final_psis = {}

    for G in G_VALUES:
        ws, cs, psi_f = evolve_and_track(psi0, G, L, col, adj, n, pos)
        all_widths[G] = ws
        all_centroids[G] = cs
        final_widths.append(ws[-1])
        final_psis[G] = psi_f
        spread = "SPREAD" if ws[-1] > w0 * 1.05 else ("FROZEN" if abs(ws[-1] - w0) < w0 * 0.05 else "SHRINK")
        print(f"{G:>8.1f}  {ws[0]:>8.4f}  {ws[-1]:>8.4f}  {np.max(ws):>8.4f}  {np.min(ws):>8.4f}  {spread:>8s}")

    print()

    # Width trajectories
    print("Width trajectories (every 10 steps):")
    header = f"{'step':>6s}"
    for G in G_VALUES:
        header += f"  {'G='+str(G):>10s}"
    print(header)
    print("-" * (6 + 12 * len(G_VALUES)))

    for t in range(0, N_STEPS + 1, 10):
        row = f"{t:>6d}"
        for G in G_VALUES:
            row += f"  {all_widths[G][t]:>10.4f}"
        print(row)
    # Also print final step
    if N_STEPS % 10 != 0:
        row = f"{N_STEPS:>6d}"
        for G in G_VALUES:
            row += f"  {all_widths[G][N_STEPS]:>10.4f}"
        print(row)
    print()

    # Find G_Zeno
    g_zeno, idx_zeno = find_g_zeno(G_VALUES, final_widths, w0)
    print(f"[*] Critical G_Zeno (width crossover): {g_zeno:.2f}")
    print(f"    (transition between G={G_VALUES[max(0, idx_zeno-1)]} and G={G_VALUES[min(idx_zeno, len(G_VALUES)-1)]})")
    print()

    # =======================================================================
    # Part 2: Geodesic tracking at critical G
    # =======================================================================
    print("[2] Geodesic tracking at critical G")
    print("-" * 72)

    # Use the G value closest to G_Zeno
    g_test = min(G_VALUES, key=lambda g: abs(g - g_zeno)) if g_zeno < float("inf") else G_VALUES[-1]
    print(f"  Testing at G={g_test}")

    center_idx = np.argmin(np.sum((pos - center)**2, axis=1))
    geo_drifts = check_geodesic_tracking(all_centroids[g_test], pos, adj, center_idx, n)
    print(f"  Centroid geodesic distance from center over time:")
    print(f"    t=0: {geo_drifts[0]:.1f},  t={N_STEPS//2}: {geo_drifts[N_STEPS//2]:.1f},  t={N_STEPS}: {geo_drifts[-1]:.1f}")
    print(f"    max drift: {np.max(geo_drifts):.1f},  mean drift: {np.mean(geo_drifts):.2f}")
    if np.max(geo_drifts) <= 1.0:
        print("    -> Centroid stays at geodesic center (localized)")
    else:
        print("    -> Centroid drifts from center")
    print()

    # =======================================================================
    # Part 3: Finite-size scaling
    # =======================================================================
    print("[3] Finite-size scaling: G_Zeno vs lattice side")
    print("-" * 72)

    g_zenos_by_size = {}
    for s in SIZE_SCAN:
        n_s = s * s
        pos_s, col_s, L_s, adj_s, _ = make_2d_periodic_lattice(s)
        center_s = np.array([s / 2.0, s / 2.0])
        psi0_s = gaussian_2d(pos_s, center_s, SIGMA, n_s)
        w0_s = width(psi0_s, pos_s)

        fws = []
        for G in G_VALUES:
            ws_s, _, _ = evolve_and_track(psi0_s, G, L_s, col_s, adj_s, n_s, pos_s)
            fws.append(ws_s[-1])

        g_z, _ = find_g_zeno(G_VALUES, fws, w0_s)
        g_zenos_by_size[s] = g_z
        print(f"  side={s:>3d} (n={n_s:>4d}): G_Zeno = {g_z:.2f}")

    print()
    values = [g_zenos_by_size[s] for s in SIZE_SCAN]
    if all(v < float("inf") for v in values):
        spread = max(values) - min(values)
        mean_gz = np.mean(values)
        print(f"  G_Zeno range: [{min(values):.2f}, {max(values):.2f}], spread={spread:.2f}")
        if spread < 0.3 * mean_gz:
            print("  -> G_Zeno approximately constant: PHYSICAL effect (not finite-size)")
        else:
            print("  -> G_Zeno varies with size: FINITE-SIZE artifact")
    else:
        print("  (Some sizes did not show Zeno transition within G range)")
    print()

    # =======================================================================
    # Part 4: Irregular graph (random geometric, side=8)
    # =======================================================================
    print("[4] Topology dependence: random geometric graph (side=8)")
    print("-" * 72)

    s_rg = 8
    n_rg = s_rg * s_rg
    pos_rg, col_rg, L_rg, adj_rg, _ = make_random_geometric_graph(s_rg)
    center_rg = np.array([s_rg / 2.0, s_rg / 2.0])
    psi0_rg = gaussian_2d(pos_rg, center_rg, SIGMA, n_rg)
    w0_rg = width(psi0_rg, pos_rg)
    print(f"  Initial width (random): {w0_rg:.4f}")

    print(f"\n{'G':>8s}  {'w_final':>8s}  {'spread':>8s}")
    print("-" * 30)

    fws_rg = []
    for G in G_VALUES:
        ws_rg, _, _ = evolve_and_track(psi0_rg, G, L_rg, col_rg, adj_rg, n_rg, pos_rg)
        fws_rg.append(ws_rg[-1])
        spread_label = "SPREAD" if ws_rg[-1] > w0_rg * 1.05 else ("FROZEN" if abs(ws_rg[-1] - w0_rg) < w0_rg * 0.05 else "SHRINK")
        print(f"{G:>8.1f}  {ws_rg[-1]:>8.4f}  {spread_label:>8s}")

    g_z_rg, _ = find_g_zeno(G_VALUES, fws_rg, w0_rg)
    print(f"\n  G_Zeno (random geometric): {g_z_rg:.2f}")
    g_z_regular = g_zenos_by_size.get(8, float("inf"))
    if g_z_regular < float("inf") and g_z_rg < float("inf"):
        ratio = g_z_rg / g_z_regular if g_z_regular > 0 else float("inf")
        print(f"  G_Zeno (regular side=8):   {g_z_regular:.2f}")
        print(f"  Ratio random/regular:      {ratio:.2f}")
        if abs(ratio - 1.0) < 0.3:
            print("  -> G_Zeno similar: Zeno effect is topology-independent")
        else:
            print("  -> G_Zeno differs: Zeno effect depends on topology")
    print()

    # =======================================================================
    # Summary
    # =======================================================================
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  G_Zeno (side=10):   {g_zeno:.2f}")
    print(f"  Finite-size stable: ", end="")
    if all(v < float("inf") for v in values):
        spread = max(values) - min(values)
        mean_gz = np.mean(values)
        print(f"{'YES' if spread < 0.3 * mean_gz else 'NO'} (spread/mean = {spread/mean_gz:.2f})")
    else:
        print("INCONCLUSIVE")
    print(f"  Topology-independent: ", end="")
    if g_z_regular < float("inf") and g_z_rg < float("inf"):
        ratio = g_z_rg / g_z_regular if g_z_regular > 0 else float("inf")
        print(f"{'YES' if abs(ratio - 1.0) < 0.3 else 'NO'} (ratio = {ratio:.2f})")
    else:
        print("INCONCLUSIVE")

    # Physics interpretation
    print()
    if g_zeno < float("inf"):
        print(f"  RESULT: Quantum Zeno localization observed at G_Zeno ~ {g_zeno:.1f}")
        print(f"  At weak G < {g_zeno:.0f}: wavepacket spreads freely")
        print(f"  At strong G > {g_zeno:.0f}: self-gravity freezes spreading")
        print(f"  Mechanism: frequent self-measurement via gravitational backreaction")
    else:
        print("  RESULT: No Zeno localization observed within G range")
        print("  Wavepacket spreads at all tested couplings")

    print()
    print("=" * 72)
    print("DONE")
    print("=" * 72)


if __name__ == "__main__":
    main()
