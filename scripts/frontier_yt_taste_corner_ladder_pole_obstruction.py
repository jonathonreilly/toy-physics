#!/usr/bin/env python3
"""
PR #230 finite-ladder taste-corner pole-witness obstruction.

The zero-mode-removed ladder pole search found finite small-mass
lambda_max >= 1 witnesses after color-singlet q=0 cancellation.  This runner
tests whether those witnesses survive a taste-corner projection.

They do not.  The crossing witnesses are dominated by non-origin
Brillouin-zone corners where sin(p)=0.  If those corners are excluded unless a
separate taste/corner theorem admits them into the scalar carrier, the finite
pole witnesses collapse below lambda_max = 1.  Therefore those finite
crossings cannot be used as retained scalar pole or LSZ evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "outputs" / "yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_taste_corner_ladder_pole_obstruction_2026-05-01.json"

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


def corner_masks(momenta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    corner = np.sum(np.sin(momenta) ** 2, axis=1) < 1.0e-14
    origin = np.sum((2.0 * np.sin(momenta / 2.0)) ** 2, axis=1) < 1.0e-14
    return corner, origin


def filtered_weights(momenta: np.ndarray, mass: float, projector: str, policy: str) -> np.ndarray:
    den = mass * mass + np.sum(np.sin(momenta) ** 2, axis=1)
    proj = projector_values(momenta, projector)
    weights = (proj * proj) / (den * den)
    corner, origin = corner_masks(momenta)
    if policy == "full":
        return weights
    if policy == "physical_origin_only":
        weights = weights.copy()
        weights[corner & ~origin] = 0.0
        return weights
    if policy == "no_corners":
        weights = weights.copy()
        weights[corner] = 0.0
        return weights
    if policy == "corner_only":
        return np.where(corner, weights, 0.0)
    if policy == "nonorigin_corner_only":
        return np.where(corner & ~origin, weights, 0.0)
    raise ValueError(f"unknown policy: {policy}")


def largest_ladder_eigenvalue(*, size: int, mass: float, projector: str, policy: str) -> float:
    momenta = momentum_grid(size)
    sqrt_w = np.sqrt(filtered_weights(momenta, mass, projector, policy))
    n = len(momenta)
    kernel = np.empty((n, n), dtype=float)
    for idx, k in enumerate(momenta):
        dq = k - momenta
        q_hat_sq = np.sum((2.0 * np.sin(dq / 2.0)) ** 2, axis=1)
        row = np.zeros(n, dtype=float)
        mask = q_hat_sq > 1.0e-14
        row[mask] = 1.0 / q_hat_sq[mask]
        kernel[idx, :] = row
    matrix = (4.0 / 3.0) * (sqrt_w[:, None] * kernel * sqrt_w[None, :]) / n
    matrix = 0.5 * (matrix + matrix.T)
    return float(np.linalg.eigvalsh(matrix)[-1])


def row_for_crossing(parent_row: dict[str, object]) -> dict[str, object]:
    size = int(parent_row["grid_size_4d"])
    mass = float(parent_row["mass"])
    projector = str(parent_row["projector"])
    policies = [
        "full",
        "physical_origin_only",
        "no_corners",
        "corner_only",
        "nonorigin_corner_only",
    ]
    values = {
        policy: largest_ladder_eigenvalue(
            size=size,
            mass=mass,
            projector=projector,
            policy=policy,
        )
        for policy in policies
    }
    return {
        "grid_size_4d": size,
        "mass": mass,
        "projector": projector,
        "taste_corner_count": int(parent_row["taste_corner_count"]),
        "lambda_by_policy": values,
        "physical_origin_only_crosses": values["physical_origin_only"] >= 1.0,
        "nonorigin_corner_fraction_of_full": values["nonorigin_corner_only"] / values["full"],
        "corner_only_fraction_of_full": values["corner_only"] / values["full"],
    }


def main() -> int:
    print("PR #230 finite-ladder taste-corner pole-witness obstruction")
    print("=" * 72)

    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    crossing_rows = parent.get("crossing_rows", [])
    rows = [row_for_crossing(row) for row in crossing_rows]
    physical_origin_values = [
        float(row["lambda_by_policy"]["physical_origin_only"])
        for row in rows
    ]
    no_corner_values = [
        float(row["lambda_by_policy"]["no_corners"])
        for row in rows
    ]
    nonorigin_fractions = [
        float(row["nonorigin_corner_fraction_of_full"])
        for row in rows
    ]
    corner_fractions = [
        float(row["corner_only_fraction_of_full"])
        for row in rows
    ]

    report(
        "parent-zero-mode-removed-pole-search-loaded",
        parent.get("proposal_allowed") is False
        and "zero-mode-removed ladder pole search" in str(parent.get("actual_current_surface_status", "")),
        str(PARENT.relative_to(ROOT)),
    )
    report(
        "parent-has-finite-crossing-witnesses",
        len(crossing_rows) == 4,
        f"crossing_rows={len(crossing_rows)}",
    )
    report(
        "crossings-live-on-even-taste-corner-grids",
        rows and all(int(row["taste_corner_count"]) == 16 for row in rows),
        f"corner_counts={[row['taste_corner_count'] for row in rows]}",
    )
    report(
        "nonorigin-corners-dominate-crossing-witnesses",
        nonorigin_fractions and min(nonorigin_fractions) > 0.65,
        f"nonorigin_corner_fraction_range=({min(nonorigin_fractions):.6g}, {max(nonorigin_fractions):.6g})",
    )
    report(
        "corner-only-kernel-reproduces-crossing-scale",
        corner_fractions and min(corner_fractions) > 0.90,
        f"corner_only_fraction_range=({min(corner_fractions):.6g}, {max(corner_fractions):.6g})",
    )
    report(
        "physical-origin-only-projection-removes-crossings",
        physical_origin_values and max(physical_origin_values) < 1.0,
        f"max_physical_origin_only_lambda={max(physical_origin_values):.12g}",
    )
    report(
        "no-corner-control-removes-crossings",
        no_corner_values and max(no_corner_values) < 0.10,
        f"max_no_corner_lambda={max(no_corner_values):.12g}",
    )
    report(
        "not-retained-closure",
        True,
        "finite crossings require a taste/corner carrier theorem before use as scalar pole evidence",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / finite-ladder taste-corner pole-witness obstruction",
        "verdict": (
            "The zero-mode-removed finite ladder crossings found after "
            "color-singlet q=0 cancellation are dominated by non-origin "
            "Brillouin-zone taste corners.  Keeping only the physical origin "
            "corner plus non-corner modes removes every finite crossing, and "
            "removing all sin(p)=0 corners removes them more strongly.  "
            "Therefore these finite lambda_max >= 1 witnesses cannot be used "
            "as retained scalar pole or LSZ evidence unless a separate "
            "continuum/taste/projector theorem derives the scalar carrier and "
            "inverse-propagator derivative, or production FH/LSZ pole data "
            "measure them."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Finite pole witnesses are taste-corner dominated and collapse "
            "under a physical-origin-only projection; no retained scalar "
            "carrier/taste theorem is supplied."
        ),
        "parent_certificate": str(PARENT.relative_to(ROOT)),
        "crossing_rows_by_policy": rows,
        "summary": {
            "crossing_rows": len(rows),
            "nonorigin_corner_fraction_min": min(nonorigin_fractions),
            "nonorigin_corner_fraction_max": max(nonorigin_fractions),
            "corner_only_fraction_min": min(corner_fractions),
            "corner_only_fraction_max": max(corner_fractions),
            "max_physical_origin_only_lambda": max(physical_origin_values),
            "max_no_corner_lambda": max(no_corner_values),
        },
        "remaining_blockers": [
            "derive whether non-origin taste corners belong to the retained scalar carrier",
            "derive the continuum/taste/projector limit of the color-singlet scalar denominator",
            "derive or measure the inverse-propagator derivative at the scalar pole",
            "run production same-source FH/LSZ pole data if the theorem route remains blocked",
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
