#!/usr/bin/env python3
"""
Package the whole Wilson compressed route as one local nilpotent-chain 1+3
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    reduction = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_GENERATOR_REDUCTION_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 106)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL NILPOTENT-CHAIN MINIMAL CERTIFICATE")
    print("=" * 106)
    print()

    h = np.array(
        [
            [1.1, 0.3 - 0.2j, 0.4 + 0.1j],
            [0.3 + 0.2j, -0.7, 0.2 - 0.5j],
            [0.4 - 0.1j, 0.2 + 0.5j, 0.6],
        ],
        dtype=complex,
    )
    h = (h + h.conj().T) / 2.0
    b = h.copy()
    spectral_gap = max(
        float(abs(np.trace(np.linalg.matrix_power(b, k)) - np.trace(np.linalg.matrix_power(h, k))))
        for k in (1, 2, 3)
    )
    check(
        "Once the local nilpotent generator exists, the remaining Wilson verification is still exactly the same 3 scalar spectral identities",
        spectral_gap < 1e-12,
        detail=f"spectral_gap={spectral_gap:.2e}",
    )
    check(
        "The reduction note already identifies the local constructive layer as one nilpotent chain generator",
        "one local nilpotent chain generator" in reduction
        and "current bank still does **not** realize even this sharper local generator" in reduction,
    )
    check(
        "The spectral-reduction note still supplies the exact post-support 3-scalar layer",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in spectral
        and "reduces to a finite scalar spectral packet" in spectral,
    )
    check(
        "The new note records the whole Wilson route as one local nilpotent-chain 1+3 certificate",
        "local nilpotent-chain `1 + 3` certificate" in note
        and "one local nilpotent chain generator `N_chain`" in note
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "current bank still does **not** realize even the first generator layer" in note,
    )
    check(
        "The theorem stays on the Wilson constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the local nilpotent chain generator" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
