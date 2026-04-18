#!/usr/bin/env python3
"""
Current-bank nonrealization of the remaining compressed-route charged source
family/channel primitive.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    source_family = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md")
    charged_embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 CHARGED SOURCE-FAMILY CURRENT-BANK NONREALIZATION")
    print("=" * 108)
    print()

    check(
        "Charged source-family target note says the compressed route is reduced to one Wilson-side charged source family/channel primitive",
        "compressed route is reduced to" in source_family
        and "Wilson-side charged source family / channel" in source_family,
        bucket="SUPPORT",
    )
    check(
        "Charged-embedding boundary note says the current bank still lacks the explicit Wilson-side charged embedding/compression object",
        "still does **not** have:" in charged_embedding
        and "explicit Wilson-side operator `I_e` or `P_e`" in charged_embedding,
        bucket="SUPPORT",
    )
    check(
        "Charged-support pullback boundary note says that object cannot be obtained by pure support pullback",
        "be obtained as a pure pullback of `E_e` through the current exact support bank" in support_pullback,
        bucket="SUPPORT",
    )
    check(
        "Wilson-to-Hermitian current-bank nonrealization note says the current bank still lacks the upstream Wilson-to-dW_e^H theorem",
        "does **not** already contain the missing" in nonreal
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in nonreal,
        bucket="SUPPORT",
    )

    check(
        "Charged source-family current-bank nonrealization note records that the current exact bank does not already realize the remaining compressed-route primitive",
        "current exact bank does **not** already realize the Wilson-side" in note
        and "charged source family / channel primitive" in note,
    )
    check(
        "Charged source-family current-bank nonrealization note records that compressed-route hidden-bank loopholes are now closed",
        "compressed-route construction now has no hidden-bank loophole left" in note,
    )
    check(
        "Charged source-family current-bank nonrealization note records that the compressed route is now a genuinely constructive one-primitive gap",
        "genuinely constructive one-primitive gap" in note,
        detail="compressed-route audit is now complete",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
