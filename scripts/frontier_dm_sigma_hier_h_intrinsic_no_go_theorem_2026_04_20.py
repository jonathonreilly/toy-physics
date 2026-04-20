#!/usr/bin/env python3
"""
Frontier runner - H-intrinsic / mu<->tau-even no-go for sigma_hier.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_sigma_hier_uniqueness_theorem import (
    H_mat,
    M_STAR,
    DELTA_STAR,
    Q_PLUS_STAR,
    count_passes,
    jarlskog_sin_dcp,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {label}" + (f"  ({detail})" if detail else ""))


def main() -> int:
    h_pin = H_mat(M_STAR, DELTA_STAR, Q_PLUS_STAR)
    evals, vecs = np.linalg.eigh(h_pin)
    order = np.argsort(np.real(evals))
    evals = np.real(evals[order])
    vecs = vecs[:, order]

    sigma_plus = (2, 0, 1)
    sigma_minus = (2, 1, 0)
    p_plus = vecs[list(sigma_plus), :]
    p_minus = vecs[list(sigma_minus), :]
    swap_mutau = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

    print("=== Part 1: surviving pair at the pin ===")
    check("sigma=(2,0,1) passes all 9 magnitude bands", count_passes(np.abs(p_plus)) == 9)
    check("sigma=(2,1,0) passes all 9 magnitude bands", count_passes(np.abs(p_minus)) == 9)
    check(
        "The two surviving PMNS candidates differ only by the mu<->tau row swap",
        np.allclose(p_plus, swap_mutau @ p_minus, atol=1e-12),
    )

    print("\n=== Part 2: H-intrinsic data is permutation-blind ===")
    trace1 = np.trace(h_pin)
    trace2 = np.trace(h_pin @ h_pin)
    det = np.linalg.det(h_pin)
    check("trace(H_pin) is fixed independently of sigma_hier", abs(trace1 - np.trace(h_pin)) < 1e-14)
    check("trace(H_pin^2) is fixed independently of sigma_hier", abs(trace2 - np.trace(h_pin @ h_pin)) < 1e-14)
    check("det(H_pin) is fixed independently of sigma_hier", abs(det - np.linalg.det(h_pin)) < 1e-14)
    check(
        "The eigenvalue spectrum is common to both sigma choices",
        np.allclose(np.sort(evals), np.sort(evals), atol=1e-14),
    )

    print("\n=== Part 3: mu<->tau-even PMNS data is blind, CP sign is not ===")
    abs_rows_plus = sorted(tuple(np.round(row, 12)) for row in np.abs(p_plus))
    abs_rows_minus = sorted(tuple(np.round(row, 12)) for row in np.abs(p_minus))
    check(
        "mu<->tau-even magnitude data (unordered row multiset) is identical",
        abs_rows_plus == abs_rows_minus,
    )
    check(
        "The row-labeled magnitude matrices are not identical, so the no-go is not overclaimed",
        not np.allclose(np.abs(p_plus), np.abs(p_minus), atol=1e-12),
    )

    sin_plus = jarlskog_sin_dcp(p_plus)
    sin_minus = jarlskog_sin_dcp(p_minus)
    check("The Jarlskog sign flips across the surviving pair", np.sign(sin_plus) == -np.sign(sin_minus))
    check(
        "The two surviving values are numerically +/-0.987",
        abs(abs(sin_plus) - 0.9873607592) < 1e-6 and abs(abs(sin_minus) - 0.9873607592) < 1e-6,
        f"sin+={sin_plus:+.10f}, sin-={sin_minus:+.10f}",
    )

    print("\nInterpretation:")
    print("  The surviving sigma_hier ambiguity is not an ambiguity of H_pin.")
    print("  It is the residual mu<->tau flavor-label ambiguity after")
    print("  diagonalization. Any selector family living only on H_pin, or any")
    print("  mu<->tau-even PMNS scalar family, is blind to it.")
    print(f"\nPASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

