#!/usr/bin/env python3
"""Audit the Planck spacetime/time-lock lane honestly.

This lane tests whether the derived single-clock 3+1 lift fixes the absolute
Planck scale or only the relative space/time unit map. The sharpened result is:

  - the exact scalar 3+1 ratio fixes the anisotropy parameter
      beta = (c a_t / a_s)^2
    to beta = 1;
  - therefore the physical spacetime unit map is locked by
      a_s = c a_t;
  - but all currently retained spacetime observables remain homogeneous under
    the common rescaling a_s -> lambda a_s, a_t -> lambda a_t;
  - so derived time kills anisotropy, not the final absolute scale ray.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
TIME = ROOT / "docs/ANOMALY_FORCES_TIME_THEOREM.md"
RATIO = ROOT / "docs/SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md"
TENSOR = ROOT / "docs/S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"
GLOBAL = ROOT / "docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md"
SCALE_RAY = ROOT / "docs/PLANCK_SCALE_GRAVITY_ACTION_SCALE_RAY_NO_GO_THEOREM_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def apbc_frequencies(lt: int) -> np.ndarray:
    n = np.arange(lt, dtype=float)
    return 2.0 * math.pi * (n + 0.5) / lt


def a2_beta(beta: float) -> float:
    return 1.0 / (2.0 * (3.0 + beta))


def ainf_beta(beta: float) -> float:
    return 1.0 / (2.0 * math.sqrt(3.0 * (3.0 + beta)))


def ratio_beta(beta: float) -> float:
    return math.sqrt((3.0 + beta) / 3.0)


def direct_a_lt(beta: float, lt: int) -> float:
    omega = apbc_frequencies(lt)
    return float(np.mean(1.0 / (3.0 + beta * np.sin(omega) ** 2)) / 2.0)


def inferred_beta_from_ratio(ratio: float) -> float:
    return 3.0 * ratio * ratio - 3.0


def main() -> int:
    note = normalized(NOTE)
    time_note = normalized(TIME)
    ratio_note = normalized(RATIO)
    tensor_note = normalized(TENSOR)
    global_note = normalized(GLOBAL)
    scale_ray_note = normalized(SCALE_RAY)

    n_pass = 0
    n_fail = 0

    print("Planck spacetime/time-lock unit-map lane audit")
    print("=" * 78)

    section("PART 1: SOURCE-BOUNDARY EVIDENCE")
    p = check(
        "anomaly note still derives exactly one time direction",
        "single-clock codimension-1 evolution excludes d_t > 1" in time_note
        and "=> d_t = 1 uniquely" in time_note,
        "the lane starts from a derived one-clock 3+1 spacetime, not an assumed time axis",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "scalar note still fixes the exact 3+1 endpoint ratio 2/sqrt(3)",
        "a_inf / a_2 = 2 / sqrt(3)" in ratio_note,
        "the time-lock argument uses the retained exact scalar ratio rather than a new fit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "tensor/global notes still provide a Lorentzian 3+1 spacetime carrier",
        "exact route-2 spacetime carrier" in tensor_note
        and "global lorentzian einstein/regge stationary action family" in global_note,
        "the lock is interpreted on the accepted 3+1 spacetime side, not just a toy kernel",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "existing Planck no-go still says the current family fixes only a scale ray",
        "fixes a scale ray, not an absolute scale anchor" in scale_ray_note,
        "the time-lock lane must improve on that honestly rather than overwrite it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: ANISOTROPIC 3+1 BRIDGE FAMILY")
    betas = [0.25, 1.0, 4.0]
    for beta in betas:
        a2_direct = direct_a_lt(beta, 2)
        a2_exact = a2_beta(beta)
        ainf_exact = ainf_beta(beta)
        ratio_direct = ainf_exact / a2_exact
        ratio_exact = ratio_beta(beta)
        print(
            f"  beta={beta:>4.2f}  "
            f"A_2(direct)={a2_direct:.15f}  "
            f"A_2(exact)={a2_exact:.15f}  "
            f"R(beta)={ratio_exact:.15f}"
        )
        p = check(
            f"A_2 formula holds at beta={beta:g}",
            abs(a2_direct - a2_exact) < 1.0e-15,
            "the anisotropic minimal-block endpoint is exact",
        )
        n_pass += int(p)
        n_fail += int(not p)
        p = check(
            f"ratio formula holds at beta={beta:g}",
            abs(ratio_direct - ratio_exact) < 1.0e-15,
            "R(beta) = sqrt((3+beta)/3) on the anisotropic same-surface family",
        )
        n_pass += int(p)
        n_fail += int(not p)

    section("PART 3: EXACT TIME-LOCK")
    retained_ratio = 2.0 / math.sqrt(3.0)
    beta_star = inferred_beta_from_ratio(retained_ratio)
    p = check(
        "retained exact scalar ratio forces beta = 1",
        abs(beta_star - 1.0) < 1.0e-15,
        "the exact 3+1 bridge collapses the anisotropy parameter to the isotropic time-lock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    c = 2.99792458e8
    a_s = 1.0
    a_t = a_s / c
    beta_lock = (c * a_t / a_s) ** 2
    p = check(
        "beta = 1 is exactly the spacetime lock a_s = c a_t",
        abs(beta_lock - 1.0) < 1.0e-15,
        "derived time fixes only the relative space/time calibration",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: COMMON-RAY NO-GO AFTER THE LOCK")
    lambdas = [0.25, 0.5, 1.0, 2.0, 4.0]
    x_lat = 7.0
    tau_lat = 5.0
    omega_min_lat = math.pi / 2.0
    g_lat = 1.0 / (4.0 * math.pi)
    vol4_lat = 80.0
    curv_lat = 0.03

    speed_values = []
    causal_values = []
    action_values = []
    freq_values = []

    print("  lambda      x/t ratio            ds^2               S_EH         omega_min")
    for lam in lambdas:
        a = lam
        x_phys = a * x_lat
        t_phys = a * tau_lat / c
        speed = x_phys / t_phys
        ds2 = -(c * t_phys) ** 2 + x_phys**2
        g_phys = (a**2) * g_lat
        vol4_phys = (a**4) * vol4_lat
        curv_phys = curv_lat / (a**2)
        s_eh = (vol4_phys * curv_phys) / (16.0 * math.pi * g_phys)
        omega_min_phys = c * omega_min_lat / a

        speed_values.append(speed)
        causal_values.append(ds2 / (a**2))
        action_values.append(s_eh)
        freq_values.append(omega_min_phys * a / c)

        print(
            f"  {lam:>6.2f}  {speed:>14.8e}  {ds2:>16.8f}  "
            f"{s_eh:>12.8f}  {omega_min_phys:>12.8e}"
        )

    p = check(
        "time-lock makes the causal speed ratio independent of the common scale",
        max(abs(x - speed_values[0]) for x in speed_values) < 1.0e-6,
        "once a_s = c a_t, velocity ratios live on the common spacetime ray",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Lorentzian interval class is unchanged along the common spacetime ray",
        max(abs(x - causal_values[0]) for x in causal_values) < 1.0e-12,
        "ds^2 rescales by lambda^2, so sign/nullness/causal class are invariant",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Einstein-Hilbert-style action remains invariant after time-lock",
        max(abs(x - action_values[0]) for x in action_values) < 1.0e-12,
        "derived time does not break the earlier scale-ray homogeneity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "minimal APBC temporal frequency is exact only in lattice units",
        max(abs(x - freq_values[0]) for x in freq_values) < 1.0e-15
        and abs(freq_values[0] - omega_min_lat) < 1.0e-15,
        "omega_min,phys ~ c/a, so it rescales and cannot anchor the common a",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE VERDICT")
    p = check(
        "note states time-lock without absolute scale closure",
        "time-lock: yes" in note and "time-alone planck derivation: no" in note,
        "the lane must record both the gain and the obstruction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note identifies beta = (c a_t / a_s)^2 and proves beta = 1",
        "beta := (c a_t / a_s)^2" in note and "=> beta = 1" in note,
        "the exact retained ratio must do the actual locking work",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "note states the surviving open target correctly",
        "absolute anchor for the common spacetime ray" in note,
        "after this lane, the remaining problem is one common absolute unit, not separate length/time minima",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Derived single-clock time does matter: it collapses the relative "
        "space/time calibration to the exact lock a_s = c a_t. But the locked "
        "spacetime pair still lives on one common positive scale ray, so time "
        "alone does not derive exact Planck. It turns two unit questions into one."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
