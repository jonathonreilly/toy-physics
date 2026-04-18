#!/usr/bin/env python3
"""
Retained staggered branch-superposition harness.

This is a fixed-adjacency staggered-fermion experiment with two classical
branches:
  A: flat branch, phi = 0
  B: curved branch, phi = (L + mu^2)^-1 rho_ext

We evolve the same initial wavepacket on both branches, then compare:
  - detector distinguishability TV(A,B)
  - detector phase shift dphi(A,B)
  - coherent-vs-mixture detector TVq
  - global branch overlap

This is a real staggered-fermion branch-superposition test. It is not yet a
graph-topology superposition test because the adjacency is fixed.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from periodic_geometry import infer_periodic_extents, minimum_image_distance

MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30


def make_lattice_1d(n: int):
    pos = np.array([(float(x), 0.0) for x in range(n)])
    color = np.array([x % 2 for x in range(n)], dtype=int)
    adj = {x: [(x + 1) % n, (x - 1) % n] for x in range(n)}
    source = n // 4
    detector = np.where(pos[:, 0] >= 0.75 * (n - 1))[0]
    return pos, color, adj, source, detector


def make_lattice_2d(side: int):
    coords = []
    colors = []
    adj = {}
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((float(x), float(y)))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    color = np.array(colors, dtype=int)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            adj[a] = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                adj[a].append(index[((x + dx) % side, (y + dy) % side)])
    source = index[(side // 4, side // 2)]
    detector = np.array([index[(x, y)] for x in range((3 * side) // 4, side) for y in range(side)])
    return pos, color, adj, source, detector


def build_laplacian(pos: np.ndarray, adj: dict[int, list[int]]):
    n = len(pos)
    lap = lil_matrix((n, n), dtype=float)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            lap[i, j] -= w
            lap[j, i] -= w
            lap[i, i] += w
            lap[j, j] += w
    return lap.tocsr()


def build_hamiltonian(pos: np.ndarray, color: np.ndarray, adj: dict[int, list[int]], phi: np.ndarray):
    n = len(pos)
    ham = lil_matrix((n, n), dtype=complex)
    parity = np.where(color == 0, 1.0, -1.0)
    ham.setdiag((MASS + phi) * parity)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            ham[i, j] += -0.5j * w
            ham[j, i] += 0.5j * w
    return ham.tocsr()


def cn_step(ham, psi: np.ndarray):
    n = ham.shape[0]
    ap = (speye(n, format="csc") + 1j * ham * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * ham * DT / 2
    return spsolve(ap, am.dot(psi))


def gaussian_packet(pos: np.ndarray, sigma: float):
    center = np.mean(pos, axis=0)
    rsq = np.sum((pos - center) ** 2, axis=1)
    psi = np.exp(-0.5 * rsq / sigma**2).astype(complex)
    return psi / np.linalg.norm(psi)


def mean_phase_difference(a: np.ndarray, b: np.ndarray):
    mask = (np.abs(a) > 1e-10) & (np.abs(b) > 1e-10)
    if not np.any(mask):
        return 0.0
    phase = np.angle(a[mask] * np.conj(b[mask]))
    return float(np.mean(np.abs(np.unwrap(phase))))


def detector_distribution(psi: np.ndarray, det: np.ndarray):
    rho = np.abs(psi[det]) ** 2
    total = float(np.sum(rho))
    if total <= 1e-20:
        return rho, total
    return rho / total, total


def run_case(dim: int, size: int, g: float):
    if dim == 1:
        pos, color, adj, source, det = make_lattice_1d(size)
        sigma = 1.5
        label = f"1D n={size}"
    else:
        pos, color, adj, source, det = make_lattice_2d(size)
        sigma = 1.5
        label = f"2D side={size}"

    n = len(pos)
    lap = build_laplacian(pos, adj)
    rho_ext = np.zeros(n)
    rho_ext[source] = g
    phi_branch = spsolve((lap + MU2 * speye(n, format="csr")).tocsc(), rho_ext)

    psi0 = gaussian_packet(pos, sigma)

    ham_a = build_hamiltonian(pos, color, adj, np.zeros(n))
    ham_b = build_hamiltonian(pos, color, adj, phi_branch)
    psi_a = psi0.copy()
    psi_b = psi0.copy()
    for _ in range(N_STEPS):
        psi_a = cn_step(ham_a, psi_a)
        psi_b = cn_step(ham_b, psi_b)

    pa, pdet_a = detector_distribution(psi_a, det)
    pb, pdet_b = detector_distribution(psi_b, det)
    tv = 0.5 * float(np.sum(np.abs(pa - pb)))
    dphi = mean_phase_difference(psi_a[det], psi_b[det])

    psi_q = psi_a + psi_b
    psi_q /= np.linalg.norm(psi_q)
    rho_mix = 0.5 * (np.abs(psi_a) ** 2 + np.abs(psi_b) ** 2)
    pq, pdet_q = detector_distribution(psi_q, det)
    pm, pdet_m = detector_distribution(np.sqrt(rho_mix), det)
    tvq = 0.5 * float(np.sum(np.abs(pq - pm)))
    overlap = float(np.abs(np.vdot(psi_a, psi_b)) ** 2)

    return {
        "label": label,
        "G": g,
        "TV": tv,
        "dphi": dphi,
        "TVq": tvq,
        "overlap": overlap,
        "Pdet_A": pdet_a,
        "Pdet_B": pdet_b,
        "Pdet_Q": pdet_q,
        "Pdet_M": pdet_m,
    }


def verdict(res: dict[str, float]):
    bounded_positive = (
        res["TV"] > 0.10
        and res["dphi"] > 0.10
        and res["TVq"] > 0.01
        and res["overlap"] < 0.8
    )
    return "BOUNDED_POSITIVE" if bounded_positive else "WEAK_OR_NULL"


def main():
    t0 = time.time()
    cases = [
        (1, 41, 10.0),
        (1, 61, 10.0),
        (2, 8, 10.0),
        (2, 10, 10.0),
        (2, 12, 10.0),
    ]

    print("=" * 78)
    print("RETAINED STAGGERED BRANCH-SUPERPOSITION HARNESS")
    print("=" * 78)
    print("Fixed adjacency. Flat branch vs screened-field branch.")
    print()
    print(
        f"{'case':<14s} {'G':>5s} {'TV':>8s} {'dphi':>8s} {'TVq':>8s} "
        f"{'overlap':>8s} {'PdetA':>8s} {'PdetB':>8s} {'verdict':>18s}"
    )
    print("-" * 96)

    for dim, size, g in cases:
        res = run_case(dim, size, g)
        print(
            f"{res['label']:<14s} {g:5.1f} {res['TV']:8.4f} {res['dphi']:8.4f} "
            f"{res['TVq']:8.4f} {res['overlap']:8.4f} {res['Pdet_A']:8.4f} "
            f"{res['Pdet_B']:8.4f} {verdict(res):>18s}"
        )

    print()
    print("Interpretation:")
    print("  TV    = detector distinguishability between flat and curved branches")
    print("  dphi  = detector phase shift between branches")
    print("  TVq   = coherent superposition vs classical mixture at detector")
    print("  overlap < 1 means globally distinguishable branches")
    print(f"Time: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
