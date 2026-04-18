#!/usr/bin/env python3
"""
Audit how much of the current Wilson-parent story is actually safe to trust
for the DM Wilson-to-dW_e^H route.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def parent_completion_witness() -> tuple[float, float, float, float]:
    """
    Show that the same compressed source block can sit inside different positive
    parent completions. This does not disprove a canonical parent theorem; it
    only audits why an arbitrary witness completion is not itself canonical.
    """

    t_src = np.array(
        [
            [2.1, 0.25],
            [0.25, 1.8],
        ],
        dtype=float,
    )
    parent_a = np.block(
        [
            [t_src, np.zeros((2, 1), dtype=float)],
            [np.zeros((1, 2), dtype=float), np.array([[2.6]], dtype=float)],
        ]
    )
    parent_b = np.block(
        [
            [t_src, np.array([[0.05], [0.04]], dtype=float)],
            [np.array([[0.05, 0.04]], dtype=float), np.array([[2.4]], dtype=float)],
        ]
    )
    p = np.diag([1.0, 1.0, 0.0])
    comp_a = p @ parent_a @ p
    comp_b = p @ parent_b @ p
    comp_err = max(
        float(np.max(np.abs(comp_a[:2, :2] - t_src))),
        float(np.max(np.abs(comp_b[:2, :2] - t_src))),
    )
    diff = float(np.max(np.abs(parent_a - parent_b)))
    min_eval_a = float(np.min(np.linalg.eigvalsh(parent_a)))
    min_eval_b = float(np.min(np.linalg.eigvalsh(parent_b)))
    return comp_err, diff, min_eval_a, min_eval_b


def main() -> int:
    print("=" * 88)
    print("DM WILSON PARENT CORRECTNESS AUDIT")
    print("=" * 88)

    transfer = read("docs/GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md")
    strong_cp = read("docs/STRONG_CP_THETA_ZERO_NOTE.md")
    factor = read("docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md")
    factor_script = read("scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py")
    underdet = read("docs/GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    support = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    current_bank = read("docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md")
    model_note = read("docs/DM_WILSON_TO_DWEH_STRUCTURED_MODEL_REALIZATION_THEOREM_NOTE_2026-04-18.md")
    model_script = read("scripts/frontier_dm_wilson_to_dweh_structured_model_realization_theorem_2026_04_18.py")

    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT REPO USES DIFFERENT PARENT-LEVEL FORMULAS")
    print("=" * 88)
    check(
        "The plaquette transfer note uses a gauge-side transfer parent",
        "`Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]`" in transfer
        and "gauge-invariant spatial Hilbert space" in transfer,
    )
    check(
        "The strong-CP note uses the determinant-dressed retained partition",
        "Z = ∫ DU det(D[U] + m) e^{-S_Wilson[U]}" in strong_cp
        and "S_eff[U] = S_Wilson[U] - ln det(D[U] + m)" in strong_cp,
    )
    check(
        "So the current notes do not yet present one theorem-grade identical parent formula across those two sectors",
        "det(D[U] + m)" not in transfer and "Tr[T_(L_s,beta)^(L_t)]" not in strong_cp,
        "gauge transfer parent and retained fermion-weighted partition are still written as different objects",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE GAUGE-SIDE FRAMEWORK-POINT DATA ARE STILL UNDERDETERMINED")
    print("=" * 88)
    check(
        "The transfer-operator note explicitly leaves framework-point transfer-state identification open",
        "explicit transfer-state identification at `beta = 6` still open" in transfer,
    )
    check(
        "The source-sector factorization note and script explicitly use a generic witness rather than the Wilson D_6 data",
        "generic positive-diagonal witness" in factor
        and "not an explicit Wilson `D_6` evaluation" in factor
        and "generic positive conjugation-symmetric diagonal witness" in factor_script
        and "does not evaluate the Wilson\nresidual diagonal D_6" in factor_script,
    )
    check(
        "The Perron/Jacobi note says even the sharpened factorized class still does not force unique framework-point data",
        "symmetry-reduced Jacobi coefficients at `beta = 6`" in underdet
        and "unique Perron moment sequence at `beta = 6`" in underdet
        and "distinct admissible" in underdet
        and "distinct Perron moments" in underdet,
    )

    print("\n" + "=" * 88)
    print("PART 3: POSITIVE REALIZATION EXISTS, BUT ONLY AT MODEL/WITNESS LEVEL")
    print("=" * 88)
    check(
        "The structured DM note explicitly separates positive model realization from Wilson-native derivation",
        "class is positively realizable for arbitrary Hermitian target `H_e`" in model_note
        and "does **not** derive `D_model` from the current-bank Wilson parent" in model_note
        and "remaining open problem is Wilson-native realization" in model_note,
    )
    check(
        "The structured model script itself says it proves constructive realization rather than the final Wilson-native bridge",
        "it proves nonempty constructive realization, not the final Wilson-native bridge" in model_script
        and "derive a current-bank Wilson parent whose compression matches the model class" in model_script,
    )

    print("\n" + "=" * 88)
    print("PART 4: THE LOAD-BEARING MISSING MAP IS STILL WILSON TO CHARGED HERMITIAN DATA")
    print("=" * 88)
    check(
        "The observable principle remains scalar and requires microscopic D plus a source path",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        and "∂W/∂j_x = Re Tr[(D+J)^(-1) P_x]" in observable,
    )
    check(
        "The support intertwiner is explicitly support-only rather than a parent-to-charged descendant theorem",
        "Its safe role is narrower" in support
        and "taste-cube operator algebra" in support
        and "restricted support" in support,
    )
    check(
        "The current-bank boundary note still says there is no Wilson-to-dW_e^H descendant law on current main",
        "does **not** already have" in current_bank
        and "a Wilson-to-`dW_e^H` descendant theorem" in current_bank
        and "or a Wilson-side Hermitian source family" in current_bank,
    )

    print("\n" + "=" * 88)
    print("PART 5: A WITNESS COMPLETION IS NOT A CANONICAL PARENT IDENTIFICATION")
    print("=" * 88)
    comp_err, diff, min_eval_a, min_eval_b = parent_completion_witness()
    check(
        "Two different positive parent completions can share the same compressed source block",
        comp_err < 1.0e-12 and diff > 1.0e-3 and min_eval_a > 0.0 and min_eval_b > 0.0,
        f"compression_err={comp_err:.2e}, parent_diff={diff:.2e}, min_eigs=({min_eval_a:.3f},{min_eval_b:.3f})",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
