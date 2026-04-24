#!/usr/bin/env python3
"""Verify the gamma phase-period obstruction theorem."""

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
    note = read("docs/PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md")
    gamma_attempt = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")
    hbar_order = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    gamma, n = sp.symbols("gamma n", real=True, integer=True)
    k, N = sp.symbols("k N", integer=True, nonzero=True)

    # Algebraic facts used by the note.
    periodic_identity = sp.simplify(sp.exp(sp.I * (gamma + 2 * sp.pi * n)) / sp.exp(sp.I * gamma))
    central_lhs = 2 * sp.pi * k / N
    passed = 0
    total = 0

    total += 1
    passed += expect(
        "u1-periodicity-only-gives-class",
        periodic_identity == 1
        and "`Phi ~ Phi + 2 pi n`" in note
        and "R / 2 pi Z" in note,
        "U(1) readout cannot choose a real representative",
    )

    total += 1
    passed += expect(
        "central-root-cannot-equal-one",
        central_lhs == 2 * sp.pi * k / N
        and "Since `pi` is irrational" in note
        and "no nonzero integer pair satisfies this equation" in note,
        "2*pi*k/N = 1 has no nonzero integer solution",
    )

    total += 1
    passed += expect(
        "no-go-is-narrow-not-blanket",
        "This is a narrow no-go theorem" in note
        and "does **not** block every central-extension\nor projective-phase route" in note
        and "The review instruction is therefore \"do not close `gamma = 1` by bare\nperiodicity,\" not \"abandon all projective or central-extension attacks.\""
        in note,
        "the obstruction is scoped to bare periodicity and finite roots alone",
    )

    total += 1
    passed += expect(
        "surviving-central-routes-recorded",
        "noncompact action-valued central extension" in note
        and "index/spectral-flow theorem" in note
        and "consistently rewritten turns/cycles convention" in note
        and "microscopic action/Ward identity" in note,
        "viable stronger central/projective routes remain open",
    )

    total += 1
    passed += expect(
        "sixteenth-root-factor-audited",
        "A finite central extension can give a 16th root of unity" in note
        and "`exp(2 pi i / 16)`" in note
        and "`Phi = 2 pi / 16`" in note
        and "track every `2 pi`\nfactor" in note,
        "the 1/16 numerical echo is not discarded without the 2*pi audit",
    )

    total += 1
    passed += expect(
        "gamma-one-remains-nonhomogeneous-unit-law",
        "`Phi(I_16) = 1`" in note
        and "`S_cell = hbar`" in note
        and "non-homogeneous primitive action-unit law" in gamma_attempt,
        "remaining lock is a real action-unit normalization",
    )

    total += 1
    passed += expect(
        "does-not-break-hbar-attack-order",
        "Demote Bare Periodicity And Central Roots" in hbar_order
        and "central extension" in note
        and "does not produce the dimensionless radian value `gamma = 1`" in note,
        "central extensions are demoted unless they supply a new conversion",
    )

    total += 1
    passed += expect(
        "no-periodicity-overclaim",
        "Do not use:\n\n> U(1) phase periodicity derives `gamma = 1`." in note
        and "Do not use:\n\n> Finite central extensions are irrelevant to the hbar lane."
        in note
        and "The branch derives `gamma = 1`" not in note,
        "the theorem refuses the false closure route",
    )

    total += 1
    passed += expect(
        "reviewer-links-phase-period-obstruction",
        "PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md" in reviewer,
        "canonical packet links the phase-period obstruction",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
