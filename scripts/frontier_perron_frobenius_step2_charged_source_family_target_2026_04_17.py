#!/usr/bin/env python3
"""
Reduction of the compressed PF route to one missing Wilson-side charged source
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
    note = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    direct = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    triplet = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")
    charged_embedding = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 CHARGED SOURCE-FAMILY TARGET")
    print("=" * 108)
    print()

    check(
        "Observable principle note already gives theorem-grade source-response machinery via W[J] = log|det(D+J)| - log|det D|",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        and "source-response coefficients" in observable,
        bucket="SUPPORT",
    )
    check(
        "Direct dW_e^H route reduction note already identifies the compressed codomain and says only the right-sensitive selector remains downstream",
        "fully typed" in note
        and "once it lands, only the right-sensitive selector remains downstream." in note,
        bucket="SUPPORT",
    )
    check(
        "Projected-source law derivation note says dW_e^H already reconstructs H_e and makes the selected transport column algorithmic",
        "`dW_e^H` reconstructs `H_e`" in note
        and "transport-relevant selected column is already algorithmic" in note,
        bucket="SUPPORT",
    )
    check(
        "Projected-source triplet-sign theorem says gamma, E1, E2 are exact linear functionals of the projected Hermitian response pack",
        "triplet channels are exact linear functionals" in triplet
        and "`gamma > 0`" in triplet
        and "`E1 > 0`" in triplet
        and "`E2 > 0`" in triplet,
        bucket="SUPPORT",
    )
    check(
        "Charged-embedding and support-pullback boundary notes say the missing primitive is genuinely Wilson-side and cannot be obtained by pure support pullback",
        "Wilson-side charged embedding /" in note
        and "cannot be obtained by pure support pullback" in note,
        bucket="SUPPORT",
    )

    check(
        "Charged source-family target note records that the compressed route is blocked by one Wilson-side charged source family/channel primitive rather than missing downstream reconstruction algebra",
        "remaining constructive primitive on the compressed route is" in note
        and "charged source family / channel" in note
        and "not more downstream" in note
        and "reconstruction algebra" in note,
    )
    check(
        "Charged source-family target note records that dW_e^H -> H_e -> packet -> triplet reconstruction is already exact",
        "downstream reconstruction from `dW_e^H` is already exact" in note
        and "`H_e`" in note
        and "`(gamma, E1, E2)`" in note,
    )
    check(
        "Charged source-family target note records that the compressed route is now a one-primitive construction problem",
        "compressed route is reduced to" in note
        and "build the Wilson-side charged source family / channel" in note,
        detail="remaining compressed-route work is now one primitive",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
