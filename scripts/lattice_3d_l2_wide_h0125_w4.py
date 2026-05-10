#!/usr/bin/env python3
"""Single-width wider-family diagnostic for the 3D dense 1/L^2 h=0.125 lane.

This is the focused follow-up to the fixed-family negative: it keeps the same
replay machinery, widens the physical box, and asks whether the weak-field
mass-law exponent moves toward 1.0 or stays pinned near the fixed-family
~0.5 limit.
"""

from __future__ import annotations

# Heavy compute / wider-family lattice diagnostic — far exceeds the 120s
# default audit timeout. Measured wall-clock at 2026-05-10: ~1002s on
# the canonical Python 3.12 machine (most time in numpy linear-algebra
# work on the wider physical box); declaring 1800s here gives ~80%
# margin while keeping the audit-cache budget bounded (same as poisson
# and the sister h0125_wider_replay runner). Without this declaration
# the audit lane caches an empty stdout under `status: timeout`,
# blocking the audit verdict.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np

from scripts.lattice_3d_l2_numpy_h0125_only import (
    K,
    born_ratio,
    build_dense_family,
    detector_probability,
    free_prefix_to_barrier,
    make_field_layers,
    propagate_field,
    propagate_free_from_barrier,
)


def fit_power(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def centroid(lat: dict[str, object], amps: np.ndarray, mask: np.ndarray) -> tuple[float | None, float]:
    probs = detector_probability(amps)
    masked = probs * mask
    total = float(masked.sum())
    if total <= 1e-30:
        return None, 0.0
    z = lat["yz"][:, 1]
    return float((masked * z).sum() / total), total


def main() -> None:
    phys_l = 6
    phys_w = 4
    h = 0.125
    z_mass_values = [1.5, 2.0, 3.0]
    strengths = [1e-7, 2e-7, 5e-7, 1e-6, 2e-6, 5e-6]

    print("=" * 92)
    print("WIDER H=0.125 W=4 DIAGNOSTIC")
    print("  goal: test whether a genuinely wider retained family rescues F~M")
    print("=" * 92)
    print(f"  family: phys_l={phys_l}, phys_w={phys_w}, h={h}")
    print(f"  strengths: {', '.join(f'{s:.0e}' for s in strengths)}")
    print()

    lat = build_dense_family(phys_l, phys_w, h)
    _prefix, barrier_in = free_prefix_to_barrier(lat)
    free_final = propagate_free_from_barrier(lat, barrier_in, lat["default_open"])
    free_full, p_free = centroid(lat, free_final, np.ones_like(lat["yz"][:, 1], dtype=bool))

    born = born_ratio(lat, barrier_in)
    field_ref = make_field_layers(lat, 3.0, strengths[-1])
    null_final = propagate_field(lat, field_ref, lat["default_open"], 0.0)
    grav_final = propagate_field(lat, field_ref, lat["default_open"], K)
    null_full, _ = centroid(lat, null_final, np.ones_like(lat["yz"][:, 1], dtype=bool))
    grav_full, p_grav = centroid(lat, grav_final, np.ones_like(lat["yz"][:, 1], dtype=bool))

    print(f"nodes={lat['n']} layers={lat['nl']} nodes/layer={lat['npl']} dense_edges={lat['edges']}")
    print(f"Born={born:.2e}")
    if null_full is not None and free_full is not None:
        print(f"k=0 check={null_full - free_full:+.6f}")
    if grav_full is not None and free_full is not None:
        print(f"gravity(z=3, s={strengths[-1]:.0e})={grav_full - free_full:+.6f}  P_det={p_grav:.3e}")
    print()

    z = lat["yz"][:, 1]
    y = lat["yz"][:, 0]
    r = np.sqrt(y * y + z * z)
    windows = {
        "full": np.ones_like(z, dtype=bool),
        "r<=1.5": r <= 1.5,
        "|y|<=0.5": np.abs(y) <= 0.5,
    }

    for label, mask in windows.items():
        z_free, p_mask = centroid(lat, free_final, mask)
        print(f"WINDOW {label}  p_free={p_mask:.3e}")
        for z_mass in z_mass_values:
            m_data: list[float] = []
            g_data: list[float] = []
            for s in strengths:
                field = make_field_layers(lat, z_mass, s)
                final = propagate_field(lat, field, lat["default_open"], K)
                z_m, _ = centroid(lat, final, mask)
                if z_m is None or z_free is None:
                    continue
                delta = z_m - z_free
                if delta > 0:
                    m_data.append(s)
                    g_data.append(delta)
            alpha = fit_power(m_data, g_data)
            if alpha is None:
                print(f"  z={z_mass:>3.1f}: count={len(m_data)} alpha=n/a")
            else:
                print(
                    f"  z={z_mass:>3.1f}: count={len(m_data)} alpha={alpha:.3f} "
                    f"delta_max={max(g_data):.6f}"
                )
        print()


if __name__ == "__main__":
    main()
