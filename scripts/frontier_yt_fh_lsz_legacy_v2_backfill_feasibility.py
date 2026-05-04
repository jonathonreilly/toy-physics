#!/usr/bin/env python3
"""
PR #230 FH/LSZ legacy chunk v2 backfill feasibility audit.

Chunks001-016 were produced before the v2 multi-tau target-timeseries schema.
This runner checks whether those chunks can be honestly upgraded from saved
artifacts.  It does not mutate any chunk output and it does not manufacture
per-configuration covariance rows from aggregate correlators.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_legacy_v2_backfill_feasibility_2026-05-04.json"

LEGACY_RANGE = range(1, 17)
V2_REFERENCE_RANGE = range(17, 37)
EXPECTED_SCHEMA_VERSION = "fh_lsz_target_timeseries_v2_multitau"

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
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def chunk_paths(index: int) -> dict[str, Path]:
    label = f"chunk{index:03d}"
    return {
        "chunk": ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_{label}_2026-05-01.json",
        "artifact": ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_chunks"
        / f"L12_T24_{label}"
        / "L12xT24"
        / "ensemble_measurement.json",
    }


def first_ensemble(chunk: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    ensembles = chunk.get("ensembles")
    if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        return ensembles[0]
    return artifact


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def has_aggregate_correlators(source: dict[str, Any]) -> bool:
    rows = source.get("energy_fits")
    if not isinstance(rows, list) or len(rows) < 3:
        return False
    for row in rows:
        correlator = row.get("correlator")
        if not isinstance(correlator, list) or len(correlator) < 6:
            return False
        if not all(isinstance(point, dict) and finite(point.get("tau")) and finite(point.get("mean")) for point in correlator):
            return False
    return True


def has_legacy_tau1_rows(source: dict[str, Any], expected_measurements: int) -> bool:
    energies = source.get("per_configuration_effective_energies")
    slopes = source.get("per_configuration_slopes")
    return (
        isinstance(energies, list)
        and len(energies) == expected_measurements
        and isinstance(slopes, list)
        and len(slopes) == expected_measurements
    )


def has_v2_rows(source: dict[str, Any], expected_measurements: int) -> bool:
    energies = source.get("per_configuration_multi_tau_effective_energies")
    slopes = source.get("per_configuration_multi_tau_slopes")
    return (
        source.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
        and isinstance(energies, list)
        and len(energies) == expected_measurements
        and isinstance(slopes, list)
        and len(slopes) == expected_measurements
    )


def has_raw_per_configuration_correlators(source: dict[str, Any]) -> bool:
    raw_keys = {
        "source_measurements",
        "per_configuration_correlators",
        "per_configuration_source_shift_correlators",
        "raw_source_shift_correlators",
    }
    if any(key in source for key in raw_keys):
        return True
    energy_fits = source.get("energy_fits")
    if not isinstance(energy_fits, list):
        return False
    for row in energy_fits:
        if isinstance(row, dict) and any(key in row for key in raw_keys):
            return True
    return False


def audit_chunk(index: int) -> dict[str, Any]:
    paths = chunk_paths(index)
    chunk = load_json(paths["chunk"])
    artifact = load_json(paths["artifact"])
    ensemble = first_ensemble(chunk, artifact)
    source = ensemble.get("scalar_source_response_analysis", {})
    if not isinstance(source, dict):
        source = {}
    metadata = chunk.get("metadata", {}) if isinstance(chunk.get("metadata"), dict) else {}
    run_control = metadata.get("run_control", {}) if isinstance(metadata.get("run_control"), dict) else {}
    measurements = int(run_control.get("measurement_sweeps") or ensemble.get("measurement_sweeps") or 0)
    aggregate = has_aggregate_correlators(source)
    legacy_tau1 = has_legacy_tau1_rows(source, measurements)
    v2 = has_v2_rows(source, measurements)
    raw = has_raw_per_configuration_correlators(source)
    return {
        "chunk_index": index,
        "chunk_output_present": bool(chunk),
        "artifact_present": bool(artifact),
        "measurement_sweeps": measurements,
        "aggregate_correlators_present": aggregate,
        "legacy_tau1_per_configuration_rows_present": legacy_tau1,
        "v2_multi_tau_rows_present": v2,
        "raw_per_configuration_correlators_present": raw,
        "schema_version": source.get("target_timeseries_schema_version"),
        "honest_v2_backfill_possible": bool(raw and not v2),
        "aggregate_only_backfill_possible": bool(aggregate and legacy_tau1 and not raw and not v2),
        "strict_limit": (
            "Aggregate source-shift correlators can reconstruct only aggregate "
            "multi-tau slopes. They cannot reconstruct per-configuration "
            "multi-tau covariance rows required by the v2 response-window gates."
        ),
    }


def main() -> int:
    print("PR #230 FH/LSZ legacy v2 backfill feasibility audit")
    print("=" * 72)

    legacy_rows = [audit_chunk(index) for index in LEGACY_RANGE]
    v2_rows = [audit_chunk(index) for index in V2_REFERENCE_RANGE]

    legacy_outputs_present = all(row["chunk_output_present"] and row["artifact_present"] for row in legacy_rows)
    legacy_has_aggregate = all(row["aggregate_correlators_present"] for row in legacy_rows)
    legacy_has_tau1 = all(row["legacy_tau1_per_configuration_rows_present"] for row in legacy_rows)
    legacy_lacks_v2 = all(not row["v2_multi_tau_rows_present"] for row in legacy_rows)
    legacy_lacks_raw = all(not row["raw_per_configuration_correlators_present"] for row in legacy_rows)
    aggregate_only = all(row["aggregate_only_backfill_possible"] for row in legacy_rows)
    honest_backfill_possible = any(row["honest_v2_backfill_possible"] for row in legacy_rows)
    v2_reference_present = all(row["v2_multi_tau_rows_present"] for row in v2_rows)
    v2_reference_lacks_proposal = True

    report("legacy-chunk-artifacts-present", legacy_outputs_present, f"chunks={LEGACY_RANGE.start:03d}-{LEGACY_RANGE.stop - 1:03d}")
    report("legacy-aggregate-correlators-present", legacy_has_aggregate, "aggregate energy-fit correlators exist")
    report("legacy-tau1-per-configuration-rows-present", legacy_has_tau1, "tau=1 target rows exist")
    report("legacy-v2-multi-tau-rows-absent", legacy_lacks_v2, "legacy chunks predate v2 schema")
    report("legacy-raw-per-configuration-correlators-absent", legacy_lacks_raw, "raw source-shift correlator time series are not stored")
    report("aggregate-only-backfill-detected", aggregate_only, "only aggregate multi-tau reconstruction would be possible")
    report("honest-v2-backfill-not-possible", not honest_backfill_possible, f"possible={honest_backfill_possible}")
    report("v2-reference-chunks-have-schema", v2_reference_present, f"chunks={V2_REFERENCE_RANGE.start:03d}-{V2_REFERENCE_RANGE.stop - 1:03d}")
    report("v2-reference-not-physical-readout", v2_reference_lacks_proposal, "v2 rows remain support-only")
    report("does-not-authorize-retained-proposal", True, "schema feasibility is not source-Higgs closure")

    result = {
        "actual_current_surface_status": "exact negative boundary / legacy chunks001-016 cannot be honestly v2-backfilled",
        "verdict": (
            "Chunks001-016 contain aggregate source-shift correlators and "
            "legacy tau=1 per-configuration target rows, but they do not store "
            "the raw per-configuration source-shift correlator time series "
            "needed to reconstruct v2 multi-tau covariance rows.  Recomputing "
            "aggregate multi-tau slopes from averaged correlators would be a "
            "schema-padded surrogate, not the v2 production evidence consumed "
            "by the response-window gates."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Backfill feasibility is run-control bookkeeping only; it does not close scalar LSZ or O_H/source-overlap.",
        "bare_retained_allowed": False,
        "legacy_range": [LEGACY_RANGE.start, LEGACY_RANGE.stop - 1],
        "v2_reference_range": [V2_REFERENCE_RANGE.start, V2_REFERENCE_RANGE.stop - 1],
        "legacy_summary": {
            "outputs_present": legacy_outputs_present,
            "aggregate_correlators_present": legacy_has_aggregate,
            "tau1_per_configuration_rows_present": legacy_has_tau1,
            "v2_multi_tau_rows_absent": legacy_lacks_v2,
            "raw_per_configuration_correlators_absent": legacy_lacks_raw,
            "honest_v2_backfill_possible": honest_backfill_possible,
            "aggregate_only_backfill_possible": aggregate_only,
        },
        "v2_reference_summary": {
            "v2_rows_present_for_all_reference_chunks": v2_reference_present,
            "used_as_physical_yukawa_readout": False,
        },
        "legacy_chunks": legacy_rows,
        "v2_reference_chunks": v2_rows,
        "strict_non_claims": [
            "does not mutate legacy chunk artifacts",
            "does not synthesize per-configuration v2 covariance rows from aggregate correlators",
            "does not treat tau=1 legacy rows as multi-tau response-window evidence",
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1, cos(theta)=1, c2=1, or Z_match=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use chunks017+ as the honest v2 multi-tau population for covariance "
            "diagnostics, or rerun chunks001-016 with the v2 harness if an "
            "all-1000-configuration same-schema covariance table becomes "
            "required.  Do not backfill legacy chunks from aggregate correlators."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
