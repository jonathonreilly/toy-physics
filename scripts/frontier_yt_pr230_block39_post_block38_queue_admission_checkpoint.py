#!/usr/bin/env python3
"""
PR #230 block39 post-block38 queue-admission checkpoint.

Block38 consumed the prioritized source-Higgs / WZ stuck fan-out.  A lane-1
companion checkpoint then closed the adjacent Euclidean source-Higgs row
shortcut: ordinary tau-keyed top/scalar-source correlators and reduced smoke
are not strict production C_ss/C_sH/C_HH(tau) rows.

This runner does not re-prove that absence.  It consumes the block38 checkpoint,
the lane-1 Block45 Euclidean-row boundary, the post-Block45 neutral
off-diagonal applicability boundary, the top mass-scan subtraction-contract
boundary, and the higher-shell source-Higgs operator boundary, then records the
required pivot:
source-Higgs remains ranked first but not admitted, and W/Z accepted-action
physical response is the next fallback but is also not admitted without a
strict production packet.  The lane remains open and waiting on a primitive-
bearing artifact.
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
    / "yt_pr230_block39_post_block38_queue_admission_checkpoint_2026-05-12.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
EXPECTED_INSPECTION_HEAD = "b0a765630fc789d76c9d9b0ee0a965e254596abc"
EXPECTED_INSPECTION_LABEL = "current PR head after higher-shell operator boundary"
BLOCK39_SUBJECT = "Record PR230 block39 queue admission checkpoint"

PARENTS = {
    "block38_bridge_stuck_fanout": "outputs/yt_pr230_block38_bridge_stuck_fanout_checkpoint_2026-05-12.json",
    "lane1_block45_physical_euclidean_rows": "outputs/yt_pr230_physical_euclidean_source_higgs_row_absence_after_block44_2026-05-12.json",
    "neutral_offdiagonal_post_block45_applicability": "outputs/yt_pr230_neutral_offdiagonal_post_block45_applicability_audit_2026-05-12.json",
    "top_mass_scan_subtraction_contract_applicability": "outputs/yt_pr230_top_mass_scan_subtraction_contract_applicability_audit_2026-05-12.json",
    "higher_shell_source_higgs_operator_boundary": "outputs/yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json",
    "wz_absolute_authority": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

SOURCE_HIGGS_REQUIRED_PATHS = {
    "accepted_same_surface_ew_higgs_action": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "physical_euclidean_source_higgs_rows": "outputs/yt_pr230_physical_euclidean_source_higgs_rows_2026-05-12.json",
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
    "promoted_tau_top_or_scalar_source_rows_to_source_higgs": False,
    "promoted_reduced_source_higgs_smoke_to_production": False,
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


def missing_roots(presence: dict[str, bool]) -> list[str]:
    return sorted(name for name, present in presence.items() if not present)


def source_higgs_admitted(presence: dict[str, bool]) -> bool:
    action = presence["accepted_same_surface_ew_higgs_action"] or presence[
        "accepted_same_source_ew_action"
    ]
    operator = presence["canonical_oh_certificate"] or presence[
        "canonical_higgs_operator_certificate"
    ]
    rows = presence["physical_euclidean_source_higgs_rows"] or presence[
        "strict_source_higgs_pole_rows"
    ] or (
        presence["source_higgs_cross_correlator_rows"]
        and presence["source_higgs_production_certificate"]
    )
    return action and operator and rows and presence["source_higgs_gram_fv_ir_authority"]


def all_present(presence: dict[str, bool]) -> bool:
    return bool(presence) and all(presence.values())


def no_fail(cert: dict[str, Any]) -> bool:
    return int(cert.get("fail_count", cert.get("fails", 0)) or 0) == 0


def main() -> int:
    print("PR #230 block39 post-block38 queue-admission checkpoint")
    print("=" * 82)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [name for name, cert in parents.items() if cert and not no_fail(cert)]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK39_SUBJECT else "HEAD"
    inspection_head = run_git(["rev-parse", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])

    source_presence = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_presence = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_presence = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block38 = parents["block38_bridge_stuck_fanout"]
    lane1_block45 = parents["lane1_block45_physical_euclidean_rows"]
    neutral_offdiag = parents["neutral_offdiagonal_post_block45_applicability"]
    top_mass_scan_subtraction = parents["top_mass_scan_subtraction_contract_applicability"]
    higher_shell_operator = parents["higher_shell_source_higgs_operator_boundary"]
    wz_absolute = parents["wz_absolute_authority"]

    block38_clean = (
        block38.get("block38_bridge_stuck_fanout_checkpoint_passed") is True
        and block38.get("proposal_allowed") is False
        and block38.get("bare_retained_allowed") is False
        and block38.get("checks", {}).get("five-frame-stuck-fanout-all-blocked")
        is True
        and block38.get("checks", {}).get("source-higgs-required-roots-still-absent")
        is True
        and block38.get("checks", {}).get("wz-required-roots-still-absent") is True
        and block38.get("checks", {}).get("forbidden-firewall-clean") is True
    )
    lane1_block45_blocks_source_rows = (
        lane1_block45.get("physical_euclidean_source_higgs_row_absence_passed")
        is True
        and lane1_block45.get("proposal_allowed") is False
        and lane1_block45.get("bare_retained_allowed") is False
        and "tau-keyed production correlators are not physical Euclidean source-Higgs"
        in status(lane1_block45)
    )
    neutral_offdiag_post_block45_boundary_consumed = (
        neutral_offdiag.get("post_block45_neutral_offdiagonal_applicability_audit_passed")
        is True
        and neutral_offdiag.get("proposal_allowed") is False
        and neutral_offdiag.get("bare_retained_allowed") is False
        and "post-Block45 artifacts do not reopen"
        in status(neutral_offdiag)
    )
    top_mass_scan_subtraction_boundary_consumed = (
        top_mass_scan_subtraction.get(
            "top_mass_scan_subtraction_contract_applicability_audit_passed"
        )
        is True
        and top_mass_scan_subtraction.get("proposal_allowed") is False
        and top_mass_scan_subtraction.get("bare_retained_allowed") is False
        and "top mass-scan response harness does not satisfy the additive-top subtraction row contract"
        in status(top_mass_scan_subtraction)
    )
    higher_shell_operator_boundary_consumed = (
        higher_shell_operator.get(
            "higher_shell_source_higgs_operator_certificate_boundary_passed"
        )
        is True
        and higher_shell_operator.get("proposal_allowed") is False
        and higher_shell_operator.get("bare_retained_allowed") is False
        and "higher-shell source-Higgs cross rows use the taste-radial second-source certificate, not canonical O_H"
        in status(higher_shell_operator)
    )
    wz_authority_still_blocked = (
        wz_absolute.get("wz_absolute_authority_route_exhaustion_passed") is True
        and wz_absolute.get("proposal_allowed") is False
        and wz_absolute.get("bare_retained_allowed") is False
        and wz_absolute.get("checks", {}).get("no-route-closes-current-surface")
        is True
        and wz_absolute.get("checks", {}).get("strict-packet-roots-absent") is True
    )

    source_admitted = source_higgs_admitted(source_presence)
    wz_admitted = all_present(wz_presence)
    neutral_admitted = all_present(neutral_presence)
    no_route_admitted = not (source_admitted or wz_admitted or neutral_admitted)
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    queue_pivot_executed = (
        block38_clean
        and lane1_block45_blocks_source_rows
        and neutral_offdiag_post_block45_boundary_consumed
        and top_mass_scan_subtraction_boundary_consumed
        and higher_shell_operator_boundary_consumed
        and not source_admitted
        and wz_authority_still_blocked
        and not wz_admitted
        and no_route_admitted
    )
    yield_for_supervisor = (
        not missing_parents
        and not failing_parents
        and not proposal_parents
        and inspection_head == EXPECTED_INSPECTION_HEAD
        and queue_pivot_executed
        and firewall_clean
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("inspection-ref-is-current-pr-head", inspection_head == EXPECTED_INSPECTION_HEAD, f"{inspection_ref}={inspection_head}; expected={EXPECTED_INSPECTION_LABEL}")
    report("block38-stuck-fanout-clean", block38_clean, status(block38))
    report("lane1-block45-source-higgs-row-boundary-consumed", lane1_block45_blocks_source_rows, status(lane1_block45))
    report("post-block45-neutral-offdiagonal-boundary-consumed", neutral_offdiag_post_block45_boundary_consumed, status(neutral_offdiag))
    report("top-mass-scan-subtraction-boundary-consumed", top_mass_scan_subtraction_boundary_consumed, status(top_mass_scan_subtraction))
    report("higher-shell-operator-boundary-consumed", higher_shell_operator_boundary_consumed, status(higher_shell_operator))
    report("source-higgs-route-not-admitted-after-block45", not source_admitted, str(source_presence))
    report("wz-absolute-authority-still-blocked", wz_authority_still_blocked, status(wz_absolute))
    report("wz-route-not-admitted-after-pivot", not wz_admitted, str(wz_presence))
    report("neutral-h3h4-route-not-admitted", not neutral_admitted, str(neutral_presence))
    report("queue-pivot-executed", queue_pivot_executed, "source-Higgs consumed first, W/Z selected next, no route admitted")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("yield-for-supervisor", yield_for_supervisor, "waiting on primitive-bearing source-Higgs, W/Z, or neutral artifact")

    result = {
        "actual_current_surface_status": (
            "open / block39 post-block38 queue-admission checkpoint; block38 "
            "stuck fan-out, lane-1 Block45 Euclidean row boundary, and "
            "post-Block45 neutral off-diagonal, top mass-scan subtraction, "
            "and higher-shell operator boundaries leave source-Higgs not "
            "admitted, W/Z accepted-action response selected as fallback but "
            "not admitted, and neutral H3/H4 still blocked"
        ),
        "conditional_surface_status": (
            "source-Higgs support only if accepted same-surface O_H/action and "
            "physical Euclidean C_ss/C_sH/C_HH(tau) pole rows with Gram/FV/IR "
            "authority land; W/Z support only if accepted action, production "
            "W/Z rows, same-source top rows, matched covariance, strict "
            "non-observed g2, delta_perp authority, and final W-response rows "
            "land"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block39 is a queue-admission checkpoint, not a retained/proposed-"
            "retained theorem.  It consumes the block38 stuck fan-out and the "
            "lane-1 Block45 physical-Euclidean-row boundary plus the "
            "post-Block45 neutral off-diagonal and top mass-scan subtraction "
            "plus higher-shell operator boundaries, then records that no "
            "accepted action, canonical O_H certificate, production "
            "source-Higgs pole-row packet, strict W/Z packet, additive-top "
            "subtraction row contract, neutral off-diagonal generator, or "
            "neutral H3/H4 certificate is present."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "block39_post_block38_queue_admission_checkpoint_passed": FAIL_COUNT == 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspection_head": inspection_head,
        "expected_inspection_head": EXPECTED_INSPECTION_HEAD,
        "expected_inspection_label": EXPECTED_INSPECTION_LABEL,
        "pr_ref": PR_REF,
        "pr_head": pr_head,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "source_higgs_route": {
            "rank": 1,
            "admitted": source_admitted,
            "block45_physical_euclidean_rows_boundary_consumed": lane1_block45_blocks_source_rows,
            "higher_shell_operator_boundary_consumed": higher_shell_operator_boundary_consumed,
            "required_paths": SOURCE_HIGGS_REQUIRED_PATHS,
            "committed_path_presence": source_presence,
            "missing_roots": missing_roots(source_presence),
            "decision": (
                "not admitted after Block45; reopen only with accepted "
                "same-surface O_H/action and physical Euclidean "
                "C_ss/C_sH/C_HH(tau) pole rows plus Gram/FV/IR authority"
            ),
        },
        "wz_accepted_action_response_route": {
            "rank": 2,
            "selected_after_source_higgs_block": True,
            "admitted": wz_admitted,
            "top_mass_scan_subtraction_boundary_consumed": top_mass_scan_subtraction_boundary_consumed,
            "required_paths": WZ_REQUIRED_PATHS,
            "committed_path_presence": wz_presence,
            "missing_roots": missing_roots(wz_presence),
            "decision": (
                "not admitted; reopen only with accepted action, production "
                "W/Z rows, same-source top rows, matched covariance, strict "
                "non-observed g2, delta_perp authority, and final W-response rows"
            ),
        },
        "neutral_h3h4_route": {
            "rank": 3,
            "admitted": neutral_admitted,
            "post_block45_neutral_offdiagonal_boundary_consumed": neutral_offdiag_post_block45_boundary_consumed,
            "required_paths": NEUTRAL_H3H4_REQUIRED_PATHS,
            "committed_path_presence": neutral_presence,
            "missing_roots": missing_roots(neutral_presence),
            "decision": (
                "do not reopen without physical neutral transfer/off-diagonal "
                "dynamics plus source/canonical-Higgs coupling authority"
            ),
        },
        "campaign_decision": {
            "queue_pivot_executed": queue_pivot_executed,
            "no_ranked_route_admitted": no_route_admitted,
            "yield_for_supervisor": yield_for_supervisor,
            "next_exact_action": (
                "Supply one primitive-bearing artifact: accepted same-surface "
                "O_H/action plus physical Euclidean C_ss/C_sH/C_HH(tau) rows "
                "with Gram/FV/IR authority, or a strict W/Z physical-response "
                "packet with accepted action, production rows, same-source top "
                "rows, matched covariance, strict non-observed g2, delta_perp, "
                "and final W-response rows."
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
            "block38-stuck-fanout-clean": block38_clean,
            "lane1-block45-source-higgs-row-boundary-consumed": lane1_block45_blocks_source_rows,
            "post-block45-neutral-offdiagonal-boundary-consumed": neutral_offdiag_post_block45_boundary_consumed,
            "top-mass-scan-subtraction-boundary-consumed": top_mass_scan_subtraction_boundary_consumed,
            "higher-shell-operator-boundary-consumed": higher_shell_operator_boundary_consumed,
            "source-higgs-route-not-admitted-after-block45": not source_admitted,
            "wz-absolute-authority-still-blocked": wz_authority_still_blocked,
            "wz-route-not-admitted-after-pivot": not wz_admitted,
            "neutral-h3h4-route-not-admitted": not neutral_admitted,
            "queue-pivot-executed": queue_pivot_executed,
            "forbidden-firewall-clean": firewall_clean,
            "yield-for-supervisor": yield_for_supervisor,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not rerun block38 as new evidence",
            "does not treat the lane-1 Block45 row boundary as a permanent no-go against future physical Euclidean rows",
            "does not treat the post-Block45 neutral off-diagonal boundary as evidence for reopening the neutral primitive route",
            "does not treat top mass-scan dE/dm_bare rows as satisfying the additive-top subtraction row contract",
            "does not treat higher-shell source-Higgs cross rows emitted under the taste-radial second-source certificate as canonical O_H or strict C_sH/C_HH source-Higgs rows",
            "does not treat ordinary top tau correlators as source-Higgs rows",
            "does not treat scalar-source response fits as source-Higgs rows",
            "does not promote reduced C_sH/C_HH smoke to production pole evidence",
            "does not relabel C_sx/C_xx as C_sH/C_HH before x=O_H is certified",
            "does not promote W/Z scout, smoke, ratio, or response-only rows to a strict W/Z packet",
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
