#!/usr/bin/env python3
"""
PR #230 block37 post-block36 supervisor-yield checkpoint.

Block36 already consumed the then-current source-Higgs and W/Z shortcut
boundaries and selected strict W/Z accepted-action physical response as the
active fallback.  The PR head then advanced with route-exhaustion/support
commits.  This checkpoint answers only the supervisor-resume question: after
those post-block36 commits, did a new committed production/certificate input
arrive that admits a ranked queue item?  If not, keep the PR230 lane waiting on
the named source-Higgs or W/Z artifacts and yield to the outer supervisor.

This runner deliberately does not re-prove the block36 absence result and does
not touch live chunk-worker output.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block37_post_block36_supervisor_yield_checkpoint_2026-05-12.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
BLOCK36_HEAD = "4b530a729a8a06b103efd1c9c4222fdfd50f87c8"
EXPECTED_INSPECTION_HEAD = "5b1b916fa638e03f1806c7a6854ad60b856963b5"
BLOCK37_SUBJECT = "Record PR230 block37 supervisor yield checkpoint"
EXPECTED_POST_BLOCK36_SUBJECTS = {
    "Package PR230 FH LSZ target-timeseries full set",
    "Record PR230 native scalar action route exhaustion",
    "Record PR230 WZ absolute authority route exhaustion",
}

PARENTS = {
    "block36_source_higgs_wz_dispatch": "outputs/yt_pr230_block36_source_higgs_wz_dispatch_checkpoint_2026-05-12.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "fh_lsz_target_timeseries_full_set": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "native_scalar_action_route_exhaustion": "outputs/yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40_2026-05-12.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "wz_absolute_authority_route_exhaustion": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "neutral_rank_one_bypass": "outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json",
}

SOURCE_HIGGS_REQUIRED_PATHS = {
    "accepted_same_surface_ew_higgs_action": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "strict_source_higgs_pole_rows": "outputs/yt_pr230_source_higgs_pole_rows_2026-05-06.json",
    "source_higgs_cross_correlator_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "source_higgs_gram_fv_ir_authority": "outputs/yt_pr230_source_higgs_gram_fv_ir_authority_certificate_2026-05-11.json",
}

WZ_REQUIRED_PATHS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "fh_gauge_mass_response_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "fh_gauge_mass_response_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "delta_perp_correction_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "same_source_w_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
}

NEUTRAL_H3H4_REQUIRED_PATHS = {
    "neutral_h3_physical_transfer": "outputs/yt_pr230_neutral_h3_physical_transfer_certificate_2026-05-11.json",
    "neutral_h4_source_higgs_coupling": "outputs/yt_pr230_neutral_h4_source_higgs_coupling_certificate_2026-05-11.json",
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
    "promoted_wz_scout_or_smoke_rows": False,
    "assumed_k_top_equals_k_gauge": False,
    "assumed_top_wz_covariance": False,
    "touched_live_chunk_worker": False,
    "inspected_active_chunk_output": False,
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


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def git_ok(args: list[str]) -> bool:
    return (
        subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def ref_path_exists(ref: str, relpath: str) -> bool:
    return git_ok(["cat-file", "-e", f"{ref}:{relpath}"])


def present_at_ref(ref: str, paths: dict[str, str]) -> dict[str, bool]:
    return {name: ref_path_exists(ref, path) for name, path in paths.items()}


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def commits(base: str, head: str) -> list[str]:
    raw = run_git(["log", "--format=%H%x09%s", f"{base}..{head}"])
    return [line for line in raw.splitlines() if line]


def subjects(lines: list[str]) -> list[str]:
    return [line.split("\t", 1)[1] for line in lines if "\t" in line]


def missing_roots(presence: dict[str, bool]) -> list[str]:
    return sorted(name for name, present in presence.items() if not present)


def source_higgs_admitted(presence: dict[str, bool]) -> bool:
    action = presence["accepted_same_surface_ew_higgs_action"] or presence[
        "accepted_same_source_ew_action"
    ]
    operator = presence["canonical_oh_certificate"] or presence[
        "canonical_higgs_operator_certificate"
    ]
    rows = presence["strict_source_higgs_pole_rows"] or (
        presence["source_higgs_cross_correlator_rows"]
        and presence["source_higgs_production_certificate"]
    )
    return action and operator and rows and presence["source_higgs_gram_fv_ir_authority"]


def all_present(presence: dict[str, bool]) -> bool:
    return bool(presence) and all(presence.values())


def main() -> int:
    print("PR #230 block37 post-block36 supervisor-yield checkpoint")
    print("=" * 78)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [
        name
        for name, cert in parents.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK37_SUBJECT else "HEAD"
    inspection_head = run_git(["rev-parse", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    commits_since_block36 = commits(BLOCK36_HEAD, inspection_ref)
    commit_subjects_since_block36 = subjects(commits_since_block36)

    source_presence = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_presence = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_presence = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block36 = parents["block36_source_higgs_wz_dispatch"]
    fh_full_set = parents["fh_lsz_target_timeseries_full_set"]
    native_scalar = parents["native_scalar_action_route_exhaustion"]
    wz_absolute = parents["wz_absolute_authority_route_exhaustion"]
    block36_clean = (
        block36.get("block36_source_higgs_wz_dispatch_checkpoint_passed") is True
        and block36.get("proposal_allowed") is False
        and block36.get("bare_retained_allowed") is False
        and block36.get("campaign_decision", {}).get("yield_for_supervisor") is True
        and block36.get("checks", {}).get("source-higgs-route-checkpointed") is True
        and block36.get("checks", {}).get("wz-pivot-selected-after-source-higgs-block")
        is True
        and block36.get("checks", {}).get("wz-pivot-not-admitted") is True
        and block36.get("checks", {}).get("no-route-admitted-without-explicit-input")
        is True
    )
    post_block36_commits_consumed = (
        inspection_head == EXPECTED_INSPECTION_HEAD
        and set(commit_subjects_since_block36) == EXPECTED_POST_BLOCK36_SUBJECTS
        and len(commit_subjects_since_block36) == len(EXPECTED_POST_BLOCK36_SUBJECTS)
    )
    post_block36_inputs_support_or_boundary_only = (
        fh_full_set.get("proposal_allowed") is False
        and fh_full_set.get("bare_retained_allowed") is False
        and "bounded-support" in status(fh_full_set)
        and native_scalar.get("native_scalar_action_lsz_route_exhaustion_passed")
        is True
        and native_scalar.get("no_current_native_scalar_action_lsz_route_closes")
        is True
        and native_scalar.get("proposal_allowed") is False
        and native_scalar.get("bare_retained_allowed") is False
        and wz_absolute.get("wz_absolute_authority_route_exhaustion_passed")
        is True
        and wz_absolute.get("proposal_allowed") is False
        and wz_absolute.get("bare_retained_allowed") is False
    )
    source_admitted = source_higgs_admitted(source_presence)
    wz_admitted = all_present(wz_presence)
    neutral_admitted = all_present(neutral_presence)
    no_route_admitted = not (source_admitted or wz_admitted or neutral_admitted)
    current_route_blocked = (
        block36_clean
        and post_block36_inputs_support_or_boundary_only
        and parents["wz_physical_response_intake"].get("production_packet_present")
        is False
        and parents["wz_same_source_action_minimal_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and not wz_admitted
    )
    pivot_back_requires_new_source_higgs_input = (
        parents["fms_action_adoption_minimal_cut"].get("adoption_allowed_now")
        is False
        and parents["source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
        and native_scalar.get("no_current_native_scalar_action_lsz_route_closes")
        is True
        and not source_admitted
    )
    neutral_reopen_blocked = (
        parents["neutral_rank_one_bypass"].get("exact_negative_boundary_passed")
        is True
        and parents["neutral_rank_one_bypass"].get("rank_one_bypass_closed")
        is False
        and not neutral_admitted
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    yield_for_supervisor = (
        block36_clean
        and post_block36_commits_consumed
        and post_block36_inputs_support_or_boundary_only
        and current_route_blocked
        and pivot_back_requires_new_source_higgs_input
        and neutral_reopen_blocked
        and no_route_admitted
        and firewall_clean
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("inspection-ref-is-current-pr-head", inspection_head == EXPECTED_INSPECTION_HEAD, f"{inspection_ref}={inspection_head}")
    report("post-block36-commits-consumed", post_block36_commits_consumed, str(commit_subjects_since_block36))
    report("post-block36-inputs-support-or-boundary-only", post_block36_inputs_support_or_boundary_only, "FH-LSZ full set support plus native-scalar and W/Z route-exhaustion boundaries")
    report("block36-clean-dispatch-checkpoint", block36_clean, status(block36))
    report("wz-active-fallback-still-blocked", current_route_blocked, str(wz_presence))
    report("source-higgs-reopen-requires-new-input", pivot_back_requires_new_source_higgs_input, str(source_presence))
    report("neutral-reopen-blocked-without-h3h4", neutral_reopen_blocked, str(neutral_presence))
    report("no-ranked-route-admitted", no_route_admitted, "source-Higgs/WZ/neutral required packets absent at inspection ref")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("yield-for-supervisor", yield_for_supervisor, "waiting on explicit production/certificate inputs")

    result = {
        "actual_current_surface_status": (
            "open / post-block36 supervisor-yield checkpoint; post-block36 "
            "support and route-exhaustion commits are consumed, W/Z "
            "accepted-action fallback remains blocked, and no ranked route is "
            "admitted without fresh production/certificate inputs"
        ),
        "conditional_surface_status": (
            "source-Higgs support only if accepted same-surface O_H/action and "
            "strict C_ss/C_sH/C_HH pole rows with Gram/FV/IR authority land; "
            "W/Z support only if accepted action, production W/Z rows, "
            "same-source top rows, matched covariance, strict non-observed g2, "
            "delta_perp authority, and final W-response rows land"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block37 is a supervisor-yield checkpoint, not a new route theorem. "
            "The inspected PR head includes post-block36 FH-LSZ full-set "
            "support plus native-scalar/action/LSZ and W/Z absolute-authority "
            "route-exhaustion boundaries, but no admitted source-Higgs, W/Z, "
            "or neutral H3/H4 production/certificate input."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "block37_post_block36_supervisor_yield_checkpoint_passed": FAIL_COUNT == 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspection_head": inspection_head,
        "pr_ref": PR_REF,
        "pr_head": pr_head,
        "block36_head": BLOCK36_HEAD,
        "expected_inspection_head": EXPECTED_INSPECTION_HEAD,
        "commits_since_block36_head": commits_since_block36,
        "commit_subjects_since_block36_head": commit_subjects_since_block36,
        "expected_post_block36_subjects": sorted(EXPECTED_POST_BLOCK36_SUBJECTS),
        "post_block36_inputs": {
            "fh_lsz_target_timeseries_full_set_support": status(fh_full_set),
            "native_scalar_action_route_exhaustion": status(native_scalar),
            "wz_absolute_authority_route_exhaustion": status(wz_absolute),
            "support_or_boundary_only": post_block36_inputs_support_or_boundary_only,
        },
        "source_higgs_route": {
            "rank": 1,
            "admitted": source_admitted,
            "required_paths": SOURCE_HIGGS_REQUIRED_PATHS,
            "committed_path_presence": source_presence,
            "missing_roots": missing_roots(source_presence),
            "decision": (
                "do not reopen until accepted same-surface O_H/action plus "
                "strict C_ss/C_sH/C_HH pole rows and Gram/FV/IR authority exist"
            ),
        },
        "wz_accepted_action_response_route": {
            "rank": 2,
            "active_fallback_from_block36": True,
            "admitted": wz_admitted,
            "required_paths": WZ_REQUIRED_PATHS,
            "committed_path_presence": wz_presence,
            "missing_roots": missing_roots(wz_presence),
            "decision": (
                "current route remains blocked; supply accepted action, "
                "production W/Z mass-response rows, same-source top rows, "
                "matched covariance, strict non-observed g2, delta_perp "
                "authority, and final W-response rows before rerunning"
            ),
        },
        "neutral_h3h4_route": {
            "rank": 3,
            "admitted": neutral_admitted,
            "required_paths": NEUTRAL_H3H4_REQUIRED_PATHS,
            "committed_path_presence": neutral_presence,
            "missing_roots": missing_roots(neutral_presence),
            "decision": (
                "do not reopen without physical neutral transfer/off-diagonal "
                "dynamics plus source/canonical-Higgs coupling authority"
            ),
        },
        "campaign_decision": {
            "current_route": "strict W/Z accepted-action physical response",
            "current_route_blocked": current_route_blocked,
            "pivot_back_to_source_higgs_requires_new_input": pivot_back_requires_new_source_higgs_input,
            "yield_for_supervisor": yield_for_supervisor,
            "next_exact_action": (
                "Supply one explicit missing artifact: accepted same-surface "
                "O_H/action plus strict C_ss/C_sH/C_HH rows, or a strict W/Z "
                "physical-response packet with accepted action, production rows, "
                "same-source top rows, matched covariance, strict non-observed "
                "g2, delta_perp, and final W-response rows."
            ),
        },
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
        },
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "checks": {
            "parent-certificates-present": not missing_parents,
            "parent-certificates-have-no-fails": not failing_parents,
            "no-parent-authorizes-proposal": not proposal_parents,
            "inspection-ref-is-current-pr-head": inspection_head == EXPECTED_INSPECTION_HEAD,
            "post-block36-commits-consumed": post_block36_commits_consumed,
            "post-block36-inputs-support-or-boundary-only": post_block36_inputs_support_or_boundary_only,
            "block36-clean-dispatch-checkpoint": block36_clean,
            "wz-active-fallback-still-blocked": current_route_blocked,
            "source-higgs-reopen-requires-new-input": pivot_back_requires_new_source_higgs_input,
            "neutral-reopen-blocked-without-h3h4": neutral_reopen_blocked,
            "no-ranked-route-admitted": no_route_admitted,
            "forbidden-firewall-clean": firewall_clean,
            "yield-for-supervisor": yield_for_supervisor,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not rerun a current-surface shortcut as new proof",
            "does not treat block36 as accepted action, source-Higgs pole-row, W/Z response-row, covariance, strict g2, or neutral H3/H4 evidence",
            "does not treat the post-block36 FH-LSZ full-set support or native-scalar/WZ route-exhaustion boundaries as closure",
            "does not relabel C_sx/C_xx as C_sH/C_HH before x=O_H is certified",
            "does not promote W/Z scout, smoke, or schema rows to production evidence",
            "does not assume top/W covariance or k_top = k_gauge",
            "does not set kappa_s, c2, Z_match, g2, or delta_perp by convention",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, or u0",
            "does not inspect live or untracked chunk-worker output",
        ],
        "passes": PASS_COUNT,
        "fails": FAIL_COUNT,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
