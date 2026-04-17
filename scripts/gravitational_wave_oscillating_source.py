#!/usr/bin/env python3
"""Oscillating-source frequency sweep (early exploration script).

NOTE: This is NOT the canonical harness for the retardation discriminator.
The canonical harness is retardation_discriminator.py, which reproduces
all retained results including the difference curve, delay law, and
global-delay fit test.

This script only runs the frequency sweep and family portability of
the raw oscillating-source phase. It does not test retardation vs
instantaneous, and does not contain the sharpest discriminator.
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
Z0 = 3.0
S = 0.004
A_OSC = 1.5
FREQS = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.5, 1.0]
SEEDS = [0, 1, 2, 3]
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


def prop_osc(pos, adj, nmap, s, z0, amp, freq, k):
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
                z_src = z0 + amp * math.sin(2 * math.pi * freq * ln * H)
                mx, my, mz = x_src, 0.0, z_src
                return s / (math.sqrt(
                    (pos[idx][0] - mx) ** 2 + (pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2
                ) + 0.1)

            lf = 0.5 * (fld(i) + fld(j))
            phase = k * L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy_e * dy_e + dz_e * dz_e), max(dx_e, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def measure_gw_phase(pos, adj, nmap, freq):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    psi_0 = prop_osc(pos, adj, nmap, S, Z0, A_OSC, 0.0, K)
    psi_f = prop_osc(pos, adj, nmap, S, Z0, A_OSC, freq, K)
    n0 = math.sqrt(sum(abs(psi_0[i]) ** 2 for i in range(ds, n)))
    nf = math.sqrt(sum(abs(psi_f[i]) ** 2 for i in range(ds, n)))
    if n0 > 0 and nf > 0:
        ov = sum(psi_0[i].conjugate() / n0 * psi_f[i] / nf for i in range(ds, n))
        return math.atan2(ov.imag, ov.real)
    return 0.0


def main():
    print("=" * 70)
    print("GRAVITATIONAL WAVE DETECTION: OSCILLATING SOURCE")
    print(f"z0={Z0}, A={A_OSC}, s={S}")
    print("=" * 70)
    print()

    # Frequency sweep on seed 0, Family 1
    pos, adj, nmap = grow(0, 0.2, 0.7)
    print("FREQUENCY SWEEP (seed=0, Fam1):")
    print(f"{'freq':>8s} {'phase':>12s}")
    print("-" * 24)
    for f in FREQS:
        p = measure_gw_phase(pos, adj, nmap, f)
        print(f"{f:8.3f} {p:+12.6f}")

    # Seed robustness at peak
    print(f"\nSEED ROBUSTNESS at f=0.03:")
    for seed in SEEDS:
        pos, adj, nmap = grow(seed, 0.2, 0.7)
        p = measure_gw_phase(pos, adj, nmap, 0.03)
        print(f"  seed {seed}: phase = {p:+.6f}")

    # Family portability at peak
    print(f"\nFAMILY PORTABILITY at f=0.03:")
    for label, drift, restore in FAMILIES:
        phases = []
        for seed in [0, 1]:
            pos, adj, nmap = grow(seed, drift, restore)
            phases.append(measure_gw_phase(pos, adj, nmap, 0.03))
        mean_p = sum(phases) / len(phases)
        print(f"  {label}: phase = {mean_p:+.6f}")


if __name__ == "__main__":
    main()
