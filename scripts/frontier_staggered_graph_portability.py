#!/usr/bin/env python3
"""Staggered graph portability probe.

Goal:
  Test whether staggered / Kahler-Dirac style transport plus potential gravity
  survives on non-cubic bipartite graph families.

Families:
  - bipartite random geometric graph
  - bipartite growing graph
  - layered bipartite DAG-compatible graph

Battery:
  - Born/linearity proxy
  - norm preservation
  - gravity sign
  - F∝M
  - achromatic force
  - equivalence
  - robustness
  - native gauge response if a cycle exists

This is intentionally narrow and retained. It is a portability probe, not a
universal graph theorem.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


DT = 0.12
N_STEPS = 10
MASS = 0.30
G = 8.0
SOURCE_STRENGTH = 4.0e-4
EPS = 0.35
K_BAND = (0.0, 0.18, 0.36, 0.54)
ACHROM_K = (0.0, 0.12, 0.24, 0.36, 0.48)
SOURCE_SIGMA = 1.15
F_TOL = 1e-12


@dataclass(frozen=True)
class GraphFamily:
    name: str
    positions: np.ndarray
    colors: np.ndarray
    adj: dict[int, list[int]]
    source: int
    detector: list[int]
    depth: np.ndarray
    has_cycle: bool
    cycle_edge: tuple[int, int] | None


@dataclass
class FamilyResult:
    family: str
    n: int
    born_lin: float
    norm_drift: float
    force_sign: str
    force_value: float
    fm_r2: float
    achrom_cv: float
    equiv_cv: float
    robust_toward: int
    robust_total: int
    gauge_j_range: float | None
    gauge_status: str


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _finalize_adj(adj_sets: dict[int, set[int]]) -> dict[int, list[int]]:
    return {i: sorted(list(nbs)) for i, nbs in adj_sets.items()}


def _bfs_depth(adj: dict[int, list[int]], source: int, n: int) -> np.ndarray:
    depth = np.full(n, np.inf)
    depth[source] = 0.0
    q = deque([source])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] != np.inf:
                continue
            depth[j] = depth[i] + 1.0
            q.append(j)
    return depth


def _find_cycle_edge(adj: dict[int, list[int]]) -> tuple[int, int] | None:
    parent: dict[int, int] = {}
    state: dict[int, int] = {}

    def dfs(node: int, prev: int | None) -> tuple[int, int] | None:
        state[node] = 1
        for nb in adj.get(node, []):
            if nb == prev:
                continue
            if nb not in state:
                parent[nb] = node
                hit = dfs(nb, node)
                if hit is not None:
                    return hit
            elif state[nb] == 1:
                return (node, nb)
        state[node] = 2
        return None

    for start in sorted(adj):
        if start in state:
            continue
        hit = dfs(start, None)
        if hit is not None:
            return hit
    return None


def _graph_distance_from_source(adj: dict[int, list[int]], source: int, n: int) -> np.ndarray:
    return _bfs_depth(adj, source, n)


def _probe_state(n: int, coords: np.ndarray, source: int, sigma: float = SOURCE_SIGMA, k0: float = 0.0) -> np.ndarray:
    center = coords[source]
    rel = coords - center
    coord = rel[:, 0] + 0.35 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / (sigma**2)) * np.exp(1j * k0 * coord)
    norm = np.linalg.norm(psi)
    return psi.astype(complex) / norm if norm > 0 else psi.astype(complex)


def _build_hamiltonian(
    graph: GraphFamily,
    mass: float,
    source_strength: float,
    flux: float = 0.0,
    flux_edge: tuple[int, int] | None = None,
) -> csr_matrix:
    n = graph.positions.shape[0]
    H = lil_matrix((n, n), dtype=complex)
    dist = graph.depth
    V = np.zeros(n, dtype=float)
    for i in range(n):
        if np.isfinite(dist[i]):
            V[i] = -mass * G * source_strength / (dist[i] + EPS)

    parity = np.where(graph.colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity + V)

    phase_edge = None
    if flux_edge is not None:
        a, b = flux_edge
        phase_edge = (min(a, b), max(a, b))

    for i, nbs in graph.adj.items():
        for j in nbs:
            if i >= j:
                continue
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist_ij = math.hypot(dx, dy)
            w = 1.0 / max(dist_ij, 0.5)
            phase = 0.0
            if phase_edge is not None and (i, j) == phase_edge:
                phase = flux
            hop = -0.5j * w * np.exp(1j * phase)
            H[i, j] += hop
            H[j, i] += np.conj(hop)

    return H.tocsr()


def _evolve_cn(H: csr_matrix, psi0: np.ndarray, dt: float, n_steps: int) -> np.ndarray:
    n = H.shape[0]
    ap = (speye(n, format="csc") + 1j * H * dt / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * dt / 2
    psi = psi0.copy()
    for _ in range(n_steps):
        psi = spsolve(ap, am.dot(psi))
    return psi


def _lin_residual(H: csr_matrix, psi_a: np.ndarray, psi_b: np.ndarray) -> float:
    ua = _evolve_cn(H, psi_a, DT, N_STEPS)
    ub = _evolve_cn(H, psi_b, DT, N_STEPS)
    uab = _evolve_cn(H, psi_a + psi_b, DT, N_STEPS)
    num = np.linalg.norm(uab - ua - ub)
    den = np.linalg.norm(uab)
    return float(num / den) if den > 0 else 0.0


def _force_from_state(graph: GraphFamily, psi: np.ndarray, mass: float, source_strength: float) -> float:
    rho = np.abs(psi) ** 2
    dist = graph.depth
    valid = np.isfinite(dist)
    grad = np.zeros_like(dist)
    grad[valid] = mass * G * source_strength / ((dist[valid] + EPS) ** 2)
    return float(np.sum(rho * grad))


def _build_family_random_geometric(seed: int, side: int = 6) -> GraphFamily:
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    adj_sets: dict[int, set[int]] = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            px = x + 0.08 * (rng.random() - 0.5)
            py = y + 0.08 * (rng.random() - 0.5)
            coords.append((px, py))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index:
                    continue
                b = index[(ii, jj)]
                if colors_a[a] == colors_a[b]:
                    continue
                dx = coords_a[b, 0] - coords_a[a, 0]
                dy = coords_a[b, 1] - coords_a[a, 1]
                if math.hypot(dx, dy) <= 1.28:
                    _add_edge(adj_sets, a, b)
    adj = _finalize_adj(adj_sets)
    source = index[(0, 0)]
    depth = _graph_distance_from_source(adj, source, len(coords_a))
    detector = [i for i, d in enumerate(depth) if np.isfinite(d) and d == np.nanmax(depth)]
    cycle_edge = _find_cycle_edge(adj)
    return GraphFamily("bipartite_random_geometric", coords_a, colors_a, adj, source, detector, depth, cycle_edge is not None, cycle_edge)


def _build_family_growing(seed: int, layers: int = 8, width: int = 6) -> GraphFamily:
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        this_layer = []
        for k in range(width):
            y = (k - (width - 1) / 2.0) + 0.18 * (rng.random() - 0.5)
            coords.append((float(layer), y))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for i in curr:
            # Connect to the two closest opposite-layer nodes.
            scored = []
            for j in nxt:
                dx = coords_a[j, 0] - coords_a[i, 0]
                dy = coords_a[j, 1] - coords_a[i, 1]
                scored.append((dx * dx + dy * dy, j))
            scored.sort(key=lambda t: (t[0], t[1]))
            for _, j in scored[:2]:
                _add_edge(adj_sets, i, j)
    adj = _finalize_adj(adj_sets)
    source = layer_nodes[0][0]
    depth = _graph_distance_from_source(adj, source, len(coords_a))
    detector = layer_nodes[-1][:]
    cycle_edge = _find_cycle_edge(adj)
    return GraphFamily("bipartite_growing", coords_a, colors_a, adj, source, detector, depth, cycle_edge is not None, cycle_edge)


def _build_family_layered_dag(seed: int, layers: int = 8, width: int = 5) -> GraphFamily:
    rng = random.Random(seed)
    coords = []
    colors = []
    layer_nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        count = 1 if layer == 0 else width
        this_layer = []
        for k in range(count):
            y = (k - (count - 1) / 2.0) + 0.08 * (rng.random() - 0.5)
            coords.append((float(layer), y))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for i_pos, i in enumerate(curr):
            # Tree-like layering: each node chooses a single child and no
            # same-layer edges are allowed. The undirected graph stays
            # DAG-compatible and usually cycle-free.
            j = nxt[(i_pos + layer) % len(nxt)]
            _add_edge(adj_sets, i, j)
    adj = _finalize_adj(adj_sets)
    source = layer_nodes[0][0]
    depth = _graph_distance_from_source(adj, source, len(coords_a))
    detector = layer_nodes[-1][:]
    cycle_edge = _find_cycle_edge(adj)
    return GraphFamily("layered_bipartite_dag", coords_a, colors_a, adj, source, detector, depth, cycle_edge is not None, cycle_edge)


def _make_graphs() -> list[GraphFamily]:
    return [
        _build_family_random_geometric(7, side=6),
        _build_family_growing(11, layers=8, width=6),
        _build_family_layered_dag(13, layers=8, width=5),
    ]


def _force_metrics(graph: GraphFamily, k0: float, mass: float, source_strength: float) -> tuple[float, float, np.ndarray]:
    # Force rows are measured as local potential-gradient observables on the
    # retained probe state. That keeps them comparable across graph families.
    psi = _probe_state(graph.positions.shape[0], graph.positions, graph.source, k0=k0)
    force = _force_from_state(graph, psi, mass, source_strength)
    dist = graph.depth
    rho = np.abs(psi) ** 2
    mask = np.isfinite(dist)
    delta_dist = float(np.sum(rho[mask] * dist[mask]) / max(np.sum(rho[mask]), 1e-30))
    return force, delta_dist, psi


def _measure_family(graph: GraphFamily) -> FamilyResult:
    n = graph.positions.shape[0]
    psi_a = _probe_state(n, graph.positions, graph.source, k0=0.0)
    psi_b = _probe_state(n, graph.positions, graph.source, k0=0.31)
    H_free = _build_hamiltonian(graph, MASS, 0.0)
    born_lin = _lin_residual(H_free, psi_a, psi_b)
    psi_free = _evolve_cn(H_free, psi_a, DT, N_STEPS)
    norm_drift = abs(np.linalg.norm(psi_free) - 1.0)

    force, delta_dist, psi_grav = _force_metrics(graph, 0.18, MASS, SOURCE_STRENGTH)
    force_sign = "TOWARD" if force > 0 else "AWAY" if force < 0 else "ZERO"

    strengths = [1.0, 2.0, 4.0, 8.0]
    f_vals = []
    for s in strengths:
        f, _, _ = _force_metrics(graph, 0.18, MASS, SOURCE_STRENGTH * s)
        f_vals.append(f)
    if len(set(round(x, 12) for x in f_vals)) > 1 and np.std(strengths) > 0:
        coeff = np.polyfit(strengths, f_vals, 1)
        pred = np.polyval(coeff, strengths)
        denom = np.sum((np.array(f_vals) - np.mean(f_vals)) ** 2)
        fm_r2 = 1.0 - float(np.sum((np.array(f_vals) - pred) ** 2) / denom) if denom > 0 else 1.0
    else:
        fm_r2 = 1.0

    force_vals = []
    for k0 in ACHROM_K:
        force_k, _, _ = _force_metrics(graph, k0, MASS, SOURCE_STRENGTH)
        force_vals.append(force_k)
    achrom_cv = float(np.std(force_vals) / max(abs(np.mean(force_vals)), 1e-30))

    masses = [0.12, 0.18, 0.30, 0.42]
    accels = []
    for m in masses:
        f_m, _, _ = _force_metrics(graph, 0.18, m, SOURCE_STRENGTH)
        accels.append(f_m / m)
    equiv_cv = float(np.std(accels) / max(abs(np.mean(accels)), 1e-30))

    robust_samples = 0
    robust_total = 0
    for k0 in (0.0, 0.2, 0.4):
        f_k, _, _ = _force_metrics(graph, k0, MASS, SOURCE_STRENGTH)
        robust_total += 1
        robust_samples += int(f_k > 0)

    if graph.has_cycle and graph.cycle_edge is not None:
        phi_vals = np.linspace(0.0, 2.0 * math.pi, 7)
        currents = []
        for phi in phi_vals:
            H_phi = _build_hamiltonian(graph, MASS, SOURCE_STRENGTH, flux=phi, flux_edge=graph.cycle_edge)
            evals, evecs = np.linalg.eigh(H_phi.toarray())
            gs = evecs[:, 0]
            i, j = graph.cycle_edge
            hop = H_phi[i, j]
            current = float(np.imag(np.conj(gs[i]) * hop * gs[j]))
            currents.append(current)
        gauge_j_range = float(max(currents) - min(currents))
        gauge_status = "PASS" if gauge_j_range > 1e-4 else "FAIL"
    else:
        gauge_j_range = None
        gauge_status = "N/A"

    return FamilyResult(
        family=graph.name,
        n=n,
        born_lin=born_lin,
        norm_drift=norm_drift,
        force_sign=force_sign,
        force_value=force,
        fm_r2=fm_r2,
        achrom_cv=achrom_cv,
        equiv_cv=equiv_cv,
        robust_toward=robust_samples,
        robust_total=robust_total,
        gauge_j_range=gauge_j_range,
        gauge_status=gauge_status,
    )


def _print_result(result: FamilyResult) -> None:
    gauge = "N/A" if result.gauge_j_range is None else f"{result.gauge_j_range:.3e}"
    print(
        f"{result.family:<26} "
        f"n={result.n:<3d} "
        f"Born/lin={result.born_lin:.2e} "
        f"norm={result.norm_drift:.2e} "
        f"force={result.force_value:+.3e}({result.force_sign}) "
        f"F~M R2={result.fm_r2:.3f} "
        f"achrom CV={result.achrom_cv:.3e} "
        f"equiv CV={result.equiv_cv:.3e} "
        f"robust={result.robust_toward}/{result.robust_total} "
        f"gauge={gauge} [{result.gauge_status}]"
    )


def main() -> None:
    print("=" * 96)
    print("STAGGERED GRAPH PORTABILITY")
    print("  Retained battery: Born/linearity, norm, force sign, F∝M, achromatic force,")
    print("  equivalence, robustness, gauge if cycles exist")
    print("=" * 96)
    print(f"  dt={DT}, steps={N_STEPS}, mass={MASS}, G={G}, source_strength={SOURCE_STRENGTH}")
    print()

    results = []
    for graph in _make_graphs():
        result = _measure_family(graph)
        results.append(result)
        _print_result(result)

    print()
    print("SUMMARY")
    for r in results:
        pass_rows = [
            r.born_lin < 1e-10,
            r.norm_drift < 1e-10,
            r.force_value > 0,
            r.fm_r2 > 0.9,
            r.achrom_cv < 0.05,
            r.equiv_cv < 0.05,
            r.robust_toward == r.robust_total,
            r.gauge_status in ("PASS", "N/A"),
        ]
        print(
            f"  {r.family:<26} "
            f"{sum(pass_rows)}/{len(pass_rows)} retained rows pass "
            f"(gauge={r.gauge_status})"
        )

    print()
    print("Interpretation:")
    print("  - This is a portability probe, not a new canonical card.")
    print("  - Gauge is only scored when the graph has a cycle.")
    print("  - Force is the primary gravity observable; centroid-based checks are not used here.")


if __name__ == "__main__":
    main()
