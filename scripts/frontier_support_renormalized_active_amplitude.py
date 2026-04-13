#!/usr/bin/env python3
"""Exact support-renormalized amplitude law for the active shell correction.

Exact content:
  1. On the star-supported source class, the microscopic map from the
     renormalized support weights q_eff to the active shell-orbit correction
     vector is rank one.
  2. That map factors exactly through the total renormalized support charge:
         A_active = m_active * 1^T
     so the active correction is
         delta_sigma_active = Q_eff * m_active,
     where Q_eff = 1^T q_eff.
  3. The same factorization holds on the active pair quotient.
  4. The exact local O_h and broader finite-rank source families satisfy this
     support-side amplitude law exactly on the current star-supported class.

Bounded content:
  5. None. This script is meant to close the remaining scalar-amplitude
     ambiguity on the current star-supported source class.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_gravity",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
dtn_corr = SourceFileLoader(
    "finite_rank_dtn_corr",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_dtn_correction_operator.py",
).load_module()


def raw_active_orbit_vector(phi_grid: np.ndarray) -> np.ndarray:
    sigma = dtn_corr.sew.full_neg_laplacian(dtn_corr.sew.exterior_projector(phi_grid, 4.0))
    sigma_rad = dtn_corr.rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    vec = []
    for channel in dtn_corr.ACTIVE_ORBITS:
        total = 0.0
        for p in dtn_corr.ORBIT_POINTS[channel]:
            total += float(delta_sigma[p])
        vec.append(total)
    return np.array(vec, dtype=float)


def support_to_active_operator() -> tuple[np.ndarray, np.ndarray]:
    size, _, interior, _, g0p, _, _, _ = finite_rank.finite_rank_setup()
    cols = []
    for j in range(g0p.shape[1]):
        q_eff = np.zeros(g0p.shape[1], dtype=float)
        q_eff[j] = 1.0
        phi_flat = g0p @ q_eff
        phi_grid = np.zeros((size, size, size), dtype=float)
        phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
        cols.append(raw_active_orbit_vector(phi_grid))
    active = np.column_stack(cols)
    pair = active[:2, :]
    return active, pair


def oh_q_eff() -> tuple[np.ndarray, np.ndarray]:
    h0, interior = same_source.build_neg_laplacian_sparse(15)
    center = interior // 2
    support = [
        same_source.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same_source.SUPPORT_COORDS
    ]
    g0p = same_source.solve_columns(h0, support)
    gs = g0p[support, :]
    w = same_source.build_commutant_operator(0.0698, 0.0499, -0.0070, 0.0642, 0.1056)
    m = same_source.build_invariant_source(0.8247, 0.2271)
    q_eff = np.linalg.solve(np.eye(7) - w @ gs, m)
    phi_flat = g0p @ q_eff
    phi_grid = np.zeros((15, 15, 15), dtype=float)
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
    return q_eff, raw_active_orbit_vector(phi_grid)


def finite_rank_q_eff() -> tuple[np.ndarray, np.ndarray]:
    size, _, interior, _, g0p, gs, w, masses = finite_rank.finite_rank_setup()
    q_eff = np.linalg.solve(np.eye(7) - w @ gs, masses)
    phi_flat = g0p @ q_eff
    phi_grid = np.zeros((size, size, size), dtype=float)
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
    return q_eff, raw_active_orbit_vector(phi_grid)


def main() -> None:
    print("Support-renormalized active-shell amplitude law")
    print("=" * 72)

    active_op, pair_op = support_to_active_operator()
    active_mode = active_op[:, 0]
    pair_mode = pair_op[:, 0]
    ones = np.ones((1, active_op.shape[1]), dtype=float)
    active_fact = active_mode[:, None] @ ones
    pair_fact = pair_mode[:, None] @ ones

    active_rank = int(np.linalg.matrix_rank(active_op, tol=1e-12))
    pair_rank = int(np.linalg.matrix_rank(pair_op, tol=1e-12))
    active_factor_resid = float(np.max(np.abs(active_op - active_fact)))
    pair_factor_resid = float(np.max(np.abs(pair_op - pair_fact)))

    adapted = same_source.build_adapted_basis()
    active_adapted = active_op @ adapted
    noninv_resid = float(np.max(np.abs(active_adapted[:, 2:])))

    q_oh, vec_oh = oh_q_eff()
    q_fr, vec_fr = finite_rank_q_eff()
    qsum_oh = float(np.sum(q_oh))
    qsum_fr = float(np.sum(q_fr))

    pred_oh = active_op @ q_oh
    pred_fr = active_op @ q_fr
    scalar_oh = active_mode * qsum_oh
    scalar_fr = active_mode * qsum_fr
    pair_scalar_oh = pair_mode * qsum_oh
    pair_scalar_fr = pair_mode * qsum_fr

    err_oh = float(np.max(np.abs(pred_oh - vec_oh)))
    err_fr = float(np.max(np.abs(pred_fr - vec_fr)))
    scalar_err_oh = float(np.max(np.abs(vec_oh - scalar_oh)))
    scalar_err_fr = float(np.max(np.abs(vec_fr - scalar_fr)))
    pair_err_oh = float(np.max(np.abs(vec_oh[:2] - pair_scalar_oh)))
    pair_err_fr = float(np.max(np.abs(vec_fr[:2] - pair_scalar_fr)))

    print("Support -> active-orbit response operator:")
    print(np.array2string(active_op, precision=8, floatmode="fixed"))
    print(f"active rank = {active_rank}")
    print(f"pair rank = {pair_rank}")
    print(f"active factorization residual = {active_factor_resid:.3e}")
    print(f"pair factorization residual = {pair_factor_resid:.3e}")
    print(f"non-invariant adapted-channel residual = {noninv_resid:.3e}")
    print(f"unit-charge active mode = {np.array2string(active_mode, precision=8, floatmode='fixed')}")
    print(f"Q_eff(local O_h) = {qsum_oh:.8f}")
    print(f"Q_eff(finite-rank) = {qsum_fr:.8f}")

    record(
        "the microscopic support-to-active correction operator is exact rank one",
        active_rank == 1 and pair_rank == 1,
        f"active rank={active_rank}, pair rank={pair_rank}",
    )
    record(
        "the support-to-active operator factors exactly through total renormalized support charge",
        active_factor_resid < 1e-12 and pair_factor_resid < 1e-12,
        (
            f"active residual={active_factor_resid:.3e}, "
            f"pair residual={pair_factor_resid:.3e}"
        ),
    )
    record(
        "all non-invariant support channels are annihilated by the exact active response operator",
        noninv_resid < 1e-12,
        f"max adapted non-invariant residual = {noninv_resid:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families satisfy the full active support-response law",
        err_oh < 1e-12 and err_fr < 1e-12 and scalar_err_oh < 1e-12 and scalar_err_fr < 1e-12,
        (
            f"direct errors: O_h={err_oh:.3e}, finite-rank={err_fr:.3e}; "
            f"scalar-law errors: O_h={scalar_err_oh:.3e}, finite-rank={scalar_err_fr:.3e}"
        ),
    )
    record(
        "the same scalar-amplitude law holds exactly on the active pair quotient",
        pair_err_oh < 1e-12 and pair_err_fr < 1e-12,
        f"pair errors: O_h={pair_err_oh:.3e}, finite-rank={pair_err_fr:.3e}",
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
