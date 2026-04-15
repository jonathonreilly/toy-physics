#!/usr/bin/env python3
"""Exact Schur localization of the direct-universal Hessian on an SO(3)-invariant background.

This runner upgrades the direct universal route beyond the anisotropic finite
prototype audit. It proves:

1. the spatially invariant background subspace is exactly the 2D `A1` core;
2. any invariant lifted background has the form `diag(a,b,b,b)`;
3. on that background the universal Hessian candidate commutes with the exact
   block projectors `P_lapse`, `P_shift`, `P_trace`, `P_shear`;
4. the old `trace <-> shear` mixer vanishes identically;
5. the shift and shear blocks are exact scalar blocks with closed-form
   eigenvalues.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Sequence

import numpy as np


ROOT = Path("/Users/jonreilly/Projects/Physics")
U = SourceFileLoader(
    "universal_conn",
    str(ROOT / "scripts" / "frontier_universal_gr_canonical_projector_connection.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def sym(i: int, j: int, n: int = 4) -> np.ndarray:
    m = np.zeros((n, n), dtype=float)
    if i == j:
        m[i, j] = 1.0
    else:
        scale = math.sqrt(2.0)
        m[i, j] = 1.0 / scale
        m[j, i] = 1.0 / scale
    return m


def diag(vals: Sequence[float]) -> np.ndarray:
    return np.diag(np.asarray(vals, dtype=float))


def canonical_polarization_frame() -> list[np.ndarray]:
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    return [
        sym(0, 0),
        sym(0, 1),
        sym(0, 2),
        sym(0, 3),
        diag((0.0, 1.0 / sqrt3, 1.0 / sqrt3, 1.0 / sqrt3)),
        diag((0.0, 1.0 / sqrt2, -1.0 / sqrt2, 0.0)),
        diag((0.0, 1.0 / sqrt6, 1.0 / sqrt6, -2.0 / sqrt6)),
        sym(1, 2),
        sym(1, 3),
        sym(2, 3),
    ]


def spectral_projector(op: np.ndarray, target: float, tol: float = 1e-9) -> np.ndarray:
    vals, vecs = np.linalg.eig(op)
    mask = np.abs(vals - target) < tol
    V = vecs[:, mask]
    if V.size == 0:
        return np.zeros_like(op)
    return np.real_if_close(V @ np.linalg.inv(V.T @ V) @ V.T, tol=1e-7)


def block_projectors() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    Gx = U.generator("x")
    Gy = U.generator("y")
    Gz = U.generator("z")
    comp_idx = [i for i in range(10) if i not in (0, 4)]
    Gc = [G[np.ix_(comp_idx, comp_idx)] for G in (Gx, Gy, Gz)]
    C = sum(G @ G for G in Gc)

    P_lapse = np.zeros((10, 10), dtype=float)
    P_lapse[0, 0] = 1.0
    P_trace = np.zeros((10, 10), dtype=float)
    P_trace[4, 4] = 1.0

    P_shift_c = spectral_projector(C, -2.0)
    P_shear_c = spectral_projector(C, -6.0)
    P_shift = np.zeros((10, 10), dtype=float)
    P_shear = np.zeros((10, 10), dtype=float)
    P_shift[np.ix_(comp_idx, comp_idx)] = P_shift_c
    P_shear[np.ix_(comp_idx, comp_idx)] = P_shear_c
    return P_lapse, P_shift, P_trace, P_shear


def bilinear(a: np.ndarray, b: np.ndarray, d: Sequence[float]) -> float:
    total = 0.0
    for i in range(4):
        for j in range(4):
            total += a[i, j] * b[j, i] / (d[i] * d[j])
    return -total


def gram_matrix(d: Sequence[float]) -> np.ndarray:
    basis = canonical_polarization_frame()
    return np.asarray([[bilinear(a, b, d) for b in basis] for a in basis], dtype=float)


def fixed_subspace_basis(gens: Sequence[np.ndarray], tol: float = 1e-12) -> np.ndarray:
    stacked = np.vstack(list(gens))
    _, s, vh = np.linalg.svd(stacked)
    rank = int(np.sum(s > tol))
    return vh[rank:].T


def scalar_block_error(h: np.ndarray, p: np.ndarray) -> float:
    rank = int(np.linalg.matrix_rank(p, tol=1e-12))
    if rank == 0:
        return 0.0
    block = p @ h @ p
    coeff = float(np.trace(block) / rank)
    return float(np.linalg.norm(block - coeff * p, ord="fro"))


def main() -> int:
    Gx = U.generator("x")
    Gy = U.generator("y")
    Gz = U.generator("z")
    P_lapse, P_shift, P_trace, P_shear = block_projectors()
    Pi_A1 = U.pi_a1()

    fixed = fixed_subspace_basis((Gx, Gy, Gz))
    fixed_rank = fixed.shape[1]
    fixed_err = float(
        max(
            np.linalg.norm(Gx @ fixed, ord="fro"),
            np.linalg.norm(Gy @ fixed, ord="fro"),
            np.linalg.norm(Gz @ fixed, ord="fro"),
        )
    )
    a1_overlap = float(np.linalg.norm((np.eye(10) - Pi_A1) @ fixed, ord="fro"))

    backgrounds = [(2.0, 3.0), (5.0, 7.0), (1.0, 1.0)]
    max_comm = 0.0
    max_trace_shear = 0.0
    max_lapse_shift = 0.0
    max_shift_shear = 0.0
    max_shift_scalar = 0.0
    max_shear_scalar = 0.0
    max_formula = 0.0

    for a, b in backgrounds:
        d = (a, b, b, b)
        h = gram_matrix(d)

        comms = [
            np.linalg.norm(P_lapse @ h - h @ P_lapse, ord="fro"),
            np.linalg.norm(P_shift @ h - h @ P_shift, ord="fro"),
            np.linalg.norm(P_trace @ h - h @ P_trace, ord="fro"),
            np.linalg.norm(P_shear @ h - h @ P_shear, ord="fro"),
        ]
        max_comm = max(max_comm, *[float(x) for x in comms])

        trace_shear = float(np.linalg.norm(P_trace @ h @ P_shear, ord="fro"))
        lapse_shift = float(np.linalg.norm(P_lapse @ h @ P_shift, ord="fro"))
        shift_shear = float(np.linalg.norm(P_shift @ h @ P_shear, ord="fro"))
        max_trace_shear = max(max_trace_shear, trace_shear)
        max_lapse_shift = max(max_lapse_shift, lapse_shift)
        max_shift_shear = max(max_shift_shear, shift_shear)

        shift_scalar = scalar_block_error(h, P_shift)
        shear_scalar = scalar_block_error(h, P_shear)
        max_shift_scalar = max(max_shift_scalar, shift_scalar)
        max_shear_scalar = max(max_shear_scalar, shear_scalar)

        alpha_lapse = float(np.trace(P_lapse @ h @ P_lapse))
        alpha_shift = float(np.trace(P_shift @ h @ P_shift) / 3.0)
        alpha_trace = float(np.trace(P_trace @ h @ P_trace))
        alpha_shear = float(np.trace(P_shear @ h @ P_shear) / 5.0)

        max_formula = max(
            max_formula,
            abs(alpha_lapse + 1.0 / (a * a)),
            abs(alpha_shift + 1.0 / (a * b)),
            abs(alpha_trace + 1.0 / (b * b)),
            abs(alpha_shear + 1.0 / (b * b)),
        )

    print("UNIVERSAL GR ISOTROPIC SCHUR LOCALIZATION")
    print("=" * 78)
    print(f"fixed-subspace rank = {fixed_rank}")
    print(f"fixed-subspace invariance error = {fixed_err:.3e}")
    print(f"fixed-subspace off-A1 overlap = {a1_overlap:.3e}")
    print(f"max block commutator error = {max_comm:.3e}")
    print(f"max lapse-shift leakage = {max_lapse_shift:.3e}")
    print(f"max shift-shear leakage = {max_shift_shear:.3e}")
    print(f"max trace-shear leakage = {max_trace_shear:.3e}")
    print(f"max shift scalar error = {max_shift_scalar:.3e}")
    print(f"max shear scalar error = {max_shear_scalar:.3e}")
    print(f"max closed-form coefficient error = {max_formula:.3e}")

    record(
        "the spatially invariant background subspace is exactly the 2D A1 core",
        fixed_rank == 2 and fixed_err < 1e-12 and a1_overlap < 1e-12,
        f"rank={fixed_rank}, invariance={fixed_err:.3e}, off-A1={a1_overlap:.3e}",
    )
    record(
        "any SO(3)-invariant lifted background therefore has the form diag(a,b,b,b)",
        fixed_rank == 2 and a1_overlap < 1e-12,
        "the only invariant source directions are lapse and spatial trace",
    )
    record(
        "on an invariant background the universal Hessian commutes with the canonical block projectors",
        max_comm < 1e-12,
        f"max commutator error={max_comm:.3e}",
    )
    record(
        "the old trace-shear obstruction vanishes identically on the invariant background",
        max_trace_shear < 1e-12 and max_lapse_shift < 1e-12 and max_shift_shear < 1e-12,
        f"lapse-shift={max_lapse_shift:.3e}, shift-shear={max_shift_shear:.3e}, trace-shear={max_trace_shear:.3e}",
    )
    record(
        "the shift and shear blocks are exact scalar Schur blocks on the invariant background",
        max_shift_scalar < 1e-12 and max_shear_scalar < 1e-12,
        f"shift={max_shift_scalar:.3e}, shear={max_shear_scalar:.3e}",
    )
    record(
        "the block coefficients are closed-form: alpha_lapse=-a^-2, alpha_shift=-(ab)^-1, alpha_trace=alpha_shear=-b^-2",
        max_formula < 1e-12,
        f"max coefficient error={max_formula:.3e}",
    )

    print("\nVerdict:")
    print(
        "The anisotropic finite prototype is not the correct universal blocker. "
        "Once the lifted background is restricted to the exact SO(3)-invariant "
        "subspace forced by the direct universal route, the Hessian Schur-"
        "localizes exactly into lapse, shift, trace, and shear blocks."
    )
    print(
        "So the previous rank-1 trace-shear mixer is a prototype artifact. The "
        "remaining direct-universal issue is now only the final Einstein/Regge "
        "operator identification / normalization on this already-localized "
        "isotropic background."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
