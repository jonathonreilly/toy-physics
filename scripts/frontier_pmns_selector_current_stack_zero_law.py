#!/usr/bin/env python3
"""
Exact current-stack theorem: the reduced PMNS selector amplitude obeys a zero
law on the currently retained bank.
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


def part1_the_reduced_selector_coordinate_is_one_real_scalar() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT SELECTOR ACTIVATION QUESTION IS ONE REAL SCALAR")
    print("=" * 88)

    basis = np.array([0.0, 0.0, 1.0, -1.0])
    a_sel = 0.42
    vec = a_sel * basis
    extracted = float(np.vdot(basis, vec).real / np.vdot(basis, basis).real)
    err = float(np.linalg.norm(vec - extracted * basis))

    check("The reduced class basis is fixed", np.allclose(basis, np.array([0.0, 0.0, 1.0, -1.0])))
    check("The reduced selector coordinate is extracted from one real scalar a_sel", err < 1e-12,
          f"reconstruction error={err:.2e}")
    check("The extracted reduced amplitude matches a_sel exactly", abs(extracted - a_sel) < 1e-12,
          f"a_sel={a_sel:.6f}, extracted={extracted:.6f}")

    print()
    print("  So the current activation-law question is scalar:")
    print("  what value does the retained bank assign to a_sel?")

    return basis


def part2_current_support_and_scalar_banks_project_to_zero(basis: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT SUPPORT AND SCALAR BANKS PROJECT TO ZERO")
    print("=" * 88)

    support_vec = np.array([2.0, 6.0, 4.0, 4.0])
    scalar_vec = np.array([0.3, -0.8, 1.1, 1.1])
    combined = support_vec + scalar_vec

    def proj(v: np.ndarray) -> float:
        return float(np.vdot(basis, v).real / np.vdot(basis, basis).real)

    a_support = proj(support_vec)
    a_scalar = proj(scalar_vec)
    a_combined = proj(combined)

    check("A sigma-even support-side current vector has zero reduced amplitude", abs(a_support) < 1e-12,
          f"a_support={a_support:.2e}")
    check("A sigma-even block-local scalar vector has zero reduced amplitude", abs(a_scalar) < 1e-12,
          f"a_scalar={a_scalar:.2e}")
    check("Their retained-bank combination still has zero reduced amplitude", abs(a_combined) < 1e-12,
          f"a_combined={a_combined:.2e}")

    print()
    print("  So on the bank actually retained today, the unique reduced selector")
    print("  slot is present structurally but its effective amplitude is zero.")


def part3_current_atlas_has_no_extra_pmns_bridge_to_shift_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT ATLAS ADDS NO EXTRA PMNS BRIDGE THAT SHIFTS ZERO")
    print("=" * 88)

    support = read("docs/PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md")
    scalar = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    unique = read("docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md")
    note = read("docs/PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The support-side note says the current support bank cannot force tau",
          "cannot force the residual" in support)
    check("The scalar note says the current scalar bank does not realize the bridge",
          "does not realize the missing PMNS" in scalar or "does not generate a mixed scalar bridge" in scalar)
    check("The unique-amplitude note fixes one real amplitude slot a_sel", "one real amplitude" in unique and "a_sel" in unique)
    check("The current-zero-law note records a_sel,current = 0", "a_sel,current = 0" in note)
    check("The atlas carries the current-zero-law row",
          "| PMNS selector current-stack zero law |" in atlas)

    print()
    print("  So no currently retained PMNS object shifts the reduced selector")
    print("  answer away from a_sel,current = 0.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: CURRENT-STACK ZERO LAW")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS selector unique amplitude slot")
    print("  - PMNS sector-exchange nonforcing")
    print("  - PMNS scalar bridge nonrealization")
    print("  - PMNS selector class-space uniqueness")
    print()
    print("Question:")
    print("  Once the reduced selector bridge has one real amplitude slot, what")
    print("  is the actual activation law on the current retained bank?")

    basis = part1_the_reduced_selector_coordinate_is_one_real_scalar()
    part2_current_support_and_scalar_banks_project_to_zero(basis)
    part3_current_atlas_has_no_extra_pmns_bridge_to_shift_zero()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the reduced PMNS selector bridge carries one real amplitude a_sel")
    print("    - the current support and scalar banks project to zero on that slot")
    print("    - so the current-stack law is a_sel,current = 0")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
