#!/usr/bin/env python3
"""
PR #230 strict source-Higgs pole-row assembly certificate.

This runner searches current PR230 outputs for source-Higgs C_ss/C_sH/C_HH
rows, classifies the strongest available evidence, and emits the future
ingestion contract needed by the K-prime/rank-repair surface.  It does not run
chunk production and it does not treat finite-mode or unratified O_H rows as
strict pole evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_pole_row_assembly_2026-05-12.json"
SCHEMA_OUTPUT = ROOT / "outputs" / "yt_source_higgs_pole_row_ingestion_contract_2026-05-12.json"

PARENTS = {
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_contract_witness": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_higgs_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "canonical_higgs_repo_authority_audit": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "osp_oh_assumption_route_audit": "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "fh_lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "fh_lsz_finite_volume": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "schur_kernel_row_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_kprime_row_absence": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_observed_targets_as_selectors",
    "used_observed_top_or_yukawa_as_selector",
    "used_yt_ward_identity",
    "used_y_t_bare",
    "used_alpha_lm_or_plaquette",
    "used_alpha_lm_or_plaquette_u0",
    "used_plaquette_u0",
    "used_hunit_matrix_element_readout",
    "used_hunit_as_operator",
    "used_static_ew_algebra_as_operator",
    "used_alias_imports_as_load_bearing",
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


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "absent" not in value.lower()


def get_path(data: Any, path: tuple[str, ...]) -> Any:
    cur = data
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def first_present(data: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> Any:
    for path in paths:
        value = get_path(data, path)
        if value is not None:
            return value
    return None


def first_mapping(data: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> dict[str, Any]:
    value = first_present(data, paths)
    return value if isinstance(value, dict) else {}


def first_bool(data: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> bool | None:
    value = first_present(data, paths)
    return value if isinstance(value, bool) else None


def first_string(data: dict[str, Any], paths: tuple[tuple[str, ...], ...]) -> str | None:
    value = first_present(data, paths)
    return value if isinstance(value, str) else None


def pole_row_from_rows(rows: Any) -> dict[str, Any]:
    if not isinstance(rows, list) or not rows:
        return {}
    for row in rows:
        if isinstance(row, dict) and row.get("selected_pole_row") is True:
            return row
    for row in rows:
        if isinstance(row, dict) and row.get("isolated_pole_fit_passed") is True:
            return row
    return rows[0] if isinstance(rows[0], dict) else {}


def candidate_residue_matrix(data: dict[str, Any]) -> tuple[dict[str, Any], str]:
    rows = data.get("pole_residue_rows")
    row = pole_row_from_rows(rows)
    if row:
        return row, "pole_residue_rows"
    matrix = data.get("residue_matrix")
    if isinstance(matrix, dict) and any(key in matrix for key in ("Res_C_ss", "Res_C_sH", "Res_C_HH")):
        return matrix, "residue_matrix"
    gram = data.get("gram_purity")
    if isinstance(gram, dict) and any(key in gram for key in ("Res_C_ss", "Res_C_sH", "Res_C_HH")):
        return gram, "gram_purity"
    return {}, "absent"


def canonical_operator(data: dict[str, Any]) -> dict[str, Any]:
    operator = first_mapping(
        data,
        (
            ("canonical_higgs_operator",),
            ("operator",),
            ("ensembles", "0", "source_higgs_cross_correlator_analysis", "operator"),
        ),
    )
    # get_path cannot index list strings, so handle the known ensemble case.
    ensembles = data.get("ensembles")
    if not operator and isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        analysis = ensembles[0].get("source_higgs_cross_correlator_analysis")
        if isinstance(analysis, dict) and isinstance(analysis.get("operator"), dict):
            operator = analysis["operator"]
    return operator


def candidate_firewall(data: dict[str, Any]) -> dict[str, Any]:
    firewall = first_mapping(data, (("firewall",), ("forbidden_import_firewall",)))
    ensembles = data.get("ensembles")
    if not firewall and isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        analysis = ensembles[0].get("source_higgs_cross_correlator_analysis")
        if isinstance(analysis, dict) and isinstance(analysis.get("firewall"), dict):
            firewall = analysis["firewall"]
    return firewall


def bool_from_operator_or_data(data: dict[str, Any], operator: dict[str, Any], field: str) -> bool | None:
    if isinstance(operator.get(field), bool):
        return operator[field]
    if isinstance(data.get(field), bool):
        return data[field]
    return None


def forbidden_checks(data: dict[str, Any], operator: dict[str, Any], firewall: dict[str, Any]) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    aliases = {
        "used_alpha_lm_or_plaquette_u0": ("used_alpha_lm_or_plaquette", "used_plaquette_u0"),
        "used_hunit_as_operator": ("hunit_used_as_operator",),
        "used_static_ew_algebra_as_operator": ("static_ew_algebra_used_as_operator",),
    }
    for field in FORBIDDEN_FALSE_FIELDS:
        value = firewall.get(field)
        if value is None:
            for alias in aliases.get(field, ()):
                if value is None:
                    value = firewall.get(alias)
                if value is None:
                    value = data.get(alias)
                if value is None:
                    value = operator.get(alias)
        if value is None:
            value = data.get(field)
        if value is None:
            value = operator.get(field)
        checks[f"firewall.{field}=false"] = value is False
    return checks


def pole_location(matrix: dict[str, Any], data: dict[str, Any]) -> Any:
    for key in ("pole_location_x", "pole_mass_sq_lat", "pole_location", "m_pole_sq_lat"):
        if finite(matrix.get(key)):
            return matrix[key]
    pole = data.get("pole_control")
    if isinstance(pole, dict):
        for key in ("pole_location_x", "pole_mass_sq_lat", "pole_location", "m_pole_sq_lat"):
            if finite(pole.get(key)):
                return pole[key]
    return None


def gram_from_matrix(matrix: dict[str, Any]) -> dict[str, Any]:
    if not all(finite(matrix.get(key)) for key in ("Res_C_ss", "Res_C_sH", "Res_C_HH")):
        return {
            "computable": False,
            "gram_determinant": None,
            "normalized_overlap_rho_sH": None,
            "purity_central_value_passed": False,
        }
    c_ss = float(matrix["Res_C_ss"])
    c_sh = float(matrix["Res_C_sH"])
    c_hh = float(matrix["Res_C_HH"])
    product = c_ss * c_hh
    determinant = product - c_sh * c_sh
    rho = c_sh / math.sqrt(product) if product > 0.0 else float("nan")
    return {
        "computable": True,
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sh,
        "Res_C_HH": c_hh,
        "gram_determinant": determinant,
        "normalized_overlap_rho_sH": rho,
        "purity_formula": "Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
        "purity_central_value_passed": product > 0.0
        and abs(determinant) <= 1.0e-9
        and math.isfinite(rho)
        and abs(abs(rho) - 1.0) <= 1.0e-9,
    }


def validate_strict_candidate(data: dict[str, Any]) -> dict[str, Any]:
    matrix, matrix_source = candidate_residue_matrix(data)
    operator = canonical_operator(data)
    firewall = candidate_firewall(data)
    pole = pole_location(matrix, data)
    phase = data.get("phase")
    if phase is None:
        metadata = data.get("metadata")
        if isinstance(metadata, dict):
            phase = metadata.get("phase")
    canonical_identity = first_bool(
        data,
        (
            ("canonical_higgs_operator_identity_passed",),
            ("canonical_higgs_operator", "canonical_higgs_operator_identity_passed"),
            ("operator", "canonical_higgs_operator_identity_passed"),
        ),
    )
    if canonical_identity is None and isinstance(operator.get("canonical_higgs_operator_identity_passed"), bool):
        canonical_identity = operator["canonical_higgs_operator_identity_passed"]

    checks = {
        "phase=production": phase == "production",
        "same_surface_cl3_z3=true": data.get("same_surface_cl3_z3") is True
        or data.get("same_surface") is True
        or data.get("same_surface_source_higgs_pairing_passed") is True,
        "same_ensemble=true": data.get("same_ensemble") is True,
        "same_source_coordinate=true": data.get("same_source_coordinate") is True,
        "source_coordinate": nonempty(data.get("source_coordinate")),
        "pole_location": finite(pole),
        "Res_C_ss": finite(matrix.get("Res_C_ss")),
        "Res_C_sH": finite(matrix.get("Res_C_sH")),
        "Res_C_HH": finite(matrix.get("Res_C_HH")),
        "Res_C_ss_err_or_covariance": finite(matrix.get("Res_C_ss_err"))
        or isinstance(data.get("residue_covariance"), (list, dict)),
        "Res_C_sH_err_or_covariance": finite(matrix.get("Res_C_sH_err"))
        or isinstance(data.get("residue_covariance"), (list, dict)),
        "Res_C_HH_err_or_covariance": finite(matrix.get("Res_C_HH_err"))
        or isinstance(data.get("residue_covariance"), (list, dict)),
        "canonical_higgs_operator.operator_id": nonempty(operator.get("operator_id")),
        "canonical_higgs_operator.operator_definition": nonempty(operator.get("operator_definition")),
        "canonical_higgs_operator_identity_passed=true": canonical_identity is True,
        "canonical_higgs_operator.identity_certificate": nonempty(operator.get("identity_certificate")),
        "canonical_higgs_operator.lsz_normalization_certificate": nonempty(
            operator.get("lsz_normalization_certificate")
        )
        or nonempty(operator.get("normalization_certificate")),
        "canonical_higgs_operator.same_surface_canonical_action_certificate": nonempty(
            operator.get("same_surface_canonical_action_certificate")
        ),
        "canonical_higgs_operator.operator_authority_scope=same_surface_canonical_action_lsz": operator.get(
            "operator_authority_scope"
        )
        == "same_surface_canonical_action_lsz"
        or data.get("same_surface_canonical_action_lsz_authority_passed") is True,
        "canonical_higgs_operator.surface_id": nonempty(operator.get("surface_id"))
        or nonempty(data.get("surface_id")),
        "canonical_higgs_operator.surface_matches_measurement=true": data.get(
            "operator_surface_matches_measurement"
        )
        is True
        or operator.get("surface_matches_measurement") is True,
        "hunit_used_as_operator=false": bool_from_operator_or_data(data, operator, "hunit_used_as_operator")
        is False,
        "static_ew_algebra_used_as_operator=false": bool_from_operator_or_data(
            data, operator, "static_ew_algebra_used_as_operator"
        )
        is False,
        "isolated_pole_fit_passed=true": matrix.get("isolated_pole_fit_passed") is True
        or data.get("isolated_pole_fit_passed") is True
        or data.get("model_class_or_pole_saturation_certificate_passed") is True,
        "model_class_or_pole_saturation_certificate_passed=true": data.get(
            "model_class_or_pole_saturation_certificate_passed"
        )
        is True,
        "fv_ir_zero_mode_control_passed=true": data.get("fv_ir_zero_mode_control_passed") is True,
        "contact_term_scheme_certificate_passed=true": data.get(
            "contact_term_scheme_certificate_passed"
        )
        is True
        or data.get("analytic_contact_terms_fit_and_subtracted") is True,
        "not_physical_yukawa_readout=true": data.get("used_as_physical_yukawa_readout") is False
        or data.get("claims_physical_yukawa_closure") is False,
    }
    checks.update(forbidden_checks(data, operator, firewall))
    gram = gram_from_matrix(matrix)
    checks["gram_purity_computed_from_residues=true"] = gram["computable"] is True
    checks["gram_purity_central_value_passed=true"] = gram["purity_central_value_passed"] is True
    missing = [key for key, ok in checks.items() if not ok]
    return {
        "matrix_source": matrix_source,
        "strict_valid": not missing,
        "checks": checks,
        "missing_or_failed_fields": missing,
        "residue_matrix": {
            key: matrix.get(key)
            for key in (
                "Res_C_ss",
                "Res_C_sH",
                "Res_C_HH",
                "Res_C_ss_err",
                "Res_C_sH_err",
                "Res_C_HH_err",
            )
            if key in matrix
        },
        "pole_location": pole,
        "gram_purity": gram,
        "operator_summary": {
            "operator_id": operator.get("operator_id"),
            "canonical_higgs_operator_identity_passed": canonical_identity,
            "identity_certificate": operator.get("identity_certificate"),
            "normalization_certificate": operator.get("normalization_certificate"),
            "same_surface_canonical_action_certificate": operator.get(
                "same_surface_canonical_action_certificate"
            ),
            "operator_authority_scope": operator.get("operator_authority_scope"),
        },
    }


def iter_dicts_with_key(data: Any, key: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    if isinstance(data, dict):
        if key in data and isinstance(data[key], dict):
            hits.append(data[key])
        for value in data.values():
            if isinstance(value, (dict, list)):
                hits.extend(iter_dicts_with_key(value, key))
    elif isinstance(data, list):
        for value in data:
            if isinstance(value, (dict, list)):
                hits.extend(iter_dicts_with_key(value, key))
    return hits


def finite_source_higgs_summary(data: dict[str, Any]) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for analysis in iter_dicts_with_key(data, "source_higgs_cross_correlator_analysis"):
        rows = analysis.get("mode_rows")
        if not isinstance(rows, dict):
            continue
        row_values = [row for row in rows.values() if isinstance(row, dict)]
        if not row_values:
            continue
        labels = ("C_ss", "C_sH", "C_HH")
        has_all_labels = all(
            any(finite(row.get(f"{label}_real")) for row in row_values) for label in labels
        )
        p2 = sorted(
            {
                round(float(row["p_hat_sq"]), 12)
                for row in row_values
                if finite(row.get("p_hat_sq"))
            }
        )
        config_counts = [
            int(row.get("configuration_count"))
            for row in row_values
            if isinstance(row.get("configuration_count"), int)
        ]
        operator = analysis.get("operator") if isinstance(analysis.get("operator"), dict) else {}
        hits.append(
            {
                "mode_count": len(row_values),
                "has_finite_C_ss_C_sH_C_HH_rows": has_all_labels,
                "distinct_p_hat_sq_count": len(p2),
                "p_hat_sq_values": p2,
                "min_configuration_count": min(config_counts) if config_counts else 0,
                "same_ensemble": analysis.get("same_ensemble"),
                "same_source_coordinate": analysis.get("same_source_coordinate"),
                "source_coordinate": analysis.get("source_coordinate"),
                "operator_id": operator.get("operator_id"),
                "canonical_higgs_operator_identity_passed": operator.get(
                    "canonical_higgs_operator_identity_passed"
                ),
                "classification": (
                    "support_only_finite_mode_unratified_or_not_pole"
                    if has_all_labels
                    else "incomplete_source_higgs_rows"
                ),
                "strict_limit": (
                    "Finite-mode C_ss/C_sH/C_HH rows are not isolated-pole "
                    "residues and are support-only unless the canonical O_H "
                    "authority, pole extraction, Gram purity, FV/IR, model-class, "
                    "and contact gates pass."
                ),
            }
        )
    return hits


def scan_paths() -> list[Path]:
    paths = sorted(path for path in (ROOT / "outputs").glob("*.json") if path.is_file())
    nested_patterns = (
        "outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/**/ensemble_measurement.json",
        "outputs/yt_direct_lattice_correlator_production_fh_lsz_polefit8x8/**/ensemble_measurement.json",
        "outputs/yt_direct_lattice_correlator_production_source_higgs/**/ensemble_measurement.json",
    )
    for pattern in nested_patterns:
        paths.extend(path for path in sorted(ROOT.glob(pattern)) if path.is_file())
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def scan_outputs() -> dict[str, Any]:
    strict_candidates: list[dict[str, Any]] = []
    support_rows: list[dict[str, Any]] = []
    c_ss_only_files: list[str] = []
    scanned: list[str] = []
    for path in scan_paths():
        if path.resolve() in {OUTPUT.resolve(), SCHEMA_OUTPUT.resolve()}:
            continue
        data = load_json(path)
        if not data:
            continue
        rel = display(path)
        scanned.append(rel)
        matrix, source = candidate_residue_matrix(data)
        if matrix:
            validation = validate_strict_candidate(data)
            strict_candidates.append(
                {
                    "file": rel,
                    "matrix_source": source,
                    "strict_valid": validation["strict_valid"],
                    "missing_or_failed_fields": validation["missing_or_failed_fields"],
                    "pole_location": validation["pole_location"],
                    "residue_matrix": validation["residue_matrix"],
                    "gram_purity": validation["gram_purity"],
                    "operator_summary": validation["operator_summary"],
                }
            )
        finite_hits = finite_source_higgs_summary(data)
        for hit in finite_hits:
            support_rows.append({"file": rel, **hit})
        text_keys = json.dumps(data, sort_keys=True)
        if "C_ss" in text_keys and "C_sH" not in text_keys and "C_HH" not in text_keys:
            c_ss_only_files.append(rel)
    strict_valid = [row for row in strict_candidates if row["strict_valid"]]
    support_rows = support_rows[:20]
    return {
        "scanned_files": scanned,
        "scanned_file_count": len(scanned),
        "strict_candidate_count": len(strict_candidates),
        "strict_valid_candidates": strict_valid,
        "strict_invalid_candidates": strict_candidates[:20],
        "support_only_source_higgs_rows": support_rows,
        "support_only_source_higgs_file_count": len({row["file"] for row in support_rows}),
        "c_ss_only_file_count": len(c_ss_only_files),
        "c_ss_only_files_sample": c_ss_only_files[:20],
    }


def ingestion_contract() -> dict[str, Any]:
    return {
        "metadata": {
            "artifact": "source_higgs_pole_row_ingestion_contract",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "future strict row schema; current rows absent",
            "compatible_with": [
                "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
                "source-Higgs Gram-purity postprocessor residue_matrix schema",
            ],
        },
        "candidate_rows_path": "outputs/yt_source_higgs_pole_rows_2026-05-12.json",
        "required_top_level": {
            "phase": "production",
            "same_surface_cl3_z3": True,
            "same_ensemble": True,
            "same_source_coordinate": True,
            "source_coordinate": "same scalar source coordinate used by C_ss and FH/LSZ source response",
            "surface_id": "stable id shared by action, source coordinate, O_H, and row measurements",
            "source_higgs_form": "pole_residue_matrix_v1",
            "claims_physical_yukawa_closure": False,
        },
        "canonical_higgs_operator": {
            "operator_id": "nonempty canonical O_H id",
            "operator_definition": "same-surface radial/canonical-Higgs operator definition",
            "surface_id": "must match top-level surface_id",
            "operator_authority_scope": "same_surface_canonical_action_lsz",
            "canonical_higgs_operator_identity_passed": True,
            "identity_certificate": "path to same-surface identity certificate",
            "lsz_normalization_certificate": "path to LSZ/canonical normalization certificate",
            "same_surface_canonical_action_certificate": "path to action-surface authority certificate",
            "surface_matches_measurement": True,
            "hunit_used_as_operator": False,
            "static_ew_algebra_used_as_operator": False,
        },
        "partition_certificate": {
            "source_pole_coordinate_certified": True,
            "canonical_higgs_operator_certified": True,
            "same_surface_source_higgs_pairing_passed": True,
            "source_higgs_covariance_included": True,
            "source_numerator_projection_rows_compatible_with_kprime": True,
        },
        "pole_control": {
            "isolated_scalar_pole_passed": True,
            "pole_location_x": "finite",
            "pole_location_scheme": "p_hat_sq or equivalent named variable",
            "pole_fit_window": "named mode/time window",
            "model_class_or_pole_saturation_certificate_passed": True,
            "fv_ir_zero_mode_control_passed": True,
            "contact_term_scheme_certificate_passed": True,
            "analytic_contact_terms_fit_and_subtracted": True,
        },
        "residue_matrix": {
            "Res_C_ss": "finite source-source pole residue",
            "Res_C_sH": "finite source-Higgs cross pole residue",
            "Res_C_HH": "finite canonical-Higgs pole residue",
            "Res_C_ss_err": "finite or supplied by covariance",
            "Res_C_sH_err": "finite or supplied by covariance",
            "Res_C_HH_err": "finite or supplied by covariance",
            "residue_covariance": "3x3 covariance for [Res_C_ss, Res_C_sH, Res_C_HH]",
        },
        "gram_purity": {
            "gram_determinant": "Res_C_ss * Res_C_HH - Res_C_sH^2",
            "normalized_overlap_rho_sH": "Res_C_sH / sqrt(Res_C_ss * Res_C_HH)",
            "purity_condition": "Delta = 0 and |rho_sH| = 1 within covariance-aware tolerance",
            "same_pole_coincidence_is_not_sufficient": True,
        },
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
        "strict_non_claims": [
            "finite-mode C_ss/C_sH/C_HH rows are not pole residues",
            "same-pole coincidence without residue Gram purity is not a closure",
            "O_H is not accepted unless same-surface canonical action/LSZ authority is certified",
            "H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed selectors, and alias imports are non-load-bearing",
        ],
    }


def exact_missing_fields() -> list[str]:
    return [
        "phase=production source-Higgs pole-row artifact",
        "same_surface_cl3_z3=true",
        "same_ensemble=true",
        "same_source_coordinate=true",
        "source_coordinate",
        "surface_id shared by action/source/O_H/rows",
        "canonical_higgs_operator.operator_id",
        "canonical_higgs_operator.operator_definition",
        "canonical_higgs_operator.surface_id matching measurement surface_id",
        "canonical_higgs_operator.operator_authority_scope=same_surface_canonical_action_lsz",
        "canonical_higgs_operator.canonical_higgs_operator_identity_passed=true",
        "canonical_higgs_operator.identity_certificate",
        "canonical_higgs_operator.lsz_normalization_certificate",
        "canonical_higgs_operator.same_surface_canonical_action_certificate",
        "canonical_higgs_operator.surface_matches_measurement=true",
        "canonical_higgs_operator.hunit_used_as_operator=false",
        "canonical_higgs_operator.static_ew_algebra_used_as_operator=false",
        "pole_control.isolated_scalar_pole_passed=true",
        "pole_control.pole_location_x or pole_residue_rows[].pole_mass_sq_lat",
        "pole_control.model_class_or_pole_saturation_certificate_passed=true",
        "pole_control.fv_ir_zero_mode_control_passed=true",
        "pole_control.contact_term_scheme_certificate_passed=true",
        "residue_matrix.Res_C_ss",
        "residue_matrix.Res_C_sH",
        "residue_matrix.Res_C_HH",
        "residue_matrix errors or 3x3 covariance for C_ss/C_sH/C_HH",
        "gram_purity computed from residues: Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
        "firewall.used_observed_targets_as_selectors=false",
        "firewall.used_yt_ward_identity=false",
        "firewall.used_y_t_bare=false",
        "firewall.used_alpha_lm_or_plaquette=false",
        "firewall.used_plaquette_u0=false",
        "firewall.used_hunit_matrix_element_readout=false",
        "firewall.used_alias_imports_as_load_bearing=false",
        "used_as_physical_yukawa_readout=false or claims_physical_yukawa_closure=false",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--schema-output", type=Path, default=SCHEMA_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 strict source-Higgs pole-row assembly")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    scan = scan_outputs()
    strict_rows = scan["strict_valid_candidates"]
    support_rows = scan["support_only_source_higgs_rows"]
    contract = ingestion_contract()

    canonical_gate_blocks = (
        "canonical-Higgs operator certificate absent" in status(parents["canonical_higgs_operator_gate"])
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    production_readiness_blocks = (
        "source-Higgs production launch blocked" in status(parents["source_higgs_production_readiness"])
        and parents["source_higgs_production_readiness"].get("source_higgs_launch_ready") is False
    )
    extractor_blocks = (
        "awaiting valid production rows" in status(parents["source_higgs_pole_residue_extractor"])
        and parents["source_higgs_pole_residue_extractor"].get("rows_written") is False
    )
    builder_blocks = (
        "source-Higgs cross-correlator rows absent" in status(parents["source_higgs_builder"])
        and parents["source_higgs_builder"].get("input_present") is False
    )
    postprocessor_blocks = (
        "awaiting production certificate" in status(parents["source_higgs_gram_postprocessor"])
        and parents["source_higgs_gram_postprocessor"].get("source_higgs_gram_purity_gate_passed") is False
    )
    contract_witness_available = (
        "source-Higgs Gram-purity contract witness" in status(parents["source_higgs_contract_witness"])
        and parents["source_higgs_contract_witness"].get("contract_witness_passed") is True
    )
    schur_contract_compat = (
        "Schur kernel row contract gate" in status(parents["schur_kernel_row_contract"])
        or "Schur K-prime row absence guard" in status(parents["schur_kprime_row_absence"])
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("canonical-oh-authority-currently-blocked", canonical_gate_blocks, status(parents["canonical_higgs_operator_gate"]))
    report("production-readiness-currently-blocked", production_readiness_blocks, status(parents["source_higgs_production_readiness"]))
    report("pole-extractor-currently-blocked", extractor_blocks, status(parents["source_higgs_pole_residue_extractor"]))
    report("builder-currently-blocked", builder_blocks, status(parents["source_higgs_builder"]))
    report("gram-postprocessor-currently-blocked", postprocessor_blocks, status(parents["source_higgs_gram_postprocessor"]))
    report("gram-contract-witness-available", contract_witness_available, status(parents["source_higgs_contract_witness"]))
    report("kprime-compatible-contract-surface-referenced", schur_contract_compat, status(parents["schur_kernel_row_contract"]))
    report("outputs-scanned", scan["scanned_file_count"] > 0, f"count={scan['scanned_file_count']}")
    report("strict-source-higgs-pole-rows-absent", not strict_rows, f"strict_valid_count={len(strict_rows)}")
    report("support-only-source-higgs-rows-classified", bool(support_rows), f"support_rows={len(support_rows)}")

    actual_status = (
        "bounded-support / strict source-Higgs pole rows assembled"
        if strict_rows
        else "open / strict source-Higgs pole-row assembly blocked by canonical O_H authority and missing pole rows"
    )
    result = {
        "actual_current_surface_status": actual_status,
        "verdict": (
            "Strict source-Higgs C_ss/C_sH/C_HH pole rows are present and "
            "assembled as bounded support only; retained-route authorization "
            "still remains outside this runner."
            if strict_rows
            else (
                "No strict source-Higgs C_ss/C_sH/C_HH pole-row certificate "
                "exists on the current PR230 surface.  The strongest current "
                "source-Higgs rows are finite-mode support-only smoke rows, "
                "and they are blocked from strict use by missing same-surface "
                "canonical O_H action/LSZ authority, missing production pole "
                "residue rows, and missing FV/IR/model-class/contact controls."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This runner assembles or blocks source-Higgs pole rows only; retained/proposed_retained wording requires retained-route authorization."
        ),
        "bare_retained_allowed": False,
        "strict_c_ss_c_sh_c_hh_rows_exist": bool(strict_rows),
        "strict_rows": strict_rows,
        "support_only_rows": support_rows,
        "blocked_by_canonical_o_h_authority": canonical_gate_blocks,
        "blocked_by_missing_production_pole_rows": not strict_rows,
        "exact_missing_production_fields": exact_missing_fields() if not strict_rows else [],
        "scan": scan,
        "ingestion_contract_output": display(args.schema_output),
        "ingestion_contract": contract,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not launch or duplicate chunk production",
            "does not treat same-pole coincidence as a source-Higgs Gram-purity proof",
            "does not use O_H unless same-surface canonical action/LSZ authority is certified",
            "does not treat finite-mode or unratified C_sH/C_HH rows as strict pole residues",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed selectors, or alias imports as load-bearing inputs",
        ],
        "exact_next_action": (
            "Supply a production source-Higgs pole-row artifact satisfying "
            f"{display(args.schema_output)}; then rerun this assembler, the "
            "pole-residue extractor/builder, Gram-purity postprocessor, PR230 "
            "assembly gate, and campaign status gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.schema_output.parent.mkdir(parents=True, exist_ok=True)
    args.schema_output.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(args.output)}")
    print(f"Wrote ingestion contract: {display(args.schema_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
