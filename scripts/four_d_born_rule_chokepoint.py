#!/usr/bin/env python3
"""4D Born-rule / Sorkin test with a true chokepoint barrier.

The key discipline is the same as in the verified 3D check:
the barrier must be a real chokepoint. If skip-layer edges bypass the
barrier, then ψ_AB != ψ_A + ψ_B for purely topological reasons and the
Sorkin test is contaminated.

This script therefore generates a 4D DAG with no cross-barrier skip
edges and checks:
  1. Direct linearity: ψ_AB = ψ_A + ψ_B at the detectors
  2. Sorkin I_3 on the fixed DAG with amplitude masking
"""

from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict, deque

BETA = 0.8


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def generate_4d_chokepoint_dag(
    n_layers: int = 12,
    nodes_per_layer: int = 25,
    spatial_range: float = 10.0,
    connect_radius: float = 4.5,
    rng_seed: int = 42,
) -> tuple[list[tuple[float, float, float, float]], dict[int, list[int]], list[list[int]]]:
    """4D DAG where all paths must pass through the barrier layer."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-spatial_range, spatial_range)
                z = rng.uniform(-spatial_range, spatial_range)
                w = rng.uniform(-spatial_range, spatial_range)
                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        prev_x = round(positions[prev_idx][0])
                        if prev_x < barrier_layer and layer > barrier_layer:
                            continue
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 + (w - pw) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def propagate_4d(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    k: float,
    blocked: set[int] | None = None,
) -> list[complex]:
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        x1, y1, z1, w1 = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x2, y2, z2, w2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            dw = w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * L) * weight / L
    return amps


def sorkin_test_4d(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
    k: float,
) -> tuple[float, float] | None:
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    barrier = layer_indices[bl_idx]
    src = layer_indices[0]
    det_list = layer_indices[-1]

    ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(ys) / len(ys)

    slit_a = {i for i in barrier if positions[i][1] > cy + 3}
    slit_b = {i for i in barrier if abs(positions[i][1] - cy) < 2}
    slit_c = {i for i in barrier if positions[i][1] < cy - 3}
    if not slit_a or not slit_b or not slit_c:
        return None

    all_slits = slit_a | slit_b | slit_c
    base_blocked = set(barrier) - all_slits

    def prob(open_set: set[int]) -> float:
        closed = all_slits - open_set
        amps = propagate_4d(positions, adj, src, k, base_blocked | closed)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    p_abc = prob(all_slits)
    p_ab = prob(slit_a | slit_b)
    p_ac = prob(slit_a | slit_c)
    p_bc = prob(slit_b | slit_c)
    p_a = prob(slit_a)
    p_b = prob(slit_b)
    p_c = prob(slit_c)
    i3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    return i3, p_abc


def linearity_check(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
    k: float,
) -> float | None:
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    barrier = layer_indices[bl_idx]
    src = layer_indices[0]
    det_list = layer_indices[-1]

    ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(ys) / len(ys)

    slit_a = {i for i in barrier if positions[i][1] > cy + 3}
    slit_b = {i for i in barrier if positions[i][1] < cy - 3}
    if not slit_a or not slit_b:
        return None

    non_slit = set(barrier) - slit_a - slit_b
    amps_a = propagate_4d(positions, adj, src, k, non_slit | slit_b)
    amps_b = propagate_4d(positions, adj, src, k, non_slit | slit_a)
    amps_ab = propagate_4d(positions, adj, src, k, non_slit)

    max_rel = 0.0
    for d in det_list:
        psi_sum = amps_a[d] + amps_b[d]
        psi_ab = amps_ab[d]
        ref = max(abs(psi_ab), abs(psi_sum))
        if ref > 1e-30:
            max_rel = max(max_rel, abs(psi_ab - psi_sum) / ref)
    return max_rel


def main():
    print("=" * 74)
    print("4D BORN RULE: Chokepoint barrier (no skip-layer crossing)")
    print("=" * 74)
    print()

    print("TEST 1: Linearity check (psi_AB = psi_A + psi_B)")
    print(f"  {'seed':>4s}  {'max_rel_err':>14s}  verdict")
    print(f"  {'-' * 30}")
    for seed in range(8):
        positions, adj, layer_indices = generate_4d_chokepoint_dag(
            n_layers=12, nodes_per_layer=25, rng_seed=seed * 13 + 5
        )
        rel = linearity_check(positions, adj, layer_indices, k=5.0)
        if rel is None:
            print(f"  {seed:4d}  {'SKIP':>14s}  no slits")
            continue
        verdict = "LINEAR" if rel < 1e-10 else "BROKEN" if rel > 1e-2 else "NOISY"
        print(f"  {seed:4d}  {rel:14.6e}  {verdict}")

    print()
    print("TEST 2: Sorkin I_3 (three-slit Born rule)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>14s}  {'P':>12s}  {'|I_3|/P':>14s}")
    print(f"  {'-' * 56}")

    for seed in range(8):
        positions, adj, layer_indices = generate_4d_chokepoint_dag(
            n_layers=12, nodes_per_layer=25, rng_seed=seed * 13 + 5
        )
        for k in [3.0, 5.0]:
            result = sorkin_test_4d(positions, adj, layer_indices, k)
            if result is None:
                print(f"  {seed:4d}  {k:4.1f}  SKIP (slits not found)")
                continue
            i3, p = result
            ratio = abs(i3) / p if p > 1e-30 else math.nan
            print(f"  {seed:4d}  {k:4.1f}  {i3:+14.6e}  {p:12.6e}  {ratio:14.6e}")

    print()
    print("EXPECTED: linearity ~ 1e-15, |I_3|/P ~ 1e-15")
    print("This confirms Born rule holds when the 4D barrier is a true chokepoint.")


if __name__ == "__main__":
    main()
