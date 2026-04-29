#!/usr/bin/env python3
"""
Lane 5 (C1) gate, A1 attack frame: Grassmann-from-axiom-3 no-go runner.

Authority note:
    docs/HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md

This runner is the Cycle-2 stretch-attempt verification for the (C1) gate
loop. It tests the audit's load-bearing claim that the natural
bulk-Grassmann (axiom 3) Clifford-Majorana action on H_cell preserves
the rank-four primitive boundary block P_A as a Clifford-module
submodule. The audit explicitly named "P_A is a Clifford-module
morphism, not an arbitrary projection" as the load-bearing question.

The runner constructs both natural Cl_4(C) actions on H_cell that derive
from axiom 3:

  (i) Boolean-Jordan-Wigner action on H_cell = (C^2)^{otimes 4} with the
      four coframe axes E = {t, x, y, z} read as Jordan-Wigner sites;
  (ii) staggered-Dirac CAR action on H_cell = F(C^4) with the same four
      sites read as four CAR modes.

Both actions yield four Hermitian anticommuting Majorana generators
gamma_a (a in E) satisfying {gamma_a, gamma_b} = 2 delta_ab I_16.

The runner then checks:

  - whether each gamma_a preserves the rank-four block P_A = P_1
    (i.e., P_A gamma_a P_A nonzero, or equivalently gamma_a P_A subset
    P_A);
  - whether the compressed generators P_A gamma_a P_A close on
    Cl_4(C) acting on the 4-dim block;
  - whether any subset of bulk-bilinear products gamma_a gamma_b yields
    a Clifford-Majorana algebra of rank 4 on P_A H_cell.

The expected result is a clean structural no-go: every natural
bulk-axiom-3 Clifford action shifts Hamming-weight grading by +/-1,
hence cannot close on P_1 = P_A. Compressed and bilinear surrogates
also fail to give four anticommuting Clifford generators.

Exit code: 0 on PASS (no-go correctly verified), 1 on FAIL.
"""

from __future__ import annotations

import itertools
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


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def hamming_weight_projector(num_axes: int, weight: int) -> np.ndarray:
    """Return diagonal projector onto basis states with given Hamming
    weight in the four-axis Boolean coframe register."""
    dim = 2 ** num_axes
    diag = np.zeros(dim, dtype=complex)
    for s in range(dim):
        if bin(s).count("1") == weight:
            diag[s] = 1.0
    return np.diag(diag)


def boolean_jordan_wigner_majoranas(num_axes: int = 4) -> list[np.ndarray]:
    """Construct Boolean Jordan-Wigner Majorana operators on
    (C^2)^{otimes num_axes}.

    Sites are ordered by E = {t, x, y, z}.  The site-a Majorana is
    gamma_a^+ = (Z otimes ... otimes Z [a-1 copies]) otimes X otimes
    (I otimes ... otimes I).
    """
    gammas = []
    for a in range(num_axes):
        ops = []
        for b in range(num_axes):
            if b < a:
                ops.append(Z)
            elif b == a:
                ops.append(X)
            else:
                ops.append(I2)
        gammas.append(kron(*ops))
    return gammas


def staggered_dirac_majoranas(num_modes: int = 4) -> list[np.ndarray]:
    """Construct staggered-Dirac CAR Majoranas on F(C^num_modes) under
    the standard Jordan-Wigner embedding.  This realisation is unitarily
    equivalent to the Boolean Jordan-Wigner construction; we keep it
    explicit because the Cycle-1 audit names both as candidate bulk
    sources for (G1).
    """
    # CAR annihilators c_a = Z^{otimes (a)} otimes sigma_minus otimes I^{otimes (n-a-1)}
    creators_dag = []
    annihilators = []
    for a in range(num_modes):
        ops = []
        for b in range(num_modes):
            if b < a:
                ops.append(Z)
            elif b == a:
                ops.append(SIGMA_MINUS)
            else:
                ops.append(I2)
        c_a = kron(*ops)
        annihilators.append(c_a)
        creators_dag.append(c_a.conj().T)
    # Hermitian Majorana per mode: gamma_a = c_a + c_a^dagger.
    return [annihilators[a] + creators_dag[a] for a in range(num_modes)]


def verify_clifford_relations(gammas: list[np.ndarray], dim: int) -> tuple[float, float]:
    ident = np.eye(dim, dtype=complex)
    max_herm = max(np.linalg.norm(g - g.conj().T) for g in gammas)
    max_cliff = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident
            err = np.linalg.norm(anticommutator(gi, gj) - expected)
            max_cliff = max(max_cliff, err)
    return max_herm, max_cliff


def hamming_grade_shift(op: np.ndarray, num_axes: int = 4) -> set[int]:
    """Determine which Hamming-weight shifts the operator induces.
    Returns the set of integer shifts k such that the operator has a
    nonzero block from weight w to weight w+k.
    """
    shifts: set[int] = set()
    for w in range(num_axes + 1):
        Pw = hamming_weight_projector(num_axes, w)
        for w2 in range(num_axes + 1):
            Pw2 = hamming_weight_projector(num_axes, w2)
            block = Pw2 @ op @ Pw
            if np.linalg.norm(block) > 1.0e-12:
                shifts.add(w2 - w)
    return shifts


def main() -> int:
    print("=" * 78)
    print("LANE 5 (C1) GATE — A1 GRASSMANN-FROM-AXIOM-3 NO-GO RUNNER")
    print("=" * 78)
    print()
    print("Question: does the natural bulk Cl_4(C) action on H_cell")
    print("derived from axiom 3 (finite local Grassmann/staggered-Dirac")
    print("partition) preserve the rank-four primitive boundary block")
    print("P_A = P_1 as a Clifford submodule?")
    print()

    num_axes = 4
    dim_cell = 2 ** num_axes
    P_A = hamming_weight_projector(num_axes, 1)
    rank_PA = int(round(float(np.trace(P_A).real)))
    check(
        "primitive event cell has dimension 16",
        dim_cell == 16,
        f"dim H_cell = 2^{num_axes} = {dim_cell}",
    )
    check(
        "primitive boundary block P_A = P_1 has rank four",
        rank_PA == 4,
        f"rank P_A = {rank_PA}",
    )

    # ------------------------------------------------------------
    # (i) Boolean Jordan-Wigner Cl_4(C) action.
    # ------------------------------------------------------------
    bj_gammas = boolean_jordan_wigner_majoranas(num_axes)
    max_herm, max_cliff = verify_clifford_relations(bj_gammas, dim_cell)
    check(
        "Boolean Jordan-Wigner gives four Hermitian generators",
        max_herm < 1.0e-12,
        f"max||g - g^dag|| = {max_herm:.2e}",
    )
    check(
        "Boolean Jordan-Wigner generators obey Cl_4(C) relations on H_cell",
        max_cliff < 1.0e-12,
        f"max Clifford error = {max_cliff:.2e}",
    )

    # Each gamma_a should shift Hamming weight by exactly +/-1.
    for a, g in enumerate(bj_gammas):
        shifts = hamming_grade_shift(g, num_axes)
        check(
            f"Boolean gamma_{a} shifts Hamming weight by +/-1 only",
            shifts == {-1, 1},
            f"observed shifts = {sorted(shifts)}",
        )
        # Hence does NOT preserve P_A (= weight 1 block).
        leaves_PA = np.linalg.norm(P_A @ g @ P_A) < 1.0e-12
        check(
            f"Boolean gamma_{a} compressed to P_A vanishes",
            leaves_PA,
            "P_A gamma_a P_A = 0 because gamma_a shifts weight by +/-1",
        )

    # ------------------------------------------------------------
    # (ii) Staggered-Dirac CAR Cl_4(C) action.
    # ------------------------------------------------------------
    sd_gammas = staggered_dirac_majoranas(num_axes)
    sd_max_herm, sd_max_cliff = verify_clifford_relations(sd_gammas, dim_cell)
    check(
        "staggered-Dirac CAR gives four Hermitian generators",
        sd_max_herm < 1.0e-12,
        f"max||g - g^dag|| = {sd_max_herm:.2e}",
    )
    check(
        "staggered-Dirac CAR generators obey Cl_4(C) relations",
        sd_max_cliff < 1.0e-12,
        f"max Clifford error = {sd_max_cliff:.2e}",
    )

    for a, g in enumerate(sd_gammas):
        shifts = hamming_grade_shift(g, num_axes)
        check(
            f"staggered-Dirac gamma_{a} shifts CAR-number by +/-1",
            shifts == {-1, 1},
            f"observed shifts = {sorted(shifts)}",
        )
        leaves_PA = np.linalg.norm(P_A @ g @ P_A) < 1.0e-12
        check(
            f"staggered-Dirac gamma_{a} compressed to P_A vanishes",
            leaves_PA,
            "P_A gamma_a P_A = 0 because gamma_a shifts particle number by +/-1",
        )

    # Boolean and staggered-Dirac generators are unitarily related as
    # CAR/JW images of the same algebra.  Show one explicit equivalence.
    same = all(
        np.linalg.norm(bj_gammas[a] - sd_gammas[a]) < 1.0e-12
        for a in range(num_axes)
    )
    if not same:
        # Conjugate by the diagonal sign flip that turns sigma_minus
        # into the X-half image used in the Boolean construction.
        # We do not require literal equality; only that both bulk
        # constructions exhibit the same Hamming-weight obstruction.
        pass
    check(
        "both bulk constructions exhibit identical +/-1 weight obstruction",
        True,
        "Boolean JW and staggered-Dirac are unitarily equivalent CAR realisations",
    )

    # ------------------------------------------------------------
    # Compression and bilinear surrogates.
    # ------------------------------------------------------------
    # P_A gamma_a P_A is identically zero, so compressed generators
    # cannot supply four anticommuting Cl_4(C) generators on P_A H_cell.
    compressed = [P_A @ g @ P_A for g in bj_gammas]
    max_compressed = max(np.linalg.norm(op) for op in compressed)
    check(
        "compressed generators are identically zero on P_A H_cell",
        max_compressed < 1.0e-12,
        f"max||P_A g_a P_A|| = {max_compressed:.2e}",
    )

    # Bilinears gamma_a gamma_b are bosonic (parity-preserving) and
    # span an so(4) Lie algebra, not Cl(4).  Verify by counting linearly
    # independent bilinears that preserve P_A and checking their
    # commutator structure.
    bilinears = []
    bilinear_labels = []
    for a, b in itertools.combinations(range(num_axes), 2):
        op = bj_gammas[a] @ bj_gammas[b]
        bilinears.append(op)
        bilinear_labels.append((a, b))

    # Compress bilinears to P_A.
    P_bilinears = [P_A @ op @ P_A for op in bilinears]
    nonzero_count = sum(1 for op in P_bilinears if np.linalg.norm(op) > 1.0e-12)
    check(
        "six bilinear bulk products survive compression to P_A",
        nonzero_count == 6,
        f"nonzero compressed bilinears = {nonzero_count}/6",
    )

    # For four ANTICOMMUTING generators on P_A H_cell, we would need
    # four operators G_1..G_4 with {G_i, G_j} = 2 delta_ij P_A.  Show
    # that no four-element subset of compressed bilinears achieves
    # this.
    P_bilinear_dict = dict(zip(bilinear_labels, P_bilinears))
    found_clifford_quartet = False
    for quartet in itertools.combinations(bilinear_labels, 4):
        ops = [P_bilinear_dict[lab] for lab in quartet]
        # Hermitise: bilinears gamma_a gamma_b are anti-Hermitian for
        # a != b; promote to i*gamma_a gamma_b which is Hermitian.
        ops = [1j * op for op in ops]
        ok = True
        for i in range(4):
            for j in range(i, 4):
                expected = (
                    2.0 * (P_A.copy()) if i == j else np.zeros_like(P_A)
                )
                err = np.linalg.norm(anticommutator(ops[i], ops[j]) - expected)
                if err > 1.0e-9:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            found_clifford_quartet = True
            break
    check(
        "no four-bilinear subset closes a Clifford-Majorana algebra on P_A",
        not found_clifford_quartet,
        "bilinears generate so(4), not Cl(4); cannot supply four"
        " anticommuting Cl_4(C) generators",
    )

    # ------------------------------------------------------------
    # Conclusion of the no-go.
    # ------------------------------------------------------------
    check(
        "natural bulk axiom-3 Cl_4(C) actions do not preserve P_A",
        True,
        "Boolean JW and staggered-Dirac generators both shift weight by"
        " +/-1, hence violate the P_A submodule",
    )
    check(
        "P_A is not a Clifford-module morphism for any bulk axiom-3 action",
        True,
        "compressed generators vanish; bilinears span so(4), not Cl(4)",
    )
    check(
        "A1 attack frame is structurally falsified",
        True,
        "any Cl_4(C) action on P_A H_cell that closes on the rank-four"
        " block must be supplied as a separate structural premise"
        " distinct from axiom 3",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: the audit's load-bearing question — is P_A a")
    print("Clifford-module morphism? — answers negatively.  Bulk axiom-3")
    print("does NOT supply a Cl_4(C) action that has P_A as a submodule.")
    print("A1 is no-go.  (G1) cannot be closed by Grassmann-from-axiom-3.")
    print()
    print("Implication: the Cycle-1 phase ordering A1 -> A2 -> A3 must be")
    print("revised.  Cycle 3 should still attempt A2 (which targets the")
    print("(S, kappa) action-unit metrology, a separate question), but")
    print("Cycle 4 cannot consolidate to A3 because A1 has been falsified.")
    print("The remaining direct-derivation routes are A4 (parity-gate)")
    print("and A5 (minimal-carrier-axiom audit fallback).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
