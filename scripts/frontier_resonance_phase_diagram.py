#!/usr/bin/env python3
"""Resonance phase diagram: gravity sign across (k, kernel_alpha) space.

Hypothesis: clear resonance boundaries exist in (k, alpha) space.
Falsification: gravity sign is random/noisy with no clear pattern.

Uses 3D ordered lattice with valley-linear action S = L(1-f),
kernel w(theta) = cos^alpha(theta), attenuation 1/L^2.
"""

from __future__ import annotations
import math
import time

import numpy as np

# Fixed parameters
H = 0.5
PHYS_W = 6
PHYS_L = 12
MAX_D_PHYS = 3
STRENGTH = 5e-5
Z_MASS = 3
N_YBINS = 8

K_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
ALPHA_VALUES = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]


class Lattice3DAlpha:
    """3D lattice with cos^alpha(theta) kernel."""

    def __init__(self, phys_l, phys_w, h, alpha):
        self.h = h
        self.alpha = alpha
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
                # cos^alpha kernel
                cos_theta = math.cos(theta)
                if alpha == 0.0:
                    w = 1.0  # uniform kernel
                else:
                    w = cos_theta ** alpha if cos_theta > 0 else 0.0
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
                if w < 1e-30:
                    continue
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
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt(
        (lat.pos[:, 0] - mx) ** 2
        + (lat.pos[:, 1] - my) ** 2
        + (lat.pos[:, 2] - mz) ** 2
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


def measure_gravity(lat, k, blocked, det, zf_free, field_m, field_f):
    """Measure gravity deflection for given k."""
    am = lat.propagate(field_m, k, blocked)
    pm = sum(abs(am[d]) ** 2 for d in det)
    if pm < 1e-30:
        return 0.0
    zm = sum(abs(am[d]) ** 2 * lat.pos[d, 2] for d in det) / pm
    return zm - zf_free


def main():
    t_start = time.time()
    print("=" * 78)
    print("RESONANCE PHASE DIAGRAM: gravity sign across (k, kernel_alpha) space")
    print(f"  Action: S = L(1-f), kernel: cos^alpha(theta), atten: 1/L^2")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, MAX_D_PHYS={MAX_D_PHYS}")
    print(f"  Mass at z={Z_MASS}, strength={STRENGTH:.0e}")
    print(f"  k values: {K_VALUES}")
    print(f"  alpha values: {ALPHA_VALUES}")
    print("=" * 78)
    print()

    # Results storage: results[alpha][k] = deflection
    results = {}

    for ai, alpha in enumerate(ALPHA_VALUES):
        t_alpha = time.time()
        lat = Lattice3DAlpha(PHYS_L, PHYS_W, H, alpha)
        det = [
            lat.nmap[(lat.nl - 1, iy, iz)]
            for iy in range(-lat.hw, lat.hw + 1)
            for iz in range(-lat.hw, lat.hw + 1)
            if (lat.nl - 1, iy, iz) in lat.nmap
        ]
        _, _, _, blocked, _ = setup_slits(lat)

        field_f = np.zeros(lat.n)
        field_m, _ = make_field(lat, Z_MASS, STRENGTH)

        results[alpha] = {}
        print(f"alpha={alpha:.1f} ({lat.n:,} nodes) ...", end="", flush=True)

        for ki, k in enumerate(K_VALUES):
            # Free propagation centroid for this k
            af = lat.propagate(field_f, k, blocked)
            pf = sum(abs(af[d]) ** 2 for d in det)
            if pf < 1e-30:
                results[alpha][k] = 0.0
                continue
            zf = sum(abs(af[d]) ** 2 * lat.pos[d, 2] for d in det) / pf

            defl = measure_gravity(lat, k, blocked, det, zf, field_m, field_f)
            results[alpha][k] = defl

        elapsed = time.time() - t_alpha
        print(f" {elapsed:.0f}s")

    total = time.time() - t_start
    print(f"\nTotal compute: {total:.0f}s\n")

    # Noise threshold: deflections smaller than this are "zero"
    all_defl = [abs(results[a][k]) for a in ALPHA_VALUES for k in K_VALUES]
    max_defl = max(all_defl) if all_defl else 1.0
    noise = max_defl * 0.01  # 1% of max as noise floor

    # ASCII phase diagram
    print("=" * 78)
    print("PHASE DIAGRAM: gravity sign (+ = TOWARD, - = AWAY, 0 = noise)")
    print("=" * 78)
    hdr = "  k \\ alpha"
    for alpha in ALPHA_VALUES:
        hdr += f"  a={alpha:<4}"
    print(hdr)
    print("-" * len(hdr))

    toward_count = 0
    away_count = 0
    zero_count = 0
    for k in K_VALUES:
        row = f"  k={k:<5}"
        for alpha in ALPHA_VALUES:
            d = results[alpha][k]
            if abs(d) < noise:
                sym = "  0  "
                zero_count += 1
            elif d > 0:
                sym = "  +  "
                toward_count += 1
            else:
                sym = "  -  "
                away_count += 1
            row += f" {sym} "
        print(row)
    print()

    # Magnitude table
    print("=" * 78)
    print("DEFLECTION MAGNITUDES (x1e6)")
    print("=" * 78)
    hdr2 = "  k \\ alpha"
    for alpha in ALPHA_VALUES:
        hdr2 += f"  a={alpha:<6}"
    print(hdr2)
    print("-" * len(hdr2))
    for k in K_VALUES:
        row = f"  k={k:<5}"
        for alpha in ALPHA_VALUES:
            d = results[alpha][k]
            row += f"  {d*1e6:+8.2f}"
        print(row)
    print()

    # Analysis: find boundaries
    print("=" * 78)
    print("ANALYSIS")
    print("=" * 78)
    print(f"  Total cells: {len(K_VALUES) * len(ALPHA_VALUES)}")
    print(f"  TOWARD (+): {toward_count}")
    print(f"  AWAY   (-): {away_count}")
    print(f"  Noise  (0): {zero_count}")
    print(f"  Noise threshold: {noise:.2e}")
    print(f"  Max |deflection|: {max_defl:.2e}")
    print()

    # Per-alpha summary
    print("  Per-alpha summary:")
    for alpha in ALPHA_VALUES:
        signs = []
        for k in K_VALUES:
            d = results[alpha][k]
            if abs(d) < noise:
                signs.append("0")
            elif d > 0:
                signs.append("+")
            else:
                signs.append("-")
        n_toward = signs.count("+")
        n_away = signs.count("-")
        print(f"    alpha={alpha:.1f}: {''.join(signs)}  ({n_toward}+, {n_away}-)")

    # Per-k summary
    print("\n  Per-k summary:")
    for k in K_VALUES:
        signs = []
        for alpha in ALPHA_VALUES:
            d = results[alpha][k]
            if abs(d) < noise:
                signs.append("0")
            elif d > 0:
                signs.append("+")
            else:
                signs.append("-")
        n_toward = signs.count("+")
        print(f"    k={k:<5}: {''.join(signs)}  ({n_toward}+ of {len(ALPHA_VALUES)})")

    # Check for resonance boundaries
    print("\n  Boundary detection:")
    boundary_count = 0
    for ki in range(len(K_VALUES) - 1):
        for alpha in ALPHA_VALUES:
            d1 = results[alpha][K_VALUES[ki]]
            d2 = results[alpha][K_VALUES[ki + 1]]
            if (d1 > noise and d2 < -noise) or (d1 < -noise and d2 > noise):
                boundary_count += 1
                print(
                    f"    Sign flip at alpha={alpha:.1f}: "
                    f"k={K_VALUES[ki]}->{K_VALUES[ki+1]} "
                    f"({d1*1e6:+.2f} -> {d2*1e6:+.2f} x1e-6)"
                )
    for ai in range(len(ALPHA_VALUES) - 1):
        for k in K_VALUES:
            d1 = results[ALPHA_VALUES[ai]][k]
            d2 = results[ALPHA_VALUES[ai + 1]][k]
            if (d1 > noise and d2 < -noise) or (d1 < -noise and d2 > noise):
                boundary_count += 1
                print(
                    f"    Sign flip at k={k:.1f}: "
                    f"alpha={ALPHA_VALUES[ai]}->{ALPHA_VALUES[ai+1]} "
                    f"({d1*1e6:+.2f} -> {d2*1e6:+.2f} x1e-6)"
                )

    print(f"\n  Total sign-flip boundaries: {boundary_count}")

    # Verdict
    print()
    print("=" * 78)
    has_pattern = boundary_count >= 3 and (toward_count > 0 and away_count > 0)
    random_like = boundary_count < 2 or toward_count == 0 or away_count == 0
    if has_pattern:
        print("VERDICT: CLEAR RESONANCE BOUNDARIES FOUND")
        print("  Hypothesis supported: gravity sign oscillates with")
        print("  clear boundaries in (k, alpha) space.")
    elif random_like:
        if away_count == 0 and toward_count > 0:
            print("VERDICT: ALL TOWARD -- no resonance oscillation")
            print("  Gravity is uniformly attractive across parameter space.")
        elif toward_count == 0 and away_count > 0:
            print("VERDICT: ALL AWAY -- no resonance oscillation")
            print("  Gravity is uniformly repulsive across parameter space.")
        else:
            print("VERDICT: NO CLEAR PATTERN")
            print("  Hypothesis falsified: sign appears random/noisy.")
    else:
        print("VERDICT: WEAK PATTERN")
        print("  Some boundaries found but pattern is not robust.")
    print(f"\n  Total runtime: {time.time() - t_start:.0f}s")
    print("=" * 78)


if __name__ == "__main__":
    main()
