#!/usr/bin/env python3
"""
PR #230 top mass-scan response harness gate.

This runner validates the reduced smoke artifact for the production-harness
schema that serializes per-configuration top mass-scan response rows from the
existing three-mass top correlator scan.  It is infrastructure support only:
the rows are not dE/dh, not kappa_s, and not physical y_t evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_pr230_top_mass_scan_response_harness_smoke_2026-05-12.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json"
EXPECTED_MASSES = [0.45, 0.75, 1.05]
EXPECTED_SELECTED_MASS = 0.75
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def approx_list(values: Any) -> list[float]:
    if not isinstance(values, list):
        return []
    return [round(float(value), 8) for value in values if finite(value)]


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def main() -> int:
    print("PR #230 top mass-scan response harness gate")
    print("=" * 72)

    smoke = load_json(SMOKE)
    ensemble = first_ensemble(smoke)
    metadata = smoke.get("metadata", {}) if isinstance(smoke.get("metadata"), dict) else {}
    top_meta = (
        metadata.get("top_mass_scan_response", {})
        if isinstance(metadata.get("top_mass_scan_response"), dict)
        else {}
    )
    top = (
        ensemble.get("top_mass_scan_response_analysis", {})
        if isinstance(ensemble.get("top_mass_scan_response_analysis"), dict)
        else {}
    )
    source = (
        ensemble.get("scalar_source_response_analysis", {})
        if isinstance(ensemble.get("scalar_source_response_analysis"), dict)
        else {}
    )
    lsz = (
        ensemble.get("scalar_two_point_lsz_analysis", {})
        if isinstance(ensemble.get("scalar_two_point_lsz_analysis"), dict)
        else {}
    )

    measurements = int(ensemble.get("measurement_sweeps", 0)) if ensemble else 0
    top_slopes = top.get("per_configuration_slopes", [])
    top_energies = top.get("per_configuration_effective_energies", [])
    top_multi_tau = top.get("per_configuration_multi_tau_slopes", [])
    mass_scan = ensemble.get("mass_parameter_scan", [])
    rng = ensemble.get("rng_seed_control", {}) if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz.get("mode_rows"), dict) else {}
    css_timeseries_status = {
        key: isinstance(row, dict)
        and isinstance(row.get("C_ss_timeseries"), list)
        and len(row.get("C_ss_timeseries", [])) == measurements
        for key, row in mode_rows.items()
    }

    report("smoke-artifact-present", bool(smoke), rel(SMOKE))
    report("single-ensemble-present", bool(ensemble), f"ensemble_keys={sorted(ensemble)[:12] if ensemble else []}")
    report(
        "numba-seed-control-preserved",
        rng.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION,
        str(rng),
    )
    report(
        "three-mass-top-scan-preserved",
        approx_list([row.get("m_bare_lat") for row in mass_scan if isinstance(row, dict)])
        == EXPECTED_MASSES,
        str(mass_scan),
    )
    report(
        "top-mass-scan-response-schema",
        top.get("row_schema_version") == "top_mass_scan_response_v1",
        str(top.get("row_schema_version")),
    )
    report(
        "selected-mass-and-bracket-recorded",
        finite(top.get("selected_mass_parameter"))
        and abs(float(top.get("selected_mass_parameter")) - EXPECTED_SELECTED_MASS) < 1.0e-12
        and approx_list(top.get("mass_scan_bracket_masses_lat")) == EXPECTED_MASSES,
        f"selected={top.get('selected_mass_parameter')} bracket={top.get('mass_scan_bracket_masses_lat')}",
    )
    report(
        "per-configuration-top-response-rows",
        measurements > 0
        and isinstance(top_energies, list)
        and isinstance(top_slopes, list)
        and len(top_energies) == measurements
        and len(top_slopes) == measurements,
        f"measurements={measurements} energies={len(top_energies) if isinstance(top_energies, list) else 'bad'} slopes={len(top_slopes) if isinstance(top_slopes, list) else 'bad'}",
    )
    report(
        "top-response-slopes-finite-support",
        isinstance(top_slopes, list)
        and any(isinstance(row, dict) and row.get("finite") is True for row in top_slopes),
        str(top_slopes[:2] if isinstance(top_slopes, list) else top_slopes),
    )
    report(
        "top-response-multitau-rows",
        isinstance(top_multi_tau, list)
        and len(top_multi_tau) == measurements
        and any(
            isinstance(row, dict)
            and int(row.get("finite_tau_count", 0)) > 0
            for row in top_multi_tau
        ),
        f"rows={len(top_multi_tau) if isinstance(top_multi_tau, list) else 'bad'}",
    )
    report(
        "scalar-source-response-legacy-timeseries-preserved",
        isinstance(source.get("per_configuration_effective_energies"), list)
        and isinstance(source.get("per_configuration_slopes"), list)
        and len(source.get("per_configuration_effective_energies", [])) == measurements,
        f"source_keys={sorted(source)}",
    )
    report(
        "scalar-two-point-css-timeseries-preserved",
        bool(css_timeseries_status) and all(css_timeseries_status.values()),
        str(css_timeseries_status),
    )
    report(
        "metadata-support-only",
        top_meta.get("row_schema_version") == "top_mass_scan_response_v1"
        and top_meta.get("extra_solve_count") == 0
        and top_meta.get("uses_existing_three_mass_top_correlator_scan") is True
        and top_meta.get("used_as_physical_yukawa_readout") is False
        and top_meta.get("physical_higgs_normalization") == "not_derived",
        str(top_meta),
    )
    report(
        "top-response-firewall",
        top.get("used_as_physical_yukawa_readout") is False
        and top.get("physical_higgs_normalization") == "not_derived"
        and "not dE/dh" in str(top.get("strict_limit", "")),
        str(top.get("strict_limit", "")),
    )
    report("does-not-authorize-retained-proposal", True, "schema support only")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": "bounded-support / top mass-scan response harness schema gate",
        "verdict": (
            "The reduced smoke artifact validates that the production harness "
            "serializes per-configuration top mass-scan effective energies and "
            "bare-mass slopes while preserving scalar FH/LSZ target time series, "
            "C_ss time series, and numba seed control.  This is support for "
            "future same-ensemble covariance/subtraction gates only."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Top bare-mass response rows do not derive canonical-Higgs/source-overlap, "
            "kappa_s, W/Z identity, g2 authority, or physical y_t closure."
        ),
        "bare_retained_allowed": False,
        "smoke_artifact": rel(SMOKE),
        "row_schema_version": top.get("row_schema_version"),
        "measurement_count": measurements,
        "seed_control_version": rng.get("seed_control_version"),
        "mass_scan_masses_lat": top.get("mass_scan_masses_lat"),
        "mass_scan_bracket_masses_lat": top.get("mass_scan_bracket_masses_lat"),
        "selected_mass_parameter": top.get("selected_mass_parameter"),
        "finite_tau1_slope_count": top.get("finite_tau1_slope_count"),
        "finite_multi_tau_slope_count": top.get("finite_multi_tau_slope_count"),
        "per_configuration_effective_energy_row_count": (
            len(top_energies) if isinstance(top_energies, list) else 0
        ),
        "per_configuration_slope_row_count": (
            len(top_slopes) if isinstance(top_slopes, list) else 0
        ),
        "per_configuration_multi_tau_slope_row_count": (
            len(top_multi_tau) if isinstance(top_multi_tau, list) else 0
        ),
        "scalar_source_response_rows_preserved": (
            isinstance(source.get("per_configuration_effective_energies"), list)
            and isinstance(source.get("per_configuration_slopes"), list)
        ),
        "scalar_two_point_css_timeseries_modes": css_timeseries_status,
        "metadata_top_mass_scan_response": top_meta,
        "top_mass_scan_response_harness_gate_passed": passed,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat dE/dm_bare as dE/dh",
            "does not derive or set kappa_s = 1",
            "does not import H_unit, yt_ward_identity, alpha_LM, plaquette/u0, observed m_t, or observed y_t as proof authority",
            "does not provide W/Z response rows, matched covariance, or g2 authority",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
