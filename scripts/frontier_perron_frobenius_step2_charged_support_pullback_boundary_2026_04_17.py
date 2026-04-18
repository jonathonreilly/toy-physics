#!/usr/bin/env python3
"""
Boundary excluding support-pullback realization of the missing Wilson-side
charged embedding/compression object.
"""

from __future__ import annotations

from pathlib import Path


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
    note = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")
    projector_interface = read("docs/DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    site_phase = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    shape = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md")
    nonreal = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 CHARGED-SUPPORT PULLBACK BOUNDARY")
    print("=" * 108)
    print()

    check(
        "PMNS projector-interface note fixes E_e only as a PMNS-side lepton support label",
        "the lepton supports `E_nu` and `E_e` are fixed" in projector_interface,
        bucket="SUPPORT",
    )
    check(
        "Charged source-response note fixes dW_e^H as Schur_{E_e}(D_-) on the charged microscopic side",
        "`L_e = Schur_{E_e}(D_-)`" in charged and "charged-lepton support `E_e ⊂ E_-`" in charged,
        bucket="SUPPORT",
    )
    check(
        "Site-phase / cube-shift intertwiner note states its safe role is support transport only on taste-cube / BZ-corner support",
        "taste-cube operator algebra and the lattice BZ-corner subspace are exactly" in site_phase
        and "Its safe role is narrower" in site_phase,
        bucket="SUPPORT",
    )
    check(
        "Bridge-candidate-shape note excludes support-only transport as the missing charged bridge",
        "support-only intertwiner cannot honestly be the missing charged-sector" in shape
        or "support-only candidate classes" in shape,
        bucket="SUPPORT",
    )
    check(
        "Current-bank nonrealization note says the present support bank still does not realize the missing cross-sector descendant law",
        "support intertwiners" in nonreal
        and "safe role is support transport only" in nonreal
        and "does **not** already contain the missing" in nonreal,
        bucket="SUPPORT",
    )

    check(
        "Charged-support pullback boundary note records that E_e is fixed on the PMNS/charged microscopic side, not yet on the Wilson parent space",
        "fixed support label, but it is fixed on the charged PMNS / DM" in note
        and "not yet on the Wilson parent space" in note,
    )
    check(
        "Charged-support pullback boundary note records that the current support intertwiner only moves statements between taste-cube and BZ-corner support",
        "moves statements only between taste-cube" in note and "BZ-corner support" in note,
    )
    check(
        "Charged-support pullback boundary note concludes the missing Wilson-side charged embedding cannot be obtained as a pure support pullback",
        "be obtained as a pure pullback of `E_e` through the current exact support bank" in note,
        detail="support transport shortcut is closed",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
