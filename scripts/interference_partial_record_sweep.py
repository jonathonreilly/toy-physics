#!/usr/bin/env python3
"""Sweep partial record probability from 0 to 1 to measure decoherence curve.

Implements probabilistic record creation: at the barrier, each path
creates a durable record with probability p. Sweeps p to find V(p).
PStack experiment: partial-records
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


def partial_record_two_slit(
    screen_positions: list[int],
    record_probability: float,
    width: int = 16, height: int = 10,
    slit_ys: set[int] | None = None,
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Two-slit with probabilistic record creation.

    At the barrier crossing, each path splits into:
    - recorded branch (probability p): amplitude *= sqrt(p), gets sector label
    - unrecorded branch (probability 1-p): amplitude *= sqrt(1-p), stays coherent

    At the detector:
    - recorded sectors: probabilities add (no interference)
    - unrecorded sector: amplitudes add coherently (interference)
    - total probability = sum of all sector probabilities
    """
    if slit_ys is None:
        slit_ys = {-4, 4}
    barrier_x = width // 2
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    source = (1, 0)
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    # State: (node, heading, sector) -> amplitude
    # Sectors: "none" (pre-barrier), "coherent" (unrecorded), "upper" / "lower" (recorded)
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j
    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    sqrt_p = math.sqrt(record_probability) if record_probability > 0 else 0.0
    sqrt_1mp = math.sqrt(1.0 - record_probability) if record_probability < 1 else 0.0

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
                phase_link_amp = link_amp
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    if neighbor[1] > 0:
                        phase_link_amp = link_amp * cmath.exp(1j * phase_shift_upper)

                    if record_probability == 0.0:
                        # Pure coherent
                        states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), "coherent")] += amp * phase_link_amp
                    elif record_probability == 1.0:
                        # Pure record
                        rec_sector = "upper" if neighbor[1] > 0 else "lower"
                        states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), rec_sector)] += amp * phase_link_amp
                    else:
                        # Split: recorded branch
                        rec_sector = "upper" if neighbor[1] > 0 else "lower"
                        states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), rec_sector)] += amp * phase_link_amp * sqrt_p
                        # Unrecorded branch
                        states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), "coherent")] += amp * phase_link_amp * sqrt_1mp
                else:
                    states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]), sector)] += amp * link_amp

    distribution: dict[int, float] = {}
    for y in screen_positions:
        sector_amps = boundary_distribution.get(y, {})
        # Coherent sector: amplitudes add, then square
        coherent_amp = sector_amps.get("coherent", 0.0) + sector_amps.get("none", 0.0)
        coherent_prob = abs(coherent_amp) ** 2
        # Recorded sectors: probabilities add
        recorded_prob = sum(
            abs(a) ** 2 for k, a in sector_amps.items()
            if k not in ("coherent", "none")
        )
        distribution[y] = coherent_prob + recorded_prob

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
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    p_values = [i * 0.05 for i in range(21)]  # 0.00, 0.05, ..., 1.00
    height = 10

    configs = [
        ("width=16, slit_sep=8", 16, {-4, 4}),
        ("width=24, slit_sep=4", 24, {-2, 2}),
        ("width=20, slit_sep=12", 20, {-6, 6}),
    ]

    print("=" * 72)
    print("PARTIAL RECORD DECOHERENCE SWEEP")
    print("=" * 72)
    print(f"record_probabilities: {[f'{p:.2f}' for p in p_values]}")
    print(f"configurations: {[c[0] for c in configs]}")
    print()

    for label, w, slits in configs:
        print(f"\n{'=' * 60}")
        print(f"CONFIG: {label}")
        print(f"{'=' * 60}")
        print()
        print(f"{'p':>6s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  {'mean_V':>10s}")
        print("-" * 52)

        for p in p_values:
            screen_ys = list(range(-height, height + 1))
            vis_by_y: dict[int, float] = {}
            for y in screen_ys:
                probs = []
                for phase in phases:
                    dist = partial_record_two_slit(
                        screen_positions=[y], record_probability=p,
                        width=w, height=height, slit_ys=slits,
                        phase_shift_upper=phase, normalize=False,
                    )
                    probs.append(dist[y])
                vis_by_y[y] = visibility(probs)

            mean_v = sum(vis_by_y.values()) / len(vis_by_y)
            print(f"{p:6.2f}  {vis_by_y[0]:10.6f}  {vis_by_y.get(1, 0):10.6f}  "
                  f"{vis_by_y.get(2, 0):10.6f}  {mean_v:10.6f}")

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
