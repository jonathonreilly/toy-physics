#!/usr/bin/env python3
"""
Boundary for the missing Wilson-side charged embedding/compression primitive.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    projector_interface = read("docs/DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    reduction = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    operator_form = read("docs/PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    shape = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 CHARGED EMBEDDING BOUNDARY")
    print("=" * 108)
    print()

    check(
        "PMNS projector-interface note already fixes the lepton support labels E_nu and E_e",
        "the lepton supports `E_nu` and `E_e` are fixed" in projector_interface,
        bucket="SUPPORT",
    )
    check(
        "Charged source-response note already fixes the charged Schur codomain dW_e^H = Schur_{E_e}(D_-) and H_e reconstruction",
        "`dW_e^H = Schur_{E_e}(D_-)`" in charged or "`L_e = Schur_{E_e}(D_-)`" in charged,
        bucket="SUPPORT",
    )
    check(
        "Wilson-to-Hermitian reduction note already supplies the schematic future operator forms I_e^* T_Wilson I_e -> D_- or P_e T_Wilson P_e -> dW_e^H",
        "`I_e^* T_Wilson I_e -> D_-`" in reduction
        and "`P_e T_Wilson P_e -> dW_e^H`" in reduction,
        bucket="SUPPORT",
    )
    check(
        "Step-2 operator-form note already promotes those forms as the only honest theorem form",
        "`I_e^* T_Wilson I_e -> D_-`" in operator_form
        and "`P_e T_Wilson P_e -> dW_e^H`" in operator_form,
        bucket="SUPPORT",
    )
    check(
        "Current-bank nonrealization note already says existing Wilson/observable/support/PMNS tools do not realize the missing cross-sector law",
        "current exact bank does **not** already contain the missing" in nonreal
        and "existing Wilson, observable, support, and PMNS" in nonreal
        and "do not yet realize" in note,
        bucket="SUPPORT",
    )
    check(
        "Bridge-candidate-shape note already excludes support-only and scalar-only surrogates for the missing bridge",
        "support-only transport is excluded" in shape or "support-only candidate classes" in shape
        and "scalar-only" in shape,
        bucket="SUPPORT",
    )

    check(
        "Charged embedding boundary note records that the missing primitive is an explicit Wilson-side charged embedding/compression object",
        "missing primitive is an explicit **Wilson-side charged embedding /" in note
        or "missing primitive is an explicit Wilson-side charged embedding /" in note,
    )
    check(
        "Charged embedding boundary note distinguishes codomain support data E_e from the absent Wilson-side embedding/compression realization",
        "PMNS-side charged support label `E_e`" in note
        and "does **not** have" in note
        and "explicit Wilson-side operator `I_e` or `P_e`" in note,
    )
    check(
        "Charged embedding boundary note identifies the next constructive target as an explicit charged embedding/compression object on the Wilson parent space",
        "explicit charged embedding/compression object on the Wilson parent space" in note,
        detail="next constructive seam is now narrower than generic operator rhetoric",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
