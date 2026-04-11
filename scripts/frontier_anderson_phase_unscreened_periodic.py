#!/usr/bin/env python3
"""
Unscreened Anderson-vs-Gravity Phase Map on Corrected Periodic 2D Surface.

Fresh runner for the mu2=0.001 recheck after the validated minimum-image fix.
This script intentionally focuses on the Anderson-phase lane only. It does not
reuse or overwrite the retained mixed eigenvalue/phase-map harness.
"""

from __future__ import annotations

import math
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

MASS = 0.30
MU2 = 0.001
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
RANDOM_SEEDS = 5
SIGN_ITER = 20
SIDES = [6, 8, 10, 12]
G_VALUES = [0.5, 1, 2, 5, 10, 20, 50]


def build_lattice_2d(side: int):
    n = side * side
    pos = np.zeros((n, 2), dtype=float)
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                adj[idx].append(jx * side + jy)
    return n, pos, adj, col


def build_laplacian(adj: dict[int, list[int]], n: int):
    lap = lil_matrix((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            lap[i, j] -= 1.0
            lap[j, i] -= 1.0
            lap[i, i] += 1.0
            lap[j, j] += 1.0
    return lap.tocsr()


def build_hamiltonian(
    pos: np.ndarray,
    col: np.ndarray,
    adj: dict[int, list[int]],
    n: int,
    phi: np.ndarray,
) -> sparse.csc_matrix:
    h = lil_matrix((n, n), dtype=complex)
    parity = np.where(col == 0, 1.0, -1.0)
    h.setdiag((MASS + phi) * parity)
    side = int(round(np.max(pos[:, 0]) + 1))

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            dx = abs(pos[j, 0] - pos[i, 0])
            dy = abs(pos[j, 1] - pos[i, 1])
            dx = min(dx, side - dx)
            dy = min(dy, side - dy)
            d = math.hypot(dx, dy)
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            h[i, j] += -0.5j * w
            h[j, i] += 0.5j * w
    return h.tocsc()


def cn_step(psi: np.ndarray, h: sparse.csc_matrix, dt: float) -> np.ndarray:
    n = h.shape[0]
    ap = (speye(n, format="csc") + 1j * h * dt / 2).tocsc()
    am = speye(n, format="csr") - 1j * h * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos: np.ndarray, n: int) -> np.ndarray:
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    dist = np.full(n, -1, dtype=int)
    dist[center] = 0
    queue = deque([center])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if dist[v] <= radius:
                    queue.append(v)
    a_set = set(i for i in range(n) if 0 <= dist[i] <= radius)
    a_nodes = sorted(a_set)
    boundary_edges = sum(1 for i in a_nodes for j in adj[i] if j not in a_set)
    return a_nodes, boundary_edges


def bfs_depth(adj: dict[int, list[int]], src: int, n: int):
    depth = np.full(n, np.inf)
    depth[src] = 0
    queue = deque([src])
    while queue:
        i = queue.popleft()
        for j in adj[i]:
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                queue.append(j)
    return depth


def evolve_self_gravity(pos, col, adj, n, g_value, n_steps=N_STEPS):
    psi = make_gaussian(pos, n)
    lap = build_laplacian(adj, n)
    solve_op = (lap + MU2 * speye(n, format="csr")).tocsc()

    phi = np.zeros(n, dtype=float)
    h = None
    for _ in range(n_steps):
        rho = np.abs(psi) ** 2
        phi = spsolve(solve_op, g_value * rho)
        h = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, h, DT)
        psi /= np.linalg.norm(psi)
    return psi, h, phi


def dirac_sea_correlation_matrix(h: sparse.csc_matrix) -> np.ndarray:
    dense = h.toarray()
    dense = 0.5 * (dense + dense.conj().T)
    evals, evecs = np.linalg.eigh(dense)
    filled = evals < 0
    n_filled = int(np.sum(filled))
    if n_filled == 0:
        n_filled = len(evals) // 2
        filled = np.zeros(len(evals), dtype=bool)
        filled[:n_filled] = True
    v = evecs[:, filled]
    return v @ v.conj().T


def entanglement_entropy_from_c(cmat: np.ndarray, a_nodes: list[int]) -> float:
    if not a_nodes:
        return 0.0
    c_a = cmat[np.ix_(a_nodes, a_nodes)]
    c_a = 0.5 * (c_a + c_a.conj().T)
    nu = np.linalg.eigvalsh(c_a).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    return float(-np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu)))


def measure_boundary_law(h: sparse.csc_matrix, adj, n: int, side: int):
    cmat = dirac_sea_correlation_matrix(h)
    center = (side // 2) * side + (side // 2)
    max_r = side // 2 - 1
    bnds = []
    entropies = []
    for radius in range(1, max_r + 1):
        a_nodes, bnd_edges = bfs_ball(adj, center, radius, n)
        if not a_nodes or len(a_nodes) >= n:
            continue
        bnds.append(bnd_edges)
        entropies.append(entanglement_entropy_from_c(cmat, a_nodes))
    if len(bnds) < 2:
        return 0.0, 0.0
    res = linregress(np.asarray(bnds, dtype=float), np.asarray(entropies, dtype=float))
    return float(res.slope), float(res.rvalue**2)


def shell_force_toward(depth: np.ndarray, n: int, psi: np.ndarray, phi: np.ndarray) -> bool:
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return False

    rho = np.abs(psi) ** 2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1, dtype=float)
    shell_count = np.zeros(max_d + 1, dtype=float)
    shell_prob = np.zeros(max_d + 1, dtype=float)

    for i in range(n):
        if not np.isfinite(depth[i]):
            continue
        d = int(depth[i])
        shell_phi[d] += phi[i]
        shell_prob[d] += rho_n[i]
        shell_count[d] += 1.0
    mask = shell_count > 0
    shell_phi[mask] /= shell_count[mask]

    grad = np.zeros(max_d + 1, dtype=float)
    for d in range(max_d + 1):
        if d == 0:
            grad[d] = shell_phi[0] - shell_phi[min(1, max_d)]
        elif d == max_d:
            grad[d] = shell_phi[d - 1] - shell_phi[d]
        else:
            grad[d] = 0.5 * (shell_phi[d - 1] - shell_phi[d + 1])
    return float(np.sum(shell_prob * grad)) > 0.0


def measure_sign_margin(pos, col, adj, n: int, side: int, phi_static, g_sign: float, n_iter: int):
    center_idx = (side // 2) * side + (side // 2)
    depth = bfs_depth(adj, center_idx, n)
    lap = build_laplacian(adj, n)
    solve_op = (lap + MU2 * speye(n, format="csr")).tocsc()

    margins = {}
    for label, sign in [("attract", +1.0), ("repulse", -1.0)]:
        psi = make_gaussian(pos, n)
        toward_count = 0
        for _ in range(n_iter):
            rho = np.abs(psi) ** 2
            if phi_static is None:
                phi = sign * spsolve(solve_op, g_sign * rho)
            else:
                phi = sign * phi_static
            if shell_force_toward(depth, n, psi, phi):
                toward_count += 1
            h = build_hamiltonian(pos, col, adj, n, phi)
            psi = cn_step(psi, h, DT)
            psi /= np.linalg.norm(psi)
        margins[label] = toward_count
    return margins["attract"] - margins["repulse"]


def sigma_away(target: float, controls: np.ndarray) -> float:
    std = float(np.std(controls))
    if std < 1e-12:
        return float("inf") if abs(target - float(np.mean(controls))) > 1e-12 else 0.0
    return abs(target - float(np.mean(controls))) / std


def run_phase_map():
    print("=" * 78)
    print("UNSCREENED ANDERSON-vs-GRAVITY PHASE MAP ON CORRECTED PERIODIC 2D SURFACE")
    print("=" * 78)
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"Sides: {SIDES}")
    print(f"G values: {G_VALUES}")
    print(f"Random seeds per row: {RANDOM_SEEDS}")
    print()
    header = (
        f"{'L':>3s}  {'G':>5s}  {'alpha_g':>11s}  {'alpha_r':>11s}  {'d_alpha':>11s}  {'sigma_a':>8s}  "
        f"{'sign_g':>7s}  {'sign_r':>7s}  {'sigma_s':>8s}  {'real?':>6s}"
    )
    print(header)
    print("-" * len(header))

    rows = []
    for side in SIDES:
        n, pos, adj, col = build_lattice_2d(side)
        for g_value in G_VALUES:
            g_sign = g_value / 5.0
            _, h_grav, phi_grav = evolve_self_gravity(pos, col, adj, n, g_value)
            alpha_grav, r2_grav = measure_boundary_law(h_grav, adj, n, side)
            sign_grav = measure_sign_margin(pos, col, adj, n, side, None, g_sign, SIGN_ITER)

            phi_mean = float(np.mean(phi_grav))
            phi_std = max(float(np.std(phi_grav)), 1e-10)
            alpha_rand = []
            sign_rand = []
            for seed in range(RANDOM_SEEDS):
                rng = np.random.RandomState(200 + seed)
                phi_random = rng.normal(phi_mean, phi_std, n)
                h_rand = build_hamiltonian(pos, col, adj, n, phi_random)
                alpha_r, _ = measure_boundary_law(h_rand, adj, n, side)
                sign_r = measure_sign_margin(pos, col, adj, n, side, phi_random, g_sign, SIGN_ITER)
                alpha_rand.append(alpha_r)
                sign_rand.append(sign_r)

            alpha_rand_arr = np.asarray(alpha_rand, dtype=float)
            sign_rand_arr = np.asarray(sign_rand, dtype=float)
            sigma_alpha = sigma_away(alpha_grav, alpha_rand_arr)
            sigma_sign = sigma_away(float(sign_grav), sign_rand_arr)
            is_real = sigma_alpha > 3.0 or sigma_sign > 3.0

            row = {
                "side": side,
                "G": g_value,
                "alpha_grav": alpha_grav,
                "r2_grav": r2_grav,
                "alpha_rand_mean": float(np.mean(alpha_rand_arr)),
                "alpha_rand_std": float(np.std(alpha_rand_arr)),
                "delta_alpha": alpha_grav - float(np.mean(alpha_rand_arr)),
                "sigma_alpha": sigma_alpha,
                "sign_grav": int(sign_grav),
                "sign_rand_mean": float(np.mean(sign_rand_arr)),
                "sign_rand_std": float(np.std(sign_rand_arr)),
                "sigma_sign": sigma_sign,
                "is_real": is_real,
            }
            rows.append(row)
            marker = "YES" if is_real else "no"
            print(
                f"{side:3d}  {g_value:5.1f}  {alpha_grav:11.4e}  {row['alpha_rand_mean']:11.4e}  "
                f"{row['delta_alpha']:11.4e}  {sigma_alpha:8.1f}  {sign_grav:+7d}  {row['sign_rand_mean']:+7.1f}  "
                f"{sigma_sign:8.1f}  {marker:>6s}"
            )

    print()
    print("Cross-size window (L=10,12, sigma_alpha > 3):")
    cross = [row for row in rows if row["side"] in (10, 12) and row["sigma_alpha"] > 3.0]
    by_g = {}
    for row in cross:
        by_g.setdefault(row["G"], set()).add(row["side"])
    for g_value in sorted(by_g):
        if by_g[g_value] == {10, 12}:
            print(f"  G={g_value:g}")

    print()
    peak = max(rows, key=lambda row: row["sigma_alpha"])
    print(
        "Peak boundary-law separation: "
        f"L={peak['side']}, G={peak['G']}, sigma_alpha={peak['sigma_alpha']:.1f}, "
        f"alpha_grav={peak['alpha_grav']:.4f}, alpha_rand_mean={peak['alpha_rand_mean']:.4f}"
    )

    grav_sign_positive = sum(1 for row in rows if row["sign_grav"] > 0)
    rand_sign_positive = sum(1 for row in rows if row["sign_rand_mean"] > 0)
    print(
        "Sign-margin summary: "
        f"gravity positive in {grav_sign_positive}/{len(rows)} rows; "
        f"random-control mean positive in {rand_sign_positive}/{len(rows)} rows"
    )
    return rows


def main():
    run_phase_map()


if __name__ == "__main__":
    main()
