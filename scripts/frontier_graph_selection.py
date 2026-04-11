#!/usr/bin/env python3
"""
Spectral-action graph selection via simulated annealing on bipartite graphs
===========================================================================

QUESTION: Does minimizing a spectral action over bipartite graphs select
a lattice-like graph with integer spectral dimension?

METHOD:
  1. Define spectral action S[G] = sum_i f(lam_i / Lambda)
     where lam_i are eigenvalues of the staggered Dirac operator D,
     f(x) = x^2 exp(-x^2), Lambda = 2.0 (cutoff).

  2. Start from a random bipartite graph on N nodes (N/2 even, N/2 odd).
     Random edges between opposite-color nodes, ~4 edges per node.

  3. Simulated annealing: add/remove one edge (preserving bipartiteness
     AND connectivity). Accept if S decreases, else accept with
     prob exp(-dS/T). Cool T from 1.0 to 0.01 over 5000 steps.

  4. Characterize minimizer: degree distribution, spectral dimension d_s,
     clustering coefficient, lattice-likeness.

  5. Five independent runs per N. Also try N=64.

  6. Two regimes: UNCONSTRAINED (free edge count) and CONSTRAINED
     (connected graph with min degree >= 1).

The staggered Dirac operator uses the convention from frontier_staggered_17card:
  H[x,y] = -i/2 (hop right), +i/2 (hop left)
  H[x,x] = (m + phi) * epsilon(x)
with m=0.3, phi=0 (free fermion, no gravity).
"""

import numpy as np
from collections import deque
import time


# ── Parameters ───────────────────────────────────────────────────────────
MASS = 0.3
LAMBDA_CUT = 2.0
N_ANNEAL_STEPS = 5000
T_START = 1.0
T_END = 0.01
N_RUNS = 5
SEED_BASE = 42


def spectral_action_f(x):
    """Cutoff function f(x) = x^2 exp(-x^2)."""
    return x**2 * np.exp(-x**2)


def build_staggered_dirac(adj, parity, mass):
    """Build staggered Dirac operator on a general bipartite graph."""
    n = len(parity)
    H = np.zeros((n, n), dtype=complex)
    for i, j in adj:
        eta = parity[i]
        H[i, j] += -1j / 2 * eta
        H[j, i] += 1j / 2 * eta
    for x in range(n):
        H[x, x] += mass * parity[x]
    return H


def compute_spectral_action(H, lam_cut):
    """Compute S[G] = sum_i f(|lam_i| / Lambda)."""
    evals = np.linalg.eigvalsh(H)
    x = np.abs(evals) / lam_cut
    return np.sum(spectral_action_f(x))


def is_connected(edge_set, n):
    """BFS connectivity check."""
    if not edge_set:
        return n <= 1
    adj = [[] for _ in range(n)]
    for i, j in edge_set:
        adj[i].append(j)
        adj[j].append(i)
    visited = set()
    queue = deque([0])
    visited.add(0)
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in visited:
                visited.add(w)
                queue.append(w)
    return len(visited) == n


def random_bipartite_graph(n_even, n_odd, avg_degree, rng, connected=False):
    """Create a random bipartite graph."""
    n = n_even + n_odd
    parity = np.ones(n, dtype=int)
    parity[n_even:] = -1

    even_nodes = list(range(n_even))
    odd_nodes = list(range(n_even, n))

    if connected:
        # Start with a spanning tree to ensure connectivity
        edges = set()
        # Random spanning tree: connect each even node to a random odd, etc.
        rng.shuffle(even_nodes_copy := list(even_nodes))
        rng.shuffle(odd_nodes_copy := list(odd_nodes))
        # Connect in a path: e0-o0-e1-o1-...
        for k in range(min(n_even, n_odd)):
            e = even_nodes_copy[k]
            o = odd_nodes_copy[k]
            edges.add((min(e, o), max(e, o)))
            if k > 0:
                # Connect previous odd to current even
                o_prev = odd_nodes_copy[k - 1]
                e_curr = even_nodes_copy[k]
                edges.add((min(o_prev, e_curr), max(o_prev, e_curr)))
        # Connect remaining nodes
        for k in range(min(n_even, n_odd), n_even):
            o = rng.choice(odd_nodes)
            edges.add((min(even_nodes_copy[k], o), max(even_nodes_copy[k], o)))
        for k in range(min(n_even, n_odd), n_odd):
            e = rng.choice(even_nodes)
            edges.add((min(e, odd_nodes_copy[k]), max(e, odd_nodes_copy[k])))

        # Add random edges to reach target degree
        n_target = int(n * avg_degree / 2)
        attempts = 0
        while len(edges) < n_target and attempts < n_target * 10:
            i = rng.choice(even_nodes)
            j = rng.choice(odd_nodes)
            edges.add((min(i, j), max(i, j)))
            attempts += 1
        return list(edges), parity

    # Unconstrained
    n_edges_target = int(n * avg_degree / 2)
    edges = set()
    while len(edges) < n_edges_target:
        i = rng.choice(even_nodes)
        j = rng.choice(odd_nodes)
        edges.add((min(i, j), max(i, j)))
    return list(edges), parity


def degree_distribution(edges, n):
    deg = np.zeros(n, dtype=int)
    for i, j in edges:
        deg[i] += 1
        deg[j] += 1
    return deg


def spectral_dimension(H):
    """Estimate spectral dimension from heat-kernel return probability."""
    evals = np.linalg.eigvalsh(H)
    lam2 = evals**2

    lam_max = np.max(np.abs(evals))
    if lam_max < 1e-10:
        return 0.0

    t_min = 0.1 / lam_max**2
    med_lam2 = np.median(lam2[lam2 > 1e-10]) if np.any(lam2 > 1e-10) else 1.0
    t_max = 10.0 / med_lam2
    t_range = np.logspace(np.log10(max(t_min, 1e-4)), np.log10(min(t_max, 100.0)), 50)

    log_t = np.log(t_range)
    log_P = np.array([np.log(max(np.mean(np.exp(-t * lam2)), 1e-300)) for t in t_range])

    mid = len(t_range) // 4
    end = 3 * len(t_range) // 4
    if end - mid < 3:
        mid, end = 0, len(t_range)
    coeffs = np.polyfit(log_t[mid:end], log_P[mid:end], 1)
    return -2 * coeffs[0]


def clustering_coefficient(edges, n):
    adj_list = [set() for _ in range(n)]
    for i, j in edges:
        adj_list[i].add(j)
        adj_list[j].add(i)
    cc_sum = 0.0
    cc_count = 0
    for v in range(n):
        nbrs = list(adj_list[v])
        k = len(nbrs)
        if k < 2:
            continue
        tri = sum(1 for a in range(k) for b in range(a + 1, k)
                  if nbrs[b] in adj_list[nbrs[a]])
        cc_sum += 2 * tri / (k * (k - 1))
        cc_count += 1
    return cc_sum / cc_count if cc_count > 0 else 0.0


def n_components(edge_set, n):
    """Count connected components."""
    adj = [[] for _ in range(n)]
    for i, j in edge_set:
        adj[i].append(j)
        adj[j].append(i)
    visited = [False] * n
    comps = 0
    for start in range(n):
        if visited[start]:
            continue
        comps += 1
        queue = deque([start])
        visited[start] = True
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if not visited[w]:
                    visited[w] = True
                    queue.append(w)
    return comps


def simulated_annealing(n_even, n_odd, n_steps, t_start, t_end, seed,
                        require_connected=False):
    """Run simulated annealing to minimize spectral action."""
    rng = np.random.RandomState(seed)
    n = n_even + n_odd

    edges, parity = random_bipartite_graph(
        n_even, n_odd, avg_degree=4, rng=rng, connected=require_connected
    )
    edge_set = set((min(i, j), max(i, j)) for i, j in edges)

    even_nodes = list(range(n_even))
    odd_nodes = list(range(n_even, n))

    H = build_staggered_dirac(list(edge_set), parity, MASS)
    S_current = compute_spectral_action(H, LAMBDA_CUT)

    best_edges = set(edge_set)
    best_S = S_current

    temps = np.logspace(np.log10(t_start), np.log10(t_end), n_steps)
    accept_count = 0
    improve_count = 0

    for step in range(n_steps):
        T = temps[step]

        # Propose move
        if rng.random() < 0.5 and len(edge_set) > n - 1:
            # Remove a random edge
            edge_list = list(edge_set)
            idx = rng.randint(len(edge_list))
            removed = edge_list[idx]
            new_edges = edge_set - {removed}

            if require_connected:
                # Check connectivity
                if not is_connected(new_edges, n):
                    continue
        else:
            # Add a random edge
            for _ in range(100):
                i = rng.choice(even_nodes)
                j = rng.choice(odd_nodes)
                e = (min(i, j), max(i, j))
                if e not in edge_set:
                    break
            else:
                continue
            new_edges = edge_set | {e}

        H_new = build_staggered_dirac(list(new_edges), parity, MASS)
        S_new = compute_spectral_action(H_new, LAMBDA_CUT)
        dS = S_new - S_current

        if dS < 0 or rng.random() < np.exp(-dS / max(T, 1e-15)):
            edge_set = new_edges
            S_current = S_new
            accept_count += 1
            if dS < 0:
                improve_count += 1
            if S_current < best_S:
                best_S = S_current
                best_edges = set(edge_set)

        if (step + 1) % 1000 == 0:
            print(f"  Step {step+1}/{n_steps}: S={S_current:.4f} "
                  f"(best={best_S:.4f}), T={T:.4f}, "
                  f"|E|={len(edge_set)}, accept={accept_count}/{step+1}")

    return best_edges, parity, best_S, accept_count, improve_count


def analyze_graph(edges, parity, n, label=""):
    """Full analysis of a graph."""
    edge_list = list(edges)
    H = build_staggered_dirac(edge_list, parity, MASS)

    S = compute_spectral_action(H, LAMBDA_CUT)
    d_s = spectral_dimension(H)
    cc = clustering_coefficient(edge_list, n)
    deg = degree_distribution(edge_list, n)
    nc = n_components(edges, n)

    mean_deg = np.mean(deg)
    std_deg = np.std(deg)
    cv_deg = std_deg / mean_deg if mean_deg > 0 else float("inf")

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Spectral action S = {S:.6f}")
    print(f"  Spectral dimension d_s = {d_s:.3f}")
    print(f"  Clustering coefficient = {cc:.4f}")
    print(f"  Edges: {len(edge_list)}, Components: {nc}")
    print(f"  Degree: mean={mean_deg:.2f}, std={std_deg:.2f}, CV={cv_deg:.3f}")
    print(f"  Degree range: [{int(np.min(deg))}, {int(np.max(deg))}]")
    print(f"  Isolated nodes: {int(np.sum(deg == 0))}")

    unique, counts = np.unique(deg, return_counts=True)
    print(f"  Degree histogram: {dict(zip(unique.tolist(), counts.tolist()))}")

    evals = np.linalg.eigvalsh(H)
    print(f"  Eigenvalue range: [{evals[0]:.4f}, {evals[-1]:.4f}]")
    print(f"  Eigenvalue gap (smallest |lam|): {np.min(np.abs(evals)):.6f}")

    return {
        "S": S, "d_s": d_s, "cc": cc, "edges": len(edge_list),
        "mean_deg": mean_deg, "std_deg": std_deg, "cv_deg": cv_deg,
        "deg_range": (int(np.min(deg)), int(np.max(deg))),
        "components": nc,
    }


def reference_lattice_action(d, n_total, mass):
    """Compute spectral action for a d-dimensional hypercubic lattice."""
    if d == 1:
        n = n_total
        parity = np.array([(-1)**x for x in range(n)])
        edges = [(x, x + 1) for x in range(n - 1)]
    elif d == 2:
        side = int(np.sqrt(n_total))
        n = side * side
        parity = np.array([(-1)**(x + y) for x in range(side) for y in range(side)])
        edges = []
        for x in range(side):
            for y in range(side):
                i = x * side + y
                if x + 1 < side:
                    edges.append((i, (x + 1) * side + y))
                if y + 1 < side:
                    edges.append((i, x * side + (y + 1)))
    elif d == 3:
        # For N=36: 3x3x4=36; for N=64: 4x4x4=64
        if n_total == 36:
            dims = (3, 3, 4)
        elif n_total == 64:
            dims = (4, 4, 4)
        else:
            cb = int(round(n_total**(1/3)))
            dims = (cb, cb, cb)
        n = dims[0] * dims[1] * dims[2]
        parity = np.zeros(n, dtype=int)
        edges = []
        for x in range(dims[0]):
            for y in range(dims[1]):
                for z in range(dims[2]):
                    i = x * dims[1] * dims[2] + y * dims[2] + z
                    parity[i] = (-1)**(x + y + z)
                    if x + 1 < dims[0]:
                        j = (x + 1) * dims[1] * dims[2] + y * dims[2] + z
                        edges.append((min(i, j), max(i, j)))
                    if y + 1 < dims[1]:
                        j = x * dims[1] * dims[2] + (y + 1) * dims[2] + z
                        edges.append((min(i, j), max(i, j)))
                    if z + 1 < dims[2]:
                        j = x * dims[1] * dims[2] + y * dims[2] + (z + 1)
                        edges.append((min(i, j), max(i, j)))
    else:
        return None

    H = build_staggered_dirac(edges, parity, mass)
    S = compute_spectral_action(H, LAMBDA_CUT)
    d_s = spectral_dimension(H)
    deg = degree_distribution(edges, n)
    return {
        "d": d, "n": n, "S": S, "d_s": d_s, "edges": len(edges),
        "S_per_node": S / n, "mean_deg": np.mean(deg),
    }


def summarize_runs(results, n_total, label):
    """Print summary statistics across runs."""
    print(f"\n{'='*70}")
    print(f"SUMMARY: {label}")
    print(f"{'='*70}")

    keys = ["S", "d_s", "mean_deg", "cv_deg", "edges", "cc", "components"]
    for k in keys:
        vals = [r[k] for r in results]
        print(f"  {k:>12s}: {np.mean(vals):.4f} +/- {np.std(vals):.4f}")

    ds_vals = [r["d_s"] for r in results]
    ds_mean = np.mean(ds_vals)
    ds_std = np.std(ds_vals)

    if ds_std < 0.3:
        nearest = round(ds_mean)
        delta = abs(ds_mean - nearest)
        print(f"\n  d_s converges near {ds_mean:.3f} +/- {ds_std:.3f}")
        print(f"  Nearest integer: {nearest}, deviation: {delta:.3f}")
        if delta < 0.2:
            print(f"  ** d_s IS close to integer {nearest} **")
        else:
            print(f"  d_s is NOT close to an integer.")
    else:
        print(f"\n  d_s does NOT converge (spread = {ds_std:.3f})")


def main():
    print("=" * 70)
    print("SPECTRAL-ACTION GRAPH SELECTION VIA SIMULATED ANNEALING")
    print("=" * 70)
    print(f"Parameters: mass={MASS}, Lambda={LAMBDA_CUT}, "
          f"steps={N_ANNEAL_STEPS}, T=[{T_START},{T_END}]")

    # ── Reference lattices ──────────────────────────────────────
    for N in [36, 64]:
        print(f"\n--- Reference lattices for N={N} ---")
        for d in [1, 2, 3]:
            ref = reference_lattice_action(d, N, MASS)
            if ref and ref["n"] == N:
                print(f"  {d}D: |E|={ref['edges']}, S={ref['S']:.4f}, "
                      f"S/N={ref['S_per_node']:.4f}, d_s={ref['d_s']:.3f}, "
                      f"mean_deg={ref['mean_deg']:.1f}")
            elif ref:
                print(f"  {d}D: N={ref['n']} (not {N}), S={ref['S']:.4f}, "
                      f"S/N={ref['S_per_node']:.4f}, d_s={ref['d_s']:.3f}")

    # ── Annealing runs ──────────────────────────────────────────
    for N_total in [36, 64]:
        n_even = N_total // 2
        n_odd = N_total - n_even

        for constrained in [False, True]:
            mode = "CONNECTED" if constrained else "UNCONSTRAINED"
            print(f"\n{'#' * 70}")
            print(f"  N = {N_total}, mode = {mode}")
            print(f"{'#' * 70}")

            results = []
            for run in range(N_RUNS):
                seed = SEED_BASE + run * 17 + (1000 if constrained else 0)
                print(f"\n--- Run {run+1}/{N_RUNS} (seed={seed}) ---")
                t0 = time.time()

                best_edges, parity, best_S, n_accept, n_improve = simulated_annealing(
                    n_even, n_odd, N_ANNEAL_STEPS, T_START, T_END, seed,
                    require_connected=constrained,
                )

                elapsed = time.time() - t0
                print(f"  Done in {elapsed:.1f}s "
                      f"(accepted {n_accept}/{N_ANNEAL_STEPS}, improved {n_improve})")

                info = analyze_graph(
                    best_edges, parity, N_total,
                    label=f"N={N_total} {mode} Run {run+1}",
                )
                info["seed"] = seed
                results.append(info)

            summarize_runs(results, N_total, f"N={N_total} {mode}")

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
