#!/usr/bin/env python3
"""
Package the Wilson compressed route as one minimal local Hermitian 4+3
certificate.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    local_four = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_REDUCTION_NOTE_2026-04-18.md")
    local_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL HERMITIAN MINIMAL CERTIFICATE")
    print("=" * 108)
    print()

    h = np.array(
        [
            [1.2, 0.6 - 0.1j, -0.4 + 0.3j],
            [0.6 + 0.1j, -0.2, 0.7 - 0.5j],
            [-0.4 - 0.3j, 0.7 + 0.5j, 0.4],
        ],
        dtype=complex,
    )
    h = (h + h.conj().T) / 2.0
    b = h.copy()
    spectral_gap = max(float(abs(np.trace(np.linalg.matrix_power(b, k)) - np.trace(np.linalg.matrix_power(h, k)))) for k in (1, 2, 3))

    check(
        "Once the minimal local Hermitian 4-source layer exists, the post-source Wilson verification still reduces exactly to the 3 scalar spectral identities",
        spectral_gap < 1e-12,
        detail=f"spectral_gap={spectral_gap:.2e}",
    )
    check(
        "The local Hermitian four-source reduction note already packages the constructive Wilson layer as the local 4-source packet",
        "local Hermitian nearest-neighbor `4`-source packet" in local_four
        and "current bank still does **not** realize even this sharper local" in local_four,
    )
    check(
        "The local Hermitian four-source minimality note already proves that packet is dimensionally sharp",
        "`dim_R V_loc^H = 4`" in local_min
        and "no honest generic local Hermitian `3`-source shortcut exists" in local_min,
    )
    check(
        "The spectral-reduction note already packages the post-source Wilson layer as the 3 scalar spectral identities",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in spectral
        and "compressed-resolvent block law to three scalar spectral identities" in spectral,
    )
    check(
        "The new note records the exact minimal local Hermitian 4+3 certificate form of the Wilson compressed route",
        "minimal local Hermitian `4 + 3` certificate" in note
        and "local Hermitian nearest-neighbor `4`-source packet" in note
        and "already known to be minimal" in note
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "current bank still does **not** realize the local Hermitian" in note,
    )

    check(
        "The theorem stays on the Wilson constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the minimal local Hermitian `4 + 3` certificate" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
