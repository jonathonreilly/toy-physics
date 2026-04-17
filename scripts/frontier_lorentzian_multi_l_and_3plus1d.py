#!/usr/bin/env python3
"""Lorentzian k=7: multi-L companion checks (props 8-9) + 3+1D feasibility.

Part 1: Multi-L checks at k=7, h=0.5
  Property 8: CL bath purity stable across L
  Property 9: gravity grows with L

Part 2: 3+1D feasibility at k=7
  Lorentzian action S = L*(1 - f*cos(2*theta)) in 4D
  Tests: Born, k=0, gravity sign, F~M

HYPOTHESIS: Lorentzian at k=7 passes multi-L checks AND 3+1D feasibility.
FALSIFICATION: If gravity doesn't grow with L, or 3+1D gravity is AWAY.
"""

from __future__ import annotations
import math
import time
import numpy as np

# --- Constants ---
BETA = 0.8
LAM = 10.0
N_YBINS = 8
STRENGTH = 5e-5

# Part 1 constants (2+1D)
MAX_D_PHYS_3D = 3
PHYS_W_3D = 6

# Part 2 constants (3+1D)
MAX_D_PHYS_4D = 2
PHYS_W_4D = 3
POWER_4D = 3  # 1/L^3 for 3 spatial dims

K = 7.0
H = 0.5


# ===================================================================
# Part 1: 2+1D Lattice3D with Lorentzian action
# ===================================================================

class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
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
                w = math.exp(-BETA * theta * theta)
                lf_factor = math.cos(2 * theta)
                self._off.append((dy, dz, L, w, lf_factor))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        """Lorentzian action: S = L * (1 - f * cos(2*theta))."""
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
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
            for dy, dz, L, w, lf_factor in self._off:
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
                act = L * (1 - lf * lf_factor)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_3d(lat, z_mass_phys, strength):
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


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


# ===================================================================
# Part 2: 3+1D Lattice4D with Lorentzian action
# ===================================================================

class Lattice4D:
    """4D ordered lattice (3 spatial + 1 causal) with Lorentzian action."""

    def __init__(self, phys_l, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(PHYS_W_4D / h)
        self.max_d = max(1, round(MAX_D_PHYS_4D / h))
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
                    w = math.exp(-BETA * theta * theta)
                    lf_factor = math.cos(2 * theta)
                    self._off.append((dy, dz, dw, L, w, lf_factor))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        """Lorentzian action: S = L*(1 - f*cos(2*theta)), 1/L^3 kernel."""
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

            for dy, dz, dw, L, w, lf_factor in self._off:
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
                act = L * (1 - lf * lf_factor)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_4D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_4d(lat, z_mass_phys, strength):
    """Spatial-only 1/r^2 field for 3+1D."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz, mw = lat.pos[mi, 1], lat.pos[mi, 2], lat.pos[mi, 3]
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my) ** 2 +
        (lat.pos[:, 2] - mz) ** 2 +
        (lat.pos[:, 3] - mw) ** 2
    ) + 0.1
    return strength / (r_spatial ** 2), mi


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
    return slope, (1 - ss_res / ss_tot if ss_tot > 0 else 0)


# ===================================================================
# Part 1: Multi-L companion checks
# ===================================================================

def run_part1():
    print("=" * 70)
    print("PART 1: MULTI-L COMPANION CHECKS (Properties 8-9)")
    print("=" * 70)
    print()
    print(f"Action: S = L*(1 - f*cos(2*theta))  [Lorentzian]")
    print(f"k={K}, h={H}, W={PHYS_W_3D}")
    print(f"Property 8: CL bath purity stable across L")
    print(f"Property 9: gravity grows with L")
    print()

    results = []
    for L_phys in [8, 10, 12, 15]:
        t0 = time.time()
        lat = Lattice3D(L_phys, PHYS_W_3D, H)
        det = [lat.nmap[(lat.nl-1, iy, iz)]
               for iy in range(-lat.hw, lat.hw+1)
               for iz in range(-lat.hw, lat.hw+1)
               if (lat.nl-1, iy, iz) in lat.nmap]
        pos = lat.pos
        bi, sa, sb, blocked = setup_slits_3d(lat)
        field_f = np.zeros(lat.n)
        field_m3, _ = make_field_3d(lat, 3, STRENGTH)

        # Flat baseline
        af = lat.propagate(field_f, K, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0

        # Gravity at z=3
        am3 = lat.propagate(field_m3, K, blocked)
        pm3 = sum(abs(am3[d])**2 for d in det)
        grav = (sum(abs(am3[d])**2*pos[d,2] for d in det)/pm3 - zf) if pm3 > 1e-30 else 0
        dr = "TOWARD" if grav > 0 else "AWAY"

        # CL bath purity
        pa = lat.propagate(field_f, K, blocked | set(sb))
        pb = lat.propagate(field_f, K, blocked | set(sa))

        bw = 2 * (PHYS_W_3D + 1) / N_YBINS
        bl_layer = lat.nl // 3
        ed = max(1, round(lat.nl / 6)); st = bl_layer + 1; sp = min(lat.nl - 1, st + ed)
        mid = []
        for l in range(st, sp):
            mid.extend([lat.nmap[(l, iy, iz)]
                        for iy in range(-lat.hw, lat.hw+1)
                        for iz in range(-lat.hw, lat.hw+1)
                        if (l, iy, iz) in lat.nmap])
        ba = np.zeros(N_YBINS, dtype=np.complex128)
        bb = np.zeros(N_YBINS, dtype=np.complex128)
        for m in mid:
            b2 = max(0, min(N_YBINS-1, int((pos[m, 1] + PHYS_W_3D + 1) / bw)))
            ba[b2] += pa[m]; bb[b2] += pb[m]
        S = float(np.sum(np.abs(ba - bb)**2))
        NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
        Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
        Dcl = math.exp(-LAM**2 * Sn)
        pur = decoherence_purity(pa, pb, det, Dcl)
        one_minus_pur = 1 - pur

        elapsed = time.time() - t0
        results.append((L_phys, grav, dr, one_minus_pur, elapsed))
        print(f"  L={L_phys:>2d}: gravity={grav:+.6f} ({dr}), 1-purity={one_minus_pur:.6f}  ({elapsed:.0f}s)")

    # Summary table
    print()
    print(f"{'L':>3s} | {'gravity':>12s} | {'direction':>9s} | {'1-purity':>12s}")
    print(f"{'-'*45}")
    for L_phys, grav, dr, omp, _ in results:
        print(f"{L_phys:>3d} | {grav:>+12.6f} | {dr:>9s} | {omp:>12.6f}")

    # Assess properties
    gravities = [r[1] for r in results]
    purities = [r[3] for r in results]

    # Prop 9: gravity grows with L
    grows = all(gravities[i] <= gravities[i+1] for i in range(len(gravities)-1))
    all_toward = all(g > 0 for g in gravities)
    print()
    print(f"Property 9 (gravity grows with L): {'PASS' if grows and all_toward else 'FAIL'}")
    if grows and all_toward:
        print(f"  Gravity monotonically increases: {[f'{g:.6f}' for g in gravities]}")
    else:
        print(f"  Gravities: {[f'{g:+.6f}' for g in gravities]}")

    # Prop 8: purity stable across L
    pur_range = max(purities) - min(purities)
    pur_mean = np.mean(purities)
    pur_cv = pur_range / pur_mean if pur_mean > 1e-10 else float('inf')
    stable = pur_cv < 1.0  # within 100% relative range
    print(f"Property 8 (purity stable): {'PASS' if stable else 'FAIL'}")
    print(f"  1-purity range: {pur_range:.6f}, mean: {pur_mean:.6f}, CV: {pur_cv:.2f}")

    return grows and all_toward and stable


# ===================================================================
# Part 2: 3+1D feasibility
# ===================================================================

def run_part2():
    print()
    print("=" * 70)
    print("PART 2: 3+1D FEASIBILITY AT k=7 (Lorentzian action)")
    print("=" * 70)
    print()
    print(f"Action: S = L*(1 - f*cos(2*theta))  [Lorentzian]")
    print(f"k={K}, h={H}, W={PHYS_W_4D}, L=10")
    print(f"Kernel: 1/L^3, Field: s/r^2, Measure: h^3")
    print()

    t_total = time.time()
    lat = Lattice4D(10, H)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits_4d(lat)
    field_f = np.zeros(lat.n)

    print(f"  Lattice: {lat.n:,} nodes, {lat.nl} layers, {lat.npl} nodes/layer")
    print(f"  {len(lat._off)} edge offsets per node")
    print()

    # Flat baseline
    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector. Lattice too small or kernel too narrow.")
        return False
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Flat propagation: {time.time()-t0:.1f}s, det_prob={pf:.4e}")

    results = {}

    # 1. Born rule
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
    born_pass = born < 1e-10 if not math.isnan(born) else False
    print(f"  1. Born |I3|/P = {born:.2e}  [{'PASS' if born_pass else 'FAIL'}]  ({time.time()-t0:.0f}s)")

    # 2. k=0 control
    field_m, _ = make_field_4d(lat, 2, STRENGTH)
    am0 = lat.propagate(field_m, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2*pos[d,2] for d in det)/pm0
               - sum(abs(af0[d])**2*pos[d,2] for d in det)/pf0)
    results["k0"] = gk0
    k0_pass = abs(gk0) < 1e-6
    print(f"  2. k=0 = {gk0:.6f}  [{'PASS' if k0_pass else 'CHECK'}]")

    # 3. Gravity sign at z=2
    am = lat.propagate(field_m, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    grav = 0
    if pm > 1e-30:
        grav = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm - zf
    dr = "TOWARD" if grav > 0 else "AWAY"
    results["grav"] = grav
    grav_pass = grav > 0
    print(f"  3. Gravity z=2 = {grav:+.6f} ({dr})  [{'PASS' if grav_pass else 'FAIL'}]")

    # 4. F~M scaling
    t0 = time.time()
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field_4d(lat, 2, s)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if abs(delta) > 1e-12:
                m_data.append(s); g_data.append(abs(delta))
    fm_alpha = float('nan')
    fm_r2 = 0
    if len(m_data) >= 3:
        slope, r2 = fit_power(m_data, g_data)
        if slope is not None:
            fm_alpha = slope
            fm_r2 = r2
    fm_pass = not math.isnan(fm_alpha) and abs(fm_alpha - 1.0) < 0.3
    results["fm_alpha"] = fm_alpha
    print(f"  4. F~M alpha = {fm_alpha:.2f} (R^2={fm_r2:.4f})  [{'PASS' if fm_pass else 'CHECK'}]  ({time.time()-t0:.0f}s)")

    total_time = time.time() - t_total
    print(f"\n  Total 3+1D time: {total_time:.0f}s")

    # Summary table
    print()
    print(f"{'Test':<10s} | {'Result':>15s}")
    print(f"{'-'*30}")
    print(f"{'Born':<10s} | {'PASS' if born_pass else 'FAIL':>15s}")
    print(f"{'k=0':<10s} | {'PASS' if k0_pass else 'FAIL':>15s}")
    print(f"{'Gravity':<10s} | {dr:>15s}")
    print(f"{'F~M':<10s} | {'PASS' if fm_pass else 'FAIL':>15s}")

    return born_pass and k0_pass and grav_pass and fm_pass


# ===================================================================
# Main
# ===================================================================

def main():
    print()
    print("=" * 70)
    print("LORENTZIAN k=7: MULTI-L CHECKS + 3+1D FEASIBILITY")
    print("=" * 70)
    print()
    print(f"HYPOTHESIS: Lorentzian at k=7 passes multi-L checks AND 3+1D feasibility.")
    print(f"FALSIFICATION: If gravity doesn't grow with L, or 3+1D gravity is AWAY.")
    print()

    t0 = time.time()

    part1_pass = run_part1()
    part2_pass = run_part2()

    print()
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    print()
    print(f"  Part 1 (multi-L):  {'PASS' if part1_pass else 'FAIL'}")
    print(f"  Part 2 (3+1D):     {'PASS' if part2_pass else 'FAIL'}")
    print()
    if part1_pass and part2_pass:
        print("  HYPOTHESIS CONFIRMED: Lorentzian at k=7 passes both multi-L")
        print("  companion checks AND 3+1D feasibility tests.")
    else:
        if not part1_pass:
            print("  FALSIFIED: Multi-L checks failed.")
        if not part2_pass:
            print("  FALSIFIED: 3+1D feasibility failed.")
    print()
    print(f"  Total wall time: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
