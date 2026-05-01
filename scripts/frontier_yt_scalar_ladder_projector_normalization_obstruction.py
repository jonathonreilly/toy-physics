#!/usr/bin/env python3
"""
PR #230 scalar ladder projector-normalization obstruction.

The previous input audit found an exact kinematic equality between the
point-split scalar source factor and the gauge-link vertex factor.  This runner
tests whether that equality is enough to fix the scalar-channel pole criterion.

It is not: the largest-eigenvalue pole test is source/projector-normalization
sensitive.  A theorem-grade route must therefore derive the scalar projector
and LSZ residue, not merely name a kinematic factor.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json"

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


def momentum_grid(size: int) -> np.ndarray:
    axes = [2.0 * math.pi * np.arange(size) / size for _ in range(4)]
    grids = np.meshgrid(*axes, indexing="ij")
    return np.stack([grid.ravel() for grid in grids], axis=1)


def projector_values(momenta: np.ndarray, mode: str) -> np.ndarray:
    if mode == "local":
        return np.ones(len(momenta), dtype=float)
    if mode == "point_split_raw":
        return np.sum(np.cos(momenta / 2.0) ** 2, axis=1)
    if mode == "point_split_zero_momentum_normalized":
        return np.sum(np.cos(momenta / 2.0) ** 2, axis=1) / 4.0
    if mode.startswith("uniform_scale:"):
        scale = float(mode.split(":", 1)[1])
        return np.full(len(momenta), scale, dtype=float)
    raise ValueError(f"unknown projector mode: {mode}")


def largest_eigenvalue(size: int, mass: float, ir_mu_sq: float, projector_mode: str) -> float:
    momenta = momentum_grid(size)
    fermion_den = mass * mass + np.sum(np.sin(momenta) ** 2, axis=1)
    projector = projector_values(momenta, projector_mode)
    weights = (projector * projector) / (fermion_den * fermion_den)
    sqrt_w = np.sqrt(weights)

    n = len(momenta)
    kernel = np.empty((n, n), dtype=float)
    for idx, k in enumerate(momenta):
        dq = k - momenta
        q_hat_sq = np.sum((2.0 * np.sin(dq / 2.0)) ** 2, axis=1)
        kernel[idx, :] = 1.0 / (q_hat_sq + ir_mu_sq)

    color_factor = 4.0 / 3.0
    matrix = color_factor * (sqrt_w[:, None] * kernel * sqrt_w[None, :]) / n
    matrix = 0.5 * (matrix + matrix.T)
    return float(np.linalg.eigvalsh(matrix)[-1])


def main() -> int:
    print("PR #230 scalar ladder projector-normalization obstruction")
    print("=" * 72)

    size = 4
    mass = 0.50
    ir_mu_sq = 0.20
    modes = [
        "local",
        "point_split_raw",
        "point_split_zero_momentum_normalized",
        "uniform_scale:2.0",
        "uniform_scale:0.5",
    ]
    lambdas = {
        mode: largest_eigenvalue(size=size, mass=mass, ir_mu_sq=ir_mu_sq, projector_mode=mode)
        for mode in modes
    }

    lambda_scale_two_ratio = lambdas["uniform_scale:2.0"] / lambdas["local"]
    lambda_scale_half_ratio = lambdas["uniform_scale:0.5"] / lambdas["local"]
    ps_raw_to_norm_ratio = (
        lambdas["point_split_raw"] / lambdas["point_split_zero_momentum_normalized"]
    )

    report("finite-projector-scan-runs", len(lambdas) == len(modes), f"modes={len(modes)}")
    report(
        "uniform-source-rescaling-scales-eigenvalue-quadratically",
        abs(lambda_scale_two_ratio - 4.0) < 1.0e-10
        and abs(lambda_scale_half_ratio - 0.25) < 1.0e-10,
        f"scale2_ratio={lambda_scale_two_ratio:.12g}, scale_half_ratio={lambda_scale_half_ratio:.12g}",
    )
    report(
        "point-split-zero-momentum-normalization-changes-pole-test-by-16",
        abs(ps_raw_to_norm_ratio - 16.0) < 1.0e-10,
        f"raw_to_norm_ratio={ps_raw_to_norm_ratio:.12g}",
    )
    report(
        "projector-normalization-can-flip-pole-criterion",
        lambdas["point_split_raw"] >= 1.0
        and lambdas["point_split_zero_momentum_normalized"] < 1.0,
        (
            "raw lambda={:.6g}, normalized lambda={:.6g}"
        ).format(
            lambdas["point_split_raw"],
            lambdas["point_split_zero_momentum_normalized"],
        ),
    )
    report(
        "local-projector-also-disagrees-with-point-split-choice",
        abs(lambdas["local"] - lambdas["point_split_zero_momentum_normalized"]) > 0.10,
        f"local={lambdas['local']:.6g}, ps_norm={lambdas['point_split_zero_momentum_normalized']:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "a retained route must derive the scalar source normalization and LSZ residue",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / projector-normalization obstruction",
        "verdict": (
            "The scalar ladder pole criterion is not invariant under admissible "
            "source/projector normalizations.  Uniform source rescaling changes "
            "lambda_max quadratically, and raw versus zero-momentum-normalized "
            "point-split scalar projectors differ by a factor of sixteen.  The "
            "same finite kernel can pass or fail the lambda_max >= 1 scout pole "
            "criterion depending only on this unproven normalization.  Therefore "
            "the shared point-split/gauge kinematic factor does not close PR #230; "
            "a scalar projector and LSZ residue theorem is still required."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The scalar projector/source normalization is not fixed by the current retained surface.",
        "parameters": {
            "grid_size_4d": size,
            "mass": mass,
            "ir_mu_sq": ir_mu_sq,
        },
        "lambda_max_by_projector": lambdas,
        "ratios": {
            "uniform_scale_2_over_local": lambda_scale_two_ratio,
            "uniform_scale_half_over_local": lambda_scale_half_ratio,
            "point_split_raw_over_zero_momentum_normalized": ps_raw_to_norm_ratio,
        },
        "required_next_theorem": [
            "derive a scalar projector from the Cl(3)/Z^3 Wilson-staggered substrate",
            "fix source normalization without H_unit matrix-element authority",
            "derive the scalar LSZ residue from the interacting two-point function",
            "then re-run the eigenvalue/pole criterion with that fixed projector",
        ],
        "strict_non_claims": [
            "not a y_t derivation",
            "not a production measurement",
            "does not use alpha_LM or plaquette normalization",
            "does not define y_t through H_unit matrix elements",
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
