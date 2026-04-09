#!/usr/bin/env python3
"""3+1D wider-lattice distance law: W=4 at h=0.5 for more TOWARD points.

THE GAP: Only 2 TOWARD points in 3+1D (z=2, z=3) with W=3.
FIX: Use W=4 at h=0.5, giving 17 nodes per transverse dim,
     17^3 = 4913 nodes/layer, 21 layers = 103,173 total nodes.

Uses corrected spatial-only field (make_field with r from y,z,w only).

EXPERIMENT:
  1. Distance law: z_mass in {1,2,3,4,5,6}, measure centroid shift
  2. F~M scaling at z=3 with 6 field strengths

HYPOTHESIS: With W=4, we get 4+ TOWARD points and alpha closer to 1.0.
FALSIFICATION: If still only 2 TOWARD points, the lattice is too small.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

K = 5.0
PHYS_W = 4          # transverse half-extent (was 3, now 4)
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
    NOT on causal (x/layer) separation. This is a static field --
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


def main():
    h = 0.5
    phys_l = 10
    weight_fn = lambda t: math.exp(-0.8 * t * t)

    print("=" * 70)
    print("3+1D WIDER DISTANCE LAW: W=4, h=0.5")
    print("=" * 70)
    print()
    print("THE GAP: Only 2 TOWARD points with W=3. Need more.")
    print("FIX: PHYS_W=4 gives 17 nodes/transverse dim, 4913 nodes/layer.")
    print()
    print(f"Parameters: h={h}, W={PHYS_W}, L={phys_l}, K={K}")
    print(f"  Kernel: exp(-0.8*t^2), 1/L^{POWER}")
    print(f"  Action: S = L(1-f) (valley-linear)")
    print(f"  Field:  s/r^2 (spatial-only 3D Coulomb)")
    print()

    # Build lattice
    t0 = time.time()
    lat = Lattice4D(phys_l, h, weight_fn=weight_fn)
    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, {lat.npl:,} nodes/layer")
    print(f"  hw={lat.hw}, max_d={lat.max_d}, {len(lat._off)} offsets/node")
    print(f"  Build time: {time.time()-t0:.1f}s")
    print()

    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked = setup_slits(lat)
    field_f = np.zeros(lat.n)

    # Flat propagation (baseline)
    print("--- Flat propagation (baseline) ---")
    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("NO SIGNAL at detector. Lattice too small or kernel too narrow.")
        return
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    dt_flat = time.time() - t0
    print(f"  det_prob = {pf:.4e}, z_flat = {zf:.6f}")
    print(f"  Time: {dt_flat:.1f}s")
    print()

    # --- DISTANCE LAW ---
    print("=" * 70)
    print("DISTANCE LAW: z_mass in {1,2,3,4,5,6}")
    print("=" * 70)
    print()
    print(f"{'z_mass':>6s} | {'delta':>12s} | {'direction':>9s} | {'time (s)':>8s}")
    print("-" * 45)

    b_data = []
    d_data = []
    all_deltas = []
    for z_mass in [1, 2, 3, 4, 5, 6]:
        t0 = time.time()
        fm, mi = make_field(lat, z_mass, STRENGTH)
        if mi is None:
            dt = time.time() - t0
            print(f"{z_mass:>6d} | {'OUT OF RANGE':>12s} | {'---':>9s} | {dt:>8.1f}")
            all_deltas.append((z_mass, None, None))
            continue
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        dt = time.time() - t0
        if pm < 1e-30:
            print(f"{z_mass:>6d} | {'NO SIGNAL':>12s} | {'---':>9s} | {dt:>8.1f}")
            all_deltas.append((z_mass, None, None))
            continue
        zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"{z_mass:>6d} | {delta:>+12.6f} | {direction:>9s} | {dt:>8.1f}")
        all_deltas.append((z_mass, delta, direction))
        if delta > 0:
            b_data.append(z_mass)
            d_data.append(delta)

    print()
    n_toward = len(b_data)
    print(f"TOWARD points: {n_toward}/{len(all_deltas)}")

    # Distance fit
    dist_alpha, dist_r2 = None, None
    if len(b_data) >= 3:
        dist_alpha, dist_r2 = fit_power(b_data, d_data)
    print()
    if dist_alpha is not None:
        print(f"Distance fit (TOWARD points): alpha = {dist_alpha:.3f}, R^2 = {dist_r2:.4f}")
    else:
        print(f"Distance fit: insufficient TOWARD points ({n_toward} < 3)")

    # --- F~M SCALING at z=3 ---
    print()
    print("=" * 70)
    print("F~M SCALING at z=3")
    print("=" * 70)
    print()
    print(f"{'strength':>12s} | {'delta':>12s} | {'direction':>9s} | {'time (s)':>8s}")
    print("-" * 50)

    m_data = []
    g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        t0 = time.time()
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        dt = time.time() - t0
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            direction = "TOWARD" if delta > 0 else "AWAY"
            print(f"{s:>12.1e} | {delta:>+12.6f} | {direction:>9s} | {dt:>8.1f}")
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)
        else:
            print(f"{s:>12.1e} | {'NO SIGNAL':>12s} | {'---':>9s} | {dt:>8.1f}")

    fm_alpha = None
    if len(m_data) >= 3:
        fm_alpha, fm_r2 = fit_power(m_data, g_data)

    print()
    if fm_alpha is not None:
        print(f"F~M at z=3: alpha = {fm_alpha:.3f}, R^2 = {fm_r2:.4f}")
    else:
        print(f"F~M at z=3: insufficient TOWARD points ({len(m_data)} < 3)")

    # --- SUMMARY ---
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print(f"  Lattice: {lat.n:,} nodes ({lat.nl} layers x {lat.npl:,} nodes/layer)")
    print(f"  h={h}, W={PHYS_W}, L={phys_l}")
    print(f"  TOWARD points: {n_toward}/6")
    if dist_alpha is not None:
        print(f"  Distance alpha: {dist_alpha:.3f} (R^2={dist_r2:.4f})")
    else:
        print(f"  Distance alpha: N/A (need 3+ TOWARD)")
    if fm_alpha is not None:
        print(f"  F~M alpha:      {fm_alpha:.3f} (R^2={fm_r2:.4f})")
    else:
        print(f"  F~M alpha:      N/A")
    print()

    # Verdict
    hyp_pass = n_toward >= 4
    print(f"  HYPOTHESIS (4+ TOWARD): {'CONFIRMED' if hyp_pass else 'FALSIFIED'}")
    if not hyp_pass:
        print(f"    Only {n_toward} TOWARD points. Lattice may still be too small.")
    if dist_alpha is not None:
        close = abs(dist_alpha - 1.0) < 0.5
        print(f"  Distance alpha ~1.0: {'YES' if close else 'NO'} ({dist_alpha:.3f})")
    print()


if __name__ == "__main__":
    main()
