#!/usr/bin/env python3
"""Multi-L companion checks (properties 8-9) for cos^2(theta) vs exp(-0.8*theta^2).

Tests:
  Property 8 (Purity stability): 1-purity stays non-zero across L in {8,10,12,15}
  Property 9 (Gravity grows):    centroid shift toward mass grows with L

Both kernels run at h=0.5, W=6 for speed.
"""

from __future__ import annotations
import math
import time

import numpy as np

# --- Constants ---
K = 5.0
LAM = 10.0
N_YBINS = 8
STRENGTH = 5e-5
MAX_D_PHYS = 3
BETA = 0.8


# --- Lattice ---
class Lattice3D:
    def __init__(self, phys_l, phys_w, h, weight_fn=None):
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

        if weight_fn is None:
            weight_fn = lambda theta: math.exp(-BETA * theta * theta)

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                w = weight_fn(theta)
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
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# --- Purity helper ---
def decoherence_purity(pa, pb, det, dcl):
    a = np.array([pa[d] for d in det], dtype=np.complex128)
    b = np.array([pb[d] for d in det], dtype=np.complex128)
    gram = np.array(
        [
            [np.vdot(a, a), np.vdot(a, b)],
            [np.vdot(b, a), np.vdot(b, b)],
        ],
        dtype=np.complex128,
    )
    mix = np.array([[1.0, dcl], [dcl, 1.0]], dtype=np.complex128)
    mg = mix @ gram
    tr = np.trace(mg).real
    if tr <= 1e-30:
        return 1.0
    return float((np.trace(mg @ mg) / (tr * tr)).real)


# --- Weight functions ---
def wfn_gauss(theta):
    return math.exp(-BETA * theta * theta)


def wfn_cos2(theta):
    return math.cos(theta) ** 2


# --- Multi-L test ---
def run_multi_L(kernel_name, weight_fn):
    print(f"\n  Kernel: {kernel_name}")
    grav_data = {}
    pur_data = {}
    phys_w = 6
    h = 0.5

    for pl in [8, 10, 12, 15]:
        t0 = time.time()
        lat = Lattice3D(pl, phys_w, h, weight_fn=weight_fn)
        det = [lat.nmap[(lat.nl - 1, iy, iz)]
               for iy in range(-lat.hw, lat.hw + 1)
               for iz in range(-lat.hw, lat.hw + 1)]
        gl = 2 * lat.nl // 3
        bl = lat.nl // 3

        # Barrier indices at slit layer
        bi = []
        for iy in range(-lat.hw, lat.hw + 1):
            for iz in range(-lat.hw, lat.hw + 1):
                idx = lat.nmap.get((bl, iy, iz))
                if idx is not None:
                    bi.append(idx)
        sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
        sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
        bk = set(bi) - set(sa + sb)

        # Flat-field baseline centroid
        ff = np.zeros(lat.n)
        af = lat.propagate(ff, K, bk)
        pf = sum(abs(af[d]) ** 2 for d in det)
        zf = sum(abs(af[d]) ** 2 * lat.pos[d, 2] for d in det) / pf if pf > 1e-30 else 0

        # Gravity: mass at z=3
        iz_m = round(3 / h)
        mi = lat.nmap.get((gl, 0, iz_m))
        if mi is not None:
            r = np.sqrt(
                (lat.pos[:, 0] - lat.pos[mi, 0]) ** 2
                + (lat.pos[:, 1] - lat.pos[mi, 1]) ** 2
                + (lat.pos[:, 2] - lat.pos[mi, 2]) ** 2
            ) + 0.1
            fm = STRENGTH / r
            am = lat.propagate(fm, K, bk)
            pm = sum(abs(am[d]) ** 2 for d in det)
            if pm > 1e-30:
                grav_data[pl] = sum(abs(am[d]) ** 2 * lat.pos[d, 2] for d in det) / pm - zf

        # Purity: propagate through upper/lower slits separately
        pa = lat.propagate(ff, K, bk | set(sb))
        pb = lat.propagate(ff, K, bk | set(sa))

        bw = 2 * (phys_w + 1) / N_YBINS
        ed = max(1, round(lat.nl / 6))
        st = bl + 1
        sp = min(lat.nl - 1, st + ed)
        mid = []
        for l in range(st, sp):
            mid.extend(
                [lat.nmap[(l, iy, iz)]
                 for iy in range(-lat.hw, lat.hw + 1)
                 for iz in range(-lat.hw, lat.hw + 1)
                 if (l, iy, iz) in lat.nmap]
            )
        ba = np.zeros(N_YBINS, dtype=np.complex128)
        bb = np.zeros(N_YBINS, dtype=np.complex128)
        for m in mid:
            b2 = max(0, min(N_YBINS - 1, int((lat.pos[m, 1] + phys_w + 1) / bw)))
            ba[b2] += pa[m]
            bb[b2] += pb[m]
        S = float(np.sum(np.abs(ba - bb) ** 2))
        NA = float(np.sum(np.abs(ba) ** 2))
        NB = float(np.sum(np.abs(bb) ** 2))
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0
        Dcl = math.exp(-LAM ** 2 * Sn)
        pur = decoherence_purity(pa, pb, det, Dcl)
        pur_data[pl] = 1 - pur

        dr = "T" if grav_data.get(pl, 0) > 0 else "A"
        print(f"    L={pl:2d}: grav={grav_data.get(pl, 0):+.6f}({dr})  "
              f"1-pur={pur_data[pl]:.4f}  ({time.time()-t0:.1f}s)")

    # Assess
    vals = sorted(grav_data.items())
    grows = len(vals) >= 2 and vals[-1][1] > vals[0][1]
    toward = all(v > 0 for _, v in vals)
    pur_vals = list(pur_data.values())
    pur_mean = np.mean(pur_vals)
    pur_std = np.std(pur_vals)
    stable = all(p > 0.01 for p in pur_vals)  # doesn't collapse to 0

    return {
        "grav": grav_data,
        "pur": pur_data,
        "grows": grows,
        "toward": toward,
        "stable": stable,
        "pur_mean": pur_mean,
        "pur_std": pur_std,
    }


def main():
    t_total = time.time()
    print("=" * 80)
    print("Multi-L companion checks (Properties 8-9)")
    print("h=0.5, W=6, L in {8, 10, 12, 15}")
    print("=" * 80)

    results = {}
    for name, wfn in [("exp(-0.8*theta^2)", wfn_gauss), ("cos^2(theta)", wfn_cos2)]:
        results[name] = run_multi_L(name, wfn)

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    header = f"{'kernel':<20s}"
    for pl in [8, 10, 12, 15]:
        header += f" | L={pl} grav"
    header += " | grows? | 1-pur stable?"
    print(header)
    print("-" * len(header))

    for name, r in results.items():
        row = f"{name:<20s}"
        for pl in [8, 10, 12, 15]:
            g = r["grav"].get(pl, 0)
            row += f" | {g:+.6f}"
        row += f" | {'YES' if r['grows'] else 'NO':6s}"
        row += f" | {'YES' if r['stable'] else 'NO'} (mean={r['pur_mean']:.3f})"
        print(row)

    print()
    for name, r in results.items():
        p8 = "PASS" if r["stable"] else "FAIL"
        p9 = "PASS" if r["grows"] and r["toward"] else "FAIL"
        print(f"  {name}: Prop 8 (purity stable) = {p8},  Prop 9 (gravity grows) = {p9}")

    print(f"\nTotal time: {time.time()-t_total:.0f}s")


if __name__ == "__main__":
    main()
