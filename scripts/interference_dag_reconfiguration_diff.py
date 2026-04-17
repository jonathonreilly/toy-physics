#!/usr/bin/env python3
"""Quantify causal-DAG reconfiguration under slit open/close changes.

The fixed-DAG Sorkin test shows the model's interference itself is Born-rule
compliant. This script measures the separate topological effect: how much the
underlying causal DAG rewires when barrier nodes are added or removed by
changing which slits are open.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    infer_arrival_times_from_source,
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
    arrival_times: dict[tuple[int, int], int]
    edges: frozenset[tuple[tuple[int, int], tuple[int, int]]]


CONFIGS = [
    SlitConfig(label="SYMMETRIC", slit_ys=(-4, 0, 4)),
    SlitConfig(label="CLOSE", slit_ys=(-2, 0, 2)),
    SlitConfig(label="WIDE", slit_ys=(-6, 0, 6)),
    SlitConfig(label="ASYMMETRIC", slit_ys=(-4, 1, 6)),
]


def build_state(config: SlitConfig, open_slits: tuple[int, ...]) -> NetworkState:
    barrier_x = config.width // 2
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
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
    arrival_times = infer_arrival_times_from_source(nodes, (1, 0), rule)
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


def render_compare(config: SlitConfig, closed_slit: int) -> str:
    full_state = build_state(config, config.slit_ys)
    pair_slits = tuple(y for y in config.slit_ys if y != closed_slit)
    pair_state = build_state(config, pair_slits)
    barrier_x = config.width // 2

    removed_nodes = sorted(full_state.nodes - pair_state.nodes)
    shared_nodes = sorted(full_state.nodes & pair_state.nodes)
    changed_arrivals = {
        node: pair_state.arrival_times[node] - full_state.arrival_times[node]
        for node in shared_nodes
        if pair_state.arrival_times[node] != full_state.arrival_times[node]
    }
    delayed = sum(1 for delta in changed_arrivals.values() if delta > 0)
    accelerated = sum(1 for delta in changed_arrivals.values() if delta < 0)
    changed_pre = sum(1 for node in changed_arrivals if node[0] < barrier_x)
    changed_post = sum(1 for node in changed_arrivals if node[0] >= barrier_x)
    max_shift_node = None
    max_shift = 0
    if changed_arrivals:
        max_shift_node, max_shift = max(
            changed_arrivals.items(),
            key=lambda item: abs(item[1]),
        )

    edge_only_full = full_state.edges - pair_state.edges
    edge_only_pair = pair_state.edges - full_state.edges
    edge_delta_by_region = {
        region: 0 for region in ("pre", "cross", "post")
    }
    for edge in edge_only_full | edge_only_pair:
        edge_delta_by_region[edge_region(edge, barrier_x)] += 1

    detector_nodes = [
        node for node in changed_arrivals if node[0] == config.width
    ]
    detector_shift_max = max(
        (abs(changed_arrivals[node]) for node in detector_nodes),
        default=0,
    )

    return "\n".join(
        [
            f"close slit y={closed_slit:+d}: {config.slit_ys} -> {pair_slits}",
            f"  removed nodes: {len(removed_nodes)} ({removed_nodes})",
            (
                f"  edges: full={len(full_state.edges)}, pair={len(pair_state.edges)}, "
                f"symmetric delta={len(edge_only_full) + len(edge_only_pair)}"
            ),
            (
                "  edge delta by region: "
                f"pre={edge_delta_by_region['pre']}, "
                f"cross={edge_delta_by_region['cross']}, "
                f"post={edge_delta_by_region['post']}"
            ),
            (
                "  shared-node arrival changes: "
                f"{len(changed_arrivals)}/{len(shared_nodes)} "
                f"(delayed={delayed}, accelerated={accelerated})"
            ),
            (
                "  changed shared nodes by region: "
                f"pre={changed_pre}, post={changed_post}, "
                f"detector max |shift|={detector_shift_max}"
            ),
            (
                "  max shared-node arrival shift: "
                f"{max_shift:+.6f} at {max_shift_node}"
                if max_shift_node is not None
                else "  max shared-node arrival shift: none"
            ),
        ]
    )


def main() -> None:
    print("=" * 72)
    print("INTERFERENCE DAG RECONFIGURATION DIFF")
    print("=" * 72)
    print("Compare a full three-slit DAG against the corresponding two-slit DAGs.")
    print("Counts measure topology changes caused by removing one barrier slit node.")
    print()

    for config in CONFIGS:
        print("=" * 72)
        print(
            f"{config.label}: slits={config.slit_ys}, "
            f"width={config.width}, height={config.height}"
        )
        print("=" * 72)
        for closed_slit in config.slit_ys:
            print(render_compare(config, closed_slit))
            print()

    print("=" * 72)
    print("INTERPRETATION")
    print("=" * 72)
    print(
        "If one removed barrier node triggers large post-barrier edge deltas and "
        "many shared-node arrival-time shifts, the open/closed-slit Sorkin signal "
        "is a topology-change effect rather than a violation of amplitude linearity."
    )


if __name__ == "__main__":
    main()
