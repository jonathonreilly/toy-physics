#!/usr/bin/env python3
"""Three-slit interference: does adding a third slit produce qualitatively
different interference structure compared to two slits?

Tests whether the model produces genuine multi-path interference (three
amplitudes combining) or just pairwise effects.

PStack experiment: three-slit interference
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


def multi_slit_distribution(
    screen_positions: list[int],
    record_created: bool,
    width: int, height: int,
    slit_ys: set[int],
    source: tuple[int, int] = (1, 0),
    phase_shifts: dict[int, float] | None = None,
    normalize: bool = True,
) -> dict[int, float]:
    """N-slit distribution with optional per-slit phase shifts."""
    if phase_shifts is None:
        phase_shifts = {}
    barrier_x = width // 2
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
                        next_sector = f"slit_{neighbor[1]}"
                    ps = phase_shifts.get(neighbor[1], 0.0)
                    if ps != 0.0:
                        link_amp *= cmath.exp(1j * ps)
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


def run_slit_config(label: str, slit_ys: set[int], width: int, height: int,
                    phase_slit_y: int | None = None) -> None:
    """Run a full phase sweep + distribution for a slit configuration."""
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    screen_ys = list(range(-height, height + 1))

    print(f"\n{'=' * 60}")
    print(f"CONFIG: {label}")
    print(f"  slits at y={sorted(slit_ys)}, width={width}")
    if phase_slit_y is not None:
        print(f"  phase sweep on slit y={phase_slit_y}")
    print(f"{'=' * 60}")

    # Distribution at zero phase shift
    for record in [False, True]:
        mode = "RECORD" if record else "COHERENT"
        dist = multi_slit_distribution(
            screen_positions=screen_ys, record_created=record,
            width=width, height=height, slit_ys=slit_ys,
            normalize=True,
        )
        print(f"\n  P(y) at zero phase, {mode}:")
        for y in screen_ys:
            p = dist.get(y, 0)
            bar = "#" * int(p * 80)
            marker = " <-- slit" if y in slit_ys else ""
            print(f"  {y:+4d}  {p:.6f}  {bar}{marker}")

    # Visibility profile with phase sweep on one slit
    if phase_slit_y is not None:
        vis_by_y: dict[int, float] = {}
        for y in screen_ys:
            probs = []
            for phase in phases:
                dist = multi_slit_distribution(
                    screen_positions=[y], record_created=False,
                    width=width, height=height, slit_ys=slit_ys,
                    phase_shifts={phase_slit_y: phase}, normalize=False,
                )
                probs.append(dist[y])
            vis_by_y[y] = visibility(probs)

        mean_v = sum(vis_by_y.values()) / len(vis_by_y)
        print(f"\n  V(y) profile (phase sweep on slit y={phase_slit_y}), COHERENT:")
        print(f"  mean_V = {mean_v:.6f}")
        for y in screen_ys:
            v = vis_by_y[y]
            bar = "#" * int(v * 50)
            marker = " <-- slit" if y in slit_ys else ""
            print(f"  {y:+4d}  {v:10.6f}  {bar}{marker}")


def main() -> None:
    w = 20
    h = 10

    print("=" * 72)
    print("THREE-SLIT INTERFERENCE COMPARISON")
    print("=" * 72)

    # Two-slit baseline
    run_slit_config("TWO-SLIT BASELINE (y=±4)", {-4, 4}, w, h, phase_slit_y=4)

    # Three-slit: symmetric
    run_slit_config("THREE-SLIT SYMMETRIC (y=-4, 0, +4)", {-4, 0, 4}, w, h, phase_slit_y=4)

    # Three-slit: asymmetric
    run_slit_config("THREE-SLIT ASYMMETRIC (y=-4, +2, +6)", {-4, 2, 6}, w, h, phase_slit_y=6)

    # Four-slit
    run_slit_config("FOUR-SLIT (y=-6, -2, +2, +6)", {-6, -2, 2, 6}, w, h, phase_slit_y=6)

    # Single slit (control — should have zero visibility)
    run_slit_config("SINGLE-SLIT CONTROL (y=0)", {0}, w, h, phase_slit_y=0)

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
