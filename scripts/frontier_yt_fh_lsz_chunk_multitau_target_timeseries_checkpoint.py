#!/usr/bin/env python3
"""
PR #230 FH/LSZ v2 multi-tau chunk target-timeseries checkpoint.

This runner audits one completed L12_T24 FH/LSZ production chunk for the
versioned multi-tau source-response rows emitted by the optimized production
harness.  It is performance/infrastructure support only: it never promotes a
source-only FH/LSZ chunk to retained or proposed-retained y_t evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SCHEMA_VERSION = "fh_lsz_target_timeseries_v2_multitau"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
EXPECTED_SELECTED_MASS = 0.75

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-index", type=int, required=True, help="L12_T24 chunk index, e.g. 17.")
    parser.add_argument("--production-date", default="2026-05-01", help="Date suffix on the production chunk JSON.")
    parser.add_argument("--certificate-date", default="2026-05-03", help="Date suffix for the emitted checkpoint JSON.")
    parser.add_argument("--output", default=None, help="Optional explicit output certificate path.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def expected_base_seed(chunk_index: int) -> int:
    return 2026051000 + int(chunk_index)


def expected_volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def chunk_paths(chunk_index: int, production_date: str, certificate_date: str, output: str | None) -> dict[str, Path]:
    chunk_label = f"chunk{chunk_index:03d}"
    default_output = (
        ROOT
        / "outputs"
        / f"yt_fh_lsz_{chunk_label}_multitau_target_timeseries_checkpoint_{certificate_date}.json"
    )
    return {
        "chunk": ROOT
        / "outputs"
        / f"yt_pr230_fh_lsz_production_L12_T24_{chunk_label}_{production_date}.json",
        "artifact": ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
        / f"L12_T24_{chunk_label}"
        / "L12xT24"
        / "ensemble_measurement.json",
        "output": Path(output) if output else default_output,
    }


def round_set(rows: list[Any], key: str) -> set[float]:
    values: set[float] = set()
    for row in rows:
        if isinstance(row, dict) and finite(row.get(key)):
            values.add(round(float(row[key]), 8))
    return values


def target_timeseries_modes(mode_rows: dict[str, Any]) -> list[str]:
    return [
        key
        for key, row in mode_rows.items()
        if isinstance(row, dict) and isinstance(row.get("C_ss_timeseries"), list) and row.get("C_ss_timeseries")
    ]


def count_finite_multi_tau_slopes(rows: list[Any]) -> int:
    total = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        slopes = row.get("slope_effective_energy_by_tau")
        if not isinstance(slopes, dict):
            continue
        total += sum(1 for value in slopes.values() if finite(value))
    return total


def energy_fits_have_selected_base_mass(rows: list[Any]) -> bool:
    bases: set[float] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        effective_mass = row.get("effective_bare_mass_lat")
        source_shift = row.get("source_shift_lat")
        if finite(effective_mass) and finite(source_shift):
            bases.add(round(float(effective_mass) - float(source_shift), 8))
    return bases == {round(EXPECTED_SELECTED_MASS, 8)}


def disabled_or_guarded(guard: Any) -> bool:
    return not guard or (isinstance(guard, dict) and guard.get("enabled") is False)


def main() -> int:
    args = parse_args()
    chunk_index = int(args.chunk_index)
    paths = chunk_paths(chunk_index, args.production_date, args.certificate_date, args.output)
    expected_seed = expected_base_seed(chunk_index)

    print(f"PR #230 FH/LSZ chunk{chunk_index:03d} v2 multi-tau target-timeseries checkpoint")
    print("=" * 78)

    chunk = load_json(paths["chunk"])
    artifact = load_json(paths["artifact"])
    metadata = chunk.get("metadata", {})
    run_control = metadata.get("run_control", {})
    source_meta = metadata.get("scalar_source_response", {})
    lsz_meta = metadata.get("scalar_two_point_lsz", {})
    policy = metadata.get("fh_lsz_measurement_policy", {})
    ensemble = first_ensemble(chunk)
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    mode_rows = lsz.get("mode_rows", {}) if isinstance(lsz, dict) else {}
    seed_control = ensemble.get("rng_seed_control")
    measurements = int(run_control.get("measurement_sweeps") or 16)

    energy_fits = source.get("energy_fits", []) if isinstance(source, dict) else []
    old_tau1_energies = source.get("per_configuration_effective_energies", []) if isinstance(source, dict) else []
    old_tau1_slopes = source.get("per_configuration_slopes", []) if isinstance(source, dict) else []
    multi_tau_energies = source.get("per_configuration_multi_tau_effective_energies", []) if isinstance(source, dict) else []
    multi_tau_slopes = source.get("per_configuration_multi_tau_slopes", []) if isinstance(source, dict) else []
    finite_multi_tau_slopes = count_finite_multi_tau_slopes(multi_tau_slopes if isinstance(multi_tau_slopes, list) else [])
    tau_window_range = source.get("multi_tau_window_range", {}) if isinstance(source, dict) else {}
    source_shifts = round_set(energy_fits if isinstance(energy_fits, list) else [], "source_shift_lat")
    mode_keys = set(mode_rows) if isinstance(mode_rows, dict) else set()
    css_timeseries_modes = target_timeseries_modes(mode_rows if isinstance(mode_rows, dict) else {})

    schema_ok = (
        source_meta.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
        and source.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
    )
    seed_valid = (
        isinstance(seed_control, dict)
        and seed_control.get("seed_control_version") == EXPECTED_SEED_CONTROL_VERSION
        and seed_control.get("base_seed") == expected_seed
        and seed_control.get("gauge_rng_seed") == expected_volume_seed(expected_seed)
        and seed_control.get("numba_gauge_seeded_before_thermalization") is True
    )
    selected_mass_policy_ok = (
        policy.get("policy") == "selected_mass_only_for_scalar_fh_lsz"
        and source_meta.get("selected_mass_only") is True
        and lsz_meta.get("selected_mass_only") is True
        and run_control.get("fh_lsz_selected_mass_only") is True
        and run_control.get("normal_equation_cache_enabled") is True
        and abs(float(policy.get("selected_mass_parameter", -1.0)) - EXPECTED_SELECTED_MASS) < 1.0e-12
    )
    selected_mass_rows_ok = (
        energy_fits_have_selected_base_mass(energy_fits if isinstance(energy_fits, list) else [])
        and isinstance(multi_tau_energies, list)
        and len(multi_tau_energies) == measurements
        and isinstance(multi_tau_slopes, list)
        and len(multi_tau_slopes) == measurements
    )
    no_physical_readout = (
        source_meta.get("used_as_physical_yukawa_readout") is False
        and lsz_meta.get("used_as_physical_yukawa_readout") is False
        and source.get("physical_higgs_normalization") == "not_derived"
        and lsz.get("physical_higgs_normalization") == "not_derived"
    )
    guarded_cross_sector = disabled_or_guarded(metadata.get("source_higgs_cross_correlator")) and disabled_or_guarded(
        metadata.get("wz_mass_response")
    )

    report("chunk-output-present", bool(chunk), str(paths["chunk"].relative_to(ROOT)))
    report("chunk-artifact-present", bool(artifact), str(paths["artifact"].relative_to(ROOT)))
    report("production-phase", metadata.get("phase") == "production", str(metadata.get("phase")))
    report(
        "run-control-seed-volume-statistics",
        run_control.get("seed") == expected_seed
        and run_control.get("volumes") == "12x24"
        and run_control.get("thermalization_sweeps") == 1000
        and run_control.get("measurement_sweeps") == 16
        and run_control.get("measurement_separation_sweeps") == 20,
        str(run_control),
    )
    report("numba-seed-control-present", seed_valid, str(seed_control))
    report("selected-mass-only-normal-cache-policy", selected_mass_policy_ok, str(policy))
    report("schema-version-recorded", schema_ok, f"schema={source.get('target_timeseries_schema_version')}")
    report(
        "same-source-fh-response-present",
        finite(source.get("slope_dE_ds_lat")) and source_shifts == {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS},
        f"slope={source.get('slope_dE_ds_lat')}, shifts={sorted(source_shifts)}",
    )
    report("same-source-lsz-modes-present", EXPECTED_MODE_KEYS <= mode_keys, f"modes={sorted(mode_keys)}")
    report(
        "legacy-tau1-target-fields-preserved",
        isinstance(old_tau1_energies, list)
        and len(old_tau1_energies) == measurements
        and isinstance(old_tau1_slopes, list)
        and len(old_tau1_slopes) == measurements,
        f"tau1_energies={len(old_tau1_energies) if isinstance(old_tau1_energies, list) else 'bad'}, "
        f"tau1_slopes={len(old_tau1_slopes) if isinstance(old_tau1_slopes, list) else 'bad'}, "
        f"measurements={measurements}",
    )
    report(
        "multi-tau-effective-energy-rows-present",
        isinstance(multi_tau_energies, list) and len(multi_tau_energies) == measurements,
        f"multi_tau_energies={len(multi_tau_energies) if isinstance(multi_tau_energies, list) else 'bad'}",
    )
    report(
        "multi-tau-slope-rows-present",
        isinstance(multi_tau_slopes, list) and len(multi_tau_slopes) == measurements,
        f"multi_tau_slopes={len(multi_tau_slopes) if isinstance(multi_tau_slopes, list) else 'bad'}",
    )
    report("finite-multi-tau-slope-diagnostic-present", finite_multi_tau_slopes > 0, f"finite={finite_multi_tau_slopes}")
    report("tau-window-range-recorded", isinstance(tau_window_range.get("tau_windows"), list), str(tau_window_range))
    report(
        "selected-mass-only-rows",
        selected_mass_rows_ok,
        "energy-fit base masses are 0.75 and multi-tau rows follow selected-mass-only policy",
    )
    report(
        "scalar-lsz-target-timeseries-present",
        EXPECTED_MODE_KEYS <= set(css_timeseries_modes),
        f"timeseries_modes={sorted(css_timeseries_modes)}",
    )
    report("cross-sector-readout-rows-absent-or-guarded", guarded_cross_sector, "source-Higgs and W/Z guards remain disabled")
    report("no-physical-yukawa-readout", no_physical_readout, "metadata remains source-coordinate support only")
    report("does-not-authorize-retained-proposal", True, "v2 chunk rows are not canonical-Higgs/source-overlap closure")

    result = {
        "actual_current_surface_status": (
            f"bounded-support / FH-LSZ chunk{chunk_index:03d} v2 multi-tau target-timeseries checkpoint"
        ),
        "verdict": (
            f"L12_T24 chunk{chunk_index:03d} carries production metadata, fixed numba seed control, "
            "selected-mass-only source-response/LSZ metadata, legacy tau=1 target rows, and v2 "
            "multi-tau source-response rows.  This is infrastructure support for later covariance "
            "and response-window gates only; it is not a physical y_t readout."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Source-only FH/LSZ rows do not derive kappa_s, source-Higgs overlap, W/Z response, "
            "or retained top-Yukawa closure."
        ),
        "chunk_index": chunk_index,
        "chunk_output": str(paths["chunk"].relative_to(ROOT)),
        "chunk_artifact": str(paths["artifact"].relative_to(ROOT)),
        "target_timeseries_schema_version": EXPECTED_SCHEMA_VERSION,
        "chunk_summary": {
            "phase": metadata.get("phase"),
            "seed": run_control.get("seed"),
            "expected_seed": expected_seed,
            "seed_control_version": run_control.get("seed_control_version"),
            "seed_independence_valid": seed_valid,
            "selected_mass_policy": policy,
            "scalar_source_response_metadata": source_meta,
            "scalar_two_point_lsz_metadata": lsz_meta,
            "legacy_tau1_effective_energy_rows": len(old_tau1_energies) if isinstance(old_tau1_energies, list) else 0,
            "legacy_tau1_slope_rows": len(old_tau1_slopes) if isinstance(old_tau1_slopes, list) else 0,
            "multi_tau_effective_energy_rows": len(multi_tau_energies) if isinstance(multi_tau_energies, list) else 0,
            "multi_tau_slope_rows": len(multi_tau_slopes) if isinstance(multi_tau_slopes, list) else 0,
            "finite_multi_tau_slope_values": finite_multi_tau_slopes,
            "tau_window_range": tau_window_range,
            "scalar_lsz_target_timeseries_modes": sorted(css_timeseries_modes),
            "slope_dE_ds_lat": source.get("slope_dE_ds_lat"),
            "slope_dE_ds_lat_err": source.get("slope_dE_ds_lat_err"),
            "source_higgs_guard": metadata.get("source_higgs_cross_correlator"),
            "wz_response_guard": metadata.get("wz_mass_response"),
        },
        "strict_non_claims": [
            "does not use source-only FH/LSZ as physical y_t",
            "does not set kappa_s = 1",
            "does not set Z_match = 1",
            "does not set c2 = 1",
            "does not use H_unit, Ward authority, observed values, alpha_LM, plaquette, or u0 as proof input",
            "does not treat a single chunk as retained or proposed-retained evidence",
        ],
        "exact_next_action": (
            "Accumulate more v2 chunks, then run a same-schema multi-tau response-window covariance "
            "gate with multiple source radii or a same-surface source-Higgs/WZ identity before any "
            "readout switch can be considered."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    paths["output"].write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {paths['output'].relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
