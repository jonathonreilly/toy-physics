#!/usr/bin/env python3
"""
PR #230 fitted scalar-kernel residue selector no-go.

The unit-projector threshold obstruction showed that the normalized finite
ladder has no pole at retained scout strength.  A tempting shortcut is to fit
a constant scalar-channel multiplier g_eff so that g_eff * lambda_unit(0) = 1,
then use the same finite row to define the LSZ residue.

This runner records why that is not retained closure.  The fitted multiplier
is itself an underived scalar-channel normalization, and after tuning the pole
the residue proxy is controlled by lambda_raw / |d lambda_raw / d p^2|.  That
ratio is still finite-row, volume, mass, and projector dependent on the
current surface.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UNIT_THRESHOLD = ROOT / "outputs" / "yt_unit_projector_pole_threshold_obstruction_2026-05-01.json"
POLE_SEARCH = ROOT / "outputs" / "yt_color_singlet_zero_mode_removed_ladder_pole_search_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fitted_kernel_residue_selector_no_go_2026-05-01.json"

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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def row_key(row: dict[str, Any]) -> tuple[int, float, str]:
    return (int(row["grid_size_4d"]), float(row["mass"]), str(row["projector"]))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def main() -> int:
    print("PR #230 fitted scalar-kernel residue selector no-go")
    print("=" * 72)

    threshold = load(UNIT_THRESHOLD)
    pole_search = load(POLE_SEARCH)
    derivative_by_key = {
        row_key(row): row
        for row in pole_search.get("crossing_derivatives", [])
        if isinstance(row, dict)
    }

    rows: list[dict[str, Any]] = []
    for unit_row in threshold.get("rows", []):
        key = row_key(unit_row)
        derivative_row = derivative_by_key.get(key)
        if not derivative_row:
            continue
        raw_lambda = float(unit_row["raw_lambda_max"])
        unit_lambda = float(unit_row["unit_projector_lambda_max"])
        dlambda_raw = float(derivative_row["d_lambda_dp_hat_sq"])
        dlambda_unit = dlambda_raw / 16.0
        fitted_multiplier = 1.0 / unit_lambda
        fitted_denominator_derivative = -fitted_multiplier * dlambda_unit
        fitted_residue_proxy = 1.0 / abs(fitted_denominator_derivative)
        raw_ratio_proxy = raw_lambda / abs(dlambda_raw)
        rows.append(
            {
                "grid_size_4d": key[0],
                "mass": key[1],
                "projector": key[2],
                "raw_lambda_max": raw_lambda,
                "unit_projector_lambda_max": unit_lambda,
                "d_lambda_raw_dp_hat_sq": dlambda_raw,
                "d_lambda_unit_dp_hat_sq": dlambda_unit,
                "fitted_kernel_multiplier": fitted_multiplier,
                "fitted_denominator_derivative": fitted_denominator_derivative,
                "fitted_residue_proxy": fitted_residue_proxy,
                "raw_lambda_over_abs_derivative": raw_ratio_proxy,
                "fit_imports_scalar_kernel_normalization": True,
            }
        )

    multipliers = [row["fitted_kernel_multiplier"] for row in rows]
    residues = [row["fitted_residue_proxy"] for row in rows]
    residue_spread = max(residues) / min(residues) if residues else float("inf")
    local_rows = [row for row in rows if row["projector"] == "local"]
    point_split_rows = [
        row for row in rows if row["projector"] == "point_split_zero_momentum_normalized"
    ]
    local_residues = [row["fitted_residue_proxy"] for row in local_rows]
    same_mass_projector_pair = [
        row for row in rows if row["grid_size_4d"] == 4 and abs(row["mass"] - 0.2) < 1.0e-12
    ]
    same_mass_projector_spread = (
        max(row["fitted_residue_proxy"] for row in same_mass_projector_pair)
        / min(row["fitted_residue_proxy"] for row in same_mass_projector_pair)
        if len(same_mass_projector_pair) >= 2
        else float("inf")
    )
    local_volume_pair = [
        row for row in rows
        if row["projector"] == "local" and abs(row["mass"] - 0.2) < 1.0e-12
    ]
    local_volume_spread = (
        max(row["fitted_residue_proxy"] for row in local_volume_pair)
        / min(row["fitted_residue_proxy"] for row in local_volume_pair)
        if len(local_volume_pair) >= 2
        else float("inf")
    )

    report(
        "unit-threshold-loaded",
        threshold.get("proposal_allowed") is False
        and "unit-projector" in threshold.get("actual_current_surface_status", ""),
        threshold.get("actual_current_surface_status", ""),
    )
    report(
        "crossing-derivatives-loaded",
        len(derivative_by_key) >= len(rows) >= 4,
        f"matched_rows={len(rows)}",
    )
    report(
        "fitted-multiplier-is-required",
        min(multipliers) > 1.0,
        f"multiplier_range=({min(multipliers):.12g}, {max(multipliers):.12g})",
    )
    report(
        "fitted-residue-proxy-finite",
        rows and all(finite(row["fitted_residue_proxy"]) for row in rows),
        f"rows={len(rows)}",
    )
    report(
        "fitted-residue-proxy-not-universal",
        residue_spread > 1.5,
        f"residue_spread={residue_spread:.12g}",
    )
    report(
        "volume-choice-load-bearing",
        local_volume_spread > 1.5,
        f"N4_vs_N6_local_m0.2_spread={local_volume_spread:.12g}",
    )
    report(
        "projector-choice-recorded",
        point_split_rows and same_mass_projector_spread >= 1.0,
        f"N4_m0.2_projector_spread={same_mass_projector_spread:.12g}",
    )
    report(
        "not-retained-closure",
        True,
        "fitting g_eff is a scalar-kernel normalization import, not a derivation",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / fitted scalar-kernel residue selector no-go"
        ),
        "verdict": (
            "Forcing the unit-projected finite ladder to a pole by choosing "
            "g_eff = 1/lambda_unit imports an underived scalar-channel "
            "normalization.  Even after granting that fitted selector, the "
            "LSZ residue proxy is lambda_raw / |d lambda_raw / d p^2| and "
            "varies across the current finite rows by a factor of "
            f"{residue_spread:.6g}.  The fitted-pole shortcut therefore does "
            "not derive the interacting scalar denominator or K'(x_pole); it "
            "only moves the missing normalization into g_eff and the finite "
            "row choice."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The pole-forcing multiplier is fitted rather than derived, and "
            "the resulting residue proxy remains finite-row dependent."
        ),
        "parent_certificates": {
            "unit_projector_pole_threshold": str(UNIT_THRESHOLD.relative_to(ROOT)),
            "zero_mode_removed_ladder_pole_search": str(POLE_SEARCH.relative_to(ROOT)),
        },
        "rows": rows,
        "summary": {
            "matched_rows": len(rows),
            "fitted_multiplier_min": min(multipliers),
            "fitted_multiplier_max": max(multipliers),
            "fitted_residue_proxy_min": min(residues),
            "fitted_residue_proxy_max": max(residues),
            "fitted_residue_proxy_spread": residue_spread,
            "local_residue_proxy_values": local_residues,
            "same_mass_projector_spread": same_mass_projector_spread,
            "local_volume_spread": local_volume_spread,
        },
        "remaining_blockers": [
            "derive g_eff or the full momentum-dependent scalar kernel from retained dynamics",
            "derive K'(x_pole) rather than fitting a constant multiplier at p=0",
            "derive the finite-volume/taste/projector limit of the residue proxy",
            "or measure the same-source scalar pole derivative in production FH/LSZ data",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained top-Yukawa closure",
            "does not set kappa_s = 1",
            "does not set fitted g_eff as a retained scalar normalization",
            "does not use H_unit or yt_ward_identity",
            "does not use observed top mass or observed y_t",
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
