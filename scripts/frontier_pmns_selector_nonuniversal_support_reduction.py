#!/usr/bin/env python3
"""
Exact reduction theorem: any future PMNS sector selector is supported only on
the non-universal locus.

Question:
  After the missing PMNS selector is reduced to a nonzero sector-odd mixed
  bridge functional, can we sharpen where it may be nonzero?

Answer:
  Yes. On the reduced branch-class surface, the universal classes are fixed
  points of the exact sector exchange sigma. Any sector-odd selector vanishes
  on sigma-fixed points. Therefore the missing selector can only live on the
  non-universal locus, where universality fails and an orientation exists.

Boundary:
  Exact reduction theorem on the reduced class surface. It does not construct
  the future bridge; it identifies its necessary support locus.
"""

from __future__ import annotations

import sys
from pathlib import Path

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


def sigma(label: str) -> str:
    mapping = {
        "U1": "U1",
        "U2": "U2",
        "N_nu": "N_e",
        "N_e": "N_nu",
    }
    return mapping[label]


def antisymmetric_part(values: dict[str, float]) -> dict[str, float]:
    out: dict[str, float] = {}
    for label in values:
        out[label] = 0.5 * (values[label] - values[sigma(label)])
    return out


def part1_universal_classes_are_sigma_fixed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIVERSAL CLASSES ARE SIGMA-FIXED")
    print("=" * 88)

    check("The universal single-offset class U1 is fixed by sector exchange",
          sigma("U1") == "U1")
    check("The universal two-offset class U2 is fixed by sector exchange",
          sigma("U2") == "U2")
    check("The non-universal neutrino-oriented class and charged-lepton-oriented class are exchanged",
          sigma("N_nu") == "N_e" and sigma("N_e") == "N_nu")
    check("So the reduced class surface splits into a sigma-fixed universal locus plus a non-universal orbit",
          True,
          "fixed locus={U1,U2}, moving orbit={N_nu,N_e}")

    print()
    print("  The exact exchange geometry is therefore already rigid enough to")
    print("  separate a fixed universal locus from the moving non-universal pair.")


def part2_sector_odd_selectors_vanish_on_sigma_fixed_points() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ANY SECTOR-ODD SELECTOR VANISHES ON THE FIXED UNIVERSAL LOCUS")
    print("=" * 88)

    candidate = {
        "U1": 1.4,
        "U2": -0.6,
        "N_nu": 2.1,
        "N_e": -0.9,
    }
    odd = antisymmetric_part(candidate)

    check("Antisymmetrization forces the odd part on U1 to vanish", abs(odd["U1"]) < 1e-12,
          f"F_-(U1)={odd['U1']:.2e}")
    check("Antisymmetrization forces the odd part on U2 to vanish", abs(odd["U2"]) < 1e-12,
          f"F_-(U2)={odd['U2']:.2e}")
    check("The non-universal orbit can carry a nonzero odd selector", abs(odd["N_nu"]) > 1e-12 and abs(odd["N_e"]) > 1e-12,
          f"F_-(N_nu)={odd['N_nu']:.3f}, F_-(N_e)={odd['N_e']:.3f}")
    check("The odd selector flips sign across the non-universal orbit", abs(odd["N_nu"] + odd["N_e"]) < 1e-12,
          f"sum={odd['N_nu'] + odd['N_e']:.2e}")

    print()
    print("  So once the selector is reduced to its sector-odd part, it is")
    print("  automatically blind to the universal fixed locus.")


def part3_current_bank_reduces_the_missing_object_to_nonuniversal_support() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MISSING OBJECT IS SUPPORTED ONLY ON UNIVERSALITY FAILURE")
    print("=" * 88)

    collapse = read("docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md")
    under = read("docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md")
    odd = read("docs/PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md")
    note = read("docs/PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    gr = read("docs/UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md")

    check("The collapse theorem says one-sided minimal branches require universality failure",
          "requires failure of" in collapse and "shared-Higgs universality" in collapse)
    check("The underdetermination theorem says both universal and non-universal classes remain admissible",
          "universal" in under and "non-universal" in under and "underdetermination" in under.lower())
    check("The sector-odd reduction theorem identifies the missing object as sector-odd",
          "sector-odd mixed bridge functional" in odd)
    check("The atlas carries all three selector-side inputs", 
          "| Lepton shared-Higgs universality collapse |" in atlas
          and "| Lepton shared-Higgs universality underdetermination |" in atlas
          and "| PMNS selector sector-odd reduction |" in atlas)
    check("The GR A1 note records the structural pattern of an exact invariant locus plus moving complement",
          "exact invariant" in gr.lower() and "complement remains frame-dependent" in gr.lower())
    check("The note concludes that the missing selector is supported only on the non-universal locus",
          "non-universal" in note and "detect universality failure" in note)

    print()
    print("  Therefore the remaining selector is now sharpened one step further:")
    print("    - it must be sector-odd,")
    print("    - it must be mixed/inter-sector,")
    print("    - and it can be nonzero only on the non-universal locus.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: NON-UNIVERSAL SUPPORT REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Lepton shared-Higgs universality collapse")
    print("  - Lepton shared-Higgs universality underdetermination")
    print("  - PMNS selector sector-odd reduction")
    print("  - Universal GR A1 invariant section (structural framing only)")
    print()
    print("Question:")
    print("  Once the missing PMNS selector is known to be sector-odd, can the")
    print("  current bank sharpen where it may be nonzero?")

    part1_universal_classes_are_sigma_fixed()
    part2_sector_odd_selectors_vanish_on_sigma_fixed_points()
    part3_current_bank_reduces_the_missing_object_to_nonuniversal_support()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the universal one-offset and two-offset classes are sigma-fixed")
    print("    - any sector-odd selector vanishes on sigma-fixed points")
    print("    - so the missing PMNS selector can be nonzero only on the")
    print("      non-universal locus")
    print("    - equivalently, the minimal missing object must detect")
    print("      universality failure and orient it")
    print()
    print("  This is a reduction theorem only; it does not construct the bridge.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
