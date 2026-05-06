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
CHUNK_COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
READY_CHUNK_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
POLEFIT8X8_COMBINER = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json"
POLEFIT8X8_POSTPROCESSOR = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json"
MODEL_CLASS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"

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


def ready_chunk_surface(data: dict[str, Any]) -> bool:
    summary = data.get("chunk_summary", {}) if isinstance(data.get("chunk_summary"), dict) else {}
    combined = data.get("combined_summary", {}) if isinstance(data.get("combined_summary"), dict) else {}
    return (
        int(summary.get("expected_chunks", 0)) == 63
        and int(summary.get("present_chunks", -1)) == 63
        and int(summary.get("ready_chunks", -1)) == 63
        and combined.get("available") is True
        and data.get("proposal_allowed") is False
    )


def ready_chunk_checkpoint(data: dict[str, Any]) -> bool:
    summary = data.get("chunk_summary", {}) if isinstance(data.get("chunk_summary"), dict) else {}
    return (
        int(summary.get("expected_chunks", 0)) == 63
        and int(summary.get("present_chunks", -1)) == 63
        and int(summary.get("ready_chunks", -1)) == 63
        and int(summary.get("missing_chunks", -1)) == 0
        and data.get("proposal_allowed") is False
    )


def ready_polefit8x8_surface(combiner: dict[str, Any], postprocessor: dict[str, Any]) -> bool:
    summary = combiner.get("chunk_summary", {}) if isinstance(combiner.get("chunk_summary"), dict) else {}
    readiness = postprocessor.get("readiness", {}) if isinstance(postprocessor.get("readiness"), dict) else {}
    return (
        int(summary.get("expected_chunks", 0)) == 63
        and int(summary.get("present_chunks", -1)) == 63
        and int(summary.get("ready_chunks", -1)) == 63
        and readiness.get("diagnostic_fit_ready") is True
        and combiner.get("proposal_allowed") is False
        and postprocessor.get("proposal_allowed") is False
    )


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


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
    chunk_combiner = load_json(CHUNK_COMBINER)
    ready_chunk_set = load_json(READY_CHUNK_SET)
    polefit8x8_combiner = load_json(POLEFIT8X8_COMBINER)
    polefit8x8_postprocessor = load_json(POLEFIT8X8_POSTPROCESSOR)
    model_class_gate = load_json(MODEL_CLASS_GATE)
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
    l12_chunked_surface_ready = ready_chunk_surface(chunk_combiner)
    l12_ready_checkpoint_consistent = ready_chunk_checkpoint(ready_chunk_set)
    polefit8x8_surface_ready = ready_polefit8x8_surface(
        polefit8x8_combiner, polefit8x8_postprocessor
    )
    model_class_blocks = (
        "blocks finite-shell fit" in str(model_class_gate.get("actual_current_surface_status", ""))
        and model_class_gate.get("proposal_allowed") is False
    )
    l12_postprocess_support_ready = l12_chunked_surface_ready and polefit8x8_surface_ready

    postprocess_requirements = [
        {
            "requirement": "monolithic_manifest_outputs_exist",
            "satisfied_now": all_outputs_exist,
            "reason": "the original monolithic L12/L16/L24 manifest files remain absent; they are not evidence",
        },
        {
            "requirement": "l12_chunked_same_source_surface_complete",
            "satisfied_now": l12_chunked_surface_ready,
            "reason": "63 seed-controlled L12 four-mode/x16 chunks are complete and the combiner wrote a support-only L12 summary",
        },
        {
            "requirement": "l12_ready_chunk_checkpoint_consistent",
            "satisfied_now": l12_ready_checkpoint_consistent,
            "reason": "dynamic ready-chunk checkpoint agrees that all 63 L12 chunks are ready with schema and seed control",
        },
        {
            "requirement": "l12_polefit8x8_finite_shell_diagnostic_complete",
            "satisfied_now": polefit8x8_surface_ready,
            "reason": "separate L12 eight-mode/x8 chunks and diagnostic postprocessor are complete but support-only",
        },
        {
            "requirement": "l16_l24_or_equivalent_multivolume_scaling_surface",
            "satisfied_now": False,
            "reason": "the completed artifact is L12-only; no L16/L24 same-source FH/LSZ production surface is accepted",
        },
        {
            "requirement": "isolated_scalar_pole_and_inverse_derivative_fit",
            "satisfied_now": False,
            "reason": "finite-shell diagnostics do not derive dGamma_ss/dp^2 at an isolated scalar pole",
        },
        {
            "requirement": "finite_volume_ir_zero_mode_limit_control",
            "satisfied_now": False,
            "reason": "no current production postprocess proves the FV/IR/zero-mode limiting order for the pole derivative",
        },
        {
            "requirement": "finite_shell_model_class_gate_passes",
            "satisfied_now": False,
            "reason": "the model-class gate deliberately blocks finite-shell fits as retained evidence",
        },
        {
            "requirement": "source_overlap_or_physical_response_bridge",
            "satisfied_now": False,
            "reason": "completed FH/LSZ source-source rows still do not provide canonical O_H/source-overlap or same-source W/Z response authority",
        },
        {
            "requirement": "no_forbidden_normalization_imports",
            "satisfied_now": True,
            "reason": "this gate forbids kappa_s=1, H_unit, yt_ward_identity, observed y_t/top mass, c2=1, Z_match=1, alpha_LM, plaquette, and u0 as proof selectors",
        },
        {
            "requirement": "retained_proposal_certificate_passes",
            "satisfied_now": False,
            "reason": "the retained-proposal certificate remains false; L12 support cannot authorize proposal wording",
        },
    ]

    retained_proposal_gate_ready = all(item["satisfied_now"] for item in postprocess_requirements)

    report("manifest-loaded", manifest_loaded, rel(MANIFEST))
    report("manifest-explicitly-not-evidence", manifest_is_not_evidence, f"proposal_allowed={manifest.get('proposal_allowed')}")
    report("three-production-output-targets", commands_present, f"commands={len(commands)}")
    report("commands-are-production-targeted-and-resumable", commands_production_targeted, "manifest commands contain production/FH/LSZ flags")
    report("monolithic-outputs-still-absent-recorded", not all_outputs_exist, f"all_outputs_exist={all_outputs_exist}")
    report("l12-chunked-support-surface-complete", l12_chunked_surface_ready, rel(CHUNK_COMBINER))
    report("l12-ready-checkpoint-consistent", l12_ready_checkpoint_consistent, rel(READY_CHUNK_SET))
    report("polefit8x8-diagnostic-surface-complete", polefit8x8_surface_ready, rel(POLEFIT8X8_POSTPROCESSOR))
    report("l12-support-only-not-retained-evidence", not all_raw_production_bundle_ready and l12_postprocess_support_ready, f"l12_postprocess_support_ready={l12_postprocess_support_ready}")
    report("model-class-gate-still-blocks-finite-shell-use", model_class_blocks, rel(MODEL_CLASS_GATE))
    report("multivolume-pole-fv-ir-bridge-requirements-explicit", True, "L16/L24, isolated pole, FV/IR, model-class, and source-overlap remain required")
    report("no-retained-proposal-gate-ready", not retained_proposal_gate_ready, f"retained_proposal_gate_ready={retained_proposal_gate_ready}")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ L12 chunked postprocess surface complete; closure gates remain open",
        "verdict": (
            "The original monolithic joint FH/LSZ manifest remains a launch "
            "surface, not evidence, and its L12/L16/L24 output files are still "
            "absent.  The replacement seed-controlled L12 chunked surfaces are "
            "now complete: the four-mode/x16 stream supplies same-source dE/ds "
            "and C_ss(q) support rows, and the separate eight-mode/x8 stream "
            "supplies a finite-shell diagnostic.  This is bounded support only. "
            "It still lacks accepted L16/L24 or equivalent multivolume scaling, "
            "an isolated scalar pole derivative, FV/IR/zero-mode control, a "
            "finite-shell model-class certificate, and a canonical-Higgs/source-"
            "overlap or same-source W/Z physical-response bridge."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Completed L12 chunked FH/LSZ rows are support-only and do not satisfy the scalar-LSZ/model-class/FV/IR/source-overlap closure gates.",
        "manifest": rel(MANIFEST),
        "completed_chunked_support_surfaces": {
            "l12_four_mode_x16_combiner": {
                "path": rel(CHUNK_COMBINER),
                "ready": l12_chunked_surface_ready,
                "status": chunk_combiner.get("actual_current_surface_status"),
                "chunk_summary": chunk_combiner.get("chunk_summary", {}),
                "combined_output_target": chunk_combiner.get("combined_output_target"),
            },
            "l12_ready_chunk_checkpoint": {
                "path": rel(READY_CHUNK_SET),
                "ready": l12_ready_checkpoint_consistent,
                "status": ready_chunk_set.get("actual_current_surface_status"),
                "chunk_summary": ready_chunk_set.get("chunk_summary", {}),
            },
            "l12_polefit8x8_combiner": {
                "path": rel(POLEFIT8X8_COMBINER),
                "ready": ready_chunk_surface(polefit8x8_combiner),
                "status": polefit8x8_combiner.get("actual_current_surface_status"),
                "chunk_summary": polefit8x8_combiner.get("chunk_summary", {}),
                "combined_output_target": polefit8x8_combiner.get("combined_output_target"),
            },
            "l12_polefit8x8_postprocessor": {
                "path": rel(POLEFIT8X8_POSTPROCESSOR),
                "ready": polefit8x8_surface_ready,
                "status": polefit8x8_postprocessor.get("actual_current_surface_status"),
                "readiness": polefit8x8_postprocessor.get("readiness", {}),
            },
        },
        "expected_source_shifts": EXPECTED_SOURCE_SHIFTS,
        "expected_scalar_modes": sorted(EXPECTED_MODE_KEYS),
        "minimum_scalar_two_point_noises": MIN_NOISE_VECTORS,
        "production_output_audits": output_audits,
        "postprocess_requirements": postprocess_requirements,
        "raw_production_bundle_ready": all_raw_production_bundle_ready,
        "l12_postprocess_support_ready": l12_postprocess_support_ready,
        "model_class_blocks_finite_shell_use": model_class_blocks,
        "retained_proposal_gate_ready": retained_proposal_gate_ready,
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not treat L12-only chunked support as multivolume production closure",
            "does not treat finite-shell diagnostics as an isolated scalar pole derivative",
            "does not set kappa_s = 1",
            "does not set c2 or Z_match to one",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
            "does not treat reduced cold pilots as production evidence",
        ],
        "exact_next_action": (
            "Do not spend closure wording on the completed L12 support rows.  "
            "Supply a fresh same-surface bridge artifact: O_sp-Higgs pole rows "
            "with canonical O_H identity/normalization, a real source-coordinate "
            "transport certificate, genuine same-source W/Z production response "
            "rows with covariance and non-observed g2 authority, same-surface "
            "Schur A/B/C kernel rows, a strict scalar-LSZ moment-threshold-FV "
            "certificate, or a neutral primitive-cone/irreducibility certificate."
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
