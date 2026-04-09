#!/usr/bin/env python3
"""Independent replay of the wide-lattice h^2+T distance-law claim.

This is intentionally narrow:
  - one retained ordered 3D family
  - valley-linear action
  - 1/L^2 kernel with h^2 measure
  - widened W=12 replay at h=0.25

The goal is to independently retest the branch-side wide-lattice far-tail
distance-law claim and decide whether it is retained frontier, still
exploratory, or a no-go.
"""

from __future__ import annotations

import math
import time

import os
import sys

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-specific
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this replay. On this machine use /usr/bin/python3."
    ) from exc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.valley_linear_same_harness_compare import (
    H,
    K,
    PHYS_L,
    STRENGTH,
    Lattice3D,
    make_field,
    setup_slits,
)


PHYS_W = 12
Z_VALUES = list(range(2, 12))
FAR_MIN_Z = 5
FIELD_SWEEP = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]


def fit_power(xs: list[float], ys: list[float]) -> tuple[float | None, float | None]:
    if len(xs) < 3:
        return None, None
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None, None
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def born_audit(lat: Lattice3D, det: list[int], blocked: set[int]) -> float:
    field_zero = np.zeros(lat.n)
    pos = lat.pos
    bl = lat.nl // 3
    barrier_nodes = {
        lat.nmap[(bl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (bl, iy, iz) in lat.nmap
    }
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
    _, _, blocked, _ = setup_slits(lat)

    print("=" * 88)
    print("WIDE-LATTICE H^2+T DISTANCE-LAW REPLAY")
    print("  Independent wide replay of the ordered 3D 1/L^2 family.")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}")
    print("=" * 88)
    print()

    field_zero = np.zeros(lat.n)
    amps_free = lat.propagate(field_zero, K, blocked, "valley_linear")
    p_free = sum(abs(amps_free[d]) ** 2 for d in det)
    z_free = sum(abs(amps_free[d]) ** 2 * pos[d, 2] for d in det) / p_free

    born = born_audit(lat, det, blocked)

    field_mass = make_field(lat, 3, STRENGTH)
    amps_k0_free = lat.propagate(field_zero, 0.0, blocked, "valley_linear")
    amps_k0_mass = lat.propagate(field_mass, 0.0, blocked, "valley_linear")
    p0_free = sum(abs(amps_k0_free[d]) ** 2 for d in det)
    p0_mass = sum(abs(amps_k0_mass[d]) ** 2 for d in det)
    k0 = 0.0
    if p0_free > 1e-30 and p0_mass > 1e-30:
        z0_free = sum(abs(amps_k0_free[d]) ** 2 * pos[d, 2] for d in det) / p0_free
        z0_mass = sum(abs(amps_k0_mass[d]) ** 2 * pos[d, 2] for d in det) / p0_mass
        k0 = z0_mass - z0_free

    print(f"Barrier sanity: Born={born:.2e}  k=0={k0:+.6f}")
    print()

    print("Distance rows:")
    toward_z: list[float] = []
    toward_delta: list[float] = []
    all_rows: list[tuple[int, float]] = []
    for z_mass in Z_VALUES:
        field = make_field(lat, z_mass, STRENGTH)
        amps = lat.propagate(field, K, blocked, "valley_linear")
        p_mass = sum(abs(amps[d]) ** 2 for d in det)
        if p_mass <= 1e-30:
            print(f"  z={z_mass:>2d}  no signal")
            continue
        z_mass_centroid = sum(abs(amps[d]) ** 2 * pos[d, 2] for d in det) / p_mass
        delta = z_mass_centroid - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  z={z_mass:>2d}  delta={delta:+.6f}  {direction}")
        all_rows.append((z_mass, delta))
        if delta > 0:
            toward_z.append(z_mass)
            toward_delta.append(delta)

    peak_i = max(range(len(toward_delta)), key=lambda i: toward_delta[i]) if toward_delta else None
    peak_tail = (math.nan, math.nan, 0)
    far_tail = (math.nan, math.nan, 0)
    if peak_i is not None:
        tail_z = toward_z[peak_i:]
        tail_d = toward_delta[peak_i:]
        if len(tail_z) >= 3:
            slope, r2 = fit_power(tail_z, tail_d)
            if slope is not None:
                peak_tail = (slope, r2, len(tail_z))
        far_pairs = [(z, d) for z, d in zip(toward_z, toward_delta) if z >= FAR_MIN_Z]
        if len(far_pairs) >= 3:
            slope, r2 = fit_power([z for z, _ in far_pairs], [d for _, d in far_pairs])
            if slope is not None:
                far_tail = (slope, r2, len(far_pairs))

    print()
    print(f"TOWARD support: {len(toward_z)}/{len(Z_VALUES)}")
    if peak_tail[2] >= 3 and toward_z:
        peak_z = toward_z[peak_i]
        print(f"Peak tail from z>={peak_z}: b^({peak_tail[0]:.2f}), R^2={peak_tail[1]:.3f}, n={peak_tail[2]}")
    if far_tail[2] >= 3:
        print(f"Far tail from z>={FAR_MIN_Z}: b^({far_tail[0]:.2f}), R^2={far_tail[1]:.3f}, n={far_tail[2]}")

    print()
    print("F~M sweep:")
    m_data: list[float] = []
    g_data: list[float] = []
    for strength in FIELD_SWEEP:
        field = make_field(lat, 3, strength)
        amps = lat.propagate(field, K, blocked, "valley_linear")
        p_mass = sum(abs(amps[d]) ** 2 for d in det)
        if p_mass <= 1e-30:
            continue
        z_mass_centroid = sum(abs(amps[d]) ** 2 * pos[d, 2] for d in det) / p_mass
        delta = z_mass_centroid - z_free
        sign = "TOWARD" if delta > 0 else "AWAY"
        print(f"  s={strength:.0e}: delta={delta:+.6e}  {sign}")
        if delta > 0:
            m_data.append(strength)
            g_data.append(delta)

    fm_alpha = math.nan
    if len(m_data) >= 3:
        fm_alpha, _ = fit_power(m_data, g_data)
    print(f"  F~M exponent: {fm_alpha:.3f}" if not math.isnan(fm_alpha) else "  F~M exponent: n/a")

    total = time.time() - t0
    print()
    print(f"Total time: {total:.1f}s")


if __name__ == "__main__":
    main()
