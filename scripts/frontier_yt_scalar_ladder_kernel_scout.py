#!/usr/bin/env python3
"""
PR #230 scalar-channel ladder kernel scout.

This is the constructive continuation after the HS/RPA contact route failed:
replace the contact coupling by a finite-momentum scalar-channel ladder kernel
from Wilson one-gluon exchange and ask whether the pole criterion

    lambda_max(K_scalar * Pi) = 1

is fixed robustly by the retained inputs.

This is a scout, not a retained theorem.  It deliberately exposes the kernel
ingredients that a theorem-grade derivation would have to freeze: fermion mass,
IR treatment of the gauge kernel, scalar projector, and finite-volume/continuum
limit.  The result is useful because it demonstrates the exact shape of the
next closure target rather than falling back to prose.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_ladder_kernel_scout_2026-05-01.json"

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


def largest_scalar_ladder_eigenvalue(size: int, mass: float, ir_mu_sq: float) -> float:
    momenta = momentum_grid(size)
    sin_k = np.sin(momenta)
    fermion_den = mass * mass + np.sum(sin_k * sin_k, axis=1)

    # Scalar bubble weight.  This is a scout-level scalar projector: the full
    # theorem would need the exact staggered taste/spin/color projector.
    weights = 1.0 / (fermion_den * fermion_den)
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
    print("PR #230 scalar-channel ladder kernel scout")
    print("=" * 72)

    size = 4
    masses = [0.10, 0.25, 0.50, 1.00]
    ir_values = [0.02, 0.05, 0.10, 0.20, 0.50, 1.00]
    scan = []
    for mass in masses:
        for ir_mu_sq in ir_values:
            lam = largest_scalar_ladder_eigenvalue(size=size, mass=mass, ir_mu_sq=ir_mu_sq)
            scan.append(
                {
                    "grid_size_4d": size,
                    "mass": mass,
                    "ir_mu_sq": ir_mu_sq,
                    "lambda_max": lam,
                    "pole_condition_lambda_ge_1": lam >= 1.0,
                }
            )

    lambdas = [row["lambda_max"] for row in scan]
    pole_patterns_by_mass = {
        str(mass): [
            row["pole_condition_lambda_ge_1"]
            for row in scan
            if row["mass"] == mass
        ]
        for mass in masses
    }
    crosses = {
        mass: any(pattern) and not all(pattern)
        for mass, pattern in pole_patterns_by_mass.items()
    }

    report("finite-ladder-scout-runs", len(scan) == len(masses) * len(ir_values), f"points={len(scan)}")
    report("kernel-eigenvalue-sensitive", max(lambdas) / min(lambdas) > 100.0, f"spread={max(lambdas) / min(lambdas):.3e}")
    report("pole-criterion-crosses-under-ir-choice", any(crosses.values()), f"crosses={crosses}")
    report(
        "heavy-mass-can-remove-scout-pole",
        not any(row["pole_condition_lambda_ge_1"] for row in scan if row["mass"] == 1.00),
        "m=1.00 gives lambda_max<1 across scanned IR regulators",
    )
    report(
        "light-mass-produces-scout-pole",
        all(row["pole_condition_lambda_ge_1"] for row in scan if row["mass"] == 0.10),
        "m=0.10 gives lambda_max>=1 across scanned IR regulators",
    )
    report(
        "scout-not-retained-closure",
        True,
        "mass, IR regulator, and scalar projector are explicit open theorem inputs",
    )

    result = {
        "actual_current_surface_status": "bounded-support / ladder-kernel scout",
        "verdict": (
            "A finite scalar-channel Wilson-exchange ladder kernel can be built, "
            "and its largest eigenvalue gives the expected pole criterion.  But "
            "the criterion is highly sensitive to mass and IR/kernel treatment.  "
            "This scout therefore does not close y_t; it identifies the precise "
            "theorem needed: a retained scalar-channel Bethe-Salpeter kernel, "
            "projector, IR/finite-volume limit, and eigenvalue crossing with "
            "pole-residue derivative."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Scout depends on explicit mass, IR regulator, and simplified scalar projector.",
        "scan": scan,
        "pole_patterns_by_mass": pole_patterns_by_mass,
        "required_next_theorem": [
            "derive the exact scalar-channel Wilson-staggered ladder kernel",
            "fix the scalar color/taste/spin projector without H_unit readout authority",
            "take the finite-volume and IR limits in a controlled order",
            "prove eigenvalue crossing and compute residue from d lambda / d p^2",
        ],
        "strict_non_claims": [
            "not a production measurement",
            "not a retained scalar pole theorem",
            "does not use observed top/Higgs/Yukawa values",
            "does not define y_t by H_unit matrix element",
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
