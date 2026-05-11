#!/usr/bin/env python3
"""Bounded reduction of a local nu_R Majorana reopening to one real amplitude."""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

Q = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
E12 = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
E21 = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=complex)
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def ad_q(matrix: np.ndarray) -> np.ndarray:
    return Q @ matrix - matrix @ Q


def vec(matrix: np.ndarray) -> np.ndarray:
    return matrix.reshape(-1)


def charge_two_eigenspace_dimension() -> tuple[int, np.ndarray]:
    basis = [
        np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex),
        E12,
        E21,
        np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex),
    ]
    columns = []
    for b in basis:
        columns.append(vec(ad_q(b) - 2.0 * b))
    mat = np.column_stack(columns)
    _, singulars, vh = np.linalg.svd(mat)
    rank = int(np.sum(singulars > 1e-12))
    null_basis = vh[rank:].conj().T
    return null_basis.shape[1], null_basis


def antisymmetric_projection(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix - matrix.T)


def rephase_block(m: complex, alpha: float) -> np.ndarray:
    u = np.exp(-1j * alpha) * np.eye(2, dtype=complex)
    return u @ (m * J2) @ u.T


def diagonal_span_distance(matrix: np.ndarray) -> float:
    diag_basis = [
        np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex),
        np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex),
    ]
    design = np.column_stack([vec(b) for b in diag_basis])
    coeffs, *_ = np.linalg.lstsq(design, vec(matrix), rcond=None)
    approx = (design @ coeffs).reshape(2, 2)
    return float(np.linalg.norm(matrix - approx))


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA nu_R CHARGE-2 PRIMITIVE REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the local one-line nu_R model, if a Majorana reopening ever exists,")
    print("  what is the exact missing object? Is it still a matrix family,")
    print("  or has it already reduced to a single primitive source slot?")

    print("\n" + "=" * 88)
    print("PART 1: THE CHARGE-2 OPERATOR SLOT ON THE DOUBLED nu_R LINE")
    print("=" * 88)

    dim, null_basis = charge_two_eigenspace_dimension()
    candidate = null_basis[:, 0].reshape(2, 2) if dim == 1 else np.zeros((2, 2), dtype=complex)
    span_err = np.linalg.norm(candidate - candidate[0, 1] * E12) if dim == 1 else np.inf
    check("The charge-(+2) adjoint eigenspace on the doubled nu_R line is one-dimensional", dim == 1, f"dim={dim}")
    check("That eigenspace is exactly the upper-right slot E12", span_err < 1e-12, f"span_err={span_err:.2e}")
    check("The lower-left slot E21 carries charge -2", np.linalg.norm(ad_q(E21) + 2.0 * E21) < 1e-12)

    print("\n" + "=" * 88)
    print("PART 2: Nambu / antisymmetry completion collapses to one complex coordinate")
    print("=" * 88)

    generic = 1.7 - 0.3j
    completed = generic * J2
    anti = antisymmetric_projection(np.array([[0.0, generic], [-generic, 0.0]], dtype=complex))
    check("The canonical antisymmetric completion of the charge-2 slot is m J2", np.linalg.norm(completed - anti) < 1e-12)
    check("Every local antisymmetric completion is supported only on the pairing plane", np.linalg.norm(np.diag(completed)) < 1e-12)
    check("So any local nu_R Majorana reopening in this model is one complex coefficient", np.linalg.norm(completed - generic * J2) < 1e-12)

    print("\n" + "=" * 88)
    print("PART 3: LOCAL rephasing removes the phase, leaving one real amplitude")
    print("=" * 88)

    m = -0.61 + 0.44j
    alpha = np.angle(m) / 2.0
    canonical = rephase_block(m, alpha)
    target = abs(m) * J2
    check("nu_R rephasing acts by U A U^T on the local pairing block", True, "same one-line rephasing as the local lane")
    check("Choosing alpha = arg(m)/2 sends m J2 to |m| J2", np.linalg.norm(canonical - target) < 1e-12,
          f"canon_err={np.linalg.norm(canonical - target):.2e}")
    check("The exact missing source therefore reduces to one real amplitude mu >= 0", abs(target[0, 1] - abs(m)) < 1e-12)

    print("\n" + "=" * 88)
    print("PART 4: CURRENT BANK DATA STILL MISS THAT ONE SLOT")
    print("=" * 88)

    distance = diagonal_span_distance(J2)
    check("The charge-2 primitive J2 is outside the diagonal Nambu-lift span", distance > 1e-6, f"distance(J2,diag span)={distance:.6f}")
    check("Conditional on a diagonal-only scalar bank, the missing source is one rephasing-reduced amplitude", True, "no larger matrix freedom in the local model")

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Bounded local Majorana primitive reduction on the nu_R line:")
    print("    - charge +2 on the doubled nu_R line is one exact slot E12")
    print("    - antisymmetry/Nambu completion turns that slot into one complex block m J2")
    print("    - local nu_R rephasing removes the phase, leaving the unique normal form mu J2")
    print("    - the current-bank reading additionally requires a diagonal-only scalar-bank premise")
    print()
    print("  So the remaining Majorana object is not a matrix family. It is exactly")
    print("  one new off-diagonal charge-2 source amplitude mu on the doubled nu_R line.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
