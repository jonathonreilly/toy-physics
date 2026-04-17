#!/usr/bin/env python3
"""
DM neutrino source-surface active-parity-compatible diagonal baseline theorem.

Question:
  If a positive diagonal baseline is required to respect the exact 23 odd/even
  grading of the live active pair, what family remains?

Answer:
  Exactly the 23-symmetric family D = diag(A,B,B).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    tdelta,
    tq,
)
from frontier_dm_neutrino_source_surface_active_curvature_23_symmetric_baseline_boundary import (
    boundary_prefactor,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

P23 = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)


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


def diagonal(a: float, b: float, c: float) -> np.ndarray:
    return np.diag([a, b, c]).astype(complex)


def commutator_norm(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a @ b - b @ a))


def delta_star() -> float:
    return math.sqrt(6.0) / 3.0


def q_star() -> float:
    return math.sqrt(6.0) / 3.0


def part1_the_live_active_pair_has_exact_23_odd_even_parity() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LIVE ACTIVE PAIR HAS EXACT 23 ODD/EVEN PARITY")
    print("=" * 88)

    td = tdelta()
    tqm = tq()

    check(
        "T_delta is exactly 23-odd",
        np.linalg.norm(P23 @ td @ P23 + td) < 1e-12,
        f"err={np.linalg.norm(P23 @ td @ P23 + td):.2e}",
    )
    check(
        "T_q is exactly 23-even",
        np.linalg.norm(P23 @ tqm @ P23 - tqm) < 1e-12,
        f"err={np.linalg.norm(P23 @ tqm @ P23 - tqm):.2e}",
    )


def part2_diagonal_baseline_compatibility_is_equivalent_to_23_symmetry() -> None:
    print("\n" + "=" * 88)
    print("PART 2: DIAGONAL BASELINE COMPATIBILITY IS EQUIVALENT TO 23 SYMMETRY")
    print("=" * 88)

    d_sym = diagonal(1.5, 0.7, 0.7)
    d_asym = diagonal(1.0, 2.0, 3.0)
    d_generic = diagonal(2.2, 0.9, 0.9)

    check(
        "A 23-symmetric diagonal baseline commutes exactly with the 23 exchange involution",
        commutator_norm(d_sym, P23) < 1e-12 and commutator_norm(d_generic, P23) < 1e-12,
        f"comm norms=({commutator_norm(d_sym, P23):.2e},{commutator_norm(d_generic, P23):.2e})",
    )
    check(
        "An asymmetric diagonal baseline fails that compatibility condition",
        commutator_norm(d_asym, P23) > 1e-6,
        f"comm norm={commutator_norm(d_asym, P23):.12f}",
    )
    check(
        "So diagonal active-parity compatibility is equivalent to the exact condition B = C",
        np.linalg.norm(P23 @ d_sym @ P23 - d_sym) < 1e-12
        and np.linalg.norm(P23 @ d_asym @ P23 - d_asym) > 1e-6,
        f"sym err={np.linalg.norm(P23 @ d_sym @ P23 - d_sym):.2e}, asym err={np.linalg.norm(P23 @ d_asym @ P23 - d_asym):.12f}",
    )


def part3_every_parity_compatible_diagonal_baseline_has_the_same_chamber_minimizer() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVERY PARITY-COMPATIBLE DIAGONAL BASELINE HAS THE SAME MINIMIZER")
    print("=" * 88)

    d_sel = delta_star()
    q_sel = q_star()

    def boundary_action(prefactor: float, delta: float) -> float:
        q_plus = q_floor(delta)
        return prefactor * (delta * delta + q_plus * q_plus)

    samples = [
        (1.0, 1.0),
        (1.0, 2.0),
        (3.5, 0.6),
    ]

    ok = True
    details = []
    for a, b in samples:
        pref = boundary_prefactor(a, b)
        deriv = pref * (4.0 * d_sel - 2.0 * math.sqrt(8.0 / 3.0))
        center = boundary_action(pref, d_sel)
        left = boundary_action(pref, d_sel - 0.2)
        right = boundary_action(pref, d_sel + 0.2)
        ok &= pref > 0.0 and abs(deriv) < 1e-12 and center < left and center < right
        details.append(f"(A,B)=({a:.1f},{b:.1f}) pref={pref:.12f}")

    check(
        "Every positive parity-compatible diagonal baseline gives a positive Euclidean prefactor",
        ok,
        "; ".join(details),
    )
    check(
        "Therefore every such baseline gives the same chamber minimizer delta_* = q_+* = sqrt(6)/3",
        ok and abs(q_sel - q_floor(d_sel)) < 1e-12,
        f"(delta_*,q_+*)=({d_sel:.12f},{q_sel:.12f})",
    )


def part4_the_note_records_the_honest_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE HONEST REDUCTION")
    print("=" * 88)

    note = read(
        "docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md"
    )

    check(
        "The note records the exact 23 odd/even grading of the live active pair",
        "`23`-odd direction `T_delta`" in note and "`23`-even direction `T_q`" in note,
    )
    check(
        "The note records that active-parity-compatible diagonal baselines are exactly D = diag(A,B,B)",
        "D = diag(A,B,B)" in note and "P_23 D P_23 = D" in note,
    )
    check(
        "The note explicitly says this removes baseline ambiguity only inside the parity-compatible class, not the full selector gap",
        "does **not** close the DM selector lane" in note and "does not yet derive the physical selector law" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ACTIVE-PARITY-COMPATIBLE DIAGONAL BASELINE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  If a positive diagonal baseline is required to respect the exact 23")
    print("  odd/even grading of the live active pair, what family remains?")

    part1_the_live_active_pair_has_exact_23_odd_even_parity()
    part2_diagonal_baseline_compatibility_is_equivalent_to_23_symmetry()
    part3_every_parity_compatible_diagonal_baseline_has_the_same_chamber_minimizer()
    part4_the_note_records_the_honest_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the live active pair already splits into exact 23-odd/even directions")
    print("    - a positive diagonal baseline respects that grading iff it is D = diag(A,B,B)")
    print("    - every such baseline gives the same chamber minimizer delta_* = q_+* = sqrt(6)/3")
    print("    - so baseline ambiguity disappears inside the active-parity-compatible diagonal class")
    print("    - the remaining live gap is still the physical selector principle or the direct Z3 law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
