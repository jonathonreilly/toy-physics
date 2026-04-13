#!/usr/bin/env python3
"""Exact discrete shell action for the local O_h sewing law.

Exact content:
  1. The exact rank-one reduced junction operator determines a unit-charge
     reduced shell vector v_red.
  2. After charge-normalizing the reduced shell data, the quadratic
     reduced shell functional
         J(z) = 1/2 || z - v_red ||^2
     has Euler-Lagrange equation z = v_red.
  3. On the exact local O_h source class, the zero within-orbit spread on
     3 < r <= 5 lifts this reduced stationarity condition to the exact
     pointwise shell law.

Bounded content:
  4. On the broader exact finite-rank source family, the same reduced action
     stays small, but the pointwise lift is only approximate because the
     within-orbit spread is bounded rather than zero.
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


rj = SourceFileLoader(
    "reduced_junction",
    "/private/tmp/physics-review-active/scripts/frontier_reduced_junction_operator.py",
).load_module()
oh = SourceFileLoader(
    "oh_pointwise_shell",
    "/private/tmp/physics-review-active/scripts/frontier_oh_pointwise_shell_closure.py",
).load_module()
same = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()


def reduced_action(z: np.ndarray, ref_vec: np.ndarray) -> tuple[float, np.ndarray]:
    resid = z - ref_vec
    return 0.5 * float(np.dot(resid, resid)), resid


def perturbation_gain(
    z: np.ndarray, ref_vec: np.ndarray, idx: int, eps: float = 1e-4
) -> float:
    base, _ = reduced_action(z, ref_vec)
    trial = z.copy()
    trial[idx] += eps
    lifted, _ = reduced_action(trial, ref_vec)
    return lifted - base


def analyze_family(label: str, phi_grid: np.ndarray, ref_vec: np.ndarray):
    charge, z = rj.reduced_vector(phi_grid)
    action, resid = reduced_action(z, ref_vec)
    max_resid = float(np.max(np.abs(resid)))
    oh_abs, oh_rel = oh.pointwise_orbit_spreads(phi_grid)
    return {
        "label": label,
        "charge": charge,
        "action": action,
        "max_resid": max_resid,
        "orbit_abs": oh_abs,
        "orbit_rel": oh_rel,
        "z": z,
    }


def main() -> None:
    print("Exact discrete shell action on the local O_h sewing law")
    print("=" * 72)

    columns, _, _ = rj.star.build_point_green_columns(15)
    ref_charge, ref_vec = rj.reduced_vector(columns[0])
    if abs(ref_charge - 1.0) > 1e-12:
        raise RuntimeError(f"unexpected unit-charge reference column: Q={ref_charge}")

    exact_oh = analyze_family("exact local O_h", same.build_best_phi_grid(), ref_vec)
    exact_fr = analyze_family("exact finite-rank", coarse.build_finite_rank_phi_grid(), ref_vec)

    gains = [perturbation_gain(exact_oh["z"], ref_vec, idx) for idx in [0, 7, 23]]

    print(f"reference unit-charge reduced vector length = {len(ref_vec)}")
    print(f"exact local O_h action = {exact_oh['action']:.3e}")
    print(f"exact finite-rank action = {exact_fr['action']:.3e}")
    print(
        "exact local O_h orbit spreads: "
        + ", ".join(f"{k}={v:.3e}" for k, v in exact_oh["orbit_abs"].items())
    )
    print(
        "finite-rank orbit spreads: "
        + ", ".join(f"{k}={v:.3e}" for k, v in exact_fr["orbit_abs"].items())
    )
    print(
        "sample quadratic gains under reduced-coordinate perturbations: "
        + ", ".join(f"{g:.3e}" for g in gains)
    )

    record(
        "the exact local O_h reduced shell data satisfy the stationary quadratic shell action",
        exact_oh["action"] < 1e-12 and exact_oh["max_resid"] < 1e-12,
        f"action={exact_oh['action']:.3e}, max residual={exact_oh['max_resid']:.3e}",
    )
    record(
        "the exact local O_h shell action lifts pointwise on 3 < r <= 5",
        all(v < 1e-12 for v in exact_oh["orbit_abs"].values()),
        (
            "orbit spreads: "
            + ", ".join(f"{k}={v:.3e}" for k, v in exact_oh["orbit_abs"].items())
        ),
    )
    record(
        "the reduced shell action has a unique local minimum at the exact O_h reduced junction law",
        all(g > 0.0 for g in gains),
        "sample perturbation gains are strictly positive",
        status="BOUNDED",
    )
    record(
        "the broader finite-rank family stays close to the same reduced shell action but is not pointwise exact",
        exact_fr["action"] < 1e-12 and max(exact_fr["orbit_rel"].values()) < 0.03,
        (
            f"action={exact_fr['action']:.3e}, "
            + ", ".join(f"{k}={100*v:.4f}%" for k, v in exact_fr["orbit_rel"].items())
        ),
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
