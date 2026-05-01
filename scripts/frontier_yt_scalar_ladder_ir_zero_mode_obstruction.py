#!/usr/bin/env python3
"""
PR #230 scalar ladder IR / zero-mode obstruction.

This is the next scalar-channel Bethe-Salpeter route check after the projector
normalization obstruction.  It holds the scalar source fixed and asks whether a
finite Wilson-exchange ladder pole test is stable under the still-undderived
IR and gauge-zero-mode prescription.

It is not.  The same finite kernel can cross or fail lambda_max >= 1 depending
only on whether the q=0 gauge mode is retained, and the same prescription can
cross or fail under finite-volume/IR-regulator changes.  Therefore PR #230
still needs a retained scalar-channel limiting theorem before the ladder pole
criterion can become load-bearing.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json"

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
    if mode == "point_split_zero_momentum_normalized":
        return np.sum(np.cos(momenta / 2.0) ** 2, axis=1) / 4.0
    raise ValueError(f"unknown projector mode: {mode}")


def largest_eigenvalue(
    *,
    size: int,
    mass: float,
    ir_mu_sq: float,
    projector_mode: str,
    remove_zero_mode: bool,
) -> float:
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
        row = 1.0 / (q_hat_sq + ir_mu_sq)
        if remove_zero_mode:
            row = row.copy()
            row[q_hat_sq < 1.0e-14] = 0.0
        kernel[idx, :] = row

    color_factor = 4.0 / 3.0
    matrix = color_factor * (sqrt_w[:, None] * kernel * sqrt_w[None, :]) / n
    matrix = 0.5 * (matrix + matrix.T)
    return float(np.linalg.eigvalsh(matrix)[-1])


def main() -> int:
    print("PR #230 scalar ladder IR / zero-mode obstruction")
    print("=" * 72)

    mass = 0.50
    sizes = [3, 4, 5]
    ir_values = [0.05, 0.10, 0.20, 0.50]
    projectors = ["local", "point_split_zero_momentum_normalized"]
    scan = []
    for projector in projectors:
        for size in sizes:
            for ir_mu_sq in ir_values:
                for remove_zero_mode in [False, True]:
                    lam = largest_eigenvalue(
                        size=size,
                        mass=mass,
                        ir_mu_sq=ir_mu_sq,
                        projector_mode=projector,
                        remove_zero_mode=remove_zero_mode,
                    )
                    scan.append(
                        {
                            "grid_size_4d": size,
                            "mass": mass,
                            "ir_mu_sq": ir_mu_sq,
                            "projector": projector,
                            "zero_mode": "removed" if remove_zero_mode else "included",
                            "lambda_max": lam,
                            "pole_condition_lambda_ge_1": lam >= 1.0,
                        }
                    )

    def get(projector: str, size: int, ir_mu_sq: float, remove_zero_mode: bool) -> float:
        for row in scan:
            if (
                row["projector"] == projector
                and row["grid_size_4d"] == size
                and abs(row["ir_mu_sq"] - ir_mu_sq) < 1.0e-12
                and row["zero_mode"] == ("removed" if remove_zero_mode else "included")
            ):
                return float(row["lambda_max"])
        raise AssertionError("scan point missing")

    fixed_included = get("local", 4, 0.10, False)
    fixed_removed = get("local", 4, 0.10, True)
    volume_small = get("local", 3, 0.20, False)
    volume_large = get("local", 5, 0.20, False)
    ir_low = get("local", 4, 0.10, False)
    ir_high = get("local", 4, 0.20, False)
    ps_included = get("point_split_zero_momentum_normalized", 3, 0.20, False)
    ps_removed = get("point_split_zero_momentum_normalized", 3, 0.20, True)

    report(
        "finite-ir-zero-mode-scan-runs",
        len(scan) == len(projectors) * len(sizes) * len(ir_values) * 2,
        f"points={len(scan)}",
    )
    report(
        "fixed-source-zero-mode-choice-flips-pole-test",
        fixed_included >= 1.0 and fixed_removed < 1.0,
        f"included={fixed_included:.12g}, removed={fixed_removed:.12g}",
    )
    report(
        "zero-mode-contribution-is-load-bearing",
        fixed_included / fixed_removed > 4.0,
        f"included/removed={fixed_included / fixed_removed:.6g}",
    )
    report(
        "same-prescription-finite-volume-can-flip-pole-test",
        volume_small >= 1.0 and volume_large < 1.0,
        f"N=3 lambda={volume_small:.12g}, N=5 lambda={volume_large:.12g}",
    )
    report(
        "same-prescription-ir-regulator-can-flip-pole-test",
        ir_low >= 1.0 and ir_high < 1.0,
        f"mu2=0.10 lambda={ir_low:.12g}, mu2=0.20 lambda={ir_high:.12g}",
    )
    report(
        "obstruction-survives-normalized-point-split-source",
        ps_included >= 1.0 and ps_removed < 1.0,
        f"included={ps_included:.12g}, removed={ps_removed:.12g}",
    )
    report(
        "not-retained-closure",
        True,
        "finite ladder needs a retained IR/zero-mode and limiting theorem before use as a pole proof",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar ladder IR zero-mode obstruction",
        "verdict": (
            "Holding the scalar source fixed, the finite Wilson-exchange ladder "
            "pole criterion is not stable under the still-undderived IR and "
            "gauge-zero-mode prescription.  The same kernel crosses or fails "
            "lambda_max >= 1 depending on whether the q=0 mode is retained; "
            "the same prescription also crosses or fails under finite-volume "
            "and IR-regulator changes.  Therefore the scalar-channel "
            "Bethe-Salpeter route cannot close PR #230 until it derives the "
            "gauge fixing / zero-mode treatment, finite-volume and IR limits, "
            "and pole-residue readout."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The scalar ladder pole criterion depends on open IR/zero-mode and "
            "finite-volume limiting imports."
        ),
        "parameters": {
            "mass": mass,
            "color_factor": 4.0 / 3.0,
            "sizes": sizes,
            "ir_mu_sq_values": ir_values,
            "projectors": projectors,
        },
        "scan": scan,
        "witnesses": {
            "fixed_source_zero_mode_flip": {
                "projector": "local",
                "grid_size_4d": 4,
                "ir_mu_sq": 0.10,
                "included": fixed_included,
                "removed": fixed_removed,
            },
            "finite_volume_flip": {
                "projector": "local",
                "ir_mu_sq": 0.20,
                "N3_included": volume_small,
                "N5_included": volume_large,
            },
            "ir_regulator_flip": {
                "projector": "local",
                "grid_size_4d": 4,
                "mu2_0_10_included": ir_low,
                "mu2_0_20_included": ir_high,
            },
            "normalized_point_split_zero_mode_flip": {
                "grid_size_4d": 3,
                "ir_mu_sq": 0.20,
                "included": ps_included,
                "removed": ps_removed,
            },
        },
        "required_next_theorem": [
            "derive the gauge fixing and zero-mode treatment for the scalar-channel ladder kernel",
            "prove the finite-volume and IR limiting order",
            "derive the scalar projector/source normalization independently",
            "prove eigenvalue crossing in that fixed limit",
            "compute the pole residue from the inverse two-point derivative",
        ],
        "strict_non_claims": [
            "not a y_t derivation",
            "not a production measurement",
            "not a retained Bethe-Salpeter pole theorem",
            "does not define y_t through H_unit matrix elements",
            "does not use observed top/Higgs/Yukawa values as selectors",
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
