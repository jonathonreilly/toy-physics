#!/usr/bin/env python3
"""Bounded tensor-drive scan in support-irrep coordinates.

This runner takes the exact support-irrep decomposition identified on the
restricted gravity class and tests whether the remaining tensor-drive
coefficient is naturally organized in those coordinates.

Setup:
  - hold the scalar A1 support sector fixed at the finite-rank value
  - turn on the finite-rank E sector and T1 sector separately
  - evaluate the scalar-derived tensor drive c_eta on the resulting exact
    star-supported source families

This is bounded evidence, not a full theorem, because it is a scan on one
exact source family direction rather than an all-class derivation.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from io import StringIO

import numpy as np


ROOT = "/private/tmp/physics-review-active"

same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    f"{ROOT}/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
utk = SourceFileLoader(
    "tensor_universal_kernel",
    f"{ROOT}/scripts/frontier_tensor_universal_kernel.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []

SIZE = 15


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def support_green_columns() -> tuple[np.ndarray, int]:
    H0, interior = same_source.build_neg_laplacian_sparse(SIZE)
    center = interior // 2
    support = [
        same_source.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same_source.SUPPORT_COORDS
    ]
    return same_source.solve_columns(H0, support), interior


G0P, INTERIOR = support_green_columns()


def phi_from_q(q: np.ndarray) -> np.ndarray:
    phi = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    phi[1:-1, 1:-1, 1:-1] = (G0P @ q).reshape((INTERIOR, INTERIOR, INTERIOR))
    return phi


def c_eta(phi_grid: np.ndarray) -> tuple[float, float, float]:
    with redirect_stdout(StringIO()):
        blk = utk.family_block("scan", phi_grid)
    return (
        float(blk.eta_floor[1] / abs(blk.scalar_action)),
        float(blk.scalar_action),
        float(blk.eta_floor[1]),
    )


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, GS, W, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)


def main() -> int:
    print("Tensor-drive scan in support-irrep coordinates")
    print("=" * 78)

    basis = same_source.build_adapted_basis()
    coeff = basis.T @ finite_rank_qeff()
    q_a1 = basis[:, :2] @ coeff[:2]
    q_e = basis[:, 2:4] @ coeff[2:4]
    q_t = basis[:, 4:7] @ coeff[4:7]

    c_a1, s_a1, ef_a1 = c_eta(phi_from_q(q_a1))
    c_e, s_e, ef_e = c_eta(phi_from_q(q_a1 + q_e))
    c_t, s_t, ef_t = c_eta(phi_from_q(q_a1 + q_t))
    c_full, s_full, ef_full = c_eta(phi_from_q(q_a1 + q_e + q_t))

    print("Endpoint values:")
    print(f"  A1 only       : c_eta={c_a1:.12e}, scalar={s_a1:.12e}, eta_floor_tf={ef_a1:.12e}")
    print(f"  A1 + E        : c_eta={c_e:.12e}, scalar={s_e:.12e}, eta_floor_tf={ef_e:.12e}")
    print(f"  A1 + T1       : c_eta={c_t:.12e}, scalar={s_t:.12e}, eta_floor_tf={ef_t:.12e}")
    print(f"  A1 + E + T1   : c_eta={c_full:.12e}, scalar={s_full:.12e}, eta_floor_tf={ef_full:.12e}")

    e_shift = c_e - c_a1
    t_shift = c_t - c_a1
    full_shift = c_full - c_a1
    additivity_err = abs((e_shift + t_shift) - full_shift)

    print("\nShift decomposition:")
    print(f"  E-sector shift    = {e_shift:+.12e}")
    print(f"  T1-sector shift   = {t_shift:+.12e}")
    print(f"  full shift        = {full_shift:+.12e}")
    print(f"  additivity error  = {additivity_err:.12e}")

    print("\nOne-parameter scans:")
    e_vals = []
    t_vals = []
    for lam in [0.0, 0.25, 0.5, 0.75, 1.0]:
        c_lam, _, _ = c_eta(phi_from_q(q_a1 + lam * q_e))
        e_vals.append((lam, c_lam))
    for lam in [0.0, 0.25, 0.5, 0.75, 1.0]:
        c_lam, _, _ = c_eta(phi_from_q(q_a1 + lam * q_t))
        t_vals.append((lam, c_lam))
    for lam, val in e_vals:
        print(f"  E scan  lambda={lam:.2f}: c_eta={val:.12e}")
    for lam, val in t_vals:
        print(f"  T1 scan lambda={lam:.2f}: c_eta={val:.12e}")

    e_second = max(
        abs(e_vals[i + 1][1] - 2.0 * e_vals[i][1] + e_vals[i - 1][1])
        for i in range(1, len(e_vals) - 1)
    )
    t_second = max(
        abs(t_vals[i + 1][1] - 2.0 * t_vals[i][1] + t_vals[i - 1][1])
        for i in range(1, len(t_vals) - 1)
    )

    record(
        "with the scalar A1 sector fixed, the E sector and T1 sector shift c_eta in opposite directions",
        e_shift < 0.0 and t_shift > 0.0,
        f"E shift={e_shift:+.6e}, T1 shift={t_shift:+.6e}",
    )
    record(
        "the c_eta response is nearly additive in the finite-rank E and T1 directions",
        additivity_err < 2e-7,
        f"full shift={full_shift:+.6e}, additive reconstruction error={additivity_err:.6e}",
    )
    record(
        "the c_eta response is nearly linear along the finite-rank E support direction",
        e_second < 1e-7,
        f"max discrete second difference along E scan={e_second:.6e}",
    )
    record(
        "the c_eta response is nearly linear along the finite-rank T1 support direction",
        t_second < 1e-7,
        f"max discrete second difference along T1 scan={t_second:.6e}",
    )

    print("\nVerdict:")
    print(
        "On the exact star-supported source class, the remaining tensor-drive "
        "coefficient is naturally organized in support-irrep coordinates: the "
        "E sector lowers c_eta, the T1 sector raises it, and the full "
        "finite-rank shift is nearly additive in those two non-scalar source "
        "channels."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
