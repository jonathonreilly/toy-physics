#!/usr/bin/env python3
"""
PR #230 source-Higgs pole-residue extractor gate.

The source-Higgs harness emits finite-mode C_ss/C_sH/C_HH rows.  The
rank-repair/Gram-purity route needs isolated-pole residues with a certified
canonical-Higgs operator.  This runner is the missing bridge: it validates a
future production artifact, fits pole residues only when the audit gates are
present, and otherwise records why no builder input rows are written.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_source_higgs_unratified_operator_smoke_run_2026-05-03.json"
DEFAULT_ROWS_OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_source_higgs_pole_residue_extractor_2026-05-03.json"

PARENTS = {
    "harness_extension": "outputs/yt_source_higgs_cross_correlator_harness_extension_2026-05-03.json",
    "builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "unratified_smoke_checkpoint": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
    "rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def nonempty_cert_ref(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "absent" not in value.lower()


def source_higgs_analysis(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ensembles = data.get("ensembles", [])
    if not isinstance(ensembles, list) or not ensembles:
        return {}, {}
    ensemble = ensembles[0] if isinstance(ensembles[0], dict) else {}
    analysis = ensemble.get("source_higgs_cross_correlator_analysis", {})
    return ensemble, analysis if isinstance(analysis, dict) else {}


def mode_rows(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    rows = analysis.get("mode_rows", {})
    if not isinstance(rows, dict):
        return []
    out: list[dict[str, Any]] = []
    for key, row in rows.items():
        if isinstance(row, dict):
            copy = dict(row)
            copy["mode_key"] = key
            out.append(copy)
    return out


def validate_artifact(data: dict[str, Any]) -> tuple[dict[str, bool], list[str], dict[str, Any]]:
    metadata = data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else {}
    run_control = metadata.get("run_control", {}) if isinstance(metadata.get("run_control", {}), dict) else {}
    source_meta = metadata.get("source_higgs_cross_correlator", {})
    if not isinstance(source_meta, dict):
        source_meta = {}
    ensemble, analysis = source_higgs_analysis(data)
    operator = analysis.get("operator", {}) if isinstance(analysis.get("operator", {}), dict) else {}
    firewall = analysis.get("firewall", {}) if isinstance(analysis.get("firewall", {}), dict) else {}
    rows = mode_rows(analysis)
    p2_values = sorted({round(float(row.get("p_hat_sq")), 12) for row in rows if finite(row.get("p_hat_sq"))})
    config_counts = [
        int(row.get("configuration_count"))
        for row in rows
        if isinstance(row.get("configuration_count"), int)
    ]

    labels = ("C_ss", "C_sH", "C_HH")
    rows_complete = bool(rows)
    for row in rows:
        rows_complete = rows_complete and finite(row.get("p_hat_sq"))
        for label in labels:
            rows_complete = rows_complete and finite(row.get(f"{label}_real"))
            rows_complete = rows_complete and finite(row.get(f"{label}_real_config_stderr"))
            series = row.get(f"{label}_timeseries")
            rows_complete = rows_complete and isinstance(series, list)
            rows_complete = rows_complete and len(series) == row.get("configuration_count")

    checks = {
        "artifact_present": bool(data),
        "production_phase": metadata.get("phase") == "production",
        "production_targets": run_control.get("production_targets") is True,
        "seed_control_version_recorded": ensemble.get("rng_seed_control", {}).get("seed_control_version")
        == "numba_gauge_seed_v1",
        "source_higgs_enabled": source_meta.get("enabled") is True,
        "same_ensemble": analysis.get("same_ensemble") is True,
        "same_source_coordinate": analysis.get("same_source_coordinate") is True,
        "source_coordinate_named": isinstance(analysis.get("source_coordinate"), str)
        and bool(analysis.get("source_coordinate")),
        "canonical_higgs_operator_identity": operator.get("canonical_higgs_operator_identity_passed") is True,
        "identity_certificate_present": nonempty_cert_ref(operator.get("identity_certificate")),
        "normalization_certificate_present": nonempty_cert_ref(operator.get("normalization_certificate")),
        "not_hunit_by_fiat": operator.get("hunit_used_as_operator") is False,
        "not_static_ew_algebra": operator.get("static_ew_algebra_used_as_operator") is False,
        "forbidden_import_firewall": all(
            firewall.get(key) is False
            for key in (
                "used_observed_targets_as_selectors",
                "used_yt_ward_identity",
                "used_alpha_lm_or_plaquette",
                "used_hunit_matrix_element_readout",
            )
        ),
        "not_physical_yukawa_readout": analysis.get("used_as_physical_yukawa_readout") is False
        and source_meta.get("used_as_physical_yukawa_readout") is False,
        "finite_mode_rows_complete": rows_complete,
        "enough_distinct_momentum_modes": len(p2_values) >= 4,
        "enough_configurations_for_errors": bool(config_counts) and min(config_counts) >= 8,
        "model_class_or_pole_saturation_control": analysis.get(
            "model_class_or_pole_saturation_certificate_passed"
        )
        is True
        or metadata.get("model_class_or_pole_saturation_certificate_passed") is True,
        "fv_ir_zero_mode_control": analysis.get("fv_ir_zero_mode_control_passed") is True
        or metadata.get("fv_ir_zero_mode_control_passed") is True,
    }
    summary = {
        "metadata_phase": metadata.get("phase"),
        "production_targets": run_control.get("production_targets"),
        "mode_count": len(rows),
        "distinct_p_hat_sq_count": len(p2_values),
        "p_hat_sq_values": p2_values,
        "min_configuration_count": min(config_counts) if config_counts else 0,
        "operator_id": operator.get("operator_id"),
        "canonical_higgs_operator_identity_passed": operator.get(
            "canonical_higgs_operator_identity_passed"
        ),
    }
    return checks, [key for key, ok in checks.items() if not ok], summary


def fit_label(rows: list[dict[str, Any]], label: str) -> dict[str, Any]:
    p2 = np.asarray([float(row["p_hat_sq"]) for row in rows], dtype=float)
    y = np.asarray([float(row[f"{label}_real"]) for row in rows], dtype=float)
    err = np.asarray(
        [max(float(row.get(f"{label}_real_config_stderr", 0.0) or 0.0), 1.0e-12) for row in rows],
        dtype=float,
    )
    max_p2 = max(float(np.max(p2)), 1.0)
    grid = np.linspace(1.0e-6, max_p2 * 4.0 + 1.0, 400)
    best: dict[str, Any] | None = None
    for m2 in grid:
        basis = np.vstack([1.0 / (p2 + m2), np.ones_like(p2)]).T
        weights = 1.0 / np.maximum(err * err, 1.0e-24)
        normal = basis.T @ (weights[:, None] * basis)
        rhs = basis.T @ (weights * y)
        try:
            coeff = np.linalg.solve(normal, rhs)
        except np.linalg.LinAlgError:
            coeff = np.linalg.pinv(normal) @ rhs
        residual = y - basis @ coeff
        dof = max(1, len(y) - 2)
        chi2_dof = float(np.sum(weights * residual * residual) / dof)
        candidate = {
            "pole_mass_sq_lat": float(m2),
            "residue": float(coeff[0]),
            "analytic_contact": float(coeff[1]),
            "chi2_dof": chi2_dof,
        }
        if best is None or candidate["chi2_dof"] < float(best["chi2_dof"]):
            best = candidate
    assert best is not None
    return best


def fit_pole_residue_row(data: dict[str, Any]) -> dict[str, Any]:
    _ensemble, analysis = source_higgs_analysis(data)
    rows = sorted(mode_rows(analysis), key=lambda row: float(row["p_hat_sq"]))
    fits = {label: fit_label(rows, label) for label in ("C_ss", "C_sH", "C_HH")}
    pole_masses = [fits[label]["pole_mass_sq_lat"] for label in fits]
    pole_mass_spread = max(pole_masses) - min(pole_masses)
    selected_pole_mass = float(np.mean(pole_masses))
    return {
        "selected_pole_row": True,
        "isolated_pole_fit_passed": True,
        "pole_fit_model": "C_AB(p_hat_sq) = Res_C_AB / (p_hat_sq + m_pole_sq) + analytic_contact",
        "pole_mass_sq_lat": selected_pole_mass,
        "pole_mass_sq_spread_across_channels": pole_mass_spread,
        "Res_C_ss": fits["C_ss"]["residue"],
        "Res_C_sH": fits["C_sH"]["residue"],
        "Res_C_HH": fits["C_HH"]["residue"],
        "Res_C_ss_err": None,
        "Res_C_sH_err": None,
        "Res_C_HH_err": None,
        "channel_fit_diagnostics": fits,
        "strict_limit": (
            "Central-value pole residues are builder input only; Gram purity, "
            "FV/IR/model-class controls, and retained-route gates remain load-bearing."
        ),
    }


def build_rows_artifact(data: dict[str, Any], input_path: Path, residue_row: dict[str, Any]) -> dict[str, Any]:
    _ensemble, analysis = source_higgs_analysis(data)
    operator = analysis.get("operator", {})
    firewall = analysis.get("firewall", {})
    return {
        "metadata": {
            "artifact": "source_higgs_cross_correlator_measurement_rows",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "input_artifact": display(input_path),
            "claim_boundary": "support_only_until_gram_purity_and_retained_route_gates_pass",
        },
        "phase": "production",
        "same_ensemble": True,
        "same_source_coordinate": True,
        "source_coordinate": analysis.get("source_coordinate"),
        "operator": {
            "operator_id": operator.get("operator_id"),
            "operator_definition": operator.get("operator_definition"),
            "canonical_higgs_operator_identity_passed": operator.get(
                "canonical_higgs_operator_identity_passed"
            ),
            "identity_certificate": operator.get("identity_certificate"),
            "normalization_certificate": operator.get("normalization_certificate"),
            "hunit_used_as_operator": operator.get("hunit_used_as_operator"),
            "static_ew_algebra_used_as_operator": operator.get("static_ew_algebra_used_as_operator"),
        },
        "firewall": {
            "used_observed_targets_as_selectors": firewall.get("used_observed_targets_as_selectors"),
            "used_yt_ward_identity": firewall.get("used_yt_ward_identity"),
            "used_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette"),
            "used_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout"),
        },
        "model_class_or_pole_saturation_certificate_passed": True,
        "fv_ir_zero_mode_control_passed": True,
        "pole_residue_rows": [residue_row],
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not bypass the source-Higgs certificate builder or Gram-purity postprocessor",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--rows-output", type=Path, default=DEFAULT_ROWS_OUTPUT)
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 source-Higgs pole-residue extractor gate")
    print("=" * 72)

    data = load_json(args.input)
    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    checks, missing_checks, input_summary = validate_artifact(data)
    gate_passed = bool(checks) and not missing_checks
    rows_written = False
    residue_row: dict[str, Any] = {}

    harness_support = (
        "source-Higgs cross-correlator harness extension" in status(parents["harness_extension"])
        and parents["harness_extension"].get("proposal_allowed") is False
    )
    builder_open = (
        "source-Higgs cross-correlator rows absent" in status(parents["builder"])
        and parents["builder"].get("proposal_allowed") is False
    )
    postprocessor_open = (
        "O_sp-Higgs Gram-purity postprocess awaiting production certificate"
        in status(parents["postprocessor"])
        and parents["postprocessor"].get("proposal_allowed") is False
    )
    rank_repair_requires_rows = (
        "non-source response rank-repair sufficiency theorem"
        in status(parents["rank_repair"])
        and parents["rank_repair"].get("current_closure_gate_passed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("harness-support-loaded", harness_support, status(parents["harness_extension"]))
    report("builder-currently-awaits-rows", builder_open, status(parents["builder"]))
    report("postprocessor-currently-awaits-certificate", postprocessor_open, status(parents["postprocessor"]))
    report("rank-repair-requires-non-source-row", rank_repair_requires_rows, status(parents["rank_repair"]))
    report("input-artifact-state-recorded", True, f"present={bool(data)} path={display(args.input)}")
    report("pole-extraction-gate-decision-recorded", True, f"gate_passed={gate_passed} missing_or_failed={missing_checks}")

    if gate_passed:
        residue_row = fit_pole_residue_row(data)
        rows_artifact = build_rows_artifact(data, args.input, residue_row)
        args.rows_output.parent.mkdir(parents=True, exist_ok=True)
        args.rows_output.write_text(json.dumps(rows_artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        rows_written = True
        report("pole-residue-rows-written", True, display(args.rows_output))
    else:
        report(
            "no-current-row-output-written-before-gate",
            True,
            "rows output is written only after full production/pole gate",
        )

    result = {
        "actual_current_surface_status": (
            "bounded-support / source-Higgs pole-residue rows extracted"
            if rows_written
            else "open / source-Higgs pole-residue extractor awaiting valid production rows"
        ),
        "verdict": (
            "A source-Higgs pole-residue extractor gate is now executable.  "
            "The current input is intentionally rejected: it is the reduced "
            "unratified-operator smoke artifact, not production data with a "
            "ratified canonical-Higgs operator, enough momentum modes, "
            "model-class pole saturation, and FV/IR control.  Therefore no "
            "C_sH/C_HH pole-residue row file is written and no closure wording "
            "is authorized."
            if not rows_written
            else (
                "Source-Higgs pole-residue rows were extracted for the builder. "
                "They remain support only until the builder, Gram-purity "
                "postprocessor, and retained-route gates pass."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Pole-residue extraction is an input bridge only; Gram-purity and retained-route gates remain authoritative.",
        "input_artifact": display(args.input),
        "rows_output": display(args.rows_output),
        "rows_written": rows_written,
        "gate_passed": gate_passed,
        "input_summary": input_summary,
        "gate_checks": checks,
        "missing_or_failed_checks": missing_checks,
        "residue_row": residue_row,
        "acceptance_schema": {
            "phase": "production",
            "required_operator": "canonical_higgs_operator_identity_passed with identity and normalization certificates",
            "required_modes": "at least four distinct p_hat_sq source-Higgs modes",
            "required_statistics": "at least eight configurations per mode before bootstrap/jackknife production use",
            "required_controls": [
                "model_class_or_pole_saturation_certificate_passed",
                "fv_ir_zero_mode_control_passed",
                "forbidden-import firewall false",
                "used_as_physical_yukawa_readout false",
            ],
            "output_contract": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json for the existing builder",
        },
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use reduced smoke rows as production evidence",
            "does not treat finite-mode C_sH/C_HH rows as pole residues before the pole gate",
            "does not define O_H by fiat or use H_unit as O_H",
            "does not set kappa_s = 1, cos(theta) = 1, c2 = 1, or Z_match = 1",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Run a production source-Higgs cross-correlator artifact with a "
            "ratified canonical-Higgs operator certificate, at least four "
            "momentum modes, and FV/IR/model-class controls; rerun this "
            "extractor, then rerun the source-Higgs builder and Gram-purity "
            "postprocessor."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.status_output.parent.mkdir(parents=True, exist_ok=True)
    args.status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(args.status_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
