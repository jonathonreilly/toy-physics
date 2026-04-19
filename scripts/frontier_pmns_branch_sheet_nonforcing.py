#!/usr/bin/env python3
"""
Exact post-selector boundary theorem:
the current Hermitian branch-observable bank cannot force the residual Z2 sheet
on a selected canonical two-Higgs PMNS branch.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def canonical_h_from_params(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    ymat = np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE
    return ymat @ ymat.conj().T


def invariant_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def reconstruct_from_observables(obs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    d1, d2, d3, r12, r23, r31, phi = obs
    alpha = r12 * r12
    beta = r23 * r23
    gamma = r31 * r31
    a = d2 * d3 - beta
    b = d1 * d2 * d3 + gamma * d2 - alpha * d3 - beta * d1
    c = gamma * (d1 * d2 - alpha)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - np.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + np.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()

    def sheet(root: float) -> tuple[np.ndarray, np.ndarray]:
        t1 = root
        t2 = alpha / (d1 - t1)
        t3 = beta / (d2 - t2)
        x = np.sqrt(np.array([t1, t2, t3], dtype=float))
        y = np.sqrt(np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float))
        return x, y

    return sheet(float(roots[0])), sheet(float(roots[1]))


def part1_two_selected_branch_sheets_are_distinct_but_share_h() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TWO SELECTED-BRANCH SHEETS ARE DISTINCT BUT SHARE H")
    print("=" * 88)

    x = np.array([1.10, 1.30, 0.80], dtype=float)
    y = np.array([0.60, 0.70, 1.00], dtype=float)
    delta = 1.10
    h = canonical_h_from_params(x, y, delta)
    obs = invariant_coordinates(h)
    (x0, y0), (x1, y1) = reconstruct_from_observables(obs)
    h0 = canonical_h_from_params(x0, y0, delta)
    h1 = canonical_h_from_params(x1, y1, delta)
    sheet_distance = float(np.linalg.norm(x0 - x1) + np.linalg.norm(y0 - y1))

    check("The two reconstructed sheets are genuinely distinct Yukawa data", sheet_distance > 1e-6,
          f"sheet distance={sheet_distance:.6f}")
    check("The first sheet reproduces the branch Hermitian matrix", np.linalg.norm(h - h0) < 1e-10,
          f"H error={np.linalg.norm(h - h0):.2e}")
    check("The second sheet reproduces the same branch Hermitian matrix", np.linalg.norm(h - h1) < 1e-10,
          f"H error={np.linalg.norm(h - h1):.2e}")

    print()
    print("  So the residual Z2 ambiguity is real at the coefficient level,")
    print("  but invisible at the Hermitian level.")


def part2_every_current_h_based_branch_observable_is_sheet_even() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EVERY CURRENT H-BASED BRANCH OBSERVABLE IS SHEET-EVEN")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    h = canonical_h_from_params(x, y, delta)
    obs = invariant_coordinates(h)
    (x0, y0), (x1, y1) = reconstruct_from_observables(obs)
    h0 = canonical_h_from_params(x0, y0, delta)
    h1 = canonical_h_from_params(x1, y1, delta)
    evals0 = np.sort(np.real(np.linalg.eigvalsh(h0)))
    evals1 = np.sort(np.real(np.linalg.eigvalsh(h1)))
    j0 = np.imag(h0[0, 1] * h0[1, 2] * h0[2, 0])
    j1 = np.imag(h1[0, 1] * h1[1, 2] * h1[2, 0])

    check("The retained seven-coordinate observable grammar is identical on both sheets",
          np.linalg.norm(invariant_coordinates(h0) - invariant_coordinates(h1)) < 1e-12,
          f"obs error={np.linalg.norm(invariant_coordinates(h0) - invariant_coordinates(h1)):.2e}")
    check("The Hermitian spectra are identical on both sheets", np.allclose(evals0, evals1, atol=1e-12),
          f"evals0={np.round(evals0, 6)}, evals1={np.round(evals1, 6)}")
    check("Hermitian CP-odd data reconstructed from H are also identical", abs(j0 - j1) < 1e-12,
          f"J(H) difference={abs(j0 - j1):.2e}")

    print()
    print("  So every current retained branch observable that factors through H")
    print("  is sheet-even by construction.")


def part3_current_bank_records_the_sheet_nonforcing_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT BANK NOW RECORDS THE SHEET-NONFORCING ENDPOINT")
    print("=" * 88)

    note = read("docs/PMNS_BRANCH_SHEET_NONFORCING_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    packet = read("docs/publication/ci3_z3/NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md")

    check("The new note states that the residual sheet is invisible to the current Hermitian bank",
          "same Hermitian matrix" in note and "sheet-even" in note and "non-Hermitian" in note)
    check("The atlas carries the PMNS branch sheet nonforcing row",
          "| PMNS branch sheet nonforcing |" in atlas)
    check("The reviewer packet now records that the current Hermitian bank cannot force the residual sheet bit",
          "cannot force that residual" in packet and "non-Hermitian" in packet)

    print()
    print("  So the exact endpoint is sharper again: after selector realization,")
    print("  the residual sheet bit is not hidden inside the current Hermitian")
    print("  observable bank.")


def main() -> int:
    print("=" * 88)
    print("PMNS BRANCH SHEET NONFORCING")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - neutrino two-Higgs observable inverse problem")
    print("  - charged-lepton two-Higgs observable inverse problem")
    print()
    print("Question:")
    print("  After selector realization, can the current Hermitian branch bank")
    print("  fix the residual Z2 sheet on the selected two-Higgs branch?")

    part1_two_selected_branch_sheets_are_distinct_but_share_h()
    part2_every_current_h_based_branch_observable_is_sheet_even()
    part3_current_bank_records_the_sheet_nonforcing_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the two residual selected-branch sheets are distinct Yukawa")
    print("      data but give the same Hermitian matrix H")
    print("    - every retained branch observable that factors through H is")
    print("      therefore sheet-even")
    print("    - so the current Hermitian branch bank cannot force the residual")
    print("      Z2 sheet")
    print()
    print("  Any future sheet-fixing datum must be genuinely non-Hermitian or")
    print("  otherwise sensitive to information beyond H = Y Y^dag.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
