#!/usr/bin/env python3
"""Nonlinear phase propagation: does intensity-dependent phase rescue 1/b?

The existing nonlinear test (amplitude saturation) barely changes the
distance law because it doesn't affect the phase structure. The phase
valley mechanism is what creates gravity, so the nonlinearity needs to
modify the PHASE to change the distance law.

Three phase-nonlinear variants:

1. KERR: phase += chi * |a_i|^2
   Like optical Kerr effect — intensity modifies refractive index.
   High-amplitude paths get extra phase, breaking linear superposition.

2. ACTION MODULATION: S_eff = S * (1 + eta * |a_i|^2)
   The spent-delay action itself depends on amplitude density.
   Regions with high amplitude have modified geometry.

3. SELF-FOCUSING: edge weight *= (|a_i|/a_ref)^(alpha-1)
   Stronger amplitude paths get amplified (alpha > 1) or suppressed
   (alpha < 1). This creates winner-take-all dynamics.

All tested with FIXED mass geometry (same mass nodes at all b values)
to avoid the confound that killed the causal field claim.

PStack experiment: nonlinear-phase-distance
"""

from __future__ import annotations
import math
import cmath
import random
import statistics
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 12
N_LAYERS = 18
NODES_PER_LAYER = 40
YZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
GAP = 5.0
MASS_COUNT = 8


def generate_3d_modular_dag(n_layers=N_LAYERS, nodes_per_layer=NODES_PER_LAYER,
                            yz_range=YZ_RANGE, connect_radius=CONNECT_RADIUS,
                            rng_seed=42, gap=GAP):
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
            layer_nodes.append(len(positions)-1)
        else:
            for ni in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if gap > 0 and layer > barrier_layer:
                    y = rng.uniform(gap/2, yz_range) if ni < nodes_per_layer//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if gap > 0 and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < 0.02:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def compute_field(positions, adj, mass_ids, iterations=50):
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


def select_mass_fixed(layer_nodes, positions, center_y, target_b, count):
    """Fixed mass selection: same count, closest to target_b."""
    target_y = center_y + target_b
    same_side = [i for i in layer_nodes if positions[i][1] >= center_y]
    ordered = sorted(same_side, key=lambda i: abs(positions[i][1] - target_y))
    return ordered[:count] if len(ordered) >= count else []


def propagate_kerr(positions, adj, field, src, k, chi=0.0):
    """Kerr nonlinearity: phase += chi * |a_i|^2."""
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
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        intensity = abs(ai)**2
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            # Kerr: extra phase proportional to intensity
            phase = k * act + chi * intensity
            ea = cmath.exp(1j * phase) * w / L
            amps[j] += ai * ea
    return amps


def propagate_action_mod(positions, adj, field, src, k, eta=0.0):
    """Action modulation: S_eff = S * (1 + eta * |a_i|^2)."""
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
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        intensity = abs(ai)**2
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            # Action modulated by local intensity
            act_eff = act * (1 + eta * intensity)
            ea = cmath.exp(1j * k * act_eff) * w / L
            amps[j] += ai * ea
    return amps


def propagate_self_focus(positions, adj, field, src, k, alpha_sf=1.0):
    """Self-focusing: edge weight *= (|a_i|/a_ref)^(alpha-1).

    alpha > 1: strong paths reinforced (self-focusing)
    alpha < 1: strong paths suppressed (self-defocusing)
    alpha = 1: linear (baseline)
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
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    a_ref = 1.0 / max(1, len(src))  # reference amplitude
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        # Self-focusing factor
        sf = (abs(ai) / a_ref) ** (alpha_sf - 1) if abs(ai) > 1e-30 else 1.0
        sf = min(sf, 100.0)  # cap to prevent blowup
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w * sf / L
            amps[j] += ai * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def run_b_sweep(propagate_fn, label, param_name, param_val, n_seeds=N_SEEDS):
    """Fixed-mass b-sweep for a given propagator."""
    b_targets = [1.5, 2.5, 3.5, 5.0, 7.0, 9.0]

    print(f"  [{label} {param_name}={param_val}]")
    print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}  {'n':>3s}")
    print(f"  {'-'*32}")

    results = []
    for b in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(rng_seed=seed*17+3)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            grav_idx = 2 * len(layer_indices) // 3
            mass = select_mass_fixed(layer_indices[grav_idx], positions, cy, b, MASS_COUNT)
            if len(mass) < MASS_COUNT:
                continue

            field = compute_field(positions, adj, mass)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in K_BAND:
                kwargs = {param_name: param_val}
                am = propagate_fn(positions, adj, field, src, k, **kwargs)
                af = propagate_fn(positions, adj, free_f, src, k, **kwargs)
                shifts.append(centroid_y(am, positions, det_list) -
                              centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts)/len(shifts))

        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            se = statistics.stdev(per_seed) / math.sqrt(len(per_seed)) if len(per_seed) > 1 else 0
            t = avg / se if se > 1e-10 else 0
            results.append((b, avg, se))
            print(f"  {b:5.1f}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  {len(per_seed):3d}")
        else:
            print(f"  {b:5.1f}  FAIL")

    # Fit power law on positive points
    pos = [(b, s) for b, s, _ in results if s > 0.01]
    if len(pos) >= 3:
        log_b = [math.log(b) for b, _ in pos]
        log_s = [math.log(s) for _, s in pos]
        n = len(log_b)
        sx, sy = sum(log_b), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_b, log_s))
        sxx = sum(x*x for x in log_b)
        denom = n * sxx - sx * sx
        if abs(denom) > 1e-10:
            gamma = -(n * sxy - sx * sy) / denom
            print(f"  → shift ~ b^{-gamma:.2f}")
            if gamma > 0.7:
                print(f"  ★ DISTANCE FALLOFF")
            elif gamma > 0.3:
                print(f"  → partial falloff")
            else:
                print(f"  → flat or increasing")
    print()
    return results


def main():
    print("=" * 70)
    print("NONLINEAR PHASE PROPAGATION: distance law test")
    print("  Fixed mass geometry across all b values")
    print("  3D modular gap=5, 12 seeds")
    print("=" * 70)
    print()

    # Baseline: linear
    run_b_sweep(propagate_kerr, "Linear (baseline)", "chi", 0.0)

    # Kerr sweep
    for chi in [1.0, 5.0, 20.0, 100.0]:
        run_b_sweep(propagate_kerr, "Kerr", "chi", chi)

    # Action modulation sweep
    for eta in [1.0, 10.0, 50.0]:
        run_b_sweep(propagate_action_mod, "Action mod", "eta", eta)

    # Self-focusing sweep
    for alpha in [0.5, 1.5, 2.0]:
        run_b_sweep(propagate_self_focus, "Self-focus", "alpha_sf", alpha)

    print("=" * 70)
    print("If any variant shows shift ~ 1/b: nonlinear phase rescues distance law")
    print("If all flat: distance law failure persists beyond linear path-sum too")
    print("=" * 70)


if __name__ == "__main__":
    main()
