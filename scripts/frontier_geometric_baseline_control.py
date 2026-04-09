#!/usr/bin/env python3
"""Geometric baseline control on the retained ordered lattice.

This script probes the user's proposed decomposition by replacing the usual
complex phase propagation with monotone delay-only controls on the same
retained 2+1D ordered-lattice setup used by frontier_spectral_on_lattice.py.

Controls tested:
  1. Standard complex propagation at k in [0.5, 2.5, 5.0, 7.0]
  2. Unit-phase positive transport: edge factor magnitude only
  3. Monotone delay weights: exp(-lambda * action) for several lambdas

The goal is not to prove a geometric law. It is to check whether delay-only
path preference tends to bend AWAY on the retained lattice, and whether the
complex result differs from that phase-free baseline.
"""

from __future__ import annotations

import cmath
import math
import time
from dataclasses import dataclass

import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """Retained ordered-lattice harness copied from frontier_spectral_on_lattice."""

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

    def propagate(self, field, k, blocked_set, mode="complex", lam=0.0):
        """Propagate from the source to the detector layer.

        mode:
          complex  - standard retained propagation with exp(i*k*act)
          unit     - phase-free positive transport, no action weighting
          exp      - monotone real weighting exp(-lam * act)
        """
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
                act = L * (1.0 - lf)

                if mode == "complex":
                    edge = np.exp(1j * k * act)
                elif mode == "unit":
                    edge = 1.0
                elif mode == "exp":
                    edge = np.exp(-lam * act)
                else:
                    raise ValueError(f"unknown mode {mode!r}")

                c = a[nz] * edge * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field on the retained 2+1D lattice."""
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
    barrier = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                barrier.append(idx)
    slit_a = [i for i in barrier if lat.pos[i, 1] >= 0.5]
    slit_b = [i for i in barrier if lat.pos[i, 1] <= -0.5]
    return set(barrier) - set(slit_a + slit_b)


def detector_amps(lat, amps):
    """Sum amplitudes on the detector layer by z coordinate."""
    dl = lat.nl - 1
    det = {}
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((dl, iy, iz))
            if idx is not None:
                det[iz] = det.get(iz, 0j) + amps[idx]
    return det


def centroid_from_amps(det_amps, h):
    prob = {z: abs(a) ** 2 for z, a in det_amps.items()}
    total = sum(prob.values())
    if total < 1e-30:
        return 0.0, total
    centroid = sum(z * h * p for z, p in prob.items()) / total
    return centroid, total


def delta_for_mode(lat, field_flat, field_mass, blocked, mode, k=None, lam=0.0):
    af = lat.propagate(field_flat, k if k is not None else 0.0, blocked, mode=mode, lam=lam)
    am = lat.propagate(field_mass, k if k is not None else 0.0, blocked, mode=mode, lam=lam)
    c_flat, pf = centroid_from_amps(detector_amps(lat, af), lat.h)
    c_mass, pm = centroid_from_amps(detector_amps(lat, am), lat.h)
    return {
        "delta": c_mass - c_flat,
        "direction": "TOWARD" if (c_mass - c_flat) > 1e-10 else "AWAY" if (c_mass - c_flat) < -1e-10 else "~zero",
        "c_flat": c_flat,
        "c_mass": c_mass,
        "p_flat": pf,
        "p_mass": pm,
    }


@dataclass
class ControlSpec:
    label: str
    mode: str
    lam: float = 0.0


def main():
    print("=" * 78)
    print("GEOMETRIC BASELINE CONTROL ON RETAINED 2+1D ORDERED LATTICE")
    print("=" * 78)
    print("Same geometry/field/slits as frontier_spectral_on_lattice.py where possible.")
    print("Question: do delay-only controls tend to bend AWAY?")
    print()

    h = 0.5
    phys_w = 6
    phys_l = 12
    z_mass = 3
    k_values = [0.5, 2.5, 5.0, 7.0]

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    blocked = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, z_mass, STRENGTH)

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={h}, W={phys_w}, L={phys_l}")
    print(f"Mass at z={z_mass}, strength={STRENGTH}")
    print(f"K set: {k_values}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    print("=" * 78)
    print("PART 1: Standard complex propagation")
    print("=" * 78)
    print(f"{'k':>6} | {'delta':>12} | {'direction':>9} | {'det_prob':>10}")
    print("-" * 52)

    complex_results = {}
    for k in k_values:
        af = lat.propagate(field_flat, k, blocked, mode="complex")
        am = lat.propagate(field_mass, k, blocked, mode="complex")
        cf, pf = centroid_from_amps(detector_amps(lat, af), lat.h)
        cm, pm = centroid_from_amps(detector_amps(lat, am), lat.h)
        delta = cm - cf
        direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
        complex_results[k] = {"delta": delta, "direction": direction, "p_mass": pm, "p_flat": pf}
        print(f"{k:>6.1f} | {delta:>+12.6f} | {direction:>9} | {pm:>10.3e}")

    print()
    print("=" * 78)
    print("PART 2: Delay-only controls")
    print("=" * 78)
    print("Controls are k-independent; they are shown once for the same retained lattice.")
    print()

    controls = [
        ControlSpec("unit-phase positive transport", "unit"),
        ControlSpec("exp(-0.25*act)", "exp", 0.25),
        ControlSpec("exp(-0.50*act)", "exp", 0.50),
        ControlSpec("exp(-1.00*act)", "exp", 1.00),
    ]

    control_results = {}
    print(f"{'control':<28} | {'delta':>12} | {'direction':>9} | {'flat P':>10} | {'mass P':>10}")
    print("-" * 80)
    for spec in controls:
        res = delta_for_mode(lat, field_flat, field_mass, blocked, spec.mode, lam=spec.lam)
        control_results[spec.label] = res
        print(f"{spec.label:<28} | {res['delta']:>+12.6f} | {res['direction']:>9} | {res['p_flat']:>10.3e} | {res['p_mass']:>10.3e}")

    print()
    print("=" * 78)
    print("PART 3: Comparison")
    print("=" * 78)
    for k in k_values:
        d = complex_results[k]["delta"]
        print(f"  complex k={k:>3.1f}: {d:+.6f} ({complex_results[k]['direction']})")
    print()
    for label, res in control_results.items():
        print(f"  {label:<28}: {res['delta']:+.6f} ({res['direction']})")

    toward_complex = sum(1 for r in complex_results.values() if r["direction"] == "TOWARD")
    away_complex = sum(1 for r in complex_results.values() if r["direction"] == "AWAY")
    toward_controls = sum(1 for r in control_results.values() if r["direction"] == "TOWARD")
    away_controls = sum(1 for r in control_results.values() if r["direction"] == "AWAY")

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print(f"  Standard complex: {toward_complex} TOWARD, {away_complex} AWAY across k={k_values}")
    print(f"  Delay-only controls: {toward_controls} TOWARD, {away_controls} AWAY")

    if away_controls > toward_controls:
        print("  Delay-only path preference leans AWAY on this retained lattice.")
    elif toward_controls > away_controls:
        print("  Delay-only path preference does not lean AWAY on this retained lattice.")
    else:
        print("  Delay-only controls are split; no clear AWAY bias from these tests alone.")

    print("  The complex k sweep still carries the resonance window structure; the")
    print("  monotone controls are the direct geometric-baseline probe.")
    print(f"\n  Total time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
