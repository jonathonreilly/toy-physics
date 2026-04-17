#!/usr/bin/env python3
"""Retardation discriminator: full retained harness.

Reproduces ALL retained results in RETARDATION_DISCRIMINATOR_NOTE.md:
  1. Frequency sweep (inst vs retarded)
  2. Difference curve (ret - inst)
  3. Delay law (difference vs delay d)
  4. Sign-split band
  5. Global-delay fit test (sharpest discriminator)
  6. Family portability of difference curve
  7. Seed robustness
  8. Exact nulls (f=0 and d=0)
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
DELAY = 5
FAMILIES = [("Fam1", 0.20, 0.70), ("Fam2", 0.05, 0.30), ("Fam3", 0.50, 0.90)]
FREQS = [0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2]


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


def _prop(pos, adj, nmap, freq, delay, phi_shift=0.0):
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
                ln_ret = max(0, ln - delay)
                z_src = Z0 + A_OSC * math.sin(2 * math.pi * freq * ln_ret * H + phi_shift)
                mx, my, mz = x_src, 0.0, z_src
                return S / (math.sqrt(
                    (pos[idx][0] - mx) ** 2 + (pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2
                ) + 0.1)

            lf = 0.5 * (fld(i) + fld(j))
            phase = K * L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy_e * dy_e + dz_e * dz_e), max(dx_e, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def _phase(pos, adj, nmap, freq, delay, phi_shift=0.0):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    psi_0 = _prop(pos, adj, nmap, 0.0, delay, phi_shift)
    psi_f = _prop(pos, adj, nmap, freq, delay, phi_shift)
    n0 = math.sqrt(sum(abs(psi_0[i]) ** 2 for i in range(ds, n)))
    nf = math.sqrt(sum(abs(psi_f[i]) ** 2 for i in range(ds, n)))
    if n0 > 0 and nf > 0:
        ov = sum(psi_0[i].conjugate() / n0 * psi_f[i] / nf for i in range(ds, n))
        return math.atan2(ov.imag, ov.real)
    return 0.0


def main():
    print("=" * 70)
    print("RETARDATION DISCRIMINATOR: FULL RETAINED HARNESS")
    print(f"delay={DELAY}, A={A_OSC}, s={S}, z0={Z0}")
    print("=" * 70)

    pos, adj, nmap = grow(0, 0.2, 0.7)

    # 1. Frequency sweep
    print("\n1. FREQUENCY SWEEP (inst vs retarded)")
    inst_curve = []
    ret_curve = []
    print(f"{'freq':>6s} {'inst':>10s} {'ret':>10s} {'diff':>10s}")
    print("-" * 40)
    for f in FREQS:
        pi = _phase(pos, adj, nmap, f, 0)
        pr = _phase(pos, adj, nmap, f, DELAY)
        inst_curve.append(pi)
        ret_curve.append(pr)
        print(f"{f:6.3f} {pi:+10.6f} {pr:+10.6f} {pr - pi:+10.6f}")

    # 2. Exact nulls
    print("\n2. EXACT NULLS")
    print(f"  f=0, d=0: {_phase(pos, adj, nmap, 0.0, 0):+.6e}")
    print(f"  f=0, d={DELAY}: {_phase(pos, adj, nmap, 0.0, DELAY):+.6e}")

    # 3. Delay law at f=0.15
    print(f"\n3. DELAY LAW at f=0.15")
    for d in [0, 1, 2, 3, 5, 7, 10]:
        pi = _phase(pos, adj, nmap, 0.15, 0)
        pr = _phase(pos, adj, nmap, 0.15, d)
        split = "SPLIT" if pi < 0 and pr > 0 else ""
        print(f"  d={d:2d}: inst={pi:+.6f}, ret={pr:+.6f}, diff={pr - pi:+.6f} {split}")

    # 4. Global-delay fit test
    print(f"\n4. GLOBAL-DELAY FIT TEST")
    best_tau = None
    best_rms = 1e10
    for tau in range(-5, 6):
        shifted = []
        for f in FREQS:
            shifted.append(_phase(pos, adj, nmap, f, 0, 2 * math.pi * f * tau * H))
        rms = math.sqrt(sum((r - s) ** 2 for r, s in zip(ret_curve, shifted)) / len(FREQS))
        if rms < best_rms:
            best_rms = rms
            best_tau = tau
    rms_ret = math.sqrt(sum(r ** 2 for r in ret_curve) / len(FREQS))
    print(f"  best tau = {best_tau}, residual/RMS = {best_rms / rms_ret:.4f}")
    if best_rms / rms_ret > 0.5:
        print(f"  FIT FAILS — different transfer function (not just a delay)")
    else:
        print(f"  fit works — retardation is a global delay")

    # 5. Family portability of difference curve
    print(f"\n5. FAMILY PORTABILITY (difference at f=0.15, d={DELAY})")
    for label, drift, restore in FAMILIES:
        diffs = []
        for seed in [0, 1]:
            p, a, nm = grow(seed, drift, restore)
            pi = _phase(p, a, nm, 0.15, 0)
            pr = _phase(p, a, nm, 0.15, DELAY)
            diffs.append(pr - pi)
        print(f"  {label}: diff = {sum(diffs) / len(diffs):+.6f}")

    # 6. Seed robustness
    print(f"\n6. SEED ROBUSTNESS (f=0.15, d={DELAY})")
    for seed in range(4):
        p, a, nm = grow(seed, 0.2, 0.7)
        pi = _phase(p, a, nm, 0.15, 0)
        pr = _phase(p, a, nm, 0.15, DELAY)
        print(f"  seed {seed}: diff = {pr - pi:+.6f}")


if __name__ == "__main__":
    main()
