#!/usr/bin/env python3
"""
PR #230 color-singlet zero-mode-removed ladder pole search.

The color-singlet zero-mode theorem removes the exact q=0 gauge mode, and the
finite-q IR regularity theorem removes the local 1/q^2 divergence concern.
This runner asks the next narrower question: does the remaining finite
Wilson-exchange ladder already give a stable scalar pole and LSZ derivative?

It does not.  The zero-mode-removed finite ladder has constructive finite pole
witnesses at small mass, but those witnesses are volume/parity, taste-corner,
projector, and derivative sensitive.  They are useful route information, not
retained y_t closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "outputs" / "yt_color_singlet_finite_q_ir_regular_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"

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


def taste_corner_count(momenta: np.ndarray) -> int:
    sin_sq = np.sum(np.sin(momenta) ** 2, axis=1)
    return int(np.count_nonzero(sin_sq < 1.0e-14))


def zero_mode_removed_kernel(momenta: np.ndarray) -> np.ndarray:
    n = len(momenta)
    kernel = np.empty((n, n), dtype=float)
    for idx, k in enumerate(momenta):
        dq = k - momenta
        q_hat_sq = np.sum((2.0 * np.sin(dq / 2.0)) ** 2, axis=1)
        row = np.zeros(n, dtype=float)
        mask = q_hat_sq > 1.0e-14
        row[mask] = 1.0 / q_hat_sq[mask]
        kernel[idx, :] = row
    return kernel


def largest_ladder_eigenvalue(
    *,
    size: int,
    mass: float,
    projector: str,
    p_total: np.ndarray | None = None,
) -> float:
    momenta = momentum_grid(size)
    if p_total is None:
        p_total = np.zeros(4, dtype=float)
    den_plus = fermion_den(momenta + 0.5 * p_total[None, :], mass)
    den_minus = fermion_den(momenta - 0.5 * p_total[None, :], mass)
    proj = projector_values(momenta, projector)
    weights = (proj * proj) / (den_plus * den_minus)
    sqrt_w = np.sqrt(np.maximum(weights, 0.0))
    kernel = zero_mode_removed_kernel(momenta)
    color_factor = 4.0 / 3.0
    matrix = color_factor * (sqrt_w[:, None] * kernel * sqrt_w[None, :]) / len(momenta)
    matrix = 0.5 * (matrix + matrix.T)
    return float(np.linalg.eigvalsh(matrix)[-1])


def derivative_row(*, size: int, mass: float, projector: str) -> dict[str, object]:
    p0 = np.zeros(4, dtype=float)
    p1 = np.asarray([2.0 * math.pi / size, 0.0, 0.0, 0.0], dtype=float)
    p_hat_sq = float(np.sum((2.0 * np.sin(p1 / 2.0)) ** 2))
    lambda0 = largest_ladder_eigenvalue(size=size, mass=mass, projector=projector, p_total=p0)
    lambda1 = largest_ladder_eigenvalue(size=size, mass=mass, projector=projector, p_total=p1)
    derivative = (lambda1 - lambda0) / p_hat_sq
    residue_proxy = 1.0 / abs(derivative) if abs(derivative) > 1.0e-30 else float("inf")
    return {
        "grid_size_4d": size,
        "mass": mass,
        "projector": projector,
        "p_hat_sq_step": p_hat_sq,
        "lambda_p0": lambda0,
        "lambda_p1": lambda1,
        "d_lambda_dp_hat_sq": derivative,
        "residue_factor_proxy_if_crossing": residue_proxy,
    }


def scan_value(scan: list[dict[str, object]], *, size: int, mass: float, projector: str) -> float:
    for row in scan:
        if (
            int(row["grid_size_4d"]) == size
            and abs(float(row["mass"]) - mass) < 1.0e-12
            and row["projector"] == projector
        ):
            return float(row["lambda_max"])
    raise AssertionError("scan point missing")


def main() -> int:
    print("PR #230 color-singlet zero-mode-removed ladder pole search")
    print("=" * 72)

    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    sizes = [3, 4, 5, 6]
    masses = [0.20, 0.30, 0.35, 0.50, 0.75, 1.00]
    projectors = ["local", "point_split_zero_momentum_normalized"]

    scan = []
    for projector in projectors:
        for mass in masses:
            for size in sizes:
                momenta = momentum_grid(size)
                lam = largest_ladder_eigenvalue(size=size, mass=mass, projector=projector)
                scan.append(
                    {
                        "grid_size_4d": size,
                        "mass": mass,
                        "projector": projector,
                        "zero_mode": "removed by color singlet q=0 cancellation",
                        "taste_corner_count": taste_corner_count(momenta),
                        "lambda_max": lam,
                        "pole_condition_lambda_ge_1": lam >= 1.0,
                    }
                )

    crossing_rows = [row for row in scan if bool(row["pole_condition_lambda_ge_1"])]
    crossing_derivatives = [
        derivative_row(
            size=int(row["grid_size_4d"]),
            mass=float(row["mass"]),
            projector=str(row["projector"]),
        )
        for row in crossing_rows
    ]
    residue_proxies = [
        float(row["residue_factor_proxy_if_crossing"])
        for row in crossing_derivatives
        if math.isfinite(float(row["residue_factor_proxy_if_crossing"]))
    ]

    local_m030 = {
        f"N{size}": scan_value(scan, size=size, mass=0.30, projector="local")
        for size in sizes
    }
    local_m020 = {
        f"N{size}": scan_value(scan, size=size, mass=0.20, projector="local")
        for size in sizes
    }
    projector_witness = {
        "N6_m0.20_local": scan_value(scan, size=6, mass=0.20, projector="local"),
        "N6_m0.20_point_split_normalized": scan_value(
            scan,
            size=6,
            mass=0.20,
            projector="point_split_zero_momentum_normalized",
        ),
    }
    crossing_sizes = sorted({int(row["grid_size_4d"]) for row in crossing_rows})
    crossing_corner_counts = sorted({int(row["taste_corner_count"]) for row in crossing_rows})
    odd_low_mass_max = max(
        float(row["lambda_max"])
        for row in scan
        if int(row["grid_size_4d"]) in {3, 5} and float(row["mass"]) <= 0.30
    )
    derivative_spread = max(residue_proxies) / min(residue_proxies) if residue_proxies else float("inf")

    report(
        "parent-color-singlet-finite-q-regularity-loaded",
        parent.get("proposal_allowed") is False
        and "finite-q IR regularity" in str(parent.get("actual_current_surface_status", "")),
        str(PARENT.relative_to(ROOT)),
    )
    report(
        "zero-mode-removed-ladder-scan-runs",
        len(scan) == len(sizes) * len(masses) * len(projectors),
        f"points={len(scan)}",
    )
    report(
        "finite-eigenvalues-computed",
        all(math.isfinite(float(row["lambda_max"])) for row in scan),
        "all lambda_max values finite at mu_IR^2=0 with q=0 removed",
    )
    report(
        "constructive-finite-pole-witnesses-exist",
        bool(crossing_rows),
        f"crossing_rows={len(crossing_rows)}",
    )
    report(
        "finite-pole-witness-not-volume-stable",
        local_m030["N4"] >= 1.0 and max(local_m030[key] for key in ("N3", "N5", "N6")) < 1.0,
        str(local_m030),
    )
    report(
        "finite-pole-witness-not-projector-stable",
        projector_witness["N6_m0.20_local"] >= 1.0
        and projector_witness["N6_m0.20_point_split_normalized"] < 1.0,
        str(projector_witness),
    )
    report(
        "taste-corner-aliasing-is-load-bearing",
        crossing_sizes and set(crossing_sizes).issubset({4, 6}) and crossing_corner_counts == [16] and odd_low_mass_max < 1.0,
        f"crossing_sizes={crossing_sizes}, crossing_corner_counts={crossing_corner_counts}, odd_low_mass_max={odd_low_mass_max:.12g}",
    )
    report(
        "crossing-residue-proxy-not-universal",
        len(residue_proxies) >= 2 and derivative_spread > 3.0,
        f"residue_proxy_spread={derivative_spread:.6g}",
    )
    report(
        "not-retained-closure",
        True,
        "finite pole witnesses need continuum/taste/projector control and a pole derivative theorem",
    )

    result = {
        "actual_current_surface_status": "bounded-support / color-singlet zero-mode-removed ladder pole search",
        "verdict": (
            "After color-singlet q=0 cancellation and finite-q IR regularity, "
            "the zero-mode-removed finite Wilson-exchange ladder does have "
            "constructive finite lambda_max >= 1 witnesses at small mass.  "
            "Those witnesses are not a retained scalar pole: they are not "
            "stable under finite volume, source projector, or taste-corner "
            "aliasing, and their finite-difference derivative/residue proxies "
            "are not universal.  The route therefore remains open until a "
            "continuum/taste/projector theorem derives the interacting "
            "color-singlet scalar pole and inverse-propagator derivative, or "
            "production FH/LSZ pole data measure them."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Finite zero-mode-removed ladder pole witnesses are volume, "
            "projector, taste-corner, and derivative sensitive; no retained "
            "interacting pole/LSZ theorem is derived."
        ),
        "parent_certificate": str(PARENT.relative_to(ROOT)),
        "parameters": {
            "sizes": sizes,
            "masses": masses,
            "projectors": projectors,
            "color_factor": 4.0 / 3.0,
            "ir_mu_sq": 0.0,
            "zero_mode_policy": "q=0 removed by color-singlet total-color-charge cancellation",
        },
        "scan": scan,
        "crossing_rows": crossing_rows,
        "crossing_derivatives": crossing_derivatives,
        "witnesses": {
            "local_m0.30_volume_sequence": local_m030,
            "local_m0.20_volume_sequence": local_m020,
            "projector_witness": projector_witness,
            "crossing_sizes": crossing_sizes,
            "crossing_taste_corner_counts": crossing_corner_counts,
            "odd_low_mass_max_lambda": odd_low_mass_max,
            "crossing_residue_proxy_spread": derivative_spread,
        },
        "remaining_blockers": [
            "derive the continuum/taste projection that removes finite corner aliasing from the scalar denominator",
            "derive the scalar source/projector normalization for the interacting color-singlet kernel",
            "derive or measure the isolated scalar pole location and d lambda_max / d p^2 or d Gamma_ss / d p^2",
            "supply production FH/LSZ pole data if the theorem route does not close",
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
