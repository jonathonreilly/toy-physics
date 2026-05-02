#!/usr/bin/env python3
"""
PR #230 taste-singlet ladder normalization boundary.

The finite zero-mode-removed ladder crossings are dominated by the 16
Brillouin-zone taste corners.  If the scalar carrier is instead a normalized
taste singlet over those corners, each scalar-source vertex carries the
standard 1/sqrt(N_taste) normalization and the ladder eigenvalue scales by
1/N_taste.

On the current finite crossing witnesses this removes every lambda_max >= 1
crossing.  Thus the unnormalized taste multiplicity is load-bearing; the
finite crossings cannot be used as scalar-pole evidence without a retained
scalar taste/projector normalization theorem.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLE_SEARCH = ROOT / "outputs" / "yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"
TASTE_AUDIT = ROOT / "outputs" / "yt_taste_carrier_import_audit_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json"

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


def main() -> int:
    print("PR #230 taste-singlet ladder normalization boundary")
    print("=" * 72)

    pole_search = json.loads(POLE_SEARCH.read_text(encoding="utf-8"))
    taste_audit = json.loads(TASTE_AUDIT.read_text(encoding="utf-8"))
    crossing_rows = pole_search.get("crossing_rows", [])
    n_taste = 16
    normalized_rows = []
    for row in crossing_rows:
        raw_lambda = float(row["lambda_max"])
        normalized_lambda = raw_lambda / n_taste
        normalized_rows.append(
            {
                "grid_size_4d": row["grid_size_4d"],
                "mass": row["mass"],
                "projector": row["projector"],
                "taste_corner_count": row["taste_corner_count"],
                "raw_lambda_max": raw_lambda,
                "taste_singlet_normalized_lambda_max": normalized_lambda,
                "raw_crosses": raw_lambda >= 1.0,
                "normalized_crosses": normalized_lambda >= 1.0,
            }
        )

    raw_values = [float(row["raw_lambda_max"]) for row in normalized_rows]
    normalized_values = [float(row["taste_singlet_normalized_lambda_max"]) for row in normalized_rows]
    ratios = [
        float(row["raw_lambda_max"]) / float(row["taste_singlet_normalized_lambda_max"])
        for row in normalized_rows
    ]

    report(
        "pole-search-crossing-witnesses-loaded",
        pole_search.get("proposal_allowed") is False and len(crossing_rows) == 4,
        f"crossing_rows={len(crossing_rows)}",
    )
    report(
        "taste-carrier-import-audit-loaded",
        taste_audit.get("proposal_allowed") is False
        and "taste-corner scalar-carrier import audit" in str(taste_audit.get("actual_current_surface_status", "")),
        str(TASTE_AUDIT.relative_to(ROOT)),
    )
    report(
        "raw-finite-crossings-exist",
        raw_values and min(raw_values) >= 1.0,
        f"raw_lambda_range=({min(raw_values):.12g}, {max(raw_values):.12g})",
    )
    report(
        "taste-singlet-normalization-removes-crossings",
        normalized_values and max(normalized_values) < 1.0,
        f"normalized_lambda_range=({min(normalized_values):.12g}, {max(normalized_values):.12g})",
    )
    report(
        "normalization-factor-is-load-bearing",
        ratios and min(ratios) == max(ratios) == n_taste,
        f"raw_over_normalized={ratios}",
    )
    report(
        "not-retained-closure",
        True,
        "taste-singlet normalization is a projector boundary, not a scalar pole/LSZ theorem",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / taste-singlet normalization removes finite ladder crossings",
        "verdict": (
            "For the four finite zero-mode-removed ladder crossing witnesses, "
            "applying normalized taste-singlet source normalization over the "
            "16 BZ corners rescales lambda_max by 1/16 and removes every "
            "lambda_max >= 1 crossing.  Therefore the unnormalized taste "
            "multiplicity is load-bearing.  A retained PR #230 scalar pole or "
            "LSZ claim still needs a scalar taste/projector normalization "
            "theorem plus the interacting pole derivative, or production "
            "same-source FH/LSZ pole data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The normalized taste-singlet check removes finite crossings and does not derive a retained scalar pole or LSZ residue.",
        "pole_search_certificate": str(POLE_SEARCH.relative_to(ROOT)),
        "taste_carrier_import_audit_certificate": str(TASTE_AUDIT.relative_to(ROOT)),
        "n_taste": n_taste,
        "normalized_rows": normalized_rows,
        "summary": {
            "raw_lambda_min": min(raw_values),
            "raw_lambda_max": max(raw_values),
            "normalized_lambda_min": min(normalized_values),
            "normalized_lambda_max": max(normalized_values),
            "raw_over_normalized": n_taste,
        },
        "remaining_blockers": [
            "derive the retained scalar taste/projector normalization from the Cl(3)/Z^3 source functional",
            "derive the continuum/taste/projector limit of the interacting color-singlet scalar denominator",
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
