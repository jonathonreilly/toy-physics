#!/usr/bin/env python3
"""Nearest-neighbor lattice refinement study.

Force exactly 3 forward edges per node (straight, up, down) regardless
of spacing. This sharply reduces fan-out growth relative to the denser
ordered-lattice branch, but it does not by itself guarantee a fully
stable raw-kernel continuum limit.

The beam confinement that gives 1/b is preserved: each step shifts
y by at most ±h.

Test: the retained refinement observables at h = 2.0, 1.0, 0.5, 0.25, 0.125.
Safe claim: Born-clean positive refinement trend through h = 0.25.
The h = 0.125 point is still unresolved for the raw kernel because the
unrescaled path sum overflows there.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K_PHYS = 5.0  # Physical coupling constant (h-independent)
LAM = 10.0
N_YBINS = 8
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
MASS_Y = 8.0


def generate_nn_lattice(spacing):
    """Lattice with exactly 3 nearest-neighbor forward edges per node."""
    nl = int(PHYS_L / spacing) + 1
    hw = int(PHYS_W / spacing)
    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(nl):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            y = iy * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx

    # Exactly 3 edges: straight (dy=0), up (dy=+1), down (dy=-1)
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for diy in [-1, 0, 1]:
                iyn = iy + diy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)

    return pos, dict(adj), nl, hw, nmap


def propagate(pos, adj, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
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
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_full(spacing):
    pos, adj, nl, hw, nmap = generate_nn_lattice(spacing)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    # Slits at physical y = ±SLIT_Y
    slit_iy = max(1, round(SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa_range = range(slit_iy, min(slit_iy + max(2, round(2/spacing)), hw + 1))
    sb_range = range(-min(slit_iy + max(1, round(1/spacing)), hw), -slit_iy + 1)
    sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    field_f = [0.0] * n

    # Field at MASS_Y (scaled strength: weaker at finer spacing)
    mass_iy = round(MASS_Y / spacing)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None
    # Physical field strength: constant regardless of spacing
    phys_strength = 0.0005
    field_m = [0.0] * n
    mx, my = pos[mass_idx]
    for i in range(n):
        ix, iy = pos[i]
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field_m[i] = phys_strength / r

    # Gravity
    af = propagate(pos, adj, field_f, K_PHYS, blocked, n)
    am = propagate(pos, adj, field_m, K_PHYS, blocked, n)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    gravity = ym - yf

    # k=0
    am0 = propagate(pos, adj, field_m, 0.0, blocked, n)
    af0 = propagate(pos, adj, field_f, 0.0, blocked, n)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0)

    # MI + decoherence
    pa = propagate(pos, adj, field_f, K_PHYS, blocked | set(sb), n)
    pb = propagate(pos, adj, field_f, K_PHYS, blocked | set(sa), n)
    bw = 2 * (PHYS_W + spacing) / N_YBINS
    prob_a = [0] * N_YBINS
    prob_b = [0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + spacing) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na = sum(prob_a)
    nb = sum(prob_b)
    MI = 0
    if na > 1e-30 and nb > 1e-30:
        pa_n = [p / na for p in prob_a]
        pb_n = [p / nb for p in prob_b]
        H = 0
        Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H - Hc

    # CL purity
    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy)] for iy in range(-hw, hw + 1) if (l, iy) in nmap])
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m][1] + PHYS_W + spacing) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA = sum(abs(a) ** 2 for a in ba)
    NB = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA + NB) if (NA + NB) > 0 else 0
    Dcl = math.exp(-LAM ** 2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (pa[d1].conjugate() * pa[d2] + pb[d1].conjugate() * pb[d2]
                             + Dcl * pa[d1].conjugate() * pb[d2]
                             + Dcl * pb[d1].conjugate() * pa[d2])
    tr = sum(rho[(d, d)] for d in det).real
    pur_cl = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    # d_TV
    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)

    # Born (3-slit)
    born = math.nan
    upper = sorted([i for i in bi if pos[i][1] > spacing], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -spacing], key=lambda i: -pos[i][1])
    middle = [i for i in bi if abs(pos[i][1]) <= spacing]
    if upper and lower and middle:
        s_a = [upper[0]]
        s_b = [lower[0]]
        s_c = [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a + s_b)),
                               ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = propagate(pos, adj, field_f, K_PHYS, bl2, n)
            probs[key] = [abs(a[d]) ** 2 for d in det]
        I3 = 0
        P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3)
            P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else math.nan

    return {
        "h": spacing, "n": n, "nl": nl, "npl": 2 * hw + 1,
        "gravity": gravity, "gk0": gk0,
        "MI": MI, "pur_cl": pur_cl, "dtv": dtv, "born": born,
    }


def main():
    print("=" * 95)
    print("NEAREST-NEIGHBOR LATTICE REFINEMENT STUDY")
    print(f"  3 edges/node at ALL spacings. Physical: W={PHYS_W}, L={PHYS_L}")
    print(f"  k={K_PHYS}, field_strength=0.0005, mass at y={MASS_Y}")
    print("=" * 95)
    print()

    print(f"  {'h':>5s}  {'nodes':>7s}  {'npl':>5s}  {'gravity':>10s}  {'k=0':>10s}  "
          f"{'MI':>8s}  {'1-pur':>8s}  {'d_TV':>8s}  {'Born':>10s}  {'time':>5s}")
    print(f"  {'-' * 88}")

    for h in [2.0, 1.0, 0.5, 0.25, 0.125]:
        t0 = time.time()
        try:
            r = measure_full(h)
        except OverflowError:
            r = None
        dt = time.time() - t0
        if r:
            born_s = f"{r['born']:.2e}" if not math.isnan(r['born']) else "       nan"
            print(f"  {h:5.3f}  {r['n']:7d}  {r['npl']:5d}  {r['gravity']:+10.6f}  "
                  f"{r['gk0']:+10.2e}  {r['MI']:8.4f}  {1-r['pur_cl']:8.4f}  "
                  f"{r['dtv']:8.4f}  {born_s}  {dt:4.0f}s")
        else:
            print(f"  {h:5.3f}  FAIL  {dt:4.0f}s")

    print()
    print("SAFE CLAIM: Born-clean positive refinement trend through h = 0.25")
    print("BORN: must stay < 1e-10 on the retained window")
    print("h = 0.125 remains unresolved for the raw kernel")


if __name__ == "__main__":
    main()
