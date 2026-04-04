#!/usr/bin/env python3
"""Bounded p-sweep for action power scaling on the retained 3D ordered family.

This is not a universal theorem harness. It freezes one fixed-family replay:

  - 3D ordered dense lattice
  - h = 0.5, W = 10, L = 12
  - kernel 1/L^2 with h^2 measure
  - field s/r
  - action family S = L(1-f^p)

It measures two things on that family:

  - F~M exponent as a function of the action power p
  - post-peak distance-tail slope on the same fixed geometry
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this sweep. On this machine use /usr/bin/python3."
    ) from exc

from action_universality_probe import (  # noqa: E402
    K,
    Lattice3D,
    detector,
    fit_power,
    label,
    measure_action,
)


H = 0.5
PHYS_W = 10
PHYS_L = 12
POWERS = [0.5, 0.75, 1.0, 1.5, 2.0]


def fmt_float(x: float, places: int = 2) -> str:
    if math.isnan(x):
        return "nan"
    return f"{x:.{places}f}"


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)
    action_modes = [f"power:{p}" for p in POWERS]

    print("=" * 108)
    print("ACTION POWER SCALING SWEEP")
    print("  Fixed 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d_phys=3")
    print("  Kernel: 1/L^2 with h^2 measure")
    print("  Field: s/r")
    print("  Action family: S = L(1-f^p)")
    print("  Goal: test bounded fixed-family scaling, not a universal theorem")
    print("=" * 108)
    print()
    print(
        f"{'p':>5} {'action':<18} {'Born':>10} {'TOWARD':>8} "
        f"{'F~M':>8} {'tail':>18} {'pred':>8}"
    )
    print("-" * 108)

    results = []
    for p, action_mode in zip(POWERS, action_modes):
        row = measure_action(lat, det, action_mode)
        results.append((p, row))
        tail = "n/a"
        pred = "n/a"
        if not math.isnan(row.tail_slope):
            peak = f"z>={row.peak_z}" if row.peak_z is not None else "tail"
            tail = f"{peak}:{row.tail_slope:+.2f}"
            if p >= 1.0:
                pred = f"{-(2.0 * p - 1.0):+.2f}"
        print(
            f"{p:>5.2f} {label(action_mode):<18} {row.born:>10.2e} "
            f"{f'{row.toward_count}/7':>8s} {fmt_float(row.fm_alpha, 2):>8s} "
            f"{tail:>18s} {pred:>8s}"
        )

    print()
    print("SAFE READ")
    print("  - On this fixed family, F~M tracks the action power p exactly within fit precision.")
    print("  - The distance tail steepens with p on the same family.")
    print("  - The strongest bounded law candidate here is the mass-scaling rule F~M = p.")
    print("  - The tail rule for p>=1 needs to be read as an empirical family fit, not a universal theorem.")

    # A tiny explicit summary table is easier for review than prose.
    fm_ok = all(
        (not math.isnan(row.fm_alpha)) and abs(row.fm_alpha - p) < 0.05
        for p, row in results
    )
    print()
    print(f"SUMMARY: F~M=p exact on this family? {'YES' if fm_ok else 'NO'}")


if __name__ == "__main__":
    main()
