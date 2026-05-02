#!/usr/bin/env python3
"""
PR #230 scalar taste/projector normalization theorem attempt.

The previous finite ladder blocks narrowed the analytic target to the taste
carrier and projector normalization.  This runner checks what can be derived
from the current source surface.

A unit-norm taste singlet over the sixteen Brillouin-zone corners is an
ordinary Hilbert-space normalization: O_singlet = (1/sqrt(16)) sum_t O_t.
That construction is exact support, but it is not PR #230 closure.  The source
functional can be written with either the unnormalized local sum or the
normalized singlet after a source-coordinate rescaling, and the current repo
has no retained authority that identifies the non-origin corners as the
physical scalar carrier or supplies the interacting pole derivative.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASTE_AUDIT = ROOT / "outputs" / "yt_taste_carrier_import_audit_2026-05-01.json"
TASTE_NORMALIZATION = (
    ROOT / "outputs" / "yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json"
)
SOURCE_UNIT = ROOT / "outputs" / "yt_cl3_source_unit_normalization_no_go_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_scalar_taste_projector_normalization_attempt_2026-05-01.json"

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


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def norm_sq(values: list[float]) -> float:
    return sum(value * value for value in values)


def main() -> int:
    print("PR #230 scalar taste/projector normalization theorem attempt")
    print("=" * 72)

    taste_audit = load(TASTE_AUDIT)
    taste_normalization = load(TASTE_NORMALIZATION)
    source_unit = load(SOURCE_UNIT)

    corners = list(itertools.product((0, math.pi), repeat=4))
    n_taste = len(corners)
    local_coefficients = [1.0 for _ in corners]
    unit_singlet_coefficients = [1.0 / math.sqrt(n_taste) for _ in corners]
    local_norm_sq = norm_sq(local_coefficients)
    unit_norm_sq = norm_sq(unit_singlet_coefficients)
    source_coordinate_rescale = math.sqrt(n_taste)
    ladder_scale_local_to_unit_singlet = unit_norm_sq / local_norm_sq

    normalized_rows = taste_normalization.get("normalized_rows", [])
    raw_values = [float(row["raw_lambda_max"]) for row in normalized_rows]
    normalized_values = [
        float(row["taste_singlet_normalized_lambda_max"]) for row in normalized_rows
    ]
    source_scales_needed_for_crossing = [
        1.0 / math.sqrt(value) for value in raw_values
    ]

    report("sixteen-corner-taste-space-constructed", n_taste == 16, f"n_taste={n_taste}")
    report(
        "unit-singlet-projector-normalized",
        abs(unit_norm_sq - 1.0) < 1.0e-12,
        f"unit_norm_sq={unit_norm_sq:.12g}",
    )
    report(
        "local-corner-sum-is-unnormalized",
        abs(local_norm_sq - 16.0) < 1.0e-12,
        f"local_norm_sq={local_norm_sq:.12g}",
    )
    report(
        "local-to-unit-singlet-rescales-ladder-by-one-sixteenth",
        abs(ladder_scale_local_to_unit_singlet - 1.0 / 16.0) < 1.0e-12
        and taste_normalization.get("summary", {}).get("raw_over_normalized") == 16,
        f"lambda_scale={ladder_scale_local_to_unit_singlet:.12g}",
    )
    report(
        "unit-singlet-normalization-removes-current-finite-crossings",
        normalized_values and max(normalized_values) < 1.0 and min(raw_values) >= 1.0,
        f"raw_min={min(raw_values):.12g}, normalized_max={max(normalized_values):.12g}",
    )
    report(
        "source-coordinate-rescaling-remains-open",
        "source-unit normalization no-go" in source_unit.get("actual_current_surface_status", "")
        and source_unit.get("proposal_allowed") is False,
        source_unit.get("actual_current_surface_status", ""),
    )
    report(
        "physical-taste-carrier-not-imported",
        "taste-corner scalar-carrier import audit"
        in taste_audit.get("actual_current_surface_status", "")
        and taste_audit.get("proposal_allowed") is False,
        taste_audit.get("actual_current_surface_status", ""),
    )
    report(
        "not-retained-closure",
        True,
        "unit projector algebra does not derive the interacting pole derivative or physical carrier",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / scalar taste-projector normalization theorem attempt blocked"
        ),
        "verdict": (
            "The current surface can construct the canonical unit-norm taste "
            "singlet over the sixteen BZ corners, but this does not close PR "
            "#230.  The unnormalized local corner sum has norm squared 16, so "
            "moving from the local sum to the unit singlet rescales the finite "
            "ladder eigenvalue by 1/16 and removes the current finite "
            "crossings.  The source functional can absorb the same factor into "
            "the source coordinate, and the current retained/audit-clean "
            "surface does not identify the non-origin corners as the physical "
            "scalar carrier or derive the interacting pole derivative.  The "
            "remaining closure route is a real scalar taste/carrier plus "
            "projector theorem tied to the interacting LSZ pole, or production "
            "same-source FH/LSZ pole data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The unit taste-singlet normalization is only projector algebra; "
            "the physical scalar carrier, source-to-Higgs normalization, and "
            "interacting pole derivative remain open."
        ),
        "taste_space": {
            "corner_count": n_taste,
            "local_corner_sum_norm_sq": local_norm_sq,
            "unit_singlet_norm_sq": unit_norm_sq,
            "source_coordinate_rescale_local_to_unit_singlet": source_coordinate_rescale,
            "ladder_scale_local_to_unit_singlet": ladder_scale_local_to_unit_singlet,
        },
        "crossing_scale_thresholds": [
            {
                "grid_size_4d": row["grid_size_4d"],
                "mass": row["mass"],
                "projector": row["projector"],
                "raw_lambda_max": row["raw_lambda_max"],
                "source_scale_needed_for_lambda_equals_one": threshold,
            }
            for row, threshold in zip(normalized_rows, source_scales_needed_for_crossing)
        ],
        "parent_certificates": {
            "taste_carrier_import_audit": str(TASTE_AUDIT.relative_to(ROOT)),
            "taste_singlet_normalization_boundary": str(TASTE_NORMALIZATION.relative_to(ROOT)),
            "source_unit_normalization_no_go": str(SOURCE_UNIT.relative_to(ROOT)),
        },
        "remaining_blockers": [
            "derive the physical scalar taste/carrier projection from the retained Cl(3)/Z^3 source functional",
            "derive the continuum projector normalization for the interacting color-singlet scalar denominator",
            "derive or measure the inverse-propagator derivative at the scalar pole",
            "match the same-source scalar pole residue to the canonical Higgs normalization used by v",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained top-Yukawa closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as proof selectors",
            "does not use alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
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
