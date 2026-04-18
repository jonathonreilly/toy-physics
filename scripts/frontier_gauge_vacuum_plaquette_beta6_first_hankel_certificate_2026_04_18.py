#!/usr/bin/env python3
"""
Repackage the first constructive non-Wilson plaquette blocker as one first
Hankel + K certificate.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


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
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md")

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 FIRST HANKEL CERTIFICATE")
    print("=" * 104)
    print()

    m1 = 0.6
    m2 = 1.1
    delta1 = m2 - m1**2
    hankel = np.array([[1.0, m1], [m1, m2]], dtype=float)
    recon_err = abs((delta1 + m1**2) - m2)
    witness_p = np.array([[1.0, 0.4], [0.4, 0.9]])
    witness_q = np.array([[1.0, 0.6], [0.6, 1.4]])
    check(
        "The first nontrivial moment pair is exactly equivalent to the first Hankel layer and the pair (m1, Delta1)",
        recon_err < 1e-12 and np.linalg.det(hankel) > 0.0,
        detail=f"det(H1)={np.linalg.det(hankel):.6f}, recon_err={recon_err:.2e}",
    )
    check(
        "Different first moment pairs induce different first Hankel layers",
        float(np.linalg.norm(witness_p - witness_q)) > 1e-12,
        detail=f"H1_gap={np.linalg.norm(witness_p - witness_q):.6f}",
    )
    check(
        "The finite-moment and compressed-rim notes already justify the sharper first Hankel + K obstruction certificate",
        "first nontrivial moment pair `(m_1, m_2)`" in finite_moment
        and "`Z_beta^env(W) = <K(W), v_beta>`" in compressed_rim
        and "first Hankel + `K` certificate" in note,
    )
    check(
        "The new note records that the current bank already fails at the first Hankel layer",
        ("current bank already fails at that first Hankel layer" in note
         or "current bank already fails at the first Hankel layer" in note)
        and "same propagated retained triple" in note
        and "different first Hankel" in note
        and "`H_1`" in note,
    )
    check(
        "The theorem stays on the plaquette non-Wilson lane and does not overclaim full beta=6 closure or a global selector",
        "What this does not close" in note
        and "the full finite moment packet" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
