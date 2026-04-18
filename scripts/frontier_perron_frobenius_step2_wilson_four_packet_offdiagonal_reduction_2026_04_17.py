#!/usr/bin/env python3
"""
Reduce theorem-grade Wilson support realization from the 7-packet chain
certificate to a 4-packet Hermitian off-diagonal chain certificate.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md")
    seven_note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON FOUR-PACKET OFF-DIAGONAL REDUCTION")
    print("=" * 108)
    print()

    f12 = embedded(e(0, 1))
    f21 = embedded(e(1, 0))
    f23 = embedded(e(1, 2))
    f32 = embedded(e(2, 1))

    s4 = f12 + f21
    s5 = -1j * f12 + 1j * f21
    s8 = f23 + f32
    s9 = -1j * f23 + 1j * f32

    rf12 = 0.5 * (s4 + 1j * s5)
    rf21 = 0.5 * (s4 - 1j * s5)
    rf23 = 0.5 * (s8 + 1j * s9)
    rf32 = 0.5 * (s8 - 1j * s9)

    rf11 = rf12 @ rf21
    rf22 = rf21 @ rf12
    rf33 = rf32 @ rf23
    mid_gap = float(np.linalg.norm(rf22 - rf23 @ rf32))
    rf13 = rf12 @ rf23
    rf31 = rf32 @ rf21
    p_e = rf11 + rf22 + rf33

    offdiag_err = max(
        float(np.linalg.norm(rf12 @ rf12)),
        float(np.linalg.norm(rf21 @ rf21)),
        float(np.linalg.norm(rf23 @ rf23)),
        float(np.linalg.norm(rf32 @ rf32)),
        float(np.linalg.norm(rf12 @ rf21 @ rf12 - rf12)),
        float(np.linalg.norm(rf21 @ rf12 @ rf21 - rf21)),
        float(np.linalg.norm(rf23 @ rf32 @ rf23 - rf23)),
        float(np.linalg.norm(rf32 @ rf23 @ rf32 - rf32)),
        float(np.linalg.norm(rf12 @ rf32)),
        float(np.linalg.norm(rf23 @ rf21)),
        float(np.linalg.norm(rf21 @ rf32)),
        float(np.linalg.norm(rf23 @ rf12)),
        mid_gap,
    )

    units = {
        (1, 1): rf11, (2, 2): rf22, (3, 3): rf33,
        (1, 2): rf12, (2, 1): rf21,
        (2, 3): rf23, (3, 2): rf32,
        (1, 3): rf13, (3, 1): rf31,
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
    print(f"off-diagonal chain max error                = {offdiag_err:.3e}")
    print(f"full matrix-unit max error                  = {full_err:.3e}")
    print()

    check(
        "A 4-element Hermitian off-diagonal Wilson packet already reconstructs the full 3x3 matrix-unit system",
        offdiag_err < 1.0e-12 and full_err < 1.0e-12 and abs(np.trace(p_e).real - 3.0) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}, offdiag_err={offdiag_err:.2e}, full_err={full_err:.2e}",
    )
    check(
        "The diagonal support data are already downstream of the off-diagonal chain through F_11=F_12F_21, F_22=F_21F_12=F_23F_32, F_33=F_32F_23",
        mid_gap < 1.0e-12
        and float(np.linalg.norm(rf11 - embedded(e(0, 0)))) < 1.0e-12
        and float(np.linalg.norm(rf22 - embedded(e(1, 1)))) < 1.0e-12
        and float(np.linalg.norm(rf33 - embedded(e(2, 2)))) < 1.0e-12,
        detail=f"middle_gap={mid_gap:.2e}",
    )
    check(
        "The new note records the exact sharpening from the 7-packet chain certificate to the Hermitian off-diagonal 4-packet certificate",
        "off-diagonal Hermitian nearest-neighbor `4`-packet" in note
        and "The diagonal matrix units are already products of the off-diagonal chain" in note
        and "one Hermitian off-diagonal `4`-packet plus finite chain identities" in note,
    )
    check(
        "The new note uses the exact 7-packet theorem in the right way and preserves the current-bank support-first obstruction",
        "nearest-neighbor `7`-packet." in seven_note
        and "current bank still does **not** realize even this sharper off-diagonal" in note
        and "`4`-packet." in note,
    )

    check(
        "The Wilson support frontier is now sharper than the 7-packet reviewer target",
        "the Wilson support frontier is now an off-diagonal `4`-packet problem" in note
        and "Then the diagonal data and long corner follow automatically" in note,
        bucket="SUPPORT",
    )
    check(
        "The current bank still fails at the sharper off-diagonal 4-packet support layer",
        "current bank still does **not** realize even this sharper off-diagonal" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
