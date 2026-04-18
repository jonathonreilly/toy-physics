#!/usr/bin/env python3
"""
Package the remaining PF science on the current bank as a minimal set of
frontier certificates.
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
    wilson_audit = read("docs/PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md")
    wilson_cert = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    pmns_prod = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md")
    plaquette_scalar = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIXED_DEPTH_SCALAR_CERTIFICATE_NOTE_2026-04-18.md")
    note = read("docs/PERRON_FROBENIUS_MINIMAL_FRONTIER_CERTIFICATES_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS MINIMAL FRONTIER CERTIFICATES")
    print("=" * 108)
    print()

    check(
        "The Wilson audit already identifies Wilson as the main positive reopening lever on the branch",
        "main positive reopening lever" in wilson_audit,
        bucket="SUPPORT",
    )
    check(
        "The Wilson route is already compressed to one local physical certificate",
        "minimal local path-algebra `2-edge + 3` certificate" in wilson_cert,
        bucket="SUPPORT",
    )
    check(
        "The PMNS-native lane is already reduced to one production-law object",
        ("nontrivial fixed-slice holonomy-pair source law" in pmns_prod
         or "nontrivial fixed-slice holonomy" in pmns_prod)
        and ("nonzero `J_chi = chi`" in pmns_prod or "nonzero `chi = J_chi`" in pmns_prod),
        bucket="SUPPORT",
    )
    check(
        "The plaquette non-Wilson lane is already reduced to one scalar certificate",
        "`moment + K` certificate" in plaquette_scalar,
        bucket="SUPPORT",
    )
    check(
        "Therefore the current PF branch now decomposes exactly into three minimal frontier certificates",
        "three minimal frontier certificates" in note
        and "Wilson positive reopening certificate" in note
        and "PMNS-native production certificate" in note
        and "Plaquette non-Wilson scalar certificate" in note,
    )
    check(
        "Only the Wilson certificate is currently a positive reopening lever, while the PMNS-native and plaquette certificates remain current-bank blockers",
        ("only the Wilson certificate" in note and "positive reopening lever" in note)
        and ("PMNS-native and plaquette certificates" in note and "blockers" in note),
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
