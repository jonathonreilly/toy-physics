#!/usr/bin/env python3
"""Debug 3D Born rule: isolate what causes I_3 != 0.

Tests:
  1. Fixed DAG, no field (field=0) → should give I_3 ~ machine epsilon
  2. Fixed DAG, with field → does gravity field break Born rule?
  3. Different slit separations
  4. Multiple seeds to check consistency

In 2D, the fixed-DAG test gave I_3/P = 4.73e-16 (machine epsilon).
The 3D joint test gave I_3/P ~ 0.5-1.4 even with "fixed" DAG.

PStack experiment: three-d-born-rule-debug
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
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, yz_range)
                    else:
                        y = rng.uniform(-yz_range, -gap / 2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def compute_field_3d(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
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


def propagate_3d(positions, adj, field, src, k, blocked=None):
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
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
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


def sorkin_fixed_dag(positions, adj, field, layer_indices, k):
    """Fixed-DAG Sorkin test: block closed slits but keep graph structure."""
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
        amps = propagate_3d(positions, adj, field, src, k, blocked)
        return sum(abs(amps[d])**2 for d in det_list)

    P_ABC = prob(slit_a | slit_b | slit_c)
    P_AB = prob(slit_a | slit_b)
    P_AC = prob(slit_a | slit_c)
    P_BC = prob(slit_b | slit_c)
    P_A = prob(slit_a)
    P_B = prob(slit_b)
    P_C = prob(slit_c)

    I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

    return {
        "I_3": I_3, "P_ABC": P_ABC,
        "P_AB": P_AB, "P_AC": P_AC, "P_BC": P_BC,
        "P_A": P_A, "P_B": P_B, "P_C": P_C,
        "n_slit_a": len(slit_a), "n_slit_b": len(slit_b), "n_slit_c": len(slit_c),
    }


def main():
    print("=" * 70)
    print("3D BORN RULE DEBUG: Isolating I_3 != 0 cause")
    print("=" * 70)
    print()

    # Test 1: No field, uniform DAG
    print("TEST 1: No field (field=0), uniform DAG (gap=0)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>12s}  {'P_ABC':>12s}  {'|I_3|/P':>12s}")
    print(f"  {'-'*52}")

    for seed in range(4):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=15, nodes_per_layer=30, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed * 13 + 5, gap=0.0,
        )
        field = [0.0] * len(positions)

        for k in [3.0, 5.0]:
            result = sorkin_fixed_dag(positions, adj, field, layer_indices, k)
            if result:
                r = abs(result["I_3"]) / result["P_ABC"] if result["P_ABC"] > 0 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {result['I_3']:+12.6e}  "
                      f"{result['P_ABC']:12.6e}  {r:12.6e}")

    print()

    # Test 2: No field, modular DAG
    print("TEST 2: No field (field=0), modular DAG (gap=3)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>12s}  {'P_ABC':>12s}  {'|I_3|/P':>12s}")
    print(f"  {'-'*52}")

    for seed in range(4):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=15, nodes_per_layer=30, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed * 13 + 5, gap=3.0,
        )
        field = [0.0] * len(positions)

        for k in [3.0, 5.0]:
            result = sorkin_fixed_dag(positions, adj, field, layer_indices, k)
            if result:
                r = abs(result["I_3"]) / result["P_ABC"] if result["P_ABC"] > 0 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {result['I_3']:+12.6e}  "
                      f"{result['P_ABC']:12.6e}  {r:12.6e}")
                if r > 0.01:
                    print(f"         slits: A={result['n_slit_a']}, B={result['n_slit_b']}, C={result['n_slit_c']}")
                    print(f"         P_AB={result['P_AB']:.6e}, P_AC={result['P_AC']:.6e}, P_BC={result['P_BC']:.6e}")
                    print(f"         P_A={result['P_A']:.6e}, P_B={result['P_B']:.6e}, P_C={result['P_C']:.6e}")

    print()

    # Test 3: With field, modular DAG
    print("TEST 3: With gravity field, modular DAG (gap=3)")
    print(f"  {'seed':>4s}  {'k':>4s}  {'I_3':>12s}  {'P_ABC':>12s}  {'|I_3|/P':>12s}")
    print(f"  {'-'*52}")

    for seed in range(4):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=15, nodes_per_layer=30, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed * 13 + 5, gap=3.0,
        )
        n = len(layer_indices)
        grav_idx = 2 * n // 3
        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)
        grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1]
        field = compute_field_3d(positions, adj, grav_mass) if grav_mass else [0.0] * len(positions)

        for k in [3.0, 5.0]:
            result = sorkin_fixed_dag(positions, adj, field, layer_indices, k)
            if result:
                r = abs(result["I_3"]) / result["P_ABC"] if result["P_ABC"] > 0 else math.nan
                print(f"  {seed:4d}  {k:4.1f}  {result['I_3']:+12.6e}  "
                      f"{result['P_ABC']:12.6e}  {r:12.6e}")

    print()

    # Test 4: Flat field, k=0 (trivial test)
    print("TEST 4: k=0 sanity (should be exact)")
    positions, adj, layer_indices = generate_3d_modular_dag(
        n_layers=15, nodes_per_layer=30, yz_range=10.0,
        connect_radius=3.5, rng_seed=42, gap=0.0,
    )
    field = [0.0] * len(positions)
    result = sorkin_fixed_dag(positions, adj, field, layer_indices, k=0.0)
    if result:
        r = abs(result["I_3"]) / result["P_ABC"] if result["P_ABC"] > 0 else math.nan
        print(f"  k=0: I_3={result['I_3']:+.6e}, P={result['P_ABC']:.6e}, |I_3|/P={r:.6e}")
    print()

    print("INTERPRETATION:")
    print("  |I_3|/P ~ 1e-15: Born rule holds (machine epsilon)")
    print("  |I_3|/P ~ 1e-6:  Numerical noise")
    print("  |I_3|/P ~ 0.1+:  Real effect — investigate cause")


if __name__ == "__main__":
    main()
