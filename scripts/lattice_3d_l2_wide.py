#!/usr/bin/env python3
"""3D 1/L^2 kernel: wider lattice at h=0.25 for distance law tail.

Use W=8, L=15 to get z=2..7 range. Numpy-optimized.
Also test h=0.125 if feasible.
"""

from __future__ import annotations
import math
import time
import numpy as np
from collections import defaultdict

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8


def generate(phys_l, phys_w, max_d_phys, h=1.0):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    max_d = max(1, round(max_d_phys / h))
    n = nl * (2 * hw + 1) ** 2

    pos = np.zeros((n, 3))
    nmap = {}
    idx = 0
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                pos[idx] = (x, iy * h, iz * h)
                nmap[(layer, iy, iz)] = idx
                idx += 1

    edge_src = []
    edge_dst = []
    edge_layer = []
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                for diy in range(-max_d, max_d + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-max_d, max_d + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            edge_src.append(si)
                            edge_dst.append(di)
                            edge_layer.append(layer)

    edge_src = np.array(edge_src, dtype=np.int64)
    edge_dst = np.array(edge_dst, dtype=np.int64)
    edge_layer = np.array(edge_layer, dtype=np.int64)

    dp = pos[edge_dst] - pos[edge_src]
    L = np.sqrt(np.sum(dp ** 2, axis=1))
    L = np.maximum(L, 1e-10)
    transverse = np.sqrt(dp[:, 1] ** 2 + dp[:, 2] ** 2)
    theta = np.arctan2(transverse, np.maximum(dp[:, 0], 1e-10))
    w = np.exp(-BETA * theta ** 2)

    return {
        'pos': pos, 'nmap': nmap, 'nl': nl, 'hw': hw, 'n': n,
        'edge_src': edge_src, 'edge_dst': edge_dst, 'edge_layer': edge_layer,
        'L': L, 'w': w,
    }


def propagate_l2(lat, field, k, blocked_set):
    n = lat['n']
    nl = lat['nl']
    amps = np.zeros(n, dtype=np.complex128)
    dists = np.sum(lat['pos'] ** 2, axis=1)
    src = np.argmin(dists)
    amps[src] = 1.0

    blocked = np.zeros(n, dtype=bool)
    for b in blocked_set:
        blocked[b] = True

    edge_field = 0.5 * (field[lat['edge_src']] + field[lat['edge_dst']])
    L = lat['L']
    dl = L * (1 + edge_field)
    ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
    act = dl - ret
    phase = np.exp(1j * k * act) * lat['w'] / (L * L)

    for layer in range(nl - 1):
        mask = lat['edge_layer'] == layer
        e_src = lat['edge_src'][mask]
        e_dst = lat['edge_dst'][mask]
        e_phase = phase[mask]
        src_amps = amps[e_src].copy()
        src_amps[blocked[e_src]] = 0
        contrib = src_amps * e_phase
        contrib[blocked[e_dst]] = 0
        np.add.at(amps, e_dst, contrib)

    return amps


def make_field(lat, z_mass_phys, strength, h):
    pos = lat['pos']
    n = lat['n']
    gl = 2 * lat['nl'] // 3
    iz = round(z_mass_phys / h)
    mi = lat['nmap'].get((gl, 0, iz))
    if mi is None:
        return np.zeros(n), None
    mx, my, mz = pos[mi]
    r = np.sqrt((pos[:, 0] - mx) ** 2 + (pos[:, 1] - my) ** 2 + (pos[:, 2] - mz) ** 2) + 0.1
    return strength / r, mi


def setup_slits(lat):
    pos = lat['pos']
    nmap = lat['nmap']
    nl = lat['nl']
    hw = lat['hw']
    bl = nl // 3
    bi = []
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i, 1] >= 0.5]
    sb = [i for i in bi if pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def fit_power(b_data, d_data):
    if len(b_data) < 3:
        return None, None
    lx = [math.log(b) for b in b_data]
    ly = [math.log(d) for d in d_data]
    nn = len(lx)
    mx = sum(lx) / nn; my = sum(ly) / nn
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def run_convergence(phys_l, phys_w, max_d_phys, h, strength):
    t0 = time.time()
    lat = generate(phys_l, phys_w, max_d_phys, h)
    n = lat['n']
    nl = lat['nl']
    hw = lat['hw']
    nmap = lat['nmap']
    pos = lat['pos']
    t_gen = time.time() - t0

    det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
           for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
    bi, sa, sb, blocked, bl = setup_slits(lat)
    n_edges = len(lat['edge_src'])

    print(f"\nh={h}: {n} nodes, {nl} layers, {n_edges:,} edges ({t_gen:.1f}s gen)")

    field_f = np.zeros(n)
    t1 = time.time()
    af = propagate_l2(lat, field_f, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL")
        return
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf
    print(f"  Free prop: {time.time()-t1:.1f}s")

    # Distance law with many z values
    max_z = min(int(phys_w * 0.9), hw)
    z_values = list(range(2, max_z + 1))
    b_data = []; d_data = []
    print(f"  Distance law (z={z_values[0]}..{z_values[-1]}):")
    for z_mass in z_values:
        t1 = time.time()
        fm, _ = make_field(lat, z_mass, strength, h)
        am = propagate_l2(lat, fm, K, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        dt = time.time() - t1
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"    z={z_mass}: {delta:+.6f} ({sign}) [{dt:.1f}s]")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)

    n_tw = len(b_data)
    print(f"  TOWARD: {n_tw}/{len(z_values)}")

    # Fit tail (after peak)
    if len(b_data) >= 3:
        peak_i = max(range(len(d_data)), key=lambda i: d_data[i])
        tail_b = b_data[peak_i:]
        tail_d = d_data[peak_i:]
        if len(tail_b) >= 3:
            slope, r2 = fit_power(tail_b, tail_d)
            if slope is not None:
                print(f"  TAIL (z>={tail_b[0]}): b^({slope:.2f}), R²={r2:.3f}")
        slope2, r22 = fit_power(b_data, d_data)
        if slope2 is not None:
            print(f"  ALL: b^({slope2:.2f}), R²={r22:.3f}")

    # Quick gravity check
    fm, _ = make_field(lat, 3, strength, h)
    am = propagate_l2(lat, fm, K, blocked)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pm > 1e-30:
        zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
        grav = zm - zf
        print(f"  Gravity z=3: {grav:+.6f} ({'TOWARD' if grav > 0 else 'AWAY'})")

    total = time.time() - t0
    print(f"  TOTAL: {total:.0f}s")


def main():
    print("=" * 70)
    print("3D 1/L^2 KERNEL: DISTANCE LAW CONVERGENCE")
    print("  Does the tail exponent steepen toward -2 at finer h?")
    print("=" * 70)

    s = 5e-5

    # h=0.5, W=8 (confirmed working)
    run_convergence(15, 8, 3, 0.5, s)

    # h=0.25, W=8 (the key test)
    run_convergence(15, 8, 3, 0.25, s)

    print("\n" + "=" * 70)
    print("CONVERGENCE TABLE")
    print("  h=0.5:  tail ~ b^(-0.35)")
    print("  h=0.25: tail ~ ???")
    print("  If steepening toward -2: Newtonian gravity in continuum limit!")
    print("=" * 70)


if __name__ == "__main__":
    main()
