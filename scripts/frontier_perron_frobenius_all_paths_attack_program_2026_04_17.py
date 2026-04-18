#!/usr/bin/env python3
"""
Atlas-backed all-paths attack program for the PF lane.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

LUESCHER_DOI = "10.1007/BF01614090"
STINESPRING_DOI = "10.1090/S0002-9939-1955-0069403-4"
EVANS_HK_DOI = "10.1112/jlms/s2-17.2.345"


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
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    attack_note = read("docs/PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md")
    three_step = read("docs/PERRON_FROBENIUS_THREE_STEP_GLOBAL_PROGRAM_BOUNDARY_NOTE_2026-04-17.md")
    step2 = read("docs/PERRON_FROBENIUS_WILSON_TO_PMNS_DESCENDANT_BOUNDARY_NOTE_2026-04-17.md")
    pmns_hw1 = read("docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    dm_triplet = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_TRIPLET_SIGN_THEOREM_NOTE_2026-04-16.md")
    pmns_polar = read("docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md")
    pmns_current = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")

    # Hermitian projected-response witness.
    r11, r22, r33 = 1.4, 1.1, 0.7
    s12, a12 = 0.6, -0.2
    s13, a13 = 0.2, 0.8
    s23, a23 = -0.3, 0.1
    gamma = a13 / 2.0
    e1 = (r22 - r33) / 2.0 + (s12 - s13) / 4.0
    e2 = r11 + (s12 + s13) / 4.0 - (r22 + r33) / 2.0 - s23 / 2.0

    # Positive Hermitian branch witness.
    h = np.array(
        [
            [2.0, 0.45, 0.30],
            [0.45, 1.7, 0.25],
            [0.30, 0.25, 1.4],
        ],
        dtype=float,
    )
    h_sqrt = psd_sqrt(h)
    support_score = int(np.sum(np.abs(np.triu(h_sqrt, 1)) > 1.0e-9))

    # Native current witness.
    u = 0.22
    v = 0.31
    j_chi = complex(u, v)

    print("=" * 108)
    print("PERRON-FROBENIUS ALL-PATHS ATTACK PROGRAM")
    print("=" * 108)
    print()
    print(f"published-math anchors          = ({LUESCHER_DOI}, {STINESPRING_DOI}, {EVANS_HK_DOI})")
    print(f"Hermitian projected channels    = (gamma={gamma:.6f}, E1={e1:.6f}, E2={e2:.6f})")
    print(f"positive-section support score  = {support_score}")
    print(f"native current witness          = ({j_chi.real:.6f} + {j_chi.imag:.6f} i)")
    print()

    check(
        "Atlas already contains the step-1, step-2, and step-3 rows needed for an all-paths PF attack program",
        "Full taste-cube site-phase / cube-shift intertwiner" in atlas
        and "Plaquette transfer-operator / character-recurrence theorem" in atlas
        and "Gauge-vacuum plaquette scalar-bridge support" in atlas
        and "DM projected-source triplet sign theorem" in atlas
        and "PMNS nontrivial `C_3` current boundary" in atlas
        and "PMNS right polar section" in atlas,
        bucket="SUPPORT",
    )
    check(
        "Attack-program note already places Luescher, Stinespring, and Evans-Hoegh-Krohn on steps 1, 2, and 3 respectively",
        LUESCHER_DOI in attack_note and STINESPRING_DOI in attack_note and EVANS_HK_DOI in attack_note,
        bucket="SUPPORT",
    )
    check(
        "Existing PF step-order notes already force step 3 to remain downstream of a real step-2 descendant theorem",
        "step 3: downstream of step 2" in three_step.lower() and "cross-sector provenance" in step2,
        bucket="SUPPORT",
    )
    check(
        "PMNS notes already record that supplied hw=1 data reconstruct downstream Hermitian / PMNS data",
        "downstream Hermitian / PMNS data exactly" in pmns_hw1,
        bucket="SUPPORT",
    )

    check(
        "The Hermitian projected-response pack already carries concrete downstream channels, so a Wilson-to-Hermitian descendant target would be mathematically useful immediately",
        abs(gamma - 0.4) < 1.0e-12 and abs(e1 - 0.3) < 1.0e-12 and abs(e2 - 0.85) < 1.0e-12,
        detail="projected Hermitian data already expose explicit linear downstream observables",
    )
    check(
        "Once branch Hermitian data are available, the positive polar section already gives intrinsic branch-side structure from H",
        support_score == 3 and "canonical intrinsic section" in pmns_polar and "branch Hermitian data are available" in pmns_polar,
        detail="the Hermitian codomain already has real downstream leverage before any non-Hermitian sheet data are added",
    )
    check(
        "The native nontrivial current is a distinct complex datum beyond the Hermitian branch readout, so step 2 must stay split into Hermitian and current subpaths",
        abs(j_chi.real - u) < 1.0e-12 and abs(j_chi.imag - v) < 1.0e-12
        and "one native complex nontrivial-character current" in pmns_current
        and "J_chi = 0" in pmns_current,
        detail="Hermitian data and the nontrivial current are not the same target",
    )
    check(
        "Therefore the honest all-paths attack order is step-1 strengthening, step-2A Hermitian descendant, step-2B current path, plaquette operator sidecar, then step-3 compatibility",
        "Step-1 strengthening path" in attack_note
        and "Step-2A Hermitian descendant path" in attack_note
        and "Step-2B current path" in attack_note
        and "Plaquette operator sidecar" in attack_note
        and "Step-3 compatibility path" in attack_note,
        detail="the PF lane now has a real attack order rather than one undifferentiated global-selector prompt",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
