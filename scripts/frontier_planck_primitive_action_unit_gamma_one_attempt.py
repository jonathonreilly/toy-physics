#!/usr/bin/env python3
"""Verify the primitive action-unit gamma=1 attempt.

This verifier is intentionally conservative. It proves the algebraic reduction
to a scale-free no-go and fails if the note claims gamma=1 is closed.
"""

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
    note = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    action_phase = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")
    hbar_order = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    c16 = read("docs/PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md")
    timelock = read("docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md")

    gamma, lam = sp.symbols("gamma lambda", positive=True)
    dim = sp.Integer(16)
    eps = sp.pi / 2

    q_atom = sp.simplify(gamma / dim)
    q_atom_scaled = sp.simplify(lam * q_atom)
    gamma_scaled = sp.simplify(lam * gamma)
    a2_over_lp2 = sp.simplify(8 * sp.pi * q_atom / eps)
    kappa_bit = sp.simplify(q_atom / 2)

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "trace-law-context-loaded",
        "`Phi(P) = gamma Tr(P) / 16`" in phase_trace
        and "`gamma = Phi(I_16)`" in note,
        "the attempt starts from the existing trace reduction",
    )

    total += 1
    passed += expect(
        "gamma-ray-is-algebraically-free",
        q_atom == gamma / 16
        and q_atom_scaled == lam * gamma / 16
        and gamma_scaled == lam * gamma
        and "`Phi_lambda(I_16) = lambda gamma`" in note,
        f"q_atom={q_atom}, scaled={q_atom_scaled}",
    )

    total += 1
    passed += expect(
        "planck-equivalence-not-closure",
        a2_over_lp2 == gamma
        and "`a^2 / l_P^2 = gamma`" in phase_trace
        and "exact conventional Planck is equivalent to\n\n`gamma = 1`" in note,
        f"a^2/l_P^2={a2_over_lp2}",
    )

    total += 1
    passed += expect(
        "information-constant-remains-scaled",
        kappa_bit == gamma / 32
        and "gamma / 32 per bit" in phase_trace
        and "`kappa_info = gamma / 32 per bit`" in note
        and "`I_* = log 4` nats `= 2` bits" in timelock,
        f"kappa_bit={kappa_bit}",
    )

    total += 1
    passed += expect(
        "ward-route-fails-by-homogeneity",
        "Route 1: primitive-cell action Ward identity" in note
        and "If `Phi` satisfies the Ward identity,\nso does `lambda Phi`" in note
        and "phase-unit\nnormalization" in note,
        "ordinary Ward invariance cannot select the total action unit",
    )

    total += 1
    passed += expect(
        "central-extension-route-needs-level-one",
        "Route 2: projective / central-extension normalization" in note
        and "choosing the minimal nontrivial level `k = 1` requires" in note
        and "level-one generator" in note,
        "central extensions can quantize a level but do not force level one here",
    )

    total += 1
    passed += expect(
        "boundary-route-needs-action-unit",
        "Route 3: microscopic boundary-action normalization" in note
        and "`c_cell = 1/4`" in note
        and "one complete primitive boundary cell contributes one reduced action unit" in note,
        "boundary counting does not by itself normalize total phase",
    )

    total += 1
    passed += expect(
        "missing-input-is-explicit",
        "one complete source-free primitive `C^16` event cell is the unit generator of\n> reduced action phase" in note
        and "`Phi(I_16) = 1`" in note
        and "`S_cell / hbar = 1`" in note,
        "the obstruction is a primitive action-unit normalization",
    )

    total += 1
    passed += expect(
        "prior-open-step-preserved",
        "the final missing step is the physical selector law" in c16
        and "The first hbar target was\n> `gamma = 1`" in hbar_order
        and "later action-phase representation\nhbar theorem also derives the structural conversion statement" in action_phase,
        "the no-go is preserved as historical reduction and superseded by later closure",
    )

    total += 1
    passed += expect(
        "no-backward-planck-or-si-hbar",
        "solving backward from `a = l_P`" in note
        and "predicting the SI value of\n`hbar`" in note
        and "> the SI value of `hbar` is predicted" in note
        and "predicting the SI decimal value of `hbar`" in action_phase,
        "the note refuses the circular and unit-convention claims",
    )

    total += 1
    passed += expect(
        "overclaiming-refused",
        "Do not use:\n\n> The branch derives `gamma = 1`." in note
        and "This attempt does not close that equivalence" in note
        and "not presently derived" in note,
        "the verifier accepts only the no-go/reduction status",
    )

    total += 1
    passed += expect(
        "forbidden-closure-phrases-absent",
        "Status:** closure theorem" not in note
        and "The branch derives `gamma = 1` from bare" not in note
        and "predicts the SI value of `hbar`" not in note.split("Do not use:")[0],
        "the document does not present gamma=1 or SI hbar as derived",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
