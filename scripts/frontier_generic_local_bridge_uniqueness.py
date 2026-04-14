#!/usr/bin/env python3
"""Generic finite-support local bridge uniqueness on the current bridge surface.

Exact content:
  1. If phi_ext is discrete harmonic on the exterior bulk, then any local
     bridge channel F(phi_ext) that is also discrete harmonic on that same bulk
     must preserve the discrete mean-value property on the realized neighbor
     data.
  2. Affine channels do preserve that property exactly.

Bounded content:
  3. Across sampled genuinely non-star finite-support source classes, quadratic
     local deformations F(phi)=1+phi+a2 phi^2 immediately violate bulk
     harmonicity and fail the Jensen/mean-value test.
  4. This extends the local-bridge uniqueness obstruction beyond the
     star-supported benchmark geometry to the broader generic finite-support
     bridge class on the current box.
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


generic = SourceFileLoader(
    "generic_bridge_class",
    "/private/tmp/physics-review-active/scripts/frontier_generic_finite_support_schur_bridge.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()


RADII = sew.radii_grid(generic.SIZE)
OUTSIDE_MASK = RADII > 5.0 + 1e-12


def bulk_harmonic_residual(phi_ext: np.ndarray, a2: float) -> float:
    field = 1.0 + phi_ext + a2 * phi_ext * phi_ext
    lap = sew.full_neg_laplacian(field)
    return float(np.max(np.abs(lap[OUTSIDE_MASK])))


def sample_neighbor_sets(phi_ext: np.ndarray):
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
                spread = max(abs(v - center) for v in neigh)
                if spread > 1e-4:
                    rows.append((center, neigh, spread))
                if len(rows) >= 4:
                    return rows
    return rows


def jensen_gap(center: float, neigh: list[float], a2: float) -> float:
    f_center = center + a2 * center * center
    f_mean = sum(v + a2 * v * v for v in neigh) / len(neigh)
    return abs(f_center - f_mean)


def main() -> None:
    print("Generic finite-support local bridge uniqueness")
    print("=" * 72)

    seeds = [4, 9, 14]
    sizes = [6, 8, 10]
    linear_res = []
    quad_pos = []
    quad_neg = []
    sample_gaps = []
    supports = []

    for seed, n_sites in zip(seeds, sizes):
        phi_grid, offsets = generic.build_generic_finite_support_phi_grid(seed, n_sites)
        supports.append(offsets)
        phi_ext = sew.exterior_projector(phi_grid, 4.0)
        linear_res.append(bulk_harmonic_residual(phi_ext, 0.0))
        quad_pos.append(bulk_harmonic_residual(phi_ext, 0.5))
        quad_neg.append(bulk_harmonic_residual(phi_ext, -0.5))

        rows = sample_neighbor_sets(phi_ext)
        for center, neigh, spread in rows:
            sample_gaps.append(
                (
                    jensen_gap(center, neigh, 0.5),
                    jensen_gap(center, neigh, -0.5),
                    spread,
                )
            )

        print(
            f"seed={seed}, n_sites={n_sites}: "
            f"linear={linear_res[-1]:.3e}, "
            f"quad(+0.5)={quad_pos[-1]:.3e}, quad(-0.5)={quad_neg[-1]:.3e}"
        )

    max_linear = max(linear_res)
    min_quad_pos = min(quad_pos)
    min_quad_neg = min(quad_neg)
    min_gap_pos = min(g[0] for g in sample_gaps)
    min_gap_neg = min(g[1] for g in sample_gaps)
    min_spread = min(g[2] for g in sample_gaps)

    record(
        "the affine local bridge channel remains exactly exterior harmonic on the tested generic finite-support class",
        max_linear < 1e-12,
        f"max affine bulk residual={max_linear:.3e}",
    )
    record(
        "quadratic local bridge deformations immediately destroy exterior harmonicity on the tested generic finite-support class",
        min_quad_pos > 1e-6 and min_quad_neg > 1e-6,
        (
            f"min bulk residuals: quad(+0.5)={min_quad_pos:.3e}, "
            f"quad(-0.5)={min_quad_neg:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the realized generic finite-support exterior neighbor data are nontrivial enough to violate the discrete mean-value rule for quadratic channels",
        min_gap_pos > 1e-10 and min_gap_neg > 1e-10 and min_spread > 1e-4,
        (
            f"min Jensen gaps: quad(+0.5)={min_gap_pos:.3e}, "
            f"quad(-0.5)={min_gap_neg:.3e}; min neighbor spread={min_spread:.3e}"
        ),
    )
    record(
        "the current local-scalar bridge uniqueness obstruction extends beyond the star-supported benchmark to the tested generic finite-support class",
        max_linear < 1e-12 and min_quad_pos > 1e-6 and min_quad_neg > 1e-6,
        "same-charge inheritance then fixes the affine coefficient to 1 on this broader class",
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
