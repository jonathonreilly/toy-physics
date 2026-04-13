#!/usr/bin/env python3
"""Distributed-source strong-field closure and common spacetime candidate.

This script extends the exact rank-one strong-field resolvent identity to a
finite-support diagonal attractive source model and then uses the same exterior
harmonic field to build a bounded static isotropic 4D metric candidate.

Exact content:
  1. Finite-support Woodbury/Dyson resolvent identity for H_V = H_0 - P V P^T
  2. Exact compressed-source formula phi = G_0 P (I - V G_S)^(-1) m
  3. Exterior harmonicity of phi outside the support S

Bounded content:
  4. Common-source spacetime candidate
       psi = 1 + phi
       alpha * psi = 1 - phi
       alpha = (1 - phi) / (1 + phi)
     which satisfies the static isotropic vacuum bridge equations outside S

This is not a derivation of full nonlinear GR.  It removes the "point source
only" limitation from the exact source-model foothold and shows how a single
source-renormalized harmonic object can feed both spatial and temporal sectors.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("scipy is required") from exc


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def build_path_laplacian(length: int) -> np.ndarray:
    H = np.zeros((length, length))
    for i in range(length):
        H[i, i] = 2.0
        if i > 0:
            H[i, i - 1] = -1.0
        if i < length - 1:
            H[i, i + 1] = -1.0
    return H


def build_neg_laplacian_sparse(size: int):
    interior = size - 2
    n = interior * interior * interior
    ii, jj, kk = np.mgrid[0:interior, 0:interior, 0:interior]
    flat = ii.ravel() * interior * interior + jj.ravel() * interior + kk.ravel()

    rows = [flat]
    cols = [flat]
    vals = [np.full(n, 6.0)]
    for di, dj, dk in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        ni = ii + di
        nj = jj + dj
        nk = kk + dk
        mask = (
            (ni >= 0)
            & (ni < interior)
            & (nj >= 0)
            & (nj < interior)
            & (nk >= 0)
            & (nk < interior)
        )
        src = flat[mask.ravel()]
        dst = ni[mask] * interior * interior + nj[mask] * interior + nk[mask]
        rows.append(src)
        cols.append(dst.ravel())
        vals.append(-np.ones(src.shape[0]))

    return sparse.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n, n),
    ), interior


def solve_columns(matrix, support: list[int]) -> np.ndarray:
    cols = []
    for site in support:
        rhs = np.zeros(matrix.shape[0])
        rhs[site] = 1.0
        cols.append(spsolve(matrix, rhs))
    return np.column_stack(cols)


def support_projector(n: int, support: list[int]) -> np.ndarray:
    P = np.zeros((n, len(support)))
    for col, site in enumerate(support):
        P[site, col] = 1.0
    return P


def finite_support_column_formula(G0P: np.ndarray, GS: np.ndarray, V: np.ndarray) -> np.ndarray:
    return G0P @ np.linalg.inv(np.eye(V.shape[0]) - V @ GS)


def flat_idx(i: int, j: int, k: int, interior: int) -> int:
    return i * interior * interior + j * interior + k


def full_neg_laplacian(field: np.ndarray) -> np.ndarray:
    lap = np.zeros_like(field)
    lap[1:-1, 1:-1, 1:-1] = (
        6.0 * field[1:-1, 1:-1, 1:-1]
        - field[2:, 1:-1, 1:-1]
        - field[:-2, 1:-1, 1:-1]
        - field[1:-1, 2:, 1:-1]
        - field[1:-1, :-2, 1:-1]
        - field[1:-1, 1:-1, 2:]
        - field[1:-1, 1:-1, :-2]
    )
    return lap


def finite_support_setup_1d():
    H0 = build_path_laplacian(25)
    support = [11, 12, 13]
    G0 = np.linalg.inv(H0)
    G0P = G0[:, support]
    GS = G0[np.ix_(support, support)]
    fractions = np.array([0.16, 0.22, 0.16])
    V = np.diag(fractions / np.diag(GS))
    masses = np.array([0.8, 1.0, 0.8])
    return H0, support, G0P, GS, V, masses


def finite_support_setup_3d():
    size = 11
    H0, interior = build_neg_laplacian_sparse(size)
    center = interior // 2
    support = [
        flat_idx(center, center, center, interior),
        flat_idx(center + 1, center, center, interior),
        flat_idx(center - 1, center, center, interior),
        flat_idx(center, center + 1, center, interior),
        flat_idx(center, center - 1, center, interior),
        flat_idx(center, center, center + 1, interior),
        flat_idx(center, center, center - 1, interior),
    ]
    G0P = solve_columns(H0, support)
    GS = G0P[support, :]
    fractions = np.array([0.11, 0.09, 0.09, 0.085, 0.085, 0.08, 0.08])
    V = np.diag(fractions / np.diag(GS))
    masses = np.array([1.0, 0.7, 0.7, 0.6, 0.6, 0.55, 0.55])
    return size, H0, interior, support, G0P, GS, V, masses


def test_distributed_resolvent_identity_1d() -> None:
    print("\n" + "=" * 72)
    print("PART 1: EXACT DISTRIBUTED-SOURCE RESOLVENT IDENTITY (1D)")
    print("=" * 72)
    H0, support, G0P, GS, V, masses = finite_support_setup_1d()
    P = support_projector(H0.shape[0], support)
    full = np.linalg.inv(H0 - P @ V @ P.T)
    exact_cols = full[:, support]
    formula_cols = finite_support_column_formula(G0P, GS, V)
    err = float(np.max(np.abs(exact_cols - formula_cols)))
    record(
        "1D finite-support column identity",
        err < 1e-10,
        f"max column error={err:.3e}, support size={len(support)}",
    )

    phi_exact = exact_cols @ masses
    renorm = np.linalg.solve(np.eye(len(support)) - V @ GS, masses)
    phi_formula = G0P @ renorm
    err_phi = float(np.max(np.abs(phi_exact - phi_formula)))
    record(
        "1D compressed distributed source",
        err_phi < 1e-10,
        f"max field error={err_phi:.3e}",
    )

    residual = H0 @ phi_formula
    mask = np.ones(H0.shape[0], dtype=bool)
    mask[support] = False
    ext_res = float(np.max(np.abs(residual[mask])))
    record(
        "1D exterior harmonicity outside support",
        ext_res < 1e-10,
        f"max exterior residual={ext_res:.3e}",
    )


def test_distributed_resolvent_identity_3d() -> tuple[np.ndarray, list[int], int]:
    print("\n" + "=" * 72)
    print("PART 2: EXACT DISTRIBUTED-SOURCE RESOLVENT IDENTITY (3D)")
    print("=" * 72)
    size, H0, interior, support, G0P, GS, V, masses = finite_support_setup_3d()
    P = support_projector(H0.shape[0], support)
    exact_cols = solve_columns(H0 - sparse.csr_matrix(P @ V @ P.T), support)
    formula_cols = finite_support_column_formula(G0P, GS, V)
    err_cols = float(np.max(np.abs(exact_cols - formula_cols)))
    record(
        "3D finite-support column identity",
        err_cols < 1e-9,
        f"max column error={err_cols:.3e}, support size={len(support)}",
    )

    renorm = np.linalg.solve(np.eye(len(support)) - V @ GS, masses)
    phi_exact = exact_cols @ masses
    phi_formula = G0P @ renorm
    err_phi = float(np.max(np.abs(phi_exact - phi_formula)))
    record(
        "3D compressed distributed source",
        err_phi < 1e-9,
        f"max field error={err_phi:.3e}",
    )

    residual = H0 @ phi_formula
    mask = np.ones(H0.shape[0], dtype=bool)
    mask[support] = False
    ext_res = float(np.max(np.abs(residual[mask])))
    record(
        "3D exterior harmonicity outside support",
        ext_res < 1e-9,
        f"max exterior residual={ext_res:.3e}",
    )

    return phi_formula, support, interior


def test_common_spacetime_candidate(phi_flat: np.ndarray, support: list[int], interior: int) -> None:
    print("\n" + "=" * 72)
    print("PART 3: BOUNDED COMMON-SPACETIME CANDIDATE")
    print("=" * 72)
    size = interior + 2
    phi_full = np.zeros((size, size, size))
    phi_full[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))

    support_full = []
    for site in support:
        i = site // (interior * interior)
        j = (site // interior) % interior
        k = site % interior
        support_full.append((i + 1, j + 1, k + 1))

    scale = 0.35 / max(float(phi_full[idx]) for idx in support_full)
    phi_full *= scale
    psi = 1.0 + phi_full
    alpha_times_psi = 1.0 - phi_full
    alpha = alpha_times_psi / psi

    mask = np.ones((size, size, size), dtype=bool)
    mask[[0, -1], :, :] = False
    mask[:, [0, -1], :] = False
    mask[:, :, [0, -1]] = False
    for idx in support_full:
        mask[idx] = False

    lap_psi = full_neg_laplacian(psi)
    lap_alpha_psi = full_neg_laplacian(alpha * psi)
    res_psi = float(np.max(np.abs(lap_psi[mask])))
    res_alpha_psi = float(np.max(np.abs(lap_alpha_psi[mask])))
    alpha_min = min(float(alpha[idx]) for idx in support_full)
    phi_max = max(float(phi_full[idx]) for idx in support_full)

    record(
        "candidate static-isotropic Einstein residual: psi",
        res_psi < 1e-10,
        f"max |(-Delta) psi| outside support={res_psi:.3e}",
        status="BOUNDED",
    )
    record(
        "candidate static-isotropic Einstein residual: alpha psi",
        res_alpha_psi < 1e-10,
        f"max |(-Delta)(alpha psi)| outside support={res_alpha_psi:.3e}",
        status="BOUNDED",
    )
    record(
        "candidate lapse remains nondegenerate",
        alpha_min > 0.0 and phi_max < 1.0,
        f"phi_max={phi_max:.6f}, alpha_min={alpha_min:.6f}",
        status="BOUNDED",
    )


def main() -> None:
    print("Distributed-source strong-field closure and common spacetime candidate")
    print("=" * 72)
    print("Exact: extend the rank-one resolvent identity to a finite-support")
    print("distributed attractive source model.")
    print("Bounded: use the same harmonic source object to build psi and alpha")
    print("for a static isotropic vacuum candidate.")

    test_distributed_resolvent_identity_1d()
    phi_formula, support, interior = test_distributed_resolvent_identity_3d()
    test_common_spacetime_candidate(phi_formula, support, interior)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    exact = sum(1 for c in CHECKS if c.status == "EXACT")
    bounded = sum(1 for c in CHECKS if c.status == "BOUNDED")
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    print(f"EXACT={exact} BOUNDED={bounded}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
