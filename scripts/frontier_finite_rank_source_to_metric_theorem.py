#!/usr/bin/env python3
"""Finite-rank source-to-metric theorem path via exact boundary action.

This runner avoids the current eta_floor_tf tensor-endpoint route.

Exact content:
  1. The finite-rank source family determines an exact renormalized exterior
     harmonic field through the Woodbury/Dyson identity.
  2. The same finite-rank shell trace is a stationary point of the exact
     microscopic Schur boundary action on the current bridge surface.

Bounded content:
  3. Shell-averaging the exact finite-rank exterior field yields a monopole- 
     dominated radial harmonic law phi_eff(r) = a/r.
  4. The corresponding isotropic metric candidate is vacuum-close, but the
     direct same-source metric still carries a nonzero Einstein residual.
  5. Therefore the finite-rank family supports a clean scalar source-to-metric
     path, but not full tensorial `3+1` closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent.parent


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
    str(ROOT / "scripts" / "frontier_finite_rank_gravity_residual.py"),
).load_module()
coarse = SourceFileLoader(
    "coarse_grained_exterior_law",
    str(ROOT / "scripts" / "frontier_coarse_grained_exterior_law.py"),
).load_module()
schur = SourceFileLoader(
    "oh_schur_boundary_action",
    str(ROOT / "scripts" / "frontier_oh_schur_boundary_action.py"),
).load_module()


def boundary_stationarity_report(phi_grid: np.ndarray):
    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
    f = action["f"]
    j = action["j_trace"]
    grad = Lambda @ f - j
    return {
        "rebuild_err": float(action["rebuild_err"]),
        "flux_err": float(action["flux_err"]),
        "stationary_grad": float(np.max(np.abs(grad))),
    }


def coarse_metric_report(phi_grid: np.ndarray):
    rows = coarse.analyze_family("exact finite-rank", phi_grid)
    best = min(rows, key=lambda row: row[5])
    return {
        "rows": rows,
        "best": best,
        "improvement": float(best[4] / max(best[5], 1e-15)),
    }


def main() -> int:
    print("FINITE-RANK SOURCE-TO-METRIC THEOREM PATH")
    print("=" * 78)

    phi_full, support, interior, q_eff = finite_rank.exact_finite_rank_field()
    print(f"support size={len(support)}, q_eff_sum={np.sum(q_eff):.8f}")

    boundary = boundary_stationarity_report(phi_full)
    coarse_report = coarse_metric_report(phi_full)
    best = coarse_report["best"]

    record(
        "the exact finite-rank source field is recovered by the Woodbury-compressed exterior solve",
        boundary["rebuild_err"] < 1e-12,
        f"boundary reconstruction error={boundary['rebuild_err']:.3e}",
    )
    record(
        "the exact finite-rank shell trace is stationary for the microscopic Schur boundary action",
        boundary["flux_err"] < 1e-12 and boundary["stationary_grad"] < 1e-12,
        (
            f"flux_err={boundary['flux_err']:.3e}, "
            f"stationary_grad={boundary['stationary_grad']:.3e}"
        ),
    )
    record(
        "the finite-rank family admits a vacuum-close coarse-grained isotropic exterior metric",
        best[5] < 1e-5,
        (
            f"R_match={best[0]:.1f}, a={best[1]:.6f}, shell_rms={best[2]:.3f}, "
            f"direct={best[4]:.3e}, coarse={best[5]:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the coarse-grained isotropic candidate strongly improves the finite-rank `3+1` residual",
        best[4] > 1e-3 and coarse_report["improvement"] > 1e3,
        (
            f"direct={best[4]:.3e}, coarse={best[5]:.3e}, "
            f"improvement={coarse_report['improvement']:.1f}x"
        ),
        status="BOUNDED",
    )

    print("\n" + "=" * 78)
    print("BLOCKER")
    print("=" * 78)
    print(
        "The finite-rank family still does not supply an exact tensorial `3+1` matching "
        "map. The direct common-source metric remains nonzero, so this route closes "
        "the scalar exterior architecture but not full nonlinear GR."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
