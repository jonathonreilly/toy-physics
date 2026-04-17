#!/usr/bin/env python3
"""Exploratory transfer-norm test + 4D Born check.

Transfer norm: for each dimension d and kernel power p, measure the
single-layer amplitude transfer norm T = Σ_j |K(i→j)| for a central
node on a regular lattice.

Important scope note:
- this script measures a *bare* transfer norm, not the bounded
  measure-corrected local probe frozen separately on `main`
- use it as an exploratory discriminator, not as a canonical proof that
  `p = d-1` is uniquely selected

Also: Born check on 4D 1/L^3 kernel.
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
K = 5.0


def transfer_norm_1d(h, max_d_phys, power):
    """1D transverse (2D lattice). Sum |w/L^p| over all edges from center."""
    max_d = max(1, round(max_d_phys / h))
    T = 0.0
    for dy in range(-max_d, max_d + 1):
        dyp = dy * h
        L = math.sqrt(h * h + dyp * dyp)
        theta = math.atan2(abs(dyp), h)
        w = math.exp(-BETA * theta * theta)
        T += w / (L ** power)
    return T


def transfer_norm_2d(h, max_d_phys, power):
    """2D transverse (3D lattice)."""
    max_d = max(1, round(max_d_phys / h))
    T = 0.0
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * h, dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            rt = math.sqrt(dyp**2 + dzp**2)
            theta = math.atan2(rt, h)
            w = math.exp(-BETA * theta * theta)
            T += w / (L ** power)
    return T


def transfer_norm_3d(h, max_d_phys, power):
    """3D transverse (4D lattice)."""
    max_d = max(1, round(max_d_phys / h))
    T = 0.0
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            for dw in range(-max_d, max_d + 1):
                dyp, dzp, dwp = dy * h, dz * h, dw * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp + dwp * dwp)
                rt = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                theta = math.atan2(rt, h)
                w = math.exp(-BETA * theta * theta)
                T += w / (L ** power)
    return T


def run_transfer_norm_test():
    print("=" * 70)
    print("EXPLORATORY TRANSFER NORM TEST: T(h) = Σ |w/L^p| for central node")
    print("  Bare local sum, not the canonical measure-corrected probe on main.")
    print("  Read this as a comparative observable, not a standalone theorem.")
    print("=" * 70)
    print()

    max_d_phys = 3
    h_values = [2.0, 1.0, 0.5, 0.25, 0.125]

    # 2D lattice (1 transverse dim, d_spatial=2)
    print("2D LATTICE (d=2, 1 transverse dim)")
    print(f"  {'h':>6s}", end="")
    for p in [0, 1, 2]:
        print(f"  {'p='+str(p):>10s}", end="")
    print()
    for h in h_values:
        print(f"  {h:6.3f}", end="")
        for p in [0, 1, 2]:
            T = transfer_norm_1d(h, max_d_phys, p)
            print(f"  {T:10.4f}", end="")
        print()
    print(f"  Exploratory read: compare p=1 against neighbors\n")

    # 3D lattice (2 transverse dims, d_spatial=3)
    print("3D LATTICE (d=3, 2 transverse dims)")
    print(f"  {'h':>6s}", end="")
    for p in [1, 2, 3]:
        print(f"  {'p='+str(p):>10s}", end="")
    print()
    for h in h_values:
        print(f"  {h:6.3f}", end="")
        for p in [1, 2, 3]:
            T = transfer_norm_2d(h, max_d_phys, p)
            print(f"  {T:10.4f}", end="")
        print()
    print(f"  Exploratory read: compare p=2 against neighbors\n")

    # 4D lattice (3 transverse dims, d_spatial=4)
    print("4D LATTICE (d=4, 3 transverse dims)")
    h_4d = [2.0, 1.0, 0.5]  # 0.25 too slow for 3D transverse sum
    print(f"  {'h':>6s}", end="")
    for p in [2, 3, 4]:
        print(f"  {'p='+str(p):>10s}", end="")
    print()
    for h in h_4d:
        print(f"  {h:6.3f}", end="")
        for p in [2, 3, 4]:
            T = transfer_norm_3d(h, max_d_phys, p)
            print(f"  {T:10.4f}", end="")
        print()
    print(f"  Exploratory read: compare p=3 against neighbors\n")


def run_4d_born():
    """Born check on 4D 1/L^3 kernel."""
    print("=" * 70)
    print("4D BORN CHECK: 1/L^3 kernel")
    print("=" * 70)
    print()

    class L4D:
        def __init__(s, pl, pw, mdp, h):
            s.h = h; s.nl = int(pl/h)+1; s.hw = int(pw/h)
            s.max_d = max(1, round(mdp/h))
            nw = 2*s.hw+1; s.npl = nw**3; s.n = s.nl*s.npl
            s.pos = np.zeros((s.n, 4)); s.nmap = {}
            s._ls = np.zeros(s.nl, dtype=np.int64)
            idx = 0
            for l in range(s.nl):
                s._ls[l] = idx; x = l*h
                for iy in range(-s.hw, s.hw+1):
                    for iz in range(-s.hw, s.hw+1):
                        for iw in range(-s.hw, s.hw+1):
                            s.pos[idx] = (x, iy*h, iz*h, iw*h)
                            s.nmap[(l, iy, iz, iw)] = idx; idx += 1
            s._off = []
            md = s.max_d
            for dy in range(-md, md+1):
                for dz in range(-md, md+1):
                    for dw in range(-md, md+1):
                        dyp, dzp, dwp = dy*h, dz*h, dw*h
                        L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                        rt = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                        th = math.atan2(rt, h)
                        s._off.append((dy, dz, dw, L, math.exp(-BETA*th*th)))
            s._nw = nw

        def prop(s, field, k, bl):
            n = s.n; nw = s._nw; nl = s.nl
            amps = np.zeros(n, dtype=np.complex128)
            src = s.nmap.get((0, 0, 0, 0), 0); amps[src] = 1.0
            bm = np.zeros(n, dtype=bool)
            for b in bl: bm[b] = True
            for layer in range(nl-1):
                ls = s._ls[layer]; ld = s._ls[layer+1] if layer+1 < nl else n
                sa = amps[ls:ls+s.npl].copy(); sa[bm[ls:ls+s.npl]] = 0
                if np.max(np.abs(sa)) < 1e-30: continue
                sf = field[ls:ls+s.npl]; df = field[ld:ld+s.npl]
                db = bm[ld:ld+s.npl]
                for dy, dz, dw, L, w in s._off:
                    ym = max(0, -dy); yM = min(nw, nw-dy)
                    zm = max(0, -dz); zM = min(nw, nw-dz)
                    wm = max(0, -dw); wM = min(nw, nw-dw)
                    if ym >= yM or zm >= zM or wm >= wM: continue
                    yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                    wr = np.arange(wm, wM)
                    siy, siz, siw = np.meshgrid(yr, zr, wr, indexing='ij')
                    si = siy.ravel()*nw*nw + siz.ravel()*nw + siw.ravel()
                    di = ((siy.ravel()+dy)*nw*nw + (siz.ravel()+dz)*nw +
                          (siw.ravel()+dw))
                    a = sa[si]; nz = np.abs(a) > 1e-30
                    if not np.any(nz): continue
                    lf = 0.5*(sf[si[nz]] + df[di[nz]])
                    dl = L*(1+lf)
                    ret = np.sqrt(np.maximum(dl*dl - L*L, 0)); act = dl - ret
                    c = a[nz] * np.exp(1j*k*act) * w / (L**3)
                    c[db[di[nz]]] = 0
                    np.add.at(amps[ld:ld+s.npl], di[nz], c)
            return amps

    h = 1.0; phys_l = 10
    t0 = time.time()
    lat = L4D(phys_l, 4, 2, h)
    print(f"4D h={h}: {lat.n:,} nodes, {lat.nl} layers")

    bl_l = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw+1):
        for iz in range(-lat.hw, lat.hw+1):
            for iw in range(-lat.hw, lat.hw+1):
                idx = lat.nmap.get((bl_l, iy, iz, iw))
                if idx is not None:
                    bi.append(idx)

    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]

    # Find 3 slits for Born test
    upper = sorted([i for i in bi if lat.pos[i, 1] > 1],
                   key=lambda i: lat.pos[i, 1])
    lower = sorted([i for i in bi if lat.pos[i, 1] < -1],
                   key=lambda i: -lat.pos[i, 1])
    middle = [i for i in bi if abs(lat.pos[i, 1]) <= 1
              and abs(lat.pos[i, 2]) <= 1 and abs(lat.pos[i, 3]) <= 1]

    if not (upper and lower and middle):
        print("  Cannot find 3 slits for Born test")
        return

    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = set(bi) - all_s

    field_f = np.zeros(lat.n)
    probs = {}
    for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl2 = other | (all_s - open_set)
        a = lat.prop(field_f, K, bl2)
        probs[key] = np.array([abs(a[d])**2 for d in det])

    I3 = 0.0; P = 0.0
    for di in range(len(det)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
              - probs['bc'][di] + probs['a'][di] + probs['b'][di]
              + probs['c'][di])
        I3 += abs(i3)
        P += probs['abc'][di]

    born = I3 / P if P > 1e-30 else float('nan')
    status = "PASS" if born < 1e-10 else "FAIL"
    dt = time.time() - t0
    print(f"  Born |I3|/P = {born:.2e}  [{status}]  ({dt:.0f}s)")

    # Also check k=0
    sa_set = set([i for i in bi if lat.pos[i, 1] >= 0.5])
    sb_set = set([i for i in bi if lat.pos[i, 1] <= -0.5])
    blocked = set(bi) - sa_set - sb_set
    a0 = lat.prop(field_f, 0.0, blocked)
    p0 = sum(abs(a0[d])**2 for d in det)
    if p0 > 1e-30:
        z0 = sum(abs(a0[d])**2 * lat.pos[d, 2] for d in det) / p0
        print(f"  k=0 centroid = {z0:.6f}  [{'PASS' if abs(z0) < 1e-6 else 'CHECK'}]")

    # MI quick check
    pa = lat.prop(field_f, K, blocked | sb_set)
    pb = lat.prop(field_f, K, blocked | sa_set)
    N_YBINS = 8
    bw = 2 * (4 + 1) / N_YBINS
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((lat.pos[d, 1] + 4 + 1) / bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na = prob_a.sum(); nb = prob_b.sum()
    MI = 0
    if na > 1e-30 and nb > 1e-30:
        pa_n = prob_a/na; pb_n = prob_b/nb
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm = 0.5*pa_n[b3] + 0.5*pb_n[b3]
            if pm > 1e-30: H -= pm * math.log2(pm)
            if pa_n[b3] > 1e-30: Hc -= 0.5*pa_n[b3]*math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5*pb_n[b3]*math.log2(pb_n[b3])
        MI = H - Hc
    print(f"  MI = {MI:.4f} bits")

    # d_TV
    da = {d: abs(pa[d])**2 for d in det}
    db = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d]/na2 - db[d]/nb2) for d in det)
    print(f"  d_TV = {dtv:.4f}")


def main():
    run_transfer_norm_test()
    print()
    run_4d_born()


if __name__ == "__main__":
    main()
