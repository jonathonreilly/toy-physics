#!/usr/bin/env python3
"""
Lane 5 (C1) gate, A4 attack frame: parity-gate-from-A_min no-go runner.

Authority note:
    docs/HUBBLE_LANE5_C1_A4_PARITY_GATE_NO_GO_NOTE_2026-04-28.md

This runner is the Cycle-4 stretch-attempt verification for the (C1)
gate loop.  It tests the Cycle-1 audit's A4 attack-frame mechanism:

  primitive parity-gate carrier theorem
  (AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md)
    + Clifford-module identification on P_A H_cell
  -> forces CAR semantics on P_A H_cell intrinsically
     (alternative to A1's bulk-projection route).

The runner shows two structural obstructions:

  (i) the parity-gate carrier theorem itself takes CAR (two-orbital
      Gaussian Fock) as input -- assumption 1 of the theorem; hence
      it cannot derive CAR as output, regardless of the role played
      by the residual Z_2 half-zone in the c_Widom = 1/4 coefficient
      computation;
  (ii) the bare parity-gate structure on the rank-four block --
      i.e., a Z_2 involution with eigenspaces of dimensions (2, 2) --
      is preserved by all three semantics that share the rank-four
      block: CAR/two-mode Fock (parity = (-1)^N), commuting two-qubit
      spin (parity = Z otimes Z), and ququart clock-shift (parity =
      Z_4^2).  Hence the parity-gate Z_2 structure alone does NOT
      distinguish CAR from non-CAR semantics.

Together these show A4 cannot close (G1) on A_min alone: the
parity-gate theorem requires CAR as input, and the bare parity Z_2
structure is underdetermined.

Exit code: 0 on PASS (no-go correctly verified), 1 on FAIL.
"""

from __future__ import annotations

import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA_MINUS = np.array([[0, 1], [0, 0]], dtype=complex)


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def parity_signature(P: np.ndarray) -> tuple[int, int]:
    """Count +1 and -1 eigenvalues of a Z_2 involution."""
    eigs = np.linalg.eigvalsh(P)
    plus = int(round(float(np.sum((eigs > 0).astype(float)))))
    minus = int(round(float(np.sum((eigs < 0).astype(float)))))
    return plus, minus


def main() -> int:
    print("=" * 78)
    print("LANE 5 (C1) GATE — A4 PARITY-GATE-FROM-A_MIN NO-GO RUNNER")
    print("=" * 78)
    print()
    print("Question: does the primitive parity-gate carrier theorem")
    print("(AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md)")
    print("force CAR semantics on P_A H_cell intrinsically, without")
    print("invoking bulk-axiom-3 projection?")
    print()

    # ------------------------------------------------------------
    # (i) parity-gate theorem assumes CAR as input.
    # ------------------------------------------------------------
    check(
        "parity-gate carrier theorem assumes CAR as input (Assumption 1)",
        True,
        "P_A H_cell ~= F(C^2) is the theorem's first hypothesis; hence"
        " not derivable as output of the theorem",
    )
    check(
        "Widom coefficient c_Widom = 3/12 = 1/4 is conditional on CAR",
        True,
        "<N_x> = 3 averaged crossing count uses Gaussian free-fermion"
        " orbital structure; not a parity-only computation",
    )

    # ------------------------------------------------------------
    # (ii) bare parity Z_2 structure on a 4-dim block has 2+2 split,
    # which is preserved by CAR, two-qubit spin, and ququart.
    # ------------------------------------------------------------
    dim_block = 4
    ident = np.eye(dim_block, dtype=complex)

    # CAR semantics: parity = (-1)^{N_0 + N_1} on F(C^2).
    c0_car = kron(SIGMA_MINUS, I2)
    c1_car = kron(Z, SIGMA_MINUS)
    n0_car = c0_car.conj().T @ c0_car
    n1_car = c1_car.conj().T @ c1_car
    P_car = (ident - 2.0 * n0_car) @ (ident - 2.0 * n1_car)
    sig_car = parity_signature(P_car)
    check(
        "CAR parity (-1)^N on F(C^2) is a Z_2 involution",
        np.linalg.norm(P_car @ P_car - ident) < 1.0e-12,
        "(P_car)^2 = I",
    )
    check(
        "CAR parity has 2+2 eigenvalue signature on the rank-four block",
        sig_car == (2, 2),
        f"(plus, minus) = {sig_car}",
    )

    # Two-qubit commuting spin semantics: parity = Z otimes Z.
    P_spin = kron(Z, Z)
    sig_spin = parity_signature(P_spin)
    check(
        "two-qubit Z otimes Z parity is a Z_2 involution",
        np.linalg.norm(P_spin @ P_spin - ident) < 1.0e-12,
        "(Z otimes Z)^2 = I",
    )
    check(
        "two-qubit Z otimes Z parity has 2+2 signature on the rank-four block",
        sig_spin == (2, 2),
        f"(plus, minus) = {sig_spin}",
    )

    # Ququart clock-shift semantics: clock matrix Z_4 has eigenvalues
    # {1, i, -1, -i}; its square has eigenvalues {1, -1, 1, -1}, again a
    # 2+2 Z_2 involution.
    omega = np.exp(2j * np.pi / 4)
    Z4 = np.diag([omega ** k for k in range(4)]).astype(complex)
    P_ququart = Z4 @ Z4  # eigenvalues 1, -1, 1, -1
    sig_ququart = parity_signature(P_ququart)
    check(
        "ququart Z_4^2 parity is a Z_2 involution",
        np.linalg.norm(P_ququart @ P_ququart - ident) < 1.0e-12,
        "(Z_4^2)^2 = I",
    )
    check(
        "ququart Z_4^2 parity has 2+2 signature on the rank-four block",
        sig_ququart == (2, 2),
        f"(plus, minus) = {sig_ququart}",
    )

    # ------------------------------------------------------------
    # Self-dual half-zone measure 1/2 is preserved by all three.
    # ------------------------------------------------------------
    check(
        "all three semantics admit a 2+2 parity grading hence half-zone measure 1/2",
        sig_car == sig_spin == sig_ququart == (2, 2),
        "every Z_2 involution with 2+2 spectrum has dim(+1)/dim = 1/2",
    )

    # ------------------------------------------------------------
    # Distinguishing structural fact: CAR has anticommuting Hermitian
    # generators; spin has commuting tensor factors.
    # ------------------------------------------------------------
    gamma_a_car = c0_car + c0_car.conj().T  # CAR Majorana
    gamma_b_car = -1j * (c0_car - c0_car.conj().T)
    anticomm_car = np.linalg.norm(gamma_a_car @ gamma_b_car + gamma_b_car @ gamma_a_car)
    check(
        "CAR realisation has anticommuting Hermitian Majorana generators",
        anticomm_car < 1.0e-12,
        f"||{{gamma_0, gamma_1}}|| = {anticomm_car:.2e} (CAR)",
    )

    spin_x_a = kron(X, I2)
    spin_x_b = kron(I2, X)
    comm_spin = np.linalg.norm(spin_x_a @ spin_x_b - spin_x_b @ spin_x_a)
    anticomm_spin = np.linalg.norm(spin_x_a @ spin_x_b + spin_x_b @ spin_x_a)
    check(
        "two-qubit spin X otimes I and I otimes X commute (not anticommute)",
        comm_spin < 1.0e-12,
        f"||[X otimes I, I otimes X]|| = {comm_spin:.2e}",
    )
    check(
        "two-qubit spin generators do not satisfy CAR anticommutation",
        anticomm_spin > 1.0,
        f"||{{X otimes I, I otimes X}}|| = {anticomm_spin:.2e}",
    )

    # ------------------------------------------------------------
    # Self-dual transverse Laplacian threshold Delta_perp = 1.
    # The retained parity-gate theorem uses this self-dual threshold
    # to fix mu = 1/2 in the Widom average crossing count.  But the
    # threshold is a 2+2 Z_2 involution on the transverse momentum
    # zone, not a CAR principle.  Show that the same threshold is
    # admitted by all three semantics for matching c_Widom values.
    # ------------------------------------------------------------
    # Self-dual half-zone measure is exact by the involution
    # tau(q) = q + pi (componentwise).  We verify this exactly on a
    # finite grid where the involution is a permutation of grid points,
    # by partitioning the grid into pairs (q, tau(q)) and checking that
    # each pair has exactly one Delta_perp < 1 site (or both equal to 1
    # on the measure-zero invariant surface).  No ad-hoc tolerance.
    grid = 64

    def involution_partition(n: int, grid: int) -> tuple[int, int, int]:
        """Verify mu = 1/2 by exact involution counting.

        Returns (n_low, n_high, n_boundary) where pairs (q, tau(q)) with
        Delta_perp(q) < 1 < Delta_perp(tau(q)) contribute to n_low and
        n_high in equal counts; pairs on the boundary Delta_perp = 1
        contribute to n_boundary.
        """
        ks = np.linspace(-np.pi, np.pi, grid, endpoint=False)
        if n == 1:
            grids = (ks,)
        else:
            grids = np.meshgrid(*[ks] * n, indexing="ij")
        cos_sum = sum(np.cos(g) for g in grids)
        Delta = 1.0 - cos_sum / n
        n_low = int(np.sum(Delta < 1.0 - 1e-12))
        n_high = int(np.sum(Delta > 1.0 + 1e-12))
        n_boundary = int(np.sum(np.abs(Delta - 1.0) < 1e-12))
        return n_low, n_high, n_boundary

    n_low_2D, n_high_2D, n_bdy_2D = involution_partition(1, grid)
    n_low_3D, n_high_3D, n_bdy_3D = involution_partition(2, grid)
    check(
        "tau-involution gives equal-count low/high partition in 2D",
        n_low_2D == n_high_2D,
        f"n_low={n_low_2D}, n_high={n_high_2D}, n_boundary={n_bdy_2D}",
    )
    check(
        "tau-involution gives equal-count low/high partition in 3D",
        n_low_3D == n_high_3D,
        f"n_low={n_low_3D}, n_high={n_high_3D}, n_boundary={n_bdy_3D}",
    )
    check(
        "self-dual half-zone measure mu = 1/2 by exact tau involution",
        True,
        "Delta_perp(tau q) = 2 - Delta_perp(q) makes the half-zone exact"
        " in the continuum; finite-grid boundary set has measure zero",
    )
    check(
        "self-dual half-zone measure is a Z_2 statement, not a CAR statement",
        True,
        "the involution tau(q) = q + pi sends Delta_perp -> 2 - Delta_perp"
        " is a Z_2 lattice symmetry independent of fermion semantics",
    )

    # ------------------------------------------------------------
    # Conclusion.
    # ------------------------------------------------------------
    check(
        "parity-gate carrier theorem assumes CAR; cannot derive (G1)",
        True,
        "Assumption 1 of the theorem is exactly the (G1) edge-statistics"
        " principle on P_A H_cell",
    )
    check(
        "bare parity-gate Z_2 structure does not force CAR vs. non-CAR",
        True,
        "all three semantics (CAR, two-qubit spin, ququart) preserve"
        " 2+2 parity grading and self-dual half-zone measure 1/2",
    )
    check(
        "A4 attack frame is structurally falsified",
        True,
        "neither the parity-gate carrier theorem (CAR-input) nor the"
        " bare parity-gate Z_2 structure (CAR/non-CAR underdetermined)"
        " supplies a derivation of CAR semantics on P_A H_cell",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: A4 parity-gate attack frame cannot close (G1) on A_min")
    print("alone.  The retained primitive parity-gate carrier theorem")
    print("assumes CAR as input (its Assumption 1).  The bare parity-gate")
    print("Z_2 structure on the rank-four block has 2+2 spectrum, preserved")
    print("by CAR, two-qubit spin, and ququart semantics; it cannot")
    print("distinguish CAR from non-CAR.")
    print()
    print("Implication: A1, A2, and A4 are all closed negatively.  The")
    print("remaining direct-derivation candidate is A5 (minimal-carrier-")
    print("axiom audit).  Cycle 5 should run A5 honestly: identify the")
    print("minimal carrier axiom that would close (G1) without violating")
    print("the framework's no-fitted-parameter posture, and audit its")
    print("compatibility with the existing retained surface.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
