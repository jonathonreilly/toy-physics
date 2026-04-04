#!/usr/bin/env python3
"""Frozen robustness sweep: valley-linear S=L(1-f), 1/L^2 kernel, 3D.

Sweeps W, max_d, L at h=0.5. Reports Born, d_TV, MI, decoherence,
gravity, F∝M, distance tail for each configuration.

Also: 2D comparison and 4D valley-linear + 1/L^3 check.
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
STRENGTH = 5e-5


class Lattice3D:
    def __init__(self, phys_l, phys_w, max_d_phys, h):
        self.h = h; self.nl = int(phys_l / h) + 1; self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        nw = 2 * self.hw + 1; self.npl = nw ** 2; self.n = self.nl * self.npl
        self._hm = h * h
        self.pos = np.zeros((self.n, 3)); self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for l in range(self.nl):
            self._ls[l] = idx; x = l * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(l, iy, iz)] = idx; idx += 1
        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h; dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                self._off.append((dy, dz, L, math.exp(-BETA * theta * theta)))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nw = self._nw; nl = self.nl; hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0); amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set: blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]; ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy(); sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30: continue
            sf = field[ls:ls + self.npl]; df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM: continue
                yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz): continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def setup_and_measure(pw, mdp, pl, h):
    lat = Lattice3D(pl, pw, mdp, h)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)]
    gl = 2 * lat.nl // 3; bl_l = lat.nl // 3; pos = lat.pos
    bi = [lat.nmap[(bl_l, iy, iz)]
          for iy in range(-lat.hw, lat.hw + 1)
          for iz in range(-lat.hw, lat.hw + 1)
          if (bl_l, iy, iz) in lat.nmap]
    sa = [i for i in bi if pos[i, 1] >= 0.5]
    sb = [i for i in bi if pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    field_f = np.zeros(lat.n)

    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

    # Born
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
        probs = {}
        for key, ops in [('abc', all_s), ('ab', set(s_a + s_b)),
                          ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                          ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - ops)
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di]
                  + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')

    # Gravity + F∝M
    iz_m = round(3 / h); mi = lat.nmap.get((gl, 0, iz_m))
    grav = 0; fm_alpha = float('nan')
    if mi is not None:
        r3 = np.sqrt((pos[:, 0]-pos[mi, 0])**2 + (pos[:, 1]-pos[mi, 1])**2 +
                      (pos[:, 2]-pos[mi, 2])**2) + 0.1
        am = lat.propagate(STRENGTH / r3, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
        m_data = []; g_data = []
        for s in [1e-6, 5e-6, 1e-5, 5e-5]:
            ams = lat.propagate(s / r3, K, blocked)
            pms = sum(abs(ams[d])**2 for d in det)
            if pms > 1e-30:
                delta = sum(abs(ams[d])**2 * pos[d, 2] for d in det) / pms - zf
                if delta > 0: m_data.append(s); g_data.append(delta)
        if len(m_data) >= 3:
            lx = np.log(m_data); ly = np.log(g_data)
            mx = lx.mean(); my = ly.mean()
            sxx = np.sum((lx - mx)**2); sxy = np.sum((lx - mx) * (ly - my))
            fm_alpha = sxy / sxx if sxx > 1e-10 else 0

    return {'born': born, 'grav': grav, 'fm': fm_alpha, 'n': lat.n}


def main():
    print("=" * 60)
    print("VALLEY-LINEAR ROBUSTNESS SWEEP")
    print("S = L(1-f), 1/L^2 kernel, h^2 measure")
    print("=" * 60)

    h = 0.5
    print(f"\nSWEEP 1: Width (L=12, max_d=3, h={h})")
    for pw in [4, 6, 8, 10]:
        t0 = time.time()
        r = setup_and_measure(pw, 3, 12, h)
        dt = time.time() - t0
        if r:
            dr = 'T' if r['grav'] > 0 else 'A'
            print(f"  W={pw:2d}: Born={r['born']:.1e}, grav={r['grav']:+.6f}({dr}), "
                  f"F~M={r['fm']:.2f}, {r['n']:,} nodes ({dt:.0f}s)")

    print(f"\nSWEEP 2: Connectivity (L=12, W=8, h={h})")
    for mdp in [1, 2, 3]:
        t0 = time.time()
        r = setup_and_measure(8, mdp, 12, h)
        dt = time.time() - t0
        if r:
            dr = 'T' if r['grav'] > 0 else 'A'
            print(f"  max_d={mdp}: Born={r['born']:.1e}, grav={r['grav']:+.6f}({dr}), "
                  f"F~M={r['fm']:.2f} ({dt:.0f}s)")

    print(f"\nSWEEP 3: Length (W=8, max_d=3, h={h})")
    for pl in [8, 10, 12, 15, 18]:
        t0 = time.time()
        r = setup_and_measure(8, 3, pl, h)
        dt = time.time() - t0
        if r:
            dr = 'T' if r['grav'] > 0 else 'A'
            print(f"  L={pl:2d}: grav={r['grav']:+.6f}({dr}), F~M={r['fm']:.2f} ({dt:.0f}s)")


if __name__ == "__main__":
    main()
