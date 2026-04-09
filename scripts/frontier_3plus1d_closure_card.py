#!/usr/bin/env python3
"""3+1D valley-linear closure card with kernel comparison.

THIS IS THE PHYSICAL SPACETIME DIMENSION TEST.
  - 3 spatial dimensions (y, z, w) + 1 causal (x) = 3+1D
  - Kernel: 1/L^3 (p = d_spatial = 3)
  - Action: S = L(1-f) (valley-linear)
  - Field: strength / r^2 (3D Coulomb, from 3 spatial dimensions)
  - Measure: h^3 (3 transverse dimensions)

Tests both angular kernels head-to-head:
  - exp(-0.8*theta^2) (current default)
  - cos^2(theta) (candidate with 10x better isotropy in 2+1D)

The "3D lattice" used previously was actually 2+1D spacetime.
This script tests 3+1D — the actual physical dimension.

HYPOTHESIS: The valley-linear action with cos^2(theta) kernel
  produces a viable 3+1D model (passes Born, gravity, k=0, F~M).

FALSIFICATION: If gravity is repulsive or Born fails with either
  kernel, the 3+1D ordered lattice does not support gravity.

Based on: lattice_4d_kernel_test.py (Lattice4D class)
         lattice_3d_valley_linear_card.py (10-property audit pattern)
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

K = 5.0
LAM = 10.0
N_YBINS = 6
PHYS_W = 4          # transverse half-extent in each spatial dim
MAX_D_PHYS = 2      # physical reach for edge connectivity
STRENGTH = 5e-5     # field coupling
POWER = 3           # kernel 1/L^3 for 3 spatial dimensions


class Lattice4D:
    """4D ordered lattice (3 spatial + 1 causal) with selectable kernel."""

    def __init__(self, phys_l, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.exp(-0.8 * t * t)

        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(PHYS_W / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3  # 3 transverse dimensions
        self.n = self.nl * self.npl
        self._hm = h ** 3   # measure for 3 transverse dims

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
        """Propagate with valley-linear action, 1/L^3 kernel, h^3 measure."""
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
                # Valley-linear action
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field(lat, z_mass_phys, strength):
    """Static 3D Coulomb field: 1/r_spatial^2 using SPATIAL dims only.

    The field depends on spatial separation (y, z, w) from the mass,
    NOT on causal (x/layer) separation. This is a static field —
    every layer sees the same spatial potential from the mass position.
    The mass is placed at (y=0, z=z_mass, w=0) on every layer.
    """
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    # Mass spatial position: (y, z, w) from the mass node
    my, mz, mw = lat.pos[mi, 1], lat.pos[mi, 2], lat.pos[mi, 3]
    # Spatial-only radius (columns 1,2,3 = y,z,w; exclude column 0 = x)
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my) ** 2 +
        (lat.pos[:, 2] - mz) ** 2 +
        (lat.pos[:, 3] - mw) ** 2
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


def decoherence_purity(pa, pb, det, dcl):
    a = np.array([pa[d] for d in det], dtype=np.complex128)
    b = np.array([pb[d] for d in det], dtype=np.complex128)
    gram = np.array([[np.vdot(a, a), np.vdot(a, b)],
                     [np.vdot(b, a), np.vdot(b, b)]], dtype=np.complex128)
    mix = np.array([[1.0, dcl], [dcl, 1.0]], dtype=np.complex128)
    mg = mix @ gram
    tr = np.trace(mg).real
    if tr <= 1e-30:
        return 1.0
    return float((np.trace(mg @ mg) / (tr * tr)).real)


def run_card(kernel_name, weight_fn, h, phys_l):
    """Run the 3+1D closure card. Returns dict of results."""
    t_total = time.time()

    lat = Lattice4D(phys_l, h, weight_fn=weight_fn)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits(lat)
    field_f = np.zeros(lat.n)

    print(f"\n{'='*70}")
    print(f"  3+1D CLOSURE CARD: {kernel_name}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers, {lat.npl} nodes/layer")
    print(f"  h={h}, W={PHYS_W}, L={phys_l}, kernel=1/L^{POWER}")
    print(f"  Action: S = L(1-f), Field: s/r^2 (3D Coulomb)")
    print(f"  {len(lat._off)} edge offsets per node")
    print(f"{'='*70}")

    # Flat propagation
    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector. Lattice too small or kernel too narrow.")
        return {"kernel": kernel_name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Flat propagation: {time.time()-t0:.1f}s, det_prob={pf:.4e}, z_flat={zf:.6f}")

    results = {"kernel": kernel_name, "signal": True}

    # 1. Born rule (3-slit Sorkin test)
    t0 = time.time()
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
    results["born"] = born
    status = "PASS" if born < 1e-10 else "FAIL"
    print(f"  1. Born |I3|/P = {born:.2e}  [{status}]  ({time.time()-t0:.0f}s)")

    # 2. k=0 control
    field_m, _ = make_field(lat, 2, STRENGTH)
    am0 = lat.propagate(field_m, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2*pos[d,2] for d in det)/pm0
               - sum(abs(af0[d])**2*pos[d,2] for d in det)/pf0)
    results["k0"] = gk0
    print(f"  2. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # 3. Gravity sign at z=2
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    dr = "TOWARD" if grav > 0 else "AWAY"
    results["grav"] = grav
    results["grav_dir"] = dr
    print(f"  3. Gravity z=2 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # 4. F~M scaling
    t0 = time.time()
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 2, s)
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
    results["fm_alpha"] = fm_alpha
    print(f"  4. F~M alpha = {fm_alpha:.2f}  [{'PASS' if not math.isnan(fm_alpha) and abs(fm_alpha-1.0)<0.3 else 'CHECK'}]  ({time.time()-t0:.0f}s)")

    # 5. d_TV (slit distinguishability)
    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = {d: abs(pa[d])**2 for d in det}; db_ = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[d]/na2 - db_[d]/nb2) for d in det) if na2 > 1e-30 and nb2 > 1e-30 else 0
    results["dtv"] = dtv
    print(f"  5. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")

    # 6. Decoherence
    bw = 2 * (PHYS_W + 1) / N_YBINS
    bl_layer = lat.nl // 3
    ed = max(1, round(lat.nl / 6)); st = bl_layer + 1; sp = min(lat.nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        for iy in range(-lat.hw, lat.hw+1):
            for iz in range(-lat.hw, lat.hw+1):
                for iw in range(-lat.hw, lat.hw+1):
                    idx = lat.nmap.get((l, iy, iz, iw))
                    if idx is not None:
                        mid.append(idx)
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS-1, int((pos[m, 1] + PHYS_W + 1) / bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba - bb)**2))
    NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    pur = decoherence_purity(pa, pb, det, Dcl)
    decoh = 100 * (1 - pur)
    results["decoh"] = decoh
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # 7. Distance law (gravity at multiple z offsets)
    b_data = []; d_data = []
    for z_mass in [1, 2, 3]:
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0: b_data.append(z_mass); d_data.append(delta)
    n_tw = len(b_data)
    results["n_toward"] = n_tw
    print(f"  7. TOWARD: {n_tw}/3")

    results["time"] = time.time() - t_total
    print(f"  Total time: {results['time']:.0f}s")
    return results


def main():
    print("=" * 70)
    print("3+1D CLOSURE CARD: VALLEY-LINEAR ON PHYSICAL SPACETIME")
    print("=" * 70)
    print()
    print("This is the PHYSICAL DIMENSION test: 3 spatial + 1 causal.")
    print("The '3D lattice' tests were actually 2+1D spacetime.")
    print()
    print("Kernel: 1/L^3 (p = d_spatial = 3)")
    print("Action: S = L(1-f) (valley-linear)")
    print("Field:  s/r^2 (3D Coulomb for 3 spatial dimensions)")
    print()
    print("HYPOTHESIS: VL + cos^2(theta) produces viable 3+1D gravity.")
    print("FALSIFICATION: if Born, gravity, or F~M fail, 3+1D is not viable.")
    print()

    # Use h=1.0 for feasibility (h=0.5 would give ~59k nodes/layer = 600k+ total)
    h = 1.0
    phys_l = 10

    kernels = [
        ("exp(-0.8*t^2)", lambda t: math.exp(-0.8 * t * t)),
        ("cos^2(theta)",  lambda t: math.cos(t) ** 2),
    ]

    all_results = []
    for name, wfn in kernels:
        r = run_card(name, wfn, h, phys_l)
        all_results.append(r)

    # Side-by-side
    print(f"\n{'='*70}")
    print("SIDE-BY-SIDE: 3+1D SPACETIME")
    print(f"{'='*70}")
    print()

    print(f"{'Property':<20s} | {'exp(-0.8t^2)':>15s} | {'cos^2(theta)':>15s}")
    print("-" * 60)

    for label, key, fmt in [
        ("Born |I3|/P", "born", ".2e"),
        ("k=0 control", "k0", ".6f"),
        ("Gravity sign", "grav", "+.6f"),
        ("Gravity dir", "grav_dir", "s"),
        ("F~M alpha", "fm_alpha", ".2f"),
        ("d_TV", "dtv", ".4f"),
        ("Decoherence %", "decoh", ".1f"),
        ("TOWARD count", "n_toward", "d"),
        ("Time (s)", "time", ".0f"),
    ]:
        vals = []
        for r in all_results:
            v = r.get(key)
            if v is None or (isinstance(v, float) and math.isnan(v)):
                vals.append("N/A")
            elif fmt == "s":
                vals.append(str(v))
            else:
                vals.append(f"{v:{fmt}}")
        print(f"{label:<20s} | {vals[0]:>15s} | {vals[1]:>15s}")

    # Verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    for r in all_results:
        if not r.get("signal", False):
            print(f"\n  {r['kernel']}: NO SIGNAL — lattice too small or kernel too narrow")
            continue

        born_pass = r["born"] < 1e-10 if not math.isnan(r["born"]) else False
        grav_pass = r["grav"] > 0
        k0_pass = abs(r["k0"]) < 1e-6
        fm_pass = not math.isnan(r["fm_alpha"]) and abs(r["fm_alpha"] - 1.0) < 0.3

        core_pass = born_pass and grav_pass and k0_pass and fm_pass
        print(f"\n  {r['kernel']}:")
        print(f"    Born:    {'PASS' if born_pass else 'FAIL'} ({r['born']:.2e})")
        print(f"    k=0:     {'PASS' if k0_pass else 'FAIL'} ({r['k0']:.6f})")
        print(f"    Gravity: {'PASS' if grav_pass else 'FAIL'} ({r['grav']:+.6f} {r['grav_dir']})")
        print(f"    F~M:     {'PASS' if fm_pass else 'CHECK'} ({r['fm_alpha']:.2f})")
        print(f"    TOWARD:  {r['n_toward']}/3")
        print(f"    Core (Born+k0+grav+F~M): {'ALL PASS' if core_pass else 'FAIL'}")

    print()
    print("  CAVEAT: h=1.0 is a coarse lattice (9 nodes per transverse dim).")
    print("  This is a coarse feasibility signal, not a physical 3+1D closure.")
    print("  The field now uses spatial-only radius (y,z,w), excluding causal x.")


if __name__ == "__main__":
    main()
