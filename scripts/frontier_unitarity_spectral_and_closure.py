#!/usr/bin/env python3
"""Unitarity hypothesis: layer normalization fixes spectral gravity.

HYPOTHESIS: Non-unitarity (spectral radius > 1) causes all four negatives.
Layer normalization fixes them.

The key idea: after each layer propagation step, normalize amplitudes so that
sum|amps|^2 = 1 over the new layer. This preserves:
  - Phase pattern (relative phases unchanged)
  - Probability distribution shape (relative |amps|^2 unchanged)
  - Born rule (linearity within each layer preserved)
But kills the exponential amplitude growth that creates 10^22 hierarchy.

Part 1: Spectral gravity with layer normalization
  - Propagate with normalization for each k, measure centroid shift
  - Spectral average (equal amplitude) across all k
  - If TOWARD: non-unitarity was the problem

Part 2: Lorentzian closure card with normalization at k=7
  - Born, k=0, gravity, F~M, d_TV, decoherence
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
LAM = 10.0
N_YBINS = 8
PHYS_W = 6
PHYS_L = 12
H = 0.5
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
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

    def propagate(self, field, k, blocked_set, action_mode="lorentzian"):
        """Lorentzian action: S = L * (1 - f * cos(2theta))."""
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

    def propagate_normalized(self, field, k, blocked_set, action_mode="lorentzian"):
        """Same as propagate() but normalizes amplitudes after each layer.

        After computing amps at layer+1, divide by sqrt(sum|amps|^2) over
        that layer only. This preserves:
          - Phase pattern (relative phases unchanged)
          - Probability shape (relative |amps|^2 unchanged)
        But makes effective spectral radius = 1.
        """
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

            # === LAYER NORMALIZATION ===
            layer_amps = amps[ld:ld + self.npl]
            norm2 = np.sum(np.abs(layer_amps)**2)
            if norm2 > 1e-60:
                amps[ld:ld + self.npl] = layer_amps / math.sqrt(norm2)

        return amps


def make_field(lat, z_mass_phys, strength):
    """Spatial-only 1/r field: mass at z=z_mass_phys on the x=2L/3 layer."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
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


def main():
    print("=" * 72)
    print("UNITARITY HYPOTHESIS: LAYER NORMALIZATION FIXES SPECTRAL GRAVITY")
    print("=" * 72)
    print()
    print("Hypothesis: Non-unitarity (spectral radius > 1) causes all four")
    print("negatives. Layer normalization (norm after each layer) fixes them.")
    print()
    print("Normalization preserves phase pattern and relative amplitudes")
    print("but kills exponential growth (effective spectral radius = 1).")
    print()

    t0 = time.time()
    K_TARGET = 7.0

    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits(lat)
    field_f = np.zeros(lat.n)
    field_m3, _ = make_field(lat, 3, STRENGTH)

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={H}")
    print(f"Action: S = L*(1 - f*cos(2theta))  [Lorentzian split]")
    print()

    # ================================================================
    # PART 1: SPECTRAL GRAVITY WITH LAYER NORMALIZATION
    # ================================================================
    print("=" * 72)
    print("PART 1: SPECTRAL GRAVITY WITH LAYER NORMALIZATION")
    print("=" * 72)
    print()

    k_values = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]

    # First: unnormalized baseline for comparison
    print("--- Unnormalized (original) per-k gravity ---")
    print(f"  {'k':>5} | {'centroid_flat':>14} | {'centroid_mass':>14} | {'delta':>12} | {'dir':>6} | {'max|amp|':>12}")
    print(f"  {'-'*72}")

    unnorm_deltas = {}
    for kk in k_values:
        af = lat.propagate(field_f, kk, blocked)
        am = lat.propagate(field_m3, kk, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        pm = sum(abs(am[d])**2 for d in det)
        if pf > 1e-30 and pm > 1e-30:
            zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            unnorm_deltas[kk] = delta
            dr = "TOWARD" if delta > 0 else "AWAY"
            max_amp = max(abs(am[d]) for d in det)
            print(f"  {kk:>5.1f} | {zf:>14.6f} | {zm:>14.6f} | {delta:>+12.6f} | {dr:>6} | {max_amp:>12.2e}")
        else:
            unnorm_deltas[kk] = 0.0
            print(f"  {kk:>5.1f} | {'(zero)':>14} | {'(zero)':>14} | {'N/A':>12} | {'N/A':>6} | {'N/A':>12}")

    n_toward_unnorm = sum(1 for d in unnorm_deltas.values() if d > 0)
    n_away_unnorm = sum(1 for d in unnorm_deltas.values() if d < 0)
    print(f"\n  Unnormalized: {n_toward_unnorm} TOWARD, {n_away_unnorm} AWAY out of {len(k_values)}")

    # Unnormalized spectral average
    print("\n--- Unnormalized spectral average ---")
    psi_total_flat = np.zeros(lat.n, dtype=np.complex128)
    psi_total_mass = np.zeros(lat.n, dtype=np.complex128)
    for kk in k_values:
        af = lat.propagate(field_f, kk, blocked)
        am = lat.propagate(field_m3, kk, blocked)
        psi_total_flat += af
        psi_total_mass += am

    pf_spec = sum(abs(psi_total_flat[d])**2 for d in det)
    pm_spec = sum(abs(psi_total_mass[d])**2 for d in det)
    if pf_spec > 1e-30 and pm_spec > 1e-30:
        zf_spec = sum(abs(psi_total_flat[d])**2 * pos[d, 2] for d in det) / pf_spec
        zm_spec = sum(abs(psi_total_mass[d])**2 * pos[d, 2] for d in det) / pm_spec
        delta_spec = zm_spec - zf_spec
        dr_spec = "TOWARD" if delta_spec > 0 else "AWAY"
        print(f"  Spectral centroid shift: {delta_spec:+.6f} ({dr_spec})")
        print(f"  (Dominated by highest-amplitude k due to 10^N hierarchy)")
    else:
        delta_spec = 0.0
        dr_spec = "N/A"
        print(f"  Spectral average: zero amplitude at detector")

    # Now: NORMALIZED per-k gravity
    print()
    print("--- Normalized (layer-norm) per-k gravity ---")
    print(f"  {'k':>5} | {'centroid_flat':>14} | {'centroid_mass':>14} | {'delta':>12} | {'dir':>6} | {'max|amp|':>12}")
    print(f"  {'-'*72}")

    norm_deltas = {}
    for kk in k_values:
        af = lat.propagate_normalized(field_f, kk, blocked)
        am = lat.propagate_normalized(field_m3, kk, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        pm = sum(abs(am[d])**2 for d in det)
        if pf > 1e-30 and pm > 1e-30:
            zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            norm_deltas[kk] = delta
            dr = "TOWARD" if delta > 0 else "AWAY"
            max_amp = max(abs(am[d]) for d in det)
            print(f"  {kk:>5.1f} | {zf:>14.6f} | {zm:>14.6f} | {delta:>+12.6f} | {dr:>6} | {max_amp:>12.2e}")
        else:
            norm_deltas[kk] = 0.0
            print(f"  {kk:>5.1f} | {'(zero)':>14} | {'(zero)':>14} | {'N/A':>12} | {'N/A':>6} | {'N/A':>12}")

    n_toward_norm = sum(1 for d in norm_deltas.values() if d > 0)
    n_away_norm = sum(1 for d in norm_deltas.values() if d < 0)
    print(f"\n  Normalized: {n_toward_norm} TOWARD, {n_away_norm} AWAY out of {len(k_values)}")

    # Normalized spectral average (NOW all k contribute equally)
    print("\n--- Normalized spectral average (equal-weight) ---")
    psi_norm_flat = np.zeros(lat.n, dtype=np.complex128)
    psi_norm_mass = np.zeros(lat.n, dtype=np.complex128)
    for kk in k_values:
        af = lat.propagate_normalized(field_f, kk, blocked)
        am = lat.propagate_normalized(field_m3, kk, blocked)
        psi_norm_flat += af
        psi_norm_mass += am

    pf_nspec = sum(abs(psi_norm_flat[d])**2 for d in det)
    pm_nspec = sum(abs(psi_norm_mass[d])**2 for d in det)
    if pf_nspec > 1e-30 and pm_nspec > 1e-30:
        zf_nspec = sum(abs(psi_norm_flat[d])**2 * pos[d, 2] for d in det) / pf_nspec
        zm_nspec = sum(abs(psi_norm_mass[d])**2 * pos[d, 2] for d in det) / pm_nspec
        delta_nspec = zm_nspec - zf_nspec
        dr_nspec = "TOWARD" if delta_nspec > 0 else "AWAY"
        print(f"  Spectral centroid shift: {delta_nspec:+.6f} ({dr_nspec})")
        print(f"  (All k contribute equally because normalization equalizes amplitudes)")
    else:
        delta_nspec = 0.0
        dr_nspec = "N/A"
        print(f"  Normalized spectral average: zero amplitude at detector")

    # Part 1 verdict
    print()
    print("-" * 72)
    print("PART 1 VERDICT:")
    if delta_nspec > 0:
        print(f"  CONFIRMED: Normalized spectral average is TOWARD ({delta_nspec:+.6f})")
        print(f"  Non-unitarity WAS the problem. Normalization fixes spectral gravity.")
    else:
        print(f"  FALSIFIED: Normalized spectral average is AWAY ({delta_nspec:+.6f})")
        print(f"  Non-unitarity is NOT the only problem.")
    print(f"  Per-k: unnorm {n_toward_unnorm}/{len(k_values)} TOWARD, norm {n_toward_norm}/{len(k_values)} TOWARD")
    print(f"  Spectral: unnorm {dr_spec}, norm {dr_nspec}")
    print(f"  Time so far: {time.time()-t0:.0f}s")

    # ================================================================
    # PART 2: CLOSURE CARD WITH NORMALIZATION AT k=7
    # ================================================================
    print()
    print("=" * 72)
    print(f"PART 2: CLOSURE CARD WITH LAYER NORMALIZATION AT k={K_TARGET}")
    print("=" * 72)
    print()

    # Flat baselines (normalized)
    af_n = lat.propagate_normalized(field_f, K_TARGET, blocked)
    pf_n = sum(abs(af_n[d])**2 for d in det)
    zf_n = sum(abs(af_n[d])**2 * pos[d, 2] for d in det) / pf_n if pf_n > 1e-30 else 0

    # === 1. Born (I3 test) ===
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a + s_b)),
                               ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate_normalized(field_f, K_TARGET, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    born_pass = born < 1e-6
    print(f"1. Born |I3|/P = {born:.2e}  [{'PASS' if born < 1e-10 else 'MARGINAL' if born < 1e-6 else 'FAIL'}]")
    if born >= 1e-6:
        print(f"   CRITICAL: Normalization is nonlinear between layers.")
        print(f"   Born rule (superposition linearity) may be broken.")

    # === 2. k=0 gravity (should be zero) ===
    am0_n = lat.propagate_normalized(field_m3, 0.0, blocked)
    af0_n = lat.propagate_normalized(field_f, 0.0, blocked)
    pm0_n = sum(abs(am0_n[d])**2 for d in det)
    pf0_n = sum(abs(af0_n[d])**2 for d in det)
    gk0 = 0
    if pm0_n > 1e-30 and pf0_n > 1e-30:
        gk0 = (sum(abs(am0_n[d])**2 * pos[d, 2] for d in det) / pm0_n
               - sum(abs(af0_n[d])**2 * pos[d, 2] for d in det) / pf0_n)
    print(f"2. k=0 gravity = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # === 3. Gravity at z=3 ===
    am3_n = lat.propagate_normalized(field_m3, K_TARGET, blocked)
    pm3_n = sum(abs(am3_n[d])**2 for d in det)
    grav = (sum(abs(am3_n[d])**2 * pos[d, 2] for d in det) / pm3_n - zf_n) if pm3_n > 1e-30 else 0
    dr = "TOWARD" if grav > 0 else "AWAY"
    print(f"3. Gravity z=3 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # === 4. F proportional to M ===
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate_normalized(fm, K_TARGET, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf_n
            if abs(delta) > 1e-12:
                m_data.append(s); g_data.append(abs(delta))
    fm_alpha = float('nan')
    fm_r2 = 0
    if len(m_data) >= 3:
        fm_alpha, fm_r2 = fit_power(m_data, g_data)
        if fm_alpha is None:
            fm_alpha = float('nan')
    print(f"4. F~M alpha = {fm_alpha:.2f} (R^2={fm_r2:.4f})  [{'PASS' if not math.isnan(fm_alpha) and abs(fm_alpha - 1.0) < 0.2 else 'CHECK'}]")

    # === 5. d_TV (slit distinguishability) ===
    pa = lat.propagate_normalized(field_f, K_TARGET, blocked | set(sb))
    pb = lat.propagate_normalized(field_f, K_TARGET, blocked | set(sa))
    da = {d: abs(pa[d])**2 for d in det}
    db_ = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[d] / na2 - db_[d] / nb2) for d in det) if na2 > 1e-30 and nb2 > 1e-30 else 0
    print(f"5. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")

    # === 6. Decoherence ===
    bw = 2 * (PHYS_W + 1) / N_YBINS
    bl_layer = lat.nl // 3
    ed = max(1, round(lat.nl / 6)); st = bl_layer + 1; sp = min(lat.nl - 1, st + ed)
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
    pur = decoherence_purity(pa, pb, det, Dcl)
    decoh = 100 * (1 - pur)
    print(f"6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # === 7. Distance law ===
    b_data = []; d_data = []
    print(f"7. Distance law (normalized):")
    for z_mass in range(2, 8):
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate_normalized(fm, K_TARGET, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf_n
            sign = "T" if delta > 0 else "A"
            print(f"   z={z_mass}: {delta:+.6f} ({sign})")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)
    n_tw = len(b_data)
    dist_slope = None
    dist_r2 = None
    if len(b_data) >= 3:
        d_arr = np.array(d_data); peak_i = int(np.argmax(d_arr))
        if peak_i < len(b_data) - 2:
            dist_slope, dist_r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
    if dist_slope is not None:
        print(f"   TOWARD: {n_tw}/6, tail b^({dist_slope:.2f}) R^2={dist_r2:.3f}")
    else:
        print(f"   TOWARD: {n_tw}/6")

    # ================================================================
    # COMPARISON: NORMALIZED vs UNNORMALIZED
    # ================================================================
    print()
    print("=" * 72)
    print("COMPARISON: NORMALIZED vs UNNORMALIZED")
    print("=" * 72)
    print()
    print(f"  {'k':>5} | {'unnorm delta':>14} | {'norm delta':>14} | {'same dir?':>10}")
    print(f"  {'-'*50}")
    for kk in k_values:
        ud = unnorm_deltas.get(kk, 0)
        nd = norm_deltas.get(kk, 0)
        same = "YES" if (ud > 0 and nd > 0) or (ud < 0 and nd < 0) else "NO"
        print(f"  {kk:>5.1f} | {ud:>+14.6f} | {nd:>+14.6f} | {same:>10}")

    # ================================================================
    # FINAL VERDICT
    # ================================================================
    print()
    print("=" * 72)
    print("FINAL VERDICT")
    print("=" * 72)
    print()

    all_pass = (born < 1e-6 and abs(gk0) < 1e-6 and grav > 0
                and not math.isnan(fm_alpha) and abs(fm_alpha - 1.0) < 0.3)

    print(f"  Spectral gravity (Part 1):")
    print(f"    Unnormalized spectral average: {dr_spec}")
    print(f"    Normalized spectral average:   {dr_nspec} ({delta_nspec:+.6f})")
    print(f"    Per-k TOWARD: unnorm {n_toward_unnorm}/{len(k_values)}, norm {n_toward_norm}/{len(k_values)}")
    print()
    print(f"  Closure card (Part 2, normalized k={K_TARGET}):")
    print(f"    Born:        {born:.2e}  [{'PASS' if born < 1e-10 else 'MARGINAL' if born < 1e-6 else 'FAIL'}]")
    print(f"    k=0:         {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")
    print(f"    Gravity:     {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")
    print(f"    F~M:         {fm_alpha:.2f} (R^2={fm_r2:.4f})  [{'PASS' if not math.isnan(fm_alpha) and abs(fm_alpha-1)<0.2 else 'CHECK'}]")
    print(f"    d_TV:        {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")
    print(f"    Decoherence: {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")
    print(f"    TOWARD:      {n_tw}/6")
    print()

    if delta_nspec > 0 and all_pass:
        print("  HYPOTHESIS CONFIRMED:")
        print("    Layer normalization fixes spectral gravity AND preserves the closure card.")
        print("    Non-unitarity was the root cause of spectral AWAY averaging.")
        print("    The model is fundamentally a PHASE effect — magnitudes are irrelevant.")
    elif delta_nspec > 0 and not all_pass:
        print("  PARTIAL CONFIRMATION:")
        print("    Spectral gravity is fixed, but some closure card tests fail.")
        print("    Normalization helps spectral averaging but may break Born rule.")
        if born >= 1e-6:
            print("    CRITICAL: Born failure means normalization is too nonlinear.")
    elif delta_nspec <= 0 and all_pass:
        print("  PARTIAL: Single-k gravity survives normalization but spectral average")
        print("    remains AWAY. The TOWARD majority does not dominate even with equal weights.")
    else:
        print("  FALSIFIED: Normalization does not fix spectral gravity and breaks closure.")

    print(f"\n  Total time: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
