#!/usr/bin/env python3
"""
PR #230 unit-projector scalar pole-threshold obstruction.

After the unit taste/projector normalization attempt, the finite ladder
crossings disappear at the retained kernel normalization used by the scout.
This runner asks whether a finite pole can still be read off without adding a
new scalar-channel enhancement.

It cannot.  On the current finite witnesses, the unit-projector eigenvalues are
all below one.  Reaching lambda_max=1 would require multiplying the scalar
kernel by an additional factor greater than two even on the best row.  No
current retained surface derives that factor, and introducing it as a fitted
pole selector would be another forbidden normalization import.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASTE_PROJECTOR = ROOT / "outputs" / "yt_scalar_taste_projector_normalization_attempt_2026-05-01.json"
TASTE_NORMALIZATION = (
    ROOT / "outputs" / "yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json"
)
POLE_SEARCH = ROOT / "outputs" / "yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_unit_projector_pole_threshold_obstruction_2026-05-01.json"

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


def main() -> int:
    print("PR #230 unit-projector scalar pole-threshold obstruction")
    print("=" * 72)

    taste_projector = load(TASTE_PROJECTOR)
    taste_normalization = load(TASTE_NORMALIZATION)
    pole_search = load(POLE_SEARCH)

    rows = []
    for row in taste_normalization.get("normalized_rows", []):
        normalized_lambda = float(row["taste_singlet_normalized_lambda_max"])
        required_kernel_multiplier = 1.0 / normalized_lambda
        rows.append(
            {
                "grid_size_4d": row["grid_size_4d"],
                "mass": row["mass"],
                "projector": row["projector"],
                "raw_lambda_max": row["raw_lambda_max"],
                "unit_projector_lambda_max": normalized_lambda,
                "crosses_at_retained_kernel_strength": normalized_lambda >= 1.0,
                "required_kernel_multiplier_for_crossing": required_kernel_multiplier,
                "extra_kernel_multiplier_needed_beyond_retained_strength": required_kernel_multiplier - 1.0,
            }
        )

    unit_lambdas = [row["unit_projector_lambda_max"] for row in rows]
    required_multipliers = [row["required_kernel_multiplier_for_crossing"] for row in rows]
    best_row = min(rows, key=lambda item: item["required_kernel_multiplier_for_crossing"])

    report(
        "parent-unit-projector-attempt-loaded",
        taste_projector.get("proposal_allowed") is False
        and "scalar taste-projector normalization theorem attempt blocked"
        in taste_projector.get("actual_current_surface_status", ""),
        taste_projector.get("actual_current_surface_status", ""),
    )
    report(
        "parent-pole-search-loaded",
        pole_search.get("proposal_allowed") is False
        and len(pole_search.get("crossing_rows", [])) == len(rows),
        f"crossing_rows={len(pole_search.get('crossing_rows', []))}",
    )
    report(
        "unit-projector-has-no-finite-crossing",
        rows and max(unit_lambdas) < 1.0,
        f"unit_lambda_range=({min(unit_lambdas):.12g}, {max(unit_lambdas):.12g})",
    )
    report(
        "extra-kernel-enhancement-required",
        min(required_multipliers) > 2.0,
        f"required_multiplier_range=({min(required_multipliers):.12g}, {max(required_multipliers):.12g})",
    )
    report(
        "best-row-still-not-pole-at-retained-strength",
        best_row["unit_projector_lambda_max"] < 1.0
        and best_row["required_kernel_multiplier_for_crossing"] > 1.0,
        (
            "best unit lambda={:.12g}, multiplier={:.12g}"
        ).format(
            best_row["unit_projector_lambda_max"],
            best_row["required_kernel_multiplier_for_crossing"],
        ),
    )
    report(
        "not-retained-closure",
        True,
        "a new scalar-channel enhancement or production pole measurement would be required",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / unit-projector finite-ladder pole-threshold obstruction"
        ),
        "verdict": (
            "With the unit taste projector fixed, the current finite "
            "zero-mode-removed ladder witnesses no longer satisfy "
            "lambda_max >= 1 at the retained scout kernel strength.  The best "
            "row has lambda_max = {:.12g}, so reaching a finite pole would "
            "require multiplying the scalar-channel kernel by {:.12g}.  No "
            "current retained/audit-clean premise derives that enhancement; "
            "using it as a fitted selector would import a new scalar "
            "normalization.  The analytic route still needs an interacting "
            "kernel theorem that derives the pole and K'(x_pole), or "
            "production same-source FH/LSZ pole data."
        ).format(
            best_row["unit_projector_lambda_max"],
            best_row["required_kernel_multiplier_for_crossing"],
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The unit projector removes the finite crossings; the extra kernel "
            "multiplier needed for a pole is not derived."
        ),
        "parent_certificates": {
            "scalar_taste_projector_normalization_attempt": str(TASTE_PROJECTOR.relative_to(ROOT)),
            "taste_singlet_ladder_normalization_boundary": str(TASTE_NORMALIZATION.relative_to(ROOT)),
            "color_singlet_zero_mode_removed_ladder_pole_search": str(POLE_SEARCH.relative_to(ROOT)),
        },
        "rows": rows,
        "summary": {
            "unit_lambda_min": min(unit_lambdas),
            "unit_lambda_max": max(unit_lambdas),
            "required_kernel_multiplier_min": min(required_multipliers),
            "required_kernel_multiplier_max": max(required_multipliers),
            "best_row": best_row,
        },
        "remaining_blockers": [
            "derive an interacting scalar-channel kernel enhancement from retained dynamics, not a fitted pole selector",
            "derive the physical scalar taste/carrier projection and continuum projector normalization",
            "derive K'(x_pole) or the inverse-propagator derivative at the scalar pole",
            "or measure the same-source pole derivative in production FH/LSZ data",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained top-Yukawa closure",
            "does not set kappa_s = 1",
            "does not fit a scalar-channel coupling to force a pole",
            "does not use H_unit, yt_ward_identity, observed top mass, or observed y_t",
            "does not use alpha_LM, plaquette, u0, reduced pilots, c2 = 1, or Z_match = 1",
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
