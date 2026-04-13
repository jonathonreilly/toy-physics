#!/usr/bin/env python3
"""Strong-field resolvent closure for a local source on the lattice.

Goal
----
Replace the ad hoc strong-field backreaction factor used in the current
strong-field metric note with an exact resolvent identity, as far as the
rank-one local-source model permits.

Setup
-----
The weak-field gravity chain already uses additive potential coupling:

    H(phi) = H_0 + phi

For a pointlike attractive source at the origin, the simplest exact local
realization is a rank-one perturbation

    H_u = H_0 - u |0><0|

with u > 0.  The exact resolvent is then given by the Sherman-Morrison /
rank-one Dyson identity:

    G_u = (H_0 - u P_0)^(-1)
        = G_0 + (u / (1 - u G_00)) G_0 P_0 G_0

where G_0 = H_0^(-1), P_0 = |0><0|, and G_00 = <0|G_0|0>.

Consequences
------------
For the source column:

    G_u(x,0) = G_0(x,0) / (1 - u G_00)

and at the source:

    G_u(0,0) = G_00 / (1 - u G_00)

If the local attractive potential is closed self-consistently by

    u G_00 = phi(0),

then the current strong-field fixed profile becomes exact:

    phi(x) = M G_u(x,0) = M G_0(x,0) / (1 - phi(0))

and therefore

    phi(0) (1 - phi(0)) = M G_00.

This does not close full nonlinear GR.  It only shows that the specific
backreaction factor used in the current strong-field point-source note is
an exact resolvent consequence of a rank-one local-source model.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
except ImportError:
    print("ERROR: scipy is required")
    sys.exit(1)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


checks: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    checks.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def build_path_laplacian(L: int) -> np.ndarray:
    H = np.zeros((L, L))
    for i in range(L):
        H[i, i] = 2.0
        if i > 0:
            H[i, i - 1] = -1.0
        if i < L - 1:
            H[i, i + 1] = -1.0
    return H


def build_3d_neg_laplacian_sparse(N: int):
    M = N - 2
    n = M * M * M
    ii, jj, kk = np.mgrid[0:M, 0:M, 0:M]
    flat = ii.ravel() * M * M + jj.ravel() * M + kk.ravel()
    rows = [flat]
    cols = [flat]
    vals = [np.full(n, 6.0)]
    for di, dj, dk in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        ni = ii + di
        nj = jj + dj
        nk = kk + dk
        mask = ((ni >= 0) & (ni < M) & (nj >= 0) & (nj < M) & (nk >= 0) & (nk < M))
        src = flat[mask.ravel()]
        dst = ni[mask] * M * M + nj[mask] * M + nk[mask]
        rows.append(src)
        cols.append(dst.ravel())
        vals.append(-np.ones(src.shape[0]))
    A = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    return A, M


def solve_green_column_sparse(A, src_idx: int) -> np.ndarray:
    rhs = np.zeros(A.shape[0])
    rhs[src_idx] = 1.0
    return spsolve(A, rhs)


def rank_one_resolvent_column(G0_col: np.ndarray, G00: float, u: float) -> np.ndarray:
    return G0_col / (1.0 - u * G00)


def test_rank_one_identity_1d() -> None:
    print("\n" + "=" * 72)
    print("PART 1: EXACT RANK-ONE RESOLVENT IDENTITY (1D)")
    print("=" * 72)
    L = 31
    H0 = build_path_laplacian(L)
    G0 = np.linalg.inv(H0)
    mid = L // 2
    G0_col = G0[:, mid]
    G00 = G0[mid, mid]
    P = np.zeros((L, L))
    P[mid, mid] = 1.0

    print(f"L = {L}, source site = {mid}, G00 = {G00:.12f}")
    for frac in [0.1, 0.25, 0.4, 0.7]:
        u = frac / G00
        Gu = np.linalg.inv(H0 - u * P)
        exact_col = Gu[:, mid]
        sm_col = rank_one_resolvent_column(G0_col, G00, u)
        err_col = np.max(np.abs(exact_col - sm_col))
        err_diag = abs(Gu[mid, mid] - G00 / (1.0 - u * G00))
        record(
            f"1D resolvent identity at uG00={frac:.2f}",
            err_col < 1e-10 and err_diag < 1e-10,
            f"column err={err_col:.3e}, diag err={err_diag:.3e}",
        )


def test_rank_one_identity_3d() -> None:
    print("\n" + "=" * 72)
    print("PART 2: EXACT RANK-ONE RESOLVENT IDENTITY (3D)")
    print("=" * 72)
    N = 7
    A, M = build_3d_neg_laplacian_sparse(N)
    mid = M // 2
    src = mid * M * M + mid * M + mid
    G0_col = solve_green_column_sparse(A, src)
    G00 = float(G0_col[src])
    print(f"N = {N}, interior = {M}^3, source idx = {src}, G00 = {G00:.12f}")
    P = sparse.csr_matrix(([1.0], ([src], [src])), shape=A.shape)

    for frac in [0.1, 0.2, 0.4, 0.7]:
        u = frac / G00
        Gu_col = spsolve(A - u * P, np.eye(A.shape[0])[:, src])
        sm_col = rank_one_resolvent_column(G0_col, G00, u)
        err_col = np.max(np.abs(Gu_col - sm_col))
        Gu00 = float(Gu_col[src])
        err_diag = abs(Gu00 - G00 / (1.0 - u * G00))
        record(
            f"3D resolvent identity at uG00={frac:.2f}",
            err_col < 1e-9 and err_diag < 1e-9,
            f"column err={err_col:.3e}, diag err={err_diag:.3e}",
        )


def test_self_consistent_fixed_point() -> None:
    print("\n" + "=" * 72)
    print("PART 3: SELF-CONSISTENT FIXED POINT FROM EXACT RESOLVENT")
    print("=" * 72)
    N = 7
    A, M = build_3d_neg_laplacian_sparse(N)
    mid = M // 2
    src = mid * M * M + mid * M + mid
    G0_col = solve_green_column_sparse(A, src)
    G00 = float(G0_col[src])
    print(f"N = {N}, G00 = {G00:.12f}")

    for frac in [0.1, 0.2, 0.24]:
        mass = frac / G00
        disc = 1.0 - 4.0 * mass * G00
        phi0 = (1.0 - math.sqrt(disc)) / 2.0
        u = phi0 / G00
        profile_exact = mass * rank_one_resolvent_column(G0_col, G00, u)
        profile_sc = mass * G0_col / (1.0 - phi0)
        err = np.max(np.abs(profile_exact - profile_sc))
        lhs = phi0 * (1.0 - phi0)
        rhs = mass * G00
        record(
            f"quadratic fixed point at M G00={frac:.2f}",
            err < 1e-10 and abs(lhs - rhs) < 1e-12,
            f"profile err={err:.3e}, quadratic err={abs(lhs-rhs):.3e}, phi0={phi0:.8f}",
            status="DERIVED",
        )

    mass_fail = 0.30 / G00
    disc_fail = 1.0 - 4.0 * mass_fail * G00
    record(
        "real fixed point exists only for M G00 <= 1/4",
        disc_fail < 0.0,
        f"for M G00=0.30, discriminant={disc_fail:.6f} < 0",
        status="DERIVED",
    )


def main() -> None:
    print("Strong-field rank-one resolvent closure")
    print("=" * 72)
    print("This script verifies that the strong-field enhancement factor")
    print("used in the current point-source metric note is an exact")
    print("resolvent identity for a rank-one attractive local potential.")
    test_rank_one_identity_1d()
    test_rank_one_identity_3d()
    test_self_consistent_fixed_point()

    n_pass = sum(c.ok for c in checks)
    n_fail = sum(not c.ok for c in checks)
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
