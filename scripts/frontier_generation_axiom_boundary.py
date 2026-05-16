#!/usr/bin/env python3
"""
Generation Axiom Boundary: Local M_3(C) Observable-Algebra Reconstruction
==========================================================================

STATUS: bounded_theorem on the retained generation surface.

CLAIM (in-scope, the only thing this runner verifies):
  Local M_3(C) observable-algebra reconstruction on H_hw=1 from the
  supplied translation-character projectors and C3 cycle generator.
  Specifically:
    - the three exact rank-one observable projectors on H_hw=1 correspond
      to the pairwise-distinct translation characters,
    - they generate the full 9-dimensional M_3(C) observable algebra,
    - the commutant of these generators on H_hw=1 is scalar (dimension 1),
      so no proper exact quotient kernel can be invariant under the
      retained observable algebra.

OUT OF SCOPE (admitted-context; NOT asserted, NOT checked by this runner):
  - the physical-species bridge from observable-separation to physically
    distinct species sectors,
  - the substrate-fundamentality question (lattice fundamental vs
    regulator-family surrogate),
  - the historical reduced-stack witness about the older five-item
    implementation memo (the runner contains no hard-coded historical
    PASS check; every PASS line below is a finite-dimensional algebraic
    computation on the supplied 3x3 generators).
  These belong to separate authority notes and are not asserted here.

PStack experiment: frontier-generation-axiom-boundary
Self-contained: numpy only.
"""

from __future__ import annotations
import sys
import numpy as np

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail="", kind="EXACT"):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Local M_3(C) observable-algebra reconstruction on H_hw=1
# =============================================================================

def retained_triplet_operator_bridge():
    """Construct the exact observable algebra on H_hw=1.

    The three rank-one translation-character projectors plus the C3 cycle
    generator operate on the 3-dimensional H_hw=1 sector. Their generated
    algebra is the full M_3(C); their commutant is scalar.
    """
    tx = np.diag([-1.0, +1.0, +1.0]).astype(complex)
    ty = np.diag([+1.0, -1.0, +1.0]).astype(complex)
    tz = np.diag([+1.0, +1.0, -1.0]).astype(complex)
    c3 = np.array(
        [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=complex,
    )
    ident = np.eye(3, dtype=complex)
    chars = [(-1, +1, +1), (+1, -1, +1), (+1, +1, -1)]
    projectors = []
    for signs in chars:
        p = ident.copy()
        for sign, op in zip(signs, (tx, ty, tz)):
            p = p @ (ident + sign * op) / 2.0
        projectors.append(p)

    words = [ident, tx, ty, tz, c3, c3 @ c3]
    basis = []
    changed = True
    while changed:
        changed = False
        for left in list(words):
            for right in list(words):
                candidate = left @ right
                vec = candidate.reshape(-1)
                if not basis:
                    basis.append(candidate)
                    changed = True
                    continue
                mat = np.stack([b.reshape(-1) for b in basis], axis=1)
                coeffs, *_ = np.linalg.lstsq(mat, vec, rcond=None)
                if np.linalg.norm(mat @ coeffs - vec) > 1e-10:
                    basis.append(candidate)
                    words.append(candidate)
                    changed = True
    algebra_dim = len(basis)

    comm_constraints = [
        np.kron(op.T, ident) - np.kron(ident, op)
        for op in (tx, ty, tz, c3)
    ]
    constraint = np.vstack(comm_constraints)
    _, svals, vh = np.linalg.svd(constraint, full_matrices=True)
    tol = 1e-10 * max(1.0, svals[0])
    comm_dim = int(np.sum(svals < tol) + max(0, vh.shape[0] - len(svals)))
    return chars, projectors, algebra_dim, comm_dim


def part1_local_m3c_reconstruction():
    """Verify the local M_3(C) observable algebra reconstructs on H_hw=1."""
    print("=" * 72)
    print("LOCAL M_3(C) OBSERVABLE-ALGEBRA RECONSTRUCTION ON H_hw=1")
    print("=" * 72)
    print()
    print("  Generators: three translation-character projectors + C3 cycle.")
    print("  Target: full M_3(C) algebra (dim 9) with scalar commutant (dim 1).")
    print()

    chars, triplet_projectors, triplet_alg_dim, triplet_comm_dim = retained_triplet_operator_bridge()

    check("hw1_translation_characters_pairwise_distinct",
          len(set(chars)) == 3,
          f"characters={chars}", kind="EXACT")
    check("hw1_translation_projectors_are_rank_one",
          all(np.linalg.matrix_rank(p, tol=1e-10) == 1 for p in triplet_projectors),
          "three exact rank-one observable projectors on H_hw=1", kind="EXACT")
    check("hw1_retained_observable_algebra_is_full_M3",
          triplet_alg_dim == 9,
          f"generated algebra dimension={triplet_alg_dim}", kind="EXACT")
    check("hw1_retained_observable_commutant_is_scalar",
          triplet_comm_dim == 1,
          f"commutant dimension={triplet_comm_dim}; no proper exact quotient kernel can be invariant",
          kind="EXACT")

    return triplet_alg_dim, triplet_comm_dim


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 72)
    print("GENERATION AXIOM BOUNDARY -- LOCAL M_3(C) RECONSTRUCTION")
    print("Local observable-algebra reconstruction on H_hw=1 (in-scope claim)")
    print("=" * 72)
    print()

    alg_dim, comm_dim = part1_local_m3c_reconstruction()

    # -------------------------------------------------------------------
    # FINAL SUMMARY
    # -------------------------------------------------------------------
    print()
    print("=" * 72)
    print("FINAL SUMMARY")
    print("=" * 72)
    print(f"\n  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print()
    print("  EXACT computational checks (in-scope):")
    print("    - three pairwise-distinct hw=1 translation characters")
    print("    - three rank-one observable projectors on H_hw=1")
    print("    - generated algebra is full M_3(C) (dim 9)")
    print("    - commutant on H_hw=1 is scalar (dim 1)")
    print()
    print("  THEOREM STATUS: bounded_theorem")
    print("    Local M_3(C) observable-algebra reconstruction on H_hw=1.")
    print("    Physical-species bridge, substrate-fundamentality, and the")
    print("    historical reduced-stack/five-item-memo witness are out of")
    print("    scope here and live in separate authority notes.")
    print()
    if FAIL_COUNT == 0:
        print("  ALL CHECKS PASSED.")
    else:
        print(f"  {FAIL_COUNT} CHECKS FAILED -- investigate.")
    print()

    return FAIL_COUNT


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
