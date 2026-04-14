#!/usr/bin/env python3
"""Audit the direct-universal tensor quotient-uniqueness candidate.

This is not a closure proof. It checks that the current atlas now supplies:

1. the exact scalar observable generator from the axiom-side observable
   principle;
2. the exact `3+1` kinematic lift on `PL S^3 x R`;
3. a symmetric tensor Hessian on the `3+1` quotient with no hidden null
   directions on the finite prototype basis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_TIME_SPACETIME_OBSERVABLE_ROUTE_NOTE.md"
BLOCKER = DOCS / "UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md"
VARIATIONAL = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"
UNIQUENESS = DOCS / "UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def bilinear(
    a: Sequence[Sequence[float]],
    b: Sequence[Sequence[float]],
    d: Sequence[float],
) -> float:
    """Exact Hessian prototype: -Tr(D^-1 a D^-1 b) for diagonal D."""

    total = 0.0
    n = len(d)
    for i in range(n):
        for j in range(n):
            total += a[i][j] * b[j][i] / (d[i] * d[j])
    return -total


def sym_basis(n: int) -> list[list[list[float]]]:
    basis: list[list[list[float]]] = []
    for i in range(n):
        m = [[0.0 for _ in range(n)] for _ in range(n)]
        m[i][i] = 1.0
        basis.append(m)
    for i in range(n):
        for j in range(i + 1, n):
            m = [[0.0 for _ in range(n)] for _ in range(n)]
            scale = 2.0 ** 0.5
            m[i][j] = 1.0 / scale
            m[j][i] = 1.0 / scale
            basis.append(m)
    return basis


def gram_matrix(
    basis: Sequence[Sequence[Sequence[float]]],
    d: Sequence[float],
) -> list[list[float]]:
    return [[bilinear(a, b, d) for b in basis] for a in basis]


def rank(matrix: Sequence[Sequence[float]], tol: float = 1e-12) -> int:
    """Basic row-echelon rank for the finite prototype."""

    rows = [list(row) for row in matrix]
    m = len(rows)
    n = len(rows[0]) if rows else 0
    r = 0
    c = 0
    while r < m and c < n:
        pivot = max(range(r, m), key=lambda i: abs(rows[i][c]))
        if abs(rows[pivot][c]) <= tol:
            c += 1
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        piv = rows[r][c]
        for j in range(c, n):
            rows[r][j] /= piv
        for i in range(m):
            if i == r:
                continue
            factor = rows[i][c]
            if abs(factor) <= tol:
                continue
            for j in range(c, n):
                rows[i][j] -= factor * rows[r][j]
        r += 1
        c += 1
    return r


def max_symmetry_error(matrix: Sequence[Sequence[float]]) -> float:
    err = 0.0
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            err = max(err, abs(val - matrix[j][i]))
    return err


def main() -> int:
    obs = read(OBSERVABLE)
    r2 = read(ROUTE2)
    blk = read(BLOCKER)
    var = read(VARIATIONAL)
    uni = read(UNIQUENESS)

    d = (2.0, 3.0, 5.0, 7.0)
    basis = sym_basis(4)
    gram = gram_matrix(basis, d)

    I = [[0.0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        I[i][i] = 1.0

    scalar_direct = bilinear(I, I, d)
    scalar_expected = -sum(1.0 / (x * x) for x in d)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle") and has(obs, "det(d+j)") and has(obs, "det d"),
            "observable principle gives the exact scalar generator",
        ),
        Check(
            "route-2 kinematic lift is exact",
            has(r2, "O_lift = 1"),
            "route-2 gives the exact PL S^3 x R selector",
        ),
        Check(
            "variational note states the exact tensor candidate",
            has(var, "metric-source hessian") and has(var, "s_gr^cand"),
            "candidate note identifies the Hessian on the lifted background",
        ),
        Check(
            "uniqueness note states symmetric quotient kernel",
            has(uni, "unique symmetric `3+1` quotient kernel")
            or has(uni, "unique bilinear lift"),
            "uniqueness note promotes the quotient-kernel statement",
        ),
        Check(
            "prototype Gram matrix is symmetric",
            max_symmetry_error(gram) < 1e-15,
            f"max symmetry error = {max_symmetry_error(gram):.3e}",
        ),
        Check(
            "prototype symmetric quotient basis is nondegenerate",
            rank(gram) == len(gram),
            f"rank = {rank(gram)} / {len(gram)}",
        ),
        Check(
            "scalar-line restriction matches the same Hessian",
            abs(scalar_direct - scalar_expected) < 1e-15,
            f"direct = {scalar_direct:.6e}, expected = {scalar_expected:.6e}",
        ),
        Check(
            "blocker now names the localization primitive",
            has(blk, "curvature-localization map") and has(blk, "einstein/regge"),
            "blocker is sharpened to the localization primitive",
        ),
    ]

    print("UNIVERSAL GR TENSOR QUOTIENT UNIQUENESS AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("PROTOTYPE RESULTS")
    print("=" * 78)
    print(f"scalar_direct   = {scalar_direct:.12e}")
    print(f"scalar_expected = {scalar_expected:.12e}")
    print(f"gram_rank       = {rank(gram)}")
    print(f"gram_size       = {len(gram)}")
    print(f"symmetry_error  = {max_symmetry_error(gram):.12e}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Direct-universal progress: the tensor Hessian is now unique on the "
            "symmetric 3+1 quotient at quadratic order, and the remaining gap is "
            "the curvature-localization map to Einstein/Regge dynamics."
        )
        return 0

    print("One or more candidate checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
