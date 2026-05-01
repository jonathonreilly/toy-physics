#!/usr/bin/env python3
"""Validate corrected staggered Dirac dispersion v_max formula.

For the 1+1d staggered Dirac dispersion E^2 = m^2 + sin^2(k), the maximum
group velocity over k at fixed m is

    v_max(m) = sqrt(m^2 + 1) - m.

This script:
  - Numerically maximizes v_g(k, m) over a fine k grid for several m.
  - Compares against the closed-form v_max(m) = sqrt(m^2 + 1) - m.
  - Confirms v_max < 1 strictly for m > 0 and v_max -> 1 as m -> 0.
  - Confirms the maximum is at k* -> 0 in the massless limit (NOT k = pi/2,
    where cos(k) = 0 and v_g = 0).
  - Reports PASS=N FAIL=N counts in the format consumed by the
    audit-lane runner classifier.

The note this validates is docs/LIGHT_CONE_FRAMING_NOTE.md (claim_id
light_cone_framing_note).
"""
from __future__ import annotations

import math

import numpy as np


MASSES = (0.0, 1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1.0, 2.0)
KGRID_N = 200_001
TOL_VMAX = 1e-6


def v_g(k: np.ndarray, m: float) -> np.ndarray:
    """Group velocity dE/dk for E^2 = m^2 + sin^2(k)."""
    E = np.sqrt(m * m + np.sin(k) ** 2)
    # avoid 0/0 at k=0 when m=0: |sin(k)cos(k)|/E = |cos(k)| in that limit
    safe_E = np.where(E > 0.0, E, 1.0)
    val = np.abs(np.sin(k) * np.cos(k)) / safe_E
    if m == 0.0:
        # at k = 0, E = 0 and v_g -> |cos(0)| = 1 (linear dispersion limit)
        val = np.where(E > 0.0, val, 1.0)
    return val


def v_max_closed_form(m: float) -> float:
    return math.sqrt(m * m + 1.0) - m


def main() -> int:
    ks = np.linspace(0.0, math.pi, KGRID_N)

    print("=" * 78)
    print("LIGHT CONE FRAMING — staggered Dirac dispersion v_max validation")
    print("=" * 78)
    print()
    print("Dispersion: E^2 = m^2 + sin^2(k)")
    print("Group velocity: v_g(k, m) = sin(k) cos(k) / E")
    print("Closed-form max: v_max(m) = sqrt(m^2 + 1) - m")
    print()
    print(f"{'m':>10s}  {'v_max(num)':>14s}  {'v_max(pred)':>14s}  "
          f"{'|diff|':>10s}  {'k_argmax':>10s}  status")
    print("-" * 78)

    passes = 0
    fails = 0

    for m in MASSES:
        v = v_g(ks, m)
        vmax_num = float(v.max())
        k_argmax = float(ks[int(v.argmax())])
        vmax_pred = v_max_closed_form(m)
        diff = abs(vmax_num - vmax_pred)

        # CHECK 1: closed-form matches numerical max to ~1e-6
        match_ok = diff < TOL_VMAX
        # CHECK 2: subluminal for m > 0
        sub_ok = (vmax_num < 1.0 + 1e-12) and (m == 0.0 or vmax_num < 1.0)
        # CHECK 3: massless max not at k = pi/2 (where cos = 0)
        not_pi_over_2_ok = (m > 0.0) or (k_argmax < math.pi / 2 - 0.1)

        all_ok = match_ok and sub_ok and not_pi_over_2_ok
        status = "PASS" if all_ok else "FAIL"
        if all_ok:
            passes += 3
        else:
            passes += int(match_ok) + int(sub_ok) + int(not_pi_over_2_ok)
            fails += (3 - (int(match_ok) + int(sub_ok) + int(not_pi_over_2_ok)))

        print(f"{m:10.5f}  {vmax_num:14.10f}  {vmax_pred:14.10f}  "
              f"{diff:10.2e}  {k_argmax:10.6f}  {status}")

    print()
    print("Limit checks:")
    # For m -> 0, v_max -> 1
    vmax_at_smallm = v_max_closed_form(1e-6)
    if abs(vmax_at_smallm - 1.0) < 1e-5:
        passes += 1
        print(f"  v_max(m=1e-6) = {vmax_at_smallm:.10f} -> 1  PASS")
    else:
        fails += 1
        print(f"  v_max(m=1e-6) = {vmax_at_smallm:.10f}  FAIL")
    # For m large, v_max -> 1/(2m)
    vmax_at_largem = v_max_closed_form(100.0)
    expected_largem = 1.0 / (2 * 100.0)
    if abs(vmax_at_largem - expected_largem) / expected_largem < 1e-3:
        passes += 1
        print(f"  v_max(m=100) = {vmax_at_largem:.6e} ~ 1/(2m) = {expected_largem:.6e}  PASS")
    else:
        fails += 1
        print(f"  v_max(m=100) = {vmax_at_largem:.6e}  FAIL")

    print()
    print(f"PASS={passes} FAIL={fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
