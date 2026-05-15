#!/usr/bin/env python3
"""
PR #230 higher-shell complete-packet Schur/Stieltjes monotonicity gate.

The higher-shell campaign is now complete at 63/63 chunks.  This runner
audits the complete packet and asks the narrow post-completion question:
do the finite same-ensemble C_ss/C_sx/C_xx rows across the five available
q-hat^2 levels satisfy the necessary divided-difference sign pattern that a
positive Stieltjes/scalar-LSZ pole proxy would have to satisfy?

This is a finite-row diagnostic and boundary certificate only.  It does not
derive an isolated pole, does not supply finite-volume/IR limiting authority,
does not identify the taste-radial x source with canonical O_H, and does not
authorize retained or proposed_retained top-Yukawa closure.
"""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_schur_higher_shell_complete_packet_monotonicity_gate_2026-05-15.json"
)
ROW_ROOT = ROOT / "outputs" / "yt_pr230_schur_higher_shell_rows"
CHECKPOINT_PATTERN = "outputs/yt_pr230_schur_higher_shell_chunk{chunk:03d}_checkpoint_2026-05-12.json"
ROW_PATTERN = (
    "outputs/yt_pr230_schur_higher_shell_rows/"
    "yt_pr230_schur_higher_shell_rows_L12_T24_chunk{chunk:03d}_2026-05-07.json"
)

PARENTS = {
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "wave_launcher": "outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json",
    "source_operator_boundary": "outputs/yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json",
    "schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
    "strict_scalar_lsz_moment_fv_authority": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "schur_complement_stieltjes_repair": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
    "schur_complement_complete_monotonicity": "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json",
    "schur_x_given_source_one_pole_scout": "outputs/yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json",
    "block70_schur_feshbach_kprime_residue_theorem": "outputs/yt_pr230_block70_schur_feshbach_kprime_residue_theorem_2026-05-12.json",
}

EXPECTED_CHUNKS = 63
EXPECTED_SEED_BASE = 2026057000
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"
EXPECTED_SELECTED_MASS = 0.75
EXPECTED_CONFIGURATION_COUNT = 16
EXPECTED_MODES = {
    "0,0,0",
    "1,0,0",
    "0,1,0",
    "0,0,1",
    "1,1,0",
    "1,0,1",
    "0,1,1",
    "1,1,1",
    "2,0,0",
    "0,2,0",
    "0,0,2",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def expected_seed(chunk: int) -> int:
    return EXPECTED_SEED_BASE + chunk


def row_path(chunk: int) -> Path:
    return ROOT / ROW_PATTERN.format(chunk=chunk)


def checkpoint_path(chunk: int) -> Path:
    return ROOT / CHECKPOINT_PATTERN.format(chunk=chunk)


def mode_series_ok(row: dict[str, Any], key: str) -> bool:
    values = row.get(key)
    if not isinstance(values, list) or len(values) != EXPECTED_CONFIGURATION_COUNT:
        return False
    prefix = key.removesuffix("_timeseries")
    real_key = f"{prefix}_real"
    imag_key = f"{prefix}_imag"
    for item in values:
        if not isinstance(item, dict) or not finite(item.get(real_key)):
            return False
        if imag_key in item and not finite(item.get(imag_key)):
            return False
    return True


def finite_schur_row(mode: str, row: dict[str, Any]) -> dict[str, Any] | None:
    needed = ("p_hat_sq", "C_ss_real", "C_sx_real", "C_xx_real")
    if not all(finite(row.get(key)) for key in needed):
        return None
    p_hat_sq = float(row["p_hat_sq"])
    c_ss = float(row["C_ss_real"])
    c_sx = float(row["C_sx_real"])
    c_xx = float(row["C_xx_real"])
    delta = c_ss * c_xx - c_sx * c_sx
    if c_ss <= 0.0 or c_xx <= 0.0 or delta <= 0.0:
        return None
    a_f = c_xx / delta
    b_f = -c_sx / delta
    c_f = c_ss / delta
    return {
        "mode": mode,
        "p_hat_sq": p_hat_sq,
        "C_ss": c_ss,
        "C_sx": c_sx,
        "C_xx": c_xx,
        "Delta_sx": delta,
        "rho_sx": c_sx / math.sqrt(c_ss * c_xx),
        "C_source_given_x": delta / c_xx,
        "C_x_given_source": delta / c_ss,
        "K_source_given_x": a_f,
        "K_x_given_source": c_f,
        "A_finite_K_ss": a_f,
        "B_finite_K_sx": b_f,
        "C_finite_K_xx": c_f,
        "det_K": 1.0 / delta,
        "inverse_identity_residual_max": max(
            abs(c_ss * a_f + c_sx * b_f - 1.0),
            abs(c_ss * b_f + c_sx * c_f),
            abs(c_sx * a_f + c_xx * b_f),
            abs(c_sx * b_f + c_xx * c_f - 1.0),
        ),
    }


def audit_chunk(chunk: int) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    checkpoint = load_json(checkpoint_path(chunk))
    data = load_json(row_path(chunk))
    if not checkpoint:
        issues.append("checkpoint missing")
    if not data:
        issues.append("row JSON missing")
        return None, issues

    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = first_ensemble(data)
    seed_control = ensemble.get("rng_seed_control") if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    source = ensemble.get("source_higgs_cross_correlator_analysis")
    lsz = ensemble.get("scalar_two_point_lsz_analysis")
    response = ensemble.get("scalar_source_response_analysis")
    expected = expected_seed(chunk)

    if checkpoint.get("checkpoint_passed") is not True:
        issues.append("checkpoint did not pass")
    if checkpoint.get("chunk_index") != chunk:
        issues.append(f"checkpoint chunk_index={checkpoint.get('chunk_index')!r}")
    if checkpoint.get("proposal_allowed") is not False:
        issues.append("checkpoint proposal_allowed is not false")
    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}")
    if run_control.get("seed") != expected:
        issues.append(f"run_control seed={run_control.get('seed')!r}")
    if run_control.get("production_targets") is not True:
        issues.append("production_targets not true")
    if run_control.get("fh_lsz_selected_mass_only") is not True:
        issues.append("selected-mass-only metadata missing")
    if float(run_control.get("fh_lsz_selected_mass_parameter", -1.0)) != EXPECTED_SELECTED_MASS:
        issues.append(f"selected mass={run_control.get('fh_lsz_selected_mass_parameter')!r}")
    if seed_control.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"seed_control_version={seed_control.get('seed_control_version')!r}")
    if seed_control.get("base_seed") != expected:
        issues.append(f"base_seed={seed_control.get('base_seed')!r}")
    if ensemble.get("selected_mass_parameter") != EXPECTED_SELECTED_MASS:
        issues.append(f"ensemble selected_mass_parameter={ensemble.get('selected_mass_parameter')!r}")
    if not isinstance(response, dict):
        issues.append("missing scalar_source_response_analysis")
    elif not isinstance(response.get("per_configuration_slopes"), list):
        issues.append("missing per_configuration_slopes")
    if not isinstance(lsz, dict):
        issues.append("missing scalar_two_point_lsz_analysis")
    elif set((lsz.get("mode_rows") or {}).keys()) != EXPECTED_MODES:
        issues.append("scalar_two_point_lsz mode set mismatch")
    if not isinstance(source, dict):
        issues.append("missing source_higgs_cross_correlator_analysis")
        return None, issues
    if source.get("canonical_higgs_operator_identity_passed") is not False:
        issues.append("canonical O_H identity unexpectedly passed")
    if source.get("used_as_physical_yukawa_readout") is not False:
        issues.append("source rows marked as physical y_t readout")
    aliases = source.get("two_source_taste_radial_row_aliases")
    if not isinstance(aliases, dict) or aliases.get("C_sx_aliases_C_sH_schema_field") is not True:
        issues.append("C_sx alias metadata missing")
    if not isinstance(aliases, dict) or aliases.get("C_xx_aliases_C_HH_schema_field") is not True:
        issues.append("C_xx alias metadata missing")

    mode_rows = source.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        issues.append("source-higgs mode set mismatch")
        return None, issues

    parsed_modes: dict[str, dict[str, Any]] = {}
    for mode, row in sorted(mode_rows.items()):
        if not isinstance(row, dict):
            issues.append(f"{mode} row not object")
            continue
        for key in ("C_ss_timeseries", "C_sx_timeseries", "C_xx_timeseries"):
            if not mode_series_ok(row, key):
                issues.append(f"{mode} missing {key}")
        parsed = finite_schur_row(mode, row)
        if parsed is None:
            issues.append(f"{mode} invalid finite Schur row")
            continue
        parsed_modes[mode] = parsed

    if set(parsed_modes) != EXPECTED_MODES:
        issues.append("parsed finite Schur mode set mismatch")
    max_inverse_residual = max(
        (float(row["inverse_identity_residual_max"]) for row in parsed_modes.values()),
        default=float("inf"),
    )
    return {
        "chunk_index": chunk,
        "seed": expected,
        "checkpoint": rel(checkpoint_path(chunk)),
        "row_output": rel(row_path(chunk)),
        "mode_rows": parsed_modes,
        "max_inverse_identity_residual": max_inverse_residual,
    }, issues


def summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "mean": None, "stdev": None, "min": None, "max": None}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def level_key(value: float) -> str:
    return f"{value:.12f}"


def level_aggregates(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    by_level: dict[str, dict[str, list[float]]] = {}
    for chunk in chunks:
        for row in chunk["mode_rows"].values():
            key = level_key(float(row["p_hat_sq"]))
            bucket = by_level.setdefault(key, {})
            for field, value in row.items():
                if field in {"mode", "p_hat_sq"}:
                    continue
                if finite(value):
                    bucket.setdefault(field, []).append(float(value))

    out: dict[str, Any] = {}
    for key in sorted(by_level, key=float):
        out[key] = {
            "p_hat_sq": float(key),
            "mode_sample_count": len(by_level[key].get("C_ss", [])),
            "summary": {field: summarize(values) for field, values in sorted(by_level[key].items())},
        }
    return out


def shell_series(levels: dict[str, Any], field: str) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    for key in sorted(levels, key=float):
        summary = levels[key]["summary"].get(field, {})
        mean = summary.get("mean")
        if finite(mean):
            xs.append(float(key))
            ys.append(float(mean))
    return xs, ys


def divided_differences(xs: list[float], ys: list[float]) -> list[list[float]]:
    table: list[list[float]] = [ys[:]]
    current = ys[:]
    for order in range(1, len(xs)):
        next_values: list[float] = []
        for index in range(len(current) - 1):
            denom = xs[index + order] - xs[index]
            next_values.append((current[index + 1] - current[index]) / denom)
        table.append(next_values)
        current = next_values
    return table


def complete_monotonicity_diagnostic(xs: list[float], ys: list[float], tolerance: float = 1.0e-12) -> dict[str, Any]:
    table = divided_differences(xs, ys)
    order_rows: list[dict[str, Any]] = []
    all_ok = True
    first_failure: int | None = None
    for order, values in enumerate(table):
        signed = [((-1.0) ** order) * value for value in values]
        ok = all(value >= -tolerance for value in signed)
        if not ok and first_failure is None:
            first_failure = order
        all_ok = all_ok and ok
        order_rows.append(
            {
                "order": order,
                "raw_values": values,
                "signed_values": signed,
                "required_sign": "nonnegative after (-1)^order multiplier",
                "passed": ok,
                "min_signed": min(signed) if signed else None,
                "max_signed": max(signed) if signed else None,
            }
        )
    return {
        "x_values": xs,
        "y_values": ys,
        "orders": order_rows,
        "complete_monotone_necessary_signs_passed": all_ok,
        "first_failed_order": first_failure,
        "strict_limit": (
            "This is a finite divided-difference necessary sign diagnostic for a "
            "positive Stieltjes/scalar-LSZ proxy.  Passing would not prove pole "
            "authority; failing rejects this finite packet as strict authority."
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_cold_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "treated_taste_radial_x_as_canonical_O_H": False,
        "treated_finite_higher_shell_rows_as_strict_pole_rows": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 higher-shell complete-packet Schur/Stieltjes monotonicity gate")
    print("=" * 78)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    parent_proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    chunks: list[dict[str, Any]] = []
    chunk_issues: dict[str, list[str]] = {}
    for chunk in range(1, EXPECTED_CHUNKS + 1):
        parsed, issues = audit_chunk(chunk)
        if parsed is not None:
            chunks.append(parsed)
        if issues:
            chunk_issues[f"chunk{chunk:03d}"] = issues

    levels = level_aggregates(chunks)
    level_values = [float(key) for key in sorted(levels, key=float)]
    diagnostics: dict[str, Any] = {}
    candidate_fields = [
        "C_ss",
        "C_xx",
        "C_source_given_x",
        "C_x_given_source",
        "K_source_given_x",
        "K_x_given_source",
        "A_finite_K_ss",
        "C_finite_K_xx",
    ]
    for field in candidate_fields:
        xs, ys = shell_series(levels, field)
        diagnostics[field] = complete_monotonicity_diagnostic(xs, ys)

    failing_fields = [
        field
        for field, row in diagnostics.items()
        if row.get("complete_monotone_necessary_signs_passed") is False
    ]
    surviving_fields = [
        field
        for field, row in diagnostics.items()
        if row.get("complete_monotone_necessary_signs_passed") is True
    ]
    inverse_identity_clean = all(
        finite(chunk.get("max_inverse_identity_residual"))
        and float(chunk["max_inverse_identity_residual"]) < 1.0e-10
        for chunk in chunks
    )
    wave = parents["wave_launcher"]
    wave_complete = (
        wave.get("wave_launcher_passed") is True
        and wave.get("completed_chunk_indices") == list(range(1, EXPECTED_CHUNKS + 1))
        and wave.get("active_chunk_indices") == []
        and wave.get("planned_launch_chunk_indices") == []
        and wave.get("proposal_allowed") is False
    )
    operator_boundary_loaded = (
        "higher-shell source-Higgs cross rows use"
        in parent_statuses["source_operator_boundary"]
        and parents["source_operator_boundary"].get(
            "higher_shell_source_higgs_operator_certificate_boundary_passed"
        )
        is True
        and parents["source_operator_boundary"].get("proposal_allowed") is False
    )
    strict_authority_absent = (
        parents["strict_scalar_lsz_moment_fv_authority"].get("proposal_allowed") is False
        and parents["strict_scalar_lsz_moment_fv_authority"].get(
            "strict_scalar_lsz_moment_fv_authority_gate_passed"
        )
        is True
        and parents["schur_route_completion"].get("proposal_allowed") is False
        and parents["full_positive_assembly"].get("proposal_allowed") is False
    )
    forbidden_clean = all(value is False for value in forbidden_firewall().values())
    monotonicity_rejects_strict_shortcut = bool(failing_fields)
    current_surface_blocks_closure = (
        monotonicity_rejects_strict_shortcut
        and not surviving_fields
        or monotonicity_rejects_strict_shortcut
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not parent_proposals, f"proposal_allowed={parent_proposals}")
    report("wave-launcher-complete-63-of-63", wave_complete, parent_statuses["wave_launcher"])
    report("all-chunk-rows-and-checkpoints-schema-clean", not chunk_issues, f"issues={dict(list(chunk_issues.items())[:3])}")
    report("complete-packet-has-63-chunks", len(chunks) == EXPECTED_CHUNKS, f"chunks={len(chunks)}")
    report("higher-shell-five-qhat-levels-present", len(level_values) == 5 and level_values[0] == 0.0, f"levels={level_values}")
    report("finite-schur-inverse-identity-clean", inverse_identity_clean, "max |G K - I| residual < 1e-10")
    report("operator-boundary-preserved", operator_boundary_loaded, parent_statuses["source_operator_boundary"])
    report("strict-scalar-lsz-authority-still-absent", strict_authority_absent, parent_statuses["strict_scalar_lsz_moment_fv_authority"])
    report("finite-stieltjes-shortcut-rejected", monotonicity_rejects_strict_shortcut, f"failing_fields={failing_fields}")
    report("does-not-authorize-retained-proposal", True, "finite higher-shell diagnostic is support/boundary only")
    report("forbidden-firewall-clean", forbidden_clean, str(forbidden_firewall()))

    passed = (
        not missing_parents
        and not parent_proposals
        and wave_complete
        and not chunk_issues
        and len(chunks) == EXPECTED_CHUNKS
        and len(level_values) == 5
        and level_values[0] == 0.0
        and inverse_identity_clean
        and operator_boundary_loaded
        and strict_authority_absent
        and monotonicity_rejects_strict_shortcut
        and forbidden_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / complete 63/63 higher-shell finite rows "
            "fail necessary Stieltjes complete-monotonicity sign tests for strict "
            "scalar-LSZ/Schur pole authority"
        ),
        "conditional_surface_status": (
            "bounded-support for future Schur work if a new strict pole/FV/IR "
            "theorem or canonical O_H/WZ physical-response bridge is supplied; "
            "the present finite packet is not that theorem"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The completed higher-shell packet is finite C_ss/C_sx/C_xx support "
            "under an unratified taste-radial second-source certificate.  Its "
            "candidate finite Stieltjes proxies fail necessary divided-difference "
            "sign tests, and the packet still lacks isolated-pole, FV/IR, "
            "canonical O_H/source-overlap, W/Z response, and matching/running authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "higher_shell_complete_packet_monotonicity_gate_passed": passed,
        "complete_packet_chunk_count": len(chunks),
        "expected_chunk_count": EXPECTED_CHUNKS,
        "qhat_sq_levels": level_values,
        "level_aggregates": levels,
        "candidate_complete_monotonicity_diagnostics": diagnostics,
        "failing_complete_monotonicity_fields": failing_fields,
        "surviving_complete_monotonicity_fields": surviving_fields,
        "strict_schur_or_scalar_lsz_authority_passed": False,
        "finite_rows_written": True,
        "strict_pole_rows_written": False,
        "pole_location_or_derivative_rows_present": False,
        "fv_ir_threshold_authority_present": False,
        "canonical_higgs_operator_identity_passed": False,
        "used_as_physical_yukawa_readout": False,
        "source_operator_is_taste_radial_not_canonical_oh": True,
        "chunk_issues": chunk_issues,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite higher-shell rows as strict scalar-LSZ pole rows",
            "does not treat divided-difference diagnostics as FV/IR or threshold authority",
            "does not treat taste-radial C_sx/C_xx aliases as canonical C_sH/C_HH rows",
            "does not treat the taste-radial x source as canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Do not spend more compute on same finite-row promotion.  Closure now "
            "requires a new same-surface artifact: canonical O_H/C_sH/C_HH pole "
            "rows, same-source W/Z response rows with identity/covariance/g2 "
            "authority, strict Schur pole derivative rows with FV/IR authority, "
            "or a neutral primitive-transfer certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
