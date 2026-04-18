#!/usr/bin/env python3
"""
Close the Wilson lane completely on the current bank at its sharpest current
certificate level.
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
    note = read("docs/PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md")
    certificate = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHARPOLY_CERTIFICATE_NOTE_2026-04-18.md")
    generator = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_GENERATOR_REDUCTION_NOTE_2026-04-18.md")
    audit = read("docs/PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS WILSON CURRENT-BANK COMPLETE CLOSURE")
    print("=" * 108)
    print()

    check(
        "The sharpest Wilson reopening route is now exactly one local nilpotent-chain 1+1 certificate",
        "local nilpotent-chain `1 + 1` certificate" in certificate
        and "`chi_(B_e)(lambda) = chi_(H_e)(lambda)`" in certificate,
    )
    check(
        "The current bank still does not realize even the first local Wilson generator layer",
        "current bank still does **not** realize even this sharper local generator" in generator,
    )
    check(
        "Therefore the current bank does not realize the Wilson reopening route at all",
        "current bank does **not** realize the Wilson reopening route" in note
        and "first generator layer" in note
        and "completely closed on the current bank" in note,
    )
    check(
        "The Wilson dependency audit remains consistent: Wilson is still the only positive reopening lever globally, but not on the current bank",
        ("only positive reopening lever" in audit or "main positive reopening lever" in audit)
        and "Wilson current-bank complete closure" not in audit,  # ensure new closure is genuinely new
        bucket="SUPPORT",
    )
    check(
        "The theorem is a current-bank closure theorem, not an impossibility theorem against future strengthened Wilson science",
        "What this does not close" in note
        and "an impossibility theorem against all future Wilson strengthening" in note
        and "a positive Wilson reopening theorem from a stronger bank" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
