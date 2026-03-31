#!/usr/bin/env python3
"""Compress open/closed-slit DAG rewiring into a small scalar family.

The fixed-DAG Sorkin test established that the apparent three-slit signal is
not a Born-rule violation. The remaining question is which compact observable
best summarizes the topology-change effect across the tested geometries.

This script joins the original open/closed-slit Sorkin ratios to per-closure
DAG observables and ranks small scalar candidates by how well they track the
spike size on a log scale.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import os
import sys
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    local_edge_properties,
)


@dataclass(frozen=True)
class SlitConfig:
    label: str
    slit_ys: tuple[int, int, int]
    width: int = 20
    height: int = 10


@dataclass(frozen=True)
class NetworkState:
    nodes: frozenset[tuple[int, int]]
    arrival_times: dict[tuple[int, int], float]
    edges: frozenset[tuple[tuple[int, int], tuple[int, int]]]


CONFIGS = (
    SlitConfig("SYMMETRIC", (-4, 0, 4)),
    SlitConfig("CLOSE", (-2, 0, 2)),
    SlitConfig("WIDE", (-6, 0, 6)),
    SlitConfig("ASYMMETRIC", (-4, 1, 6)),
)


def make_rule():
    return derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )


def build_state(config: SlitConfig, open_slits: tuple[int, ...]) -> NetworkState:
    barrier_x = config.width // 2
    blocked_nodes = frozenset(
        (barrier_x, y)
        for y in range(-config.height, config.height + 1)
        if y not in open_slits
    )
    nodes = build_rectangular_nodes(
        width=config.width,
        height=config.height,
        blocked_nodes=blocked_nodes,
    )
    arrival_times = infer_arrival_times_from_source(nodes, (1, 0), make_rule())
    dag = build_causal_dag(nodes, arrival_times)
    edges = frozenset(
        (source, target)
        for source, targets in dag.items()
        for target in targets
    )
    return NetworkState(
        nodes=frozenset(nodes),
        arrival_times=arrival_times,
        edges=edges,
    )


def slit_distribution(config: SlitConfig, open_slits: tuple[int, ...]) -> dict[int, float]:
    barrier_x = config.width // 2
    detector_x = config.width
    nodes = build_rectangular_nodes(
        width=config.width,
        height=config.height,
        blocked_nodes=frozenset(
            (barrier_x, y)
            for y in range(-config.height, config.height + 1)
            if y not in open_slits
        ),
    )
    rule = make_rule()
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, (1, 0), rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    states: DefaultDict[tuple[tuple[int, int], tuple[int, int]], complex] = defaultdict(complex)
    states[((1, 0), (1, 0))] = 1.0 + 0.0j
    boundary_amps: DefaultDict[int, complex] = defaultdict(complex)

    for node in order:
        matching = [(state, amp) for state, amp in list(states.items()) if state[0] == node]
        if not matching:
            continue
        if node[0] == detector_x:
            for state, amp in matching:
                boundary_amps[node[1]] += amp
                del states[state]
            continue
        for (cur, heading), amp in matching:
            del states[(cur, heading)]
            for neighbor in dag.get(node, []):
                _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)
                new_heading = (neighbor[0] - node[0], neighbor[1] - node[1])
                states[(neighbor, new_heading)] += amp * link_amp

    return {
        y: abs(boundary_amps.get(y, 0.0)) ** 2
        for y in range(-config.height, config.height + 1)
    }


def edge_region(
    edge: tuple[tuple[int, int], tuple[int, int]],
    barrier_x: int,
) -> str:
    source, target = edge
    if source[0] < barrier_x and target[0] <= barrier_x:
        return "pre"
    if source[0] < barrier_x <= target[0]:
        return "cross"
    return "post"


def closure_metrics(config: SlitConfig, closed_slit: int) -> dict[str, float]:
    full_state = build_state(config, config.slit_ys)
    pair_slits = tuple(y for y in config.slit_ys if y != closed_slit)
    pair_state = build_state(config, pair_slits)
    barrier_x = config.width // 2

    changed_arrivals = {
        node: pair_state.arrival_times[node] - full_state.arrival_times[node]
        for node in (full_state.nodes & pair_state.nodes)
        if pair_state.arrival_times[node] != full_state.arrival_times[node]
    }
    changed_post = {
        node: delta
        for node, delta in changed_arrivals.items()
        if node[0] >= barrier_x
    }

    edge_delta_by_region = {region: 0 for region in ("pre", "cross", "post")}
    for edge in (full_state.edges - pair_state.edges) | (pair_state.edges - full_state.edges):
        edge_delta_by_region[edge_region(edge, barrier_x)] += 1

    detector_deltas = [
        delta
        for node, delta in changed_post.items()
        if node[0] == config.width
    ]
    return {
        "closed_slit": float(closed_slit),
        "post_edge_delta": float(edge_delta_by_region["post"]),
        "changed_post_nodes": float(len(changed_post)),
        "max_post_delay": max(changed_post.values(), default=0.0),
        "sum_post_delay": sum(changed_post.values()),
        "detector_max_delay": max(detector_deltas, default=0.0),
        "detector_sum_delay": sum(detector_deltas),
    }


def sorkin_ratio(config: SlitConfig) -> float:
    ya, yb, yc = config.slit_ys
    p_abc = slit_distribution(config, config.slit_ys)
    p_ab = slit_distribution(config, (ya, yb))
    p_ac = slit_distribution(config, (ya, yc))
    p_bc = slit_distribution(config, (yb, yc))
    p_a = slit_distribution(config, (ya,))
    p_b = slit_distribution(config, (yb,))
    p_c = slit_distribution(config, (yc,))

    i3_values = {
        y: (
            p_abc[y]
            - p_ab[y]
            - p_ac[y]
            - p_bc[y]
            + p_a[y]
            + p_b[y]
            + p_c[y]
        )
        for y in p_abc
    }
    max_prob = max(max(p_abc.values()), 1e-30)
    max_i3 = max(abs(value) for value in i3_values.values())
    return max_i3 / max_prob


def pearson(xs: list[float], ys: list[float]) -> float:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = sum((x - mean_x) ** 2 for x in xs)
    den_y = sum((y - mean_y) ** 2 for y in ys)
    den = math.sqrt(den_x * den_y)
    return num / den if den else 0.0


def fit_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0.0
    intercept = mean_y - slope * mean_x
    return intercept, slope


def aggregate_metrics(per_closure: list[dict[str, float]]) -> dict[str, float]:
    return {
        "sum_post_edge_delta": sum(row["post_edge_delta"] for row in per_closure),
        "sum_post_delay": sum(row["sum_post_delay"] for row in per_closure),
        "sum_detector_max_delay": sum(row["detector_max_delay"] for row in per_closure),
        "sum_detector_delay": sum(row["detector_sum_delay"] for row in per_closure),
        "max_post_delay": max(row["max_post_delay"] for row in per_closure),
    }


def main() -> None:
    per_config: list[tuple[SlitConfig, float, list[dict[str, float]], dict[str, float]]] = []
    for config in CONFIGS:
        rows = [closure_metrics(config, closed_slit) for closed_slit in config.slit_ys]
        ratio = sorkin_ratio(config)
        per_config.append((config, ratio, rows, aggregate_metrics(rows)))

    candidate_names = [
        "sum_detector_max_delay",
        "sum_post_delay",
        "sum_detector_delay",
        "sum_post_edge_delta",
        "max_post_delay",
    ]
    log_ratios = [math.log10(ratio) for _, ratio, _, _ in per_config]
    ranked = []
    for name in candidate_names:
        log_values = [
            math.log10(max(aggregate[name], 1e-30))
            for _, _, _, aggregate in per_config
        ]
        ranked.append((abs(pearson(log_values, log_ratios)), name, log_values))
    ranked.sort(reverse=True)

    best_corr, best_name, best_logs = ranked[0]
    intercept, slope = fit_line(best_logs, log_ratios)

    print("=" * 88)
    print("INTERFERENCE DAG RECONFIGURATION ORDER PARAMETER")
    print("=" * 88)
    print("Join the open/closed-slit Sorkin spike size to compact DAG-reconfiguration scalars.")
    print("All ratios below are max |I_3| / max |P_ABC| on the original open/closed DAG.")
    print()

    for config, ratio, rows, aggregate in per_config:
        print("=" * 88)
        print(f"{config.label}: slits={config.slit_ys}")
        print("=" * 88)
        print(
            "  closed slit   post_edges   post_nodes   max_post_dt   "
            "sum_post_dt   detector_max_dt   detector_sum_dt"
        )
        print("  " + "-" * 78)
        for row in rows:
            print(
                f"  {int(row['closed_slit']):+11d}"
                f"   {int(row['post_edge_delta']):10d}"
                f"   {int(row['changed_post_nodes']):10d}"
                f"   {row['max_post_delay']:11.6f}"
                f"   {row['sum_post_delay']:11.6f}"
                f"   {row['detector_max_delay']:16.6f}"
                f"   {row['detector_sum_delay']:16.6f}"
            )
        print()
        print(f"  max |I_3| / max |P_ABC| = {ratio:.6e}")
        print(
            "  aggregates: "
            f"sum_post_edge_delta={aggregate['sum_post_edge_delta']:.0f}, "
            f"sum_post_delay={aggregate['sum_post_delay']:.6f}, "
            f"sum_detector_max_delay={aggregate['sum_detector_max_delay']:.6f}, "
            f"sum_detector_delay={aggregate['sum_detector_delay']:.6f}, "
            f"max_post_delay={aggregate['max_post_delay']:.6f}"
        )
        print()

    print("=" * 88)
    print("CANDIDATE RANKING")
    print("=" * 88)
    print("Ranked by |Pearson corr(log10(candidate), log10(max |I_3| / max |P_ABC|))|.")
    for corr_value, name, _ in ranked:
        print(f"  {name:23s} corr={corr_value:.4f}")
    print()
    print("Best single scalar on the tested four-geometry set:")
    print(f"  {best_name}  (corr={best_corr:.4f})")
    print(
        "  fit: log10(max |I_3| / max |P_ABC|) = "
        f"{intercept:.3f} + {slope:.3f} * log10({best_name})"
    )
    print()
    print("Per-geometry best-scalar fit:")
    for config, ratio, _, aggregate in per_config:
        x = math.log10(max(aggregate[best_name], 1e-30))
        predicted = intercept + slope * x
        actual = math.log10(ratio)
        print(
            f"  {config.label:11s} actual={actual:7.3f}  "
            f"predicted={predicted:7.3f}  residual={actual - predicted:+7.3f}"
        )
    print()
    print("PHYSICAL READING")
    print(
        "  The large open/closed-slit Sorkin spike is best compressed by detector-side "
        "retiming, not by raw edge rewiring counts. Post-barrier topology changes matter "
        "because they retime the detector boundary, and that retiming is what the path-sum "
        "amplifies into the huge apparent higher-order signal."
    )


if __name__ == "__main__":
    main()
