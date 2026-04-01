#!/usr/bin/env python3
"""Compare packet-local action-flow gravity readouts across two minimal families.

This is a bounded follow-on to the readout-only gravity checkpoint. It keeps the
corrected microscopic propagator and field construction fixed, then asks whether
the winning near-mass ``action_channel`` can be compressed into a smaller
packet-local action-flow observable that also survives transfer to a second
minimal family.

Families:
- layered random DAG scaling family (retained benchmark)
- branching tree control (minimal route multiplicity)

Compared readouts:
- detector centroid shift (baseline)
- near-mass action_channel (current retained coarse readout)
- packet_action_channel (adaptive packet-local node-weight version)
- packet_flow_action (adaptive packet-local forward-flow version)
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
    _edge_terms,
    _node_probs,
    _propagate_action_means,
    _propagate_node_amplitudes,
    _visibility_guardrail,
)
from scripts.scaling_testbench import build_branching_tree  # noqa: E402
from scripts.two_register_decoherence import compute_field, centroid_y  # noqa: E402


DAG_SIZES = (8, 12, 15, 20, 25)
TREE_SIZES = (6, 8, 10, 12)


@dataclass(frozen=True)
class TrialRow:
    family: str
    size: int
    seed: int
    detector_centroid: float
    action_channel: float
    packet_action_channel: float
    packet_flow_action: float
    visibility_guardrail: float


def _peak_packet_mean(
    positions: list[tuple[float, float]],
    weights: dict[int, float],
    values: dict[int, float],
    side_nodes: list[int],
    retain_share: float,
) -> float:
    weighted_nodes = [(node, weights.get(node, 0.0)) for node in side_nodes]
    weighted_nodes = [(node, weight) for node, weight in weighted_nodes if weight > 1e-30]
    if not weighted_nodes:
        return 0.0

    peak_node = max(weighted_nodes, key=lambda item: item[1])[0]
    peak_y = positions[peak_node][1]
    total_weight = sum(weight for _node, weight in weighted_nodes)
    ordered = sorted(
        weighted_nodes,
        key=lambda item: (abs(positions[item[0]][1] - peak_y), -item[1], item[0]),
    )

    kept_nodes: list[tuple[int, float]] = []
    carried_weight = 0.0
    target = max(1e-30, retain_share * total_weight)
    for node, weight in ordered:
        kept_nodes.append((node, weight))
        carried_weight += weight
        if carried_weight >= target:
            break

    denom = sum(weight for _node, weight in kept_nodes)
    if denom <= 1e-30:
        return 0.0
    return sum(weight * values.get(node, 0.0) for node, weight in kept_nodes) / denom


def _packet_action_channel_bias(
    positions: list[tuple[float, float]],
    action_delta: dict[int, float],
    node_weights: dict[int, float],
    probe_layers: set[int],
    center_y: float,
    retain_share: float,
) -> float:
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    upper_nodes = [
        node
        for node, weight in node_weights.items()
        if weight > 1e-30 and by_layer[node] in probe_layers and positions[node][1] >= center_y
    ]
    lower_nodes = [
        node
        for node, weight in node_weights.items()
        if weight > 1e-30 and by_layer[node] in probe_layers and positions[node][1] < center_y
    ]
    upper_mean = _peak_packet_mean(positions, node_weights, action_delta, upper_nodes, retain_share)
    lower_mean = _peak_packet_mean(positions, node_weights, action_delta, lower_nodes, retain_share)
    return upper_mean - lower_mean


def _edge_flow_weights(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    amps: list[complex],
    source_layers: set[int],
    probe_layers: set[int],
    k: float,
) -> dict[int, float]:
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    flows: dict[int, float] = defaultdict(float)
    for i, nbs in adj.items():
        if by_layer[i] not in source_layers:
            continue
        amp_i = amps[i]
        if abs(amp_i) < 1e-30:
            continue
        for j in nbs:
            if by_layer[j] not in probe_layers:
                continue
            edge_amp, _action, _length = _edge_terms(positions, field, i, j, k)
            if edge_amp == 0:
                continue
            flows[j] += abs(amp_i * edge_amp) ** 2
    return flows


def _packet_flow_action_bias(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    amps: list[complex],
    action_delta: dict[int, float],
    source_layers: set[int],
    probe_layers: set[int],
    center_y: float,
    k: float,
    retain_share: float,
) -> float:
    flow_weights = _edge_flow_weights(
        positions=positions,
        adj=adj,
        field=field,
        amps=amps,
        source_layers=source_layers,
        probe_layers=probe_layers,
        k=k,
    )
    by_layer = {idx: round(pos[0]) for idx, pos in enumerate(positions)}
    upper_nodes = [
        node
        for node, weight in flow_weights.items()
        if weight > 1e-30 and by_layer[node] in probe_layers and positions[node][1] >= center_y
    ]
    lower_nodes = [
        node
        for node, weight in flow_weights.items()
        if weight > 1e-30 and by_layer[node] in probe_layers and positions[node][1] < center_y
    ]
    upper_mean = _peak_packet_mean(positions, flow_weights, action_delta, upper_nodes, retain_share)
    lower_mean = _peak_packet_mean(positions, flow_weights, action_delta, lower_nodes, retain_share)
    return upper_mean - lower_mean


def _evaluate_family(
    family: str,
    size: int,
    seed: int,
    retain_share: float,
) -> TrialRow | None:
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
        if len(layers) < 5:
            return None
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

    if not det or len(grav_mass) < 1:
        return None

    n = len(positions)
    free_field = [0.0] * n
    mass_field = compute_field(positions, adj, grav_mass)
    source_layers = {layers[mid - 1], layers[mid]} if mid > 0 else {layers[mid]}
    probe_layers = {layers[mid], layers[min(mid + 1, len(layers) - 1)]}

    detector_centroid_values: list[float] = []
    action_channel_values: list[float] = []
    packet_action_values: list[float] = []
    packet_flow_values: list[float] = []
    visibility_values: list[float] = []

    free_action_mean = _propagate_action_means(positions, adj, free_field, src)
    mass_action_mean = _propagate_action_means(positions, adj, mass_field, src)
    action_delta = {
        node: mass_action_mean.get(node, 0.0) - free_action_mean.get(node, 0.0)
        for node in range(n)
    }

    for k in K_BAND:
        free_amps = _propagate_node_amplitudes(positions, adj, free_field, src, k)
        mass_amps = _propagate_node_amplitudes(positions, adj, mass_field, src, k)
        free_probs = _detector_probs(free_amps, det)
        mass_probs = _detector_probs(mass_amps, det)
        mass_node_probs = _node_probs(mass_amps)
        width_ref = _beam_width(free_probs, positions)

        detector_centroid_values.append(
            (centroid_y(mass_probs, positions) - centroid_y(free_probs, positions)) / width_ref
        )
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
        visibility_values.append(_visibility_guardrail(free_probs, positions))

    return TrialRow(
        family=family,
        size=size,
        seed=seed,
        detector_centroid=statistics.fmean(detector_centroid_values),
        action_channel=statistics.fmean(action_channel_values),
        packet_action_channel=statistics.fmean(packet_action_values),
        packet_flow_action=statistics.fmean(packet_flow_values),
        visibility_guardrail=statistics.fmean(visibility_values),
    )


def _evaluate_task(task: tuple[str, int, int, float]) -> TrialRow | None:
    family, size, seed, retain_share = task
    return _evaluate_family(family, size, seed, retain_share)


def _render_family_summary(
    family: str,
    rows: list[TrialRow],
    sizes: tuple[int, ...],
) -> dict[str, tuple[float, float, float, bool]]:
    grouped: dict[int, list[TrialRow]] = defaultdict(list)
    for row in rows:
        grouped[row.size].append(row)

    metrics = (
        ("detector_centroid", lambda row: row.detector_centroid),
        ("action_channel", lambda row: row.action_channel),
        ("packet_action_channel", lambda row: row.packet_action_channel),
        ("packet_flow_action", lambda row: row.packet_flow_action),
    )

    print("=" * 96)
    print(f"Family: {family}")
    print("=" * 96)
    print(
        f"{'size':>6s} {'n':>3s} {'R_det':>10s} {'R_act':>10s} "
        f"{'R_pkt':>10s} {'R_flow':>10s} {'V_free':>10s}"
    )
    print("-" * 74)
    for size in sizes:
        bucket = grouped.get(size, [])
        if not bucket:
            continue
        print(
            f"{size:6d} {len(bucket):3d} "
            f"{statistics.fmean(row.detector_centroid for row in bucket):+10.4f} "
            f"{statistics.fmean(row.action_channel for row in bucket):+10.4f} "
            f"{statistics.fmean(row.packet_action_channel for row in bucket):+10.4f} "
            f"{statistics.fmean(row.packet_flow_action for row in bucket):+10.4f} "
            f"{statistics.fmean(row.visibility_guardrail for row in bucket):10.4f}"
        )
    print()

    anchor_size = 12 if family == "random_dag" else sizes[0]
    high_size = sizes[-1]
    anchor_bucket = grouped.get(anchor_size, [])
    high_bucket = grouped.get(high_size, [])
    retained: dict[str, tuple[float, float, float, bool]] = {}
    if anchor_bucket and high_bucket:
        print(f"Endpoint retention: size {high_size} / {anchor_size}")
        for label, getter in metrics:
            anchor = statistics.fmean(getter(row) for row in anchor_bucket)
            high = statistics.fmean(getter(row) for row in high_bucket)
            abs_ratio = abs(high) / abs(anchor) if abs(anchor) > 1e-12 else float("inf")
            signed_ratio = high / anchor if abs(anchor) > 1e-12 else float("inf")
            sign_stable = (anchor == 0.0 and high == 0.0) or (anchor > 0 and high > 0) or (anchor < 0 and high < 0)
            retained[label] = (anchor, high, abs_ratio, sign_stable)
            print(
                f"  {label:>22s}: {anchor:+.4f} -> {high:+.4f} "
                f"signed={signed_ratio:+.4f} |mag|={abs_ratio:.4f} sign_stable={sign_stable}"
            )
        print()
    return retained


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
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
            rows = list(pool.map(_evaluate_task, tasks))
    rows = [row for row in rows if row is not None]

    print("=" * 96)
    print("GRAVITY PACKET-LOCAL ACTION-FLOW TRANSFER COMPARE")
    print("=" * 96)
    print(
        f"workers={args.workers}, dag_seeds={args.dag_seeds}, retain_share={args.retain_share:.2f}, "
        f"k_band={K_BAND}"
    )
    print("Transport and field law are unchanged; only the gravity readout is compressed.")
    print()

    dag_rows = [row for row in rows if row.family == "random_dag"]
    tree_rows = [row for row in rows if row.family == "branching_tree"]
    dag_retained = _render_family_summary("random_dag", dag_rows, DAG_SIZES)
    tree_retained = _render_family_summary("branching_tree", tree_rows, TREE_SIZES)

    labels = ("detector_centroid", "action_channel", "packet_action_channel", "packet_flow_action")
    print("=" * 96)
    print("SHARED TRANSFER RANKING")
    print("=" * 96)
    ranked: list[tuple[int, float, float, str]] = []
    for label in labels:
        if label not in dag_retained or label not in tree_retained:
            continue
        dag_anchor, dag_high, dag_ratio, dag_sign = dag_retained[label]
        tree_anchor, tree_high, tree_ratio, tree_sign = tree_retained[label]
        shared_floor = min(dag_ratio, tree_ratio)
        ranked.append((1 if (dag_sign and tree_sign) else 0, shared_floor, dag_ratio * tree_ratio, label))
        print(
            f"{label:>22s}: dag {dag_anchor:+.4f}->{dag_high:+.4f} (|mag| {dag_ratio:.4f}, sign={dag_sign}) | "
            f"tree {tree_anchor:+.4f}->{tree_high:+.4f} (|mag| {tree_ratio:.4f}, sign={tree_sign})"
        )
    print()
    ranked.sort(reverse=True)
    if ranked:
        sign_flag, shared_floor, _combined, best_label = ranked[0]
        print("Interpretation:")
        if best_label == "packet_flow_action":
            print(
                "  The compressed packet-local forward-flow readout now survives on both the random-DAG "
                "family and the branching-tree control, so the retained gravity observable can be stated "
                "as packet-local action flow rather than the broader node-weight action channel."
            )
        elif best_label == "packet_action_channel":
            print(
                "  Packet-localization helps, but the surviving transfer read is still node-weighted rather "
                "than fully flow-based; the geometry compression is real, but action flow has not fully won yet."
            )
        elif best_label == "action_channel":
            print(
                "  The older action_channel still transfers best. The smaller packet-local cuts help on one "
                "family but do not yet beat the coarser near-mass readout across both families."
            )
        else:
            print(
                "  Detector centroid still transfers best here, so the packet-local action compression did not "
                "yet earn the retained claim on the two-family test."
            )
        print(
            f"  Best shared endpoint retention is {best_label} with weakest-family |mag| ratio {shared_floor:.4f} "
            f"and two-family sign stability={bool(sign_flag)}."
        )


if __name__ == "__main__":
    main()
