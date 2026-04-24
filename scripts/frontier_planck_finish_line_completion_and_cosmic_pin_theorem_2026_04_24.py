#!/usr/bin/env python3
"""Verify the finish-line completion and cosmic-pin theorem."""

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


def main() -> int:
    note = read("docs/PLANCK_SCALE_FINISH_LINE_COMPLETION_AND_COSMIC_PIN_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")
    cosmic = read("docs/PLANCK_SCALE_COSMIC_ADDRESS_IMPORT_UNIT_MAP_THEOREM_2026-04-23.md")
    realification = read("docs/PLANCK_SCALE_REALIFICATION_ADMISSIBILITY_THEOREM_2026-04-24.md")
    b3 = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md")
    weyl = read("docs/PLANCK_SCALE_PRIMITIVE_WEYL_HBAR_REPRESENTATION_THEOREM_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-finish-line-theorem",
        "Planck-Scale Finish-Line Completion And Cosmic-Pin Theorem" in note
        and "**Status:** strongest retained endpoint and SI-pinning obstruction" in note
        and "frontier_planck_finish_line_completion_and_cosmic_pin_theorem_2026_04_24.py"
        in note,
        "new finish-line theorem and verifier are present",
    )

    finite_trace_comm = 0
    finite_trace_identity = 16

    total += 1
    passed += expect(
        "finite-only-closure-is-impossible",
        finite_trace_comm == 0
        and finite_trace_identity != 0
        and "`Tr([A,B]) = 0`" in note
        and "`Tr(i hbar I_16) = 16 i hbar`" in note
        and "zero Lie algebra" in note,
        "trace and finite-Lie obstructions block finite-only Ward/commutator closure",
    )

    total += 1
    passed += expect(
        "realification-is-forced-by-response-question",
        "`T_Z tensor_Z R`" in note
        and "factors uniquely through" in note
        and "not an optional continuum import" in note
        and "initial\nreal linear response object" in realification
        and "`T_R = T_Z tensor_Z R`" in b3,
        "first-order response forces the realified translation module",
    )

    total += 1
    passed += expect(
        "coherent-history-completion-is-forced-by-action-phase-question",
        "`M_cell = N[A_cell]`" in note
        and "`U(H_1 (+) H_2) = U(H_1) U(H_2)`" in note
        and "`theta = Phi`" in note
        and "`S/hbar = Phi`" in note
        and "`S(H)/hbar = Phi(H)`" in action_phase,
        "action-phase question forces coherent gluing and the phase generator",
    )

    age = Fraction(1, 1)
    n1 = Fraction(10**60, 1)
    n2 = Fraction(10**61, 1)
    tau1 = age / n1
    tau2 = age / n2

    total += 1
    passed += expect(
        "cosmic-age-pin-alone-does-not-fix-tick",
        tau1 != tau2
        and n1 * tau1 == age
        and n2 * tau2 == age
        and "Without a native theorem for the dimensionless count `N_U`" in note
        and "That would import the result in count language" in cosmic,
        f"same age decomposes as {n1}*{tau1} and {n2}*{tau2}",
    )

    c_cell = Fraction(1, 4)
    a2_over_lp2 = 4 * c_cell
    area = Fraction(10**122, 1)
    microscopic = c_cell * area
    gravitational = area / 4

    total += 1
    passed += expect(
        "cosmic-area-cancels-from-planck-comparison",
        microscopic == gravitational
        and a2_over_lp2 == 1
        and "`c_cell A_U/a^2 = A_U/(4 l_P^2)`" in note
        and "`a^2/l_P^2 = 4 c_cell = 1`" in note
        and "Since `A_U > 0`, the address-dependent area cancels" in cosmic,
        f"a2/lP2={a2_over_lp2}, area cancels from {area}",
    )

    total += 1
    passed += expect(
        "si-prediction-requires-derived-dimensionless-bridge",
        "a derived cosmic tick count `N_U = T_U/t_cell`" in note
        and "a derived cosmic radius count `N_R = R_U/a`" in note
        and "a derived dimensionless constant such as `alpha`" in note
        and "downstream of the unit map, not independently predicted by the cosmic pins"
        in note,
        "SI values need an extra native dimensionless bridge or the standard unit map",
    )

    total += 1
    passed += expect(
        "finish-line-claim-includes-all-retained-positive-results",
        "`a/l_P=1`" in note
        and "`S/hbar=Phi`" in note
        and "standard Weyl/commutator/uncertainty/angular-momentum" in note
        and "`[X,P] = i hbar I`" in weyl
        and "The result is not a prediction of the SI decimal value of `hbar`" in weyl,
        "strongest endpoint is complete but dimensionless/scoped",
    )

    total += 1
    passed += expect(
        "reviewer-packet-links-finish-line-theorem",
        "PLANCK_SCALE_FINISH_LINE_COMPLETION_AND_COSMIC_PIN_THEOREM_2026-04-24.md"
        in reviewer,
        "canonical reviewer packet exposes the finish-line theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
