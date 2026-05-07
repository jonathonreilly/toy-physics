#!/usr/bin/env python3
"""
PR #230 source-Higgs pole-row acceptance contract.

This runner defines the strict landing pad for a future positive O_H/C_sH/C_HH
bridge.  It passes as a contract while the row file is absent, but it refuses to
turn absent, aliased, or source-only rows into closure evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROWS = ROOT / "outputs" / "yt_pr230_source_higgs_pole_rows_2026-05-06.json"
LEGACY_ROWS = ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json"
)

PARENTS = {
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "post_fms_source_overlap_necessity": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "two_source_chunk_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FLAGS = {
    "used_hunit_matrix_element_readout",
    "used_hunit_to_top_matrix_element",
    "used_yt_ward_identity",
    "used_observed_top_or_yukawa_selector",
    "used_alpha_lm",
    "used_plaquette_or_u0",
    "set_kappa_s_equal_one",
    "set_c2_equal_one",
    "set_z_match_equal_one",
    "defined_y_t_bare",
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


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def rows_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("pole_rows", payload.get("rows", []))
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    if isinstance(rows, dict):
        return [row for row in rows.values() if isinstance(row, dict)]
    return []


def uncertainty_ok(row: dict[str, Any], key: str) -> bool:
    return finite(row.get(key)) and (
        finite(row.get(f"{key}_err"))
        or finite(row.get(f"{key}_uncertainty"))
        or finite(row.get(f"sigma_{key}"))
    )


def validate_rows(payload: dict[str, Any]) -> dict[str, Any]:
    rows = rows_from_payload(payload)
    forbidden_flags = payload.get("forbidden_firewall", {})
    if not isinstance(forbidden_flags, dict):
        forbidden_flags = {}
    row_violations: list[dict[str, Any]] = []
    ensemble_ids = set()
    for index, row in enumerate(rows):
        ensemble_id = row.get("ensemble_id")
        if ensemble_id is not None:
            ensemble_ids.add(str(ensemble_id))
        labels = set(row.get("correlator_labels", [])) if isinstance(row.get("correlator_labels"), list) else set()
        has_alias = bool(
            row.get("C_sx_aliases_C_sH_schema_field")
            or row.get("C_xx_aliases_C_HH_schema_field")
            or "C_sx" in labels
            or "C_xx" in labels
        )
        required = {
            "Res_C_ss": uncertainty_ok(row, "Res_C_ss"),
            "Res_C_sH": uncertainty_ok(row, "Res_C_sH"),
            "Res_C_HH": uncertainty_ok(row, "Res_C_HH"),
            "gram_determinant": uncertainty_ok(row, "gram_determinant")
            or finite(row.get("gram_determinant_zscore")),
            "scalar_lsz": row.get("scalar_lsz_certificate_passed") is True,
            "isolated_pole": row.get("isolated_pole_certificate_passed") is True,
            "fv_ir": row.get("finite_volume_ir_certificate_passed") is True,
            "same_ensemble": ensemble_id is not None,
            "not_alias": not has_alias,
        }
        if not all(required.values()):
            row_violations.append(
                {
                    "row_index": index,
                    "failed_requirements": [key for key, ok in required.items() if not ok],
                    "labels": sorted(labels),
                    "ensemble_id": ensemble_id,
                }
            )
    forbidden_used = sorted(
        flag for flag in FORBIDDEN_FLAGS if forbidden_flags.get(flag) is True
    )
    all_same_ensemble = len(ensemble_ids) == 1 if rows else False
    return {
        "row_count": len(rows),
        "all_same_ensemble": all_same_ensemble,
        "forbidden_used": forbidden_used,
        "row_violations": row_violations,
        "rows_acceptance_passed": bool(rows)
        and all_same_ensemble
        and not forbidden_used
        and not row_violations,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", default=str(DEFAULT_ROWS), help="Future strict pole-row JSON.")
    parser.add_argument("--output", default=str(OUTPUT), help="Contract output JSON.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    rows_path = Path(args.rows)
    output_path = Path(args.output)
    print("PR #230 source-Higgs pole-row acceptance contract")
    print("=" * 78)

    certs = {name: load(ROOT / rel_path) for name, rel_path in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    payload = load(rows_path)
    legacy_payload = load(LEGACY_ROWS)
    rows_present = bool(payload)
    legacy_rows_present = bool(legacy_payload)
    validation = validate_rows(payload) if rows_present else {
        "row_count": 0,
        "all_same_ensemble": False,
        "forbidden_used": [],
        "row_violations": [],
        "rows_acceptance_passed": False,
    }

    canonical_oh_passed = (
        certs["canonical_higgs_gate"].get("candidate_present") is True
        and certs["canonical_higgs_gate"].get("candidate_valid") is True
    )
    parent_rows_absent = (
        certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_postprocess"].get("candidate_present") is False
    )
    post_fms_blocks_current_inference = (
        certs["post_fms_source_overlap_necessity"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and certs["post_fms_source_overlap_necessity"].get(
            "current_source_overlap_authority_present"
        )
        is False
    )
    chunk_package_support_only = (
        certs["two_source_chunk_package"].get("chunk_package_audit_passed") is True
        and certs["two_source_chunk_package"].get("proposal_allowed") is False
        and certs["two_source_chunk_package"].get("active_chunks_counted_as_evidence")
        is False
    )
    closure_contract_satisfied = (
        rows_present
        and canonical_oh_passed
        and validation["rows_acceptance_passed"]
        and certs["source_higgs_gram"].get("source_higgs_gram_purity_gate_passed") is True
        and certs["retained_route"].get("proposal_allowed") is True
        and certs["campaign_status"].get("proposal_allowed") is True
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("strict-row-file-status-recorded", True, f"rows_present={rows_present} path={rel(rows_path)}")
    report("legacy-row-file-status-recorded", True, f"legacy_rows_present={legacy_rows_present} path={rel(LEGACY_ROWS)}")
    report("current-source-higgs-rows-absent-in-parents", parent_rows_absent, "builder/postprocess remain absent")
    report("post-fms-gate-blocks-current-source-overlap-inference", post_fms_blocks_current_inference, "Res C_sH not determined")
    report("chunk-package-is-support-only", chunk_package_support_only, "C_sx/C_xx rows not C_sH/C_HH pole rows")
    report("canonical-oh-not-yet-accepted", canonical_oh_passed is False, str(certs["canonical_higgs_gate"].get("actual_current_surface_status")))
    report("strict-rows-not-yet-accepted", validation["rows_acceptance_passed"] is False, str(validation))
    report("closure-contract-not-satisfied-on-current-surface", closure_contract_satisfied is False, "remaining bridge is explicit")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "open / source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract; "
            "strict rows absent on current surface"
        ),
        "conditional_surface_status": (
            "exact-support if a future same-surface row certificate satisfies this "
            "contract and the retained-route/campaign gates subsequently allow proposal wording"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This is a strict input contract, not evidence.  Current artifacts do "
            "not contain accepted canonical O_H authority or same-ensemble "
            "C_ss/C_sH/C_HH pole rows with Gram/FV/IR/scalar-LSZ checks."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "source_higgs_pole_row_acceptance_contract_passed": passed,
        "closure_contract_satisfied": closure_contract_satisfied,
        "rows_path": rel(rows_path),
        "rows_present": rows_present,
        "legacy_rows_path": rel(LEGACY_ROWS),
        "legacy_rows_present": legacy_rows_present,
        "canonical_oh_passed": canonical_oh_passed,
        "validation": validation,
        "parent_certificates": PARENTS,
        "parent_statuses": {
            name: cert.get("actual_current_surface_status") for name, cert in certs.items()
        },
        "remaining_positive_contract": [
            "same-surface canonical O_H identity and normalization certificate",
            "same-ensemble pole rows containing Res_C_ss, Res_C_sH, Res_C_HH with uncertainties",
            "no C_sx/C_xx aliasing in the accepted row labels",
            "Gram purity/positivity certificate with uncertainty control",
            "isolated scalar pole, FV/IR, and scalar-LSZ/model-class certificates",
            "forbidden-input firewall: no H_unit, yt_ward, observed selector, alpha_LM, plaquette/u0, kappa_s=1, c2=1, or Z_match=1",
            "rerun full assembly, retained-route, campaign status, and audit pipeline after rows land",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not fabricate C_sH/C_HH pole rows",
            "does not treat C_sx/C_xx aliases as canonical O_H correlators",
            "does not infer source-Higgs overlap from source-only rows or FMS expansion",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(output_path)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
