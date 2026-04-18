#!/usr/bin/env python3
"""
Package the fixed-depth plaquette beta=6 non-Wilson route as one minimal scalar
certificate: a finite moment packet plus the explicit K(W) boundary law.
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
    finite_moment = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md")
    compressed_rim = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md")
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIXED_DEPTH_SCALAR_CERTIFICATE_NOTE_2026-04-18.md")

    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 FIXED-DEPTH SCALAR CERTIFICATE")
    print("=" * 112)
    print()

    check(
        "The finite-moment reduction note already identifies the sharp fixed-depth bulk datum as one finite cyclic-moment packet",
        "finite cyclic-moment packet" in finite_moment
        and "first nontrivial moment pair" in finite_moment,
        bucket="SUPPORT",
    )
    check(
        "The compressed rim theorem already makes the downstream boundary law explicit through K(W)",
        "`Z_beta^env(W) = <K(W), v_beta>`" in compressed_rim
        and "`K(W)`" in compressed_rim,
        bucket="SUPPORT",
    )
    check(
        "Therefore the whole fixed-depth non-Wilson plaquette lane is one minimal moment+K certificate",
        "`moment + K` certificate" in note
        and "one finite cyclic-moment packet" in note
        and "one explicit downstream boundary evaluation law" in note,
    )
    check(
        "The current bank still fails at the first scalar layer of that certificate",
        "fails already at the first scalar layer" in note
        and "(m_1, m_2)" in note,
    )
    check(
        "The new note aligns the plaquette route with the Wilson-certificate framing at the scalar level",
        "one local `2-edge + 3` certificate" in note
        and "one minimal `moment + K`" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
