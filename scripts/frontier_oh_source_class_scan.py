#!/usr/bin/env python3
"""Exact O_h-symmetric local source class and strong-field metric scan.

Exact content:
  1. The most general real symmetric O_h-invariant source operator on the
     star support S = {0, ±e_x, ±e_y, ±e_z} has five parameters.
  2. The most general O_h-invariant bare source vector on the same support has
     two parameters.
  3. This follows from the symmetry-adapted decomposition
       A1g(center) ⊕ A1g(arms-sum) ⊕ Eg ⊕ T1u.

Bounded content:
  4. Scan the exact O_h source class at fixed strong-field amplitude and test
     the direct common-source metric candidate against 4D Einstein residuals.
  5. Report the best residual found within the full local cubic-symmetric
     source class.

This does not close full nonlinear GR. It removes another ambiguity by
showing exactly what the local static cubic-symmetric source law can be, and
whether source-class freedom alone is enough to make the direct metric
candidate vacuum-close.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product

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


def build_oh_group() -> list[np.ndarray]:
    group = []
    eye = np.eye(3, dtype=int)
    for perm in permutations(range(3)):
        P = eye[:, perm]
        for signs in product([-1, 1], repeat=3):
            M = np.diag(signs) @ P
            if not any(np.array_equal(M, G) for G in group):
                group.append(M)
    return group


OH = build_oh_group()

SUPPORT_COORDS = [
    np.array([0, 0, 0], dtype=int),
    np.array([1, 0, 0], dtype=int),
    np.array([-1, 0, 0], dtype=int),
    np.array([0, 1, 0], dtype=int),
    np.array([0, -1, 0], dtype=int),
    np.array([0, 0, 1], dtype=int),
    np.array([0, 0, -1], dtype=int),
]
SUPPORT_MAP = {tuple(v.tolist()): i for i, v in enumerate(SUPPORT_COORDS)}


def support_representation(M: np.ndarray) -> np.ndarray:
    U = np.zeros((len(SUPPORT_COORDS), len(SUPPORT_COORDS)))
    for i, v in enumerate(SUPPORT_COORDS):
        image = tuple((M @ v).tolist())
        j = SUPPORT_MAP[image]
        U[j, i] = 1.0
    return U


U_GROUP = [support_representation(G) for G in OH]


def symmetry_adapted_basis() -> np.ndarray:
    e0 = np.zeros(7)
    e0[0] = 1.0
    px, mx, py, my, pz, mz = [np.eye(7)[i] for i in range(1, 7)]
    s = (px + mx + py + my + pz + mz) / np.sqrt(6.0)
    e1 = (px + mx - py - my) / 2.0
    e2 = (px + mx + py + my - 2.0 * pz - 2.0 * mz) / np.sqrt(12.0)
    tx = (px - mx) / np.sqrt(2.0)
    ty = (py - my) / np.sqrt(2.0)
    tz = (pz - mz) / np.sqrt(2.0)
    B = np.column_stack([e0, s, e1, e2, tx, ty, tz])
    return B


B_ADAPT = symmetry_adapted_basis()


def build_commutant_operator(a: float, b: float, c: float, lam_e: float, lam_t: float) -> np.ndarray:
    block = np.array([
        [a, c, 0.0, 0.0, 0.0, 0.0, 0.0],
        [c, b, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, lam_e, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, lam_e, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, lam_t, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, lam_t, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, lam_t],
    ])
    return B_ADAPT @ block @ B_ADAPT.T


def build_invariant_source(m0: float, ms: float) -> np.ndarray:
    vec = np.zeros(7)
    vec[0] = m0
    vec[1:] = ms
    return vec


def reynolds_project(mat: np.ndarray) -> np.ndarray:
    acc = np.zeros_like(mat, dtype=float)
    for U in U_GROUP:
        acc += U @ mat @ U.T
    return acc / len(U_GROUP)


def reynolds_project_vec(vec: np.ndarray) -> np.ndarray:
    acc = np.zeros_like(vec, dtype=float)
    for U in U_GROUP:
        acc += U @ vec
    return acc / len(U_GROUP)


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


def finite_support_setup():
    size = 15
    H0, interior = build_neg_laplacian_sparse(size)
    center = interior // 2
    support = [flat_idx(center + v[0], center + v[1], center + v[2], interior) for v in SUPPORT_COORDS]
    G0P = solve_columns(H0, support)
    GS = G0P[support, :]
    return size, H0, interior, support, G0P, GS


def interpolate_field(phi_grid: np.ndarray, point: np.ndarray) -> float:
    center = (phi_grid.shape[0] - 1) / 2.0
    coords = np.array(
        [[center + point[0]], [center + point[1]], [center + point[2]]],
        dtype=float,
    )
    return float(map_coordinates(phi_grid, coords, order=3, mode="nearest")[0])


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


def residual_norm(phi_grid: np.ndarray) -> float:
    def metric_fn(point: np.ndarray) -> np.ndarray:
        return metric_from_phi(interpolate_field(phi_grid, point))

    points = [
        np.array([2.5, 0.0, 0.0]),
        np.array([3.0, 0.0, 0.0]),
        np.array([3.5, 0.0, 0.0]),
        np.array([2.5 / np.sqrt(2), 2.5 / np.sqrt(2), 0.0]),
        np.array([3.0 / np.sqrt(3)] * 3),
    ]
    vals = []
    for p in points:
        G = einstein_tensor(metric_fn, p)
        vals.append(float(np.max(np.abs(G))))
    return max(vals)


def exact_source_class_checks():
    # exact commutant dimension
    basis = []
    for i in range(7):
        for j in range(i, 7):
            M = np.zeros((7, 7))
            M[i, j] = 1.0
            M[j, i] = 1.0 if j != i else 1.0
            basis.append(reynolds_project(M).reshape(-1))
    rank = np.linalg.matrix_rank(np.column_stack(basis), tol=1e-10)
    record(
        "O_h-invariant symmetric source operator class has dimension five",
        rank == 5,
        f"commutant dimension={rank}",
    )

    # explicit parameterization spans the commutant
    model_basis = [
        build_commutant_operator(1, 0, 0, 0, 0).reshape(-1),
        build_commutant_operator(0, 1, 0, 0, 0).reshape(-1),
        build_commutant_operator(0, 0, 1, 0, 0).reshape(-1),
        build_commutant_operator(0, 0, 0, 1, 0).reshape(-1),
        build_commutant_operator(0, 0, 0, 0, 1).reshape(-1),
    ]
    M_model = np.column_stack(model_basis)
    rng = np.random.default_rng(20260413)
    worst = 0.0
    for _ in range(5):
        A = rng.standard_normal((7, 7))
        A = (A + A.T) / 2.0
        proj = reynolds_project(A).reshape(-1)
        coeffs, _, _, _ = np.linalg.lstsq(M_model, proj, rcond=None)
        err = float(np.max(np.abs(M_model @ coeffs - proj)))
        worst = max(worst, err)
    record(
        "explicit five-parameter basis spans the exact commutant",
        worst < 1e-10,
        f"worst projection reconstruction error={worst:.3e}",
    )

    # source-vector invariant space dimension
    vec_basis = []
    for i in range(7):
        e = np.eye(7)[i]
        vec_basis.append(reynolds_project_vec(e))
    rank_vec = np.linalg.matrix_rank(np.column_stack(vec_basis), tol=1e-10)
    record(
        "O_h-invariant bare source vector space has dimension two",
        rank_vec == 2,
        f"invariant vector dimension={rank_vec}",
    )


def bounded_metric_scan():
    size, H0, interior, support, G0P, GS = finite_support_setup()
    P = support_projector(H0.shape[0], support)
    center = interior // 2
    rng = np.random.default_rng(7)

    best = None
    best_payload = None
    tested = 0

    # broad but cheap scan over exact physical source class
    for _ in range(180):
        # 2x2 positive block in the A1g sector
        x1, x2 = rng.uniform(0.02, 0.25, size=2)
        mix = rng.uniform(-0.10, 0.10)
        if abs(mix) >= np.sqrt(x1 * x2):
            continue
        lam_e = rng.uniform(0.00, 0.18)
        lam_t = rng.uniform(0.00, 0.18)
        W = build_commutant_operator(x1, x2, mix, lam_e, lam_t)
        rho = max(abs(ev) for ev in np.linalg.eigvals(W @ GS))
        if rho >= 0.98:
            continue

        m0 = rng.uniform(0.6, 1.4)
        ms = rng.uniform(0.2, 1.0)
        m = build_invariant_source(m0, ms)
        q_eff = np.linalg.solve(np.eye(7) - W @ GS, m)
        phi_flat = G0P @ q_eff
        phi_grid = np.zeros((size, size, size))
        phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))

        support_points = [(center + v[0] + 1, center + v[1] + 1, center + v[2] + 1) for v in SUPPORT_COORDS]
        phi_max = max(float(phi_grid[idx]) for idx in support_points)
        if phi_max <= 0:
            continue
        scale = 0.35 / phi_max
        phi_grid *= scale

        res = residual_norm(phi_grid)
        tested += 1
        if best is None or res < best:
            best = res
            best_payload = {
                "params": (x1, x2, mix, lam_e, lam_t, m0, ms),
                "scale": scale,
                "rho": rho,
                "res": res,
            }

    assert best_payload is not None
    record(
        "exact O_h local source class materially reduces the direct 4D residual",
        best_payload["res"] < 0.035,
        f"best max |G_mu_nu|={best_payload['res']:.3e} over {tested} O_h-symmetric source laws",
        status="BOUNDED",
    )
    record(
        "source-class freedom alone does not fully close the direct metric candidate",
        best_payload["res"] > 1e-3,
        f"best max |G_mu_nu|={best_payload['res']:.3e} remains nonzero",
        status="BOUNDED",
    )
    return best_payload, tested


def main() -> None:
    print("Exact O_h-symmetric local source class and strong-field metric scan")
    print("=" * 72)
    exact_source_class_checks()
    best, tested = bounded_metric_scan()

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    x1, x2, mix, lam_e, lam_t, m0, ms = best["params"]
    print(
        "Best source parameters: "
        f"A1g-block=({x1:.4f}, {x2:.4f}, mix={mix:.4f}), "
        f"lam_E={lam_e:.4f}, lam_T={lam_t:.4f}, "
        f"m0={m0:.4f}, ms={ms:.4f}"
    )
    print(f"Spectral radius rho(W G_S)={best['rho']:.4f}")
    print(f"Support rescaling={best['scale']:.4f}")
    print(f"Best max |G_mu_nu|={best['res']:.6e} over {tested} exact O_h source laws")
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
