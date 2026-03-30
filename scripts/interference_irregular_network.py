#!/usr/bin/env python3
"""Test interference on irregular (perturbed) networks.

The key question: are the interference findings (topological threshold,
monotonic trends, record suppression) specific to rectangular grids,
or do they survive on irregular networks?

Approach: start with a rectangular grid, then randomly perturb node
positions by varying amounts. This preserves the topology (same
neighbors) but breaks the geometric regularity.

PStack experiment: irregular-network-interference
"""

from __future__ import annotations
import math
import cmath
import random
import sys
import os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    derive_local_rule,
)


def build_perturbed_grid(
    width: int, height: int, perturbation: float, seed: int,
) -> tuple[dict[tuple[int, int], tuple[float, float]], set[tuple[int, int]]]:
    """Build a rectangular grid with random position perturbations.

    Returns:
        positions: map from integer grid coords to perturbed (x, y) positions
        nodes: set of integer grid coordinates (for topology)
    """
    rng = random.Random(seed)
    nodes = set()
    positions: dict[tuple[int, int], tuple[float, float]] = {}
    for x in range(width + 1):
        for y in range(-height, height + 1):
            nodes.add((x, y))
            # Perturb position but keep integer coords for topology
            px = x + rng.uniform(-perturbation, perturbation)
            py = y + rng.uniform(-perturbation, perturbation)
            positions[(x, y)] = (px, py)
    return positions, nodes


def perturbed_two_slit(
    screen_positions: list[int],
    record_created: bool,
    width: int, height: int,
    slit_ys: set[int],
    perturbation: float,
    seed: int,
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Two-slit on a perturbed grid.

    Topology is rectangular (same neighbors), but edge lengths
    vary due to position perturbation. This changes delays and
    actions on each edge, breaking the grid's geometric regularity
    while preserving its connectivity.
    """
    positions, nodes = build_perturbed_grid(width, height, perturbation, seed)
    barrier_x = width // 2
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    active_nodes = nodes - blocked_nodes
    source = (1, 0)
    detector_x = width

    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )

    # Build arrival times using perturbed distances
    # Simple BFS with perturbed edge weights
    import heapq
    arrival_times: dict[tuple[int, int], float] = {source: 0.0}
    heap = [(0.0, source)]

    while heap:
        t, node = heapq.heappop(heap)
        if t > arrival_times.get(node, float("inf")):
            continue
        px, py = positions[node]
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb not in active_nodes:
                    continue
                npx, npy = positions[nb]
                # Edge length from perturbed positions
                edge_len = math.sqrt((npx - px) ** 2 + (npy - py) ** 2)
                # Delay = edge_len (signal speed = 1)
                delay = edge_len
                new_t = t + delay
                if new_t < arrival_times.get(nb, float("inf")):
                    arrival_times[nb] = new_t
                    heapq.heappush(heap, (new_t, nb))

    # Build causal DAG
    dag: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for node in active_nodes:
        if node not in arrival_times:
            continue
        px, py = positions[node]
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb not in active_nodes or nb not in arrival_times:
                    continue
                if arrival_times[nb] > arrival_times[node]:
                    dag[node].append(nb)

    order = sorted(arrival_times, key=arrival_times.get)

    # Path sum with perturbed edge properties
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j
    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    phase_per_action = 4.0

    for node in order:
        matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
        if not matching:
            continue
        if node[0] == detector_x:
            for state, amp in matching:
                boundary_distribution[node[1]][state[2]] += amp
                del states[state]
            continue
        for (cur, heading, sector), amp in matching:
            del states[(cur, heading, sector)]
            px, py = positions[cur]
            for nb in dag.get(node, []):
                npx, npy = positions[nb]
                edge_len = math.sqrt((npx - px) ** 2 + (npy - py) ** 2)
                delay = edge_len
                # Action = spent delay (delay - retained update)
                retained = math.sqrt(max(delay * delay - edge_len * edge_len, 0.0))
                action = delay - retained  # = delay - 0 = delay for light-like
                # For non-light-like, use proper formula
                link_amp = cmath.exp(1j * phase_per_action * action) * (1.0 / max(delay, 0.001))

                next_sector = sector
                if node[0] < barrier_x <= nb[0] and nb[1] in slit_ys:
                    if record_created:
                        next_sector = "upper" if nb[1] > 0 else "lower"
                    if nb[1] > 0:
                        link_amp *= cmath.exp(1j * phase_shift_upper)

                states[(nb, (nb[0]-node[0], nb[1]-node[1]), next_sector)] += amp * link_amp

    distribution: dict[int, float] = {}
    for y in screen_positions:
        sector_amps = boundary_distribution.get(y, {})
        if record_created:
            probability = sum(abs(a) ** 2 for a in sector_amps.values())
        else:
            probability = abs(sum(sector_amps.values())) ** 2
        distribution[y] = probability

    if not normalize:
        return distribution
    norm = sum(distribution.values())
    if norm == 0:
        return {y: 0.0 for y in screen_positions}
    return {y: p / norm for y, p in distribution.items()}


def visibility(probs: list[float]) -> float:
    p_max, p_min = max(probs), min(probs)
    denom = p_max + p_min
    return (p_max - p_min) / denom if denom > 0 else 0.0


def main() -> None:
    width = 20
    height = 10
    slit_ys = {-4, 4}
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    screen_ys = list(range(-height, height + 1))

    perturbations = [0.0, 0.1, 0.2, 0.3, 0.4]
    seeds = [42, 123, 777]

    print("=" * 72)
    print("IRREGULAR NETWORK INTERFERENCE TEST")
    print("=" * 72)
    print(f"width={width}, height={height}, slits at y={sorted(slit_ys)}")
    print(f"perturbations: {perturbations}")
    print(f"seeds: {seeds}")
    print()

    # For each perturbation level and seed, measure V(y) and mean_V
    print(f"{'pert':>5s}  {'seed':>5s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  "
          f"{'V(y=3)':>10s}  {'mean_V':>10s}  {'record_leak':>12s}")
    print("-" * 80)

    for pert in perturbations:
        for seed in seeds:
            vis_by_y: dict[int, float] = {}
            for y in screen_ys:
                probs = []
                for phase in phases:
                    dist = perturbed_two_slit(
                        screen_positions=[y], record_created=False,
                        width=width, height=height, slit_ys=slit_ys,
                        perturbation=pert, seed=seed,
                        phase_shift_upper=phase, normalize=False,
                    )
                    probs.append(dist[y])
                vis_by_y[y] = visibility(probs)

            mean_v = sum(vis_by_y.values()) / len(vis_by_y)

            # Check record suppression
            record_probs = []
            for phase in phases:
                dist = perturbed_two_slit(
                    screen_positions=[0], record_created=True,
                    width=width, height=height, slit_ys=slit_ys,
                    perturbation=pert, seed=seed,
                    phase_shift_upper=phase, normalize=False,
                )
                record_probs.append(dist[0])
            record_v = visibility(record_probs)

            print(f"{pert:5.1f}  {seed:5d}  {vis_by_y[0]:10.6f}  {vis_by_y.get(1, 0):10.6f}  "
                  f"{vis_by_y.get(2, 0):10.6f}  {vis_by_y.get(3, 0):10.6f}  "
                  f"{mean_v:10.6f}  {record_v:12.6f}")

    # Full distribution at pert=0 and pert=0.4 for visual comparison
    for pert in [0.0, 0.4]:
        print(f"\n  P(y) at phase=0, pert={pert}, seed=42, COHERENT:")
        dist = perturbed_two_slit(
            screen_positions=screen_ys, record_created=False,
            width=width, height=height, slit_ys=slit_ys,
            perturbation=pert, seed=42, normalize=True,
        )
        for y in screen_ys:
            p = dist.get(y, 0)
            bar = "#" * int(p * 80)
            marker = " <-- slit" if abs(y) == 4 else ""
            print(f"  {y:+4d}  {p:.6f}  {bar}{marker}")

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
