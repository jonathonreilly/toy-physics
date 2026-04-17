#!/usr/bin/env python3
"""Explain when packet-local gravity readouts help by comparing packet support structure.

This bounded follow-on stays on the current readout-only gravity lane. It keeps
the corrected microscopic transport and field law fixed, then measures the
support geometry behind the packet-local readouts that were compared in the
two-family transfer script.

The goal is to explain why `packet_flow_action` helps on the layered random-DAG
family but does not replace the broader `action_channel` on the branching-tree
control.

Measured structure:
- side-resolved packet support width compression
- side-resolved carried probe share inside the retained packet
- the readout values that those support metrics are meant to explain
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.gravity_observable_readout_scaling_compare import (  # noqa: E402
    K_BAND,
    _action_channel_bias,
    _beam_width,
    _detector_probs,
    _node_probs,
    _propagate_action_means,
    _propagate_node_amplitudes,
)
from scripts.gravity_packet_local_action_flow_transfer_compare import (  # noqa: E402
    DAG_SIZES,
    TREE_SIZES,
    _edge_flow_weights,
    _packet_action_channel_bias,
    _packet_flow_action_bias,
)
from scripts.scaling_testbench import build_branching_tree  # noqa: E402
from scripts.two_register_decoherence import compute_field  # noqa: E402


@dataclass(frozen=True)
class TrialRow:
    family: str
    size: int
    seed: int
    action_channel: float
    packet_action_channel: float
    packet_flow_action: float
    node_upper_compression: float
    node_lower_compression: float
    node_upper_probe_share: float
    node_lower_probe_share: float
    flow_upper_compression: float
    flow_lower_compression: float
    flow_upper_probe_share: float
    flow_lower_probe_share: float


def _weighted_rms(
    positions: list[tuple[float, float]],
    weights: dict[int, float],
    nodes: list[int],
    width_floor: float = 0.0,
) -> float:
    weighted_nodes = [(node, weights.get(node, 0.0)) for node in nodes]
    weighted_nodes = [(node, weight) for node, weight in weighted_nodes if weight > 1e-30]
    if not weighted_nodes:
        return 0.0
    total_weight = sum(weight for _node, weight in weighted_nodes)
    mean_y = sum(positions[node][1] * weight for node, weight in weighted_nodes) / total_weight
    variance = (
        sum(((positions[node][1] - mean_y) ** 2) * weight for node, weight in weighted_nodes) / total_weight
    )
    return max(math.sqrt(max(variance, 0.0)), width_floor)


def _spacing_floor(
    positions: list[tuple[float, float]],
    nodes: list[int],
) -> float:
    ys = sorted({positions[node][1] for node in nodes})
    if len(ys) < 2:
        return 0.5
    gaps = [right - left for left, right in zip(ys, ys[1:]) if (right - left) > 1e-9]
    if not gaps:
        return 0.5
    return max(statistics.median(gaps), 0.5)


def _packet_nodes(
    positions: list[tuple[float, float]],
    weights: dict[int, float],
    side_nodes: list[int],
    retain_share: float,
) -> list[tuple[int, float]]:
    weighted_nodes = [(node, weights.get(node, 0.0)) for node in side_nodes]
    weighted_nodes = [(node, weight) for node, weight in weighted_nodes if weight > 1e-30]
    if not weighted_nodes:
        return []

    peak_node = max(weighted_nodes, key=lambda item: item[1])[0]
    peak_y = positions[peak_node][1]
    total_weight = sum(weight for _node, weight in weighted_nodes)
    target = max(1e-30, retain_share * total_weight)

    ordered = sorted(
        weighted_nodes,
        key=lambda item: (abs(positions[item[0]][1] - peak_y), -item[1], item[0]),
    )

    kept_nodes: list[tuple[int, float]] = []
    carried_weight = 0.0
    for node, weight in ordered:
        kept_nodes.append((node, weight))
        carried_weight += weight
        if carried_weight >= target:
            break
    return kept_nodes


def _side_packet_metrics(
    positions: list[tuple[float, float]],
    weights: dict[int, float],
    probe_nodes: list[int],
    side_nodes: list[int],
    retain_share: float,
) -> tuple[float, float]:
    width_floor = _spacing_floor(positions, side_nodes)
    full_rms = _weighted_rms(positions, weights, side_nodes, width_floor=width_floor)
    packet = _packet_nodes(positions, weights, side_nodes, retain_share)
    packet_weights = {node: weight for node, weight in packet}
    packet_nodes = list(packet_weights)
    packet_rms = _weighted_rms(positions, packet_weights, packet_nodes, width_floor=width_floor)
    compression = full_rms / packet_rms if packet_rms > 1e-30 else 0.0

    packet_total = sum(packet_weights.values())
    probe_total = sum(weights.get(node, 0.0) for node in probe_nodes)
    probe_share = packet_total / probe_total if probe_total > 1e-30 else 0.0
    return compression, probe_share


def _family_geometry(
    family: str,
    size: int,
    seed: int,
) -> tuple[
    list[tuple[float, float]],
    dict[int, list[int]],
    list[int],
    set[int],
    float,
    list[int],
    set[int],
    set[int],
]:
    if family == "random_dag":
        positions, adj, _layer_indices = generate_causal_dag(
            n_layers=size,
            nodes_per_layer=25,
            y_range=12.0,
            connect_radius=3.0,
            rng_seed=seed * 11 + 7,
        )
        by_layer: dict[int, list[int]] = defaultdict(list)
        for idx, (x, _y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer)
        src = by_layer[layers[0]]
        det = set(by_layer[layers[-1]])
        center_y = statistics.fmean(y for _x, y in positions)
        mid = len(layers) // 2
        grav_mass = [node for node in by_layer[layers[mid]] if positions[node][1] > center_y + 2.0]
    elif family == "branching_tree":
        positions, adj, layer_indices = build_branching_tree(size, branching_factor=2, y_range=10.0)
        layers = list(range(len(layer_indices)))
        by_layer = {layer: nodes for layer, nodes in enumerate(layer_indices)}
        src = by_layer[layers[0]]
        det = set(by_layer[layers[-1]])
        center_y = statistics.fmean(y for _x, y in positions)
        mid = len(layers) // 2
        grav_mass = [node for node in by_layer[layers[mid]] if positions[node][1] > center_y + 1.0]
    else:
        raise ValueError(f"Unknown family: {family}")

    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}
    return positions, adj, src, det, center_y, grav_mass, source_layers, probe_layers


def _evaluate_family(
    family: str,
    size: int,
    seed: int,
    retain_share: float,
) -> TrialRow | None:
    (
        positions,
        adj,
        src,
        det,
        center_y,
        grav_mass,
        source_layers,
        probe_layers,
    ) = _family_geometry(family, size, seed)

    if not det or not grav_mass:
        return None

    n = len(positions)
    free_field = [0.0] * n
    mass_field = compute_field(positions, adj, grav_mass)
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    probe_nodes = [node for node in range(n) if by_layer[node] in probe_layers]

    free_action_mean = _propagate_action_means(positions, adj, free_field, src)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src)
    action_delta = {
        node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0)
        for node in range(n)
    }

    action_channel_values: list[float] = []
    packet_action_values: list[float] = []
    packet_flow_values: list[float] = []

    node_upper_compressions: list[float] = []
    node_lower_compressions: list[float] = []
    node_upper_probe_shares: list[float] = []
    node_lower_probe_shares: list[float] = []
    flow_upper_compressions: list[float] = []
    flow_lower_compressions: list[float] = []
    flow_upper_probe_shares: list[float] = []
    flow_lower_probe_shares: list[float] = []

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k)
        free_probs = _detector_probs(free_amps, det)
        width_ref = _beam_width(free_probs, positions)
        mass_node_probs = _node_probs(mass_amps)
        flow_weights = _edge_flow_weights(
            positions=positions,
            adj=adj,
            field=mass_field,
            amps=mass_amps,
            source_layers=source_layers,
            probe_layers=probe_layers,
            k=k,
        )

        upper_probe_nodes = [node for node in probe_nodes if positions[node][1] >= center_y]
        lower_probe_nodes = [node for node in probe_nodes if positions[node][1] < center_y]

        node_upper_compression, node_upper_probe_share = _side_packet_metrics(
            positions=positions,
            weights=mass_node_probs,
            probe_nodes=probe_nodes,
            side_nodes=upper_probe_nodes,
            retain_share=retain_share,
        )
        node_lower_compression, node_lower_probe_share = _side_packet_metrics(
            positions=positions,
            weights=mass_node_probs,
            probe_nodes=probe_nodes,
            side_nodes=lower_probe_nodes,
            retain_share=retain_share,
        )
        flow_upper_compression, flow_upper_probe_share = _side_packet_metrics(
            positions=positions,
            weights=flow_weights,
            probe_nodes=probe_nodes,
            side_nodes=upper_probe_nodes,
            retain_share=retain_share,
        )
        flow_lower_compression, flow_lower_probe_share = _side_packet_metrics(
            positions=positions,
            weights=flow_weights,
            probe_nodes=probe_nodes,
            side_nodes=lower_probe_nodes,
            retain_share=retain_share,
        )

        node_upper_compressions.append(node_upper_compression)
        node_lower_compressions.append(node_lower_compression)
        node_upper_probe_shares.append(node_upper_probe_share)
        node_lower_probe_shares.append(node_lower_probe_share)
        flow_upper_compressions.append(flow_upper_compression)
        flow_lower_compressions.append(flow_lower_compression)
        flow_upper_probe_shares.append(flow_upper_probe_share)
        flow_lower_probe_shares.append(flow_lower_probe_share)

        action_channel_values.append(
            _action_channel_bias(positions, action_delta, mass_node_probs, probe_layers, center_y) / width_ref
        )
        packet_action_values.append(
            _packet_action_channel_bias(
                positions=positions,
                action_delta=action_delta,
                node_weights=mass_node_probs,
                probe_layers=probe_layers,
                center_y=center_y,
                retain_share=retain_share,
            )
            / width_ref
        )
        packet_flow_values.append(
            _packet_flow_action_bias(
                positions=positions,
                adj=adj,
                field=mass_field,
                amps=mass_amps,
                action_delta=action_delta,
                source_layers=source_layers,
                probe_layers=probe_layers,
                center_y=center_y,
                k=k,
                retain_share=retain_share,
            )
            / width_ref
        )

    return TrialRow(
        family=family,
        size=size,
        seed=seed,
        action_channel=statistics.fmean(action_channel_values),
        packet_action_channel=statistics.fmean(packet_action_values),
        packet_flow_action=statistics.fmean(packet_flow_values),
        node_upper_compression=statistics.fmean(node_upper_compressions),
        node_lower_compression=statistics.fmean(node_lower_compressions),
        node_upper_probe_share=statistics.fmean(node_upper_probe_shares),
        node_lower_probe_share=statistics.fmean(node_lower_probe_shares),
        flow_upper_compression=statistics.fmean(flow_upper_compressions),
        flow_lower_compression=statistics.fmean(flow_lower_compressions),
        flow_upper_probe_share=statistics.fmean(flow_upper_probe_shares),
        flow_lower_probe_share=statistics.fmean(flow_lower_probe_shares),
    )


def _evaluate_task(task: tuple[str, int, int, float]) -> TrialRow | None:
    family, size, seed, retain_share = task
    return _evaluate_family(family, size, seed, retain_share)


def _render_family_table(
    family: str,
    rows: list[TrialRow],
    sizes: tuple[int, ...],
) -> dict[int, dict[str, float]]:
    grouped: dict[int, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.size].append(row)

    print("=" * 120)
    print(f"Family: {family}")
    print("=" * 120)
    print(
        f"{'size':>6s} {'n':>3s} {'R_act':>10s} {'R_pkt':>10s} {'R_flow':>10s} "
        f"{'flowC_u':>9s} {'flowC_l':>9s} {'flowS_u':>9s} {'flowS_l':>9s} {'flowGap':>9s}"
    )
    print("-" * 98)

    summary: dict[int, dict[str, float]] = {}
    for size in sizes:
        bucket = grouped.get(size, [])
        if not bucket:
            continue
        stats = {
            "action_channel": statistics.fmean(row.action_channel for row in bucket),
            "packet_action_channel": statistics.fmean(row.packet_action_channel for row in bucket),
            "packet_flow_action": statistics.fmean(row.packet_flow_action for row in bucket),
            "node_upper_compression": statistics.fmean(row.node_upper_compression for row in bucket),
            "node_lower_compression": statistics.fmean(row.node_lower_compression for row in bucket),
            "node_upper_probe_share": statistics.fmean(row.node_upper_probe_share for row in bucket),
            "node_lower_probe_share": statistics.fmean(row.node_lower_probe_share for row in bucket),
            "flow_upper_compression": statistics.fmean(row.flow_upper_compression for row in bucket),
            "flow_lower_compression": statistics.fmean(row.flow_lower_compression for row in bucket),
            "flow_upper_probe_share": statistics.fmean(row.flow_upper_probe_share for row in bucket),
            "flow_lower_probe_share": statistics.fmean(row.flow_lower_probe_share for row in bucket),
        }
        summary[size] = stats
        print(
            f"{size:6d} {len(bucket):3d} "
            f"{stats['action_channel']:+10.4f} "
            f"{stats['packet_action_channel']:+10.4f} "
            f"{stats['packet_flow_action']:+10.4f} "
            f"{stats['flow_upper_compression']:9.3f} "
            f"{stats['flow_lower_compression']:9.3f} "
            f"{stats['flow_upper_probe_share']:9.3f} "
            f"{stats['flow_lower_probe_share']:9.3f} "
            f"{stats['flow_upper_probe_share'] - stats['flow_lower_probe_share']:9.3f}"
        )

    print()
    print("Node-weight support compression and packet probe share")
    print(
        f"{'size':>6s} {'nodeC_u':>9s} {'nodeC_l':>9s} {'nodeS_u':>9s} {'nodeS_l':>9s} {'nodeGap':>9s}"
    )
    print("-" * 58)
    for size in sizes:
        stats = summary.get(size)
        if not stats:
            continue
        print(
            f"{size:6d} "
            f"{stats['node_upper_compression']:9.3f} "
            f"{stats['node_lower_compression']:9.3f} "
            f"{stats['node_upper_probe_share']:9.3f} "
            f"{stats['node_lower_probe_share']:9.3f} "
            f"{stats['node_upper_probe_share'] - stats['node_lower_probe_share']:9.3f}"
        )
    print()
    return summary


def _format_endpoint_summary(
    family: str,
    summary: dict[int, dict[str, float]],
    anchor_size: int,
    high_size: int,
) -> None:
    anchor = summary[anchor_size]
    high = summary[high_size]
    print(f"Interpretation for {family}:")
    print(
        "  flow packet share gap "
        f"{anchor['flow_upper_probe_share'] - anchor['flow_lower_probe_share']:+.3f} -> "
        f"{high['flow_upper_probe_share'] - high['flow_lower_probe_share']:+.3f}; "
        f"mass-side carried-flow share {anchor['flow_upper_probe_share']:.3f} -> {high['flow_upper_probe_share']:.3f}; "
        f"opposite-side share {anchor['flow_lower_probe_share']:.3f} -> {high['flow_lower_probe_share']:.3f}."
    )
    print(
        "  flow support compression stays at "
        f"{anchor['flow_upper_compression']:.3f}x/{anchor['flow_lower_compression']:.3f}x -> "
        f"{high['flow_upper_compression']:.3f}x/{high['flow_lower_compression']:.3f}x "
        "(upper/lower), measuring how much broader the full support is than the retained packet."
    )
    print(
        "  readout retention over the same endpoint grows from "
        f"{anchor['packet_flow_action'] / anchor['action_channel'] if abs(anchor['action_channel']) > 1e-30 else 0.0:+.3f} "
        f"to {high['packet_flow_action'] / high['action_channel'] if abs(high['action_channel']) > 1e-30 else 0.0:+.3f} "
        "for packet_flow_action / action_channel."
    )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--dag-seeds", type=int, default=5)
    parser.add_argument("--retain-share", type=float, default=0.5)
    args = parser.parse_args()

    tasks: list[tuple[str, int, int, float]] = []
    tasks.extend(("random_dag", size, seed, args.retain_share) for size in DAG_SIZES for seed in range(args.dag_seeds))
    tasks.extend(("branching_tree", size, 0, args.retain_share) for size in TREE_SIZES)

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        rows = [_evaluate_task(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                rows = list(pool.map(_evaluate_task, tasks))
        except PermissionError:
            rows = [_evaluate_task(task) for task in tasks]
    rows = [row for row in rows if row is not None]

    print("=" * 120)
    print("GRAVITY PACKET-LOCAL SUPPORT STRUCTURE COMPARE")
    print("=" * 120)
    print(
        f"workers={args.workers}, dag_seeds={args.dag_seeds}, retain_share={args.retain_share:.2f}, "
        f"k_band={K_BAND}"
    )
    print("Transport and field law are unchanged; only packet support structure is being compared.")
    print()

    dag_rows = [row for row in rows if row.family == "random_dag"]
    tree_rows = [row for row in rows if row.family == "branching_tree"]
    dag_summary = _render_family_table("random_dag", dag_rows, DAG_SIZES)
    tree_summary = _render_family_table("branching_tree", tree_rows, TREE_SIZES)

    print("=" * 120)
    print("INTERPRETATION")
    print("=" * 120)
    _format_endpoint_summary("random_dag", dag_summary, anchor_size=12, high_size=25)
    _format_endpoint_summary("branching_tree", tree_summary, anchor_size=6, high_size=12)
    print("Shared read:")
    print(
        "  Packet-local flow is a real dense-route refinement because the random-DAG family develops a growing "
        "mass-side carried-flow packet while the opposite side diffuses. The branching-tree control does not: "
        "its two probe sides stay nearly symmetric and only weakly broader than the retained packet. So the "
        "cross-family gravity law is still the coarser action_channel, while packet_flow_action is the better "
        "regime-specific read when multi-route support broadens and then refocuses around the mass-side packet."
    )


if __name__ == "__main__":
    main()
