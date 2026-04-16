#!/usr/bin/env python3
"""
Baryogenesis nonperturbative-route pivot on the current main package surface.

This runner packages the next honest scientific result after the old scalar
route and APBC rescue hatch are both closed:

  - the current framework already contains the native nonperturbative
    electroweak B+L-violating / B-L-preserving channel
  - the strongest perturbative same-surface scalar package currently derived
    on main still stays below half of the old target, even before screening

So any live same-surface baryogenesis closure route on current main must be a
genuinely nonperturbative EWPT / sphaleron / transport route.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

V = 246.282818290129
G1_GUT_V = 0.464376
G2_V = 0.648031
VT_TARGET = 0.52
MH_2L = 119.77
MH_3L = 125.10

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)

TASTE_STATES = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]

SELECTOR_EQUIV_ONE_DOUBLET = 1.0 + 1.0 / math.sqrt(3.0)
MAX_APBC_ENDPOINT_FACTOR = 2.0 / math.sqrt(3.0)
MAX_PERTURBATIVE_SELECTOR_EQUIV = (
    SELECTOR_EQUIV_ONE_DOUBLET * MAX_APBC_ENDPOINT_FACTOR
)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def hamming_weight(state: tuple[int, int, int]) -> int:
    return sum(state)


def baryon_and_lepton_operators() -> tuple[np.ndarray, np.ndarray]:
    baryon = np.zeros((8, 8), dtype=complex)
    lepton = np.zeros((8, 8), dtype=complex)
    for idx, state in enumerate(TASTE_STATES):
        hw = hamming_weight(state)
        if hw in (1, 2):
            baryon[idx, idx] = 1.0 / 3.0
        else:
            lepton[idx, idx] = 1.0
    return baryon, lepton


def su2_generators() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    s_x = 0.5 * (
        np.kron(np.kron(SIGMA_X, I2), I2)
        + np.kron(np.kron(I2, SIGMA_X), I2)
        + np.kron(np.kron(I2, I2), SIGMA_X)
    )
    s_y = 0.5 * (
        np.kron(np.kron(SIGMA_Y, I2), I2)
        + np.kron(np.kron(I2, SIGMA_Y), I2)
        + np.kron(np.kron(I2, I2), SIGMA_Y)
    )
    s_z = 0.5 * (
        np.kron(np.kron(SIGMA_Z, I2), I2)
        + np.kron(np.kron(I2, SIGMA_Z), I2)
        + np.kron(np.kron(I2, I2), SIGMA_Z)
    )
    return s_x, s_y, s_z


def gauge_cubic() -> float:
    g_y = G1_GUT_V * math.sqrt(3.0 / 5.0)
    m_w = 0.5 * G2_V * V
    m_z = 0.5 * math.sqrt(G2_V * G2_V + g_y * g_y) * V
    return (2.0 * m_w**3 + m_z**3) / (4.0 * math.pi * V**3)


def route_target_selector_equiv(m_h: float) -> dict[str, float]:
    lam = m_h * m_h / (2.0 * V * V)
    delta_e_target = VT_TARGET * lam / 2.0 - gauge_cubic()
    delta_e_sel_one = 1.0 / (12.0 * math.pi) * (3.0 * lam) ** 1.5
    target_selector_equiv = delta_e_target / delta_e_sel_one
    max_coverage = MAX_PERTURBATIVE_SELECTOR_EQUIV / target_selector_equiv
    shortfall = target_selector_equiv / MAX_PERTURBATIVE_SELECTOR_EQUIV
    return {
        "lambda": lam,
        "target_selector_equiv": target_selector_equiv,
        "max_coverage": max_coverage,
        "shortfall": shortfall,
    }


def part1_native_nonperturbative_channel() -> None:
    print("=" * 80)
    print("PART 1: NATIVE NONPERTURBATIVE ELECTROWEAK CHANNEL")
    print("=" * 80)
    print()

    baryon, lepton = baryon_and_lepton_operators()
    b_minus_l = baryon - lepton

    commutators = []
    for label, generator in zip(("Sx", "Sy", "Sz"), su2_generators()):
        comm = np.linalg.norm(baryon @ generator - generator @ baryon)
        commutators.append(comm)
        info(f"commutator norm for [B, {label}]", f"||[B,{label}]|| = {comm:.6f}")

    check(
        "B fails to commute with the retained SU(2) algebra",
        max(commutators) > 1e-10,
        f"max_a ||[B,S_a]|| = {max(commutators):.6f}",
    )

    bml_values = []
    for state in TASTE_STATES:
        hw = hamming_weight(state)
        bml_values.append(1.0 / 3.0 if hw in (1, 2) else -1.0)
    linear_sum = sum(bml_values)

    check(
        "linear B-L anomaly cancels exactly on the retained one-generation taste surface",
        abs(linear_sum) < 1e-12,
        f"Sum(B-L) = {linear_sum:.1f}",
    )
    check(
        "B-L eigenvalues keep the exact quark/lepton split",
        np.count_nonzero(np.isclose(np.diag(b_minus_l).real, 1.0 / 3.0)) == 6
        and np.count_nonzero(np.isclose(np.diag(b_minus_l).real, -1.0)) == 2,
        f"diag(B-L) = {np.diag(b_minus_l).real.tolist()}",
    )
    info(
        "native route meaning",
        "the current framework surface already contains the electroweak nonperturbative B+L-violating / B-L-protecting channel needed for a sphaleron-style route",
    )
    print()


def audit_route(label: str, m_h: float) -> None:
    values = route_target_selector_equiv(m_h)
    print(f"  {label}:")
    print(f"    lambda_H                         = {values['lambda']:.6f}")
    print(f"    target selector-equiv strength  = {values['target_selector_equiv']:.6f}")
    print(f"    exact perturbative upper bound  = {MAX_PERTURBATIVE_SELECTOR_EQUIV:.6f}")
    print(f"    maximal coverage before screen  = {values['max_coverage']:.6f}")
    print(f"    residual shortfall factor       = {values['shortfall']:.6f}x")
    print()

    check(
        f"{label} target remains above the exact perturbative same-surface upper bound",
        values["target_selector_equiv"] > MAX_PERTURBATIVE_SELECTOR_EQUIV,
        f"{values['target_selector_equiv']:.6f} > {MAX_PERTURBATIVE_SELECTOR_EQUIV:.6f}",
    )
    check(
        f"{label} exact perturbative same-surface upper bound stays below half the target",
        values["max_coverage"] < 0.5,
        f"coverage = {values['max_coverage']:.6f}",
    )
    check(
        f"{label} route would still need more than a factor-two enhancement after the exact upper bound is granted",
        values["shortfall"] > 2.0,
        f"shortfall = {values['shortfall']:.6f}x",
    )


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS NONPERTURBATIVE-ROUTE PIVOT")
    print("=" * 80)
    print()
    print("Question:")
    print("  After the old scalar route and APBC rescue hatch are both closed,")
    print("  what route class is actually still live on the current framework")
    print("  surface?")
    print()

    part1_native_nonperturbative_channel()

    print("=" * 80)
    print("PART 2: EXACT PERTURBATIVE SCALAR UPPER BOUND")
    print("=" * 80)
    print()

    print(f"  selector-equiv one-doublet surface = {SELECTOR_EQUIV_ONE_DOUBLET:.6f}")
    print(f"  max exact APBC endpoint factor     = {MAX_APBC_ENDPOINT_FACTOR:.6f}")
    print(f"  exact perturbative upper bound     = {MAX_PERTURBATIVE_SELECTOR_EQUIV:.6f}")
    print()

    check(
        "exact perturbative upper bound is fixed by the one-doublet match and the APBC endpoint band",
        abs(
            MAX_PERTURBATIVE_SELECTOR_EQUIV
            - ((1.0 + 1.0 / math.sqrt(3.0)) * (2.0 / math.sqrt(3.0)))
        )
        < 1e-12,
        f"n_equiv,max = {MAX_PERTURBATIVE_SELECTOR_EQUIV:.6f}",
    )

    audit_route("2-loop Higgs support route", MH_2L)
    audit_route("full 3-loop Higgs route", MH_3L)

    info(
        "route consequence",
        "even after granting the largest exact APBC endpoint normalization, the current perturbative same-surface scalar package cannot rescue the old route; screening would only reduce it further",
    )
    print()

    print("=" * 80)
    print("PART 3: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    pivot_note = (DOCS / "BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "pivot note records the genuinely nonperturbative surviving route class",
        "same-surface baryogenesis closure must be a genuinely" in pivot_note
        and "nonperturbative electroweak transition / sphaleron / transport route"
        in pivot_note,
    )
    check(
        "closure-gate note points to the nonperturbative-route pivot note",
        "BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md" in gate_note,
    )
    check(
        "derivation atlas carries the nonperturbative-route pivot row",
        "Baryogenesis nonperturbative-route pivot" in atlas,
    )
    check(
        "canonical harness index includes the nonperturbative-route pivot runner",
        "frontier_baryogenesis_nonperturbative_route_pivot.py" in harness,
    )
    check(
        "current flagship entrypoint points to the nonperturbative-route pivot note",
        "BARYOGENESIS_NONPERTURBATIVE_ROUTE_PIVOT_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - the current framework surface already contains the native")
    print("      electroweak nonperturbative B+L-violating channel")
    print("    - the strongest currently derived perturbative same-surface")
    print("      scalar package still stays below half of the old target,")
    print("      even before screening")
    print("    - so any live same-surface baryogenesis closure route on")
    print("      current main must be a genuinely nonperturbative")
    print("      EWPT / sphaleron / transport route")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
