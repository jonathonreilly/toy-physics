#!/usr/bin/env python3
"""Retarded (causal) field propagation: does it restore 1/b distance scaling?

RETRACTED: The b-sweep uses a moving y-window to select mass nodes,
so source count/geometry change with b. Fixed-mass verification on main
(causal_field_fixed_mass_verify.py) shows NO distance falloff once
occupancy is controlled. The ~1/b claim from this script was an artifact.
The positive-only power law fit further inflated the apparent trend.

The derivation identified the Laplacian field as the b-independence engine:
it spreads f everywhere on the graph, making all paths feel roughly equal
phase perturbation regardless of mass position.

A CAUSAL (retarded) field propagates only forward along the DAG:
  f(j) = max(f sources) or sum, decaying with distance
  Field at node j only depends on upstream nodes (x_j > x_source)
  No backward propagation — field stays localized near/downstream of mass

This keeps f large near the mass and small far away (transversely),
which SHOULD produce b-dependent gravity if the derivation is correct.

Three causal field variants:
  1. Forward diffusion: f propagates forward, decaying per edge
  2. Forward Green's: f(j) = sum_mass 1/r(j,m) but only if j downstream
  3. Causal cone: f nonzero only within the forward light cone of mass

PStack experiment: causal-field-gravity
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


def field_laplacian(positions, adj, mass_ids, iterations=50):
    """Standard bidirectional Laplacian relaxation (baseline)."""
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def field_causal_diffusion(positions, adj, mass_ids, decay=0.7):
    """Forward-only field diffusion along the DAG.

    Field propagates from mass nodes FORWARD (increasing x) only.
    At each edge, f decays by factor `decay`.
    f(j) = max over parents of (decay * f(parent)) if not a mass source.
    """
    n = len(positions)
    # Topological order
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

    ms = set(mass_ids)
    field = [0.0] * n
    for m in ms:
        field[m] = 1.0

    for i in order:
        if field[i] <= 0:
            continue
        for j in adj.get(i, []):
            propagated = decay * field[i]
            # Use max (strongest field wins) or sum
            field[j] = max(field[j], propagated)

    return field


def field_causal_sum(positions, adj, mass_ids, decay=0.8):
    """Forward-only field with additive propagation.

    Each edge contributes decay * f(parent) to child.
    Sum over all parents — more paths from mass = stronger field.
    """
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

    ms = set(mass_ids)
    field = [0.0] * n
    for m in ms:
        field[m] = 1.0

    for i in order:
        if field[i] <= 0:
            continue
        for j in adj.get(i, []):
            field[j] += decay * field[i] / max(1, len(adj.get(i, [])))

    # Normalize to [0, 1]
    mx = max(field) if max(field) > 0 else 1
    return [f / mx for f in field]


def field_causal_1r(positions, mass_ids):
    """1/r field from mass, but only at nodes DOWNSTREAM (x > x_mass).

    Upstream and same-layer nodes get f=0.
    """
    n = len(positions)
    field = [0.0] * n
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            if ix <= mx:  # Only downstream
                continue
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2)
            field[i] += 0.3 / (r + 0.1)
    return field


def propagate(positions, adj, field, src, k):
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
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def measure_b(field_fn, label, n_seeds=16):
    k_band = [3.0, 5.0, 7.0]
    b_targets = [1, 2, 3, 4, 6, 8, 10]

    print(f"  [{label}]")
    print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'shift*b':>8s}  scaling")
    print(f"  {'-'*42}")

    results = []
    for b in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_dag(
                n_layers=18, nodes_per_layer=40, yz_range=12.0,
                connect_radius=3.5, rng_seed=seed*17+3)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass_ids = [i for i in layer_indices[mid]
                        if abs(positions[i][1] - (cy + b)) < 2.0]
            if len(mass_ids) < 2:
                continue

            field = field_fn(positions, adj, mass_ids)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) -
                              centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts) / len(shifts))

        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            se = math.sqrt(sum((s-avg)**2 for s in per_seed) / len(per_seed)) / math.sqrt(len(per_seed))
            results.append((b, avg, se))
            print(f"  {b:5d}  {avg:+8.4f}  {se:6.4f}  {avg*b:+8.3f}")

    # Assess scaling
    pos = [(b, s) for b, s, _ in results if s > 0.01]
    if len(pos) >= 3:
        products = [s*b for b, s in pos]
        shifts = [s for _, s in pos]
        mean_p = sum(products) / len(products)
        cv_1b = (max(products) - min(products)) / abs(mean_p) if abs(mean_p) > 0 else 999
        mean_s = sum(shifts) / len(shifts)
        cv_flat = (max(shifts) - min(shifts)) / abs(mean_s) if abs(mean_s) > 0 else 999

        if cv_1b < 0.4 and cv_1b < cv_flat:
            print(f"  → shift*b ≈ const (CV={cv_1b:.2f}): 1/b SCALING!")
        elif cv_flat < 0.5:
            print(f"  → shift ≈ const (CV={cv_flat:.2f}): b-independent")
        else:
            # Check if shift decreases with b
            if len(pos) >= 4 and pos[-1][1] < pos[0][1] * 0.5:
                print(f"  → shift DECREASES with b (decaying, not 1/b)")
            else:
                print(f"  → noisy (CV flat={cv_flat:.2f}, CV 1/b={cv_1b:.2f})")
    elif results:
        print(f"  → weak signal (few positive shifts)")
    print()


def main():
    print("=" * 70)
    print("CAUSAL FIELD GRAVITY: does retarded propagation restore 1/b?")
    print("=" * 70)
    print()

    # Wrapper to match (positions, adj, mass_ids) signature
    def laplacian_fn(pos, adj, m):
        return field_laplacian(pos, adj, m)

    def causal_diff_fn(pos, adj, m):
        return field_causal_diffusion(pos, adj, m, decay=0.7)

    def causal_sum_fn(pos, adj, m):
        return field_causal_sum(pos, adj, m, decay=0.8)

    def causal_1r_fn(pos, adj, m):
        return field_causal_1r(pos, m)

    families = [
        (laplacian_fn, "Laplacian (baseline — bidirectional)"),
        (causal_diff_fn, "Causal diffusion (forward max, decay=0.7)"),
        (causal_sum_fn, "Causal sum (forward additive, decay=0.8)"),
        (causal_1r_fn, "Causal 1/r (downstream only)"),
    ]

    for fn, label in families:
        measure_b(fn, label, n_seeds=16)

    print("=" * 70)
    print("INTERPRETATION:")
    print("  Laplacian: field spreads everywhere → b-independent (known)")
    print("  Causal: field stays near/downstream → b-dependent?")
    print()
    print("  If causal gives 1/b: the FIELD PROPAGATION is the key")
    print("  If causal gives flat: b-independence survives even without")
    print("    global field spreading")
    print("=" * 70)


if __name__ == "__main__":
    main()
