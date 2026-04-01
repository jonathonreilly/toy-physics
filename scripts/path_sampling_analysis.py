#!/usr/bin/env python3
"""Path sampling analysis: WHY is gravity b-independent?

Hypothesis: b-independence comes from path ensemble averaging.
On any sufficiently connected graph, the set of high-weight paths
to a given detector samples the full transverse extent. So the
average field perturbation is independent of where the mass is.

Testable predictions:
  1. The amplitude-weighted mean y of intermediate nodes should be
     near 0 (center) for ALL detectors, regardless of detector y.
     This means paths to y=+5 and y=-5 both sample y≈0 on average.

  2. The variance of the y-distribution of intermediate nodes
     should be large compared to the mass offset b.
     This means the path ensemble "washes out" the mass position.

  3. If we RESTRICT paths to a narrow transverse band (forcing
     locality), then b-dependence should appear.

PStack experiment: path-sampling-analysis
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_dag(n_layers=18, nodes_per_layer=40, yz_range=12.0,
                    connect_radius=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def propagate_track(positions, adj, src, k):
    """Propagate and track amplitude-weighted y distribution at each layer."""
    n = len(positions)
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    field = [0.0] * n
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * L) * w / L
            amps[j] += amps[i] * ea

    return amps


def main():
    print("=" * 70)
    print("PATH SAMPLING ANALYSIS: Why is gravity b-independent?")
    print("=" * 70)
    print()

    positions, adj, layer_indices = generate_3d_dag(
        n_layers=18, nodes_per_layer=40, yz_range=12.0,
        connect_radius=3.5, rng_seed=42)

    src = layer_indices[0]
    det_list = layer_indices[-1]
    k = 5.0

    amps = propagate_track(positions, adj, src, k)

    # Prediction 1: amplitude-weighted <y> of intermediate nodes
    # conditioned on detector y-position
    print("PREDICTION 1: Path sampling is y-uniform")
    print("  Amplitude-weighted <y> at intermediate layers, by detector y-bin")
    print()

    # Bin detectors by y
    det_bins = {"y<-4": [], "-4<y<-1": [], "-1<y<1": [], "1<y<4": [], "y>4": []}
    for d in det_list:
        y = positions[d][1]
        if y < -4:
            det_bins["y<-4"].append(d)
        elif y < -1:
            det_bins["-4<y<-1"].append(d)
        elif y < 1:
            det_bins["-1<y<1"].append(d)
        elif y < 4:
            det_bins["1<y<4"].append(d)
        else:
            det_bins["y>4"].append(d)

    # For each detector bin, compute what fraction of total probability
    # comes from paths through different y-regions of intermediate layers
    # We approximate this by looking at the amplitude distribution at the
    # mid-layer, weighted by detector amplitude

    mid_layer = layer_indices[len(layer_indices)//2]

    # First, just look at the amplitude distribution at intermediate layers
    print("  Amplitude-weighted <y> at each layer:")
    print(f"  {'layer':>5s}  {'<y>':>8s}  {'std(y)':>8s}  {'n_active':>8s}")
    print(f"  {'-'*36}")

    for li, nodes in enumerate(layer_indices):
        if li == 0 or li == len(layer_indices)-1:
            continue
        total_p = 0
        wy = 0
        wy2 = 0
        n_active = 0
        for i in nodes:
            p = abs(amps[i])**2
            if p > 1e-30:
                n_active += 1
                total_p += p
                wy += p * positions[i][1]
                wy2 += p * positions[i][1]**2
        if total_p > 0:
            mean_y = wy / total_p
            var_y = wy2 / total_p - mean_y**2
            std_y = math.sqrt(max(var_y, 0))
            print(f"  {li:5d}  {mean_y:+8.3f}  {std_y:8.3f}  {n_active:8d}")

    print()
    print("  If <y> ≈ 0 at all layers: paths sample y uniformly")
    print("  If std(y) >> b_max: path ensemble covers full transverse range")
    print()

    # Prediction 2: the amplitude at detectors has WEAK correlation with
    # the transverse position — most amplitude comes from near y=0
    # regardless of detector position
    print("PREDICTION 2: Detector probability vs detector y")
    print(f"  {'y_bin':>12s}  {'mean_P':>10s}  {'n_det':>6s}")
    print(f"  {'-'*32}")

    for bin_name, det_ids in det_bins.items():
        if not det_ids:
            continue
        probs = [abs(amps[d])**2 for d in det_ids]
        mean_p = sum(probs) / len(probs)
        print(f"  {bin_name:>12s}  {mean_p:10.6e}  {len(det_ids):6d}")

    print()

    # Prediction 3: the "effective sampling width" of paths
    # How much of the transverse range does a typical path sample?
    # We measure this by propagating from a single detector BACKWARDS
    # and seeing how spread the amplitude is at the source layer.
    # (Approximation: look at correlation between detector y and mid-layer y)
    print("PREDICTION 3: Detector-conditioned mid-layer y-distribution")
    print("  For detectors at different y, where is the mid-layer amplitude?")
    print()

    # Reverse propagation: for each detector, what's the amplitude-weighted
    # y at the mid-layer? Use forward amps as proxy (not exact but indicative).

    # Actually, let's do something simpler: compute the two-point correlation
    # between mid-layer y and detector y, weighted by amplitude product.

    # Correlation: rho = <y_mid * y_det> / (std_mid * std_det)
    # If rho ≈ 0: mid-layer y is uncorrelated with detector y → b-independent
    # If rho ≈ 1: paths are geometrically local → b-dependent possible

    # Approximate: for each detector d, estimate the "effective mid-layer y"
    # by looking at which mid-layer nodes have high overlap with d's amplitude.

    # Simpler: propagate from SINGLE SOURCE at different y offsets and see
    # how the detector distribution changes. This directly tests whether
    # the graph "remembers" transverse position.

    y_offsets = [-8, -4, 0, 4, 8]
    print(f"  Source y-offset → detector <y>")
    print(f"  {'y_src':>6s}  {'<y_det>':>8s}  {'std_det':>8s}")
    print(f"  {'-'*28}")

    for y_off in y_offsets:
        # Find source-layer node closest to (0, y_off, 0)
        src_layer = layer_indices[0]
        if len(src_layer) == 1:
            # Only one source node — can't offset. Use layer 1 instead.
            src_layer = layer_indices[1]

        # Find closest node to y_off
        best = min(src_layer, key=lambda i: abs(positions[i][1] - y_off))
        src_set = [best]

        amps_off = propagate_track(positions, adj, src_set, k)

        total_p = 0
        wy = 0
        wy2 = 0
        for d in det_list:
            p = abs(amps_off[d])**2
            total_p += p
            wy += p * positions[d][1]
            wy2 += p * positions[d][1]**2

        if total_p > 1e-30:
            mean_det = wy / total_p
            var_det = wy2 / total_p - mean_det**2
            std_det = math.sqrt(max(var_det, 0))
            print(f"  {y_off:+6d}  {mean_det:+8.3f}  {std_det:8.3f}")
        else:
            print(f"  {y_off:+6d}  NO SIGNAL")

    print()
    print("  If <y_det> tracks y_src: graph preserves transverse position")
    print("  If <y_det> ≈ 0 always: graph scrambles position → b-independent")
    print()

    # Summary metric
    print("=" * 70)
    print("SUMMARY")
    print("  b-independence requires: paths at intermediate layers sample")
    print("  the full transverse range, regardless of source/detector position.")
    print("  This 'path scrambling' means mass at any b affects all paths equally.")
    print("=" * 70)


if __name__ == "__main__":
    main()
