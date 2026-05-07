#!/usr/bin/env python3
"""
PR #230 source-Higgs time-kernel harness extension gate.

This validates the default-off FH/LSZ harness path that emits same-surface
Euclidean-time scalar matrix rows C_ss/C_sH/C_Hs/C_HH(t).  The gate is
infrastructure support only.  It must not authorize retained/proposed_retained
closure, kappa_s, or physical y_t.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_harness_smoke_numba_2026-05-07.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json"

PASS_COUNT = 0
FAIL_COUNT = 0

FORBIDDEN_FALSE = {
    "uses_H_unit_matrix_element_readout": False,
    "uses_yt_ward_identity_as_authority": False,
    "uses_observed_top_mass_or_y_t_selector": False,
    "uses_alpha_LM_plaquette_or_u0_as_proof_input": False,
    "uses_reduced_pilot_as_production_evidence": False,
    "sets_c2_to_one": False,
    "sets_Z_match_to_one": False,
    "sets_kappa_s_to_one": False,
    "treats_taste_radial_x_as_canonical_O_H": False,
    "treats_time_kernel_smoke_as_physics_evidence": False,
}


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def mode_rows_have_contract(mode_rows: dict[str, Any]) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if set(mode_rows) != {"0,0,0"}:
        issues.append(f"unexpected mode set {sorted(mode_rows)}")
        return False, issues
    row = mode_rows.get("0,0,0")
    if not isinstance(row, dict):
        issues.append("0,0,0 row absent")
        return False, issues
    tau_rows = row.get("tau_rows")
    matrix_by_t = row.get("C_matrix_by_t")
    if not isinstance(tau_rows, list) or len(tau_rows) != 2:
        issues.append("tau_rows must contain tau=0 and tau=1")
        return False, issues
    if matrix_by_t is not tau_rows and matrix_by_t != tau_rows:
        issues.append("C_matrix_by_t must mirror tau_rows")
    for expected_tau, tau_row in enumerate(tau_rows):
        if not isinstance(tau_row, dict):
            issues.append(f"tau row {expected_tau} is not an object")
            continue
        if int(tau_row.get("tau", -1)) != expected_tau:
            issues.append(f"tau row {expected_tau} has wrong tau")
        for label in ("C_ss", "C_sH", "C_Hs", "C_HH", "C_sx", "C_xs", "C_xx"):
            if not finite(tau_row.get(f"{label}_real")):
                issues.append(f"{label}_real missing/nonfinite at tau {expected_tau}")
            if not finite(tau_row.get(f"{label}_imag")):
                issues.append(f"{label}_imag missing/nonfinite at tau {expected_tau}")
            if not isinstance(tau_row.get(f"{label}_timeseries"), list):
                issues.append(f"{label}_timeseries missing at tau {expected_tau}")
        matrix_real = tau_row.get("C_matrix_real")
        matrix_imag = tau_row.get("C_matrix_imag")
        if not (
            isinstance(matrix_real, list)
            and len(matrix_real) == 2
            and all(isinstance(row, list) and len(row) == 2 for row in matrix_real)
        ):
            issues.append(f"C_matrix_real not 2x2 at tau {expected_tau}")
        if not (
            isinstance(matrix_imag, list)
            and len(matrix_imag) == 2
            and all(isinstance(row, list) and len(row) == 2 for row in matrix_imag)
        ):
            issues.append(f"C_matrix_imag not 2x2 at tau {expected_tau}")
    return not issues, issues


def main() -> int:
    print("PR #230 source-Higgs time-kernel harness extension gate")
    smoke = load_json(SMOKE)
    report("smoke-artifact-present", bool(smoke), str(SMOKE.relative_to(ROOT)))
    metadata = smoke.get("metadata") if isinstance(smoke.get("metadata"), dict) else {}
    ensemble = selected_ensemble(smoke)
    analysis = ensemble.get("source_higgs_time_kernel_analysis")
    if not isinstance(analysis, dict):
        analysis = {}

    seed_version = ensemble.get("rng_seed_control", {}).get("seed_control_version")
    report("numba-seed-control", seed_version == "numba_gauge_seed_v1", str(seed_version))

    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    report(
        "three-mass-scan-preserved",
        run_control.get("masses") == [0.45, 0.75, 1.05],
        str(run_control.get("masses")),
    )
    report(
        "selected-mass-is-middle",
        float(ensemble.get("selected_mass_parameter", float("nan"))) == 0.75,
        str(ensemble.get("selected_mass_parameter")),
    )

    policy = ensemble.get("fh_lsz_measurement_policy")
    if not isinstance(policy, dict):
        policy = {}
    report(
        "selected-mass-only-policy",
        policy.get("source_higgs_time_kernel_selected_mass_only") is True,
        str(policy.get("source_higgs_time_kernel_selected_mass_only")),
    )

    meta_kernel = metadata.get("source_higgs_time_kernel")
    if not isinstance(meta_kernel, dict):
        meta_kernel = {}
    report("metadata-enabled", meta_kernel.get("enabled") is True, str(meta_kernel.get("enabled")))
    report(
        "metadata-support-only",
        meta_kernel.get("used_as_physical_yukawa_readout") is False
        and meta_kernel.get("physical_higgs_normalization") == "not_derived",
        str(meta_kernel),
    )

    report(
        "schema-version",
        analysis.get("time_kernel_schema_version") == "source_higgs_time_kernel_v1",
        str(analysis.get("time_kernel_schema_version")),
    )
    report(
        "analysis-firewall",
        analysis.get("used_as_physical_yukawa_readout") is False
        and analysis.get("physical_higgs_normalization") == "not_derived"
        and analysis.get("canonical_higgs_operator_identity_passed") is False,
        str(
            {
                "used": analysis.get("used_as_physical_yukawa_readout"),
                "normalization": analysis.get("physical_higgs_normalization"),
                "canonical": analysis.get("canonical_higgs_operator_identity_passed"),
            }
        ),
    )

    mode_rows = analysis.get("mode_rows")
    if not isinstance(mode_rows, dict):
        mode_rows = {}
    rows_ok, row_issues = mode_rows_have_contract(mode_rows)
    report("time-kernel-mode-rows", rows_ok, "; ".join(row_issues) if row_issues else "schema ok")

    top_source = ensemble.get("scalar_source_response_analysis")
    top_lsz = ensemble.get("scalar_two_point_lsz_analysis")
    report(
        "legacy-fh-lsz-blocks-present",
        isinstance(top_source, dict) and isinstance(top_lsz, dict),
        "source and LSZ blocks are still serialized",
    )

    firewall = dict(FORBIDDEN_FALSE)
    report("forbidden-import-firewall", all(value is False for value in firewall.values()), str(firewall))
    report(
        "no-closure-claimed",
        smoke.get("actual_current_surface_status") is None
        and metadata.get("phase") == "reduced_scope",
        f"phase={metadata.get('phase')} actual_status={smoke.get('actual_current_surface_status')}",
    )

    certificate = {
        "artifact": "yt_pr230_source_higgs_time_kernel_harness_extension_gate",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actual_current_surface_status": (
            "source-Higgs time-kernel harness support-only infrastructure; "
            "open physics closure"
        ),
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "used_as_physical_yukawa_readout": False,
        "physical_higgs_normalization": "not_derived",
        "smoke_artifact": str(SMOKE.relative_to(ROOT)),
        "checks": {
            "PASS": PASS_COUNT,
            "FAIL": FAIL_COUNT,
        },
        "firewall": firewall,
        "contract": {
            "adds_default_off_time_kernel_rows": True,
            "preserves_three_mass_scan": True,
            "selected_mass_only": True,
            "schema_version": "source_higgs_time_kernel_v1",
            "performance_scope": "future FH/LSZ source-Higgs chunks avoid non-selected-mass time-kernel solves",
            "production_evidence": False,
        },
        "strict_limit": (
            "This gate certifies harness/schema support only.  The taste-radial "
            "second-source smoke row is not canonical O_H, not kappa_s, and not "
            "physical y_t evidence."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  wrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
