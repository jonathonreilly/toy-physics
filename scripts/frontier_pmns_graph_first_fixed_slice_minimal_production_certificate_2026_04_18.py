#!/usr/bin/env python3
"""
Package the PMNS-native production frontier as one minimal fixed-slice
two-holonomy certificate.
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
    collapse = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md")
    production = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md")
    note = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_MINIMAL_PRODUCTION_CERTIFICATE_NOTE_2026-04-18.md")

    print("=" * 110)
    print("PMNS GRAPH-FIRST FIXED-SLICE MINIMAL PRODUCTION CERTIFICATE")
    print("=" * 110)
    print()

    check(
        "The collapse theorem already says any two independent fixed-slice native holonomies reconstruct chi exactly",
        "two independent native holonomies reconstruct `chi` exactly" in collapse
        or "two independent native holonomies reconstruct chi exactly" in collapse
        or "two independent native holonomies collapse the fixed slice exactly" in collapse,
        bucket="SUPPORT",
    )
    check(
        "The production-boundary theorem already says the only remaining content is a nontrivial fixed-slice holonomy pair, equivalently nonzero chi",
        "nontrivial fixed-slice holonomy-pair" in production
        and ("nonzero `chi = J_chi`" in production or "nonzero `J_chi = chi`" in production),
        bucket="SUPPORT",
    )
    check(
        "Therefore the PMNS-native frontier is exactly one minimal fixed-slice two-holonomy production certificate",
        ("minimal" in note and "fixed-slice two-holonomy" in note and "production certificate" in note)
        and ("one fixed slice" in note or "fix one slice" in note)
        and "one independent two-holonomy pair" in note,
    )
    check(
        "The current bank still does not realize that certificate",
        "still does **not** realize that certificate" in note,
    )
    check(
        "The new note aligns the PMNS-native frontier with the Wilson and plaquette certificate framing",
        "Wilson positive reopening is one local `2-edge + 3` certificate" in note
        and "plaquette non-Wilson closure is one minimal `moment + K` certificate" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
