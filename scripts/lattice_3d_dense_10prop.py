#!/usr/bin/env python3
"""Canonical 10-property card: 3D dense lattice, spent-delay, ultra-weak field.

This is the retained harness for the 3D dense spent-delay branch.
All 10 properties are evaluated on one ordered graph family with one
propagator, while the note/log chain keeps the claim surface bounded.

Graph: 3D integer lattice, max_d=3 (49 edges/node)
Action: spent-delay S = dl - sqrt(dl² - L²)
Field: 0.1/r with ultra-weak strength (5e-5)
Slits: y >= 0.5 (upper), y <= -0.5 (lower)
Mass: z-offset for gravity/distance
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
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 6
MAX_D = 3
STRENGTH = 0.00005


def generate(phys_l, h=1.0):
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
                for diy in range(-MAX_D, MAX_D + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-MAX_D, MAX_D + 1):
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


def make_field(pos, nmap, gl, z_mass, n):
    mi = nmap.get((gl, 0, round(z_mass)))
    if mi is None:
        return [0.0] * n, None
    field = [0.0] * n
    mx, my, mz = pos[mi]
    for i in range(n):
        pi = pos[i]
        r = math.sqrt((pi[0]-mx)**2 + (pi[1]-my)**2 + (pi[2]-mz)**2) + 0.1
        field[i] = STRENGTH / r
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


def detector_reads(amps, det, pos):
    ptot = sum(abs(amps[d])**2 for d in det)
    if ptot <= 1e-30:
        return 0.0, math.nan, math.nan, math.nan
    centroid = sum(abs(amps[d])**2 * pos[d][2] for d in det) / ptot
    near = [d for d in det if pos[d][2] >= 0]
    far = [d for d in det if pos[d][2] < 0]
    p_near = sum(abs(amps[d])**2 for d in near) / ptot
    channel_bias = (
        sum(abs(amps[d])**2 for d in near) - sum(abs(amps[d])**2 for d in far)
    ) / ptot
    return ptot, centroid, p_near, channel_bias


def classify_sign(delta_centroid, delta_pnear, delta_bias):
    if delta_centroid > 0 and delta_pnear > 0 and delta_bias > 0:
        return "ATTRACTIVE"
    if delta_centroid < 0 and delta_pnear < 0 and delta_bias < 0:
        return "AWAY"
    return "MIXED"


def main():
    phys_l = 12
    h = 1.0
    pos, adj, nl, hw, nmap = generate(phys_l, h)
    n = len(pos)
    det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1) for iz in range(-hw, hw+1)]
    gl = 2 * nl // 3
    bi, sa, sb, blocked, bl = setup_slits(pos, nmap, nl, hw)
    field_f = [0.0] * n

    print("=" * 80)
    print("3D DENSE LATTICE: CANONICAL 10-PROPERTY CARD")
    print(f"  49 edges/node, spent-delay, s={STRENGTH}")
    print(f"  L={phys_l}, W={PHYS_W}, h={h}, nodes={n}")
    print("=" * 80)
    print()

    af = propagate(pos, adj, field_f, K, blocked, n)
    pf, zf, pnear_f, bias_f = detector_reads(af, det, pos)

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
    born_s = f"{born:.2e}" if not math.isnan(born) else "nan"
    status = "PASS" if born < 1e-10 else "FAIL"
    print(f"  1. Born |I3|/P = {born_s}  [{status}]")

    # 2. d_TV
    pa = propagate(pos, adj, field_f, K, blocked | set(sb), n)
    pb = propagate(pos, adj, field_f, K, blocked | set(sa), n)
    da = {d: abs(pa[d])**2 for d in det}
    db = {d: abs(pb[d])**2 for d in det}
    na = sum(da.values()); nb = sum(db.values())
    dtv = 0
    if na > 1e-30 and nb > 1e-30:
        dtv = 0.5 * sum(abs(da[d]/na - db[d]/nb) for d in det)
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")

    # 3. k=0
    field_k0, _ = make_field(pos, nmap, gl, 3, n)
    af0 = propagate(pos, adj, field_f, 0.0, blocked, n)
    am0 = propagate(pos, adj, field_k0, 0.0, blocked, n)
    _, zf0, pnear_f0, bias_f0 = detector_reads(af0, det, pos)
    _, zm0, pnear_m0, bias_m0 = detector_reads(am0, det, pos)
    k0_delta = zm0 - zf0
    print(f"  3. k=0 = {k0_delta:.6f}  [{'PASS' if abs(k0_delta) < 1e-12 else 'FAIL'}]")

    # 4. F∝M
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        field_m, _ = make_field(pos, nmap, gl, 3, n)
        # Rescale field
        field_s = [f * s / STRENGTH for f in field_m]
        am = propagate(pos, adj, field_s, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            _, zm, _, _ = detector_reads(am, det, pos)
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
    fm_s = f"{fm_alpha:.2f}" if not math.isnan(fm_alpha) else "nan"
    print(f"  4. F∝M alpha = {fm_s}  [{'PASS' if not math.isnan(fm_alpha) and fm_alpha > 0 else 'CHECK'}]")

    # 5. Gravity grows with N
    gravs = {}
    for pl in [10, 12, 15]:
        p2, a2, nl2, hw2, nm2 = generate(pl, h)
        n2 = len(p2)
        d2 = [nm2[(nl2-1, iy, iz)] for iy in range(-hw2, hw2+1) for iz in range(-hw2, hw2+1)]
        _, _, _, bk2, _ = setup_slits(p2, nm2, nl2, hw2)
        gl2 = 2 * nl2 // 3
        ff2 = [0.0] * n2
        af2 = propagate(p2, a2, ff2, K, bk2, n2)
        pf2, zf2, _, _ = detector_reads(af2, d2, p2)
        if pf2 < 1e-30:
            continue
        fm2, _ = [0.0]*n2, None
        mi2 = nm2.get((gl2, 0, 3))
        if mi2 is None:
            continue
        fm2 = [0.0] * n2
        mx2, my2, mz2 = p2[mi2]
        for i in range(n2):
            pi = p2[i]
            fm2[i] = STRENGTH / (math.sqrt((pi[0]-mx2)**2+(pi[1]-my2)**2+(pi[2]-mz2)**2) + 0.1)
        am2 = propagate(p2, a2, fm2, K, bk2, n2)
        pm2, zm2, _, _ = detector_reads(am2, d2, p2)
        if pm2 > 1e-30:
            gravs[pl] = zm2 - zf2
    grows = False
    if len(gravs) >= 2:
        vals = list(gravs.values())
        grows = vals[-1] > vals[0]
    for pl, g in sorted(gravs.items()):
        sign = "TOWARD" if g > 0 else "AWAY"
        print(f"  5. Gravity N={pl}: {g:+.6f} ({sign})")
    print(f"     Grows with N: {'YES' if grows else 'NO'}  [{'PASS' if grows else 'CHECK'}]")

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
    NA2 = sum(abs(a)**2 for a in ba); NB2 = sum(abs(b)**2 for b in bb)
    Sn = S/(NA2+NB2) if (NA2+NB2) > 0 else 0
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
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # 7. MI
    prob_a = [0]*N_YBINS; prob_b = [0]*N_YBINS
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((pos[d][1]+PHYS_W+1)/bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na2 = sum(prob_a); nb2 = sum(prob_b); MI = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        pa_n = [p/na2 for p in prob_a]; pb_n = [p/nb2 for p in prob_b]
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5*pa_n[b3] + 0.5*pb_n[b3]
            if pm2 > 1e-30: H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5*pa_n[b3]*math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5*pb_n[b3]*math.log2(pb_n[b3])
        MI = H - Hc
    print(f"  7. MI = {MI:.4f} bits  [{'PASS' if MI > 0.05 else 'WEAK'}]")

    # 8. Purity scaling
    pur_data = {}
    for pl in [8, 10, 12, 15]:
        p2, a2, nl2, hw2, nm2 = generate(pl, h)
        n2 = len(p2)
        d2 = [nm2[(nl2-1, iy, iz)] for iy in range(-hw2, hw2+1) for iz in range(-hw2, hw2+1)]
        bi2, sa2, sb2, bk2, bl2 = setup_slits(p2, nm2, nl2, hw2)
        order2 = sorted(range(n2), key=lambda i: p2[i][0])
        ff2 = [0.0] * n2
        amps_a = [0j]*n2; amps_b = [0j]*n2
        src2 = next(i for i, p in enumerate(p2)
                    if abs(p[0])<1e-10 and abs(p[1])<1e-10 and abs(p[2])<1e-10)
        amps_a[src2] = 1.0; amps_b[src2] = 1.0
        for i in order2:
            if abs(amps_a[i]) > 1e-30 and i not in (bk2 | set(sb2)):
                for j in a2.get(i, []):
                    if j in (bk2 | set(sb2)): continue
                    pi2, pj2 = p2[i], p2[j]
                    dx=pj2[0]-pi2[0];dy=pj2[1]-pi2[1];dz=pj2[2]-pi2[2]
                    L=math.sqrt(dx*dx+dy*dy+dz*dz)
                    if L<1e-10:continue
                    theta=math.atan2(math.sqrt(dy*dy+dz*dz),max(dx,1e-10))
                    w=math.exp(-BETA*theta*theta)
                    amps_a[j]+=amps_a[i]*cmath.exp(1j*K*L)*w/L
            if abs(amps_b[i]) > 1e-30 and i not in (bk2 | set(sa2)):
                for j in a2.get(i, []):
                    if j in (bk2 | set(sa2)): continue
                    pi2, pj2 = p2[i], p2[j]
                    dx=pj2[0]-pi2[0];dy=pj2[1]-pi2[1];dz=pj2[2]-pi2[2]
                    L=math.sqrt(dx*dx+dy*dy+dz*dz)
                    if L<1e-10:continue
                    theta=math.atan2(math.sqrt(dy*dy+dz*dz),max(dx,1e-10))
                    w=math.exp(-BETA*theta*theta)
                    amps_b[j]+=amps_b[i]*cmath.exp(1j*K*L)*w/L
        bw2 = 2*(PHYS_W+1)/N_YBINS
        ed2 = max(1,round(nl2/6)); st2=bl2+1; sp2=min(nl2-1,st2+ed2)
        mid2 = []
        for l in range(st2, sp2):
            mid2.extend([nm2[(l,iy,iz)] for iy in range(-hw2,hw2+1)
                        for iz in range(-hw2,hw2+1) if (l,iy,iz) in nm2])
        ba2=[0j]*N_YBINS; bb2=[0j]*N_YBINS
        for m in mid2:
            b2=max(0,min(N_YBINS-1,int((p2[m][1]+PHYS_W+1)/bw2)))
            ba2[b2]+=amps_a[m]; bb2[b2]+=amps_b[m]
        S2=sum(abs(a-b)**2 for a,b in zip(ba2,bb2))
        NA3=sum(abs(a)**2 for a in ba2); NB3=sum(abs(b)**2 for b in bb2)
        Sn2=S2/(NA3+NB3) if (NA3+NB3)>0 else 0
        Dcl2=math.exp(-LAM**2*Sn2)
        rho2={}
        for d1 in d2:
            for d2_ in d2:
                rho2[(d1,d2_)]=(amps_a[d1].conjugate()*amps_a[d2_]
                               +amps_b[d1].conjugate()*amps_b[d2_]
                               +Dcl2*amps_a[d1].conjugate()*amps_b[d2_]
                               +Dcl2*amps_b[d1].conjugate()*amps_a[d2_])
        tr2=sum(rho2[(d,d)] for d in d2).real
        if tr2>1e-30:
            for key in rho2: rho2[key]/=tr2
            pur2=sum(abs(v)**2 for v in rho2.values()).real
            pur_data[pl]=1-pur2
    if len(pur_data) >= 3:
        ns = sorted(pur_data.keys())
        ys = [pur_data[n_] for n_ in ns]
        lx = [math.log(n_) for n_ in ns]
        ly = [math.log(y) for y in ys]
        nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
        sxx = sum((x-mx_l)**2 for x in lx)
        sxy = sum((x-mx_l)*(y-my_l) for x, y in zip(lx, ly))
        slope = sxy/sxx if sxx > 1e-10 else 0
        ss_res = sum((y-(my_l+slope*(x-mx_l)))**2 for x, y in zip(lx, ly))
        ss_tot = sum((y-my_l)**2 for y in ly)
        r2 = 1-ss_res/ss_tot if ss_tot > 0 else 0
        A = math.exp(my_l - slope*mx_l)
        n_half = (0.01/A)**(1/slope) if slope < 0 else float('inf')
        for pl in ns:
            print(f"  8. Purity L={pl}: 1-pur={pur_data[pl]:.4f}")
        print(f"     Exponent: N^({slope:.2f}), R²={r2:.3f}, N_half={n_half:.0f}")

    # 9. k=0 control
    k0_hierarchy = max(abs(k0_delta), abs(pnear_m0 - pnear_f0), abs(bias_m0 - bias_f0))
    print(f"  9. k=0 control = {k0_hierarchy:.6f}  [{'PASS' if k0_hierarchy < 1e-12 else 'FAIL'}]")

    # 10. Distance law
    b_data = []; d_data = []
    b_hier = []; d_hier = []
    for z_mass in [2, 3, 4, 5]:
        field_m, _ = make_field(pos, nmap, gl, z_mass, n)
        am = propagate(pos, adj, field_m, K, blocked, n)
        pm, zm, pnear_m, bias_m = detector_reads(am, det, pos)
        if pm > 1e-30:
            delta = zm - zf
            delta_pnear = pnear_m - pnear_f
            delta_bias = bias_m - bias_f
            sign = classify_sign(delta, delta_pnear, delta_bias)
            print(
                f" 10. Distance z={z_mass}: centroid={delta:+.6f}, "
                f"P_near={delta_pnear:+.6f}, bias={delta_bias:+.6f} [{sign}]"
            )
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)
            if sign == "ATTRACTIVE":
                b_hier.append(z_mass); d_hier.append(delta)
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
        print(f"     Centroid law: b^({slope:.2f}), R²={r2:.3f}")
    if len(b_hier) >= 3:
        lx = [math.log(b) for b in b_hier]
        ly = [math.log(d) for d in d_hier]
        nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
        sxx = sum((x-mx_l)**2 for x in lx)
        sxy = sum((x-mx_l)*(y-my_l) for x, y in zip(lx, ly))
        slope = sxy/sxx if sxx > 1e-10 else 0
        ss_res = sum((y-(my_l+slope*(x-mx_l)))**2 for x, y in zip(lx, ly))
        ss_tot = sum((y-my_l)**2 for y in ly)
        r2 = 1-ss_res/ss_tot if ss_tot > 0 else 0
        print(
            f"     Hierarchy-aligned support: {len(b_hier)}/{len([2,3,4,5])} points, "
            f"b^({slope:.2f}), R²={r2:.3f}"
        )

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
