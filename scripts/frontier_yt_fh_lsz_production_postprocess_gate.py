#!/usr/bin/env python3
"""
PR #230 FH/LSZ production postprocess gate.

This runner is a strict acceptance boundary for the joint Feynman-Hellmann /
same-source scalar-LSZ production route.  It does not launch production and it
does not treat a manifest as evidence.  It verifies the manifest shape, audits
the expected production outputs if they exist, and records the exact
postprocess requirements that must be satisfied before a retained-proposal
certificate may even be attempted.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_production_manifest_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_production_postprocess_gate_2026-05-01.json"

EXPECTED_SOURCE_SHIFTS = [-0.01, 0.0, 0.01]
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
MIN_NOISE_VECTORS = 16

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
    return json.loads(path.read_text(encoding="utf-8"))


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or not ensembles:
        return {}
    first = ensembles[0]
    return first if isinstance(first, dict) else {}


def source_response_ready(ensemble: dict[str, Any]) -> tuple[bool, list[str]]:
    issues: list[str] = []
    response = ensemble.get("scalar_source_response_analysis")
    if not isinstance(response, dict) or not response:
        return False, ["missing scalar_source_response_analysis"]

    shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in response.get("energy_fits", [])
        if isinstance(row, dict) and finite_number(row.get("source_shift_lat"))
    }
    expected = {round(value, 8) for value in EXPECTED_SOURCE_SHIFTS}
    if shifts != expected:
        issues.append(f"source shifts {sorted(shifts)} != expected {sorted(expected)}")
    if response.get("fit_kind") != "linear_dE_ds":
        issues.append(f"fit_kind={response.get('fit_kind')!r}")
    if not finite_number(response.get("slope_dE_ds_lat")):
        issues.append("missing finite slope_dE_ds_lat")
    if not finite_number(response.get("slope_dE_ds_lat_err")):
        issues.append("missing finite slope_dE_ds_lat_err")
    if response.get("physical_higgs_normalization") != "not_derived":
        issues.append("scalar response claims physical Higgs normalization")
    return not issues, issues


def scalar_lsz_ready(data: dict[str, Any], ensemble: dict[str, Any]) -> tuple[bool, list[str]]:
    issues: list[str] = []
    metadata = data.get("metadata", {})
    lsz_metadata = metadata.get("scalar_two_point_lsz") if isinstance(metadata, dict) else {}
    if not isinstance(lsz_metadata, dict) or lsz_metadata.get("enabled") is not True:
        issues.append("metadata.scalar_two_point_lsz.enabled is not true")
    noise_vectors = lsz_metadata.get("noise_vectors_per_configuration")
    if not isinstance(noise_vectors, int) or noise_vectors < MIN_NOISE_VECTORS:
        issues.append(f"noise_vectors_per_configuration={noise_vectors!r}")

    analysis = ensemble.get("scalar_two_point_lsz_analysis")
    if not isinstance(analysis, dict) or not analysis:
        return False, issues + ["missing scalar_two_point_lsz_analysis"]
    mode_rows = analysis.get("mode_rows")
    if not isinstance(mode_rows, dict):
        issues.append("missing scalar two-point mode_rows")
    else:
        missing_modes = sorted(EXPECTED_MODE_KEYS - set(mode_rows))
        if missing_modes:
            issues.append(f"missing scalar momentum modes {missing_modes}")
        for key in EXPECTED_MODE_KEYS & set(mode_rows):
            row = mode_rows.get(key, {})
            if not finite_number(row.get("Gamma_ss_real")):
                issues.append(f"{key} missing finite Gamma_ss_real")
            if int(row.get("configuration_count", 0)) <= 0:
                issues.append(f"{key} has no configurations")
    proxy = analysis.get("finite_difference_residue_proxy", {})
    if not isinstance(proxy, dict) or proxy.get("available") is not True:
        issues.append("finite residue proxy missing")
    if analysis.get("physical_higgs_normalization") != "not_derived":
        issues.append("scalar LSZ analysis claims physical Higgs normalization")
    return not issues, issues


def audit_output(command_row: dict[str, Any]) -> dict[str, Any]:
    rel_output = command_row.get("output", "")
    path = ROOT / rel_output
    data = load_json(path)
    if not data:
        return {
            "label": command_row.get("label"),
            "volume": command_row.get("volume"),
            "path": rel_output,
            "exists": False,
            "phase": None,
            "production_phase": False,
            "source_response_ready": False,
            "scalar_lsz_ready": False,
            "retained_evidence_ready": False,
            "issues": ["production output absent"],
        }

    metadata = data.get("metadata", {})
    phase = metadata.get("phase") if isinstance(metadata, dict) else data.get("phase")
    ensemble = selected_ensemble(data)
    response_ok, response_issues = source_response_ready(ensemble)
    lsz_ok, lsz_issues = scalar_lsz_ready(data, ensemble)
    production_phase = phase == "production"
    no_forbidden_readout = True
    forbidden_issues: list[str] = []
    if isinstance(metadata, dict):
        for key in ("scalar_source_response", "scalar_two_point_lsz"):
            block = metadata.get(key, {})
            if isinstance(block, dict) and block.get("used_as_physical_yukawa_readout") is not False:
                no_forbidden_readout = False
                forbidden_issues.append(f"metadata.{key}.used_as_physical_yukawa_readout is not false")

    issues = []
    if not production_phase:
        issues.append(f"phase={phase!r}, expected 'production'")
    issues.extend(response_issues)
    issues.extend(lsz_issues)
    issues.extend(forbidden_issues)

    return {
        "label": command_row.get("label"),
        "volume": command_row.get("volume"),
        "path": rel_output,
        "exists": True,
        "phase": phase,
        "production_phase": production_phase,
        "source_response_ready": response_ok,
        "scalar_lsz_ready": lsz_ok,
        "no_forbidden_physical_readout": no_forbidden_readout,
        "retained_evidence_ready": production_phase and response_ok and lsz_ok and no_forbidden_readout,
        "issues": issues,
    }


def command_has_required_flags(command: str) -> bool:
    required = [
        "--production-targets",
        "--resume",
        "--scalar-source-shifts",
        "--scalar-two-point-modes",
        "--scalar-two-point-noises",
    ]
    return all(flag in command for flag in required)


def main() -> int:
    print("PR #230 FH/LSZ production postprocess gate")
    print("=" * 72)

    manifest = load_json(MANIFEST)
    commands = manifest.get("commands", []) if manifest else []
    output_audits = [audit_output(row) for row in commands if isinstance(row, dict)]

    manifest_loaded = bool(manifest)
    manifest_is_not_evidence = manifest.get("manifest_only") is True and manifest.get("proposal_allowed") is False
    commands_present = len(commands) == 3
    commands_production_targeted = all(
        isinstance(row, dict) and command_has_required_flags(str(row.get("command", "")))
        for row in commands
    )
    all_outputs_exist = all(row.get("exists") for row in output_audits) if output_audits else False
    all_outputs_production = all(row.get("production_phase") for row in output_audits) if output_audits else False
    all_source_response_ready = all(row.get("source_response_ready") for row in output_audits) if output_audits else False
    all_scalar_lsz_ready = all(row.get("scalar_lsz_ready") for row in output_audits) if output_audits else False
    all_raw_production_bundle_ready = all(
        row.get("retained_evidence_ready") for row in output_audits
    ) if output_audits else False

    postprocess_requirements = [
        {
            "requirement": "all_manifest_outputs_exist",
            "satisfied_now": all_outputs_exist,
            "reason": "each expected production JSON must be present before evidence is considered",
        },
        {
            "requirement": "all_outputs_mark_phase_production",
            "satisfied_now": all_outputs_production,
            "reason": "reduced_scope and pilot outputs are scout evidence only",
        },
        {
            "requirement": "common_ensemble_correlated_dE_ds_fit",
            "satisfied_now": all_source_response_ready,
            "reason": "the accepted observable is dE_top/ds from symmetric source shifts on the same ensembles",
        },
        {
            "requirement": "same_source_scalar_two_point_lsz_modes",
            "satisfied_now": all_scalar_lsz_ready,
            "reason": "Gamma_ss(q) must be measured for the same additive source with sufficient noise vectors",
        },
        {
            "requirement": "isolated_scalar_pole_and_inverse_derivative_fit",
            "satisfied_now": False,
            "reason": "no production pole-fit certificate derives dGamma_ss/dp^2 at an isolated scalar pole",
        },
        {
            "requirement": "finite_volume_ir_zero_mode_limit_control",
            "satisfied_now": False,
            "reason": "no current production postprocess proves the FV/IR/zero-mode limiting order for the pole derivative",
        },
        {
            "requirement": "no_forbidden_normalization_imports",
            "satisfied_now": True,
            "reason": "this gate only accepts same-source LSZ residue measurement and forbids kappa_s=1, H_unit, yt_ward_identity, observed y_t/top mass, c2=1, and Z_match=1 as proof selectors",
        },
        {
            "requirement": "retained_proposal_certificate_passes",
            "satisfied_now": False,
            "reason": "the retained-proposal certificate has not been run on production pole data and currently remains false",
        },
    ]

    retained_proposal_gate_ready = all(item["satisfied_now"] for item in postprocess_requirements)

    report("manifest-loaded", manifest_loaded, str(MANIFEST.relative_to(ROOT)))
    report("manifest-explicitly-not-evidence", manifest_is_not_evidence, f"proposal_allowed={manifest.get('proposal_allowed')}")
    report("three-production-output-targets", commands_present, f"commands={len(commands)}")
    report("commands-are-production-targeted-and-resumable", commands_production_targeted, "manifest commands contain production/FH/LSZ flags")
    report("current-production-outputs-not-yet-all-present", not all_outputs_exist, f"all_outputs_exist={all_outputs_exist}")
    report("no-current-output-qualifies-for-retained-evidence", not all_raw_production_bundle_ready, f"raw_bundle_ready={all_raw_production_bundle_ready}")
    report("pole-fit-requirement-explicit", not postprocess_requirements[4]["satisfied_now"], postprocess_requirements[4]["reason"])
    report("fv-ir-zero-mode-control-explicit", not postprocess_requirements[5]["satisfied_now"], postprocess_requirements[5]["reason"])
    report("no-retained-proposal-gate-ready", not retained_proposal_gate_ready, f"retained_proposal_gate_ready={retained_proposal_gate_ready}")

    result = {
        "actual_current_surface_status": "open / FH-LSZ production postprocess gate blocks manifest-as-evidence",
        "verdict": (
            "The joint FH/LSZ production manifest is a valid launch surface but "
            "not evidence.  The expected production files are absent or "
            "incomplete, and even complete raw production files would still "
            "need a same-source scalar pole fit, dGamma_ss/dp^2 at the pole, "
            "finite-volume/IR/zero-mode control, and a retained-proposal "
            "certificate before physical y_t wording is allowed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No production FH/LSZ output and pole-derivative postprocess certificate currently satisfy the acceptance gate.",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "expected_source_shifts": EXPECTED_SOURCE_SHIFTS,
        "expected_scalar_modes": sorted(EXPECTED_MODE_KEYS),
        "minimum_scalar_two_point_noises": MIN_NOISE_VECTORS,
        "production_output_audits": output_audits,
        "postprocess_requirements": postprocess_requirements,
        "raw_production_bundle_ready": all_raw_production_bundle_ready,
        "retained_proposal_gate_ready": retained_proposal_gate_ready,
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set c2 or Z_match to one",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not treat reduced cold pilots as production evidence",
        ],
        "exact_next_action": (
            "Either launch/schedule the manifest and then run this gate on the "
            "completed production files plus a pole-fit certificate, or pivot "
            "to a new analytic scalar denominator/residue theorem."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
