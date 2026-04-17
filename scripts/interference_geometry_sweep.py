#!/usr/bin/env python3
"""Sweep grid geometry parameters for the two-slit interference setup.

Measures fringe contrast as a function of grid width and slit separation,
with and without durable record formation.

PStack experiment: interference-geometry-sensitivity
"""

from __future__ import annotations

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict
from typing import DefaultDict

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    local_edge_properties,
)
import cmath


def parameterized_two_slit_distribution(
    screen_positions: list[int],
    record_created: bool,
    width: int = 16,
    height: int = 10,
    barrier_x: int | None = None,
    slit_ys: set[int] | None = None,
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Two-slit distribution with configurable geometry."""

    if barrier_x is None:
        barrier_x = width // 2
    if slit_ys is None:
        slit_ys = {-4, 4}

    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(
            phase_per_action=4.0,
            attenuation_power=1.0,
        ),
    )
    source = (1, 0)
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y)
        for y in range(-height, height + 1)
        if y not in slit_ys
    )
    nodes = build_rectangular_nodes(
        width=width,
        height=height,
        blocked_nodes=blocked_nodes,
    )
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j
    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    for node in order:
        matching_states = [
            (state, amplitude)
            for state, amplitude in list(states.items())
            if state[0] == node
        ]
        if not matching_states:
            continue

        if node[0] == detector_x:
            for state, amplitude in matching_states:
                _current_node, _heading, sector = state
                boundary_distribution[node[1]][sector] += amplitude
                del states[state]
            continue

        for (current_node, heading, sector), amplitude in matching_states:
            del states[(current_node, heading, sector)]
            for neighbor in dag.get(node, []):
                dx = neighbor[0] - node[0]
                dy = neighbor[1] - node[1]
                next_heading = (dx, dy)
                _delay, _action_increment, link_amplitude = local_edge_properties(
                    node,
                    neighbor,
                    rule,
                    node_field,
                )

                next_sector = sector
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    if record_created:
                        next_sector = "upper" if neighbor[1] > 0 else "lower"
                    if neighbor[1] > 0:
                        link_amplitude *= cmath.exp(1j * phase_shift_upper)

                states[(neighbor, next_heading, next_sector)] += amplitude * link_amplitude

    distribution: dict[int, float] = {}
    for y in screen_positions:
        sector_amplitudes = boundary_distribution.get(y, {})
        if record_created:
            probability = sum(abs(amplitude) ** 2 for amplitude in sector_amplitudes.values())
        else:
            probability = abs(sum(sector_amplitudes.values())) ** 2
        distribution[y] = probability

    if not normalize:
        return distribution

    normalizer = sum(distribution.values())
    if normalizer == 0:
        return {y: 0.0 for y in screen_positions}
    return {y: probability / normalizer for y, probability in distribution.items()}


def fringe_contrast(probs_by_phase: list[float]) -> float:
    """Visibility V = (max - min) / (max + min)."""
    if not probs_by_phase:
        return 0.0
    p_max = max(probs_by_phase)
    p_min = min(probs_by_phase)
    denom = p_max + p_min
    if denom == 0:
        return 0.0
    return (p_max - p_min) / denom


def main() -> None:
    widths = [8, 12, 16, 20, 24, 28]
    slit_half_seps = [2, 4, 6, 8]
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    height = 10

    print("=" * 72)
    print("INTERFERENCE GEOMETRY SWEEP")
    print("=" * 72)
    print(f"widths: {widths}")
    print(f"slit_half_separations: {slit_half_seps}")
    print(f"phase_steps: {n_phases}")
    print(f"height: {height}")
    print()

    # Baseline validation: reproduce default geometry
    print("--- BASELINE VALIDATION (width=16, slit_sep=4, no record) ---")
    baseline_probs = []
    for phase in phases:
        dist = parameterized_two_slit_distribution(
            screen_positions=[0],
            record_created=False,
            width=16,
            height=10,
            slit_ys={-4, 4},
            phase_shift_upper=phase,
            normalize=False,
        )
        baseline_probs.append(dist[0])
    baseline_max = max(baseline_probs)
    normalized_baseline = [p / baseline_max if baseline_max > 0 else 0 for p in baseline_probs]
    print(f"baseline_center_phase_response: {[round(p, 4) for p in normalized_baseline]}")
    print(f"baseline_contrast: {fringe_contrast(baseline_probs):.6f}")
    print()

    # Main sweep
    print("--- GEOMETRY SWEEP ---")
    print()

    results = []

    for w in widths:
        for slit_half in slit_half_seps:
            if slit_half >= height:
                print(f"SKIP width={w} slit_half={slit_half} (slit outside grid)")
                continue

            barrier_x = w // 2
            slit_ys_set = {-slit_half, slit_half}
            screen_ys = list(range(-height, height + 1))

            for record in [False, True]:
                phase_probs_center = []
                for phase in phases:
                    dist = parameterized_two_slit_distribution(
                        screen_positions=[0],
                        record_created=record,
                        width=w,
                        height=height,
                        barrier_x=barrier_x,
                        slit_ys=slit_ys_set,
                        phase_shift_upper=phase,
                        normalize=False,
                    )
                    phase_probs_center.append(dist[0])

                contrast = fringe_contrast(phase_probs_center)

                # Full distribution at phase=0 for this geometry
                full_dist = parameterized_two_slit_distribution(
                    screen_positions=screen_ys,
                    record_created=record,
                    width=w,
                    height=height,
                    barrier_x=barrier_x,
                    slit_ys=slit_ys_set,
                    phase_shift_upper=0.0,
                    normalize=True,
                )

                record_label = "RECORD" if record else "COHERENT"
                result_row = {
                    "width": w,
                    "slit_half_sep": slit_half,
                    "record": record,
                    "contrast": contrast,
                    "center_prob_phase0": full_dist.get(0, 0.0),
                    "center_prob_max": max(phase_probs_center),
                    "center_prob_min": min(phase_probs_center),
                }
                results.append(result_row)

                print(f"width={w:3d}  slit_half={slit_half}  mode={record_label:8s}  "
                      f"contrast={contrast:.6f}  "
                      f"center_range=[{min(phase_probs_center):.6f}, {max(phase_probs_center):.6f}]")

    print()
    print("--- CONTRAST SUMMARY TABLE ---")
    print()
    print(f"{'width':>6s} {'slit_sep':>8s} {'coherent':>10s} {'record':>10s} {'ratio':>10s}")
    print("-" * 50)

    for w in widths:
        for slit_half in slit_half_seps:
            if slit_half >= height:
                continue
            coherent = [r for r in results if r["width"] == w and r["slit_half_sep"] == slit_half and not r["record"]]
            record = [r for r in results if r["width"] == w and r["slit_half_sep"] == slit_half and r["record"]]
            if coherent and record:
                c_val = coherent[0]["contrast"]
                r_val = record[0]["contrast"]
                ratio = r_val / c_val if c_val > 0 else float("inf")
                print(f"{w:6d} {slit_half * 2:8d} {c_val:10.6f} {r_val:10.6f} {ratio:10.6f}")

    print()
    print("--- FULL DISTRIBUTION AT PHASE=0, COHERENT MODE (selected geometries) ---")
    print()
    selected_geometries = [(16, 4), (8, 4), (28, 4), (16, 2), (16, 8)]
    for w, slit_half in selected_geometries:
        if slit_half >= height:
            continue
        barrier_x = w // 2
        slit_ys_set = {-slit_half, slit_half}
        screen_ys = list(range(-height, height + 1))
        dist = parameterized_two_slit_distribution(
            screen_positions=screen_ys,
            record_created=False,
            width=w,
            height=height,
            barrier_x=barrier_x,
            slit_ys=slit_ys_set,
            phase_shift_upper=0.0,
            normalize=True,
        )
        print(f"width={w}, slit_sep={slit_half * 2}:")
        for y in screen_ys:
            bar = "#" * int(dist.get(y, 0) * 100)
            print(f"  y={y:+3d}: {dist.get(y, 0):.6f} {bar}")
        print()

    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
