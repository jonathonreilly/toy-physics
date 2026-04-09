#!/usr/bin/env python3
"""3+1D same-geometry refinement: h=1.0 vs h=0.5 at FIXED W=3.

The previous 3+1D tests changed BOTH h and W simultaneously, making
it impossible to distinguish resolution effects from box-size effects.
This script holds W=3 fixed and varies only h, giving a clean refinement
check.

With the corrected spatial-only field (r computed from y,z,w only):
  h=1.0 at W=4 gave AWAY (repulsive) — too coarse
  h=0.5 at W=3 gave TOWARD with F~M=1.00 — but W changed

This script resolves: is h=0.5 TOWARD because of better resolution,
or because W=3 is a different physical box?

HYPOTHESIS: h=0.5 TOWARD survives at W=3 AND h=1.0 is AWAY at W=3.
  This would confirm that resolution (not box size) is the issue.

FALSIFICATION: If h=1.0 at W=3 is also TOWARD, the box size (not h)
  was the relevant variable.
"""

from __future__ import annotations
import math
import time
import numpy as np

K = 5.0
PHYS_W = 3
MAX_D_PHYS = 2
STRENGTH = 5e-5
POWER = 3


class Lattice4D:
    def __init__(self, phys_l, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.exp(-0.8 * t * t)
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(PHYS_W / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3
        self.n = self.nl * self.npl
        self._hm = h ** 3
        self.pos = np.zeros((self.n, 4))
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
        self._off = []
        md = self.max_d
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    w = weight_fn(theta)
                    self._off.append((dy, dz, dw, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
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
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                wm = max(0, -dw); wM = min(nw, nw - dw)
                if ym >= yM or zm >= zM or wm >= wM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                wr = np.arange(wm, wM)
                siy, siz, siw = np.meshgrid(yr, zr, wr, indexing='ij')
                si = siy.ravel()*nw*nw + siz.ravel()*nw + siw.ravel()
                di = ((siy.ravel()+dy)*nw*nw + (siz.ravel()+dz)*nw + (siw.ravel()+dw))
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field(lat, z_mass_phys, strength):
    """Static 3D Coulomb: spatial-only radius."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz, mw = lat.pos[mi, 1], lat.pos[mi, 2], lat.pos[mi, 3]
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2 +
        (lat.pos[:, 3] - mw)**2
    ) + 0.1
    return strength / (r_spatial ** 2), mi


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


def run_quick_card(h, kernel_name, weight_fn):
    """Run Born + k=0 + gravity + F~M at one h value."""
    phys_l = 10
    t0 = time.time()
    lat = Lattice4D(phys_l, h, weight_fn=weight_fn)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits(lat)
    field_f = np.zeros(lat.n)

    print(f"\n  h={h}, {kernel_name}: {lat.n:,} nodes, {lat.nl} layers")

    # Flat baseline
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("    NO SIGNAL")
        return {"h": h, "kernel": kernel_name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

    # Born
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1 and abs(pos[i, 3]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                               ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
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

    # k=0
    field_m, _ = make_field(lat, 2, STRENGTH)
    am0 = lat.propagate(field_m, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2*pos[d,2] for d in det)/pm0
               - sum(abs(af0[d])**2*pos[d,2] for d in det)/pf0)

    # Gravity
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf

    # F~M (only if gravity is TOWARD)
    fm_alpha = float('nan')
    if grav > 0:
        m_data = []; g_data = []
        for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
            fm, _ = make_field(lat, 2, s)
            am2 = lat.propagate(fm, K, blocked)
            pm2 = sum(abs(am2[d])**2 for d in det)
            if pm2 > 1e-30:
                zm2 = sum(abs(am2[d])**2 * pos[d, 2] for d in det) / pm2
                delta = zm2 - zf
                if delta > 0:
                    m_data.append(s); g_data.append(delta)
        if len(m_data) >= 3:
            lx = np.log(np.array(m_data)); ly = np.log(np.array(g_data))
            mx = lx.mean(); my_ = ly.mean()
            sxx = np.sum((lx-mx)**2); sxy = np.sum((lx-mx)*(ly-my_))
            if sxx > 1e-10:
                fm_alpha = sxy / sxx

    elapsed = time.time() - t0
    dr = "TOWARD" if grav > 0 else "AWAY"
    born_s = "PASS" if born < 1e-10 else "FAIL"
    k0_s = "PASS" if abs(gk0) < 1e-6 else "FAIL"
    grav_s = "PASS" if grav > 0 else "FAIL"
    fm_s = f"{fm_alpha:.2f}" if not math.isnan(fm_alpha) else "N/A"

    print(f"    Born={born:.2e} [{born_s}]  k0={gk0:.6f} [{k0_s}]")
    print(f"    Grav={grav:+.6f} ({dr}) [{grav_s}]  F~M={fm_s}  ({elapsed:.0f}s)")

    return {"h": h, "kernel": kernel_name, "born": born, "k0": gk0,
            "grav": grav, "grav_dir": dr, "fm_alpha": fm_alpha,
            "time": elapsed, "signal": True}


def main():
    print("=" * 70)
    print("3+1D SAME-GEOMETRY REFINEMENT: h=1.0 vs h=0.5 at W=3")
    print("=" * 70)
    print()
    print("Both runs use W=3, L=10, spatial-only 1/r^2 field.")
    print("Only h varies. This isolates resolution from box-size effects.")
    print()

    kernels = [
        ("exp(-0.8t^2)", lambda t: math.exp(-0.8 * t * t)),
        ("cos^2(theta)", lambda t: math.cos(t) ** 2),
    ]

    results = []
    for h in [1.0, 0.5]:
        print(f"--- h = {h} ---")
        for name, wfn in kernels:
            r = run_quick_card(h, name, wfn)
            results.append(r)

    # Summary
    print(f"\n{'='*70}")
    print("COMPARISON TABLE (W=3 fixed, h varies)")
    print(f"{'='*70}")
    print(f"{'h':>4} {'kernel':>15} | {'Born':>10} | {'k=0':>10} | {'gravity':>12} | {'F~M':>6}")
    print("-" * 70)
    for r in results:
        if not r["signal"]:
            print(f"{r['h']:>4} {r['kernel']:>15} | NO SIGNAL")
            continue
        born_s = f"{r['born']:.2e}"
        grav_s = f"{r['grav']:+.6f} {r['grav_dir']}"
        fm_s = f"{r['fm_alpha']:.2f}" if not math.isnan(r['fm_alpha']) else "N/A"
        print(f"{r['h']:>4.1f} {r['kernel']:>15} | {born_s:>10} | {r['k0']:>10.6f} | {grav_s:>12} | {fm_s:>6}")

    # Verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    h1_results = [r for r in results if r["h"] == 1.0 and r["signal"]]
    h05_results = [r for r in results if r["h"] == 0.5 and r["signal"]]

    h1_toward = [r for r in h1_results if r["grav"] > 0]
    h05_toward = [r for r in h05_results if r["grav"] > 0]

    if not h1_toward and h05_toward:
        print("\n  h=1.0: AWAY for all kernels")
        print("  h=0.5: TOWARD for some/all kernels")
        print("  ==> RESOLUTION is the relevant variable (not box size)")
        print("  ==> h <= 0.5 required for 3+1D gravity with spatial-only field")
    elif h1_toward and h05_toward:
        print("\n  Both h values give TOWARD gravity")
        print("  ==> h=1.0 is already sufficient at W=3")
        print("  ==> The h=1.0 AWAY at W=4 was a box-size effect, not resolution")
    elif not h1_toward and not h05_toward:
        print("\n  BOTH h values give AWAY gravity at W=3")
        print("  ==> W=3 may be too small for 3+1D gravity")
        print("  ==> The h=0.5/W=3 TOWARD from the earlier run needs investigation")
    else:
        print("\n  MIXED: results depend on kernel choice at each h")

    print()


if __name__ == "__main__":
    main()
