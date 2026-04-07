#!/usr/bin/env python3
"""Packet memory: initial-condition information survives to the detector.

Reproduces all retained results in PACKET_MEMORY_NOTE.md:
  Tier A: overlap vs offset, overlap vs NL, gravity-by-packet
  Tier B: width (sigma_z) for narrow / medium / offset packets
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
PW = 8
S = 0.004
MASS_Z = 3.0


def grow(seed, drift, restore, NL):
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


def _prop(pos, adj, nmap, NL, k, sources, field_fn=None):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    for idx, amp in sources:
        if idx is not None:
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
            f = 0.0
            if field_fn is not None:
                f = 0.5 * (field_fn(i) + field_fn(j))
            phase = k * L * (1.0 - f)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def _det_amps(amps, pos, NL):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    return amps[n - npl:]


def _overlap(a, b):
    na = math.sqrt(sum(abs(x) ** 2 for x in a))
    nb = math.sqrt(sum(abs(x) ** 2 for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return abs(sum(x.conjugate() * y for x, y in zip(a, b))) / (na * nb)


def _packet_src(nmap, iz_off):
    s = nmap.get((0, 0, iz_off))
    if s is None:
        s = nmap.get((1, 0, iz_off))
    return [(s, 1.0 + 0j)] if s is not None else []


def _cz(amps_det, pos, NL):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n_pos = len(pos)
    ds = n_pos - npl
    t = sum(abs(a) ** 2 for a in amps_det)
    if t <= 0:
        return 0.0
    return sum(abs(a) ** 2 * pos[ds + k][2] for k, a in enumerate(amps_det)) / t


def _sigmaz(amps_det, pos, NL):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n_pos = len(pos)
    ds = n_pos - npl
    t = sum(abs(a) ** 2 for a in amps_det)
    if t <= 0:
        return 0.0
    mu = sum(abs(a) ** 2 * pos[ds + k][2] for k, a in enumerate(amps_det)) / t
    var = sum(abs(a) ** 2 * (pos[ds + k][2] - mu) ** 2 for k, a in enumerate(amps_det)) / t
    return math.sqrt(var)


def _imposed_field(pos, x_src, z_src, s):
    return [s / (math.sqrt((p[0] - x_src) ** 2 + (p[2] - z_src) ** 2) + 0.1) for p in pos]


def main():
    print("=" * 70)
    print("PACKET MEMORY HARNESS")
    print("=" * 70)

    # Tier A.1: overlap vs offset at NL=30
    print("\nA.1 OVERLAP vs OFFSET (NL=30)")
    NL = 30
    pos, adj, nmap = grow(0, 0.2, 0.7, NL)
    a0 = _det_amps(_prop(pos, adj, nmap, NL, K, _packet_src(nmap, 0)), pos, NL)
    print(f"  {'offset':>6s} {'overlap':>10s}")
    for off in [0, 1, 2, 3, 8]:
        ax = _det_amps(_prop(pos, adj, nmap, NL, K, _packet_src(nmap, off)), pos, NL)
        print(f"  {off:6d} {_overlap(a0, ax):10.4f}")

    # Tier A.2: overlap (origin vs z=2) across NL
    print("\nA.2 OVERLAP (origin vs z=2) vs NL")
    print(f"  {'NL':>4s} {'overlap':>10s}")
    for NL in [15, 25, 30, 40]:
        pos, adj, nmap = grow(0, 0.2, 0.7, NL)
        a0 = _det_amps(_prop(pos, adj, nmap, NL, K, _packet_src(nmap, 0)), pos, NL)
        a2 = _det_amps(_prop(pos, adj, nmap, NL, K, _packet_src(nmap, 2)), pos, NL)
        print(f"  {NL:4d} {_overlap(a0, a2):10.4f}")

    # Tier A.3: gravity by packet position (NL=30)
    print("\nA.3 GRAVITY BY PACKET")
    NL = 30
    pos, adj, nmap = grow(0, 0.2, 0.7, NL)
    field = _imposed_field(pos, (NL // 3) * H, MASS_Z, S)

    def fld(i):
        return field[i]

    print(f"  {'packet':>10s} {'delta_z':>12s}")
    for label, off in [("origin", 0), ("z=+1", 1), ("z=+2", 2), ("z=+3", 3), ("z=-2", -2)]:
        srcs = _packet_src(nmap, off)
        free = _det_amps(_prop(pos, adj, nmap, NL, K, srcs), pos, NL)
        grav = _det_amps(_prop(pos, adj, nmap, NL, K, srcs, field_fn=fld), pos, NL)
        delta = _cz(grav, pos, NL) - _cz(free, pos, NL)
        print(f"  {label:>10s} {delta:+12.6f}")

    # Tier B: width sigma_z
    print("\nB. WIDTH (sigma_z) at NL=30")
    NL = 30
    pos, adj, nmap = grow(0, 0.2, 0.7, NL)
    # narrow: origin only
    a_narrow = _det_amps(_prop(pos, adj, nmap, NL, K, [(0, 1.0 + 0j)]), pos, NL)
    # medium: 3x3 patch around origin
    med = []
    for iy in range(-1, 2):
        for iz in range(-1, 2):
            idx = nmap.get((1, iy, iz))
            if idx is not None:
                med.append((idx, 1.0 + 0j))
    a_med = _det_amps(_prop(pos, adj, nmap, NL, K, med), pos, NL)
    # offset: z=+2
    a_off = _det_amps(_prop(pos, adj, nmap, NL, K, _packet_src(nmap, 2)), pos, NL)
    print(f"  narrow (origin) sigma_z = {_sigmaz(a_narrow, pos, NL):.3f}")
    print(f"  medium (3x3)    sigma_z = {_sigmaz(a_med, pos, NL):.3f}")
    print(f"  offset (z=+2)   sigma_z = {_sigmaz(a_off, pos, NL):.3f}")


if __name__ == "__main__":
    main()
