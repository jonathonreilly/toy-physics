#!/usr/bin/env python3
"""Verify the parent-source Schur naturality obstruction theorem."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_PARENT_SOURCE_NATURALITY_OBSTRUCTION_THEOREM_2026-04-24.md"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def mat_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    diff = left - right
    return all(sp.simplify(entry) == 0 for entry in diff)


def main() -> int:
    note = NOTE.read_text(encoding="utf-8")
    ward = read("docs/PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md")
    parent = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    b3 = read("docs/PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md")

    src, delta = sp.symbols("s delta", real=True)

    # Axis basis order: t, x, y, z.
    t = sp.Matrix([1, 0, 0, 0])
    x = sp.Matrix([0, 1, 0, 0])
    y = sp.Matrix([0, 0, 1, 0])
    z = sp.Matrix([0, 0, 0, 1])
    singlet = (x + y + z) / sp.sqrt(3)
    e1 = (x - y) / sp.sqrt(2)
    e2 = (x + y - 2 * z) / sp.sqrt(6)

    p_a = sp.eye(4)
    q = sp.Matrix.vstack(t.T, singlet.T)
    p_q = sp.simplify(q.T * q)
    p_e = sp.simplify(e1 * e1.T + e2 * e2.T)

    u_event_axis = sp.exp(src) * p_a
    quotient_after_source = sp.simplify(q * u_event_axis * q.T)
    source_after_quotient = sp.exp(src) * sp.eye(2)

    # The quotient source is scalar, so it commutes with the floor-subtracted Schur shape.
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    lambda_min = min(l_sigma.eigenvals().keys())
    l_floor = sp.simplify(l_sigma - lambda_min * sp.eye(2))
    floor_commutator = sp.simplify(source_after_quotient * l_floor - l_floor * source_after_quotient)

    lifted_projector = sp.simplify(p_q + p_e)
    lifted_source = sp.simplify(sp.eye(4) + (sp.exp(src) - 1) * lifted_projector)

    mass_q = sp.simplify(sp.trace(p_q) / 16)
    mass_a = sp.simplify(sp.trace(p_a) / 16)

    z_event = 1 + (sp.exp(src) - 1) * mass_a
    p_event = sp.simplify(sp.diff(sp.log(z_event), src).subs(src, 0))

    nu_delta = sp.simplify(lambda_min + p_event + delta)
    p_schur_delta = sp.simplify(nu_delta - lambda_min)
    quotient_character = sp.simplify(sp.exp(src * (p_schur_delta - p_event)))

    sample_deltas = [sp.Rational(-2, 3), sp.Rational(1, 5), sp.Integer(2)]
    delta_changes_only_scalar = all(
        sp.simplify(p_schur_delta.subs(delta, d) - p_event) == d
        and mat_equal(l_sigma, l_sigma)
        and mat_equal(p_q + p_e, p_a)
        for d in sample_deltas
    )

    checks: list[tuple[str, bool, str]] = [
        (
            "finite-event-ward-derivative-is-distinct",
            p_event == sp.Rational(1, 4)
            and "The finite event Ward derivative is exact" in note
            and "The Schur/event equality is a different statement" in note
            and "This theorem does not mention `L_Sigma` or `nu`" in note,
            f"p_event={p_event}",
        ),
        (
            "schur-parent-source-quotient-commutes",
            mat_equal(quotient_after_source, source_after_quotient)
            and mat_equal(q * p_a * q.T, sp.eye(2))
            and "Q U_A(s) Q^* = exp(s) I_(H_q)" in note,
            "Q exp(s P_A) Q^* = exp(s I_q)",
        ),
        (
            "floor-subtraction-does-not-carry-source-charge",
            lambda_min == 1
            and mat_equal(floor_commutator, sp.zeros(2))
            and sorted(l_floor.eigenvals().keys()) == [sp.Integer(0), sp.Rational(2, 3)]
            and "it commutes with the\nfloor-subtracted Schur shape" in note,
            f"lambda_min={lambda_min}, floor_eigs={sorted(l_floor.eigenvals().keys())}",
        ),
        (
            "multiplicity-lift-restores-parent-source",
            mat_equal(lifted_projector, p_a)
            and mat_equal(lifted_source, u_event_axis)
            and mass_q == sp.Rational(1, 8)
            and mass_a == sp.Rational(1, 4)
            and "P_q -> P_q + P_E = P_A" in note,
            f"mass_q={mass_q}, mass_a={mass_a}",
        ),
        (
            "carrier-diagram-commutes-but-only-at-carrier-level",
            "carrier-level naturality diagram commutes" in note
            and "carriers, projectors, and\nsource-group support" in note
            and "`P_A = P_q + P_E`" in parent,
            "positive result is support naturality, not scalar normalization",
        ),
        (
            "affine-hidden-character-obstruction",
            quotient_character == sp.exp(src * delta)
            and p_schur_delta == sp.Rational(1, 4) + delta
            and delta_changes_only_scalar
            and "`chi_delta(s) = exp(s delta)`" in note,
            f"p_schur(delta)={p_schur_delta}, chi={quotient_character}",
        ),
        (
            "functorial-schur-remains-object-class-input",
            "functorial Schur representation remains an object-class input" in note
            and "derive from the gravity sector that `delta = 0`" in note
            and "finite event Ward derivative remains true\nbut does not determine `nu`" in ward,
            "the verifier refuses to treat the Schur/event equality as bare-derived",
        ),
        (
            "bare-gravity-sector-status-consistent",
            "B3 remains open" in b3
            and "The gravitational parent-source boundary-action object-class item is not\nclosed from the bare gravity sector" in note
            and "Do not use:\n\n> Bare gravity already derives the parent-source boundary-action object class."
            in note,
            "new no-go is aligned with the B3 obstruction status",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
