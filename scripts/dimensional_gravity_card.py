#!/usr/bin/env python3
"""Canonical dimensional gravity card.

Takes spatial dimension d as input. Produces the full gravity card
using the dimensional prescription:

  Kernel:  1/L^(d-1)
  Field:   s/r^(d-2)
  Action:  S = L(1-f)       (valley-linear)
  Measure: h^(d-1)

Measures: Born, d_TV, k=0, F∝M, gravity sign, decoherence, MI,
distance law (with tail fit).

Usage:
  python3 dimensional_gravity_card.py          # default d=3
  python3 dimensional_gravity_card.py --dim 4  # 4D test
"""

from __future__ import annotations
import argparse
import math
import os
import time
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this card. On this machine use /usr/bin/python3."
    ) from exc

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
STRENGTH = 5e-5


# ---------------------------------------------------------------------------
# Lattice generators
# ---------------------------------------------------------------------------

class Lattice3D:
    """3D lattice (2 transverse dims)."""
    def __init__(self, phys_l, phys_w, max_d_phys, h):
        self.h = h; self.d = 3
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2; self.n = self.nl * self.npl
        self._hm = h ** 2; self._kernel_power = 2  # d-1
        self._field_power = 1  # d-2
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
                L = math.sqrt(h*h + dyp*dyp + dzp*dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                self._off.append((dy, dz, L, math.exp(-BETA * theta**2)))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        amps = np.zeros(self.n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0); amps[src] = 1.0
        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set: blocked[b] = True
        nw = self._nw; hm = self._hm; kp = self._kernel_power
        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < self.nl else self.n
            sa = amps[ls:ls+self.npl].copy(); sa[blocked[ls:ls+self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30: continue
            sf = field[ls:ls+self.npl]; df = field[ld:ld+self.npl]
            db = blocked[ld:ld+self.npl]
            for dy, dz, L, w in self._off:
                ym=max(0,-dy);yM=min(nw,nw-dy)
                zm=max(0,-dz);zM=min(nw,nw-dz)
                if ym>=yM or zm>=zM: continue
                yr=np.arange(ym,yM);zr=np.arange(zm,zM)
                siy,siz=np.meshgrid(yr,zr,indexing='ij')
                si=siy.ravel()*nw+siz.ravel()
                di=(siy.ravel()+dy)*nw+(siz.ravel()+dz)
                a=sa[si];nz=np.abs(a)>1e-30
                if not np.any(nz): continue
                lf=0.5*(sf[si[nz]]+df[di[nz]])
                act=L*(1-lf)
                c=a[nz]*np.exp(1j*k*act)*w*hm/(L**kp)
                c[db[di[nz]]]=0
                np.add.at(amps[ld:ld+self.npl],di[nz],c)
        return amps

    def make_field(self, z_mass, strength):
        gl = 2 * self.nl // 3
        iz = round(z_mass / self.h)
        mi = self.nmap.get((gl, 0, iz))
        if mi is None: return np.zeros(self.n), None
        r = np.sqrt(np.sum((self.pos - self.pos[mi])**2, axis=1)) + 0.1
        return strength / (r ** self._field_power), mi

    def setup_slits(self):
        bl = self.nl // 3; bi = []
        for iy in range(-self.hw, self.hw+1):
            for iz in range(-self.hw, self.hw+1):
                idx = self.nmap.get((bl, iy, iz))
                if idx is not None: bi.append(idx)
        sa = [i for i in bi if self.pos[i, 1] >= 0.5]
        sb = [i for i in bi if self.pos[i, 1] <= -0.5]
        return bi, sa, sb, set(bi) - set(sa + sb), bl

    def detector(self):
        return [self.nmap[(self.nl-1, iy, iz)]
                for iy in range(-self.hw, self.hw+1)
                for iz in range(-self.hw, self.hw+1)
                if (self.nl-1, iy, iz) in self.nmap]


class Lattice4D:
    """4D lattice (3 transverse dims)."""
    def __init__(self, phys_l, phys_w, max_d_phys, h):
        self.h = h; self.d = 4
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3; self.n = self.nl * self.npl
        self._hm = h ** 3; self._kernel_power = 3; self._field_power = 2
        self.pos = np.zeros((self.n, 4)); self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for l in range(self.nl):
            self._ls[l] = idx; x = l * h
            for iy in range(-self.hw, self.hw+1):
                for iz in range(-self.hw, self.hw+1):
                    for iw in range(-self.hw, self.hw+1):
                        self.pos[idx] = (x, iy*h, iz*h, iw*h)
                        self.nmap[(l, iy, iz, iw)] = idx; idx += 1
        self._off = []
        for dy in range(-self.max_d, self.max_d+1):
            for dz in range(-self.max_d, self.max_d+1):
                for dw in range(-self.max_d, self.max_d+1):
                    dyp,dzp,dwp = dy*h, dz*h, dw*h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    rt = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(rt, h)
                    self._off.append((dy, dz, dw, L, math.exp(-BETA*theta**2)))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        amps = np.zeros(self.n, dtype=np.complex128)
        src = self.nmap.get((0,0,0,0), 0); amps[src] = 1.0
        blocked = np.zeros(self.n, dtype=bool)
        for b in blocked_set: blocked[b] = True
        nw = self._nw; hm = self._hm; kp = self._kernel_power
        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer+1] if layer+1 < self.nl else self.n
            sa = amps[ls:ls+self.npl].copy(); sa[blocked[ls:ls+self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30: continue
            sf = field[ls:ls+self.npl]; df = field[ld:ld+self.npl]
            db = blocked[ld:ld+self.npl]
            for dy,dz,dw,L,w in self._off:
                ym=max(0,-dy);yM=min(nw,nw-dy)
                zm=max(0,-dz);zM=min(nw,nw-dz)
                wm=max(0,-dw);wM=min(nw,nw-dw)
                if ym>=yM or zm>=zM or wm>=wM: continue
                yr=np.arange(ym,yM);zr=np.arange(zm,zM);wr=np.arange(wm,wM)
                siy,siz,siw=np.meshgrid(yr,zr,wr,indexing='ij')
                si=siy.ravel()*nw*nw+siz.ravel()*nw+siw.ravel()
                di=(siy.ravel()+dy)*nw*nw+(siz.ravel()+dz)*nw+(siw.ravel()+dw)
                a=sa[si];nz=np.abs(a)>1e-30
                if not np.any(nz): continue
                lf=0.5*(sf[si[nz]]+df[di[nz]])
                act=L*(1-lf)
                c=a[nz]*np.exp(1j*k*act)*w*hm/(L**kp)
                c[db[di[nz]]]=0
                np.add.at(amps[ld:ld+self.npl],di[nz],c)
        return amps

    def make_field(self, z_mass, strength):
        gl = 2 * self.nl // 3
        iz = round(z_mass / self.h)
        mi = self.nmap.get((gl, 0, iz, 0))
        if mi is None: return np.zeros(self.n), None
        r = np.sqrt(np.sum((self.pos - self.pos[mi])**2, axis=1)) + 0.1
        return strength / (r ** self._field_power), mi

    def setup_slits(self):
        bl = self.nl // 3; bi = []
        for iy in range(-self.hw, self.hw+1):
            for iz in range(-self.hw, self.hw+1):
                for iw in range(-self.hw, self.hw+1):
                    idx = self.nmap.get((bl, iy, iz, iw))
                    if idx is not None: bi.append(idx)
        sa = [i for i in bi if self.pos[i, 1] >= 0.5]
        sb = [i for i in bi if self.pos[i, 1] <= -0.5]
        return bi, sa, sb, set(bi) - set(sa + sb), bl

    def detector(self):
        return [v for k, v in self.nmap.items() if k[0] == self.nl - 1]


# ---------------------------------------------------------------------------
# Measurement functions
# ---------------------------------------------------------------------------

def fit_power(b_data, d_data):
    if len(b_data) < 3: return None, None
    lx = np.log(np.array(b_data, dtype=float))
    ly = np.log(np.array(d_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx)**2)
    if sxx < 1e-12: return None, None
    sxy = np.sum((lx - mx) * (ly - my))
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx)))**2)
    ss_tot = np.sum((ly - my)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def run_card(lat, params):
    t_total = time.time()
    d = lat.d
    det = lat.detector()
    bi, sa, sb, blocked, bl = lat.setup_slits()
    pos = lat.pos
    field_f = np.zeros(lat.n)

    print(f"{'='*60}")
    print(f"DIMENSIONAL GRAVITY CARD (d={d})")
    print(f"  Kernel: 1/L^{d-1}, Field: s/r^{d-2}, Action: S=L(1-f)")
    print(f"  h={lat.h}, W={params['w']}, L={params['l']}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers")
    print(f"{'='*60}\n")

    # Free propagation
    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[i])**2 for i in det)
    if pf < 1e-30:
        print("NO SIGNAL"); return
    zf = sum(abs(af[i])**2 * pos[i, 2] for i in det) / pf
    print(f"  Free prop: {time.time()-t0:.1f}s\n")

    # 1. Born
    t0 = time.time()
    z_col = 2 if d == 3 else 2
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    mid_crit = [abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1 for i in bi]
    if d == 4:
        mid_crit = [abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1
                    and abs(pos[i, 3]) <= 1 for i in bi]
    middle = [bi[j] for j, c in enumerate(mid_crit) if c]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a+s_b+s_c); other = set(bi) - all_s
        probs = {}
        for key, ops in [('abc',all_s),('ab',set(s_a+s_b)),('ac',set(s_a+s_c)),
                          ('bc',set(s_b+s_c)),('a',set(s_a)),('b',set(s_b)),('c',set(s_c))]:
            bl2 = other | (all_s - ops)
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[i])**2 for i in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di]-probs['ab'][di]-probs['ac'][di]
                  -probs['bc'][di]+probs['a'][di]+probs['b'][di]+probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    print(f"  1. Born = {born:.2e}  [{'PASS' if born < 1e-10 else 'FAIL'}]  ({time.time()-t0:.0f}s)")

    # 2. d_TV + setup for decoherence/MI
    t0 = time.time()
    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = {i: abs(pa[i])**2 for i in det}
    db_ = {i: abs(pb[i])**2 for i in det}
    na2 = sum(da.values()); nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[i]/na2 - db_[i]/nb2) for i in det) if na2>1e-30 and nb2>1e-30 else 0
    print(f"  2. d_TV = {dtv:.4f}  ({time.time()-t0:.0f}s)")

    # 3. k=0
    fm3, _ = lat.make_field(3, STRENGTH)
    am0 = lat.propagate(fm3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[i])**2 for i in det); pf0 = sum(abs(af0[i])**2 for i in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[i])**2*pos[i,2] for i in det)/pm0
               - sum(abs(af0[i])**2*pos[i,2] for i in det)/pf0)
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0)<1e-6 else 'CHECK'}]")

    # 4. F∝M
    t0 = time.time()
    fm_base, mi_base = lat.make_field(3, STRENGTH)
    if mi_base is not None:
        r_base = np.sqrt(np.sum((pos - pos[mi_base])**2, axis=1)) + 0.1
        m_data = []; g_data = []
        for s in [1e-6, 5e-6, 1e-5, 5e-5]:
            fms = s / (r_base ** lat._field_power)
            ams = lat.propagate(fms, K, blocked)
            pms = sum(abs(ams[i])**2 for i in det)
            if pms > 1e-30:
                delta = sum(abs(ams[i])**2*pos[i,2] for i in det)/pms - zf
                if delta > 0: m_data.append(s); g_data.append(delta)
        fm_alpha = float('nan')
        if len(m_data) >= 3:
            sl, _ = fit_power(m_data, g_data)
            if sl is not None: fm_alpha = sl
        print(f"  4. F~M = {fm_alpha:.2f}  ({time.time()-t0:.0f}s)")
    else:
        print(f"  4. F~M = n/a")

    # 5. Gravity sign
    am3 = lat.propagate(fm3, K, blocked)
    pm3 = sum(abs(am3[i])**2 for i in det)
    grav = (sum(abs(am3[i])**2*pos[i,2] for i in det)/pm3 - zf) if pm3>1e-30 else 0
    dr = "TOWARD" if grav > 0 else "AWAY"
    print(f"  5. Gravity = {grav:+.6f} ({dr})")

    # 6. Decoherence
    pw = params['w']
    bw = 2 * (pw + 1) / N_YBINS
    ed = max(1, round(lat.nl/6)); st = bl+1; sp = min(lat.nl-1, st+ed)
    mid_layers = []
    if d == 3:
        for l in range(st, sp):
            mid_layers.extend([lat.nmap[(l,iy,iz)]
                               for iy in range(-lat.hw,lat.hw+1)
                               for iz in range(-lat.hw,lat.hw+1)
                               if (l,iy,iz) in lat.nmap])
    elif d == 4:
        for l in range(st, sp):
            mid_layers.extend([lat.nmap[(l,iy,iz,iw)]
                               for iy in range(-lat.hw,lat.hw+1)
                               for iz in range(-lat.hw,lat.hw+1)
                               for iw in range(-lat.hw,lat.hw+1)
                               if (l,iy,iz,iw) in lat.nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid_layers:
        b2 = max(0, min(N_YBINS-1, int((pos[m,1]+pw+1)/bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba-bb)**2))
    NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
    Sn = S/(NA3+NB3) if (NA3+NB3)>0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2]+pb[d1].conjugate()*pb[d2]
                           +Dcl*pa[d1].conjugate()*pb[d2]+Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(i,i)] for i in det).real; pur = 1.0
    if tr > 1e-30:
        for key in rho: rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
    decoh = 100*(1-pur)
    print(f"  6. Decoherence = {decoh:.1f}%")

    # 7. MI
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for i in det:
        b2 = max(0, min(N_YBINS-1, int((pos[i,1]+pw+1)/bw)))
        prob_a[b2] += abs(pa[i])**2; prob_b[b2] += abs(pb[i])**2
    na3 = prob_a.sum(); nb3 = prob_b.sum(); MI = 0
    if na3>1e-30 and nb3>1e-30:
        pa_n=prob_a/na3;pb_n=prob_b/nb3;H=0;Hc=0
        for b3 in range(N_YBINS):
            pm2=0.5*pa_n[b3]+0.5*pb_n[b3]
            if pm2>1e-30:H-=pm2*math.log2(pm2)
            if pa_n[b3]>1e-30:Hc-=0.5*pa_n[b3]*math.log2(pa_n[b3])
            if pb_n[b3]>1e-30:Hc-=0.5*pb_n[b3]*math.log2(pb_n[b3])
        MI=H-Hc
    print(f"  7. MI = {MI:.4f} bits")

    # 8. Distance law
    t0 = time.time()
    max_z = min(int(pw * 0.85), lat.hw)
    z_vals = list(range(2, max_z + 1))
    b_data = []; d_data = []
    print(f"  8. Distance law (z={z_vals[0]}..{z_vals[-1]}):")
    for z in z_vals:
        fm, mi = lat.make_field(z, STRENGTH)
        if mi is None: continue
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[i])**2 for i in det)
        if pm > 1e-30:
            zm = sum(abs(am[i])**2*pos[i,2] for i in det)/pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"      z={z}: {delta:+.8f} ({sign})")
            if delta > 0: b_data.append(z); d_data.append(delta)

    n_tw = len(b_data)
    print(f"      TOWARD: {n_tw}/{len(z_vals)}")
    if len(b_data) >= 3:
        d_arr = np.array(d_data)
        peak_i = int(np.argmax(d_arr))
        if peak_i < len(b_data) - 2:
            sl, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
            if sl is not None:
                print(f"      Tail (z>={b_data[peak_i]}): b^({sl:.2f}), R²={r2:.3f}")
        # Far tail (z>=5)
        b5 = [b for b in b_data if b >= 5]
        d5 = [dd for b, dd in zip(b_data, d_data) if b >= 5]
        if len(b5) >= 3:
            sl5, r25 = fit_power(b5, d5)
            if sl5 is not None:
                print(f"      Far tail (z>=5): b^({sl5:.2f}), R²={r25:.3f}")
    newtonian = d - 2 if d >= 3 else "ln"
    print(f"      Newtonian: 1/b^{newtonian}")
    print(f"      ({time.time()-t0:.0f}s)")

    print(f"\n{'='*60}")
    print(f"  Total: {time.time()-t_total:.0f}s")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Dimensional gravity card")
    parser.add_argument("--dim", type=int, default=3, choices=[3, 4],
                        help="Spatial dimension (3 or 4)")
    parser.add_argument("--h", type=float, default=None,
                        help="Lattice spacing (default: 0.25 for 3D, 0.5 for 4D)")
    parser.add_argument("--w", type=int, default=None,
                        help="Lattice half-width (default: 12 for 3D, 7 for 4D)")
    parser.add_argument("--l", type=int, default=None,
                        help="Lattice length (default: 12)")
    parser.add_argument("--max-d", type=int, default=3,
                        help="Physical transverse reach (default: 3 for 3D, 2 for 4D)")
    args = parser.parse_args()

    d = args.dim
    h = args.h or (0.25 if d == 3 else 0.5)
    w = args.w or (12 if d == 3 else 7)
    l = args.l or 12
    md = args.max_d if d == 3 else min(args.max_d, 2)

    params = {'w': w, 'l': l}

    if d == 3:
        lat = Lattice3D(l, w, md, h)
    elif d == 4:
        lat = Lattice4D(l, w, md, h)

    run_card(lat, params)


if __name__ == "__main__":
    main()
