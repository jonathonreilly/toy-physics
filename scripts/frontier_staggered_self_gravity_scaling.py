#!/usr/bin/env python3
"""
Staggered Self-Gravity Scaling Probe — Retained
================================================

Measure how the endogenous self-gravity contraction scales with graph size on
admissible staggered graph families.

The probe is intentionally narrow:
  - no external source
  - matter density |psi|^2 generates its own Phi
  - Phi acts back through V = -m * Phi
  - force is the primary gravity observable
  - contraction is measured against the corresponding free evolution

Families:
  - random geometric bipartite graphs
  - growing bipartite graphs
  - layered cycle graphs

Per size case we report:
  - final width ratio (self / free)
  - force sign stability across iterations
  - norm drift

The retained question is whether contraction survives as the graph gets larger
and whether the force stays TOWARD without sign flips.
"""

from __future__ import annotations

import math
import random
import time
from collections import deque
from dataclasses import dataclass

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 50.0
N_ITER = 20


@dataclass(frozen=True)
class GraphFamily:
    name: str
    positions: np.ndarray
    colors: np.ndarray
    adj: dict[int, list[int]]
    source: int


@dataclass(frozen=True)
class SizeCase:
    family: str
    label: str
    n: int
    graph: GraphFamily


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


def _laplacian(pos: np.ndarray, adj: dict[int, list[int]], n: int) -> np.ndarray:
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def _solve_phi(laplacian, rho: np.ndarray) -> np.ndarray:
    if np.allclose(rho, 0.0):
        return np.zeros_like(rho)
    A = (laplacian + MU2 * speye(laplacian.shape[0], format="csr")).tocsc()
    return spsolve(A, rho).astype(float)


def _build_hamiltonian(
    pos: np.ndarray,
    colors: np.ndarray,
    adj: dict[int, list[int]],
    n: int,
    mass: float,
    phi: np.ndarray,
):
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity - mass * phi)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _cn_step(H, n: int, psi: np.ndarray) -> np.ndarray:
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def _width(psi: np.ndarray, pos: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    total = float(np.sum(rho))
    if total <= 0:
        return 0.0
    rho /= total
    cx = float(np.sum(rho * pos[:, 0]))
    cy = float(np.sum(rho * pos[:, 1]))
    return float(np.sqrt(np.sum(rho * ((pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2))))


def _shell_force(depth: np.ndarray, max_d: int, n: int, psi: np.ndarray, phi: np.ndarray) -> float:
    if max_d <= 0:
        return 0.0
    rho = np.abs(psi) ** 2
    ps = np.zeros(max_d + 1)
    rs = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(n):
        d_ = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps[d_] += phi[i]
            rs[d_] += rho[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps[d_] /= cnt[d_]
            rs[d_] /= cnt[d_]
    grad = np.zeros(max_d + 1)
    for d_ in range(max_d + 1):
        if d_ == 0:
            grad[d_] = ps[0] - ps[min(1, max_d)]
        elif d_ == max_d:
            grad[d_] = ps[d_ - 1] - ps[d_]
        else:
            grad[d_] = 0.5 * (ps[d_ - 1] - ps[d_ + 1])
    return float(np.sum(rs * grad))


def _gauss_state(pos: np.ndarray, src: int, sigma: float = 1.15) -> np.ndarray:
    center = pos[src]
    rel = pos - center
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / sigma**2).astype(complex)
    norm = np.linalg.norm(psi)
    return psi / norm if norm > 0 else psi


def _make_random_geometric(seed: int, side: int) -> GraphFamily:
    rng = random.Random(seed)
    coords: list[tuple[float, float]] = []
    colors: list[int] = []
    index: dict[tuple[int, int], int] = {}
    adj: dict[int, set[int]] = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5), y + 0.08 * (rng.random() - 0.5)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords, dtype=float)
    col = np.array(colors, dtype=int)
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
                    _add_edge(adj, a, b)
    center = np.array([0.5 * (side - 1), 0.5 * (side - 1)], dtype=float)
    src = int(np.argmin(np.sum((pos - center) ** 2, axis=1)))
    return GraphFamily("random_geometric", pos, col, _finalize_adj(adj), src)


def _make_growing(seed: int, n_target: int) -> GraphFamily:
    rng = random.Random(seed)
    coords: list[tuple[float, float]] = [(0.0, 0.0), (1.0, 0.0)]
    colors: list[int] = [0, 1]
    adj: dict[int, set[int]] = {0: {1}, 1: {0}}
    cur = 2
    while cur < n_target:
        px = rng.uniform(-3, 3)
        py = rng.uniform(-3, 3)
        nc = cur % 2
        coords.append((px, py))
        colors.append(nc)
        opp = [i for i in range(cur) if colors[i] != nc]
        if opp:
            ds = sorted((math.hypot(px - coords[i][0], py - coords[i][1]), i) for i in opp)
            for _, j in ds[: min(4, len(ds))]:
                _add_edge(adj, cur, j)
        cur += 1
    pos = np.array(coords, dtype=float)
    col = np.array(colors, dtype=int)
    return GraphFamily("growing", pos, col, _finalize_adj(adj), 0)


def _make_layered_cycle(seed: int, layers: int, width: int) -> GraphFamily:
    rng = random.Random(seed)
    coords: list[tuple[float, float]] = []
    colors: list[int] = []
    layer_nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        count = max(2, width)
        this_layer: list[int] = []
        for k in range(count):
            y = float(k) + 0.05 * (rng.random() - 0.5)
            coords.append((float(layer), y))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    pos = np.array(coords, dtype=float)
    col = np.array(colors, dtype=int)
    adj: dict[int, set[int]] = {i: set() for i in range(len(pos))}
    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for i_pos, i in enumerate(curr):
            j1 = nxt[i_pos % len(nxt)]
            j2 = nxt[(i_pos + 1) % len(nxt)]
            _add_edge(adj, i, j1)
            _add_edge(adj, i, j2)
    return GraphFamily("layered_cycle", pos, col, _finalize_adj(adj), layer_nodes[0][0])


def _size_cases() -> list[SizeCase]:
    cases: list[SizeCase] = []
    for side in (4, 6, 8, 10):
        graph = _make_random_geometric(seed=42 + side, side=side)
        cases.append(SizeCase("random_geometric", f"side={side}", graph.positions.shape[0], graph))
    for n_target in (16, 36, 64, 100):
        graph = _make_growing(seed=100 + n_target, n_target=n_target)
        cases.append(SizeCase("growing", f"n={n_target}", graph.positions.shape[0], graph))
    for width in (3, 4, 5, 6):
        graph = _make_layered_cycle(seed=200 + width, layers=6, width=width)
        cases.append(SizeCase("layered_cycle", f"layers=6,width={width}", graph.positions.shape[0], graph))
    return cases


def _run_case(case: SizeCase) -> dict[str, float | int | str]:
    graph = case.graph
    n = graph.positions.shape[0]
    lap = _laplacian(graph.positions, graph.adj, n)
    depth = _bfs_depth(graph.adj, graph.source, n)
    max_d = int(np.max(depth[np.isfinite(depth)])) if np.any(np.isfinite(depth)) else 0
    psi_self = _gauss_state(graph.positions, graph.source)
    psi_free = psi_self.copy()
    H_free = _build_hamiltonian(graph.positions, graph.colors, graph.adj, n, MASS, np.zeros(n))

    forces: list[float] = []
    widths_self: list[float] = []
    widths_free: list[float] = []
    norms: list[float] = []

    for _ in range(N_ITER):
        rho = np.abs(psi_self) ** 2
        phi = _solve_phi(lap, G_SELF * rho)
        H = _build_hamiltonian(graph.positions, graph.colors, graph.adj, n, MASS, phi)
        psi_self = _cn_step(H, n, psi_self)
        psi_free = _cn_step(H_free, n, psi_free)
        forces.append(_shell_force(depth, max_d, n, psi_self, phi))
        widths_self.append(_width(psi_self, graph.positions))
        widths_free.append(_width(psi_free, graph.positions))
        norms.append(float(np.linalg.norm(psi_self)))

    ratio = widths_self[-1] / widths_free[-1] if widths_free[-1] > 0 else 1.0
    flips = sum(1 for i in range(len(forces) - 1) if (forces[i] > 0) != (forces[i + 1] > 0))
    toward = sum(1 for f in forces if f > 0)
    norm_drift = max(abs(nm - 1.0) for nm in norms)
    return {
        "family": case.family,
        "label": case.label,
        "n": case.n,
        "width_ratio": ratio,
        "contraction": 1.0 - ratio,
        "toward": toward,
        "steps": N_ITER,
        "flips": flips,
        "norm_drift": norm_drift,
        "min_force": min(forces),
        "max_force": max(forces),
        "final_force": forces[-1],
        "score": int(ratio < 1.0) + int(flips == 0 and toward == N_ITER) + int(norm_drift < 1e-3),
    }


def _fit_trend(rows: list[dict[str, float | int | str]]) -> tuple[float, float]:
    if len(rows) < 2:
        return 0.0, 0.0
    xs = np.asarray([float(r["n"]) for r in rows], dtype=float)
    ys = np.asarray([float(r["width_ratio"]) for r in rows], dtype=float)
    x0 = float(np.mean(xs))
    y0 = float(np.mean(ys))
    denom = float(np.sum((xs - x0) ** 2))
    if denom <= 0:
        return 0.0, 0.0
    slope = float(np.sum((xs - x0) * (ys - y0)) / denom)
    corr = float(np.corrcoef(xs, ys)[0, 1]) if len(xs) >= 2 else 0.0
    return slope, corr


def main() -> None:
    print("=" * 72)
    print("STAGGERED SELF-GRAVITY SCALING PROBE")
    print("=" * 72)
    print(f"G_SELF={G_SELF}, mu2={MU2}, dt={DT}, iterations={N_ITER}")
    print("No external source. |psi|^2 generates its own Phi.")
    print()

    cases = _size_cases()
    results_by_family: dict[str, list[dict[str, float | int | str]]] = {
        "random_geometric": [],
        "growing": [],
        "layered_cycle": [],
    }

    for case in cases:
        row = _run_case(case)
        results_by_family[case.family].append(row)
        print(
            f"{case.family:16s} {case.label:18s} n={case.n:3d} "
            f"width_ratio={row['width_ratio']:.4f} contraction={row['contraction']:.4f} "
            f"force={row['toward']:2d}/{row['steps']} TW flips={row['flips']:2d} "
            f"norm={row['norm_drift']:.2e} score={row['score']}/3"
        )

    print()
    print("=" * 72)
    print("SUMMARY BY FAMILY")
    print("=" * 72)
    for family, rows in results_by_family.items():
        slope, corr = _fit_trend(rows)
        mean_ratio = float(np.mean([float(r["width_ratio"]) for r in rows]))
        min_ratio = float(np.min([float(r["width_ratio"]) for r in rows]))
        max_ratio = float(np.max([float(r["width_ratio"]) for r in rows]))
        min_norm = float(np.max([float(r["norm_drift"]) for r in rows]))
        all_toward = all(int(r["toward"]) == N_ITER for r in rows)
        no_flips = all(int(r["flips"]) == 0 for r in rows)
        print(
            f"{family:16s} mean_ratio={mean_ratio:.4f} range=[{min_ratio:.4f},{max_ratio:.4f}] "
            f"slope={slope:+.3e} corr={corr:+.3f} force_all_TW={all_toward} "
            f"no_flips={no_flips} max_norm_drift={min_norm:.2e}"
        )

    print()
    print("Retained question: does width_ratio stay below 1 and remain stable as graph size grows?")


if __name__ == "__main__":
    main()
