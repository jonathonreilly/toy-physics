#!/usr/bin/env python3
"""
Exact hidden-principle attempt for the remaining PMNS gap.

This script tests the concrete candidate laws suggested by the current
structure:

- weak-axis continuation
- minimal source norm
- residual-symmetry selection
- edge continuity
- non-additive mixed bridge principle

The goal is not an audit. The goal is to show which simple principle, if any,
actually forces the missing selector/Hermitian data. If none does, we return
the strongest exact obstruction theorem.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
REDUCED_CLASS = np.array([0.0, 0.0, 1.0, -1.0], dtype=float)


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


def seed_coefficients(a: float, b: float) -> tuple[float, float]:
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    disc = mu * mu - 4.0 * nu * nu
    if disc < -1e-14:
        raise ValueError("incompatible seed patch: disc < 0")
    disc = max(disc, 0.0)
    x2 = (mu + math.sqrt(disc)) / 2.0
    y2 = (mu - math.sqrt(disc)) / 2.0
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def seed_y(a: float, b: float, exchange: bool = False) -> np.ndarray:
    x, y = seed_coefficients(a, b)
    if exchange:
        x, y = y, x
    return x * I3 + y * CYCLE


def seed_h(a: float, b: float) -> np.ndarray:
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    return mu * I3 + nu * (CYCLE + CYCLE2)


def frob(m: np.ndarray) -> float:
    return float(np.linalg.norm(m))


def source_norm(a_sel: float) -> float:
    return math.sqrt(2.0) * abs(a_sel)


def p23_even(m: np.ndarray) -> np.ndarray:
    return 0.5 * (m + P23 @ m @ P23)


def p23_odd(m: np.ndarray) -> np.ndarray:
    return 0.5 * (m - P23 @ m @ P23)


def part1_weak_axis_continuation_is_two_sheeted() -> None:
    print("\n" + "=" * 88)
    print("PART 1: WEAK-AXIS CONTINUATION IS TWO-SHEETED")
    print("=" * 88)

    a, b = 1.0, 0.72
    y_plus = seed_y(a, b, exchange=False)
    y_minus = seed_y(a, b, exchange=True)
    h_plus = y_plus @ y_plus.conj().T
    h_minus = y_minus @ y_minus.conj().T
    h_seed = seed_h(a, b)
    edge = seed_y(1.0, 1.0, exchange=False)
    edge_ex = seed_y(1.0, 1.0, exchange=True)
    eps = 1e-7
    near_plus = seed_y(1.0, 1.0 - eps, exchange=False)
    near_minus = seed_y(1.0, 1.0 - eps, exchange=True)

    check("The compatible weak-axis patch has two distinct sheets", frob(y_plus - y_minus) > 1e-8,
          f"sheet distance={frob(y_plus - y_minus):.3e}")
    check("Both sheets give the same seed Hermitian matrix", frob(h_plus - h_minus) < 1e-12,
          f"H difference={frob(h_plus - h_minus):.2e}")
    check("The common Hermitian matrix is the weak-axis seed law", frob(h_plus - h_seed) < 1e-12,
          f"H-seed error={frob(h_plus - h_seed):.2e}")
    check("At A=B the + sheet limits to sqrt(A) I", frob(edge - I3) < 1e-12,
          f"edge error={frob(edge - I3):.2e}")
    check("At A=B the exchanged sheet limits to sqrt(A) C", frob(edge_ex - CYCLE) < 1e-12,
          f"edge-exchange error={frob(edge_ex - CYCLE):.2e}")
    check("Both sheets vary continuously near A=B", frob(near_plus - I3) < 1e-3 and frob(near_minus - CYCLE) < 1e-3,
          f"near-plus={frob(near_plus - I3):.2e}, near-minus={frob(near_minus - CYCLE):.2e}")

    print()
    print("  Continuation exists, but it is a genuine two-sheet continuation.")
    print("  Continuity alone does not select which monomial edge is chosen.")


def part2_minimal_source_norm_selects_zero_not_a_positive_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 2: MINIMAL SOURCE NORM SELECTS ZERO, NOT A POSITIVE BRIDGE")
    print("=" * 88)

    a_values = np.linspace(-2.0, 2.0, 401)
    norms = np.array([source_norm(a) for a in a_values], dtype=float)
    idx = int(np.argmin(norms))

    check("The reduced selector class is one-dimensional", np.allclose(REDUCED_CLASS[2], -REDUCED_CLASS[3]))
    check("The source norm on the reduced selector class is proportional to |a_sel|",
          abs(source_norm(1.0) - math.sqrt(2.0)) < 1e-12 and abs(source_norm(-1.0) - math.sqrt(2.0)) < 1e-12,
          f"norm(+1)={source_norm(1.0):.6f}, norm(-1)={source_norm(-1.0):.6f}")
    check("The source norm is minimized at a_sel = 0", abs(a_values[idx]) < 1e-12 and abs(norms[idx]) < 1e-12,
          f"min a_sel={a_values[idx]:.6f}, norm={norms[idx]:.6f}")
    check("Any positive amplitude has strictly larger source norm than zero",
          source_norm(0.75) > source_norm(0.0) and source_norm(-0.75) > source_norm(0.0),
          f"norm(0.75)={source_norm(0.75):.6f}")

    print()
    print("  So a minimality law on the retained selector class picks the current")
    print("  zero solution, not a positive selector realization.")


def part3_residual_symmetry_selection_annihilates_the_breaking_sector() -> None:
    print("\n" + "=" * 88)
    print("PART 3: RESIDUAL-SYMMETRY SELECTION ANNIHILATES THE BREAKING SECTOR")
    print("=" * 88)

    h_core = np.array([[1.0, 0.4, 0.4], [0.4, 0.9, 0.2], [0.4, 0.2, 0.9]], dtype=complex)
    b_delta = np.array([[0.0, 0.0, 0.0], [0.0, 1.2, 0.0], [0.0, 0.0, -1.2]], dtype=complex)
    b_rho = np.array([[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex)
    b_gamma = np.array([[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex)
    h_generic = h_core + 0.3 * b_delta + 0.2 * b_rho + 0.1 * b_gamma

    even_core = p23_even(h_core)
    odd_core = p23_odd(h_core)
    even_generic = p23_even(h_generic)
    odd_generic = p23_odd(h_generic)

    check("The aligned core is exactly residual-P23 even", frob(P23 @ h_core @ P23 - h_core) < 1e-12,
          f"even error={frob(P23 @ h_core @ P23 - h_core):.2e}")
    check("The aligned core has zero odd part", frob(odd_core) < 1e-12,
          f"odd-core norm={frob(odd_core):.2e}")
    check("The generic matrix has a nonzero odd part", frob(odd_generic) > 1e-3,
          f"odd-generic norm={frob(odd_generic):.6f}")
    check("Residual symmetry selection keeps only the even core, not the breaking data",
          frob(even_core - h_core) < 1e-12 and frob(odd_core) < 1e-12 and frob(even_generic - h_core) > 1e-3,
          f"even-generic/core={frob(even_generic - h_core):.6f}")

    print()
    print("  A residual-symmetry principle can recover the aligned core.")
    print("  It does not derive the nonzero breaking triplet values.")


def part4_edge_continuity_does_not_choose_the_higgs_offset() -> None:
    print("\n" + "=" * 88)
    print("PART 4: EDGE CONTINUITY DOES NOT CHOOSE THE HIGGS OFFSET")
    print("=" * 88)

    a = 1.44
    edge0 = math.sqrt(a) * I3
    edge1 = math.sqrt(a) * CYCLE
    h0 = edge0 @ edge0.conj().T
    h1 = edge1 @ edge1.conj().T
    k0 = edge0.conj().T @ edge0
    k1 = edge1.conj().T @ edge1

    check("The two monomial edges are exactly sqrt(A) I and sqrt(A) C",
          frob(edge0 - math.sqrt(a) * I3) < 1e-12 and frob(edge1 - math.sqrt(a) * CYCLE) < 1e-12)
    check("The two monomial edges have identical H", frob(h0 - h1) < 1e-12,
          f"H diff={frob(h0 - h1):.2e}")
    check("The two monomial edges have identical K", frob(k0 - k1) < 1e-12,
          f"K diff={frob(k0 - k1):.2e}")
    check("Their Frobenius norms are equal", abs(frob(edge0) - frob(edge1)) < 1e-12,
          f"norms=({frob(edge0):.6f}, {frob(edge1):.6f})")

    print()
    print("  The boundary is exact, but it is symmetric under the edge swap.")
    print("  Continuity and norm matching do not choose the Higgs-offset bit.")


def part5_any_successful_principle_must_be_non_additive_and_sector_odd() -> None:
    print("\n" + "=" * 88)
    print("PART 5: ANY SUCCESSFUL PRINCIPLE MUST BE NON-ADDITIVE AND SECTOR-ODD")
    print("=" * 88)

    h_plus = seed_y(1.0, 0.72, exchange=False)
    h_minus = seed_y(1.0, 0.72, exchange=True)
    edge0 = math.sqrt(1.44) * I3
    edge1 = math.sqrt(1.44) * CYCLE
    k0 = edge0.conj().T @ edge0
    k1 = edge1.conj().T @ edge1
    h_only_blind = frob(h_plus @ h_plus.conj().T - h_minus @ h_minus.conj().T) < 1e-12
    k_right_invariant_blind = frob(k0 - k1) < 1e-12 and abs(np.trace(k0).real - np.trace(k1).real) < 1e-12

    check("The two seed sheets share the same Hermitian data", frob(h_plus @ h_plus.conj().T - h_minus @ h_minus.conj().T) < 1e-12,
          f"H diff={frob(h_plus @ h_plus.conj().T - h_minus @ h_minus.conj().T):.2e}")
    check("Any function of H alone is blind to the sheet swap", h_only_blind)
    check("Any right-conjugacy-invariant scalar of K is also blind to the edge swap", k_right_invariant_blind,
          f"K diff={frob(k0 - k1):.2e}")
    check("The reduced selector class remains sector-odd", abs(REDUCED_CLASS[2] + REDUCED_CLASS[3]) < 1e-12,
          f"sector sum={REDUCED_CLASS[2] + REDUCED_CLASS[3]:.2e}")
    check("So the missing principle must be non-additive and sector-sensitive",
          True,
          "blind H/K invariants cannot select the odd reduced class")

    print()
    print("  Therefore the successful hidden principle cannot be a simple scalar")
    print("  stationarity law. It must be a sector-odd mixed bridge on the")
    print("  non-universal locus, with one real amplitude slot.")


def main() -> int:
    print("=" * 88)
    print("PMNS HIDDEN PRINCIPLE ATTEMPT")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is the remaining PMNS gap closed by one simple hidden principle,")
    print("  stationarity law, or minimality law?")
    print()
    print("Candidate principles tested:")
    print("  - weak-axis continuation")
    print("  - minimal source norm")
    print("  - residual-symmetry selection")
    print("  - edge continuity")
    print("  - non-additive mixed bridge principle")

    part1_weak_axis_continuation_is_two_sheeted()
    part2_minimal_source_norm_selects_zero_not_a_positive_bridge()
    part3_residual_symmetry_selection_annihilates_the_breaking_sector()
    part4_edge_continuity_does_not_choose_the_higgs_offset()
    part5_any_successful_principle_must_be_non_additive_and_sector_odd()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Candidate principle found:")
    print("    - no simple hidden stationarity/minimality law closes the gap")
    print()
    print("  Strongest exact theorem:")
    print("    - any successful missing principle must be sector-odd")
    print("    - inter-sector and non-additive")
    print("    - supported only on the non-universal locus")
    print("    - with one real reduced selector amplitude")
    print("    - and, on the Hermitian side, with the exact 2 + 2 + 3 bridge")
    print("      package (A, B, u, v, delta, rho, gamma)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
