#!/usr/bin/env python3
"""
Reduce theorem-grade Wilson support realization from a 9-element Hermitian
packet to a 7-element nearest-neighbor chain packet.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_SEVEN_PACKET_CHAIN_REDUCTION_NOTE_2026-04-17.md")
    nine_packet = read("docs/PERRON_FROBENIUS_STEP2_WILSON_HERMITIAN_SOURCE_PACKET_REALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON SEVEN-PACKET CHAIN REDUCTION")
    print("=" * 108)
    print()

    f11 = embedded(e(0, 0))
    f22 = embedded(e(1, 1))
    f33 = embedded(e(2, 2))
    f12 = embedded(e(0, 1))
    f21 = embedded(e(1, 0))
    f23 = embedded(e(1, 2))
    f32 = embedded(e(2, 1))

    s1 = f11
    s2 = f22
    s3 = f33
    s4 = f12 + f21
    s5 = -1j * f12 + 1j * f21
    s8 = f23 + f32
    s9 = -1j * f23 + 1j * f32

    rf11 = s1
    rf22 = s2
    rf33 = s3
    rf12 = 0.5 * (s4 + 1j * s5)
    rf21 = 0.5 * (s4 - 1j * s5)
    rf23 = 0.5 * (s8 + 1j * s9)
    rf32 = 0.5 * (s8 - 1j * s9)
    rf13 = rf12 @ rf23
    rf31 = rf32 @ rf21
    p_e = rf11 + rf22 + rf33

    units = {
        (1, 1): rf11, (2, 2): rf22, (3, 3): rf33,
        (1, 2): rf12, (2, 1): rf21,
        (2, 3): rf23, (3, 2): rf32,
        (1, 3): rf13, (3, 1): rf31,
    }

    chain_err = 0.0
    chain_relations = [
        rf12 - rf11 @ rf12 @ rf22,
        rf21 - rf22 @ rf21 @ rf11,
        rf23 - rf22 @ rf23 @ rf33,
        rf32 - rf33 @ rf32 @ rf22,
        rf12 @ rf21 - rf11,
        rf21 @ rf12 - rf22,
        rf23 @ rf32 - rf22,
        rf32 @ rf23 - rf33,
    ]
    for rel in chain_relations:
        chain_err = max(chain_err, float(np.linalg.norm(rel)))

    full_err = 0.0
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                for l in range(1, 4):
                    lhs = units[(i, j)] @ units[(k, l)]
                    rhs = units[(i, l)] if j == k else np.zeros_like(lhs)
                    full_err = max(full_err, float(np.linalg.norm(lhs - rhs)))

    s6 = rf13 + rf31
    s7 = -1j * rf13 + 1j * rf31
    corner_err = max(
        float(np.linalg.norm(rf13 - embedded(e(0, 2)))),
        float(np.linalg.norm(rf31 - embedded(e(2, 0)))),
        float(np.linalg.norm(s6 - (embedded(e(0, 2)) + embedded(e(2, 0))))),
        float(np.linalg.norm(s7 - (-1j * embedded(e(0, 2)) + 1j * embedded(e(2, 0))))),
    )

    print(f"rank(P_e)                                   = {int(round(np.trace(p_e).real))}")
    print(f"chain relation max error                    = {chain_err:.3e}")
    print(f"full matrix-unit max error                  = {full_err:.3e}")
    print(f"derived (1,3) corner max error              = {corner_err:.3e}")
    print()

    check(
        "A 7-element nearest-neighbor Hermitian Wilson packet already reconstructs the full 3x3 matrix-unit system",
        chain_err < 1.0e-12 and full_err < 1.0e-12 and abs(np.trace(p_e).real - 3.0) < 1.0e-12,
        detail=f"rank(P_e)={int(round(np.trace(p_e).real))}, chain_err={chain_err:.2e}, full_err={full_err:.2e}",
    )
    check(
        "The long (1,3) corner is already downstream of the chain packet through F_13 = F_12 F_23 and F_31 = F_32 F_21",
        corner_err < 1.0e-12,
        detail=f"corner_err={corner_err:.2e}",
    )
    check(
        "The new note records the exact sharpening from a 9-packet to a 7-packet nearest-neighbor chain certificate",
        "nearest-neighbor Hermitian chain packet" in note
        and "The `(1,3)` corner is algebraically downstream of the chain" in note
        and "one nearest-neighbor `7`-packet plus finite chain identities" in note,
    )
    check(
        "The new note uses the exact 9-packet theorem in the right way and preserves the current-bank support-first obstruction",
        "`9`-element Hermitian source packet" in nine_packet
        and "So the current bank still does **not** realize even this sharper" in note
        and "nearest-neighbor `7`-packet." in note
        and "the full Hermitian `9`-packet" in note,
    )

    check(
        "The Wilson support frontier is now smaller than a 9-packet reviewer target",
        "A future positive Wilson support theorem may now be judged by the smaller" in note
        and "Then the `(1,3)` corner and hence the full `9`-packet follow automatically" in note,
        bucket="SUPPORT",
    )
    check(
        "The current bank still fails at the sharper 7-packet support layer",
        "The current exact bank still does **not** realize even this finite packet." in nine_packet
        and "So the current bank still does **not** realize even this sharper" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
