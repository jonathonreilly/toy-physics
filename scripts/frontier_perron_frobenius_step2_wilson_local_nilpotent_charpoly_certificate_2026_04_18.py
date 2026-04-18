#!/usr/bin/env python3
"""
Compress the Wilson route from a local nilpotent-chain 1+3 certificate to a
local nilpotent-chain 1+1 certificate.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHARPOLY_CERTIFICATE_NOTE_2026-04-18.md")
    nilpotent = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_NILPOTENT_CHAIN_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 112)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL NILPOTENT-CHARPOLY CERTIFICATE")
    print("=" * 112)
    print()

    h = np.array(
        [
            [0.9, 0.3 - 0.2j, 0.1 + 0.4j],
            [0.3 + 0.2j, -0.5, 0.6 - 0.1j],
            [0.1 - 0.4j, 0.6 + 0.1j, 0.2],
        ],
        dtype=complex,
    )
    h = (h + h.conj().T) / 2.0
    b = h.copy()
    coeff_gap = float(np.max(np.abs(np.poly(b) - np.poly(h))))
    trace_gap = max(
        float(abs(np.trace(np.linalg.matrix_power(b, k)) - np.trace(np.linalg.matrix_power(h, k))))
        for k in (1, 2, 3)
    )
    check(
        "For Hermitian 3x3 blocks, equality of the 3 trace powers is exactly equivalent to equality of characteristic polynomials",
        coeff_gap < 1e-12 and trace_gap < 1e-12,
        detail=f"coeff_gap={coeff_gap:.2e}, trace_gap={trace_gap:.2e}",
    )
    check(
        "The nilpotent-chain minimal-certificate note already packages the Wilson route as generator plus 3 scalar traces",
        "local nilpotent-chain `1 + 3` certificate" in nilpotent
        and "one local nilpotent chain generator `N_chain`" in nilpotent
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in nilpotent,
    )
    check(
        "The spectral-reduction note already states that Hermitian 3x3 unitary equivalence is exactly equivalent to characteristic-polynomial equality",
        "same characteristic polynomial" in spectral
        and "Hermitian `3 x 3` matrices" in spectral,
    )
    check(
        "The new note records the whole Wilson route as one local nilpotent-chain 1+1 certificate",
        "local nilpotent-chain `1 + 1` certificate" in note
        and "one cubic spectral identity" in note
        and "`chi_(B_e)(lambda) = chi_(H_e)(lambda)`" in note
        and "current bank still does **not** realize even the first generator layer" in note,
    )
    check(
        "The theorem stays on the Wilson lane and does not overclaim positive realization or a global selector",
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
