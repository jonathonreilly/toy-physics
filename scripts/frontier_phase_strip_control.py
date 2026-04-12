#!/usr/bin/env python3
"""Retained-lattice phase-strip control.

Goal: test whether the attractive retained-lattice signal survives when the
complex phase structure is removed or randomized.

This script reuses the retained 2+1D ordered-lattice setup from the spectral
on-lattice harness and compares three propagation modes:
  1. standard:      exp(i * k * act)
  2. phase stripped: 1
  3. randomized:    same magnitude, random edge phases per run

It measures centroid shifts for a few single-k values and for one narrowband
spectral packet centered near k=5.0.
"""

from __future__ import annotations

import math
import time
from collections import defaultdict

import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """Retained ordered-lattice harness with variable k and phase modes."""

    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw * nw
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

    def propagate(self, field, k, blocked_set, phase_mode="standard", rng_seed=None):
        """Propagate from the source to the detector layer.

        phase_mode:
          - standard: exp(i*k*act)
          - stripped: 1
          - randomized: random unit phase per edge contribution
        """
        n = self.n
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0 + 0j
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        rng = None
        if phase_mode == "randomized":
            rng = np.random.default_rng(rng_seed)

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
                act = L * (1.0 - lf)
                if phase_mode == "standard":
                    phase = np.exp(1j * k * act)
                elif phase_mode == "stripped":
                    phase = np.ones_like(act, dtype=np.complex128)
                elif phase_mode == "randomized":
                    assert rng is not None
                    phase = np.exp(1j * (2.0 * math.pi * rng.random(act.shape[0])))
                else:
                    raise ValueError(f"unknown phase_mode={phase_mode!r}")
                c = a[nz] * phase * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field on the ordered lattice."""
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


def centroid_from_amps(det_amps, h):
    prob = {z: abs(a) ** 2 for z, a in det_amps.items()}
    total = sum(prob.values())
    if total < 1e-30:
        return 0.0, total
    c = sum(z * h * p for z, p in prob.items()) / total
    return c, total


def detector_amps(lat, amps):
    dl = lat.nl - 1
    det_amps = {}
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((dl, iy, iz))
            if idx is not None:
                det_amps[iz] = det_amps.get(iz, 0j) + amps[idx]
    return det_amps


def shift_for_mode(lat, field_mass, field_flat, blocked, k, mode, rng_seed=None):
    am = lat.propagate(field_mass, k, blocked, phase_mode=mode, rng_seed=rng_seed)
    af = lat.propagate(field_flat, k, blocked, phase_mode=mode, rng_seed=rng_seed)
    cm, _ = centroid_from_amps(detector_amps(lat, am), lat.h)
    cf, _ = centroid_from_amps(detector_amps(lat, af), lat.h)
    return cm - cf


def spectral_shift_for_mode(lat, field_mass, field_flat, blocked, k_samples, weights, mode, seed_base=None):
    def summed_detector(field, use_seed=False):
        combined = defaultdict(complex)
        for i, (k, w) in enumerate(zip(k_samples, weights)):
            rng_seed = None if seed_base is None else seed_base * 1000 + i
            amps = lat.propagate(field, k, blocked, phase_mode=mode, rng_seed=rng_seed if use_seed else rng_seed)
            det = detector_amps(lat, amps)
            for z, a in det.items():
                combined[z] += w * a
        return dict(combined)

    dm = summed_detector(field_mass, use_seed=(mode == "randomized"))
    df = summed_detector(field_flat, use_seed=(mode == "randomized"))
    cm, _ = centroid_from_amps(dm, lat.h)
    cf, _ = centroid_from_amps(df, lat.h)
    return cm - cf


def gaussian_weights(k_samples, k0, sigma):
    raw = [math.exp(-((k - k0) ** 2) / (2.0 * sigma ** 2)) for k in k_samples]
    s = sum(raw)
    return [x / s for x in raw]


def sign_label(delta, tol=1e-10):
    if delta > tol:
        return "T"
    if delta < -tol:
        return "A"
    return "~"


def main():
    print("=" * 78)
    print("RETAINED-LATTICE PHASE-STRIP CONTROL")
    print("=" * 78)
    print("Question: does the attractive signal survive when phase is removed or randomized?")
    print("Harness: retained 2+1D ordered lattice, same slit/field setup as spectral test")
    print()

    h = 0.5
    phys_w = 6
    phys_l = 12
    z_mass = 3
    key_ks = [0.5, 2.5, 5.0, 7.0]
    rand_seeds = list(range(8))
    packet_center = 5.0
    packet_sigma = 0.5
    packet_k_samples = np.arange(3.5, 6.51, 0.25)
    packet_weights = gaussian_weights(packet_k_samples, packet_center, packet_sigma)

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    blocked = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, z_mass, STRENGTH)

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={h}")
    print(f"Mass at z={z_mass}, strength={STRENGTH}")
    print(f"Packet: k0={packet_center}, sigma={packet_sigma}, samples={len(packet_k_samples)}")
    print(f"Randomized phase seeds: {rand_seeds}")
    print(f"Setup time: {time.time() - t0:.1f}s")
    print()

    # Single-k control table
    print("=" * 78)
    print("SINGLE-k CONTROL")
    print("=" * 78)
    print(f"{'k':>5} | {'standard':>24} | {'stripped':>24} | {'randomized mean':>24}")
    print("-" * 90)

    single_rows = []
    for k in key_ks:
        std = shift_for_mode(lat, field_mass, field_flat, blocked, k, "standard")
        strip = shift_for_mode(lat, field_mass, field_flat, blocked, k, "stripped")
        rand = [shift_for_mode(lat, field_mass, field_flat, blocked, k, "randomized", seed) for seed in rand_seeds]
        rand_mean = float(np.mean(rand))
        rand_std = float(np.std(rand))
        rand_toward = sum(1 for x in rand if x > 0)
        rand_away = sum(1 for x in rand if x < 0)
        single_rows.append((k, std, strip, rand_mean, rand_std, rand_toward, rand_away))
        print(
            f"{k:>5.1f} | "
            f"{std:+.6f} ({sign_label(std)}) | "
            f"{strip:+.6f} ({sign_label(strip)}) | "
            f"{rand_mean:+.6f} ±{rand_std:.6f} ({rand_toward}T/{rand_away}A)"
        )

    # Narrowband packet around k=5
    print()
    print("=" * 78)
    print("NARROWBAND PACKET CONTROL")
    print("=" * 78)
    print(f"k0={packet_center}, sigma={packet_sigma}")
    print(f"{'mode':>12} | {'delta':>12} | {'sign':>5} | {'randomized summary':>24}")
    print("-" * 70)

    std_packet = spectral_shift_for_mode(lat, field_mass, field_flat, blocked, packet_k_samples, packet_weights, "standard")
    strip_packet = spectral_shift_for_mode(lat, field_mass, field_flat, blocked, packet_k_samples, packet_weights, "stripped")
    rand_packet = [
        spectral_shift_for_mode(lat, field_mass, field_flat, blocked, packet_k_samples, packet_weights, "randomized", seed)
        for seed in rand_seeds
    ]
    rand_packet_mean = float(np.mean(rand_packet))
    rand_packet_std = float(np.std(rand_packet))
    rand_packet_toward = sum(1 for x in rand_packet if x > 0)
    rand_packet_away = sum(1 for x in rand_packet if x < 0)

    print(f"{'standard':>12} | {std_packet:+12.6f} | {sign_label(std_packet):>5} |")
    print(f"{'stripped':>12} | {strip_packet:+12.6f} | {sign_label(strip_packet):>5} |")
    print(
        f"{'randomized':>12} | "
        f"{rand_packet_mean:+12.6f} | "
        f"{sign_label(rand_packet_mean):>5} | "
        f"{rand_packet_toward}T/{rand_packet_away}A, std={rand_packet_std:.6f}"
    )

    # Verdict
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    std_toward = sum(1 for _, std, _, _, _, _, _ in single_rows if std > 0)
    strip_toward = sum(1 for _, _, strip, _, _, _, _ in single_rows if strip > 0)
    rand_toward = sum(1 for _, _, _, rmean, _, _, _ in single_rows if rmean > 0)
    print(f"Single-k TOWARD counts: standard {std_toward}/{len(key_ks)}, stripped {strip_toward}/{len(key_ks)}, randomized-mean {rand_toward}/{len(key_ks)}")
    print(
        f"Packet centered at k={packet_center}: standard {sign_label(std_packet)}, "
        f"stripped {sign_label(strip_packet)}, randomized-mean {sign_label(rand_packet_mean)}"
    )

    if abs(strip_packet) < 1e-10 and abs(rand_packet_mean) < 1e-10:
        print("Verdict: no, removing phase collapses the signal to ~zero, not AWAY.")
    elif strip_packet < 0 or rand_packet_mean < 0:
        print("Verdict: yes, an AWAY baseline appears once phase structure is removed.")
    else:
        print("Verdict: mixed; phase removal weakens attraction but does not cleanly produce AWAY.")

    print(f"Total runtime: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
