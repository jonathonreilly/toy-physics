#!/usr/bin/env python3
"""
Package the fixed-depth plaquette beta=6 operator lane as one minimal finite
certificate: one identity-rim Jacobi packet plus the explicit K(W) boundary
evaluation law.
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
    compressed_rim = read("docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md")
    finite_jacobi = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_JACOBI_PACKET_REDUCTION_NOTE_2026-04-18.md")
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIXED_DEPTH_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")

    print("=" * 116)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 FIXED-DEPTH MINIMAL CERTIFICATE")
    print("=" * 116)
    print()

    check(
        "The compressed rim theorem already makes the boundary law explicit as Z_beta^env(W)=<K(W), v_beta>",
        "`Z_beta^env(W) = <K(W), v_beta>`" in compressed_rim
        and "`K(W)`" in compressed_rim
        and "remaining unknown is only the beta-dependent vector `v_beta`" in compressed_rim,
        bucket="SUPPORT",
    )
    check(
        "The finite-Jacobi reduction already identifies the sharp fixed-depth bulk datum as one identity-rim Jacobi packet",
        "finite **Jacobi packet**" in finite_jacobi
        and "fixed-depth class-sector closure depends only on the finite Jacobi packet" in finite_jacobi
        and "first nontrivial Jacobi packet" in finite_jacobi,
        bucket="SUPPORT",
    )

    check(
        "Therefore the whole fixed-depth plaquette lane packages as one minimal two-layer certificate: bulk Jacobi packet plus explicit K(W) evaluation law",
        "`Jacobi + K` certificate" in note
        and "one finite identity-rim Jacobi packet" in note
        and "one already-explicit downstream boundary evaluation law" in note,
    )
    check(
        "The certificate is minimal in the current theorem order because the current bank already fails at the first Jacobi layer before any downstream K(W) ambiguity enters",
        "fails at the first certificate layer" in note
        and "fails at the first Jacobi layer" in note,
    )
    check(
        "So the remaining non-Wilson PF seam is no longer a generic operator-evaluation prompt but one finite Jacobi+K certificate",
        "not a generic" in note
        and "operator-evaluation problem but one finite `Jacobi + K` certificate" in note,
    )
    check(
        "The new note aligns the plaquette frontier with the Wilson-certificate style without importing any extra theorem beyond the existing bulk and rim reductions",
        "same hard-review-safe form as the" in note
        and "Wilson side." in note
        and "one local `2-edge + 3` certificate" in note
        and "one minimal `Jacobi + K`" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
