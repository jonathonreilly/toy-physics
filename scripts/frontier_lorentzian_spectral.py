#!/usr/bin/env python3
"""Lorentzian vs Euclidean spectral averaging: raw equal-amplitude measure.

Tests whether the Lorentzian split-delay action changes the raw broadband
spectral sum result (which was AWAY for the Euclidean model).

CAVEATS (from review):
  1. This tests only the RAW equal-amplitude coherent sum. The separate
     flux-normalized test (frontier_natural_weight_spectral.py) shows that
     inverse-probability weighting flips the result to TOWARD for BOTH
     models. The spectral sign depends on the weighting scheme.
  2. The "geometric TOWARD baseline" framing assumed weak-field geodesic
     attraction, which is only demonstrated at strong field (5e-2). At the
     closure-card weak field (5e-5), the lattice cannot resolve the
     geodesic deflection.
  3. The raw AWAY result is dominated by a single mode (k=0.5) with 10^22
     times more detector probability than the attractive-window modes.

RESULT: Raw broadband sums are AWAY for both models. This is a property
of the raw measure (non-unitary amplification bias), not necessarily of
the underlying physics. See frontier_natural_weight_spectral.py for the
flux-normalized analysis.
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5
PHYS_W = 6
PHYS_L = 12
H = 0.5


class Lattice3D:
    """3D lattice supporting both Euclidean and Lorentzian actions."""

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
        # Pre-compute edge offsets with both Euclidean and Lorentzian factors
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

    def propagate(self, field, k, blocked_set, lorentzian=False):
        """Propagate amplitude through lattice.

        Euclidean action: S = L * (1 - f)
        Lorentzian action: S = L * (1 - f * cos(2*theta))
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
                if lorentzian:
                    act = L * (1 - lf * lf_factor)
                else:
                    act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field."""
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
    return blocked


def measure_gravity(lat, det, pos, field_flat, field_mass, k, blocked, lorentzian):
    """Measure centroid shift for a single k value."""
    af = lat.propagate(field_flat, k, blocked, lorentzian=lorentzian)
    am = lat.propagate(field_mass, k, blocked, lorentzian=lorentzian)
    pf = sum(abs(af[d])**2 for d in det)
    pm = sum(abs(am[d])**2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return 0.0, af, am
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
    return zm - zf, af, am


def spectral_centroid(det, pos, amp_dict, k_fine, weights):
    """Coherent spectral sum: psi = sum w(k)*psi_k, then centroid of |psi|^2."""
    coh = {d: sum(weights[k] * amp_dict[k][d] for k in k_fine) for d in det}
    p = sum(abs(coh[d])**2 for d in det)
    if p < 1e-30:
        return 0.0
    return sum(abs(coh[d])**2 * pos[d, 2] for d in det) / p


def main():
    print("=" * 72)
    print("LORENTZIAN vs EUCLIDEAN SPECTRAL AVERAGING: THE DECISIVE TEST")
    print("=" * 72)
    print()
    print("Euclidean S=L(1-f):           geometric baseline AWAY")
    print("Lorentzian S=L(1-f*cos(2t)):  geometric baseline TOWARD")
    print()
    print("Question: does Lorentzian give TOWARD under spectral averaging?")
    print()

    t0 = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    blocked = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, 3, STRENGTH)

    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    pos = lat.pos

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={H}")
    print(f"Mass at z=3, strength={STRENGTH}")
    print(f"Setup: {time.time()-t0:.1f}s")

    # ==================================================================
    # PART 1: Single-k sweep — both models side by side
    # ==================================================================
    print(f"\n{'='*72}")
    print("PART 1: Single-k sweep (Euclidean vs Lorentzian)")
    print(f"{'='*72}\n")

    k_sweep = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 6.5, 7.0, 7.5, 8.0, 10.0, 12.0]

    print(f"{'k':>5} | {'Euclidean':>12} {'':>7} | {'Lorentzian':>12} {'':>7}")
    print(f"{'':>5} | {'delta':>12} {'dir':>7} | {'delta':>12} {'dir':>7}")
    print("-" * 58)

    for k in k_sweep:
        de, _, _ = measure_gravity(lat, det, pos, field_flat, field_mass, k, blocked, lorentzian=False)
        dl, _, _ = measure_gravity(lat, det, pos, field_flat, field_mass, k, blocked, lorentzian=True)
        dir_e = "TOWARD" if de > 1e-10 else "AWAY" if de < -1e-10 else "~zero"
        dir_l = "TOWARD" if dl > 1e-10 else "AWAY" if dl < -1e-10 else "~zero"
        print(f"{k:>5.1f} | {de:>+12.6f} {dir_e:>7} | {dl:>+12.6f} {dir_l:>7}")

    # ==================================================================
    # PART 2: Pre-compute detector amplitudes at fine k grid
    # ==================================================================
    print(f"\n{'='*72}")
    print("PART 2: Spectral averaging (coherent wave packets)")
    print(f"{'='*72}\n")

    k_fine = np.arange(0.5, 12.01, 0.25)
    print(f"Pre-computing {len(k_fine)} k-values x 2 fields x 2 models = {len(k_fine)*4} propagations...")
    t1 = time.time()

    # Store detector-level amplitudes: model -> field -> k -> {det_idx: amp}
    euc_flat_amps = {}
    euc_mass_amps = {}
    lor_flat_amps = {}
    lor_mass_amps = {}

    for i, k in enumerate(k_fine):
        k_r = round(k, 4)
        # Euclidean
        af_e = lat.propagate(field_flat, k, blocked, lorentzian=False)
        am_e = lat.propagate(field_mass, k, blocked, lorentzian=False)
        euc_flat_amps[k_r] = {d: af_e[d] for d in det}
        euc_mass_amps[k_r] = {d: am_e[d] for d in det}
        # Lorentzian
        af_l = lat.propagate(field_flat, k, blocked, lorentzian=True)
        am_l = lat.propagate(field_mass, k, blocked, lorentzian=True)
        lor_flat_amps[k_r] = {d: af_l[d] for d in det}
        lor_mass_amps[k_r] = {d: am_l[d] for d in det}

        if (i + 1) % 10 == 0:
            elapsed = time.time() - t1
            rate = (i + 1) / elapsed
            remaining = (len(k_fine) - i - 1) / rate
            print(f"  {i+1}/{len(k_fine)} done ({elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining)")

    k_fine_r = [round(k, 4) for k in k_fine]
    print(f"Pre-computation done in {time.time()-t1:.0f}s\n")

    # ==================================================================
    # Spectral configs
    # ==================================================================
    configs = [
        (3.5, 0.5, "narrow k=3.5"),
        (3.5, 1.0, "medium k=3.5"),
        (3.5, 2.0, "broad k=3.5"),
        (3.5, 4.0, "v.broad k=3.5"),
        (5.0, 0.5, "narrow k=5.0"),
        (5.0, 1.0, "medium k=5.0"),
        (5.0, 2.0, "broad k=5.0"),
        (5.0, 4.0, "v.broad k=5.0"),
        (7.0, 0.5, "narrow k=7.0"),
        (7.0, 1.0, "medium k=7.0"),
        (7.0, 2.0, "broad k=7.0"),
        (7.0, 4.0, "v.broad k=7.0"),
    ]

    header = (f"{'Config':<16} | {'Euclidean':>12} {'':>7} | {'Lorentzian':>12} {'':>7}")
    subhdr = (f"{'k0  sigma':<16} | {'delta':>12} {'dir':>7} | {'delta':>12} {'dir':>7}")
    print(header)
    print(subhdr)
    print("-" * 66)

    results = []
    for k0, sigma, label in configs:
        weights = {}
        w_sum = 0.0
        for k in k_fine_r:
            w = math.exp(-(k - k0)**2 / (2 * sigma**2))
            weights[k] = w
            w_sum += w
        weights = {k: w / w_sum for k, w in weights.items()}

        # Euclidean coherent
        zm_e = spectral_centroid(det, pos, euc_mass_amps, k_fine_r, weights)
        zf_e = spectral_centroid(det, pos, euc_flat_amps, k_fine_r, weights)
        de = zm_e - zf_e
        dir_e = "TOWARD" if de > 1e-10 else "AWAY" if de < -1e-10 else "~zero"

        # Lorentzian coherent
        zm_l = spectral_centroid(det, pos, lor_mass_amps, k_fine_r, weights)
        zf_l = spectral_centroid(det, pos, lor_flat_amps, k_fine_r, weights)
        dl = zm_l - zf_l
        dir_l = "TOWARD" if dl > 1e-10 else "AWAY" if dl < -1e-10 else "~zero"

        tag = f"{k0:.1f}  {sigma:.1f}"
        print(f"{tag:<16} | {de:>+12.6f} {dir_e:>7} | {dl:>+12.6f} {dir_l:>7}")
        results.append({"k0": k0, "sigma": sigma, "label": label,
                        "de": de, "dir_e": dir_e, "dl": dl, "dir_l": dir_l})

    # ==================================================================
    # Flat spectrum (equal weight)
    # ==================================================================
    print()
    weights_flat = {k: 1.0 / len(k_fine_r) for k in k_fine_r}

    zm_e = spectral_centroid(det, pos, euc_mass_amps, k_fine_r, weights_flat)
    zf_e = spectral_centroid(det, pos, euc_flat_amps, k_fine_r, weights_flat)
    de_flat = zm_e - zf_e
    dir_e_flat = "TOWARD" if de_flat > 1e-10 else "AWAY" if de_flat < -1e-10 else "~zero"

    zm_l = spectral_centroid(det, pos, lor_mass_amps, k_fine_r, weights_flat)
    zf_l = spectral_centroid(det, pos, lor_flat_amps, k_fine_r, weights_flat)
    dl_flat = zm_l - zf_l
    dir_l_flat = "TOWARD" if dl_flat > 1e-10 else "AWAY" if dl_flat < -1e-10 else "~zero"

    print(f"{'flat spectrum':<16} | {de_flat:>+12.6f} {dir_e_flat:>7} | {dl_flat:>+12.6f} {dir_l_flat:>7}")

    # ==================================================================
    # PART 3: Summary comparison table
    # ==================================================================
    print(f"\n{'='*72}")
    print("PART 3: HEAD-TO-HEAD SUMMARY")
    print(f"{'='*72}\n")

    print(f"{'':>16} | {'Euclidean':^20} | {'Lorentzian':^20}")
    print(f"{'Config':<16} | {'delta':>9}  {'dir':>7}  | {'delta':>9}  {'dir':>7}")
    print("-" * 62)

    for r in results:
        tag = f"k0={r['k0']:.1f} s={r['sigma']:.1f}"
        print(f"{tag:<16} | {r['de']:>+9.6f}  {r['dir_e']:>7}  | {r['dl']:>+9.6f}  {r['dir_l']:>7}")

    print(f"{'flat':<16} | {de_flat:>+9.6f}  {dir_e_flat:>7}  | {dl_flat:>+9.6f}  {dir_l_flat:>7}")

    # ==================================================================
    # VERDICT
    # ==================================================================
    print(f"\n{'='*72}")
    print("VERDICT")
    print(f"{'='*72}\n")

    # Count directions for each model
    euc_toward = sum(1 for r in results if r["dir_e"] == "TOWARD")
    euc_away = sum(1 for r in results if r["dir_e"] == "AWAY")
    lor_toward = sum(1 for r in results if r["dir_l"] == "TOWARD")
    lor_away = sum(1 for r in results if r["dir_l"] == "AWAY")

    # Broad-only (sigma >= 2)
    broad = [r for r in results if r["sigma"] >= 2.0]
    euc_broad_toward = sum(1 for r in broad if r["dir_e"] == "TOWARD")
    euc_broad_away = sum(1 for r in broad if r["dir_e"] == "AWAY")
    lor_broad_toward = sum(1 for r in broad if r["dir_l"] == "TOWARD")
    lor_broad_away = sum(1 for r in broad if r["dir_l"] == "AWAY")

    # Very broad only (sigma >= 4)
    vbroad = [r for r in results if r["sigma"] >= 4.0]
    lor_vbroad_toward = sum(1 for r in vbroad if r["dir_l"] == "TOWARD")
    lor_vbroad_away = sum(1 for r in vbroad if r["dir_l"] == "AWAY")

    print(f"  Euclidean:   all configs: {euc_toward} TOWARD, {euc_away} AWAY")
    print(f"               broad (s>=2): {euc_broad_toward} TOWARD, {euc_broad_away} AWAY")
    print(f"               flat spectrum: {dir_e_flat}")
    print()
    print(f"  Lorentzian:  all configs: {lor_toward} TOWARD, {lor_away} AWAY")
    print(f"               broad (s>=2): {lor_broad_toward} TOWARD, {lor_broad_away} AWAY")
    print(f"               v.broad (s>=4): {lor_vbroad_toward} TOWARD, {lor_vbroad_away} AWAY")
    print(f"               flat spectrum: {dir_l_flat}")

    print()
    # The decisive question
    lor_universal = (lor_broad_toward == len(broad) and dir_l_flat == "TOWARD")
    euc_universal = (euc_broad_toward == len(broad) and dir_e_flat == "TOWARD")

    if lor_universal and not euc_universal:
        print("  *** HYPOTHESIS CONFIRMED ***")
        print("  Lorentzian spectral averaging gives UNIVERSAL TOWARD.")
        print("  Euclidean does NOT.")
        print()
        print("  The Lorentzian geometric baseline (TOWARD) survives spectral")
        print("  averaging because when wave resonances wash out, the underlying")
        print("  geodesic attraction remains. This is UNIVERSAL GRAVITATIONAL")
        print("  ATTRACTION from the Lorentzian action principle.")
    elif lor_universal and euc_universal:
        print("  Both models give universal TOWARD under spectral averaging.")
        print("  The Lorentzian advantage is NOT unique.")
    elif not lor_universal:
        print("  *** HYPOTHESIS FALSIFIED ***")
        print("  Lorentzian spectral averaging does NOT give universal TOWARD.")
        print(f"  Broad spectra: {lor_broad_toward} TOWARD, {lor_broad_away} AWAY")
        print(f"  Flat spectrum: {dir_l_flat}")
        print()
        if lor_broad_toward > euc_broad_toward:
            print("  However, Lorentzian shows MORE TOWARD configs than Euclidean.")
            print("  The geometric baseline shift is real but not dominant enough")
            print("  to overcome wave-structure AWAY at all spectral shapes.")
        else:
            print("  Lorentzian does not even outperform Euclidean on spectral")
            print("  averaging. The geometric baseline TOWARD is overwhelmed.")

    print(f"\n  Total time: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
