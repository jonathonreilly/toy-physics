#!/usr/bin/env python3
"""Bounded source-consistency spectrum probe on the retained ordered lattice.

This is the first honest follow-up to the broadband-gravity failure.

The previous detector-equalized reweightings answered a control question:
can suppressing dominant detector modes flip the sign? Yes.
But they did not answer the physical question:

  does a localized source naturally emit a k-spectrum concentrated in the
  attractive Lorentzian window?

This script stays strictly source-side:
  1. choose candidate localized emitters on the retained ordered lattice
  2. propagate them freely over a short segment
  3. measure how well the source re-identifies itself at a post-source
     reference layer as a function of the action wavenumber k
  4. treat that re-identification score as a source-consistency spectrum
  5. use that source-derived weight to form a broadband sum on the full
     Euclidean and split-delay Lorentzian lattices

Important caveat:
  these are candidate localized emitters / packet surrogates, not a theorem
  that the codebase already has true persistent-pattern emitters.

Review-safe question:
  do source-consistency weights rescue broadband TOWARD on the retained
  Lorentzian lane, or does attraction remain a narrowband phenomenon?
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
SOURCE_SEGMENT_L = 6
H = 0.5


class Lattice3D:
    """Retained ordered lattice with Euclidean and split-delay Lorentzian actions."""

    def __init__(self, phys_l: float, phys_w: float, h: float) -> None:
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw**2
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

    def propagate(self, init_amps: np.ndarray, field: np.ndarray, k: float, lorentzian: bool) -> np.ndarray:
        n = self.n
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = init_amps.copy()

        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls : ls + self.npl].copy()
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls : ls + self.npl]
            df = field[ld : ld + self.npl]
            for dy, dz, L, w, lf_factor in self._off:
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
                if lorentzian:
                    act = L * (1 - lf * lf_factor)
                else:
                    act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                np.add.at(amps[ld : ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat: Lattice3D, z_mass_phys: float, strength: float) -> np.ndarray:
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    field = np.zeros(lat.n)
    if mi is None:
        return field
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    field[:] = strength / r
    return field


def setup_slits(lat: Lattice3D) -> set[int]:
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    return set(bi) - set(sa + sb)


def apply_blocked(amps: np.ndarray, blocked: set[int]) -> None:
    for idx in blocked:
        amps[idx] = 0.0


def detector_indices(lat: Lattice3D) -> list[int]:
    dl = lat.nl - 1
    return [
        lat.nmap[(dl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (dl, iy, iz) in lat.nmap
    ]


def layer_distribution(lat: Lattice3D, amps: np.ndarray, layer: int) -> np.ndarray:
    dist = np.zeros((2 * lat.hw + 1, 2 * lat.hw + 1), dtype=float)
    ls = lat._ls[layer]
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(layer, iy, iz)]
            dist[iy + lat.hw, iz + lat.hw] = abs(amps[idx]) ** 2
    total = dist.sum()
    if total > 1e-30:
        dist /= total
    return dist


def overlap_score(a: np.ndarray, b: np.ndarray) -> float:
    flat_a = a.ravel()
    flat_b = b.ravel()
    denom = math.sqrt(float(np.dot(flat_a, flat_a) * np.dot(flat_b, flat_b)))
    if denom < 1e-30:
        return 0.0
    return float(np.dot(flat_a, flat_b) / denom)


def width(dist: np.ndarray, h: float) -> float:
    n = dist.shape[0]
    hw = (n - 1) // 2
    coords = np.arange(-hw, hw + 1, dtype=float) * h
    y_grid, z_grid = np.meshgrid(coords, coords, indexing="ij")
    total = dist.sum()
    if total < 1e-30:
        return 0.0
    cy = float(np.sum(dist * y_grid) / total)
    cz = float(np.sum(dist * z_grid) / total)
    var = np.sum(dist * ((y_grid - cy) ** 2 + (z_grid - cz) ** 2)) / total
    return float(math.sqrt(max(var, 0.0)))


def gaussian_source(lat: Lattice3D, sigma: float) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(0, iy, iz)]
            y = iy * lat.h
            z = iz * lat.h
            init[idx] = math.exp(-0.5 * (y * y + z * z) / (sigma * sigma))
    norm = np.linalg.norm(init)
    return init / norm if norm > 1e-30 else init


def point_source(lat: Lattice3D) -> np.ndarray:
    init = np.zeros(lat.n, dtype=np.complex128)
    init[lat.nmap[(0, 0, 0)]] = 1.0
    return init


def source_profiles(lat: Lattice3D) -> list[tuple[str, np.ndarray]]:
    return [
        ("point", point_source(lat)),
        ("gauss_sigma1.25", gaussian_source(lat, 1.25)),
        ("gauss_sigma2.50", gaussian_source(lat, 2.50)),
    ]


def centroid_delta(lat: Lattice3D, det: list[int], flat_amps: np.ndarray, mass_amps: np.ndarray) -> float:
    pf = sum(abs(flat_amps[d]) ** 2 for d in det)
    pm = sum(abs(mass_amps[d]) ** 2 for d in det)
    if pf < 1e-30 or pm < 1e-30:
        return 0.0
    zf = sum(abs(flat_amps[d]) ** 2 * lat.pos[d, 2] for d in det) / pf
    zm = sum(abs(mass_amps[d]) ** 2 * lat.pos[d, 2] for d in det) / pm
    return zm - zf


def normalize_weights(weights: dict[float, float]) -> dict[float, float]:
    total = sum(max(w, 0.0) for w in weights.values())
    if total < 1e-30:
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: max(w, 0.0) / total for k, w in weights.items()}


def spectral_delta(
    lat: Lattice3D,
    det: list[int],
    flat_amp_dict: dict[float, np.ndarray],
    mass_amp_dict: dict[float, np.ndarray],
    weights: dict[float, float],
) -> float:
    coh_flat = np.zeros(lat.n, dtype=np.complex128)
    coh_mass = np.zeros(lat.n, dtype=np.complex128)
    for k, w in weights.items():
        coh_flat += w * flat_amp_dict[k]
        coh_mass += w * mass_amp_dict[k]
    return centroid_delta(lat, det, coh_flat, coh_mass)


def main() -> None:
    print("=" * 88)
    print("BOUNDED SOURCE-CONSISTENCY SPECTRUM PROBE")
    print("=" * 88)
    print()
    print("Question:")
    print("  do candidate localized emitters naturally prefer a k-spectrum in the")
    print("  attractive Lorentzian window, or does attraction remain narrowband?")
    print()

    t0 = time.time()
    full_lat = Lattice3D(PHYS_L, PHYS_W, H)
    seg_lat = Lattice3D(SOURCE_SEGMENT_L, PHYS_W, H)
    blocked_full = setup_slits(full_lat)
    blocked_seg = set()
    field_flat_full = np.zeros(full_lat.n)
    field_mass_full = make_field_spatial(full_lat, 3.0, STRENGTH)
    det = detector_indices(full_lat)
    ref_layer = seg_lat.nl - 1
    print(f"Full lattice: L={PHYS_L}, W={PHYS_W}, h={H}, {full_lat.n:,} nodes")
    print(f"Source segment: L={SOURCE_SEGMENT_L}, reference layer={ref_layer}")
    print(f"Mass strength: {STRENGTH}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    k_values = [round(k, 4) for k in np.arange(0.5, 12.01, 0.5)]
    models = {
        "euclidean": False,
        "lorentzian": True,
    }

    # Precompute full-lattice detector amplitudes for spectral sums.
    print(f"Pre-computing full-lattice detector responses ({len(k_values) * len(models) * 2} propagations)...")
    t1 = time.time()
    full_data: dict[str, dict[str, dict[float, np.ndarray]]] = {}
    for model_name, is_lorentzian in models.items():
        model_flat = {}
        model_mass = {}
        for i, k in enumerate(k_values, start=1):
            src = point_source(full_lat)
            af = full_lat.propagate(src, field_flat_full, k, lorentzian=is_lorentzian)
            am = full_lat.propagate(src, field_mass_full, k, lorentzian=is_lorentzian)
            apply_blocked(af, blocked_full)
            apply_blocked(am, blocked_full)
            model_flat[k] = af
            model_mass[k] = am
            if i % 12 == 0:
                print(f"  {model_name}: {i}/{len(k_values)} k values")
        full_data[model_name] = {"flat": model_flat, "mass": model_mass}
    print(f"Done in {time.time() - t1:.0f}s")
    print()

    print("=" * 88)
    print("SOURCE-CONSISTENCY SPECTRA")
    print("=" * 88)

    for model_name, is_lorentzian in models.items():
        print()
        print(f"{model_name.upper()}:")
        print(
            f"{'source':<16} | {'k_peak':>6} | {'peak_dir':>7} | {'w_toward':>8} | "
            f"{'w_away':>8} | {'broad_delta':>11} {'dir':>7}"
        )
        print("-" * 78)

        for label, init in source_profiles(seg_lat):
            source_template = layer_distribution(seg_lat, init, 0)
            source_width = width(source_template, seg_lat.h)
            score_weights = {}
            for k in k_values:
                amps = seg_lat.propagate(init, np.zeros(seg_lat.n), k, lorentzian=is_lorentzian)
                ref_dist = layer_distribution(seg_lat, amps, ref_layer)
                score = overlap_score(source_template, ref_dist)
                ref_width = width(ref_dist, seg_lat.h)
                width_ratio = ref_width / source_width if source_width > 1e-30 else 0.0
                # Penalize explosive broadening; keep source-side only.
                score_weights[k] = score / (1.0 + abs(width_ratio - 1.0))

            weights = normalize_weights(score_weights)
            k_peak = max(weights, key=weights.get)
            delta_peak = centroid_delta(
                full_lat,
                det,
                full_data[model_name]["flat"][k_peak],
                full_data[model_name]["mass"][k_peak],
            )
            peak_dir = "TOWARD" if delta_peak > 1e-10 else "AWAY" if delta_peak < -1e-10 else "~zero"
            w_toward = 0.0
            w_away = 0.0
            for k in k_values:
                delta_k = centroid_delta(
                    full_lat,
                    det,
                    full_data[model_name]["flat"][k],
                    full_data[model_name]["mass"][k],
                )
                if delta_k > 1e-10:
                    w_toward += weights[k]
                elif delta_k < -1e-10:
                    w_away += weights[k]

            broadband_delta = spectral_delta(
                full_lat,
                det,
                full_data[model_name]["flat"],
                full_data[model_name]["mass"],
                weights,
            )
            broad_dir = "TOWARD" if broadband_delta > 1e-10 else "AWAY" if broadband_delta < -1e-10 else "~zero"
            print(
                f"{label:<16} | {k_peak:>6.1f} | {peak_dir:>7} | {w_toward:>8.3f} | "
                f"{w_away:>8.3f} | {broadband_delta:>+11.6f} {broad_dir:>7}"
            )

    print()
    print("Interpretation:")
    print("  - k_peak is the source-consistency peak from short free propagation only.")
    print("  - w_toward / w_away split the source-derived weight across attractive and repulsive windows.")
    print("  - broad_delta tests whether that source-derived spectrum rescues broadband attraction.")
    print("  - This is a bounded source-side probe, not a persistent-pattern theorem.")


if __name__ == "__main__":
    main()
