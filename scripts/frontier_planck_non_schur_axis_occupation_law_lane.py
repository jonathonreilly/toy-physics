#!/usr/bin/env python3
"""Audit the non-Schur axis occupation-law lane honestly.

This lane does not claim that normalized Schur/Perron data close quarter.
It proves a sharper conditional theorem on the full physical cell:

  - work on the exact time-locked 4-bit cell H_cell = C^{16};
  - let the local bit-flip group act by xor on the primitive cell basis;
  - any normalized positive diagonal occupation law invariant under that group
    is uniquely the tracial state I_16 / 16;
  - the already-forced coarse worldtube packet P_A has rank 4;
  - therefore its full-cell occupation is exactly 4/16 = 1/4.

So the non-Schur route reduces exact boundary Planck closure to one precise
physical principle: source-free local occupation is bit-flip invariant on the
full physical cell.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md"
SECTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md"
MULTIPLICITY = ROOT / "docs/PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md"
WEIGHTED = ROOT / "docs/PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md"
POSITIVE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md"
CELL16 = ROOT / "docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md"
SITE_PHASE = ROOT / "docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def xor_bits(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x ^ y) for x, y in zip(a, b))


def main() -> int:
    note = normalized(NOTE)
    section_note = normalized(SECTION)
    multiplicity = normalized(MULTIPLICITY)
    weighted = normalized(WEIGHTED)
    positive = normalized(POSITIVE)
    cell16 = normalized(CELL16)
    site_phase = normalized(SITE_PHASE)

    n_pass = 0
    n_fail = 0

    print("Planck non-Schur axis occupation-law lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM ALIGNMENT")
    p = check(
        "the coarse worldtube packet is still section-canonical",
        "section-canonical" in section_note
        and "the physical selector can be forced onto" in section_note
        and "worldtube sector" in section_note,
        "the non-Schur law should start from the already-forced packet P_A",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the multiplicity-lift lane still fixes the full packet mass as 1/4 under the democratic state",
        "tr(rho_cell p_a) = 2 tr(rho_cell p_q) = 1/4" in multiplicity,
        "the new lane should explain rho_cell rather than re-solving the factor of two",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the weighted Schur lane still rules out quarter from normalized Schur/Perron data",
        "1/13 <= alpha(beta) <= 1/7" in weighted
        and "full-cell occupation" in weighted,
        "this route should be genuinely non-Schur, not hidden Schur packaging",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the positive-residual lane still identifies delta = Tr(rho_cell P_A) as the unique positive candidate",
        "delta = tr(rho_cell p_a)" in positive
        and "m_axis = 1/4" in positive,
        "the non-Schur occupation law should target the same quarter candidate",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 one-sixteenth lane still treats I_16/16 as the canonical democratic full-cell state",
        "rho_cell = i_16 / 16" in cell16
        and "canonical democratic state" in cell16
        and "every primitive taste cell therefore carries exact weight `1/16`" in cell16,
        "the non-Schur lane should explain this state by symmetry rather than insert it by hand",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the site-phase / cube-shift note still records exact native bit flips on the taste cube",
        "phi^dagger p_mu phi = s_mu" in site_phase
        and "bit-flip law" in site_phase,
        "bit flips are already native cube/taste operations on the framework side",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT BIT-FLIP GROUP ON THE FULL CELL")
    states = list(product((0, 1), repeat=4))
    flips = states[:]
    one_hot = [s for s in states if sum(s) == 1]

    p = check(
        "the full time-locked cell has exactly 16 primitive states",
        len(states) == 16,
        "this is the exact C^16 carrier on the minimal 4-bit cell",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the coarse worldtube packet consists of the four Hamming-weight-one states",
        len(one_hot) == 4 and set(one_hot) == {(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)},
        "P_A should still be the exact four-axis packet",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the xor bit-flip action is transitive on the 16-state cell",
        all(xor_bits(a, xor_bits(a, b)) == b for a in states for b in states),
        "for any pair of states there is a unique flip taking one to the other",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the local flip set forms the full (Z_2)^4 group",
        len(flips) == 16 and xor_bits(flips[3], flips[5]) in flips and (0, 0, 0, 0) in flips,
        "independent bit complementation on the four cell bits generates the whole local flip group",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: UNIQUE INVARIANT OCCUPATION LAW")
    vars_p = sp.symbols("p0:16", real=True)
    index = {state: i for i, state in enumerate(states)}
    equations = []
    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    for s in states:
        for g in generators:
            equations.append(sp.Eq(vars_p[index[s]], vars_p[index[xor_bits(s, g)]]))
    equations.append(sp.Eq(sum(vars_p), 1))

    solution = sp.linsolve([eq.lhs - eq.rhs for eq in equations], vars_p)
    tuple_solution = next(iter(solution))
    uniform = tuple(sp.Rational(1, 16) for _ in states)

    p = check(
        "bit-flip invariance plus normalization has a unique solution",
        tuple_solution == uniform,
        "transitivity should force every primitive occupation weight to be exactly 1/16",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the unique invariant state is the tracial/democratic full-cell state",
        all(entry == sp.Rational(1, 16) for entry in tuple_solution),
        "the non-Schur source-free occupation law is rho = I_16 / 16",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: EXACT QUARTER ON THE FORCED PACKET")
    alpha = sum(tuple_solution[index[s]] for s in one_hot)

    p = check(
        "the forced packet occupation is exactly 4 * (1/16)",
        alpha == sp.Rational(1, 4),
        "the four one-hot worldtube cells each carry 1/16 under the unique invariant state",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "rank/trace packaging agrees with direct counting",
        sp.Rational(len(one_hot), 16) == alpha,
        "Tr((I_16/16) P_A) = rank(P_A)/16 = 4/16 = 1/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-Schur full-cell law beats the normalized Schur no-extra-datum bound",
        alpha > sp.Rational(1, 7),
        "quarter sits strictly above the weighted-Schur ceiling 1/7",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: ACTION-LANE CONSEQUENCE")
    lambda_min = sp.Integer(1)
    nu = lambda_min + alpha

    p = check(
        "the action-lane closure datum becomes nu = 5/4 on the canonical witness",
        nu == sp.Rational(5, 4),
        "if p_phys is the non-Schur packet occupation, then nu = lambda_min + 1/4 = 5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE ALIGNMENT")
    p = check(
        "the note states the unique invariant full-cell state as I_16 / 16",
        "rho_tr = i_16 / 16" in note
        or "rho = i_16 / 16" in note
        or "rho_cell = i_16 / 16" in note,
        "the writeup should make the invariant-state conclusion explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states exact packet occupation alpha = 1/4",
        "alpha = tr(rho p_a) = 1/4" in note or "alpha = tr((i_16 / 16) p_a) = 1/4" in note,
        "the writeup should make the quarter conclusion explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the remaining principle as bit-flip-invariant source-free occupation",
        "source-free full-cell occupation" in note
        and "full four-bit local flip group" in note,
        "the review burden should now be one explicit non-Schur physical principle",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass} PASS / {n_fail} FAIL")
    print("=" * 78)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
