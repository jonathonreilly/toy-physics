#!/usr/bin/env python3
"""Discrete Shapiro delay: c-dependent phase lag on three grown families.

The causal field produces a phase lag at the detector that depends on
the field propagation speed c. This is the discrete analog of the
Shapiro time delay in GR.

Tests portability across three independent grown families.
Zero control: c=None (instantaneous) gives phase=0 by construction.
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
C_VALUES = [2.0, 1.0, 0.5, 0.25]
FAMILIES = [
    ("Fam1", 0.20, 0.70),
    ("Fam2", 0.05, 0.30),
    ("Fam3", 0.50, 0.90),
]
SEEDS = [0, 1]


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


def prop_field(pos, adj, nmap, s, z_src, k, c_field=None):
    n = len(pos)
    gl = NL // 3
    iz_s = round(z_src / H)
    mi = nmap.get((gl, 0, iz_s))
    if mi is None:
        return [0j] * n
    mx, my, mz = pos[mi]
    x_src = gl * H
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

            def field_at(idx):
                if c_field is None:
                    r = math.sqrt(
                        (pos[idx][0] - mx) ** 2
                        + (pos[idx][1] - my) ** 2
                        + (pos[idx][2] - mz) ** 2
                    ) + 0.1
                    return s / r
                x_n = pos[idx][0]
                if x_n < x_src - 0.01:
                    return 0.0
                dt = abs(x_n - x_src) / H
                reach = c_field * dt * H + 0.1
                r_t = math.sqrt((pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2)
                if r_t > reach:
                    return 0.0
                r = math.sqrt(
                    (pos[idx][0] - mx) ** 2
                    + (pos[idx][1] - my) ** 2
                    + (pos[idx][2] - mz) ** 2
                ) + 0.1
                return s / r

            fi = field_at(i)
            fj = field_at(j)
            lf = 0.5 * (fi + fj)
            act = L * (1.0 - lf)
            phase = k * act
            theta = math.atan2(math.sqrt(dy_e * dy_e + dz_e * dz_e), max(dx_e, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += (
                amps[i]
                * complex(math.cos(phase), math.sin(phase))
                * w
                * h2
                / (L * L)
            )
    return amps


def main():
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2

    print("=" * 75)
    print("DISCRETE SHAPIRO DELAY: THREE-FAMILY PORTABILITY")
    print(f"NL={NL}, W={PW}, s={S}, z_src={MASS_Z}")
    print(f"Families: {len(FAMILIES)}, Seeds: {len(SEEDS)}, c values: {C_VALUES}")
    print("=" * 75)
    print()

    for label, drift, restore in FAMILIES:
        print(f"{label} (drift={drift}, restore={restore}):")
        print(f"  {'c':>6s}", end="")
        for seed in SEEDS:
            print(f"  {'s' + str(seed) + '_phase':>10s}", end="")
        print(f"  {'mean_phase':>12s}")
        print("  " + "-" * (8 + 12 * len(SEEDS) + 14))

        for c in [None] + C_VALUES:
            phases = []
            for seed in SEEDS:
                pos, adj, nmap = grow(seed, drift, restore)
                n = len(pos)
                ds = n - npl

                psi_inst = prop_field(pos, adj, nmap, S, MASS_Z, K, c_field=None)
                psi_c = prop_field(pos, adj, nmap, S, MASS_Z, K, c_field=c)

                # Overlap at detector
                det_inst = psi_inst[ds:]
                det_c = psi_c[ds:]
                n_inst = math.sqrt(sum(abs(a) ** 2 for a in det_inst))
                n_c = math.sqrt(sum(abs(a) ** 2 for a in det_c))

                if n_inst > 0 and n_c > 0:
                    overlap = sum(
                        a.conjugate() / n_inst * b / n_c
                        for a, b in zip(det_inst, det_c)
                    )
                    phase = math.atan2(overlap.imag, overlap.real)
                else:
                    phase = 0.0
                phases.append(phase)

            mean_p = sum(phases) / len(phases)
            c_label = f"{'inst':>6s}" if c is None else f"{c:6.2f}"
            row = f"  {c_label}"
            for p in phases:
                row += f"  {p:+10.6f}"
            row += f"  {mean_p:+12.6f}"
            print(row)
        print()

    print("SAFE READ")
    print("  phase at c=None (instantaneous) is 0.000 by construction")
    print("  phase > 0 at finite c: Shapiro-like delay from causal propagation")
    print("  if phase(c) is the same across families: geometry-independent")
    print("  if phase increases as c decreases: slower field → more delay")


if __name__ == "__main__":
    main()
