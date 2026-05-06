#!/usr/bin/env python3
"""Staggered + Wilson determinant-positivity bridge runner.

Companion to
`docs/STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`.

The bridge theorem proves that under the canonical-A_min conventions
asserted by the parent reflection-positivity note (M_W commutes with
the staggered chirality eps; mass = m * I; symmetric-canonical
M_W = r * d * I; balanced sublattices) the canonical staggered + Wilson
Dirac operator M = M_KS + M_W + m * I has

    det(M) = prod_{i=1..n/2} (alpha**2 + sigma_i**2)

where alpha = m + r * d and sigma_i are the singular values of the
off-diagonal staggered-hop block K of the eps-block decomposition of M.
Hence det(M) > 0 configuration-by-configuration on every SU(3) gauge
background for any m > 0.

This runner is the load-bearing assertion runner for that bridge. It
constructs the staggered + Wilson Dirac operator on small periodic 4D
SU(3) gauge backgrounds, performs the eps-block decomposition explicitly,
verifies the closed-form factorisation by comparing two independent
computations of det(M), and asserts per-configuration positivity. It does
NOT hard-code an L -> infinity value; it tests structural identities
that are exact at finite volume.

Reproducibility: deterministic seeded SU(3) link configurations.
"""

from __future__ import annotations

import math
import sys

import numpy as np


SEED = 42
PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


# ---- SU(3) generators (Gell-Mann basis) ------------------------------------
GM = np.array(
    [
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]] / np.sqrt(3),
    ],
    dtype=complex,
)


def random_su3(rng: np.random.Generator, scale: float = 1.0) -> np.ndarray:
    """Random SU(3) matrix at given scale (scale=0 -> identity, scale=1 -> generic)."""
    coeffs = rng.standard_normal(8) * scale
    H = sum(coeffs[k] * GM[k] for k in range(8)) / 2.0
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T


# ---- 4D periodic lattice with staggered Dirac operator ---------------------

def build_links(L: int, scale: float, rng: np.random.Generator) -> np.ndarray:
    """Generate a deterministic seeded SU(3) link configuration.

    `links` has shape (L, L, L, L, 4, 3, 3) with the last two axes the
    SU(3) link matrix and the second-to-last axis the direction
    (0=x, 1=y, 2=z, 3=t). Sites use even side lengths so the staggered
    chirality wraps cleanly under PBC.
    """
    assert L % 2 == 0, "lattice side must be even for balanced sublattices"
    sites = (L,) * 4
    links = np.zeros(sites + (4, 3, 3), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for t in range(L):
                    for mu in range(4):
                        links[x, y, z, t, mu] = random_su3(rng, scale)
    return links


def staggered_phase(x: int, y: int, z: int, t: int, mu: int) -> int:
    """Canonical staggered phase eta_mu(x).

    eta_0 = 1, eta_1 = (-1)^x, eta_2 = (-1)^{x+y}, eta_3 = (-1)^{x+y+z}.
    """
    if mu == 0:
        return 1
    if mu == 1:
        return (-1) ** x
    if mu == 2:
        return (-1) ** (x + y)
    if mu == 3:
        return (-1) ** (x + y + z)
    raise ValueError(f"bad direction {mu}")


def site_eps(x: int, y: int, z: int, t: int) -> int:
    """Staggered chirality eps(x) = (-1)^{x+y+z+t}."""
    return (-1) ** (x + y + z + t)


def build_M_KS(L: int, links: np.ndarray) -> np.ndarray:
    """Construct the canonical Kogut-Susskind staggered Dirac hop on an L^4 lattice.

    M_KS_{x,y} = (1/2) sum_mu eta_mu(x) [
        delta_{y, x+mu} U_mu(x) - delta_{y, x-mu} U_mu(x-mu)^dag
    ]

    The (3, 3) SU(3) colour structure is carried, so M_KS is a
    (3 N_sites) x (3 N_sites) matrix.
    """
    N = L ** 4
    dim = 3 * N

    def site_idx(x, y, z, t):
        return x + L * (y + L * (z + L * t))

    M = np.zeros((dim, dim), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for t in range(L):
                    s = site_idx(x, y, z, t)
                    for mu, dvec in enumerate(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))):
                        eta = staggered_phase(x, y, z, t, mu)
                        # forward hop: x -> x + mu
                        nx = (x + dvec[0]) % L
                        ny = (y + dvec[1]) % L
                        nz = (z + dvec[2]) % L
                        nt = (t + dvec[3]) % L
                        sn = site_idx(nx, ny, nz, nt)
                        U = links[x, y, z, t, mu]
                        M[3 * s : 3 * s + 3, 3 * sn : 3 * sn + 3] += 0.5 * eta * U
                        M[3 * sn : 3 * sn + 3, 3 * s : 3 * s + 3] += -0.5 * eta * U.conj().T
    return M


def build_M_W_diagonal(dim: int, r: float, d: int) -> np.ndarray:
    """Symmetric-canonical Wilson term: M_W = r * d * I.

    This is the eps-commuting projection of a standard Wilson term and is
    the canonical convention asserted by the parent reflection-positivity
    note (eps M_W eps = M_W). The off-diagonal NN-hop part of a standard
    Wilson Laplacian is excluded by this projection; that is the parent
    note's own asserted convention, not a narrowing introduced here.
    """
    return float(r * d) * np.eye(dim, dtype=complex)


def build_eps_diagonal(L: int) -> np.ndarray:
    """Block-diagonal eps = diag(+I, -I) ordering: +1 sublattice first."""
    plus_indices: list[int] = []
    minus_indices: list[int] = []
    for x in range(L):
        for y in range(L):
            for z in range(L):
                for t in range(L):
                    s = x + L * (y + L * (z + L * t))
                    for c in range(3):
                        idx = 3 * s + c
                        if site_eps(x, y, z, t) > 0:
                            plus_indices.append(idx)
                        else:
                            minus_indices.append(idx)
    perm = plus_indices + minus_indices
    return perm, len(plus_indices), len(minus_indices)


# ---- Bridge structural and numerical checks ---------------------------------

def run_volume(L: int, scale: float, masses: list[float], rng: np.random.Generator) -> dict:
    print()
    print(f"=== L = {L}, scale = {scale} ===")
    links = build_links(L, scale, rng)
    M_KS = build_M_KS(L, links)
    dim = M_KS.shape[0]

    # eps-block ordering
    perm, n_plus, n_minus = build_eps_diagonal(L)
    P = np.eye(dim)[:, perm]
    eps_diag = np.array([+1] * n_plus + [-1] * n_minus, dtype=float)

    # Reorder M_KS into the eps-block basis
    M_KS_blocked = P.T @ M_KS @ P

    # Verify eps-block structure of M_KS: top-left and bottom-right must vanish
    A_KS = M_KS_blocked[:n_plus, :n_plus]
    D_KS = M_KS_blocked[n_plus:, n_plus:]
    K = M_KS_blocked[:n_plus, n_plus:]
    K_lower = M_KS_blocked[n_plus:, :n_plus]
    diag_block_norm = max(np.max(np.abs(A_KS)), np.max(np.abs(D_KS)))
    K_lower_check = float(np.max(np.abs(K_lower + K.conj().T)))
    K_lower_minus_K_dag_norm = float(np.max(np.abs(K_lower - (-K.conj().T))))

    check(
        f"L={L}: M_KS has zero diagonal eps-blocks (anticommutation {{eps, M_KS}} = 0)",
        diag_block_norm < 1e-12,
        detail=f"max |diag block| = {diag_block_norm:.3e}",
    )
    check(
        f"L={L}: M_KS lower-left block equals -K^dagger (anti-Hermiticity)",
        K_lower_check < 1e-10,
        detail=f"max |K_lower + K^dag| = {K_lower_check:.3e}, alt-form |K_lower - (-K^dag)| = {K_lower_minus_K_dag_norm:.3e}",
    )

    # Compute SVD of K
    U_svd, sigmas, Vh = np.linalg.svd(K)
    sigmas = np.real(sigmas)

    results: list[dict] = []
    for m in masses:
        r = 1.0
        d = 4
        alpha = m + r * d
        # Direct det of M = M_KS + (alpha) * I (since M_W = r*d*I and mass = m*I,
        # so M_W + m*I = (r*d + m) * I = alpha * I).
        M_full = M_KS + alpha * np.eye(dim, dtype=complex)

        # Method 1: direct det in log space (slogdet returns complex sign for
        # complex matrices, but for our gamma_5-Hermitian setup the determinant
        # is real, so we expect sign.imag = 0).
        sign_direct, log_det_direct = np.linalg.slogdet(M_full)
        sign_direct_real = float(np.real(sign_direct))
        sign_direct_imag = float(np.imag(sign_direct))

        # Method 2: closed-form bridge product over singular values.
        # det(M) = prod_{i=1..n/2} (alpha^2 + sigma_i^2). Use log-sum to avoid
        # overflow. Note: sigmas has length n_plus = n/2 since balanced.
        log_det_bridge = float(np.sum(np.log(alpha ** 2 + sigmas ** 2)))
        sign_bridge = +1.0  # every factor (alpha^2 + sigma^2) > 0 for m > 0

        # Sign agreement: bridge predicts +1; direct should also be +1 (real).
        sign_match = (
            abs(sign_direct_imag) < 1e-10
            and abs(sign_direct_real - sign_bridge) < 0.5
        )
        is_positive = sign_direct_real > 0.5 and abs(sign_direct_imag) < 1e-10

        # Log-magnitude agreement
        log_diff = abs(float(log_det_direct) - log_det_bridge)
        factorisation_match = sign_match and log_diff < 1e-7

        results.append(
            {
                "L": L,
                "scale": scale,
                "m": m,
                "alpha": alpha,
                "sign_direct_real": sign_direct_real,
                "sign_direct_imag": sign_direct_imag,
                "log_det_direct": float(log_det_direct),
                "log_det_bridge": log_det_bridge,
                "log_diff": log_diff,
                "n_sigmas": len(sigmas),
                "sigma_max": float(sigmas.max()) if len(sigmas) else 0.0,
                "sigma_min": float(sigmas.min()) if len(sigmas) else 0.0,
                "is_positive": is_positive,
                "factorisation_match": factorisation_match,
            }
        )

        print(
            f"  m={m:.2f}, alpha={alpha:.2f}: log_det_direct={float(log_det_direct):+.6f}, "
            f"log_det_bridge={log_det_bridge:+.6f}, log_diff={log_diff:.2e}, "
            f"sign_real={sign_direct_real:+.3f}, sign_imag={sign_direct_imag:+.2e}"
        )

    return {
        "L": L,
        "scale": scale,
        "n_plus": n_plus,
        "n_minus": n_minus,
        "n_sigmas": len(sigmas),
        "results": results,
    }


def main() -> int:
    print("=" * 78)
    print("STAGGERED + WILSON DET-POSITIVITY BRIDGE VERIFIER")
    print("=" * 78)
    print(f"seed={SEED}")
    print(f"convention: M_W = r * d * I (eps-commuting); mass = m * I")
    print(f"            r = 1, d = 4 (4D); alpha = m + r * d = m + 4")
    print()
    print("Block decomposition: eps reorders sites so eps = diag(+I, -I).")
    print("Then M = M_KS + alpha * I has eps-block form")
    print("    [[ +alpha I, +K     ],")
    print("     [ -K^dag,   +alpha I ]]")
    print("Bridge: det(M) = prod_i (alpha^2 + sigma_i^2) > 0 unconditionally.")
    print()

    rng = np.random.default_rng(SEED)

    # Multiple lattice sizes (must be even side lengths) and gauge scales
    cases = []
    for L in (2, 4):
        for scale in (0.0, 0.5, 1.0):
            volume = run_volume(L, scale, masses=[0.1, 0.5, 1.0, 2.0], rng=rng)
            cases.append(volume)

    # Aggregate assertions
    print()
    print("--- Bridge assertions ---")

    # Balanced sublattice on every L
    for v in cases:
        check(
            f"balanced sublattice n_+ = n_- on L={v['L']}",
            v["n_plus"] == v["n_minus"],
            detail=f"n_+={v['n_plus']}, n_-={v['n_minus']}",
        )

    # All m, scale combinations have det > 0
    all_positive = all(r["is_positive"] for v in cases for r in v["results"])
    check(
        "every (L, scale, m) case has det(M) > 0",
        all_positive,
        detail=f"checked {sum(len(v['results']) for v in cases)} (L, scale, m) configurations",
    )

    # Bridge factorisation matches direct det to high precision
    all_match = all(r["factorisation_match"] for v in cases for r in v["results"])
    max_log_diff = max(r["log_diff"] for v in cases for r in v["results"])
    check(
        "bridge factorisation det(M) = prod (alpha^2 + sigma_i^2) matches direct det",
        all_match,
        detail=f"max log_diff over all cases = {max_log_diff:.2e} (tol 1e-7)",
    )

    # Sigma sets give n/2 singular values (balanced sublattice condition)
    for v in cases:
        n_expected = v["n_plus"]  # = n_minus = (3 N_sites)/2 in colour space
        check(
            f"L={v['L']} K block has n_+ = {n_expected} singular values",
            v["n_sigmas"] == n_expected,
            detail=f"got {v['n_sigmas']}",
        )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
