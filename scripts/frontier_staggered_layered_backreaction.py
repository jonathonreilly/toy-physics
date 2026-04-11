#!/usr/bin/env python3
"""Staggered layered backreaction bridge.

Goal:
  Combine the staggered transport law with a source-generated Phi on a layered,
  DAG-compatible graph family.

Minimum deliverable:
  - zero-source control
  - source-on response
  - one stability / robustness check on a layered or DAG-compatible graph

Observable:
  - force F = -<dPhi/dd> is primary

This is intentionally narrow. It is not a self-gravity closure.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
import time
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
POISSON_MU2 = 0.22
SOURCE_SIGMA = 0.85
SOURCE_STRENGTHS = (0.0, 0.25, 0.50, 1.0, 2.0)
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
class BridgeResult:
    family: str
    n: int
    zero_phi_norm: float
    zero_force: float
    source_force: float
    source_r2: float
    phi_residual: float
    norm_drift: float
    robustness_toward: int
    robustness_total: int
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
    state: dict[int, int] = {}

    def dfs(node: int, prev: int | None) -> tuple[int, int] | None:
        state[node] = 1
        for nb in adj.get(node, []):
            if nb == prev:
                continue
            if nb not in state:
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


def _build_layered_family(seed: int, layers: int, width: int, fanout: int) -> GraphFamily:
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
            x = float(layer) + 0.04 * (rng.random() - 0.5)
            coords.append((x, y))
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
            # Keep the graph layered and bipartite: only connect forward.
            j = nxt[(i_pos + layer) % len(nxt)]
            _add_edge(adj_sets, i, j)
            if fanout > 1 and len(nxt) > 2 and (i_pos + layer) % 3 == 0:
                j2 = nxt[(i_pos + layer + 1) % len(nxt)]
                _add_edge(adj_sets, i, j2)

    adj = _finalize_adj(adj_sets)
    source = layer_nodes[0][0]
    depth = _bfs_depth(adj, source, len(coords_a))
    detector = layer_nodes[-1][:]
    cycle_edge = _find_cycle_edge(adj)
    return GraphFamily(
        name=f"layered_bipartite_dag_s{seed}_n{len(coords_a)}",
        positions=coords_a,
        colors=colors_a,
        adj=adj,
        source=source,
        detector=detector,
        depth=depth,
        has_cycle=cycle_edge is not None,
        cycle_edge=cycle_edge,
    )


def _graph_laplacian(graph: GraphFamily) -> csr_matrix:
    n = graph.positions.shape[0]
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in graph.adj.items():
        diag = 0.0
        for j in nbs:
            if i >= j:
                continue
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist = math.hypot(dx, dy)
            w = 1.0 / max(dist, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            diag += w
            L[j, j] += w
        L[i, i] += diag
    return L.tocsr()


def _probe_state(coords: np.ndarray, source: int, sigma: float = 0.95, k0: float = 0.0) -> np.ndarray:
    center = coords[source]
    rel = coords - center
    coord = rel[:, 0] + 0.35 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / (sigma**2)) * np.exp(1j * k0 * coord)
    norm = np.linalg.norm(psi)
    return psi.astype(complex) / norm if norm > 0 else psi.astype(complex)


def _source_density(graph: GraphFamily, source_nodes: list[int], strengths: list[float]) -> np.ndarray:
    rho = np.zeros(graph.positions.shape[0], dtype=float)
    for s, strength in zip(source_nodes, strengths):
        center = graph.positions[s]
        rel = graph.positions - center
        w = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / (SOURCE_SIGMA**2))
        w /= max(np.sum(w), 1e-30)
        rho += strength * w
    return rho


def _solve_phi(graph: GraphFamily, rho: np.ndarray) -> np.ndarray:
    if np.allclose(rho, 0.0):
        return np.zeros_like(rho)
    L = _graph_laplacian(graph)
    A = (L + POISSON_MU2 * speye(L.shape[0], format="csr")).tocsc()
    return spsolve(A, rho).astype(float)


def _build_hamiltonian(graph: GraphFamily, mass: float, phi: np.ndarray) -> csr_matrix:
    n = graph.positions.shape[0]
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(graph.colors == 0, 1.0, -1.0)
    # Parity (scalar 1⊗1) coupling: Φ modulates mass gap via ε(x).
    H.setdiag((mass + phi) * parity)
    for i, nbs in graph.adj.items():
        for j in nbs:
            if i >= j:
                continue
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist = math.hypot(dx, dy)
            w = 1.0 / max(dist, 0.5)
            hop = -0.5j * w
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


def _shell_values(graph: GraphFamily, values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    shell_map: dict[int, list[float]] = {}
    for i, d in enumerate(graph.depth):
        if not np.isfinite(d):
            continue
        shell_map.setdefault(int(d), []).append(float(values[i]))
    shells = np.array(sorted(shell_map), dtype=int) if shell_map else np.array([0], dtype=int)
    means = np.array([statistics.fmean(shell_map[int(d)]) for d in shells], dtype=float) if shell_map else np.array([0.0])
    return shells, means


def _force_from_phi(graph: GraphFamily, psi: np.ndarray, phi: np.ndarray) -> float:
    shells_rho, rho_shell = _shell_values(graph, np.abs(psi) ** 2)
    shells_phi, phi_shell = _shell_values(graph, phi)
    if shells_rho.size == 0 or shells_phi.size == 0:
        return 0.0
    max_shell = min(int(shells_rho[-1]), int(shells_phi[-1]))
    if max_shell <= 0:
        return 0.0

    phi_by_depth = np.zeros(max_shell + 1, dtype=float)
    rho_by_depth = np.zeros(max_shell + 1, dtype=float)
    for d, v in zip(shells_phi.astype(int), phi_shell):
        if d <= max_shell:
            phi_by_depth[d] = v
    for d, v in zip(shells_rho.astype(int), rho_shell):
        if d <= max_shell:
            rho_by_depth[d] = v

    grad_toward = np.zeros(max_shell + 1, dtype=float)
    for d in range(max_shell + 1):
        if max_shell == 0:
            grad_toward[d] = 0.0
        elif d == 0:
            grad_toward[d] = phi_by_depth[0] - phi_by_depth[1]
        elif d == max_shell:
            grad_toward[d] = phi_by_depth[d - 1] - phi_by_depth[d]
        else:
            grad_toward[d] = 0.5 * (phi_by_depth[d - 1] - phi_by_depth[d + 1])
    return float(np.sum(rho_by_depth * grad_toward))


def _measure_family(graph: GraphFamily) -> BridgeResult:
    n = graph.positions.shape[0]
    psi0 = _probe_state(graph.positions, graph.source, k0=0.18)

    # Zero-source control.
    rho0 = np.zeros(n, dtype=float)
    phi0 = _solve_phi(graph, rho0)
    H0 = _build_hamiltonian(graph, MASS, phi0)
    psi_zero = _evolve_cn(H0, psi0, DT, N_STEPS)
    zero_force = _force_from_phi(graph, psi_zero, phi0)
    zero_phi_norm = float(np.linalg.norm(phi0))
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    # Source-on response.
    rho1 = _source_density(graph, [graph.source], [1.0])
    phi1 = _solve_phi(graph, rho1)
    H1 = _build_hamiltonian(graph, MASS, phi1)
    psi1 = _evolve_cn(H1, psi0, DT, N_STEPS)
    source_force = _force_from_phi(graph, psi1, phi1)
    phi_residual = float(np.linalg.norm((_graph_laplacian(graph) + POISSON_MU2 * speye(n, format="csr")).dot(phi1) - rho1) / max(np.linalg.norm(rho1), 1e-30))

    # Source linearity / robustness sweep.
    strengths = list(SOURCE_STRENGTHS)
    forces = []
    for s in strengths:
        rho = _source_density(graph, [graph.source], [s])
        phi = _solve_phi(graph, rho)
        psi = _evolve_cn(_build_hamiltonian(graph, MASS, phi), psi0, DT, N_STEPS)
        forces.append(_force_from_phi(graph, psi, phi))
    f_arr = np.asarray(forces, dtype=float)
    s_arr = np.asarray(strengths, dtype=float)
    if np.sum((f_arr - np.mean(f_arr)) ** 2) > 0:
        coeff = np.polyfit(s_arr, f_arr, 1)
        pred = np.polyval(coeff, s_arr)
        source_r2 = 1.0 - float(np.sum((f_arr - pred) ** 2) / np.sum((f_arr - np.mean(f_arr)) ** 2))
    else:
        source_r2 = 1.0

    # Stability check across a tiny local perturbation family: source and
    # one nearby support node both need to keep the sign TOWARD.
    support = graph.detector[0] if graph.detector else graph.source
    rho_support = _source_density(graph, [graph.source, support], [1.0, 0.5])
    phi_support = _solve_phi(graph, rho_support)
    psi_support = _evolve_cn(_build_hamiltonian(graph, MASS, phi_support), psi0, DT, N_STEPS)
    support_force = _force_from_phi(graph, psi_support, phi_support)
    robustness_toward = int(zero_force >= -F_TOL) + int(source_force > 0) + int(support_force > 0)
    robustness_total = 3

    if graph.has_cycle and graph.cycle_edge is not None:
        phi_vals = np.linspace(0.0, 2.0 * math.pi, 7)
        currents = []
        for phi in phi_vals:
            H_phi = _build_hamiltonian(graph, MASS, phi1)
            i, j = graph.cycle_edge
            H_phi = H_phi.tolil()
            phase = np.exp(1j * phi)
            H_phi[i, j] *= phase
            H_phi[j, i] = np.conj(H_phi[i, j])
            evals, evecs = np.linalg.eigh(H_phi.toarray())
            gs = evecs[:, 0]
            hop = H_phi[i, j]
            currents.append(float(np.imag(np.conj(gs[i]) * hop * gs[j])))
        gauge_status = "PASS" if (max(currents) - min(currents)) > 1e-4 else "FAIL"
    else:
        gauge_status = "N/A"

    return BridgeResult(
        family=graph.name,
        n=n,
        zero_phi_norm=zero_phi_norm,
        zero_force=zero_force,
        source_force=source_force,
        source_r2=source_r2,
        phi_residual=phi_residual,
        norm_drift=norm_drift,
        robustness_toward=robustness_toward,
        robustness_total=robustness_total,
        gauge_status=gauge_status,
    )


def _print_result(result: BridgeResult) -> None:
    print(
        f"{result.family:<32} "
        f"n={result.n:<3d} "
        f"Phi0={result.zero_phi_norm:.2e} "
        f"F0={result.zero_force:+.3e} "
        f"F1={result.source_force:+.3e} "
        f"R2={result.source_r2:.4f} "
        f"Phi_res={result.phi_residual:.2e} "
        f"norm={result.norm_drift:.2e} "
        f"robust={result.robustness_toward}/{result.robustness_total} "
        f"gauge={result.gauge_status}"
    )


def main() -> None:
    t0 = time.time()
    print("=" * 96)
    print("STAGGERED LAYERED BACKREACTION BRIDGE")
    print("  zero-source control + source-on response on layered/DAG-compatible graphs")
    print("  primary observable: force F = -<dPhi/dd>")
    print("=" * 96)
    print(f"dt={DT}, steps={N_STEPS}, mass={MASS}, mu2={POISSON_MU2}, source_sigma={SOURCE_SIGMA}")
    print()

    graphs = [
        _build_layered_family(seed=13, layers=8, width=5, fanout=1),
        _build_layered_family(seed=29, layers=10, width=6, fanout=2),
    ]

    results: list[BridgeResult] = []
    for graph in graphs:
        result = _measure_family(graph)
        results.append(result)
        _print_result(result)

    print()
    print("SUMMARY")
    zero_ok = sum(abs(r.zero_force) < 1e-10 and r.zero_phi_norm < 1e-10 for r in results)
    source_ok = sum(r.source_force > 0 for r in results)
    r2_ok = sum(r.source_r2 > 0.99 for r in results)
    robust_ok = sum(r.robustness_toward == r.robustness_total for r in results)
    print(f"  zero-source control exact: {zero_ok}/{len(results)}")
    print(f"  source-on response TOWARD: {source_ok}/{len(results)}")
    print(f"  source linearity R^2 > 0.99: {r2_ok}/{len(results)}")
    print(f"  robustness (zero+source+support): {robust_ok}/{len(results)}")
    print(
        f"  norm drift: mean={statistics.fmean(r.norm_drift for r in results):.3e}, "
        f"max={max(r.norm_drift for r in results):.3e}"
    )
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("Interpretation:")
    print("  - This is the first layered/DAG-compatible backreaction bridge, not a")
    print("    self-gravity closure.")
    print("  - The retained observable is force, not centroid shift.")
    print("  - If the source-on force survives larger graph families, the next step is")
    print("    to replace the point-source approximation with a graph-solved source")
    print("    sector that is fed by the evolving matter density.")


if __name__ == "__main__":
    main()
