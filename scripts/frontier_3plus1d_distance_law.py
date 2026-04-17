#!/usr/bin/env python3
"""3+1D and 2+1D distance-law comparison.

GAP: We have F proportional to M (alpha=1.00) in 3+1D but zero data on how
deflection varies with distance. The 2+1D card gives b^(-0.93). What does
3+1D give?

SETUP:
  - 3+1D: Lattice4D from frontier_3plus1d_closure_card.py, h=0.5, W=3, L=10
  - 2+1D: Lattice3D, h=0.5, W=6, L=12
  - Both use spatial-only fields and valley-linear action
  - cos^2(theta) kernel (confirmed best isotropy)

EXPERIMENT:
  For z_mass in {1, 2, 3} (and more if feasible):
    1. Build spatial-only field centered at mass position
    2. Propagate with valley-linear action
    3. Measure z-centroid shift (delta)
    4. Report delta vs z_mass

  Fit: delta = A / z_mass^alpha. Report alpha and R^2.

HYPOTHESIS: 3+1D deflection falls off with distance, giving a measurable
  distance exponent.

FALSIFICATION: If only 1-2 of 3 z_mass values give TOWARD, insufficient
  data for a fit.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

# ── Shared constants ──────────────────────────────────────────────────
K = 5.0
STRENGTH = 5e-5

# ── 3+1D constants ───────────────────────────────────────────────────
PHYS_W_4D = 3
MAX_D_PHYS_4D = 2
POWER_4D = 3       # kernel 1/L^3 for 3 spatial dimensions

# ── 2+1D constants ───────────────────────────────────────────────────
PHYS_W_2D = 6
MAX_D_PHYS_2D = 3
POWER_2D = 2       # kernel 1/L^2 for 2 spatial dimensions


# ══════════════════════════════════════════════════════════════════════
#  Lattice4D (3 spatial + 1 causal)
# ══════════════════════════════════════════════════════════════════════
class Lattice4D:
    """4D ordered lattice with selectable kernel."""

    def __init__(self, phys_l, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.cos(t) ** 2

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
                    L = math.sqrt(h * h + dyp * dyp + dzp * dzp + dwp * dwp)
                    r_trans = math.sqrt(dyp ** 2 + dzp ** 2 + dwp ** 2)
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
                si = siy.ravel() * nw * nw + siz.ravel() * nw + siw.ravel()
                di = ((siy.ravel() + dy) * nw * nw +
                      (siz.ravel() + dz) * nw +
                      (siw.ravel() + dw))
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_4D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ══════════════════════════════════════════════════════════════════════
#  Lattice3D (2 spatial + 1 causal)
# ══════════════════════════════════════════════════════════════════════
class Lattice3D:
    """3D ordered lattice with selectable angular kernel."""

    def __init__(self, phys_l, phys_w, h, weight_fn=None):
        if weight_fn is None:
            weight_fn = lambda t: math.cos(t) ** 2

        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS_2D / h))
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
                theta = math.atan2(math.sqrt(dyp ** 2 + dzp ** 2), h)
                w = weight_fn(theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
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
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_2D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ══════════════════════════════════════════════════════════════════════
#  Field constructors (spatial-only)
# ══════════════════════════════════════════════════════════════════════
def make_field_4d(lat, z_mass_phys, strength):
    """Static 3D Coulomb field: strength / r_spatial^2.

    Spatial-only: depends on (y, z, w) separation from mass, NOT on x.
    Mass at (y=0, z=z_mass, w=0) on every layer.
    """
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


def make_field_3d(lat, z_mass_phys, strength):
    """Static 2D Coulomb field: strength / r_spatial.

    Spatial-only: depends on (y, z) separation from mass, NOT on x.
    Mass at (y=0, z=z_mass) on every layer.
    """
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r_spatial = np.sqrt(
        (lat.pos[:, 1] - my) ** 2 +
        (lat.pos[:, 2] - mz) ** 2
    ) + 0.1
    return strength / r_spatial, mi


# ══════════════════════════════════════════════════════════════════════
#  Slit setup
# ══════════════════════════════════════════════════════════════════════
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
    return blocked


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
    return blocked


# ══════════════════════════════════════════════════════════════════════
#  Power-law fit
# ══════════════════════════════════════════════════════════════════════
def fit_power(b_data, d_data):
    if len(b_data) < 2:
        return None, None
    lx = np.log(np.array(b_data, dtype=float))
    ly = np.log(np.array(d_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx) ** 2); sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx))) ** 2)
    ss_tot = np.sum((ly - my) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


# ══════════════════════════════════════════════════════════════════════
#  Distance sweep
# ══════════════════════════════════════════════════════════════════════
def run_distance_sweep_4d(h, phys_l, z_masses):
    """Run 3+1D distance sweep and return results list."""
    print(f"\n{'='*65}")
    print("  3+1D DISTANCE LAW (spatial-only 1/r^2 field)")
    print(f"  h={h}, W={PHYS_W_4D}, L={phys_l}, kernel=cos^2(theta)")
    print(f"{'='*65}")

    t0 = time.time()
    lat = Lattice4D(phys_l, h)
    det = [lat.nmap[(lat.nl - 1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           for iw in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    blocked = setup_slits_4d(lat)
    print(f"  {lat.n:,} nodes, {lat.nl} layers, {lat.npl} per layer")
    print(f"  Lattice built in {time.time()-t0:.1f}s")

    # Flat baseline
    t0 = time.time()
    field_f = np.zeros(lat.n)
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector.")
        return []
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf
    print(f"  Flat baseline: z_flat={zf:.6f}, prob={pf:.4e} ({time.time()-t0:.1f}s)")

    results = []
    for z_mass in z_masses:
        t0 = time.time()
        fm, mi = make_field_4d(lat, z_mass, STRENGTH)
        if mi is None:
            print(f"  z_mass={z_mass}: OUT OF BOUNDS")
            continue
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm < 1e-30:
            print(f"  z_mass={z_mass}: NO SIGNAL")
            continue
        zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY"
        results.append((z_mass, delta, direction))
        print(f"  z_mass={z_mass}: delta={delta:+.8f} ({direction})  [{time.time()-t0:.1f}s]")

    return results


def run_distance_sweep_3d(h, phys_l, phys_w, z_masses):
    """Run 2+1D distance sweep and return results list."""
    print(f"\n{'='*65}")
    print("  2+1D DISTANCE LAW (spatial-only 1/r field)")
    print(f"  h={h}, W={phys_w}, L={phys_l}, kernel=cos^2(theta)")
    print(f"{'='*65}")

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    pos = lat.pos
    blocked = setup_slits_3d(lat)
    print(f"  {lat.n:,} nodes, {lat.nl} layers, {lat.npl} per layer")
    print(f"  Lattice built in {time.time()-t0:.1f}s")

    # Flat baseline
    t0 = time.time()
    field_f = np.zeros(lat.n)
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL at detector.")
        return []
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf
    print(f"  Flat baseline: z_flat={zf:.6f}, prob={pf:.4e} ({time.time()-t0:.1f}s)")

    results = []
    for z_mass in z_masses:
        t0 = time.time()
        fm, mi = make_field_3d(lat, z_mass, STRENGTH)
        if mi is None:
            print(f"  z_mass={z_mass}: OUT OF BOUNDS")
            continue
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm < 1e-30:
            print(f"  z_mass={z_mass}: NO SIGNAL")
            continue
        zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY"
        results.append((z_mass, delta, direction))
        print(f"  z_mass={z_mass}: delta={delta:+.8f} ({direction})  [{time.time()-t0:.1f}s]")

    return results


# ══════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("DISTANCE LAW: 3+1D vs 2+1D COMPARISON")
    print("=" * 65)
    print()
    print("GAP: F proportional to M confirmed in 3+1D, but no distance data.")
    print("     The 2+1D card shows b^(-0.93). What does 3+1D give?")
    print()
    print("HYPOTHESIS: 3+1D deflection falls off with distance,")
    print("  giving a measurable distance exponent.")
    print()
    print("FALSIFICATION: If <2 of 3 z_mass give TOWARD, no fit possible.")
    print()

    z_masses_4d = [1, 2, 3]
    z_masses_2d = [1, 2, 3, 4, 5]

    # ── 3+1D sweep ────────────────────────────────────────────────────
    results_4d = run_distance_sweep_4d(h=0.5, phys_l=10, z_masses=z_masses_4d)

    # ── 2+1D sweep ────────────────────────────────────────────────────
    results_2d = run_distance_sweep_3d(h=0.5, phys_l=12, phys_w=PHYS_W_2D,
                                        z_masses=z_masses_2d)

    # ── Summary table ─────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("SUMMARY TABLE")
    print(f"{'='*65}")
    print()
    print(f"{'Dimension':<12s} | {'z_mass':>6s} | {'delta':>14s} | {'direction':>10s}")
    print("-" * 50)

    for z, d, dr in results_4d:
        print(f"{'3+1D':<12s} | {z:>6d} | {d:>+14.8f} | {dr:>10s}")
    for z, d, dr in results_2d:
        print(f"{'2+1D':<12s} | {z:>6d} | {d:>+14.8f} | {dr:>10s}")

    # ── Power-law fits ────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("POWER-LAW FITS: delta = A / z_mass^alpha")
    print(f"{'='*65}")

    # 3+1D fit (TOWARD only)
    b4 = [z for z, d, dr in results_4d if d > 0]
    d4 = [d for z, d, dr in results_4d if d > 0]
    if len(b4) >= 2:
        alpha4, r2_4 = fit_power(b4, d4)
        if alpha4 is not None:
            # fit_power gives slope of log(delta) vs log(z), which is positive
            # for delta ~ z^alpha. We want delta ~ 1/z^alpha, so negate.
            print(f"  3+1D: alpha = {-alpha4:.3f}, R^2 = {r2_4:.4f}")
            print(f"         (fit on {len(b4)} TOWARD points: z = {b4})")
        else:
            print("  3+1D: fit failed (degenerate data)")
    else:
        print(f"  3+1D: insufficient TOWARD data ({len(b4)}/{len(results_4d)})")

    # 2+1D fit (TOWARD only)
    b2 = [z for z, d, dr in results_2d if d > 0]
    d2 = [d for z, d, dr in results_2d if d > 0]
    if len(b2) >= 2:
        alpha2, r2_2 = fit_power(b2, d2)
        if alpha2 is not None:
            print(f"  2+1D: alpha = {-alpha2:.3f}, R^2 = {r2_2:.4f}")
            print(f"         (fit on {len(b2)} TOWARD points: z = {b2})")
        else:
            print("  2+1D: fit failed (degenerate data)")
    else:
        print(f"  2+1D: insufficient TOWARD data ({len(b2)}/{len(results_2d)})")

    # ── Interpretation ────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("INTERPRETATION")
    print(f"{'='*65}")
    print()

    n_toward_4d = sum(1 for _, d, _ in results_4d if d > 0)
    n_toward_2d = sum(1 for _, d, _ in results_2d if d > 0)

    if n_toward_4d >= 2 and len(b4) >= 2 and alpha4 is not None:
        print(f"  3+1D TOWARD: {n_toward_4d}/{len(results_4d)}")
        print(f"  3+1D distance exponent: {-alpha4:.3f}")
        if abs(-alpha4 - 1.0) < 0.5:
            print("  --> Consistent with 1/b (3D Coulomb expectation)")
        elif -alpha4 > 1.5:
            print("  --> Steeper than 1/b -- possible lattice artifact")
        else:
            print(f"  --> Deviation from 1/b needs investigation")
    else:
        print(f"  3+1D: HYPOTHESIS FALSIFIED -- only {n_toward_4d} TOWARD")

    if n_toward_2d >= 2 and len(b2) >= 2 and alpha2 is not None:
        print(f"  2+1D TOWARD: {n_toward_2d}/{len(results_2d)}")
        print(f"  2+1D distance exponent: {-alpha2:.3f}")
        print(f"  (compare: previous card reported ~0.93)")
    else:
        print(f"  2+1D: only {n_toward_2d} TOWARD")

    print()


if __name__ == "__main__":
    main()
