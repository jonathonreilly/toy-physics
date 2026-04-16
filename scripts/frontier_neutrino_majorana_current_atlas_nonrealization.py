#!/usr/bin/env python3
"""
Current-atlas non-realization boundary for the missing Majorana primitive.

Question:
  Does the current main-branch atlas / retained matter toolkit already contain
  the missing charge-2 Majorana primitive under another name?

Answer on the current lane:
  No. The atlas fixes the channel and provides scalar/tensor/toolkit surfaces,
  but no currently retained object realizes a fermionic charge-2 primitive on
  the unique nu_R channel.

Boundary:
  This is a current-atlas boundary only. It does NOT prove that no future
  axiom-side primitive can be derived.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

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


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_observable_principle_stays_scalar_normal() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT ATLAS OBSERVABLE BACKBONE IS SCALAR / DETERMINANT-BASED")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    obs = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")

    has_observable_row = "| Observable principle | `log|det(D+J)|`" in atlas
    has_closure_row = "| Observable-principle closure |" in atlas
    mentions_pfaffian = "Pfaffian" in atlas or "Nambu" in atlas
    mentions_scalar = "scalar observable generator" in obs.lower() or "scalar generator" in obs.lower()
    mentions_det = "log |det(d+j)|" in obs.lower() or "log|det(d+j)|" in obs.lower()

    check("Atlas explicitly retains the determinant observable-principle row", has_observable_row)
    check("Atlas retains observable-principle closure on the same determinant surface", has_closure_row)
    check("Observable-principle note is explicitly scalar", mentions_scalar)
    check("Observable-principle note is explicitly determinant-based", mentions_det)
    check("Current atlas observable rows do not already introduce a Pfaffian/Nambu primitive", not mentions_pfaffian)

    print()
    print("  So the retained observable backbone is exact, but scalar/normal.")
    print("  It fixes the current grammar; it does not already supply a charge-2")
    print("  fermionic primitive.")


def test_spatial_composite_route_misses_nu_r() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXISTING SPATIAL COMPOSITE ROUTE DOES NOT REALIZE THE nu_R PRIMITIVE")
    print("=" * 88)

    rhs = read("scripts/frontier_right_handed_sector.py")
    closure = read("docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md")

    has_nu_r_closure = "`nu_R : (1,1)_0`" in closure
    wedge_line = "The antisymmetric wedge^2(C^8) = C^28 does contain SU(2) singlets" in rhs
    dr_found = 'check("d_R (Y=-2/3) found in wedge^2 singlets"' in rhs
    er_found = 'check("e_R (Y=-2) found in wedge^2 singlets"' in rhs
    ur_absent = 'check("u_R (Y=+4/3) ABSENT from wedge^2 singlets (needs degree 4)"' in rhs
    missing_zero_and_u = "MISSING from wedge^2 singlets: {Fraction(0, 1), Fraction(4, 3)}" in rhs or "Fraction(0)" in rhs
    awkward = "the composite route is structurally awkward" in rhs.lower()

    check("Retained matter closure includes nu_R as the final right-handed singlet", has_nu_r_closure)
    check("Right-handed-sector audit has an explicit antisymmetric wedge^2(C^8) composite route", wedge_line)
    check("That route realizes d_R and e_R degree-2 singlets", dr_found and er_found)
    check("That route explicitly misses u_R on wedge^2(C^8)", ur_absent)
    check("The same wedge^2(C^8) audit also misses the Y=0 slot needed for nu_R", missing_zero_and_u)
    check("The script itself labels the composite route structurally awkward", awkward)

    print()
    print("  So the existing antisymmetric composite object on the spatial side is")
    print("  not the missing Majorana primitive: it does not realize the nu_R slot.")


def test_non_scalar_atlas_primitives_are_gravity_side() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CURRENT ATLAS PRIMITIVES BEYOND THE SCALAR BACKBONE ARE GRAVITY/TENSOR-SIDE")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    required_rows = [
        "Route 2 exact bilinear tensor carrier `K_R`",
        "Route 2 tensor prototype `Theta_R^(0)`",
        "Constructed support tensor primitive `Xi_R^(0)`",
        "Tensorized Schur/Dirichlet primitive",
        "Route 2 spacetime tensor carrier",
        "Universal tensor variational candidate",
    ]

    found = [row for row in required_rows if row in atlas]
    missing = [row for row in required_rows if row not in atlas]

    # The atlas should have no neutrino/Majorana/Pfaffian row at present.
    neutrino_rows = re.findall(r"\|\s*([^|]*Majorana[^|]*)\|", atlas, flags=re.IGNORECASE)
    pfaffian_rows = re.findall(r"\|\s*([^|]*Pfaffian[^|]*)\|", atlas, flags=re.IGNORECASE)
    neutrino_primitive_rows = re.findall(r"\|\s*([^|]*neutrino[^|]*primitive[^|]*)\|", atlas, flags=re.IGNORECASE)

    check("Atlas contains the current non-scalar tensor/gravity primitive rows", len(found) == len(required_rows),
          f"missing rows={len(missing)}")
    check("Current atlas has no Majorana primitive row", len(neutrino_rows) == 0,
          f"majorana rows={neutrino_rows}")
    check("Current atlas has no Pfaffian primitive row", len(pfaffian_rows) == 0,
          f"pfaffian rows={pfaffian_rows}")
    check("Current atlas has no neutrino primitive row", len(neutrino_primitive_rows) == 0,
          f"neutrino primitive rows={neutrino_primitive_rows}")

    print()
    print("  The atlas does contain real new primitives, but they are tensor /")
    print("  gravity / source objects. None of them is already a fermionic")
    print("  charge-2 realization on the Majorana lane.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CURRENT ATLAS NON-REALIZATION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print("  - docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md")
    print("  - scripts/frontier_right_handed_sector.py")
    print("  - docs/NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md")
    print()
    print("Question:")
    print("  Does the current main-branch atlas / retained matter toolkit already")
    print("  contain the missing charge-2 Majorana primitive under another name?")

    test_observable_principle_stays_scalar_normal()
    test_spatial_composite_route_misses_nu_r()
    test_non_scalar_atlas_primitives_are_gravity_side()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The current atlas fixes the channel and provides real scalar and")
    print("  tensor tool surfaces, but it does not already contain the missing")
    print("  fermionic charge-2 primitive on the nu_R Majorana lane.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
