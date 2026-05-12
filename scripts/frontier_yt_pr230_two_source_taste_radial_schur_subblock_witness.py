#!/usr/bin/env python3
"""
PR #230 two-source taste-radial Schur-subblock witness.

The strict Schur K'(pole) route still needs kernel rows A, B, C and their pole
derivatives.  The completed two-source taste-radial chunks do, however, supply
real same-ensemble finite-mode rows for a certified source/complement pair:

    G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]].

This runner packages that object as bounded Schur-subblock support.  It is not
the strict Schur kernel-row contract, not pole/LSZ authority, and not canonical
O_H or y_t closure.
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
    / "yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json"
)

MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
COMBINER = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"

PARENTS = {
    "two_source_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kernel_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_abc_definition": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "1,0,0", "0,1,0", "0,0,1"}
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


def read_chunk_observations(row: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    output = ROOT / str(row.get("output", ""))
    if not output.exists():
        return [], [f"chunk{row.get('chunk_index')} output absent"]
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
        issues.append(f"chunk{row.get('chunk_index')} source_higgs analysis absent")
        return [], issues
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
        return [], issues

    observations: list[dict[str, Any]] = []
    for mode, mode_row in sorted(mode_rows.items()):
        if not isinstance(mode_row, dict):
            issues.append(f"chunk{row.get('chunk_index')} {mode} row not object")
            continue
        needed = ("C_ss_real", "C_sx_real", "C_xx_real")
        if not all(finite(mode_row.get(key)) for key in needed):
            issues.append(f"chunk{row.get('chunk_index')} {mode} missing finite C_ss/C_sx/C_xx")
            continue
        c_ss = float(mode_row["C_ss_real"])
        c_sx = float(mode_row["C_sx_real"])
        c_xx = float(mode_row["C_xx_real"])
        det = c_ss * c_xx - c_sx * c_sx
        rho = c_sx / math.sqrt(c_ss * c_xx) if c_ss > 0.0 and c_xx > 0.0 else float("nan")
        schur_source_given_x = det / c_xx if c_xx != 0.0 else float("nan")
        schur_x_given_source = det / c_ss if c_ss != 0.0 else float("nan")
        inverse_preview = {
            "K_ss_preview": c_xx / det if det != 0.0 else None,
            "K_sx_preview": -c_sx / det if det != 0.0 else None,
            "K_xx_preview": c_ss / det if det != 0.0 else None,
            "strict_limit": (
                "Inverse of the finite two-source correlator subblock only. "
                "This is not the strict Schur K'(pole) kernel row contract."
            ),
        }
        observations.append(
            {
                "chunk_index": int(row["chunk_index"]),
                "seed": row.get("seed"),
                "mode": mode,
                "A_corr_C_ss": c_ss,
                "B_corr_C_sx": c_sx,
                "C_corr_C_xx": c_xx,
                "gram_determinant": det,
                "rho_sx": rho,
                "corr_schur_source_given_x": schur_source_given_x,
                "corr_schur_x_given_source": schur_x_given_source,
                "inverse_kernel_preview": inverse_preview,
                "configuration_count": mode_row.get("configuration_count"),
            }
        )
    return observations, issues


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


def per_mode_summary(observations: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {mode: [] for mode in sorted(EXPECTED_MODES)}
    for row in observations:
        grouped.setdefault(str(row.get("mode")), []).append(row)
    output: dict[str, Any] = {}
    numeric_keys = (
        "A_corr_C_ss",
        "B_corr_C_sx",
        "C_corr_C_xx",
        "gram_determinant",
        "rho_sx",
        "corr_schur_source_given_x",
        "corr_schur_x_given_source",
    )
    for mode, rows in sorted(grouped.items()):
        output[mode] = {
            key: summarize([float(row[key]) for row in rows if finite(row.get(key))])
            for key in numeric_keys
        }
        output[mode]["positive_gram_determinant_all_ready_rows"] = all(
            finite(row.get("gram_determinant")) and float(row["gram_determinant"]) > 0.0
            for row in rows
        )
        output[mode]["row_count"] = len(rows)
    return output


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
        "treated_partial_rows_as_pole_or_fv_ir_authority": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 two-source taste-radial Schur-subblock witness")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    ready_manifest_rows = manifest_rows_for_ready_chunks(manifest, combiner)

    observations: list[dict[str, Any]] = []
    chunk_issues: list[str] = []
    for row in ready_manifest_rows:
        rows, issues = read_chunk_observations(row)
        observations.extend(rows)
        chunk_issues.extend(issues)

    summary = per_mode_summary(observations)
    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")
    all_mode_counts_ok = all(
        summary.get(mode, {}).get("row_count") == ready_chunks for mode in EXPECTED_MODES
    )
    all_dets_positive = all(
        row.get("positive_gram_determinant_all_ready_rows") is True
        for row in summary.values()
    )
    chart_support = (
        parents["two_source_chart"].get("two_source_taste_radial_chart_support_passed") is True
        and parents["two_source_chart"].get("proposal_allowed") is False
    )
    action_support = (
        parents["two_source_action"].get("two_source_taste_radial_action_passed") is True
        and parents["two_source_action"].get("canonical_higgs_operator_identity_passed") is False
        and parents["two_source_action"].get("proposal_allowed") is False
    )
    row_contract_support = (
        parents["two_source_row_contract"].get("two_source_taste_radial_row_contract_passed") is True
        and parents["two_source_row_contract"].get("proposal_allowed") is False
    )
    combiner_support = (
        isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and (
            (
                parents["two_source_combiner"].get("combined_rows_written") is False
                and 0 < ready_chunks < expected_chunks
            )
            or (
                parents["two_source_combiner"].get("combined_rows_written") is True
                and ready_chunks == expected_chunks == 63
            )
        )
        and parents["two_source_combiner"].get("proposal_allowed") is False
    )
    schur_contract_still_strictly_open = (
        parents["schur_kernel_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and parents["schur_kernel_contract"].get("candidate_rows_present") is False
    )
    schur_sufficiency_loaded = (
        parents["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and parents["schur_sufficiency"].get("current_schur_kernel_rows_present") is False
    )
    schur_route_still_open = parents["schur_route_completion"].get("proposal_allowed") is False
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("two-source-chart-support-loaded", chart_support, statuses["two_source_chart"])
    report("two-source-action-support-loaded", action_support, statuses["two_source_action"])
    report("two-source-row-contract-loaded", row_contract_support, statuses["two_source_row_contract"])
    report("combiner-support-loaded", combiner_support, f"ready={ready_chunks}/{expected_chunks}")
    report("ready-manifest-rows-found", len(ready_manifest_rows) == ready_chunks, f"rows={len(ready_manifest_rows)}")
    report("chunk-row-audits-clean", not chunk_issues, f"issues={chunk_issues[:5]}")
    report("all-ready-mode-counts-present", all_mode_counts_ok, f"modes={summary}")
    report("finite-schur-subblock-determinants-positive", all_dets_positive, "det(C_ss C_xx - C_sx^2) > 0")
    report("schur-sufficiency-loaded", schur_sufficiency_loaded, statuses["schur_sufficiency"])
    report("strict-schur-kernel-contract-still-open", schur_contract_still_strictly_open, statuses["schur_kernel_contract"])
    report("schur-route-still-open", schur_route_still_open, statuses["schur_route_completion"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", all(value is False for value in forbidden_firewall().values()), str(forbidden_firewall()))

    passed = (
        not missing
        and not proposals
        and chart_support
        and action_support
        and row_contract_support
        and combiner_support
        and len(ready_manifest_rows) == ready_chunks
        and not chunk_issues
        and all_mode_counts_ok
        and all_dets_positive
        and schur_sufficiency_loaded
        and schur_contract_still_strictly_open
        and schur_route_still_open
        and retained_open
        and campaign_open
        and all(value is False for value in forbidden_firewall().values())
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial Schur-subblock witness; "
            "strict Schur K-prime pole rows and canonical O_H authority absent"
        ),
        "conditional_surface_status": (
            "conditional-support for the Schur route after a complete 63/63 row "
            "packet, pole/derivative/FV/IR authority, and a canonical O_H/source-overlap "
            "or physical-response bridge are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This witness supplies finite two-source C_ss/C_sx/C_xx subblocks for "
            "the certified taste-radial complement x only.  It does not provide "
            "K'(pole), A/B/C pole derivatives, canonical O_H identity, kappa_s, "
            "or retained-route authorization."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "two_source_taste_radial_schur_subblock_witness_passed": passed,
        "same_surface_source_complement_partition_supported": chart_support and action_support,
        "finite_correlator_subblock_rows_present": len(observations) > 0,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "ready_chunk_indices": combiner.get("ready_chunk_indices"),
        "mode_count": len(EXPECTED_MODES),
        "observation_count": len(observations),
        "partial_mode_schur_summary": summary,
        "row_definition": {
            "A_corr": "C_ss(q), finite correlator row for the uniform scalar source s",
            "B_corr": "C_sx(q), finite correlator cross row between s and taste-radial source x",
            "C_corr": "C_xx(q), finite correlator row for taste-radial source x",
            "gram_determinant": "A_corr*C_corr - B_corr^2",
            "corr_schur_source_given_x": "gram_determinant / C_corr",
            "strict_limit": (
                "These are correlator subblocks for a certified two-source chart. "
                "They are not the strict Schur kernel rows A(pole), B(pole), C(pole) "
                "and derivatives required by the K-prime sufficiency theorem."
            ),
        },
        "strict_schur_kernel_row_contract_passed": False,
        "strict_schur_kernel_rows_written": False,
        "pole_derivative_rows_present": False,
        "isolated_pole_fv_ir_authority_present": False,
        "canonical_higgs_operator_identity_passed": False,
        "used_as_physical_yukawa_readout": False,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat taste-radial x as canonical O_H",
            "does not treat finite C_sx/C_xx rows as canonical C_sH/C_HH rows",
            "does not treat finite correlator subblocks as K'(pole) Schur kernel rows",
            "does not set kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use the complete finite packet only as staging support.  For closure, "
            "fit a real pole/derivative Schur kernel packet for the source/complement block or supply canonical "
            "O_H/source-overlap or W/Z physical-response authority."
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
