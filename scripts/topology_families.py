#!/usr/bin/env python3
"""Non-uniform DAG topology families for the decoherence topology pivot.

Three graph families designed to preserve slit-path structural separation
as N grows, unlike uniform random DAGs where CLT convergence erases
slit distinction by N~25.

All generators return the same (positions, adj, arrival) triple as
generate_causal_dag, so they plug into the existing CL bath / IF machinery.

Family 1: HIERARCHICAL / FUNNELLED
  Nodes funnel through a narrow waist at the barrier, then expand.
  Slit separation is enforced by geometry: upper-half and lower-half
  nodes have limited cross-connectivity.

Family 2: MODULAR TWO-CHANNEL
  Two separate channels (upper/lower) with sparse crosslinks.
  Each slit feeds primarily into one channel. Crosslink probability
  controls how much mixing occurs.

Family 3: PREFERENTIAL ATTACHMENT (scale-free-like)
  Hub nodes get more connections. Slit paths tend to route through
  different hubs, preserving structural separation even as N grows.
"""

from __future__ import annotations
import math
import random
from collections import defaultdict


def _make_arrival(positions, adj):
    """Compute arrival times via BFS from layer 0."""
    n = len(positions)
    arrival = [float("inf")] * n
    for i in range(n):
        if positions[i][0] == 0.0:
            arrival[i] = 0.0
    # topo order by x
    order = sorted(range(n), key=lambda i: (positions[i][0], i))
    for i in order:
        if not math.isfinite(arrival[i]):
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            cand = arrival[i] + dist
            if cand < arrival[j]:
                arrival[j] = cand
    return arrival


# ─────────────────────────────────────────────────────────────────────
# Family 1: Hierarchical / Funnelled DAG
# ─────────────────────────────────────────────────────────────────────

def generate_hierarchical_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    channel_leak: float = 0.05,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Hierarchical DAG with upper/lower channel separation.

    Post-barrier, nodes are assigned to upper (y>0) or lower (y<0) channel.
    Within-channel connections use full connect_radius.
    Cross-channel connections use connect_radius * channel_leak.

    This preserves the slit→channel mapping as N grows because
    cross-channel mixing is geometrically suppressed.
    """
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    # Barrier at layer n_layers // 3
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                # Connect to previous layers
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)

                        # Post-barrier: enforce channel separation
                        if layer > barrier_layer and prev_layer[0] != 0:
                            # Check if same channel (both y>0 or both y<0)
                            same_channel = (y * py > 0)  # same sign
                            if same_channel:
                                r = connect_radius
                            else:
                                r = connect_radius * channel_leak
                        else:
                            r = connect_radius

                        if dist <= r:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival


# ─────────────────────────────────────────────────────────────────────
# Family 2: Modular Two-Channel DAG
# ─────────────────────────────────────────────────────────────────────

def generate_modular_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    crosslink_prob: float = 0.02,
    gap: float = 4.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Two-channel modular DAG with sparse probabilistic crosslinks.

    Post-barrier nodes are placed in two separate y-bands:
      Upper channel: y in [+gap/2, +y_range]
      Lower channel: y in [-y_range, -gap/2]

    Within each channel, normal radius-based connectivity.
    Cross-channel edges added with probability crosslink_prob
    (only when within 2x connect_radius).

    The physical gap between channels means paths through different
    slits stay in different channels with high probability.
    """
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                if layer > barrier_layer:
                    # Place in upper or lower channel
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, y_range)
                    else:
                        y = rng.uniform(-y_range, -gap / 2)
                else:
                    y = rng.uniform(-y_range, y_range)

                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)

                        if layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                # Sparse crosslink
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival


# ─────────────────────────────────────────────────────────────────────
# Family 3: Preferential Attachment DAG
# ─────────────────────────────────────────────────────────────────────

def generate_preferential_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    hub_boost: float = 3.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Scale-free-like DAG with preferential attachment.

    Connection probability is proportional to the parent's existing
    out-degree (plus 1). High-degree "hub" nodes attract more connections,
    creating structural heterogeneity.

    Different slits tend to route through different hubs because
    each hub's y-position biases which slit feeds it. This structural
    separation persists as N grows (unlike uniform random DAGs where
    all nodes become equivalent).
    """
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    out_degree: dict[int, int] = defaultdict(int)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                # Collect candidates with preferential weight
                candidates = []
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            # Weight: base 1 + hub_boost * out_degree
                            w = 1.0 + hub_boost * out_degree[prev_idx]
                            candidates.append((prev_idx, w, dist))

                if candidates:
                    # Normalize weights to probabilities, accept with that prob
                    max_w = max(c[1] for c in candidates)
                    for prev_idx, w, dist in candidates:
                        p_accept = w / max_w
                        if rng.random() < p_accept:
                            adj[prev_idx].append(idx)
                            out_degree[prev_idx] += 1

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival
