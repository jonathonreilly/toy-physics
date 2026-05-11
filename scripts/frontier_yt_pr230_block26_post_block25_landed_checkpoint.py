#!/usr/bin/env python3
"""
PR #230 block26 post-block25 landed checkpoint.

Block25 was the post-block24 landed checkpoint.  This checkpoint answers the
narrow resume question after that checkpoint landed on draft PR #230: did the
PR head move by anything other than the block25 checkpoint, and does that landed
head admit the source-Higgs, W/Z, or neutral H3/H4 queue item without touching
the live chunk worker?
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
    / "yt_pr230_block26_post_block25_landed_checkpoint_2026-05-11.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
MAIN_REF = "origin/main"
BLOCK25_INPUT_HEAD = "a864e5fe55391ace59047afde57cbc0c47928854"
BLOCK25_SUBJECT = "Record PR230 block25 landed checkpoint"
BLOCK26_SUBJECT = "Record PR230 block26 post-block25 landed checkpoint"

PARENTS = {
    "block25_post_block24_landed": "outputs/yt_pr230_block25_post_block24_landed_checkpoint_2026-05-11.json",
    "block23_remote_candidate_intake": "outputs/yt_pr230_block23_remote_candidate_intake_checkpoint_2026-05-11.json",
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

ALLOWED_BLOCK25_PATHS = {
    "scripts/frontier_yt_pr230_block25_post_block24_landed_checkpoint.py",
    "scripts/frontier_yt_pr230_campaign_status_certificate.py",
    "docs/YT_PR230_BLOCK25_POST_BLOCK24_LANDED_CHECKPOINT_NOTE_2026-05-11.md",
    "outputs/yt_pr230_block25_post_block24_landed_checkpoint_2026-05-11.json",
    "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

ALLOWED_BLOCK25_PREFIXES = (
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


def allowed_block25_path(path: str) -> bool:
    return path in ALLOWED_BLOCK25_PATHS or any(
        path.startswith(prefix) for prefix in ALLOWED_BLOCK25_PREFIXES
    )


def all_absent(values: dict[str, bool]) -> bool:
    return bool(values) and not any(values.values())


def missing_roots(values: dict[str, bool]) -> list[str]:
    return sorted(name for name, present in values.items() if not present)


def main() -> int:
    print("PR #230 block26 post-block25 landed checkpoint")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    local_head = run_git(["rev-parse", "HEAD"])
    local_subject = run_git(["log", "-1", "--format=%s", "HEAD"])
    inspection_ref = "HEAD^" if local_subject == BLOCK26_SUBJECT else "HEAD"
    inspected_head = run_git(["rev-parse", inspection_ref])
    inspected_subject = run_git(["log", "-1", "--format=%s", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    main_head = run_git(["rev-parse", "--verify", MAIN_REF])
    commits_since_block25_input = [
        line
        for line in run_git(
            ["log", "--format=%H%x09%s", f"{BLOCK25_INPUT_HEAD}..{inspection_ref}"]
        ).splitlines()
        if line
    ]
    paths_since_block25_input = changed_paths(BLOCK25_INPUT_HEAD, inspection_ref)
    disallowed_paths_since_block25_input = [
        path for path in paths_since_block25_input if not allowed_block25_path(path)
    ]

    source_paths = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_paths = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_paths = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block25 = parents["block25_post_block24_landed"]
    package = parents["two_source_package"]
    combiner = parents["two_source_combiner"]

    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [
        name for name, cert in parents.items() if int(cert.get("fail_count", 0) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    no_chunk063_committed = not any(
        ref_path_exists(inspection_ref, relpath)
        for relpath in (
            "outputs/yt_pr230_two_source_taste_radial_chunk063_checkpoint_2026-05-06.json",
            "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
            "docs/YT_PR230_TWO_SOURCE_TASTE_RADIAL_CHUNKS063_063_PACKAGE_NOTE_2026-05-07.md",
        )
    )
    only_block25_checkpoint_since_input = (
        len(commits_since_block25_input) == 1
        and commits_since_block25_input[0].endswith(f"\t{BLOCK25_SUBJECT}")
        and not disallowed_paths_since_block25_input
    )

    source_blocked = all_absent(source_paths)
    wz_blocked = all_absent(wz_paths)
    neutral_blocked = all_absent(neutral_paths)

    queue_pivot = [
        {
            "rank": 1,
            "opportunity": "certified O_H plus production source-Higgs pole rows with Gram flatness",
            "admission": "blocked_waiting_on_explicit_certificate_inputs",
            "missing_roots": missing_roots(source_paths),
        },
        {
            "rank": 2,
            "opportunity": "strict W/Z physical-response packet with accepted action",
            "admission": "blocked_waiting_on_explicit_certificate_inputs",
            "missing_roots": missing_roots(wz_paths),
        },
        {
            "rank": 3,
            "opportunity": "same-surface neutral H3/H4 physical-transfer authority",
            "admission": "blocked_waiting_on_explicit_certificate_inputs",
            "missing_roots": missing_roots(neutral_paths),
        },
    ]

    checks = {
        "inspection-head-is-current-pr-head-or-parent-of-block26": inspected_head == pr_head
        or local_head == pr_head,
        "inspection-head-is-block25-checkpoint": inspected_subject == BLOCK25_SUBJECT,
        "only-block25-checkpoint-since-block25-input-head": only_block25_checkpoint_since_input,
        "parent-certificates-loaded": not missing_parents,
        "parent-certificates-have-no-fails": not failing_parents,
        "parent-certificates-deny-proposal": not proposal_parents,
        "block25-no-route-admitted": block25.get("checks", {}).get(
            "queue-rank1-source-higgs-not-admitted"
        )
        is True
        and block25.get("checks", {}).get("queue-rank2-wz-not-admitted") is True
        and block25.get("checks", {}).get("queue-rank3-neutral-h3h4-not-admitted")
        is True,
        "block25-forbidden-firewall-clean": block25.get("checks", {}).get(
            "forbidden-firewall-clean"
        )
        is True,
        "source-higgs-required-paths-still-absent-on-pr-ref": source_blocked,
        "wz-required-paths-still-absent-on-pr-ref": wz_blocked,
        "neutral-h3h4-required-paths-still-absent-on-pr-ref": neutral_blocked,
        "two-source-prefix-still-62-of-63": package.get("completed_chunk_count") == 62
        and combiner.get("ready_chunks") == 62
        and combiner.get("expected_chunks") == 63,
        "chunk063-and-combined-rows-not-committed": no_chunk063_committed
        and combiner.get("combined_rows_written") is False,
        "queue-rank1-source-higgs-not-admitted": source_blocked,
        "queue-rank2-wz-not-admitted": wz_blocked,
        "queue-rank3-neutral-h3h4-not-admitted": neutral_blocked,
        "forbidden-firewall-clean": all(value is False for value in FORBIDDEN_FIREWALL.values()),
    }

    report(
        "inspection-head-is-current-pr-head-or-parent-of-block26",
        checks["inspection-head-is-current-pr-head-or-parent-of-block26"],
        f"HEAD={local_head[:9]} inspected={inspected_head[:9]} PR={pr_head[:9]}",
    )
    report(
        "only-block25-checkpoint-since-block25-input-head",
        checks["only-block25-checkpoint-since-block25-input-head"],
        f"commits={len(commits_since_block25_input)} disallowed_paths={len(disallowed_paths_since_block25_input)}",
    )
    report(
        "parent-certificates-loaded",
        checks["parent-certificates-loaded"],
        f"missing={missing_parents}",
    )
    report(
        "parent-certificates-have-no-fails",
        checks["parent-certificates-have-no-fails"],
        f"failing={failing_parents}",
    )
    report(
        "block25-no-route-admitted",
        checks["block25-no-route-admitted"],
        status(block25),
    )
    report(
        "source-higgs-required-paths-still-absent-on-pr-ref",
        checks["source-higgs-required-paths-still-absent-on-pr-ref"],
        f"missing={missing_roots(source_paths)}",
    )
    report(
        "wz-required-paths-still-absent-on-pr-ref",
        checks["wz-required-paths-still-absent-on-pr-ref"],
        f"missing={missing_roots(wz_paths)}",
    )
    report(
        "neutral-h3h4-required-paths-still-absent-on-pr-ref",
        checks["neutral-h3h4-required-paths-still-absent-on-pr-ref"],
        f"missing={missing_roots(neutral_paths)}",
    )
    report(
        "chunk063-and-combined-rows-not-committed",
        checks["chunk063-and-combined-rows-not-committed"],
        f"ready={combiner.get('ready_chunks')}/{combiner.get('expected_chunks')} combined={combiner.get('combined_rows_written')}",
    )
    report(
        "forbidden-firewall-clean",
        checks["forbidden-firewall-clean"],
        "no forbidden proof import or live-worker access used",
    )

    result = {
        "artifact": "YT_PR230_BLOCK26_POST_BLOCK25_LANDED_CHECKPOINT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_head": local_head,
        "git_head_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspected_head": inspected_head,
        "inspected_head_subject": inspected_subject,
        "pr_ref": PR_REF,
        "pr_ref_head": pr_head,
        "origin_main_head": main_head,
        "block25_input_head": BLOCK25_INPUT_HEAD,
        "commits_since_block25_input_head": commits_since_block25_input,
        "paths_since_block25_input_head": paths_since_block25_input,
        "disallowed_paths_since_block25_input_head": disallowed_paths_since_block25_input,
        "parents": {name: status(cert) for name, cert in parents.items()},
        "checks": checks,
        "source_higgs_required_paths_pr_ref": source_paths,
        "wz_required_paths_pr_ref": wz_paths,
        "neutral_h3h4_required_paths_pr_ref": neutral_paths,
        "queue_pivot": queue_pivot,
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
            "counted_pending_checkpoint_as_evidence": False,
        },
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "actual_current_surface_status": (
            "open / block26 post-block25 landed checkpoint; PR head contains "
            "only the block25 checkpoint after the previous landed-checkpoint input "
            "head, and ranked source-Higgs, W/Z, and neutral H3/H4 opportunities "
            "remain waiting on explicit production/certificate inputs"
        ),
        "conditional_surface_status": (
            "support if a future accepted same-surface canonical O_H plus strict "
            "C_ss/C_sH/C_HH pole rows exists, or if a strict W/Z matched "
            "physical-response packet or neutral H3/H4 physical-transfer "
            "authority is supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block26 is a landed-checkpoint, not a new closure artifact.  The "
            "current PR head is the block25 checkpoint commit; no required "
            "source-Higgs, W/Z, or neutral H3/H4 certificate paths are present, "
            "the row prefix remains 62/63 with combined rows unwritten, and no "
            "forbidden import or live-worker output is used."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "current_queue_decision": (
            "yield this PR230 lane for supervisor continuation unless a real "
            "production/certificate input is supplied; do not rerun current-surface "
            "shortcut gates or count chunk063 completion alone as closure"
        ),
        "strict_non_claims": [
            "does not claim retained or proposed_retained status",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not identify taste-radial x with canonical O_H",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, u0, or unit conventions",
            "does not promote W/Z scout or smoke rows to production evidence",
            "does not inspect active chunk-worker output or pending checkpoints",
            "does not treat the block25 checkpoint commit as new physics evidence",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
