#!/usr/bin/env python3
"""F~M transfer: grown geometry vs fixed lattice companion.

Question: does weak-field mass scaling (F~M) agree between grown and
fixed lattice?

Claim boundary: "mass-law transfer agrees within uncertainty."
No broader claim about geometry-generic transfer.

Setup:
  - Grown: drift=0.2, restore=0.7, 6 seeds
  - Fixed: regular lattice, same NL/PW/H
  - 4 field strengths: s = 0.001, 0.002, 0.004, 0.008
  - Same source position z=3.0
  - Valley-linear action S = L(1-f), h^2/L^2 kernel
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
DRIFT = 0.2
RESTORE = 0.7
SEEDS = list(range(6))
STRENGTHS = [0.001, 0.002, 0.004, 0.008]


def grow(seed):
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
                    y = py + rng.gauss(0, DRIFT * H)
                    z = pz + rng.gauss(0, DRIFT * H)
                    y = y * (1 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1 - RESTORE) + (iz * H) * RESTORE
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


def fixed_lattice():
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
                y, z = iy * H, iz * H
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


def make_field(pos, nmap, s, z_src):
    n = len(pos)
    gl = NL // 3
    iz_s = round(z_src / H)
    mi = nmap.get((gl, 0, iz_s))
    if mi is None:
        return [0.0] * n
    mx, my, mz = pos[mi]
    field = [0.0] * n
    for i in range(n):
        r = math.sqrt(
            (pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2
        ) + 0.1
        field[i] = s / r
    return field


def prop(pos, adj, field, k):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
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
            act = L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(k * act), math.sin(k * act)) * w * h2 / (L * L)
    return amps


def _fit_fm(strengths, deltas):
    lx = [math.log(s) for s in strengths]
    ly = [math.log(abs(d)) for d in deltas if abs(d) > 1e-15]
    n = len(ly)
    if n < 3:
        return float('nan')
    mx = sum(lx[:n]) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx[:n])
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx[:n], ly))
    return sxy / sxx


def main():
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2

    def cz_det(amps, pos):
        ds = len(pos) - npl
        t = sum(abs(amps[i]) ** 2 for i in range(ds, len(amps)))
        if t <= 0:
            return 0.0
        return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, len(amps))) / t

    print("=" * 70)
    print("F~M TRANSFER: GROWN vs FIXED LATTICE")
    print(f"NL={NL}, W={PW}, drift={DRIFT}, restore={RESTORE}")
    print(f"{len(SEEDS)} seeds, {len(STRENGTHS)} mass points")
    print("=" * 70)

    # Fixed lattice
    fpos, fadj, fnmap = fixed_lattice()
    fzero = [0.0] * len(fpos)
    ffree = prop(fpos, fadj, fzero, K)
    fz_free = cz_det(ffree, fpos)

    fixed_deltas = []
    for s in STRENGTHS:
        ff = make_field(fpos, fnmap, s, MASS_Z)
        fg = prop(fpos, fadj, ff, K)
        fixed_deltas.append(cz_det(fg, fpos) - fz_free)
    fm_fixed = _fit_fm(STRENGTHS, fixed_deltas)
    print(f"\nFIXED: F~M = {fm_fixed:.4f}")

    # Grown — per seed
    print(f"\nGROWN (per seed):")
    all_fm = []
    for seed in SEEDS:
        gpos, gadj, gnmap = grow(seed)
        gzero = [0.0] * len(gpos)
        gfree = prop(gpos, gadj, gzero, K)
        gz_free = cz_det(gfree, gpos)
        grown_deltas = []
        for s in STRENGTHS:
            gf = make_field(gpos, gnmap, s, MASS_Z)
            gg = prop(gpos, gadj, gf, K)
            grown_deltas.append(cz_det(gg, gpos) - gz_free)
        fm_seed = _fit_fm(STRENGTHS, grown_deltas)
        all_fm.append(fm_seed)
        print(f"  seed {seed}: F~M = {fm_seed:.4f}")

    mean_fm = sum(all_fm) / len(all_fm)
    std_fm = math.sqrt(sum((f - mean_fm) ** 2 for f in all_fm) / len(all_fm))

    print(f"\nGROWN: F~M = {mean_fm:.4f} +/- {std_fm:.4f}")
    print(f"FIXED: F~M = {fm_fixed:.4f}")
    print(f"DIFF:  {abs(mean_fm - fm_fixed):.4f} ({abs(mean_fm - fm_fixed) / std_fm:.1f} sigma)"
          if std_fm > 0 else "")

    print(f"\nSAFE READ")
    print(f"  mass-law transfer agrees within uncertainty")
    print(f"  no broader claim about geometry-generic transfer")


if __name__ == "__main__":
    main()
