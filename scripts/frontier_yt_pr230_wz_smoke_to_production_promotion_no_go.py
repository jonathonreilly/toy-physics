#!/usr/bin/env python3
"""
PR #230 W/Z smoke-to-production promotion no-go.

The new W/Z harness smoke path is useful only as schema plumbing.  This runner
checks whether the smoke artifact can honestly be promoted into the strict
production W/Z mass-response surface needed by the W/Z bypass route.  It must
fail that promotion unless a genuine same-source EW action, production W/Z
mass-fit rows, matched top/W covariance, non-observed g2 certificate, and
identity certificates are present.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json"
SMOKE_GATE = ROOT / "outputs" / "yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json"
SMOKE_ARTIFACT = ROOT / "outputs" / "yt_pr230_wz_harness_smoke_schema_smoke_2026-05-05.json"

PARENTS = {
    "wz_harness_smoke_schema": "outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json",
    "wz_response_harness_implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
    "wz_same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def smoke_wz_analysis(artifact: dict[str, Any]) -> dict[str, Any]:
    ensembles = artifact.get("ensembles", [])
    if not isinstance(ensembles, list) or not ensembles:
        return {}
    ensemble = ensembles[0]
    if not isinstance(ensemble, dict):
        return {}
    analysis = ensemble.get("wz_mass_response_analysis", {})
    return analysis if isinstance(analysis, dict) else {}


def row_sources(analysis: dict[str, Any]) -> set[str]:
    rows = analysis.get("per_source_shift_rows", [])
    sources: set[str] = set()
    if not isinstance(rows, list):
        return sources
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key in ("w_mass_fit", "z_mass_fit"):
            fit = row.get(key)
            if isinstance(fit, dict) and isinstance(fit.get("correlator_source"), str):
                sources.add(fit["correlator_source"])
    return sources


def promotion_blockers(analysis: dict[str, Any], metadata: dict[str, Any]) -> dict[str, bool]:
    identities = analysis.get("identity_certificates", {})
    gauge_response = analysis.get("gauge_response", {})
    ew = analysis.get("electroweak_coupling", {})
    wz_meta = metadata.get("wz_mass_response", {}) if isinstance(metadata, dict) else {}
    sources = row_sources(analysis)
    return {
        "analysis_phase_is_scout": analysis.get("phase") == "scout",
        "metadata_says_not_ew_production": wz_meta.get("implementation_status")
        == "smoke_schema_enabled_not_ew_production",
        "production_rows_not_written": wz_meta.get("production_wz_rows_written") is False,
        "rows_marked_synthetic": sources == {"synthetic_scout_contract_not_EW_field"},
        "same_source_identity_not_certified": analysis.get("same_source_identity_certified") is False,
        "sector_identity_false": isinstance(identities, dict)
        and identities.get("same_source_sector_overlap_identity_passed") is False,
        "canonical_higgs_identity_false": isinstance(identities, dict)
        and identities.get("canonical_higgs_pole_identity_passed") is False,
        "retained_route_gate_false": isinstance(identities, dict)
        and identities.get("retained_route_or_proposal_gate_passed") is False,
        "covariance_absent": isinstance(gauge_response, dict)
        and gauge_response.get("covariance_status") == "absent_in_smoke_schema",
        "g2_absent": isinstance(ew, dict)
        and ew.get("g2") is None
        and ew.get("used_observed_g2_as_selector") is False,
        "smoke_not_yukawa_readout": analysis.get("used_as_physical_yukawa_readout") is False,
    }


def main() -> int:
    print("PR #230 W/Z smoke-to-production promotion no-go")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}

    smoke_gate = load_json(SMOKE_GATE)
    smoke_artifact = load_json(SMOKE_ARTIFACT)
    metadata = smoke_artifact.get("metadata", {}) if isinstance(smoke_artifact, dict) else {}
    analysis = smoke_wz_analysis(smoke_artifact)
    blockers = promotion_blockers(analysis, metadata)

    strict_wz_rows_absent = (
        parents["wz_mass_fit_response_row_builder"].get("strict_wz_mass_fit_response_row_builder_passed")
        is False
        and parents["wz_mass_fit_response_row_builder"].get("measurement_rows_written") is False
    )
    matched_covariance_absent = (
        parents["top_wz_matched_covariance_builder"].get("strict_top_wz_matched_covariance_builder_passed")
        is False
        and parents["top_wz_matched_covariance_builder"].get("covariance_certificate_written") is False
    )
    same_source_ew_action_absent = (
        parents["wz_same_source_ew_action_builder"].get("same_source_ew_action_certificate_valid") is False
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    wz_path_absent = (
        parents["wz_correlator_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
        and parents["wz_correlator_mass_fit_path_gate"].get("future_mass_fit_rows_present") is False
    )
    same_source_wz_gate_open = (
        parents["same_source_wz_response_gate"].get("same_source_wz_response_certificate_gate_passed")
        is False
    )
    aggregate_proposal_denied = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    all_smoke_blockers_present = bool(blockers) and all(blockers.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("smoke-gate-passed", smoke_gate.get("wz_harness_smoke_schema_gate_passed") is True, display(SMOKE_GATE))
    report("smoke-artifact-loaded", bool(analysis), display(SMOKE_ARTIFACT))
    for key, ok in blockers.items():
        report(key.replace("_", "-"), ok, str(ok))
    report("same-source-ew-action-absent", same_source_ew_action_absent, statuses["wz_same_source_ew_action_builder"])
    report("wz-correlator-mass-fit-path-absent", wz_path_absent, statuses["wz_correlator_mass_fit_path_gate"])
    report("strict-wz-response-rows-absent", strict_wz_rows_absent, statuses["wz_mass_fit_response_row_builder"])
    report("matched-top-w-covariance-absent", matched_covariance_absent, statuses["top_wz_matched_covariance_builder"])
    report("same-source-wz-gate-open", same_source_wz_gate_open, statuses["same_source_wz_response_gate"])
    report("aggregate-proposal-denied", aggregate_proposal_denied, "assembly/retained/campaign proposal_allowed=false")
    report("smoke-promotion-blocked", all_smoke_blockers_present, str([k for k, ok in blockers.items() if not ok]))

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ smoke rows cannot be promoted to production WZ response",
        "verdict": (
            "The W/Z smoke artifact is a scout/schema artifact and cannot be "
            "promoted into the strict production W/Z response surface.  Its "
            "rows are explicitly synthetic, production_wz_rows_written is "
            "false, same-source and canonical-Higgs identities are false, "
            "g2 and matched covariance are absent, and the strict W/Z row, "
            "same-source EW action, matched covariance, W/Z gate, assembly, "
            "retained-route, and campaign certificates all deny proposal authority."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Promotion would import the same-source EW action, W/Z production "
            "row, covariance, g2, and identity certificates that the smoke "
            "schema explicitly does not supply."
        ),
        "bare_retained_allowed": False,
        "wz_smoke_to_production_promotion_no_go_passed": FAIL_COUNT == 0,
        "smoke_gate": display(SMOKE_GATE),
        "smoke_artifact": display(SMOKE_ARTIFACT),
        "promotion_blockers": blockers,
        "strict_surface_checks": {
            "same_source_ew_action_absent": same_source_ew_action_absent,
            "wz_correlator_mass_fit_path_absent": wz_path_absent,
            "strict_wz_response_rows_absent": strict_wz_rows_absent,
            "matched_top_w_covariance_absent": matched_covariance_absent,
            "same_source_wz_gate_open": same_source_wz_gate_open,
            "aggregate_proposal_denied": aggregate_proposal_denied,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not promote smoke rows to production rows",
            "does not treat synthetic correlators as W/Z field measurements",
            "does not infer same-source EW action or source-coordinate identity from schema metadata",
            "does not use static EW algebra, H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Create a genuine same-source EW action certificate and production "
            "W/Z correlator mass-fit rows, then rerun the W/Z mass-fit response "
            "row builder and matched top/W covariance builder in strict mode."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
