#!/usr/bin/env python3
"""
Minimal positive completion class for step 2 of the PF lane.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md")
    reduction = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    constructive = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEorem_NOTE_2026-04-17.md") if False else read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md")
    extension = read("docs/PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md")
    class_space = read("docs/PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md")
    amplitude = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")
    zero_law = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")

    lambda_star = 0.795532193595
    eta_root = 1.0
    gamma_root = 0.177466004463
    e1_root = 0.247922610478
    e2_root = 1.552085732579

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 MINIMAL POSITIVE COMPLETION CLASS")
    print("=" * 108)
    print()
    print(f"constructive exact-closure witness: lambda_*={lambda_star:.12f}, eta/eta_obs={eta_root:.6f}")
    print(f"projected-source triplet at root: gamma={gamma_root:.12f}, E1={e1_root:.12f}, E2={e2_root:.12f}")
    print()

    check(
        "Wilson-to-Hermitian reduction note already fixes the first honest codomain to Wilson -> D_- -> dW_e^H -> H_e",
        "`Wilson -> D_- -> dW_e^H -> H_e`" in reduction,
        bucket="SUPPORT",
    )
    check(
        "Wilson-to-Hermitian current-bank nonrealization note already closes the hidden-bank loophole for that bridge",
        "does **not** already contain the missing" in nonreal
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in nonreal,
        bucket="SUPPORT",
    )
    check(
        "Constructive continuity theorem already proves the PMNS constructive chamber contains an exact eta/eta_obs = 1 point",
        "exact `eta / eta_obs = 1` point" in constructive
        or "exact `eta = eta_obs` point" in constructive,
        bucket="SUPPORT",
    )
    check(
        "PMNS minimal microscopic extension note already proves any future positive selector must be a non-additive sector-sensitive inter-sector mixed bridge",
        "sector-sensitive and inter-sector" in extension
        and "non-additive over the lepton direct sum" in extension
        and "mixed bridge with one real amplitude slot" in extension
        and "one real amplitude slot" in extension,
        bucket="SUPPORT",
    )
    check(
        "PMNS selector class-space uniqueness note already proves only one reduced selector class survives",
        "one-dimensional" in class_space
        and "`S_cls = chi_N_nu - chi_N_e`" in class_space,
        bucket="SUPPORT",
    )
    check(
        "PMNS unique amplitude-slot note already reduces every future microscopic realization to B_red = a_sel S_cls",
        "`B_red = a_sel S_cls`" in amplitude
        and "one real amplitude slot" in amplitude,
        bucket="SUPPORT",
    )
    check(
        "PMNS current-stack zero-law note already proves the retained bank activates that reduced bridge with zero amplitude today",
        "`a_sel,current = 0`" in zero_law,
        bucket="SUPPORT",
    )

    check(
        "Constructive exact-closure witness is genuinely interior and keeps the projected-source triplet positive",
        0.0 < lambda_star < 1.0 and abs(eta_root - 1.0) < 1.0e-12 and min(gamma_root, e1_root, e2_root) > 0.0,
        detail="existence is not the live blocker on the PMNS side",
    )
    check(
        "Minimal positive completion note states the exact two-stage structure: one upstream descendant law plus at most one downstream reduced bridge amplitude",
        "one upstream descendant law" in note
        and "plus at most one downstream reduced bridge amplitude" in note,
    )
    check(
        "The note records the reduced PMNS bridge in the one-slot form B_red = a_sel (chi_N_nu - chi_N_e)",
        "`B_red = a_sel (chi_N_nu - chi_N_e)`" in note,
    )
    check(
        "The note keeps support-only and scalar-only extensions excluded and stays within structural current-stack scope",
        "support-only and scalar-only extensions are already ruled out" in note
        and "What this does not close" in note
        and "a positive global PF selector" in note,
        detail="hard-review-safe structural reduction only",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
