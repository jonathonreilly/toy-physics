#!/usr/bin/env python3
"""Caldeira-Leggett bath decoherence on 3D causal DAGs.

The 2D model achieves pur_min ~ 0.93 at N=25-40 but hits a CLT ceiling
at large N (pur_min → 1 as N → infinity). The fundamental issue: on
sufficiently connected 2D graphs, per-slit amplitude distributions
converge to the same Gaussian, making the bath contrast S → 0.

In 3D, paths have more spatial diversity (y AND z dimensions). The
question: does the extra dimension help maintain slit separation at
larger N, delaying or eliminating the CLT ceiling?

Tests:
  1. CL bath contrast S vs N (does S stay bounded in 3D?)
  2. Purity vs N scaling (does the ceiling shift or disappear?)
  3. Comparison: 3D uniform vs 3D modular

PStack experiment: three-d-decoherence
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8  # bins along y-axis for CL bath contrast


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
            # Source at origin
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


def propagate_3d(positions, adj, field, src, k, blocked=None):
    """Corrected propagator on 3D graph with directional measure."""
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


def cl_bath_contrast_3d(amps_a, amps_b, mid_nodes, positions, n_bins=N_YBINS):
    """Compute CL bath contrast S using y-bins.

    S = sum_bins |psi_A(y_b) - psi_B(y_b)|^2
    """
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0, 0.0
    y_min = min(ys) - 0.01
    y_max = max(ys) + 0.01
    bin_width = (y_max - y_min) / n_bins

    bins_a = [0j] * n_bins
    bins_b = [0j] * n_bins
    for m in mid_nodes:
        y = positions[m][1]
        b = int((y - y_min) / bin_width)
        b = max(0, min(n_bins - 1, b))
        bins_a[b] += amps_a[m]
        bins_b[b] += amps_b[m]

    S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    N_A = sum(abs(a) ** 2 for a in bins_a)
    N_B = sum(abs(b) ** 2 for b in bins_b)
    denom = N_A + N_B
    S_norm = S / denom if denom > 0 else 0.0
    return S, S_norm


def cl_purity(amps_a, amps_b, D, det_list):
    """Purity under CL bath decoherence factor D."""
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab = amps_a[d1] * amps_b[d2].conjugate()
            ba = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + D * ab + D * ba

    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def setup_slit_experiment_3d(positions, adj, layer_indices, slit_sep=3.0):
    """Set up double-slit geometry on a 3D DAG.

    Barrier at layer n//3. Two slits: y > +slit_sep and y < -slit_sep.
    Mass nodes in post-barrier region near y=0 (between slits).
    """
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3

    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list:
        return None

    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)

    # Barrier: block all nodes except slit openings
    barrier_nodes = layer_indices[bl_idx]
    slit_a = [i for i in barrier_nodes if positions[i][1] > cy + slit_sep][:5]
    slit_b = [i for i in barrier_nodes if positions[i][1] < cy - slit_sep][:5]
    if not slit_a or not slit_b:
        return None

    slit_set = set(slit_a + slit_b)
    blocked = set(barrier_nodes) - slit_set

    # Mass nodes: post-barrier, near center (between slits)
    mass_nodes = []
    for li in range(bl_idx + 1, min(n_layers, bl_idx + 3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= slit_sep:
                mass_nodes.append(i)

    # Gravity mass further along
    grav_idx = 2 * n_layers // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1]

    all_mass = set(mass_nodes) | set(grav_mass)
    field = compute_field_3d(positions, adj, list(all_mass)) if all_mass else [0.0] * len(positions)

    # Mid-region nodes for CL bath contrast
    mid_nodes = []
    for li in range(bl_idx + 1, n_layers - 1):
        for i in layer_indices[li]:
            if i not in blocked and i not in set(det_list):
                mid_nodes.append(i)

    return {
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "mid_nodes": mid_nodes,
        "field": field,
        "cy": cy,
    }


def run_scaling_test(label, gap, n_layers_list, n_seeds=16, lam=5.0):
    """Test purity vs N scaling on 3D DAGs."""
    k_band = [3.0, 5.0, 7.0]

    print(f"  [{label}]")
    print(f"  {'N':>4s}  {'S_norm':>8s}  {'pur_cl':>8s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'n_ok':>4s}")
    print(f"  {'-'*48}")

    results = []
    for nl in n_layers_list:
        pur_list = []
        min_list = []
        s_list = []

        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed * 13 + 5, gap=gap,
            )

            setup = setup_slit_experiment_3d(positions, adj, layer_indices)
            if setup is None:
                continue

            blocked = setup["blocked"]
            blocked_a = blocked | set(setup["slit_b"])
            blocked_b = blocked | set(setup["slit_a"])
            mid_nodes = setup["mid_nodes"]

            if len(mid_nodes) < 4 or len(setup["det_list"]) < 3:
                continue

            for k in k_band:
                amps_a = propagate_3d(positions, adj, setup["field"],
                                      setup["src"], k, blocked_a)
                amps_b = propagate_3d(positions, adj, setup["field"],
                                      setup["src"], k, blocked_b)

                _, S_norm = cl_bath_contrast_3d(
                    amps_a, amps_b, mid_nodes, positions)
                D = math.exp(-lam**2 * S_norm)

                pur = cl_purity(amps_a, amps_b, D, setup["det_list"])
                pur_min = cl_purity(amps_a, amps_b, 0.0, setup["det_list"])

                if not math.isnan(pur) and not math.isnan(pur_min):
                    pur_list.append(pur)
                    min_list.append(pur_min)
                    s_list.append(S_norm)

        if pur_list:
            mp = sum(pur_list) / len(pur_list)
            mm = sum(min_list) / len(min_list)
            ms = sum(s_list) / len(s_list)
            n_ok = len(pur_list)
            print(f"  {nl:4d}  {ms:8.5f}  {mp:8.4f}  {mm:8.4f}  "
                  f"{1-mp:+8.4f}  {n_ok:4d}")
            results.append((nl, ms, mp, mm))
        else:
            print(f"  {nl:4d}  FAIL")

    return results


def main():
    print("=" * 70)
    print("3D DECOHERENCE: CL bath on 3D causal DAGs")
    print("  Does the CLT ceiling shift in 3D?")
    print("  D = exp(-lambda^2 * S_norm), lambda = 5.0")
    print("=" * 70)
    print()

    n_layers_list = [10, 15, 20, 25, 30, 40]

    # Test 1: 3D uniform (gap=0)
    print("TEST 1: Purity scaling")
    print()
    r_uniform = run_scaling_test("3D Uniform (gap=0)", gap=0.0,
                                 n_layers_list=n_layers_list, n_seeds=16)
    print()

    r_mod3 = run_scaling_test("3D Modular gap=3", gap=3.0,
                               n_layers_list=n_layers_list, n_seeds=16)
    print()

    r_mod5 = run_scaling_test("3D Modular gap=5", gap=5.0,
                               n_layers_list=n_layers_list, n_seeds=16)
    print()

    # Test 2: Lambda sweep at fixed N
    print("TEST 2: Lambda sweep at N=20 (3D Modular gap=5)")
    print()
    k_band = [3.0, 5.0, 7.0]
    print(f"  {'lambda':>6s}  {'pur_cl':>8s}  {'pur_min':>8s}  {'decoh':>8s}")
    print(f"  {'-'*36}")

    for lam in [0.0, 1.0, 3.0, 5.0, 10.0, 20.0]:
        pur_list = []
        min_list = []
        for seed in range(16):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=20, nodes_per_layer=30, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed * 13 + 5, gap=5.0,
            )
            setup = setup_slit_experiment_3d(positions, adj, layer_indices)
            if setup is None:
                continue

            blocked_a = setup["blocked"] | set(setup["slit_b"])
            blocked_b = setup["blocked"] | set(setup["slit_a"])

            for k in k_band:
                amps_a = propagate_3d(positions, adj, setup["field"],
                                      setup["src"], k, blocked_a)
                amps_b = propagate_3d(positions, adj, setup["field"],
                                      setup["src"], k, blocked_b)

                _, S_norm = cl_bath_contrast_3d(
                    amps_a, amps_b, setup["mid_nodes"], positions)
                D = math.exp(-lam**2 * S_norm) if lam > 0 else 1.0

                pur = cl_purity(amps_a, amps_b, D, setup["det_list"])
                pur_min = cl_purity(amps_a, amps_b, 0.0, setup["det_list"])
                if not math.isnan(pur) and not math.isnan(pur_min):
                    pur_list.append(pur)
                    min_list.append(pur_min)

        if pur_list:
            mp = sum(pur_list) / len(pur_list)
            mm = sum(min_list) / len(min_list)
            print(f"  {lam:6.1f}  {mp:8.4f}  {mm:8.4f}  {1-mp:+8.4f}")

    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print()
    print("  2D CL bath ceiling: pur_min → 1 at N=80+ (CLT convergence)")
    print("  Question: does 3D delay or eliminate this ceiling?")
    print()
    print("  If S_norm stays bounded → 3D breaks the CLT ceiling")
    print("  If S_norm → 0 with N → same CLT problem in 3D")
    print()
    print("  If pur_cl stays < 0.95 at N=40: 3D helps")
    print("  If pur_cl → 1 at N=40: 3D doesn't help")
    print("=" * 70)


if __name__ == "__main__":
    main()
