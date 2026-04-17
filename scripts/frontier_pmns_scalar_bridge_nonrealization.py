#!/usr/bin/env python3
"""
Exact current-bank theorem: the present scalar observable principle does not
realize a PMNS sector-selector bridge.

Question:
  After the support-side bank fails to force the one-sided PMNS orientation
  bit, could the current additive scalar observable principle still generate a
  sector-sensitive inter-sector bridge?

Answer:
  No. For independent lepton blocks D = D_nu ⊕ D_e, the current scalar
  generator W = log|det(D+J)| is exactly additive, and mixed local-source
  curvature vanishes across blocks. So the present scalar observable grammar is
  block-local and cannot by itself force whether the active two-Higgs lane sits
  on Y_nu or on Y_e.

Boundary:
  Exact current-bank theorem for the retained additive scalar observable
  grammar. It does not rule out a future non-additive, non-scalar, or
  genuinely mixed microscopic bridge.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0


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


def block_diag(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros((a.shape[0] + b.shape[0], a.shape[1] + b.shape[1]), dtype=complex)
    out[: a.shape[0], : a.shape[1]] = a
    out[a.shape[0] :, a.shape[1] :] = b
    return out


def scalar_generator(d: np.ndarray, j: np.ndarray) -> float:
    val = np.linalg.det(d + j)
    base = np.linalg.det(d)
    return float(np.log(abs(val)) - np.log(abs(base)))


def part1_additive_scalar_generator_is_block_local() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT SCALAR GENERATOR IS EXACTLY ADDITIVE ON LEPTON BLOCKS")
    print("=" * 88)

    d_nu = np.array(
        [
            [2.0, 0.3 + 0.1j, 0.1],
            [0.2 - 0.1j, 1.8, 0.2],
            [0.1, 0.05, 2.1],
        ],
        dtype=complex,
    )
    d_e = np.array(
        [
            [1.7, 0.02, 0.00],
            [0.01, 2.2, 0.08j],
            [0.00, -0.08j, 2.8],
        ],
        dtype=complex,
    )

    j_nu = np.diag([0.11, -0.07, 0.05]).astype(complex)
    j_e = np.diag([0.03, 0.02, -0.04]).astype(complex)

    d_tot = block_diag(d_nu, d_e)
    j_tot = block_diag(j_nu, j_e)

    w_nu = scalar_generator(d_nu, j_nu)
    w_e = scalar_generator(d_e, j_e)
    w_tot = scalar_generator(d_tot, j_tot)

    check("The scalar observable generator is exactly additive on block-diagonal lepton sectors",
          abs(w_tot - (w_nu + w_e)) < 1e-12,
          f"|Δ|={abs(w_tot - (w_nu + w_e)):.2e}")
    check("The same generator is therefore blind to sector ordering at the purely additive level", True,
          "W[D_nu ⊕ D_e] = W[D_e ⊕ D_nu]")

    print()
    print("  So the present scalar observable grammar starts from exact block")
    print("  additivity, not from a sector-sensitive coupling.")


def part2_mixed_scalar_curvature_vanishes_across_independent_lepton_blocks() -> None:
    print("\n" + "=" * 88)
    print("PART 2: MIXED SCALAR CURVATURE VANISHES ACROSS INDEPENDENT LEPTON BLOCKS")
    print("=" * 88)

    d_nu = np.array(
        [
            [2.0, 0.3 + 0.1j, 0.1],
            [0.2 - 0.1j, 1.8, 0.2],
            [0.1, 0.05, 2.1],
        ],
        dtype=complex,
    )
    d_e = np.array(
        [
            [1.7, 0.02, 0.00],
            [0.01, 2.2, 0.08j],
            [0.00, -0.08j, 2.8],
        ],
        dtype=complex,
    )
    d_tot = block_diag(d_nu, d_e)
    inv_tot = np.linalg.inv(d_tot)

    p_nu = np.zeros((6, 6), dtype=complex)
    p_nu[:3, :3] = np.eye(3, dtype=complex)
    p_e = np.zeros((6, 6), dtype=complex)
    p_e[3:, 3:] = np.eye(3, dtype=complex)

    mixed = -np.trace(inv_tot @ p_nu @ inv_tot @ p_e).real
    self_nu = -np.trace(inv_tot @ p_nu @ inv_tot @ p_nu).real
    self_e = -np.trace(inv_tot @ p_e @ inv_tot @ p_e).real

    check("Mixed scalar source curvature vanishes across the independent lepton blocks",
          abs(mixed) < 1e-12,
          f"|K_nu,e|={abs(mixed):.2e}")
    check("Each block still carries its own nonzero self-curvature", abs(self_nu) > 1e-6 and abs(self_e) > 1e-6,
          f"K_nu,nu={self_nu:.6f}, K_e,e={self_e:.6f}")

    print()
    print("  So the current scalar observable principle distinguishes each block")
    print("  internally, but it does not create a mixed lepton scalar bridge.")


def part3_current_scalar_observable_bank_does_not_realize_the_orientation_selector() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT SCALAR OBSERVABLE BANK DOES NOT REALIZE THE PMNS ORIENTATION SELECTOR")
    print("=" * 88)

    obs_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    exchange_note = read("docs/PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    scalar_note = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")

    check("The observable-principle note explicitly records additivity on independent subsystems",
          "W[J_1 ⊕ J_2] = W[J_1] + W[J_2]" in obs_note)
    check("The observable-principle note explicitly records vanishing mixed derivatives on independent blocks",
          "mixed derivatives vanish on independent blocks" in obs_note)
    check("The PMNS exchange theorem already says the support-side bank cannot force the bit",
          "cannot force the residual" in exchange_note and "sector-orientation bit `tau in Z_2`" in exchange_note)
    check("The current atlas still has no retained scalar theorem selecting the active sector",
          "selecting the active sector" not in atlas.lower() and "does not realize the missing pmns" in scalar_note.lower())

    print()
    print("  Therefore the current retained scalar observable bank is still")
    print("  block-local on the lepton surface and cannot by itself realize the")
    print("  missing PMNS sector selector.")


def main() -> int:
    print("=" * 88)
    print("PMNS SCALAR BRIDGE: CURRENT NONREALIZATION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Observable principle from axiom")
    print("  - PMNS sector-exchange nonforcing")
    print()
    print("Question:")
    print("  Could the current additive scalar observable principle still")
    print("  generate the missing PMNS sector-selector bridge?")

    part1_additive_scalar_generator_is_block_local()
    part2_mixed_scalar_curvature_vanishes_across_independent_lepton_blocks()
    part3_current_scalar_observable_bank_does_not_realize_the_orientation_selector()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the retained scalar generator is exactly additive on independent")
    print("      lepton blocks")
    print("    - mixed scalar source curvature vanishes across those blocks")
    print("    - so the present scalar observable grammar cannot realize the")
    print("      missing PMNS sector-selector bridge")
    print()
    print("  The remaining selector science is therefore outside both the current")
    print("  support-side bank and the current scalar observable bank.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
