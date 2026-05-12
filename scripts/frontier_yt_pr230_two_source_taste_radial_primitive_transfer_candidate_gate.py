#!/usr/bin/env python3
"""
PR #230 two-source taste-radial primitive-transfer candidate gate.

The ready C_sx/C_xx chunks provide a real same-ensemble finite source/
complement correlator block.  This runner asks whether that new finite
off-diagonal row can be promoted to the missing H3 physical neutral transfer
or off-diagonal generator required by the same-surface neutral
multiplicity-one route.

It cannot on the current surface.  The finite C_sx row is a correlator
covariance/overlap diagnostic for the taste-radial second source, not a
same-surface transfer/action matrix, primitive cone certificate, isolated-pole
kernel row, or canonical O_H/source-overlap row.
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
    / "yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json"
)

MANIFEST = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
COMBINER = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json"

PARENTS = {
    "two_source_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "schur_subblock": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
    "finite_schur_abc": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
    "finite_to_pole_lift": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "same_surface_neutral_multiplicity_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "same_surface_neutral_multiplicity_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "z3_positive_cone_support": "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json",
    "z3_triplet_conditional_primitive": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_MODES = {"0,0,0", "0,0,1", "0,1,0", "1,0,0"}

FORBIDDEN_FIREWALL = {
    "uses_H_unit": False,
    "uses_yt_ward_identity": False,
    "uses_observed_targets": False,
    "uses_alpha_lm_plaquette_u0": False,
    "uses_reduced_pilot_evidence": False,
    "sets_c2_zmatch_kappas_to_one_by_convention": False,
    "uses_pslq_or_value_recognition_selector": False,
    "takes_absolute_value_to_force_positive_transfer": False,
    "treats_finite_correlator_as_transfer_action": False,
    "treats_taste_radial_x_as_canonical_O_H": False,
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


def ready_manifest_rows(manifest: dict[str, Any], combiner: dict[str, Any]) -> list[dict[str, Any]]:
    rows = manifest.get("chunk_commands")
    ready = combiner.get("ready_chunk_indices")
    if not isinstance(rows, list) or not isinstance(ready, list):
        return []
    ready_indices = {int(index) for index in ready if isinstance(index, int)}
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("chunk_index"), int)
        and int(row["chunk_index"]) in ready_indices
    ]


def chunk_mode_rows(manifest_row: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    output = ROOT / str(manifest_row.get("output", ""))
    if not output.exists():
        return [], [f"chunk{manifest_row.get('chunk_index')} output absent"]
    data = load_json(output)
    ensemble = selected_ensemble(data)
    source = ensemble.get("source_higgs_cross_correlator_analysis")
    if not isinstance(source, dict):
        return [], [f"chunk{manifest_row.get('chunk_index')} source_higgs analysis absent"]
    mode_rows = source.get("mode_rows")
    if not isinstance(mode_rows, dict) or set(mode_rows) != EXPECTED_MODES:
        return [], [f"chunk{manifest_row.get('chunk_index')} mode set mismatch"]
    rows: list[dict[str, Any]] = []
    issues: list[str] = []
    for mode, row in sorted(mode_rows.items()):
        if not isinstance(row, dict):
            issues.append(f"chunk{manifest_row.get('chunk_index')} {mode} row not object")
            continue
        if not all(finite(row.get(key)) for key in ("C_ss_real", "C_sx_real", "C_xx_real")):
            issues.append(f"chunk{manifest_row.get('chunk_index')} {mode} missing finite C rows")
            continue
        c_ss = float(row["C_ss_real"])
        c_sx = float(row["C_sx_real"])
        c_xx = float(row["C_xx_real"])
        determinant = c_ss * c_xx - c_sx * c_sx
        rows.append(
            {
                "chunk_index": int(manifest_row["chunk_index"]),
                "mode": mode,
                "C_ss_real": c_ss,
                "C_sx_real": c_sx,
                "C_xx_real": c_xx,
                "gram_determinant": determinant,
                "rho_sx": c_sx / math.sqrt(c_ss * c_xx)
                if c_ss > 0.0 and c_xx > 0.0
                else None,
                "offdiagonal_nonzero": abs(c_sx) > 1.0e-14,
                "positive_correlator_block": c_ss > 0.0 and c_xx > 0.0 and determinant > 0.0,
            }
        )
    return rows, issues


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


def mode_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for mode in sorted(EXPECTED_MODES):
        mode_rows = [row for row in rows if row.get("mode") == mode]
        c_sx = [float(row["C_sx_real"]) for row in mode_rows if finite(row.get("C_sx_real"))]
        positive = sum(1 for value in c_sx if value > 0.0)
        negative = sum(1 for value in c_sx if value < 0.0)
        zero = sum(1 for value in c_sx if value == 0.0)
        summary[mode] = {
            "row_count": len(mode_rows),
            "C_sx_real": summarize(c_sx),
            "rho_sx": summarize(
                [float(row["rho_sx"]) for row in mode_rows if finite(row.get("rho_sx"))]
            ),
            "gram_determinant": summarize(
                [
                    float(row["gram_determinant"])
                    for row in mode_rows
                    if finite(row.get("gram_determinant"))
                ]
            ),
            "C_sx_sign_counts": {"positive": positive, "negative": negative, "zero": zero},
            "all_blocks_positive_definite": all(
                row.get("positive_correlator_block") is True for row in mode_rows
            ),
            "offdiagonal_entry_observed": any(
                row.get("offdiagonal_nonzero") is True for row in mode_rows
            ),
            "strict_transfer_obstruction": (
                "C_sx is a finite correlator/covariance entry.  Mixed signs or "
                "near-zero means cannot be converted into a positive primitive "
                "transfer by absolute values or stochastic normalization without "
                "an additional same-surface action/transfer theorem."
            ),
        }
    return summary


def main() -> int:
    print("PR #230 two-source taste-radial primitive-transfer candidate gate")
    print("=" * 78)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    manifest = load_json(MANIFEST)
    combiner = load_json(COMBINER)
    ready_rows = ready_manifest_rows(manifest, combiner)
    observations: list[dict[str, Any]] = []
    issues: list[str] = []
    for row in ready_rows:
        chunk_rows, chunk_issues = chunk_mode_rows(row)
        observations.extend(chunk_rows)
        issues.extend(chunk_issues)
    summary = mode_summary(observations)

    ready_count = combiner.get("ready_chunks")
    expected_count = combiner.get("expected_chunks")
    finite_offdiagonal_observed = any(
        row.get("offdiagonal_nonzero") is True for row in observations
    )
    all_blocks_positive = all(
        row.get("positive_correlator_block") is True for row in observations
    )
    finite_packet_support_boundary = (
        isinstance(ready_count, int)
        and isinstance(expected_count, int)
        and 0 < ready_count <= expected_count
    )
    candidate_rejected = (
        parents["same_surface_neutral_multiplicity_candidate"].get("candidate_accepted")
        is False
        and parents["same_surface_neutral_multiplicity_candidate"].get("proposal_allowed")
        is False
    )
    primitive_route_still_missing_h3 = (
        parents["neutral_primitive_route_completion"].get("proposal_allowed") is False
        and "H3" in str(parents["neutral_primitive_route_completion"])
    )
    pole_lift_blocks_derivative = (
        "finite Schur A/B/C rows do not lift" in statuses["finite_to_pole_lift"]
        and parents["finite_to_pole_lift"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    physical_transfer_candidate_accepted = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("ready-packet-loaded", len(ready_rows) == ready_count, f"ready={len(ready_rows)}/{expected_count}")
    report("chunk-row-audits-clean", not issues, f"issues={issues[:4]}")
    report("finite-offdiagonal-csx-observed", finite_offdiagonal_observed, "finite C_sx rows exist")
    report("finite-correlator-blocks-positive", all_blocks_positive, "C_ss*C_xx-C_sx^2 > 0 on ready rows")
    report("finite-row-packet-support-only", finite_packet_support_boundary, f"ready={ready_count}/{expected_count}")
    report("same-surface-candidate-still-rejected", candidate_rejected, statuses["same_surface_neutral_multiplicity_candidate"])
    report("neutral-primitive-route-still-missing-h3", primitive_route_still_missing_h3, statuses["neutral_primitive_route_completion"])
    report("finite-to-pole-lift-blocks-transfer-promotion", pole_lift_blocks_derivative, statuses["finite_to_pole_lift"])
    report("no-positive-transfer-action-row-written", True, "finite correlator rows are not action/transfer rows")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("physical-transfer-candidate-not-accepted", not physical_transfer_candidate_accepted, "H3 remains absent")

    result = {
        "actual_current_surface_status": (
            "bounded support plus exact boundary / two-source taste-radial finite "
            "C_sx rows do not certify a physical primitive neutral transfer"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface action/transfer theorem "
            "or direct neutral transfer row converts the measured source/complement "
            "block into a positive primitive neutral transfer with pole/FV/IR and "
            "source/canonical-Higgs coupling authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The finite C_sx rows are real same-ensemble off-diagonal correlator "
            "entries, but they are not a transfer/action matrix, positive primitive "
            "cone certificate, isolated-pole kernel derivative, canonical O_H row, "
            "or kappa_s authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "physical_transfer_candidate_accepted": physical_transfer_candidate_accepted,
        "finite_offdiagonal_correlation_support": finite_offdiagonal_observed,
        "finite_correlator_blocks_positive": all_blocks_positive,
        "ready_chunks": ready_count,
        "expected_chunks": expected_count,
        "combined_rows_written": combiner.get("combined_rows_written"),
        "mode_summary": summary,
        "primitive_transfer_obligations": [
            {
                "id": "same_surface_transfer_or_action_row",
                "current_satisfied": False,
                "reason": "ready rows are correlator entries, not transfer/action dynamics",
            },
            {
                "id": "positive_cone_orientation_without_absolute_value",
                "current_satisfied": False,
                "reason": "positive transfer cannot be created by taking |C_sx| or stochasticizing finite covariance rows",
            },
            {
                "id": "primitive_power_or_irreducible_generator",
                "current_satisfied": False,
                "reason": "no transfer matrix or off-diagonal generator is derived",
            },
            {
                "id": "pole_fv_ir_transfer_limit",
                "current_satisfied": False,
                "reason": "finite-to-pole lift gate blocks endpoint/secant promotion",
            },
            {
                "id": "source_canonical_higgs_coupling",
                "current_satisfied": False,
                "reason": "taste-radial x is not canonical O_H and C_spH/C_HH rows are absent",
            },
        ],
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not treat finite C_sx/C_xx rows as canonical C_sH/C_HH rows",
            "does not treat finite correlator covariance as a transfer/action matrix",
            "does not use absolute values or stochastic normalization to create a positive transfer",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
        ],
        "exact_next_action": (
            "Supply a same-surface physical neutral transfer/action row or "
            "off-diagonal generator theorem, or a model-class/pole/FV/IR theorem "
            "that converts the measured C_ss/C_sx/C_xx block into a primitive "
            "neutral transfer and couples it to canonical O_H."
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
