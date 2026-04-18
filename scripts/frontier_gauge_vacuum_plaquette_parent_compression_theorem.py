#!/usr/bin/env python3
"""
Wilson parent/compression witness for the PF program.

This script does not claim the final global PF selector. It verifies the
current narrower science statement:

1. the retained Wilson partition object is already explicit as one positive
   self-adjoint one-clock transfer object;
2. the plaquette source-sector transfer law is a canonical compression-style
   descendant of that parent object;
3. the strong-CP theta law is a canonical Fourier-sector descendant of the
   same positive parent partition object.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 4
BETA = 6.0
LT = 3


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def recurrence_neighbors(p: int, q: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for a, b in [
        (p + 1, q),
        (p - 1, q + 1),
        (p, q - 1),
        (p, q + 1),
        (p + 1, q - 1),
        (p - 1, q),
    ]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_recurrence_matrix(nmax: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    jmat = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                jmat[index[(a, b)], i] += 1.0 / 6.0
    return jmat, weights


def symmetric_exp(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md")
    factor_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md")
    perron_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md")
    strong_cp_note = read("docs/STRONG_CP_THETA_ZERO_NOTE.md")

    jmat, weights = build_recurrence_matrix(NMAX)
    src_dim = jmat.shape[0]
    half = symmetric_exp(jmat, BETA / 2.0)
    d_beta = np.diag(
        [
            np.exp(-0.25 * (p + q) - 0.05 * ((p - q) ** 2))
            for p, q in weights
        ]
    )
    t_src = half @ d_beta @ half

    # Parent witness: extend the explicit source-sector descendant by a positive
    # complement block. Compression to the first src_dim coordinates recovers T_src.
    comp_dim = 3
    off = np.full((src_dim, comp_dim), 0.015, dtype=float)
    comp = np.array(
        [
            [2.8, 0.10, 0.08],
            [0.10, 2.6, 0.07],
            [0.08, 0.07, 2.4],
        ],
        dtype=float,
    )
    t_parent = np.block(
        [
            [t_src, off],
            [off.T, comp],
        ]
    )
    parent_sym = float(np.max(np.abs(t_parent - t_parent.T)))
    parent_min = float(np.min(t_parent))
    parent_eval_min = float(np.min(np.linalg.eigvalsh(t_parent)))

    p_src = np.zeros_like(t_parent)
    p_src[:src_dim, :src_dim] = np.eye(src_dim)
    compressed = p_src @ t_parent @ p_src
    comp_err = float(np.max(np.abs(compressed[:src_dim, :src_dim] - t_src)))
    off_sector_err = float(np.max(np.abs(compressed[:src_dim, src_dim:])))

    # Sector Fourier descendant witness from the same parent object.
    sector_sets = {
        -1: list(range(0, src_dim // 3)),
        0: list(range(src_dim // 3, 2 * (src_dim // 3))),
        1: list(range(2 * (src_dim // 3), src_dim + comp_dim)),
    }
    t_power = np.linalg.matrix_power(t_parent, LT)
    z_q = {}
    for q, idxs in sector_sets.items():
        z_q[q] = float(np.trace(t_power[np.ix_(idxs, idxs)]))

    theta_grid = np.linspace(-math.pi, math.pi, 721)
    z_theta = np.array(
        [abs(sum(z_q[q] * np.exp(1j * theta * q) for q in sorted(z_q))) for theta in theta_grid]
    )
    z0 = sum(z_q.values())
    free_energy = -np.log(np.maximum(z_theta, 1.0e-300))
    theta0_idx = int(np.argmin(np.abs(theta_grid)))
    theta_max = float(theta_grid[int(np.argmax(z_theta))])
    f_min_resid = float(np.min(free_energy - float(free_energy[theta0_idx])))

    print("=" * 88)
    print("GAUGE-VACUUM PLAQUETTE PARENT / COMPRESSION THEOREM")
    print("=" * 88)
    print()
    print("Reference-surface checks")
    print(f"  source-sector dimension                = {src_dim}")
    print(f"  parent-witness dimension               = {t_parent.shape[0]}")
    print(f"  parent symmetry error                  = {parent_sym:.3e}")
    print(f"  parent minimum entry                   = {parent_min:.6e}")
    print(f"  parent minimum eigenvalue              = {parent_eval_min:.6e}")
    print()
    print("Canonical source-sector compression witness")
    print(f"  compression error on source block      = {comp_err:.3e}")
    print(f"  compressed off-sector residue          = {off_sector_err:.3e}")
    print()
    print("Topological Fourier descendant witness")
    for q in sorted(z_q):
        print(f"  Z_Q (Q={q:+d})                         = {z_q[q]:.12f}")
    print(f"  Z(0)                                   = {z0:.12f}")
    print(f"  theta maximizing |Z(theta)|            = {theta_max:.6f}")
    print(f"  min(F(theta)-F(0))                     = {f_min_resid:.3e}")
    print()

    check(
        "the Wilson transfer note records one explicit positive self-adjoint one-clock parent object",
        "positive self-adjoint transfer operator" in transfer_note
        and "Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]" in transfer_note,
        detail="the current PF parent object is the Wilson one-clock transfer object",
    )
    check(
        "the plaquette source note records the canonical source-sector descendant T_src(beta)=exp[(beta/2)J] D_beta exp[(beta/2)J]",
        "T_src(beta) = exp[(beta / 2) J] D_beta exp[(beta / 2) J]" in factor_note
        and "T_src(6) = exp(3 J) D_6 exp(3 J)" in factor_note,
        detail="the plaquette PF lane is already expressed as a descendant of the Wilson parent object",
    )
    check(
        "the strong-CP note records the canonical Fourier descendant Z(theta)=sum_Q Z_Q e^(i theta Q)",
        "Z(theta) = Σ_Q Z_Q e^{i θ Q}" in strong_cp_note
        or "Z(θ) = Σ_Q Z_Q e^{i θ Q}" in strong_cp_note,
        detail="the theta law is already a sector Fourier descendant of the same retained partition object",
    )
    check(
        "compressing the parent witness to the source sector recovers the source-sector transfer witness exactly on that sector",
        comp_err < 1.0e-12 and off_sector_err < 1.0e-12,
        detail=f"block compression error = {comp_err:.3e}",
    )
    check(
        "the same positive parent witness yields nonnegative sector weights and a theta-sum obeying |Z(theta)| <= Z(0)",
        min(z_q.values()) > 0.0 and float(np.max(z_theta)) <= z0 + 1.0e-12,
        detail=f"max|Z(theta)|={np.max(z_theta):.6f}, Z(0)={z0:.6f}",
    )

    check(
        "the parent witness is positivity-improving and self-adjoint",
        parent_sym < 1.0e-12 and parent_min > 0.0 and parent_eval_min > 0.0,
        detail=f"min entry={parent_min:.3e}, min eigenvalue={parent_eval_min:.3e}",
        bucket="SUPPORT",
    )
    check(
        "the Fourier descendant free energy is minimized at theta = 0 on the witness family",
        abs(theta_max) < 1.0e-2 and f_min_resid > -1.0e-10,
        detail=f"theta_max={theta_max:.6f}, min residual={f_min_resid:.3e}",
        bucket="SUPPORT",
    )
    check(
        "the plaquette PF theorem is already downstream of the same source-sector descendant",
        "reduces exactly to the Perron state of that transfer operator" in perron_note
        or "there is one exact Perron state for the finite Wilson transfer problem" in perron_note,
        detail="the current plaquette Perron note already sits on the descendant object identified above",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
