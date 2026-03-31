#!/usr/bin/env python3
"""Opaque mass decoherence with corrected propagator.

With transparent mass (field only affects phase), decoherence was weak
(5/12) because uniform attenuation preserves coherence.

With opaque mass (mass nodes BLOCK paths), decoherence should be
stronger because removing paths fundamentally changes which-path
information, regardless of attenuation model.

Previous result: opaque oscillation gave 8-16x stronger decoherence
than field-only with standard propagator. Does this hold with 1/L^p?

PStack experiment: corrected-opaque-decoherence
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


def pathsum_corrected(positions, adj, field, source_indices, detector_indices,
                      phase_k, atten_power=1.0,
                      barrier_indices=None, slit_indices=None,
                      opaque_indices=None):
    """Corrected propagator with optional barrier/slits and opaque nodes."""
    n = len(positions)
    blocked = set()
    if barrier_indices is not None and slit_indices is not None:
        blocked = set(barrier_indices) - set(slit_indices)
    if opaque_indices:
        blocked |= set(opaque_indices)

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


def visibility(probs, positions):
    if not probs:
        return 0.0
    prob_by_y = defaultdict(float)
    for d, p in probs.items():
        prob_by_y[positions[d][1]] += p
    ys = sorted(prob_by_y.keys())
    if len(ys) < 3:
        return 0.0
    vals = [prob_by_y[y] for y in ys]
    peaks = []
    troughs = []
    for i in range(1, len(vals) - 1):
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]:
            peaks.append(vals[i])
        if vals[i] < vals[i-1] and vals[i] < vals[i+1]:
            troughs.append(vals[i])
    if peaks and troughs:
        mx = max(peaks)
        mn = min(troughs)
        return (mx - mn) / (mx + mn) if (mx + mn) > 0 else 0
    return 0.0


def main() -> None:
    n_layers = 15
    nodes_per_layer = 25
    connect_radius = 3.0
    n_seeds = 12
    k_band = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

    print("=" * 80)
    print("OPAQUE MASS DECOHERENCE WITH CORRECTED PROPAGATOR")
    print("=" * 80)
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
        if len(layers) < 6:
            continue

        source_indices = by_layer[layers[0]]
        detector_indices = by_layer[layers[-1]]
        mid = len(layers) // 2

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)

        # Mass nodes: 3 layers, above center
        mass_layers = [layers[mid - 1], layers[mid], layers[mid + 1]]
        mass_indices = []
        for l in mass_layers:
            mass_indices.extend(i for i in by_layer[l] if positions[i][1] > center_y + 1)
        if len(mass_indices) < 3:
            continue

        mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)

        # Barrier for interference
        barrier_layer = layers[mid - 3] if mid - 3 >= 0 else layers[1]
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

        # k-averaged measurements
        grav_shifts = []
        v_free_list = []
        v_transparent_list = []
        v_opaque_list = []

        for k in k_band:
            # GRAVITY: centroid shift
            fp = pathsum_corrected(positions, adj, free_field, source_indices,
                                   detector_indices, phase_k=k)
            mp_t = pathsum_corrected(positions, adj, mass_field, source_indices,
                                     detector_indices, phase_k=k)
            mp_o = pathsum_corrected(positions, adj, free_field, source_indices,
                                     detector_indices, phase_k=k,
                                     opaque_indices=mass_indices)

            fcy = centroid_y(fp, positions)
            tcy = centroid_y(mp_t, positions)
            ocy = centroid_y(mp_o, positions)
            grav_shifts.append(tcy - fcy)

            # INTERFERENCE: visibility through slits
            # Free (no mass)
            bp_free = pathsum_corrected(positions, adj, free_field, source_indices,
                                        detector_indices, phase_k=k,
                                        barrier_indices=barrier_indices,
                                        slit_indices=slit_indices)
            v_free_list.append(visibility(bp_free, positions))

            # Transparent mass (field only)
            bp_trans = pathsum_corrected(positions, adj, mass_field, source_indices,
                                         detector_indices, phase_k=k,
                                         barrier_indices=barrier_indices,
                                         slit_indices=slit_indices)
            v_transparent_list.append(visibility(bp_trans, positions))

            # Opaque mass (blocks paths)
            bp_opaque = pathsum_corrected(positions, adj, free_field, source_indices,
                                          detector_indices, phase_k=k,
                                          barrier_indices=barrier_indices,
                                          slit_indices=slit_indices,
                                          opaque_indices=mass_indices)
            v_opaque_list.append(visibility(bp_opaque, positions))

        avg_grav = sum(grav_shifts) / len(grav_shifts)
        avg_v_free = sum(v_free_list) / len(v_free_list)
        avg_v_trans = sum(v_transparent_list) / len(v_transparent_list)
        avg_v_opaque = sum(v_opaque_list) / len(v_opaque_list)

        toward = mass_cy - center_y
        attracts = (toward > 0 and avg_grav > 0.05) or (toward < 0 and avg_grav < -0.05)
        decoh_trans = avg_v_free - avg_v_trans
        decoh_opaque = avg_v_free - avg_v_opaque

        results.append({
            'seed': seed,
            'grav': avg_grav,
            'attracts': attracts,
            'v_free': avg_v_free,
            'v_trans': avg_v_trans,
            'v_opaque': avg_v_opaque,
            'decoh_trans': decoh_trans,
            'decoh_opaque': decoh_opaque,
        })

    # ================================================================
    # RESULTS
    # ================================================================
    print(f"  {'seed':>4s}  {'grav':>7s}  {'attr':>4s}  "
          f"{'V_free':>6s}  {'V_tran':>6s}  {'V_opaq':>6s}  "
          f"{'d_tran':>6s}  {'d_opaq':>6s}  {'ratio':>6s}")
    print(f"  {'-' * 60}")

    grav_yes = 0
    trans_decoh_yes = 0
    opaque_decoh_yes = 0
    all_three = 0
    ratios = []

    for r in results:
        ratio = r['decoh_opaque'] / r['decoh_trans'] if abs(r['decoh_trans']) > 0.001 else 0
        ratios.append(ratio)

        if r['attracts']:
            grav_yes += 1
        if r['decoh_trans'] > 0.01:
            trans_decoh_yes += 1
        if r['decoh_opaque'] > 0.01:
            opaque_decoh_yes += 1
        if r['attracts'] and r['v_free'] > 0.05 and r['decoh_opaque'] > 0.01:
            all_three += 1

        print(f"  {r['seed']:4d}  {r['grav']:+7.3f}  "
              f"{'Y' if r['attracts'] else 'n':>4s}  "
              f"{r['v_free']:6.3f}  {r['v_trans']:6.3f}  {r['v_opaque']:6.3f}  "
              f"{r['decoh_trans']:+6.3f}  {r['decoh_opaque']:+6.3f}  "
              f"{ratio:6.1f}x")

    n = len(results)
    print()
    print(f"  Gravity (attraction): {grav_yes}/{n}")
    print(f"  Interference (V>0.05): {sum(1 for r in results if r['v_free'] > 0.05)}/{n}")
    print(f"  Decoherence (transparent): {trans_decoh_yes}/{n}")
    print(f"  Decoherence (opaque): {opaque_decoh_yes}/{n}")
    print(f"  ALL THREE (grav + interf + opaque decoh): {all_three}/{n}")

    if ratios:
        pos_ratios = [r for r in ratios if r > 0]
        if pos_ratios:
            print(f"\n  Opaque/transparent decoherence ratio: {sum(pos_ratios)/len(pos_ratios):.1f}x average")

    print()
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    print()
    print("Transparent mass: field shifts phase but doesn't block paths.")
    print("  → Weak decoherence (paths still exist, just phase-shifted)")
    print()
    print("Opaque mass: active nodes block paths entirely.")
    print("  → Strong decoherence (which-path info recorded by removal)")
    print("  → This is the physical mechanism: persistent patterns are OPAQUE")
    print("    because they occupy nodes, preventing other signals from passing")
    print()
    print("With corrected propagator (1/L^p):")
    print("  - Gravity comes from PHASE (transparent field)")
    print("  - Decoherence comes from OPACITY (path blocking)")
    print("  - Two DIFFERENT mechanisms, both from same mass")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
