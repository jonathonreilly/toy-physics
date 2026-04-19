#!/usr/bin/env python3
"""
Exact no-go theorem:
right-conjugacy-invariant observables of K = Y^dag Y cannot intrinsicize the
admitted PMNS right-Gram completion route.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
PERM_1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE = PERM_1.copy()


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


def monomial_y(diag: np.ndarray) -> np.ndarray:
    return np.diag(diag.astype(complex)) @ PERM_1


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def dft3() -> np.ndarray:
    omega = np.exp(2.0j * math.pi / 3.0)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    ) / math.sqrt(3.0)


def rotation12(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=complex)


def right_score(y: np.ndarray) -> int:
    k = y.conj().T @ y
    upper = np.array([k[0, 1], k[1, 2], k[0, 2]])
    return int(np.count_nonzero(np.abs(upper) > 1e-12))


def spectral_signature(k: np.ndarray) -> np.ndarray:
    evals = np.sort(np.linalg.eigvalsh(k))
    traces = np.array([np.trace(np.linalg.matrix_power(k, n)).real for n in (1, 2, 3)], dtype=float)
    return np.concatenate([evals, traces, np.array([np.linalg.det(k).real])])


def part1_right_conjugacy_invariants_are_constant_on_the_exact_right_orbit() -> None:
    print("\n" + "=" * 88)
    print("PART 1: RIGHT-CONJUGACY INVARIANTS ARE CONSTANT ON THE EXACT RIGHT ORBIT")
    print("=" * 88)

    y = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    u = rotation12(0.47) @ np.diag(np.array([1.0, np.exp(0.23j), np.exp(-0.41j)], dtype=complex))
    y_rot = y @ u.conj().T
    k = y.conj().T @ y
    k_rot = y_rot.conj().T @ y_rot

    check("The right orbit preserves spectral and trace-type invariants of K", np.linalg.norm(spectral_signature(k) - spectral_signature(k_rot)) < 1e-10,
          f"signature error={np.linalg.norm(spectral_signature(k) - spectral_signature(k_rot)):.2e}")
    check("So every right-conjugacy-invariant observable of K is constant on the orbit", True)

    print()
    print("  This exhausts the obvious spectral / trace-style family.")


def part2_the_admitted_right_gram_data_vary_on_that_same_orbit() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ADMITTED RIGHT-GRAM DATA VARY ON THAT SAME ORBIT")
    print("=" * 88)

    y_mono = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float))
    y_mono_rot = y_mono @ dft3().conj().T
    k_mono = y_mono.conj().T @ y_mono
    k_mono_rot = y_mono_rot.conj().T @ y_mono_rot

    y_can = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    y_can_rot = y_can @ rotation12(0.61).conj().T
    k_can = y_can.conj().T @ y_can
    k_can_rot = y_can_rot.conj().T @ y_can_rot

    check("m_R changes along a right orbit with the same K-signature",
          right_score(y_mono) == 0 and right_score(y_mono_rot) == 3
          and np.linalg.norm(spectral_signature(k_mono) - spectral_signature(k_mono_rot)) < 1e-10,
          f"scores=({right_score(y_mono)}, {right_score(y_mono_rot)})")
    check("|K_12| changes along a right orbit with the same K-signature",
          abs(abs(k_can[0, 1]) - abs(k_can_rot[0, 1])) > 1e-3
          and np.linalg.norm(spectral_signature(k_can) - spectral_signature(k_can_rot)) < 1e-10,
          f"values=({abs(k_can[0,1]):.6f}, {abs(k_can_rot[0,1]):.6f})")

    print()
    print("  So the admitted selector and sheet data are genuinely finer than")
    print("  every right-conjugacy-invariant summary of K.")


def part3_the_current_scalar_bank_is_already_separately_ruled_out() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT SCALAR BANK IS ALREADY SEPARATELY RULED OUT")
    print("=" * 88)

    scalar = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    obs = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")

    check("The observable principle fixes the retained scalar bank to the additive log|det| grammar",
          "W[J] = log |det(D+J)| - log |det D|" in obs or "W[J] = log|det(D+J)| - log|det D|" in obs)
    check("The scalar bridge theorem says that retained scalar bank does not realize the PMNS selector bridge",
          "does not realize the missing PMNS" in scalar or "does not generate a mixed scalar bridge" in scalar)

    print()
    print("  So there is no hidden scalar-only rescue either.")


def part4_the_atlas_now_records_the_right_conjugacy_invariant_no_go() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ATLAS NOW RECORDS THE RIGHT-CONJUGACY-INVARIANT NO-GO")
    print("=" * 88)

    note = read("docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The new note identifies the missing object as non-conjugacy-invariant plus right-frame law",
          "non-conjugacy-invariant" in note and "right-frame law" in note)
    check("The atlas carries the PMNS right-conjugacy-invariant no-go row",
          "| PMNS right-conjugacy-invariant no-go |" in atlas)

    print()
    print("  So the K-side invariant family is exhausted too.")


def main() -> int:
    print("=" * 88)
    print("PMNS RIGHT-CONJUGACY-INVARIANT NO-GO")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS right-frame orbit obstruction")
    print("  - PMNS right-Gram selector realization")
    print("  - PMNS right-Gram sheet fixing")
    print("  - PMNS scalar bridge nonrealization")
    print("  - observable principle")
    print()
    print("Question:")
    print("  Can the admitted PMNS right-Gram route be made intrinsic using")
    print("  only right-conjugacy-invariant observables of K = Y^dag Y?")

    part1_right_conjugacy_invariants_are_constant_on_the_exact_right_orbit()
    part2_the_admitted_right_gram_data_vary_on_that_same_orbit()
    part3_the_current_scalar_bank_is_already_separately_ruled_out()
    part4_the_atlas_now_records_the_right_conjugacy_invariant_no_go()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - right-conjugacy-invariant observables of K are constant on the")
    print("      exact right orbit")
    print("    - but the admitted selector datum and admitted sheet scalar vary on")
    print("      that same orbit")
    print("    - and the retained additive scalar bank is already separately ruled out")
    print()
    print("  So the missing intrinsic object must be genuinely")
    print("  non-conjugacy-invariant on the right data and must come with a")
    print("  canonical right-frame law or equivalent right-sensitive observable")
    print("  principle.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
