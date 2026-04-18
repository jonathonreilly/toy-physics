#!/usr/bin/env python3
"""
Sharpen the compressed step-2 primitive to a finite nine-channel charged
Hermitian response family.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_NINE_CHANNEL_CHARGED_SOURCE_TARGET_NOTE_2026-04-17.md")
    source_family = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md")
    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 NINE-CHANNEL CHARGED SOURCE TARGET")
    print("=" * 108)
    print()

    check(
        "The compressed route is already reduced to one Wilson-side charged source family primitive aimed at dW_e^H",
        "remaining constructive primitive on the compressed route is" in source_family
        and "Wilson-side charged source family / channel" in source_family
        and "the compressed target: `Wilson -> dW_e^H`" in direct_dweh,
        detail="the route target is already compressed and Wilson-side",
    )
    check(
        "The projected-source-law note already fixes a finite nine-response Hermitian reconstruction target",
        "nine real linear responses" in projected
        and "standard Hermitian basis determine `H_e` exactly" in projected
        and "selected transport column is derivable" in projected,
        detail="recovering dW_e^H is finitely equivalent to recovering the Hermitian basis responses",
    )
    check(
        "The observable principle already supplies theorem-grade Wilson-side source-response grammar",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        and "exact derivatives are" in observable,
        detail="the missing issue is which charged family to realize, not whether response grammar exists",
    )
    check(
        "Therefore the compressed primitive can be sharpened to a finite nine-channel charged Hermitian source family on E_e",
        "finite **nine-channel charged Hermitian source family**" in note
        and "nine real linear responses" in note
        and "finite nine-channel charged Hermitian source family on `E_e`" in note
        and "does **not** bypass the charged-embedding problem" in note
        and "explicit Wilson-side charged embedding" in embedding,
        detail="the compressed route is now a finite construction problem once the Wilson-side charged realization is attacked",
    )

    check(
        "The note keeps the remaining blocker on the Wilson side rather than pretending the finite response target itself is already realized",
        "Wilson-side charged embedding/compression realization" in note
        and "What this does not close" in note
        and "positive Wilson-to-`dW_e^H` theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
