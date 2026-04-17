#!/usr/bin/env python3
"""Bounded scan of simple same-source nonlinear metric closures.

Purpose:
  Starting from the exact O_h-symmetric strong-field source law already found
  on codex/review-active, test whether the remaining 4D Einstein residual is
  merely due to the too-rigid direct closure

      psi = 1 + phi
      alpha * psi = 1 - phi

  or whether the residual survives the simplest nonlinear same-source
  deformations consistent with the weak-field limit.

Ansatz family:
  psi(phi)        = 1 + phi + a2 * phi^2
  alpha*psi(phi)  = 1 - phi + b2 * phi^2

The linear coefficients are fixed by the retained weak-field surface.
This is a bounded search, not a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np
from scipy import sparse
from scipy.ndimage import map_coordinates
from scipy.sparse.linalg import spsolve


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name, ok, detail, status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


SUPPORT_COORDS = [
    np.array([0, 0, 0], dtype=int),
    np.array([1, 0, 0], dtype=int),
    np.array([-1, 0, 0], dtype=int),
    np.array([0, 1, 0], dtype=int),
    np.array([0, -1, 0], dtype=int),
    np.array([0, 0, 1], dtype=int),
    np.array([0, 0, -1], dtype=int),
]


def build_neg_laplacian_sparse(size: int):
    interior = size - 2
    n = interior**3
    ii, jj, kk = np.mgrid[0:interior, 0:interior, 0:interior]
    flat = ii.ravel() * interior * interior + jj.ravel() * interior + kk.ravel()

    rows = [flat]
    cols = [flat]
    vals = [np.full(n, 6.0)]
    for di, dj, dk in [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]:
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

    H0 = sparse.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(n, n),
    )
    return H0, interior


def flat_idx(i: int, j: int, k: int, interior: int) -> int:
    return i * interior * interior + j * interior + k


def solve_columns(matrix, support: list[int]) -> np.ndarray:
    cols = []
    for site in support:
        rhs = np.zeros(matrix.shape[0])
        rhs[site] = 1.0
        cols.append(spsolve(matrix, rhs))
    return np.column_stack(cols)


def build_adapted_basis() -> np.ndarray:
    e0 = np.zeros(7)
    e0[0] = 1.0
    px, mx, py, my, pz, mz = [np.eye(7)[i] for i in range(1, 7)]
    s = (px + mx + py + my + pz + mz) / np.sqrt(6.0)
    e1 = (px + mx - py - my) / 2.0
    e2 = (px + mx + py + my - 2.0 * pz - 2.0 * mz) / np.sqrt(12.0)
    tx = (px - mx) / np.sqrt(2.0)
    ty = (py - my) / np.sqrt(2.0)
    tz = (pz - mz) / np.sqrt(2.0)
    return np.column_stack([e0, s, e1, e2, tx, ty, tz])


B = build_adapted_basis()


def build_commutant_operator(a: float, b: float, c: float, lam_e: float, lam_t: float) -> np.ndarray:
    block = np.array(
        [
            [a, c, 0.0, 0.0, 0.0, 0.0, 0.0],
            [c, b, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, lam_e, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, lam_e, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, lam_t, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, lam_t, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, lam_t],
        ]
    )
    return B @ block @ B.T


def build_invariant_source(m0: float, ms: float) -> np.ndarray:
    v = np.zeros(7)
    v[0] = m0
    v[1:] = ms
    return v


def build_best_phi_grid():
    size = 15
    H0, interior = build_neg_laplacian_sparse(size)
    center = interior // 2
    support = [flat_idx(center + v[0], center + v[1], center + v[2], interior) for v in SUPPORT_COORDS]
    G0P = solve_columns(H0, support)
    GS = G0P[support, :]

    # Best exact O_h-symmetric source law found by frontier_oh_source_class_scan.py
    x1, x2, mix, lam_e, lam_t = 0.0698, 0.0499, -0.0070, 0.0642, 0.1056
    m0, ms = 0.8247, 0.2271
    W = build_commutant_operator(x1, x2, mix, lam_e, lam_t)
    m = build_invariant_source(m0, ms)
    q_eff = np.linalg.solve(np.eye(7) - W @ GS, m)
    phi_flat = G0P @ q_eff

    phi_grid = np.zeros((size, size, size))
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))

    support_points = [(center + v[0] + 1, center + v[1] + 1, center + v[2] + 1) for v in SUPPORT_COORDS]
    phi_max = max(float(phi_grid[idx]) for idx in support_points)
    scale = 0.35 / phi_max
    phi_grid *= scale
    return phi_grid


def interpolate_field(phi_grid: np.ndarray, point: np.ndarray) -> float:
    center = (phi_grid.shape[0] - 1) / 2.0
    coords = np.array([[center + point[0]], [center + point[1]], [center + point[2]]], dtype=float)
    return float(map_coordinates(phi_grid, coords, order=3, mode="nearest")[0])


def metric_from_phi(phi: float, a2: float, b2: float) -> np.ndarray:
    psi = 1.0 + phi + a2 * phi * phi
    alpha_psi = 1.0 - phi + b2 * phi * phi
    alpha = alpha_psi / psi
    return np.diag(np.array([-(alpha**2), psi**4, psi**4, psi**4], dtype=float))


def christoffel(metric_fn, point: np.ndarray, h: float = 0.05) -> np.ndarray:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    dg = np.zeros((4, 4, 4))
    for axis in range(1, 4):
        dp = point.copy()
        dm = point.copy()
        dp[axis - 1] += h
        dm[axis - 1] -= h
        dg[axis] = (metric_fn(dp) - metric_fn(dm)) / (2.0 * h)
    gamma = np.zeros((4, 4, 4))
    for lam, mu, nu in product(range(4), repeat=3):
        total = 0.0
        for rho in range(4):
            total += g_inv[lam, rho] * (dg[mu, rho, nu] + dg[nu, rho, mu] - dg[rho, mu, nu])
        gamma[lam, mu, nu] = 0.5 * total
    return gamma


def dgamma(metric_fn, point: np.ndarray, axis: int, h: float = 0.05) -> np.ndarray:
    if axis == 0:
        return np.zeros((4, 4, 4))
    dp = point.copy()
    dm = point.copy()
    dp[axis - 1] += h
    dm[axis - 1] -= h
    return (christoffel(metric_fn, dp, h) - christoffel(metric_fn, dm, h)) / (2.0 * h)


def einstein_tensor(metric_fn, point: np.ndarray, h: float = 0.05) -> np.ndarray:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    gamma = christoffel(metric_fn, point, h)
    dgammas = np.zeros((4, 4, 4, 4))
    for axis in range(1, 4):
        dgammas[axis] = dgamma(metric_fn, point, axis, h)

    ricci = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            term1 = term2 = term3 = term4 = 0.0
            for lam in range(4):
                term1 += dgammas[lam, lam, mu, nu]
                term2 += dgammas[nu, lam, mu, lam]
                trace_lam = sum(gamma[rho, lam, rho] for rho in range(4))
                term3 += gamma[lam, mu, nu] * trace_lam
                for rho in range(4):
                    term4 += gamma[rho, mu, lam] * gamma[lam, nu, rho]
            ricci[mu, nu] = term1 - term2 + term3 - term4
    scalar = float(np.sum(g_inv * ricci))
    return ricci - 0.5 * g * scalar


def residual_norm(phi_grid: np.ndarray, a2: float, b2: float) -> float:
    def metric_fn(point: np.ndarray) -> np.ndarray:
        phi = interpolate_field(phi_grid, point)
        return metric_from_phi(phi, a2, b2)

    points = [
        np.array([2.5, 0.0, 0.0]),
        np.array([3.0, 0.0, 0.0]),
        np.array([3.0 / np.sqrt(3)] * 3),
    ]
    vals = []
    for p in points:
        G = einstein_tensor(metric_fn, p)
        vals.append(float(np.max(np.abs(G))))
    return max(vals)


def positivity_ok(phi_grid: np.ndarray, a2: float, b2: float) -> bool:
    pts = [
        np.array([2.0, 0.0, 0.0]),
        np.array([2.5, 0.0, 0.0]),
        np.array([3.0 / np.sqrt(3)] * 3),
    ]
    for p in pts:
        phi = interpolate_field(phi_grid, p)
        psi = 1.0 + phi + a2 * phi * phi
        alpha_psi = 1.0 - phi + b2 * phi * phi
        if psi <= 0.0 or alpha_psi <= 0.0:
            return False
    return True


def main() -> None:
    print("Same-source nonlinear metric ansatz scan")
    print("=" * 72)
    phi_grid = build_best_phi_grid()

    # Baseline direct candidate
    baseline = residual_norm(phi_grid, 0.0, 0.0)
    record(
        "baseline direct same-source metric reproduces prior residual floor",
        baseline < 3.5e-2,
        f"baseline max |G_mu_nu|={baseline:.3e}",
    )

    grid = np.linspace(-1.0, 1.0, 11)
    best = None
    best_params = None
    tested = 0
    for a2, b2 in product(grid, grid):
        if not positivity_ok(phi_grid, a2, b2):
            continue
        res = residual_norm(phi_grid, a2, b2)
        tested += 1
        if best is None or res < best:
            best = res
            best_params = (a2, b2)

    assert best is not None and best_params is not None
    record(
        "simple nonlinear same-source ansatz can improve the direct metric residual",
        best < baseline,
        f"baseline={baseline:.3e}, best={best:.3e} at a2={best_params[0]:.2f}, b2={best_params[1]:.2f}",
    )
    record(
        "simple quadratic same-source closure still does not produce vacuum-grade 4D closure",
        best > 1e-3,
        f"best max |G_mu_nu|={best:.3e} over {tested} admissible (a2,b2) choices",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"Baseline max |G_mu_nu|={baseline:.6e}")
    print(f"Best max |G_mu_nu|={best:.6e}")
    print(f"Best parameters: a2={best_params[0]:.3f}, b2={best_params[1]:.3f}")
    print(f"Admissible ansatze tested: {tested}")
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
