#!/usr/bin/env python3
"""Staggered source-generated backreaction prototype.

Goal:
  Replace an externally imposed gravity potential with a source-generated Phi
  on the same graph, while keeping force as the primary gravity observable.

This is intentionally narrow and retained:
  - source sector -> solve screened graph Poisson for Phi
  - staggered matter -> evolve under V = -m * Phi
  - primary observable -> force F = < -dPhi/dd >
  - controls -> Phi=0, external-kernel Phi, doubled-source response
  - battery -> source-response linearity, two-body additivity, stability across
    graph families

The prototype is not a self-gravitating theory. It is the first honest check of
whether the staggered force result survives when Phi is endogenous to the same
graph instead of being imposed by hand.
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
G = 8.0
SOURCE_SIGMA = 0.90
SOURCE_STRENGTHS = (0.0, 0.25, 0.50, 1.0, 2.0)
POISSON_MU2 = 0.22
EXT_KERNEL_MU = 0.38
EXT_KERNEL_EPS = 0.25
F_TOL = 1e-12
STRONG_TOL = 1e-9


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
class BackreactionResult:
    family: str
    n: int
    zero_phi_norm: float
    zero_force: float
    ext_force: float
    solve_force: float
    force_gap_rel: float
    source_r2: float
    two_body_resid: float
    toward_fraction: int
    toward_total: int
    norm_drift: float
    phi_residual: float
    self_force: float
    self_gap_rel: float


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


def _probe_state(coords: np.ndarray, source: int, sigma: float = 1.15, k0: float = 0.0) -> np.ndarray:
    center = coords[source]
    rel = coords - center
    coord = rel[:, 0] + 0.35 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / (sigma**2)) * np.exp(1j * k0 * coord)
    norm = np.linalg.norm(psi)
    return psi.astype(complex) / norm if norm > 0 else psi.astype(complex)


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


def _build_hamiltonian(graph: GraphFamily, mass: float, phi: np.ndarray) -> csr_matrix:
    n = graph.positions.shape[0]
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(graph.colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity - mass * phi)
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
    if not shell_map:
        return np.array([0.0]), np.array([0.0])
    shells = np.array(sorted(shell_map))
    means = np.array([statistics.fmean(shell_map[int(d)]) for d in shells], dtype=float)
    return shells, means


def _force_from_phi(graph: GraphFamily, psi: np.ndarray, phi: np.ndarray) -> float:
    shells_rho, rho_shell = _shell_values(graph, np.abs(psi) ** 2)
    shells_phi, phi_shell = _shell_values(graph, phi)
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


def _external_phi(graph: GraphFamily, source_nodes: list[int], strengths: list[float]) -> np.ndarray:
    phi = np.zeros(graph.positions.shape[0], dtype=float)
    for s, strength in zip(source_nodes, strengths):
        center = graph.positions[s]
        rel = graph.positions - center
        r = np.sqrt(rel[:, 0] ** 2 + rel[:, 1] ** 2)
        phi += strength * np.exp(-EXT_KERNEL_MU * r) / (r + EXT_KERNEL_EPS)
    return phi


def _make_graphs() -> list[GraphFamily]:
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
        depth = _bfs_depth(adj, source, len(coords_a))
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
        depth = _bfs_depth(adj, source, len(coords_a))
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
                j = nxt[(i_pos + layer) % len(nxt)]
                _add_edge(adj_sets, i, j)
        adj = _finalize_adj(adj_sets)
        source = layer_nodes[0][0]
        depth = _bfs_depth(adj, source, len(coords_a))
        detector = layer_nodes[-1][:]
        cycle_edge = _find_cycle_edge(adj)
        return GraphFamily("layered_bipartite_dag", coords_a, colors_a, adj, source, detector, depth, cycle_edge is not None, cycle_edge)

    return [
        _build_family_random_geometric(7, side=6),
        _build_family_growing(11, layers=8, width=6),
        _build_family_layered_dag(13, layers=8, width=5),
    ]


def _measure_family(graph: GraphFamily) -> BackreactionResult:
    n = graph.positions.shape[0]
    source_nodes = [graph.source]
    source_strengths = [1.0]
    psi0 = _probe_state(graph.positions, graph.source, k0=0.18)

    rho_zero = np.zeros(n, dtype=float)
    phi_zero = _solve_phi(graph, rho_zero)
    H_zero = _build_hamiltonian(graph, MASS, phi_zero)
    psi_zero = _evolve_cn(H_zero, psi0, DT, N_STEPS)
    zero_force = _force_from_phi(graph, psi_zero, phi_zero)
    zero_phi_norm = float(np.linalg.norm(phi_zero))
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    rho_s = _source_density(graph, source_nodes, source_strengths)
    phi_solve = _solve_phi(graph, rho_s)
    phi_ext = _external_phi(graph, source_nodes, source_strengths)

    H_solve = _build_hamiltonian(graph, MASS, phi_solve)
    H_ext = _build_hamiltonian(graph, MASS, phi_ext)
    psi_solve = _evolve_cn(H_solve, psi0, DT, N_STEPS)
    psi_ext = _evolve_cn(H_ext, psi0, DT, N_STEPS)
    force_solve = _force_from_phi(graph, psi_solve, phi_solve)
    force_ext = _force_from_phi(graph, psi_ext, phi_ext)
    force_gap_rel = abs(force_solve - force_ext) / max(abs(force_ext), 1e-30)

    # One-step endogenous update: feed the evolved density back into the same
    # Poisson solve to see whether the force remains stable when Phi is sourced
    # by the state itself rather than by the initial control density.
    rho_self = np.abs(psi_solve) ** 2
    rho_self *= max(np.sum(rho_s), 1e-30) / max(np.sum(rho_self), 1e-30)
    phi_self = _solve_phi(graph, rho_self)
    self_force = _force_from_phi(graph, psi_solve, phi_self)
    self_gap_rel = abs(self_force - force_solve) / max(abs(force_solve), 1e-30)

    strengths = list(SOURCE_STRENGTHS)
    forces = []
    for strength in strengths:
        rho = _source_density(graph, source_nodes, [strength])
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

    # Two-body additivity on the same graph: a pair of separated source blobs
    # should superpose linearly in the screened Poisson solve.
    if len(graph.detector) > 0:
        partner = graph.detector[0]
    else:
        partner = max(range(n), key=lambda i: graph.depth[i] if np.isfinite(graph.depth[i]) else -1)
    rho_a = _source_density(graph, [graph.source], [1.0])
    rho_b = _source_density(graph, [partner], [1.0])
    rho_ab = _source_density(graph, [graph.source, partner], [1.0, 1.0])
    phi_a = _solve_phi(graph, rho_a)
    phi_b = _solve_phi(graph, rho_b)
    phi_ab = _solve_phi(graph, rho_ab)
    denom = max(np.linalg.norm(phi_ab), 1e-30)
    phi_residual = float(np.linalg.norm(phi_ab - (phi_a + phi_b)) / denom)
    psi_ab = _evolve_cn(_build_hamiltonian(graph, MASS, phi_ab), psi0, DT, N_STEPS)
    force_ab = _force_from_phi(graph, psi_ab, phi_ab)
    force_add = _force_from_phi(graph, _evolve_cn(_build_hamiltonian(graph, MASS, phi_a + phi_b), psi0, DT, N_STEPS), phi_a + phi_b)
    two_body_resid = abs(force_ab - force_add) / max(abs(force_ab), 1e-30)

    toward_total = 3
    toward_samples = int(zero_force >= -F_TOL) + int(force_solve > 0) + int(force_ext > 0)

    return BackreactionResult(
        family=graph.name,
        n=n,
        zero_phi_norm=zero_phi_norm,
        zero_force=zero_force,
        ext_force=force_ext,
        solve_force=force_solve,
        force_gap_rel=force_gap_rel,
        source_r2=source_r2,
        two_body_resid=two_body_resid,
        toward_fraction=toward_samples,
        toward_total=toward_total,
        norm_drift=norm_drift,
        phi_residual=phi_residual,
        self_force=self_force,
        self_gap_rel=self_gap_rel,
    )


def _print_result(result: BackreactionResult) -> None:
    print(
        f"{result.family:<26} "
        f"n={result.n:<3d} "
        f"Phi0={result.zero_phi_norm:.2e} "
        f"F0={result.zero_force:+.3e} "
        f"F_ext={result.ext_force:+.3e} "
        f"F_solve={result.solve_force:+.3e} "
        f"gap={result.force_gap_rel:.3e} "
        f"R2={result.source_r2:.4f} "
        f"2body={result.two_body_resid:.3e} "
        f"Phi_add={result.phi_residual:.3e} "
        f"selfF={result.self_force:+.3e} "
        f"self_gap={result.self_gap_rel:.3e} "
        f"norm={result.norm_drift:.2e} "
        f"TOWARD={result.toward_fraction}/{result.toward_total}"
    )


def main() -> None:
    t0 = time.time()
    print("=" * 100)
    print("STAGGERED SOURCE-GENERATED BACKREACTION PROTOTYPE")
    print("  source sector solves a screened graph Poisson field Phi on the same graph")
    print("  matter evolves with V = -m * Phi; force remains the primary observable")
    print("=" * 100)
    print(
        f"dt={DT}, steps={N_STEPS}, mass={MASS}, G={G}, "
        f"source_sigma={SOURCE_SIGMA}, mu2={POISSON_MU2}, ext_mu={EXT_KERNEL_MU}"
    )
    print()

    results: list[BackreactionResult] = []
    for graph in _make_graphs():
        result = _measure_family(graph)
        results.append(result)
        _print_result(result)

    print()
    print("SUMMARY")
    zero_ok = sum(abs(r.zero_force) < 1e-10 and r.zero_phi_norm < 1e-10 for r in results)
    force_ok = sum(r.solve_force > 0 for r in results)
    lin_ok = sum(r.source_r2 > 0.99 for r in results)
    body_ok = sum(r.two_body_resid < 1e-10 for r in results)
    self_ok = sum(r.self_force > 0 for r in results)
    print(f"  zero-source reduction: {zero_ok}/{len(results)} families exact")
    print(f"  source-response linearity: {lin_ok}/{len(results)} families R^2 > 0.99")
    print(f"  two-body additivity: {body_ok}/{len(results)} families residual < 1e-10")
    print(f"  force sign: {force_ok}/{len(results)} families TOWARD")
    print(f"  one-step endogenous backreaction: {self_ok}/{len(results)} families TOWARD")
    print(
        f"  force gap (external vs solved): mean={statistics.fmean(r.force_gap_rel for r in results):.3e}, "
        f"max={max(r.force_gap_rel for r in results):.3e}"
    )
    print(
        f"  self-update gap: mean={statistics.fmean(r.self_gap_rel for r in results):.3e}, "
        f"max={max(r.self_gap_rel for r in results):.3e}"
    )
    print(
        f"  norm drift: mean={statistics.fmean(r.norm_drift for r in results):.3e}, "
        f"max={max(r.norm_drift for r in results):.3e}"
    )
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("Interpretation:")
    print("  - This is a source-generated Phi prototype, not a self-gravity closure.")
    print("  - The key blocker, if any, will be whether the solved Phi stays close")
    print("    to the external-kernel control while preserving the TOWARD force.")
    print("  - The next step, if this survives, is to feed the evolved matter density")
    print("    back into the same Poisson solve for one-step endogenous backreaction.")


if __name__ == "__main__":
    main()
