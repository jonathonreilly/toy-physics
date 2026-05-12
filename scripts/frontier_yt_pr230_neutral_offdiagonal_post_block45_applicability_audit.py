#!/usr/bin/env python3
"""
PR #230 neutral off-diagonal post-Block45 applicability audit.

This runner asks whether the existing neutral off-diagonal / primitive-transfer
no-go still applies after the latest source target-time-series and tau-row
audits.  It is intentionally narrow: it does not rerun the old proof, and it
does not claim a permanent no-go.  It checks whether any new current-surface
artifact has appeared that retires the load-bearing missing H3/H4 premises.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_neutral_offdiagonal_post_block45_applicability_audit_2026-05-12.json"
)

PARENTS = {
    "neutral_offdiagonal_generator": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "neutral_burnside": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
    "same_surface_neutral_multiplicity_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "same_surface_neutral_multiplicity_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "two_source_primitive_transfer_candidate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
    "block43_full_timeseries_neutral_transfer_no_go": "outputs/yt_pr230_full_timeseries_neutral_transfer_lift_no_go_after_block42_2026-05-12.json",
    "block44_mc_timeseries_krylov_no_go": "outputs/yt_pr230_mc_timeseries_krylov_transfer_no_go_after_block43_2026-05-12.json",
    "block45_physical_euclidean_source_higgs_absence": "outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json",
    "source_higgs_time_kernel_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "source_higgs_time_kernel_rows": "outputs/yt_pr230_source_higgs_time_kernel_rows",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_higher_shell_chunk001": "outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk001_2026-05-07.json",
    "schur_higher_shell_chunk002": "outputs/yt_pr230_schur_higher_shell_rows/yt_pr230_schur_higher_shell_rows_L12_T24_chunk002_2026-05-07.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_c_sx_covariance_as_transfer_generator": False,
    "treated_mc_timeseries_as_transfer_generator": False,
    "treated_top_tau_rows_as_source_higgs_rows": False,
    "treated_reduced_smoke_as_production_rows": False,
    "treated_active_worker_as_completed_evidence": False,
    "claimed_retained_or_proposed_retained": False,
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


def load(rel: str | Path) -> dict[str, Any]:
    path = Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def path_present(rel: str) -> bool:
    path = ROOT / rel
    if path.is_dir():
        return any(path.rglob("*.json"))
    return path.exists()


def active_worker_summary() -> dict[str, Any]:
    return {
        "active_worker_intent_counted_as_evidence": False,
        "volatile_process_details_recorded": False,
        "reason": (
            "Running or queued worker processes are not completed JSON/certificate "
            "artifacts and cannot retire H3/H4 or source-Higgs premises."
        ),
    }


def main() -> int:
    print("PR #230 neutral off-diagonal post-Block45 applicability audit")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    failing_parents = [
        name for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", cert.get("checks", {}).get("FAIL", 0))) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_presence = {name: path_present(path) for name, path in FUTURE_FILES.items()}
    workers = active_worker_summary()

    old_no_go_applies = (
        "neutral off-diagonal generator not derivable"
        in statuses["neutral_offdiagonal_generator"]
        and certs["neutral_offdiagonal_generator"].get("exact_negative_boundary_passed")
        is True
        and certs["neutral_offdiagonal_generator"].get("proposal_allowed") is False
    )
    finite_c_sx_not_transfer = (
        "C_sx rows do not certify a physical primitive neutral transfer"
        in statuses["two_source_primitive_transfer_candidate"]
        and certs["two_source_primitive_transfer_candidate"].get("proposal_allowed") is False
        and certs["two_source_primitive_transfer_candidate"].get(
            "physical_transfer_candidate_accepted"
        )
        is False
    )
    h3h4_still_absent = (
        certs["neutral_h3h4_aperture"].get(
            "h3_physical_transfer_or_offdiagonal_generator_absent"
        )
        is True
        and certs["neutral_h3h4_aperture"].get("proposal_allowed") is False
    )
    block43_does_not_reopen = (
        certs["block43_full_timeseries_neutral_transfer_no_go"].get(
            "full_timeseries_neutral_transfer_lift_no_go_passed"
        )
        is True
        and certs["block43_full_timeseries_neutral_transfer_no_go"].get(
            "proposal_allowed"
        )
        is False
    )
    block44_does_not_reopen = (
        certs["block44_mc_timeseries_krylov_no_go"].get(
            "mc_timeseries_krylov_transfer_no_go_passed"
        )
        is True
        and certs["block44_mc_timeseries_krylov_no_go"].get("proposal_allowed")
        is False
    )
    block45_does_not_reopen = (
        certs["block45_physical_euclidean_source_higgs_absence"].get(
            "physical_euclidean_source_higgs_row_absence_passed"
        )
        is True
        and certs["block45_physical_euclidean_source_higgs_absence"].get(
            "proposal_allowed"
        )
        is False
    )
    no_completed_future_artifact = not any(future_presence.values())
    active_workers_not_evidence = (
        workers["active_worker_intent_counted_as_evidence"] is False
        and workers["volatile_process_details_recorded"] is False
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    audit_passed = all(
        [
            not missing_parents,
            not failing_parents,
            not proposal_parents,
            old_no_go_applies,
            finite_c_sx_not_transfer,
            h3h4_still_absent,
            block43_does_not_reopen,
            block44_does_not_reopen,
            block45_does_not_reopen,
            no_completed_future_artifact,
            active_workers_not_evidence,
            aggregate_still_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("old-neutral-offdiagonal-no-go-applies", old_no_go_applies, statuses["neutral_offdiagonal_generator"])
    report("finite-csx-not-transfer", finite_c_sx_not_transfer, statuses["two_source_primitive_transfer_candidate"])
    report("h3h4-physical-transfer-still-absent", h3h4_still_absent, statuses["neutral_h3h4_aperture"])
    report("block43-does-not-reopen-neutral-route", block43_does_not_reopen, statuses["block43_full_timeseries_neutral_transfer_no_go"])
    report("block44-does-not-reopen-neutral-route", block44_does_not_reopen, statuses["block44_mc_timeseries_krylov_no_go"])
    report("block45-does-not-reopen-neutral-route", block45_does_not_reopen, statuses["block45_physical_euclidean_source_higgs_absence"])
    report("no-completed-future-neutral-artifact", no_completed_future_artifact, str(future_presence))
    report("active-workers-not-counted-as-evidence", active_workers_not_evidence, workers["reason"])
    report("aggregate-gates-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("post-block45-neutral-offdiagonal-applicability-audit", audit_passed, "no current artifact retires H3/H4")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / post-Block45 artifacts do not reopen "
            "the neutral off-diagonal generator or primitive-transfer route"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface physical neutral "
            "transfer/off-diagonal generator, primitive-cone certificate, "
            "strict source-Higgs row packet, or strict W/Z physical-response "
            "packet lands"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current post-Block45 surface adds source target-time-series "
            "and tau-row absence boundaries, but still supplies no completed "
            "same-surface off-diagonal neutral generator, primitive transfer, "
            "source-Higgs row packet, or strict W/Z physical-response packet."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "post_block45_neutral_offdiagonal_applicability_audit_passed": audit_passed,
        "future_artifact_presence": future_presence,
        "active_worker_summary": workers,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "open_imports": [
            "same-surface physical neutral transfer/off-diagonal generator",
            "strict primitive-cone or Burnside irreducibility certificate",
            "canonical O_H/source-Higgs or strict W/Z coupling authority",
            "pole/FV/IR/model-class authority for the neutral scalar row",
        ],
        "exact_next_action": (
            "Do not reopen the neutral off-diagonal route from C_sx support, "
            "MC target series, ordinary tau rows, reduced smoke, or active "
            "worker intent.  Reopen only with a completed same-surface H3/H4 "
            "artifact or pivot to strict source-Higgs/WZ/scalar-action roots."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and audit_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
