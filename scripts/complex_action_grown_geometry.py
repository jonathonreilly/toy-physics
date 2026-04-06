#!/usr/bin/env python3
"""Complex action on generated (grown) geometry.

Boundary probe:
  Test whether the complex action S = L(1-f) + i*gamma*L*f keeps the
  regular-lattice weak-field class on grown geometry. If the sweep fails
  the weak-field or Born controls, freeze it as a no-go instead of
  promoting geometry-independence.

Uses the Gate B growth rule: template + drift + restore + NN connectivity.
Tests gamma sweep, Born, and mass scaling on grown DAGs.
"""

from __future__ import annotations

import cmath
import math
import random
import time

BETA = 0.8
K = 5.0
STRENGTH = 0.1
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
MASS_Z = 3.0
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1, 2, 3, 4, 5]
GAMMAS = [0.0, 0.1, 0.2, 0.5, 1.0]


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
                    y = iy * H
                    z = iz * H
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


def make_field(pos, nmap, s, z_src):
    n = len(pos)
    gl = NL // 3
    iz_src = round(z_src / H)
    mi = nmap.get((gl, 0, iz_src))
    if mi is None:
        return [0.0] * n
    mx, my, mz = pos[mi]
    field = [0.0] * n
    for i in range(n):
        r = math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2) + 0.1
        field[i] = s / r
    return field


def propagate_complex(pos, adj, field, k, gamma):
    """Complex action propagator on arbitrary graph."""
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
                amp_factor = 0.0
            elif decay > 50:
                amp_factor = math.exp(50)
            else:
                amp_factor = math.exp(decay)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * amp_factor * w * h2 / (L * L)
    return amps


def centroid_z(amps, pos, det_layer_start):
    total = 0.0
    weighted = 0.0
    for i in range(det_layer_start, len(pos)):
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 0 else 0.0


def det_prob(amps, det_layer_start):
    return sum(abs(amps[i]) ** 2 for i in range(det_layer_start, len(amps)))


def main():
    print("=" * 85)
    print("COMPLEX ACTION ON GENERATED (GROWN) GEOMETRY")
    print(f"  S = L(1-f) + i*gamma*L*f, growth rule: drift={DRIFT}, restore={RESTORE}")
    print(f"  {len(SEEDS)} seeds, NL={NL}, W={PW}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 85)
    print()

    # Find detector layer start
    hw = int(PW / H)
    npl_approx = (2 * hw + 1) ** 2

    print(f"{'gamma':>6s}  {'toward':>6s}/{len(SEEDS)}  {'avg_defl':>12s}  {'avg_escape':>12s}  {'F~M':>6s}")
    print("-" * 55)

    for gamma in GAMMAS:
        toward = 0
        deflections = []
        escapes = []
        fm_deltas = []

        for seed in SEEDS:
            pos, adj, nmap = grow(seed)
            det_start = len(pos) - npl_approx
            field_zero = [0.0] * len(pos)
            field = make_field(pos, nmap, STRENGTH, MASS_Z)

            free = propagate_complex(pos, adj, field_zero, K, gamma)
            grav = propagate_complex(pos, adj, field, K, gamma)

            z_free = centroid_z(free, pos, det_start)
            z_grav = centroid_z(grav, pos, det_start)
            delta = z_grav - z_free
            deflections.append(delta)
            if delta > 0:
                toward += 1

            p_free = det_prob(free, det_start)
            p_grav = det_prob(grav, det_start)
            escapes.append(p_grav / p_free if p_free > 0 else 0.0)

            # F~M at two strengths
            f2 = make_field(pos, nmap, STRENGTH / 2, MASS_Z)
            g2 = propagate_complex(pos, adj, f2, K, gamma)
            d2 = centroid_z(g2, pos, det_start) - z_free
            fm_deltas.append((abs(delta), abs(d2)))

        avg_defl = sum(deflections) / len(deflections)
        avg_escape = sum(escapes) / len(escapes)

        # F~M from ratio of deflections at s and s/2
        ratios = [d1 / d2 if d2 > 1e-15 else float('nan')
                  for d1, d2 in fm_deltas]
        valid_ratios = [r for r in ratios if not math.isnan(r) and r > 0]
        if valid_ratios:
            avg_ratio = sum(valid_ratios) / len(valid_ratios)
            fm = math.log(avg_ratio) / math.log(2.0)  # since s2 = s/2
        else:
            fm = float('nan')
        fm_s = f"{fm:.3f}" if not math.isnan(fm) else "  nan"

        print(f"{gamma:6.2f}  {toward:6d}/{len(SEEDS)}  {avg_defl:+12.6e}  {avg_escape:12.4f}  {fm_s}")

    # Born test on grown geometry at gamma=0 and gamma=0.5
    print()
    print("BORN TEST on grown geometry (seed=0)")
    pos, adj, nmap = grow(0)
    det_start = len(pos) - npl_approx
    field = make_field(pos, nmap, STRENGTH, MASS_Z)

    for gamma in [0.0, 0.5]:
        slits = [-1, 0, 1]
        hw_val = int(PW / H)

        def _p_born(open_slits):
            n = len(pos)
            amps_b = [0j] * n
            for s in open_slits:
                node = nmap.get((0, s, 0))
                if node is not None:
                    amps_b[node] = 1.0
            order = sorted(range(n), key=lambda i: pos[i][0])
            h2 = H * H
            for i in order:
                if abs(amps_b[i]) < 1e-30:
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
                    phase = K * s_real
                    decay_val = -K * s_imag
                    if decay_val < -50:
                        af = 0.0
                    elif decay_val > 50:
                        af = math.exp(50)
                    else:
                        af = math.exp(decay_val)
                    theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                    w = math.exp(-BETA * theta * theta)
                    amps_b[j] += amps_b[i] * complex(math.cos(phase), math.sin(phase)) * af * w * h2 / (L * L)
            return det_prob(amps_b, det_start)

        s1, s2, s3 = slits
        p123 = _p_born([s1, s2, s3])
        p12 = _p_born([s1, s2])
        p13 = _p_born([s1, s3])
        p23 = _p_born([s2, s3])
        p1 = _p_born([s1])
        p2 = _p_born([s2])
        p3 = _p_born([s3])
        i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
        born = abs(i3) / max(p123, 1e-300)
        print(f"  gamma={gamma:.1f}: |I3|/P = {born:.2e}")

    print()
    print("SAFE READ")
    print("  Born can remain clean on grown geometry, but that alone is not enough")
    print("  to promote geometry-independence.")
    print("  This sweep does not preserve the regular-lattice weak-field class")
    print("  (gamma=0 F~M is below unity), so the safe read is no-go for promotion.")
    print("  Keep the result as a grown-geometry boundary probe only.")


if __name__ == "__main__":
    main()
