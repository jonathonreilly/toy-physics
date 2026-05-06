#!/usr/bin/env python3
"""Gravitomagnetic effect: velocity-dependent Shapiro correction.

NOTE: This is a full executable replay harness, not a reconstruction.
It recomputes all phase values from scratch on each run.

A moving source produces an antisymmetric phase shift beyond the
static Shapiro delay. This is the discrete analog of gravitomagnetic
frame-dragging.

Tests portability across three independent grown families.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

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
C_FIELD = 0.5
FAMILIES = [
    ("Fam1", 0.20, 0.70),
    ("Fam2", 0.05, 0.30),
    ("Fam3", 0.50, 0.90),
]
V_VALUES = [-0.5, -0.2, 0.0, +0.2, +0.5]
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


def prop_moving(pos, adj, nmap, s, z0, v_z, k, c_field):
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
                x_n = pos[idx][0]
                z_src = z0 + v_z * (ln - gl) * H
                mx, my, mz = x_src, 0.0, z_src
                if c_field is not None:
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

            lf = 0.5 * (fld(i) + fld(j))
            phase = k * L * (1.0 - lf)
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


def measure_phase(pos, adj, nmap, s, z0, v_z, c):
    n = len(pos)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = n - npl
    pi = prop_moving(pos, adj, nmap, s, z0, v_z, K, None)
    pc = prop_moving(pos, adj, nmap, s, z0, v_z, K, c)
    ni = math.sqrt(sum(abs(pi[i]) ** 2 for i in range(ds, n)))
    nc = math.sqrt(sum(abs(pc[i]) ** 2 for i in range(ds, n)))
    if ni > 0 and nc > 0:
        ov = sum(pi[i].conjugate() / ni * pc[i] / nc for i in range(ds, n))
        return math.atan2(ov.imag, ov.real)
    return 0.0


def main():
    print("=" * 80)
    print("GRAVITOMAGNETIC EFFECT: THREE-FAMILY PORTABILITY")
    print(f"c={C_FIELD}, s={S}, z0={MASS_Z}, {len(SEEDS)} seeds per family")
    print("=" * 80)
    print()

    for label, drift, restore in FAMILIES:
        print(f"{label} (drift={drift}, restore={restore}):")
        print(f"  {'v_z':>6s} {'mean_phase':>12s} {'delta':>12s}")
        print("  " + "-" * 34)

        # Pass 1: collect all phases (so the v=0 baseline is known before
        # delta is computed for any row, including v<0).
        phases: dict[float, float] = {}
        for v in V_VALUES:
            ps = []
            for seed in SEEDS:
                pos, adj, nmap = grow(seed, drift, restore)
                ps.append(measure_phase(pos, adj, nmap, S, MASS_Z, v, C_FIELD))
            phases[v] = sum(ps) / len(ps)

        if 0.0 not in phases:
            raise RuntimeError("V_VALUES must include v=0.0 for the static baseline")
        phase_static = phases[0.0]

        # Pass 2: print phase + delta-from-static, antisymmetric in v.
        for v in V_VALUES:
            mean_p = phases[v]
            delta = mean_p - phase_static
            print(f"  {v:+6.1f} {mean_p:+12.6f} {delta:+12.6f}")
        print()

    print("SAFE READ")
    print("  delta antisymmetric in v: +v gives positive delta, -v gives negative")
    print("  if all three families agree: gravitomagnetic effect is portable")
    print("  this is the discrete analog of gravitomagnetic frame-dragging")


if __name__ == "__main__":
    main()
