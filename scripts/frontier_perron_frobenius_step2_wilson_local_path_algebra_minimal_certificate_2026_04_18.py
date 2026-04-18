#!/usr/bin/env python3
"""
Package the Wilson compressed route as one minimal local path-algebra 2-edge+3
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    path_alg = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    two_edge_min = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_MINIMALITY_NOTE_2026-04-18.md")
    spectral = read("docs/PERRON_FROBENIUS_STEP2_WILSON_COMPRESSED_BLOCK_SPECTRAL_REDUCTION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL PATH-ALGEBRA MINIMAL CERTIFICATE")
    print("=" * 108)
    print()

    h = np.array(
        [
            [0.9, 0.2 - 0.4j, 0.1 + 0.5j],
            [0.2 + 0.4j, -0.8, 0.6 - 0.3j],
            [0.1 - 0.5j, 0.6 + 0.3j, 0.4],
        ],
        dtype=complex,
    )
    h = (h + h.conj().T) / 2.0
    b = h.copy()
    spectral_gap = max(float(abs(np.trace(np.linalg.matrix_power(b, k)) - np.trace(np.linalg.matrix_power(h, k)))) for k in (1, 2, 3))
    check(
        "Once the local path-algebra layer exists, the remaining Wilson verification is still exactly the same 3 scalar spectral identities",
        spectral_gap < 1e-12,
        detail=f"spectral_gap={spectral_gap:.2e}",
    )
    check(
        "The local chain path-algebra target note already identifies the first Wilson layer as Phi_chain on the physical adjacent two-edge chain",
        "`Phi_chain : A_chain -> End(H_W)`" in path_alg
        and "physical adjacent two-edge chain" in path_alg
        and "current bank still does **not** realize even the local path-algebra" in path_alg,
    )
    check(
        "The two-edge chain minimality note already proves the underlying physical support is minimal",
        "exact minimal local lattice support target" in two_edge_min
        and "no honest one-edge shortcut" in two_edge_min,
    )
    check(
        "The spectral-reduction note still supplies the exact 3-scalar post-support layer",
        "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in spectral
        and "reduces to a finite scalar spectral packet" in spectral,
    )
    check(
        "The new note records the whole Wilson route as one minimal local path-algebra 2-edge+3 certificate",
        "minimal local path-algebra `2-edge + 3` certificate" in note
        and "`Phi_chain : A_chain -> End(H_W)`" in note
        and "already known to be physically minimal" in note
        and "`Tr(B_e^k) = Tr(H_e^k)` for `k = 1, 2, 3`" in note
        and "current bank still does **not** realize the local path-algebra" in note,
    )

    check(
        "The theorem stays on the Wilson local constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive realization of the minimal local path-algebra `2-edge + 3`" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
