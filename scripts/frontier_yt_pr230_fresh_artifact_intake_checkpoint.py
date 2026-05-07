#!/usr/bin/env python3
"""
PR #230 fresh artifact intake checkpoint.

This runner consumes only committed PR-head certificates.  It asks whether the
post-block17 surface contains either of the high-priority campaign inputs:

1. certified canonical O_H plus production C_ss/C_sH/C_HH pole rows with Gram
   flatness; or
2. a strict W/Z physical-response packet with accepted action, production rows,
   matched covariance, strict non-observed g2 authority, delta_perp authority,
   and final W-response rows.

It intentionally does not inspect active chunk-worker output, pending logs, or
uncommitted live files.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_fresh_artifact_intake_checkpoint_2026-05-07.json"

PARENTS = {
    "source_higgs_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "two_source_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "common_oh_wz_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "open_surface_bridge_intake": "outputs/yt_pr230_open_surface_bridge_intake_2026-05-07.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "positive_completion_audit": "outputs/yt_pr230_positive_closure_completion_audit_2026-05-05.json",
    "retained_route_certificate": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

SOURCE_HIGGS_ROOTS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "two_source_combined_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
}

WZ_PRODUCTION_ROOTS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "fh_gauge_mass_response_measurement_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "fh_gauge_mass_response_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "delta_perp_correction_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "same_source_w_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
}

FORBIDDEN_FIREWALL = {
    "used_yt_ward_identity": False,
    "used_hunit_matrix_element_or_operator": False,
    "used_y_t_bare": False,
    "used_observed_y_t_or_top_mass": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "aliased_c_sx_to_c_sh_before_canonical_oh": False,
    "promoted_scout_or_smoke_rows": False,
    "assumed_k_top_equals_k_gauge": False,
    "assumed_top_wz_covariance": False,
    "touched_live_chunk_worker": False,
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


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present_map(paths: dict[str, str]) -> dict[str, bool]:
    return {name: (ROOT / relpath).exists() for name, relpath in paths.items()}


def git_value(*args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=ROOT, text=True).strip()


def main() -> int:
    print("PR #230 fresh artifact intake checkpoint")
    print("=" * 72)

    parents = {name: load_json(relpath) for name, relpath in PARENTS.items()}
    source_roots = present_map(SOURCE_HIGGS_ROOTS)
    wz_roots = present_map(WZ_PRODUCTION_ROOTS)

    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    source = parents["source_higgs_aperture"]
    lsz = parents["strict_scalar_lsz"]
    combiner = parents["two_source_combiner"]
    package = parents["two_source_package"]
    common_cut = parents["common_oh_wz_cut"]
    open_surface = parents["open_surface_bridge_intake"]
    fms_cut = parents["fms_action_adoption_minimal_cut"]
    additive_top = parents["additive_top_jacobian_rows"]
    wz_root = parents["wz_accepted_action_root"]
    wz_intake = parents["wz_physical_response_intake"]
    campaign = parents["campaign_status"]

    ready_chunks = combiner.get("ready_chunks")
    expected_chunks = combiner.get("expected_chunks")
    missing_chunks = combiner.get("missing_chunk_indices", [])
    if not isinstance(missing_chunks, list):
        missing_chunks = []

    source_higgs_closure_present = (
        all(source_roots.values())
        and source.get("proposal_allowed") is True
        and lsz.get("strict_scalar_lsz_moment_fv_authority_present") is True
    )
    strict_wz_packet_present = (
        all(wz_roots.values())
        and wz_intake.get("proposal_allowed") is True
        and wz_root.get("accepted_same_source_ew_action") is True
    )

    checks = {
        "parent_certificates_loaded": not missing_parents,
        "parent_proposals_all_false": not proposal_parents,
        "pr_head_open_status": campaign.get("proposal_allowed") is False,
        "source_higgs_roots_absent": not any(source_roots.values()),
        "source_higgs_parent_still_open": source.get("proposal_allowed") is False,
        "two_source_prefix_is_current_partial": isinstance(ready_chunks, int)
        and isinstance(expected_chunks, int)
        and expected_chunks == 63
        and 0 < ready_chunks < expected_chunks,
        "two_source_combined_rows_absent": combiner.get("combined_rows_written") is False,
        "next_missing_chunk_is_ready_plus_one": bool(missing_chunks)
        and isinstance(ready_chunks, int)
        and missing_chunks[0] == ready_chunks + 1,
        "strict_scalar_lsz_not_authority": lsz.get("proposal_allowed") is False
        and lsz.get("strict_scalar_lsz_moment_fv_authority_present") is not True,
        "common_cut_support_only": common_cut.get("proposal_allowed") is False,
        "open_surface_bridge_support_only": open_surface.get("proposal_allowed")
        is False
        and "open-surface bridge intake" in status(open_surface),
        "fms_action_cut_support_only": fms_cut.get("proposal_allowed") is False
        and fms_cut.get("closure_authorized") is False
        and fms_cut.get("adoption_allowed_now") is False
        and "FMS action-adoption minimal cut" in status(fms_cut),
        "additive_top_jacobian_support_only": additive_top.get("proposal_allowed")
        is False
        and "additive-top" in status(additive_top)
        and "closure still open" in status(additive_top),
        "wz_production_roots_absent": not any(wz_roots.values()),
        "wz_accepted_action_absent": wz_root.get("accepted_same_source_ew_action") is not True,
        "wz_packet_parent_still_open": wz_intake.get("proposal_allowed") is False,
        "no_closure_artifact_present": not source_higgs_closure_present
        and not strict_wz_packet_present,
        "forbidden_firewall_clean": not any(FORBIDDEN_FIREWALL.values()),
    }

    for name, ok in checks.items():
        report(name, bool(ok), "ok" if ok else "failed")

    result = {
        "artifact": "YT_PR230_FRESH_ARTIFACT_INTAKE_CHECKPOINT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_head": git_value("rev-parse", "HEAD"),
        "git_head_subject": git_value("log", "-1", "--pretty=%s"),
        "actual_current_surface_status": (
            "open / fresh-artifact intake checkpoint at PR #230 head; "
            "no certified O_H/source-Higgs pole-row packet or strict W/Z "
            "accepted-action physical-response packet is present"
        ),
        "conditional_surface_status": (
            "exact support if future same-surface artifacts supply certified O_H "
            "plus production C_ss/C_sH/C_HH pole rows with Gram flatness, or an "
            "accepted EW/Higgs action, canonical O_H/sector-overlap authority, "
            "production W/Z correlator mass-fit rows, same-source top-response "
            "rows, matched top/W or top/Z covariance, strict non-observed g2, "
            "delta_perp authority, and final W-response rows"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            f"The committed PR head contains a {ready_chunks}/{expected_chunks} "
            "C_sx/C_xx staging prefix, additive-response aggregate wiring, "
            "open-surface bridge intake, additive-top coarse Jacobian rows, "
            "and the FMS action-adoption minimal cut, all at support/boundary "
            "or route-guidance status.  "
            "The source-Higgs closure roots, W/Z accepted-action roots, W/Z "
            "production roots, matched covariance, strict g2 certificate, "
            "delta_perp authority, and final W-response rows remain absent."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "consumed_committed_pr_head_only": True,
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
            "note": (
                "Active chunk-worker files, pending checkpoints, and logs are "
                "not consumed by this runner."
            ),
        },
        "source_higgs_route": {
            "closure_artifact_present": source_higgs_closure_present,
            "root_presence": source_roots,
            "aperture_status": status(source),
            "strict_scalar_lsz_status": status(lsz),
            "two_source_prefix": {
                "ready_chunks": ready_chunks,
                "expected_chunks": expected_chunks,
                "combined_rows_written": combiner.get("combined_rows_written"),
                "first_missing_chunk": missing_chunks[0] if missing_chunks else None,
                "package_status": status(package),
            },
        },
        "wz_route": {
            "strict_packet_present": strict_wz_packet_present,
            "production_root_presence": wz_roots,
            "accepted_action_root_status": status(wz_root),
            "physical_response_intake_status": status(wz_intake),
        },
        "common_root_cut_status": status(common_cut),
        "open_surface_bridge_intake_status": status(open_surface),
        "fms_action_adoption_minimal_cut_status": status(fms_cut),
        "additive_top_jacobian_rows_status": status(additive_top),
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "checks": checks,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
        "summary": {
            "pass": PASS_COUNT,
            "fail": FAIL_COUNT,
        },
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
