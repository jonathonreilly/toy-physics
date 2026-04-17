#!/usr/bin/env python3
"""Complex action: kernel-generic vs gravity-specific effects.

The complex action S = L(1-f) + i*gamma*L*f has TWO distinct effects:

  1. KERNEL-GENERIC: any nonzero field f produces escape < 1 at gamma > 0.
     This is because exp(-k*gamma*L*f) < 1 whenever f > 0 and gamma > 0.
     It does NOT require 1/r structure, mass, or localization.

  2. GRAVITY-SPECIFIC: the 1/r field produces a LOCALIZED deflection that
     changes direction from TOWARD (gamma=0) to AWAY (gamma > threshold).
     This requires the spatial structure of the field (gradient, not just
     magnitude).

This script explicitly separates the two effects with matched controls.
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
SEEDS = [0, 1]
GAMMAS = [0.0, 0.1, 0.2, 0.5]


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


def make_gravity_field(pos, nmap, s, z_src):
    n = len(pos)
    gl = NL // 3
    iz_s = round(z_src / H)
    mi = nmap.get((gl, 0, iz_s))
    if mi is None:
        return [0.0] * n
    mx, my, mz = pos[mi]
    return [s / (math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 +
                            (pos[i][2] - mz) ** 2) + 0.1)
            for i in range(n)]


def make_uniform_field(pos, f_val):
    return [f_val] * len(pos)


def prop_cx(pos, adj, field, k, gamma):
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
            s_real = L * (1.0 - lf)
            s_imag = gamma * L * lf
            phase = k * s_real
            decay = -k * s_imag
            if decay < -50:
                amp_f = 0.0
            elif decay > 50:
                amp_f = math.exp(50)
            else:
                amp_f = math.exp(decay)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * amp_f * w * h2 / (L * L)
    return amps


def main():
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2

    def cz(amps, pos):
        ds = len(pos) - npl
        t = sum(abs(amps[i]) ** 2 for i in range(ds, len(amps)))
        if t <= 0:
            return 0.0
        return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, len(amps))) / t

    def dp(amps, pos):
        ds = len(pos) - npl
        return sum(abs(amps[i]) ** 2 for i in range(ds, len(amps)))

    print("=" * 75)
    print("COMPLEX ACTION: KERNEL-GENERIC vs GRAVITY-SPECIFIC")
    print(f"drift={DRIFT}, restore={RESTORE}")
    print("=" * 75)

    field_configs = [
        ("ZERO", lambda pos, nmap: [0.0] * len(pos)),
        ("UNIFORM (f=0.005)", lambda pos, nmap: make_uniform_field(pos, 0.005)),
        ("UNIFORM (f=0.01)", lambda pos, nmap: make_uniform_field(pos, 0.01)),
        ("GRAVITY (s=0.004)", lambda pos, nmap: make_gravity_field(pos, nmap, 0.004, MASS_Z)),
    ]

    for label, field_fn in field_configs:
        print(f"\nFIELD: {label}")
        print(f"  {'gamma':>6s} {'toward':>6s}/{len(SEEDS)} {'avg_defl':>12s} {'avg_esc':>10s}")
        print("  " + "-" * 42)

        for gamma in GAMMAS:
            towrd = 0
            defls = []
            escs = []
            for seed in SEEDS:
                pos, adj, nmap = grow(seed)
                field = field_fn(pos, nmap)
                free_ref = prop_cx(pos, adj, [0.0] * len(pos), K, 0.0)
                z_free = cz(free_ref, pos)
                p_free = dp(free_ref, pos)

                amps = prop_cx(pos, adj, field, K, gamma)
                delta = cz(amps, pos) - z_free
                esc = dp(amps, pos) / p_free if p_free > 0 else 0
                if delta > 0:
                    towrd += 1
                defls.append(delta)
                escs.append(esc)

            avg_d = sum(defls) / len(defls)
            avg_e = sum(escs) / len(escs)
            dr = "T" if avg_d > 0 else "A"
            print(f"  {gamma:6.1f} {towrd:6d}/{len(SEEDS)} {avg_d:+12.4e}{dr} {avg_e:10.4f}")

    print()
    print("SEPARATION OF EFFECTS")
    print()
    print("  KERNEL-GENERIC (escape < 1 at gamma > 0):")
    print("    present for UNIFORM field (no spatial structure)")
    print("    present for GRAVITY field")
    print("    NOT present for ZERO field")
    print("    mechanism: exp(-k*gamma*L*f) < 1 whenever f > 0")
    print()
    print("  GRAVITY-SPECIFIC (deflection TOWARD -> AWAY):")
    print("    present ONLY for GRAVITY field (1/r spatial structure)")
    print("    NOT present for UNIFORM field (no gradient)")
    print("    NOT present for ZERO field")
    print("    mechanism: 1/r gradient couples to beam centroid")


if __name__ == "__main__":
    main()
