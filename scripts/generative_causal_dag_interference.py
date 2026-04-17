#!/usr/bin/env python3
"""Generative causal DAG with path-sum interference test.

The graph itself generates the causal structure. No pre-built grid.
Events spawn forward in "time" (increasing x), creating a directed
DAG. A barrier region with two gaps acts as a natural two-slit setup.
The path-sum over this generated DAG tests whether interference
EMERGES from the graph dynamics.

This is the key experiment: does the graph generate physics, not
just host it?

PStack experiment: generative-causal-interference
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_causal_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 15,
    y_range: float = 10.0,
    connect_radius: float = 2.5,
    rng_seed: int = 42,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Generate a causal DAG by spawning layers of events.

    Each layer is at a fixed x-coordinate (the "time" direction).
    Within each layer, nodes are placed at random y-positions.
    Edges go ONLY from earlier layers to later layers (causal).
    A node connects to all nodes in the next layer within connect_radius.

    Returns: (positions, forward_adjacency, arrival_times)
    """
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    arrival: list[float] = []
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            # Seed: single source node at center
            idx = len(positions)
            positions.append((x, 0.0))
            arrival.append(0.0)
            layer_nodes.append(idx)
        else:
            # Spawn nodes at random y-positions in this layer
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                # Connect to all reachable nodes in PREVIOUS layers
                # (creates the causal DAG — edges only go forward in x)
                best_arrival = float("inf")
                for prev_layer in layer_indices[max(0, layer - 2):]:  # Look back 2 layers
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
                            # Arrival time = parent arrival + edge distance
                            candidate = arrival[prev_idx] + dist
                            if math.isfinite(candidate) and candidate < best_arrival:
                                best_arrival = candidate

                arrival.append(best_arrival)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), arrival


def causal_order(
    positions: list[tuple[float, float]],
    arrival: list[float],
) -> list[int]:
    """Return a topological processing order for generated DAGs.

    The layer/x coordinate is the true causal order. Arrival times are only a
    secondary tie-breaker inside a layer and should never reorder nodes across
    layers.
    """

    return sorted(
        range(len(positions)),
        key=lambda i: (positions[i][0], math.isinf(arrival[i]), arrival[i], i),
    )


def path_sum_on_dag(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    arrival: list[float],
    source_idx: int,
    detector_x: float,
    detector_ys: list[float],
    detector_tolerance: float,
    barrier_x: float,
    slit_ys: list[float],
    slit_width: float,
    phase_per_action: float = 4.0,
    phase_shift_upper: float = 0.0,
) -> dict[float, float]:
    """Path-sum amplitude calculation on the generated DAG.

    Barrier: nodes near barrier_x with y NOT near any slit_y are "blocked"
    (amplitude zeroed, not removed — fixed DAG).
    Phase shift applied to paths through the upper slit.
    """
    n = len(positions)

    # Identify barrier-blocked nodes (amplitude = 0 at these)
    blocked = set()
    for i in range(n):
        x, y = positions[i]
        if abs(x - barrier_x) < 0.5:
            # Is this node near a slit?
            near_slit = any(abs(y - sy) < slit_width for sy in slit_ys)
            if not near_slit:
                blocked.add(i)

    # Propagate amplitudes
    order = causal_order(positions, arrival)
    amplitudes: dict[int, complex] = {source_idx: 1.0 + 0.0j}
    detector_amps: defaultdict[float, complex] = defaultdict(complex)

    upper_slit_y = max(slit_ys)

    for i in order:
        if i not in amplitudes or amplitudes[i] == 0:
            continue
        amp = amplitudes[i]

        if i in blocked:
            continue  # Amplitude stops here

        x, y = positions[i]

        # Collect at detector
        if abs(x - detector_x) < 0.5:
            # Find nearest detector_y
            for dy in detector_ys:
                if abs(y - dy) < detector_tolerance:
                    detector_amps[dy] += amp
            continue

        # Propagate to children
        for j in adj.get(i, []):
            jx, jy = positions[j]
            dist = math.sqrt((jx - x) ** 2 + (jy - y) ** 2)
            delay = dist  # Free field: delay = distance
            action = delay  # Simplified: action = delay for light-like
            link_amp = cmath.exp(1j * phase_per_action * action) / max(delay, 0.01)

            # Phase shift at barrier crossing through upper slit
            if x < barrier_x <= jx:
                near_upper = abs(jy - upper_slit_y) < slit_width
                if near_upper:
                    link_amp *= cmath.exp(1j * phase_shift_upper)

            if j not in amplitudes:
                amplitudes[j] = 0.0 + 0.0j
            amplitudes[j] += amp * link_amp

    # Probabilities
    return {dy: abs(detector_amps[dy]) ** 2 for dy in detector_ys}


def visibility(probs: list[float]) -> float:
    pm, pn = max(probs), min(probs)
    return (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0


def main() -> None:
    print("=" * 72)
    print("GENERATIVE CAUSAL DAG: INTERFERENCE TEST")
    print("=" * 72)
    print()

    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    barrier_layer = 12
    detector_layer = n_layers - 1
    slit_ys = [-3.0, 3.0]
    slit_width = 1.5
    n_phases = 16
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    detector_ys = [float(y) for y in range(-8, 9)]
    detector_tol = 1.5

    print(f"Layers: {n_layers}, nodes/layer: {nodes_per_layer}")
    print(f"Barrier at layer {barrier_layer}, slits at y={slit_ys}")
    print()

    # Test across multiple random seeds
    for seed in [42, 123, 456, 789, 1000]:
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )

        # Count reachable nodes
        reachable = sum(1 for a in arrival if a < float("inf"))
        edges = sum(len(v) for v in adj.values())

        # Phase sweep for interference visibility
        vis_by_y: dict[float, float] = {}
        for dy in detector_ys:
            probs = []
            for phase in phases:
                dist = path_sum_on_dag(
                    positions, adj, arrival,
                    source_idx=0,
                    detector_x=float(detector_layer),
                    detector_ys=[dy],
                    detector_tolerance=detector_tol,
                    barrier_x=float(barrier_layer),
                    slit_ys=slit_ys,
                    slit_width=slit_width,
                    phase_shift_upper=phase,
                )
                probs.append(dist.get(dy, 0.0))

            if any(p > 0 for p in probs):
                vis_by_y[dy] = visibility(probs)
            else:
                vis_by_y[dy] = -1.0  # No signal

        active_vis = {y: v for y, v in vis_by_y.items() if v >= 0}
        mean_v = sum(active_vis.values()) / len(active_vis) if active_vis else 0
        v_center = vis_by_y.get(0.0, -1.0)
        n_active = len(active_vis)

        print(f"  seed={seed}: {len(positions)} nodes, {reachable} reachable, {edges} edges, "
              f"V(y=0)={v_center:.6f}, mean_V={mean_v:.6f} ({n_active} active detectors)")

    # Detailed profile for seed=42
    print()
    print("=" * 72)
    print("DETAILED VISIBILITY PROFILE (seed=42)")
    print("=" * 72)
    print()

    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=nodes_per_layer,
        y_range=y_range, connect_radius=2.5, rng_seed=42,
    )

    for dy in detector_ys:
        probs = []
        for phase in phases:
            dist = path_sum_on_dag(
                positions, adj, arrival, 0,
                float(detector_layer), [dy], detector_tol,
                float(barrier_layer), slit_ys, slit_width,
                phase_shift_upper=phase,
            )
            probs.append(dist.get(dy, 0.0))

        if any(p > 0 for p in probs):
            v = visibility(probs)
            bar = "#" * int(v * 40) if v > 0 else ""
            slit_mark = " <-- slit" if any(abs(dy - sy) < slit_width for sy in slit_ys) else ""
            print(f"  y={dy:+5.1f}  V={v:8.6f}  {bar}{slit_mark}")
        else:
            print(f"  y={dy:+5.1f}  (no signal)")

    # Control: no barrier (all nodes open) — should have V=0
    print()
    print("CONTROL: No barrier (should have V≈0)")
    control_probs = []
    for phase in phases:
        dist = path_sum_on_dag(
            positions, adj, arrival, 0,
            float(detector_layer), [0.0], detector_tol,
            barrier_x=100.0,  # Barrier way off-grid
            slit_ys=slit_ys, slit_width=slit_width,
            phase_shift_upper=phase,
        )
        control_probs.append(dist.get(0.0, 0.0))
    if any(p > 0 for p in control_probs):
        print(f"  V(y=0, no barrier) = {visibility(control_probs):.6f}")
    else:
        print(f"  No signal at y=0 without barrier")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
