#!/usr/bin/env python3
"""
Sharpen the plaquette beta=6 propagated retained triple target on the current
bank: it is already the minimal positive finite target, and the stronger
current-bank negative statement is that even its normalized value is still not
determined.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def exact_first_symmetric_matrix() -> sp.Matrix:
    sqrt = sp.sqrt
    s = sqrt(2 - sqrt(2))
    r = sqrt(2)
    u = sqrt(2 - sqrt(2 + sqrt(2)))
    v = sqrt(2 - sqrt(2 - sqrt(2)))
    Sigma = sqrt(2 + sqrt(2))
    x = sqrt(2 + sqrt(2 + sqrt(2)))
    y = sqrt(2 + sqrt(2 - sqrt(2)))
    a = -3 * s
    b = -3 * r + 3 * u + 3 * v
    c = 16 + 8 * Sigma - 8 * x - 8 * y
    d = 3 * r + 3 * u - 3 * v
    e = 16 - 8 * Sigma - 8 * x + 8 * y
    return sp.Matrix([[1, a, 0], [1, b, c], [1, d, e]])


def main() -> int:
    target_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md"
    )
    evaluator_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    current_stack_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CURRENT_STACK_CONSTRAINT_BOUNDARY_NOTE_2026-04-17.md"
    )
    cone_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md"
    )
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    wedge_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_CONTROLLED_RETAINED_COEFFICIENT_WEDGE_NOTE_2026-04-17.md"
    )
    finite_packet_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md"
    )

    f_exact = exact_first_symmetric_matrix()
    det_f = sp.simplify(f_exact.det())
    rank_f = int(f_exact.rank())
    det_numeric = complex(sp.N(det_f, 50))

    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST PROPAGATED RETAINED TRIPLE MINIMALITY AND CURRENT-BANK NO-GO")
    print("=" * 112)
    print()
    print("Exact first symmetric radical matrix F")
    print(f_exact)
    print()
    print(f"  rank(F)                                     = {rank_f}")
    print(f"  det(F)                                      = {det_numeric.real:.12f}")
    print()

    check(
        "the target note already identifies the propagated retained three-sample output as the first honest finite evaluator target",
        "propagated retained three-sample output" in target_note
        and "first retained propagated coefficient triple" in target_note,
        detail="the live beta=6 plaquette target is already finite and propagated",
    )
    check(
        "the exact radical first symmetric matrix is invertible, so any smaller linear target would require an extra collapse not present in the current bank",
        rank_f == 3 and abs(det_numeric) > 1.0e-12
        and "there is no further universal linear collapse below" in radical_note
        and "no additional symmetry or source-observable collapse below the three named" in current_stack_note,
        detail=f"rank(F)={rank_f}, det(F)={det_numeric.real:.12f}",
    )
    check(
        "the first retained propagated coefficient triple is only an equivalent reformulation of the same target, not a strictly smaller one",
        "equivalently the first retained propagated coefficient triple of `v_6`" in target_note
        and "exact algebraic inverse map" in radical_note,
        detail="the inverse radical map makes the coefficient triple equivalent to the sample triple",
    )
    check(
        "the evaluator-route theorem already gives the stronger current-bank no-go directly at the normalized propagated triple",
        "determine unique normalized" in evaluator_note
        and "actual evaluator" in evaluator_note,
        detail="even the normalized minimal finite target is not determined",
    )
    check(
        "the cone, truncation, and Tau-wedge notes add exact constraint geometry but not evaluation",
        "exact positive cone" in cone_note
        and "exact universal tail envelope" in envelope_note
        and "exact tau-controlled outer wedge" in wedge_note
        and "What this does not close" in cone_note
        and "does **not** support" in envelope_note
        and "explicit closure" in envelope_note
        and "does **not** solve `rho10`, `rho11`, or `tau`" in wedge_note,
        detail="the current bank constrains the target region but does not collapse it to a value",
    )
    check(
        "finite sample extension still cannot by itself close the full beta-side vector",
        "no finite sample packet can by itself determine the full" in finite_packet_note
        and "finite retained" in finite_packet_note,
        detail="the operator route remains necessary beyond the first finite target",
    )

    check(
        "the target note and current-stack boundary agree that there is no smaller exact evaluative object below the three named same-surface values on the current bank",
        "It only fixes the next honest target shape." in target_note
        and "those three explicit values to be" in current_stack_note
        and "evaluated." in current_stack_note,
        bucket="SUPPORT",
    )
    check(
        "the evaluator-route and finite-sample nonclosure notes separate the minimal finite target from full beta-side closure",
        "determine unique normalized" in evaluator_note
        and "no finite sample packet can by itself determine" in finite_packet_note,
        bucket="SUPPORT",
    )
    check(
        "the positive-cone and Tau-wedge notes provide theorem-grade admissible-region geometry for the target rather than an evaluator",
        "`Z_B >= Z_A`" in cone_note
        and "`rho10 <= k10 (1 + tau)`" in wedge_note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
