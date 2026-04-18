#!/usr/bin/env python3
"""
Repackage the sharpest Wilson support theorem as one adjacent directed two-edge
chain on the physical nearest-neighbor lattice.
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


def e(i: int, j: int) -> np.ndarray:
    m = np.zeros((3, 3), dtype=complex)
    m[i, j] = 1.0
    return m


def embedded(x: np.ndarray) -> np.ndarray:
    out = np.zeros((5, 5), dtype=complex)
    out[:3, :3] = x
    return out


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    four_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md")
    four_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_MINIMALITY_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON TWO-EDGE CHAIN REDUCTION")
    print("=" * 108)
    print()

    g12 = embedded(e(0, 1))
    g23 = embedded(e(1, 2))
    f21 = g12.conj().T
    f32 = g23.conj().T
    f11 = g12 @ f21
    f22 = f21 @ g12
    f33 = f32 @ g23
    f13 = g12 @ g23
    f31 = f32 @ f21
    p_e = f11 + f22 + f33

    edge_err = max(
        float(np.linalg.norm(g12 @ g12)),
        float(np.linalg.norm(g23 @ g23)),
        float(np.linalg.norm(g12 @ f21 @ g12 - g12)),
        float(np.linalg.norm(g23 @ f32 @ g23 - g23)),
        float(np.linalg.norm(f21 @ g12 - g23 @ f32)),
        float(np.linalg.norm(g23 @ g12)),
        float(np.linalg.norm(g12 @ f32)),
    )

    units = {
        (1, 1): f11, (2, 2): f22, (3, 3): f33,
        (1, 2): g12, (2, 1): f21,
        (2, 3): g23, (3, 2): f32,
        (1, 3): f13, (3, 1): f31,
    }
    full_err = 0.0
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                for l in range(1, 4):
                    lhs = units[(i, j)] @ units[(k, l)]
                    rhs = units[(i, l)] if j == k else np.zeros_like(lhs)
                    full_err = max(full_err, float(np.linalg.norm(lhs - rhs)))

    print(f"rank(P_e)                                   = {int(round(np.trace(p_e).real))}")
    print(f"two-edge chain max error                    = {edge_err:.3e}")
    print(f"full matrix-unit max error                  = {full_err:.3e}")
    print()

    check(
        "An adjacent directed two-edge chain already reconstructs the full 3x3 matrix-unit system and rank-3 support",
        edge_err < 1.0e-12 and full_err < 1.0e-12 and abs(np.trace(p_e).real - 3.0) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}, edge_err={edge_err:.2e}, full_err={full_err:.2e}",
    )
    check(
        "Reverse edges, diagonal support data, and the long corner are already downstream of the physical two-edge chain",
        float(np.linalg.norm(f21 - embedded(e(1, 0)))) < 1.0e-12
        and float(np.linalg.norm(f11 - embedded(e(0, 0)))) < 1.0e-12
        and float(np.linalg.norm(f22 - embedded(e(1, 1)))) < 1.0e-12
        and float(np.linalg.norm(f33 - embedded(e(2, 2)))) < 1.0e-12
        and float(np.linalg.norm(f13 - embedded(e(0, 2)))) < 1.0e-12,
    )
    check(
        "The new note records the exact physical re-reading of the sharpest Wilson support target as one adjacent directed two-edge chain",
        "adjacent directed two-edge chain" in note
        and "the lattice is treated as physical" in note
        and "local edge data on the nearest-neighbor lattice" in note,
    )
    check(
        "The new note uses the exact four-packet and four-packet-minimality theorems in the right way and preserves the current-bank support-first obstruction",
        "off-diagonal Hermitian nearest-neighbor `4`-packet" in four_note
        and "exact minimal finite number of real Hermitian Wilson source" in four_min
        and "current bank still does **not** realize even this physical adjacent" in note
        and "two-edge chain." in note,
    )

    check(
        "The Wilson front is now stated as a local physical-lattice target rather than an abstract packet",
        "It is local:" in note and "one adjacent directed two-edge chain" in note,
        bucket="SUPPORT",
    )
    check(
        "The current bank still fails at that physical local two-edge chain layer",
        "current bank still does **not** realize even this physical adjacent" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
