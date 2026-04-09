#!/usr/bin/env python3
"""Canonical action-power harness on fixed 2D/3D lattices.

This is the FROZEN harness for the action-power family S = L × |f|^p.
It measures:
  - same-harness 2D comparison
  - 3D close-slit barrier card for Born / k=0 / MI / d_TV / pur_cl / gravity
  - 3D no-barrier companion for distance law and mass response

Explicit comparison against the current spent-delay baseline.

NOTE: Changing the action formula is an AXIOM FORK. Results here
do NOT inherit from the spent-delay flagship. Every claim must be
independently validated.
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


def generate_nn_lattice(phys_l, phys_w, h):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
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
            for diy in [-1, 0, 1]:
                iyn = iy + diy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def generate_3d_nn_lattice(phys_l, phys_w, h):
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
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
                for diy in [-1, 0, 1]:
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in [-1, 0, 1]:
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def propagate_2d(pos, adj, field, k, blocked, n, action_type):
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
            x1, y1 = pos[i]; x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action_type == 'spent_delay':
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
            elif action_type == 'power':
                act = L * (abs(lf) ** 0.5)  # p=0.5 (same as spent-delay asymptotic)
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def propagate_3d(pos, adj, field, k, blocked, n, action_type):
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
            dx = pj[0] - pi[0]; dy = pj[1] - pi[1]; dz = pj[2] - pi[2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action_type == 'spent_delay':
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl*dl - L*L, 0))
                act = dl - ret
            elif action_type == 'power':
                act = L * (abs(lf) ** 0.5)
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def make_field_2d(pos, nmap, gl, mass_y, strength, n):
    mass_iy = round(mass_y)
    mi = nmap.get((gl, mass_iy))
    if mi is None:
        return [0.0] * n, None
    field = [0.0] * n
    mx, my = pos[mi]
    for i in range(n):
        ix, iy = pos[i]
        field[i] = strength / (math.sqrt((ix-mx)**2 + (iy-my)**2) + 0.1)
    return field, mi


def make_field_3d(pos, nmap, gl, mass_z, strength, hw, n):
    mi = nmap.get((gl, 0, round(mass_z)))
    if mi is None:
        return [0.0] * n, None
    field = [0.0] * n
    mx, my, mz = pos[mi]
    for i in range(n):
        pi = pos[i]
        field[i] = strength / (math.sqrt((pi[0]-mx)**2 + (pi[1]-my)**2 + (pi[2]-mz)**2) + 0.1)
    return field, mi


def fit_power_law(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return math.nan, 0.0
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx_l = sum(lx) / len(lx)
    my_l = sum(ly) / len(ly)
    sxx = sum((x - mx_l) ** 2 for x in lx)
    if sxx <= 1e-12:
        return math.nan, 0.0
    sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
    slope = sxy / sxx
    ss_res = sum((y - (my_l + slope * (x - mx_l))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my_l) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def run_2d_harness(action_type, phys_l=40, phys_w=20, h=1.0, strength=0.001,
                    slit_y=3):
    """Full 2D harness: Born, k=0, MI, d_TV, pur_cl, distance, mass."""
    pos, adj, nl, hw, nmap = generate_nn_lattice(phys_l, phys_w, h)
    n = len(pos)
    det = [nmap[(nl-1, iy)] for iy in range(-hw, hw+1)]
    bl = nl // 3; gl = 2 * nl // 3
    slit_iy = round(slit_y / h)
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw+1) if (bl, iy) in nmap]
    sa = [nmap[(bl, iy)] for iy in range(slit_iy, min(slit_iy+3, hw+1)) if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in range(-min(slit_iy+2, hw), -slit_iy+1) if (bl, iy) in nmap]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    field_f = [0.0] * n
    prop = lambda f, k, bl_set: propagate_2d(pos, adj, f, k, bl_set, n, action_type)

    results = {"action": action_type, "dim": 2, "h": h, "n": n}

    # Gravity at mass_y=8
    field_m, _ = make_field_2d(pos, nmap, gl, 8, strength, n)
    af = prop(field_f, K, blocked); am = prop(field_m, K, blocked)
    pf = sum(abs(af[d])**2 for d in det); pm = sum(abs(am[d])**2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    yf = sum(abs(af[d])**2*pos[d][1] for d in det)/pf
    ym = sum(abs(am[d])**2*pos[d][1] for d in det)/pm
    results["gravity"] = ym - yf

    # k=0
    am0 = prop(field_m, 0.0, blocked); af0 = prop(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    results["k0"] = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        results["k0"] = (sum(abs(am0[d])**2*pos[d][1] for d in det)/pm0
                         - sum(abs(af0[d])**2*pos[d][1] for d in det)/pf0)

    # MI + d_TV + pur_cl
    pa = prop(field_f, K, blocked | set(sb))
    pb = prop(field_f, K, blocked | set(sa))
    bw = 2*(phys_w+h)/N_YBINS; prob_a = [0]*N_YBINS; prob_b = [0]*N_YBINS
    da = {}; db = {}
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((pos[d][1]+phys_w+h)/bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
        da[d] = abs(pa[d])**2; db[d] = abs(pb[d])**2
    na = sum(prob_a); nb = sum(prob_b)
    if na > 1e-30 and nb > 1e-30:
        pa_n = [p/na for p in prob_a]; pb_n = [p/nb for p in prob_b]
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5*pa_n[b3]+0.5*pb_n[b3]
            if pm2 > 1e-30: H -= pm2*math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5*pa_n[b3]*math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5*pb_n[b3]*math.log2(pb_n[b3])
        results["MI"] = H - Hc
        results["d_TV"] = 0.5*sum(abs(da[d]/na - db[d]/nb) for d in det)
    else:
        results["MI"] = 0; results["d_TV"] = 0

    # CL purity
    ed = max(1, round(nl/6)); st = bl+1; sp = min(nl-1, st+ed)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy)] for iy in range(-hw, hw+1) if (l, iy) in nmap])
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid:
        b2 = max(0, min(N_YBINS-1, int((pos[m][1]+phys_w+h)/bw)))
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
        results["pur_cl"] = sum(abs(v)**2 for v in rho.values()).real
    else:
        results["pur_cl"] = 1.0

    # Born
    upper = sorted([i for i in bi if pos[i][1] > h], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -h], key=lambda i: -pos[i][1])
    middle = [i for i in bi if abs(pos[i][1]) <= h]
    results["born"] = math.nan
    if upper and lower and middle:
        s_a = [upper[0]]; s_b = [lower[0]]; s_c = [middle[0]]
        all_s = set(s_a+s_b+s_c); other = set(bi)-all_s; probs = {}
        for key, open_set in [('abc',all_s),('ab',set(s_a+s_b)),('ac',set(s_a+s_c)),
                               ('bc',set(s_b+s_c)),('a',set(s_a)),('b',set(s_b)),('c',set(s_c))]:
            bl2 = other|(all_s-open_set)
            a = prop(field_f, K, bl2)
            probs[key] = [abs(a[d])**2 for d in det]
        I3 = 0; P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di]-probs['ab'][di]-probs['ac'][di]-probs['bc'][di]
                  +probs['a'][di]+probs['b'][di]+probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        results["born"] = I3/P if P > 1e-30 else math.nan

    # Distance law (no barrier)
    af_nb = prop(field_f, K, set())
    pf_nb = sum(abs(af_nb[d])**2 for d in det)
    yf_nb = sum(abs(af_nb[d])**2*pos[d][1] for d in det)/pf_nb if pf_nb > 1e-30 else 0
    b_data = []; d_data = []
    for b_phys in [5, 7, 10, 13, 16, 19]:
        field_mb, _ = make_field_2d(pos, nmap, gl, b_phys, strength, n)
        am_nb = prop(field_mb, K, set())
        pm_nb = sum(abs(am_nb[d])**2 for d in det)
        if pm_nb > 1e-30:
            ym_nb = sum(abs(am_nb[d])**2*pos[d][1] for d in det)/pm_nb
            b_data.append(b_phys); d_data.append(abs(ym_nb - yf_nb))
    results["dist_exp"] = math.nan; results["dist_r2"] = 0
    if len(b_data) >= 4:
        pk = b_data[d_data.index(max(d_data))]
        falloff = [(b,d) for b,d in zip(b_data,d_data) if b >= pk and d > 0]
        if len(falloff) >= 3:
            lx = [math.log(b) for b,_ in falloff]; ly = [math.log(d) for _,d in falloff]
            nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
            sxx = sum((x-mx_l)**2 for x in lx); sxy = sum((x-mx_l)*(y-my_l) for x,y in zip(lx,ly))
            slope = sxy/sxx if sxx > 1e-10 else 0
            ss_res = sum((y-(my_l+slope*(x-mx_l)))**2 for x,y in zip(lx,ly))
            ss_tot = sum((y-my_l)**2 for y in ly)
            results["dist_exp"] = slope
            results["dist_r2"] = 1-ss_res/ss_tot if ss_tot > 0 else 0

    # Mass response
    m_data = []; g_data = []
    for s_mult in [0.5, 1.0, 2.0, 5.0]:
        s = strength * s_mult
        field_mb, _ = make_field_2d(pos, nmap, gl, 8, s, n)
        am_m = prop(field_mb, K, blocked)
        pm_m = sum(abs(am_m[d])**2 for d in det)
        if pm_m > 1e-30:
            ym_m = sum(abs(am_m[d])**2*pos[d][1] for d in det)/pm_m
            delta = abs(ym_m - yf)
            if delta > 1e-10: m_data.append(s_mult); g_data.append(delta)
    results["fm_alpha"] = math.nan
    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]; ly = [math.log(g) for g in g_data]
        nn2 = len(lx); mx_l = sum(lx)/nn2; my_l = sum(ly)/nn2
        sxx = sum((x-mx_l)**2 for x in lx); sxy = sum((x-mx_l)*(y-my_l) for x,y in zip(lx,ly))
        results["fm_alpha"] = sxy/sxx if sxx > 1e-10 else 0

    return results


def run_3d_harness(
    action_type,
    phys_l=12,
    phys_w=6,
    h=1.0,
    strength=0.0001,
    slit_a=(2, 0),
    slit_b=(-2, 0),
    slit_c=(0, 1),
    mass_z=6,
):
    """3D barrier card plus no-barrier distance/mass companion on one family."""
    pos, adj, nl, hw, nmap = generate_3d_nn_lattice(phys_l, phys_w, h)
    n = len(pos)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    bl = nl // 3
    gl = 2 * nl // 3
    barrier = [nmap[(bl, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]

    try:
        sa = [nmap[(bl, slit_a[0], slit_a[1])]]
        sb = [nmap[(bl, slit_b[0], slit_b[1])]]
        sc = [nmap[(bl, slit_c[0], slit_c[1])]]
    except KeyError:
        return None

    blocked = set(barrier) - set(sa + sb)
    field_f = [0.0] * n
    prop = lambda f, k, bl_set: propagate_3d(pos, adj, f, k, bl_set, n, action_type)

    results = {
        "action": action_type,
        "dim": 3,
        "h": h,
        "n": n,
        "barrier_slits": (slit_a, slit_b, slit_c),
    }

    # Barrier-card gravity and k=0 on z centroid.
    field_m, _ = make_field_3d(pos, nmap, gl, mass_z, strength, hw, n)
    af = prop(field_f, K, blocked)
    am = prop(field_m, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return None
    zf = sum(abs(af[d]) ** 2 * pos[d][2] for d in det) / pf
    zm = sum(abs(am[d]) ** 2 * pos[d][2] for d in det) / pm
    results["gravity"] = zm - zf

    am0 = prop(field_m, 0.0, blocked)
    af0 = prop(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    results["k0"] = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        results["k0"] = (
            sum(abs(am0[d]) ** 2 * pos[d][2] for d in det) / pm0
            - sum(abs(af0[d]) ** 2 * pos[d][2] for d in det) / pf0
        )

    # Barrier-card MI, d_TV, and CL purity using y-bins for consistency with the 2D scorer.
    pa = prop(field_f, K, blocked | set(sb))
    pb = prop(field_f, K, blocked | set(sa))
    na = sum(abs(pa[d]) ** 2 for d in det)
    nb = sum(abs(pb[d]) ** 2 for d in det)
    if na < 1e-30 or nb < 1e-30:
        return None

    bw = 2 * (phys_w + h) / N_YBINS
    prob_a = [0.0] * N_YBINS
    prob_b = [0.0] * N_YBINS
    da = {}
    db = {}
    for d in det:
        y = pos[d][1]
        b2 = max(0, min(N_YBINS - 1, int((y + phys_w + h) / bw)))
        pa2 = abs(pa[d]) ** 2
        pb2 = abs(pb[d]) ** 2
        prob_a[b2] += pa2
        prob_b[b2] += pb2
        da[d] = pa2
        db[d] = pb2

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
    results["MI"] = H - Hc
    results["d_TV"] = 0.5 * sum(abs(da[d] / na - db[d] / nb) for d in det)

    env_depth = max(1, round(nl / 6))
    st = bl + 1
    sp = min(nl - 1, st + env_depth)
    mid = [
        nmap[(l, iy, iz)]
        for l in range(st, sp)
        for iy in range(-hw, hw + 1)
        for iz in range(-hw, hw + 1)
    ]
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid:
        y = pos[m][1]
        b2 = max(0, min(N_YBINS - 1, int((y + phys_w + h) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA = sum(abs(a) ** 2 for a in ba)
    NB = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (
                pa[d1].conjugate() * pa[d2]
                + pb[d1].conjugate() * pb[d2]
                + Dcl * pa[d1].conjugate() * pb[d2]
                + Dcl * pb[d1].conjugate() * pa[d2]
            )
    tr = sum(rho[(d, d)] for d in det).real
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        results["pur_cl"] = sum(abs(v) ** 2 for v in rho.values()).real
    else:
        results["pur_cl"] = 1.0

    # Born companion on the same barrier geometry with a genuine third slit.
    results["born"] = math.nan
    all_s = set(sa + sb + sc)
    other = set(barrier) - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(sa + sb)),
        ("ac", set(sa + sc)),
        ("bc", set(sb + sc)),
        ("a", set(sa)),
        ("b", set(sb)),
        ("c", set(sc)),
    ]:
        bl2 = other | (all_s - open_set)
        a = prop(field_f, K, bl2)
        probs[key] = [abs(a[d]) ** 2 for d in det]
    I3 = 0.0
    P = 0.0
    for di in range(len(det)):
        i3 = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        I3 += abs(i3)
        P += probs["abc"][di]
    results["born"] = I3 / P if P > 1e-30 else math.nan
    results["born_signal"] = P
    results["slit_a_signal"] = na
    results["slit_b_signal"] = nb

    # No-barrier companion distance law on z centroid.
    af_nb = prop(field_f, K, set())
    pf_nb = sum(abs(af_nb[d]) ** 2 for d in det)
    zf_nb = sum(abs(af_nb[d]) ** 2 * pos[d][2] for d in det) / pf_nb if pf_nb > 1e-30 else 0.0
    b_data = []
    d_data = []
    for b_phys in [2, 3, 4, 5, 6]:
        field_mb, _ = make_field_3d(pos, nmap, gl, b_phys, strength, hw, n)
        am_nb = prop(field_mb, K, set())
        pm_nb = sum(abs(am_nb[d]) ** 2 for d in det)
        if pm_nb > 1e-30:
            zm_nb = sum(abs(am_nb[d]) ** 2 * pos[d][2] for d in det) / pm_nb
            b_data.append(b_phys)
            d_data.append(abs(zm_nb - zf_nb))
    results["dist_exp"], results["dist_r2"] = fit_power_law(b_data, d_data)

    # No-barrier mass response on the same 3D family.
    m_data = []
    g_data = []
    for s_mult in [0.5, 1.0, 2.0, 5.0]:
        field_mb, _ = make_field_3d(pos, nmap, gl, mass_z, strength * s_mult, hw, n)
        am_nb = prop(field_mb, K, set())
        pm_nb = sum(abs(am_nb[d]) ** 2 for d in det)
        if pm_nb > 1e-30:
            zm_nb = sum(abs(am_nb[d]) ** 2 * pos[d][2] for d in det) / pm_nb
            delta = abs(zm_nb - zf_nb)
            if delta > 1e-12:
                m_data.append(s_mult)
                g_data.append(delta)
    results["fm_alpha"], results["fm_r2"] = fit_power_law(m_data, g_data)

    return results


def print_card(r):
    if r is None:
        print("  FAIL")
        return
    print(f"  Action: {r['action']}, {r['dim']}D, h={r['h']}, nodes={r['n']}")
    born_s = f"{r['born']:.2e}" if not math.isnan(r['born']) else "nan"
    dist_s = f"{r['dist_exp']:.2f}" if not math.isnan(r['dist_exp']) else "nan"
    fm_s = f"{r['fm_alpha']:.2f}" if not math.isnan(r['fm_alpha']) else "nan"
    print(f"  Born={born_s}  k=0={r['k0']:+.2e}  MI={r.get('MI',0):.4f}  "
          f"d_TV={r.get('d_TV',0):.4f}  1-pur={1-r.get('pur_cl',1):.4f}")
    print(f"  gravity={r['gravity']:+.6f}  dist={dist_s}(R²={r['dist_r2']:.3f})  "
          f"F∝M={fm_s}")


def main():
    print("=" * 90)
    print("CANONICAL ACTION-POWER HARNESS")
    print("Same fixed harness, same scorer, two action families.")
    print("NOTE: Changed action = axiom fork. No inherited claims.")
    print("=" * 90)
    print()

    # 2D spent-delay baseline
    print("2D SPENT-DELAY BASELINE (h=1.0, strength=0.001):")
    r = run_2d_harness('spent_delay', strength=0.001)
    print_card(r)
    print()

    # 2D power action p=0.5
    print("2D POWER ACTION p=0.5 (h=1.0, strength=0.001):")
    r = run_2d_harness('power', strength=0.001)
    print_card(r)
    print()

    # 2D spent-delay ultra-weak
    print("2D SPENT-DELAY ULTRA-WEAK (h=1.0, strength=0.0001):")
    r = run_2d_harness('spent_delay', strength=0.0001)
    print_card(r)
    print()

    # 2D power ultra-weak
    print("2D POWER p=0.5 ULTRA-WEAK (h=1.0, strength=0.0001):")
    r = run_2d_harness('power', strength=0.0001)
    print_card(r)
    print()

    print("3D SPENT-DELAY CLOSE-SLIT BARRIER CARD (L=12, W=6, strength=0.0001):")
    r = run_3d_harness('spent_delay', strength=0.0001)
    print_card(r)
    print("  NOTE: distance and F∝M above are the no-barrier companion on the same 3D family.")
    print(
        f"  close-slit barrier: slits={r['barrier_slits']}  "
        f"slit_signals=({r['slit_a_signal']:.3e}, {r['slit_b_signal']:.3e})  "
        f"Born_signal={r['born_signal']:.3e}"
    )
    print()

    print("3D POWER ACTION p=0.5 CLOSE-SLIT BARRIER CARD (L=12, W=6, strength=0.0001):")
    r = run_3d_harness('power', strength=0.0001)
    print_card(r)
    print("  NOTE: distance and F∝M above are the no-barrier companion on the same 3D family.")
    print(
        f"  close-slit barrier: slits={r['barrier_slits']}  "
        f"slit_signals=({r['slit_a_signal']:.3e}, {r['slit_b_signal']:.3e})  "
        f"Born_signal={r['born_signal']:.3e}"
    )
    print()


if __name__ == "__main__":
    main()
