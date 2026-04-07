#!/usr/bin/env python3
"""Wave-equation self-field: time-dependent generalization of 3D Poisson.

Solves the discrete wave equation
    (1/c^2) * d^2f/dt^2 - laplacian_yz(f) = source(t, y, z)
with x as time (lightcone discretization on the DAG layers).

Stencil (c = 1 lattice unit per layer, dt = h):
    f[t+1] = 2 f[t] - f[t-1] + h^2 * (laplacian_yz(f[t]) + src[t])

Tests:
  1. Static source: stationary profile should match 3D Poisson
  2. F~M across 3 families with static source
  3. Born test with static wave-equation field
  4. Null at s=0
  5. Retardation: pulsed source -> response arrives with delay = d/c
  6. Family portability
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
MASS_Z = 3.0
S = 0.004
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


def _laplacian_yz(f, nw):
    lap = [[0.0] * nw for _ in range(nw)]
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            lap[iy][iz] = f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1] - 4.0 * f[iy][iz]
    return lap


def _solve_wave(nw, src_layer, src_iy, src_iz, strength, pulse_layers=None):
    """Wave-equation evolution; returns f[t][iy][iz] for t in 0..NL-1.

    pulse_layers=None -> static source (on for t >= src_layer)
    pulse_layers=set  -> source on only at those layer indices (pulse)
    """
    sy = src_iy + nw // 2
    sz = src_iz + nw // 2
    f_prev = [[0.0] * nw for _ in range(nw)]
    f_curr = [[0.0] * nw for _ in range(nw)]
    history = [[[0.0] * nw for _ in range(nw)]]
    history.append([[0.0] * nw for _ in range(nw)])
    h2 = H * H
    for t in range(2, NL):
        active = (pulse_layers is None and t >= src_layer) or (pulse_layers is not None and t in pulse_layers)
        lap = _laplacian_yz(f_curr, nw)
        f_next = [[0.0] * nw for _ in range(nw)]
        for iy in range(nw):
            for iz in range(nw):
                src = strength if (active and iy == sy and iz == sz) else 0.0
                f_next[iy][iz] = 2.0 * f_curr[iy][iz] - f_prev[iy][iz] + h2 * (lap[iy][iz] + src)
        f_prev = f_curr
        f_curr = f_next
        history.append([row[:] for row in f_curr])
    return history


def _make_wave_field(s, z_src, pulse_layers=None):
    hw = int(PW / H)
    nw = 2 * hw + 1
    src_layer = NL // 3
    iz_src = round(z_src / H)
    return _solve_wave(nw, src_layer, 0, iz_src, s, pulse_layers=pulse_layers)


def _field_at(history, layer, iy, iz):
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL and 0 <= sy < nw and 0 <= sz < nw:
        return history[layer][sy][sz]
    return 0.0


def _prop_beam(pos, adj, nmap, history, k, sources=None):
    n = len(pos)
    hw = int(PW / H)
    nw = 2 * hw + 1
    field = [0.0] * n
    if history is not None:
        for layer in range(NL):
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    idx = nmap.get((layer, iy, iz))
                    if idx is not None:
                        field[idx] = _field_at(history, layer, iy, iz)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            phase = k * L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def _cz(amps, pos):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl
    n = len(pos)
    t = sum(abs(amps[i]) ** 2 for i in range(ds, n))
    if t <= 0:
        return 0.0
    return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, n)) / t


def _dp(amps, pos):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl
    return sum(abs(amps[i]) ** 2 for i in range(ds, len(pos)))


def main():
    print("=" * 70)
    print("WAVE-EQUATION SELF-FIELD HARNESS")
    print(f"NL={NL}, W={PW}, s={S}, z_src={MASS_Z}")
    print("=" * 70)

    print("\nSolving wave equation (static source)...")
    history = _make_wave_field(S, MASS_Z)

    # 1. Stationary profile
    gl = NL // 3
    iz_src = round(MASS_Z / H)
    print("\n1. STATIONARY PROFILE at late time (layer NL-2)")
    print(f"  {'iz':>4s} {'f_wave':>14s}")
    for iz in range(-3, 8):
        f = _field_at(history, NL - 2, 0, iz)
        print(f"  {iz:4d} {f:+14.6f}")

    # 2. Gravity TOWARD across families
    print("\n2. GRAVITY across families (static wave field)")
    for label, drift, restore in FAMILIES:
        pos, adj, nmap = grow(0, drift, restore)
        free = _prop_beam(pos, adj, nmap, None, K)
        z_free = _cz(free, pos)
        g = _prop_beam(pos, adj, nmap, history, K)
        delta = _cz(g, pos) - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {label}: delta={delta:+.6f} {direction}")

    # 3. F~M
    print("\n3. F~M across families")
    strengths = [0.001, 0.002, 0.004, 0.008]
    fls = [_make_wave_field(s, MASS_Z) for s in strengths]
    for label, drift, restore in FAMILIES:
        pos, adj, nmap = grow(0, drift, restore)
        free = _prop_beam(pos, adj, nmap, None, K)
        z_free = _cz(free, pos)
        deltas = []
        for fl in fls:
            g = _prop_beam(pos, adj, nmap, fl, K)
            deltas.append(abs(_cz(g, pos) - z_free))
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in deltas if y > 1e-15]
        if len(ly) >= 3:
            mx = sum(lx[: len(ly)]) / len(ly)
            my = sum(ly) / len(ly)
            sxx = sum((x - mx) ** 2 for x in lx[: len(ly)])
            fm = sum((x - mx) * (y - my) for x, y in zip(lx[: len(ly)], ly)) / sxx
            print(f"  {label}: F~M = {fm:.4f}")

    # 4. Born
    print("\n4. BORN TEST (Fam1, seed=0, wave-equation field)")
    pos, adj, nmap = grow(0, 0.2, 0.7)
    slits = [-1, 0, 1]

    def pb(sl):
        srcs = [(nmap.get((0, s, 0)) or nmap.get((1, s, 0)), 1.0 + 0j) for s in sl]
        srcs = [(i, a) for i, a in srcs if i is not None]
        return _dp(_prop_beam(pos, adj, nmap, history, K, sources=srcs), pos)

    p123 = pb(slits)
    p12 = pb([-1, 0])
    p13 = pb([-1, 1])
    p23 = pb([0, 1])
    p1 = pb([-1])
    p2 = pb([0])
    p3 = pb([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)
    print(f"  Born |I3|/P = {born:.2e}")

    # 5. Null
    print("\n5. NULL TEST")
    pos, adj, nmap = grow(0, 0.2, 0.7)
    free = _prop_beam(pos, adj, nmap, None, K)
    z_free = _cz(free, pos)
    h0 = _make_wave_field(0.0, MASS_Z)
    g0 = _prop_beam(pos, adj, nmap, h0, K)
    print(f"  s=0: delta = {_cz(g0, pos) - z_free:+.6e}")

    # 6. RETARDATION: pulse source at one layer and watch arrival
    print("\n6. RETARDATION (single-layer pulse at src_layer)")
    src_layer = NL // 3
    pulse_history = _make_wave_field(S * 100.0, MASS_Z, pulse_layers={src_layer})
    print(f"  pulse fired at layer {src_layer}")
    print(f"  {'layer':>5s} {'dt':>4s} {'|f| at iz=src':>16s}")
    for layer in range(src_layer, min(src_layer + 8, NL)):
        f = abs(_field_at(pulse_history, layer, 0, iz_src))
        print(f"  {layer:5d} {layer - src_layer:4d} {f:16.6e}")
    print("  (lightcone: response should grow at most one cell per dt)")


if __name__ == "__main__":
    main()
