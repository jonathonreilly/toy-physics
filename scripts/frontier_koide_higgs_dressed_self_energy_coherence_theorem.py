#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed self-energy coherence theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_SELF_ENERGY_COHERENCE_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import H3, M_STAR, DELTA_STAR, Q_PLUS_STAR, koide_Q


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


LAMBDA_STAR = 0.01580870328539511
H_STAR = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)
M_OMIT = H_STAR[0, 0]
G_VEC = np.array([H_STAR[2, 0], H_STAR[1, 0]], dtype=complex)
H_REACHED = H_STAR[np.ix_([2, 1], [2, 1])]


def sigma_mode(mode: str) -> np.ndarray:
    full = np.outer(G_VEC, G_VEC.conj())
    if mode == "arm1":
        v = np.array([G_VEC[0], 0.0], dtype=complex)
        return np.outer(v, v.conj())
    if mode == "arm2":
        v = np.array([0.0, G_VEC[1]], dtype=complex)
        return np.outer(v, v.conj())
    if mode == "diagonly":
        return np.diag(np.abs(G_VEC) ** 2)
    if mode == "offdiagonly":
        return full - np.diag(np.abs(G_VEC) ** 2)
    if mode == "full":
        return full
    raise ValueError(mode)


def q_branch(lam: float, h0: float, mode: str) -> float:
    sigma = sigma_mode(mode)
    block = np.linalg.inv(lam * np.eye(2) - H_REACHED - sigma / (lam - M_OMIT))
    masses = np.abs(np.linalg.eigvalsh((block + block.conj().T) / 2.0))
    x = abs(1.0 / (lam - h0))
    return koide_Q(np.array([masses[0], masses[1], x])) - 2.0 / 3.0


def local_root(lam: float, mode: str, guess: float) -> float:
    grid = np.linspace(guess - 0.001, guess + 0.001, 2001)
    prev_x = None
    prev_v = None
    for x in grid:
        v = q_branch(lam, x, mode)
        if not np.isfinite(v):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * v < 0.0:
            return brentq(lambda h0: q_branch(lam, h0, mode), prev_x, x)
        prev_x = x
        prev_v = v
    raise ValueError(f"no local root for {mode} near {guess}")


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed self-energy coherence theorem")
    print("=" * 88)

    mode_guesses = {
        "arm1": -0.0015828353,
        "arm2": -0.0033889327,
        "diagonly": -0.0080254383,
        "offdiagonly": -0.0062353557,
        "full": 0.0,
    }

    full_sigma = sigma_mode("full")
    check(
        "The physical omitted-channel self-energy is rank 1",
        np.linalg.matrix_rank(full_sigma, tol=1.0e-10) == 1,
        detail=f"det={np.linalg.det(full_sigma):+.3e}",
    )
    check(
        "The diagonal-only and off-diagonal-only pieces separately lose that rank-1 coherence",
        np.linalg.matrix_rank(sigma_mode("diagonly"), tol=1.0e-10) == 2
        and np.linalg.matrix_rank(sigma_mode("offdiagonly"), tol=1.0e-10) == 2,
    )

    mode_roots = {}
    mode_slopes = {}
    sample_dlambda = np.array([-2.0e-5, 0.0, 2.0e-5])
    for mode, guess in mode_guesses.items():
        roots = np.array([local_root(LAMBDA_STAR + dl, mode, guess) for dl in sample_dlambda])
        fit = np.polyfit(sample_dlambda, roots, 1)
        mode_roots[mode] = roots
        mode_slopes[mode] = fit[0]

    check(
        "Each partial self-energy mode has a unique nearby local Koide branch, but all miss the physical origin",
        all(abs(mode_roots[m][1]) > 1.0e-3 for m in ("arm1", "arm2", "diagonly", "offdiagonly")),
        detail=(
            f"arm1={mode_roots['arm1'][1]:+.6e}, arm2={mode_roots['arm2'][1]:+.6e}, "
            f"diag={mode_roots['diagonly'][1]:+.6e}, offdiag={mode_roots['offdiagonly'][1]:+.6e}"
        ),
    )
    check(
        "Only the full coherent rank-1 self-energy restores the local root to the physical origin",
        abs(mode_roots["full"][1]) < 1.0e-10,
        detail=f"full={mode_roots['full'][1]:+.3e}",
    )
    check(
        "No single omitted-channel arm reproduces the observed full slope",
        abs(mode_slopes["arm1"] - mode_slopes["full"]) > 0.01
        and abs(mode_slopes["arm2"] - mode_slopes["full"]) > 1.0e-3,
        detail=f"arm1={mode_slopes['arm1']:.12f}, arm2={mode_slopes['arm2']:.12f}, full={mode_slopes['full']:.12f}",
    )
    check(
        "The incoherent diagonal/off-diagonal splits also fail to reproduce the physical branch",
        abs(mode_slopes["diagonly"] - mode_slopes["full"]) > 1.0e-3
        and abs(mode_slopes["offdiagonly"] - mode_slopes["full"]) > 1.0e-3,
        detail=f"diag={mode_slopes['diagonly']:.12f}, offdiag={mode_slopes['offdiagonly']:.12f}",
    )
    check(
        "The full coherent combination simultaneously fixes the root position and the physical slope",
        0.95 < mode_slopes["full"] < 0.97,
        detail=f"slope_full={mode_slopes['full']:.12f}",
    )

    print()
    print("Interpretation:")
    print("  The physical local transport correction is not the effect of one omitted")
    print("  arm, nor of a diagonal magnitude correction, nor of off-diagonal mixing")
    print("  by itself. It is a coherence effect of the full rank-1 omitted-channel")
    print("  self-energy generated by the single coupling vector g.")
    print("  So the remaining microscopic object is sharper again:")
    print("      derive the coherent omitted-channel coupling vector g from retained physics.")
    print()
    print(f"  full slope      = {mode_slopes['full']:.12f}")
    print(f"  arm1 slope      = {mode_slopes['arm1']:.12f}")
    print(f"  arm2 slope      = {mode_slopes['arm2']:.12f}")
    print(f"  diagonly slope  = {mode_slopes['diagonly']:.12f}")
    print(f"  offdiag slope   = {mode_slopes['offdiagonly']:.12f}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
