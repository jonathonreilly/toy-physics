#!/usr/bin/env python3
"""Batch: grow one DAG, measure all b-values. One family+seed per invocation.

Usage: python3 lensing_fine_h_batch.py <family> <seed>
Output: one RESULT line per b-value, parseable by the runner.
"""

from __future__ import annotations
import math
import random
import sys
import time

BETA = 0.8
K_PER_H = 2.5
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0
B_VALUES = [3.0, 4.0, 5.0, 6.0]

FAMILIES = {
    "Fam1": (0.20, 0.70),
    "Fam2": (0.05, 0.30),
    "Fam3": (0.50, 0.90),
}


def grow(seed, drift, restore, NL, PW, H):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
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
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap, NL, hw


def true_kubo(pos, adj, NL, PW, H, k_phase, x_src, z_src):
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    A[0] = 1.0 + 0j
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            w_eff = w * h2 / (L * L)
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * phi * w_eff
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return float('nan')
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 lensing_fine_h_batch.py <family> <seed>")
        sys.exit(1)

    fam_name = sys.argv[1]
    seed = int(sys.argv[2])
    drift, restore = FAMILIES[fam_name]
    H = 0.25
    NL = int(T_PHYS / H) + 1
    k_phase = K_PER_H / H
    x_src = int(NL * SRC_LAYER_FRAC) * H

    t0 = time.time()
    pos, adj, nmap, _, hw = grow(seed, drift, restore, NL, PW_PHYS, H)
    dt_grow = time.time() - t0

    for b in B_VALUES:
        t1 = time.time()
        k = true_kubo(pos, adj, NL, PW_PHYS, H, k_phase, x_src, b)
        dt = time.time() - t1
        print(f"RESULT {fam_name} seed={seed} b={b:.1f} kubo={k:+.6f} t={dt:.1f}s", flush=True)

    print(f"DONE {fam_name} seed={seed} grow={dt_grow:.1f}s nodes={len(pos)}", flush=True)


if __name__ == "__main__":
    main()
