#!/usr/bin/env python3
"""
Two-orbital mutual attraction under shared self-consistent gravity.

This is the cleaner follow-up to frontier_two_body_mutual_attraction.py.
Instead of one wavefunction with two lobes, evolve two separate orbitals
under a shared self-consistent scalar field:

  rho_total = |psi_A|^2 + |psi_B|^2
  Phi = (L + mu^2 I)^(-1) G rho_total
  H(Phi) acts on both orbitals

The key control is "self-only", where each orbital evolves only under the
field sourced by its own density. Any extra approach in the shared-field
run is the mutual channel.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# Physical parameters
MASS = 0.30
MU2 = 0.22
DT = 0.12
SIGMA = 1.2
SIDE = 24
N_STEPS = 80
G_VALUES = [5, 10, 20, 40, 80]


def build_open_lattice(side: int):
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    for x in range(side):
        for y in range(side):
            idx = x * side + y
            pos[idx] = (x, y)
            col[idx] = (x + y) % 2
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                jx, jy = x + dx, y + dy
                if 0 <= jx < side and 0 <= jy < side:
                    adj[idx].append(jx * side + jy)

    return n, pos, adj, col


def build_laplacian(adj: dict[int, list[int]], n: int):
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            L[i, j] -= 1.0
            L[j, i] -= 1.0
            L[i, i] += 1.0
            L[j, j] += 1.0
    return L.tocsr()


def build_hamiltonian(pos, col, adj, n, phi):
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w
    return H.tocsc()


def cn_step(psi, H, n):
    ap = (speye(n, format="csc") + 1j * H * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def solve_phi(L, n: int, rho: np.ndarray, G: float):
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + MU2 * speye(n, format="csr")).tocsc()
    return spsolve(A, G * rho)


def gaussian(pos, cx: float, cy: float, sigma: float):
    rsq = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-0.5 * rsq / sigma**2).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def centroid_x(psi: np.ndarray, pos: np.ndarray):
    rho = np.abs(psi) ** 2
    rho /= max(np.sum(rho), 1e-30)
    return float(np.sum(rho * pos[:, 0]))


def evolve_free(pos, col, adj, n, psi_a0, psi_b0, n_steps):
    phi = np.zeros(n)
    H = build_hamiltonian(pos, col, adj, n, phi)
    psi_a = psi_a0.copy()
    psi_b = psi_b0.copy()
    seps = []
    for _ in range(n_steps):
        psi_a = cn_step(psi_a, H, n)
        psi_b = cn_step(psi_b, H, n)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        seps.append(centroid_x(psi_b, pos) - centroid_x(psi_a, pos))
    return np.asarray(seps)


def evolve_self_only(pos, col, adj, n, L, psi_a0, psi_b0, G, n_steps):
    psi_a = psi_a0.copy()
    psi_b = psi_b0.copy()
    seps = []
    for _ in range(n_steps):
        phi_a = solve_phi(L, n, np.abs(psi_a) ** 2, G)
        phi_b = solve_phi(L, n, np.abs(psi_b) ** 2, G)
        H_a = build_hamiltonian(pos, col, adj, n, phi_a)
        H_b = build_hamiltonian(pos, col, adj, n, phi_b)
        psi_a = cn_step(psi_a, H_a, n)
        psi_b = cn_step(psi_b, H_b, n)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        seps.append(centroid_x(psi_b, pos) - centroid_x(psi_a, pos))
    return np.asarray(seps)


def evolve_shared_self_consistent(pos, col, adj, n, L, psi_a0, psi_b0, G, n_steps):
    psi_a = psi_a0.copy()
    psi_b = psi_b0.copy()
    seps = []
    for _ in range(n_steps):
        rho = np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2
        phi = solve_phi(L, n, rho, G)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi_a = cn_step(psi_a, H, n)
        psi_b = cn_step(psi_b, H, n)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        seps.append(centroid_x(psi_b, pos) - centroid_x(psi_a, pos))
    return np.asarray(seps)


def evolve_frozen_shared(pos, col, adj, n, L, psi_a0, psi_b0, G, n_steps):
    rho0 = np.abs(psi_a0) ** 2 + np.abs(psi_b0) ** 2
    phi = solve_phi(L, n, rho0, G)
    H = build_hamiltonian(pos, col, adj, n, phi)
    psi_a = psi_a0.copy()
    psi_b = psi_b0.copy()
    seps = []
    for _ in range(n_steps):
        psi_a = cn_step(psi_a, H, n)
        psi_b = cn_step(psi_b, H, n)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)
        seps.append(centroid_x(psi_b, pos) - centroid_x(psi_a, pos))
    return np.asarray(seps)


def run_one(G: float):
    n, pos, adj, col = build_open_lattice(SIDE)
    L = build_laplacian(adj, n)

    y0 = SIDE / 2
    psi_a0 = gaussian(pos, 7.0, y0, SIGMA)
    psi_b0 = gaussian(pos, 17.0, y0, SIGMA)
    init_sep = centroid_x(psi_b0, pos) - centroid_x(psi_a0, pos)

    free = evolve_free(pos, col, adj, n, psi_a0, psi_b0, N_STEPS)
    self_only = evolve_self_only(pos, col, adj, n, L, psi_a0, psi_b0, G, N_STEPS)
    frozen = evolve_frozen_shared(pos, col, adj, n, L, psi_a0, psi_b0, G, N_STEPS)
    shared = evolve_shared_self_consistent(pos, col, adj, n, L, psi_a0, psi_b0, G, N_STEPS)

    return {
        "G": G,
        "init_sep": init_sep,
        "free": free,
        "self_only": self_only,
        "frozen": frozen,
        "shared": shared,
    }


def summarize(label: str, seps: np.ndarray):
    delta = float(seps[-1] - seps[0])
    monotone_frac = float(np.mean(np.diff(seps) <= 0)) if len(seps) > 1 else 0.0
    return label, delta, monotone_frac, float(seps[-1])


def main():
    t0 = time.time()
    print("=" * 78)
    print("TWO-ORBITAL MUTUAL ATTRACTION VIA SHARED SELF-CONSISTENT GRAVITY")
    print("=" * 78)
    print(f"Lattice: {SIDE}x{SIDE} open staggered ({SIDE*SIDE} nodes)")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}, SIGMA={SIGMA}, N_STEPS={N_STEPS}")
    print()

    rows = []
    for G in G_VALUES:
        res = run_one(G)
        print("-" * 78)
        print(f"G = {G}")
        print(f"Initial separation: {res['init_sep']:.4f}")
        print()
        print(f"{'Mode':<14s} {'Delta sep':>12s} {'Mono frac':>10s} {'Final sep':>12s}")
        print("-" * 52)
        for label, data in [
            ("FREE", res["free"]),
            ("SELF_ONLY", res["self_only"]),
            ("FROZEN", res["frozen"]),
            ("SHARED", res["shared"]),
        ]:
            row = summarize(label, data)
            rows.append((G,) + row[1:])
            print(f"{label:<14s} {row[1]:>+12.6f} {row[2]:>10.3f} {row[3]:>12.4f}")

        mutual_delta = float(res["shared"][-1] - res["self_only"][-1])
        print()
        print(f"Mutual channel (shared - self_only, final separation): {mutual_delta:+.6f}")
        if mutual_delta < -1e-2:
            print("  -> shared field pulls the packets closer than self-only evolution")
        elif mutual_delta > 1e-2:
            print("  -> shared field leaves the packets farther apart than self-only evolution")
        else:
            print("  -> no material separation from self-only evolution")
        print()

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for G in G_VALUES:
        sub = [r for r in rows if r[0] == G]
        shared = [r for r in sub if abs(r[1] - (next(x for x in sub if x[1] == x[1])[1])) < 1e9]
        _ = shared
    print("Compare SHARED against SELF_ONLY first; that is the clean mutual-attraction control.")
    print(f"Total time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
