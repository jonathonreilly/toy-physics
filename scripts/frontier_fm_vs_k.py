#!/usr/bin/env python3
"""Frontier card: F proportional to M linearity across k values.

Tests whether the F~M = 1.00 power-law (measured at k=5) holds at other
wavenumbers. If alpha=1.00 at all k, linearity is structural to the
resonance mechanism. If it varies, "Newton" was k-specific.

Setup: 3D ordered lattice, h=0.5, W=6, L=12.
Attractive window: k in {1,2,3,4,5,6}
Away window:       k in {7,10}

HYPOTHESIS: F~M = 1.00 at all k values, both TOWARD and AWAY.
FALSIFICATION: alpha deviates by >10% from 1.0 at any k.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc

# --- Constants ---
BETA = 0.8
LAM = 10.0
PHYS_W = 6
PHYS_L = 12
H = 0.5
MAX_D_PHYS = 3
STRENGTHS = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
K_ATTRACT = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
K_AWAY = [7.0, 10.0]
Z_MASS = 3


class Lattice3D:
    """3D dense lattice with valley-linear action S=L(1-f), 1/L^2 kernel."""

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
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n
        hw = self.hw
        nl = self.nl
        nw = self._nw
        hm = self._hm
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
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field(lat, z_mass_phys, strength):
    """Spatial-only 1/r field from a mass at z=z_mass_phys."""
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt(
        (lat.pos[:, 0] - mx)**2 +
        (lat.pos[:, 1] - my)**2 +
        (lat.pos[:, 2] - mz)**2
    ) + 0.1
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
    return bi, sa, sb, blocked, bl


def fit_power(x_data, y_data):
    """Fit log(y) = alpha * log(x) + const. Return (alpha, R^2)."""
    if len(x_data) < 3:
        return None, None
    lx = np.log(np.array(x_data, dtype=float))
    ly = np.log(np.array(y_data, dtype=float))
    mx = lx.mean()
    my = ly.mean()
    sxx = np.sum((lx - mx)**2)
    sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx)))**2)
    ss_tot = np.sum((ly - my)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def measure_alpha(lat, det, pos, blocked, k, zf_cache):
    """Measure F~M power-law alpha at a given k.

    Returns (alpha, r2, direction, deltas).
    direction is 'TOWARD' if centroid shifts toward mass, 'AWAY' otherwise.
    """
    # Free propagation centroid at this k (cache it)
    if k not in zf_cache:
        field_f = np.zeros(lat.n)
        af = lat.propagate(field_f, k, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        if pf > 1e-30:
            zf_cache[k] = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
        else:
            zf_cache[k] = 0.0
    zf = zf_cache[k]

    s_data = []
    d_data = []
    raw_deltas = []
    for s in STRENGTHS:
        fm, _ = make_field(lat, Z_MASS, s)
        am = lat.propagate(fm, k, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            raw_deltas.append((s, delta))
            if abs(delta) > 1e-15:
                s_data.append(s)
                d_data.append(abs(delta))

    # Determine direction from majority sign
    toward_count = sum(1 for _, d in raw_deltas if d > 0)
    away_count = sum(1 for _, d in raw_deltas if d < 0)
    direction = "TOWARD" if toward_count >= away_count else "AWAY"

    alpha, r2 = fit_power(s_data, d_data)
    return alpha, r2, direction, raw_deltas


def main():
    t_total = time.time()

    print("=" * 70)
    print("FRONTIER CARD: F~M LINEARITY vs WAVENUMBER k")
    print(f"  Action: S = L(1-f),  Kernel: 1/L^2,  h^2 measure")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}")
    print(f"  Mass at z={Z_MASS}, strengths: {STRENGTHS[0]:.0e} .. {STRENGTHS[-1]:.0e}")
    print(f"  Attractive window: k = {K_ATTRACT}")
    print(f"  Away window:       k = {K_AWAY}")
    print(f"  HYPOTHESIS: alpha = 1.00 at all k")
    print(f"  FALSIFICATION: |alpha - 1.0| > 0.10 at any k")
    print("=" * 70)
    print()

    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    pos = lat.pos
    bi, sa, sb, blocked, bl = setup_slits(lat)

    print(f"  Lattice: {lat.n:,} nodes, {lat.nl} layers, {len(det)} detector nodes")
    print()

    zf_cache = {}
    results = {}

    all_k = K_ATTRACT + K_AWAY
    for k in all_k:
        t0 = time.time()
        alpha, r2, direction, deltas = measure_alpha(
            lat, det, pos, blocked, k, zf_cache
        )
        elapsed = time.time() - t0

        window = "ATTRACT" if k in K_ATTRACT else "AWAY"
        alpha_str = f"{alpha:.3f}" if alpha is not None else "N/A"
        r2_str = f"{r2:.4f}" if r2 is not None else "N/A"

        passed = alpha is not None and abs(alpha - 1.0) < 0.10
        tag = "PASS" if passed else "FAIL"

        results[k] = {
            'alpha': alpha, 'r2': r2, 'direction': direction,
            'window': window, 'passed': passed
        }

        print(f"  k={k:5.1f} [{window:7s}]  alpha={alpha_str:>7s}  "
              f"R^2={r2_str:>6s}  {direction:6s}  [{tag}]  ({elapsed:.0f}s)")

        # Print raw deltas at lower verbosity
        for s, d in deltas:
            print(f"         strength={s:.0e}  delta={d:+.8f}")
        print()

    # --- Summary ---
    print("=" * 70)
    print("SUMMARY")
    print("-" * 70)
    print(f"  {'k':>5s}  {'Window':>7s}  {'alpha':>7s}  {'R^2':>6s}  {'Dir':>6s}  {'Result':>6s}")
    print("-" * 70)
    all_pass = True
    for k in all_k:
        r = results[k]
        a_str = f"{r['alpha']:.3f}" if r['alpha'] is not None else "N/A"
        r2_str = f"{r['r2']:.4f}" if r['r2'] is not None else "N/A"
        tag = "PASS" if r['passed'] else "FAIL"
        if not r['passed']:
            all_pass = False
        print(f"  {k:5.1f}  {r['window']:>7s}  {a_str:>7s}  {r2_str:>6s}  "
              f"{r['direction']:>6s}  {tag:>6s}")

    print("-" * 70)
    n_pass = sum(1 for r in results.values() if r['passed'])
    n_total = len(results)

    if all_pass:
        verdict = "CONFIRMED"
        detail = "F~M = 1.00 at ALL k values. Linearity is structural."
    else:
        failed_ks = [k for k in all_k if not results[k]['passed']]
        verdict = "FALSIFIED"
        detail = f"alpha deviates >10% from 1.0 at k={failed_ks}"

    print(f"\n  {n_pass}/{n_total} k-values pass |alpha-1| < 0.10")
    print(f"  VERDICT: {verdict}")
    print(f"  {detail}")
    print(f"  Total time: {time.time() - t_total:.0f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
