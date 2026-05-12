#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode/x8 pole-fit chunk combiner gate.

This audits the separate polefit8x8 L12 stream.  It can write a combined
diagnostic support surface from ready chunks, but that surface is never a
retained y_t readout by itself.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json"
COMBINED_OUTPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
KPRIME_FIXTURE = ROOT / "fixtures" / "yt_pr230_kprime_pole_row_fixture.json"
KPRIME_SCHEMA_VERSION = "yt_pr230_kprime_pole_row_v1"

EXPECTED_SOURCE_SHIFTS = {-0.01, 0.0, 0.01}
EXPECTED_MODE_KEYS = {"0,0,0", "1,0,0", "1,1,0", "1,1,1", "2,0,0", "2,1,0", "2,1,1", "2,2,0"}
EXPECTED_MASSES = [0.75]
EXPECTED_NOISES = 8
EXPECTED_THERM = 1000
EXPECTED_SEPARATION = 20
EXPECTED_CHUNK_MEASUREMENTS = 16
EXPECTED_VOLUME = "12x24"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
KPRIME_FORBIDDEN_FALSE_FIELDS = (
    "used_hunit_matrix_element_readout",
    "used_yt_ward_identity",
    "used_y_t_bare",
    "used_alpha_lm_or_plaquette_u0",
    "used_observed_target_selectors",
    "used_alias_imports",
    "used_reduced_cold_pilots_as_production_evidence",
    "set_c2_equal_one",
    "set_z_match_equal_one",
    "set_kappa_s_equal_one",
    "set_cos_theta_equal_one",
)

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def finite_vector(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(finite_number(item) for item in value)


def finite_matrix(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(row, list) and row and all(finite_number(item) for item in row) for row in value)
    )


def dot(left: list[float], right: list[float]) -> float:
    return sum(float(a) * float(b) for a, b in zip(left, right))


def mat_vec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [dot([float(item) for item in row], vector) for row in matrix]


def close(a: Any, b: Any, tolerance: float = 1.0e-9) -> bool:
    return finite_number(a) and finite_number(b) and abs(float(a) - float(b)) <= tolerance


def interval_pair(value: Any) -> tuple[float, float] | None:
    if not isinstance(value, list) or len(value) != 2:
        return None
    if not finite_number(value[0]) or not finite_number(value[1]):
        return None
    lo = float(value[0])
    hi = float(value[1])
    if lo > hi:
        return None
    return lo, hi


def interval_contains(interval: tuple[float, float] | None, value: float) -> bool:
    return interval is not None and interval[0] <= value <= interval[1]


def interval_excludes_zero(interval: tuple[float, float] | None) -> bool:
    return interval is not None and (interval[1] < 0.0 or interval[0] > 0.0)


def interval_hull(intervals: list[tuple[float, float]]) -> list[float] | None:
    if not intervals:
        return None
    return [min(lo for lo, _hi in intervals), max(hi for _lo, hi in intervals)]


def manifest_chunks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in manifest.get("commands", []) if isinstance(row, dict)]


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    first = ensembles[0]
    return first if isinstance(first, dict) else {}


def expected_volume_seed(base_seed: int, spatial_l: int = 12, time_l: int = 24) -> int:
    return int(base_seed + 1000003 * spatial_l + 9176 * time_l)


def audit_run_control(metadata: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    run_control = metadata.get("run_control")
    if not isinstance(run_control, dict):
        return ["metadata.run_control missing"]
    if run_control.get("seed") != expected.get("seed"):
        issues.append(f"seed={run_control.get('seed')!r}, expected {expected.get('seed')}")
    if run_control.get("volumes") != EXPECTED_VOLUME:
        issues.append(f"volumes={run_control.get('volumes')!r}")
    if [float(x) for x in run_control.get("masses", [])] != EXPECTED_MASSES:
        issues.append(f"masses={run_control.get('masses')!r}")
    if run_control.get("thermalization_sweeps") != EXPECTED_THERM:
        issues.append(f"thermalization_sweeps={run_control.get('thermalization_sweeps')!r}")
    if run_control.get("measurement_sweeps") != EXPECTED_CHUNK_MEASUREMENTS:
        issues.append(f"measurement_sweeps={run_control.get('measurement_sweeps')!r}")
    if run_control.get("measurement_separation_sweeps") != EXPECTED_SEPARATION:
        issues.append(f"measurement_separation_sweeps={run_control.get('measurement_separation_sweeps')!r}")
    if run_control.get("production_targets") is not True:
        issues.append("production_targets is not true")
    shifts = {round(float(x), 8) for x in run_control.get("scalar_source_shifts", [])}
    if shifts != {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}:
        issues.append(f"scalar_source_shifts={run_control.get('scalar_source_shifts')!r}")
    modes = {
        ",".join(str(int(v)) for v in mode)
        for mode in run_control.get("scalar_two_point_modes", [])
        if isinstance(mode, list)
    }
    if modes != EXPECTED_MODE_KEYS:
        issues.append(f"scalar_two_point_modes={sorted(modes)}")
    if run_control.get("scalar_two_point_noises") != EXPECTED_NOISES:
        issues.append(f"scalar_two_point_noises={run_control.get('scalar_two_point_noises')!r}")
    if run_control.get("production_output_dir") != expected.get("production_output_dir"):
        issues.append(f"production_output_dir={run_control.get('production_output_dir')!r}")
    if run_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"seed_control_version={run_control.get('seed_control_version')!r}")
    return issues


def audit_seed_control(ensemble: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    seed_control = ensemble.get("rng_seed_control")
    if not isinstance(seed_control, dict):
        return ["missing ensemble.rng_seed_control"]
    issues: list[str] = []
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"seed_control_version={seed_control.get('seed_control_version')!r}")
    if seed_control.get("base_seed") != expected.get("seed"):
        issues.append(f"base_seed={seed_control.get('base_seed')!r}, expected {expected.get('seed')}")
    expected_seed = expected_volume_seed(int(expected.get("seed", 0)))
    if seed_control.get("gauge_rng_seed") != expected_seed:
        issues.append(f"gauge_rng_seed={seed_control.get('gauge_rng_seed')!r}, expected {expected_seed}")
    if seed_control.get("numba_gauge_seeded_before_thermalization") is not True:
        issues.append("numba_gauge_seeded_before_thermalization is not true")
    return issues


def audit_source_response(ensemble: dict[str, Any]) -> list[str]:
    analysis = ensemble.get("scalar_source_response_analysis")
    if not isinstance(analysis, dict):
        return ["missing scalar_source_response_analysis"]
    issues: list[str] = []
    if analysis.get("fit_kind") != "linear_dE_ds":
        issues.append(f"fit_kind={analysis.get('fit_kind')!r}")
    shifts = {
        round(float(row.get("source_shift_lat")), 8)
        for row in analysis.get("energy_fits", [])
        if isinstance(row, dict) and finite_number(row.get("source_shift_lat"))
    }
    if shifts != {round(x, 8) for x in EXPECTED_SOURCE_SHIFTS}:
        issues.append(f"source shifts {sorted(shifts)}")
    if not finite_number(analysis.get("slope_dE_ds_lat")):
        issues.append("missing finite slope_dE_ds_lat")
    if analysis.get("physical_higgs_normalization") != "not_derived":
        issues.append("source response claims physical Higgs normalization")
    return issues


def audit_scalar_lsz(metadata: dict[str, Any], ensemble: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    meta = metadata.get("scalar_two_point_lsz")
    if not isinstance(meta, dict) or meta.get("enabled") is not True:
        issues.append("metadata.scalar_two_point_lsz.enabled is not true")
    if not isinstance(meta, dict) or meta.get("noise_vectors_per_configuration") != EXPECTED_NOISES:
        issues.append(f"noise_vectors_per_configuration={meta.get('noise_vectors_per_configuration') if isinstance(meta, dict) else None!r}")
    if isinstance(meta, dict) and meta.get("used_as_physical_yukawa_readout") is not False:
        issues.append("scalar_two_point_lsz used_as_physical_yukawa_readout is not false")
    analysis = ensemble.get("scalar_two_point_lsz_analysis")
    if not isinstance(analysis, dict):
        return issues + ["missing scalar_two_point_lsz_analysis"]
    if analysis.get("physical_higgs_normalization") != "not_derived":
        issues.append("scalar LSZ analysis claims physical Higgs normalization")
    rows = analysis.get("mode_rows")
    if not isinstance(rows, dict):
        return issues + ["missing mode_rows"]
    missing = sorted(EXPECTED_MODE_KEYS - set(rows))
    if missing:
        issues.append(f"missing modes {missing}")
    for key in sorted(EXPECTED_MODE_KEYS & set(rows)):
        row = rows.get(key, {})
        if not finite_number(row.get("C_ss_real")):
            issues.append(f"{key} missing finite C_ss_real")
        if not finite_number(row.get("Gamma_ss_real")):
            issues.append(f"{key} missing finite Gamma_ss_real")
        if int(row.get("configuration_count", 0)) <= 0:
            issues.append(f"{key} has no configurations")
    return issues


def kprime_schema_manifest() -> dict[str, Any]:
    return {
        "schema_version": KPRIME_SCHEMA_VERSION,
        "row_container_locations": [
            "ensemble.schur_kprime_pole_rows[]",
            "metadata.schur_kprime_kernel_rows.rows[]",
            "top-level kprime_pole_rows[]",
        ],
        "required_sections_per_row": [
            "transfer_schur_kernel_at_pole",
            "derivative_wrt_pole_coordinate",
            "eigen_projection",
            "source_numerator_projection",
            "error_interval",
            "provenance",
        ],
        "transfer_schur_kernel_at_pole": {
            "schur_form": "one_orthogonal_mode_v1 or precontracted_matrix_v1",
            "one_orthogonal_mode_v1": ["A_at_pole", "B_at_pole", "C_at_pole"],
            "precontracted_matrix_v1": ["A_at_pole", "B_Cinv_B_at_pole"],
            "must_compute": "effective_denominator_at_pole",
        },
        "derivative_wrt_pole_coordinate": {
            "coordinate": "pole coordinate, e.g. p_hat_sq or x",
            "one_orthogonal_mode_v1": ["A_prime_at_pole", "B_prime_at_pole", "C_prime_at_pole"],
            "precontracted_matrix_v1": [
                "A_prime_at_pole",
                "two_Bprime_Cinv_B_at_pole",
                "B_Cinv_Cprime_Cinv_B_at_pole",
            ],
            "must_compute": "effective_denominator_prime_at_pole",
            "projection_sign_convention": "D_eff_prime",
        },
        "eigen_projection": {
            "required": [
                "left_eigenvector",
                "right_eigenvector",
                "kernel_prime_matrix_at_pole",
                "projected_kprime_at_pole",
                "vector_normalization",
            ],
            "computed_check": "<l,K_prime(pole)r>/<l,r>",
        },
        "source_numerator_projection": {
            "required": [
                "source_vector",
                "left_source_projection",
                "right_source_projection",
                "source_numerator_at_pole",
            ],
            "computed_check": "<l,s><s,r>/<l,r>",
        },
        "error_interval": {
            "required": [
                "effective_denominator_at_pole",
                "projected_kprime_at_pole",
                "source_numerator_at_pole",
            ],
            "strict_certificate_requires": [
                "effective_denominator_at_pole interval contains zero",
                "projected_kprime_at_pole interval excludes zero",
                "source_numerator_at_pole interval excludes zero",
            ],
        },
        "provenance": {
            "required": [
                "phase",
                "same_surface_cl3_z3",
                "source_coordinate",
                "chunk_index",
                "production_output_dir",
                "row_builder",
                "forbidden_import_firewall",
            ],
            "forbidden_import_firewall_false": list(KPRIME_FORBIDDEN_FALSE_FIELDS),
        },
    }


def compute_schur_from_kprime_row(row: dict[str, Any]) -> dict[str, Any]:
    kernel = row.get("transfer_schur_kernel_at_pole", {})
    derivative = row.get("derivative_wrt_pole_coordinate", {})
    if not isinstance(kernel, dict) or not isinstance(derivative, dict):
        return {"valid_numeric_form": False, "reason": "missing kernel or derivative section"}
    form = str(kernel.get("schur_form") or row.get("schur_form") or "")
    if form == "one_orthogonal_mode_v1":
        scalar_keys = ("A_at_pole", "B_at_pole", "C_at_pole")
        derivative_keys = ("A_prime_at_pole", "B_prime_at_pole", "C_prime_at_pole")
        if not all(finite_number(kernel.get(key)) for key in scalar_keys):
            return {"valid_numeric_form": False, "reason": "missing one_orthogonal_mode_v1 pole keys"}
        if not all(finite_number(derivative.get(key)) for key in derivative_keys):
            return {"valid_numeric_form": False, "reason": "missing one_orthogonal_mode_v1 derivative keys"}
        a0 = float(kernel["A_at_pole"])
        b0 = float(kernel["B_at_pole"])
        c0 = float(kernel["C_at_pole"])
        a1 = float(derivative["A_prime_at_pole"])
        b1 = float(derivative["B_prime_at_pole"])
        c1 = float(derivative["C_prime_at_pole"])
        if c0 == 0.0:
            return {"valid_numeric_form": False, "reason": "C_at_pole is zero"}
        return {
            "valid_numeric_form": True,
            "schur_form": form,
            "effective_denominator_at_pole": a0 - b0 * b0 / c0,
            "effective_denominator_prime_at_pole": a1 - 2.0 * b0 * b1 / c0 + (b0 * b0 * c1) / (c0 * c0),
        }
    if form == "precontracted_matrix_v1":
        kernel_keys = ("A_at_pole", "B_Cinv_B_at_pole")
        derivative_keys = ("A_prime_at_pole", "two_Bprime_Cinv_B_at_pole", "B_Cinv_Cprime_Cinv_B_at_pole")
        if not all(finite_number(kernel.get(key)) for key in kernel_keys):
            return {"valid_numeric_form": False, "reason": "missing precontracted_matrix_v1 pole keys"}
        if not all(finite_number(derivative.get(key)) for key in derivative_keys):
            return {"valid_numeric_form": False, "reason": "missing precontracted_matrix_v1 derivative keys"}
        return {
            "valid_numeric_form": True,
            "schur_form": form,
            "effective_denominator_at_pole": float(kernel["A_at_pole"]) - float(kernel["B_Cinv_B_at_pole"]),
            "effective_denominator_prime_at_pole": (
                float(derivative["A_prime_at_pole"])
                - float(derivative["two_Bprime_Cinv_B_at_pole"])
                + float(derivative["B_Cinv_Cprime_Cinv_B_at_pole"])
            ),
        }
    return {"valid_numeric_form": False, "reason": f"unsupported schur_form={form!r}"}


def validate_kprime_row(row: dict[str, Any], *, allow_fixture: bool = False) -> dict[str, Any]:
    if not isinstance(row, dict):
        return {"valid": False, "reasons": ["row is not a JSON object"]}
    required_sections = (
        "transfer_schur_kernel_at_pole",
        "derivative_wrt_pole_coordinate",
        "eigen_projection",
        "source_numerator_projection",
        "error_interval",
        "provenance",
    )
    sections_present = {name: isinstance(row.get(name), dict) for name in required_sections}
    schur = compute_schur_from_kprime_row(row)
    kernel = row.get("transfer_schur_kernel_at_pole", {})
    derivative = row.get("derivative_wrt_pole_coordinate", {})
    projection = row.get("eigen_projection", {})
    source = row.get("source_numerator_projection", {})
    intervals = row.get("error_interval", {})
    provenance = row.get("provenance", {})
    firewall = provenance.get("forbidden_import_firewall", {}) if isinstance(provenance, dict) else {}

    left = [float(item) for item in projection.get("left_eigenvector", [])] if finite_vector(projection.get("left_eigenvector")) else []
    right = [float(item) for item in projection.get("right_eigenvector", [])] if finite_vector(projection.get("right_eigenvector")) else []
    matrix = (
        [[float(item) for item in matrix_row] for matrix_row in projection.get("kernel_prime_matrix_at_pole", [])]
        if finite_matrix(projection.get("kernel_prime_matrix_at_pole"))
        else []
    )
    source_vector = [float(item) for item in source.get("source_vector", [])] if finite_vector(source.get("source_vector")) else []
    vector_normalization = float(projection.get("vector_normalization")) if finite_number(projection.get("vector_normalization")) else float("nan")
    projected = float(projection.get("projected_kprime_at_pole")) if finite_number(projection.get("projected_kprime_at_pole")) else float("nan")
    source_numerator = float(source.get("source_numerator_at_pole")) if finite_number(source.get("source_numerator_at_pole")) else float("nan")
    computed_projection = float("nan")
    computed_left_source = float("nan")
    computed_right_source = float("nan")
    computed_source_numerator = float("nan")
    if left and right and matrix and len(left) == len(right) == len(matrix) and all(len(row_) == len(right) for row_ in matrix):
        normal = dot(left, right)
        divisor = vector_normalization if vector_normalization != 0.0 else normal
        if divisor != 0.0:
            computed_projection = dot(left, mat_vec(matrix, right)) / divisor
    if left and right and source_vector and len(left) == len(right) == len(source_vector):
        computed_left_source = dot(left, source_vector)
        computed_right_source = dot(source_vector, right)
        normal = vector_normalization if math.isfinite(vector_normalization) else dot(left, right)
        if normal != 0.0:
            computed_source_numerator = computed_left_source * computed_right_source / normal

    d_eff_value = float(kernel.get("effective_denominator_at_pole")) if finite_number(kernel.get("effective_denominator_at_pole")) else float("nan")
    d_eff_prime_value = (
        float(derivative.get("effective_denominator_prime_at_pole"))
        if finite_number(derivative.get("effective_denominator_prime_at_pole"))
        else float("nan")
    )
    d_eff_interval = interval_pair(intervals.get("effective_denominator_at_pole")) if isinstance(intervals, dict) else None
    kprime_interval = interval_pair(intervals.get("projected_kprime_at_pole")) if isinstance(intervals, dict) else None
    numerator_interval = interval_pair(intervals.get("source_numerator_at_pole")) if isinstance(intervals, dict) else None
    phase = provenance.get("phase") if isinstance(provenance, dict) else None
    allowed_phases = {"production", "theorem"} | ({"fixture"} if allow_fixture else set())

    checks = {
        "schema_version": row.get("schema_version") == KPRIME_SCHEMA_VERSION,
        **{f"has_{name}": ok for name, ok in sections_present.items()},
        "valid_schur_numeric_form": schur.get("valid_numeric_form") is True,
        "recorded_denominator_matches_schur": close(d_eff_value, schur.get("effective_denominator_at_pole")),
        "recorded_derivative_matches_schur": close(d_eff_prime_value, schur.get("effective_denominator_prime_at_pole")),
        "left_right_vectors_present": bool(left) and bool(right) and len(left) == len(right),
        "kernel_prime_matrix_present": bool(matrix),
        "projection_normalization_nonzero": finite_number(vector_normalization) and vector_normalization != 0.0,
        "projected_kprime_matches_eigenprojection": close(projected, computed_projection),
        "projected_kprime_matches_schur_derivative": close(projected, schur.get("effective_denominator_prime_at_pole")),
        "source_vector_present": bool(source_vector) and len(source_vector) == len(left),
        "left_source_projection_matches": close(source.get("left_source_projection"), computed_left_source),
        "right_source_projection_matches": close(source.get("right_source_projection"), computed_right_source),
        "source_numerator_matches_projection": close(source_numerator, computed_source_numerator),
        "denominator_interval_contains_value": interval_contains(d_eff_interval, d_eff_value),
        "denominator_interval_contains_zero": interval_contains(d_eff_interval, 0.0),
        "kprime_interval_contains_value": interval_contains(kprime_interval, projected),
        "kprime_interval_excludes_zero": interval_excludes_zero(kprime_interval),
        "source_numerator_interval_contains_value": interval_contains(numerator_interval, source_numerator),
        "source_numerator_interval_excludes_zero": interval_excludes_zero(numerator_interval),
        "phase_allowed": phase in allowed_phases,
        "same_surface_cl3_z3": provenance.get("same_surface_cl3_z3") is True if isinstance(provenance, dict) else False,
        "source_coordinate_named": isinstance(provenance.get("source_coordinate"), str) and bool(provenance.get("source_coordinate")) if isinstance(provenance, dict) else False,
        "chunk_index_recorded": isinstance(provenance.get("chunk_index"), int) if isinstance(provenance, dict) else False,
        "production_output_dir_recorded": isinstance(provenance.get("production_output_dir"), str) and bool(provenance.get("production_output_dir")) if isinstance(provenance, dict) else False,
        "row_builder_recorded": isinstance(provenance.get("row_builder"), str) and bool(provenance.get("row_builder")) if isinstance(provenance, dict) else False,
    }
    checks.update({f"forbidden_{field}_false": firewall.get(field) is False for field in KPRIME_FORBIDDEN_FALSE_FIELDS})
    reasons = [key for key, ok in checks.items() if not ok]
    return {
        "valid": not reasons,
        "schema_version": row.get("schema_version"),
        "checks": checks,
        "reasons": reasons,
        "computed": {
            "schur": schur,
            "projected_kprime_at_pole": computed_projection,
            "left_source_projection": computed_left_source,
            "right_source_projection": computed_right_source,
            "source_numerator_at_pole": computed_source_numerator,
            "effective_denominator_interval": list(d_eff_interval) if d_eff_interval else None,
            "projected_kprime_interval": list(kprime_interval) if kprime_interval else None,
            "source_numerator_interval": list(numerator_interval) if numerator_interval else None,
        },
        "row_id": row.get("row_id"),
    }


def normalize_kprime_row_container(container: Any) -> list[dict[str, Any]]:
    if isinstance(container, list):
        return [row for row in container if isinstance(row, dict)]
    if isinstance(container, dict):
        rows = container.get("rows") or container.get("kprime_pole_rows") or container.get("schur_kprime_pole_rows")
        if isinstance(rows, list):
            schema_version = container.get("schema_version")
            out = []
            for row in rows:
                if isinstance(row, dict):
                    copy = dict(row)
                    copy.setdefault("schema_version", schema_version)
                    out.append(copy)
            return out
        if container.get("schema_version") == KPRIME_SCHEMA_VERSION:
            return [container]
    return []


def extract_kprime_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(normalize_kprime_row_container(data.get("kprime_pole_rows")))
    metadata = data.get("metadata", {})
    if isinstance(metadata, dict):
        rows.extend(normalize_kprime_row_container(metadata.get("schur_kprime_kernel_rows")))
    for ensemble in data.get("ensembles", []):
        if isinstance(ensemble, dict):
            rows.extend(normalize_kprime_row_container(ensemble.get("schur_kprime_pole_rows")))
            rows.extend(normalize_kprime_row_container(ensemble.get("kprime_pole_rows")))
    return rows


def validate_kprime_fixture(path: Path) -> dict[str, Any]:
    data = load_json(path)
    rows = normalize_kprime_row_container(data)
    validations = [validate_kprime_row(row, allow_fixture=True) for row in rows]
    valid = bool(rows) and all(row.get("valid") for row in validations)
    return {
        "fixture_path": rel(path),
        "present": bool(data),
        "row_count": len(rows),
        "valid": valid,
        "row_validations": validations,
    }


def combine_kprime_rows(audits: list[dict[str, Any]]) -> dict[str, Any]:
    present: list[dict[str, Any]] = []
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for audit in audits:
        for validation in audit.get("kprime_pole_row_validations", []):
            row_record = {
                "chunk_index": audit.get("chunk_index"),
                "output": audit.get("output"),
                "validation": validation,
            }
            present.append(row_record)
            if validation.get("valid"):
                valid.append(row_record)
            else:
                invalid.append(row_record)

    kprime_intervals: list[tuple[float, float]] = []
    numerator_intervals: list[tuple[float, float]] = []
    denominator_intervals: list[tuple[float, float]] = []
    for row in valid:
        computed = row["validation"].get("computed", {})
        kprime_interval = interval_pair(computed.get("projected_kprime_interval"))
        numerator_interval = interval_pair(computed.get("source_numerator_interval"))
        denominator_interval = interval_pair(computed.get("effective_denominator_interval"))
        if kprime_interval is not None:
            kprime_intervals.append(kprime_interval)
        if numerator_interval is not None:
            numerator_intervals.append(numerator_interval)
        if denominator_interval is not None:
            denominator_intervals.append(denominator_interval)

    complete_l12 = bool(audits) and len(valid) == len(audits) and all(row.get("ready_for_polefit8x8_combination") for row in audits)
    kprime_hull = interval_hull(kprime_intervals)
    numerator_hull = interval_hull(numerator_intervals)
    denominator_hull = interval_hull(denominator_intervals)
    strict_certificate_passed = (
        complete_l12
        and not invalid
        and kprime_hull is not None
        and numerator_hull is not None
        and denominator_hull is not None
        and interval_excludes_zero(tuple(kprime_hull))
        and interval_excludes_zero(tuple(numerator_hull))
        and interval_contains(tuple(denominator_hull), 0.0)
    )
    return {
        "available": bool(valid),
        "schema_version": KPRIME_SCHEMA_VERSION,
        "present_row_count": len(present),
        "valid_row_count": len(valid),
        "invalid_row_count": len(invalid),
        "valid_chunks": [row["chunk_index"] for row in valid],
        "invalid_rows": [
            {
                "chunk_index": row["chunk_index"],
                "output": row["output"],
                "reasons": row["validation"].get("reasons", [])[:12],
            }
            for row in invalid[:10]
        ],
        "complete_l12_kprime_rows": complete_l12,
        "strict_certificate_passed": strict_certificate_passed,
        "strict_certificate_status": (
            "strict K-prime row certificate passed"
            if strict_certificate_passed
            else "not passed; absent, partial, invalid, or non-excluding K-prime/source intervals"
        ),
        "conservative_intervals": {
            "effective_denominator_at_pole_hull": denominator_hull,
            "projected_kprime_at_pole_hull": kprime_hull,
            "source_numerator_at_pole_hull": numerator_hull,
        },
        "strict_limit": (
            "A passed K-prime row certificate supplies source-pole denominator "
            "and projection data only. It still does not identify O_sp with "
            "the canonical Higgs mode or authorize retained/proposed-retained "
            "top-Yukawa closure by itself."
        ),
    }


def audit_chunk(expected: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / str(expected.get("output", ""))
    data = load_json(path)
    if not data:
        return {**expected, "exists": False, "ready_for_polefit8x8_combination": False, "issues": ["chunk output absent"]}
    metadata = data.get("metadata", {})
    ensemble = selected_ensemble(data)
    issues: list[str] = []
    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}, expected production")
    if ensemble.get("spatial_L") != 12 or ensemble.get("time_L") != 24:
        issues.append(f"dims={ensemble.get('dims')!r}, expected 12^3x24")
    if ensemble.get("thermalization_sweeps") != EXPECTED_THERM:
        issues.append(f"thermalization_sweeps={ensemble.get('thermalization_sweeps')!r}")
    if ensemble.get("measurement_sweeps") != EXPECTED_CHUNK_MEASUREMENTS:
        issues.append(f"measurement_sweeps={ensemble.get('measurement_sweeps')!r}")
    issues.extend(audit_run_control(metadata, expected))
    issues.extend(audit_seed_control(ensemble, expected))
    issues.extend(audit_source_response(ensemble))
    issues.extend(audit_scalar_lsz(metadata, ensemble))
    kprime_rows = extract_kprime_rows(data)
    kprime_validations = [validate_kprime_row(row) for row in kprime_rows]
    return {
        **expected,
        "exists": True,
        "phase": metadata.get("phase"),
        "ready_for_polefit8x8_combination": not issues,
        "issues": issues,
        "kprime_pole_rows_present": bool(kprime_rows),
        "kprime_pole_row_count": len(kprime_rows),
        "kprime_pole_row_validations": kprime_validations,
    }


def weighted_mean(values: list[tuple[float, float]]) -> dict[str, float]:
    finite = [(v, e) for v, e in values if math.isfinite(v)]
    if not finite:
        return {"mean": float("nan"), "stderr": float("nan")}
    weights = [1.0 / (e * e) if math.isfinite(e) and e > 0.0 else 1.0 for _v, e in finite]
    total = sum(weights)
    mean = sum(v * w for (v, _e), w in zip(finite, weights)) / total
    stderr = math.sqrt(1.0 / total) if total > 0.0 else float("nan")
    return {"mean": float(mean), "stderr": float(stderr)}


def p_hat_sq_from_key(key: str) -> float:
    return sum((2.0 * math.sin(math.pi * int(n) / 12.0)) ** 2 for n in key.split(","))


def combine_ready(audits: list[dict[str, Any]], combined_output: Path) -> dict[str, Any]:
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    if not ready:
        return {"available": False, "reason": "no ready polefit8x8 chunks"}
    source_values: list[tuple[float, float]] = []
    mode_values: dict[str, list[tuple[float, float]]] = {key: [] for key in EXPECTED_MODE_KEYS}
    for row in ready:
        data = load_json(ROOT / str(row["output"]))
        ensemble = selected_ensemble(data)
        source = ensemble.get("scalar_source_response_analysis", {})
        source_values.append(
            (
                float(source.get("slope_dE_ds_lat", float("nan"))),
                float(source.get("slope_dE_ds_lat_err", float("nan"))),
            )
        )
        modes = ensemble.get("scalar_two_point_lsz_analysis", {}).get("mode_rows", {})
        for key in EXPECTED_MODE_KEYS:
            mode = modes.get(key, {})
            err = float(mode.get("C_ss_real_config_stderr", float("nan")))
            mode_values[key].append((float(mode.get("C_ss_real", float("nan"))), err))

    mode_rows = {}
    for key, values in mode_values.items():
        c = weighted_mean(values)
        gamma = 1.0 / c["mean"] if math.isfinite(c["mean"]) and abs(c["mean"]) > 1.0e-30 else float("nan")
        mode_rows[key] = {
            "momentum_mode": [int(part) for part in key.split(",")],
            "p_hat_sq": p_hat_sq_from_key(key),
            "C_ss_real_weighted": c["mean"],
            "C_ss_real_weighted_stderr": c["stderr"],
            "Gamma_ss_real_proxy": gamma,
        }
    return {
        "available": True,
        "combined_output_target": rel(combined_output),
        "chunk_count": len(ready),
        "saved_configurations": len(ready) * EXPECTED_CHUNK_MEASUREMENTS,
        "complete_l12_target": len(ready) == len(audits),
        "source_response": weighted_mean(source_values),
        "mode_rows": mode_rows,
    }


def write_combined(
    summary: dict[str, Any],
    audits: list[dict[str, Any]],
    combined_output: Path,
    manifest_path: Path,
    kprime_summary: dict[str, Any],
) -> None:
    if not summary.get("available"):
        return
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    payload = {
        "metadata": {
            "phase": "partial_l12_polefit8x8_chunk_summary"
            if not summary.get("complete_l12_target")
            else "combined_l12_polefit8x8_chunk_summary",
            "source": "frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py",
            "manifest": rel(manifest_path),
            "chunk_count": summary.get("chunk_count"),
            "saved_configurations": summary.get("saved_configurations"),
            "complete_l12_target": summary.get("complete_l12_target"),
            "strict_limit": (
                "Eight-mode/x8 L12 rows are same-source scalar-LSZ support only. "
                "They do not supply L16/L24 scaling, FV/IR/zero-mode control, "
                "a model-class theorem, canonical-Higgs/source overlap, or "
                "retained-proposal authority."
            ),
        },
        "chunk_indices": [int(row["chunk_index"]) for row in ready],
        "source_response_summary": summary.get("source_response", {}),
        "combined_lsz_summary": {"mode_rows": summary.get("mode_rows", {})},
        "kprime_pole_row_certificate": kprime_summary,
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not mix this eight-mode/x8 stream with the four-mode/x16 L12 stream",
        ],
    }
    combined_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--combined-output", type=Path, default=COMBINED_OUTPUT)
    parser.add_argument("--kprime-fixture", type=Path, default=KPRIME_FIXTURE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = resolve_repo_path(args.manifest)
    output_path = resolve_repo_path(args.output)
    combined_output = resolve_repo_path(args.combined_output)
    fixture_path = resolve_repo_path(args.kprime_fixture)

    print("PR #230 FH/LSZ eight-mode/x8 pole-fit chunk combiner gate")
    print("=" * 72)

    manifest = load_json(manifest_path)
    chunks = manifest_chunks(manifest)
    audits = [audit_chunk(row) for row in chunks]
    present = [row for row in audits if row.get("exists")]
    ready = [row for row in audits if row.get("ready_for_polefit8x8_combination")]
    missing = [row for row in audits if not row.get("exists")]
    kprime_fixture = validate_kprime_fixture(fixture_path)
    kprime_summary = combine_kprime_rows(audits)
    combined = combine_ready(audits, combined_output)
    combined_output.parent.mkdir(parents=True, exist_ok=True)
    write_combined(combined, audits, combined_output, manifest_path, kprime_summary)
    shells = sorted({round(p_hat_sq_from_key(key), 12) for key in EXPECTED_MODE_KEYS})

    report("manifest-loaded", bool(manifest), rel(manifest_path))
    report("chunk-grid-reconstructed", len(chunks) == 63, f"chunks={len(chunks)}")
    report("polefit8x8-mode-shape-recorded", len(shells) >= 4, f"shells={shells}")
    report("present-chunks-valid-or-absent", all(row.get("ready_for_polefit8x8_combination") or not row.get("exists") for row in audits), f"present={len(present)} ready={len(ready)}")
    report("kprime-fixture-schema-valid", kprime_fixture.get("valid") is True, f"rows={kprime_fixture.get('row_count')} fixture={rel(fixture_path)}")
    report("present-kprime-rows-valid-or-absent", kprime_summary.get("invalid_row_count") == 0, f"present={kprime_summary.get('present_row_count')} valid={kprime_summary.get('valid_row_count')}")
    report("combination-state-recorded", True, f"ready={len(ready)} missing={len(missing)} combined={combined.get('available')}")
    report("not-retained-closure", True, "polefit8x8 L12 rows are support only")

    complete = bool(chunks) and len(ready) == len(chunks)
    status = (
        "bounded-support / FH-LSZ complete L12 eight-mode-x8 pole-fit summary constructed"
        if complete
        else "bounded-support / FH-LSZ partial eight-mode-x8 pole-fit stream"
        if ready
        else "open / FH-LSZ eight-mode-x8 pole-fit combiner awaiting chunks"
    )
    result = {
        "actual_current_surface_status": status,
        "verdict": (
            "The separate eight-mode/x8 pole-fit stream has an auditable combiner "
            f"gate.  Present chunks={len(present)}, ready chunks={len(ready)}, "
            f"expected chunks={len(chunks)}.  The combiner writes a diagnostic "
            "L12 same-source scalar-LSZ support summary when ready chunks exist, "
            "but that summary is not physical y_t evidence and cannot be mixed "
            "with the four-mode/x16 L12 stream."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "L12 polefit8x8 rows do not close FV/IR, model-class, or canonical-Higgs/source-overlap gates.",
        "manifest": rel(manifest_path),
        "combined_output_target": rel(combined_output),
        "chunk_summary": {
            "expected_chunks": len(chunks),
            "present_chunks": len(present),
            "ready_chunks": len(ready),
            "missing_chunks": len(missing),
            "target_saved_configurations": int(manifest.get("chunk_policy", {}).get("target_measurements", 0)) if manifest else 0,
            "available_saved_configurations": len(ready) * EXPECTED_CHUNK_MEASUREMENTS,
        },
        "first_missing_outputs": [row["output"] for row in missing[:10]],
        "first_blocking_issues": [
            {"chunk_index": row["chunk_index"], "output": row["output"], "issues": row.get("issues", [])[:5]}
            for row in audits
            if row.get("issues")
        ][:10],
        "combined_summary": combined,
        "kprime_pole_row_schema": kprime_schema_manifest(),
        "kprime_fixture_validation": kprime_fixture,
        "kprime_pole_row_certificate": kprime_summary,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not mix eight-mode/x8 and four-mode/x16 chunks as one homogeneous ensemble",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(output_path)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
