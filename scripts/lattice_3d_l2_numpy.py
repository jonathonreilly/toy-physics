#!/usr/bin/env python3
"""3D dense lattice with 1/L^2 kernel — numpy-optimized for h=0.25.

Numpy acceleration: pre-compute edge arrays (src, dst, weight, action)
then propagate layer-by-layer using vectorized scatter-add.

Target: confirm distance exponent steepens toward -2 at h=0.25.
"""

from __future__ import annotations
import math
import time
import numpy as np
from collections import defaultdict

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8


def generate(phys_l, phys_w, max_d_phys, h=1.0):
    """Generate lattice and return numpy-friendly edge arrays."""
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    max_d = max(1, round(max_d_phys / h))
    npl = (2 * hw + 1) ** 2  # nodes per layer
    n = nl * npl

    # Positions: (x, y, z) for each node
    pos = np.zeros((n, 3))
    nmap = {}
    idx = 0
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                pos[idx] = (x, iy * h, iz * h)
                nmap[(layer, iy, iz)] = idx
                idx += 1

    # Build edge lists per layer transition
    # edges[layer] = list of (src_idx, dst_idx)
    edge_src = []
    edge_dst = []
    edge_layer = []  # which layer transition this edge belongs to

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
                            edge_src.append(si)
                            edge_dst.append(di)
                            edge_layer.append(layer)

    edge_src = np.array(edge_src, dtype=np.int64)
    edge_dst = np.array(edge_dst, dtype=np.int64)
    edge_layer = np.array(edge_layer, dtype=np.int64)

    # Pre-compute geometric quantities for each edge
    dp = pos[edge_dst] - pos[edge_src]  # (n_edges, 3)
    L = np.sqrt(np.sum(dp ** 2, axis=1))
    L = np.maximum(L, 1e-10)
    transverse = np.sqrt(dp[:, 1] ** 2 + dp[:, 2] ** 2)
    theta = np.arctan2(transverse, np.maximum(dp[:, 0], 1e-10))
    w = np.exp(-BETA * theta ** 2)

    return {
        'pos': pos, 'nmap': nmap, 'nl': nl, 'hw': hw, 'n': n, 'npl': npl,
        'edge_src': edge_src, 'edge_dst': edge_dst, 'edge_layer': edge_layer,
        'L': L, 'w': w, 'max_d': max_d,
    }


def propagate_l2(lat, field, k, blocked_set):
    """Vectorized propagation with 1/L^2 kernel."""
    n = lat['n']
    nl = lat['nl']
    amps = np.zeros(n, dtype=np.complex128)

    # Find source
    dists = np.sum(lat['pos'] ** 2, axis=1)
    src = np.argmin(dists)
    amps[src] = 1.0

    # Create blocked mask
    blocked = np.zeros(n, dtype=bool)
    for b in blocked_set:
        blocked[b] = True

    # Pre-compute field at edges
    edge_field = 0.5 * (field[lat['edge_src']] + field[lat['edge_dst']])
    L = lat['L']
    dl = L * (1 + edge_field)
    ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
    act = dl - ret

    # Edge kernel: exp(ikS) * w / L^2
    phase = np.exp(1j * k * act) * lat['w'] / (L * L)

    # Propagate layer by layer
    for layer in range(nl - 1):
        mask = lat['edge_layer'] == layer
        e_src = lat['edge_src'][mask]
        e_dst = lat['edge_dst'][mask]
        e_phase = phase[mask]

        # Source amplitudes (zero out blocked)
        src_amps = amps[e_src].copy()
        src_amps[blocked[e_src]] = 0

        # Contributions
        contrib = src_amps * e_phase

        # Scatter add to destinations (skip blocked destinations)
        dst_blocked = blocked[e_dst]
        contrib[dst_blocked] = 0

        # Use np.add.at for scatter add
        np.add.at(amps, e_dst, contrib)

    return amps


def make_field(lat, z_mass_phys, strength, h):
    pos = lat['pos']
    n = lat['n']
    gl = 2 * lat['nl'] // 3
    iz = round(z_mass_phys / h)
    mi = lat['nmap'].get((gl, 0, iz))
    if mi is None:
        return np.zeros(n), None
    mx, my, mz = pos[mi]
    r = np.sqrt((pos[:, 0] - mx) ** 2 + (pos[:, 1] - my) ** 2 + (pos[:, 2] - mz) ** 2) + 0.1
    field = strength / r
    return field, mi


def setup_slits(lat):
    pos = lat['pos']
    nmap = lat['nmap']
    nl = lat['nl']
    hw = lat['hw']
    bl = nl // 3
    bi = []
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i, 1] >= 0.5]
    sb = [i for i in bi if pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def run_card(phys_l, phys_w, max_d_phys, h, strength):
    t0 = time.time()
    lat = generate(phys_l, phys_w, max_d_phys, h)
    n = lat['n']
    nl = lat['nl']
    hw = lat['hw']
    nmap = lat['nmap']
    pos = lat['pos']
    t_gen = time.time() - t0

    det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
           for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
    gl = 2 * nl // 3
    bi, sa, sb, blocked, bl = setup_slits(lat)

    n_edges = len(lat['edge_src'])
    print(f"\n{'='*70}")
    print(f"3D DENSE + 1/L^2 KERNEL (h={h})")
    print(f"  {n} nodes, {nl} layers, {n_edges} edges")
    print(f"  Generated in {t_gen:.1f}s")
    print(f"{'='*70}\n")

    field_f = np.zeros(n)

    # Free-field propagation
    t1 = time.time()
    af = propagate_l2(lat, field_f, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL")
        return
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf
    t_prop = time.time() - t1
    print(f"  Free propagation: {t_prop:.1f}s")

    # 1. Born (3-slit)
    t1 = time.time()
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a + s_b)),
                               ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = propagate_l2(lat, field_f, K, bl2)
            probs[key] = np.array([abs(a[d]) ** 2 for d in det])
        I3 = 0; P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    status = "PASS" if born < 1e-10 else "FAIL"
    t_born = time.time() - t1
    print(f"  1. Born |I3|/P = {born:.2e}  [{status}] ({t_born:.1f}s)")

    # 2. d_TV
    t1 = time.time()
    pa = propagate_l2(lat, field_f, K, blocked | set(sb))
    pb = propagate_l2(lat, field_f, K, blocked | set(sa))
    da = {d: abs(pa[d]) ** 2 for d in det}
    db = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)
    print(f"  2. d_TV = {dtv:.4f}")

    # 3. k=0
    field_m, _ = make_field(lat, 3, strength, h)
    am0 = propagate_l2(lat, field_m, 0.0, blocked)
    af0 = propagate_l2(lat, field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d]) ** 2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d]) ** 2 * pos[d, 2] for d in det) / pf0)
    print(f"  3. k=0 = {gk0:.6f}")

    # 5. Gravity at z=3
    am = propagate_l2(lat, field_m, K, blocked)
    pm = sum(abs(am[d]) ** 2 for d in det)
    grav = 0
    if pm > 1e-30:
        zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
        grav = zm - zf
    print(f"  5. Gravity z=3: {grav:+.6f} ({'TOWARD' if grav > 0 else 'AWAY'})")

    # 4. F∝M
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 3, s, h)
        am2 = propagate_l2(lat, fm, K, blocked)
        pm2 = sum(abs(am2[d]) ** 2 for d in det)
        if pm2 > 1e-30:
            zm2 = sum(abs(am2[d]) ** 2 * pos[d, 2] for d in det) / pm2
            delta = zm2 - zf
            if delta > 0:
                m_data.append(s); g_data.append(delta)
    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]
        ly = [math.log(g) for g in g_data]
        nn2 = len(lx); mx_l = sum(lx) / nn2; my_l = sum(ly) / nn2
        sxx = sum((x - mx_l) ** 2 for x in lx)
        sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
        fm_alpha = sxy / sxx if sxx > 1e-10 else 0
        print(f"  4. F~M alpha = {fm_alpha:.2f}")
    else:
        print(f"  4. F~M: too few TOWARD points ({len(m_data)})")

    # 6-7: Decoherence + MI
    bw = 2 * (phys_w + 1) / N_YBINS
    ed = max(1, round(nl / 6)); st = bl + 1; sp = min(nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([nmap[(l, iy, iz)] for iy in range(-hw, hw + 1)
                    for iz in range(-hw, hw + 1) if (l, iy, iz) in nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + phys_w + 1) / bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = np.sum(np.abs(ba - bb) ** 2)
    NA3 = np.sum(np.abs(ba) ** 2); NB3 = np.sum(np.abs(bb) ** 2)
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM ** 2 * float(Sn))
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (pa[d1].conjugate() * pa[d2] + pb[d1].conjugate() * pb[d2]
                             + Dcl * pa[d1].conjugate() * pb[d2]
                             + Dcl * pb[d1].conjugate() * pa[d2])
    tr = sum(rho[(d, d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur = sum(abs(v) ** 2 for v in rho.values()).real
    decoh = 100 * (1 - pur)
    print(f"  6. Decoherence = {decoh:.1f}%")

    prob_a = np.zeros(N_YBINS)
    prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + phys_w + 1) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na3 = prob_a.sum(); nb3 = prob_b.sum()
    MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                MI -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                MI += 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                MI += 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = -MI  # H(Y) - H(Y|X)
    # Fix: MI = H - Hc
    MI2 = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI2 = H - Hc
    print(f"  7. MI = {MI2:.4f} bits")

    # 10. Distance law
    t1 = time.time()
    b_data = []; d_data = []
    max_z = int(phys_w * 0.9)
    z_values = [z for z in range(2, max_z + 1)]
    print(f"  10. Distance law (s={strength:.0e}):")
    for z_mass in z_values:
        fm, _ = make_field(lat, z_mass, strength, h)
        am2 = propagate_l2(lat, fm, K, blocked)
        pm2 = sum(abs(am2[d]) ** 2 for d in det)
        if pm2 > 1e-30:
            zm2 = sum(abs(am2[d]) ** 2 * pos[d, 2] for d in det) / pm2
            delta = zm2 - zf
            sign = "TOWARD" if delta > 0 else "AWAY"
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)

    # Fit to tail (after peak)
    if len(b_data) >= 3:
        peak_i = max(range(len(d_data)), key=lambda i: d_data[i])
        tail_b = b_data[peak_i:]
        tail_d = d_data[peak_i:]
        if len(tail_b) >= 3:
            lx = [math.log(b) for b in tail_b]
            ly = [math.log(d) for d in tail_d]
            nn2 = len(lx); mx_l = sum(lx) / nn2; my_l = sum(ly) / nn2
            sxx = sum((x - mx_l) ** 2 for x in lx)
            sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
            slope = sxy / sxx if sxx > 1e-10 else 0
            ss_res = sum((y - (my_l + slope * (x - mx_l))) ** 2 for x, y in zip(lx, ly))
            ss_tot = sum((y - my_l) ** 2 for y in ly)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            print(f"      Tail (z>={tail_b[0]}): b^({slope:.2f}), R²={r2:.3f}")
        # Also fit ALL positive
        lx = [math.log(b) for b in b_data]
        ly = [math.log(d) for d in d_data]
        nn2 = len(lx); mx_l = sum(lx) / nn2; my_l = sum(ly) / nn2
        sxx = sum((x - mx_l) ** 2 for x in lx)
        sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
        slope = sxy / sxx if sxx > 1e-10 else 0
        print(f"      All TOWARD: b^({slope:.2f})")
    t_dist = time.time() - t1
    print(f"      Distance time: {t_dist:.1f}s")

    total = time.time() - t0
    print(f"\n  TOTAL TIME: {total:.0f}s")


def main():
    # h=1.0: baseline
    run_card(12, 6, 3, 1.0, 5e-5)

    # h=0.5: confirmed TOWARD
    run_card(12, 6, 3, 0.5, 5e-5)

    # h=0.5 wider: for distance law tail
    run_card(15, 8, 3, 0.5, 5e-5)

    # h=0.25: the critical test
    # ~117k nodes, ~73M edges. Try with smaller lattice first.
    print("\n\n" + "=" * 70)
    print("h=0.25 TEST (smaller lattice: L=10, W=5)")
    print("=" * 70)
    run_card(10, 5, 3, 0.25, 5e-5)


if __name__ == "__main__":
    main()
