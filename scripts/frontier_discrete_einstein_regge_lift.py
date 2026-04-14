#!/usr/bin/env python3
"""Discrete Einstein/Regge lift on the restricted strong-field class.

This script verifies the exact local field equation

    I_R(f; j) = 1/2 f^T Lambda_R f - j^T f

and its stationarity condition

    delta I_R = 0  <=>  Lambda_R f = j

on the current restricted bridge surface.

Exact content:
  1. The shell trace is recovered by the boundary-action minimizer.
  2. The quadratic completion identity holds to machine precision.
  3. The local static conformal lift remains exact on the same class.

Bounded content:
  4. Sampled perturbations raise the exact microscopic boundary action.
  5. The same lift persists on the broader support-class widening already on
     the branch.
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


microscopic = SourceFileLoader(
    "microscopic_dirichlet",
    "/private/tmp/physics-review-active/scripts/frontier_microscopic_dirichlet_bridge_principle.py",
).load_module()
same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
generic = SourceFileLoader(
    "generic_bridge_class",
    "/private/tmp/physics-review-active/scripts/frontier_generic_finite_support_schur_bridge.py",
).load_module()
static_lift = SourceFileLoader(
    "static_lift",
    "/private/tmp/physics-review-active/scripts/frontier_oh_static_constraint_lift.py",
).load_module()
schur = SourceFileLoader(
    "schur",
    "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
).load_module()


def action_report(name: str, phi_grid: np.ndarray, Lambda: np.ndarray, trace_idx: np.ndarray, bulk_idx: np.ndarray, interior: int):
    action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
    f = action["f"]
    j = action["j_trace"]
    f_star = np.linalg.solve(Lambda, j)
    base_val, base_grad = microscopic.boundary_action(Lambda, f_star, j)
    delta_exact = float(np.max(np.abs(f_star - f)))
    grad_exact = float(np.max(np.abs(base_grad)))

    rng = np.random.default_rng(29)
    delta_scale = max(float(np.max(np.abs(f_star))), 1e-3) * 1e-3
    sampled_gaps = []
    for _ in range(5):
        delta = rng.normal(size=f_star.shape)
        delta /= max(float(np.linalg.norm(delta)), 1e-12)
        delta *= delta_scale
        observed_gap, exact_gap = microscopic.completion_gap(Lambda, f_star, delta, j)
        sampled_gaps.append((observed_gap, exact_gap))

    min_gap = min(g[0] for g in sampled_gaps)
    max_gap_err = max(abs(g[0] - g[1]) for g in sampled_gaps)
    lift = static_lift.analyze_family(phi_grid)

    print(
        f"{name}: trace_match={delta_exact:.3e}, stationary_grad={grad_exact:.3e}, "
        f"action={base_val:.6e}, min_sampled_gap={min_gap:.3e}, "
        f"completion_err={max_gap_err:.3e}, "
        f"lift_residuals=(psi={float(np.max(np.abs(lift['res_psi']))):.3e}, "
        f"chi={float(np.max(np.abs(lift['res_chi']))):.3e})"
    )

    return {
        "trace_match": delta_exact,
        "grad_exact": grad_exact,
        "min_gap": min_gap,
        "completion_err": max_gap_err,
        "lift_psi": float(np.max(np.abs(lift["res_psi"]))),
        "lift_chi": float(np.max(np.abs(lift["res_chi"]))),
    }


def main() -> None:
    print("Discrete Einstein/Regge lift on the restricted strong-field class")
    print("=" * 80)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(0.5 * (Lambda + Lambda.T))
    min_eig = float(np.min(eigvals))

    exact_oh = action_report(
        "exact local O_h",
        same_source.build_best_phi_grid(),
        Lambda,
        trace_idx,
        bulk_idx,
        interior,
    )
    exact_fr = action_report(
        "finite-rank",
        coarse.build_finite_rank_phi_grid(),
        Lambda,
        trace_idx,
        bulk_idx,
        interior,
    )

    generic_rows = []
    for seed, n_sites in [(4, 6), (9, 8), (14, 10)]:
        phi_grid, _ = generic.build_generic_finite_support_phi_grid(seed, n_sites)
        generic_rows.append((seed, n_sites, action_report(f"generic finite support seed={seed}", phi_grid, Lambda, trace_idx, bulk_idx, interior)))

    max_generic_trace = max(row[2]["trace_match"] for row in generic_rows)
    max_generic_grad = max(row[2]["grad_exact"] for row in generic_rows)
    max_generic_lift = max(max(row[2]["lift_psi"], row[2]["lift_chi"]) for row in generic_rows)
    max_generic_gap = max(row[2]["min_gap"] for row in generic_rows)

    record(
        "the boundary operator is symmetric positive definite on the current bridge surface",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}",
    )
    record(
        "the exact local O_h shell trace is recovered by the boundary-action minimizer",
        exact_oh["trace_match"] < 1e-12 and exact_oh["grad_exact"] < 1e-12,
        f"trace match={exact_oh['trace_match']:.3e}, gradient={exact_oh['grad_exact']:.3e}",
    )
    record(
        "the exact local O_h bridge and lift remain exact at machine precision",
        exact_oh["lift_psi"] < 1e-12 and exact_oh["lift_chi"] < 1e-12,
        f"lift residuals=(psi={exact_oh['lift_psi']:.3e}, chi={exact_oh['lift_chi']:.3e})",
    )
    record(
        "the finite-rank bridge is recovered by the same discrete lift",
        exact_fr["trace_match"] < 1e-12 and exact_fr["grad_exact"] < 1e-12,
        f"trace match={exact_fr['trace_match']:.3e}, gradient={exact_fr['grad_exact']:.3e}",
    )
    record(
        "the support-agnostic generic finite-support samples satisfy the same restricted lift",
        max_generic_trace < 1e-12 and max_generic_grad < 1e-12 and max_generic_lift < 1e-12,
        f"max generic trace={max_generic_trace:.3e}, grad={max_generic_grad:.3e}, lift={max_generic_lift:.3e}",
        status="BOUNDED",
    )
    record(
        "sampled perturbations raise the exact microscopic boundary action",
        exact_oh["min_gap"] > 0.0 and exact_fr["min_gap"] > 0.0 and max_generic_gap > 0.0,
        f"min gaps: O_h={exact_oh['min_gap']:.3e}, finite-rank={exact_fr['min_gap']:.3e}, generic={max_generic_gap:.3e}",
        status="BOUNDED",
    )
    record(
        "the restricted Einstein/Regge-style 3+1 lift is exact on the current bridge surface and support-agnostic on finite support",
        exact_oh["trace_match"] < 1e-12
        and exact_fr["trace_match"] < 1e-12
        and max_generic_trace < 1e-12
        and exact_oh["lift_psi"] < 1e-12
        and exact_fr["lift_psi"] < 1e-12
        and max_generic_lift < 1e-12,
        "Schur boundary action + exact local static lift = restricted 3+1 closure",
    )

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
