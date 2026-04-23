#!/usr/bin/env python3
"""Supersession audit for the historical Planck retained-status note."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def expect(name: str, cond: bool) -> int:
    if cond:
        print(f"PASS: {name}")
        return 1
    print(f"FAIL: {name}")
    return 0


def main() -> int:
    note = read("docs/PLANCK_SCALE_AXIOM_NATIVE_RETAINED_AUDIT_2026-04-23.md")
    packet = read("docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md")
    acceptance = read("docs/PLANCK_SCALE_ONE_AXIOM_ACCEPTANCE_HOSTILE_REVIEW_MEMO_2026-04-23.md")

    passed = 0
    total = 0

    print("Planck historical retained-audit supersession check")
    print("=" * 78)

    total += 1
    passed += expect(
        "historical-audit-declares-supersession",
        "Supersession Note" in note
        and "should not be used as the current status entrypoint" in note,
    )

    total += 1
    passed += expect(
        "historical-audit-points-to-current-native-packet",
        "PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md" in note,
    )

    total += 1
    passed += expect(
        "current-packet-keeps-authorized-surface-claim",
        "Authorized surface" in packet
        and "one-axiom information / Hilbert / locality surface" in packet,
    )

    total += 1
    passed += expect(
        "acceptance-memo-keeps-minimal-ledger-caveat",
        "not yet front-door minimal-ledger retained" in acceptance,
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
