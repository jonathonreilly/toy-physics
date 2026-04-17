#!/usr/bin/env python3
"""Decoherence on locally-grown graphs: closing the axiom chain.

Local growth rules produce d_eff ≈ 3. From our dimensional scaling:
  d_spatial=2 (d_eff=3): alpha ≈ -0.7

Can we verify this by running the CL bath on a graph that was GROWN
by a local rule (not imposed)?

This is the decisive test: if a locally-grown graph with d_eff≈3
produces decoherence with alpha ≈ -0.7, the axiom chain closes:

  Local growth → d_eff≈3 graph → path-sum → {gravity, decoherence, Born}

Setup: grow a random k-regular layered DAG, insert a barrier,
run the standard CL bath decoherence measurement.
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque


BETA = 0.8
N_YBINS = 8
LAM = 10.0


def grow_layered_dag(n_layers=20, npl=25, k_connect=5, rng_seed=42):
    """Grow a layered DAG with local random connectivity.

    Each layer has npl nodes at random positions. Edges connect each
    new node to k_connect random nodes in the previous 1-2 layers.

    No geometry is imposed — positions are just labels for later
    measurement. The graph structure is what matters.

    Returns (positions, adj) where positions are (layer, random_y).
    """
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((float(layer), 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(npl):
                y = rng.gauss(0, 3.0)  # random position, no structure imposed
                idx = len(positions)
                positions.append((float(layer), y))
                layer_nodes.append(idx)

                # Connect to k random nodes in previous layers
                candidates = []
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    candidates.extend(prev_layer)
                if candidates:
                    targets = rng.sample(candidates, min(k_connect, len(candidates)))
                    for t in targets:
                        adj[t].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj)


def _topo_order(adj, n):
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
    return order


def compute_field(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_decoherence(positions, adj, nl, seed_label=""):
    """Measure pur_min and gravity on one grown graph."""
    k_band = [3.0, 5.0, 7.0]
    n = len(positions)

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]

    # Slits: top/bottom tercile of barrier layer
    bi_sorted = sorted(bi, key=lambda i: positions[i][1])
    n_slit = max(1, len(bi_sorted) // 3)
    sa = bi_sorted[-n_slit:]  # top
    sb = bi_sorted[:n_slit]   # bottom
    blocked = set(bi) - set(sa + sb)

    # Mass
    grav_layer = layers[2 * len(layers) // 3]
    mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mn = []
    for layer in layers[start:stop]:
        mn.extend(by_layer[layer])
    field = compute_field(positions, list(set(mn) | set(mass)))
    field_flat = [0.0] * n

    pm_vals, gd_vals = [], []
    for k in k_band:
        aa = propagate(positions, adj, field, src, k, blocked | set(sb))
        ab = propagate(positions, adj, field, src, k, blocked | set(sa))

        # pur_min
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2]
                                  + ab[d1].conjugate() * ab[d2])
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr > 1e-30:
            for key in rho:
                rho[key] /= tr
            pm_vals.append(sum(abs(v) ** 2 for v in rho.values()).real)

        # gravity
        am = propagate(positions, adj, field, src, k, blocked)
        af = propagate(positions, adj, field_flat, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            gd_vals.append(ym - yf)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "grav": sum(gd_vals) / len(gd_vals) if gd_vals else 0.0,
    }


def main():
    import time

    print("=" * 70)
    print("DECOHERENCE ON LOCALLY-GROWN GRAPHS")
    print("  Does the full axiom chain close?")
    print("  Local growth → d_eff≈3 → path-sum → decoherence + gravity")
    print("=" * 70)
    print()

    n_seeds = 16

    for k_connect in [4, 6, 8]:
        print(f"  [k_connect={k_connect}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'grav':>8s}  "
              f"{'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 44}")

        data = {}
        for nl in [12, 18, 25, 30, 40, 60]:
            t0 = time.time()
            pm_all, gd_all = [], []
            for seed_i in range(n_seeds):
                seed = seed_i * 7 + 3
                positions, adj = grow_layered_dag(nl, 25, k_connect, seed)
                r = measure_decoherence(positions, adj, nl)
                if r:
                    pm_all.append(r["pm"])
                    gd_all.append(r["grav"])

            dt = time.time() - t0
            if pm_all:
                apm = sum(pm_all) / len(pm_all)
                agd = sum(gd_all) / len(gd_all)
                data[nl] = apm
                n_ok = len(pm_all)
                se_g = (sum((g - agd) ** 2 for g in gd_all) / n_ok) ** 0.5 / math.sqrt(n_ok) if n_ok > 1 else 0
                g_se = agd / se_g if se_g > 0 else 0
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {agd:+8.3f}  "
                      f"{n_ok:4d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL")

            import sys
            sys.stdout.flush()

        # Fit exponent
        fit_ns = [n for n in sorted(data.keys()) if 1 - data[n] > 0.001]
        if len(fit_ns) >= 3:
            xs = [math.log(n) for n in fit_ns]
            ys = [math.log(1 - data[n]) for n in fit_ns]
            nn = len(xs)
            mx = sum(xs) / nn
            my = sum(ys) / nn
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)
            alpha = sxy / sxx
            r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
            print(f"\n  Exponent: alpha = {alpha:.3f}, R² = {r2:.3f}")
            if alpha > -0.5:
                print(f"  → SHALLOW (consistent with d_eff≈3)")
            elif alpha > -1.0:
                print(f"  → MODERATE")
            else:
                print(f"  → STEEP (like 2D imposed graphs)")
        print()

    print("=" * 70)
    print("AXIOM CHAIN TEST:")
    print("  If alpha ≈ -0.7 on grown graphs (like 3D imposed):")
    print("    → local growth + path-sum produces physics automatically")
    print("  If alpha ≈ -1.5 on grown graphs (like 2D imposed):")
    print("    → growth rule doesn't provide enough effective dimension")


if __name__ == "__main__":
    main()
