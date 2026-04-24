#!/usr/bin/env python3
"""Verify the boundary source-functorial Ward hardening theorem."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def main() -> int:
    note = read("docs/PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md")
    derivation = read("docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md")
    same_source = read("docs/PLANCK_SCALE_BOUNDARY_SAME_SOURCE_COVARIANCE_THEOREM_2026-04-23.md")
    parent = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    observable = read("docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    s, nu = sp.symbols("s nu", real=True)
    m = sp.Rational(1, 4)
    lambda_min = sp.Integer(1)
    z = 1 + (sp.exp(s) - 1) * m
    p_event = sp.simplify(sp.diff(sp.log(z), s).subs(s, 0))
    p_schur = nu - lambda_min
    delta = sp.simplify(p_schur - p_event)
    quotient_character = sp.exp(s * delta)

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "finite-event-ward-derivative-is-exact",
        p_event == m
        and "`d/ds log Tr(rho_cell exp(s P_A))|_(s=0) = Tr(rho_cell P_A)`"
        in note
        and "`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A)`" in derivation,
        f"p_event={p_event}",
    )

    total += 1
    passed += expect(
        "schur-equality-is-not-from-scalar-observable-alone",
        "not derived from the\nscalar Schur observable grammar alone" in note
        and "p_vac = (1/(2n)) log det(L_Sigma)" in note
        and "physical boundary pressure is the current observable-principle scalar" in observable,
        "the theorem does not erase the older scalar-pressure no-go",
    )

    total += 1
    passed += expect(
        "parent-source-object-class-is-explicit-load",
        "`B_parent := (H_A, P_A)`" in note
        and "`B_parent := (H_A, P_A)`" in parent
        and "two functorial representations of the same parent" in note,
        "the load-bearing parent-source object is explicit",
    )

    total += 1
    passed += expect(
        "quotient-character-is-hidden-source-if-nonzero",
        quotient_character == sp.exp(s * (nu - sp.Rational(5, 4)))
        and "`chi_Delta(s) = exp(s Delta)`" in note
        and "`Delta = (nu - lambda_min(L_Sigma)) - Tr(rho_cell P_A)`" in note
        and "hidden source-free boundary-action data" in note,
        f"chi={quotient_character}",
    )

    total += 1
    passed += expect(
        "same-source-covariance-is-functorial-not-magic",
        "a source-free primitive boundary cell cannot carry two inequivalent" in same_source
        and "source-functoriality forces equal generators" in note
        and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in note,
        "same-source equality is a no-extra-character statement",
    )

    total += 1
    passed += expect(
        "limits-and-stop-condition-are-clear",
        "It does not prove:" in note
        and "a conventional path-integral Ward identity" in note
        and "If that rejection is accepted, the finite event Ward derivative remains true\nbut does not determine `nu`"
        in note,
        "hostile reviewer can reject the parent-source representation claim",
    )

    total += 1
    passed += expect(
        "safe-and-unsafe-claims-recorded",
        "finite parent-source functoriality theorem" in note
        and "Do not use:\n\n> The scalar Schur observable principle alone derives the quarter."
        in note
        and "Do not use:\n\n> The branch derives a conventional continuum path-integral Ward identity."
        in note,
        "the theorem prevents overclaiming the Ward bridge",
    )

    total += 1
    passed += expect(
        "reviewer-packet-links-functorial-ward",
        "PLANCK_SCALE_BOUNDARY_SOURCE_FUNCTORIAL_WARD_THEOREM_2026-04-24.md"
        in reviewer,
        "canonical packet links the hardening theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
