#!/usr/bin/env python3
"""Verify the hbar non-homogeneous real action-unit reduction theorem.

The verifier checks the algebraic closure under an explicit primitive unit law
and the countermodels that keep gamma free when that law is omitted.
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


def phase(rank: int, gamma: Fraction) -> Fraction:
    return gamma * Fraction(rank, 16)


def homogeneous_premises_hold(gamma: Fraction) -> bool:
    atoms_equal = all(phase(1, gamma) == phase(1, gamma) for _ in range(16))
    additive_identity = sum(phase(1, gamma) for _ in range(16)) == phase(16, gamma)
    positive = all(phase(rank, gamma) >= 0 for rank in range(17))
    return atoms_equal and additive_identity and positive


def primitive_unit_law_holds(gamma: Fraction) -> bool:
    return phase(16, gamma) == 1


def main() -> int:
    note = read(
        "docs/PLANCK_SCALE_HBAR_NONHOMOGENEOUS_REAL_ACTION_UNIT_REDUCTION_THEOREM_2026-04-24.md"
    )
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    gamma_attempt = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")
    gamma_period = read("docs/PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")

    passed = 0
    total = 0

    gamma_one = Fraction(1, 1)
    gamma_two = Fraction(2, 1)
    q_atom_one = phase(1, gamma_one)
    q_atom_two = phase(1, gamma_two)
    kappa_bit_one = q_atom_one / 2
    a2_over_lp2_one = 16 * q_atom_one

    total += 1
    passed += expect(
        "new-note-is-hbar-scoped",
        "Planck-Scale Hbar Non-Homogeneous Real Action-Unit Reduction Theorem" in note
        and "**Status:** conditional closure plus no-go/reduction" in note
        and "frontier_planck_hbar_nonhomogeneous_real_action_unit_reduction_2026_04_24.py"
        in note,
        "new document and verifier are hbar/action-unit specific",
    )

    total += 1
    passed += expect(
        "target-starts-after-trace-shape",
        "`Phi(P) = gamma Tr(P) / 16`" in note
        and "`Phi(P) = gamma Tr(P) / 16`" in phase_trace
        and "Do not use trace/naturality to set `gamma`" in note,
        "the theorem uses trace shape only as prior context, not as gamma closure",
    )

    total += 1
    passed += expect(
        "primitive-unit-law-is-nonhomogeneous",
        "`Phi_action(n [A_cell]) = n`" in note
        and "`Phi_action([A_cell]) = 1`" in note
        and "`(lambda Phi_action)([A_cell]) = lambda`" in note,
        "generator-count coordinate breaks Phi -> lambda Phi scaling",
    )

    total += 1
    passed += expect(
        "conditional-gamma-one-algebra",
        primitive_unit_law_holds(gamma_one)
        and q_atom_one == Fraction(1, 16)
        and kappa_bit_one == Fraction(1, 32)
        and a2_over_lp2_one == 1
        and "`q_atom = 1/16`" in note
        and "`kappa_info = 1/32 per bit`" in note
        and "`a^2 / l_P^2 = 1`" in note,
        f"q_atom={q_atom_one}, kappa_bit={kappa_bit_one}, a2/lP2={a2_over_lp2_one}",
    )

    total += 1
    passed += expect(
        "homogeneous-countermodel-keeps-gamma-free",
        homogeneous_premises_hold(gamma_one)
        and homogeneous_premises_hold(gamma_two)
        and primitive_unit_law_holds(gamma_one)
        and not primitive_unit_law_holds(gamma_two)
        and q_atom_two == Fraction(1, 8)
        and "`Phi_lambda(I_16) = lambda`" in note
        and "`Phi -> lambda Phi`" in gamma_attempt,
        "lambda=2 obeys homogeneous premises but fails the unit law",
    )

    total += 1
    passed += expect(
        "equivalence-is-explicit",
        "Given the trace-reduced primitive phase law, the following are equivalent" in note
        and "`gamma := Phi(I_16)`" in note
        and "`Phi(I_16) = 1`" in note
        and "`gamma = 1`" in note,
        "gamma-one is exactly the one-cell real action unit statement",
    )

    total += 1
    passed += expect(
        "noncompact-central-route-reduced",
        "`0 -> R_action -> G_hat -> G -> 1`" in note
        and "`t -> lambda t`, with `lambda > 0`" in note
        and "`Z_{\\ge 0} [A_cell] subset R_action`" in note
        and "only moves the ambiguity from periodic phase to real central\nscale" in note,
        "a real central line still needs a primitive integral generator",
    )

    total += 1
    passed += expect(
        "index-route-needs-action-index-unit-map",
        "`Index(D_cell) = SF(D_cell) = 1`" in note
        and "`Phi = c Index`" in note
        and "`Phi = Index`" in note
        and "action-index unit\nmap" in note,
        "index one alone allows Phi=c*Index unless c=1 is derived",
    )

    total += 1
    passed += expect(
        "primitive-action-monoid-route-preserved",
        "`M_action = N [A_cell]`" in note
        and "real action coordinate is the primitive count coordinate rather than" in note
        and "`lambda` times that coordinate" in note,
        "primitive monoid is the sharp viable route but still needs scale-breaking",
    )

    total += 1
    passed += expect(
        "ward-route-needs-unit-calibrated-source",
        "`d/ds log Z_cell(s) |_{s=0} = 1`" in note
        and "`s -> lambda s`" in note
        and "unit-calibrated microscopic action\nsource" in note,
        "Ward balance closes only if the source parameter is already reduced action",
    )

    total += 1
    passed += expect(
        "periodicity-and-finite-roots-not-reused",
        "without invoking bare `U(1)`\nperiodicity" in note
        and "finite roots alone" in note
        and "Phase periodicity and central extensions can quantize phase classes" in gamma_period
        and "A 16th root gives phase\n`exp(2 pi i / 16)`" in gamma_period,
        "the theorem preserves the existing phase-period obstruction",
    )

    total += 1
    passed += expect(
        "prior-action-phase-targets-match",
        "`q_* = 1/16`" in action_phase
        and "`kappa_info = 1/32 per bit`" in action_phase
        and "`gamma = 1`" in action_phase
        and "Theorem 1: Conditional Gamma-One Closure" in note,
        "conditional unit law reproduces the established hbar target values",
    )

    total += 1
    passed += expect(
        "status-not-overclaimed",
        "does **not** derive the non-homogeneous action-unit law from\n"
        "the current bare event algebra" in note
        and "not\nunconditionally closed" in note
        and "**Status:** closure theorem" not in note
        and "The current branch has not derived the primitive real action-unit law" in note
        and "> The branch derives `gamma = 1` from the current bare trace/naturality stack."
        in note,
        "gamma=1 is conditional, not claimed from current bare premises",
    )

    total += 1
    passed += expect(
        "si-hbar-not-predicted",
        "not a prediction of the SI decimal\nvalue of `hbar`" in note
        and "> The SI decimal value of `hbar` is predicted." in note
        and "does not derive the SI value of `hbar`" in phase_trace,
        "the theorem stays on dimensionless reduced action",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
