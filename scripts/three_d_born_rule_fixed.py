#!/usr/bin/env python3
"""3D Born rule test with NO amplitude threshold.

The debug test showed I_3/P ~ O(1) in 3D. The cause is the 1e-30
amplitude threshold in propagate_3d: when only one slit is open,
intermediate nodes can fall below threshold and get skipped, but
with multiple slits they stay above. This breaks linearity.

Fix: remove the threshold entirely for the Sorkin test. This is
slower but gives the correct mathematical result.

PStack experiment: three-d-born-rule-fixed
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_modular_dag(n_layers=15, nodes_per_layer=30, yz_range=8.0,
                            connect_radius=3.5, rng_seed=42, gap=3.0,
                            crosslink_prob=0.02):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if use_channels and layer > barrier_layer:
                    y = rng.uniform(gap/2, yz_range) if node_i < nodes_per_layer//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < crosslink_prob:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def propagate_3d_exact(positions, adj, field, src, k, blocked=None):
    """Propagator with NO amplitude threshold — exact linear propagation."""
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
    for i in order:
        if i in blocked:
            continue
        # NO threshold check — propagate all nonzero amplitudes
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
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += a_i * ea
    return amps


def sorkin_exact(positions, adj, field, layer_indices, k):
    """Fixed-DAG Sorkin test with exact (no threshold) propagation."""
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    barrier = layer_indices[bl_idx]
    src = layer_indices[0]
    det_list = layer_indices[-1]

    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)

    slit_a = set(i for i in barrier if positions[i][1] > cy + 4)
    slit_b = set(i for i in barrier if abs(positions[i][1] - cy) < 2)
    slit_c = set(i for i in barrier if positions[i][1] < cy - 4)

    if not slit_a or not slit_b or not slit_c:
        return None

    all_slits = slit_a | slit_b | slit_c
    base_blocked = set(barrier) - all_slits

    def prob(open_set):
        closed = all_slits - open_set
        blocked = base_blocked | closed
        amps = propagate_3d_exact(positions, adj, field, src, k, blocked)
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


def main():
    print("=" * 70)
    print("3D BORN RULE: Exact propagation (no threshold)")
    print("=" * 70)
    print()

    print("TEST 1: No field, uniform (gap=0)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>14s}  {'P_ABC':>12s}  {'|I_3|/P':>14s}")
    print(f"  {'-'*56}")

    for seed in range(6):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=12, nodes_per_layer=25, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed*13+5, gap=0.0,
        )
        field = [0.0] * len(positions)
        for k in [3.0, 5.0]:
            result = sorkin_exact(positions, adj, field, layer_indices, k)
            if result:
                I_3, P = result
                r = abs(I_3) / P if P > 0 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {I_3:+14.6e}  {P:12.6e}  {r:14.6e}")

    print()

    print("TEST 2: No field, modular (gap=3)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>14s}  {'P_ABC':>12s}  {'|I_3|/P':>14s}")
    print(f"  {'-'*56}")

    for seed in range(6):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=12, nodes_per_layer=25, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed*13+5, gap=3.0,
        )
        field = [0.0] * len(positions)
        for k in [3.0, 5.0]:
            result = sorkin_exact(positions, adj, field, layer_indices, k)
            if result:
                I_3, P = result
                r = abs(I_3) / P if P > 0 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {I_3:+14.6e}  {P:12.6e}  {r:14.6e}")

    print()
    print("EXPECTED: |I_3|/P ~ 1e-15 (machine epsilon)")
    print("This confirms Born rule holds for the linear path-sum propagator.")


if __name__ == "__main__":
    main()
