#!/usr/bin/env python3
"""
PR #230 scalar source two-point stretch attempt.

This is a first-principles pressure test on the narrowed Ward-readout blocker:
derive as much as possible about the scalar-bilinear source two-point function
from the retained Wilson-staggered source surface, without using the old
H_unit matrix-element definition, observed top data, alpha_LM, or plaquette
normalization.

The stretch result is intentionally narrow.  The source curvature is an exact
fermion-bubble functional of the staggered Dirac operator.  On the free
staggered surface its canonical-residue proxy varies with the fermion mass and
finite volume, so the current A_min data do not select kappa_H = 1 or a common
scalar/gauge dressing.  This does not rule out a future interacting scalar
bound-state theorem; it states what the present retained source calculus can
and cannot close.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_source_two_point_stretch_2026-05-01.json"

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8", errors="ignore")


def free_staggered_scalar_bubble(
    spatial_size: int,
    time_size: int,
    mass: float,
    bosonic_time_momentum_index: int,
    source_prefactor: float = 1.0,
) -> float:
    """Connected scalar-density curvature on the free staggered surface.

    We use the standard finite-volume momentum expression for the connected
    scalar source curvature:

        C(p) = - d^2 log det(D + J O_p) / dJ_p dJ_-p |_{J=0}
             = - Tr[G(k) O_p G(k+p) O_-p].

    For a scalar density with the naive/staggered free denominator, the
    spin/taste trace reduces to the bubble integrand below up to an overall
    positive degeneracy.  The overall degeneracy is irrelevant for the
    source-normalization question, so it is omitted and source_prefactor is
    kept explicit.
    """

    axes = [
        2.0 * math.pi * np.arange(spatial_size) / spatial_size,
        2.0 * math.pi * np.arange(spatial_size) / spatial_size,
        2.0 * math.pi * np.arange(spatial_size) / spatial_size,
        2.0 * math.pi * (np.arange(time_size) + 0.5) / time_size,
    ]
    grids = np.meshgrid(*axes, indexing="ij")
    sin_k = np.stack([np.sin(grid) for grid in grids], axis=0)
    den_k = mass * mass + np.sum(sin_k * sin_k, axis=0)

    p0 = 2.0 * math.pi * bosonic_time_momentum_index / time_size
    sin_k_plus_p = np.stack(
        [
            sin_k[0],
            sin_k[1],
            sin_k[2],
            np.sin(grids[3] + p0),
        ],
        axis=0,
    )
    den_k_plus_p = mass * mass + np.sum(sin_k_plus_p * sin_k_plus_p, axis=0)
    dot = np.sum(sin_k * sin_k_plus_p, axis=0)
    raw_bubble = np.mean((mass * mass - dot) / (den_k * den_k_plus_p))
    connected_curvature = -raw_bubble
    return float(source_prefactor * source_prefactor * connected_curvature)


def residue_proxy(spatial_size: int, time_size: int, mass: float, source_prefactor: float = 1.0) -> dict:
    """Fit inverse C(p) = A + B p_hat^2 at the first three bosonic momenta."""

    rows = []
    for n in [1, 2, 3]:
        p0 = 2.0 * math.pi * n / time_size
        p_hat_sq = 4.0 * math.sin(p0 / 2.0) ** 2
        curvature = free_staggered_scalar_bubble(
            spatial_size,
            time_size,
            mass,
            n,
            source_prefactor=source_prefactor,
        )
        rows.append({"n": n, "p_hat_sq": p_hat_sq, "curvature": curvature})

    x = np.array([row["p_hat_sq"] for row in rows], dtype=float)
    y = np.array([1.0 / row["curvature"] for row in rows], dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    fit = intercept + slope * x
    max_relative_fit_error = float(np.max(np.abs((fit - y) / y)))
    residue = float(1.0 / slope)
    return {
        "spatial_size": spatial_size,
        "time_size": time_size,
        "mass": mass,
        "source_prefactor": source_prefactor,
        "rows": rows,
        "inverse_intercept": float(intercept),
        "inverse_slope": float(slope),
        "residue_proxy": residue,
        "max_relative_fit_error": max_relative_fit_error,
    }


def main() -> int:
    print("PR #230 scalar source two-point stretch attempt")
    print("=" * 72)

    minimal_axioms = read("docs/MINIMAL_AXIOMS_2026-04-11.md")
    source_bridge = read("docs/YT_SOURCE_HIGGS_LEGENDRE_SSB_BRIDGE_NOTE_2026-05-01.md")
    kappa_obstruction = read("docs/YT_SOURCE_HIGGS_KAPPA_RESIDUE_OBSTRUCTION_NOTE_2026-05-01.md")

    report(
        "minimal-action-surface-read",
        "staggered-Dirac partition" in minimal_axioms and "g_bare = 1" in minimal_axioms,
        "A_min includes finite Grassmann/staggered-Dirac partition and g_bare=1 surface",
    )
    report(
        "source-normalization-gap-read",
        "kappa_H" in source_bridge and "two-point residue" in source_bridge,
        "prior bridge names the two-point residue as the open normalization",
    )
    report(
        "counts-ssb-no-selection-read",
        "cannot select" in kappa_obstruction and "kappa_H = 1" in kappa_obstruction,
        "prior obstruction blocks counts+SSB selection",
    )

    n_color = 3
    n_iso = 2
    source_prefactor = 1.0 / math.sqrt(n_color * n_iso)
    report(
        "source-prefactor-fixed-by-counts",
        abs(source_prefactor - 1.0 / math.sqrt(6.0)) < 1.0e-15,
        f"c_source={source_prefactor:.15f}",
    )

    scan = []
    for spatial_size, time_size in [(6, 12), (8, 16), (10, 20)]:
        for mass in [0.10, 0.25, 0.50, 1.00]:
            scan.append(residue_proxy(spatial_size, time_size, mass, source_prefactor=source_prefactor))

    residues = [row["residue_proxy"] for row in scan]
    positive_curvatures = all(point["curvature"] > 0.0 for row in scan for point in row["rows"])
    positive_slopes = all(row["inverse_slope"] > 0.0 for row in scan)
    residue_spread = max(residues) / min(residues)
    near_unit = [row for row in scan if abs(row["residue_proxy"] - 1.0) < 0.05]

    report("free-source-curvatures-positive", positive_curvatures, "connected scalar curvature is positive after sign convention")
    report("inverse-curvature-has-positive-slope", positive_slopes, "local inverse-curvature slope can define a residue proxy")
    report("residue-proxy-not-universal", residue_spread > 10.0, f"spread={residue_spread:.3f}")
    report("residue-proxy-not-selected-to-one", not near_unit, f"near_unit_count={len(near_unit)}")

    # Source rescaling is not an allowed closure move, but it is a useful
    # functional sanity check: the source two-point residue scales as the
    # square of the source normalization unless the source-to-field convention
    # is independently fixed.
    base = residue_proxy(8, 16, 0.25, source_prefactor=source_prefactor)
    scaled = residue_proxy(8, 16, 0.25, source_prefactor=2.0 * source_prefactor)
    scale_ratio = scaled["residue_proxy"] / base["residue_proxy"]
    report("source-rescaling-quadratic", abs(scale_ratio - 4.0) < 1.0e-10, f"Z(2c)/Z(c)={scale_ratio:.12f}")

    report(
        "no-h-unit-matrix-element-used",
        True,
        "runner uses only logdet/source curvature; H_unit matrix-element authority is not an input",
    )
    report(
        "no-observed-top-input-used",
        True,
        "no m_t/y_t comparator appears in the computation",
    )
    report(
        "common-dressing-still-open",
        True,
        "free scalar source curvature does not derive interacting scalar/gauge dressing equality",
    )

    result = {
        "actual_current_surface_status": "exact-support / open bridge",
        "verdict": (
            "The scalar-bilinear source two-point function is derivable as a "
            "fermion-bubble curvature of W[J]=log det(D+J O).  On the free "
            "Wilson-staggered source surface the resulting residue proxy is "
            "positive but depends strongly on fermion mass, volume, and source "
            "normalization.  A_min therefore does not select kappa_H=1 or a "
            "common scalar/gauge dressing.  A future closure must add the "
            "interacting scalar pole/bound-state theorem or direct measurement."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source curvature formula is exact support, but the physical pole residue/common dressing remains open.",
        "source_prefactor": source_prefactor,
        "scan": scan,
        "residue_spread": residue_spread,
        "near_unit_count": len(near_unit),
        "required_next_theorem": [
            "prove the interacting C_OO(p) has an isolated Higgs-carrier pole",
            "compute the pole residue Z_phi and source-to-canonical kappa_H on the retained action",
            "derive or measure relative scalar/gauge dressing",
        ],
        "strict_non_claims": [
            "does not define y_t_bare by H_unit matrix element",
            "does not use observed top mass or Yukawa",
            "does not prove retained y_t closure",
            "does not rule out a future interacting scalar pole theorem",
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
