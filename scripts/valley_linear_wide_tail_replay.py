#!/usr/bin/env python3
"""Bounded wide-tail replay for the 3D valley-linear ordered-lattice lane.

This is a narrow follow-up to the retained h=0.25 valley-linear family.

It asks only:
  - does a wider W=12 lattice preserve the barrier-side sanity checks?
  - does the no-barrier post-peak tail become better resolved?

It is not a universal theorem harness.
"""

from __future__ import annotations

import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this replay. On this machine use /usr/bin/python3."
    ) from exc

from scripts.valley_linear_same_harness_compare import (
    H,
    K,
    PHYS_L,
    STRENGTH,
    Lattice3D,
    fit_power,
    make_field,
    setup_slits,
)


PHYS_W = 12
Z_VALUES = list(range(2, 11))


def born_audit(lat: Lattice3D, det: list[int], sa: list[int], sb: list[int], blocked: set[int]) -> float:
    field_zero = np.zeros(lat.n)
    bl = lat.nl // 3
    barrier_nodes = {
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap
    }
    pos = lat.pos
    upper = sorted([i for i in barrier_nodes if pos[i, 1] > 1.0], key=lambda i: pos[i, 1])
    lower = sorted([i for i in barrier_nodes if pos[i, 1] < -1.0], key=lambda i: -pos[i, 1])
    middle = [i for i in barrier_nodes if abs(pos[i, 1]) <= 1.0 and abs(pos[i, 2]) <= 1.0]
    if not upper or not lower or not middle:
        return math.nan

    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = barrier_nodes - all_s
    probs = {}
    for key, open_set in [
        ("abc", all_s),
        ("ab", set(s_a + s_b)),
        ("ac", set(s_a + s_c)),
        ("bc", set(s_b + s_c)),
        ("a", set(s_a)),
        ("b", set(s_b)),
        ("c", set(s_c)),
    ]:
        blocked_now = other | (all_s - open_set)
        amps = lat.propagate(field_zero, K, blocked_now, "valley_linear")
        probs[key] = np.array([abs(amps[d]) ** 2 for d in det])

    i3 = 0.0
    total = 0.0
    for idx in range(len(det)):
        term = (
            probs["abc"][idx]
            - probs["ab"][idx]
            - probs["ac"][idx]
            - probs["bc"][idx]
            + probs["a"][idx]
            + probs["b"][idx]
            + probs["c"][idx]
        )
        i3 += abs(term)
        total += probs["abc"][idx]
    return i3 / total if total > 1e-30 else math.nan


def main() -> None:
    t0 = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    pos = lat.pos
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    sa, sb, blocked, _ = setup_slits(lat)

    print("=" * 88)
    print("3D VALLEY-LINEAR WIDE-TAIL REPLAY")
    print("  Bounded h=0.25, W=12 follow-up on the ordered-lattice 1/L^2 family.")
    print(f"  nodes={lat.n:,}  layers={lat.nl}  h={H}  W={PHYS_W}  max_d={lat.max_d}")
    print("=" * 88)
    print()

    field_zero = np.zeros(lat.n)
    amps_flat = lat.propagate(field_zero, K, blocked, "valley_linear")
    p_flat = sum(abs(amps_flat[d]) ** 2 for d in det)
    z_flat = sum(abs(amps_flat[d]) ** 2 * pos[d, 2] for d in det) / p_flat

    born = born_audit(lat, det, sa, sb, blocked)

    field_mass3 = make_field(lat, 3, STRENGTH)
    amps_f0 = lat.propagate(field_zero, 0.0, blocked, "valley_linear")
    amps_m0 = lat.propagate(field_mass3, 0.0, blocked, "valley_linear")
    p_f0 = sum(abs(amps_f0[d]) ** 2 for d in det)
    p_m0 = sum(abs(amps_m0[d]) ** 2 for d in det)
    k0 = 0.0
    if p_f0 > 1e-30 and p_m0 > 1e-30:
        z_f0 = sum(abs(amps_f0[d]) ** 2 * pos[d, 2] for d in det) / p_f0
        z_m0 = sum(abs(amps_m0[d]) ** 2 * pos[d, 2] for d in det) / p_m0
        k0 = z_m0 - z_f0

    print(f"Barrier sanity: Born={born:.2e}  k=0={k0:+.6f}")
    print()

    rows = []
    b_all = []
    d_all = []
    print("No-barrier distance rows:")
    for z_mass in Z_VALUES:
        field = make_field(lat, z_mass, STRENGTH)
        amps = lat.propagate(field, K, set(), "valley_linear")
        p_mass = sum(abs(amps[d]) ** 2 for d in det)
        if p_mass <= 1e-30:
            continue
        z_mass_centroid = sum(abs(amps[d]) ** 2 * pos[d, 2] for d in det) / p_mass
        delta = z_mass_centroid - z_flat
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  z={z_mass:>2d}  delta={delta:+.6f}  {direction}")
        rows.append((z_mass, delta))
        if delta > 0:
            b_all.append(z_mass)
            d_all.append(delta)

    peak_i = int(np.argmax(np.array(d_all))) if d_all else 0
    peak_z = b_all[peak_i] if b_all else math.nan
    slope_peak = r2_peak = math.nan
    slope_far = r2_far = math.nan
    n_peak = n_far = 0

    if len(d_all[peak_i:]) >= 3:
        slope_peak, r2_peak = fit_power(b_all[peak_i:], d_all[peak_i:])
        n_peak = len(d_all[peak_i:])

    far_pairs = [(b, d) for b, d in zip(b_all, d_all) if b >= 5]
    if len(far_pairs) >= 3:
        slope_far, r2_far = fit_power([b for b, _ in far_pairs], [d for _, d in far_pairs])
        n_far = len(far_pairs)

    print()
    print(f"TOWARD support: {len(b_all)}/{len(Z_VALUES)}")
    if n_peak >= 3:
        print(f"Tail from peak (z>={peak_z}): b^({slope_peak:.2f}), R^2={r2_peak:.3f}  n={n_peak}")
    if n_far >= 3:
        print(f"Far tail (z>=5): b^({slope_far:.2f}), R^2={r2_far:.3f}  n={n_far}")
    print()
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
