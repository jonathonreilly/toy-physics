#!/usr/bin/env python3
"""
Anderson Multifractal Analysis of Self-Gravity Localization
===========================================================

Test whether the self-gravity localization transition (beta~0.19 for random
geometric graphs) belongs to the Anderson localization universality class by
computing multifractal dimensions D_q.

At the Anderson transition, wavefunctions are multifractal:
  IPR_q = sum_i |psi_i|^{2q} ~ N^{-tau_q}
  tau_q = D_q * (q-1)

Classification:
  - Extended (weak G):   D_q ~ d (spatial dimension) for all q
  - Localized (strong G): D_q ~ 0 for all q
  - Critical (G ~ G_c):  0 < D_q < d with non-trivial q-dependence
    (anomalous multifractality: D_q decreases with q)

Protocol:
  For each G, sweep graph sizes (side=6,8,10,12), compute IPR_q,
  fit tau_q from size scaling, extract D_q = tau_q/(q-1).
"""

from __future__ import annotations

import math
import random
import time
from collections import deque

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# ── Physics constants ──────────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_ITER = 30

# ── Sweep parameters ──────────────────────────────────────────────────
G_VALUES = [1, 2, 5, 10, 20, 50]
SIDES = [6, 8, 10, 12]
Q_VALUES = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
N_SEEDS = 3  # disorder averaging


# ── Graph construction ─────────────────────────────────────────────────
def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _finalize_adj(adj_sets: dict[int, set[int]]) -> dict[int, list[int]]:
    return {i: sorted(list(nbs)) for i, nbs in adj_sets.items()}


def make_random_geometric(seed: int, side: int):
    rng = random.Random(seed)
    coords: list[tuple[float, float]] = []
    colors: list[int] = []
    index: dict[tuple[int, int], int] = {}
    adj: dict[int, set[int]] = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08 * (rng.random() - 0.5),
                           y + 0.08 * (rng.random() - 0.5)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords, dtype=float)
    col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            for di, dj in ((1, 0), (0, 1), (1, 1), (1, -1)):
                ii, jj = i + di, j + dj
                if (ii, jj) not in index:
                    continue
                b = index[(ii, jj)]
                if col[a] == col[b]:
                    continue
                if math.hypot(pos[b, 0] - pos[a, 0], pos[b, 1] - pos[a, 1]) <= 1.28:
                    _add_edge(adj, a, b)
    return pos, col, _finalize_adj(adj)


# ── Physics operators ──────────────────────────────────────────────────
def laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def solve_phi(lap, rho):
    if np.allclose(rho, 0.0):
        return np.zeros_like(rho)
    A = (lap + MU2 * speye(lap.shape[0], format="csr")).tocsc()
    return spsolve(A, rho).astype(float)


def build_hamiltonian(pos, colors, adj, n, phi):
    H = lil_matrix((n, n), dtype=complex)
    parity = np.where(colors == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * parity)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def cn_step(H, psi, n):
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def gauss_state(pos, n, sigma=1.15):
    center = np.mean(pos, axis=0)
    rel = pos - center
    psi = np.exp(-0.5 * np.sum(rel**2, axis=1) / sigma**2).astype(complex)
    norm = np.linalg.norm(psi)
    return psi / norm if norm > 0 else psi


# ── Self-gravity evolution ─────────────────────────────────────────────
def evolve_self_gravity(pos, col, adj, n, G, n_iter=N_ITER):
    lap = laplacian(pos, adj, n)
    psi = gauss_state(pos, n)
    for _ in range(n_iter):
        rho = np.abs(psi)**2
        phi = solve_phi(lap, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(H, psi, n)
    return psi


# ── Multifractal analysis ─────────────────────────────────────────────
def compute_ipr(psi, q_values):
    """Compute IPR_q = sum_i rho_i^q for each q."""
    rho = np.abs(psi)**2
    rho /= np.sum(rho)  # normalize to probability
    result = {}
    for q in q_values:
        if q == 1.0:
            # IPR_1 = 1 always; use Shannon entropy instead
            # S = -sum rho * log(rho) ~ tau_1 * log(N)
            mask = rho > 0
            result[q] = float(-np.sum(rho[mask] * np.log(rho[mask])))
        else:
            result[q] = float(np.sum(rho**q))
    return result


def fit_tau_q(ipr_by_size, q_values):
    """
    Fit tau_q from IPR_q ~ N^{-tau_q} across sizes.
    For q=1, use Shannon entropy S ~ tau_1 * ln(N).
    Returns dict q -> tau_q.
    """
    sizes = sorted(ipr_by_size.keys())
    if len(sizes) < 2:
        return {q: 0.0 for q in q_values}

    log_n = np.log(np.array(sizes, dtype=float))
    tau = {}

    for q in q_values:
        if q == 1.0:
            # S = -sum rho*log(rho) ~ D_1 * ln(N) => tau_1 = D_1
            entropies = np.array([ipr_by_size[n][q] for n in sizes])
            # Fit S = D_1 * ln(N) + const
            A = np.vstack([log_n, np.ones_like(log_n)]).T
            result = np.linalg.lstsq(A, entropies, rcond=None)
            tau[q] = float(result[0][0])  # D_1 directly (tau_1 = D_1 * 0 doesn't work)
        else:
            log_ipr = np.log(np.array([ipr_by_size[n][q] for n in sizes]))
            # log(IPR_q) = -tau_q * log(N) + const
            A = np.vstack([log_n, np.ones_like(log_n)]).T
            result = np.linalg.lstsq(A, log_ipr, rcond=None)
            tau[q] = float(-result[0][0])  # negative slope = tau_q

    return tau


def tau_to_dq(tau, q_values):
    """Convert tau_q to D_q = tau_q / (q-1). For q=1, tau already is D_1."""
    dq = {}
    for q in q_values:
        if q == 1.0:
            dq[q] = tau[q]  # already D_1 from entropy fit
        else:
            dq[q] = tau[q] / (q - 1.0)
    return dq


# ── Main ───────────────────────────────────────────────────────────────
def main():
    t0 = time.time()
    print("=" * 76)
    print("ANDERSON MULTIFRACTAL ANALYSIS OF SELF-GRAVITY LOCALIZATION")
    print("=" * 76)
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, N_ITER={N_ITER}")
    print(f"G values: {G_VALUES}")
    print(f"Sides: {SIDES} => N = {[s*s for s in SIDES]}")
    print(f"q values: {Q_VALUES}")
    print(f"Seeds per (G, side): {N_SEEDS}")
    print()

    # Storage: dq_results[G] = {q: D_q}
    dq_results: dict[int, dict[float, float]] = {}
    tau_results: dict[int, dict[float, float]] = {}

    for G in G_VALUES:
        print(f"--- G = {G} ---")

        # ipr_by_size[N] = {q: mean_IPR_q} averaged over seeds
        ipr_by_size: dict[int, dict[float, float]] = {}

        for side in SIDES:
            n = side * side
            ipr_accum = {q: [] for q in Q_VALUES}

            for seed_offset in range(N_SEEDS):
                seed = 42 + side * 100 + seed_offset
                pos, col, adj = make_random_geometric(seed, side)
                actual_n = pos.shape[0]

                psi = evolve_self_gravity(pos, col, adj, actual_n, float(G))
                ipr = compute_ipr(psi, Q_VALUES)

                for q in Q_VALUES:
                    ipr_accum[q].append(ipr[q])

            ipr_mean = {q: float(np.mean(ipr_accum[q])) for q in Q_VALUES}
            ipr_by_size[n] = ipr_mean

            # Print IPR_2 for monitoring
            print(f"  side={side:2d} N={n:3d}  IPR_2={ipr_mean[2.0]:.6f}  "
                  f"IPR_3={ipr_mean[3.0]:.6f}  S={ipr_mean[1.0]:.4f}")

        # Fit tau_q from size scaling
        tau = fit_tau_q(ipr_by_size, Q_VALUES)
        dq = tau_to_dq(tau, Q_VALUES)

        tau_results[G] = tau
        dq_results[G] = dq

        dq_str = "  ".join(f"D_{q:.1f}={dq[q]:+.3f}" for q in Q_VALUES)
        print(f"  => {dq_str}")
        print()

    # ── Summary table ──────────────────────────────────────────────────
    print("=" * 76)
    print("D_q SPECTRUM AT EACH G")
    print("=" * 76)
    header = f"{'G':>4s}" + "".join(f"  D_{q:.1f}:>7s" if False else f"  D_{q:.1f}" for q in Q_VALUES)
    # Build proper header
    cols = ["  G"]
    for q in Q_VALUES:
        cols.append(f"D_{q:.1f}")
    print(f"{'G':>4s}  " + "  ".join(f"{'D_'+str(q):>7s}" for q in Q_VALUES))
    print("-" * 76)
    for G in G_VALUES:
        dq = dq_results[G]
        vals = "  ".join(f"{dq[q]:+7.3f}" for q in Q_VALUES)
        print(f"{G:4d}  {vals}")

    # ── D_2 vs G curve ─────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("D_2 vs G (LOCALIZATION CROSSOVER)")
    print("=" * 76)
    print(f"{'G':>4s}  {'D_2':>7s}  {'D_2/(d=2)':>9s}  {'Classification':>16s}")
    print("-" * 50)
    for G in G_VALUES:
        d2 = dq_results[G][2.0]
        ratio = d2 / 2.0  # fraction of full dimension d=2
        if ratio > 0.7:
            cls = "EXTENDED"
        elif ratio < 0.15:
            cls = "LOCALIZED"
        else:
            cls = "CRITICAL"
        print(f"{G:4d}  {d2:+7.3f}  {ratio:9.3f}  {cls:>16s}")

    # ── Anderson signature check ───────────────────────────────────────
    print()
    print("=" * 76)
    print("ANDERSON MULTIFRACTALITY SIGNATURE")
    print("=" * 76)
    print("At Anderson transition, D_q should DECREASE with q (anomalous multifractality).")
    print()

    for G in G_VALUES:
        dq = dq_results[G]
        dq_vals = [dq[q] for q in Q_VALUES if q != 1.0]
        q_nontrivial = [q for q in Q_VALUES if q != 1.0]

        # Check monotonic decrease
        decreasing = all(dq_vals[i] >= dq_vals[i+1] for i in range(len(dq_vals)-1))
        spread = max(dq_vals) - min(dq_vals)
        mean_d = np.mean(dq_vals)

        if mean_d > 1.4:
            status = "extended (no multifractality)"
        elif mean_d < 0.3:
            status = "localized (trivial)"
        elif decreasing and spread > 0.1:
            status = "ANDERSON MULTIFRACTAL"
        elif spread < 0.1:
            status = "near-uniform D_q (weak multifractality)"
        else:
            status = "non-monotonic (atypical)"

        print(f"G={G:3d}: D_q range=[{min(dq_vals):+.3f}, {max(dq_vals):+.3f}]  "
              f"spread={spread:.3f}  monotonic={decreasing}  => {status}")

    # ── tau_q spectrum (for completeness) ──────────────────────────────
    print()
    print("=" * 76)
    print("tau_q SPECTRUM (MASS EXPONENTS)")
    print("=" * 76)
    print(f"{'G':>4s}  " + "  ".join(f"{'t_'+str(q):>7s}" for q in Q_VALUES))
    print("-" * 76)
    for G in G_VALUES:
        tau = tau_results[G]
        vals = "  ".join(f"{tau[q]:+7.3f}" for q in Q_VALUES)
        print(f"{G:4d}  {vals}")

    # ── Final verdict ──────────────────────────────────────────────────
    print()
    print("=" * 76)
    print("VERDICT")
    print("=" * 76)

    # Find the G closest to critical (D_2 ~ 0.5-1.5 for d=2)
    critical_candidates = []
    for G in G_VALUES:
        d2 = dq_results[G][2.0]
        if 0.2 < d2 < 1.8:
            critical_candidates.append((G, d2))

    if critical_candidates:
        best_G, best_d2 = min(critical_candidates, key=lambda x: abs(x[1] - 1.0))
        dq = dq_results[best_G]
        dq_vals = [dq[q] for q in Q_VALUES if q != 1.0]
        decreasing = all(dq_vals[i] >= dq_vals[i+1] for i in range(len(dq_vals)-1))
        spread = max(dq_vals) - min(dq_vals)

        print(f"Best critical candidate: G={best_G} with D_2={best_d2:.3f}")
        print(f"  D_q spectrum: {', '.join(f'D_{q:.1f}={dq[q]:.3f}' for q in Q_VALUES)}")
        print(f"  Monotonically decreasing: {decreasing}")
        print(f"  D_q spread: {spread:.3f}")
        print()
        if decreasing and spread > 0.1 and 0.3 < best_d2 < 1.7:
            print("CONCLUSION: Self-gravity localization transition shows Anderson-class")
            print("multifractality. The D_q spectrum is non-trivial and monotonically")
            print(f"decreasing, consistent with a critical point at G~{best_G}.")
            print(f"Critical D_2 = {best_d2:.3f} on 2D staggered lattice (new prediction).")
        elif spread < 0.1:
            print("CONCLUSION: D_q spectrum is nearly flat -- weak or no multifractality.")
            print("The transition may not be in the Anderson universality class.")
        else:
            print("CONCLUSION: D_q spectrum is non-monotonic or atypical.")
            print("The transition differs from standard Anderson localization.")
    else:
        print("No G value produced a clear critical regime (D_2 between 0.2 and 1.8).")
        print("The transition may be sharper than Anderson or the G range needs adjustment.")

    elapsed = time.time() - t0
    print(f"\nElapsed: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
