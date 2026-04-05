#!/usr/bin/env python3
"""Nearest-neighbor lattice with normalized transfer matrix.

The 1/L kernel diverges as h -> 0 because L ~ h. Fix: divide each edge
weight by the total outgoing norm T = sum_edges |w/L^p|, making the
per-node transfer norm exactly 1. This is still LINEAR in amplitudes
(T depends only on lattice geometry, not on psi) so Born holds.

Test: all observables at h = 2.0, 1.0, 0.5, 0.25, 0.125.
"""

from __future__ import annotations

import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K_PHYS = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 20.0
PHYS_L = 40.0
SLIT_Y = 3.0
MASS_Y = 8.0


def generate_nn(spacing):
    nl = int(PHYS_L / spacing) + 1
    hw = int(PHYS_W / spacing)
    pos = []
    adj = defaultdict(list)
    nmap = {}

    for layer in range(nl):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            idx = len(pos)
            pos.append((x, iy * spacing))
            nmap[(layer, iy)] = idx

    edges = {}  # (i, j) -> (L, w)
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
                    x1, y1 = pos[si]
                    x2, y2 = pos[di]
                    dx, dy = x2 - x1, y2 - y1
                    L = math.sqrt(dx * dx + dy * dy)
                    theta = math.atan2(abs(dy), max(dx, 1e-10))
                    w = math.exp(-BETA * theta * theta)
                    adj[si].append(di)
                    edges[(si, di)] = (L, w)

    # Compute per-node transfer norm and normalize
    # T_i = sum_{j: i->j} w_j / L_j
    node_norm = {}
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            T = 0.0
            for j in adj.get(si, []):
                L, w = edges[(si, j)]
                T += w / L
            node_norm[si] = T if T > 1e-30 else 1.0

    return pos, dict(adj), edges, node_norm, nl, hw, nmap


def propagate_normed(pos, adj, edges, node_norm, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, (x, y) in enumerate(pos) if abs(x) < 1e-10 and abs(y) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        T = node_norm.get(i, 1.0)
        for j in adj.get(i, []):
            if j in blocked:
                continue
            L, w = edges[(i, j)]
            lf = 0.5 * (field[i] + field[j])
            # Valley-linear action
            act = L * (1.0 - lf)
            # Normalized kernel: exp(ikS) * w / (L * T)
            ea = cmath.exp(1j * k * act) * w / (L * T)
            amps[j] += amps[i] * ea
    return amps


def measure_full(spacing):
    pos, adj, edges, node_norm, nl, hw, nmap = generate_nn(spacing)
    n = len(pos)
    det_layer = nl - 1
    det = [nmap[(det_layer, iy)] for iy in range(-hw, hw + 1) if (det_layer, iy) in nmap]
    bl = nl // 3
    gl = 2 * nl // 3

    # Slits
    slit_iy = max(1, round(SLIT_Y / spacing))
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    sa_range = range(slit_iy, min(slit_iy + max(2, round(2 / spacing)), hw + 1))
    sb_range = range(-min(slit_iy + max(1, round(1 / spacing)), hw), -slit_iy + 1)
    sa = [nmap[(bl, iy)] for iy in sa_range if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in sb_range if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    field_f = [0.0] * n

    mass_iy = round(MASS_Y / spacing)
    mass_idx = nmap.get((gl, mass_iy))
    if mass_idx is None:
        return None
    phys_strength = 0.0005
    field_m = [0.0] * n
    mx, my = pos[mass_idx]
    for i in range(n):
        ix, iy = pos[i]
        r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
        field_m[i] = phys_strength / r

    def prop(field, k, extra_blocked=set()):
        return propagate_normed(pos, adj, edges, node_norm, field, k, blocked | extra_blocked, n)

    # Gravity
    af = prop(field_f, K_PHYS)
    am = prop(field_m, K_PHYS)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d]) ** 2 * pos[d][1] for d in det) / pf
    ym = sum(abs(am[d]) ** 2 * pos[d][1] for d in det) / pm
    gravity = ym - yf

    # k=0
    am0 = prop(field_m, 0.0)
    af0 = prop(field_f, 0.0)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d][1] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d][1] for d in det) / pf0)

    # MI + decoherence
    pa = prop(field_f, K_PHYS, set(sb))
    pb = prop(field_f, K_PHYS, set(sa))
    bw = 2 * (PHYS_W + spacing) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d][1] + PHYS_W + spacing) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na = sum(prob_a)
    nb = sum(prob_b)
    MI = 0.0
    if na > 1e-30 and nb > 1e-30:
        pa_n = [p / na for p in prob_a]
        pb_n = [p / nb for p in prob_b]
        H = 0.0
        Hc = 0.0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H - Hc

    # CL purity (low-rank approx)
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
    dtv = 0.0
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
            a = propagate_normed(pos, adj, edges, node_norm, field_f, K_PHYS, bl2, n)
            probs[key] = [abs(a[d]) ** 2 for d in det]
        I3 = 0.0
        P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3)
            P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else math.nan

    # Amplitude max (check no overflow)
    amp_max = max(abs(a) for a in af)

    return {
        "h": spacing, "n": n, "nl": nl, "npl": 2 * hw + 1,
        "gravity": gravity, "gk0": gk0,
        "MI": MI, "pur_cl": pur_cl, "dtv": dtv, "born": born,
        "amp_max": amp_max,
    }


def main():
    print("=" * 100)
    print("NEAREST-NEIGHBOR NORMED-TRANSFER CONTINUUM LIMIT")
    print(f"  3 edges/node, transfer norm = 1 at all h. Physical: W={PHYS_W}, L={PHYS_L}")
    print(f"  Valley-linear action: S = L(1-f). k={K_PHYS}, field=0.0005, mass at y={MASS_Y}")
    print("=" * 100)
    print()

    print(f"  {'h':>5s}  {'nodes':>7s}  {'gravity':>10s}  {'k=0':>10s}  "
          f"{'MI':>8s}  {'1-pur':>8s}  {'d_TV':>8s}  {'Born':>10s}  {'amp_max':>10s}  {'time':>5s}")
    print(f"  {'-' * 95}")

    for h in [2.0, 1.0, 0.5, 0.25, 0.125]:
        t0 = time.time()
        r = measure_full(h)
        dt = time.time() - t0
        if r:
            born_s = f"{r['born']:.2e}" if not math.isnan(r['born']) else "       nan"
            print(f"  {h:5.3f}  {r['n']:7d}  {r['gravity']:+10.6f}  "
                  f"{r['gk0']:+10.2e}  {r['MI']:8.4f}  {1 - r['pur_cl']:8.4f}  "
                  f"{r['dtv']:8.4f}  {born_s}  {r['amp_max']:10.2e}  {dt:4.0f}s")
        else:
            print(f"  {h:5.3f}  FAIL  {dt:4.0f}s")

    print()
    print("SAFE READ")
    print("  CONVERGENCE: values should stabilize as h -> 0")
    print("  BORN: must stay < 1e-10 at all h")
    print("  amp_max: should not overflow (< 1e100)")
    print("  gravity: sign must be consistent (TOWARD = positive)")
    print("  if gravity, MI, d_TV converge to finite nonzero limits: continuum limit exists")


if __name__ == "__main__":
    main()
