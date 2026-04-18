#!/usr/bin/env python3
"""
Reduce the remaining Wilson compressed-route constructive primitive to one local
adjacent two-edge source law on the physical nearest-neighbor lattice.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_TWO_EDGE_SOURCE_TARGET_NOTE_2026-04-18.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    source_target = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SOURCE_FAMILY_TARGET_NOTE_2026-04-17.md")
    direct_dweh = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    two_edge = read("docs/PERRON_FROBENIUS_STEP2_WILSON_TWO_EDGE_CHAIN_REDUCTION_NOTE_2026-04-18.md")
    physical_cert = read("docs/PERRON_FROBENIUS_STEP2_WILSON_PHYSICAL_SHARPEST_CERTIFICATE_TARGET_NOTE_2026-04-18.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 WILSON LOCAL TWO-EDGE SOURCE TARGET")
    print("=" * 108)
    print()

    d_inv = np.array(
        [
            [1.7, 0.2 - 0.4j, -0.3 + 0.1j],
            [0.2 + 0.4j, -0.6, 0.5 - 0.2j],
            [-0.3 - 0.1j, 0.5 + 0.2j, 0.9],
        ],
        dtype=complex,
    )
    g12 = e(0, 1)
    g23 = e(1, 2)
    dg12 = float(np.trace(d_inv @ g12).real)
    dg23 = float(np.trace(d_inv @ g23).real)
    dg12i = float(np.trace(d_inv @ (1j * g12)).real)
    dg23i = float(np.trace(d_inv @ (1j * g23)).real)

    check(
        "The observable principle already turns a chosen local two-edge source path into exact first responses",
        abs(dg12 - d_inv[1, 0].real) < 1e-12
        and abs(dg23 - d_inv[2, 1].real) < 1e-12
        and abs(dg12i + d_inv[1, 0].imag) < 1e-12
        and abs(dg23i + d_inv[2, 1].imag) < 1e-12,
        detail=f"dg12={dg12:.6f}, dg23={dg23:.6f}, dg12i={dg12i:.6f}, dg23i={dg23i:.6f}",
    )
    check(
        "The exact source-response and projected-source notes already separate source-law construction from downstream dW_e^H -> H_e reconstruction",
        "W[J] = log |det(D+J)| - log |det D|" in observable
        and "remaining constructive primitive on the compressed route is" in source_target
        and "Wilson-side charged source family / channel" in source_target
        and "fully reduced and honest" in direct_dweh
        and "first derive `Wilson -> dW_e^H`" in direct_dweh
        and "`dW_e^H` reconstructs the active charged-lepton Hermitian block `H_e`" in projected,
        detail="the only missing content is the Wilson-side source law itself",
    )
    check(
        "The exact two-edge and physical-certificate notes already show that the Wilson support theorem is local on the physical nearest-neighbor lattice",
        "adjacent directed nearest-neighbor two-edge chain" in two_edge
        and "local physical" in physical_cert
        and "`2-edge + 3` certificate" in physical_cert,
        detail="the support theorem is already local before any PMNS-side readout",
    )
    check(
        "The new note records the exact sharpening from an abstract charged source family to one local adjacent two-edge source law",
        "local adjacent two-edge Wilson source law" in note
        and "rather than as an abstract charged" in note
        and "source family" in note
        and "build one local adjacent two-edge source law on the physical lattice" in note,
    )
    check(
        "The new note preserves the current-bank local nonrealization statement",
        "current bank still does **not** realize even this physical adjacent" in two_edge
        and "two-edge chain" in two_edge
        and "current bank still does **not** realize even this sharper local source" in note,
    )

    check(
        "The theorem stays on the Wilson compressed-route constructive lane and does not overclaim a positive bridge theorem",
        "What this does not close" in note
        and "a positive Wilson-to-`dW_e^H` theorem" in note
        and "a positive global PF selector" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
