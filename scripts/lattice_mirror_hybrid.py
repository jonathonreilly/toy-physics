#!/usr/bin/env python3
"""Lattice-symmetry bridge probe on the ordered lattice family.

Combines:
  - Regular 2D lattice (integer grid) → beam confinement → 1/b
  - Z₂ mirror symmetry (explicit edge mirroring) → decoherence
  - Dense connectivity (max_dy=5, 11 edges/node) → attraction
  - Linear propagator → Born compliance

This script is an exploratory same-family two-harness bridge on the
standard-strength slice, not a promoted one-family unified architecture. On
that slice the unresolved blocker is the same-slit gravity-sign problem.

Bridge read: barrier coexistence card + no-barrier distance-law companion.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8


def generate_lattice_mirror_hybrid(n_layers, half_width, max_dy=5):
    """Dense Z₂-symmetric lattice.

    Nodes at integer (x, y). Edges to (x+1, y') with |y'-y| ≤ max_dy.
    The lattice is inherently Z₂ symmetric: every edge (x,y)→(x+1,y')
    has a mirror (x,-y)→(x+1,-y') because both node pairs exist on
    the integer grid.
    """
    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(n_layers):
        x = float(layer)
        for y in range(-half_width, half_width + 1):
            idx = len(pos)
            pos.append((x, float(y)))
            nmap[(layer, y)] = idx

    for layer in range(n_layers - 1):
        for y in range(-half_width, half_width + 1):
            si = nmap.get((layer, y))
            if si is None:
                continue
            for dy in range(-max_dy, max_dy + 1):
                yn = y + dy
                if abs(yn) > half_width:
                    continue
                di = nmap.get((layer + 1, yn))
                if di is not None:
                    adj[si].append(di)

    return pos, dict(adj), n_layers // 3, nmap


def propagate(pos, adj, field, src, k, blocked):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
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
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def main():
    NL = 40
    W = 20
    MAX_DY = 5

    pos, adj, bl, nmap = generate_lattice_mirror_hybrid(NL, W, MAX_DY)
    n = len(pos)
    det = [nmap[(NL-1, y)] for y in range(-W, W+1)]
    src = [nmap[(0, 0)]]
    gl = 2 * NL // 3

    # Barrier with slits at y = ±3,±4,±5 (symmetric)
    bi = [nmap[(bl, y)] for y in range(-W, W+1)]
    sa = [nmap[(bl, y)] for y in [3, 4, 5]]
    sb = [nmap[(bl, y)] for y in [-5, -4, -3]]
    blocked = set(bi) - set(sa + sb)

    print("=" * 80)
    print("LATTICE-SYMMETRY HYBRID: SAME-FAMILY TWO-HARNESS BRIDGE")
    print(f"  NL={NL}, W={W}, max_dy={MAX_DY} ({2*MAX_DY+1} edges/node)")
    print(f"  k={K}, slits at y=±3,±4,±5")
    print("=" * 80)
    print()

    # Mass at y=6 (just above slit, in the near-field attraction zone)
    mass_y = 6
    mass_idx = nmap[(gl, mass_y)]
    field_m = [0.0] * n
    mx, my = pos[mass_idx]
    for i in range(n):
        ix, iy = pos[i]
        field_m[i] = 0.1 / (math.sqrt((ix-mx)**2 + (iy-my)**2) + 0.1)
    field_f = [0.0] * n

    # 1. Gravity (centroid shift)
    am = propagate(pos, adj, field_m, src, K, blocked)
    af = propagate(pos, adj, field_f, src, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    pf = sum(abs(af[d])**2 for d in det)
    ym = sum(abs(am[d])**2 * pos[d][1] for d in det) / pm
    yf = sum(abs(af[d])**2 * pos[d][1] for d in det) / pf
    gravity = ym - yf
    print(f"  Gravity (b={mass_y}): {gravity:+.4f} ({'TOWARD' if gravity > 0 else 'AWAY'})")

    # 2. k=0 control
    am0 = propagate(pos, adj, field_m, src, 0.0, blocked)
    af0 = propagate(pos, adj, field_f, src, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det)
    pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = (sum(abs(am0[d])**2*pos[d][1] for d in det)/pm0
           - sum(abs(af0[d])**2*pos[d][1] for d in det)/pf0)
    print(f"  k=0 control: {gk0:+.6e}")

    # 3. CL decoherence (single-slit propagations)
    pa = propagate(pos, adj, field_m, src, K, blocked | set(sb))
    pb = propagate(pos, adj, field_m, src, K, blocked | set(sa))

    # MI
    bw = 2*(W+1) / N_YBINS
    prob_a = [0]*N_YBINS; prob_b = [0]*N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((pos[d][1]+W+1)/bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na = sum(prob_a); nb = sum(prob_b)
    if na > 1e-30 and nb > 1e-30:
        prob_a = [p/na for p in prob_a]; prob_b = [p/nb for p in prob_b]
        H = 0; Hc = 0
        for b2 in range(N_YBINS):
            pm2 = 0.5*prob_a[b2] + 0.5*prob_b[b2]
            if pm2 > 1e-30: H -= pm2 * math.log2(pm2)
            if prob_a[b2] > 1e-30: Hc -= 0.5*prob_a[b2]*math.log2(prob_a[b2])
            if prob_b[b2] > 1e-30: Hc -= 0.5*prob_b[b2]*math.log2(prob_b[b2])
        MI = H - Hc
        print(f"  MI: {MI:.4f} bits")

    # CL purity
    env_depth = max(1, round(NL/6))
    st = bl + 1; sp = min(NL-1, st + env_depth)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, y)] for y in range(-W, W+1)])
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS-1, int((pos[m][1]+W+1)/bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    NA = sum(abs(a)**2 for a in ba); NB = sum(abs(b)**2 for b in bb)
    Sn = S/(NA+NB) if (NA+NB) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2] + pb[d1].conjugate()*pb[d2]
                           + Dcl*pa[d1].conjugate()*pb[d2] + Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(d,d)] for d in det).real
    if tr > 1e-30:
        for key in rho: rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
        print(f"  pur_cl: {pur:.4f} (1-pur = {1-pur:.4f} = {(1-pur)*100:.1f}% decoherence)")

    # d_TV
    da = {d: abs(pa[d])**2 for d in det}; db = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d]/na2 - db[d]/nb2) for d in det)
        print(f"  d_TV: {dtv:.4f}")

    # 4. Born companion audit (same family, different aperture card)
    upper = sorted([i for i in bi if pos[i][1] > 1], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -1], key=lambda i: -pos[i][1])
    middle = sorted([i for i in bi if abs(pos[i][1]) <= 1], key=lambda i: abs(pos[i][1]))
    if upper and lower and middle:
        s_a = [upper[0]]; s_b = [lower[0]]; s_c = [middle[0]]
        all_s = set(s_a+s_b+s_c); other = set(bi)-all_s
        probs = {}
        for key, open_set in [('abc',all_s),('ab',set(s_a+s_b)),('ac',set(s_a+s_c)),
                               ('bc',set(s_b+s_c)),('a',set(s_a)),('b',set(s_b)),('c',set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = propagate(pos, adj, field_f, src, K, bl2)
            probs[key] = [abs(a[d])**2 for d in det]
        I3 = 0; P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di]-probs['ab'][di]-probs['ac'][di]-probs['bc'][di]
                  +probs['a'][di]+probs['b'][di]+probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3/P if P > 1e-30 else float('nan')
        print(f"  Born |I3|/P: {born:.2e}")

    # 5. Distance law companion harness (no barrier)
    print()
    print("  DISTANCE LAW (no barrier):")
    flat = propagate(pos, adj, field_f, src, K, set())
    fc = sum(abs(flat[d])**2*pos[d][1] for d in det) / sum(abs(flat[d])**2 for d in det)
    b_data, d_data = [], []
    for b_val in [3, 5, 7, 10, 13, 16, 19]:
        mi = nmap.get((gl, b_val))
        if mi is None: continue
        f2 = [0.0]*n; mx2, my2 = pos[mi]
        for i in range(n): ix, iy = pos[i]; f2[i] = 0.1/(math.sqrt((ix-mx2)**2+(iy-my2)**2)+0.1)
        am2 = propagate(pos, adj, f2, src, K, set())
        pm3 = sum(abs(am2[d])**2 for d in det)
        mc = sum(abs(am2[d])**2*pos[d][1] for d in det) / pm3
        delta = mc - fc
        print(f"    b={b_val:2d}: delta={delta:+.4f} (|delta|={abs(delta):.4f})")
        if abs(delta) > 0.01:
            b_data.append(b_val); d_data.append(abs(delta))

    # Power law fit on falloff region
    if len(d_data) >= 4:
        peak_idx = max(range(len(d_data)), key=lambda i: d_data[i])
        pk = b_data[peak_idx]
        falloff = [(b, d) for b, d in zip(b_data, d_data) if b >= pk]
        if len(falloff) >= 3:
            lx = [math.log(b) for b, _ in falloff]
            ly = [math.log(d) for _, d in falloff]
            nn = len(lx); mx_l = sum(lx)/nn; my_l = sum(ly)/nn
            sxx = sum((x-mx_l)**2 for x in lx)
            sxy = sum((x-mx_l)*(y-my_l) for x, y in zip(lx, ly))
            slope = sxy/sxx if sxx > 1e-10 else 0
            ss_res = sum((y-(my_l+slope*(x-mx_l)))**2 for x, y in zip(lx, ly))
            ss_tot = sum((y-my_l)**2 for y in ly)
            r2 = 1-ss_res/ss_tot if ss_tot > 0 else 0
            print(f"    Falloff: |delta| ~ b^({slope:.2f}), R²={r2:.3f}")

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
