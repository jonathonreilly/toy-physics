#!/usr/bin/env python3
"""
Proof-form boundary for future positive step-2A theorems.
"""

from __future__ import annotations

from pathlib import Path


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


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md")
    reduction = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    shape = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md")
    all_paths = read("docs/PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md")
    proof_standard = read("docs/PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md")

    print("=" * 102)
    print("PERRON-FROBENIUS STEP-2 OPERATOR-FORM BOUNDARY")
    print("=" * 102)
    print()

    check(
        "Step-2A reduction note already fixes the target as charged-sector operator/Hermitian data",
        "`Wilson -> D_- -> dW_e^H -> H_e`" in reduction,
        bucket="SUPPORT",
    )
    check(
        "Candidate-shape boundary note already excludes scalar-only and support-only bridge classes",
        "scalar-only and support-only candidate classes" in shape
        and "matrix-valued cross-sector descendant/intertwiner law" in shape,
        bucket="SUPPORT",
    )
    check(
        "All-paths note already assigns Stinespring to step 2 as a compression/intertwiner template",
        "Stinespring" in all_paths
        and "compression / dilation / intertwiner law" in all_paths,
        bucket="SUPPORT",
    )
    check(
        "External-theory proof-standard note already restricts outside theory to hypothesis-template use only",
        "hypothesis template" in proof_standard
        and "plug-in closure" in proof_standard,
        bucket="SUPPORT",
    )

    check(
        "Operator-form boundary note states that future positive step-2A closure must be an operator-level descendant/intertwiner law rather than a scalar transplant",
        "operator-level descendant/intertwiner law" in note
        and "scalar-observable or support-only statement" in note,
    )
    check(
        "Operator-form boundary note records the admissible schematic operator forms I_e^* T_Wilson I_e -> D_- and P_e T_Wilson P_e -> dW_e^H",
        "`I_e^* T_Wilson I_e -> D_-`" in note
        and "`P_e T_Wilson P_e -> dW_e^H`" in note,
    )
    check(
        "Operator-form boundary note keeps Stinespring at the level of theorem form, not imported closure",
        "Stinespring indicates the right kind of theorem shape" in note
        and "may **not** safely say" in note,
        detail="hard-review-safe use of outside theory",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
