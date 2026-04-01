#!/usr/bin/env python3
"""Field localization test: is b-independence caused by the Laplacian field?

The Laplacian-relaxed field f permeates the entire graph — f is never
exactly zero. So all paths experience phase perturbation, regardless
of distance from the mass.

Hypothesis: if we use a SHARPLY localized field (f=1 only at mass
nodes, f=0 elsewhere), paths far from the mass won't feel it,
and b-dependent deflection should appear.

Test:
  1. Sharp field: f(i) = 1 if i is mass node, 0 otherwise
  2. Local field: f(i) = strength / r(i, mass) with hard cutoff at r=R
  3. Laplacian field: standard relaxation (baseline)

If sharp field gives 1/b: the Laplacian spreading is what kills b-dependence.
If sharp field is also flat: b-independence is in the path-sum itself.

PStack experiment: field-localization-test
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
    """Standard Laplacian-relaxed field."""
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


def field_sharp(positions, mass_ids, strength=0.3):
    """Sharp field: nonzero ONLY at mass nodes."""
    n = len(positions)
    ms = set(mass_ids)
    return [strength if i in ms else 0.0 for i in range(n)]


def field_local(positions, mass_ids, cutoff=3.0, strength=0.1):
    """Locally decaying field with hard cutoff."""
    n = len(positions)
    field = [0.0] * n
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2)
            if r < cutoff:
                field[i] += strength / (r + 0.1)
    return field


def field_local_soft(positions, mass_ids, sigma=2.0, strength=0.3):
    """Gaussian-decaying field."""
    n = len(positions)
    field = [0.0] * n
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r2 = (ix-mx)**2 + (iy-my)**2 + (iz-mz)**2
            field[i] += strength * math.exp(-r2 / (2*sigma*sigma))
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


def measure_b_scaling(field_fn, label, n_seeds=16):
    """Measure shift vs b for a given field function."""
    k_band = [3.0, 5.0, 7.0]
    b_targets = [1, 2, 3, 4, 6, 8, 10]

    print(f"  [{label}]")
    print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'shift/b':>8s}")
    print(f"  {'-'*32}")

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
            sb = avg / b if b > 0 else 0
            print(f"  {b:5d}  {avg:+8.4f}  {se:6.4f}  {sb:+8.4f}")

    print()


def main():
    print("=" * 70)
    print("FIELD LOCALIZATION TEST")
    print("  Is b-independence caused by the Laplacian field spreading?")
    print("=" * 70)
    print()

    # Wrapper functions that match the (positions, adj, mass_ids) signature
    def laplacian_fn(positions, adj, mass_ids):
        return field_laplacian(positions, adj, mass_ids)

    def sharp_fn(positions, adj, mass_ids):
        return field_sharp(positions, mass_ids, strength=0.3)

    def local_r3_fn(positions, adj, mass_ids):
        return field_local(positions, mass_ids, cutoff=3.0, strength=0.1)

    def local_r6_fn(positions, adj, mass_ids):
        return field_local(positions, mass_ids, cutoff=6.0, strength=0.1)

    def gaussian_s2_fn(positions, adj, mass_ids):
        return field_local_soft(positions, mass_ids, sigma=2.0, strength=0.3)

    def gaussian_s1_fn(positions, adj, mass_ids):
        return field_local_soft(positions, mass_ids, sigma=1.0, strength=0.3)

    families = [
        (laplacian_fn, "Laplacian-relaxed (baseline)"),
        (sharp_fn, "Sharp (f=0.3 at mass, 0 elsewhere)"),
        (local_r3_fn, "Local 1/r, cutoff=3"),
        (local_r6_fn, "Local 1/r, cutoff=6"),
        (gaussian_s2_fn, "Gaussian sigma=2"),
        (gaussian_s1_fn, "Gaussian sigma=1"),
    ]

    for fn, label in families:
        measure_b_scaling(fn, label, n_seeds=16)

    print("=" * 70)
    print("INTERPRETATION:")
    print("  If sharp/local field gives shift/b ~ 1/b: Laplacian spreading")
    print("    was causing b-independence. Localized field fixes it.")
    print("  If all fields give flat shift/b: b-independence is in the")
    print("    path-sum mechanism itself, not the field shape.")
    print("=" * 70)


if __name__ == "__main__":
    main()
