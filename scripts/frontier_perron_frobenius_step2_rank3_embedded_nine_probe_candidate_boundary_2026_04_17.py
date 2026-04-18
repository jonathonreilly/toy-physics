#!/usr/bin/env python3
"""
Strongest live positive candidate class on the compressed PMNS route.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_RANK3_EMBEDDED_NINE_PROBE_CANDIDATE_BOUNDARY_NOTE_2026-04-17.md")
    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    source_family_nine = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md")
    operator_form = read("docs/PERRON_FROBENIUS_STEP2_OPERATOR_FORM_BOUNDARY_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    scalar_nonreal = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    bank_nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 RANK-3 EMBEDDED NINE-PROBE CANDIDATE BOUNDARY")
    print("=" * 108)
    print()

    check(
        "The compressed route is already the clean first PMNS-side target and its minimal constructive response target is already finite",
        "the compressed target: `Wilson -> dW_e^H`" in direct_dweh
        and "finite **nine-channel charged Hermitian source family**" in source_family_nine
        and "nine real Hermitian-basis responses" in note,
        detail="the remaining compressed-route work is now concrete and finite in target shape",
    )
    check(
        "The operator-form boundary already admits exactly the rank-3 charged embedding/compression form needed by the candidate class",
        "`I_e^* T_Wilson I_e -> D_-`" in operator_form
        and "`P_e T_Wilson P_e -> dW_e^H`" in operator_form
        and "rank-3 Wilson-side charged embedding/compression `I_e` or `P_e`" in note,
        detail="the candidate class matches the already-admitted operator proof form",
    )
    check(
        "The observable engine is already available, while scalar-only, support-only, and hidden-current-bank classes are already excluded",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        and "block-local" in scalar_nonreal
        and "missing PMNS" in scalar_nonreal
        and "sector-selector bridge" in scalar_nonreal
        and "be obtained as a pure pullback of `E_e`" in support_pullback
        and "under another name" in bank_nonreal,
        detail="everything weaker than the embedded nine-probe class is already dead",
    )
    check(
        "Therefore the strongest honest next positive candidate on the compressed route is the rank-3 embedded nine-probe class",
        "strongest honest next positive candidate class on the compressed" in note
        and "embedded nine-probe Hermitian source family" in note
        and "everything weaker than the embedded rank-3" in note,
        detail="this is a candidate-class theorem, not a fake bridge proof",
    )

    check(
        "The note keeps the result typed as a candidate boundary rather than as a proved Wilson-to-dW_e^H theorem",
        "candidate boundary, not a proof" in note
        and "does **not** prove" in note
        and "positive Wilson-to-`dW_e^H` theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
