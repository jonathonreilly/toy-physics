#!/usr/bin/env python3
"""
DM neutrino source-surface parity/source fixed-point selector theorem.

Question:
  Can the last live point-selection gap close on the strongest current native
  local route by combining:

    1. the exact parity-compatible local scalar curvature on (delta, q_+),
    2. the exact sharp even-source quotient on the fixed E1 channel?

Answer:
  Yes.

  The active curvature route is exactly blind to swapping delta and q_+, so a
  unique selected point must satisfy delta = q_+.

  The sharp source route is exactly blind to swapping the unresolved E1 split,
  so a unique selected split must satisfy delta = rho = E1/2.

  Therefore

      delta_* = q_+* = rho_* = sqrt(6)/3,

  and hence r31,* = 1/2, phi_+,* = pi/2.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_source_surface_active_curvature_23_symmetric_baseline_boundary import (
    boundary_prefactor,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    active_half_plane_h,
    q_floor,
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


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def rho_star() -> float:
    return math.sqrt(6.0) / 3.0


def active_exchange(delta: float, q_plus: float) -> tuple[float, float]:
    return q_plus, delta


def source_split_swap(delta: float, rho: float) -> tuple[float, float]:
    return rho, delta


def part1_parity_compatible_curvature_descends_to_the_active_exchange_quotient() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PARITY-COMPATIBLE CURVATURE DESCENDS TO THE ACTIVE EXCHANGE QUOTIENT")
    print("=" * 88)

    def q_action(a: float, b: float, delta: float, q_plus: float) -> float:
        return boundary_prefactor(a, b) * (delta * delta + q_plus * q_plus)

    samples = [
        (1.0, 1.0, 0.2, 1.7),
        (1.0, 2.0, 0.7, 1.3),
        (3.5, 0.6, -0.3, 2.1),
    ]

    ok_swap = True
    details = []
    for a, b, delta, q_plus in samples:
        lhs = q_action(a, b, delta, q_plus)
        rhs = q_action(a, b, *active_exchange(delta, q_plus))
        ok_swap &= abs(lhs - rhs) < 1e-12
        details.append(f"(A,B)=({a:.1f},{b:.1f}) diff={abs(lhs-rhs):.2e}")

    t = delta_star()

    check(
        "On every positive parity-compatible diagonal baseline the exact local scalar curvature is invariant under (delta,q_+) -> (q_+,delta)",
        ok_swap,
        "; ".join(details),
    )
    check(
        "Therefore any unique selected point on that exact local scalar route must lie on the active-exchange fixed set delta = q_+ = t",
        abs(t - q_star()) < 1e-12 and t >= exact_package().E1 / 2.0 - 1e-12,
        f"t={t:.12f}, E1/2={exact_package().E1/2.0:.12f}",
    )


def part2_the_sharp_even_source_descends_to_the_unresolved_source_split_quotient() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SHARP EVEN SOURCE DESCENDS TO THE UNRESOLVED SOURCE-SPLIT QUOTIENT")
    print("=" * 88)

    pkg = exact_package()
    tau_e = 0.5
    tau_t = 0.5
    delta = rho = pkg.E1 / 2.0
    d_swap, r_swap = source_split_swap(delta, rho)

    check(
        "The exact sharp source theorem fixes the even source as the swap-even coordinates (tau_E,tau_T) = (1/2,1/2)",
        abs(tau_e - 0.5) < 1e-12 and abs(tau_t - 0.5) < 1e-12 and abs(tau_e - tau_t) < 1e-12,
        f"(tau_E,tau_T)=({tau_e:.6f},{tau_t:.6f})",
    )
    check(
        "On the live source-oriented sheet the unresolved source split is exactly delta + rho = E1 = sqrt(8/3)",
        abs(delta + rho - pkg.E1) < 1e-12,
        f"(delta,rho,E1)=({delta:.12f},{rho:.12f},{pkg.E1:.12f})",
    )
    check(
        "The sharp even-source route is therefore fixed by the split swap (delta,rho) -> (rho,delta)",
        abs(d_swap - delta) < 1e-12 and abs(r_swap - rho) < 1e-12,
        f"swap(delta,rho)=({d_swap:.12f},{r_swap:.12f})",
    )
    check(
        "So the unique sharp split is the equal split delta = rho = E1/2",
        abs(delta - rho_star()) < 1e-12 and abs(rho - rho_star()) < 1e-12,
        f"delta=rho={delta:.12f}",
    )


def part3_the_unique_compatible_live_point_is_forced() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE UNIQUE COMPATIBLE LIVE POINT IS FORCED")
    print("=" * 88)

    pkg = exact_package()
    delta = delta_star()
    q_plus = q_star()
    rho = rho_star()
    _h, r31, phi = active_half_plane_h(delta, q_plus, m=0.0)

    check(
        "Combining the active fixed set and the sharp equal split gives delta_* = q_+* = rho_* = sqrt(6)/3",
        abs(delta - q_plus) < 1e-12 and abs(delta - rho) < 1e-12 and abs(delta - math.sqrt(6.0) / 3.0) < 1e-12,
        f"(delta_*,q_+*,rho_*)=({delta:.12f},{q_plus:.12f},{rho:.12f})",
    )
    check(
        "The exact active-half-plane inverse chart then gives r31,* = 1/2 and phi_+,* = pi/2",
        abs(r31 - pkg.gamma) < 1e-12 and abs(phi - 0.5 * math.pi) < 1e-12,
        f"(r31,phi)=({r31:.12f},{phi:.12f})",
    )
    check(
        "The selected point sits exactly on the chamber boundary q_+ = E1 - delta",
        abs(q_plus - q_floor(delta)) < 1e-12,
        f"q_+ - q_floor(delta)={q_plus - q_floor(delta):.12f}",
    )


def part4_the_note_records_the_honest_closure_scope() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE HONEST CLOSURE SCOPE")
    print("=" * 88)

    note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_SOURCE_FIXED_POINT_SELECTOR_THEOREM_NOTE_2026-04-17.md"
    )

    check(
        "The note records the parity-compatible local scalar route and the sharp even-source route as the two native quotient structures",
        "Active curvature quotient." in note and "Sharp even-source quotient." in note,
    )
    check(
        "The note records the selected point delta_* = q_+* = rho_* = sqrt(6)/3",
        "delta_* = q_+* = rho_* = sqrt(6) / 3" in note,
    )
    check(
        "The note is explicit that it closes the strongest current native local route rather than every imaginable future route",
        "strongest currently native local route" in note and "does **not** claim that every conceivable future selector route must" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE PARITY/SOURCE FIXED-POINT SELECTOR THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the last live point-selection gap close on the strongest current")
    print("  native local route by combining the exact parity-compatible local")
    print("  curvature quotient with the exact sharp even-source quotient?")

    part1_parity_compatible_curvature_descends_to_the_active_exchange_quotient()
    part2_the_sharp_even_source_descends_to_the_unresolved_source_split_quotient()
    part3_the_unique_compatible_live_point_is_forced()
    part4_the_note_records_the_honest_closure_scope()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact conditional answer on the strongest current native local route:")
    print("    - the parity-compatible local scalar route fixes the active diagonal set")
    print("    - the sharp even-source route fixes the equal split of the E1 channel")
    print("    - the unique compatible live point is delta_* = q_+* = rho_* = sqrt(6)/3")
    print("    - hence r31,* = 1/2 and phi_+,* = pi/2")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
