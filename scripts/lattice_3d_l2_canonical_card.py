#!/usr/bin/env python3
"""Frozen 3D 1/L^2 card at h=0.25.

This is a reviewer-facing eight-property harness for the 3D ordered-lattice
`1/L^2` branch at one fixed retained resolution. It is a useful trust-building
artifact, but it is not a full same-family closure theorem.

Architecture:
  - 3D dense lattice, W=10, L=12, h=0.25
  - max_d_phys=3 → max_d=12 lattice units → 625 edges/center node
  - Kernel: exp(ikS) * w * h^2 / L^2 (spent-delay action, h^2 measure)
  - Field: s/r with s=5e-5 (ultra-weak)
  - Slits: y >= 0.5 (upper), y <= -0.5 (lower)
  - Mass: z-offset for gravity/distance

Measured here:
  1. Born |I3|/P (3-slit Sorkin test)
  2. d_TV (total variation distance between slit distributions)
  3. k=0 control (gravity vanishes at k=0)
  4. F∝M (mass scaling exponent)
  5. Gravity sign (TOWARD/AWAY at z=3)
  6. Decoherence (CL bath purity)
  7. MI (mutual information between slit choice and detector)
  8. Distance law (deflection vs mass position, z=2..9)

Intentionally not measured in this fixed-resolution card:
  - purity scaling vs lattice length
  - gravity growth vs lattice length
Those require separate multi-size runs and stay in companion harnesses.
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
        self.phys_w = phys_w
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._h_measure = h * h

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
        n = self.n
        hw = self.hw
        nl = self.nl
        nw = self._nw
        hm = self._h_measure

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
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)

                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue

                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                dl = L * (1 + lf)
                ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
                act = dl - ret
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
    sxx = np.sum((lx - mx)**2)
    sxy = np.sum((lx - mx) * (ly - my))
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
    print("FROZEN 3D 1/L^2 CARD (8 measured properties)")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers, {lat.npl} npl")
    print(f"  Kernel: exp(ikS) * w * h^2 / L^2 (spent-delay)")
    print("=" * 70)
    print()

    # Free-field baseline
    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Free propagation: {time.time()-t0:.1f}s")
    print()

    # ===== 1. BORN =====
    t0 = time.time()
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
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di]
                  + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    status = "PASS" if born < 1e-10 else "FAIL"
    print(f"  1. Born |I3|/P = {born:.2e}  [{status}]  ({time.time()-t0:.0f}s)")

    # ===== 2. d_TV =====
    t0 = time.time()
    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = {d: abs(pa[d])**2 for d in det}
    db = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d] / na2 - db[d] / nb2) for d in det)
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]  ({time.time()-t0:.0f}s)")

    # ===== 3. k=0 =====
    field_m3, _ = make_field(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det)
    pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d])**2 * pos[d, 2] for d in det) / pf0)
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # ===== 4. F∝M =====
    t0 = time.time()
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
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
    print(f"  4. F~M alpha = {fm_alpha:.2f}  ({time.time()-t0:.0f}s)")

    # ===== 5. Gravity sign =====
    am3 = lat.propagate(field_m3, K, blocked)
    pm3 = sum(abs(am3[d])**2 for d in det)
    grav = 0
    if pm3 > 1e-30:
        zm3 = sum(abs(am3[d])**2 * pos[d, 2] for d in det) / pm3
        grav = zm3 - zf
    dr = "TOWARD" if grav > 0 else "AWAY"
    print(f"  5. Gravity z=3 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # ===== 6. Decoherence =====
    bw = 2 * (PHYS_W + 1) / N_YBINS
    ed = max(1, round(lat.nl / 6)); st = bl + 1; sp = min(lat.nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([lat.nmap[(l, iy, iz)]
                     for iy in range(-lat.hw, lat.hw + 1)
                     for iz in range(-lat.hw, lat.hw + 1)
                     if (l, iy, iz) in lat.nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
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
                             + Dcl * pa[d1].conjugate() * pb[d2]
                             + Dcl * pb[d1].conjugate() * pa[d2])
    tr = sum(rho[(d, d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho:
            rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
    decoh = 100 * (1 - pur)
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # ===== 7. MI =====
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + PHYS_W + 1) / bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na3 = prob_a.sum(); nb3 = prob_b.sum()
    MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        H_val = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H_val -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H_val - Hc
    print(f"  7. MI = {MI:.4f} bits  [{'PASS' if MI > 0.05 else 'WEAK'}]")

    # ===== Companion-only properties =====
    print("  Companion-only: purity scaling / gravity-vs-N require multi-size runs")

    # ===== 8. Distance law =====
    t0 = time.time()
    max_z = min(int(PHYS_W * 0.9), lat.hw)
    z_values = list(range(2, max_z + 1))
    b_data = []; d_data = []
    print(f"  8. Distance law (z={z_values[0]}..{z_values[-1]}):")
    for z_mass in z_values:
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)

    n_tw = len(b_data)
    print(f"      TOWARD: {n_tw}/{len(z_values)}")

    if len(b_data) >= 3:
        d_arr = np.array(d_data)
        peak_i = int(np.argmax(d_arr))
        # Fit tail (after peak)
        if peak_i < len(b_data) - 2:
            tail_b = b_data[peak_i:]
            tail_d = d_data[peak_i:]
            slope, r2 = fit_power(tail_b, tail_d)
            if slope is not None:
                print(f"      Tail (z>={b_data[peak_i]}): b^({slope:.2f}), R²={r2:.3f}")
        # Fit all
        slope2, r22 = fit_power(b_data, d_data)
        if slope2 is not None:
            print(f"      All TOWARD: b^({slope2:.2f}), R²={r22:.3f}")

    print(f"      ({time.time()-t0:.0f}s)")

    # ===== Summary =====
    print()
    print("=" * 70)
    print("SUMMARY")
    print(f"  Born:         {born:.2e}")
    print(f"  d_TV:         {dtv:.4f}")
    print(f"  k=0:          {gk0:.6f}")
    print(f"  F~M alpha:    {fm_alpha:.2f}")
    print(f"  Gravity:      {grav:+.6f} ({dr})")
    print(f"  Decoherence:  {decoh:.1f}%")
    print(f"  MI:           {MI:.4f} bits")
    print(f"  Distance:     {n_tw}/{len(z_values)} TOWARD")
    print(f"  Total time:   {time.time()-t_total:.0f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
