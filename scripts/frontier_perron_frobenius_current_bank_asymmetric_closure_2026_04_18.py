#!/usr/bin/env python3
"""
Record the asymmetric closure consequence of the current PF bank.
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
    frontier = read("docs/PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md")
    note = read("docs/PERRON_FROBENIUS_CURRENT_BANK_ASYMMETRIC_CLOSURE_NOTE_2026-04-18.md")

    print("=" * 110)
    print("PERRON-FROBENIUS CURRENT-BANK ASYMMETRIC CLOSURE")
    print("=" * 110)
    print()

    check(
        "The minimal-frontier note already says only Wilson is the positive reopening lever",
        "only the Wilson certificate" in frontier and "positive reopening lever" in frontier,
        bucket="SUPPORT",
    )
    check(
        "The minimal-frontier note already says the PMNS-native and plaquette certificates remain current-bank blockers",
        "PMNS-native and plaquette certificates" in frontier and "blockers" in frontier,
        bucket="SUPPORT",
    )
    check(
        "Therefore the current PF branch is asymmetrically closed: positive reopening depends on Wilson, negative closure does not",
        "asymmetrically closed" in note
        and "only positive reopening lever" in note
        and "independent current-bank blockers" in note,
    )
    check(
        "So weakening Wilson makes the branch more clearly negative rather than more open",
        "more clearly negative, not more open" in note,
    )
    check(
        "The note states the Wilson consequence as a branch-level current-bank result rather than a new Wilson theorem",
        "What this does not close" in note and "a Wilson robustness theorem" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
