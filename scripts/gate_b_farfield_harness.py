#!/usr/bin/env python3
"""Gate B far-field harness: grown geometry at h=0.5, z>=3.

Freezes the bounded far-field grown-geometry result.

Growth rule: template previous layer + drift + restoring force + NN connectivity.
Tests gravity at z=3,4,5 (far from slits, where the fixed lattice gives 100%).

Reports: TOWARD fraction, F∝M, per-seed detail.
"""

from __future__ import annotations
import cmath
import math
import random
import time

try:
    import numpy as np
except ModuleNotFoundError:
    raise SystemExit("numpy required")

BETA = 0.8
K = 5.0
STRENGTH = 5e-5
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
SEEDS = list(range(12))
Z_MASSES = [3, 4, 5]
DRIFT_RESTORE_ROWS = [
    (0.3, 0.5),
    (0.2, 0.7),
    (0.1, 0.9),
    (0.0, 1.0),
]


def grow(drift, restore, seed):
    rng = random.Random(seed)
    hw = int(PW / H)
    nl = NL
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    layers = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, nl):
        x = layer * H
        nodes = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def propagate(pos, adj, field, k, blocked):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w * hm / (L * L)
    return amps


def main():
    t_total = time.time()
    print("=" * 65)
    print("GATE B FAR-FIELD HARNESS")
    print(f"  Growth: template + drift + restore + NN connectivity")
    print(f"  h={H}, W={PW}, NL={NL}, {len(SEEDS)} seeds, z_masses={Z_MASSES}")
    print("=" * 65)

    for drift, restore in DRIFT_RESTORE_ROWS:
        tw = 0
        tot = 0
        fm_vals = []
        label = f"drift={drift:.1f},rest={restore:.1f}" if drift > 0 else "exact grid"

        for seed in SEEDS:
            pos, adj, layers, nmap = grow(drift, restore, seed)
            n = len(pos)
            det = layers[-1]
            bl_l = NL // 3
            gl = 2 * NL // 3
            barrier = layers[bl_l]
            sa = [i for i in barrier if pos[i][1] >= 0.5]
            sb = [i for i in barrier if pos[i][1] <= -0.5]
            blocked = set(barrier) - set(sa + sb)
            ff = [0.0] * n

            af = propagate(pos, adj, ff, K, blocked)
            pf = sum(abs(af[d]) ** 2 for d in det)
            if pf < 1e-30:
                continue
            zf = sum(abs(af[d]) ** 2 * pos[d][2] for d in det) / pf

            for z_mass in Z_MASSES:
                iz_m = round(z_mass / H)
                mi = nmap.get((gl, 0, iz_m))
                if mi is None:
                    continue
                field = [0.0] * n
                mx, my, mz = pos[mi]
                for i in range(n):
                    r = math.sqrt(
                        (pos[i][0] - mx) ** 2
                        + (pos[i][1] - my) ** 2
                        + (pos[i][2] - mz) ** 2
                    ) + 0.1
                    field[i] = STRENGTH / r
                am = propagate(pos, adj, field, K, blocked)
                pm = sum(abs(am[d]) ** 2 for d in det)
                if pm > 1e-30:
                    zm = sum(abs(am[d]) ** 2 * pos[d][2] for d in det) / pm
                    delta = zm - zf
                    tot += 1
                    if delta > 0:
                        tw += 1

            # F∝M on one z
            mi3 = nmap.get((gl, 0, round(3 / H)))
            if mi3:
                m_data = []
                g_data = []
                for s in [1e-6, 1e-5, 5e-5]:
                    field_s = [0.0] * n
                    mx, my, mz = pos[mi3]
                    for i in range(n):
                        r = math.sqrt(
                            (pos[i][0] - mx) ** 2
                            + (pos[i][1] - my) ** 2
                            + (pos[i][2] - mz) ** 2
                        ) + 0.1
                        field_s[i] = s / r
                    ams = propagate(pos, adj, field_s, K, blocked)
                    pms = sum(abs(ams[d]) ** 2 for d in det)
                    if pms > 1e-30:
                        d2 = sum(abs(ams[d]) ** 2 * pos[d][2] for d in det) / pms - zf
                        if d2 > 0:
                            m_data.append(s)
                            g_data.append(d2)
                if len(m_data) >= 3:
                    lx = np.log(m_data)
                    ly = np.log(g_data)
                    mx_l = np.mean(lx)
                    my_l = np.mean(ly)
                    sxx = np.sum((lx - mx_l) ** 2)
                    sxy = np.sum((lx - mx_l) * (ly - my_l))
                    if sxx > 1e-10:
                        fm_vals.append(sxy / sxx)

        pct = tw / max(tot, 1)
        fm_s = f"{np.mean(fm_vals):.2f}" if fm_vals else "n/a"
        print(f"  {label:25s}: {tw}/{tot} TOWARD ({pct:.0%}), F~M={fm_s}")

    print(f"\nTotal time: {time.time() - t_total:.0f}s")
    print()
    print("SAFE INTERPRETATION")
    print("  This harness tests far-field (z>=3) gravity on grown geometry.")
    print("  If TOWARD > 90%: the growth rule works in the far field.")
    print("  If mixed: the growth rule is noisy even in the far field.")
    print("  F~M should match the fixed-lattice value (1.00) if the")
    print("  universality class transfers to grown geometry.")


if __name__ == "__main__":
    main()
