#!/usr/bin/env python3
"""Quick check: does 2D TOWARD survive refinement where 3D doesn't?

Compare 2D dense and 3D dense at h=1.0 vs h=0.5.
If 2D converges but 3D doesn't, the dimensionality is the issue.
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0


def generate_2d(phys_l, phys_w, max_d_phys, h=1.0):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    max_d = max(1, round(max_d_phys / h))
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            idx = len(pos)
            pos.append((x, iy * h))
            nmap[(layer, iy)] = idx
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for dy in range(-max_d, max_d + 1):
                iyn = iy + dy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def generate_3d(phys_l, phys_w, max_d_phys, h=1.0):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    max_d = max(1, round(max_d_phys / h))
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


def propagate_2d(pos, adj, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, p in enumerate(pos) if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def propagate_3d(pos, adj, field, k, blocked, n):
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
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dz = pj[2] - pi[2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def test_gravity_2d(phys_l, phys_w, max_d_phys, h, strength, b_values):
    pos, adj, nl, hw, nmap = generate_2d(phys_l, phys_w, max_d_phys, h)
    n = len(pos)
    det = [nmap[(nl-1, iy)] for iy in range(-hw, hw+1) if (nl-1, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    # Slits
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw+1) if (bl, iy) in nmap]
    slit_iy = max(1, round(3.0 / h))
    sa = [nmap[(bl, iy)] for iy in range(slit_iy, hw+1) if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in range(-hw, -slit_iy+1) if (bl, iy) in nmap]
    blocked = set(bi) - set(sa + sb)

    field_f = [0.0] * n
    af = propagate_2d(pos, adj, field_f, K, blocked, n)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    yf = sum(abs(af[d])**2 * pos[d][1] for d in det) / pf

    results = []
    for b in b_values:
        iy_mass = round(b / h)
        mi = nmap.get((gl, iy_mass))
        if mi is None:
            continue
        field = [0.0] * n
        mx, my = pos[mi]
        for i in range(n):
            r = math.sqrt((pos[i][0]-mx)**2 + (pos[i][1]-my)**2) + 0.1
            field[i] = strength / r
        am = propagate_2d(pos, adj, field, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            ym = sum(abs(am[d])**2 * pos[d][1] for d in det) / pm
            delta = ym - yf
            results.append((b, delta, "TOWARD" if delta > 0 else "AWAY"))

    return results


def test_gravity_3d(phys_l, phys_w, max_d_phys, h, strength, b_values):
    pos, adj, nl, hw, nmap = generate_3d(phys_l, phys_w, max_d_phys, h)
    n = len(pos)
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
    af = propagate_3d(pos, adj, field_f, K, blocked, n)
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
        am = propagate_3d(pos, adj, field, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            results.append((b, delta, "TOWARD" if delta > 0 else "AWAY"))

    return results


def main():
    print("=" * 80)
    print("2D vs 3D CONTINUUM CONVERGENCE: GRAVITY TOWARD/AWAY")
    print("=" * 80)
    print()

    strengths = [5e-5, 1e-5, 5e-6]
    b_values = [4, 6, 8, 10]

    # --- 2D Dense lattice ---
    print("2D DENSE LATTICE (max_d_phys=5, W=20, L=40)")
    print("-" * 60)
    for h in [1.0, 0.5]:
        t0 = time.time()
        for s in strengths:
            results = test_gravity_2d(40, 20, 5, h, s, b_values)
            if results:
                n_tw = sum(1 for _, _, d in results if d == "TOWARD")
                r_str = " ".join(f"b={b}:{d:+.4f}({dr[0]})" for b, d, dr in results)
                print(f"  h={h}, s={s:.0e}: {r_str}  [{n_tw}/{len(results)} TOWARD]")
            else:
                print(f"  h={h}, s={s:.0e}: FAIL")
        dt = time.time() - t0
        print(f"  ({dt:.0f}s)")
        print()

    # --- 3D Dense lattice ---
    print("3D DENSE LATTICE (max_d_phys=3, W=6, L=12)")
    print("-" * 60)
    b_3d = [2, 3, 4, 5]
    for h in [1.0, 0.5]:
        t0 = time.time()
        for s in strengths:
            results = test_gravity_3d(12, 6, 3, h, s, b_3d)
            if results:
                n_tw = sum(1 for _, _, d in results if d == "TOWARD")
                r_str = " ".join(f"b={b}:{d:+.4f}({dr[0]})" for b, d, dr in results)
                print(f"  h={h}, s={s:.0e}: {r_str}  [{n_tw}/{len(results)} TOWARD]")
            else:
                print(f"  h={h}, s={s:.0e}: FAIL")
        dt = time.time() - t0
        print(f"  ({dt:.0f}s)")
        print()

    # --- 3D with h-scaled field ---
    print("3D DENSE with RG SCALING s_eff = s0 * h (keep total phase constant)")
    print("-" * 60)
    s0 = 5e-5
    for h in [1.0, 0.5]:
        t0 = time.time()
        s_eff = s0 * h
        results = test_gravity_3d(12, 6, 3, h, s_eff, b_3d)
        if results:
            n_tw = sum(1 for _, _, d in results if d == "TOWARD")
            r_str = " ".join(f"b={b}:{d:+.4f}({dr[0]})" for b, d, dr in results)
            print(f"  h={h}, s_eff={s_eff:.0e}: {r_str}  [{n_tw}/{len(results)} TOWARD]")
        else:
            print(f"  h={h}, s_eff={s_eff:.0e}: FAIL")
        dt = time.time() - t0
        print(f"  ({dt:.0f}s)")
        print()

    print("=" * 80)
    print("VERDICT: If 2D TOWARD survives h=0.5 but 3D doesn't →")
    print("  dimensionality (beam spreading in 2 transverse dimensions) is the issue")
    print("=" * 80)


if __name__ == "__main__":
    main()
