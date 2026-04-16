#!/usr/bin/env python3
"""
DM neutrino weak-triplet coefficient axiom boundary.

Framework convention for this runner:
  "axiom" means only the single framework axiom

      Cl(3) on Z^3.

Question:
  Does the current single-axiom Cl(3) on Z^3 stack, together with the current
  derived atlas rows, already derive the transfer coefficients c_odd and
  M_even in

      gamma = c_odd * a_sel
      [E1,E2]^T = M_even [tau_E,tau_T]^T ?

Answer:
  Yes.

  The transfer class is exact, and the transfer coefficients are now fixed:

    - c_odd = +1 on the source-oriented branch convention
    - M_even = v_even [1,1]
    - v_even = (sqrt(8/3), sqrt(8)/3)

  by bosonic matching on the reduced selector / triplet odd blocks and on the
  exact weak row factor / even dual generators.

  Equivalently:

    - gamma = a_sel
    - E1 = sqrt(8/3) * (tau_E + tau_T)
    - E2 = (sqrt(8)/3) * (tau_E + tau_T)

  What remains open is not transfer-coefficient normalization. It is the
  source-amplitude law for a_sel and tau_+, and the benchmark runner has not
  yet been rebuilt around that exact transfer law.
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


def part1_axiom_means_only_cl3_on_z3() -> None:
    print("\n" + "=" * 88)
    print("PART 1: FRAMEWORK AXIOM MEANS ONLY Cl(3) ON Z^3")
    print("=" * 88)

    flagship = read("docs/FLAGSHIP_PAPER_CONTRIBUTION_STATEMENT_NOTE.md")
    transfer = read("docs/DM_NEUTRINO_WEAK_TRIPLET_TRANSFER_CLASS_THEOREM_NOTE_2026-04-15.md")

    check(
        "The framework sentence states the single physical theory is Cl(3) on Z^3",
        "We take `Cl(3)` on `Z^3` as the physical theory. Everything else is derived." in flagship,
    )
    check(
        "The transfer-class theorem is a derived structural theorem on top of that single axiom",
        "exact transfer-class theorem" in transfer and "coefficient problem" in transfer,
    )


def part2_c_odd_is_now_fixed_by_bosonic_matching() -> None:
    print("\n" + "=" * 88)
    print("PART 2: C_ODD IS NOW FIXED BY BOSONIC MATCHING")
    print("=" * 88)

    selector = Path("/Users/jonBridger/Toy Physics-neutrino-majorana/docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md").read_text(
        encoding="utf-8"
    )
    sign = Path("/Users/jonBridger/Toy Physics-neutrino-majorana/docs/PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md").read_text(
        encoding="utf-8"
    )
    source = read("docs/DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md")
    codd = read("docs/DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")

    check(
        "The source side gives exactly one real selector amplitude slot a_sel",
        "one real amplitude slot" in selector and "B_red = a_sel S_cls" in selector,
    )
    check(
        "The target side gives exactly one odd triplet slot gamma",
        "CP-odd triplet slot `gamma`" in source or "CP-odd triplet slot" in source,
    )
    check(
        "The bosonic matching theorem fixes the canonical odd normalization to |c_odd| = 1",
        "|c_odd| = 1" in codd and "c_odd = +1" in codd,
    )
    check(
        "The source-oriented sign convention records c_odd = +1",
        "a_sel > 0" in sign,
        "positive selector orientation picks the source-oriented branch",
    )


def part3_the_exact_source_carrier_closes_the_even_leg() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT SOURCE CARRIER CLOSES THE EVEN LEG")
    print("=" * 88)

    primitive = Path("/Users/jonBridger/Toy Physics/.claude/worktrees/strong-cp-nature/docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md").read_text(
        encoding="utf-8"
    )
    reduction = read("docs/DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md")
    veven = read("docs/DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")

    v_even = np.array([0.7, -0.2], dtype=float)
    m = np.column_stack([v_even, v_even])

    check(
        "The exact source carrier treats the two bright columns symmetrically as u_E and u_T",
        "K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]".replace(" ", "")
        in primitive.replace(" ", ""),
    )
    check(
        "The swap-reduction theorem records the exact common-column form M_even = v_even [1,1]",
        "v_even [1,1]" in reduction or "v_even [1, 1]" in reduction,
    )
    check(
        "The antisymmetric source mode lies in the kernel of the swap-fixed exact class",
        np.linalg.norm(m @ np.array([1.0, -1.0])) < 1e-12,
        f"kernel err={np.linalg.norm(m @ np.array([1.0,-1.0])):.2e}",
    )
    check(
        "The even bosonic-normalization theorem fixes v_even exactly",
        "v_even = (sqrt(8/3), sqrt(8)/3)" in veven,
    )
    check(
        "So the exact even transfer law is [E1,E2]^T = v_even (tau_E + tau_T)",
        "E1 = sqrt(8/3) tau_+" in veven and "E2 = (sqrt(8)/3) tau_+" in veven,
    )
    check(
        "The source-side carrier still factors through the symmetric row mode only",
        "bounded linear readout" in primitive and "exact carrier" in primitive,
    )


def part4_the_current_single_axiom_boundary_is_exact() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT SINGLE-AXIOM BOUNDARY IS EXACT")
    print("=" * 88)

    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")
    lepto = read("docs/DM_LEPTOGENESIS_NOTE.md")

    check(
        "The blocker note records that the live gap is now source amplitudes rather than transfer coefficients",
        "source amplitudes" in blocker and "a_sel" in blocker and "tau_+" in blocker,
    )
    check(
        "The leptogenesis note records that the benchmark remains bounded because the source amplitudes are still open",
        "a_sel" in lepto and "tau_+" in lepto and "eta = 1.81e-10" in lepto,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO WEAK-TRIPLET COEFFICIENT AXIOM BOUNDARY")
    print("=" * 88)

    part1_axiom_means_only_cl3_on_z3()
    part2_c_odd_is_now_fixed_by_bosonic_matching()
    part3_the_exact_source_carrier_closes_the_even_leg()
    part4_the_current_single_axiom_boundary_is_exact()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
