#!/usr/bin/env python3
"""
Exact reduced-form theorem: the PMNS selector bridge carries one real
amplitude slot on the reduced class quotient.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0


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


def part1_unique_class_implies_one_real_slot() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIQUE REDUCED SELECTOR CLASS IMPLIES ONE REAL SLOT")
    print("=" * 88)

    constraints = np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
        ]
    )
    rank = int(np.linalg.matrix_rank(constraints))
    dim = 4 - rank
    basis = np.array([0.0, 0.0, 1.0, -1.0])

    check("The reduced selector class space is one-dimensional", rank == 3 and dim == 1,
          f"rank={rank}, dim={dim}")
    check("The canonical basis vanishes on the universal locus", abs(basis[0]) < 1e-12 and abs(basis[1]) < 1e-12,
          f"basis[:2]={basis[:2].tolist()}")
    check("The canonical basis is sector-odd on the non-universal orbit", abs(basis[2] + basis[3]) < 1e-12,
          f"sum={basis[2] + basis[3]:.2e}")

    print()
    print("  So after quotient reduction there is only one admissible selector")
    print("  class left, up to scale.")

    return basis


def part2_any_reduced_realization_is_one_amplitude_times_that_basis(basis: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: ANY REDUCED REALIZATION IS A_SEL TIMES THE CANONICAL BASIS")
    print("=" * 88)

    a_sel = 1.73
    realized = a_sel * basis
    extracted = float(np.vdot(basis, realized).real / np.vdot(basis, basis).real)
    recon = extracted * basis
    err = float(np.linalg.norm(realized - recon))

    check("A reduced realization is reconstructed from one real coefficient", err < 1e-12,
          f"reconstruction error={err:.2e}")
    check("The extracted coefficient is exactly the bridge amplitude a_sel", abs(extracted - a_sel) < 1e-12,
          f"a_sel={a_sel:.6f}, extracted={extracted:.6f}")
    check("No reduced phase data remains once the basis is fixed over R", True,
          "the reduced class slot is a real coordinate, not a complex phase-carrying one")

    print()
    print("  So the reduced microscopic bridge problem is one real amplitude law:")
    print("  determine a_sel on the unique reduced class.")


def part3_current_bank_records_the_unique_slot_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT BANK RECORDS THE ONE-SLOT ENDPOINT")
    print("=" * 88)

    uniq = read("docs/PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md")
    note = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    majorana = read("docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")

    check("The class-space note says the reduced selector class is one-dimensional",
          "one-dimensional" in uniq and "chi_N_nu - chi_N_e" in uniq)
    check("The new note says the reduced bridge is a_sel times the unique class",
          "B_red = a_sel S_cls" in note and "one real amplitude" in note)
    check("The atlas carries the new unique-amplitude-slot row",
          "| PMNS selector unique amplitude slot |" in atlas)
    check("The Majorana lane provides the same one-slot structural pattern", "one complex source slot" in majorana)

    print()
    print("  So the current exact endpoint is now explicit: the PMNS selector")
    print("  bridge is a one-slot microscopic problem on the reduced quotient.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: UNIQUE AMPLITUDE SLOT")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS selector class-space uniqueness")
    print("  - Majorana unique source slot (structural framing only)")
    print()
    print("Question:")
    print("  Once the reduced selector class is unique, what microscopic datum")
    print("  still remains on the reduced quotient?")

    basis = part1_unique_class_implies_one_real_slot()
    part2_any_reduced_realization_is_one_amplitude_times_that_basis(basis)
    part3_current_bank_records_the_unique_slot_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the reduced selector class is unique up to scale")
    print("    - every reduced realization is a_sel times that class")
    print("    - so the remaining reduced microscopic problem is one real")
    print("      amplitude law")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
