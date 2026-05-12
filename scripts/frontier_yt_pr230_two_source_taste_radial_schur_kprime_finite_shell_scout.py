#!/usr/bin/env python3
"""
PR #230 two-source taste-radial finite-shell Schur K-prime scout.

The previous Schur-subblock witness proves that completed ready chunks contain
real finite same-ensemble rows for

    G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]].

This runner asks the next, narrower question: what finite-shell inverse-block
slope is visible if we invert that 2x2 correlator block and compare the zero
mode to the first nonzero momentum shell?  This is a scout only.  It is not an
isolated-pole K'(pole) row, not a finite-volume/IR theorem, not canonical O_H
authority, and not y_t closure.
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
    / "yt_pr230_two_source_taste_radial_schur_kprime_finite_shell_scout_2026-05-06.json"
)
MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
COMBINER = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"

PARENTS = {
    "two_source_schur_subblock_witness": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kernel_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
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


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


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


def manifest_rows_for_ready_chunks(manifest: dict[str, Any], combiner: dict[str, Any]) -> list[dict[str, Any]]:
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


def schur_rows_from_mode(mode: str, row: dict[str, Any]) -> dict[str, Any] | None:
    needed = ("p_hat_sq", "C_ss_real", "C_sx_real", "C_xx_real")
    if not all(finite(row.get(key)) for key in needed):
        return None
    p_hat_sq = float(row["p_hat_sq"])
    c_ss = float(row["C_ss_real"])
    c_sx = float(row["C_sx_real"])
    c_xx = float(row["C_xx_real"])
    delta = c_ss * c_xx - c_sx * c_sx
    if delta == 0.0 or c_ss == 0.0 or c_xx == 0.0:
        return None
    return {
        "mode": mode,
        "p_hat_sq": p_hat_sq,
        "C_ss": c_ss,
        "C_sx": c_sx,
        "C_xx": c_xx,
        "Delta_sx": delta,
        "C_source_given_x": delta / c_xx,
        "C_x_given_source": delta / c_ss,
        "K_source_given_x_preview": c_xx / delta,
        "K_x_given_source_preview": c_ss / delta,
        "rho_sx": c_sx / math.sqrt(c_ss * c_xx) if c_ss > 0.0 and c_xx > 0.0 else None,
        "strict_limit": (
            "Finite-shell inverse of the measured two-source correlator block. "
            "Not an isolated-pole K'(pole) Schur kernel row."
        ),
    }


def read_chunk(row: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    issues: list[str] = []
    output = ROOT / str(row.get("output", ""))
    if not output.exists():
        return None, [f"chunk{row.get('chunk_index')} output absent"]
    data = load_json(output)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    run_control = metadata.get("run_control") if isinstance(metadata.get("run_control"), dict) else {}
    ensemble = selected_ensemble(data)
    seed = ensemble.get("rng_seed_control") if isinstance(ensemble.get("rng_seed_control"), dict) else {}
    source = ensemble.get("source_higgs_cross_correlator_analysis")

    if metadata.get("phase") != "production":
        issues.append(f"chunk{row.get('chunk_index')} phase={metadata.get('phase')!r}")
    if run_control.get("seed") != row.get("seed"):
        issues.append(f"chunk{row.get('chunk_index')} seed mismatch")
    if seed.get("seed_control_version") != EXPECTED_SEED_CONTROL_VERSION:
        issues.append(f"chunk{row.get('chunk_index')} seed control mismatch")
    if ensemble.get("selected_mass_parameter") != 0.75:
        issues.append(f"chunk{row.get('chunk_index')} selected mass mismatch")
    if not isinstance(source, dict):
        issues.append(f"chunk{row.get('chunk_index')} source rows absent")
        return None, issues
    if source.get("canonical_higgs_operator_identity_passed") is not False:
        issues.append(f"chunk{row.get('chunk_index')} canonical O_H unexpectedly passed")
    if source.get("used_as_physical_yukawa_readout") is not False:
        issues.append(f"chunk{row.get('chunk_index')} source rows marked physical")
    aliases = source.get("two_source_taste_radial_row_aliases")
    if not isinstance(aliases, dict) or aliases.get("C_sx_aliases_C_sH_schema_field") is not True:
        issues.append(f"chunk{row.get('chunk_index')} C_sx alias missing")
    if not isinstance(aliases, dict) or aliases.get("C_xx_aliases_C_HH_schema_field") is not True:
        issues.append(f"chunk{row.get('chunk_index')} C_xx alias missing")

    mode_rows = source.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        issues.append(f"chunk{row.get('chunk_index')} mode set mismatch")
        return None, issues

    modes: dict[str, dict[str, Any]] = {}
    for mode, mode_row in sorted(mode_rows.items()):
        if not isinstance(mode_row, dict):
            issues.append(f"chunk{row.get('chunk_index')} {mode} row not object")
            continue
        parsed = schur_rows_from_mode(mode, mode_row)
        if parsed is None:
            issues.append(f"chunk{row.get('chunk_index')} {mode} invalid finite Schur row")
            continue
        modes[mode] = parsed

    zero = modes.get(ZERO_MODE)
    shell_modes = [mode for mode in sorted(modes) if mode != ZERO_MODE]
    if zero is None or set(shell_modes) != (EXPECTED_MODES - {ZERO_MODE}):
        issues.append(f"chunk{row.get('chunk_index')} zero/shell rows missing")
        return None, issues
    shell_p_values = [float(modes[mode]["p_hat_sq"]) for mode in shell_modes]
    shell_p_mean = statistics.fmean(shell_p_values)
    if not all(abs(value - shell_p_mean) <= 1.0e-12 for value in shell_p_values):
        issues.append(f"chunk{row.get('chunk_index')} shell p_hat_sq anisotropy")
    if shell_p_mean <= float(zero["p_hat_sq"]):
        issues.append(f"chunk{row.get('chunk_index')} shell p_hat_sq not above zero mode")
        return None, issues

    def mean_shell(key: str) -> float:
        return statistics.fmean(float(modes[mode][key]) for mode in shell_modes)

    dp = shell_p_mean - float(zero["p_hat_sq"])
    chunk_index = int(row["chunk_index"])
    return {
        "chunk_index": chunk_index,
        "seed": row.get("seed"),
        "zero_mode": zero,
        "shell_modes": {mode: modes[mode] for mode in shell_modes},
        "shell_p_hat_sq_mean": shell_p_mean,
        "shell_p_hat_sq_stdev": statistics.stdev(shell_p_values) if len(shell_p_values) > 1 else 0.0,
        "finite_difference": {
            "delta_p_hat_sq": dp,
            "K_source_given_x_shell_mean": mean_shell("K_source_given_x_preview"),
            "K_source_given_x_zero": float(zero["K_source_given_x_preview"]),
            "K_source_given_x_slope": (
                mean_shell("K_source_given_x_preview")
                - float(zero["K_source_given_x_preview"])
            )
            / dp,
            "C_source_given_x_shell_mean": mean_shell("C_source_given_x"),
            "C_source_given_x_zero": float(zero["C_source_given_x"]),
            "C_source_given_x_slope": (
                mean_shell("C_source_given_x") - float(zero["C_source_given_x"])
            )
            / dp,
            "K_x_given_source_shell_mean": mean_shell("K_x_given_source_preview"),
            "K_x_given_source_zero": float(zero["K_x_given_source_preview"]),
            "K_x_given_source_slope": (
                mean_shell("K_x_given_source_preview")
                - float(zero["K_x_given_source_preview"])
            )
            / dp,
            "rho_sx_shell_mean": mean_shell("rho_sx"),
            "rho_sx_zero": float(zero["rho_sx"]),
        },
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
        "K_source_given_x_slope",
        "C_source_given_x_slope",
        "K_x_given_source_slope",
        "K_source_given_x_zero",
        "K_source_given_x_shell_mean",
        "C_source_given_x_zero",
        "C_source_given_x_shell_mean",
        "rho_sx_zero",
        "rho_sx_shell_mean",
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
        "treated_finite_shell_slope_as_kprime_pole": False,
        "treated_taste_radial_x_as_canonical_O_H": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 finite-shell Schur K-prime scout")
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
    finite_slopes = all(
        finite(chunk.get("finite_difference", {}).get("K_source_given_x_slope"))
        and finite(chunk.get("finite_difference", {}).get("C_source_given_x_slope"))
        for chunk in chunks
    )
    shell_complete = (
        isinstance(ready_chunks, int)
        and len(chunks) == ready_chunks
        and all(set(chunk.get("shell_modes", {})) == (EXPECTED_MODES - {ZERO_MODE}) for chunk in chunks)
    )
    witness_loaded = (
        parents["two_source_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and parents["two_source_schur_subblock_witness"].get("proposal_allowed") is False
    )
    schur_support_loaded = (
        parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_schur_kernel_rows_present") is False
    )
    strict_contract_still_open = (
        parents["schur_kernel_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_kernel_contract"].get("candidate_rows_present") is False
    )
    schur_route_open = parents["schur_route_completion"].get("proposal_allowed") is False
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    packet_support_boundary = (
        isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and 0 < ready_chunks <= expected_chunks
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("schur-subblock-witness-loaded", witness_loaded, statuses["two_source_schur_subblock_witness"])
    report("schur-sufficiency-loaded", schur_support_loaded, statuses["schur_sufficiency"])
    report("ready-manifest-rows-found", len(ready_rows) == ready_chunks, f"rows={len(ready_rows)}")
    report("chunk-row-audits-clean", not chunk_issues, f"issues={chunk_issues[:5]}")
    report("zero-plus-first-shell-complete", shell_complete, f"chunks={len(chunks)} ready={ready_chunks}")
    report("finite-shell-schur-slopes-finite", finite_slopes, str(summary))
    report("finite-packet-boundary-preserved", packet_support_boundary, f"ready={ready_chunks}/{expected_chunks}")
    report("strict-schur-contract-still-open", strict_contract_still_open, statuses["schur_kernel_contract"])
    report("schur-route-still-open", schur_route_open, statuses["schur_route_completion"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", all(value is False for value in forbidden_firewall().values()), str(forbidden_firewall()))

    passed = (
        not missing
        and not proposals
        and witness_loaded
        and schur_support_loaded
        and len(ready_rows) == ready_chunks
        and not chunk_issues
        and shell_complete
        and finite_slopes
        and packet_support_boundary
        and strict_contract_still_open
        and schur_route_open
        and retained_open
        and campaign_open
        and all(value is False for value in forbidden_firewall().values())
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / finite-shell Schur inverse-slope scout from "
            "two-source taste-radial rows; strict K-prime pole authority absent"
        ),
        "conditional_surface_status": (
            "conditional-support for Schur K-prime work only after complete "
            "63/63 rows, pole-location/derivative extraction, FV/IR limiting "
            "authority, and canonical O_H/source-overlap or physical-response "
            "authority are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The scout computes finite-shell inverse-block slopes from the "
            "measured two-source correlator subblock.  A zero-to-first-shell "
            "finite difference is not an isolated-pole K'(pole) derivative, "
            "not a strict Schur A/B/C row packet, not FV/IR authority, and not "
            "canonical O_H or kappa_s authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "finite_shell_schur_kprime_scout_passed": passed,
        "strict_schur_kprime_authority_passed": False,
        "strict_schur_kernel_rows_written": False,
        "pole_location_or_derivative_rows_present": False,
        "fv_ir_zero_mode_authority_present": False,
        "canonical_higgs_operator_identity_passed": False,
        "used_as_physical_yukawa_readout": False,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "ready_chunk_indices": combiner.get("ready_chunk_indices"),
        "chunk_finite_shell_rows": chunks,
        "finite_shell_summary": summary,
        "row_definition": {
            "G": "[[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]",
            "Delta_sx": "C_ss*C_xx - C_sx^2",
            "K_source_given_x_preview": "C_xx / Delta_sx",
            "finite_shell_slope": "(K_shell_mean - K_zero) / (p_hat_sq_shell - p_hat_sq_zero)",
            "strict_limit": (
                "This is an inverse finite-correlator-block slope between two "
                "available lattice momentum shells.  It is not K'(pole), not "
                "a pole residue, and not a continuum/FV/IR limiting theorem."
            ),
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite-shell slopes as isolated-pole K'(pole)",
            "does not write strict Schur A/B/C kernel rows",
            "does not treat taste-radial x as canonical O_H",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use the complete finite packet only as staging support.  For closure, "
            "replace the scout with a pole extraction/FV-IR theorem "
            "for K'(pole), or supply canonical O_H/source-overlap or W/Z "
            "physical-response authority."
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
