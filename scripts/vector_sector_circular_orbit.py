#!/usr/bin/env python3
"""Vector sector: circular orbit handedness — full executable harness.

Reproduces all retained results in VECTOR_SECTOR_NOTE.md:
  1. Frequency sweep CCW vs CW (vector dy, dz metric)
  2. Phase-averaged handedness (DC component over phi0 sweep)
  3. First-harmonic / lock-in readout (1H amplitude)
  4. f-oddness (+f vs -f sign flip)
  5. Time-order control (time-reversed CCW vs CW)
  6. Family portability (3 families)
  7. Exact nulls (s=0, f=0)
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 30
PW = 8
S = 0.004
R = 4.0
FAMILIES = [("Fam1", 0.20, 0.70), ("Fam2", 0.05, 0.30), ("Fam3", 0.50, 0.90)]


def grow(seed, drift, restore):
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
    return pos, adj, nmap


def _prop_orbit(pos, adj, nmap, s, R_o, direction, freq, k, phi0=0.0, time_reverse=False):
    n = len(pos)
    gl = NL // 3
    x_src = gl * H
    hw = int(PW / H)
    node_layer = {}
    for layer in range(NL):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = nmap.get((layer, iy, iz))
                if idx is not None:
                    node_layer[idx] = layer
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx_e = pos[j][0] - pos[i][0]
            dy_e = pos[j][1] - pos[i][1]
            dz_e = pos[j][2] - pos[i][2]
            L = math.sqrt(dx_e * dx_e + dy_e * dy_e + dz_e * dz_e)
            if L < 1e-10:
                continue

            def fld(idx):
                ln = node_layer.get(idx, 0)
                if time_reverse:
                    ln = NL - 1 - ln
                angle = direction * 2 * math.pi * freq * ln * H + phi0
                y_s = R_o * math.cos(angle)
                z_s = R_o * math.sin(angle)
                return s / (math.sqrt(
                    (pos[idx][0] - x_src) ** 2 + (pos[idx][1] - y_s) ** 2 + (pos[idx][2] - z_s) ** 2
                ) + 0.1)

            lf = 0.5 * (fld(i) + fld(j))
            phase = k * L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy_e * dy_e + dz_e * dz_e), max(dx_e, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def _meas_yz(pos, adj, nmap, s, R_o, d, f, phi0=0.0, time_reverse=False):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    free = _prop_orbit(pos, adj, nmap, 0.0, R_o, +1, f, K)
    tf = sum(abs(free[i]) ** 2 for i in range(ds, n))
    yf = sum(abs(free[i]) ** 2 * pos[i][1] for i in range(ds, n)) / tf if tf > 0 else 0
    zf = sum(abs(free[i]) ** 2 * pos[i][2] for i in range(ds, n)) / tf if tf > 0 else 0
    psi = _prop_orbit(pos, adj, nmap, s, R_o, d, f, K, phi0, time_reverse)
    tp = sum(abs(psi[i]) ** 2 for i in range(ds, n))
    yp = sum(abs(psi[i]) ** 2 * pos[i][1] for i in range(ds, n)) / tp if tp > 0 else 0
    zp = sum(abs(psi[i]) ** 2 * pos[i][2] for i in range(ds, n)) / tp if tp > 0 else 0
    return yp - yf, zp - zf


def main():
    print("=" * 70)
    print("VECTOR SECTOR: CIRCULAR ORBIT HARNESS")
    print(f"R={R}, s={S}, NL={NL}")
    print("=" * 70)

    pos, adj, nmap = grow(0, 0.2, 0.7)
    FREQ = 0.02

    # 1. Exact nulls
    print("\n1. EXACT NULLS")
    dy, dz = _meas_yz(pos, adj, nmap, 0.0, R, +1, FREQ)
    print(f"  s=0:  dy={dy:+.6e}, dz={dz:+.6e}")
    dy_ccw, dz_ccw = _meas_yz(pos, adj, nmap, S, R, +1, 0.0)
    dy_cw, dz_cw = _meas_yz(pos, adj, nmap, S, R, -1, 0.0)
    print(f"  f=0 CCW: dy={dy_ccw:+.6e}, dz={dz_ccw:+.6e}")
    print(f"  f=0 CW:  dy={dy_cw:+.6e}, dz={dz_cw:+.6e}")
    print(f"  f=0 dz diff: {dz_ccw - dz_cw:+.6e}")

    # 2. Frequency sweep (vector metric)
    print(f"\n2. FREQUENCY SWEEP (vector dy, dz)")
    print(f"  {'freq':>6s} {'dy_CCW':>10s} {'dz_CCW':>10s} {'dy_CW':>10s} {'dz_CW':>10s} {'flip':>6s}")
    for f in [0.01, 0.02, 0.03, 0.05, 0.07, 0.1]:
        dy1, dz1 = _meas_yz(pos, adj, nmap, S, R, +1, f)
        dy2, dz2 = _meas_yz(pos, adj, nmap, S, R, -1, f)
        flip = "YES" if (dz1 > 0) != (dz2 > 0) else "no"
        print(f"  {f:6.2f} {dy1:+10.6f} {dz1:+10.6f} {dy2:+10.6f} {dz2:+10.6f} {flip:>6s}")

    # 3. Phase-averaged handedness
    print(f"\n3. PHASE-AVERAGED HANDEDNESS at f={FREQ}")
    N_PHI = 12
    dz_ccw_all = []
    dz_cw_all = []
    for k_phi in range(N_PHI):
        phi0 = 2 * math.pi * k_phi / N_PHI
        _, d1 = _meas_yz(pos, adj, nmap, S, R, +1, FREQ, phi0)
        _, d2 = _meas_yz(pos, adj, nmap, S, R, -1, FREQ, phi0)
        dz_ccw_all.append(d1)
        dz_cw_all.append(d2)
    dc_ccw = sum(dz_ccw_all) / N_PHI
    dc_cw = sum(dz_cw_all) / N_PHI
    print(f"  <dz>_CCW = {dc_ccw:+.6f}")
    print(f"  <dz>_CW  = {dc_cw:+.6f}")
    print(f"  diff: {dc_ccw - dc_cw:+.6f}")

    # 4. First-harmonic
    dz_diff = [c - w for c, w in zip(dz_ccw_all, dz_cw_all)]
    re_1 = sum(dz_diff[k] * math.cos(2 * math.pi * k / N_PHI) for k in range(N_PHI))
    im_1 = sum(dz_diff[k] * math.sin(2 * math.pi * k / N_PHI) for k in range(N_PHI))
    amp_1h = 2 * math.sqrt(re_1 ** 2 + im_1 ** 2) / N_PHI
    dc = sum(dz_diff) / N_PHI
    print(f"\n4. FIRST-HARMONIC (lock-in) READOUT")
    print(f"  DC: {dc:+.6f}")
    print(f"  1H amplitude: {amp_1h:.6f}")
    if abs(dc) > 1e-10:
        print(f"  ratio 1H/DC: {amp_1h / abs(dc):.0f}")

    # 5. f-oddness
    print(f"\n5. f-ODDNESS (+f vs -f, direction=+1)")
    for f in [0.01, 0.02, 0.05]:
        _, dz_pf = _meas_yz(pos, adj, nmap, S, R, +1, +f)
        _, dz_nf = _meas_yz(pos, adj, nmap, S, R, +1, -f)
        flip = "YES" if (dz_pf > 0) != (dz_nf > 0) else "no"
        print(f"  f={f}: dz(+f)={dz_pf:+.6f}, dz(-f)={dz_nf:+.6f}, flip={flip}")

    # 6. Time-order control
    print(f"\n6. TIME-ORDER CONTROL at f={FREQ}")
    _, dz_normal = _meas_yz(pos, adj, nmap, S, R, +1, FREQ)
    _, dz_cw_norm = _meas_yz(pos, adj, nmap, S, R, -1, FREQ)
    _, dz_revtime = _meas_yz(pos, adj, nmap, S, R, +1, FREQ, time_reverse=True)
    print(f"  CCW (normal):    dz = {dz_normal:+.6f}")
    print(f"  CW (normal):     dz = {dz_cw_norm:+.6f}")
    print(f"  CCW (time-rev):  dz = {dz_revtime:+.6f}")

    # 7. Family portability
    print(f"\n7. FAMILY PORTABILITY at f={FREQ}")
    for label, drift, restore in FAMILIES:
        dz_c = []
        dz_w = []
        for seed in [0, 1]:
            p, a, nm = grow(seed, drift, restore)
            _, d1 = _meas_yz(p, a, nm, S, R, +1, FREQ)
            _, d2 = _meas_yz(p, a, nm, S, R, -1, FREQ)
            dz_c.append(d1)
            dz_w.append(d2)
        m1 = sum(dz_c) / 2
        m2 = sum(dz_w) / 2
        flip = "YES" if (m1 > 0) != (m2 > 0) else "no"
        print(f"  {label}: dz_CCW={m1:+.6f}, dz_CW={m2:+.6f}, flip={flip}")


if __name__ == "__main__":
    main()
