#!/usr/bin/env python3
"""4D lattice: bounded persistence comparison for nearby kernel powers.

This is an exploratory 4D follow-up on the ordered-lattice kernel fork.

It does not prove unique selection. The goal is narrower:
- compare 1/L, 1/L^2, 1/L^3 on the same 4D family
- check whether higher powers look more persistent on longer tested lattices
- keep the result bounded to the current tested windows

4D lattice: nodes at (x, y, z, w) where x is propagation direction,
y/z/w are transverse. Slits select on y, mass offset in z, gravity
measured in z-direction (same as 3D setup but with extra w dimension).
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
K = 5.0
PHYS_W = 4  # Width in each transverse dimension
MAX_D_PHYS = 2  # Physical transverse reach


class Lattice4D:
    def __init__(self, phys_l, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(PHYS_W / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3  # 3 transverse dims
        self.n = self.nl * self.npl

        self.pos = np.zeros((self.n, 4))  # x, y, z, w
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    for iw in range(-self.hw, self.hw + 1):
                        self.pos[idx] = (x, iy * h, iz * h, iw * h)
                        self.nmap[(layer, iy, iz, iw)] = idx
                        idx += 1

        # Pre-compute offsets
        self._off = []
        md = self.max_d
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    w = math.exp(-BETA * theta * theta)
                    self._off.append((dy, dz, dw, L, w))

        self._nw = nw

    def propagate(self, field, k, blocked_set, power):
        """Propagate with 1/L^power kernel and h^3 measure."""
        n = self.n
        hw = self.hw
        nl = self.nl
        nw = self._nw
        h = self.h
        h_measure = h ** 3  # 3 transverse dims measure factor

        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0, 0), 0)
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

            for dy, dz, dw, L, w in self._off:
                # Compute valid ranges for 3D transverse indexing
                # Flat index in npl: iy*nw*nw + iz*nw + iw (shifted by hw)
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                wm = max(0, -dw); wM = min(nw, nw - dw)
                if ym >= yM or zm >= zM or wm >= wM:
                    continue

                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                wr = np.arange(wm, wM)
                siy, siz, siw = np.meshgrid(yr, zr, wr, indexing='ij')
                si = siy.ravel() * nw * nw + siz.ravel() * nw + siw.ravel()
                di = ((siy.ravel() + dy) * nw * nw +
                      (siz.ravel() + dz) * nw +
                      (siw.ravel() + dw))

                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue

                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                dl = L * (1 + lf)
                ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
                act = dl - ret

                c = a[nz] * np.exp(1j * k * act) * w * h_measure / (L ** power)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)

        return amps


def make_field(lat, z_mass_phys, strength):
    pos = lat.pos
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    mx = pos[mi]
    r = np.sqrt(np.sum((pos - mx) ** 2, axis=1)) + 0.1
    return strength / r, mi


def setup_slits(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            for iw in range(-lat.hw, lat.hw + 1):
                idx = lat.nmap.get((bl, iy, iz, iw))
                if idx is not None:
                    bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked


def test_kernel(lat, blocked, det, gl, strength, power, label):
    """Test a specific kernel power on the 4D lattice."""
    field_f = np.zeros(lat.n)
    t0 = time.time()

    af = lat.propagate(field_f, K, blocked, power)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        print(f"  {label}: NO SIGNAL")
        return

    zf = sum(abs(af[d]) ** 2 * lat.pos[d, 2] for d in det) / pf

    # Gravity at multiple z
    s = strength
    results = []
    for z_mass in [1, 2, 3]:
        fm, mi = make_field(lat, z_mass, s)
        if mi is None:
            continue
        am = lat.propagate(fm, K, blocked, power)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * lat.pos[d, 2] for d in det) / pm
            delta = zm - zf
            results.append((z_mass, delta, "T" if delta > 0 else "A"))

    dt = time.time() - t0
    n_tw = sum(1 for _, _, d in results if d == "T")
    r_str = " ".join(f"z={z}:{d:+.4f}({dr})" for z, d, dr in results)
    print(f"  {label}: {r_str}  [{n_tw}/{len(results)} TOWARD] ({dt:.0f}s)")
    return n_tw, len(results)


def main():
    print("=" * 70)
    print("4D LATTICE: EXPLORATORY KERNEL PERSISTENCE TEST")
    print("  Compare 1/L, 1/L^2, 1/L^3 on the same 4D ordered family.")
    print("  Use the result as bounded persistence evidence, not a theorem.")
    print("=" * 70)
    print()

    strengths = [5e-5, 1e-5]

    for h in [1.0, 0.5]:
        phys_l = 10
        t0 = time.time()
        lat = Lattice4D(phys_l, h)
        bi, sa, sb, blocked = setup_slits(lat)
        det = [lat.nmap[(lat.nl - 1, iy, iz, iw)]
               for iy in range(-lat.hw, lat.hw + 1)
               for iz in range(-lat.hw, lat.hw + 1)
               for iw in range(-lat.hw, lat.hw + 1)
               if (lat.nl - 1, iy, iz, iw) in lat.nmap]
        gl = 2 * lat.nl // 3

        print(f"h={h}: {lat.n:,} nodes, {lat.nl} layers, "
              f"~{len(lat._off)} edges/node ({time.time()-t0:.1f}s gen)")
        print()

        for s in strengths:
            print(f"  Field strength s={s:.0e}:")
            for power, label in [(1, "1/L   "), (2, "1/L^2 "), (3, "1/L^3 ")]:
                test_kernel(lat, blocked, det, gl, s, power, label)
            print()

    print("=" * 70)
    print("Read as a bounded persistence comparison across nearby kernel powers.")
    print("Short lattices are not discriminative; longer tested lattices matter.")
    print("=" * 70)


if __name__ == "__main__":
    main()
