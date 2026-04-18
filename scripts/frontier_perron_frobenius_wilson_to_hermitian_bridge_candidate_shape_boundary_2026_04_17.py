#!/usr/bin/env python3
"""
Shape boundary for future positive Wilson-to-Hermitian bridge candidates.
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
    note = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md")
    reduction = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    scalar_nonreal = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    support = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    extension = read("docs/PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md")
    step2_positive = read("docs/PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md")

    print("=" * 112)
    print("PERRON-FROBENIUS WILSON-TO-HERMITIAN BRIDGE CANDIDATE SHAPE BOUNDARY")
    print("=" * 112)
    print()

    check(
        "Step-2A reduction note already fixes the codomain to the charged chain Wilson -> D_- -> dW_e^H -> H_e",
        "`Wilson -> D_- -> dW_e^H -> H_e`" in reduction,
        bucket="SUPPORT",
    )
    check(
        "Charged source-response note already identifies dW_e^H as charged-sector Schur/Hermitian data rather than scalar data",
        "`dW_e^H` is an exact charged-sector Schur pushforward" in charged
        and "`dW_e^H` reconstructs `H_e`" in charged,
        bucket="SUPPORT",
    )
    check(
        "Current-bank nonrealization note already excludes hidden Wilson/observable/support candidates in the present bank",
        "The current bank contains:" in nonreal
        and "current exact bank does **not** already contain the missing" in nonreal
        and "existing Wilson, observable, support, and PMNS" in nonreal,
        bucket="SUPPORT",
    )
    check(
        "Observable-principle note already keeps the retained observable grammar additive and scalar",
        "`W[J] = log|det(D+J)| - log|det D|`" in observable
        or "`W[J] = log |det(D+J)| - log |det D|`" in observable,
        bucket="SUPPORT",
    )
    check(
        "PMNS scalar-bridge nonrealization note already excludes the current additive scalar grammar as the missing inter-sector bridge",
        "present scalar observable bank does not realize the missing PMNS" in scalar_nonreal
        and "block-local" in scalar_nonreal,
        bucket="SUPPORT",
    )
    check(
        "Site-phase / cube-shift note already limits the exact support intertwiner to support transport",
        "support transport only" in support
        or "Its safe role is narrower" in support,
        bucket="SUPPORT",
    )
    check(
        "Minimal PMNS extension theorem already types any future positive selector as sector-sensitive, inter-sector, and non-additive",
        "sector-sensitive and inter-sector" in extension
        and "non-additive over the lepton direct sum" in extension
        and "mixed bridge with one real amplitude slot" in extension,
        bucket="SUPPORT",
    )
    check(
        "Step-2 minimal positive-completion theorem already splits the future positive completion into upstream descendant law plus downstream bridge amplitude if needed",
        "one upstream descendant law" in step2_positive
        and "at most one downstream reduced bridge amplitude" in step2_positive,
        bucket="SUPPORT",
    )

    check(
        "Bridge candidate-shape note excludes scalar-only and support-only candidate classes explicitly",
        "cannot be:" in note
        and "another additive scalar observable" in note
        and "another support-only intertwiner" in note,
    )
    check(
        "Bridge candidate-shape note identifies the admissible step-2A shape as a genuinely new matrix-valued cross-sector descendant/intertwiner law",
        "matrix-valued cross-sector descendant/intertwiner law" in note
        and "`D_- / dW_e^H / H_e`" in note,
    )
    check(
        "Bridge candidate-shape note keeps the step-2B object structurally distinct as a sector-sensitive inter-sector non-additive mixed bridge",
        "step 2A and step 2B now have distinct shape signatures" in note
        and "sector-sensitive mixed-bridge" in note,
        detail="hard-review-safe candidate typing rather than dynamics closure",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
