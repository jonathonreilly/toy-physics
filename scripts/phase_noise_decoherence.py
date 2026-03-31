#!/usr/bin/env python3
"""Phase noise decoherence: stochastic dephasing with corrected propagator.

The corrected propagator (1/L^p) is too coherent for decoherence.
Physical decoherence comes from environment coupling → random phase kicks.

Model: each edge amplitude gets a random phase factor exp(iη·ξ) where
ξ ~ N(0,1) and η is the noise strength. Average probability over many
noise realizations. At η=0: full coherence. At large η: full decoherence.

Key test: does phase noise reduce V (decoherence) while preserving
the gravitational centroid shift (attraction)?

If yes: complete model = corrected propagator + phase noise.
  - Gravity from phase structure (unitary)
  - Decoherence from phase noise (non-unitary)
  - Interference from coherent limit (η→0)

PStack experiment: phase-noise-decoherence
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
    local_edge_properties,
)


def propagate_with_noise(
    nodes, source, node_field, rule, dag, arrival_times,
    blocked, screen_ys, det_x, noise_eta, rng,
):
    """Propagate with random phase noise on each edge."""
    order = sorted(arrival_times, key=arrival_times.get)
    amplitudes = {source: 1.0 + 0.0j}

    for node in order:
        if node not in amplitudes or node in blocked:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
            _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
            # Add random phase noise
            noise_phase = noise_eta * rng.gauss(0, 1)
            noisy_amp = link_amp * cmath.exp(1j * noise_phase)
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * noisy_amp

    return {y: abs(amplitudes.get((det_x, y), 0.0)) ** 2 for y in screen_ys}


def visibility(probs, screen_ys):
    vals = [probs.get(y, 0) for y in sorted(screen_ys)]
    peaks = [vals[i] for i in range(1, len(vals) - 1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals) - 1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
    return 0.0


def centroid_y(probs, screen_ys):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in probs.items()) / total


def main() -> None:
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))

    barrier_x = 20
    det_x = 40
    slit_ys = [-4, 4]

    barrier_all = set()
    for y in range(-height, height + 1):
        barrier_all.add((barrier_x, y))
    slit_nodes = set()
    for sy in slit_ys:
        for y in range(sy - 1, sy + 2):
            slit_nodes.add((barrier_x, y))
    blocked = barrier_all - slit_nodes

    postulates = RulePostulates(
        phase_per_action=2.0, attenuation_power=1.0,
        attenuation_mode="geometry",
    )
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)

    # Mass for gravity test
    mass_nodes = frozenset((25, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    n_realizations = 30

    print("=" * 80)
    print("PHASE NOISE DECOHERENCE")
    print(f"  Grid: {width}x{2*height+1}, k=2.0, corrected propagator")
    print(f"  {n_realizations} noise realizations per η value")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Noise strength vs visibility (interference)
    # ================================================================
    print("TEST 1: Noise η vs fringe visibility V")
    print()

    print(f"  {'eta':>8s}  {'mean_V':>8s}  {'std_V':>8s}  {'V/V0':>6s}")
    print(f"  {'-' * 34}")

    v0 = None
    for eta in [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
        v_list = []
        for i in range(n_realizations):
            rng = random.Random(i * 31 + 7)
            probs = propagate_with_noise(
                nodes, source, field, rule, dag, arrival_times,
                blocked, screen_ys, det_x, eta, rng,
            )
            v_list.append(visibility(probs, screen_ys))

        mean_v = sum(v_list) / len(v_list)
        std_v = (sum((v - mean_v) ** 2 for v in v_list) / len(v_list)) ** 0.5

        if v0 is None:
            v0 = mean_v
        ratio = mean_v / v0 if v0 > 0 else 0

        print(f"  {eta:8.3f}  {mean_v:8.4f}  {std_v:8.4f}  {ratio:6.2f}")

    # ================================================================
    # TEST 2: Noise vs gravity (does attraction survive?)
    # ================================================================
    print()
    print("TEST 2: Noise η vs gravitational centroid shift")
    print("  Mass at x=25, y=4..8")
    print()

    det_grav = [30, 35, 40, 45]
    print(f"  {'eta':>8s}  {'mean_shift':>10s}  {'std_shift':>10s}  {'attracts':>8s}")
    print(f"  {'-' * 42}")

    for eta in [0.0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]:
        shift_list = []
        for i in range(n_realizations):
            rng_free = random.Random(i * 31 + 7)
            rng_mass = random.Random(i * 31 + 7)  # Same noise seed for fair comparison

            # Free propagation (no barrier for gravity test)
            free_probs = propagate_with_noise(
                nodes, source, field, rule, dag, arrival_times,
                set(), screen_ys, det_x, eta, rng_free,
            )

            # Mass propagation
            mass_arrival = infer_arrival_times_from_source(nodes, source, mass_rule)
            mass_dag = build_causal_dag(nodes, mass_arrival)
            mass_probs = propagate_with_noise(
                nodes, source, mass_field, mass_rule, mass_dag, mass_arrival,
                set(), screen_ys, det_x, eta, rng_mass,
            )

            fcy = centroid_y(free_probs, screen_ys)
            mcy = centroid_y(mass_probs, screen_ys)
            shift_list.append(mcy - fcy)

        mean_shift = sum(shift_list) / len(shift_list)
        std_shift = (sum((s - mean_shift) ** 2 for s in shift_list) / len(shift_list)) ** 0.5
        attracts = "YES" if mean_shift > 0.5 else "weak" if mean_shift > 0.1 else "no"

        print(f"  {eta:8.3f}  {mean_shift:+10.3f}  {std_shift:10.3f}  {attracts:>8s}")

    # ================================================================
    # TEST 3: Phase diagram — V and gravity shift vs η
    # ================================================================
    print()
    print("TEST 3: Phase diagram — can we have V↓ AND shift↑?")
    print("  Find η where V drops significantly but shift remains positive")
    print()

    print(f"  {'eta':>8s}  {'V':>8s}  {'shift':>8s}  {'V_drop%':>8s}  {'regime':>20s}")
    print(f"  {'-' * 58}")

    for eta in [0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0]:
        # Interference
        v_list = []
        for i in range(20):
            rng = random.Random(i * 31 + 7)
            probs = propagate_with_noise(
                nodes, source, field, rule, dag, arrival_times,
                blocked, screen_ys, det_x, eta, rng,
            )
            v_list.append(visibility(probs, screen_ys))
        mean_v = sum(v_list) / len(v_list)

        # Gravity
        shift_list = []
        for i in range(20):
            rng_f = random.Random(i * 31 + 7)
            rng_m = random.Random(i * 31 + 7)
            fp = propagate_with_noise(
                nodes, source, field, rule, dag, arrival_times,
                set(), screen_ys, det_x, eta, rng_f,
            )
            mass_arrival = infer_arrival_times_from_source(nodes, source, mass_rule)
            mass_dag = build_causal_dag(nodes, mass_arrival)
            mp = propagate_with_noise(
                nodes, source, mass_field, mass_rule, mass_dag, mass_arrival,
                set(), screen_ys, det_x, eta, rng_m,
            )
            shift_list.append(centroid_y(mp, screen_ys) - centroid_y(fp, screen_ys))
        mean_shift = sum(shift_list) / len(shift_list)

        v_drop = (1 - mean_v / v0) * 100 if v0 > 0 else 0

        if mean_v > 0.5 and mean_shift > 0.5:
            regime = "coherent + gravity"
        elif mean_v < 0.3 and mean_shift > 0.5:
            regime = "DECOHERENT + gravity"
        elif mean_v < 0.3 and mean_shift < 0.5:
            regime = "fully decoherent"
        else:
            regime = "transitional"

        print(f"  {eta:8.3f}  {mean_v:8.4f}  {mean_shift:+8.3f}  {v_drop:7.1f}%  {regime:>20s}")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("If there exists an η where V drops but shift remains:")
    print("  → Complete model = corrected propagator + phase noise")
    print("  → Gravity from phase structure (deterministic, unitary)")
    print("  → Decoherence from noise (stochastic, non-unitary)")
    print("  → The η parameter controls the quantum-to-classical transition")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
