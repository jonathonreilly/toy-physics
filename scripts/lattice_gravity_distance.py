#!/usr/bin/env python3
"""Gravity distance scaling on a regular 3D lattice.

Hypothesis: b-independence on random DAGs comes from paths sampling
the full transverse extent. On a regular lattice, paths are
geometrically constrained — a path from (0,0,0) to (N,y,z) stays
near (y,z) and only feels the phase valley if it passes near the mass.

This should give b-dependent deflection if the hypothesis is correct.

Setup: 3D rectangular lattice. Nodes at integer (x,y,z) coordinates.
Edges connect forward neighbors (dx=1, |dy|<=1, |dz|<=1).
Corrected propagator: exp(i*k*S) / L, directional measure.

PStack experiment: lattice-gravity-distance
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque

BETA = 0.8


def build_3d_lattice(nx=20, ny=15, nz=15):
    """Build a regular 3D lattice DAG.

    Nodes at integer coordinates (x, y, z) where:
      x in [0, nx-1], y in [-ny, ny], z in [-nz, nz]
    Edges: forward only (dx=1), with transverse reach |dy|<=1, |dz|<=1.
    """
    positions = {}  # node_id → (x, y, z)
    adj = defaultdict(list)
    node_id = {}  # (x,y,z) → id

    idx = 0
    for x in range(nx):
        for y in range(-ny, ny + 1):
            for z in range(-nz, nz + 1):
                positions[idx] = (float(x), float(y), float(z))
                node_id[(x, y, z)] = idx
                idx += 1

    n = idx

    # Forward edges: dx=1, |dy|<=1, |dz|<=1
    for x in range(nx - 1):
        for y in range(-ny, ny + 1):
            for z in range(-nz, nz + 1):
                src_id = node_id[(x, y, z)]
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        ny2, nz2 = y + dy, z + dz
                        if -ny <= ny2 <= ny and -nz <= nz2 <= nz:
                            dst_id = node_id[(x + 1, ny2, nz2)]
                            adj[src_id].append(dst_id)

    # Layer indices
    layer_indices = []
    for x in range(nx):
        layer = [node_id[(x, y, z)] for y in range(-ny, ny+1) for z in range(-nz, nz+1)]
        layer_indices.append(layer)

    return positions, dict(adj), layer_indices, node_id, n


def compute_field_lattice(positions, n, adj, mass_ids, iterations=80):
    """Laplacian-relaxed field on the lattice."""
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
    field = {i: (1.0 if i in ms else 0.0) for i in range(n)}
    for _ in range(iterations):
        nf = {}
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
            else:
                nf[i] = 0.0
        field = nf
    return field


def propagate_lattice(positions, adj, field, src_ids, k, n):
    """Corrected propagator on lattice."""
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
    for s in src_ids:
        amps[s] = 1.0 / len(src_ids)

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            pi = positions[i]
            pj = positions[j]
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dz = pj[2] - pi[2]
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


def centroid_y(amps, positions, det_ids):
    total = wy = 0.0
    for d in det_ids:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def main():
    # Use smaller lattice for speed (still ~30k nodes)
    nx, ny, nz = 20, 10, 5
    print("=" * 70)
    print(f"LATTICE GRAVITY: {nx}x{2*ny+1}x{2*nz+1} regular grid")
    print("  Corrected propagator, directional measure")
    print("  Does the lattice give b-dependent deflection?")
    print("=" * 70)
    print()

    positions, adj, layer_indices, node_id, n = build_3d_lattice(nx, ny, nz)
    print(f"  Nodes: {n}, Edges: {sum(len(v) for v in adj.values())}")
    print()

    # Source: all nodes at x=0
    src_ids = layer_indices[0]
    # Detectors: all nodes at x=nx-1
    det_ids = layer_indices[-1]

    k_band = [2.0, 4.0, 6.0]

    # k=0 sanity
    print("SANITY: k=0 → zero deflection")
    field_zero = {i: 0.0 for i in range(n)}
    mass_y = 5
    mass_ids = [node_id[(nx//2, mass_y, z)] for z in range(-nz, nz+1)
                if (nx//2, mass_y, z) in node_id]
    field_m = compute_field_lattice(positions, n, adj, mass_ids)

    a0_m = propagate_lattice(positions, adj, field_m, src_ids, 0.0, n)
    a0_f = propagate_lattice(positions, adj, field_zero, src_ids, 0.0, n)
    d0 = centroid_y(a0_m, positions, det_ids) - centroid_y(a0_f, positions, det_ids)
    print(f"  k=0: delta = {d0:+.6e}")
    print()

    # Test 1: Basic attraction
    print("TEST 1: Attraction (mass at y=5)")
    print(f"  {'k':>4s}  {'shift':>8s}  direction")
    print(f"  {'-'*24}")
    for k in k_band:
        am = propagate_lattice(positions, adj, field_m, src_ids, k, n)
        af = propagate_lattice(positions, adj, field_zero, src_ids, k, n)
        shift = centroid_y(am, positions, det_ids) - centroid_y(af, positions, det_ids)
        d = "ATTRACT" if shift > 0.01 else "REPEL" if shift < -0.01 else "FLAT"
        print(f"  {k:4.1f}  {shift:+8.4f}  {d}")
    print()

    # Test 2: Distance scaling — THE KEY TEST
    print("TEST 2: Distance scaling (shift vs mass position b)")
    print(f"  Mass: 1 row of nodes at (nx//2, b, z) for all z")
    print()

    for k in k_band:
        print(f"  k={k:.1f}:")
        print(f"  {'b':>5s}  {'shift':>8s}  {'shift*b':>8s}  {'shift*b²':>9s}")
        print(f"  {'-'*36}")

        shifts_for_k = []
        for b in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if b > ny:
                continue
            m_ids = [node_id[(nx//2, b, z)] for z in range(-nz, nz+1)
                     if (nx//2, b, z) in node_id]
            if not m_ids:
                continue
            field_b = compute_field_lattice(positions, n, adj, m_ids)
            am = propagate_lattice(positions, adj, field_b, src_ids, k, n)
            af = propagate_lattice(positions, adj, field_zero, src_ids, k, n)
            shift = centroid_y(am, positions, det_ids) - centroid_y(af, positions, det_ids)
            shifts_for_k.append((b, shift))
            print(f"  {b:5d}  {shift:+8.4f}  {shift*b:+8.3f}  {shift*b*b:+9.2f}")

        # Check scaling
        pos = [(b, s) for b, s in shifts_for_k if s > 0]
        if len(pos) >= 3:
            products = [s*b for b, s in pos]
            mean_p = sum(products) / len(products)
            cv_1b = (max(products) - min(products)) / abs(mean_p) if abs(mean_p) > 0 else 999
            shifts_only = [s for _, s in pos]
            mean_s = sum(shifts_only) / len(shifts_only)
            cv_flat = (max(shifts_only) - min(shifts_only)) / abs(mean_s) if abs(mean_s) > 0 else 999
            print(f"  → CV(shift): {cv_flat:.2f}, CV(shift*b): {cv_1b:.2f}")
            if cv_1b < cv_flat and cv_1b < 0.5:
                print(f"  ★ 1/b SCALING DETECTED on lattice!")
            elif cv_flat < 0.4:
                print(f"  → b-independent (flat)")
            else:
                print(f"  → noisy, no clear pattern")
        print()

    print("=" * 70)
    print("INTERPRETATION:")
    print("  If lattice gives 1/b: geometric locality constrains paths")
    print("  If lattice gives flat: b-independence is TRULY fundamental")
    print("=" * 70)


if __name__ == "__main__":
    main()
