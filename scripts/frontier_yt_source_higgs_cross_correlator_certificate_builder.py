#!/usr/bin/env python3
"""
Build/validate a PR #230 source-Higgs cross-correlator production certificate.

This is the concrete input contract for the selected Gram-purity lane.  It
does not manufacture O_H/C_sH/C_HH data.  When a future measurement row file is
present, it validates the claim firewall, attaches the already-derived
Legendre/LSZ source-pole operator normalization, computes both raw and
O_sp-normalized pole-residue Gram quantities, and writes the candidate
certificate consumed by
frontier_yt_source_higgs_gram_purity_postprocessor.py.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
STATUS_OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json"
SOURCE_POLE_OPERATOR = ROOT / "outputs" / "yt_legendre_source_pole_operator_construction_2026-05-03.json"
GENUINE_SOURCE_POLE_INTAKE = (
    ROOT / "outputs" / "yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json"
)

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def pick_pole_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    explicit = [row for row in rows if row.get("selected_pole_row") is True]
    if explicit:
        return explicit[0]
    isolated = [row for row in rows if row.get("isolated_pole_fit_passed") is True]
    if isolated:
        return isolated[0]
    return rows[0]


def compute_gram(row: dict[str, Any]) -> dict[str, Any]:
    c_ss = float(row["Res_C_ss"])
    c_sh = float(row["Res_C_sH"])
    c_hh = float(row["Res_C_HH"])
    product = c_ss * c_hh
    delta = product - c_sh * c_sh
    rho = c_sh / math.sqrt(product) if product > 0.0 else float("nan")
    dgamma_ss = 1.0 / c_ss if c_ss > 0.0 else float("nan")
    c_sp_h = c_sh * math.sqrt(dgamma_ss) if dgamma_ss > 0.0 else float("nan")
    delta_sp_h = c_hh - c_sp_h * c_sp_h if math.isfinite(c_sp_h) else float("nan")
    rho_sp_h = c_sp_h / math.sqrt(c_hh) if c_hh > 0.0 and math.isfinite(c_sp_h) else float("nan")
    return {
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sh,
        "Res_C_HH": c_hh,
        "Res_C_ss_err": row.get("Res_C_ss_err"),
        "Res_C_sH_err": row.get("Res_C_sH_err"),
        "Res_C_HH_err": row.get("Res_C_HH_err"),
        "gram_determinant": delta,
        "normalized_overlap_rho_sH": rho,
        "Dprime_ss_at_pole": dgamma_ss,
        "Res_C_sp_sp": 1.0 if c_ss > 0.0 else None,
        "Res_C_spH": c_sp_h,
        "osp_higgs_gram_determinant": delta_sp_h,
        "normalized_overlap_rho_spH": rho_sp_h,
        "purity_gate_passed_by_central_values": product > 0.0 and abs(delta) <= 1.0e-9 and abs(abs(rho) - 1.0) <= 1.0e-9,
        "osp_higgs_purity_gate_passed_by_central_values": (
            c_hh > 0.0
            and math.isfinite(delta_sp_h)
            and math.isfinite(rho_sp_h)
            and abs(delta_sp_h) <= 1.0e-9
            and abs(abs(rho_sp_h) - 1.0) <= 1.0e-9
        ),
    }


def validate_measurement_input(data: dict[str, Any]) -> tuple[dict[str, bool], list[str]]:
    rows = data.get("pole_residue_rows", [])
    if not isinstance(rows, list):
        rows = []
    row = pick_pole_row(rows)
    firewall = data.get("firewall", {})
    operator = data.get("operator", {})
    checks = {
        "production_phase": data.get("phase") == "production",
        "same_ensemble": data.get("same_ensemble") is True,
        "same_source_coordinate": data.get("same_source_coordinate") is True,
        "has_source_coordinate": isinstance(data.get("source_coordinate"), str) and bool(data.get("source_coordinate")),
        "canonical_higgs_operator_identity": operator.get("canonical_higgs_operator_identity_passed") is True,
        "canonical_higgs_operator_named": isinstance(operator.get("operator_id"), str) and bool(operator.get("operator_id")),
        "has_identity_certificate": isinstance(operator.get("identity_certificate"), str)
        and bool(operator.get("identity_certificate")),
        "has_normalization_certificate": isinstance(operator.get("normalization_certificate"), str)
        and bool(operator.get("normalization_certificate")),
        "not_hunit_by_fiat": operator.get("hunit_used_as_operator") is False,
        "not_static_ew_algebra": operator.get("static_ew_algebra_used_as_operator") is False,
        "no_observed_target_selectors": firewall.get("used_observed_targets_as_selectors") is False,
        "no_prior_ward_authority": firewall.get("used_yt_ward_identity") is False,
        "no_alpha_lm_or_plaquette_authority": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout") is False,
        "has_pole_rows": bool(rows),
        "has_selected_res_c_ss": finite(row.get("Res_C_ss")),
        "has_selected_res_c_sh": finite(row.get("Res_C_sH")),
        "has_selected_res_c_hh": finite(row.get("Res_C_HH")),
        "isolated_pole_or_model_gate": row.get("isolated_pole_fit_passed") is True
        or data.get("model_class_or_pole_saturation_certificate_passed") is True,
        "fv_ir_zero_mode_control": data.get("fv_ir_zero_mode_control_passed") is True,
    }
    return checks, [key for key, ok in checks.items() if not ok]


def source_pole_summary(source_pole: dict[str, Any], intake: dict[str, Any]) -> dict[str, Any]:
    candidate = source_pole.get("operator_candidate", {})
    intake_ok = (
        intake.get("artifact_is_genuine_current_surface_support") is True
        and intake.get("artifact_is_physics_closure") is False
        and intake.get("same_surface_source_coordinate") is True
        and intake.get("source_rescaling_invariant") is True
        and intake.get("contact_term_invariant") is True
        and intake.get("canonical_higgs_operator_identity_passed") is False
        and intake.get("proposal_allowed") is False
    )
    return {
        "operator_id": candidate.get("operator_id"),
        "certificate": str(SOURCE_POLE_OPERATOR.relative_to(ROOT)),
        "genuine_intake_certificate": str(GENUINE_SOURCE_POLE_INTAKE.relative_to(ROOT)),
        "genuine_source_pole_intake_passed": intake_ok,
        "artifact_is_genuine_current_surface_support": intake.get(
            "artifact_is_genuine_current_surface_support"
        ),
        "artifact_is_physics_closure": intake.get("artifact_is_physics_closure"),
        "same_surface_source_coordinate": intake.get("same_surface_source_coordinate"),
        "source_rescaling_invariant": intake.get("source_rescaling_invariant"),
        "contact_term_invariant": intake.get("contact_term_invariant"),
        "source_pole_operator_constructed": source_pole.get("source_pole_operator_constructed") is True,
        "source_pole_residue_normalized_to_one": candidate.get("source_pole_residue_normalized_to_one") is True,
        "canonical_higgs_operator_identity_passed": source_pole.get("canonical_higgs_operator_identity_passed") is True,
        "strict_limit": (
            "O_sp is the normalized source-pole side only; O_sp = O_H still "
            "requires the O_sp-Higgs Gram-purity postprocessor or an equivalent identity certificate."
        ),
    }


def build_candidate(
    data: dict[str, Any], input_path: Path, source_pole: dict[str, Any], intake: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, bool], list[str]]:
    checks, missing = validate_measurement_input(data)
    row = pick_pole_row(data.get("pole_residue_rows", []))
    gram = compute_gram(row) if all(checks[k] for k in ("has_selected_res_c_ss", "has_selected_res_c_sh", "has_selected_res_c_hh")) else {}
    operator = data.get("operator", {})
    firewall = data.get("firewall", {})
    sp_summary = source_pole_summary(source_pole, intake)
    checks["legendre_lsz_source_pole_operator_available"] = (
        sp_summary["source_pole_operator_constructed"] is True
        and sp_summary["source_pole_residue_normalized_to_one"] is True
        and sp_summary["canonical_higgs_operator_identity_passed"] is False
    )
    checks["genuine_source_pole_intake_available"] = (
        sp_summary["genuine_source_pole_intake_passed"] is True
    )
    missing = [key for key, ok in checks.items() if not ok]
    candidate = {
        "metadata": {
            "artifact": "source_higgs_cross_correlator_production_candidate",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "input_rows": str(input_path.relative_to(ROOT)) if input_path.is_relative_to(ROOT) else str(input_path),
            "claim_boundary": "support_only_until_retained_route_gate_passes",
        },
        "phase": data.get("phase"),
        "same_ensemble": data.get("same_ensemble"),
        "same_source_coordinate": data.get("same_source_coordinate"),
        "source_coordinate": data.get("source_coordinate"),
        "canonical_higgs_operator_identity_passed": operator.get("canonical_higgs_operator_identity_passed"),
        "canonical_higgs_operator": {
            "operator_id": operator.get("operator_id"),
            "operator_definition": operator.get("operator_definition"),
            "identity_certificate": operator.get("identity_certificate"),
            "normalization_certificate": operator.get("normalization_certificate"),
        },
        "source_pole_operator": sp_summary,
        "selected_source_side_normalization": "legendre_lsz_source_pole_operator_v1",
        "selected_source_side_support_certificate": str(
            GENUINE_SOURCE_POLE_INTAKE.relative_to(ROOT)
        ),
        "source_side_contract_version": "genuine_osp_lsz_intake_required_v1",
        "hunit_used_as_operator": operator.get("hunit_used_as_operator"),
        "observed_targets_used_as_selectors": firewall.get("used_observed_targets_as_selectors"),
        "firewall": {
            "used_observed_targets_as_selectors": firewall.get("used_observed_targets_as_selectors"),
            "used_yt_ward_identity": firewall.get("used_yt_ward_identity"),
            "used_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette"),
            "used_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout"),
            "used_static_ew_algebra_as_operator": operator.get("static_ew_algebra_used_as_operator"),
        },
        "residue_matrix": {
            key: gram.get(key)
            for key in (
                "Res_C_ss",
                "Res_C_sH",
                "Res_C_HH",
                "Res_C_ss_err",
                "Res_C_sH_err",
                "Res_C_HH_err",
                "Dprime_ss_at_pole",
                "Res_C_sp_sp",
                "Res_C_spH",
            )
            if key in gram
        },
        "gram_purity": {
            "gram_determinant": gram.get("gram_determinant"),
            "normalized_overlap_rho_sH": gram.get("normalized_overlap_rho_sH"),
            "osp_higgs_gram_determinant": gram.get("osp_higgs_gram_determinant"),
            "normalized_overlap_rho_spH": gram.get("normalized_overlap_rho_spH"),
            "purity_gate_passed": False,
            "central_values_pass": gram.get("purity_gate_passed_by_central_values", False),
            "osp_higgs_central_values_pass": gram.get("osp_higgs_purity_gate_passed_by_central_values", False),
            "strict_limit": "final purity is evaluated by frontier_yt_source_higgs_gram_purity_postprocessor.py",
        },
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing,
        "model_class_or_pole_saturation_certificate_passed": data.get("model_class_or_pole_saturation_certificate_passed"),
        "fv_ir_zero_mode_control_passed": data.get("fv_ir_zero_mode_control_passed"),
        "retained_route_gate_passed": False,
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not treat H_unit as O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
    }
    return candidate, checks, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--status-output", type=Path, default=STATUS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 source-Higgs cross-correlator certificate builder")
    print("=" * 72)

    data = load_json(args.input)
    source_pole = load_json(SOURCE_POLE_OPERATOR)
    intake = load_json(GENUINE_SOURCE_POLE_INTAKE)
    input_present = bool(data)
    source_pole_ok = (
        source_pole.get("source_pole_operator_constructed") is True
        and source_pole.get("operator_candidate", {}).get("source_pole_residue_normalized_to_one") is True
        and source_pole.get("canonical_higgs_operator_identity_passed") is False
    )
    source_pole_intake_ok = (
        intake.get("artifact_is_genuine_current_surface_support") is True
        and intake.get("artifact_is_physics_closure") is False
        and intake.get("same_surface_source_coordinate") is True
        and intake.get("source_rescaling_invariant") is True
        and intake.get("contact_term_invariant") is True
        and intake.get("canonical_higgs_operator_identity_passed") is False
        and intake.get("proposal_allowed") is False
    )
    candidate_written = False
    candidate = {}
    checks: dict[str, bool] = {}
    missing: list[str] = []

    report("source-pole-operator-certificate-state-recorded", source_pole_ok, str(SOURCE_POLE_OPERATOR.relative_to(ROOT)))
    report(
        "genuine-source-pole-intake-recorded",
        source_pole_intake_ok,
        str(GENUINE_SOURCE_POLE_INTAKE.relative_to(ROOT)),
    )
    report("measurement-row-input-state-recorded", True, f"present={input_present}")
    if input_present:
        candidate, checks, missing = build_candidate(data, args.input, source_pole, intake)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        candidate_written = True
        report("candidate-certificate-written", True, str(args.output.relative_to(ROOT)))
        report("candidate-schema-complete", not missing, f"missing_or_failed={missing}")
    else:
        report("measurement-row-input-absent", True, str(args.input.relative_to(ROOT)))

    status = {
        "actual_current_surface_status": (
            "open / source-Higgs cross-correlator rows absent"
            if not input_present
            else "bounded-support / source-Higgs cross-correlator candidate certificate built"
        ),
        "verdict": (
            "No source-Higgs O_H/C_sH/C_HH measurement rows are present, so no "
            "production candidate certificate was written."
            if not input_present
            else (
                "A source-Higgs cross-correlator candidate certificate was written. "
                "It remains support only and must be evaluated by the Gram-purity "
                "postprocessor and retained-route gate."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Builder output is support only; retained-route gate remains authoritative.",
        "input_rows": str(args.input.relative_to(ROOT)) if args.input.is_relative_to(ROOT) else str(args.input),
        "candidate_output": str(args.output.relative_to(ROOT)) if args.output.is_relative_to(ROOT) else str(args.output),
        "source_pole_operator_certificate": str(SOURCE_POLE_OPERATOR.relative_to(ROOT)),
        "genuine_source_pole_intake_certificate": str(GENUINE_SOURCE_POLE_INTAKE.relative_to(ROOT)),
        "source_pole_operator_available": source_pole_ok,
        "genuine_source_pole_intake_available": source_pole_intake_ok,
        "source_side_normalization": "O_sp = sqrt(dGamma_ss/dx|pole) O_s; Res(C_sp,sp)=1",
        "source_side_contract_version": "genuine_osp_lsz_intake_required_v1",
        "input_present": input_present,
        "candidate_written": candidate_written,
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not manufacture O_H, C_sH, or C_HH data",
            "does not treat H_unit, static EW algebra, or observed targets as O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not identify O_sp with O_H without an O_sp-Higgs Gram-purity pass",
        ],
        "exact_next_action": (
            "Produce same-ensemble measurement rows for a certified O_H operator "
            "with Res_C_ss, Res_C_sH, and Res_C_HH; attach the Legendre/LSZ "
            "O_sp source-side normalization, rerun this builder, then run the "
            "Gram-purity postprocessor."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.status_output.parent.mkdir(parents=True, exist_ok=True)
    args.status_output.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {args.status_output.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
