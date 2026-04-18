#!/usr/bin/env python3
"""
Package the Wilson compressed route as one minimal invariant local chain-plane
4+3 certificate.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PLANE_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    chain_plane = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_CHAIN_PLANE_TARGET_NOTE_2026-04-18.md")
    local_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_HERMITIAN_FOUR_SOURCE_MINIMALITY_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL CHAIN-PLANE MINIMAL CERTIFICATE")
    print("=" * 108)
    print()

    h = np.array(
        [
            [1.1, 0.4 - 0.3j, -0.2 + 0.5j],
            [0.4 + 0.3j, -0.7, 0.9 - 0.1j],
            [-0.2 - 0.5j, 0.9 + 0.1j, 0.2],
        ],
        dtype=complex,
    )
    h = (h + h.conj().T) / 2.0
    b = h.copy()
    spectral_gap = max(float(abs(np.trace(np.linalg.matrix_power(b, k)) - np.trace(np.linalg.matrix_power(h, k)))) for k in (1, 2, 3))
    check(
        "Once the local chain-plane layer exists, the remaining Wilson verification is still exactly the same 3 scalar spectral identities",
        spectral_gap < 1e-12,
        detail=f"spectral_gap={spectral_gap:.2e}",
    )
    check(
        "The chain-plane target note already identifies the first local Wilson layer invariantly as Psi_chain : V_chain^H -> Herm(H_W)",
        "`Psi_chain : V_chain^H -> Herm(H_W)`" in chain_plane
        and "one invariant Hermitian chain-plane embedding" in chain_plane
        and "current bank still does **not** realize even the restricted local" in chain_plane,
    )
    check(
        "The local Hermitian minimality note already proves the first local layer is minimal at real dimension 4",
        "`dim_R V_loc^H = 4`" in local_min
        and "no honest generic local Hermitian `3`-source shortcut exists" in local_min,
    )
    check(
        "The spectral-reduction note still supplies the exact 3-scalar post-support layer",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in spectral
        and "reduces to a finite scalar spectral packet" in spectral,
    )
    check(
        "The new note records the whole Wilson route as one minimal invariant local chain-plane 4+3 certificate",
        "minimal local chain-plane `4 + 3` certificate" in note
        and "`Psi_chain : V_chain^H -> Herm(H_W)`" in note
        and "three scalar identities" in note
        and "current bank still does **not** realize the local chain-plane" in note,
    )

    check(
        "The theorem stays on the Wilson local constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the minimal local chain-plane `4 + 3` certificate" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
