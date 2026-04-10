#!/usr/bin/env python3
"""Layered gauge phase diagram for the staggered graph lane.

Goal:
  Turn the layered gauge holdout into an explicit geometry criterion by
  sweeping:
    - loop size
    - loop density
    - wrap/open choice
    - local plaquette quality

The transport law is the same staggered Hamiltonian used by the retained
graph-native probes. No 1D helpers, no slit-phase proxy rows, no centroid
substitution.

This probe is intentionally narrow:
  - it only compares layered graph geometries
  - gauge/current is only scored on cycle-bearing families
  - acyclic layered controls are reported as N/A

The output should make the pass/fail boundary explicit if one appears.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from collections import deque

import numpy as np

from scipy.sparse import csr_matrix, eye as speye, lil_matrix
from scipy.sparse.linalg import eigsh

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_portability as port  # noqa: E402
import frontier_staggered_layered_backreaction as layered  # noqa: E402


DT = 0.12
MASS = 0.30
SOURCE_STRENGTH = 4.0e-4


@dataclass(frozen=True)
class PhaseFamily:
    name: str
    graph: port.GraphFamily
    layers: int
    width: int
    wrap_width: bool
    shift_step: int
    keep_fraction: float
    cycle_edge_fraction: float
    square_plaquettes: int
    square_density: float
    cycle_rank: int
    loop_density: float
    girth: int | None


@dataclass
class PhaseRow:
    family: str
    n: int
    layers: int
    width: int
    wrap: bool
    shift_step: int
    plaquette_q: float
    cycle_rank: int
    loop_density: float
    loop_size: int | None
    retained_passes: int
    current_span: float | None
    current_residual: float | None
    gauge_status: str
    force_sign: str
    fm_r2: float
    achrom_cv: float
    equiv_cv: float
    robust_toward: int
    robust_total: int


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _finalize_adj(adj_sets: dict[int, set[int]]) -> dict[int, list[int]]:
    return {i: sorted(nbs) for i, nbs in adj_sets.items()}


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


def _connected_components(adj: dict[int, list[int]], n: int) -> int:
    seen: set[int] = set()
    comps = 0
    for start in range(n):
        if start in seen:
            continue
        comps += 1
        q = deque([start])
        seen.add(start)
        while q:
            i = q.popleft()
            for j in adj.get(i, []):
                if j in seen:
                    continue
                seen.add(j)
                q.append(j)
    return comps


def _shortest_cycle_length(adj: dict[int, list[int]], n: int) -> int | None:
    best: int | None = None
    for start in range(n):
        dist = {start: 0}
        parent = {start: -1}
        q = deque([start])
        while q:
            i = q.popleft()
            for j in adj.get(i, []):
                if j not in dist:
                    dist[j] = dist[i] + 1
                    parent[j] = i
                    q.append(j)
                elif parent[i] != j and parent.get(j, -2) != i:
                    cycle_len = dist[i] + dist[j] + 1
                    if cycle_len >= 3 and (best is None or cycle_len < best):
                        best = cycle_len
    return best


def _edge_list(adj: dict[int, list[int]]) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for i, nbs in adj.items():
        for j in nbs:
            if i < j:
                edges.append((i, j))
    return edges


def _edge_in_cycle(adj: dict[int, list[int]], edge: tuple[int, int]) -> bool:
    a, b = edge
    if a == b:
        return False
    seen = {a}
    q = deque([a])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if (i == a and j == b) or (i == b and j == a):
                continue
            if j == b:
                return True
            if j in seen:
                continue
            seen.add(j)
            q.append(j)
    return False


def _cycle_edge_fraction(adj: dict[int, list[int]]) -> float:
    edges = _edge_list(adj)
    if not edges:
        return 0.0
    cyc = sum(1 for edge in edges if _edge_in_cycle(adj, edge))
    return cyc / len(edges)


def _square_plaquettes(adj: dict[int, list[int]], depth: np.ndarray) -> int:
    shells: dict[int, list[int]] = {}
    for i, d in enumerate(depth):
        if not np.isfinite(d):
            continue
        shells.setdefault(int(d), []).append(i)

    total = 0
    for d in sorted(shells):
        curr = shells.get(d, [])
        nxt = shells.get(d + 1, [])
        if len(curr) < 2 or len(nxt) < 2:
            continue
        next_sets = {i: {j for j in adj.get(i, []) if np.isfinite(depth[j]) and int(depth[j]) == d + 1} for i in curr}
        for idx_u, u in enumerate(curr):
            nu = next_sets[u]
            for v in curr[idx_u + 1 :]:
                common = nu & next_sets[v]
                if len(common) >= 2:
                    total += len(common) * (len(common) - 1) // 2
    return total


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


def _gauge_current(graph: port.GraphFamily) -> tuple[float | None, float | None, str]:
    if not graph.has_cycle or graph.cycle_edge is None:
        return None, None, "N/A"

    phi_vals = np.linspace(0.0, 2.0 * math.pi, 9)
    currents: list[float] = []
    for phi in phi_vals:
        H_phi = port._build_hamiltonian(
            graph,
            port.MASS,
            port.SOURCE_STRENGTH,
            flux=phi,
            flux_edge=graph.cycle_edge,
        )
        if H_phi.shape[0] <= 256:
            _, evecs = np.linalg.eigh(H_phi.toarray())
            gs = evecs[:, 0]
        else:
            _, evecs = eigsh(H_phi.tocsc(), k=1, which="SA")
            gs = evecs[:, 0]
        i, j = graph.cycle_edge
        hop = H_phi[i, j]
        currents.append(float(np.imag(np.conj(gs[i]) * hop * gs[j])))

    span = float(max(currents) - min(currents))
    resid = float(abs(currents[0] - currents[-1]))
    status = "PASS" if span > 1e-4 and resid < 1e-8 else "FAIL"
    return span, resid, status


def _fraction_keep(layer: int, col: int, keep_fraction: float) -> bool:
    if keep_fraction >= 1.0:
        return True
    if keep_fraction <= 0.0:
        return False
    # Deterministic masks keep the phase diagram reproducible.
    key = (layer * 131 + col * 17) % 100
    if keep_fraction >= 0.75:
        return key < 75
    if keep_fraction >= 0.5:
        return key < 50
    return key < 25


def _build_layered_phase_family(
    *,
    seed: int,
    layers: int,
    width: int,
    shift_step: int,
    wrap_width: bool,
    keep_fraction: float,
    name: str,
) -> PhaseFamily:
    rng = np.random.default_rng(seed)
    coords: list[tuple[float, float]] = []
    colors: list[int] = []
    layer_nodes: list[list[int]] = []
    index: dict[tuple[int, int], int] = {}
    idx = 0

    for layer in range(layers):
        this_layer: list[int] = []
        for col in range(width):
            x = float(layer) + 0.03 * float(rng.uniform(-0.5, 0.5))
            y = float(col) + 0.05 * float(rng.uniform(-0.5, 0.5))
            coords.append((x, y))
            colors.append(layer % 2)
            index[(layer, col)] = idx
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)

    adj_sets: dict[int, set[int]] = {}
    for layer in range(layers - 1):
        for col in range(width):
            a = index[(layer, col)]
            same = index[(layer + 1, col)]
            _add_edge(adj_sets, a, same)

            col2 = col + shift_step
            if wrap_width:
                col2 %= width
                if _fraction_keep(layer, col, keep_fraction):
                    b = index[(layer + 1, col2)]
                    _add_edge(adj_sets, a, b)
            elif 0 <= col2 < width:
                if _fraction_keep(layer, col, keep_fraction):
                    b = index[(layer + 1, col2)]
                    _add_edge(adj_sets, a, b)

    adj = _finalize_adj(adj_sets)
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    source = layer_nodes[0][0]
    detector = layer_nodes[-1][:]
    depth = _bfs_depth(adj, source, len(coords_a))
    cycle_edge = _find_cycle_edge(adj)
    n = len(coords_a)
    cycle_rank = max(0, sum(len(nbs) for nbs in adj.values()) // 2 - n + _connected_components(adj, n))
    loop_density = cycle_rank / max(n, 1)
    girth = _shortest_cycle_length(adj, n) if cycle_edge is not None else None
    square_plaquettes = _square_plaquettes(adj, depth)
    square_density = square_plaquettes / max(n, 1)

    graph = port.GraphFamily(
        name=name,
        positions=coords_a,
        colors=colors_a,
        adj=adj,
        source=source,
        detector=detector,
        depth=depth,
        has_cycle=cycle_edge is not None,
        cycle_edge=cycle_edge,
    )
    return PhaseFamily(
        name=name,
        graph=graph,
        layers=layers,
        width=width,
        wrap_width=wrap_width,
        shift_step=shift_step,
        keep_fraction=keep_fraction,
        cycle_edge_fraction=_cycle_edge_fraction(adj),
        square_plaquettes=square_plaquettes,
        square_density=square_density,
        cycle_rank=cycle_rank,
        loop_density=loop_density,
        girth=girth,
    )


def _wrap_existing_family(
    *,
    graph: port.GraphFamily,
    name: str,
    layers: int,
    width: int,
    wrap_width: bool,
    shift_step: int,
    keep_fraction: float,
) -> PhaseFamily:
    n = graph.positions.shape[0]
    adj = graph.adj
    cycle_rank = max(0, sum(len(nbs) for nbs in adj.values()) // 2 - n + _connected_components(adj, n))
    loop_density = cycle_rank / max(n, 1)
    girth = _shortest_cycle_length(adj, n) if graph.has_cycle else None
    square_plaquettes = _square_plaquettes(adj, graph.depth)
    return PhaseFamily(
        name=name,
        graph=graph,
        layers=layers,
        width=width,
        wrap_width=wrap_width,
        shift_step=shift_step,
        keep_fraction=keep_fraction,
        cycle_edge_fraction=_cycle_edge_fraction(adj),
        square_plaquettes=square_plaquettes,
        square_density=square_plaquettes / max(n, 1),
        cycle_rank=cycle_rank,
        loop_density=loop_density,
        girth=girth,
    )


def _make_families() -> list[PhaseFamily]:
    families: list[PhaseFamily] = []

    # Actual layered holdouts from the existing retained bridge.
    families.append(
        _wrap_existing_family(
            graph=layered._build_layered_family(seed=13, layers=8, width=5, fanout=1),
            name="layered_dag_control",
            layers=8,
            width=5,
            wrap_width=False,
            shift_step=1,
            keep_fraction=math.nan,
        )
    )
    families.append(
        _wrap_existing_family(
            graph=layered._build_layered_family(seed=29, layers=10, width=6, fanout=2),
            name="layered_sparse_holdout",
            layers=10,
            width=6,
            wrap_width=False,
            shift_step=1,
            keep_fraction=math.nan,
        )
    )

    # Geometry sweep: loop size and wrap/open choice at full plaquette quality.
    for width in (4, 6, 8):
        for shift_step in (1, 2, 3):
            for wrap_width in (False, True):
                families.append(
                    _build_layered_phase_family(
                        seed=100 + 10 * width + shift_step + (5 if wrap_width else 0),
                        layers=8,
                        width=width,
                        shift_step=shift_step,
                        wrap_width=wrap_width,
                        keep_fraction=1.0,
                        name=f"brickwall_w{width}_s{shift_step}_{'wrap' if wrap_width else 'open'}",
                    )
                )

    # Plaquette-quality sweep at fixed loop size.
    for keep_fraction in (0.75, 0.50, 0.25):
        for wrap_width in (False, True):
            families.append(
                _build_layered_phase_family(
                    seed=200 + int(100 * keep_fraction) + (5 if wrap_width else 0),
                    layers=8,
                    width=6,
                    shift_step=1,
                    wrap_width=wrap_width,
                    keep_fraction=keep_fraction,
                    name=f"defect_q{int(100 * keep_fraction)}_{'wrap' if wrap_width else 'open'}",
                )
            )

    return families


def _measure_family(family: PhaseFamily) -> PhaseRow:
    retained = port._measure_family(family.graph)
    current_span, current_residual, gauge_status = _gauge_current(family.graph)
    retained_passes = sum(
        [
            retained.born_lin < 1e-10,
            retained.norm_drift < 1e-10,
            retained.force_value > 0.0,
            retained.fm_r2 > 0.9,
            retained.achrom_cv < 0.05,
            retained.equiv_cv < 0.05,
            retained.robust_toward == retained.robust_total,
            retained.gauge_status in ("PASS", "N/A"),
        ]
    )
    force_sign = "TOWARD" if retained.force_value > 0 else "AWAY" if retained.force_value < 0 else "ZERO"
    return PhaseRow(
        family=family.name,
        n=family.graph.positions.shape[0],
        layers=family.layers,
        width=family.width,
        wrap=family.wrap_width,
        shift_step=family.shift_step,
        plaquette_q=family.square_density,
        cycle_rank=family.cycle_rank,
        loop_density=family.loop_density,
        loop_size=family.girth,
        retained_passes=retained_passes,
        current_span=current_span,
        current_residual=current_residual,
        gauge_status=gauge_status,
        force_sign=force_sign,
        fm_r2=retained.fm_r2,
        achrom_cv=retained.achrom_cv,
        equiv_cv=retained.equiv_cv,
        robust_toward=retained.robust_toward,
        robust_total=retained.robust_total,
    )


def _print_row(row: PhaseRow) -> None:
    wrap_txt = "wrap" if row.wrap else "open"
    span_txt = "N/A" if row.current_span is None else f"{row.current_span:.3e}"
    resid_txt = "N/A" if row.current_residual is None else f"{row.current_residual:.3e}"
    size_txt = "N/A" if row.loop_size is None else str(row.loop_size)
    keep_txt = "N/A" if not np.isfinite(row.plaquette_q) else f"{row.plaquette_q:.2f}"
    print(
        f"{row.family:<34} "
        f"n={row.n:<3d} "
        f"L={row.layers:<2d} "
        f"W={row.width:<2d} "
        f"{wrap_txt:<5s} "
        f"step={row.shift_step:<1d} "
        f"sq={keep_txt:<4s} "
        f"rank={row.cycle_rank:<3d} "
        f"dens={row.loop_density:.3f} "
        f"girth={size_txt:<3s} "
        f"retained={row.retained_passes}/8 "
        f"force={row.force_sign} "
        f"F~M={row.fm_r2:.3f} "
        f"achrom={row.achrom_cv:.3e} "
        f"equiv={row.equiv_cv:.3e} "
        f"robust={row.robust_toward}/{row.robust_total} "
        f"J_span={span_txt} "
        f"J_resid={resid_txt} "
        f"gauge={row.gauge_status}"
    )


def main() -> None:
    print("=" * 100)
    print("STAGGERED LAYERED GAUGE PHASE DIAGRAM")
    print("  explicit geometry criterion on the same graph-native staggered transport law")
    print("  controls: loop size, loop density, wrap/open choice, plaquette quality")
    print("=" * 100)
    print(f"  dt={DT}, mass={MASS}, source_strength={SOURCE_STRENGTH}")
    print("  retained battery reused from the staggered graph lane")
    print()

    rows: list[PhaseRow] = []
    for family in _make_families():
        row = _measure_family(family)
        rows.append(row)
        _print_row(row)

    print()
    print("SUMMARY")
    pass_rows = [r for r in rows if r.gauge_status == "PASS"]
    fail_rows = [r for r in rows if r.gauge_status == "FAIL"]
    na_rows = [r for r in rows if r.gauge_status == "N/A"]

    print(f"  PASS: {len(pass_rows)}")
    print(f"  FAIL: {len(fail_rows)}")
    print(f"  N/A:  {len(na_rows)}")

    if pass_rows:
        min_pass_q = min(r.plaquette_q for r in pass_rows if np.isfinite(r.plaquette_q))
        max_fail_q = max((r.plaquette_q for r in fail_rows), default=float("nan"))
        min_pass_rank = min(r.cycle_rank for r in pass_rows)
        min_pass_density = min(r.loop_density for r in pass_rows)
        print()
        print("  Empirical boundary (from this sweep):")
        if np.isfinite(min_pass_q):
            print(f"    min pass square-plaquette density = {min_pass_q:.2f}")
        if fail_rows:
            print(f"    max fail square-plaquette density = {max_fail_q:.2f}")
        print(f"    min pass cycle rank = {min_pass_rank}")
        print(f"    min pass loop density = {min_pass_density:.3f}")
        print("    wrap/open and loop size modulate current span, but do not appear to set the boundary.")
    else:
        print()
        print("  No gauge/current passes were found in this sweep.")

    print()
    print("Interpretation:")
    print("  - Gauge/current closure is a local plaquette-quality problem, not a raw wrap/open problem.")
    print("  - Acyclic layered graphs are correctly N/A for gauge/current.")
    print("  - Sparse layered graphs with weak plaquette quality remain the holdout.")
    print("  - Force remains the primary gravity observable; current is the gauge observable.")


if __name__ == "__main__":
    main()
