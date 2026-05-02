#!/usr/bin/env python3
"""
PR #230 scalar zero-mode limit-order theorem.

The previous ladder blocks showed finite pole and residue witnesses are
zero-mode/IR sensitive.  This runner isolates the exact reason in the current
Wilson-exchange ladder model: the retained gauge zero mode contributes a
positive diagonal term proportional to 1 / (V mu_IR^2).  Taking the IR
regulator to zero before the finite-volume limit, taking volume first, or
scaling mu_IR with the box gives different scalar-channel denominators.

This is an exact negative boundary, not closure.  It names the missing theorem:
a retained gauge fixing / zero-mode / finite-volume / IR limiting prescription
for the interacting scalar denominator before the LSZ derivative can be
load-bearing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from frontier_yt_scalar_ladder_ir_zero_mode_obstruction import (
    ROOT,
    largest_eigenvalue,
    momentum_grid,
    projector_values,
)


OUTPUT = ROOT / "outputs" / "yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json"

PARENTS = {
    "derivative_limit": ROOT / "outputs" / "yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
    "residue_envelope": ROOT / "outputs" / "yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
    "kernel_ward": ROOT / "outputs" / "yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def fermion_weights(size: int, mass: float, projector: str) -> np.ndarray:
    momenta = momentum_grid(size)
    fermion_den = mass * mass + np.sum(np.sin(momenta) ** 2, axis=1)
    proj = projector_values(momenta, projector)
    return (proj * proj) / (fermion_den * fermion_den)


def zero_mode_diagonal(size: int, mass: float, projector: str, ir_mu_sq: float) -> np.ndarray:
    color_factor = 4.0 / 3.0
    volume = float(size**4)
    return color_factor * fermion_weights(size, mass, projector) / (volume * ir_mu_sq)


def ladder_matrix(
    *,
    size: int,
    mass: float,
    ir_mu_sq: float,
    projector: str,
    remove_zero_mode: bool,
) -> np.ndarray:
    momenta = momentum_grid(size)
    weights = fermion_weights(size, mass, projector)
    sqrt_w = np.sqrt(weights)
    n = len(momenta)
    kernel = np.empty((n, n), dtype=float)
    for idx, k in enumerate(momenta):
        dq = k - momenta
        q_hat_sq = np.sum((2.0 * np.sin(dq / 2.0)) ** 2, axis=1)
        row = 1.0 / (q_hat_sq + ir_mu_sq)
        if remove_zero_mode:
            row = row.copy()
            row[q_hat_sq < 1.0e-14] = 0.0
        kernel[idx, :] = row

    color_factor = 4.0 / 3.0
    matrix = color_factor * (sqrt_w[:, None] * kernel * sqrt_w[None, :]) / n
    return 0.5 * (matrix + matrix.T)


def power_slope(x0: float, y0: float, x1: float, y1: float) -> float:
    return math.log(abs(y1) / abs(y0)) / math.log(x1 / x0)


def load_parent(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 scalar zero-mode limit-order theorem")
    print("=" * 72)

    mass = 0.50
    projector = "local"
    size_for_decomposition = 3
    mu_for_decomposition = 0.10

    parent_data = {name: load_parent(path) for name, path in PARENTS.items()}

    included = ladder_matrix(
        size=size_for_decomposition,
        mass=mass,
        ir_mu_sq=mu_for_decomposition,
        projector=projector,
        remove_zero_mode=False,
    )
    removed = ladder_matrix(
        size=size_for_decomposition,
        mass=mass,
        ir_mu_sq=mu_for_decomposition,
        projector=projector,
        remove_zero_mode=True,
    )
    difference = included - removed
    expected_diag = zero_mode_diagonal(
        size_for_decomposition,
        mass,
        projector,
        mu_for_decomposition,
    )
    off_diagonal = difference - np.diag(np.diag(difference))
    max_offdiag_abs = float(np.max(np.abs(off_diagonal)))
    max_diag_error = float(np.max(np.abs(np.diag(difference) - expected_diag)))

    fixed_n = 4
    mu_values = [0.20, 0.10, 0.05, 0.02, 0.01]
    fixed_volume_zero_mode = [
        {
            "grid_size_4d": fixed_n,
            "ir_mu_sq": mu,
            "zero_mode_max_diagonal": float(np.max(zero_mode_diagonal(fixed_n, mass, projector, mu))),
        }
        for mu in mu_values
    ]
    mu_scaled_products = [
        row["ir_mu_sq"] * row["zero_mode_max_diagonal"] for row in fixed_volume_zero_mode
    ]
    product_spread = max(mu_scaled_products) / min(mu_scaled_products)

    sizes = [4, 5, 6, 8]
    paths: dict[str, list[dict[str, float]]] = {
        "fixed_mu2_0_10": [],
        "mu2_scaled_as_N_minus_2": [],
        "mu2_scaled_as_N_minus_4": [],
        "mu2_scaled_as_N_minus_6": [],
    }
    for size in sizes:
        path_mus = {
            "fixed_mu2_0_10": 0.10,
            "mu2_scaled_as_N_minus_2": 0.10 * (4.0 / size) ** 2,
            "mu2_scaled_as_N_minus_4": 0.10 * (4.0 / size) ** 4,
            "mu2_scaled_as_N_minus_6": 0.10 * (4.0 / size) ** 6,
        }
        for path_name, mu in path_mus.items():
            paths[path_name].append(
                {
                    "grid_size_4d": float(size),
                    "ir_mu_sq": float(mu),
                    "zero_mode_max_diagonal": float(np.max(zero_mode_diagonal(size, mass, projector, mu))),
                }
            )

    fixed_mu_drop = paths["fixed_mu2_0_10"][0]["zero_mode_max_diagonal"] / paths["fixed_mu2_0_10"][-1]["zero_mode_max_diagonal"]
    nminus4_spread = (
        max(row["zero_mode_max_diagonal"] for row in paths["mu2_scaled_as_N_minus_4"])
        / min(row["zero_mode_max_diagonal"] for row in paths["mu2_scaled_as_N_minus_4"])
    )
    nminus6_growth = paths["mu2_scaled_as_N_minus_6"][-1]["zero_mode_max_diagonal"] / paths["mu2_scaled_as_N_minus_6"][0]["zero_mode_max_diagonal"]

    included_low_mu = largest_eigenvalue(
        size=fixed_n,
        mass=mass,
        ir_mu_sq=0.01,
        projector_mode=projector,
        remove_zero_mode=False,
    )
    removed_low_mu = largest_eigenvalue(
        size=fixed_n,
        mass=mass,
        ir_mu_sq=0.01,
        projector_mode=projector,
        remove_zero_mode=True,
    )
    zero_mode_lower_bound = float(np.max(zero_mode_diagonal(fixed_n, mass, projector, 0.01)))
    included_removed_split = included_low_mu / removed_low_mu

    fixed_volume_ir_slope = power_slope(
        mu_values[0],
        fixed_volume_zero_mode[0]["zero_mode_max_diagonal"],
        mu_values[-1],
        fixed_volume_zero_mode[-1]["zero_mode_max_diagonal"],
    )

    report(
        "parent-obstructions-loaded",
        all(data.get("proposal_allowed") is False for data in parent_data.values()),
        ", ".join(f"{name}={bool(data)}" for name, data in parent_data.items()),
    )
    report(
        "zero-mode-decomposition-is-exact-diagonal",
        max_offdiag_abs < 1.0e-12 and max_diag_error < 1.0e-12,
        f"max_offdiag={max_offdiag_abs:.3e}, max_diag_error={max_diag_error:.3e}",
    )
    report(
        "fixed-volume-zero-mode-diverges-as-one-over-mu2",
        fixed_volume_ir_slope < -0.99 and fixed_volume_ir_slope > -1.01 and product_spread < 1.0 + 1.0e-12,
        f"slope={fixed_volume_ir_slope:.6g}, mu2_product_spread={product_spread:.6g}",
    )
    report(
        "volume-first-limit-removes-zero-mode-at-fixed-ir",
        fixed_mu_drop > 10.0,
        f"N4/N8 zero-mode diagonal ratio={fixed_mu_drop:.6g}",
    )
    report(
        "box-scaled-ir-path-keeps-zero-mode-finite",
        nminus4_spread < 1.0 + 1.0e-12,
        f"N^-4 path spread={nminus4_spread:.6g}",
    )
    report(
        "faster-ir-scaling-makes-zero-mode-grow-with-volume",
        nminus6_growth > 3.5,
        f"N8/N4 zero-mode diagonal ratio on N^-6 path={nminus6_growth:.6g}",
    )
    report(
        "included-kernel-bounded-below-by-zero-mode-piece",
        included_low_mu >= zero_mode_lower_bound and included_removed_split > 10.0,
        f"lambda_included={included_low_mu:.6g}, zero_bound={zero_mode_lower_bound:.6g}, included/removed={included_removed_split:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "different allowed IR/volume paths give different scalar denominators until a gauge-fixing/limit theorem is supplied",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar zero-mode limit-order theorem",
        "verdict": (
            "In the current finite Wilson-exchange scalar ladder, retaining the "
            "gauge zero mode adds an exact positive diagonal term proportional "
            "to 1/(V mu_IR^2).  Therefore the scalar-channel denominator has "
            "path-dependent IR/finite-volume behavior: mu_IR -> 0 at fixed "
            "volume diverges, volume -> infinity at fixed mu_IR removes the "
            "zero-mode contribution, and box-scaled regulators can leave a "
            "finite or growing zero-mode term.  The current surface has no "
            "retained rule selecting one path, so the scalar LSZ derivative and "
            "FH/LSZ readout remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The zero-mode/IR/finite-volume limiting prescription is a "
            "load-bearing open premise for the interacting scalar denominator."
        ),
        "parent_certificates": {name: str(path.relative_to(ROOT)) for name, path in PARENTS.items()},
        "exact_decomposition_witness": {
            "grid_size_4d": size_for_decomposition,
            "mass": mass,
            "projector": projector,
            "ir_mu_sq": mu_for_decomposition,
            "max_offdiag_abs": max_offdiag_abs,
            "max_diag_error": max_diag_error,
        },
        "fixed_volume_zero_mode": fixed_volume_zero_mode,
        "volume_ir_paths": paths,
        "witnesses": {
            "fixed_volume_ir_power_slope": fixed_volume_ir_slope,
            "mu2_times_zero_mode_diagonal_spread": product_spread,
            "fixed_mu_N4_over_N8_zero_mode_ratio": fixed_mu_drop,
            "N_minus_4_path_spread": nminus4_spread,
            "N_minus_6_path_N8_over_N4_ratio": nminus6_growth,
            "included_low_mu_lambda": included_low_mu,
            "removed_low_mu_lambda": removed_low_mu,
            "zero_mode_lower_bound_low_mu": zero_mode_lower_bound,
            "included_over_removed_low_mu": included_removed_split,
        },
        "required_next_theorem": [
            "derive the gauge fixing and zero-mode prescription for the scalar-channel kernel",
            "derive the finite-volume and IR limiting order before using the scalar denominator",
            "prove convergence of the pole location and inverse-propagator derivative in that selected limit",
            "or measure the same-source scalar pole derivative on production ensembles with the prescription fixed",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as selectors",
            "does not use alpha_LM, plaquette, u0, or reduced pilots as proof inputs",
            "does not set c2 = 1 or Z_match = 1",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
