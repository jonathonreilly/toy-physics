#!/usr/bin/env python3
"""
Current-bank nonrealization of the active off-seed five-real target packet.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    pmns_transfer = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    active = read("docs/DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md")
    d_last = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 ACTIVE FIVE-REAL CURRENT-BANK NONREALIZATION")
    print("=" * 108)
    print()

    check(
        "PMNS transfer dominant-mode note says the aligned transfer law does not determine the generic 5-real corner-breaking source",
        "does **not** determine the generic `5`-real" in pmns_transfer
        and "corner-breaking source" in pmns_transfer,
        bucket="SUPPORT",
    )
    check(
        "PMNS active-projector reduction note says the remaining one-sided PMNS object is exactly the active five-real source",
        "remaining DM-relevant PMNS object is exactly the active five-real" in active
        or "remaining PMNS-relevant object is exactly the active five-real" in active,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic D last-mile note says the remaining D-level object is only the active off-seed 5-real breaking source",
        "remaining `D`-level object is only the active `5`-real breaking source" in d_last
        and "(xi_1, xi_2, eta_1, eta_2, delta)" in d_last,
        bucket="SUPPORT",
    )
    check(
        "Wilson-to-Hermitian current-bank nonrealization note says the current bank still lacks the upstream Wilson-to-D_- / Wilson-to-dW_e^H descendant theorem",
        "does **not** already contain the missing" in nonreal
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in nonreal,
        bucket="SUPPORT",
    )

    check(
        "Active five-real current-bank nonrealization note records that the current exact bank still does not determine the active off-seed five-real packet",
        "current exact bank still does **not** determine the active" in note
        and "off-seed `5`-real source" in note,
    )
    check(
        "Active five-real current-bank nonrealization note records that the next missing construction is one exact packet rather than a family",
        "next missing construction is one exact packet" in note,
    )
    check(
        "Active five-real current-bank nonrealization note records that current-bank global PF nonclosure on the PMNS side includes this exact packet",
        "current-bank global PF nonclosure" in note
        and "includes this exact missing" in note,
        detail="PMNS obstruction is now pinned to one packet",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
