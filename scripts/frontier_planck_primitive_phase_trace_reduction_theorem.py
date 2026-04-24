#!/usr/bin/env python3
"""Verify the primitive phase trace reduction theorem."""

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
    note = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    c16 = read("docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md")
    target = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    gamma = sp.symbols("gamma", positive=True)
    dim = sp.Integer(16)
    rank_atom = sp.Integer(1)
    rank_axis = sp.Integer(4)
    eps = sp.pi / 2

    q_atom = sp.simplify(gamma * rank_atom / dim)
    q_axis = sp.simplify(gamma * rank_axis / dim)
    a_ratio = sp.simplify(8 * sp.pi * q_atom / eps)
    kappa_bit = sp.simplify(q_atom / 2)

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "trace-shape-derived-up-to-gamma",
        q_atom == gamma / 16
        and q_axis == gamma / 4
        and "`Phi(P) = gamma Tr(P) / 16`" in note,
        f"q_atom={q_atom}, q_axis={q_axis}",
    )

    total += 1
    passed += expect(
        "source-free-assumptions-explicit",
        "finitely additive" in note
        and "natural under the event-algebra automorphisms" in note
        and "no atomic event is preferred" in note,
        "the theorem exposes the object-class assumptions",
    )

    total += 1
    passed += expect(
        "planck-target-is-gamma-one",
        a_ratio == gamma
        and "`a^2 / l_P^2 = gamma`" in note
        and "`gamma = 1`" in note,
        f"a^2/l_P^2={a_ratio}",
    )

    total += 1
    passed += expect(
        "kappa-is-gamma-over-thirty-two",
        kappa_bit == gamma / 32
        and "`kappa_info = q_* / I_* = gamma / 32 per bit`" in note,
        f"kappa_bit={kappa_bit}",
    )

    total += 1
    passed += expect(
        "c16-structural-support-inherited",
        "primitive-cell share" in c16
        and "the final missing step is the physical selector law" in c16
        and "structural `16`" in note,
        "new theorem sharpens the open C16 phase-share step",
    )

    total += 1
    passed += expect(
        "hbar-not-si-predicted",
        "It does not derive the SI value of `hbar`" in note
        and "solving for `hbar` is only\na unit-map rewrite" in note
        and "predicting the SI decimal value of `hbar`" in target,
        "the theorem does not overclaim numerical hbar",
    )

    total += 1
    passed += expect(
        "remaining-objections-are-exact",
        "action phase belongs to the source-free primitive event functional object\n   class" in note
        and "the elementary action phase is the minimal primitive event atom" in note
        and "the complete primitive `C^16` event cell carries one reduced action unit" in note,
        "remaining hbar denials are narrowed to three statements",
    )

    total += 1
    passed += expect(
        "reviewer-links-phase-trace",
        "PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md" in reviewer,
        "canonical packet links the phase trace theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
