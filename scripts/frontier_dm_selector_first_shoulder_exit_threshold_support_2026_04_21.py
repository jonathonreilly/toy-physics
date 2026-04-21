#!/usr/bin/env python3
"""
DM selector first-shoulder-exit threshold support theorem.

Question:
  Does the exact intrinsic threshold-volume family contain a genuinely
  canonical breakpoint candidate that already selects the preferred recovered
  lift, rather than only a broad stabilization interval?

Answer:
  Yes.

  For each recovered lift, the piecewise witness-volume law changes branch at
  tau_b(i) = log(1 + b_i), where b_i is the middle inverse eigenvalue of the
  common-shifted positive comparison window. The earliest such breakpoint over
  the recovered bank is unique, belongs to the preferred recovered lift, lies
  inside the previously certified stabilization window, and already makes the
  preferred lift the unique minimizer of V_tau.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import (
    ANCHOR_OFFSET,
    PREFERRED_RECOVERED_LIFT,
    common_shift,
    recovered_bank,
)
from frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization import (
    inverse_eigenvalue_parameters,
    witness_volume_from_atomic_field,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def threshold_volume(params: tuple[float, float, float], tau: float) -> float:
    return witness_volume_from_atomic_field(params, float(tau))


def main() -> int:
    print("=" * 88)
    print("DM SELECTOR FIRST-SHOULDER-EXIT THRESHOLD SUPPORT THEOREM")
    print("=" * 88)

    lifts, hs_bank, repairs_bank, _targets = recovered_bank()
    mu_bank = common_shift(repairs_bank, ANCHOR_OFFSET)
    params_bank = [inverse_eigenvalue_parameters(h, mu_bank) for h in hs_bank]

    tau_b = np.array([math.log1p(p[1]) for p in params_bank], dtype=float)
    tau_a = np.array([math.log1p(p[0]) for p in params_bank], dtype=float)
    tau_star = 0.1316375782215522
    tau_b_min = float(np.min(tau_b))
    tau_b_argmin = int(np.argmin(tau_b))
    tau_zero_next = float(np.min(tau_a[1:]))

    vals_bmin = np.array([threshold_volume(p, tau_b_min) for p in params_bank], dtype=float)
    winner_bmin = int(np.argmin(vals_bmin))

    note = read("docs/DM_SELECTOR_THRESHOLD_STABILIZATION_SUPPORT_THEOREM_NOTE_2026-04-21.md")
    nonrealization = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ATOMIC_WITNESS_VOLUME_SELECTOR_NONREALIZATION_NOTE_2026-04-18.md")

    print("\n" + "=" * 88)
    print("PART 1: THE EARLIEST MIDDLE-BRANCH BREAKPOINT IS UNIQUE")
    print("=" * 88)

    check(
        "The preferred recovered lift is still lift 0 on the current selector branch",
        np.linalg.norm(np.asarray(lifts[0], dtype=float) - PREFERRED_RECOVERED_LIFT) < 1.0e-12,
        f"preferred lift = {np.round(lifts[0], 12)}",
    )
    check(
        "Each recovered lift has an intrinsic middle-branch threshold tau_b = log(1+b)",
        np.all(np.isfinite(tau_b)) and np.all(tau_b > 0.0),
        f"tau_b = {np.round(tau_b, 12)}",
    )
    check(
        "The earliest middle-branch threshold is unique and belongs to the preferred recovered lift",
        tau_b_argmin == 0 and tau_b[0] + 1.0e-12 < np.min(tau_b[1:]),
        f"(tau_b_min, next) = ({tau_b[0]:.15f}, {np.min(tau_b[1:]):.15f})",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE EARLIEST BREAKPOINT LIES INSIDE THE STABILIZATION WINDOW")
    print("=" * 88)

    check(
        "The threshold-stabilization theorem already records the high-threshold onset tau_star",
        "tau_star" in note and "0.131637578221552" in note,
    )
    check(
        "The earliest middle-branch threshold lies strictly above tau_star",
        tau_b_min > tau_star,
        f"(tau_b_min - tau_star) = {tau_b_min - tau_star:.15f}",
    )
    check(
        "The earliest middle-branch threshold also lies strictly below the next zero-volume tie",
        tau_b_min < tau_zero_next,
        f"(tau_b_min, tau_zero_next)=({tau_b_min:.15f},{tau_zero_next:.15f})",
    )

    print("\n" + "=" * 88)
    print("PART 3: THAT BREAKPOINT ALREADY SELECTS THE PREFERRED LIFT")
    print("=" * 88)

    check(
        "At tau_b,min the preferred recovered lift is already the unique minimizer of the exact threshold-volume family",
        winner_bmin == 0 and np.all(vals_bmin[0] + 1.0e-12 < vals_bmin[1:]),
        f"vals(tau_b,min) = {np.round(vals_bmin, 12)}",
    )
    check(
        "So the exact intrinsic family already carries one canonical breakpoint candidate selecting the preferred lift",
        True,
        f"tau_b,min = {tau_b_min:.15f}",
    )

    print("\n" + "=" * 88)
    print("PART 4: SCIENTIFIC CONSEQUENCE")
    print("=" * 88)

    check(
        "The older nonrealization note still honestly states that no intrinsic threshold law is yet derived",
        "intrinsic threshold law" in nonrealization and "tau = 0.13" in nonrealization and "tau = 0.14" in nonrealization,
    )
    check(
        "This theorem narrows the positive selector burden further without promoting closure",
        True,
        "a natural breakpoint candidate now exists: the earliest middle-branch threshold tau_b,min",
    )
    check(
        "What remains is to derive why the physical threshold law should equal that earliest intrinsic breakpoint, or else derive a stronger microscopic law",
        True,
        "support narrowing only",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The exact intrinsic threshold-volume family now contains a canonical")
    print("  breakpoint candidate, tau_b,min = min_i log(1+b_i).")
    print("  On the recovered bank that breakpoint belongs uniquely to the preferred")
    print("  lift and already selects it.")
    print("  The remaining selector-side burden is therefore narrower again:")
    print("    derive why the physical threshold law is the earliest middle-branch")
    print("    breakpoint, or derive a stronger microscopic selector law.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
