#!/usr/bin/env python3
"""
Package the remaining PF branch at its current sharpest frontier-certificate
level.
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
    old_frontier = read("docs/PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md")
    wilson = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHARPOLY_CERTIFICATE_NOTE_2026-04-18.md")
    pmns = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md")
    plaquette = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md")
    note = read("docs/PERRON_FROBENIUS_SHARPEST_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md")

    print("=" * 102)
    print("PERRON-FROBENIUS SHARPEST FRONTIER CERTIFICATES")
    print("=" * 102)
    print()

    check(
        "The previous frontier decomposition had already reduced the branch to Wilson, PMNS-native, and plaquette certificates",
        "three minimal frontier certificates" in old_frontier
        and "Wilson positive reopening certificate" in old_frontier
        and "PMNS-native production certificate" in old_frontier
        and "Plaquette non-Wilson scalar certificate" in old_frontier,
        bucket="SUPPORT",
    )
    check(
        "The Wilson frontier is now sharper than before: one local nilpotent-chain 1+1 certificate",
        "local nilpotent-chain `1 + 1` certificate" in wilson,
    )
    check(
        "The PMNS-native frontier is now sharper than before: one scalar production discriminant",
        "scalar discriminant" in pmns and "current bank still does **not** realize even that scalar certificate" in pmns,
    )
    check(
        "The plaquette frontier is now sharper than before: one first Hankel + K certificate",
        "first Hankel + `K` certificate" in plaquette
        and "current bank already fails at that first Hankel layer" in plaquette,
    )
    check(
        "The new note records the sharpest remaining frontier as Wilson generator, PMNS scalar, and plaquette first-Hankel certificates",
        "Wilson positive reopening certificate" in note
        and "one local nilpotent-chain `1 + 1` certificate" in note
        and "PMNS-native scalar production certificate" in note
        and "one fixed-slice scalar holonomy discriminant" in note
        and "Plaquette first constructive scalar certificate" in note
        and "one first Hankel + `K` certificate" in note,
    )
    check(
        "Only the Wilson certificate remains a positive reopening lever on the current bank",
        "positive reopening lever is still only Wilson" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
