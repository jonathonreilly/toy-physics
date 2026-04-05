#!/usr/bin/env python3
"""Bounded Nyquist-diffraction probe on the retained 3D ordered-lattice family.

This is a small, review-safe follow-up to the Nyquist-flip claim:

1. scan the phase coupling k across the expected lattice cutoff
2. measure the gravity-side centroid shift for a fixed weak field
3. repeat for two lattice spacings and several field strengths

The safe question is not whether the sign flips. The safe question is:

- does the first sign flip track pi / h?
- does that flip stay field-independent?

If yes, the clean read is a lattice artifact / UV cutoff effect rather than a
continuum-retained prediction.
"""

from __future__ import annotations

import math
import os
import sys

try:
    import numpy as np
except ModuleNotFoundError:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.lattice_3d_valley_linear_card import Lattice3D, K, make_field, setup_slits


PHYS_L = 4
PHYS_W = 4
MASS_Z = 2.0
FIELD_STRENGTHS = (1e-4, 1e-2)
HS = (0.5, 0.25)
K_SAMPLES = 13
K_SCAN_FACTOR = 1.2
DELTA_EPS = 1e-12


def detector_indices(lat: Lattice3D) -> list[int]:
    return [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]


def centroid_z(amps: np.ndarray, det: list[int], pos: np.ndarray) -> float:
    probs = np.array([abs(amps[d]) ** 2 for d in det], dtype=float)
    total = probs.sum()
    if total < 1e-30:
        return 0.0
    return float(np.dot(probs, pos[det, 2]) / total)


def gravity_delta(lat: Lattice3D, blocked: set[int], field: np.ndarray, k: float) -> float:
    det = detector_indices(lat)
    free = lat.propagate(np.zeros(lat.n), 0.0 if k == 0 else k, blocked)  # type: ignore[arg-type]
    grav = lat.propagate(field, k, blocked)
    return centroid_z(grav, det, lat.pos) - centroid_z(free, det, lat.pos)


def sign_label(delta: float) -> str:
    if delta > DELTA_EPS:
        return "TOWARD"
    if delta < -DELTA_EPS:
        return "AWAY"
    return "ZERO"


def first_positive_to_negative_flip(samples: list[tuple[float, float]]) -> float | None:
    prev_k = None
    prev_d = None
    for k, delta in samples:
        if abs(delta) <= DELTA_EPS:
            continue
        if prev_d is not None and prev_d > 0 and delta < 0:
            if abs(delta - prev_d) < 1e-30:
                return 0.5 * (prev_k + k)
            return prev_k + (0 - prev_d) * (k - prev_k) / (delta - prev_d)
        prev_k = k
        prev_d = delta
    return None


def summarize_field_strength(lat: Lattice3D, blocked: set[int], strength: float) -> dict[str, object]:
    field, _ = make_field(lat, MASS_Z, strength)
    nyquist = math.pi / lat.h
    k_values = np.linspace(0.0, K_SCAN_FACTOR * nyquist, K_SAMPLES)
    samples: list[tuple[float, float]] = []
    for k in k_values:
        delta = gravity_delta(lat, blocked, field, float(k))
        samples.append((float(k), float(delta)))
    flip = first_positive_to_negative_flip(samples)
    signs = [sign_label(delta) for _, delta in samples]
    return {
        "strength": strength,
        "nyquist": nyquist,
        "samples": samples,
        "flip": flip,
        "signs": signs,
    }


def main() -> None:
    print("=" * 96)
    print("LATTICE 3D NYQUIST DIFFRACTION PROBE")
    print("  Retained 3D ordered-lattice valley-linear family")
    print(f"  Field strengths: {', '.join(f'{s:g}' for s in FIELD_STRENGTHS)}")
    print(f"  Spatial sizes: h in {HS}, PHYS_L={PHYS_L}, PHYS_W={PHYS_W}")
    print("  Goal: does the first gravity sign flip track pi/h, or does it remain")
    print("        at a fixed physical scale?")
    print("=" * 96)

    for h in HS:
        lat = Lattice3D(PHYS_L, PHYS_W, h)
        _, _, _, blocked, _ = setup_slits(lat)
        print(f"\nSPACING h={h}")
        print(f"  nyquist pi/h = {math.pi / h:.6f}")
        print(f"  lattice nodes = {lat.n:,}")

        flips = []
        for strength in FIELD_STRENGTHS:
            result = summarize_field_strength(lat, blocked, strength)
            flip = result["flip"]
            flips.append(flip)
            print(f"\n  strength={strength:g}")
            print(f"    k      delta_z      sign")
            for k, delta in result["samples"]:
                print(f"    {k:7.3f}  {delta:+.8f}  {sign_label(delta)}")
            if flip is None:
                print("    first flip: not found in scanned range")
            else:
                rel_err = abs(flip - result["nyquist"]) / result["nyquist"]
                print(f"    first flip: {flip:.6f}")
                print(f"    rel_err vs pi/h: {rel_err:.3%}")

        finite_flips = [f for f in flips if f is not None]
        if finite_flips:
            mean_flip = float(np.mean(finite_flips))
            spread = float(np.max(finite_flips) - np.min(finite_flips)) if len(finite_flips) > 1 else 0.0
            print(f"\n  flip summary: mean={mean_flip:.6f}, spread={spread:.6f}")
            print(f"  mean/(pi/h) = {mean_flip / (math.pi / h):.6f}")
        else:
            print("\n  flip summary: no positive-to-negative flip found")

    print("\nSAFE READ")
    print("  - If the first sign flip sits at ~pi/h for both spacings and stays fixed")
    print("    across field strengths, it is a lattice-scale Nyquist effect.")
    print("  - In that case it is a UV cutoff artifact in the continuum limit, even")
    print("    though it is a real and field-independent discrete-lattice prediction.")
    print("  - If the flip failed to track pi/h, that would be the unexpected retained")
    print("    prediction. This probe is designed to check that directly.")


if __name__ == "__main__":
    main()
