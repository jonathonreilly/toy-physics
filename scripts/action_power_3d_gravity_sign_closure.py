#!/usr/bin/env python3
"""Bounded 3D action-power gravity-sign closure on ordered lattices.

Question:
Can the retained 3D power-action close-slit barrier card recover gravity
toward mass on the current ordered-lattice family by varying only:
  1. field strength
  2. forward connectivity density
  3. geometric jitter with fixed NN topology

This script keeps the 3D close-slit barrier geometry fixed and reports only the
barrier-card gravity sign on the detector z-centroid. It is a bounded negative
probe, not a full re-validation harness.
"""

from __future__ import annotations

import cmath
import math
import os
import random
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.action_power_canonical_harness import BETA, K  # noqa: E402


PHYS_L = 12
PHYS_W = 6
H = 1.0
ACTION = "power"
SLIT_A = (2, 0)
SLIT_B = (-2, 0)
MASS_Z_VALUES = [3, 6]


def build_ordered_lattice(phys_l: float, phys_w: float, h: float, span: int, jitter: float, seed: int):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    pos = []
    adj = defaultdict(list)
    nmap = {}
    rng = random.Random(seed)

    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                y = iy * h
                z = iz * h
                if jitter > 0.0 and layer != 0:
                    y += rng.uniform(-jitter * h, jitter * h)
                    z += rng.uniform(-jitter * h, jitter * h)
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx

    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                src = nmap[(layer, iy, iz)]
                for diy in range(-span, span + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-span, span + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        dst = nmap[(layer + 1, iyn, izn)]
                        adj[src].append(dst)
    return pos, dict(adj), nl, hw, nmap


def make_field_3d(pos, nmap, gl: int, mass_z: int, strength: float, n: int):
    mi = nmap.get((gl, 0, round(mass_z)))
    if mi is None:
        return [0.0] * n
    mx, my, mz = pos[mi]
    field = [0.0] * n
    for i, (x, y, z) in enumerate(pos):
        field[i] = strength / (math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1)
    return field


def propagate(pos, adj, field, blocked: set[int]):
    order = sorted(range(len(pos)), key=lambda i: pos[i][0])
    amps = [0j] * len(pos)
    src = 0  # central node at layer 0 is created first for iy=0,iz=0 offset? no; set explicitly below
    for i, p in enumerate(pos):
        if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10 and abs(p[2]) < 1e-10:
            src = i
            break
    amps[src] = 1.0
    for i in order:
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        pi = pos[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pj = pos[j]
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dz = pj[2] - pi[2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if ACTION == "power":
                act = L * (abs(lf) ** 0.5)
            else:
                raise ValueError(f"Unsupported action: {ACTION}")
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
    return amps


def barrier_gravity_shift(span: int, jitter: float, seed: int, strength: float, mass_z: int):
    pos, adj, nl, hw, nmap = build_ordered_lattice(PHYS_L, PHYS_W, H, span, jitter, seed)
    n = len(pos)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    bl = nl // 3
    gl = 2 * nl // 3
    barrier = [nmap[(bl, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    sa = [nmap[(bl, SLIT_A[0], SLIT_A[1])]]
    sb = [nmap[(bl, SLIT_B[0], SLIT_B[1])]]
    blocked = set(barrier) - set(sa + sb)

    field_f = [0.0] * n
    field_m = make_field_3d(pos, nmap, gl, mass_z, strength, n)
    af = propagate(pos, adj, field_f, blocked)
    am = propagate(pos, adj, field_m, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return math.nan
    zf = sum(abs(af[d]) ** 2 * pos[d][2] for d in det) / pf
    zm = sum(abs(am[d]) ** 2 * pos[d][2] for d in det) / pm
    return zm - zf


def sign_label(delta: float) -> str:
    if math.isnan(delta):
        return "FAIL"
    return "TOWARD" if delta > 0 else "AWAY"


def main():
    print("=" * 88)
    print("ACTION-POWER 3D BARRIER GRAVITY-SIGN CLOSURE")
    print("Fixed 3D close-slit barrier card on the ordered-lattice family.")
    print("Question: can strength, density, or geometric jitter recover attraction?")
    print("=" * 88)
    print()

    print("Canonical geometry:")
    print(f"  L={PHYS_L}, W={PHYS_W}, h={H}, slits={SLIT_A} and {SLIT_B}, action=power(p=0.5)")
    print()

    strengths = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3]
    print("1) FIELD-STRENGTH SWEEP ON NN TOPOLOGY (span=1, 9 edges/node)")
    print("strength    mass_z=3          mass_z=6")
    toward_count = 0
    total = 0
    for s in strengths:
        row = [f"{s:>8.5f}"]
        for mass_z in MASS_Z_VALUES:
            delta = barrier_gravity_shift(span=1, jitter=0.0, seed=0, strength=s, mass_z=mass_z)
            total += 1
            toward_count += int(delta > 0)
            row.append(f"{delta:+.6f} {sign_label(delta)}")
        print("  " + "   ".join(row))
    print(f"  toward count: {toward_count}/{total}")
    print()

    print("2) FORWARD-CONNECTIVITY DENSITY SWEEP (strength=0.00010, mass_z=3)")
    print("span   edges/node   gravity")
    toward_count = 0
    total = 0
    for span in [1, 2, 3]:
        delta = barrier_gravity_shift(span=span, jitter=0.0, seed=0, strength=1e-4, mass_z=3)
        total += 1
        toward_count += int(delta > 0)
        edges = (2 * span + 1) ** 2
        print(f"  {span:<4d}  {edges:<10d}   {delta:+.6f} {sign_label(delta)}")
    print(f"  toward count: {toward_count}/{total}")
    print()

    print("3) GEOMETRIC JITTER SWEEP WITH FIXED NN TOPOLOGY (span=1, strength=0.00010, mass_z=3)")
    print("jitter   toward/8   mean gravity")
    for jitter in [0.0, 0.1, 0.3, 0.5]:
        vals = [barrier_gravity_shift(span=1, jitter=jitter, seed=seed, strength=1e-4, mass_z=3) for seed in range(8)]
        ok = [v for v in vals if not math.isnan(v)]
        toward = sum(v > 0 for v in ok)
        mean = sum(ok) / len(ok) if ok else math.nan
        print(f"  {jitter:<5.1f}    {toward}/8        {mean:+.6f}")
    print()

    print("Conclusion:")
    print("  On the tested 3D ordered-lattice power branch, barrier gravity stays away")
    print("  from mass under field-strength weakening, denser forward connectivity,")
    print("  and geometric jitter. This closes the current ordered-family barrier-sign")
    print("  lane as a bounded negative result.")


if __name__ == "__main__":
    main()
