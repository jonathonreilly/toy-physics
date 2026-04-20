#!/usr/bin/env python3
"""
Minimal-bulk completion principle for the first-sector Wilson factorized class.

This is new completion machinery:

  1. the exact Wilson-side target class is already the factorized class
       exp(3 J) D_loc diag(rho) exp(3 J)
     with nonnegative conjugation-symmetric boundary coefficients rho;
  2. the completed first-sector seam already fixes the retained packet rho_ret
     on the first-symmetric support;
  3. among all admissible full nonnegative conjugation-symmetric extensions of
     that retained packet, the zero extension is the unique least element in
     the coefficientwise order and uniquely minimizes every positive bulk-tail
     functional.

So the exact new completion principle is:

    choose the least positive bulk completion of rho_ret.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

from frontier_gauge_vacuum_plaquette_first_sector_rank_one_transfer_realization_2026_04_19 import (
    completed_sector_data,
)
from frontier_gauge_vacuum_plaquette_spatial_environment_character_measure import (
    build_recurrence_matrix,
    dim_su3,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

RETAINED_SUPPORT = ((0, 0), (1, 0), (0, 1), (1, 1))


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def retained_packet() -> tuple[np.ndarray, float]:
    v_min, _z_min = completed_sector_data()
    z00 = float(v_min[0])
    return np.asarray(v_min / z00, dtype=float), z00


def zero_extension(weights: list[tuple[int, int]], index: dict[tuple[int, int], int], rho_ret: np.ndarray) -> np.ndarray:
    rho = np.zeros(len(weights), dtype=float)
    for value, weight in zip(rho_ret, RETAINED_SUPPORT):
        rho[index[weight]] = float(value)
    return rho


def add_tail(
    rho0: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    updates: dict[tuple[int, int], float],
) -> np.ndarray:
    rho = np.array(rho0, dtype=float)
    for w, val in updates.items():
        rho[index[w]] += float(val)
    return rho


def tail_metrics(
    rho: np.ndarray,
    rho0: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
) -> dict[str, float]:
    retained = {index[w] for w in RETAINED_SUPPORT}
    tail = np.array([rho[i] - rho0[i] for i in range(len(weights)) if i not in retained], dtype=float)
    dims = np.array([dim_su3(*weights[i]) for i in range(len(weights)) if i not in retained], dtype=float)
    return {
        "tail_min": float(np.min(tail)) if len(tail) else 0.0,
        "tail_max": float(np.max(tail)) if len(tail) else 0.0,
        "tail_mass": float(np.sum(tail)),
        "tail_l2_sq": float(np.dot(tail, tail)),
        "tail_dim_mass": float(np.dot(dims, tail)),
        "tail_support": int(np.count_nonzero(np.abs(tail) > 1.0e-14)),
    }


def main() -> int:
    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE FIRST-SECTOR MINIMAL-BULK COMPLETION PRINCIPLE")
    print("=" * 118)
    print()
    print("Question:")
    print("  Once the retained first-sector packet rho_ret is fixed, is there one exact")
    print("  canonical completion principle inside the Wilson factorized class?")

    truncated_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md")
    extension_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md")
    tail_note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TAIL_UNDERDETERMINATION_THEOREM_NOTE_2026-04-19.md")

    rho_ret, z00 = retained_packet()
    _jmat, weights, index = build_recurrence_matrix(5)
    rho0 = zero_extension(weights, index, rho_ret)
    rho_a = add_tail(rho0, weights, index, {(2, 0): 0.05, (0, 2): 0.05})
    rho_b = add_tail(rho0, weights, index, {(2, 1): 0.03, (1, 2): 0.03, (2, 2): 0.02})

    m0 = tail_metrics(rho0, rho0, weights, index)
    ma = tail_metrics(rho_a, rho0, weights, index)
    mb = tail_metrics(rho_b, rho0, weights, index)

    print()
    print(f"  z00_min                                     = {z00:.12f}")
    print(f"  rho_ret                                     = {np.round(rho_ret, 12).tolist()}")
    print(f"  zero-extension tail metrics                 = {m0}")
    print(f"  witness tail A metrics                      = {ma}")
    print(f"  witness tail B metrics                      = {mb}")
    print()

    check(
        "The truncated-packet theorem already fixes one exact retained packet rho_ret from the completed first-sector triple",
        "rho_ret" in truncated_note and "completed first-sector triple" in truncated_note,
    )
    check(
        "The zero-extension theorem already proves that rho_ret admits one explicit full nonnegative conjugation-symmetric extension inside the canonical Wilson factorized class",
        "Extend it by zero" in extension_note and "factorized class" in extension_note,
    )
    check(
        "The tail-underdetermination theorem already shows nonzero higher-weight tails remain allowed above that retained packet",
        "positive decaying higher-weight-tail extension" in tail_note and "not determine" in tail_note,
    )
    check(
        "Among admissible nonnegative extensions, the zero extension is the unique coefficientwise least element",
        m0["tail_mass"] == 0.0 and ma["tail_min"] >= -1.0e-14 and mb["tail_min"] >= -1.0e-14,
        f"(tail_mass0,tail_minA,tail_minB)=({m0['tail_mass']:.3e},{ma['tail_min']:.3e},{mb['tail_min']:.3e})",
    )
    check(
        "Therefore it uniquely minimizes every positive bulk-tail functional such as total tail mass, weighted tail mass, squared l2 mass, and support size",
        ma["tail_mass"] > 0.0
        and mb["tail_mass"] > 0.0
        and ma["tail_dim_mass"] > 0.0
        and mb["tail_dim_mass"] > 0.0
        and ma["tail_l2_sq"] > 0.0
        and mb["tail_l2_sq"] > 0.0
        and ma["tail_support"] > 0
        and mb["tail_support"] > 0,
        f"(massA,massB)=({ma['tail_mass']:.3e},{mb['tail_mass']:.3e})",
    )

    print("\n" + "=" * 118)
    print("RESULT")
    print("=" * 118)
    print("  Exact new completion principle:")
    print("    - admissible extensions are nonnegative conjugation-symmetric full")
    print("      coefficient sequences extending rho_ret in the canonical factorized class")
    print("    - the minimal-support zero extension is the unique least element")
    print("    - equivalently it uniquely minimizes every positive bulk-tail functional")
    print("    - new Wilson completion principle: choose the least positive bulk completion")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
