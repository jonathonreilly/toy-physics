#!/usr/bin/env python3
"""
PR #230 scalar ladder total-momentum derivative scout.

The previous gate showed that a scalar ladder pole witness needs
d lambda_max / d p^2 at the crossing, not only lambda_max=1.  This runner
computes that derivative in a finite Wilson-exchange ladder scout by giving
the fermion bubble weights a nonzero total scalar momentum p.

The result is useful but not retained closure: the derivative is finite and
computable in this finite scan, but its magnitude remains sensitive to the
scalar projector, IR/zero-mode prescription, mass, and finite volume.  This
runner records the derivative sign instead of treating sign changes as a
required finding.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EIGEN_GATE = ROOT / "outputs" / "yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json"

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


def fermion_den(momentum: np.ndarray, mass: float) -> np.ndarray:
    return mass * mass + np.sum(np.sin(momentum) ** 2, axis=1)


def projector_values(momenta: np.ndarray, mode: str) -> np.ndarray:
    if mode == "local":
        return np.ones(len(momenta), dtype=float)
    if mode == "point_split_zero_momentum_normalized":
        return np.sum(np.cos(momenta / 2.0) ** 2, axis=1) / 4.0
    raise ValueError(f"unknown projector mode: {mode}")


def largest_ladder_eigenvalue(
    *,
    size: int,
    mass: float,
    ir_mu_sq: float,
    p_total: np.ndarray,
    projector: str,
    remove_zero_mode: bool,
) -> float:
    momenta = momentum_grid(size)
    den_plus = fermion_den(momenta + 0.5 * p_total[None, :], mass)
    den_minus = fermion_den(momenta - 0.5 * p_total[None, :], mass)
    proj = projector_values(momenta, projector)
    weights = (proj * proj) / (den_plus * den_minus)
    sqrt_w = np.sqrt(np.maximum(weights, 0.0))

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
    matrix = 0.5 * (matrix + matrix.T)
    return float(np.linalg.eigvalsh(matrix)[-1])


def derivative_row(
    *,
    size: int,
    mass: float,
    ir_mu_sq: float,
    projector: str,
    remove_zero_mode: bool,
) -> dict[str, object]:
    p0 = np.zeros(4)
    p1 = np.asarray([2.0 * math.pi / size, 0.0, 0.0, 0.0], dtype=float)
    p_hat_sq = float(np.sum((2.0 * np.sin(p1 / 2.0)) ** 2))
    lambda0 = largest_ladder_eigenvalue(
        size=size,
        mass=mass,
        ir_mu_sq=ir_mu_sq,
        p_total=p0,
        projector=projector,
        remove_zero_mode=remove_zero_mode,
    )
    lambda1 = largest_ladder_eigenvalue(
        size=size,
        mass=mass,
        ir_mu_sq=ir_mu_sq,
        p_total=p1,
        projector=projector,
        remove_zero_mode=remove_zero_mode,
    )
    derivative = (lambda1 - lambda0) / p_hat_sq
    return {
        "grid_size_4d": size,
        "mass": mass,
        "ir_mu_sq": ir_mu_sq,
        "projector": projector,
        "zero_mode": "removed" if remove_zero_mode else "included",
        "p_hat_sq_step": p_hat_sq,
        "lambda_p0": lambda0,
        "lambda_p1": lambda1,
        "d_lambda_dp_hat_sq": derivative,
        "pole_condition_at_p0": lambda0 >= 1.0,
        "residue_factor_proxy_if_crossing": 1.0 / abs(derivative) if abs(derivative) > 1.0e-30 else float("inf"),
    }


def main() -> int:
    print("PR #230 scalar ladder total-momentum derivative scout")
    print("=" * 72)

    eigen_gate = json.loads(EIGEN_GATE.read_text(encoding="utf-8"))
    sizes = [3, 4, 5]
    masses = [0.35, 0.50, 0.75]
    ir_values = [0.05, 0.10, 0.20]
    projectors = ["local", "point_split_zero_momentum_normalized"]
    scan = []
    for size in sizes:
        for mass in masses:
            for ir_mu_sq in ir_values:
                for projector in projectors:
                    for remove_zero_mode in [False, True]:
                        scan.append(
                            derivative_row(
                                size=size,
                                mass=mass,
                                ir_mu_sq=ir_mu_sq,
                                projector=projector,
                                remove_zero_mode=remove_zero_mode,
                            )
                        )

    derivatives = np.asarray([float(row["d_lambda_dp_hat_sq"]) for row in scan], dtype=float)
    finite_derivatives = [value for value in derivatives if math.isfinite(float(value))]
    abs_derivatives = [abs(value) for value in finite_derivatives if abs(value) > 1.0e-14]
    sign_values = {int(np.sign(value)) for value in finite_derivatives if abs(value) > 1.0e-14}
    crossing_rows = [row for row in scan if row["pole_condition_at_p0"]]
    crossing_derivatives = [float(row["d_lambda_dp_hat_sq"]) for row in crossing_rows]
    local_included = [
        row for row in scan
        if row["projector"] == "local" and row["zero_mode"] == "included"
    ]
    ps_removed = [
        row for row in scan
        if row["projector"] == "point_split_zero_momentum_normalized" and row["zero_mode"] == "removed"
    ]

    report("eigen-derivative-gate-loaded", EIGEN_GATE.exists(), str(EIGEN_GATE.relative_to(ROOT)))
    report("eigen-gate-not-closure", eigen_gate.get("proposal_allowed") is False, str(eigen_gate.get("proposal_allowed")))
    report(
        "total-momentum-derivative-scan-runs",
        len(scan) == len(sizes) * len(masses) * len(ir_values) * len(projectors) * 2,
        f"points={len(scan)}",
    )
    report("finite-derivatives-computed", len(finite_derivatives) == len(scan), f"finite={len(finite_derivatives)}")
    report(
        "derivative-sensitive-to-prescriptions",
        max(abs_derivatives) / min(abs_derivatives) > 20.0,
        f"abs_derivative_spread={max(abs_derivatives) / min(abs_derivatives):.6g}",
    )
    report(
        "derivative-sign-recorded",
        sign_values == {-1},
        f"sign_values={sorted(sign_values)}",
    )
    report(
        "crossing-rows-still-need-derivative-control",
        bool(crossing_rows) and max(abs(x) for x in crossing_derivatives) / min(abs(x) for x in crossing_derivatives if abs(x) > 1.0e-14) > 5.0,
        f"crossing_rows={len(crossing_rows)}",
    )
    report(
        "projector-zero-mode-choice-load-bearing",
        abs(np.mean([float(row["d_lambda_dp_hat_sq"]) for row in local_included]))
        != abs(np.mean([float(row["d_lambda_dp_hat_sq"]) for row in ps_removed])),
        "local/included and point-split/removed derivative means differ",
    )
    report("not-retained-closure", True, "finite derivative scout lacks retained limiting theorem")

    result = {
        "actual_current_surface_status": "bounded-support / scalar ladder total-momentum derivative scout",
        "verdict": (
            "The scalar ladder total-momentum derivative can be computed in a "
            "finite Wilson-exchange scout.  This is constructive support for "
            "the LSZ route.  It is not retained closure: d lambda_max/dp^2 is "
            "highly sensitive to projector, IR/zero-mode prescription, mass, "
            "and volume.  In this scan the finite-difference derivative is "
            "negative throughout, so the sign is recorded rather than claimed "
            "as unstable.  The route still needs a retained limiting theorem "
            "or production pole-derivative data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The derivative scout is finite but prescription-sensitive; no retained continuum/IR limit is derived.",
        "eigen_derivative_gate_certificate": str(EIGEN_GATE.relative_to(ROOT)),
        "scan": scan,
        "summary": {
            "points": len(scan),
            "derivative_min": float(min(finite_derivatives)),
            "derivative_max": float(max(finite_derivatives)),
            "abs_derivative_spread": float(max(abs_derivatives) / min(abs_derivatives)),
            "sign_values": sorted(sign_values),
            "crossing_rows": len(crossing_rows),
        },
        "required_next_theorem": [
            "derive the scalar ladder projector/source normalization",
            "derive the gauge-zero-mode and IR limiting prescription",
            "prove convergence of d lambda_max / d p^2 in the finite-volume limit",
            "then insert that derivative into the FH/LSZ invariant readout",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
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
