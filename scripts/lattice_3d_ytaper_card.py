#!/usr/bin/env python3
"""3D Y-only tapered lattice: taper in slit direction, uniform in gravity direction.

The full taper (y AND z) gives TOWARD that survives refinement but
breaks the distance law (mass at different z sees different taper).

Fix: taper ONLY in y (slit direction). Keep z connectivity uniform.
This way the mass at any z sees the same lattice structure.

Taper in y:
  |y| < 2: max_dy = 3
  2 <= |y| < 4: max_dy = 2
  |y| >= 4: max_dy = 1

Z always: max_dz = 3 (uniform dense connectivity)
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 6
STRENGTH = 5e-5


def generate_ytaper(phys_l, h=1.0):
    nl = int(phys_l / h) + 1
    hw = int(PHYS_W / h)
    max_dz = max(1, round(3 / h))  # z always dense
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
                y_phys = abs(iy * h)
                if y_phys < 2:
                    max_dy = max(1, round(3 / h))
                elif y_phys < 4:
                    max_dy = max(1, round(2 / h))
                else:
                    max_dy = max(1, round(1 / h))
                for diy in range(-max_dy, max_dy + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-max_dz, max_dz + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def propagate(pos, adj, field, k, blocked, n):
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


def make_field(pos, nmap, gl, z_mass_phys, n, strength, h):
    iz = round(z_mass_phys / h)
    mi = nmap.get((gl, 0, iz))
    if mi is None:
        return [0.0] * n, None
    field = [0.0] * n
    mx, my, mz = pos[mi]
    for i in range(n):
        pi = pos[i]
        r = math.sqrt((pi[0]-mx)**2 + (pi[1]-my)**2 + (pi[2]-mz)**2) + 0.1
        field[i] = strength / r
    return field, mi


def setup_slits(pos, nmap, nl, hw):
    bl = nl // 3
    bi = []
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def run_card(h):
    phys_l = 12
    pos, adj, nl, hw, nmap = generate_ytaper(phys_l, h)
    n = len(pos)
    det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
           for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
    gl = 2 * nl // 3
    bi, sa, sb, blocked, bl = setup_slits(pos, nmap, nl, hw)
    field_f = [0.0] * n

    center_idx = nmap.get((1, 0, 0), 0)
    edges_center = len(adj.get(center_idx, []))
    edge_idx = nmap.get((1, 0, round(5/h)), 0)
    edges_edge = len(adj.get(edge_idx, []))

    print(f"\n{'='*70}")
    print(f"3D Y-TAPERED LATTICE CARD (h={h})")
    print(f"  {n} nodes, {nl} layers, {2*hw+1}x{2*hw+1} cross-section")
    print(f"  Center (y=0): ~{edges_center} edges  |  Edge (z=5): ~{edges_edge} edges")
    print(f"  Y-taper: |y|<2 dense, |y|>=4 NN. Z always dense.")
    print(f"{'='*70}\n")

    af = propagate(pos, adj, field_f, K, blocked, n)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL AT DETECTOR")
        return
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    # 1. Born
    upper = sorted([i for i in bi if pos[i][1] > 1], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -1], key=lambda i: -pos[i][1])
    middle = [i for i in bi if abs(pos[i][1]) <= 1 and abs(pos[i][2]) <= 1]
    born = math.nan
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                               ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = propagate(pos, adj, field_f, K, bl2, n)
            probs[key] = [abs(a[d])**2 for d in det]
        I3 = 0; P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else math.nan
    status = "PASS" if born < 1e-10 else "FAIL"
    print(f"  1. Born |I3|/P = {born:.2e}  [{status}]")

    # 2. d_TV
    pa = propagate(pos, adj, field_f, K, blocked | set(sb), n)
    pb = propagate(pos, adj, field_f, K, blocked | set(sa), n)
    da = {d: abs(pa[d])**2 for d in det}
    db = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d]/na2 - db[d]/nb2) for d in det)
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")

    # 3. k=0
    field_m, _ = make_field(pos, nmap, gl, 3, n, STRENGTH, h)
    am0 = propagate(pos, adj, field_m, 0.0, blocked, n)
    af0 = propagate(pos, adj, field_f, 0.0, blocked, n)
    pm0 = sum(abs(am0[d])**2 for d in det)
    pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2 * pos[d][2] for d in det) / pm0
               - sum(abs(af0[d])**2 * pos[d][2] for d in det) / pf0)
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # 4. F∝M
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(pos, nmap, gl, 3, n, s, h)
        am = propagate(pos, adj, fm, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s); g_data.append(delta)
    fm_alpha = math.nan
    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]
        ly = [math.log(g) for g in g_data]
        nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
        sxx = sum((x-mx_l)**2 for x in lx)
        sxy = sum((x-mx_l)*(y-my_l) for x, y in zip(lx, ly))
        fm_alpha = sxy/sxx if sxx > 1e-10 else 0
    print(f"  4. F~M alpha = {fm_alpha:.2f}" if not math.isnan(fm_alpha)
          else "  4. F~M alpha = nan")

    # 5. Gravity
    am = propagate(pos, adj, field_m, K, blocked, n)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
        grav = zm - zf
    print(f"  5. Gravity = {grav:+.6f} ({'TOWARD' if grav > 0 else 'AWAY'})")

    # 6. Decoherence
    bw = 2 * (PHYS_W + 1) / N_YBINS
    ed = max(1, round(nl/6)); st = bl + 1; sp = min(nl-1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy, iz)] for iy in range(-hw, hw+1)
                    for iz in range(-hw, hw+1) if (l, iy, iz) in nmap])
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS-1, int((pos[m][1]+PHYS_W+1)/bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    NA3 = sum(abs(a)**2 for a in ba); NB3 = sum(abs(b)**2 for b in bb)
    Sn = S/(NA3+NB3) if (NA3+NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2] + pb[d1].conjugate()*pb[d2]
                           + Dcl*pa[d1].conjugate()*pb[d2] + Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(d,d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho: rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
    decoh = 100*(1-pur)
    print(f"  6. Decoherence = {decoh:.1f}%")

    # 7. MI
    prob_a = [0]*N_YBINS; prob_b = [0]*N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((pos[d][1]+PHYS_W+1)/bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na3 = sum(prob_a); nb3 = sum(prob_b); MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = [p/na3 for p in prob_a]; pb_n = [p/nb3 for p in prob_b]
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5*pa_n[b3] + 0.5*pb_n[b3]
            if pm2 > 1e-30: H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5*pa_n[b3]*math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5*pb_n[b3]*math.log2(pb_n[b3])
        MI = H - Hc
    print(f"  7. MI = {MI:.4f} bits")

    # 10. Distance law
    b_data = []; d_data = []
    print(f"  10. Distance law:")
    for z_mass in [2, 3, 4, 5]:
        fm, _ = make_field(pos, nmap, gl, z_mass, n, STRENGTH, h)
        am = propagate(pos, adj, fm, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            sign = "TOWARD" if delta > 0 else "AWAY"
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)
    if len(b_data) >= 3:
        lx = [math.log(b) for b in b_data]
        ly = [math.log(d) for d in d_data]
        nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
        sxx = sum((x-mx_l)**2 for x in lx)
        sxy = sum((x-mx_l)*(y-my_l) for x, y in zip(lx, ly))
        slope = sxy/sxx if sxx > 1e-10 else 0
        ss_res = sum((y-(my_l+slope*(x-mx_l)))**2 for x, y in zip(lx, ly))
        ss_tot = sum((y-my_l)**2 for y in ly)
        r2 = 1-ss_res/ss_tot if ss_tot > 0 else 0
        print(f"      Exponent: b^({slope:.2f}), R²={r2:.3f}")

    print()


def main():
    for h in [1.0, 0.5]:
        t0 = time.time()
        run_card(h)
        dt = time.time() - t0
        print(f"  Total time: {dt:.0f}s")


if __name__ == "__main__":
    main()
