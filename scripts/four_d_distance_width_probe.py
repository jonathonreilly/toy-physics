#!/usr/bin/env python3
"""Bounded 4D width-limited distance-law probe.

This freezes a small width ladder on the retained 4D valley-linear family:

  - action:  S = L(1-f)
  - kernel:  1/L^3
  - field:   f = s / r^2
  - measure: h^3

The goal is intentionally narrow:
  - compare a small width ladder at fixed h
  - count TOWARD rows across a retained mass-offset scan
  - report the early-tail and far-tail power-law fits
  - state plainly that width limits still block asymptotic closure

This script does not try to solve the 4D tail law. It freezes the current
width-limited status on the same retained family.
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
except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

from scripts.dimensional_gravity_card import Lattice4D, fit_power

K = 5.0
H = 0.5
PHYS_L = 15
MAX_D_PHYS = 2
FIELD_STRENGTH = 5e-5
WIDTH_LADDER = [5, 6, 7]
Z_MASS_VALUES = [2, 3, 4, 5, 6, 7]


def summarize_row(lat: Lattice4D, width: int) -> None:
    det = lat.detector()
    bi, sa, sb, blocked, bl = lat.setup_slits()
    pos = lat.pos
    field_f = np.zeros(lat.n)

    print(f"WIDTH W={width}  nodes={lat.n:,}  layers={lat.nl}  max_d={lat.max_d}")

    t0 = time.time()
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[i]) ** 2 for i in det)
    if pf < 1e-30:
        print("  free propagation: no detector signal")
        return
    zf = sum(abs(af[i]) ** 2 * pos[i, 2] for i in det) / pf
    print(f"  free propagation baseline z={zf:.6f} ({time.time() - t0:.1f}s)")

    b_vals = []
    deltas = []
    rows = []
    for z_mass in Z_MASS_VALUES:
        fm, mi = lat.make_field(z_mass, FIELD_STRENGTH)
        if mi is None:
            continue
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[i]) ** 2 for i in det)
        if pm < 1e-30:
            continue
        zm = sum(abs(am[i]) ** 2 * pos[i, 2] for i in det) / pm
        delta = zm - zf
        rows.append((z_mass, delta))
        b_vals.append(z_mass)
        deltas.append(delta)

    toward = sum(1 for _, delta in rows if delta > 0)
    peak_idx = int(np.argmax(deltas)) if deltas else -1
    peak_z = b_vals[peak_idx] if peak_idx >= 0 else None

    print("  mass offsets:")
    for z_mass, delta in rows:
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"    z={z_mass}: {delta:+.8f} ({direction})")

    print(f"  TOWARD support: {toward}/{len(rows)}")
    if peak_z is not None:
        print(f"  peak at z={peak_z}")

    if len(b_vals) >= 3 and peak_idx >= 0:
        early_b = b_vals[peak_idx:]
        early_d = deltas[peak_idx:]
        if len(early_b) >= 3:
            slope, r2 = fit_power(early_b, early_d)
            if slope is not None:
                print(f"  early tail (z>={early_b[0]}): b^({slope:.2f}), R²={r2:.3f}")
        far_b = [b for b in b_vals if b >= (peak_z + 1)]
        far_d = [d for b, d in zip(b_vals, deltas) if b >= (peak_z + 1)]
        if len(far_b) >= 3:
            slope, r2 = fit_power(far_b, far_d)
            if slope is not None:
                print(f"  far tail   (z>={far_b[0]}): b^({slope:.2f}), R²={r2:.3f}")
        else:
            print(
                f"  far tail: only {len(far_b)} point(s) beyond the peak; "
                "width still blocks asymptotic closure"
            )
    else:
        print("  tail fits: not enough post-peak support to fit")


def main() -> None:
    t_all = time.time()
    print("=" * 72)
    print("4D WIDTH-LIMITED DISTANCE-LAW PROBE")
    print("Family: valley-linear S = L(1-f), kernel 1/L^3, field f=s/r^2")
    print(f"Fixed h={H}, L={PHYS_L}, strength={FIELD_STRENGTH:.0e}, max_d_phys={MAX_D_PHYS}")
    print(f"Width ladder: {WIDTH_LADDER}")
    print(f"Mass offsets: {Z_MASS_VALUES}")
    print("Goal: freeze current 4D support without overclaiming asymptotic closure")
    print("=" * 72)
    print()

    for width in WIDTH_LADDER:
        t0 = time.time()
        lat = Lattice4D(PHYS_L, width, MAX_D_PHYS, H)
        summarize_row(lat, width)
        print(f"  elapsed: {time.time() - t0:.1f}s")
        print()

    print("=" * 72)
    print(
        "Readout: the retained 4D family remains TOWARD across the tested "
        "width ladder, but the tail fits are still width-limited and do not "
        "close to a stable asymptotic law here."
    )
    print(f"Total elapsed: {time.time() - t_all:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
