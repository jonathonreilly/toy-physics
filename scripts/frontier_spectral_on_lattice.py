#!/usr/bin/env python3
"""Spectral averaging on the RETAINED ordered-lattice harness.

The previous spectral test (frontier_spectral_gravity.py) ran on the
2D toy_event_physics infrastructure and found that averaging over k
does NOT produce universal attraction. Does this negative TRANSPORT
to the retained 3D ordered lattice (the flagship lane)?

This is the decisive test: if spectral averaging also fails on the
retained 2+1D/3+1D harness, the resonance-window nature of gravity
is confirmed as a property of the flagship model, not just the 2D toy.

APPROACH:
  For each center frequency k0 and spectral width sigma_k:
  1. Build a Gaussian spectrum of k values: A(k) = exp(-(k-k0)^2/(2*sigma^2))
  2. For each k in the spectrum: propagate on the 3D lattice, collect psi_k(z) at detector
  3. Coherent sum: psi_total(z) = sum_k A(k) * psi_k(z)
  4. Measure centroid of |psi_total|^2

Test both 2+1D (Lattice3D) and 3+1D (Lattice4D if feasible, otherwise just 2+1D).

HYPOTHESIS: "Spectral averaging on the retained lattice also fails to produce
  universal attraction."
FALSIFICATION: "If broad spectra always give TOWARD on the retained lattice,
  the 2D negative was infrastructure-specific."
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """Copied from lattice_3d_valley_linear_card.py with variable k."""

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
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field (2D Coulomb for 2 spatial dims)."""
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


def get_detector_amps(lat, amps):
    """Return dict {iz_index: complex_amplitude} at detector layer."""
    dl = lat.nl - 1
    ls = lat._ls[dl]
    det_amps = {}
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((dl, iy, iz))
            if idx is not None:
                # Sum over iy for z-centroid (gravity is in z direction)
                det_amps[iz] = det_amps.get(iz, 0j) + amps[idx]
    return det_amps


def centroid_from_amps(det_amps, h):
    """Compute z-centroid from complex amplitude dict."""
    prob = {z: abs(a)**2 for z, a in det_amps.items()}
    total = sum(prob.values())
    if total < 1e-30:
        return 0.0, total
    c = sum(z * h * p for z, p in prob.items()) / total
    return c, total


def main():
    print("=" * 70)
    print("SPECTRAL AVERAGING ON RETAINED 2+1D ORDERED LATTICE")
    print("=" * 70)
    print()
    print("Does spectral averaging over k produce universal attraction")
    print("on the retained 3D lattice (valley-linear, 1/L^2, h=0.5)?")
    print()

    h = 0.5
    phys_w = 6
    phys_l = 12
    z_mass = 3

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    blocked = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, z_mass, STRENGTH)

    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    pos = lat.pos

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={h}")
    print(f"Mass at z={z_mass}, strength={STRENGTH}")
    print(f"Setup: {time.time()-t0:.1f}s")
    print()

    # ================================================================
    # Part 1: Single-k sweep on the retained lattice
    # ================================================================
    print("=" * 70)
    print("PART 1: Single-k gravity on retained 2+1D lattice")
    print("=" * 70)
    print()

    k_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]

    print(f"{'k':>6} | {'delta':>12} | {'direction':>9} | {'det_prob':>10}")
    print("-" * 50)

    single_k_results = {}
    for k in k_values:
        # Flat baseline at this k
        af = lat.propagate(field_flat, k, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0

        # With mass
        am = lat.propagate(field_mass, k, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm if pm > 1e-30 else 0

        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY" if delta < -1e-10 else "~zero"
        single_k_results[k] = {"delta": delta, "dir": direction, "prob": pm}
        print(f"{k:>6.1f} | {delta:>+12.6f} | {direction:>9} | {pm:>10.3e}")

    n_toward = sum(1 for r in single_k_results.values() if r["dir"] == "TOWARD")
    n_away = sum(1 for r in single_k_results.values() if r["dir"] == "AWAY")
    print(f"\nTOWARD: {n_toward}/{len(k_values)}, AWAY: {n_away}/{len(k_values)}")

    # ================================================================
    # Part 2: Spectral averaging
    # ================================================================
    print(f"\n{'='*70}")
    print("PART 2: Spectral averaging (Gaussian wave packets)")
    print(f"{'='*70}")
    print()

    # For spectral averaging, we need detector-level COMPLEX AMPLITUDES
    # at each k, then sum coherently.
    k_fine = np.arange(0.5, 12.01, 0.25)

    # Pre-compute flat centroids and detector amplitudes for all k
    print(f"Pre-computing {len(k_fine)} propagations...")
    t1 = time.time()

    flat_centroids = {}
    mass_det_amps = {}  # k -> {det_idx: complex_amp}
    flat_det_amps = {}

    for k in k_fine:
        af = lat.propagate(field_flat, k, blocked)
        am = lat.propagate(field_mass, k, blocked)

        flat_det_amps[k] = {d: af[d] for d in det}
        mass_det_amps[k] = {d: am[d] for d in det}

        pf = sum(abs(af[d])**2 for d in det)
        flat_centroids[k] = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0

    print(f"Done in {time.time()-t1:.0f}s")
    print()

    # Test spectral configs
    configs = [
        # (k0, sigma_k, label)
        (2.5, 0.5, "narrow around k=2.5"),
        (2.5, 1.0, "medium around k=2.5"),
        (2.5, 2.0, "broad around k=2.5"),
        (2.5, 4.0, "very broad around k=2.5"),
        (5.0, 0.5, "narrow around k=5.0"),
        (5.0, 1.0, "medium around k=5.0"),
        (5.0, 2.0, "broad around k=5.0"),
        (5.0, 4.0, "very broad around k=5.0"),
        (7.0, 1.0, "medium around k=7.0"),
        (7.0, 2.0, "broad around k=7.0"),
        (3.5, 1.0, "medium around k=3.5"),
        (3.5, 3.0, "very broad around k=3.5"),
    ]

    print(f"{'k0':>4} {'sigma':>5} | {'delta_coh':>12} {'dir_coh':>9} | {'delta_inc':>12} {'dir_inc':>9} | {'label'}")
    print("-" * 90)

    spectral_results = []
    for k0, sigma, label in configs:
        # Gaussian weights
        weights = {k: math.exp(-(k - k0)**2 / (2 * sigma**2)) for k in k_fine}
        w_sum = sum(weights.values())
        weights = {k: w / w_sum for k, w in weights.items()}

        # Coherent sum: psi_total = sum w_k * psi_k
        coh_mass = {d: sum(weights[k] * mass_det_amps[k][d] for k in k_fine) for d in det}
        coh_flat = {d: sum(weights[k] * flat_det_amps[k][d] for k in k_fine) for d in det}

        # Coherent centroid
        pm_coh = sum(abs(coh_mass[d])**2 for d in det)
        pf_coh = sum(abs(coh_flat[d])**2 for d in det)
        zm_coh = sum(abs(coh_mass[d])**2 * pos[d, 2] for d in det) / pm_coh if pm_coh > 1e-30 else 0
        zf_coh = sum(abs(coh_flat[d])**2 * pos[d, 2] for d in det) / pf_coh if pf_coh > 1e-30 else 0
        delta_coh = zm_coh - zf_coh
        dir_coh = "TOWARD" if delta_coh > 1e-10 else "AWAY" if delta_coh < -1e-10 else "~zero"

        # Incoherent sum: P_total = sum w_k^2 * |psi_k|^2
        inc_mass = {d: sum(weights[k]**2 * abs(mass_det_amps[k][d])**2 for k in k_fine) for d in det}
        inc_flat = {d: sum(weights[k]**2 * abs(flat_det_amps[k][d])**2 for k in k_fine) for d in det}

        pm_inc = sum(inc_mass[d] for d in det)
        pf_inc = sum(inc_flat[d] for d in det)
        zm_inc = sum(inc_mass[d] * pos[d, 2] for d in det) / pm_inc if pm_inc > 1e-30 else 0
        zf_inc = sum(inc_flat[d] * pos[d, 2] for d in det) / pf_inc if pf_inc > 1e-30 else 0
        delta_inc = zm_inc - zf_inc
        dir_inc = "TOWARD" if delta_inc > 1e-10 else "AWAY" if delta_inc < -1e-10 else "~zero"

        print(f"{k0:>4.1f} {sigma:>5.1f} | {delta_coh:>+12.6f} {dir_coh:>9} | "
              f"{delta_inc:>+12.6f} {dir_inc:>9} | {label}")

        spectral_results.append({
            "k0": k0, "sigma": sigma,
            "delta_coh": delta_coh, "dir_coh": dir_coh,
            "delta_inc": delta_inc, "dir_inc": dir_inc,
        })

    # ================================================================
    # Part 3: Flat spectrum (equal weight on all k)
    # ================================================================
    print(f"\n{'='*70}")
    print("PART 3: Flat spectrum (equal weight on all k)")
    print(f"{'='*70}")

    weights_flat = {k: 1.0 / len(k_fine) for k in k_fine}
    coh_mass_f = {d: sum(weights_flat[k] * mass_det_amps[k][d] for k in k_fine) for d in det}
    coh_flat_f = {d: sum(weights_flat[k] * flat_det_amps[k][d] for k in k_fine) for d in det}
    pm_f = sum(abs(coh_mass_f[d])**2 for d in det)
    pf_f = sum(abs(coh_flat_f[d])**2 for d in det)
    zm_f = sum(abs(coh_mass_f[d])**2 * pos[d, 2] for d in det) / pm_f if pm_f > 1e-30 else 0
    zf_f = sum(abs(coh_flat_f[d])**2 * pos[d, 2] for d in det) / pf_f if pf_f > 1e-30 else 0
    delta_flat = zm_f - zf_f
    dir_flat = "TOWARD" if delta_flat > 1e-10 else "AWAY" if delta_flat < -1e-10 else "~zero"
    print(f"\n  Flat spectrum (k=0.5 to 12.0): delta = {delta_flat:+.6f} ({dir_flat})")

    # ================================================================
    # VERDICT
    # ================================================================
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    n_coh_toward = sum(1 for r in spectral_results if r["dir_coh"] == "TOWARD")
    n_coh_away = sum(1 for r in spectral_results if r["dir_coh"] == "AWAY")
    broad_results = [r for r in spectral_results if r["sigma"] >= 2.0]
    n_broad_toward = sum(1 for r in broad_results if r["dir_coh"] == "TOWARD")
    n_broad_away = sum(1 for r in broad_results if r["dir_coh"] == "AWAY")

    print(f"\n  All configs: {n_coh_toward} TOWARD, {n_coh_away} AWAY (coherent)")
    print(f"  Broad (sigma>=2): {n_broad_toward} TOWARD, {n_broad_away} AWAY")
    print(f"  Flat spectrum: {dir_flat}")

    if n_broad_toward > 0 and n_broad_away > 0:
        print(f"\n  The 2D spectral-averaging negative TRANSPORTS to the retained lattice.")
        print(f"  Broad spectra give MIXED results — resonance structure survives.")
        print(f"  Universal attraction from spectral averaging is NOT achieved.")
    elif n_broad_toward == len(broad_results):
        print(f"\n  The 2D negative does NOT transport — broad spectra all give TOWARD")
        print(f"  on the retained lattice. The 2D failure was infrastructure-specific.")
    elif n_broad_away == len(broad_results):
        print(f"\n  Even worse: broad spectra all give AWAY on the retained lattice.")

    # Compare coherent vs incoherent
    same_sign = sum(1 for r in spectral_results
                    if r["dir_coh"] == r["dir_inc"] and r["dir_coh"] != "~zero")
    diff_sign = sum(1 for r in spectral_results
                    if r["dir_coh"] != r["dir_inc"]
                    and r["dir_coh"] != "~zero" and r["dir_inc"] != "~zero")
    print(f"\n  Coherent vs incoherent: same sign {same_sign}x, opposite sign {diff_sign}x")
    if diff_sign > same_sign:
        print(f"  Quantum interference between k modes dominates the result.")
    elif same_sign > diff_sign:
        print(f"  Classical (incoherent) averaging mostly agrees with coherent.")

    print(f"\n  Total time: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
