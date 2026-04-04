#!/usr/bin/env python3
"""CANONICAL 3D VALLEY-LINEAR CARD at h=0.25 — frozen harness.

Action: S = L(1-f) — phase valley, linear in field f
Kernel: 1/L^2 with h^2 measure
Architecture: 3D dense lattice, W=10, L=12, h=0.25

All 10 properties measured.
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 10
PHYS_L = 12
H = 0.25
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h

        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; hw = self.hw; nl = self.nl; nw = self._nw; hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                # Valley-linear action: S = L(1-f)
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field(lat, z_mass_phys, strength):
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx)**2 + (lat.pos[:, 1] - my)**2 +
                (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def setup_slits(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def fit_power(b_data, d_data):
    if len(b_data) < 3:
        return None, None
    lx = np.log(np.array(b_data, dtype=float))
    ly = np.log(np.array(d_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx)**2); sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx)))**2)
    ss_tot = np.sum((ly - my)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def main():
    t_total = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    gl = 2 * lat.nl // 3
    bi, sa, sb, blocked, bl = setup_slits(lat)
    pos = lat.pos
    field_f = np.zeros(lat.n)

    print("=" * 70)
    print("CANONICAL 3D VALLEY-LINEAR CARD")
    print(f"  Action: S = L(1-f)")
    print(f"  Kernel: 1/L^2, h^2 measure")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers")
    print("=" * 70)
    print()

    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Free propagation: {time.time()-t0:.1f}s\n")

    # 1. Born
    t0 = time.time()
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a + s_b)),
                               ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    print(f"  1. Born |I3|/P = {born:.2e}  [{'PASS' if born < 1e-10 else 'FAIL'}]  ({time.time()-t0:.0f}s)")

    # 2. d_TV
    t0 = time.time()
    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = {d: abs(pa[d])**2 for d in det}; db_ = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[d]/na2 - db_[d]/nb2) for d in det) if na2 > 1e-30 and nb2 > 1e-30 else 0
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]  ({time.time()-t0:.0f}s)")

    # 3. k=0
    field_m3, _ = make_field(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d])**2 * pos[d, 2] for d in det) / pf0)
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # 4. F∝M
    t0 = time.time()
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked); pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s); g_data.append(delta)
    fm_alpha = float('nan')
    if len(m_data) >= 3:
        slope, _ = fit_power(m_data, g_data)
        if slope is not None:
            fm_alpha = slope
    print(f"  4. F~M alpha = {fm_alpha:.2f}  [{'PASS' if abs(fm_alpha - 1.0) < 0.2 else 'CHECK'}]  ({time.time()-t0:.0f}s)")

    # 5. Gravity sign
    am3 = lat.propagate(field_m3, K, blocked); pm3 = sum(abs(am3[d])**2 for d in det)
    grav = (sum(abs(am3[d])**2 * pos[d, 2] for d in det) / pm3 - zf) if pm3 > 1e-30 else 0
    dr = "TOWARD" if grav > 0 else "AWAY"
    print(f"  5. Gravity z=3 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # 6. Decoherence
    bw = 2 * (PHYS_W + 1) / N_YBINS
    ed = max(1, round(lat.nl / 6)); st = bl + 1; sp = min(lat.nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([lat.nmap[(l, iy, iz)] for iy in range(-lat.hw, lat.hw + 1)
                     for iz in range(-lat.hw, lat.hw + 1) if (l, iy, iz) in lat.nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128); bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + PHYS_W + 1) / bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba - bb)**2))
    NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1, d2)] = (pa[d1].conjugate() * pa[d2] + pb[d1].conjugate() * pb[d2]
                             + Dcl * pa[d1].conjugate() * pb[d2] + Dcl * pb[d1].conjugate() * pa[d2])
    tr = sum(rho[(d, d)] for d in det).real; pur = 1.0
    if tr > 1e-30:
        for key in rho: rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
    decoh = 100 * (1 - pur)
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # 7. MI
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + PHYS_W + 1) / bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na3 = prob_a.sum(); nb3 = prob_b.sum(); MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        H_val = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30: H_val -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H_val - Hc
    print(f"  7. MI = {MI:.4f} bits  [{'PASS' if MI > 0.05 else 'WEAK'}]")

    # 8. Purity scaling + 9. Gravity grows (at h=0.5 for speed)
    print(f"  8-9. Multi-L test (h=0.5 for speed):")
    grav_data = {}; pur_data = {}
    for pl in [8, 10, 12, 15]:
        lat2 = Lattice3D(pl, 6, 0.5)
        det2 = [lat2.nmap[(lat2.nl-1, iy, iz)] for iy in range(-lat2.hw, lat2.hw+1)
                for iz in range(-lat2.hw, lat2.hw+1)]
        gl2 = 2*lat2.nl//3; bl2 = lat2.nl//3
        bi2 = []
        for iy in range(-lat2.hw, lat2.hw+1):
            for iz in range(-lat2.hw, lat2.hw+1):
                idx = lat2.nmap.get((bl2, iy, iz))
                if idx is not None: bi2.append(idx)
        sa2 = [i for i in bi2 if lat2.pos[i, 1] >= 0.5]
        sb2 = [i for i in bi2 if lat2.pos[i, 1] <= -0.5]
        bk2 = set(bi2) - set(sa2 + sb2)
        ff2 = np.zeros(lat2.n)
        af2 = lat2.propagate(ff2, K, bk2)
        pf2 = sum(abs(af2[d])**2 for d in det2)
        zf2 = sum(abs(af2[d])**2 * lat2.pos[d, 2] for d in det2) / pf2
        # Gravity
        iz_m = round(3 / 0.5); mi2 = lat2.nmap.get((gl2, 0, iz_m))
        if mi2 is not None:
            r2 = np.sqrt((lat2.pos[:, 0]-lat2.pos[mi2, 0])**2 + (lat2.pos[:, 1]-lat2.pos[mi2, 1])**2 +
                          (lat2.pos[:, 2]-lat2.pos[mi2, 2])**2) + 0.1
            fm2 = STRENGTH / r2
            am2 = lat2.propagate(fm2, K, bk2); pm2 = sum(abs(am2[d])**2 for d in det2)
            if pm2 > 1e-30:
                grav_data[pl] = sum(abs(am2[d])**2 * lat2.pos[d, 2] for d in det2) / pm2 - zf2
        # Purity
        pa2 = lat2.propagate(ff2, K, bk2 | set(sb2)); pb2 = lat2.propagate(ff2, K, bk2 | set(sa2))
        bw2 = 2 * 7 / N_YBINS
        ed2 = max(1, round(lat2.nl/6)); st2 = bl2+1; sp2 = min(lat2.nl-1, st2+ed2)
        mid2 = []
        for l in range(st2, sp2):
            mid2.extend([lat2.nmap[(l, iy, iz)] for iy in range(-lat2.hw, lat2.hw+1)
                         for iz in range(-lat2.hw, lat2.hw+1) if (l, iy, iz) in lat2.nmap])
        ba2 = np.zeros(N_YBINS, dtype=np.complex128); bb2 = np.zeros(N_YBINS, dtype=np.complex128)
        for m in mid2:
            b2_ = max(0, min(N_YBINS-1, int((lat2.pos[m, 1]+7)/bw2)))
            ba2[b2_] += pa2[m]; bb2[b2_] += pb2[m]
        S2 = float(np.sum(np.abs(ba2-bb2)**2))
        NA4 = float(np.sum(np.abs(ba2)**2)); NB4 = float(np.sum(np.abs(bb2)**2))
        Sn2 = S2/(NA4+NB4) if (NA4+NB4) > 0 else 0
        Dcl2 = math.exp(-LAM**2*Sn2)
        rho2 = {}
        for d1 in det2:
            for d2 in det2:
                rho2[(d1,d2)] = (pa2[d1].conjugate()*pa2[d2]+pb2[d1].conjugate()*pb2[d2]
                                +Dcl2*pa2[d1].conjugate()*pb2[d2]+Dcl2*pb2[d1].conjugate()*pa2[d2])
        tr2 = sum(rho2[(d,d)] for d in det2).real; pur2 = 1.0
        if tr2 > 1e-30:
            for key in rho2: rho2[key] /= tr2
            pur2 = sum(abs(v)**2 for v in rho2.values()).real
        pur_data[pl] = 1-pur2

    for pl in sorted(grav_data):
        dr2 = "T" if grav_data[pl] > 0 else "A"
        print(f"       L={pl}: grav={grav_data[pl]:+.6f}({dr2}), 1-pur={pur_data.get(pl,0):.4f}")
    vals = sorted(grav_data.items())
    grows = len(vals) >= 2 and vals[-1][1] > vals[0][1]
    print(f"  8. Purity: stable ~{np.mean(list(pur_data.values())):.1%}")
    print(f"  9. Gravity grows: {'YES' if grows else 'NO'}  [{'PASS' if grows else 'CHECK'}]")

    # 10. Distance law
    t0 = time.time()
    b_data = []; d_data = []
    print(f"  10. Distance law:")
    for z_mass in range(2, 10):
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked); pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0: b_data.append(z_mass); d_data.append(delta)
    n_tw = len(b_data)
    print(f"      TOWARD: {n_tw}/8")
    if len(b_data) >= 3:
        d_arr = np.array(d_data); peak_i = int(np.argmax(d_arr))
        if peak_i < len(b_data) - 2:
            slope, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
            if slope is not None:
                print(f"      Tail (z>={b_data[peak_i]}): b^({slope:.2f}), R²={r2:.3f}")
    print(f"      ({time.time()-t0:.0f}s)")

    # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY — Valley-linear S=L(1-f), 1/L^2, h={H}")
    print(f"  Born:         {born:.2e}")
    print(f"  d_TV:         {dtv:.4f}")
    print(f"  k=0:          {gk0:.6f}")
    print(f"  F~M alpha:    {fm_alpha:.2f}")
    print(f"  Gravity:      {grav:+.6f} ({dr})")
    print(f"  Decoherence:  {decoh:.1f}%")
    print(f"  MI:           {MI:.4f} bits")
    print(f"  Distance:     {n_tw}/8 TOWARD")
    print(f"  Total time:   {time.time()-t_total:.0f}s")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
