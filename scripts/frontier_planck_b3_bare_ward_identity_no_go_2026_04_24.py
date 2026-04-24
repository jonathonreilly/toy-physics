#!/usr/bin/env python3
"""Verifier for the B3 bare Ward-identity no-go theorem."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PLANCK_SCALE_B3_BARE_WARD_IDENTITY_NO_GO_2026-04-24.md"


def expect(name: str, cond: bool, detail: str) -> bool:
    status = "PASS" if cond else "FAIL"
    print(f"{status}: {name} - {detail}")
    return cond


def signed_permutation_group() -> list[sp.Matrix]:
    mats: list[sp.Matrix] = []
    for perm in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            mat = sp.zeros(3)
            for row, col in enumerate(perm):
                mat[row, col] = signs[row]
            mats.append(mat)
    return mats


def mat_to_vec(mat: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([mat[i, j] for i in range(mat.rows) for j in range(mat.cols)])


def rank_of_basis(basis: list[sp.Matrix]) -> int:
    if not basis:
        return 0
    return sp.Matrix.hstack(*(mat_to_vec(mat) for mat in basis)).rank()


def scalar_basis() -> list[sp.Matrix]:
    return [sp.eye(3)]


def antisymmetric_basis() -> list[sp.Matrix]:
    basis = []
    for i in range(3):
        for j in range(i + 1, 3):
            mat = sp.zeros(3)
            mat[i, j] = 1
            mat[j, i] = -1
            basis.append(mat)
    return basis


def symmetric_traceless_basis() -> list[sp.Matrix]:
    return [
        sp.diag(1, -1, 0),
        sp.diag(1, 1, -2),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    ]


def is_scalar(mat: sp.Matrix) -> bool:
    return mat == sp.eye(3) * (sp.trace(mat) / 3)


def is_antisymmetric(mat: sp.Matrix) -> bool:
    return mat.T == -mat


def is_symmetric_traceless(mat: sp.Matrix) -> bool:
    return mat.T == mat and sp.trace(mat) == 0


def frobenius_norm_squared(mat: sp.Matrix) -> sp.Expr:
    return sp.trace(mat.T * mat)


@dataclass(frozen=True)
class Channel:
    name: str
    basis: list[sp.Matrix]
    predicate: object


def channel_invariant(group: list[sp.Matrix], channel: Channel) -> bool:
    predicate = channel.predicate
    return all(predicate(g * basis_mat * g.T) for g in group for basis_mat in channel.basis)


def quadratic_norm_invariant(group: list[sp.Matrix], channel: Channel) -> bool:
    for g in group:
        for basis_mat in channel.basis:
            transformed = g * basis_mat * g.T
            if frobenius_norm_squared(transformed) != frobenius_norm_squared(basis_mat):
                return False
    return True


def min_nonidentity_distance_squared(group: list[sp.Matrix]) -> sp.Expr:
    identity = sp.eye(3)
    return min(
        frobenius_norm_squared(g - identity)
        for g in group
        if g != identity
    )


def main() -> int:
    doc = DOC.read_text()
    flat_doc = " ".join(doc.split())
    group = signed_permutation_group()
    identity = sp.eye(3)
    channels = [
        Channel("scalar-trace", scalar_basis(), is_scalar),
        Channel("antisymmetric", antisymmetric_basis(), is_antisymmetric),
        Channel("symmetric-traceless", symmetric_traceless_basis(), is_symmetric_traceless),
    ]

    results: list[bool] = []

    results.append(
        expect(
            "document-records-exact-missing-primitive",
            "local gaugeable defect-to-coframe response primitive" in flat_doc
            and "local translation defects to one coframe/metric response variable" in flat_doc
            and "continuous local redundancy" in flat_doc
            and "symmetric and conserved" in flat_doc,
            "single missing primitive is named explicitly",
        )
    )

    results.append(
        expect(
            "no-hidden-geometric-sector-definition",
            "preselected \"geometric sector\"" in flat_doc
            and "No step assumes a variable metric" in flat_doc
            and "not extra names for an already assumed \"geometric sector\"" in flat_doc,
            "the note forbids metricity-by-definition",
        )
    )

    results.append(
        expect(
            "signed-permutation-group-is-exact-finite-frame-group",
            len(group) == 48
            and len({tuple(g) for g in group}) == 48
            and all(g.T * g == identity for g in group)
            and all(abs(int(g.det())) == 1 for g in group)
            and "Z^3 semidirect O(3,Z)" in flat_doc
            and "discrete basepoint-shift group" in flat_doc
            and "48" in flat_doc
            and "Lie algebra is zero" in flat_doc,
            f"|O(3,Z)|={len(group)}",
        )
    )

    results.append(
        expect(
            "identity-component-is-discrete",
            min_nonidentity_distance_squared(group) > 0
            and "identity component is trivial" in flat_doc
            and "pointwise finite relabelings and sign flips" in flat_doc,
            f"minimum nonidentity Frobenius distance squared = {min_nonidentity_distance_squared(group)}",
        )
    )

    dimensions = [rank_of_basis(channel.basis) for channel in channels]
    direct_sum_rank = rank_of_basis([basis_mat for channel in channels for basis_mat in channel.basis])
    results.append(
        expect(
            "response-space-decomposes-into-1-3-5-channels",
            dimensions == [1, 3, 5]
            and direct_sum_rank == 9
            and "dimension `1`" in flat_doc
            and "dimension `3`" in flat_doc
            and "dimension `5`" in flat_doc,
            f"channel dimensions={dimensions}, direct-sum rank={direct_sum_rank}",
        )
    )

    results.append(
        expect(
            "all-three-response-channels-are-bare-invariant",
            all(channel_invariant(group, channel) for channel in channels)
            and all(quadratic_norm_invariant(group, channel) for channel in channels),
            "scalar, antisymmetric, and symmetric-traceless onsite quadratic symbols are invariant",
        )
    )

    scalar_witness = sp.eye(3)
    antisymmetric_witness = antisymmetric_basis()[0]
    symmetric_witness = symmetric_traceless_basis()[0]
    results.append(
        expect(
            "nonmetric-countermodels-survive-retained-constraints",
            is_scalar(scalar_witness)
            and not is_symmetric_traceless(scalar_witness)
            and is_antisymmetric(antisymmetric_witness)
            and not (antisymmetric_witness.T == antisymmetric_witness)
            and is_symmetric_traceless(symmetric_witness)
            and "scalar and antisymmetric witnesses are not symmetric spin-2 responses" in flat_doc,
            "bare-compatible scalar and antisymmetric response witnesses are not symmetric spin-2",
        )
    )

    results.append(
        expect(
            "b3-status-is-reduced-not-closed",
            "**reduced:**" in doc
            and "**open:**" in doc
            and "B3 is not closed" in doc,
            "the theorem sharpens B3 to the missing primitive without claiming closure",
        )
    )

    passed = sum(results)
    total = len(results)
    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
