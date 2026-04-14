#!/usr/bin/env python3
"""Finite-rank strong-field source closure and 4D residual test.

Exact content:
  1. Finite-rank Woodbury / Dyson identity for H_V = H_0 - P W P^T with
     positive-semidefinite W on a finite support S.
  2. Exact compressed-source formula phi = G_0 P (I - W G_S)^(-1) m.
  3. Exact exterior harmonicity of phi outside S.

Bounded content:
  4. Shell-averaged exterior field is monopole-dominated.
  5. The direct common-source metric candidate built from the exact phi has a
     nonzero 4D Einstein residual outside the source.
  6. The monopole-projected isotropic candidate from the same phi has a much
     smaller 4D Einstein residual.

This sharpens the remaining gravity blocker: the exact strong-field source
model is now broader than the old diagonal class, but the exact field still
needs a theorem-grade reduction to the static isotropic vacuum surface before
full nonlinear GR can be claimed.
"""

from __future__ import annotations

from dataclasses import dataclass

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


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


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


def flat_idx(i: int, j: int, k: int, interior: int) -> int:
    return i * interior * interior + j * interior + k


def support_projector(n: int, support: list[int]) -> np.ndarray:
    P = np.zeros((n, len(support)))
    for col, site in enumerate(support):
        P[site, col] = 1.0
    return P


def solve_columns(matrix, support: list[int]) -> np.ndarray:
    cols = []
    for site in support:
        rhs = np.zeros(matrix.shape[0])
        rhs[site] = 1.0
        cols.append(spsolve(matrix, rhs))
    return np.column_stack(cols)


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


def finite_rank_setup():
    size = 15
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

    base = np.array([0.11, 0.08, 0.08, 0.075, 0.075, 0.07, 0.07])
    D = np.diag(np.sqrt(base / np.diag(GS)))
    corr = np.eye(len(support)) + 0.18 * np.ones((len(support), len(support)))
    W_raw = D @ corr @ D

    eigvals = np.linalg.eigvals(W_raw @ GS)
    rho = max(abs(ev) for ev in eigvals)
    scale = 0.45 / rho
    W = scale * W_raw

    masses = np.array([1.0, 0.82, 0.77, 0.73, 0.69, 0.64, 0.61])
    return size, H0, interior, support, G0P, GS, W, masses


def exact_finite_rank_field():
    size, H0, interior, support, G0P, GS, W, masses = finite_rank_setup()
    P = support_projector(H0.shape[0], support)
    full = solve_columns(H0 - sparse.csr_matrix(P @ W @ P.T), support)
    formula = G0P @ np.linalg.inv(np.eye(W.shape[0]) - W @ GS)
    err_cols = float(np.max(np.abs(full - formula)))
    record(
        "finite-rank column identity",
        err_cols < 1e-9,
        f"max column error={err_cols:.3e}, support size={len(support)}",
    )

    phi_exact = full @ masses
    q_eff = np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)
    phi_formula = G0P @ q_eff
    err_phi = float(np.max(np.abs(phi_exact - phi_formula)))
    record(
        "finite-rank compressed source",
        err_phi < 1e-9,
        f"max field error={err_phi:.3e}",
    )

    residual = H0 @ phi_formula
    mask = np.ones(H0.shape[0], dtype=bool)
    mask[support] = False
    ext_res = float(np.max(np.abs(residual[mask])))
    record(
        "finite-rank exterior harmonicity outside support",
        ext_res < 1e-9,
        f"max exterior residual={ext_res:.3e}",
    )

    full_grid = np.zeros((size, size, size))
    full_grid[1:-1, 1:-1, 1:-1] = phi_formula.reshape((interior, interior, interior))
    return full_grid, support, interior, q_eff


def shell_average_monopole_fit(phi_full: np.ndarray):
    size = phi_full.shape[0]
    center = (size - 1) / 2.0
    shells: dict[int, list[float]] = {}
    radii: dict[int, float] = {}
    support_radius_sq = 1
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            for k in range(1, size - 1):
                dx = i - center
                dy = j - center
                dz = k - center
                d2 = int(dx * dx + dy * dy + dz * dz)
                if d2 <= support_radius_sq or d2 == 0:
                    continue
                shells.setdefault(d2, []).append(float(phi_full[i, j, k]))
                radii[d2] = float(np.sqrt(d2))

    usable = sorted(d2 for d2, vals in shells.items() if len(vals) >= 6 and radii[d2] <= center - 1)
    r = np.array([radii[d2] for d2 in usable], dtype=float)
    y = np.array([np.mean(shells[d2]) for d2 in usable], dtype=float)
    X = np.column_stack([1.0 / r, 1.0 / (r**3)])
    coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    a_fit, b_fit = coeffs
    y_fit = X @ coeffs
    rel_rms = float(np.sqrt(np.mean((y - y_fit) ** 2)) / max(np.max(np.abs(y)), 1e-12))
    record(
        "shell-averaged field is monopole-dominated",
        rel_rms < 0.12 and a_fit > 0.0,
        f"a={a_fit:.6f}, b={b_fit:.6f}, relative RMS fit error={rel_rms:.3f}",
        status="BOUNDED",
    )
    return float(a_fit), float(b_fit), rel_rms


def interpolate_phi(phi_full: np.ndarray, point: np.ndarray) -> float:
    center = (phi_full.shape[0] - 1) / 2.0
    coords = np.array([[point[0] + center], [point[1] + center], [point[2] + center]])
    return float(map_coordinates(phi_full, coords, order=3, mode="nearest")[0])


def metric_from_phi(phi: float) -> np.ndarray:
    psi = 1.0 + phi
    alpha = (1.0 - phi) / (1.0 + phi)
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
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                total = 0.0
                for rho in range(4):
                    total += g_inv[lam, rho] * (
                        dg[mu, rho, nu] + dg[nu, rho, mu] - dg[rho, mu, nu]
                    )
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
            term1 = 0.0
            term2 = 0.0
            term3 = 0.0
            term4 = 0.0
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


def residual_probe(metric_fn, points: list[np.ndarray], h: float = 0.05):
    norms = []
    for point in points:
        G = einstein_tensor(metric_fn, point, h)
        norms.append(float(np.max(np.abs(G))))
    return max(norms), norms


def bounded_metric_residual_tests(phi_full: np.ndarray, a_fit: float) -> None:
    size = phi_full.shape[0]
    center = (size - 1) / 2.0

    def metric_direct(point: np.ndarray) -> np.ndarray:
        phi = interpolate_phi(phi_full, point)
        return metric_from_phi(phi)

    def metric_monopole(point: np.ndarray) -> np.ndarray:
        r = float(np.linalg.norm(point))
        phi = a_fit / r
        return metric_from_phi(phi)

    sample_points = [
        np.array([2.5, 0.0, 0.0]),
        np.array([3.0, 0.0, 0.0]),
        np.array([3.5, 0.0, 0.0]),
        np.array([2.5 / np.sqrt(2), 2.5 / np.sqrt(2), 0.0]),
        np.array([3.0 / np.sqrt(3)] * 3),
    ]
    sample_points = [p for p in sample_points if np.max(np.abs(p)) < center - 1.5]

    direct_max, direct_each = residual_probe(metric_direct, sample_points)
    mono_max, mono_each = residual_probe(metric_monopole, sample_points)
    improvement = direct_max / max(mono_max, 1e-15)

    record(
        "direct common-source candidate has bounded nonzero 4D residual",
        direct_max > 1e-3,
        f"max |G_mu_nu|={direct_max:.3e} across {len(sample_points)} exterior probes",
        status="BOUNDED",
    )
    record(
        "monopole-projected isotropic candidate sharply reduces 4D residual",
        mono_max < direct_max * 0.1,
        f"direct max={direct_max:.3e}, monopole max={mono_max:.3e}, improvement={improvement:.1f}x",
        status="BOUNDED",
    )
    record(
        "monopole candidate is near-vacuum on exterior probes",
        mono_max < 5e-4,
        f"max |G_mu_nu|={mono_max:.3e}; pointwise={', '.join(f'{x:.1e}' for x in mono_each)}",
        status="BOUNDED",
    )


def main() -> None:
    print("Finite-rank strong-field closure and 4D Einstein-residual test")
    print("=" * 72)
    phi_full, support, interior, q_eff = exact_finite_rank_field()
    a_fit, b_fit, rel_rms = shell_average_monopole_fit(phi_full)
    bounded_metric_residual_tests(phi_full, a_fit)

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"Effective renormalized support weights sum = {np.sum(q_eff):.6f}")
    print(f"Monopole fit coefficient a = {a_fit:.6f}, subleading b = {b_fit:.6f}")
    print(f"Shell-fit relative RMS = {rel_rms:.3f}")
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
