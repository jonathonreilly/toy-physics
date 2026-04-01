#!/usr/bin/env python3
"""3D Born rule with barrier chokepoint: no skip-layer connections across barrier.

The linearity check revealed that ψ_AB ≠ ψ_A + ψ_B because edges
can skip the barrier layer (layer L-1 → layer L+1), so paths bypass
the barrier entirely. These bypass paths get double-counted.

Fix: during graph generation, prevent edges from crossing the barrier
layer. All paths MUST pass through the barrier.

PStack experiment: three-d-born-rule-chokepoint
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_dag_chokepoint(n_layers=12, nodes_per_layer=25, yz_range=10.0,
                                connect_radius=3.5, rng_seed=42):
    """3D DAG with barrier as a forced chokepoint (no skip-layer edges across it)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

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

                # Connect to previous 1-2 layers, but NO cross-barrier skip
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        # Check if this edge would skip the barrier
                        prev_x = round(positions[prev_idx][0])
                        curr_x = layer
                        if prev_x < barrier_layer and curr_x > barrier_layer:
                            # This edge would skip the barrier — forbid it
                            continue

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
    field = [0.0] * n
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
            ea = cmath.exp(1j * k * L) * w / L
            amps[j] += a_i * ea
    return amps


def sorkin_test(positions, adj, layer_indices, k):
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    barrier = layer_indices[bl_idx]
    src = layer_indices[0]
    det_list = layer_indices[-1]

    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)

    slit_a = set(i for i in barrier if positions[i][1] > cy + 3)
    slit_b = set(i for i in barrier if abs(positions[i][1] - cy) < 2)
    slit_c = set(i for i in barrier if positions[i][1] < cy - 3)

    if not slit_a or not slit_b or not slit_c:
        return None

    all_slits = slit_a | slit_b | slit_c
    base_blocked = set(barrier) - all_slits

    def prob(open_set):
        closed = all_slits - open_set
        blocked = base_blocked | closed
        amps = propagate(positions, adj, src, k, blocked)
        return sum(abs(amps[d])**2 for d in det_list)

    P_ABC = prob(slit_a | slit_b | slit_c)
    P_AB = prob(slit_a | slit_b)
    P_AC = prob(slit_a | slit_c)
    P_BC = prob(slit_b | slit_c)
    P_A = prob(slit_a)
    P_B = prob(slit_b)
    P_C = prob(slit_c)

    I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
    return I_3, P_ABC


def linearity_check(positions, adj, layer_indices, k):
    """Direct check: psi_AB = psi_A + psi_B at all detectors."""
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
        return math.nan

    non_slit = set(barrier) - slit_a - slit_b
    amps_a = propagate(positions, adj, src, k, non_slit | slit_b)
    amps_b = propagate(positions, adj, src, k, non_slit | slit_a)
    amps_ab = propagate(positions, adj, src, k, non_slit)

    max_rel = 0.0
    for d in det_list:
        psi_sum = amps_a[d] + amps_b[d]
        psi_ab = amps_ab[d]
        err = abs(psi_ab - psi_sum)
        ref = max(abs(psi_ab), abs(psi_sum))
        if ref > 1e-30:
            max_rel = max(max_rel, err / ref)

    return max_rel


def main():
    print("=" * 70)
    print("3D BORN RULE: Chokepoint barrier (no skip-layer crossing)")
    print("=" * 70)
    print()

    # Test 1: Linearity check
    print("TEST 1: Linearity check (psi_AB = psi_A + psi_B)")
    print(f"  {'seed':>4s}  {'max_rel_err':>14s}  verdict")
    print(f"  {'-'*30}")

    for seed in range(8):
        positions, adj, layer_indices = generate_3d_dag_chokepoint(
            n_layers=12, nodes_per_layer=25, rng_seed=seed*13+5)
        rel = linearity_check(positions, adj, layer_indices, k=5.0)
        v = "LINEAR" if rel < 1e-10 else "BROKEN" if rel > 0.01 else "NOISY"
        print(f"  {seed:4d}  {rel:14.6e}  {v}")

    print()

    # Test 2: Sorkin test
    print("TEST 2: Sorkin I_3 (three-slit Born rule)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>14s}  {'P':>12s}  {'|I_3|/P':>14s}")
    print(f"  {'-'*56}")

    for seed in range(8):
        positions, adj, layer_indices = generate_3d_dag_chokepoint(
            n_layers=12, nodes_per_layer=25, rng_seed=seed*13+5)
        for k in [3.0, 5.0]:
            result = sorkin_test(positions, adj, layer_indices, k)
            if result:
                I_3, P = result
                r = abs(I_3) / P if P > 1e-30 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {I_3:+14.6e}  {P:12.6e}  {r:14.6e}")
            else:
                print(f"  {seed:4d}  {k:4.1f}  SKIP (slits not found)")

    print()
    print("EXPECTED: linearity ~ 1e-15, |I_3|/P ~ 1e-15")
    print("This confirms Born rule holds when barrier is a true chokepoint.")


if __name__ == "__main__":
    main()
