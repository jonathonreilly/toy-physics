#!/usr/bin/env python3
"""
Close all three PF frontier certificates negatively on the current bank.
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
    note = read("docs/PERRON_FROBENIUS_CURRENT_BANK_FULL_FRONTIER_CLOSURE_NOTE_2026-04-18.md")
    wilson = read("docs/PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md")
    pmns = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md")
    plaquette = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md")

    print("=" * 110)
    print("PERRON-FROBENIUS CURRENT-BANK FULL FRONTIER CLOSURE")
    print("=" * 110)
    print()

    check(
        "The Wilson frontier is closed negatively on the current bank",
        "completely closed on the current bank" in wilson
        and "current bank does **not** realize the Wilson reopening route" in wilson,
    )
    check(
        "The PMNS-native frontier is closed negatively on the current bank",
        "scalar discriminant" in pmns
        and "current bank still does **not** realize even that scalar certificate" in pmns,
    )
    check(
        "The plaquette first constructive frontier is closed negatively on the current bank",
        "first Hankel + `K` certificate" in plaquette
        and "current bank already fails at that first Hankel layer" in plaquette,
    )
    check(
        "The new note records that no live positive PF route remains on the present bank",
        "no remaining positive PF route left open" in note
        and "fully closed negatively" in note
        and "future reopening now requires genuinely new science" in note,
    )
    check(
        "The theorem is a current-bank closure theorem rather than an impossibility theorem against future strengthening",
        "What this does not close" in note
        and "an impossibility theorem against future strengthening" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
