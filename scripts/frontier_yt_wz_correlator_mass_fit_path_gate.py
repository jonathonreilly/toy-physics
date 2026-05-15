#!/usr/bin/env python3
"""
PR #230 W/Z correlator mass-fit path gate.

The W/Z fallback route cannot use static electroweak mass algebra as a measured
dM_W/ds or dM_Z/ds.  After the same-source EW action gate, the next required
work unit is a real W/Z two-point correlator mass-fit path under source shifts.

This runner defines and stress-tests that future mass-fit contract, verifies
that the current PR230 QCD/top harness does not implement it, and records the
exact boundary without writing W/Z measurement rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_correlator_mass_fit_path_gate_2026-05-04.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
EW_GAUGE_MASS_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
FUTURE_MASS_FIT_ROWS = ROOT / "outputs" / "yt_wz_correlator_mass_fit_rows_2026-05-04.json"
FUTURE_RESPONSE_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"

PARENTS = {
    "implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
    "same_source_ew_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "wz_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
    "wz_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str | Path) -> dict[str, Any]:
    path = Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def has_neg_zero_pos(values: list[Any]) -> bool:
    numeric = [float(value) for value in values if finite(value)]
    return any(v < 0.0 for v in numeric) and any(abs(v) <= 1.0e-15 for v in numeric) and any(v > 0.0 for v in numeric)


def fit_row_ok(row: dict[str, Any]) -> bool:
    correlator = row.get("correlator", [])
    plateau = row.get("effective_mass_plateau", {})
    fit = row.get("mass_fit", {})
    return (
        finite(row.get("source_shift"))
        and row.get("boson") in {"W", "Z"}
        and isinstance(correlator, list)
        and len(correlator) >= 6
        and all(isinstance(point, dict) and finite(point.get("tau")) and finite(point.get("mean")) for point in correlator)
        and isinstance(plateau, dict)
        and finite(plateau.get("tau_min"))
        and finite(plateau.get("tau_max"))
        and plateau.get("single_state_dominance") is True
        and isinstance(fit, dict)
        and finite(fit.get("mass_lat"))
        and finite(fit.get("mass_lat_err"))
        and fit.get("from_correlator") is True
        and finite(row.get("jackknife_or_bootstrap_block_count"))
    )


def validate_mass_fit_rows(data: dict[str, Any]) -> dict[str, Any]:
    rows = data.get("per_source_shift_mass_fits", [])
    source_shifts = data.get("source_shifts", [])
    firewall = data.get("firewall", {})
    checks = {
        "production_phase": data.get("phase") == "production",
        "same_source_coordinate": data.get("same_source_coordinate") is True,
        "source_coordinate_named": isinstance(data.get("source_coordinate"), str) and bool(data.get("source_coordinate")),
        "source_shifts_neg_zero_pos": isinstance(source_shifts, list) and has_neg_zero_pos(source_shifts),
        "mass_fit_rows_present": isinstance(rows, list) and len(rows) >= 3,
        "mass_fit_rows_are_correlator_fits": isinstance(rows, list) and all(isinstance(row, dict) and fit_row_ok(row) for row in rows),
        "same_boson_across_rows": isinstance(rows, list) and len({row.get("boson") for row in rows if isinstance(row, dict)}) == 1,
        "no_static_ew_mass_algebra": firewall.get("used_static_EW_mass_algebra") is False,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "not_yukawa_readout": data.get("used_as_physical_yukawa_readout") is False,
    }
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "missing_or_failed": [key for key, ok in checks.items() if not ok],
    }


def positive_witness() -> dict[str, Any]:
    rows = []
    for shift, mass in [(-0.01, 0.312), (0.0, 0.318), (0.01, 0.324)]:
        correlator = [{"tau": tau, "mean": math.exp(-mass * tau), "stderr": 0.01} for tau in range(1, 9)]
        rows.append(
            {
                "source_shift": shift,
                "boson": "W",
                "correlator": correlator,
                "effective_mass_plateau": {
                    "tau_min": 3,
                    "tau_max": 7,
                    "single_state_dominance": True,
                },
                "mass_fit": {
                    "mass_lat": mass,
                    "mass_lat_err": 0.004,
                    "from_correlator": True,
                    "fit_window": [3, 7],
                },
                "jackknife_or_bootstrap_block_count": 64,
            }
        )
    return {
        "phase": "production",
        "same_source_coordinate": True,
        "source_coordinate": "uniform additive scalar source s used for top FH response",
        "source_shifts": [-0.01, 0.0, 0.01],
        "per_source_shift_mass_fits": rows,
        "firewall": {
            "used_static_EW_mass_algebra": False,
            "used_observed_WZ_masses_as_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
        },
        "used_as_physical_yukawa_readout": False,
    }


def rejection_witnesses() -> dict[str, dict[str, Any]]:
    static_algebra = {
        "phase": "support",
        "same_source_coordinate": False,
        "source_coordinate": "canonical h after EW Higgs supplied",
        "source_shifts": [],
        "per_source_shift_mass_fits": [],
        "firewall": {
            "used_static_EW_mass_algebra": True,
            "used_observed_WZ_masses_as_selector": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
        },
        "used_as_physical_yukawa_readout": False,
    }
    aggregate_slope_only = positive_witness()
    aggregate_slope_only.pop("per_source_shift_mass_fits")
    aggregate_slope_only["aggregate_slope_dM_W_ds"] = 0.6
    mismatch = positive_witness()
    mismatch["same_source_coordinate"] = False
    mismatch["source_coordinate"] = "separate gauge-sector source"
    observed = positive_witness()
    observed["firewall"]["used_observed_WZ_masses_as_selector"] = True
    return {
        "static_ew_algebra": static_algebra,
        "aggregate_slope_only": aggregate_slope_only,
        "mismatched_source_coordinate": mismatch,
        "observed_wz_selector": observed,
    }


def main() -> int:
    print("PR #230 W/Z correlator mass-fit path gate")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    harness_text = read_text(PRODUCTION_HARNESS)
    ew_text = read_text(EW_GAUGE_MASS_NOTE)
    witness = positive_witness()
    witness_validation = validate_mass_fit_rows(witness)
    rejections = {name: validate_mass_fit_rows(row) for name, row in rejection_witnesses().items()}

    implementation_plan_names_mass_fits = any(
        row.get("id") == "wz_correlator_mass_fits"
        for row in certs["implementation_plan"].get("implementation_work_units", [])
    )
    same_source_action_blocked = (
        "same-source EW action not defined" in status(certs["same_source_ew_action"])
        and certs["same_source_ew_action"].get("same_source_ew_action_ready") is False
    )
    row_contract_blocks_current = (
        "WZ response measurement-row contract gate" in status(certs["wz_row_contract"])
        and certs["wz_row_contract"].get("wz_measurement_row_contract_gate_passed") is False
    )
    row_production_negative = (
        "WZ response row production attempt" in status(certs["wz_row_production_attempt"])
        and certs["wz_row_production_attempt"].get("measurement_rows_written") is False
    )
    builder_rows_absent = (
        "same-source WZ response rows absent" in status(certs["wz_builder"])
        and certs["wz_builder"].get("input_present") is False
    )
    same_source_gate_open = (
        "same-source WZ response certificate gate not passed" in status(certs["same_source_wz_gate"])
        and certs["same_source_wz_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    retained_route_open = (
        "closure not yet reached" in status(certs["retained_route"])
        and certs["retained_route"].get("proposal_allowed") is False
    )
    harness_has_wz_absent_guard = (
        '"wz_mass_response"' in harness_text
        and "absent_guarded" in harness_text
        and "Static EW algebra, smoke" in harness_text
        and "physics evidence" in harness_text
    )
    harness_has_wz_smoke_schema_path = all(
        token in harness_text
        for token in (
            "--wz-mass-response-smoke",
            "smoke_schema_enabled_not_ew_production",
            "synthetic_scout_contract_not_EW_field",
        )
    )
    harness_has_real_wz_mass_fit_path = any(
        token in harness_text
        for token in (
            "wz_correlator_measurement",
            "fit_wz_mass_correlator",
            "wz_effective_mass_plateau",
            "per_source_shift_mass_fits",
        )
    ) or (
        "--wz-source-shifts" in harness_text
        and not harness_has_wz_smoke_schema_path
    )
    ew_note_is_static_dictionary = "M_W = g_2 v / 2" in ew_text and "Assume a neutral Higgs vacuum" in ew_text
    future_mass_fit_rows_present = FUTURE_MASS_FIT_ROWS.exists()
    future_response_rows_present = FUTURE_RESPONSE_ROWS.exists()
    all_rejections_fail = all(result["valid"] is False for result in rejections.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("implementation-plan-names-mass-fit-work-unit", implementation_plan_names_mass_fits, "wz_correlator_mass_fits")
    report("same-source-ew-action-still-blocked", same_source_action_blocked, status(certs["same_source_ew_action"]))
    report("row-contract-blocks-current-surface", row_contract_blocks_current, status(certs["wz_row_contract"]))
    report("row-production-attempt-negative", row_production_negative, status(certs["wz_row_production_attempt"]))
    report("builder-rows-absent", builder_rows_absent, status(certs["wz_builder"]))
    report("same-source-wz-gate-open", same_source_gate_open, status(certs["same_source_wz_gate"]))
    report("retained-route-still-open", retained_route_open, status(certs["retained_route"]))
    report("positive-witness-passes-mass-fit-contract", witness_validation["valid"], str(witness_validation["missing_or_failed"]))
    report("rejection-witnesses-fail-contract", all_rejections_fail, str({k: v["missing_or_failed"] for k, v in rejections.items()}))
    report("qcd-harness-has-wz-absent-guard", harness_has_wz_absent_guard, display(PRODUCTION_HARNESS))
    report(
        "qcd-harness-has-wz-smoke-schema-path",
        harness_has_wz_smoke_schema_path,
        "default-off synthetic schema path only",
    )
    report(
        "qcd-harness-has-no-real-wz-mass-fit-path",
        not harness_has_real_wz_mass_fit_path,
        display(PRODUCTION_HARNESS),
    )
    report("ew-note-is-static-dictionary-not-correlator-fit", ew_note_is_static_dictionary, display(EW_GAUGE_MASS_NOTE))
    report("future-mass-fit-rows-absent", not future_mass_fit_rows_present, display(FUTURE_MASS_FIT_ROWS))
    report("future-response-rows-absent", not future_response_rows_present, display(FUTURE_RESPONSE_ROWS))

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ correlator mass-fit path absent on PR230 surface",
        "verdict": (
            "The second W/Z implementation work unit is not satisfied on the "
            "current PR230 surface.  A future row must contain actual W/Z "
            "two-point correlators, effective-mass plateaus or fit windows, "
            "jackknife/bootstrap errors, and negative/zero/positive source "
            "shifts under the same source coordinate.  The current QCD top "
            "harness has only a W/Z absent guard plus a synthetic smoke-schema "
            "path and no production W/Z mass-fit CLI/path; static EW "
            "gauge-mass algebra is rejected as measurement evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No W/Z correlator mass-fit rows, same-source EW action, sector identity, or retained-route gate pass.",
        "bare_retained_allowed": False,
        "wz_correlator_mass_fit_path_ready": False,
        "future_mass_fit_rows": display(FUTURE_MASS_FIT_ROWS),
        "future_mass_fit_rows_present": future_mass_fit_rows_present,
        "future_response_rows": display(FUTURE_RESPONSE_ROWS),
        "future_response_rows_present": future_response_rows_present,
        "positive_witness_validation": witness_validation,
        "rejection_validations": rejections,
        "current_surface_findings": {
            "qcd_harness_has_wz_absent_guard": harness_has_wz_absent_guard,
            "qcd_harness_has_wz_smoke_schema_path": harness_has_wz_smoke_schema_path,
            "qcd_harness_has_real_wz_mass_fit_path": harness_has_real_wz_mass_fit_path,
            "ew_note_is_static_dictionary": ew_note_is_static_dictionary,
        },
        "mass_fit_row_contract": {
            "required": [
                "production phase",
                "same source coordinate as top FH response",
                "negative, zero, and positive source shifts",
                "per-shift W or Z correlator time series",
                "effective-mass plateau or fit window with single-state dominance",
                "mass_lat and mass_lat_err from the correlator",
                "jackknife/bootstrap block count",
                "firewall excluding static EW algebra, observed W/Z selectors, H_unit/Ward, alpha_LM/plaquette/u0",
            ]
        },
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write W/Z mass-fit or response rows",
            "does not treat static EW gauge-mass algebra as a measured W/Z correlator mass fit",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Implement a genuine same-source EW action plus W/Z two-point "
            "correlator mass-fit harness, or pivot to source-Higgs C_sH/C_HH "
            "pole rows, Schur A/B/C rows, neutral-sector irreducibility, or "
            "FH/LSZ production evidence."
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
