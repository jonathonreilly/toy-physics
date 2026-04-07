#!/usr/bin/env python3
"""Off-scaffold held-out test of the free_coh predictor.

The previous cross-generator lanes all placed nodes on the same
(layer, iy, iz) grid with edges varying. The last retained caveat is:

    "All 21 held-out generators share the (layer, iy, iz) grid scaffold;
     generalization beyond that substrate is untested."

This lane removes that caveat. The generators here are LAYERED but
their transverse (y, z) positions are NOT snapped to any integer grid.
Each layer holds exactly n_per_layer points so the existing detector
cz/dp functions still work by node index, but the (y, z) coordinates
are drawn from continuous distributions (uniform, Gaussian, clustered,
rotated, Halton quasi-random).

Connectivity: k nearest forward neighbors by Euclidean distance.

Threshold: `free_coh >= 7.9597e-04`, frozen from the swept-set fit in
global_coherence_predictor.py. Applied WITHOUT REFIT.

Pre-committed predictions (both coh-sign and pass/fail) are hard-coded
BEFORE running. The audit trail is the dict in this source file.

If free_coh generalizes off-scaffold (say >= 65% rule accuracy on this
batch), the last caveat on the classifier lane is cleared. If not, the
grid scaffold was doing work the classifier was attributing to free_coh,
and the classifier program is genuinely closed — the next move is
matter/inertial closure or analytic derivation.
"""

from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import independent_generators_heldout as ind

# Constants (match ind module so battery code works)
NL = ind.NL
PW = ind.PW
H = ind.H
K = ind.K
S_BASE = ind.S_BASE
MASS_Z = ind.MASS_Z

FREE_COH_THRESHOLD = 7.9597e-04
K_NEIGHBORS = 15      # forward neighbor count per node (default)
HW = int(PW / H)
N_PER_LAYER = (2 * HW + 1) ** 2


# ========== OFF-SCAFFOLD LAYERED GENERATORS ==========

def _empty_adj_nmap():
    return {}, {}


def _build_knn_edges(pos, layer_to_indices, k):
    """Connect each node to its k nearest forward (next-layer) neighbors."""
    adj = {}
    layers = sorted(layer_to_indices.keys())
    for l in layers:
        nl = l + 1
        if nl not in layer_to_indices:
            continue
        next_nodes = layer_to_indices[nl]
        for i in layer_to_indices[l]:
            yi, zi = pos[i][1], pos[i][2]
            dists = [(((pos[j][1] - yi) ** 2 + (pos[j][2] - zi) ** 2), j) for j in next_nodes]
            dists.sort()
            adj[i] = [j for _, j in dists[:k]]
    return adj


def _nmap_from_positions(pos, layer_to_indices):
    """Build a nmap that lets `nmap.get((layer, iy, iz))` find the nearest
    node in that layer to (iy*H, iz*H). Enables Born slit source lookup."""
    nmap = {}
    for layer, inds in layer_to_indices.items():
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                ty, tz = iy * H, iz * H
                best = None
                best_d = float("inf")
                for j in inds:
                    d = (pos[j][1] - ty) ** 2 + (pos[j][2] - tz) ** 2
                    if d < best_d:
                        best_d = d
                        best = j
                if best is not None:
                    nmap[(layer, iy, iz)] = best
    return nmap


def _finalize(pos, layer_to_indices, k):
    adj = _build_knn_edges(pos, layer_to_indices, k)
    nmap = _nmap_from_positions(pos, layer_to_indices)
    return pos, adj, nmap


def grow_uniform_random(seed, k=K_NEIGHBORS):
    """Each layer has n_per_layer points uniformly in [-PW, PW]²."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    for layer in range(1, NL):
        x = layer * H
        inds = []
        for _ in range(N_PER_LAYER):
            y = rng.uniform(-PW, PW)
            z = rng.uniform(-PW, PW)
            inds.append(len(pos))
            pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_gaussian_random(seed, k=K_NEIGHBORS, sigma=2.0):
    """Gaussian distribution per layer around (0, 0)."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    for layer in range(1, NL):
        x = layer * H
        inds = []
        for _ in range(N_PER_LAYER):
            y = rng.gauss(0, sigma)
            z = rng.gauss(0, sigma)
            # clip to [-PW, PW]
            y = max(-PW, min(PW, y))
            z = max(-PW, min(PW, z))
            inds.append(len(pos))
            pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_clustered(seed, k=K_NEIGHBORS, n_clusters=4):
    """Cluster centers per layer with Gaussian spread around each."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    for layer in range(1, NL):
        x = layer * H
        centers = [
            (rng.uniform(-PW * 0.7, PW * 0.7), rng.uniform(-PW * 0.7, PW * 0.7))
            for _ in range(n_clusters)
        ]
        inds = []
        for i in range(N_PER_LAYER):
            cy, cz = centers[i % n_clusters]
            y = cy + rng.gauss(0, 0.5)
            z = cz + rng.gauss(0, 0.5)
            y = max(-PW, min(PW, y))
            z = max(-PW, min(PW, z))
            inds.append(len(pos))
            pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_rotated_grid(seed, k=K_NEIGHBORS):
    """Grid positions rotated by a per-layer random angle."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    for layer in range(1, NL):
        x = layer * H
        theta = rng.uniform(0, 2 * math.pi)
        c, s = math.cos(theta), math.sin(theta)
        inds = []
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                y0, z0 = iy * H, iz * H
                y = c * y0 - s * z0
                z = s * y0 + c * z0
                inds.append(len(pos))
                pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_halton(seed, k=K_NEIGHBORS):
    """Halton low-discrepancy quasi-random sequence per layer."""

    def halton(n, base):
        f = 1.0
        r = 0.0
        while n > 0:
            f /= base
            r += f * (n % base)
            n //= base
        return r

    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    rng = random.Random(seed)
    base_y, base_z = 2, 3
    for layer in range(1, NL):
        x = layer * H
        offset = rng.randint(0, 10000)
        inds = []
        for i in range(N_PER_LAYER):
            y = (halton(offset + i + 1, base_y) * 2 - 1) * PW
            z = (halton(offset + i + 1, base_z) * 2 - 1) * PW
            inds.append(len(pos))
            pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_radial(seed, k=K_NEIGHBORS):
    """Polar grid per layer: concentric rings."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    n_rings = 8
    n_per_ring = N_PER_LAYER // n_rings + 1
    for layer in range(1, NL):
        x = layer * H
        theta_offset = rng.uniform(0, 2 * math.pi)
        inds = []
        count = 0
        for ring in range(n_rings):
            r = (ring + 0.5) / n_rings * PW
            for j in range(n_per_ring):
                if count >= N_PER_LAYER:
                    break
                theta = theta_offset + j * 2 * math.pi / n_per_ring
                y = r * math.cos(theta)
                z = r * math.sin(theta)
                inds.append(len(pos))
                pos.append((x, y, z))
                count += 1
        while count < N_PER_LAYER:
            y = rng.uniform(-PW, PW)
            z = rng.uniform(-PW, PW)
            inds.append(len(pos))
            pos.append((x, y, z))
            count += 1
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_stretched(seed, k=K_NEIGHBORS):
    """Per-layer random anisotropic stretching of a uniform sample."""
    rng = random.Random(seed)
    pos = [(0.0, 0.0, 0.0)]
    layer_to_indices = {0: [0]}
    for layer in range(1, NL):
        x = layer * H
        sy = rng.uniform(0.4, 1.8)
        sz = rng.uniform(0.4, 1.8)
        inds = []
        for _ in range(N_PER_LAYER):
            y0 = rng.uniform(-PW, PW)
            z0 = rng.uniform(-PW, PW)
            y = max(-PW, min(PW, y0 * sy))
            z = max(-PW, min(PW, z0 * sz))
            inds.append(len(pos))
            pos.append((x, y, z))
        layer_to_indices[layer] = inds
    return _finalize(pos, layer_to_indices, k)


def grow_uniform_k30(seed):
    return grow_uniform_random(seed, k=30)


def grow_uniform_k8(seed):
    return grow_uniform_random(seed, k=8)


# ========== PRE-COMMITTED PREDICTIONS ==========
# Hard-coded BEFORE running. Audit trail = these dicts.

PREDICTIONS_COH = {
    # coh_high = will free_coh be >= 7.96e-04?
    "OF1_uniform_k15":    False,  # random positions, no spatial structure
    "OF2_uniform_k30":    True,   # dense random, LLN should give some coh
    "OF3_uniform_k8":     False,  # sparse random, phases randomize
    "OF4_gaussian":       False,  # concentrated but still random
    "OF5_clustered":      False,  # clusters break smooth coherence
    "OF6_rotated_grid":   True,   # still a grid, just rotated; structure preserved
    "OF7_halton":         True,   # quasi-random is nearly uniform
    "OF8_radial":         True,   # concentric rings have rotational symmetry
    "OF9_stretched":      False,  # per-layer anisotropy breaks Z2
}

PREDICTIONS_PASS = {
    # my structural intuition for the static battery PASS
    "OF1_uniform_k15":    True,   # k=15 random should approximate ER-like pass
    "OF2_uniform_k30":    True,   # denser → more likely PASS
    "OF3_uniform_k8":     False,  # too sparse, expect F~M to break
    "OF4_gaussian":       True,   # Gaussian shape still OK
    "OF5_clustered":      False,  # clusters break detector uniformity
    "OF6_rotated_grid":   True,   # rotated grid preserves the neighbor stencil spirit
    "OF7_halton":         True,   # quasi-uniform should give PASS
    "OF8_radial":         True,   # rotationally symmetric
    "OF9_stretched":      False,  # per-layer stretching breaks Z2
}


def make_off_scaffold_families():
    return [
        ("OF1_uniform_k15",  lambda: grow_uniform_random(0, 15)),
        ("OF2_uniform_k30",  lambda: grow_uniform_k30(0)),
        ("OF3_uniform_k8",   lambda: grow_uniform_k8(0)),
        ("OF4_gaussian",     lambda: grow_gaussian_random(0)),
        ("OF5_clustered",    lambda: grow_clustered(0)),
        ("OF6_rotated_grid", lambda: grow_rotated_grid(0)),
        ("OF7_halton",       lambda: grow_halton(0)),
        ("OF8_radial",       lambda: grow_radial(0)),
        ("OF9_stretched",    lambda: grow_stretched(0)),
    ]


def free_beam_metrics(pos, adj, nmap):
    """Compute free-beam (no field) detector metrics. Mirrors
    global_coherence_predictor.free_beam_metrics but on off-scaffold pos."""
    free = ind.prop_beam(pos, adj, nmap, None, K)
    npl = N_PER_LAYER
    n = len(pos)
    ds = n - npl
    det = free[ds:n]
    p_det = sum(abs(a) ** 2 for a in det)
    if p_det <= 0:
        return 0.0, 0.0
    sum_amp = sum(det, 0j)
    n_det = len(det)
    sum_abs2 = sum(abs(a) ** 2 for a in det)
    coh = (abs(sum_amp) ** 2) / max(sum_abs2 * n_det, 1e-30)
    return p_det, coh


def main():
    print("=" * 100)
    print("OFF-SCAFFOLD HELD-OUT TEST OF free_coh")
    print(f"Frozen rule: free_coh >= {FREE_COH_THRESHOLD:.4e}")
    print("Generators have random transverse positions (NOT snapped to the (iy,iz) grid)")
    print("Threshold frozen from swept-set fit; applied WITHOUT REFIT")
    print("=" * 100)

    results = []
    for i, (name, builder) in enumerate(make_off_scaffold_families(), 1):
        print(f"\n[{i}/9] {name:22s}", end="", flush=True)
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            p_det, coh = free_beam_metrics(pos, adj, nmap)
            r["free_p_det"] = p_det
            r["free_coh"] = coh
            results.append(r)
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  {tag}  avg_deg={r['avg_deg']:.1f}  "
                  f"free_coh={coh:.4e}  delta={r['delta']:+.4f}  dyn={r['dyn_gap']:.1%}")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"name": name, "pass": False, "error": str(e)})

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"{'family':22s} {'avg_deg':>8s} {'free_coh':>12s} {'p_det':>11s}"
          f" {'delta':>9s} {'dyn':>7s} {'pass':>6s}")
    print("-" * 100)
    for r in results:
        if "error" in r:
            print(f"{r['name']:22s}  ERROR")
            continue
        print(f"{r['name']:22s} {r['avg_deg']:8.2f} {r['free_coh']:12.4e} "
              f"{r['free_p_det']:11.3e} {r['delta']:+9.4f} "
              f"{r['dyn_gap']:7.2%} {('PASS' if r['pass'] else 'FAIL'):>6s}")

    n_pass = sum(1 for r in results if r.get("pass"))
    n_fail = sum(1 for r in results if not r.get("pass") and "error" not in r)
    n_eval = sum(1 for r in results if "error" not in r)
    print(f"\nactual: PASS {n_pass} / FAIL {n_fail}")

    # Level 1: free_coh sign predictions
    print("\nL1. PRE-COMMITTED free_coh SIGN vs measured high/low")
    print(f"{'family':22s} {'predicted':>10s} {'actual':>8s} {'agree':>7s}")
    L1_correct = 0
    for r in results:
        if "error" in r:
            continue
        committed = PREDICTIONS_COH.get(r["name"])
        actual = r["free_coh"] >= FREE_COH_THRESHOLD
        agree = (committed == actual)
        if agree:
            L1_correct += 1
        print(f"{r['name']:22s} {str(committed):>10s} {str(actual):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL1 coh-sign accuracy: {L1_correct}/{n_eval} = {L1_correct/max(n_eval,1):.1%}")

    # Level 2: frozen rule applied without refit
    print("\nL2. FROZEN RULE (free_coh >= 7.96e-04) applied WITHOUT refit")
    print(f"{'family':22s} {'rule':>6s} {'actual':>8s} {'agree':>7s}")
    L2_correct = 0
    for r in results:
        if "error" in r:
            continue
        rule_pred = r["free_coh"] >= FREE_COH_THRESHOLD
        agree = (rule_pred == r["pass"])
        if agree:
            L2_correct += 1
        print(f"{r['name']:22s} {str(rule_pred):>6s} {str(r['pass']):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL2 frozen rule accuracy: {L2_correct}/{n_eval} = {L2_correct/max(n_eval,1):.1%}")

    # Level 3: pre-committed pass/fail predictions
    print("\nL3. PRE-COMMITTED package PASS/FAIL predictions")
    print(f"{'family':22s} {'predicted':>10s} {'actual':>8s} {'agree':>7s}")
    L3_correct = 0
    for r in results:
        if "error" in r:
            continue
        committed = PREDICTIONS_PASS.get(r["name"])
        agree = (committed == r["pass"])
        if agree:
            L3_correct += 1
        print(f"{r['name']:22s} {str(committed):>10s} {str(r['pass']):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL3 pre-committed pass/fail: {L3_correct}/{n_eval} = {L3_correct/max(n_eval,1):.1%}")

    # Comparison vs old node-level rule
    print("\nCOMPARISON to old node-level rule (avg_deg >= 10.42 AND reach_frac >= 0.86)")
    old_correct = sum(
        1 for r in results
        if "error" not in r
        and (r["avg_deg"] >= 10.415 and r["reach_frac"] >= 0.859) == r["pass"]
    )
    print(f"  old 2-prop rule on this batch: {old_correct}/{n_eval} = {old_correct/max(n_eval,1):.1%}")
    print(f"  new free_coh rule on this batch: {L2_correct}/{n_eval} = {L2_correct/max(n_eval,1):.1%}")

    print("\nVERDICT")
    rate_new = L2_correct / max(n_eval, 1)
    rate_old = old_correct / max(n_eval, 1)
    if rate_new >= 0.65:
        print(f"  GENERALIZES — frozen rule at {rate_new:.0%} on off-scaffold batch")
        print("  the last remaining caveat on the classifier lane is cleared")
        if rate_new > rate_old + 0.05:
            print(f"    beats the old node-level rule by {rate_new - rate_old:+.0%}")
    elif rate_new >= 0.50:
        print(f"  PARTIAL — frozen rule at {rate_new:.0%} on off-scaffold batch")
        print("  the scaffold caveat is partially relaxed but not fully cleared")
    else:
        print(f"  FAILS OFF-SCAFFOLD — frozen rule at {rate_new:.0%}")
        print("  the grid scaffold was doing work the classifier attributed to free_coh")
        print("  the classifier program is genuinely closed; next move is matter or analytic")


if __name__ == "__main__":
    main()
