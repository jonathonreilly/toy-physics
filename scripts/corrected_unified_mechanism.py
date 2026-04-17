#!/usr/bin/env python3
"""Unified mechanism with corrected propagator.

The standard propagator (1/delay^p attenuation) produces:
  - Gravity: REPULSION (wrong sign)
  - Interference: YES
  - Decoherence: YES

The corrected propagator (1/L^p attenuation) produces:
  - Gravity: ATTRACTION (correct!)
  - Interference: ???
  - Decoherence: ???

This test checks all three phenomena with the corrected propagator
on generated causal DAGs using a single oscillating pattern as the
mass source.

PStack experiment: corrected-unified-mechanism
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field_on_dag(positions, adj, mass_indices, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_indices)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        new_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                new_field[i] = 1.0
                continue
            nbs = undirected.get(i, set())
            if nbs:
                new_field[i] = sum(field[j] for j in nbs) / len(nbs)
        field = new_field
    return field


def pathsum_corrected(
    positions, adj, field, source_indices, detector_indices,
    phase_k, atten_power,
    barrier_indices=None, slit_indices=None,
):
    """Path-sum with geometry-only attenuation (1/L^p).

    If barrier_indices and slit_indices provided, blocks barrier
    except slit nodes (for interference test).
    """
    n = len(positions)
    blocked = set()
    if barrier_indices is not None and slit_indices is not None:
        blocked = set(barrier_indices) - set(slit_indices)

    in_degree = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_degree[j] += 1

    from collections import deque
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)

    amplitudes = [0.0 + 0.0j] * n
    for s in source_indices:
        amplitudes[s] = 1.0 / len(source_indices) + 0.0j

    for i in order:
        if i in blocked:
            continue
        amp = amplitudes[i]
        if abs(amp) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power)
            ea = cmath.exp(1j * phase_k * action) * atten
            amplitudes[j] += amp * ea

    probs = {}
    for d in detector_indices:
        probs[d] = abs(amplitudes[d]) ** 2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def visibility(probs, positions, n_bins=20):
    """Compute fringe visibility from probability distribution."""
    if not probs:
        return 0.0

    ys = sorted(set(positions[d][1] for d in probs))
    if len(ys) < 3:
        return 0.0

    prob_by_y = defaultdict(float)
    for d, p in probs.items():
        prob_by_y[positions[d][1]] += p

    vals = [prob_by_y[y] for y in ys]

    peaks = []
    troughs = []
    for i in range(1, len(vals) - 1):
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]:
            peaks.append(vals[i])
        if vals[i] < vals[i-1] and vals[i] < vals[i+1]:
            troughs.append(vals[i])

    if peaks and troughs:
        max_p = max(peaks)
        min_t = min(troughs)
        return (max_p - min_t) / (max_p + min_t) if (max_p + min_t) > 0 else 0
    return 0.0


def main() -> None:
    n_layers = 15
    nodes_per_layer = 25
    connect_radius = 3.0
    phase_k = 5.5  # In the attraction sweet spot for DAGs
    atten_power = 1.0
    n_seeds = 12

    print("=" * 80)
    print("CORRECTED UNIFIED MECHANISM TEST")
    print("  Propagator: exp(i*k*S_spent) / L^p")
    print("  Does one pattern produce gravity + interference + decoherence?")
    print("=" * 80)
    print(f"  DAG: {n_layers} layers × {nodes_per_layer} nodes, radius={connect_radius}")
    print(f"  k={phase_k}, atten_power={atten_power}, seeds={n_seeds}")
    print()

    results = []

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius, rng_seed=seed * 11 + 7,
        )

        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 5:
            continue

        source_indices = by_layer[layers[0]]
        detector_indices = by_layer[layers[-1]]

        # Mass in middle layers (simulating persistent pattern)
        mid = len(layers) // 2
        mass_layers = [layers[mid - 1], layers[mid], layers[mid + 1]]

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)

        # Mass above center
        mass_indices = []
        for l in mass_layers:
            mass_indices.extend(i for i in by_layer[l] if positions[i][1] > center_y + 1)
        if len(mass_indices) < 3:
            continue

        mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)

        # Barrier layer for interference test (before mass)
        barrier_layer = layers[mid - 2]
        barrier_indices = by_layer[barrier_layer]

        # Select "slits" — two groups of nodes, above and below center
        slit_above = [i for i in barrier_indices if positions[i][1] > center_y + 2]
        slit_below = [i for i in barrier_indices if positions[i][1] < center_y - 2]

        if not slit_above or not slit_below:
            continue

        # Pick 2-3 nodes from each group as slits
        slit_a = slit_above[:min(3, len(slit_above))]
        slit_b = slit_below[:min(3, len(slit_below))]
        slit_indices = slit_a + slit_b

        # ============================
        # TEST A: GRAVITY (attraction)
        # ============================
        free_field = [0.0] * len(positions)
        mass_field = compute_field_on_dag(positions, adj, mass_indices)

        free_probs = pathsum_corrected(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, atten_power,
        )
        mass_probs = pathsum_corrected(
            positions, adj, mass_field, source_indices, detector_indices,
            phase_k, atten_power,
        )

        fcy = centroid_y(free_probs, positions)
        mcy = centroid_y(mass_probs, positions)
        gravity_shift = mcy - fcy
        toward_mass = mass_cy - center_y
        gravity_attracts = (toward_mass > 0 and gravity_shift > 0.05) or \
                           (toward_mass < 0 and gravity_shift < -0.05)

        # ============================
        # TEST B: INTERFERENCE (visibility)
        # ============================
        # Both slits open
        both_probs = pathsum_corrected(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, atten_power,
            barrier_indices=barrier_indices, slit_indices=slit_indices,
        )
        V_both = visibility(both_probs, positions)

        # Single slit A only
        single_probs = pathsum_corrected(
            positions, adj, free_field, source_indices, detector_indices,
            phase_k, atten_power,
            barrier_indices=barrier_indices, slit_indices=slit_a,
        )
        V_single = visibility(single_probs, positions)

        # Interference = visibility with both slits > single slit
        interference_present = V_both > 0.05

        # ============================
        # TEST C: DECOHERENCE (mass reduces visibility)
        # ============================
        both_mass_probs = pathsum_corrected(
            positions, adj, mass_field, source_indices, detector_indices,
            phase_k, atten_power,
            barrier_indices=barrier_indices, slit_indices=slit_indices,
        )
        V_mass = visibility(both_mass_probs, positions)

        decoherence = V_both - V_mass
        decoherence_present = decoherence > 0.01

        results.append({
            'seed': seed,
            'gravity_shift': gravity_shift,
            'gravity_attracts': gravity_attracts,
            'V_both': V_both,
            'V_single': V_single,
            'interference': interference_present,
            'V_mass': V_mass,
            'decoherence': decoherence,
            'decoherence_present': decoherence_present,
        })

    # ================================================================
    # RESULTS TABLE
    # ================================================================
    print(f"  {'seed':>4s}  {'grav_shift':>10s}  {'attract':>7s}  "
          f"{'V_both':>7s}  {'V_mass':>7s}  {'interf':>6s}  "
          f"{'decoh':>7s}  {'all_3':>5s}")
    print(f"  {'-' * 68}")

    all_three = 0
    grav_yes = 0
    interf_yes = 0
    decoh_yes = 0

    for r in results:
        a3 = r['gravity_attracts'] and r['interference'] and r['decoherence_present']
        if a3:
            all_three += 1
        if r['gravity_attracts']:
            grav_yes += 1
        if r['interference']:
            interf_yes += 1
        if r['decoherence_present']:
            decoh_yes += 1

        print(f"  {r['seed']:4d}  {r['gravity_shift']:+10.3f}  "
              f"{'YES' if r['gravity_attracts'] else 'no':>7s}  "
              f"{r['V_both']:7.3f}  {r['V_mass']:7.3f}  "
              f"{'YES' if r['interference'] else 'no':>6s}  "
              f"{r['decoherence']:+7.3f}  "
              f"{'YES' if a3 else 'no':>5s}")

    n = len(results)
    print()
    print(f"  Gravity (attraction): {grav_yes}/{n}")
    print(f"  Interference (V>0.05): {interf_yes}/{n}")
    print(f"  Decoherence (V drops): {decoh_yes}/{n}")
    print(f"  ALL THREE: {all_three}/{n}")

    # ================================================================
    # k-averaged version
    # ================================================================
    print()
    print("=" * 80)
    print("k-AVERAGED UNIFIED MECHANISM (k=3..8, 6 values)")
    print("=" * 80)
    print()

    k_band = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    ka_results = []

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius, rng_seed=seed * 11 + 7,
        )

        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 5:
            continue

        source_indices = by_layer[layers[0]]
        detector_indices = by_layer[layers[-1]]
        mid = len(layers) // 2
        mass_layers = [layers[mid - 1], layers[mid], layers[mid + 1]]

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)

        mass_indices = []
        for l in mass_layers:
            mass_indices.extend(i for i in by_layer[l] if positions[i][1] > center_y + 1)
        if len(mass_indices) < 3:
            continue

        mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)

        barrier_layer = layers[mid - 2]
        barrier_indices = by_layer[barrier_layer]
        slit_above = [i for i in barrier_indices if positions[i][1] > center_y + 2]
        slit_below = [i for i in barrier_indices if positions[i][1] < center_y - 2]
        if not slit_above or not slit_below:
            continue
        slit_a = slit_above[:min(3, len(slit_above))]
        slit_b = slit_below[:min(3, len(slit_below))]
        slit_indices = slit_a + slit_b

        free_field = [0.0] * len(positions)
        mass_field = compute_field_on_dag(positions, adj, mass_indices)

        # Average gravity shift over k
        grav_shifts = []
        for k in k_band:
            fp = pathsum_corrected(positions, adj, free_field, source_indices,
                                   detector_indices, k, atten_power)
            mp = pathsum_corrected(positions, adj, mass_field, source_indices,
                                   detector_indices, k, atten_power)
            fcy = centroid_y(fp, positions)
            mcy = centroid_y(mp, positions)
            grav_shifts.append(mcy - fcy)

        avg_grav = sum(grav_shifts) / len(grav_shifts)
        toward_mass = mass_cy - center_y
        grav_ok = (toward_mass > 0 and avg_grav > 0.05) or \
                  (toward_mass < 0 and avg_grav < -0.05)

        # Average interference V over k
        v_boths = []
        v_masses = []
        for k in k_band:
            bp = pathsum_corrected(positions, adj, free_field, source_indices,
                                   detector_indices, k, atten_power,
                                   barrier_indices, slit_indices)
            v_boths.append(visibility(bp, positions))

            bmp = pathsum_corrected(positions, adj, mass_field, source_indices,
                                    detector_indices, k, atten_power,
                                    barrier_indices, slit_indices)
            v_masses.append(visibility(bmp, positions))

        avg_v = sum(v_boths) / len(v_boths)
        avg_vm = sum(v_masses) / len(v_masses)
        interf_ok = avg_v > 0.05
        decoh_ok = (avg_v - avg_vm) > 0.01

        a3 = grav_ok and interf_ok and decoh_ok

        ka_results.append({
            'seed': seed, 'avg_grav': avg_grav, 'grav_ok': grav_ok,
            'avg_v': avg_v, 'avg_vm': avg_vm, 'interf_ok': interf_ok,
            'decoh_ok': decoh_ok, 'all_three': a3,
        })

    print(f"  {'seed':>4s}  {'avg_grav':>8s}  {'attract':>7s}  "
          f"{'V_avg':>6s}  {'Vm_avg':>6s}  {'interf':>6s}  "
          f"{'decoh':>5s}  {'all_3':>5s}")
    print(f"  {'-' * 56}")

    ka_grav = ka_interf = ka_decoh = ka_all = 0
    for r in ka_results:
        if r['grav_ok']: ka_grav += 1
        if r['interf_ok']: ka_interf += 1
        if r['decoh_ok']: ka_decoh += 1
        if r['all_three']: ka_all += 1

        print(f"  {r['seed']:4d}  {r['avg_grav']:+8.3f}  "
              f"{'YES' if r['grav_ok'] else 'no':>7s}  "
              f"{r['avg_v']:6.3f}  {r['avg_vm']:6.3f}  "
              f"{'YES' if r['interf_ok'] else 'no':>6s}  "
              f"{'YES' if r['decoh_ok'] else 'no':>5s}  "
              f"{'YES' if r['all_three'] else 'no':>5s}")

    nk = len(ka_results)
    print()
    print(f"  k-averaged: gravity={ka_grav}/{nk}, interference={ka_interf}/{nk}, "
          f"decoherence={ka_decoh}/{nk}, ALL THREE={ka_all}/{nk}")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("If ALL THREE present: the corrected propagator preserves the unified")
    print("mechanism. One oscillating pattern on a random graph produces:")
    print("  1. Gravitational ATTRACTION (correct sign!)")
    print("  2. Interference fringes (wave-like behavior)")
    print("  3. Decoherence (mass reduces fringe visibility)")
    print()
    print("This would mean: gravity, interference, and decoherence all emerge")
    print("from the same minimal structure with a physically motivated propagator.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
