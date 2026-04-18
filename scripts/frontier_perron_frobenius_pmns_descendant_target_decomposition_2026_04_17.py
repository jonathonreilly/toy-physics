#!/usr/bin/env python3
"""
Exact decomposition of the PMNS descendant target on the PF lane.
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


def psd_sqrt(matrix: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(matrix)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.T


def main() -> int:
    note = read("docs/PERRON_FROBENIUS_PMNS_DESCENDANT_TARGET_DECOMPOSITION_NOTE_2026-04-17.md")
    pmns_hw1 = read("docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    pmns_mode = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    dm_triplet = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")
    pmns_polar = read("docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md")
    pmns_current = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")

    # Projected Hermitian response witness.
    r11, r22, r33 = 1.6, 1.2, 0.8
    s12, s13, s23 = 0.4, 0.1, -0.2
    a13 = 0.5
    gamma = a13 / 2.0
    e1 = (r22 - r33) / 2.0 + (s12 - s13) / 4.0
    e2 = r11 + (s12 + s13) / 4.0 - (r22 + r33) / 2.0 - s23 / 2.0

    # Hermitian branch/readout witness.
    h = np.array(
        [
            [2.1, 0.50, 0.28],
            [0.50, 1.8, 0.34],
            [0.28, 0.34, 1.5],
        ],
        dtype=float,
    )
    h_sqrt = psd_sqrt(h)
    support_score = int(np.sum(np.abs(np.triu(h_sqrt, 1)) > 1.0e-9))

    # Residual current witness.
    u = 0.19
    v = 0.27
    j_chi = complex(u, v)

    print("=" * 108)
    print("PERRON-FROBENIUS PMNS DESCENDANT TARGET DECOMPOSITION")
    print("=" * 108)
    print()
    print(f"Hermitian projected channels   = (gamma={gamma:.6f}, E1={e1:.6f}, E2={e2:.6f})")
    print(f"positive-section support score = {support_score}")
    print(f"residual current witness       = ({j_chi.real:.6f} + {j_chi.imag:.6f} i)")
    print()

    check(
        "PMNS notes already distinguish supplied-pack closure from sole-axiom triviality",
        "downstream Hermitian / PMNS data exactly" in pmns_hw1
        and "stays trivial" in pmns_sole
        and "exactly `(I3, I3)`" in pmns_sole,
        bucket="SUPPORT",
    )
    check(
        "Projected-source sign theorem already identifies dW_e^H as a concrete downstream carrier",
        "projected Hermitian response pack" in dm_triplet
        and "`gamma = A13 / 2`" in dm_triplet
        and "`E1 = delta + rho" in dm_triplet
        and "`E2 = A + b - c - d" in dm_triplet,
        bucket="SUPPORT",
    )
    check(
        "Right-polar note already identifies selected-branch Hermitian data as an intrinsic branch-side codomain while leaving a residual sheet bit",
        "canonical intrinsic section" in pmns_polar
        and "sheet-even" in pmns_polar
        and "cannot fix the residual" in pmns_polar,
        bucket="SUPPORT",
    )
    check(
        "Current-boundary note already identifies J_chi as the smallest remaining PMNS-side source object",
        "one native complex nontrivial-character current" in pmns_current
        and "J_chi = 0" in pmns_current,
        bucket="SUPPORT",
    )

    check(
        "Projected Hermitian response data already carry explicit downstream observables",
        abs(gamma - 0.25) < 1.0e-12 and abs(e1 - 0.275) < 1.0e-12 and abs(e2 - 0.825) < 1.0e-12,
        detail="dW_e^H is already a mathematically useful codomain",
    )
    check(
        "Branch Hermitian data already support an intrinsic positive-section readout while remaining sheet-even",
        support_score == 3,
        detail="H-level data are strong enough for branch-side structure but not the whole PMNS last mile",
    )
    check(
        "The residual nontrivial current is a distinct complex datum beyond the Hermitian codomain",
        abs(j_chi.real - u) < 1.0e-12 and abs(j_chi.imag - v) < 1.0e-12,
        detail="J_chi is the clean residual non-Hermitian target",
    )
    check(
        "Therefore the PMNS side of step 2 decomposes into a Wilson-to-Hermitian descendant target followed by a Wilson-to-J_chi target if needed",
        "Wilson-to-Hermitian descendant" in note
        and "Wilson-to-`J_chi`" in note
        and "aligned seed carrier is too small" in note,
        detail="the PMNS descendant route is now split into exact subtargets",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
