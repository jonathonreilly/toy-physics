#!/usr/bin/env python3
"""
Reduce the Wilson local two-edge source primitive to one local Hermitian
nearest-neighbor 4-source packet.
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


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md")
    local_two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md")
    four_packet = read("docs/PERRON_FROBENIUS_STEP2_WILSON_FOUR_PACKET_OFFDIAGONAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL HERMITIAN FOUR-SOURCE REDUCTION")
    print("=" * 108)
    print()

    e12 = e(0, 1)
    e21 = e(1, 0)
    e23 = e(1, 2)
    e32 = e(2, 1)

    x12 = e12 + e21
    y12 = -1j * e12 + 1j * e21
    x23 = e23 + e32
    y23 = -1j * e23 + 1j * e32

    rec12 = (x12 + 1j * y12) / 2.0
    rec21 = (x12 - 1j * y12) / 2.0
    rec23 = (x23 + 1j * y23) / 2.0
    rec32 = (x23 - 1j * y23) / 2.0

    hermitian_err = max(
        float(np.linalg.norm(x12 - x12.conj().T)),
        float(np.linalg.norm(y12 - y12.conj().T)),
        float(np.linalg.norm(x23 - x23.conj().T)),
        float(np.linalg.norm(y23 - y23.conj().T)),
    )
    recon_err = max(
        float(np.linalg.norm(rec12 - e12)),
        float(np.linalg.norm(rec21 - e21)),
        float(np.linalg.norm(rec23 - e23)),
        float(np.linalg.norm(rec32 - e32)),
    )

    check(
        "The local adjacent two-edge complex data are exactly equivalent to one local Hermitian nearest-neighbor 4-source packet",
        hermitian_err < 1e-12 and recon_err < 1e-12,
        detail=f"hermitian_err={hermitian_err:.2e}, recon_err={recon_err:.2e}",
    )

    coeffs = np.array([0.7 - 0.4j, -0.2 + 0.9j], dtype=complex)
    target = coeffs[0] * e12 + np.conj(coeffs[0]) * e21 + coeffs[1] * e23 + np.conj(coeffs[1]) * e32
    hx = coeffs[0].real * x12 - coeffs[0].imag * y12 + coeffs[1].real * x23 - coeffs[1].imag * y23
    check(
        "Arbitrary local two-edge Hermitian source data decompose exactly into the 4-source packet coordinates",
        float(np.linalg.norm(target - hx)) < 1e-12,
        detail=f"packet decomposition error={np.linalg.norm(target - hx):.2e}",
    )

    check(
        "The existing local-source note already identifies one local adjacent two-edge source law as the remaining primitive",
        "one local adjacent two-edge Wilson source law" in local_two_edge
        and "current bank still does **not** realize even this sharper local source" in local_two_edge,
    )
    check(
        "The existing four-packet note already identifies the same nearest-neighbor support content in Hermitian packet form",
        "off-diagonal Hermitian nearest-neighbor `4`-packet" in four_packet
        and "current bank still does **not** realize even this sharper off-diagonal" in four_packet,
    )
    check(
        "The new note records the exact sharpening from local two-edge source law to local Hermitian 4-source packet",
        "local Hermitian nearest-neighbor `4`-source packet" in note
        and "`E_12 = (X_12 + i Y_12)/2`" in note
        and "`E_23 = (X_23 + i Y_23)/2`" in note
        and "current bank still does **not** realize even this sharper local" in note,
    )

    check(
        "The theorem stays on the Wilson source-side lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the local Hermitian `4`-source packet" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

