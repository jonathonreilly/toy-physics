#!/usr/bin/env python3
"""Break reflection symmetry with asymmetric slit placement and off-center source.

Tests whether the model's interference is a genuine dynamical property
or depends on the symmetric setup.
PStack experiment: asymmetric-interference
"""

from __future__ import annotations
import math, cmath, sys, os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toy_event_physics import (
    RulePostulates, build_causal_dag, build_rectangular_nodes,
    derive_local_rule, derive_node_field, infer_arrival_times_from_source,
    local_edge_properties,
)


def asymmetric_two_slit(
    screen_positions: list[int],
    record_created: bool,
    width: int, height: int,
    barrier_x: int,
    slit_ys: set[int],
    source: tuple[int, int],
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Two-slit distribution with arbitrary source position and slit placement."""
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j
    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )
    # Identify "upper" slit as the one with larger y
    upper_y = max(slit_ys)

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
            for neighbor in dag.get(node, []):
                _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)
                next_sector = sector
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    if record_created:
                        next_sector = "upper" if neighbor[1] == upper_y else "lower"
                    if neighbor[1] == upper_y:
                        link_amp *= cmath.exp(1j * phase_shift_upper)
                states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), next_sector)] += amp * link_amp

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


def run_config(label: str, width: int, height: int, barrier_x: int,
               slit_ys: set[int], source: tuple[int, int]) -> None:
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    screen_ys = list(range(-height, height + 1))

    print(f"\n{'=' * 60}")
    print(f"CONFIG: {label}")
    print(f"  width={width}, height={height}, barrier_x={barrier_x}")
    print(f"  slits at y={sorted(slit_ys)}, source={source}")
    print(f"{'=' * 60}")

    for record in [False, True]:
        mode = "RECORD" if record else "COHERENT"
        vis_by_y: dict[int, float] = {}
        for y in screen_ys:
            probs = []
            for phase in phases:
                dist = asymmetric_two_slit(
                    screen_positions=[y], record_created=record,
                    width=width, height=height, barrier_x=barrier_x,
                    slit_ys=slit_ys, source=source,
                    phase_shift_upper=phase, normalize=False,
                )
                probs.append(dist[y])
            vis_by_y[y] = visibility(probs)

        print(f"\n  --- {mode} mode ---")
        print(f"  {'y':>4s}  {'V(y)':>10s}  bar")
        for y in screen_ys:
            v = vis_by_y[y]
            bar = "#" * int(v * 50)
            marker = " <-- slit" if y in slit_ys else ""
            src_mark = " <-- source" if y == source[1] else ""
            print(f"  {y:+4d}  {v:10.6f}  {bar}{marker}{src_mark}")

        # Distribution at phase=0
        dist0 = asymmetric_two_slit(
            screen_positions=screen_ys, record_created=record,
            width=width, height=height, barrier_x=barrier_x,
            slit_ys=slit_ys, source=source,
            phase_shift_upper=0.0, normalize=True,
        )
        print(f"\n  P(y) at phase=0, {mode}:")
        for y in screen_ys:
            p = dist0.get(y, 0)
            bar = "#" * int(p * 100)
            print(f"  {y:+4d}  {p:.6f}  {bar}")


def main() -> None:
    print("=" * 72)
    print("ASYMMETRIC INTERFERENCE SWEEP")
    print("=" * 72)

    h = 10
    w = 16
    bx = 8

    # 1. Baseline: symmetric
    run_config("SYMMETRIC BASELINE", w, h, bx, {-4, 4}, (1, 0))

    # 2. Asymmetric slits: y=+2 and y=+6
    run_config("ASYMMETRIC SLITS (+2, +6)", w, h, bx, {2, 6}, (1, 0))

    # 3. Strongly asymmetric: y=+1 and y=+8
    run_config("STRONGLY ASYMMETRIC SLITS (+1, +8)", w, h, bx, {1, 8}, (1, 0))

    # 4. Off-center source with symmetric slits
    run_config("OFF-CENTER SOURCE (1,+3), SYMMETRIC SLITS", w, h, bx, {-4, 4}, (1, 3))

    # 5. Off-center source + asymmetric slits
    run_config("OFF-CENTER SOURCE (1,+3) + ASYMMETRIC SLITS (+2, +6)", w, h, bx, {2, 6}, (1, 3))

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
