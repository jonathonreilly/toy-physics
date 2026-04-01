#!/usr/bin/env python3
"""G2: Coarse-grained propagator.

Instead of summing over all microscopic paths, group paths into
"bundles" by their coarse y-trajectory (which y-bin they pass through
at each layer). Each bundle contributes one effective amplitude.

Near-degenerate paths within a bundle interfere internally, producing
a bundle amplitude. The detector probability is the path-sum over
bundles, not microscopic paths. This naturally reduces path multiplicity.

Implementation: at each layer, bin nodes by y-position into N_bins
coarse bins. Amplitude propagates between coarse bins, not individual
nodes. Within each bin, the microscopic amplitudes are summed (internal
interference), then the bin emits a single effective amplitude.

Pass criterion: R_grav should not collapse to plateau on DAG family.

PStack experiment: g2-coarse-grained-propagator
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import compute_field, centroid_y


def propagate_coarse_grained(positions, adj, field, src, det, k, n_ybins=6):
    """Coarse-grained propagator: bin nodes by y at each layer.

    At each layer, nodes are grouped into y-bins. Within each bin,
    amplitudes are summed (coherent within bin). Between layers,
    amplitude propagates from bin to bin using the average edge
    properties of the bin-to-bin connections.
    """
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    all_ys = [y for _, y in positions]
    y_min = min(all_ys)
    y_max = max(all_ys)
    y_range = y_max - y_min + 1e-10
    bin_width = y_range / n_ybins

    def y_bin(y):
        return min(int((y - y_min) / bin_width), n_ybins - 1)

    # Initialize: amplitude at source nodes
    # Bin by y at each layer, propagate between layers
    # State: {(layer_idx, y_bin): amplitude}
    state = defaultdict(complex)
    for s in src:
        yb = y_bin(positions[s][1])
        state[(0, yb)] += 1.0 / len(src)

    for li in range(len(layers) - 1):
        curr_layer = layers[li]
        next_layer = layers[li + 1]
        curr_nodes = by_layer[curr_layer]
        next_nodes = by_layer[next_layer]

        # Group current and next nodes by y-bin
        curr_bins = defaultdict(list)
        for i in curr_nodes:
            curr_bins[y_bin(positions[i][1])].append(i)

        next_bins = defaultdict(list)
        for j in next_nodes:
            next_bins[y_bin(positions[j][1])].append(j)

        # For each curr_bin → next_bin: compute average edge amplitude
        new_state = defaultdict(complex)
        for cb, cb_nodes in curr_bins.items():
            amp = state.get((li, cb), 0.0 + 0.0j)
            if abs(amp) < 1e-30:
                continue

            # Find all edges from this bin to next layer, grouped by dest bin
            dest_amps = defaultdict(list)
            for i in cb_nodes:
                for j in adj.get(i, []):
                    if j not in set(next_nodes):
                        continue
                    nb = y_bin(positions[j][1])
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    L = math.sqrt((x2-x1)**2+(y2-y1)**2)
                    if L < 1e-10:
                        continue
                    lf = 0.5*(field[i]+field[j])
                    dl = L*(1+lf)
                    ret = math.sqrt(max(dl*dl-L*L, 0))
                    act = dl-ret
                    ea = cmath.exp(1j*k*act)/(L**1.0)
                    dest_amps[nb].append(ea)

            # Each destination bin gets the AVERAGE edge amplitude × source amp
            for nb, eas in dest_amps.items():
                avg_ea = sum(eas) / len(eas)  # coherent average within bundle
                new_state[(li+1, nb)] += amp * avg_ea

        state.update(new_state)

    # Collect at detector layer: distribute bin amplitude evenly among
    # detector nodes in that bin to avoid occupancy-count distortion.
    det_layer_idx = len(layers) - 1

    # Group detector nodes by bin
    det_by_bin = defaultdict(list)
    for d in det:
        det_by_bin[y_bin(positions[d][1])].append(d)

    probs = {}
    for yb, d_nodes in det_by_bin.items():
        bin_amp = state.get((det_layer_idx, yb), 0.0+0.0j)
        bin_prob = abs(bin_amp)**2
        # Distribute bin probability evenly among nodes in this bin
        per_node = bin_prob / len(d_nodes) if d_nodes else 0
        for d in d_nodes:
            probs[d] = per_node

    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("G2: COARSE-GRAINED PROPAGATOR")
    print("  Bin nodes by y, propagate between bins")
    print("=" * 70)
    print()

    # Pass: R_grav should not collapse from N=12 to N=25
    for n_bins in [4, 6, 8, 12]:
        print(f"  n_ybins = {n_bins}:")
        print(f"    {'N_layers':>8s}  {'R_grav_std':>10s}  {'R_grav_cg':>10s}  {'k0_cg':>8s}")
        print(f"    {'-' * 40}")

        for nl in [8, 12, 15, 20, 25]:
            rg_std, rg_cg, k0s = [], [], []
            for seed in range(5):
                positions, adj, _ = generate_causal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed*11+7)
                n = len(positions)
                by_layer = defaultdict(list)
                for idx, (x, y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 5:
                    continue

                src = by_layer[layers[0]]
                det = set(by_layer[layers[-1]])
                if not det:
                    continue

                all_ys = [y for _, y in positions]
                cy = sum(all_ys)/len(all_ys)
                mid = len(layers)//2
                grav_mass = [i for i in by_layer[layers[mid]] if positions[i][1] > cy+2]
                if len(grav_mass) < 2:
                    continue

                free_f = [0.0]*n
                field = compute_field(positions, adj, grav_mass)

                # Standard propagator
                from scripts.two_register_decoherence import pathsum_coherent
                std_shifts = []
                for k in k_band:
                    fp = pathsum_coherent(positions, adj, free_f, src, det, k)
                    mp = pathsum_coherent(positions, adj, field, src, det, k)
                    std_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

                # Coarse-grained
                cg_shifts = []
                for k in k_band:
                    fp = propagate_coarse_grained(positions, adj, free_f, src, det, k, n_bins)
                    mp = propagate_coarse_grained(positions, adj, field, src, det, k, n_bins)
                    cg_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))

                # Beam width
                fp0 = pathsum_coherent(positions, adj, free_f, src, det, 5.0)
                total = sum(fp0.values())
                width = 1.0
                if total > 0:
                    mean = sum(positions[d][1]*p for d, p in fp0.items())/total
                    var = sum(positions[d][1]**2*p for d, p in fp0.items())/total - mean**2
                    width = max(var**0.5, 0.1)

                rg_std.append(sum(std_shifts)/len(std_shifts) / width)
                rg_cg.append(sum(cg_shifts)/len(cg_shifts) / width)

                # k=0 check
                fp0 = propagate_coarse_grained(positions, adj, free_f, src, det, 0.0, n_bins)
                mp0 = propagate_coarse_grained(positions, adj, field, src, det, 0.0, n_bins)
                k0s.append(centroid_y(mp0, positions) - centroid_y(fp0, positions))

            if rg_std:
                k0_avg = sum(abs(s) for s in k0s)/len(k0s)
                print(f"    {nl:8d}  {sum(rg_std)/len(rg_std):+10.3f}  "
                      f"{sum(rg_cg)/len(rg_cg):+10.3f}  {k0_avg:8.5f}")

        print()

    print("PASS: R_grav_cg at N=25 >= R_grav_cg at N=12")
    print("FAIL: R_grav_cg collapses like R_grav_std")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
