#!/usr/bin/env python3
"""Dimension-dependent kernel test: w(theta) = cos^(d_spatial)(theta).

HYPOTHESIS: The angular kernel should scale with spatial dimension.
  In 2+1D (2 spatial dims): w(theta) = cos^2(theta)
  In 3+1D (3 spatial dims): w(theta) = cos^3(theta)

Adding one power of cos(theta) per spatial dimension compensates for
the growing path density at large theta (which scales as sin^(d-1)(theta)),
maintaining a balanced gravity-to-isotropy trade-off across dimensions.

EXPERIMENT:
  Part 1 (2+1D): Compare cos(t), cos^2(t), cos^3(t)
  Part 2 (3+1D): Compare cos^2(t), cos^3(t), cos^4(t), exp(-0.8t^2)

FALSIFICATION: If the optimal kernel power doesn't track d_spatial,
the kernel is dimension-independent.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

# Shared constants
K = 5.0
LAM = 10.0
N_YBINS = 6
STRENGTH = 5e-5

# --- 2+1D constants ---
PHYS_W_3D = 6
MAX_D_PHYS_3D = 3
POWER_3D = 2       # kernel 1/L^2 for 2 spatial dimensions

# --- 3+1D constants ---
PHYS_W_4D = 4
MAX_D_PHYS_4D = 2
POWER_4D = 3       # kernel 1/L^3 for 3 spatial dimensions


# =========================================================================
# Lattice3D (2+1D spacetime: 2 spatial + 1 causal)
# Adapted from lattice_3d_valley_linear_card.py with weight_fn parameter
# =========================================================================
class Lattice3D:
    """3D ordered lattice (2 spatial + 1 causal) with selectable kernel."""

    def __init__(self, phys_l, phys_w, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.exp(-0.8 * t * t)

        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS_3D / h))
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
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_3D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# =========================================================================
# Lattice4D (3+1D spacetime: 3 spatial + 1 causal)
# Copied from frontier_3plus1d_closure_card.py
# =========================================================================
class Lattice4D:
    """4D ordered lattice (3 spatial + 1 causal) with selectable kernel."""

    def __init__(self, phys_l, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.exp(-0.8 * t * t)

        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(PHYS_W_4D / h)
        self.max_d = max(1, round(MAX_D_PHYS_4D / h))
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
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_4D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# =========================================================================
# Shared helpers
# =========================================================================

def make_field_3d(lat, z_mass_phys, strength):
    """1/r field for 2 spatial dimensions (2D Coulomb)."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx = lat.pos[mi]
    r = np.sqrt(np.sum((lat.pos - mx) ** 2, axis=1)) + 0.1
    return strength / r, mi


def make_field_4d(lat, z_mass_phys, strength):
    """1/r^2 field for 3 spatial dimensions (3D Coulomb)."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    mx = lat.pos[mi]
    r = np.sqrt(np.sum((lat.pos - mx) ** 2, axis=1)) + 0.1
    return strength / (r ** 2), mi


def setup_slits_3d(lat):
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
    return bi, sa, sb, blocked


def setup_slits_4d(lat):
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


# =========================================================================
# 2+1D card runner
# =========================================================================

def run_card_3d(kernel_name, weight_fn, h, phys_l, phys_w):
    """Run the 2+1D measurement suite. Returns dict of results."""
    t_total = time.time()

    lat = Lattice3D(phys_l, phys_w, h, weight_fn=weight_fn)
    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits_3d(lat)
    field_f = np.zeros(lat.n)

    print(f"\n{'='*60}")
    print(f"  2+1D: {kernel_name}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers, h={h}, W={phys_w}, L={phys_l}")
    print(f"  kernel=1/L^{POWER_3D}, field=s/r, {len(lat._off)} offsets/node")
    print(f"{'='*60}")

    # Flat propagation
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector.")
        return {"kernel": kernel_name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Flat: det_prob={pf:.4e}, z_flat={zf:.6f}")

    results = {"kernel": kernel_name, "signal": True}

    # Born rule
    t0 = time.time()
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
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
    print(f"  Born |I3|/P = {born:.2e}  ({time.time()-t0:.0f}s)")

    # Gravity sign at z=3
    field_m, _ = make_field_3d(lat, 3, STRENGTH)
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    dr = "TOWARD" if grav > 0 else "AWAY"
    results["grav"] = grav
    results["grav_dir"] = dr
    print(f"  Gravity z=3 = {grav:+.6f} ({dr})")

    # F~M scaling
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field_3d(lat, 3, s)
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
    print(f"  F~M alpha = {fm_alpha:.2f}")

    results["time"] = time.time() - t_total
    print(f"  Time: {results['time']:.0f}s")
    return results


# =========================================================================
# 3+1D card runner
# =========================================================================

def run_card_4d(kernel_name, weight_fn, h, phys_l):
    """Run the 3+1D measurement suite. Returns dict of results."""
    t_total = time.time()

    lat = Lattice4D(phys_l, h, weight_fn=weight_fn)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits_4d(lat)
    field_f = np.zeros(lat.n)

    print(f"\n{'='*60}")
    print(f"  3+1D: {kernel_name}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers, h={h}, W={PHYS_W_4D}, L={phys_l}")
    print(f"  kernel=1/L^{POWER_4D}, field=s/r^2, {len(lat._off)} offsets/node")
    print(f"{'='*60}")

    # Flat propagation
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector.")
        return {"kernel": kernel_name, "signal": False}
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Flat: det_prob={pf:.4e}, z_flat={zf:.6f}")

    results = {"kernel": kernel_name, "signal": True}

    # Born rule
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
    print(f"  Born |I3|/P = {born:.2e}  ({time.time()-t0:.0f}s)")

    # Gravity sign at z=2
    field_m, _ = make_field_4d(lat, 2, STRENGTH)
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    dr = "TOWARD" if grav > 0 else "AWAY"
    results["grav"] = grav
    results["grav_dir"] = dr
    print(f"  Gravity z=2 = {grav:+.6f} ({dr})")

    # F~M scaling
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field_4d(lat, 2, s)
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
    print(f"  F~M alpha = {fm_alpha:.2f}")

    results["time"] = time.time() - t_total
    print(f"  Time: {results['time']:.0f}s")
    return results


# =========================================================================
# Main
# =========================================================================

def main():
    print("=" * 70)
    print("DIMENSION-DEPENDENT KERNEL TEST")
    print("  w(theta) = cos^(d_spatial)(theta)")
    print("=" * 70)
    print()
    print("HYPOTHESIS: cos^(d_spatial)(theta) gives the best gravity-to-isotropy")
    print("trade-off in each dimension, compensating for sin^(d-1)(theta) path")
    print("density growth at large angles.")
    print()

    # =====================================================================
    # Part 1: 2+1D (d_spatial = 2)
    # =====================================================================
    print()
    print("#" * 70)
    print("# PART 1: 2+1D (2 spatial dimensions)")
    print("# Dimension-matched kernel: cos^2(theta)")
    print("#" * 70)

    h_3d = 0.5
    L_3d = 12
    W_3d = 6

    kernels_3d = [
        ("cos^1(t) [d-1]",  lambda t: max(0.0, math.cos(t)) ** 1),
        ("cos^2(t) [d=2]",  lambda t: max(0.0, math.cos(t)) ** 2),
        ("cos^3(t) [d+1]",  lambda t: max(0.0, math.cos(t)) ** 3),
    ]

    results_3d = []
    for name, wfn in kernels_3d:
        r = run_card_3d(name, wfn, h_3d, L_3d, W_3d)
        results_3d.append(r)

    # =====================================================================
    # Part 2: 3+1D (d_spatial = 3)
    # =====================================================================
    print()
    print("#" * 70)
    print("# PART 2: 3+1D (3 spatial dimensions)")
    print("# Dimension-matched kernel: cos^3(theta)")
    print("#" * 70)

    h_4d = 1.0
    L_4d = 10

    kernels_4d = [
        ("cos^2(t) [d-1]",   lambda t: max(0.0, math.cos(t)) ** 2),
        ("cos^3(t) [d=3]",   lambda t: max(0.0, math.cos(t)) ** 3),
        ("cos^4(t) [d+1]",   lambda t: max(0.0, math.cos(t)) ** 4),
        ("exp(-0.8t^2)",      lambda t: math.exp(-0.8 * t * t)),
    ]

    results_4d = []
    for name, wfn in kernels_4d:
        r = run_card_4d(name, wfn, h_4d, L_4d)
        results_4d.append(r)

    # =====================================================================
    # Summary tables
    # =====================================================================
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    # 2+1D table
    print()
    print("--- 2+1D (d_spatial = 2, kernel 1/L^2, field s/r) ---")
    print(f"{'Kernel':<18s} | {'Born |I3|/P':>12s} | {'Gravity':>10s} | {'Dir':>6s} | {'F~M alpha':>10s}")
    print("-" * 66)
    for r in results_3d:
        if not r.get("signal", False):
            print(f"{r['kernel']:<18s} | {'NO SIGNAL':>12s} |")
            continue
        b = f"{r['born']:.2e}" if not math.isnan(r['born']) else "N/A"
        g = f"{r['grav']:+.6f}"
        d = r.get('grav_dir', '?')
        a = f"{r['fm_alpha']:.2f}" if not math.isnan(r['fm_alpha']) else "N/A"
        print(f"{r['kernel']:<18s} | {b:>12s} | {g:>10s} | {d:>6s} | {a:>10s}")

    # 3+1D table
    print()
    print("--- 3+1D (d_spatial = 3, kernel 1/L^3, field s/r^2) ---")
    print(f"{'Kernel':<18s} | {'Born |I3|/P':>12s} | {'Gravity':>10s} | {'Dir':>6s} | {'F~M alpha':>10s}")
    print("-" * 66)
    for r in results_4d:
        if not r.get("signal", False):
            print(f"{r['kernel']:<18s} | {'NO SIGNAL':>12s} |")
            continue
        b = f"{r['born']:.2e}" if not math.isnan(r['born']) else "N/A"
        g = f"{r['grav']:+.6f}"
        d = r.get('grav_dir', '?')
        a = f"{r['fm_alpha']:.2f}" if not math.isnan(r['fm_alpha']) else "N/A"
        print(f"{r['kernel']:<18s} | {b:>12s} | {g:>10s} | {d:>6s} | {a:>10s}")

    # =====================================================================
    # Verdict
    # =====================================================================
    print()
    print("=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Find best kernel in each dimension
    def score(r):
        """Higher is better: gravity magnitude * (1 if TOWARD else -1), penalize bad Born."""
        if not r.get("signal", False):
            return -999
        g = r.get("grav", 0)
        b = r.get("born", 1.0)
        if math.isnan(b):
            b = 1.0
        sign = 1 if g > 0 else -1
        return sign * abs(g) - 100 * b

    best_3d = max(results_3d, key=score)
    best_4d = max(results_4d, key=score)

    print()
    print(f"  2+1D best kernel: {best_3d['kernel']}")
    print(f"    gravity={best_3d.get('grav', 0):+.6f}, Born={best_3d.get('born', float('nan')):.2e}")
    print()
    print(f"  3+1D best kernel: {best_4d['kernel']}")
    print(f"    gravity={best_4d.get('grav', 0):+.6f}, Born={best_4d.get('born', float('nan')):.2e}")

    # Check if dimension-matched wins in both
    dim_matched_2d = [r for r in results_3d if "d=2" in r["kernel"]]
    dim_matched_3d = [r for r in results_4d if "d=3" in r["kernel"]]

    print()
    if dim_matched_2d and dim_matched_3d:
        dm2 = dim_matched_2d[0]
        dm3 = dim_matched_3d[0]
        win_2d = score(dm2) >= score(best_3d) - 1e-8
        win_3d = score(dm3) >= score(best_4d) - 1e-8

        if win_2d and win_3d:
            print("  HYPOTHESIS SUPPORTED: cos^(d_spatial)(theta) wins in BOTH dimensions.")
            print("  The kernel should scale with spatial dimension.")
        elif win_2d or win_3d:
            dim_win = "2+1D" if win_2d else "3+1D"
            dim_lose = "3+1D" if win_2d else "2+1D"
            print(f"  MIXED: cos^(d_spatial) wins in {dim_win} but not {dim_lose}.")
            print(f"  Evidence is inconclusive.")
        else:
            print("  HYPOTHESIS FALSIFIED: cos^(d_spatial) is NOT the best kernel")
            print("  in either dimension. The optimal power is dimension-independent,")
            print("  or the relationship is more complex.")

    # Check if same power wins in both
    print()
    best_3d_power = best_3d["kernel"].split("^")[1][0] if "^" in best_3d["kernel"] else "?"
    best_4d_power = best_4d["kernel"].split("^")[1][0] if "^" in best_4d["kernel"] else "?"
    print(f"  Best power in 2+1D: {best_3d_power}")
    print(f"  Best power in 3+1D: {best_4d_power}")
    if best_3d_power == best_4d_power and best_3d_power != "?":
        print(f"  Same power ({best_3d_power}) wins in both dims => dimension-INDEPENDENT kernel")
    else:
        print(f"  Different powers win => kernel may be dimension-DEPENDENT")

    print()


if __name__ == "__main__":
    main()
