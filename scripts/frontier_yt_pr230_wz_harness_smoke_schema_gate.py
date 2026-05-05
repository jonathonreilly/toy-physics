#!/usr/bin/env python3
"""
PR #230 W/Z harness smoke-schema gate.

This runner exercises the default-off W/Z mass-response smoke path in the
direct top-correlator harness.  The path exists only to validate schema and
firewall plumbing for a future same-source W/Z response campaign.  It writes no
production W/Z evidence and cannot authorize retained/proposed-retained
top-Yukawa closure.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
SMOKE_OUTPUT = ROOT / "outputs" / "yt_pr230_wz_harness_smoke_schema_smoke_2026-05-05.json"
SMOKE_DIR = ROOT / "outputs" / "yt_pr230_wz_harness_smoke_schema_tmp"
OUTPUT = ROOT / "outputs" / "yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json"

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


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def is_nan(value: Any) -> bool:
    return isinstance(value, float) and math.isnan(value)


def rows_from_mode_container(container: Any) -> list[dict[str, Any]]:
    if isinstance(container, dict):
        return [row for row in container.values() if isinstance(row, dict)]
    if isinstance(container, list):
        return [row for row in container if isinstance(row, dict)]
    return []


def run_smoke_harness() -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(HARNESS),
        "--volumes",
        "2x4",
        "--masses",
        "0.45,0.75,1.05",
        "--therm",
        "0",
        "--measurements",
        "2",
        "--separation",
        "0",
        "--overrelax",
        "0",
        "--engine",
        "numba",
        "--production-targets",
        "--scalar-source-shifts=-0.01,0.0,0.01",
        "--scalar-two-point-modes",
        "0,0,0;1,0,0;0,1,0;0,0,1",
        "--scalar-two-point-noises",
        "2",
        "--wz-mass-response-smoke",
        "--wz-source-shifts=-0.01,0.0,0.01",
        "--wz-boson-channel",
        "W",
        "--production-output-dir",
        str(SMOKE_DIR),
        "--seed",
        "2026050501",
        "--output",
        str(SMOKE_OUTPUT),
    ]
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def validate_artifact(data: dict[str, Any]) -> dict[str, bool]:
    metadata = data.get("metadata", {})
    run_control = metadata.get("run_control", {})
    wz_meta = metadata.get("wz_mass_response", {})
    ensembles = data.get("ensembles", [])
    ensemble = ensembles[0] if isinstance(ensembles, list) and ensembles else {}
    scalar = ensemble.get("scalar_source_response_analysis", {}) if isinstance(ensemble, dict) else {}
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {}) if isinstance(ensemble, dict) else {}
    lsz_rows = rows_from_mode_container(lsz.get("mode_rows", [])) if isinstance(lsz, dict) else []
    wz = ensemble.get("wz_mass_response_analysis", {}) if isinstance(ensemble, dict) else {}
    wz_rows = wz.get("per_source_shift_rows", []) if isinstance(wz, dict) else []
    gauge_response = wz.get("gauge_response", {}) if isinstance(wz, dict) else {}
    firewall = wz.get("firewall", {}) if isinstance(wz, dict) else {}
    ew_coupling = wz.get("electroweak_coupling", {}) if isinstance(wz, dict) else {}
    identities = wz.get("identity_certificates", {}) if isinstance(wz, dict) else {}
    seed = ensemble.get("rng_seed_control", {}) if isinstance(ensemble, dict) else {}

    row_checks = []
    for row in wz_rows if isinstance(wz_rows, list) else []:
        mass_fit = row.get("w_mass_fit", {}) if isinstance(row, dict) else {}
        correlator = row.get("correlator", []) if isinstance(row, dict) else []
        row_checks.append(
            isinstance(row, dict)
            and finite(row.get("source_shift"))
            and row.get("configuration_count", 0) >= 2
            and isinstance(mass_fit, dict)
            and mass_fit.get("from_correlator") is True
            and mass_fit.get("correlator_source") == "synthetic_scout_contract_not_EW_field"
            and finite(mass_fit.get("mass_lat"))
            and float(mass_fit.get("mass_lat")) > 0.0
            and finite(mass_fit.get("mass_lat_err"))
            and float(mass_fit.get("mass_lat_err")) >= 0.0
            and isinstance(correlator, list)
            and len(correlator) >= 4
            and all(isinstance(point, dict) and finite(point.get("tau")) and finite(point.get("mean")) for point in correlator)
        )

    source_shifts = [row.get("source_shift") for row in wz_rows if isinstance(row, dict)] if isinstance(wz_rows, list) else []
    source_shift_contract = (
        any(finite(x) and float(x) < 0.0 for x in source_shifts)
        and any(finite(x) and abs(float(x)) <= 1.0e-15 for x in source_shifts)
        and any(finite(x) and float(x) > 0.0 for x in source_shifts)
    )
    firewall_false = all(value is False for value in firewall.values()) if isinstance(firewall, dict) and firewall else False
    identities_false = (
        isinstance(identities, dict)
        and identities.get("same_source_sector_overlap_identity_passed") is False
        and identities.get("canonical_higgs_pole_identity_passed") is False
        and identities.get("retained_route_or_proposal_gate_passed") is False
    )
    lsz_timeseries_ok = bool(lsz_rows) and all("C_ss_timeseries" in row for row in lsz_rows)

    return {
        "metadata_wz_enabled": wz_meta.get("enabled") is True,
        "metadata_wz_smoke_status": wz_meta.get("implementation_status") == "smoke_schema_enabled_not_ew_production",
        "metadata_wz_not_production": wz_meta.get("production_wz_rows_written") is False,
        "metadata_wz_not_readout": wz_meta.get("used_as_physical_yukawa_readout") is False,
        "run_control_records_smoke": run_control.get("wz_mass_response_smoke") is True,
        "ensemble_numba_seed_control": seed.get("seed_control_version") == "numba_gauge_seed_v1",
        "scalar_effective_energies_present": isinstance(scalar.get("per_configuration_effective_energies"), list)
        and len(scalar.get("per_configuration_effective_energies")) >= 2,
        "scalar_slopes_present": isinstance(scalar.get("per_configuration_slopes"), list)
        and len(scalar.get("per_configuration_slopes")) >= 2,
        "lsz_mode_rows_c_ss_timeseries_present": lsz_timeseries_ok,
        "wz_phase_scout": wz.get("phase") == "scout",
        "wz_same_source_coordinate_schema_only": wz.get("same_source_coordinate") is True
        and wz.get("same_source_identity_certified") is False
        and wz.get("same_source_coordinate_certification_status") == "schema_only_not_physics_authority",
        "wz_mass_fits_from_correlators": wz.get("wz_mass_fits_from_correlators") is True,
        "wz_rows_neg_zero_pos": source_shift_contract,
        "wz_rows_have_contract": bool(row_checks) and all(row_checks),
        "wz_slope_finite": finite(gauge_response.get("slope_dM_W_ds"))
        and finite(gauge_response.get("slope_error"))
        and gauge_response.get("slope_error") >= 0.0,
        "wz_covariance_absent_in_smoke": gauge_response.get("covariance_status") == "absent_in_smoke_schema"
        and is_nan(gauge_response.get("cov_dE_top_dM_W")),
        "electroweak_coupling_not_selector": ew_coupling.get("used_observed_g2_as_selector") is False
        and ew_coupling.get("g2") is None,
        "identity_certificates_false": identities_false,
        "firewall_all_false": firewall_false,
        "not_physical_yukawa_readout": wz.get("used_as_physical_yukawa_readout") is False,
    }


def main() -> int:
    print("PR #230 W/Z harness smoke-schema gate")
    print("=" * 72)

    completed = run_smoke_harness()
    report("smoke-command-exits-zero", completed.returncode == 0, f"returncode={completed.returncode}")
    report("smoke-output-written", SMOKE_OUTPUT.exists(), display(SMOKE_OUTPUT))

    data: dict[str, Any] = {}
    if SMOKE_OUTPUT.exists():
        data = json.loads(SMOKE_OUTPUT.read_text(encoding="utf-8"))
    checks = validate_artifact(data) if data else {}
    for name, ok in checks.items():
        report(name.replace("_", "-"), ok, str(ok))

    result = {
        "actual_current_surface_status": "bounded-support / WZ harness smoke schema path",
        "verdict": (
            "The direct top-correlator harness can now emit default-off W/Z "
            "mass-response smoke rows for schema validation.  The smoke rows "
            "are synthetic positive correlators on the selected top mass only; "
            "they preserve seed metadata and scalar FH/LSZ target series, but "
            "do not define a same-source EW action, do not certify the "
            "source-coordinate identity, do not carry top/WZ covariance, and "
            "are not production W/Z evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Smoke-schema support is infrastructure only; same-source EW "
            "action, production W/Z correlators, covariance, sector identity, "
            "canonical-Higgs/source overlap, and retained-route gates remain open."
        ),
        "bare_retained_allowed": False,
        "wz_harness_smoke_schema_gate_passed": FAIL_COUNT == 0,
        "smoke_artifact": display(SMOKE_OUTPUT),
        "volume_artifact_dir": display(SMOKE_DIR),
        "command_returncode": completed.returncode,
        "command_stdout_tail": completed.stdout.splitlines()[-12:],
        "command_stderr_tail": completed.stderr.splitlines()[-12:],
        "schema_checks": checks,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write production W/Z rows",
            "does not treat synthetic smoke slopes as dM_W/ds evidence",
            "does not certify same-source EW action or source-coordinate identity",
            "does not use static EW algebra, H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use this schema as a harness contract only; the physics route still "
            "requires a genuine same-source EW action and production W/Z "
            "correlator mass-fit rows, or another canonical-Higgs/source-overlap "
            "closure path."
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
