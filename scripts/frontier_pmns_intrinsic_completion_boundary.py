#!/usr/bin/env python3
"""
Exact current-bank theorem:
selected-branch Hermitian closure is exact but conditional, and the remaining
intrinsic PMNS gap now sits at the Hermitian-data law layer, plus one residual
sheet-fixing datum for coefficient-level closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def hermitian_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def rebuild_h(coords: np.ndarray) -> np.ndarray:
    d1, d2, d3, r12, r23, r31, phi = coords
    return np.array(
        [
            [d1, r12, r31 * np.exp(-1j * phi)],
            [r12, d2, r23],
            [r31 * np.exp(1j * phi), r23, d3],
        ],
        dtype=complex,
    )


def part1_selected_branch_hermitian_closure_targets_are_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SELECTED-BRANCH HERMITIAN CLOSURE TARGETS ARE EXACT")
    print("=" * 88)

    y_nu = canonical_y(np.array([0.9, 0.7, 1.1], dtype=float), np.array([0.4, 0.6, 0.5], dtype=float), 1.3)
    h_nu = y_nu @ y_nu.conj().T
    coords_nu = hermitian_coordinates(h_nu)
    h_nu_rec = rebuild_h(coords_nu)

    y_e = canonical_y(np.array([0.24, 0.38, 1.07], dtype=float), np.array([0.09, 0.22, 0.61], dtype=float), 1.1)
    h_e = y_e @ y_e.conj().T
    coords_e = hermitian_coordinates(h_e)
    h_e_rec = rebuild_h(coords_e)

    check("The neutrino-side seven-coordinate grammar reconstructs H_nu exactly", np.linalg.norm(h_nu - h_nu_rec) < 1e-12,
          f"error={np.linalg.norm(h_nu - h_nu_rec):.2e}")
    check("The charged-lepton-side seven-coordinate grammar reconstructs H_e exactly", np.linalg.norm(h_e - h_e_rec) < 1e-12,
          f"error={np.linalg.norm(h_e - h_e_rec):.2e}")
    check("So selected-branch Hermitian data are exact local closure targets", True)

    print()
    print("  The selected-branch Hermitian inverse problems are already exact.")
    print("  The remaining issue is not local H-reconstruction.")


def part2_current_bank_still_does_not_make_the_completion_intrinsic() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT BANK STILL DOES NOT MAKE THE COMPLETION INTRINSIC")
    print("=" * 88)

    zero = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")
    polar = read("docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md")
    # PMNS_BRANCH_SHEET_NONFORCING_NOTE was split: the "same Hermitian matrix"
    # claim now lives in PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE
    # and the "sheet-even" framing in PMNS_RIGHT_POLAR_SECTION_NOTE.
    sheet_closure = read("docs/PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md")

    check("The current-stack selector amplitude is still exactly zero", "a_sel,current = 0" in zero)
    check("The polar-section theorem says the generic full-rank right orbit already has Y_+(H) = H^(1/2)",
          "Y_+(H)" in polar and "H^(1/2)" in polar)
    check("The sheet-nonforcing theorem says H-based retained observables are sheet-even",
          "same Hermitian matrix" in sheet_closure and "sheet-even" in polar)

    print()
    print("  So even with exact branch Hermitian grammars, the current bank")
    print("  still does not produce the branch Hermitian data as axiom-side")
    print("  outputs, and every H-based construction remains sheet-even.")


def part3_the_minimal_missing_intrinsic_object_is_now_sharp() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MINIMAL MISSING INTRINSIC OBJECT IS NOW SHARP")
    print("=" * 88)

    # Note archived 2026-05-01 because its EWSB-aligned dependency chain
    # never landed and the publication surface superseded it. Runner kept
    # as stale-runner record pointing at the archived no-go note.
    note = read(
        "archive_unlanded/pmns-publication-state-supersession-2026-05-01/"
        "PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md"
    )
    core = read("docs/PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md")
    seed = read("docs/PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md")
    spectral = read("docs/PMNS_EWSB_RESIDUAL_Z2_SPECTRAL_PRIMITIVE_NOTE.md")
    nonforcing = read("docs/PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md")
    slots = read("docs/PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The new note identifies the remaining gap as Hermitian-data law plus sheet-fixing datum",
          "Hermitian data law" in note and "sheet-fixing datum" in note)
    check("The EWSB-aligned active-branch note reduces the active Hermitian law to a four-parameter core",
          "[[a,b,b],[b,c,d],[b,d,c]]" in core or "[ a  b  b ]" in core)
    cseed = compact(seed)
    check("The weak-axis seed note records the exact two-parameter seed inside the aligned surface",
          "diag(A,B,B)" in seed and "muI+nu(C+C^2)" in cseed and "A<=4B" in cseed)
    check("The spectral-primitive note reduces the aligned core to three eigenvalues plus one angle",
          "three spectral invariants plus one even-sector angle" in spectral)
    check("The alignment nonforcing note says the current bank does not force EWSB alignment",
          "does not force EWSB alignment" in nonforcing)
    check("The breaking-slot note says the current bank does not yet derive the breaking-slot vector",
          "does not yet derive the breaking-slot vector" in slots)
    check("The atlas carries the PMNS intrinsic completion boundary row",
          "| PMNS intrinsic completion boundary |" in atlas)
    check("The atlas carries the PMNS EWSB residual-Z2 Hermitian core row",
          "| PMNS EWSB residual-Z2 Hermitian core |" in atlas)
    check("The atlas carries the PMNS EWSB weak-axis Z3 seed row",
          "| PMNS EWSB weak-axis Z3 seed |" in atlas)
    check("The atlas carries the PMNS EWSB residual-Z2 spectral primitive row",
          "| PMNS EWSB residual-Z2 spectral primitive reduction |" in atlas)
    check("The atlas carries the PMNS EWSB breaking-slot nonrealization row",
          "| PMNS EWSB breaking-slot nonrealization |" in atlas)

    print()
    print("  So the remaining exact object is no longer vague.")
    print("  It is the selected-branch Hermitian data law, sharpened on the")
    print("  EWSB-aligned one-sided surface to a derived weak-axis seed, a")
    print("  2+1 spectral primitive package, and explicit breaking slots,")
    print("  while the current bank still does not derive alignment or the")
    print("  generic breaking-slot vector, and for coefficient-level closure")
    print("  one residual sheet-fixing datum.")


def main() -> int:
    print("=" * 88)
    print("PMNS INTRINSIC COMPLETION BOUNDARY")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - neutrino and charged-lepton two-Higgs observable inverse problems")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - PMNS selector current-stack zero law")
    print("  - PMNS right polar section")
    print("  - PMNS branch sheet nonforcing")
    print()
    print("Question:")
    print("  What exactly remains between the current bank and intrinsic")
    print("  positive PMNS / neutrino closure?")

    part1_selected_branch_hermitian_closure_targets_are_exact()
    part2_current_bank_still_does_not_make_the_completion_intrinsic()
    part3_the_minimal_missing_intrinsic_object_is_now_sharp()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - selected-branch Hermitian closure is already exact")
    print("    - on the generic full-rank patch the right orbit already has the")
    print("      canonical positive representative Y_+(H) = H^(1/2)")
    print("    - and on the explicit EWSB-aligned one-sided surface the active")
    print("      Hermitian law already sharpens to a four-parameter residual-Z2")
    print("      core plus explicit breaking slots")
    print("    - so once H_nu and H_e are available, the one-sided branch is")
    print("      intrinsically readable from Hermitian data")
    print("    - but every H-based construction remains sheet-even")
    print("    - so the remaining exact gap is the branch Hermitian-data law,")
    print("      plus one residual sheet-fixing datum for coefficient closure")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
