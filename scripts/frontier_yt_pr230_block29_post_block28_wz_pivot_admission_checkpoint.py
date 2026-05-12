#!/usr/bin/env python3
"""
PR #230 block29 post-block28 W/Z pivot admission checkpoint.

Block28 consumed the degree-one O_H radial-tangent theorem as exact support.
This checkpoint records the required campaign pivot: the source-Higgs route is
sharper but still not admitted, so the next ranked W/Z accepted-action response
route is inspected at the current PR head.  No live chunk-worker output is read
or packaged.
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
    / "yt_pr230_block29_post_block28_wz_pivot_admission_checkpoint_2026-05-11.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
MAIN_REF = "origin/main"
BLOCK28_INPUT_HEAD = "e17c485639be9229af4d8ecb65222efdc159b0d1"
BLOCK28_SUBJECT = "Record PR230 block28 degree-one OH support intake"
BLOCK29_SUBJECT = "Record PR230 block29 post-block28 WZ pivot checkpoint"

PARENTS = {
    "block28_degree_one_oh_support_intake": "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "degree_one_action_premise": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "source_higgs_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "fms_oh_candidate_action": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "additive_top_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
    "two_source_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

SOURCE_HIGGS_REQUIRED_PATHS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "two_source_combined_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
}

WZ_REQUIRED_PATHS = {
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

NEUTRAL_H3H4_REQUIRED_PATHS = {
    "neutral_h3_physical_transfer": "outputs/yt_pr230_neutral_h3_physical_transfer_certificate_2026-05-11.json",
    "neutral_h4_source_higgs_coupling": "outputs/yt_pr230_neutral_h4_source_higgs_coupling_certificate_2026-05-11.json",
}

ALLOWED_BLOCK28_PATHS = {
    "scripts/frontier_yt_pr230_block28_degree_one_oh_support_intake_checkpoint.py",
    "scripts/frontier_yt_pr230_campaign_status_certificate.py",
    "docs/YT_PR230_BLOCK28_DEGREE_ONE_OH_SUPPORT_INTAKE_CHECKPOINT_NOTE_2026-05-11.md",
    "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json",
    "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

ALLOWED_BLOCK28_PREFIXES = (
    ".claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/",
    "docs/audit/",
)

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
    "inspected_active_chunk_output": False,
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
    if not run_git(["rev-parse", "--verify", ref]):
        return {name: False for name in paths}
    return {name: ref_path_exists(ref, relpath) for name, relpath in paths.items()}


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def changed_paths(base: str, head: str) -> list[str]:
    raw = run_git(["diff", "--name-only", f"{base}..{head}"])
    return sorted(line for line in raw.splitlines() if line)


def allowed_block28_path(path: str) -> bool:
    return path in ALLOWED_BLOCK28_PATHS or any(
        path.startswith(prefix) for prefix in ALLOWED_BLOCK28_PREFIXES
    )


def missing_roots(values: dict[str, bool]) -> list[str]:
    return sorted(name for name, present in values.items() if not present)


def all_absent(values: dict[str, bool]) -> bool:
    return bool(values) and not any(values.values())


def main() -> int:
    print("PR #230 block29 post-block28 W/Z pivot admission checkpoint")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK29_SUBJECT else "HEAD"
    inspected_head = run_git(["rev-parse", inspection_ref])
    inspected_subject = run_git(["log", "-1", "--format=%s", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    main_head = run_git(["rev-parse", "--verify", MAIN_REF])
    commits_since_block28_input = [
        line
        for line in run_git(
            ["log", "--format=%H%x09%s", f"{BLOCK28_INPUT_HEAD}..{inspection_ref}"]
        ).splitlines()
        if line
    ]
    paths_since_block28_input = changed_paths(BLOCK28_INPUT_HEAD, inspection_ref)
    disallowed_paths_since_block28_input = [
        path for path in paths_since_block28_input if not allowed_block28_path(path)
    ]

    source_paths = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_paths = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_paths = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block28 = parents["block28_degree_one_oh_support_intake"]
    degree_one = parents["degree_one_radial_tangent_oh"]
    degree_one_premise = parents["degree_one_action_premise"]
    wz_root = parents["wz_accepted_action_root"]
    wz_packet = parents["wz_physical_response_intake"]
    package = parents["two_source_package"]
    combiner = parents["two_source_combiner"]

    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [
        name for name, cert in parents.items() if int(cert.get("fail_count", 0) or 0) != 0
    ]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    only_block28_support_since_input = (
        len(commits_since_block28_input) == 1
        and commits_since_block28_input[0].endswith(f"\t{BLOCK28_SUBJECT}")
        and not disallowed_paths_since_block28_input
    )
    block28_exact_support_no_closure = (
        block28.get("proposal_allowed") is False
        and block28.get("checks", {}).get(
            "only-block27-checkpoint-since-block27-input-head"
        )
        is True
        and block28.get("checks", {}).get("degree-one-oh-support-loaded") is True
        and block28.get("checks", {}).get(
            "degree-one-action-premise-still-missing"
        )
        is True
        and block28.get("checks", {}).get("source-higgs-route-not-admitted")
        is True
        and block28.get("checks", {}).get("wz-route-not-admitted") is True
    )
    degree_one_support_still_conditional = (
        degree_one.get("degree_one_radial_tangent_oh_theorem_passed") is True
        and degree_one.get("same_surface_linear_tangent_premise_derived") is False
        and degree_one.get("canonical_oh_identity_derived") is False
        and degree_one.get("source_higgs_pole_rows_present") is False
        and degree_one_premise.get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
    )
    source_higgs_route_blocked_after_block28 = (
        all_absent(source_paths)
        and parents["source_higgs_aperture"].get("proposal_allowed") is False
        and parents["fms_oh_candidate_action"].get("closure_authorized") is False
        and parents["fms_source_overlap_readout"].get("readout_executable_now")
        is False
    )
    wz_pivot_selected = source_higgs_route_blocked_after_block28
    wz_pivot_not_admitted = (
        all_absent(wz_paths)
        and wz_root.get("proposal_allowed") is False
        and wz_packet.get("proposal_allowed") is False
        and "exact negative boundary" in status(wz_packet)
    )
    neutral_not_admitted = (
        all_absent(neutral_paths)
        and parents["neutral_h3h4_aperture"].get("proposal_allowed") is False
    )
    row_prefix_still_staging = (
        package.get("completed_chunk_count") == 62
        and combiner.get("ready_chunks") == 62
        and combiner.get("expected_chunks") == 63
        and combiner.get("combined_rows_written") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-runners-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_allowed_parents,
        f"proposal_allowed={proposal_allowed_parents}",
    )
    report(
        "inspected-head-is-current-pr-head",
        inspected_head == pr_head,
        f"inspected={inspected_head} pr={pr_head}",
    )
    report(
        "only-block28-support-since-block28-input-head",
        only_block28_support_since_input,
        f"commits={commits_since_block28_input} disallowed_paths={disallowed_paths_since_block28_input}",
    )
    report("block28-exact-support-no-closure", block28_exact_support_no_closure, status(block28))
    report(
        "degree-one-support-still-conditional",
        degree_one_support_still_conditional,
        status(degree_one_premise),
    )
    report(
        "source-higgs-route-blocked-after-block28",
        source_higgs_route_blocked_after_block28,
        f"missing={missing_roots(source_paths)}",
    )
    report(
        "wz-pivot-selected-after-source-higgs-block",
        wz_pivot_selected,
        "W/Z accepted-action response is the next ranked fallback route",
    )
    report(
        "wz-pivot-not-admitted-without-required-packet",
        wz_pivot_not_admitted,
        f"missing={missing_roots(wz_paths)}",
    )
    report(
        "neutral-h3h4-route-not-admitted",
        neutral_not_admitted,
        f"missing={missing_roots(neutral_paths)}",
    )
    report(
        "row-prefix-still-bounded-staging",
        row_prefix_still_staging,
        f"completed={package.get('completed_chunk_count')} ready={combiner.get('ready_chunks')} combined={combiner.get('combined_rows_written')}",
    )
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    checks = {
        "parent-certificates-present": not missing_parents,
        "parent-runners-have-no-fails": not failing_parents,
        "no-parent-authorizes-proposal": not proposal_allowed_parents,
        "inspected-head-is-current-pr-head": inspected_head == pr_head,
        "only-block28-support-since-block28-input-head": only_block28_support_since_input,
        "block28-exact-support-no-closure": block28_exact_support_no_closure,
        "degree-one-support-still-conditional": degree_one_support_still_conditional,
        "source-higgs-route-blocked-after-block28": source_higgs_route_blocked_after_block28,
        "wz-pivot-selected-after-source-higgs-block": wz_pivot_selected,
        "wz-pivot-not-admitted-without-required-packet": wz_pivot_not_admitted,
        "neutral-h3h4-route-not-admitted": neutral_not_admitted,
        "row-prefix-still-bounded-staging": row_prefix_still_staging,
        "forbidden-firewall-clean": firewall_clean,
    }

    result = {
        "actual_current_surface_status": (
            "open / block29 post-block28 W/Z pivot admission checkpoint; source-Higgs "
            "degree-one support is exact support only and the W/Z accepted-action "
            "response route is not admitted without the required production packet"
        ),
        "conditional_surface_status": (
            "source-Higgs support remains conditional on accepted same-surface "
            "EW/Higgs action or canonical O_H plus strict C_ss/C_sH/C_HH rows; "
            "W/Z support would require accepted action, production rows, "
            "same-source top rows, matched covariance, strict non-observed g2, "
            "delta_perp, and final W-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block29 is a pivot-admission checkpoint.  It verifies that block28 "
            "only supplied exact degree-one O_H support, then selects the W/Z "
            "accepted-action response route as the next fallback while recording "
            "that its accepted action, production W/Z rows, same-source top rows, "
            "matched covariance, strict non-observed g2, delta_perp, and final "
            "W-response authority are absent."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "checkpoint_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspected_head": inspected_head,
        "inspected_subject": inspected_subject,
        "pr_head": pr_head,
        "main_head": main_head,
        "block28_input_head": BLOCK28_INPUT_HEAD,
        "commits_since_block28_input": commits_since_block28_input,
        "paths_since_block28_input": paths_since_block28_input,
        "disallowed_paths_since_block28_input": disallowed_paths_since_block28_input,
        "route_admission": {
            "rank1_source_higgs": {
                "decision": "blocked_after_block28_exact_support",
                "missing": missing_roots(source_paths),
                "required_paths": source_paths,
            },
            "rank2_wz_accepted_action_response": {
                "decision": "pivot_selected_but_not_admitted_without_required_packet",
                "missing": missing_roots(wz_paths),
                "required_paths": wz_paths,
            },
            "rank3_neutral_h3h4": {
                "decision": "not_admitted",
                "missing": missing_roots(neutral_paths),
                "required_paths": neutral_paths,
            },
        },
        "row_prefix": {
            "completed_chunk_count": package.get("completed_chunk_count"),
            "completed_prefix_last": package.get("completed_prefix_last"),
            "ready_chunks": combiner.get("ready_chunks"),
            "expected_chunks": combiner.get("expected_chunks"),
            "combined_rows_written": combiner.get("combined_rows_written"),
            "closure_role": "bounded staging support only",
        },
        "checks": checks,
        "parents": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
        },
        "strict_non_claims": [
            "does not treat the degree-one theorem as an actual canonical O_H certificate",
            "does not identify taste-radial x with canonical O_H on the current surface",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not promote W/Z scout or smoke rows to production evidence",
            "does not treat additive-top coarse rows as matched covariance",
            "does not treat chunk063 completion alone as closure",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, u0, or unit matching conventions",
            "does not touch or inspect live chunk-worker output",
        ],
        "exact_next_action": (
            "Reopen the source-Higgs route only with accepted same-surface O_H "
            "action/operator authority plus strict C_ss/C_sH/C_HH rows.  If "
            "unavailable, continue the W/Z route only with accepted action, "
            "production W/Z rows, same-source top rows, matched covariance, "
            "strict non-observed g2, delta_perp, and final W-response authority."
        ),
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
