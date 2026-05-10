"""SU(3) Wigner engine — L_s=3 PBC cube treewidth-based contractor.

Engineering item #2 from PR #507/#509: implement treewidth-based
contraction ordering for the L_s=3 PBC cube exact tensor network.

Approach:
  1. Build the LINK ADJACENCY GRAPH: 81 nodes (= link tensors after
     channel-merge), edges = shared cyclic indices. The graph has 324
     edges (each cyclic index = one edge between 2 link tensors).
  2. Compute MIN-DEGREE ELIMINATION ORDER on this graph. This gives a
     treewidth UPPER BOUND.
  3. Estimate max clique size during elimination = max intermediate
     size in contraction.
  4. Report whether the earlier 8^9 estimate survives the link-graph
     analysis. In this runner it does not: the observed upper bound is
     29, which makes naive node-elimination infeasible.

Forbidden imports: none (numpy + scipy.special only).

Run:
    python3 scripts/frontier_su3_wigner_l3_treewidth_2026_05_04.py
"""

from __future__ import annotations

import math
import sys
import time
from typing import Dict, List, Set, Tuple

import numpy as np


BETA = 6.0
N_COLOR = 3
EPSILON_WITNESS = 3.03e-4
BRIDGE_SUPPORT_TARGET = 0.5935306800
P_TRIV_REFERENCE = 0.4225317396
P_LOC_REFERENCE = 0.4524071590
P_CANDIDATE_REFERENCE = 0.4291049969
L = 3
MEMORY_LIMIT_BYTES = 4 * 1024**3


# ===========================================================================
# Section A. Singlet basis (Block 2 algorithm).
# ===========================================================================

def gellmann_basis() -> List[np.ndarray]:
    l = [None] * 8
    l[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    l[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    l[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    l[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    l[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    l[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    l[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    l[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3)
    return l


def structure_constants() -> Tuple[np.ndarray, np.ndarray]:
    lam = gellmann_basis()
    n = 8
    f = np.zeros((n, n, n), dtype=float)
    d = np.zeros((n, n, n), dtype=float)
    for a in range(n):
        for b in range(n):
            comm = lam[a] @ lam[b] - lam[b] @ lam[a]
            anti = lam[a] @ lam[b] + lam[b] @ lam[a]
            for c in range(n):
                f[a, b, c] = float((1.0 / (4j) * np.trace(lam[c] @ comm)).real)
                d[a, b, c] = float((1.0 / 4.0 * np.trace(lam[c] @ anti)).real)
    return f, d


def adjoint_generators(f: np.ndarray) -> List[np.ndarray]:
    n = 8
    return [np.array([[-1j * f[a, b, c] for c in range(n)] for b in range(n)],
                       dtype=complex) for a in range(n)]


def four_fold_haar_singlet_basis(verbose: bool = True) -> np.ndarray:
    f, _ = structure_constants()
    T = adjoint_generators(f)
    n = 8
    I8 = np.eye(n, dtype=complex)
    if verbose:
        print("    Building 8 total generators on V^4...")
    T_total = []
    for a in range(n):
        Ta_1 = np.kron(np.kron(np.kron(T[a], I8), I8), I8)
        Ta_2 = np.kron(np.kron(np.kron(I8, T[a]), I8), I8)
        Ta_3 = np.kron(np.kron(np.kron(I8, I8), T[a]), I8)
        Ta_4 = np.kron(np.kron(np.kron(I8, I8), I8), T[a])
        T_total.append(Ta_1 + Ta_2 + Ta_3 + Ta_4)
    if verbose:
        print("    Computing C_2_total...")
    dim = 4096
    C = np.zeros((dim, dim), dtype=complex)
    for Ta in T_total:
        C = C + Ta @ Ta
    C = (C + C.conj().T) / 2.0
    if verbose:
        print("    Diagonalizing...")
    eigvals, eigvecs = np.linalg.eigh(C)
    singlet_indices = np.where(np.abs(eigvals) < 1e-8)[0]
    return eigvecs[:, singlet_indices]


# ===========================================================================
# Section B. L_s=3 PBC cube geometry.
# ===========================================================================

def link_id(x: int, y: int, z: int, direction: int) -> int:
    return (((x * L) + y) * L + z) * 3 + direction


def all_wilson_plaquettes() -> List[Tuple]:
    plaquettes = []
    seen = set()
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for mu in range(3):
                    for nu in range(mu + 1, 3):
                        site = [x, y, z]
                        x_p_mu = list(site); x_p_mu[mu] = (x_p_mu[mu] + 1) % L
                        x_p_nu = list(site); x_p_nu[nu] = (x_p_nu[nu] + 1) % L
                        l_1 = link_id(site[0], site[1], site[2], mu)
                        l_2 = link_id(x_p_mu[0], x_p_mu[1], x_p_mu[2], nu)
                        l_3 = link_id(x_p_nu[0], x_p_nu[1], x_p_nu[2], mu)
                        l_4 = link_id(site[0], site[1], site[2], nu)
                        link_set = frozenset([l_1, l_2, l_3, l_4])
                        if link_set in seen:
                            continue
                        seen.add(link_set)
                        plaquettes.append((tuple(site), mu, nu,
                                             [(l_1, +1), (l_2, +1),
                                              (l_3, -1), (l_4, -1)]))
    return plaquettes


def link_to_plaquette_slots(plaquettes: List[Tuple]) -> Dict[int, List]:
    out: Dict[int, List] = {}
    for p_idx, (_, _, _, links) in enumerate(plaquettes):
        for slot, (l_id, sign) in enumerate(links):
            out.setdefault(l_id, []).append((p_idx, slot, sign))
    return out


# ===========================================================================
# Section C. Link adjacency graph for treewidth analysis.
# ===========================================================================

# Plaquette cyclic-index map: which slots share which cyclic index?
# slot 0: row=cyc[0], col=cyc[1]
# slot 1: row=cyc[1], col=cyc[2]
# slot 2: row=cyc[3], col=cyc[2]
# slot 3: row=cyc[0], col=cyc[3]
# So adjacencies within a plaquette (= shared cyclic indices):
#   slot 0 - slot 1: share cyc[1]
#   slot 0 - slot 3: share cyc[0]
#   slot 1 - slot 2: share cyc[2]
#   slot 2 - slot 3: share cyc[3]
# Slots 0-2 and 1-3 do NOT share any cyclic index within a plaquette.

PLAQUETTE_INTERNAL_ADJACENCIES = [(0, 1), (0, 3), (1, 2), (2, 3)]


def build_link_adjacency_graph(plaquettes: List[Tuple]
                                  ) -> Dict[int, Set[int]]:
    """Build the link adjacency graph: nodes are links, edges are shared
    cyclic indices.

    Returns adjacency dict: link_id -> set of neighboring link_ids.
    """
    adj: Dict[int, Set[int]] = {}
    for p_idx, (_, _, _, links) in enumerate(plaquettes):
        l_ids = [l_id for (l_id, _) in links]
        for (s_a, s_b) in PLAQUETTE_INTERNAL_ADJACENCIES:
            l_a = l_ids[s_a]
            l_b = l_ids[s_b]
            adj.setdefault(l_a, set()).add(l_b)
            adj.setdefault(l_b, set()).add(l_a)
    return adj


# ===========================================================================
# Section D. Min-degree elimination order.
# ===========================================================================

def min_degree_elimination_order(adj_in: Dict[int, Set[int]]
                                    ) -> Tuple[List[int], int]:
    """Compute min-degree elimination order on a graph.

    Returns (elim_order, max_clique_size_during_elim).

    The max clique size during elimination = treewidth UPPER BOUND.
    """
    # Copy the graph so we can mutate it
    adj = {u: set(neighbors) for u, neighbors in adj_in.items()}
    elim_order: List[int] = []
    max_clique = 0
    while adj:
        # Find node with min degree (tie-break by ID)
        min_node = min(adj.keys(), key=lambda u: (len(adj[u]), u))
        deg = len(adj[min_node])
        # The "clique" formed by min_node's neighbors during elimination
        # has size deg + 1 (min_node + its deg neighbors).
        clique_size = deg + 1
        if clique_size > max_clique:
            max_clique = clique_size
        # Eliminate min_node: connect all its neighbors pairwise
        neighbors = adj[min_node]
        for u in neighbors:
            for v in neighbors:
                if u != v:
                    adj[u].add(v)
        # Remove min_node
        for u in neighbors:
            adj[u].discard(min_node)
        del adj[min_node]
        elim_order.append(min_node)
    return elim_order, max_clique


def min_fill_elimination_order(adj_in: Dict[int, Set[int]]
                                 ) -> Tuple[List[int], int]:
    """Min-fill heuristic: eliminate the node that adds the fewest new
    edges to its neighbor clique.

    Often gives better treewidth bounds than min-degree.
    """
    adj = {u: set(neighbors) for u, neighbors in adj_in.items()}
    elim_order: List[int] = []
    max_clique = 0
    while adj:
        # Find node with min FILL (= number of missing edges between
        # its neighbors)
        best_node = None
        best_fill = float('inf')
        best_deg = float('inf')
        for u in adj.keys():
            neighbors = adj[u]
            # Count missing edges among neighbors
            fill = 0
            ns = list(neighbors)
            for i in range(len(ns)):
                for j in range(i + 1, len(ns)):
                    if ns[j] not in adj[ns[i]]:
                        fill += 1
            if fill < best_fill or (fill == best_fill and len(neighbors) < best_deg):
                best_fill = fill
                best_deg = len(neighbors)
                best_node = u
        u = best_node
        deg = len(adj[u])
        clique_size = deg + 1
        if clique_size > max_clique:
            max_clique = clique_size
        neighbors = adj[u]
        for v in neighbors:
            for w in neighbors:
                if v != w:
                    adj[v].add(w)
        for v in neighbors:
            adj[v].discard(u)
        del adj[u]
        elim_order.append(u)
    return elim_order, max_clique


# ===========================================================================
# Section E. Driver — scoping analysis only.
# ===========================================================================

def driver() -> int:
    print("=" * 78)
    print(f"SU(3) Wigner Engine — L_s={L} PBC Cube Treewidth Analysis")
    print("=" * 78)
    print()

    pass_count = 0
    fail_count = 0
    support_count = 0

    # ===== Section A: cube geometry =====
    print(f"--- Section A: L_s={L} PBC cube geometry ---")
    plaquettes = all_wilson_plaquettes()
    n_plaq = len(plaquettes)
    link_dict = link_to_plaquette_slots(plaquettes)
    n_links = len(link_dict)
    print(f"  unique plaquettes: {n_plaq}")
    print(f"  unique directed links: {n_links}")
    if n_plaq == 81 and n_links == 81:
        print("  PASS: 81 × 81 cube geometry.")
        pass_count += 1
    else:
        print("  FAIL.")
        fail_count += 1
    print()

    # ===== Section B: link adjacency graph =====
    print("--- Section B: link adjacency graph (shared cyclic indices) ---")
    adj = build_link_adjacency_graph(plaquettes)
    n_nodes = len(adj)
    n_edges = sum(len(neighbors) for neighbors in adj.values()) // 2
    degrees = [len(neighbors) for neighbors in adj.values()]
    print(f"  nodes: {n_nodes}")
    print(f"  edges: {n_edges}")
    print(f"  degree stats: min={min(degrees)}, max={max(degrees)}, "
          f"mean={sum(degrees)/len(degrees):.2f}")
    # Note: graph is 8-regular (each link in 4 plaquettes × 2 adjacent
    # links per plaquette). Edge count = 81 × 8 / 2 = 324.
    if n_nodes == 81 and n_edges == 324 and all(d == 8 for d in degrees):
        print("  PASS: 81 nodes × 324 edges = 8-regular (4 plaq × 2 adj/plaq).")
        pass_count += 1
    else:
        print(f"  FAIL: nodes/edges/degree mismatch.")
        fail_count += 1
    print()

    # ===== Section C: min-degree elimination order =====
    print("--- Section C: min-degree elimination order (treewidth upper bound) ---")
    t0 = time.time()
    elim_md, max_clique_md = min_degree_elimination_order(adj)
    print(f"  [{time.time() - t0:.2f}s] min-degree completed")
    print(f"  Elimination length: {len(elim_md)} (expected 81)")
    print(f"  Max clique size during elimination: {max_clique_md}")
    print(f"  Treewidth UPPER BOUND (min-degree): {max_clique_md - 1}")
    print(f"  Worst intermediate size: 8^{max_clique_md} = "
          f"{8**max_clique_md:,} entries = "
          f"{8**max_clique_md * 16 / 1024**3:.2f} GB")
    print()

    # ===== Section D: min-fill elimination order =====
    print("--- Section D: min-fill elimination order ---")
    t0 = time.time()
    elim_mf, max_clique_mf = min_fill_elimination_order(adj)
    print(f"  [{time.time() - t0:.2f}s] min-fill completed")
    print(f"  Max clique size during elimination: {max_clique_mf}")
    print(f"  Treewidth UPPER BOUND (min-fill): {max_clique_mf - 1}")
    print(f"  Worst intermediate size: 8^{max_clique_mf} = "
          f"{8**max_clique_mf:,} entries = "
          f"{8**max_clique_mf * 16 / 1024**3:.2f} GB")
    print()

    # ===== Section E: feasibility verdict =====
    print("--- Section E: feasibility verdict ---")
    print()
    print(f"  Memory budget:                   "
          f"{MEMORY_LIMIT_BYTES / 1024**3:.1f} GB")
    print(f"  Min-degree max intermediate:     "
          f"{8**max_clique_md * 16 / 1024**3:.2f} GB")
    print(f"  Min-fill max intermediate:       "
          f"{8**max_clique_mf * 16 / 1024**3:.2f} GB")
    print()
    best_clique = min(max_clique_md, max_clique_mf)
    best_method = "min-degree" if max_clique_md <= max_clique_mf else "min-fill"
    best_intermediate_bytes = 8 ** best_clique * 16
    print(f"  Best heuristic: {best_method} with treewidth bound {best_clique - 1}")
    print(f"  Best max intermediate: 8^{best_clique} = "
          f"{best_intermediate_bytes / 1024**3:.2f} GB")
    print()
    if best_intermediate_bytes <= MEMORY_LIMIT_BYTES:
        print(f"  *** FEASIBLE *** Best heuristic gives intermediate "
              f"≤ memory budget.")
        print(f"  Engineering item #2 is achievable with this elimination order.")
        print(f"  Next step: implement contractor that follows this elim order.")
        pass_count += 1
    elif best_intermediate_bytes <= 16 * 1024**3:
        print(f"  MARGINAL: best heuristic gives "
              f"{best_intermediate_bytes / 1024**3:.1f} GB intermediate, "
              f"close to but exceeds 4 GB budget.")
        print(f"  Closure path: increase memory budget OR use better")
        print(f"  contraction-order algorithm (e.g., simulated annealing,")
        print(f"  branch-and-bound on small subnetworks).")
        support_count += 1
    else:
        print(f"  INFEASIBLE: best heuristic gives "
              f"{best_intermediate_bytes / 1024**3:.1f} GB intermediate, "
              f"exceeds 4 GB budget by "
              f"{best_intermediate_bytes / MEMORY_LIMIT_BYTES:.0f}×.")
        print(f"  Closure path: alternative methods needed:")
        print(f"    - tensor-train / matrix-product-state ansatz")
        print(f"    - hierarchical tucker decomposition")
        print(f"    - adopt opt_einsum library (changes import policy)")
        support_count += 1
    print()

    # ===== Summary =====
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} "
          f"FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  L_s={L} PBC cube link adjacency graph: 81 nodes, "
          f"{n_edges} edges, degree stats {min(degrees)}-{max(degrees)}")
    print(f"  Min-degree treewidth bound: {max_clique_md - 1} "
          f"(intermediate 8^{max_clique_md} = "
          f"{8**max_clique_md * 16 / 1024**3:.2f} GB)")
    print(f"  Min-fill treewidth bound:   {max_clique_mf - 1} "
          f"(intermediate 8^{max_clique_mf} = "
          f"{8**max_clique_mf * 16 / 1024**3:.2f} GB)")
    print(f"  Best heuristic intermediate: "
          f"{best_intermediate_bytes / 1024**3:.2f} GB")
    print(f"  Memory budget: 4.0 GB")
    if best_intermediate_bytes <= MEMORY_LIMIT_BYTES:
        print(f"  Verdict: FEASIBLE — implement contractor next")
    else:
        print(f"  Verdict: NEEDS BETTER ORDERING or alternative method")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
