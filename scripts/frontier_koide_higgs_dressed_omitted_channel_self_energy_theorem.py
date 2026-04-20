#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed omitted-channel self-energy theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_OMITTED_CHANNEL_SELF_ENERGY_THEOREM_NOTE_2026-04-20.md`.
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
G_VEC = np.array([[H_STAR[2, 0]], [H_STAR[1, 0]]], dtype=complex)
H_REACHED = H_STAR[np.ix_([2, 1], [2, 1])]
LAMBDA_PLUS = Q_PLUS_STAR + DELTA_STAR - np.sqrt(8.0 / 3.0)
LAMBDA_MINUS = Q_PLUS_STAR - DELTA_STAR + np.sqrt(8.0 / 3.0)


def reached_block_full(lam: float) -> np.ndarray:
    resolvent = np.linalg.inv(lam * np.eye(3) - H_STAR)
    return resolvent[np.ix_([2, 1], [2, 1])]


def reached_block_schur(lam: float) -> np.ndarray:
    self_energy = (G_VEC @ G_VEC.conj().T) / (lam - M_OMIT)
    return np.linalg.inv(lam * np.eye(2) - H_REACHED - self_energy)


def reached_block_decoupled(lam: float) -> np.ndarray:
    return np.linalg.inv(lam * np.eye(2) - H_REACHED)


def q_branch(lam: float, h0: float, full: bool) -> float:
    block = reached_block_full(lam) if full else reached_block_decoupled(lam)
    masses = np.abs(np.linalg.eigvalsh((block + block.conj().T) / 2.0))
    x = abs(1.0 / (lam - h0))
    return koide_Q(np.array([masses[0], masses[1], x])) - 2.0 / 3.0


def local_root(lam: float, full: bool) -> float:
    grid = np.linspace(-0.002, 0.01, 6001)
    prev_x = None
    prev_v = None
    roots: list[float] = []
    for x in grid:
        v = q_branch(lam, x, full)
        if not np.isfinite(v):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * v < 0.0:
            roots.append(brentq(lambda h0: q_branch(lam, h0, full), prev_x, x))
        prev_x = x
        prev_v = v
    roots = [r for r in roots if abs(r) < 0.01]
    if not roots:
        raise ValueError("no local root found")
    return min(roots, key=abs)


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed omitted-channel self-energy theorem")
    print("=" * 88)

    self_energy_star = (G_VEC @ G_VEC.conj().T) / (LAMBDA_STAR - M_OMIT)
    check(
        "The reached transport block is exactly the Schur-complement resolvent with one omitted-channel self-energy",
        np.max(np.abs(reached_block_full(LAMBDA_STAR) - reached_block_schur(LAMBDA_STAR))) < 1.0e-12,
    )
    check(
        "That omitted-channel correction is rank 1",
        np.linalg.matrix_rank(self_energy_star, tol=1.0e-10) == 1,
        detail=f"self_energy={np.round(self_energy_star, 12).tolist()}",
    )
    check(
        "The omitted-channel coupling vector is exactly the visible two-link chamber packet plus the fixed half-gamma phase",
        abs(float(G_VEC[0, 0].real) - LAMBDA_PLUS) < 1.0e-15
        and abs(float(G_VEC[0, 0].imag) - 0.5) < 1.0e-15
        and abs(float(G_VEC[1, 0].real) - LAMBDA_MINUS) < 1.0e-15
        and abs(float(G_VEC[1, 0].imag)) < 1.0e-15,
        detail=f"g={np.round(G_VEC.flatten(), 12).tolist()}",
    )

    sample_lambdas = np.linspace(LAMBDA_STAR - 6.0e-5, LAMBDA_STAR + 6.0e-5, 5)
    roots_decoupled = np.array([local_root(lam, full=False) for lam in sample_lambdas])
    roots_full = np.array([local_root(lam, full=True) for lam in sample_lambdas])
    coeff_decoupled = np.polyfit(sample_lambdas - LAMBDA_STAR, roots_decoupled, 1)
    coeff_full = np.polyfit(sample_lambdas - LAMBDA_STAR, roots_full, 1)

    check(
        "Without the omitted-channel self-energy the local branch does not pass through the physical origin",
        abs(coeff_decoupled[1]) > 5.0e-4,
        detail=f"intercept_decoupled={coeff_decoupled[1]:.12e}",
    )
    check(
        "With the full omitted-channel self-energy the local branch passes through the physical origin",
        abs(coeff_full[1]) < 1.0e-9,
        detail=f"intercept_full={coeff_full[1]:.12e}",
    )
    check(
        "The decoupled reached-sector branch tracks lambda with slope ~1",
        0.999 < coeff_decoupled[0] < 1.002,
        detail=f"slope_decoupled={coeff_decoupled[0]:.12f}",
    )
    check(
        "The omitted-channel self-energy is what lowers the physical slope to the observed alpha",
        0.95 < coeff_full[0] < 0.97 and coeff_full[0] < coeff_decoupled[0],
        detail=f"slope_full={coeff_full[0]:.12f}",
    )

    print()
    print("Interpretation:")
    print("  The local Koide transport correction is not sourced by generic reached")
    print("  2x2 dynamics alone. The full reached block is exactly the Schur resolvent")
    print("  with one rank-1 omitted-channel self-energy, and that omitted channel is")
    print("  what both shifts the local root onto the physical origin and lowers the")
    print("  affine slope from ~1 to the observed alpha.")
    print("  So the remaining microscopic transport object is sharper again:")
    print("      derive the omitted-channel self-energy term from retained physics.")
    print()
    print(f"  slope_decoupled = {coeff_decoupled[0]:.12f}")
    print(f"  slope_full      = {coeff_full[0]:.12f}")
    print(f"  intercept_decoupled = {coeff_decoupled[1]:.12e}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
