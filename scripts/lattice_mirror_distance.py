#!/usr/bin/env python3
"""Lattice-mirror DAG: regular grid with Z₂ symmetry for distance law.

On random DAGs, amplitude executes a transverse random walk that
fills the y-range, preventing beam confinement and 1/b falloff.

On a LATTICE, nodes are at fixed grid positions. Each node connects
to neighbors in the next layer with |Δy| ≤ 1. The beam spreads
as sqrt(N) in y, much slower than on random graphs.

If the mass is at y_mass >> sqrt(N), the beam doesn't reach the
mass region, and gravity should decay with distance.

Implementation:
  - Nodes at (x, y) where x = 0..N-1, y = -W..+W (integer grid)
  - Z₂ mirror: edges at y mirror to edges at -y
  - Forward edges: (x,y) → (x+1, y'), |y' - y| ≤ 1
  - Diagonal edges: (x,y) → (x+1, y±1) with weight phase from action
  - Barrier at x = N/3 with slits at |y| > slit_gap
  - Mass at layer x = 2N/3 at y = b (impact parameter)
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
N_YBINS = 8
LAM = 10.0
SLIT_GAP = 2  # Slits at |y| > slit_gap


def generate_lattice_mirror(n_layers, half_width, rng_seed, add_noise=0.0):
    """Generate a 2D lattice with Z₂ symmetry.

    Nodes at integer positions (x, y) where y ∈ [-half_width, +half_width].
    Edges: (x,y) → (x+1, y') where |y'-y| ≤ 1.
    Z₂: every edge (x,y)→(x+1,y') has mirror (x,-y)→(x+1,-y').

    add_noise: small random perturbation to y-positions (0 = perfect lattice).
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    node_map = {}  # (layer, y) → node_idx

    for layer in range(n_layers):
        x = float(layer)
        for y in range(-half_width, half_width + 1):
            y_pos = float(y) + (rng.gauss(0, add_noise) if add_noise > 0 else 0)
            idx = len(positions)
            positions.append((x, y_pos))
            node_map[(layer, y)] = idx

    # Build edges: forward connections with |Δy| ≤ 1
    for layer in range(n_layers - 1):
        for y in range(-half_width, half_width + 1):
            src_idx = node_map.get((layer, y))
            if src_idx is None:
                continue
            for dy in [-1, 0, 1]:
                y_next = y + dy
                if abs(y_next) > half_width:
                    continue
                dst_idx = node_map.get((layer + 1, y_next))
                if dst_idx is not None:
                    adj[src_idx].append(dst_idx)

    barrier_layer = n_layers // 3
    return positions, dict(adj), barrier_layer, node_map


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions)
    # Topo order on lattice is just layer order
    order = sorted(range(n), key=lambda i: positions[i][0])
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


def compute_field_at_b(positions, node_map, grav_layer, b, n_mass=3,
                        strength=0.1):
    """Field from mass nodes at y ≈ b on the gravity layer."""
    n = len(positions)
    field = [0.0] * n
    # Select nodes closest to y = b on gravity layer
    candidates = []
    for y in range(-30, 31):
        idx = node_map.get((grav_layer, y))
        if idx is not None:
            candidates.append((abs(y - b), idx))
    candidates.sort()
    mass_nodes = [idx for _, idx in candidates[:n_mass]]

    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += strength / r
    return field, mass_nodes


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    return m, math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1) / len(vals))


def main():
    print("=" * 90)
    print("LATTICE-MIRROR: DISTANCE LAW ON REGULAR GRID")
    print(f"  k={K}, BETA={BETA}")
    print("=" * 90)
    print()

    n_layers_list = [30, 40, 60]
    half_width = 20
    b_values = [3, 5, 7, 10, 13, 16, 19]

    for nl in n_layers_list:
        print(f"  N_LAYERS = {nl}, half_width = {half_width}")
        print(f"  beam spread ≈ sqrt({2*nl//3}) = {math.sqrt(2*nl/3):.1f}")
        print(f"  {'b':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>6s}")
        print(f"  {'-' * 34}")

        positions, adj, bl, nmap = generate_lattice_mirror(nl, half_width, 42)
        layers_sorted = sorted(set(round(p[0]) for p in positions))
        src_layer = layers_sorted[0]
        det_layer = layers_sorted[-1]

        src = [nmap[(src_layer, 0)]]  # Source at y=0
        det_list = [nmap[(det_layer, y)] for y in range(-half_width, half_width+1)
                    if (det_layer, y) in nmap]

        # Barrier: block nodes at |y| ≤ slit_gap on barrier layer
        bi = [nmap[(bl, y)] for y in range(-half_width, half_width+1) if (bl, y) in nmap]
        sa = [nmap[(bl, y)] for y in range(SLIT_GAP+1, half_width+1) if (bl, y) in nmap][:3]
        sb = [nmap[(bl, y)] for y in range(-half_width, -SLIT_GAP) if (bl, y) in nmap][:3]
        blocked = set(bi) - set(sa + sb)

        grav_layer = layers_sorted[2 * len(layers_sorted) // 3]

        b_data, d_data = [], []
        for b in b_values:
            if b > half_width:
                continue
            field_m, mass = compute_field_at_b(positions, nmap, grav_layer, b, n_mass=1)
            field_f = [0.0] * len(positions)
            am = propagate(positions, adj, field_m, src, K, blocked)
            af = propagate(positions, adj, field_f, src, K, blocked)
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                delta = ym - yf
                print(f"  {b:4d}  {delta:+8.4f}")
                if delta > 0:
                    b_data.append(b)
                    d_data.append(delta)

        if len(b_data) >= 3:
            peak_idx = max(range(len(d_data)), key=lambda i: d_data[i])
            pk = b_data[peak_idx]
            falloff = [(b, d) for b, d in zip(b_data, d_data) if b > pk and d > 0]
            if len(falloff) >= 2:
                lx = [math.log(b) for b, _ in falloff]
                ly = [math.log(d) for _, d in falloff]
                nn = len(lx)
                mx = sum(lx) / nn
                my = sum(ly) / nn
                sxx = sum((x - mx) ** 2 for x in lx)
                sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
                slope = sxy / sxx if sxx > 1e-10 else 0
                print(f"  Peak at b={pk}, falloff ~ b^({slope:.2f})")
            else:
                print(f"  Peak at b={pk}, not enough falloff points")
        print()

    # k=0 control
    print("k=0 CONTROL (N=40, b=7):")
    positions, adj, bl, nmap = generate_lattice_mirror(40, half_width, 42)
    layers_sorted = sorted(set(round(p[0]) for p in positions))
    src = [nmap[(layers_sorted[0], 0)]]
    det_list = [nmap[(layers_sorted[-1], y)] for y in range(-half_width, half_width+1)
                if (layers_sorted[-1], y) in nmap]
    bi = [nmap[(bl, y)] for y in range(-half_width, half_width+1) if (bl, y) in nmap]
    sa = [nmap[(bl, y)] for y in range(SLIT_GAP+1, half_width+1) if (bl, y) in nmap][:3]
    sb = [nmap[(bl, y)] for y in range(-half_width, -SLIT_GAP) if (bl, y) in nmap][:3]
    blocked = set(bi) - set(sa + sb)
    grav_layer = layers_sorted[2 * len(layers_sorted) // 3]
    field_m, _ = compute_field_at_b(positions, nmap, grav_layer, 7, n_mass=1)
    field_f = [0.0] * len(positions)
    am = propagate(positions, adj, field_m, src, 0.0, blocked)
    af = propagate(positions, adj, field_f, src, 0.0, blocked)
    pm = sum(abs(am[d]) ** 2 for d in det_list)
    pf = sum(abs(af[d]) ** 2 for d in det_list)
    if pm > 1e-30 and pf > 1e-30:
        gk0 = (sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
               - sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf)
        print(f"  gravity at k=0: {gk0:+.6e}")

    print()
    print("PREDICTION: beam spread ~ sqrt(N) on lattice.")
    print("  If b > sqrt(N): beam doesn't reach mass → gravity decays")
    print("  If b < sqrt(N): beam reaches mass → gravity b-independent")
    print("  Transition at b ~ sqrt(N) should give 1/b-like falloff")


if __name__ == "__main__":
    main()
