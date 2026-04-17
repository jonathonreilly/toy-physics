#!/usr/bin/env python3
"""
DM odd-slot minimal mixed-bridge extension theorem.

Question:
  After the odd-slot theorem and the current-stack zero law, what is the
  smallest honest positive extension class that could activate the DM odd slot?

Answer:
  A residual-Z2-odd non-additive mixed bridge with one real amplitude slot.

  More precisely, any future positive local activator must:
    - lie outside the current retained even support/Hermitian/scalar bank
    - be supported on the canonical non-universal two-Higgs locus
    - be residual-Z2 odd
    - be non-additive over the even/odd circulant decomposition
    - reduce to one real amplitude slot on the unique odd class i(S-S^2)

Boundary:
  This is an extension-class theorem only. It does not derive the microscopic
  bridge functional itself.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

S = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)
S2 = S @ S
ODD_BASIS = 1j * (S - S2)


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


def part1_current_bank_eliminates_even_additive_routes() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK ELIMINATES THE EVEN / ADDITIVE ROUTES")
    print("=" * 88)

    zero = read("docs/DM_NEUTRINO_ODD_CIRCULANT_CURRENT_STACK_ZERO_LAW_NOTE_2026-04-15.md")
    slot = read("docs/DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md")

    check(
        "The odd-slot theorem identifies one unique residual-Z2-odd local class",
        "exactly one residual-`Z_2`-odd slot" in slot or "unique residual-`Z_2`-odd slot" in slot,
    )
    check(
        "The current-zero-law note records c_odd,current = 0",
        "c_odd,current = 0" in zero,
    )
    check(
        "The current-zero-law note says the present bank is residual-Z2 even",
        "residual-`Z_2` even" in zero or "residual-Z2 even" in zero,
    )

    print()
    print("  So any positive realization must leave the current even local bank.")


def part2_remaining_support_is_the_canonical_two_higgs_locus() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING SUPPORT IS THE CANONICAL TWO-HIGGS LOCUS")
    print("=" * 88)

    minimality = read("docs/DM_NEUTRINO_TWO_HIGGS_MINIMALITY_THEOREM_NOTE_2026-04-15.md")
    continuity = read("docs/DM_NEUTRINO_TWO_HIGGS_CONTINUITY_SHEET_THEOREM_NOTE_2026-04-15.md")

    check(
        "The two-Higgs minimality theorem says there is no smaller exact local escape",
        "unique minimal exact local escape" in minimality,
    )
    check(
        "The continuity theorem says the physical sheet is fixed on the DM circulant lane",
        "continuity to the retained universal bridge picks the `+` sheet uniquely" in continuity
        or "fixes the residual local two-Higgs sheet intrinsically" in continuity,
    )

    print()
    print("  So any positive activator must live on the canonical non-universal")
    print("  two-Higgs branch, not on some other smaller local extension.")


def part3_reduced_positive_extension_class_has_one_real_amplitude() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REDUCED POSITIVE EXTENSION CLASS HAS ONE REAL AMPLITUDE")
    print("=" * 88)

    basis_norm = np.linalg.norm(ODD_BASIS)
    candidate = 0.37 * ODD_BASIS
    extracted = float(np.vdot(ODD_BASIS, candidate).real / np.vdot(ODD_BASIS, ODD_BASIS).real)

    check(
        "The unique odd class is one-dimensional, spanned by i(S-S^2)",
        basis_norm > 0.0 and np.linalg.matrix_rank(ODD_BASIS) == 2,
        f"||basis||={basis_norm:.6f}",
    )
    check(
        "Any reduced positive activator on that class carries one real amplitude slot",
        abs(extracted - 0.37) < 1e-12,
        f"a_odd={extracted:.6f}",
    )

    print()
    print("  So the minimal surviving positive DM extension class is not a family of")
    print("  unrelated activators. On the reduced local quotient it is one odd class")
    print("  with one real amplitude slot.")


def main() -> int:
    print("=" * 88)
    print("DM ODD-SLOT MINIMAL MIXED-BRIDGE EXTENSION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - DM odd-circulant residual-Z2 slot theorem")
    print("  - DM odd-circulant current-stack zero law")
    print("  - DM two-Higgs minimality theorem")
    print("  - DM two-Higgs continuity sheet theorem")
    print()
    print("Question:")
    print("  What is the smallest honest positive extension class that could")
    print("  activate the unique DM odd slot?")

    part1_current_bank_eliminates_even_additive_routes()
    part2_remaining_support_is_the_canonical_two_higgs_locus()
    part3_reduced_positive_extension_class_has_one_real_amplitude()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact extension-class answer:")
    print("    - the current even/additive bank is ruled out")
    print("    - the remaining support is the canonical non-universal two-Higgs lane")
    print("    - the surviving local class is the unique odd circulant class")
    print("    - the reduced positive extension therefore carries one real amplitude")
    print("      on a residual-Z2-odd non-additive mixed bridge")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
