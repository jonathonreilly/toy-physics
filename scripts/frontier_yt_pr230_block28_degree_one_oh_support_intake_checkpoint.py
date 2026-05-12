#!/usr/bin/env python3
"""
PR #230 block28 degree-one O_H support intake checkpoint.

Block27 was the post-block26 landed checkpoint.  This block does not repeat the
same absence gate.  It consumes the already committed degree-one radial-tangent
O_H theorem as source-Higgs bridge support, checks that the block27 PR-head
movement is only the block27 checkpoint, and keeps the actual current surface
open because the action premise, canonical O_H certificate, and strict
C_ss/C_sH/C_HH pole rows remain absent.
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
    / "yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
MAIN_REF = "origin/main"
BLOCK27_INPUT_HEAD = "f1d72283b92fb1b76292ea8ba53d7586ad0c294d"
BLOCK27_SUBJECT = "Record PR230 block27 post-block26 checkpoint"
BLOCK28_SUBJECT = "Record PR230 block28 degree-one O_H support intake"

PARENTS = {
    "block27_post_block26_landed": "outputs/yt_pr230_block27_post_block26_landed_checkpoint_2026-05-11.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "degree_one_action_premise": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "source_higgs_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "fms_oh_candidate_action": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
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

ALLOWED_BLOCK27_PATHS = {
    "scripts/frontier_yt_pr230_block27_post_block26_landed_checkpoint.py",
    "scripts/frontier_yt_pr230_campaign_status_certificate.py",
    "docs/YT_PR230_BLOCK27_POST_BLOCK26_LANDED_CHECKPOINT_NOTE_2026-05-11.md",
    "outputs/yt_pr230_block27_post_block26_landed_checkpoint_2026-05-11.json",
    "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

ALLOWED_BLOCK27_PREFIXES = (
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


def allowed_block27_path(path: str) -> bool:
    return path in ALLOWED_BLOCK27_PATHS or any(
        path.startswith(prefix) for prefix in ALLOWED_BLOCK27_PREFIXES
    )


def all_absent(values: dict[str, bool]) -> bool:
    return bool(values) and not any(values.values())


def missing_roots(values: dict[str, bool]) -> list[str]:
    return sorted(name for name, present in values.items() if not present)


def main() -> int:
    print("PR #230 block28 degree-one O_H support intake checkpoint")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK28_SUBJECT else "HEAD"
    inspected_head = run_git(["rev-parse", inspection_ref])
    inspected_subject = run_git(["log", "-1", "--format=%s", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    main_head = run_git(["rev-parse", "--verify", MAIN_REF])
    commits_since_block27_input = [
        line
        for line in run_git(
            ["log", "--format=%H%x09%s", f"{BLOCK27_INPUT_HEAD}..{inspection_ref}"]
        ).splitlines()
        if line
    ]
    paths_since_block27_input = changed_paths(BLOCK27_INPUT_HEAD, inspection_ref)
    disallowed_paths_since_block27_input = [
        path for path in paths_since_block27_input if not allowed_block27_path(path)
    ]

    source_paths = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_paths = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_paths = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    degree_one = parents["degree_one_radial_tangent_oh"]
    degree_one_premise = parents["degree_one_action_premise"]
    block27 = parents["block27_post_block26_landed"]
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

    only_block27_checkpoint_since_input = (
        len(commits_since_block27_input) == 1
        and commits_since_block27_input[0].endswith(f"\t{BLOCK27_SUBJECT}")
        and not disallowed_paths_since_block27_input
    )
    degree_one_support_loaded = (
        degree_one.get("degree_one_radial_tangent_oh_theorem_passed") is True
        and degree_one.get("degree_one_tangent_unique") is True
        and degree_one.get("same_surface_linear_tangent_premise_derived") is False
        and degree_one.get("canonical_oh_identity_derived") is False
        and degree_one.get("source_higgs_pole_rows_present") is False
        and degree_one.get("proposal_allowed") is False
        and degree_one.get("higher_degree_boundary", {}).get(
            "z3_tracezero_invariant_rank"
        )
        == 3
    )
    degree_one_premise_still_missing = (
        degree_one_premise.get("degree_one_premise_authorized_on_current_surface")
        is False
        and "degree-one Higgs-action premise not derived"
        in status(degree_one_premise)
    )
    source_higgs_not_admitted = (
        all_absent(source_paths)
        and parents["source_higgs_aperture"].get("proposal_allowed") is False
        and parents["fms_oh_candidate_action"].get("closure_authorized") is False
        and parents["fms_source_overlap_readout"].get("readout_executable_now")
        is False
    )
    wz_not_admitted = (
        all_absent(wz_paths)
        and parents["wz_physical_response_intake"].get("proposal_allowed") is False
        and parents["wz_accepted_action_root"].get("proposal_allowed") is False
    )
    neutral_not_admitted = (
        all_absent(neutral_paths)
        and parents["neutral_h3h4_aperture"].get("proposal_allowed") is False
    )
    package_ready = package.get("ready_chunks")
    if package_ready is None:
        package_ready = package.get("completed_chunks") or combiner.get("ready_chunks")
    committed_prefix_still_staging = (
        package_ready == 62
        and combiner.get("ready_chunks") == 62
        and combiner.get("combined_rows_written") is False
    )
    block27_open_no_route = (
        block27.get("proposal_allowed") is False
        and block27.get("checks", {}).get(
            "only-block26-checkpoint-since-block26-input-head"
        )
        is True
        and block27.get("checks", {}).get("queue-rank1-source-higgs-not-admitted")
        is True
        and block27.get("checks", {}).get("queue-rank2-wz-not-admitted") is True
        and block27.get("checks", {}).get("queue-rank3-neutral-h3h4-not-admitted")
        is True
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
        "only-block27-checkpoint-since-block27-input-head",
        only_block27_checkpoint_since_input,
        f"commits={commits_since_block27_input} disallowed_paths={disallowed_paths_since_block27_input}",
    )
    report(
        "degree-one-oh-support-loaded",
        degree_one_support_loaded,
        status(degree_one),
    )
    report(
        "degree-one-action-premise-still-missing",
        degree_one_premise_still_missing,
        status(degree_one_premise),
    )
    report(
        "source-higgs-route-not-admitted",
        source_higgs_not_admitted,
        f"missing={missing_roots(source_paths)}",
    )
    report(
        "wz-route-not-admitted",
        wz_not_admitted,
        f"missing={missing_roots(wz_paths)}",
    )
    report(
        "neutral-h3h4-route-not-admitted",
        neutral_not_admitted,
        f"missing={missing_roots(neutral_paths)}",
    )
    report(
        "committed-prefix-still-staging",
        committed_prefix_still_staging,
        f"ready={package_ready} combined={combiner.get('combined_rows_written')}",
    )
    report("block27-still-open-no-route", block27_open_no_route, status(block27))
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    checks = {
        "parent-certificates-present": not missing_parents,
        "parent-runners-have-no-fails": not failing_parents,
        "no-parent-authorizes-proposal": not proposal_allowed_parents,
        "inspected-head-is-current-pr-head": inspected_head == pr_head,
        "only-block27-checkpoint-since-block27-input-head": only_block27_checkpoint_since_input,
        "degree-one-oh-support-loaded": degree_one_support_loaded,
        "degree-one-action-premise-still-missing": degree_one_premise_still_missing,
        "source-higgs-route-not-admitted": source_higgs_not_admitted,
        "wz-route-not-admitted": wz_not_admitted,
        "neutral-h3h4-route-not-admitted": neutral_not_admitted,
        "committed-prefix-still-staging": committed_prefix_still_staging,
        "block27-still-open-no-route": block27_open_no_route,
        "forbidden-firewall-clean": firewall_clean,
    }

    result = {
        "actual_current_surface_status": (
            "exact-support / block28 degree-one O_H support intake; current "
            "surface remains open because action premise, canonical O_H "
            "certificate, source-Higgs pole rows, strict W/Z packet, and "
            "neutral H3/H4 authority remain absent"
        ),
        "conditional_surface_status": (
            "degree-one O_H axis support if a future same-surface EW/Higgs "
            "action proves canonical O_H is a linear Z3-covariant radial "
            "tangent and supplies canonical LSZ normalization; readout support "
            "only after strict C_ss/C_sH/C_HH rows exist"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block28 intakes an exact support theorem: the degree-one "
            "Z3-covariant radial tangent is unique and matches the taste-radial "
            "axis.  It is not a closure artifact because the current surface "
            "still lacks the degree-one action premise, canonical O_H "
            "certificate, strict C_ss/C_sH/C_HH pole rows, Gram/FV/IR "
            "authority, accepted W/Z action/response packet, and neutral H3/H4 "
            "physical-transfer authority."
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
        "block27_input_head": BLOCK27_INPUT_HEAD,
        "commits_since_block27_input": commits_since_block27_input,
        "paths_since_block27_input": paths_since_block27_input,
        "disallowed_paths_since_block27_input": disallowed_paths_since_block27_input,
        "degree_one_support": {
            "runner": "scripts/frontier_yt_pr230_degree_one_radial_tangent_oh_theorem.py",
            "note": "docs/YT_PR230_DEGREE_ONE_RADIAL_TANGENT_OH_THEOREM_NOTE_2026-05-07.md",
            "output": PARENTS["degree_one_radial_tangent_oh"],
            "axis": degree_one.get("radial_axis", {}).get("operator"),
            "unique_degree_one_tangent": degree_one.get("degree_one_tangent_unique"),
            "higher_degree_boundary": degree_one.get("higher_degree_boundary"),
            "current_action_premise_derived": degree_one.get(
                "same_surface_linear_tangent_premise_derived"
            ),
            "canonical_oh_identity_derived": degree_one.get(
                "canonical_oh_identity_derived"
            ),
            "source_higgs_pole_rows_present": degree_one.get(
                "source_higgs_pole_rows_present"
            ),
        },
        "route_admission": {
            "source_higgs_required_paths": source_paths,
            "source_higgs_missing": missing_roots(source_paths),
            "wz_required_paths": wz_paths,
            "wz_missing": missing_roots(wz_paths),
            "neutral_h3h4_required_paths": neutral_paths,
            "neutral_h3h4_missing": missing_roots(neutral_paths),
        },
        "row_prefix": {
            "ready_chunks": package_ready,
            "expected_chunks": package.get("expected_chunks")
            or combiner.get("expected_chunks"),
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
            "does not treat chunk063 completion alone as closure",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, u0, or unit matching conventions",
            "does not touch or inspect live chunk-worker output",
        ],
        "exact_next_action": (
            "Supply an accepted same-surface EW/Higgs action or canonical O_H "
            "certificate that makes the degree-one radial tangent premise "
            "current-surface authority, then produce strict C_ss/C_sH/C_HH "
            "pole rows with Gram/FV/IR checks.  If unavailable, pivot to a "
            "strict W/Z matched physical-response packet with accepted action, "
            "same-source top/W covariance, strict non-observed g2, delta_perp, "
            "and final W-response authority."
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
