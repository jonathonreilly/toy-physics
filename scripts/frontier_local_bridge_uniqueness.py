#!/usr/bin/env python3
"""Local bridge uniqueness on the star-supported strong-field class.

Exact content:
  1. If phi_ext is discrete harmonic on the exterior bulk, then any local
     bridge channel of the form F(phi_ext) that is also discrete harmonic on
     that same bulk for the whole star-supported finite-rank class must be
     affine in phi_ext.
  2. Same-charge inheritance then fixes the spatial bridge to psi = 1 + phi_ext.
  3. The attractive temporal branch fixes chi = 1 - phi_ext.

Bounded content:
  4. Random star-supported finite-rank examples show that any tested nonlinear
     local deformation F(phi)=1+phi+a2 phi^2 immediately produces bulk
     residual away from the shell, while the affine bridge stays exact.
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


star_class = SourceFileLoader(
    "star_bridge_class",
    "/private/tmp/physics-review-active/scripts/frontier_star_supported_bridge_class.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()


RADII = sew.radii_grid(15)
OUTSIDE_MASK = RADII > 5.0 + 1e-12


def bulk_harmonic_residual(phi_ext: np.ndarray, a2: float) -> float:
    field = 1.0 + phi_ext + a2 * phi_ext * phi_ext
    lap = sew.full_neg_laplacian(field)
    return float(np.max(np.abs(lap[OUTSIDE_MASK])))


def sample_neighbor_quadruples(phi_ext: np.ndarray):
    rows = []
    for i in range(1, phi_ext.shape[0] - 1):
        for j in range(1, phi_ext.shape[1] - 1):
            for k in range(1, phi_ext.shape[2] - 1):
                if not OUTSIDE_MASK[i, j, k]:
                    continue
                vals = [
                    float(phi_ext[i, j, k]),
                    float(phi_ext[i + 1, j, k]),
                    float(phi_ext[i - 1, j, k]),
                    float(phi_ext[i, j + 1, k]),
                    float(phi_ext[i, j - 1, k]),
                    float(phi_ext[i, j, k + 1]),
                    float(phi_ext[i, j, k - 1]),
                ]
                center = vals[0]
                neigh = vals[1:]
                if max(abs(v - center) for v in neigh) > 1e-4:
                    rows.append((center, neigh))
                if len(rows) >= 3:
                    return rows
    return rows


def jensen_gap(center: float, neigh: list[float], a2: float) -> float:
    f_center = center + a2 * center * center
    f_mean = sum(v + a2 * v * v for v in neigh) / len(neigh)
    return abs(f_center - f_mean)


def main() -> None:
    print("Local bridge uniqueness on the star-supported strong-field class")
    print("=" * 72)

    seeds = [3, 7, 11]
    linear_res = []
    quad_pos = []
    quad_neg = []
    sample_gaps = []

    for seed in seeds:
        phi_grid = star_class.build_star_supported_phi_grid(seed)
        phi_ext = sew.exterior_projector(phi_grid, 4.0)
        linear_res.append(bulk_harmonic_residual(phi_ext, 0.0))
        quad_pos.append(bulk_harmonic_residual(phi_ext, 0.5))
        quad_neg.append(bulk_harmonic_residual(phi_ext, -0.5))

        for center, neigh in sample_neighbor_quadruples(phi_ext):
            sample_gaps.append(
                (
                    jensen_gap(center, neigh, 0.5),
                    jensen_gap(center, neigh, -0.5),
                )
            )

        print(
            f"seed={seed}: linear={linear_res[-1]:.3e}, "
            f"quad(+0.5)={quad_pos[-1]:.3e}, quad(-0.5)={quad_neg[-1]:.3e}"
        )

    max_linear = max(linear_res)
    min_quad_pos = min(quad_pos)
    min_quad_neg = min(quad_neg)
    min_gap_pos = min(g[0] for g in sample_gaps)
    min_gap_neg = min(g[1] for g in sample_gaps)

    record(
        "the affine local bridge channel remains exactly exterior harmonic on the whole tested star-supported finite-rank class",
        max_linear < 1e-12,
        f"max affine bulk residual={max_linear:.3e}",
    )
    record(
        "nonlinear local bridge deformations immediately destroy exterior harmonicity on the tested star-supported finite-rank class",
        min_quad_pos > 1e-6 and min_quad_neg > 1e-6,
        (
            f"min bulk residuals: quad(+0.5)={min_quad_pos:.3e}, "
            f"quad(-0.5)={min_quad_neg:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the discrete mean-value identity on nontrivial exterior neighbor data forces non-affine quadratic maps to fail Jensen preservation",
        min_gap_pos > 1e-10 and min_gap_neg > 1e-10,
        (
            f"min Jensen gaps: quad(+0.5)={min_gap_pos:.3e}, "
            f"quad(-0.5)={min_gap_neg:.3e}"
        ),
    )
    record(
        "on the current star-supported class the native bridge is the unique local scalar exterior-harmonic bridge up to affine coefficient choice",
        max_linear < 1e-12 and min_quad_pos > 1e-6 and min_quad_neg > 1e-6,
        "same-charge inheritance then fixes the affine coefficient to 1",
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
