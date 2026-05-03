#!/usr/bin/env python3
"""
PR #230 same-source W/Z response measurement-row contract gate.

This runner hardens the physical-response bypass before any future rows are
loaded.  It defines the minimum row-level schema for W/Z mass response under
the same scalar source used for the top FH slope, validates a synthetic
positive witness, and rejects static EW algebra, slope-only rows, and observed
mass selectors.  It is a contract/firewall only; it does not create W/Z data
or authorize retained wording.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_response_measurement_row_contract_gate_2026-05-03.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"

PARENTS = {
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "fh_gauge_mass_response_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "higgs_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
}

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def has_negative_zero_positive(values: list[Any]) -> bool:
    numeric = [float(value) for value in values if finite(value)]
    return any(value < 0.0 for value in numeric) and any(abs(value) <= 1.0e-15 for value in numeric) and any(
        value > 0.0 for value in numeric
    )


def mass_fit_from_correlator(row: dict[str, Any]) -> bool:
    for key in ("w_mass_fit", "z_mass_fit"):
        fit = row.get(key)
        if isinstance(fit, dict) and finite(fit.get("mass_lat")) and fit.get("from_correlator") is True:
            return True
    return False


def source_shift_key(value: Any) -> str:
    if finite(value):
        return f"{float(value):.15g}"
    return str(value)


def contract_schema() -> dict[str, Any]:
    return {
        "future_rows_path": display(FUTURE_ROWS),
        "required_top_level_fields": [
            "phase=production",
            "same_source_coordinate=true",
            "source_coordinate",
            "source_shifts with negative, zero, and positive values",
            "per_source_shift_rows",
            "top_response.slope_dE_top_ds and slope_error",
            "gauge_response.slope_dM_W_ds or slope_dM_Z_ds and slope_error",
            "gauge_response covariance with dE_top/ds",
            "electroweak_coupling.g2 and g2_certificate",
            "identity_certificates for sector overlap, canonical-Higgs pole identity, and retained-route gate",
            "firewall booleans rejecting observed masses, H_unit/Ward, alpha_LM/plaquette/u0, c2=1, and Z_match=1",
        ],
        "per_source_shift_row_fields": [
            "source_shift",
            "configuration_count",
            "top_energy_fit.mass_lat from the top correlator",
            "W or Z mass fit from a W/Z correlator",
            "fit_window or effective-mass method",
            "jackknife_or_bootstrap_block_count",
            "rng_seed_control.seed_control_version",
        ],
        "explicit_rejections": [
            "static EW algebra dM_W/dh without dM_W/ds rows",
            "aggregate slope-only rows without source-shift mass fits and covariance",
            "any observed W/Z, top, y_t, or observed g2 proof selector",
            "same-source labels without sector-overlap and canonical-Higgs identity certificates",
        ],
    }


def validate_measurement_rows(data: dict[str, Any]) -> dict[str, Any]:
    source_shifts = data.get("source_shifts", [])
    per_shift_rows = data.get("per_source_shift_rows", [])
    top = data.get("top_response", {})
    gauge = data.get("gauge_response", {})
    ew = data.get("electroweak_coupling", {})
    identity = data.get("identity_certificates", {})
    firewall = data.get("firewall", {})

    source_shift_set = {source_shift_key(value) for value in source_shifts}
    row_shift_set = {
        source_shift_key(row.get("source_shift"))
        for row in per_shift_rows
        if isinstance(row, dict) and "source_shift" in row
    }
    row_checks = []
    for row in per_shift_rows if isinstance(per_shift_rows, list) else []:
        if not isinstance(row, dict):
            row_checks.append(False)
            continue
        top_fit = row.get("top_energy_fit", {})
        rng_seed = row.get("rng_seed_control", {})
        row_checks.append(
            row.get("source_shift") is not None
            and finite(row.get("configuration_count"))
            and isinstance(top_fit, dict)
            and finite(top_fit.get("mass_lat"))
            and top_fit.get("from_correlator") is True
            and mass_fit_from_correlator(row)
            and bool(row.get("fit_window") or row.get("effective_mass_method"))
            and finite(row.get("jackknife_or_bootstrap_block_count"))
            and isinstance(rng_seed, dict)
            and bool(rng_seed.get("seed_control_version"))
        )

    has_w_or_z_slope = finite(gauge.get("slope_dM_W_ds")) or finite(gauge.get("slope_dM_Z_ds"))
    has_top_wz_covariance = finite(gauge.get("cov_dE_top_dM_W")) or finite(gauge.get("cov_dE_top_dM_Z"))

    checks = {
        "production_phase": data.get("phase") == "production",
        "same_source_coordinate": data.get("same_source_coordinate") is True,
        "source_coordinate_named": isinstance(data.get("source_coordinate"), str) and bool(data.get("source_coordinate")),
        "source_shifts_negative_zero_positive": isinstance(source_shifts, list)
        and has_negative_zero_positive(source_shifts),
        "per_source_shift_rows_present": isinstance(per_shift_rows, list) and len(per_shift_rows) >= len(source_shift_set) >= 3,
        "per_source_shift_rows_cover_shifts": bool(source_shift_set) and source_shift_set.issubset(row_shift_set),
        "per_source_shift_rows_are_correlator_fits": bool(row_checks) and all(row_checks),
        "finite_top_response_slope": finite(top.get("slope_dE_top_ds")),
        "finite_top_response_error": finite(top.get("slope_error")),
        "finite_w_or_z_response_slope": has_w_or_z_slope,
        "finite_w_or_z_response_error": finite(gauge.get("slope_error")),
        "top_wz_covariance_present": has_top_wz_covariance,
        "finite_g2": finite(ew.get("g2")),
        "g2_certificate_present": isinstance(ew.get("g2_certificate"), str) and bool(ew.get("g2_certificate")),
        "sector_overlap_identity_passed": identity.get("same_source_sector_overlap_identity_passed") is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_pole_identity_passed") is True,
        "retained_route_gate_passed": identity.get("retained_route_or_proposal_gate_passed") is True,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_observed_top_or_yt_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
        "no_observed_g2_selector": ew.get("used_observed_g2_as_selector") is False,
        "no_static_v_selector": firewall.get("used_static_v_overlap_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "missing_or_failed_checks": [key for key, ok in checks.items() if not ok],
    }


def positive_witness() -> dict[str, Any]:
    source_shifts = [-0.01, 0.0, 0.01]
    rows = []
    for shift in source_shifts:
        rows.append(
            {
                "source_shift": shift,
                "configuration_count": 256,
                "top_energy_fit": {"mass_lat": 0.72 + shift, "from_correlator": True},
                "w_mass_fit": {"mass_lat": 0.31 + 0.5 * shift, "from_correlator": True},
                "fit_window": [4, 10],
                "jackknife_or_bootstrap_block_count": 64,
                "rng_seed_control": {"seed_control_version": "numba_gauge_seed_v1"},
            }
        )
    return {
        "phase": "production",
        "same_source_coordinate": True,
        "source_coordinate": "uniform additive scalar source s used for top FH response",
        "source_shifts": source_shifts,
        "per_source_shift_rows": rows,
        "top_response": {"slope_dE_top_ds": 1.31, "slope_error": 0.04},
        "gauge_response": {"slope_dM_W_ds": 0.46, "slope_error": 0.02, "cov_dE_top_dM_W": 0.0007},
        "electroweak_coupling": {
            "g2": 0.65,
            "g2_certificate": "outputs/future_retained_g2_certificate.json",
            "used_observed_g2_as_selector": False,
        },
        "identity_certificates": {
            "same_source_sector_overlap_identity_passed": True,
            "canonical_higgs_pole_identity_passed": True,
            "retained_route_or_proposal_gate_passed": True,
        },
        "firewall": {
            "used_observed_WZ_masses_as_selector": False,
            "used_observed_top_or_yukawa_as_selector": False,
            "used_static_v_overlap_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }


def rejection_witnesses() -> dict[str, Any]:
    static_algebra = {
        "phase": "support",
        "same_source_coordinate": False,
        "source_coordinate": "canonical h after EW Higgs is assumed",
        "source_shifts": [],
        "per_source_shift_rows": [],
        "top_response": {"slope_dE_top_ds": 1.0, "slope_error": 0.0},
        "gauge_response": {"slope_dM_W_ds": 0.325, "slope_error": 0.0},
        "electroweak_coupling": {
            "g2": 0.65,
            "g2_certificate": "tree algebra only",
            "used_observed_g2_as_selector": False,
        },
        "identity_certificates": {},
        "firewall": {
            "used_observed_WZ_masses_as_selector": False,
            "used_observed_top_or_yukawa_as_selector": False,
            "used_static_v_overlap_selector": True,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    slope_only = positive_witness()
    slope_only["per_source_shift_rows"] = []
    slope_only["identity_certificates"] = {
        "same_source_sector_overlap_identity_passed": False,
        "canonical_higgs_pole_identity_passed": False,
        "retained_route_or_proposal_gate_passed": False,
    }
    observed_selector = positive_witness()
    observed_selector["firewall"]["used_observed_WZ_masses_as_selector"] = True
    observed_selector["electroweak_coupling"]["used_observed_g2_as_selector"] = True
    return {
        "static_ew_algebra": static_algebra,
        "slope_only_without_rows_or_identity": slope_only,
        "observed_mass_selector": observed_selector,
    }


def main() -> int:
    print("PR #230 W/Z response measurement-row contract gate")
    print("=" * 72)

    parents = {name: load_rel(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    parent_proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    current_rows = load_json(FUTURE_ROWS)
    current_validation = validate_measurement_rows(current_rows) if current_rows else {
        "valid": False,
        "checks": {},
        "missing_or_failed_checks": ["future W/Z measurement rows absent"],
    }
    positive_validation = validate_measurement_rows(positive_witness())
    rejections = {
        name: validate_measurement_rows(witness)
        for name, witness in rejection_witnesses().items()
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not parent_proposals, f"proposal_allowed={parent_proposals}")
    report("contract-schema-recorded", bool(contract_schema()["required_top_level_fields"]), "row contract available")
    report("positive-witness-passes-contract", positive_validation["valid"], str(positive_validation["missing_or_failed_checks"]))
    report(
        "static-ew-algebra-rejected",
        not rejections["static_ew_algebra"]["valid"],
        str(rejections["static_ew_algebra"]["missing_or_failed_checks"]),
    )
    report(
        "slope-only-rows-rejected",
        not rejections["slope_only_without_rows_or_identity"]["valid"],
        str(rejections["slope_only_without_rows_or_identity"]["missing_or_failed_checks"]),
    )
    report(
        "observed-selector-rows-rejected",
        not rejections["observed_mass_selector"]["valid"],
        str(rejections["observed_mass_selector"]["missing_or_failed_checks"]),
    )
    report("future-row-input-state-recorded", True, f"present={bool(current_rows)}")
    report("current-rows-do-not-pass", not current_validation["valid"], str(current_validation["missing_or_failed_checks"]))
    report("contract-is-not-evidence", True, "schema/firewall only")

    result = {
        "actual_current_surface_status": "bounded-support / WZ response measurement-row contract gate",
        "verdict": (
            "The same-source W/Z response route now has a row-level contract for "
            "future measurement input.  The contract accepts only production "
            "source-shift W/Z correlator mass fits with top-response covariance, "
            "retained g2 provenance, sector-overlap and canonical-Higgs identity "
            "certificates, and explicit forbidden-import firewalls.  The current "
            "measurement-row file is absent, so this is support only."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The gate defines future W/Z row acceptance but no current production W/Z rows pass it.",
        "measurement_rows_path": display(FUTURE_ROWS),
        "current_measurement_rows_present": bool(current_rows),
        "current_measurement_rows_validation": current_validation,
        "wz_measurement_row_contract_gate_passed": bool(current_rows) and current_validation["valid"],
        "contract_schema": contract_schema(),
        "positive_witness_validation": positive_validation,
        "rejection_witness_validations": rejections,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not create or infer W/Z mass-response data",
            "does not treat static EW algebra as dM_W/ds",
            "does not use observed W/Z masses, observed top mass, observed y_t, or observed g2 as proof selectors",
            "does not set kappa_s, c2, Z_match, or k_top/k_gauge to one",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, or reduced pilots as proof authority",
        ],
        "exact_next_action": (
            "Produce production same-source W/Z measurement rows satisfying this "
            "contract, then rerun the W/Z response builder, W/Z response gate, "
            "retained-route certificate, and campaign status certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
