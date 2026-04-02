#!/usr/bin/env python3
"""Direct linearity check: is psi_AB(d) = psi_A(d) + psi_B(d)?

If the path-sum is linear, blocking slit B shouldn't affect slit A's
contribution. So psi_AB(d) = psi_A(d) + psi_B(d) exactly.

If NOT: something about the DAG structure creates coupling between
slit configurations. This would be a genuine discrete-network effect.
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_dag(n_layers=12, nodes_per_layer=25, yz_range=10.0,
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
            layer_nodes.append(0)
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


def propagate(positions, adj, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
    field = [0.0] * n  # no gravity
    for i in order:
        if i in blocked:
            continue
        a_i = amps[i]
        if a_i == 0j:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            act = L  # S = L when field = 0
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += a_i * ea
    return amps


def main():
    print("=" * 70)
    print("LINEARITY CHECK: psi_AB(d) vs psi_A(d) + psi_B(d)")
    print("=" * 70)
    print()

    for seed in range(5):
        positions, adj, layer_indices = generate_3d_dag(
            n_layers=12, nodes_per_layer=25, rng_seed=seed*13+5)

        n_layers = len(layer_indices)
        bl_idx = n_layers // 3
        barrier = layer_indices[bl_idx]
        src = layer_indices[0]
        det_list = layer_indices[-1]

        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)

        slit_a = set(i for i in barrier if positions[i][1] > cy + 3)
        slit_b = set(i for i in barrier if positions[i][1] < cy - 3)
        if not slit_a or not slit_b:
            print(f"  seed {seed}: slits not found, skip")
            continue

        non_slit = set(barrier) - slit_a - slit_b
        k = 5.0

        # Propagate: A only, B only, AB
        blocked_all = non_slit  # always blocked
        amps_a = propagate(positions, adj, src, k, blocked_all | slit_b)
        amps_b = propagate(positions, adj, src, k, blocked_all | slit_a)
        amps_ab = propagate(positions, adj, src, k, blocked_all)

        # Check at each detector
        max_err = 0.0
        max_rel = 0.0
        n_det = 0
        for d in det_list:
            psi_sum = amps_a[d] + amps_b[d]
            psi_ab = amps_ab[d]
            err = abs(psi_ab - psi_sum)
            ref = max(abs(psi_ab), abs(psi_sum))
            rel = err / ref if ref > 0 else 0
            max_err = max(max_err, err)
            if ref > 1e-30:
                max_rel = max(max_rel, rel)
                n_det += 1

        # Also check at barrier nodes (should all be identical)
        barrier_err = 0.0
        for b in slit_a | slit_b:
            e = abs(amps_ab[b] - amps_a[b] - amps_b[b])
            barrier_err = max(barrier_err, e)

        # And at the first post-barrier layer
        post_barrier = layer_indices[bl_idx + 1]
        post_err = 0.0
        for p in post_barrier:
            e = abs(amps_ab[p] - amps_a[p] - amps_b[p])
            post_err = max(post_err, e)

        # Check source layer amplitude (should be identical across configs)
        src_err = 0.0
        for s in src:
            e = abs(amps_ab[s] - amps_a[s])
            src_err = max(src_err, e)

        print(f"  seed {seed}: slits A={len(slit_a)}, B={len(slit_b)}, non={len(non_slit)}")
        print(f"    source amp diff:       {src_err:.6e}")
        print(f"    barrier amp diff:      {barrier_err:.6e}")
        print(f"    post-barrier amp diff: {post_err:.6e}")
        print(f"    detector max |err|:    {max_err:.6e}")
        print(f"    detector max rel err:  {max_rel:.6e} ({n_det} det with signal)")

        # Check: do slit nodes receive different amplitude across configs?
        print(f"    slit A amps check:")
        for a in sorted(slit_a)[:3]:
            print(f"      node {a}: AB={amps_ab[a]:.6e}, A={amps_a[a]:.6e}, diff={abs(amps_ab[a]-amps_a[a]):.6e}")

        print()

    print("If max rel err ~ 1e-15: perfect linearity (Born rule holds)")
    print("If max rel err ~ 0.1+: linearity broken — investigate cause")


if __name__ == "__main__":
    main()
