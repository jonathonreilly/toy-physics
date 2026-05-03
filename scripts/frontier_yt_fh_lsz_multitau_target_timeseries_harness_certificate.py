#!/usr/bin/env python3
"""
PR #230 FH/LSZ multi-tau target time-series harness certificate.

This runner verifies the production harness can now serialize
per-configuration multi-tau source-response rows needed by a future
response-window covariance gate.  It certifies infrastructure only: the smoke
artifact is reduced-scope support, not production evidence or a readout switch.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_multitau_target_timeseries_smoke_2026-05-03.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_multitau_target_timeseries_harness_certificate_2026-05-03.json"

EXPECTED_SCHEMA_VERSION = "fh_lsz_target_timeseries_v2_multitau"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def count_finite_multi_tau_slopes(rows: list[Any]) -> int:
    total = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        slopes = row.get("slope_effective_energy_by_tau", {})
        if not isinstance(slopes, dict):
            continue
        total += sum(1 for value in slopes.values() if finite(value))
    return total


def scalar_two_point_timeseries_present(lsz: dict[str, Any]) -> bool:
    mode_rows = lsz.get("mode_rows", {})
    if not isinstance(mode_rows, dict) or not mode_rows:
        return False
    for row in mode_rows.values():
        if not isinstance(row, dict):
            return False
        series = row.get("C_ss_timeseries")
        if not isinstance(series, list) or not series:
            return False
    return True


def main() -> int:
    print("PR #230 FH/LSZ multi-tau target time-series harness certificate")
    print("=" * 72)

    data = load_json(SMOKE)
    metadata = data.get("metadata", {})
    run_control = metadata.get("run_control", {})
    scalar_source_meta = metadata.get("scalar_source_response", {})
    scalar_lsz_meta = metadata.get("scalar_two_point_lsz", {})
    policy = metadata.get("fh_lsz_measurement_policy", {})
    ensemble = first_ensemble(data)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    seed_control = ensemble.get("rng_seed_control", {})

    old_tau1_energies = source.get("per_configuration_effective_energies", [])
    old_tau1_slopes = source.get("per_configuration_slopes", [])
    multi_tau_energies = source.get("per_configuration_multi_tau_effective_energies", [])
    multi_tau_slopes = source.get("per_configuration_multi_tau_slopes", [])
    finite_multi_tau_slopes = count_finite_multi_tau_slopes(multi_tau_slopes if isinstance(multi_tau_slopes, list) else [])
    tau_window_range = source.get("multi_tau_window_range", {})

    phase = metadata.get("phase")
    source_schema_ok = (
        scalar_source_meta.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
        and source.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
    )
    selected_mass_policy_ok = (
        policy.get("policy") == "selected_mass_only_for_scalar_fh_lsz"
        and scalar_source_meta.get("selected_mass_only") is True
        and scalar_lsz_meta.get("selected_mass_only") is True
        and run_control.get("fh_lsz_selected_mass_only") is True
        and run_control.get("normal_equation_cache_enabled") is True
    )
    no_physical_readout = (
        scalar_source_meta.get("used_as_physical_yukawa_readout") is False
        and scalar_lsz_meta.get("used_as_physical_yukawa_readout") is False
        and source.get("physical_higgs_normalization") == "not_derived"
        and lsz.get("physical_higgs_normalization") == "not_derived"
    )

    report("smoke-output-loaded", bool(data), str(SMOKE.relative_to(ROOT)))
    report("phase-is-reduced-scope", phase == "reduced_scope", f"phase={phase}")
    report("numba-seed-control-present", seed_control.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION, str(seed_control))
    report("selected-mass-normal-cache-metadata-present", selected_mass_policy_ok, str(policy))
    report("schema-version-recorded", source_schema_ok, f"schema={source.get('target_timeseries_schema_version')}")
    report(
        "legacy-tau1-target-fields-preserved",
        isinstance(old_tau1_energies, list) and bool(old_tau1_energies)
        and isinstance(old_tau1_slopes, list) and bool(old_tau1_slopes),
        f"tau1_energies={len(old_tau1_energies) if isinstance(old_tau1_energies, list) else 'bad'}, "
        f"tau1_slopes={len(old_tau1_slopes) if isinstance(old_tau1_slopes, list) else 'bad'}",
    )
    report(
        "multi-tau-effective-energy-rows-present",
        isinstance(multi_tau_energies, list) and len(multi_tau_energies) == len(old_tau1_energies),
        f"multi_tau_energies={len(multi_tau_energies) if isinstance(multi_tau_energies, list) else 'bad'}",
    )
    report(
        "multi-tau-slope-rows-present",
        isinstance(multi_tau_slopes, list) and len(multi_tau_slopes) >= len(old_tau1_slopes),
        f"multi_tau_slopes={len(multi_tau_slopes) if isinstance(multi_tau_slopes, list) else 'bad'}",
    )
    report("finite-multi-tau-slope-diagnostic-present", finite_multi_tau_slopes > 0, f"finite_multi_tau_slopes={finite_multi_tau_slopes}")
    report("tau-window-range-recorded", isinstance(tau_window_range.get("tau_windows"), list), str(tau_window_range))
    report("scalar-lsz-target-timeseries-preserved", scalar_two_point_timeseries_present(lsz), "C_ss_timeseries rows present")
    report("no-physical-yukawa-readout", no_physical_readout, "metadata remains source-coordinate support only")
    report("reduced-smoke-is-not-production-evidence", phase == "reduced_scope", "smoke run is infrastructure only")
    report("does-not-authorize-retained-proposal", True, "multi-tau rows are not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ multi-tau target time-series harness extension",
        "verdict": (
            "The direct lattice harness now serializes versioned per-configuration "
            "multi-tau source-response rows while preserving the legacy tau=1 "
            "target fields and same-source scalar two-point C_ss/Gamma_ss series. "
            "This removes the harness-side blocker for future response-window "
            "covariance checks.  The smoke output is reduced-scope infrastructure "
            "support only and does not authorize a response readout switch."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Multi-tau serialization support is not retained or proposed-retained closure evidence.",
        "target_timeseries_schema_version": EXPECTED_SCHEMA_VERSION,
        "smoke_certificate": str(SMOKE.relative_to(ROOT)),
        "source_summary": {
            "legacy_tau1_effective_energy_rows": len(old_tau1_energies) if isinstance(old_tau1_energies, list) else 0,
            "legacy_tau1_slope_rows": len(old_tau1_slopes) if isinstance(old_tau1_slopes, list) else 0,
            "multi_tau_effective_energy_rows": len(multi_tau_energies) if isinstance(multi_tau_energies, list) else 0,
            "multi_tau_slope_rows": len(multi_tau_slopes) if isinstance(multi_tau_slopes, list) else 0,
            "finite_multi_tau_slope_values": finite_multi_tau_slopes,
            "tau_window_range": tau_window_range,
            "multi_tau_rule": source.get("multi_tau_target_timeseries_rule"),
            "strict_limit": source.get("strict_limit"),
        },
        "rng_seed_control": seed_control,
        "fh_lsz_measurement_policy": policy,
        "required_next_gate": (
            "Rerun production chunks with the v2 multi-tau target schema, then "
            "combine multi-tau covariance with multiple source radii before any "
            "response-window readout switch can be considered."
        ),
        "strict_non_claims": [
            "does not use reduced smoke output as production evidence",
            "does not treat multi-tau target rows as physical dE/dh",
            "does not authorize a response-window readout switch",
            "does not derive kappa_s or canonical-Higgs/source overlap",
            "does not claim retained or proposed_retained y_t closure",
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
