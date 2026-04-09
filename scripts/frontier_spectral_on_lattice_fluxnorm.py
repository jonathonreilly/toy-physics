#!/usr/bin/env python3
"""Spectral averaging on the retained ordered-lattice harness with per-k flux normalization.

This script is a focused follow-up to frontier_spectral_on_lattice.py.
It asks a narrower question:

    Does the broadband AWAY result survive once the raw detector-flux
    amplification at each k is removed before spectral summation?

Approach:
  1. Reproduce the retained 2+1D ordered-lattice spectral sum.
  2. Keep the raw coherent sum for comparison.
  3. Add a flux-normalized coherent sum where each detector-sector
     amplitude psi_k is scaled so the total detector probability is 1
     before applying spectral weights.
  4. Compare raw vs flux-normalized results across representative
     configs:
       - k0 = 2.5, 5.0
       - sigma = 0.5, 1.0, 2.0
       - flat spectrum

Verdict target:
  Does broadband AWAY persist after per-k detector-flux normalization?
"""

from __future__ import annotations

import math
import time

import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """Retained 2+1D ordered lattice with valley-linear propagation."""

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
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
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


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field for the retained 2+1D ordered lattice."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None

    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
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


def detector_indices(lat):
    dl = lat.nl - 1
    return [
        lat.nmap[(dl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (dl, iy, iz) in lat.nmap
    ]


def centroid_from_det_probs(det_probs, pos, h):
    total = float(sum(det_probs.values()))
    if total < 1e-30:
        return 0.0, total
    zc = sum(z * h * p for z, p in det_probs.items()) / total
    return zc, total


def det_amps_for_lat(lat, amps):
    dl = lat.nl - 1
    det_amps = {}
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((dl, iy, iz))
            if idx is not None:
                det_amps[iz] = det_amps.get(iz, 0j) + amps[idx]
    return det_amps


def normalize_detector_amps(det_amps):
    total = sum(abs(a) ** 2 for a in det_amps.values())
    if total < 1e-30:
        return {z: 0j for z in det_amps}, total
    scale = 1.0 / math.sqrt(total)
    return {z: a * scale for z, a in det_amps.items()}, total


def centroid_from_amps(det_amps, pos_map):
    det_probs = {z: abs(a) ** 2 for z, a in det_amps.items()}
    return centroid_from_det_probs(det_probs, pos_map["pos"], pos_map["h"])


def main():
    print("=" * 78)
    print("SPECTRAL AVERAGING ON RETAINED 2+1D ORDERED LATTICE")
    print("WITH PER-k FLUX NORMALIZATION")
    print("=" * 78)
    print()
    print("Question:")
    print("  Does broadband AWAY persist once each detector sector psi_k is")
    print("  normalized to unit detector probability before spectral summation?")
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
    det = detector_indices(lat)
    pos_map = {"pos": lat.pos, "h": h}

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={h}")
    print(f"Mass at z={z_mass}, strength={STRENGTH}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    print("=" * 78)
    print("PART 1: Single-k gravity on retained 2+1D lattice")
    print("=" * 78)
    print()

    k_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    print(f"{'k':>6} | {'delta':>12} | {'direction':>9} | {'det_prob':>10}")
    print("-" * 50)

    single_k_results = {}
    for k in k_values:
        af = lat.propagate(field_flat, k, blocked)
        pf = sum(abs(af[d]) ** 2 for d in det)
        zf = sum(abs(af[d]) ** 2 * lat.pos[d, 2] for d in det) / pf if pf > 1e-30 else 0.0

        am = lat.propagate(field_mass, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        zm = sum(abs(am[d]) ** 2 * lat.pos[d, 2] for d in det) / pm if pm > 1e-30 else 0.0

        delta = zm - zf
        direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
        single_k_results[k] = {"delta": delta, "dir": direction, "prob": pm}
        print(f"{k:>6.1f} | {delta:>+12.6f} | {direction:>9} | {pm:>10.3e}")

    n_toward = sum(1 for r in single_k_results.values() if r["dir"] == "TOWARD")
    n_away = sum(1 for r in single_k_results.values() if r["dir"] == "AWAY")
    print(f"\nTOWARD: {n_toward}/{len(k_values)}, AWAY: {n_away}/{len(k_values)}")
    print()

    print("=" * 78)
    print("PART 2: Spectral averaging with and without per-k flux normalization")
    print("=" * 78)
    print()

    k_fine = np.arange(0.5, 12.01, 0.25)
    print(f"Pre-computing {len(k_fine)} propagations...")
    t1 = time.time()

    flat_det_amps = {}
    mass_det_amps = {}
    flat_det_amps_norm = {}
    mass_det_amps_norm = {}
    flat_det_prob = {}
    mass_det_prob = {}

    for k in k_fine:
        af = lat.propagate(field_flat, k, blocked)
        am = lat.propagate(field_mass, k, blocked)

        flat_det = det_amps_for_lat(lat, af)
        mass_det = det_amps_for_lat(lat, am)
        flat_det_amps[k] = flat_det
        mass_det_amps[k] = mass_det

        flat_det_amps_norm[k], flat_det_prob[k] = normalize_detector_amps(flat_det)
        mass_det_amps_norm[k], mass_det_prob[k] = normalize_detector_amps(mass_det)

    print(f"Done in {time.time() - t1:.0f}s")
    print()

    configs = [
        (2.5, 0.5, "narrow around k=2.5"),
        (2.5, 1.0, "medium around k=2.5"),
        (2.5, 2.0, "broad around k=2.5"),
        (5.0, 0.5, "narrow around k=5.0"),
        (5.0, 1.0, "medium around k=5.0"),
        (5.0, 2.0, "broad around k=5.0"),
        (None, None, "flat spectrum"),
    ]

    print(
        f"{'k0':>4} {'sigma':>5} | "
        f"{'raw_delta':>12} {'raw_dir':>9} | "
        f"{'flux_delta':>12} {'flux_dir':>9} | label"
    )
    print("-" * 106)

    spectral_results = []
    for k0, sigma, label in configs:
        if k0 is None:
            weights = {k: 1.0 / len(k_fine) for k in k_fine}
        else:
            weights = {k: math.exp(-(k - k0) ** 2 / (2 * sigma ** 2)) for k in k_fine}
            w_sum = sum(weights.values())
            weights = {k: w / w_sum for k, w in weights.items()}

        raw_coh_mass = {
            d: sum(weights[k] * mass_det_amps[k][d] for k in k_fine)
            for d in range(-lat.hw, lat.hw + 1)
        }
        raw_coh_flat = {
            d: sum(weights[k] * flat_det_amps[k][d] for k in k_fine)
            for d in range(-lat.hw, lat.hw + 1)
        }
        raw_pm = sum(abs(raw_coh_mass[d]) ** 2 for d in raw_coh_mass)
        raw_pf = sum(abs(raw_coh_flat[d]) ** 2 for d in raw_coh_flat)
        raw_zm = (
            sum(abs(raw_coh_mass[d]) ** 2 * d * h for d in raw_coh_mass) / raw_pm
            if raw_pm > 1e-30 else 0.0
        )
        raw_zf = (
            sum(abs(raw_coh_flat[d]) ** 2 * d * h for d in raw_coh_flat) / raw_pf
            if raw_pf > 1e-30 else 0.0
        )
        raw_delta = raw_zm - raw_zf
        raw_dir = "TOWARD" if raw_delta > 1e-10 else "AWAY" if raw_delta < -1e-10 else "~zero"

        flux_coh_mass = {
            d: sum(weights[k] * mass_det_amps_norm[k][d] for k in k_fine)
            for d in range(-lat.hw, lat.hw + 1)
        }
        flux_coh_flat = {
            d: sum(weights[k] * flat_det_amps_norm[k][d] for k in k_fine)
            for d in range(-lat.hw, lat.hw + 1)
        }
        flux_pm = sum(abs(flux_coh_mass[d]) ** 2 for d in flux_coh_mass)
        flux_pf = sum(abs(flux_coh_flat[d]) ** 2 for d in flux_coh_flat)
        flux_zm = (
            sum(abs(flux_coh_mass[d]) ** 2 * d * h for d in flux_coh_mass) / flux_pm
            if flux_pm > 1e-30 else 0.0
        )
        flux_zf = (
            sum(abs(flux_coh_flat[d]) ** 2 * d * h for d in flux_coh_flat) / flux_pf
            if flux_pf > 1e-30 else 0.0
        )
        flux_delta = flux_zm - flux_zf
        flux_dir = "TOWARD" if flux_delta > 1e-10 else "AWAY" if flux_delta < -1e-10 else "~zero"

        print(
            f"{'' if k0 is None else f'{k0:>4.1f}'} "
            f"{'' if sigma is None else f'{sigma:>5.1f}'} | "
            f"{raw_delta:>+12.6f} {raw_dir:>9} | "
            f"{flux_delta:>+12.6f} {flux_dir:>9} | {label}"
        )

        spectral_results.append({
            "k0": k0,
            "sigma": sigma,
            "label": label,
            "raw_delta": raw_delta,
            "raw_dir": raw_dir,
            "flux_delta": flux_delta,
            "flux_dir": flux_dir,
        })

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    raw_broad = [r for r in spectral_results if r["sigma"] is not None and r["sigma"] >= 2.0]
    flux_broad = [r for r in spectral_results if r["sigma"] is not None and r["sigma"] >= 2.0]

    raw_toward = sum(1 for r in raw_broad if r["raw_dir"] == "TOWARD")
    raw_away = sum(1 for r in raw_broad if r["raw_dir"] == "AWAY")
    flux_toward = sum(1 for r in flux_broad if r["flux_dir"] == "TOWARD")
    flux_away = sum(1 for r in flux_broad if r["flux_dir"] == "AWAY")

    flat_row = next(r for r in spectral_results if r["label"] == "flat spectrum")
    raw_flat_dir = flat_row["raw_dir"]
    flux_flat_dir = flat_row["flux_dir"]

    print(f"Raw broad spectra:   {raw_toward} TOWARD, {raw_away} AWAY")
    print(f"Flux-normalized broad spectra: {flux_toward} TOWARD, {flux_away} AWAY")
    print(f"Raw flat spectrum:   {raw_flat_dir}")
    print(f"Flux flat spectrum:   {flux_flat_dir}")

    if flux_away > 0 and flux_toward == 0:
        print()
        print("Verdict: broadband AWAY persists after per-k flux normalization.")
        print("The raw amplification bias is not the only driver.")
    elif flux_toward > 0 and flux_away > 0:
        print()
        print("Verdict: flux normalization softens the raw result, but broadband is still mixed.")
    elif flux_toward > 0 and flux_away == 0:
        print()
        print("Verdict: broadband AWAY does NOT persist after flux normalization.")
    else:
        print()
        print("Verdict: flux-normalized broadband result is inconclusive.")

    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
