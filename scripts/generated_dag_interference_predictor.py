#!/usr/bin/env python3
"""Find which generated-graph observable predicts interference strength.

Across seeds, V(y=0) varies from 0.08 to 0.99. What structural
feature of the random graph determines this?

Candidates:
1. Path count ratio (paths through upper slit / paths through lower slit)
2. Amplitude ratio (|A_upper| / |A_lower| at the detector)
3. Local connectivity near the barrier
4. Slit-to-detector path diversity
5. Graph clustering near the slits

Method: generate 30 random DAGs, measure V(y=0) and all candidate
observables, then correlate.

PStack experiment: interference-predictor
"""

from __future__ import annotations
import math
import cmath
import random
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import (
    generate_causal_dag,
    path_sum_on_dag,
)
from toy_event_physics import (
    RulePostulates,
    derive_local_rule,
    derive_node_field,
    local_edge_properties,
)


def per_slit_amplitude(
    positions, adj, arrival, source_idx,
    detector_x, detector_y, detector_tol,
    barrier_x, slit_ys, slit_width,
) -> dict[str, complex]:
    """Decompose detector amplitude by which slit the path used."""
    n = len(positions)
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    node_field = {i: 0.0 for i in range(n)}

    order = sorted(range(n), key=lambda i: arrival[i])
    # state: (node_idx, slit_label) -> amplitude
    states: dict[tuple[int, str], complex] = {(source_idx, "pre"): 1.0 + 0.0j}
    result: dict[str, complex] = defaultdict(complex)

    for i in order:
        matching = [(k, a) for k, a in list(states.items()) if k[0] == i]
        if not matching:
            continue
        x, y = positions[i]
        if abs(x - detector_x) < 0.5 and abs(y - detector_y) < detector_tol:
            for (_, label), amp in matching:
                result[label] += amp
                del states[(i, label)]
            continue
        if abs(x - detector_x) < 0.5:
            for k, _ in matching:
                del states[k]
            continue

        for (idx, label), amp in matching:
            del states[(idx, label)]
            for j in adj.get(i, []):
                jx, jy = positions[j]
                dist = math.dist(positions[i], positions[j])
                delay = dist
                action = delay
                link_amp = cmath.exp(1j * 4.0 * action) / max(delay, 0.01)

                new_label = label
                if x < barrier_x <= jx:
                    for sy in slit_ys:
                        if abs(jy - sy) < slit_width:
                            new_label = f"slit_{sy:.0f}"
                            break
                    else:
                        link_amp = 0.0  # blocked by barrier

                if (j, new_label) not in states:
                    states[(j, new_label)] = 0.0 + 0.0j
                states[(j, new_label)] += amp * link_amp

    return dict(result)


def count_barrier_paths(adj, positions, arrival, barrier_x, slit_ys, slit_width):
    """Count nodes reachable through each slit region."""
    n = len(positions)
    order = sorted(range(n), key=lambda i: arrival[i])
    # Track which slit each node was reached through
    slit_reach: dict[int, set] = defaultdict(set)
    slit_reach[0] = {"source"}

    for i in order:
        if i not in slit_reach:
            continue
        x, y = positions[i]
        for j in adj.get(i, []):
            jx, jy = positions[j]
            if x < barrier_x <= jx:
                # Barrier crossing — check if through a slit
                through_slit = None
                for sy in slit_ys:
                    if abs(jy - sy) < slit_width:
                        through_slit = f"slit_{sy:.0f}"
                        break
                if through_slit:
                    slit_reach[j].add(through_slit)
            else:
                slit_reach[j].update(slit_reach[i])

    # Count post-barrier nodes reachable through each slit
    upper_count = sum(1 for i, slits in slit_reach.items()
                      if any("3" in s for s in slits) and positions[i][0] > barrier_x)
    lower_count = sum(1 for i, slits in slit_reach.items()
                      if any("-3" in s for s in slits) and positions[i][0] > barrier_x)
    both_count = sum(1 for i, slits in slit_reach.items()
                     if len(slits) >= 2 and positions[i][0] > barrier_x)

    return upper_count, lower_count, both_count


def graph_observables(positions, adj, arrival, barrier_x, slit_ys, slit_width):
    """Compute structural observables of the generated graph."""
    n = len(positions)

    # Degree stats near barrier
    barrier_nodes = [i for i in range(n) if abs(positions[i][0] - barrier_x) < 2]
    barrier_degrees = [len(adj.get(i, [])) for i in barrier_nodes]

    # Slit node counts
    slit_nodes = [i for i in range(n)
                  if abs(positions[i][0] - barrier_x) < 0.5
                  and any(abs(positions[i][1] - sy) < slit_width for sy in slit_ys)]

    # Post-barrier connectivity
    post_barrier = [i for i in range(n) if positions[i][0] > barrier_x]
    post_degrees = [len(adj.get(i, [])) for i in post_barrier]

    # Path reachability
    upper_reach, lower_reach, both_reach = count_barrier_paths(
        adj, positions, arrival, barrier_x, slit_ys, slit_width)

    return {
        "n_slit_nodes": len(slit_nodes),
        "mean_barrier_degree": sum(barrier_degrees) / max(len(barrier_degrees), 1),
        "mean_post_degree": sum(post_degrees) / max(len(post_degrees), 1),
        "upper_reach": upper_reach,
        "lower_reach": lower_reach,
        "both_reach": both_reach,
        "reach_ratio": min(upper_reach, lower_reach) / max(upper_reach, lower_reach, 1),
        "both_fraction": both_reach / max(len(post_barrier), 1),
    }


def main() -> None:
    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    barrier_layer = 12
    detector_layer = n_layers - 1
    slit_ys = [-3.0, 3.0]
    slit_width = 1.5
    n_phases = 16
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    detector_tol = 1.5

    print("=" * 80)
    print("INTERFERENCE PREDICTOR: Which graph observable determines V?")
    print("=" * 80)
    print()

    seeds = list(range(30))
    results = []

    print(f"{'seed':>5s}  {'V(y=0)':>8s}  {'amp_ratio':>10s}  {'reach_ratio':>11s}  "
          f"{'both_frac':>10s}  {'slit_nodes':>10s}  {'barrier_deg':>11s}")
    print("-" * 80)

    for seed in seeds:
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )

        # Measure V(y=0)
        probs = []
        for phase in phases:
            dist = path_sum_on_dag(
                positions, adj, arrival, 0,
                float(detector_layer), [0.0], detector_tol,
                float(barrier_layer), slit_ys, slit_width,
                phase_shift_upper=phase,
            )
            probs.append(dist.get(0.0, 0.0))

        if any(p > 0 for p in probs):
            pm, pn = max(probs), min(probs)
            v = (pm - pn) / (pm + pn)
        else:
            v = -1.0

        # Per-slit amplitudes
        amps = per_slit_amplitude(
            positions, adj, arrival, 0,
            float(detector_layer), 0.0, detector_tol,
            float(barrier_layer), slit_ys, slit_width,
        )
        slit_mags = {k: abs(a) for k, a in amps.items() if k.startswith("slit")}
        if len(slit_mags) >= 2:
            vals = sorted(slit_mags.values())
            amp_ratio = vals[0] / vals[-1] if vals[-1] > 0 else 0
        elif len(slit_mags) == 1:
            amp_ratio = 0.0  # Only one slit contributes
        else:
            amp_ratio = -1.0

        # Graph observables
        obs = graph_observables(positions, adj, arrival, float(barrier_layer), slit_ys, slit_width)

        row = {"seed": seed, "V": v, "amp_ratio": amp_ratio, **obs}
        results.append(row)

        print(f"{seed:5d}  {v:8.4f}  {amp_ratio:10.4f}  {obs['reach_ratio']:11.4f}  "
              f"{obs['both_fraction']:10.4f}  {obs['n_slit_nodes']:10d}  "
              f"{obs['mean_barrier_degree']:11.2f}")

    # Correlation analysis
    print()
    print("=" * 80)
    print("CORRELATION: Which observable best predicts V(y=0)?")
    print("=" * 80)
    print()

    valid = [r for r in results if r["V"] >= 0]
    if len(valid) < 5:
        print("  Too few valid data points")
        return

    v_values = [r["V"] for r in valid]
    observables = ["amp_ratio", "reach_ratio", "both_fraction", "n_slit_nodes", "mean_barrier_degree"]

    for obs_name in observables:
        obs_values = [r[obs_name] for r in valid]
        # Pearson correlation
        n = len(valid)
        mean_v = sum(v_values) / n
        mean_o = sum(obs_values) / n
        cov = sum((v - mean_v) * (o - mean_o) for v, o in zip(v_values, obs_values)) / n
        std_v = math.sqrt(sum((v - mean_v) ** 2 for v in v_values) / n)
        std_o = math.sqrt(sum((o - mean_o) ** 2 for o in obs_values) / n)
        corr = cov / (std_v * std_o) if std_v > 0 and std_o > 0 else 0

        print(f"  {obs_name:>20s}: correlation with V = {corr:+.4f}")

    # Best predictor details
    print()
    best = max(observables, key=lambda o: abs(
        sum((r["V"] - sum(r2["V"] for r2 in valid)/len(valid)) *
            (r[o] - sum(r2[o] for r2 in valid)/len(valid))
            for r in valid)))
    print(f"  Best predictor: {best}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
