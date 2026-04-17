#!/usr/bin/env python3
"""Test potential fixes for 3D gravity collapse under refinement.

Fix 1: Power action S = L|f|^0.5 (different phase accumulation scaling)
Fix 2: Tapered lattice (dense center, sparse edges)
Fix 3: 1/L^2 kernel in 3D (stronger beam confinement)

All tested at h=1.0 and h=0.5 to check refinement survival.
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
PHYS_W = 6
MAX_D = 3


def generate_dense(phys_l, h=1.0):
    """Standard dense 3D lattice."""
    nl = int(phys_l / h) + 1
    hw = int(PHYS_W / h)
    max_d = max(1, round(MAX_D / h))
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = len(pos)
                pos.append((x, iy * h, iz * h))
                nmap[(layer, iy, iz)] = idx
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                for diy in range(-max_d, max_d + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-max_d, max_d + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def generate_tapered(phys_l, h=1.0):
    """Tapered 3D lattice: dense near center, sparse at edges.

    |y| < 2 and |z| < 2: max_d = 3 (49 edges)
    2 <= |y| < 4 or 2 <= |z| < 4: max_d = 2 (25 edges)
    |y| >= 4 or |z| >= 4: max_d = 1 (9 edges)
    """
    nl = int(phys_l / h) + 1
    hw = int(PHYS_W / h)
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = len(pos)
                pos.append((x, iy * h, iz * h))
                nmap[(layer, iy, iz)] = idx

    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                # Physical position determines taper
                y_phys = abs(iy * h)
                z_phys = abs(iz * h)
                r_phys = max(y_phys, z_phys)
                if r_phys < 2:
                    md = max(1, round(3 / h))
                elif r_phys < 4:
                    md = max(1, round(2 / h))
                else:
                    md = max(1, round(1 / h))

                for diy in range(-md, md + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-md, md + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def propagate_spent_delay(pos, adj, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, p in enumerate(pos)
               if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10 and abs(p[2]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pi, pj = pos[i], pos[j]
            dx, dy, dz = pj[0]-pi[0], pj[1]-pi[1], pj[2]-pi[2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def propagate_power(pos, adj, field, k, blocked, n, p=0.5):
    """Power action: S = L * |f|^p."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, pp in enumerate(pos)
               if abs(pp[0]) < 1e-10 and abs(pp[1]) < 1e-10 and abs(pp[2]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pi, pj = pos[i], pos[j]
            dx, dy, dz = pj[0]-pi[0], pj[1]-pi[1], pj[2]-pi[2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = abs(0.5 * (field[i] + field[j]))
            act = L * (lf ** p) if lf > 1e-20 else 0.0
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def propagate_l2_kernel(pos, adj, field, k, blocked, n):
    """1/L^2 kernel for stronger beam confinement in 3D."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, p in enumerate(pos)
               if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10 and abs(p[2]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pi, pj = pos[i], pos[j]
            dx, dy, dz = pj[0]-pi[0], pj[1]-pi[1], pj[2]-pi[2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / (L * L)
    return amps


def test_gravity(pos, adj, nmap, nl, hw, n, h, strength, propagator, b_values):
    det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
           for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    bi = []
    for iy in range(-hw, hw+1):
        for iz in range(-hw, hw+1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)

    field_f = [0.0] * n
    af = propagator(pos, adj, field_f, K, blocked, n)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    results = []
    for b in b_values:
        iz_mass = round(b / h)
        mi = nmap.get((gl, 0, iz_mass))
        if mi is None:
            continue
        field = [0.0] * n
        mx, my, mz = pos[mi]
        for i in range(n):
            pi = pos[i]
            r = math.sqrt((pi[0]-mx)**2 + (pi[1]-my)**2 + (pi[2]-mz)**2) + 0.1
            field[i] = strength / r
        am = propagator(pos, adj, field, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            results.append((b, delta, "TOWARD" if delta > 0 else "AWAY"))

    return results


def run_test(name, gen_fn, prop_fn, phys_l, h_values, strengths, b_values):
    print(f"\n{name}")
    print("-" * 60)
    for h in h_values:
        pos, adj, nl, hw, nmap = gen_fn(phys_l, h)
        n = len(pos)
        edges = len(adj.get(nmap.get((1, 0, 0), 0), [])) if adj else 0
        print(f"  h={h}: {n} nodes, ~{edges} edges/center_node")
        for s in strengths:
            t0 = time.time()
            results = test_gravity(pos, adj, nmap, nl, hw, n, h, s, prop_fn, b_values)
            dt = time.time() - t0
            if results:
                n_tw = sum(1 for _, _, d in results if d == "TOWARD")
                r_str = " ".join(f"b={b}:{d:+.4f}({dr[0]})" for b, d, dr in results)
                print(f"    s={s:.0e}: {r_str} [{n_tw}/{len(results)}] ({dt:.0f}s)")
            else:
                print(f"    s={s:.0e}: FAIL ({dt:.0f}s)")


def main():
    print("=" * 80)
    print("3D GRAVITY FIXES: TESTING ALTERNATIVES")
    print("=" * 80)

    phys_l = 12
    b_values = [2, 3, 4, 5]
    strengths = [5e-5, 1e-5]
    h_values = [1.0, 0.5]

    # Control: dense lattice with spent-delay (known to fail at h=0.5)
    run_test("CONTROL: Dense + Spent-delay",
             generate_dense, propagate_spent_delay,
             phys_l, h_values, strengths, b_values)

    # Fix 1: Dense + Power action
    run_test("FIX 1: Dense + Power action (p=0.5)",
             generate_dense, propagate_power,
             phys_l, h_values, strengths, b_values)

    # Fix 2: Tapered lattice + Spent-delay
    run_test("FIX 2: Tapered + Spent-delay",
             generate_tapered, propagate_spent_delay,
             phys_l, h_values, strengths, b_values)

    # Fix 3: Dense + 1/L^2 kernel
    run_test("FIX 3: Dense + 1/L^2 kernel",
             generate_dense, propagate_l2_kernel,
             phys_l, h_values, strengths, b_values)

    # Fix 4: Tapered + Power action
    run_test("FIX 4: Tapered + Power action (p=0.5)",
             generate_tapered, propagate_power,
             phys_l, h_values, strengths, b_values)

    print()
    print("=" * 80)
    print("SUCCESS = TOWARD at BOTH h=1.0 AND h=0.5 (survives refinement)")
    print("=" * 80)


if __name__ == "__main__":
    main()
