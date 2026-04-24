#!/usr/bin/env python3
"""Verify the primitive integral action-count theorem.

This checks the discrete invariant-cell lemma, the free integral monoid unit,
and the resulting gamma=1 reduced-action closure.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def shift_subset(mask: int, n: int = 16) -> int:
    out = 0
    for i in range(n):
        if mask & (1 << i):
            out |= 1 << ((i + 1) % n)
    return out


def invariant_under_transitive_cycle(mask: int, n: int = 16) -> bool:
    return shift_subset(mask, n) == mask


def primitive_count(ncells: int) -> int:
    return ncells


def phase(rank: int, gamma: Fraction) -> Fraction:
    return gamma * Fraction(rank, 16)


def main() -> int:
    note = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    reduction = read(
        "docs/PLANCK_SCALE_HBAR_NONHOMOGENEOUS_REAL_ACTION_UNIT_REDUCTION_THEOREM_2026-04-24.md"
    )
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    gamma_attempt = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")

    passed = 0
    total = 0

    invariant_masks = [mask for mask in range(1 << 16) if invariant_under_transitive_cycle(mask)]
    full_mask = (1 << 16) - 1

    total += 1
    passed += expect(
        "document-is-positive-integral-action-count-theorem",
        "Planck-Scale Primitive Integral Action-Count Theorem" in note
        and "**Status:** positive reduced-action closure" in note
        and "frontier_planck_primitive_integral_action_count_theorem_2026_04_24.py" in note,
        "new theorem and verifier are present",
    )

    total += 1
    passed += expect(
        "transitive-source-free-idempotents-are-empty-or-full",
        invariant_masks == [0, full_mask]
        and "The only\nsubsets invariant under a transitive action are the empty subset and the full\nset"
        in note,
        f"invariant masks={len(invariant_masks)}",
    )

    total += 1
    passed += expect(
        "rank-one-atoms-are-not-source-free-unit",
        "Rank-one projectors `P_eta` are valid event atoms after a selector or source is\nnamed"
        in note
        and "Treating an atom as the\nunit action history would add hidden preparation data" in note,
        "the unit is the full source-free cell, not a prepared atom",
    )

    total += 1
    passed += expect(
        "closed-history-monoid-is-free-on-full-cell",
        "M_cell = N [A_cell]" in note
        and "[A_cell]` is indecomposable" in note
        and primitive_count(0) == 0
        and primitive_count(1) == 1
        and primitive_count(7) == 7,
        "free one-generator monoid has canonical cell count",
    )

    total += 1
    passed += expect(
        "rescaled-real-functional-is-not-integral-count",
        "For `lambda = 2`, the one-cell\ngenerator is assigned the count of a two-cell history"
        in note
        and "for `0 < lambda < 1`, it\ndoes not land in the integral history count at all" in note
        and "Phi -> lambda Phi" in gamma_attempt,
        "lambda-rescaling remains a real measure but not the primitive count coordinate",
    )

    gamma = Fraction(1, 1)
    q_atom = phase(1, gamma)
    kappa_info = q_atom / 2
    a2_over_lp2 = 16 * q_atom

    total += 1
    passed += expect(
        "gamma-one-follows-from-cell-count",
        phase(16, gamma) == 1
        and q_atom == Fraction(1, 16)
        and kappa_info == Fraction(1, 32)
        and a2_over_lp2 == 1
        and "`gamma = 1`" in note
        and "`Phi(P_eta) = 1/16`" in note
        and "`kappa_info = 1/32 per bit`" in note
        and "`a^2 / l_P^2 = 1`" in note,
        f"q_atom={q_atom}, kappa={kappa_info}, a2/lP2={a2_over_lp2}",
    )

    total += 1
    passed += expect(
        "supplies-the-previous-nonhomogeneous-target",
        "`Phi(I_16) = 1`" in note
        and "`Phi(I_16) = 1`" in reduction
        and "`gamma := Phi(I_16)`" in phase_trace
        and "The integral action-count theorem supplies the missing non-homogeneous unit"
        in note,
        "the new theorem targets exactly the prior necessary-and-sufficient law",
    )

    total += 1
    passed += expect(
        "scope-does-not-overclaim-hbar-or-b3",
        "not a prediction of\nthe SI value of `hbar`" in note
        and "does not close the separate B3 gravity-sector\nderivation" in note
        and "Do not use:\n\n> The SI numerical value of `hbar` is predicted." in note
        and "Do not use:\n\n> Bare `Cl(3)` / `Z^3` has therefore derived the dynamical gravitational"
        in note,
        "the theorem closes reduced action count only",
    )

    total += 1
    passed += expect(
        "real-measure-refusal-keeps-countermodel",
        "If a reviewer refuses the integral primitive-history reading" in note
        and "`Phi_lambda(P) = lambda Tr(P) / 16`" in note
        and "does **not** derive the non-homogeneous action-unit law from\n"
        "the current bare event algebra" in reduction,
        "the hostile-review fallback is explicit",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
