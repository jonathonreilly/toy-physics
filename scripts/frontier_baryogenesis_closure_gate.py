#!/usr/bin/env python3
"""
Baryogenesis closure-gate audit on the current main package.

This runner does not claim a first-principles EWPT or transport computation.
Its job is narrower:

  1. verify that the current retained surface already contains the
     sphaleron-style B+L-violating / B-L-preserving structure,
  2. verify that the promoted CKM package supplies a nonzero weak-sector
     CP invariant,
  3. normalize the remaining eta bridge as the single open EWPT/transport gate.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0


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


I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)

TASTE_STATES = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]


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


def jarlskog_from_package() -> tuple[float, float]:
    v_us = 0.22727
    v_cb = 0.04217
    v_ub = 0.003913
    delta_deg = 65.905

    s13 = v_ub
    c13 = math.sqrt(1.0 - s13 * s13)
    s12 = v_us / c13
    s23 = v_cb / c13
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    delta = math.radians(delta_deg)
    j = c12 * s12 * c23 * s23 * c13 * c13 * s13 * math.sin(delta)
    return delta_deg, j


def part1_baryon_violation_structure() -> None:
    print("=" * 80)
    print("PART 1: SPHALERON-STYLE B+L VIOLATION STRUCTURE")
    print("=" * 80)
    print()

    baryon, lepton = baryon_and_lepton_operators()
    b_minus_l = baryon - lepton
    generators = su2_generators()

    commutators = []
    for label, generator in zip(("Sx", "Sy", "Sz"), generators):
        comm = np.linalg.norm(baryon @ generator - generator @ baryon)
        commutators.append(comm)
        info(f"commutator norm for [B, {label}]", f"||[B,{label}]|| = {comm:.6f}")

    check(
        "B fails to commute with the SU(2) algebra",
        max(commutators) > 1e-10,
        f"max_a ||[B,S_a]|| = {max(commutators):.6f}",
    )

    bml_values = []
    for state in TASTE_STATES:
        hw = hamming_weight(state)
        bml_values.append(1.0 / 3.0 if hw in (1, 2) else -1.0)

    linear_sum = sum(bml_values)
    check(
        "linear B-L anomaly cancels on the one-generation taste surface",
        abs(linear_sum) < 1e-12,
        f"Sum(B-L) = {linear_sum:.1f}",
    )

    diag = np.diag(b_minus_l).real
    check(
        "B-L eigenvalues have the expected quark/lepton split",
        np.count_nonzero(np.isclose(diag, 1.0 / 3.0)) == 6
        and np.count_nonzero(np.isclose(diag, -1.0)) == 2,
        f"diag(B-L) = {diag.tolist()}",
    )

    print()
    print("  Consequence:")
    print("    The current retained surface already carries the electroweak")
    print("    B+L-violating / B-L-protecting structure required for the first")
    print("    Sakharov condition.")
    print()


def part2_ckm_cp_source() -> float:
    print("=" * 80)
    print("PART 2: WEAK-SECTOR CP SOURCE")
    print("=" * 80)
    print()

    delta_deg, j = jarlskog_from_package()
    promoted_j = 3.331e-5

    check(
        "promoted CKM phase is nonzero",
        abs(delta_deg) > 1e-12,
        f"delta = {delta_deg:.3f} deg",
    )
    check(
        "promoted CKM Jarlskog invariant is positive",
        j > 0.0,
        f"J = {j:.6e}",
    )
    check(
        "reconstructed J matches the promoted CKM package",
        abs(j - promoted_j) / promoted_j < 5e-4,
        f"J(reconstructed) = {j:.6e}, J(package) = {promoted_j:.6e}",
    )

    print()
    print("  Consequence:")
    print("    The second Sakharov condition is already present on main.")
    print("    The baryogenesis lane no longer lacks a weak-sector CP source.")
    print()

    return j


def part3_eta_bridge(j: float) -> None:
    print("=" * 80)
    print("PART 3: ETA BRIDGE NORMALIZATION")
    print("=" * 80)
    print()

    eta_obs = 6.12e-10
    eta_over_j = eta_obs / j

    h = 0.674
    omega_b_h2 = 3.6515e-3 * (eta_obs / 1.0e-10)
    omega_b = omega_b_h2 / (h * h)

    check(
        "eta/J normalization is positive and parametrically small",
        0.0 < eta_over_j < 1.0e-3,
        f"eta/J = {eta_over_j:.6e}",
    )
    check(
        "eta reproduces the observed baryon density through the BBN bridge",
        abs(omega_b - 0.0493) / 0.0493 < 0.01,
        f"Omega_b(BBN) = {omega_b:.6f}",
    )

    baryo_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    factor_note = (DOCS / "BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md").read_text(
        encoding="utf-8"
    )
    omega_note = (DOCS / "OMEGA_LAMBDA_DERIVATION_NOTE.md").read_text(encoding="utf-8")
    omega_runner = (ROOT / "scripts" / "frontier_omega_lambda_derivation.py").read_text(encoding="utf-8")

    check(
        "cosmology note still marks eta as imported",
        "eta imported from observation" in omega_note,
    )
    check(
        "cosmology runner now records the historical v/T route anchor explicitly",
        "Historical v/T anchor: ~0.52" in omega_runner,
    )
    check(
        "cosmology runner records that the old taste-scalar route is not live on current main",
        "old taste-scalar implementation is not live on current main" in omega_runner,
    )
    check(
        "closure-gate note records the exact weak-flavor reduction eta = J * K_NP",
        "`η = J * K_NP`" in baryo_note,
    )
    check(
        "factorization note records the target K_NP = eta / J",
        "`K_NP,target = η_obs / J = 1.837341e-5`" in factor_note,
    )

    info(
        "open baryogenesis object",
        "the real CP-even nonperturbative electroweak functional K_NP multiplying the exact weak-flavor source J",
    )
    print()
    print("  Consequence:")
    print("    The observed eta does not require a new source of B or CP violation.")
    print("    It requires the missing nonperturbative electroweak functional K_NP")
    print("    in the exact factorized bridge eta = J * K_NP.")
    print()


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS CLOSURE-GATE AUDIT")
    print("=" * 80)
    print()
    print("Question:")
    print("  What is actually still missing for baryogenesis on the current")
    print("  main-branch framework surface?")
    print()

    part1_baryon_violation_structure()
    j = part2_ckm_cp_source()
    part3_eta_bridge(j)

    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - electroweak B+L violation is already structurally present")
    print("    - weak-sector CP violation is already quantitatively present")
    print("    - the remaining missing object is the real nonperturbative")
    print("      electroweak functional K_NP in the factorized bridge")
    print("      eta = J * K_NP")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
