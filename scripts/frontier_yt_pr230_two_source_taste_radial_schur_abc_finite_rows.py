#!/usr/bin/env python3
"""
PR #230 two-source taste-radial finite Schur A/B/C row certificate.

Completed two-source taste-radial chunks provide finite same-ensemble
correlator blocks

    G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]].

This runner computes the finite inverse-block rows

    K(q) = G(q)^(-1) = [[A_f(q), B_f(q)], [B_f(q), C_f(q)]]

for the certified source/complement chart.  This is a real finite row artifact
for the Schur route, but it is not the strict neutral-kernel A/B/C pole-row
packet required for closure.  It does not identify x with canonical O_H, does
not supply FV/IR or pole-derivative authority, and does not set kappa_s = 1.
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
    / "yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json"
)
MANIFEST = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
)
COMBINER = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"
)

PARENTS = {
    "two_source_schur_subblock_witness": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
    "two_source_schur_kprime_finite_shell_scout": "outputs/yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kernel_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_abc_definition": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
ZERO_MODE = "0,0,0"
EXPECTED_SEED_CONTROL_VERSION = "numba_gauge_seed_v1"

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


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    row = ensembles[0]
    return row if isinstance(row, dict) else {}


def manifest_rows_for_ready_chunks(
    manifest: dict[str, Any], combiner: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = manifest.get("chunk_commands")
    ready_indices = combiner.get("ready_chunk_indices")
    if not isinstance(rows, list) or not isinstance(ready_indices, list):
        return []
    ready = {int(index) for index in ready_indices if isinstance(index, int)}
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and int(row["chunk_index"]) in ready
    ]


def finite_inverse_rows(mode: str, row: dict[str, Any]) -> dict[str, Any] | None:
    needed = ("p_hat_sq", "C_ss_real", "C_sx_real", "C_xx_real")
    if not all(finite(row.get(key)) for key in needed):
        return None
    p_hat_sq = float(row["p_hat_sq"])
    c_ss = float(row["C_ss_real"])
    c_sx = float(row["C_sx_real"])
    c_xx = float(row["C_xx_real"])
    delta = c_ss * c_xx - c_sx * c_sx
    if delta <= 0.0 or c_ss <= 0.0 or c_xx <= 0.0:
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
        "A_finite_K_ss": a_f,
        "B_finite_K_sx": b_f,
        "C_finite_K_xx": c_f,
        "det_K": 1.0 / delta,
        "inverse_identity_check": {
            "ss": c_ss * a_f + c_sx * b_f,
            "sx": c_ss * b_f + c_sx * c_f,
            "xs": c_sx * a_f + c_xx * b_f,
            "xx": c_sx * b_f + c_xx * c_f,
        },
        "strict_limit": (
            "Finite inverse of the measured correlator block.  Not a strict "
            "neutral-kernel A/B/C row at the scalar pole."
        ),
    }


def read_chunk(row: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    chunk_index = row.get("chunk_index")
    output = ROOT / str(row.get("output", ""))
    if not output.exists():
        return None, [f"chunk{chunk_index} output absent"]
    data = load_json(output)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = selected_ensemble(data)
    seed = ensemble.get("rng_seed_control") if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    source = ensemble.get("source_higgs_cross_correlator_analysis")

    if metadata.get("phase") != "production":
        issues.append(f"chunk{chunk_index} phase={metadata.get('phase')!r}")
    if run_control.get("seed") != row.get("seed"):
        issues.append(f"chunk{chunk_index} seed mismatch")
    if seed.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"chunk{chunk_index} seed control mismatch")
    if ensemble.get("selected_mass_parameter") != 0.75:
        issues.append(f"chunk{chunk_index} selected mass mismatch")
    if not isinstance(source, dict):
        issues.append(f"chunk{chunk_index} source rows absent")
        return None, issues
    if source.get("canonical_higgs_operator_identity_passed") is not False:
        issues.append(f"chunk{chunk_index} canonical O_H unexpectedly passed")
    if source.get("used_as_physical_yukawa_readout") is not False:
        issues.append(f"chunk{chunk_index} source rows marked physical")
    aliases = source.get("two_source_taste_radial_row_aliases")
    if not isinstance(aliases, dict) or aliases.get("C_sx_aliases_C_sH_schema_field") is not True:
        issues.append(f"chunk{chunk_index} C_sx alias missing")
    if not isinstance(aliases, dict) or aliases.get("C_xx_aliases_C_HH_schema_field") is not True:
        issues.append(f"chunk{chunk_index} C_xx alias missing")

    mode_rows = source.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        issues.append(f"chunk{chunk_index} mode set mismatch")
        return None, issues

    modes: dict[str, dict[str, Any]] = {}
    for mode, mode_row in sorted(mode_rows.items()):
        if not isinstance(mode_row, dict):
            issues.append(f"chunk{chunk_index} {mode} row not object")
            continue
        parsed = finite_inverse_rows(mode, mode_row)
        if parsed is None:
            issues.append(f"chunk{chunk_index} {mode} invalid inverse block")
            continue
        modes[mode] = parsed

    zero = modes.get(ZERO_MODE)
    shell_modes = [mode for mode in sorted(modes) if mode != ZERO_MODE]
    if zero is None or set(shell_modes) != (EXPECTED_MODES - {ZERO_MODE}):
        issues.append(f"chunk{chunk_index} zero/shell rows missing")
        return None, issues
    shell_p_values = [float(modes[mode]["p_hat_sq"]) for mode in shell_modes]
    shell_p_mean = statistics.fmean(shell_p_values)
    if not all(abs(value - shell_p_mean) <= 1.0e-12 for value in shell_p_values):
        issues.append(f"chunk{chunk_index} shell p_hat_sq anisotropy")
    if shell_p_mean <= float(zero["p_hat_sq"]):
        issues.append(f"chunk{chunk_index} shell p_hat_sq not above zero")
        return None, issues

    def mean_shell(key: str) -> float:
        return statistics.fmean(float(modes[mode][key]) for mode in shell_modes)

    dp = shell_p_mean - float(zero["p_hat_sq"])
    finite_difference = {}
    for key in ("A_finite_K_ss", "B_finite_K_sx", "C_finite_K_xx", "det_K", "rho_sx"):
        finite_difference[f"{key}_zero"] = float(zero[key])
        finite_difference[f"{key}_shell_mean"] = mean_shell(key)
        finite_difference[f"{key}_shell_minus_zero_over_dp"] = (
            finite_difference[f"{key}_shell_mean"] - finite_difference[f"{key}_zero"]
        ) / dp

    max_inverse_identity_residual = 0.0
    for mode_row in modes.values():
        checks = mode_row["inverse_identity_check"]
        residuals = (
            abs(float(checks["ss"]) - 1.0),
            abs(float(checks["sx"])),
            abs(float(checks["xs"])),
            abs(float(checks["xx"]) - 1.0),
        )
        max_inverse_identity_residual = max(max_inverse_identity_residual, *residuals)

    return {
        "chunk_index": int(chunk_index),
        "seed": row.get("seed"),
        "mode_rows": modes,
        "shell_p_hat_sq_mean": shell_p_mean,
        "shell_p_hat_sq_stdev": statistics.stdev(shell_p_values) if len(shell_p_values) > 1 else 0.0,
        "finite_difference": finite_difference,
        "max_inverse_identity_residual": max_inverse_identity_residual,
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


def summarize_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    keys = (
        "A_finite_K_ss_zero",
        "A_finite_K_ss_shell_mean",
        "A_finite_K_ss_shell_minus_zero_over_dp",
        "B_finite_K_sx_zero",
        "B_finite_K_sx_shell_mean",
        "B_finite_K_sx_shell_minus_zero_over_dp",
        "C_finite_K_xx_zero",
        "C_finite_K_xx_shell_mean",
        "C_finite_K_xx_shell_minus_zero_over_dp",
        "det_K_zero",
        "det_K_shell_mean",
        "det_K_shell_minus_zero_over_dp",
        "rho_sx_zero",
        "rho_sx_shell_mean",
        "rho_sx_shell_minus_zero_over_dp",
    )
    return {
        key: summarize(
            [
                float(chunk["finite_difference"][key])
                for chunk in chunks
                if finite(chunk.get("finite_difference", {}).get(key))
            ]
        )
        for key in keys
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
        "treated_finite_inverse_rows_as_strict_kernel_rows": False,
        "treated_finite_shell_slope_as_kprime_pole": False,
        "treated_taste_radial_x_as_canonical_O_H": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 two-source taste-radial finite Schur A/B/C rows")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    ready_rows = manifest_rows_for_ready_chunks(manifest, combiner)
    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")

    chunks: list[dict[str, Any]] = []
    chunk_issues: list[str] = []
    for row in ready_rows:
        chunk, issues = read_chunk(row)
        if chunk is not None:
            chunks.append(chunk)
        chunk_issues.extend(issues)

    summary = summarize_chunks(chunks)
    finite_rows = all(
        finite(mode_row.get("A_finite_K_ss"))
        and finite(mode_row.get("B_finite_K_sx"))
        and finite(mode_row.get("C_finite_K_xx"))
        and finite(mode_row.get("Delta_sx"))
        and float(mode_row["Delta_sx"]) > 0.0
        for chunk in chunks
        for mode_row in chunk.get("mode_rows", {}).values()
    )
    inverse_identity_clean = all(
        finite(chunk.get("max_inverse_identity_residual"))
        and float(chunk["max_inverse_identity_residual"]) < 1.0e-10
        for chunk in chunks
    )
    shell_complete = (
        isinstance(ready_chunks, int)
        and len(chunks) == ready_chunks
        and all(set(chunk.get("mode_rows", {})) == EXPECTED_MODES for chunk in chunks)
    )
    finite_derivatives = all(
        finite(value)
        for chunk in chunks
        for value in chunk.get("finite_difference", {}).values()
    )
    witness_loaded = (
        parents["two_source_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and parents["two_source_schur_subblock_witness"].get("proposal_allowed") is False
    )
    scout_loaded = (
        parents["two_source_schur_kprime_finite_shell_scout"].get(
            "finite_shell_schur_kprime_scout_passed"
        )
        is True
        and parents["two_source_schur_kprime_finite_shell_scout"].get(
            "strict_schur_kprime_authority_passed"
        )
        is False
        and parents["two_source_schur_kprime_finite_shell_scout"].get("proposal_allowed")
        is False
    )
    schur_support_loaded = (
        parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_schur_kernel_rows_present") is False
    )
    strict_contract_still_open = (
        parents["schur_kernel_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_kernel_contract"].get("candidate_rows_present") is False
    )
    abc_definition_boundary_loaded = (
        parents["schur_abc_definition"].get("exact_negative_boundary_passed") is True
        and parents["schur_abc_definition"].get("schur_abc_rows_written") is False
        and parents["schur_abc_definition"].get("proposal_allowed") is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    packet_support_boundary = (
        isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and 0 < ready_chunks <= expected_chunks
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("schur-subblock-witness-loaded", witness_loaded, statuses["two_source_schur_subblock_witness"])
    report("finite-shell-kprime-scout-loaded", scout_loaded, statuses["two_source_schur_kprime_finite_shell_scout"])
    report("schur-sufficiency-loaded", schur_support_loaded, statuses["schur_sufficiency"])
    report("strict-schur-contract-still-open", strict_contract_still_open, statuses["schur_kernel_contract"])
    report("abc-definition-boundary-loaded", abc_definition_boundary_loaded, statuses["schur_abc_definition"])
    report("ready-manifest-rows-found", len(ready_rows) == ready_chunks, f"rows={len(ready_rows)} ready={ready_chunks}")
    report("chunk-row-audits-clean", not chunk_issues, f"issues={chunk_issues[:5]}")
    report("zero-plus-first-shell-complete", shell_complete, f"chunks={len(chunks)} ready={ready_chunks}")
    report("finite-inverse-abc-rows-finite", finite_rows, "A_f/B_f/C_f rows finite with Delta_sx>0")
    report("inverse-identity-check-clean", inverse_identity_clean, "max |G K - I| residual < 1e-10")
    report("finite-shell-abc-differences-finite", finite_derivatives, str(summary))
    report("finite-packet-boundary-preserved", packet_support_boundary, f"ready={ready_chunks}/{expected_chunks}")
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    passed = (
        not missing
        and not proposals
        and witness_loaded
        and scout_loaded
        and schur_support_loaded
        and strict_contract_still_open
        and abc_definition_boundary_loaded
        and len(ready_rows) == ready_chunks
        and not chunk_issues
        and shell_complete
        and finite_rows
        and inverse_identity_clean
        and finite_derivatives
        and packet_support_boundary
        and retained_open
        and campaign_open
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / finite Schur A/B/C inverse-block rows from "
            "two-source taste-radial correlator subblocks; strict pole rows absent"
        ),
        "conditional_surface_status": (
            "conditional-support for the Schur route only after complete 63/63 "
            "rows, isolated-pole K'(pole) or equivalent derivative authority, "
            "FV/IR limiting control, and canonical O_H/source-overlap or "
            "same-source W/Z response authority are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The runner computes finite inverse rows from measured C_ss/C_sx/C_xx "
            "blocks.  These rows are not the strict neutral-kernel A/B/C pole-row "
            "packet and cannot provide closure without pole/FV/IR and canonical "
            "bridge authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "two_source_taste_radial_schur_abc_finite_rows_passed": passed,
        "finite_schur_abc_rows_written": True,
        "strict_schur_abc_kernel_rows_written": False,
        "strict_schur_kprime_authority_passed": False,
        "pole_location_or_derivative_rows_present": False,
        "fv_ir_zero_mode_authority_present": False,
        "canonical_higgs_operator_identity_passed": False,
        "used_as_physical_yukawa_readout": False,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "ready_chunk_indices": combiner.get("ready_chunk_indices"),
        "chunk_finite_schur_abc_rows": chunks,
        "finite_shell_summary": summary,
        "row_definition": {
            "G": "[[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]",
            "Delta_sx": "C_ss*C_xx - C_sx^2",
            "A_finite_K_ss": "C_xx / Delta_sx",
            "B_finite_K_sx": "-C_sx / Delta_sx",
            "C_finite_K_xx": "C_ss / Delta_sx",
            "finite_shell_difference": "(shell_mean - zero) / (p_hat_sq_shell - p_hat_sq_zero)",
            "strict_limit": (
                "These are finite inverse-correlator-block rows on the measured "
                "source/complement chart.  They are not strict Schur kernel rows "
                "at an isolated scalar pole and do not identify x with O_H."
            ),
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite inverse rows as strict neutral-kernel A/B/C pole rows",
            "does not treat finite shell differences as isolated-pole K'(pole)",
            "does not treat taste-radial x as canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use the complete finite packet only as staging support.  For closure, "
            "replace finite inverse rows with isolated-pole K'(pole)/A'B'C' "
            "authority or add canonical O_H/source-overlap or W/Z response authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
