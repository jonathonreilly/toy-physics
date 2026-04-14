#!/usr/bin/env python3
"""Exact bridge-side closure on the star-supported finite-rank source class.

Exact content:
  1. For any star-supported finite-rank source field phi on the current
     Dirichlet box, the projector shell source sigma_R = H_0 Pi_R^ext phi is
     supported on the sewing band 3 < r <= 5.
  2. The native same-charge bridge
         psi = 1 + phi_ext
         chi = 1 - phi_ext = alpha * psi
     yields the exact local static conformal constraint pair
         H_0 psi = 2 pi psi^5 rho
         H_0 chi = -2 pi alpha psi^5 (rho + 2S)
     with rho = sigma_R / (2 pi psi^5), S = 0.5 rho (1/alpha - 1).
  3. The exact shell trace is the stationary point of the microscopic
     Schur-complement boundary action on Gamma_R.

Bounded consequence:
  4. Random star-supported finite-rank examples verify these exact identities
     outside the previously hand-tuned O_h and benchmark finite-rank families.
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


finite_rank = SourceFileLoader(
    "finite_rank_metric",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
static_lift = SourceFileLoader(
    "oh_static_constraint_lift",
    "/private/tmp/physics-review-active/scripts/frontier_oh_static_constraint_lift.py",
).load_module()
schur = SourceFileLoader(
    "oh_schur_boundary_action",
    "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
).load_module()


STAR_COORDS = [
    np.array([0, 0, 0], dtype=int),
    np.array([1, 0, 0], dtype=int),
    np.array([-1, 0, 0], dtype=int),
    np.array([0, 1, 0], dtype=int),
    np.array([0, -1, 0], dtype=int),
    np.array([0, 0, 1], dtype=int),
    np.array([0, 0, -1], dtype=int),
]


def build_star_supported_phi_grid(seed: int) -> np.ndarray:
    size = 15
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    center = interior // 2
    support = [
        finite_rank.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in STAR_COORDS
    ]
    G0P = finite_rank.solve_columns(H0, support)
    GS = G0P[support, :]

    rng = np.random.default_rng(seed)
    A = rng.normal(size=(7, 7))
    W_raw = A @ A.T
    eigvals = np.linalg.eigvals(W_raw @ GS)
    rho = max(abs(ev) for ev in eigvals)
    scale = 0.35 / rho
    W = scale * W_raw

    m = rng.normal(size=7)
    if abs(np.sum(m)) < 0.2:
        m[0] += 0.5

    q_eff = np.linalg.solve(np.eye(7) - W @ GS, m)
    phi_flat = G0P @ q_eff

    phi_grid = np.zeros((size, size, size))
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))

    support_points = [(center + v[0] + 1, center + v[1] + 1, center + v[2] + 1) for v in STAR_COORDS]
    max_abs = max(abs(float(phi_grid[idx])) for idx in support_points)
    if max_abs > 0.0:
        phi_grid *= 0.30 / max_abs
    return phi_grid


def main() -> None:
    print("Exact bridge-side closure on the star-supported finite-rank class")
    print("=" * 72)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)

    seeds = [3, 7, 11, 19, 23]
    shell_min = []
    shell_max = []
    res_psi = []
    res_chi = []
    grad_err = []
    rebuild_err = []

    for seed in seeds:
        phi_grid = build_star_supported_phi_grid(seed)
        family = static_lift.analyze_family(phi_grid)
        shell_min.append(family["shell_support_min"])
        shell_max.append(family["shell_support_max"])
        res_psi.append(float(np.max(np.abs(family["res_psi"]))))
        res_chi.append(float(np.max(np.abs(family["res_chi"]))))

        action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
        grad_err.append(float(np.max(np.abs(action["grad_expected"] - action["j_trace"]))))
        rebuild_err.append(action["rebuild_err"])

        print(
            f"seed={seed}: band=[{family['shell_support_min']:.6f}, {family['shell_support_max']:.6f}], "
            f"max residuals=(psi={res_psi[-1]:.3e}, chi={res_chi[-1]:.3e}), "
            f"action errs=(rebuild={rebuild_err[-1]:.3e}, grad={grad_err[-1]:.3e})"
        )

    record(
        "every tested star-supported finite-rank field keeps the exact shell source on the sewing band 3 < r <= 5",
        min(shell_min) > 3.0 and max(shell_max) <= 5.0 + 1e-12,
        (
            f"shell band envelope=[{min(shell_min):.6f}, {max(shell_max):.6f}] "
            f"across {len(seeds)} seeds"
        ),
    )
    record(
        "every tested star-supported finite-rank field satisfies the first local static conformal constraint exactly",
        max(res_psi) < 1e-12,
        f"max sampled psi residual={max(res_psi):.3e}",
    )
    record(
        "every tested star-supported finite-rank field satisfies the second local static conformal constraint exactly",
        max(res_chi) < 1e-12,
        f"max sampled chi residual={max(res_chi):.3e}",
    )
    record(
        "every tested star-supported finite-rank field is stationary for the same microscopic Schur boundary action",
        max(grad_err) < 1e-12 and max(rebuild_err) < 1e-12,
        (
            f"max sampled (rebuild,grad)=({max(rebuild_err):.3e}, "
            f"{max(grad_err):.3e})"
        ),
    )
    record(
        "the bridge-side exact closure package extends beyond the benchmark O_h and benchmark finite-rank families to the full tested star-supported finite-rank class",
        max(res_psi) < 1e-12 and max(res_chi) < 1e-12 and max(grad_err) < 1e-12,
        "exact shell source + exact local constraints + exact microscopic boundary action",
        status="BOUNDED",
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
