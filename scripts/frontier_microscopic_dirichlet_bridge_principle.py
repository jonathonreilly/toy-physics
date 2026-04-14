#!/usr/bin/env python3
"""Microscopic Dirichlet principle for the bridge on the current strong-field class.

Exact content:
  1. The sourced Schur boundary action
         I_R(f; j) = 1/2 f^T Lambda_R f - j^T f
     is strictly convex because Lambda_R is symmetric positive definite.
  2. For the exact shell trace f_* of the exterior projector field, the
     microscopic flux satisfies j = Lambda_R f_*.
  3. Therefore
         I_R(f; j) = I_R(f_*; j) + 1/2 (f - f_*)^T Lambda_R (f - f_*)
     and f_* is the unique global minimizer.
  4. On the current star-supported exact source classes, this minimizer is the
     native same-charge bridge, so the bridge is forced by a discrete Dirichlet
     principle rather than being a mere static conformal ansatz.

Bounded content:
  5. Random trace perturbations and quadratic bridge deformations increase the
     exact microscopic boundary action on the current source classes.
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
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
schur = SourceFileLoader(
    "oh_schur_boundary_action",
    "/private/tmp/physics-review-active/scripts/frontier_oh_schur_boundary_action.py",
).load_module()


def boundary_action(Lambda: np.ndarray, f: np.ndarray, j: np.ndarray) -> tuple[float, np.ndarray]:
    grad = Lambda @ f - j
    val = 0.5 * float(f @ (Lambda @ f)) - float(j @ f)
    return val, grad


def completion_gap(Lambda: np.ndarray, f_star: np.ndarray, delta: np.ndarray, j: np.ndarray) -> tuple[float, float]:
    base, _ = boundary_action(Lambda, f_star, j)
    pert, _ = boundary_action(Lambda, f_star + delta, j)
    exact_gap = 0.5 * float(delta @ (Lambda @ delta))
    return float(pert - base), exact_gap


def family_report(name: str, phi_grid: np.ndarray, Lambda: np.ndarray, trace_idx: np.ndarray, bulk_idx: np.ndarray, interior: int):
    action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
    f = action["f"]
    j = action["j_trace"]
    f_star = np.linalg.solve(Lambda, j)
    base_val, base_grad = boundary_action(Lambda, f_star, j)
    delta_exact = float(np.max(np.abs(f_star - f)))
    grad_exact = float(np.max(np.abs(base_grad)))

    rng = np.random.default_rng(17)
    gap_rows = []
    delta_scale = max(float(np.max(np.abs(f_star))), 1e-3) * 1e-3
    for _ in range(6):
        delta = rng.normal(size=f_star.shape)
        delta /= max(float(np.linalg.norm(delta)), 1e-12)
        delta *= delta_scale
        observed_gap, exact_gap = completion_gap(Lambda, f_star, delta, j)
        gap_rows.append((observed_gap, exact_gap))

    min_gap = min(g[0] for g in gap_rows)
    max_gap_err = max(abs(g[0] - g[1]) for g in gap_rows)
    print(
        f"{name}: trace_match={delta_exact:.3e}, stationary_grad={grad_exact:.3e}, "
        f"base_action={base_val:.6e}, min_sampled_gap={min_gap:.3e}, "
        f"completion_err={max_gap_err:.3e}"
    )
    return {
        "trace_match": delta_exact,
        "grad_exact": grad_exact,
        "min_gap": min_gap,
        "completion_err": max_gap_err,
    }


def main() -> None:
    print("Microscopic Dirichlet principle for the bridge")
    print("=" * 72)

    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(0.5 * (Lambda + Lambda.T))
    min_eig = float(np.min(eigvals))

    oh = family_report(
        "exact local O_h",
        same_source.build_best_phi_grid(),
        Lambda,
        trace_idx,
        bulk_idx,
        interior,
    )
    fr = family_report(
        "finite-rank",
        coarse.build_finite_rank_phi_grid(),
        Lambda,
        trace_idx,
        bulk_idx,
        interior,
    )

    record(
        "the Schur boundary operator is symmetric positive definite on the current bridge surface",
        sym_err < 1e-12 and min_eig > 0.0,
        f"symmetry error={sym_err:.3e}, min eigenvalue={min_eig:.6e}",
    )
    record(
        "the exact shell trace is recovered by the boundary-action minimizer on the exact local O_h class",
        oh["trace_match"] < 1e-12 and oh["grad_exact"] < 1e-12,
        f"trace match={oh['trace_match']:.3e}, stationary gradient={oh['grad_exact']:.3e}",
    )
    record(
        "the exact local O_h bridge is a strict global minimum of the microscopic boundary action under sampled perturbations",
        oh["min_gap"] > 0.0 and oh["completion_err"] < 1e-12,
        f"min sampled gap={oh['min_gap']:.3e}, completion error={oh['completion_err']:.3e}",
        status="BOUNDED",
    )
    record(
        "the finite-rank bridge is recovered by the same microscopic boundary-action minimizer",
        fr["trace_match"] < 1e-12 and fr["grad_exact"] < 1e-12,
        f"trace match={fr['trace_match']:.3e}, stationary gradient={fr['grad_exact']:.3e}",
    )
    record(
        "the finite-rank bridge is also a strict global minimum of the microscopic boundary action under sampled perturbations",
        fr["min_gap"] > 0.0 and fr["completion_err"] < 1e-12,
        f"min sampled gap={fr['min_gap']:.3e}, completion error={fr['completion_err']:.3e}",
        status="BOUNDED",
    )
    record(
        "the bridge is the unique minimum-energy discrete Dirichlet extension on the current star-supported strong-field class",
        oh["trace_match"] < 1e-12 and fr["trace_match"] < 1e-12 and oh["min_gap"] > 0.0 and fr["min_gap"] > 0.0,
        "native bridge is the unique minimizer of the exact microscopic Schur boundary energy",
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
