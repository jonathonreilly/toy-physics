#!/usr/bin/env python3
"""2D dense lattice: does the distance law converge under refinement?

The 2D gravity (TOWARD) survives h=0.5. Does the distance exponent
also converge? Test at h=1.0, 0.5, 0.25.

From the resolution note: at h=1.0 with s=0.0005, the fit was
b^(-0.94) over b=6..19. The expected Newtonian law in 2+1D is 1/b
(since gravity ∝ 1/r^(d-1) in d spatial dimensions, and this is a
2D spatial lattice → 1/r^1 = 1/b).
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0


def generate(phys_l, phys_w, max_d_phys, h=1.0):
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


def propagate(pos, adj, field, k, blocked, n):
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


def measure_distance(phys_l, phys_w, max_d_phys, h, strength, b_values):
    pos, adj, nl, hw, nmap = generate(phys_l, phys_w, max_d_phys, h)
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
    af = propagate(pos, adj, field_f, K, blocked, n)
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
        am = propagate(pos, adj, field, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            ym = sum(abs(am[d])**2 * pos[d][1] for d in det) / pm
            delta = ym - yf
            results.append((b, delta))

    return results


def fit_power_law(bvals, dvals):
    """Fit delta = A * b^slope to positive values only."""
    pos_b = [b for b, d in zip(bvals, dvals) if d > 0]
    pos_d = [d for d in dvals if d > 0]
    if len(pos_b) < 3:
        return None, None
    lx = [math.log(b) for b in pos_b]
    ly = [math.log(d) for d in pos_d]
    nn = len(lx)
    mx = sum(lx) / nn
    my = sum(ly) / nn
    sxx = sum((x - mx)**2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = sum((y - (my + slope * (x - mx)))**2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my)**2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def main():
    print("=" * 80)
    print("2D DENSE LATTICE: DISTANCE LAW CONVERGENCE")
    print("  Does the exponent converge to -1.0 (2+1D Newtonian) as h → 0?")
    print("=" * 80)
    print()

    phys_l = 40
    phys_w = 20
    max_d_phys = 5
    strength = 0.0005  # Same as resolution note

    b_values = [4, 5, 6, 7, 8, 10, 13, 16, 19]

    for h in [1.0, 0.5, 0.25]:
        t0 = time.time()
        print(f"h = {h}:")
        pos, adj, nl, hw, nmap = generate(phys_l, phys_w, max_d_phys, h)
        n = len(pos)
        edges = len(adj.get(0, [])) if adj else 0
        print(f"  Lattice: {n} nodes, {nl} layers, {2*hw+1} nodes/layer, "
              f"~{edges} edges/node")

        results = measure_distance(phys_l, phys_w, max_d_phys, h, strength, b_values)
        dt = time.time() - t0

        if results:
            print(f"  Results:")
            for b, delta in results:
                dr = "TOWARD" if delta > 0 else "AWAY"
                print(f"    b={b:2d}: delta={delta:+.4f} ({dr})")

            # Fit to decreasing part (after peak)
            peak_idx = 0
            for i, (b, d) in enumerate(results):
                if d > 0 and (peak_idx == 0 or d > results[peak_idx][1]):
                    peak_idx = i

            # Fit all positive values after (and including) peak
            fit_b = [b for b, d in results[peak_idx:] if d > 0]
            fit_d = [d for b, d in results[peak_idx:] if d > 0]

            if len(fit_b) >= 3:
                slope, r2 = fit_power_law(fit_b, fit_d)
                if slope is not None:
                    print(f"  Distance law (b>={results[peak_idx][0]}): "
                          f"b^({slope:.2f}), R²={r2:.3f}")

            # Also fit ALL positive values
            all_b = [b for b, d in results if d > 0]
            all_d = [d for b, d in results if d > 0]
            if len(all_b) >= 3:
                slope2, r22 = fit_power_law(all_b, all_d)
                if slope2 is not None:
                    print(f"  Distance law (all TOWARD): "
                          f"b^({slope2:.2f}), R²={r22:.3f}")

            n_tw = sum(1 for _, d in results if d > 0)
            print(f"  TOWARD: {n_tw}/{len(results)}")
        else:
            print(f"  FAIL")

        print(f"  ({dt:.0f}s)")
        print()

    # Also test weaker field to see if it helps
    print("\n--- Weaker field (s=5e-5) ---")
    for h in [1.0, 0.5]:
        t0 = time.time()
        results = measure_distance(phys_l, phys_w, max_d_phys, h, 5e-5, b_values)
        dt = time.time() - t0
        if results:
            n_tw = sum(1 for _, d in results if d > 0)
            fit_b = [b for b, d in results if d > 0]
            fit_d = [d for b, d in results if d > 0]
            slope, r2 = fit_power_law(fit_b, fit_d) if len(fit_b) >= 3 else (None, None)
            s_str = f"exp={slope:.2f}, R²={r2:.3f}" if slope else "too few"
            res_str = " ".join(f"{b}:{d:+.4f}" for b, d in results)
            print(f"  h={h}: {n_tw}/{len(results)} TOWARD, {s_str}")
            print(f"    {res_str}")
        print(f"  ({dt:.0f}s)")
        print()


if __name__ == "__main__":
    main()
