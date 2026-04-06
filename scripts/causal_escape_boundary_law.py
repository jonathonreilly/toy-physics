#!/usr/bin/env python3
"""Causal-escape boundary law: eta_max(c) and s-dependence.

Executable replay harness. Reproduces:
  - eta_crit where inst escape = 0.5 (by bisection)
  - eta_max(c) where dyn escape drops to 0.85
  - s-dependence at anchor points
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
                    y = py + rng.gauss(0, 0.2 * H)
                    z = pz + rng.gauss(0, 0.2 * H)
                    y = y * 0.3 + (iy * H) * 0.7
                    z = z * 0.3 + (iz * H) * 0.7
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


def _prop_trap(pos, adj, nmap, s, z_src, k, c_field, eta):
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

            def fld(idx):
                if c_field is None:
                    return s / (math.sqrt((pos[idx][0] - mx) ** 2 + (pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2) + 0.1)
                x_n = pos[idx][0]
                if x_n < x_src - 0.01:
                    return 0.0
                dt = abs(x_n - x_src) / H
                reach = c_field * dt * H + 0.1
                r_t = math.sqrt((pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2)
                if r_t > reach:
                    return 0.0
                return s / (math.sqrt((pos[idx][0] - mx) ** 2 + (pos[idx][1] - my) ** 2 + (pos[idx][2] - mz) ** 2) + 0.1)

            lf = 0.5 * (fld(i) + fld(j))
            phase = k * L * (1.0 - lf)
            trap = math.exp(-eta * lf) if eta > 0 else 1.0
            theta = math.atan2(math.sqrt(dy_e * dy_e + dz_e * dz_e), max(dx_e, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * trap * w * h2 / (L * L)
    return amps


def _esc(pos, adj, nmap, s, z_src, k, cf, eta):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    a = _prop_trap(pos, adj, nmap, s, z_src, k, cf, eta)
    a0 = _prop_trap(pos, adj, nmap, s, z_src, k, cf, 0.0)
    t = sum(abs(a[i]) ** 2 for i in range(ds, n))
    t0 = sum(abs(a0[i]) ** 2 for i in range(ds, n))
    return t / t0 if t0 > 0 else 0


def main():
    pos, adj, nmap = grow(0)

    print("CAUSAL-ESCAPE BOUNDARY LAW")
    print()

    # Find inst trap threshold
    lo, hi = 1.0, 100.0
    for _ in range(20):
        mid = (lo + hi) / 2
        ei = _esc(pos, adj, nmap, S, MASS_Z, K, None, mid)
        if ei > 0.5:
            lo = mid
        else:
            hi = mid
    eta_crit = (lo + hi) / 2
    print(f"Inst trap threshold: eta_crit = {eta_crit:.1f}")

    # eta_max(c) where dyn drops to 0.85
    print(f"\nBoundary law: eta_max(c)")
    for c in [2.0, 1.0, 0.5, 0.25, 0.1]:
        lo, hi = 1.0, 500.0
        for _ in range(25):
            mid = (lo + hi) / 2
            ed = _esc(pos, adj, nmap, S, MASS_Z, K, c, mid)
            if ed > 0.85:
                lo = mid
            else:
                hi = mid
        print(f"  c={c}: eta_max = {(lo + hi) / 2:.1f}")

    # s-dependence
    print(f"\nS-dependence (eta=20, c=0.25)")
    for s in [0.001, 0.004, 0.016]:
        ei = _esc(pos, adj, nmap, s, MASS_Z, K, None, 20)
        ed = _esc(pos, adj, nmap, s, MASS_Z, K, 0.25, 20)
        print(f"  s={s:.3f}: inst={ei:.4f}, dyn={ed:.4f}, ratio={ed / ei:.2f}" if ei > 0 else f"  s={s:.3f}: inst=0")


if __name__ == "__main__":
    main()
