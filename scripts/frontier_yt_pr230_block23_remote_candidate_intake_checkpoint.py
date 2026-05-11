#!/usr/bin/env python3
"""
PR #230 block23 remote-candidate intake checkpoint.

This checkpoint resumes after block22 and asks whether the current PR head or
freshly fetched remote surfaces contain an admissible canonical O_H/source-Higgs
packet or strict W/Z accepted-action response packet.  It reads only committed
certificates and git refs.  It does not inspect active chunk-worker output.
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
    / "yt_pr230_block23_remote_candidate_intake_checkpoint_2026-05-11.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
MAIN_REF = "origin/main"
BLOCK22_PR_BODY_HEAD = "0c266edf474e303e85defbd48a13913c910a08ba"

PARENTS = {
    "fresh_artifact_intake": "outputs/yt_pr230_fresh_artifact_intake_checkpoint_2026-05-07.json",
    "source_higgs_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "fms_oh_candidate_action": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "fms_action_adoption_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_same_source_action_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
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

ALL_REQUIRED_PATHS = {
    **{f"source_higgs:{key}": path for key, path in SOURCE_HIGGS_REQUIRED_PATHS.items()},
    **{f"wz:{key}": path for key, path in WZ_REQUIRED_PATHS.items()},
    **{f"neutral:{key}": path for key, path in NEUTRAL_H3H4_REQUIRED_PATHS.items()},
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
    "inspected_active_chunk_output": False,
}

REMOTE_RELEVANT_TERMS = (
    "pr230",
    "yt-direct-lattice-correlator",
    "source-higgs",
    "source_higgs",
    "canonical-oh",
    "canonical_oh",
    " oh ",
    "wz",
    "w/z",
    "top-yukawa",
    "higgs",
)
REMOTE_ADMISSIBLE_TERMS = (
    "pr230",
    "yt-direct-lattice-correlator",
    "source-higgs",
    "source_higgs",
    "canonical-oh",
    "canonical_oh",
    "wz",
    "w/z",
)

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


def load_json(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present_local(paths: dict[str, str]) -> dict[str, bool]:
    return {name: (ROOT / relpath).exists() for name, relpath in paths.items()}


def present_at_ref(ref: str, paths: dict[str, str]) -> dict[str, bool]:
    if not run_git(["rev-parse", "--verify", ref]):
        return {name: False for name in paths}
    return {name: ref_path_exists(ref, relpath) for name, relpath in paths.items()}


def all_present(values: dict[str, bool]) -> bool:
    return bool(values) and all(values.values())


def remote_refs() -> list[dict[str, Any]]:
    fmt = "%(committerdate:unix)%09%(committerdate:iso8601)%09%(refname:short)%09%(objectname:short)%09%(subject)"
    raw = run_git(["for-each-ref", f"--format={fmt}", "refs/remotes/origin"])
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines():
        parts = line.split("\t", 4)
        if len(parts) != 5:
            continue
        unix_s, date_s, ref, oid, subject = parts
        text = f"{ref} {subject}".lower()
        if not any(term in text for term in REMOTE_RELEVANT_TERMS):
            continue
        try:
            unix_time = int(unix_s)
        except ValueError:
            unix_time = 0
        rows.append(
            {
                "unix_time": unix_time,
                "date": date_s,
                "ref": ref,
                "oid": oid,
                "subject": subject,
                "admissible_name_scope": any(
                    term in text for term in REMOTE_ADMISSIBLE_TERMS
                ),
            }
        )
    rows.sort(key=lambda row: (row["unix_time"], row["ref"]), reverse=True)
    return rows


def ref_required_path_summary(ref: str) -> dict[str, Any]:
    source = present_at_ref(ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz = present_at_ref(ref, WZ_REQUIRED_PATHS)
    neutral = present_at_ref(ref, NEUTRAL_H3H4_REQUIRED_PATHS)
    return {
        "source_higgs_paths_present": sorted(key for key, value in source.items() if value),
        "wz_paths_present": sorted(key for key, value in wz.items() if value),
        "neutral_paths_present": sorted(key for key, value in neutral.items() if value),
        "strict_source_higgs_packet_present": all_present(source),
        "strict_wz_packet_present": all_present(wz),
        "strict_neutral_h3h4_packet_present": all_present(neutral),
    }


def branch_candidate_summary() -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for row in remote_refs():
        summary = ref_required_path_summary(str(row["ref"]))
        summaries.append({**row, **summary})
    return summaries


def main() -> int:
    print("PR #230 block23 remote-candidate intake checkpoint")
    print("=" * 72)

    parents = {name: load_json(relpath) for name, relpath in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    failing_parents = [
        name for name, cert in parents.items() if int(cert.get("fail_count", 0) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    local_head = run_git(["rev-parse", "HEAD"])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])
    main_head = run_git(["rev-parse", "--verify", MAIN_REF])
    head_subject = run_git(["log", "-1", "--pretty=%s"])

    source_local = present_local(SOURCE_HIGGS_REQUIRED_PATHS)
    wz_local = present_local(WZ_REQUIRED_PATHS)
    neutral_local = present_local(NEUTRAL_H3H4_REQUIRED_PATHS)
    source_pr = present_at_ref(PR_REF, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_pr = present_at_ref(PR_REF, WZ_REQUIRED_PATHS)
    neutral_pr = present_at_ref(PR_REF, NEUTRAL_H3H4_REQUIRED_PATHS)
    required_path_local_presence = present_local(ALL_REQUIRED_PATHS)

    candidates = branch_candidate_summary()
    admissible_candidates = [
        row
        for row in candidates
        if row.get("admissible_name_scope")
        and (
            row.get("source_higgs_paths_present")
            or row.get("wz_paths_present")
            or row.get("neutral_paths_present")
        )
    ]
    strict_source_refs = [
        str(row["ref"]) for row in candidates if row.get("strict_source_higgs_packet_present")
    ]
    strict_wz_refs = [
        str(row["ref"]) for row in candidates if row.get("strict_wz_packet_present")
    ]
    strict_neutral_refs = [
        str(row["ref"]) for row in candidates if row.get("strict_neutral_h3h4_packet_present")
    ]

    combiner = parents["two_source_combiner"]
    source = parents["source_higgs_aperture"]
    fresh = parents["fresh_artifact_intake"]
    fms_action = parents["fms_oh_candidate_action"]
    fms_readout = parents["fms_source_overlap_readout"]
    fms_cut = parents["fms_action_adoption_cut"]
    wz_intake = parents["wz_physical_response_intake"]
    wz_root = parents["wz_action_root"]
    neutral = parents["neutral_h3h4_aperture"]

    ready_chunks = (
        fresh.get("source_higgs_route", {})
        .get("two_source_prefix", {})
        .get("ready_chunks")
    )
    expected_chunks = (
        fresh.get("source_higgs_route", {})
        .get("two_source_prefix", {})
        .get("expected_chunks")
    )

    checks = {
        "parent-certificates-loaded": not missing_parents,
        "parent-certificates-have-no-fails": not failing_parents,
        "parent-certificates-deny-proposal": not proposal_parents,
        "local-head-matches-pr-head": bool(local_head and local_head == pr_head),
        "block22-pr-body-head-is-ancestor": git_ok(
            ["merge-base", "--is-ancestor", BLOCK22_PR_BODY_HEAD, "HEAD"]
        ),
        "source-higgs-required-paths-absent-locally": not any(source_local.values()),
        "source-higgs-required-paths-absent-on-pr-ref": not any(source_pr.values()),
        "wz-required-paths-absent-locally": not any(wz_local.values()),
        "wz-required-paths-absent-on-pr-ref": not any(wz_pr.values()),
        "neutral-h3h4-required-paths-absent-locally": not any(neutral_local.values()),
        "neutral-h3h4-required-paths-absent-on-pr-ref": not any(neutral_pr.values()),
        "no-candidate-ref-has-strict-source-packet": not strict_source_refs,
        "no-candidate-ref-has-strict-wz-packet": not strict_wz_refs,
        "no-candidate-ref-has-strict-neutral-packet": not strict_neutral_refs,
        "no-admissible-remote-required-paths-found": not admissible_candidates,
        "fresh-intake-still-no-closure-artifact": fresh.get("checks", {}).get(
            "no_closure_artifact_present"
        )
        is True,
        "source-higgs-aperture-still-open": source.get("proposal_allowed") is False
        and source.get("current_surface_closure_satisfied") is False,
        "fms-candidate-still-conditional": fms_action.get("proposal_allowed") is False
        and fms_action.get("accepted_current_surface") is False
        and fms_action.get("closure_authorized") is False,
        "fms-readout-not-executable-now": fms_readout.get("proposal_allowed") is False
        and fms_readout.get("readout_executable_now") is False,
        "fms-action-cut-not-adopted": fms_cut.get("proposal_allowed") is False
        and fms_cut.get("accepted_current_surface") is False,
        "wz-packet-still-absent": wz_intake.get("proposal_allowed") is False
        and wz_intake.get("production_packet_present") is False,
        "wz-accepted-action-root-still-open": wz_root.get("proposal_allowed") is False,
        "neutral-h3h4-still-open": neutral.get("proposal_allowed") is False
        and neutral.get("current_surface_closure_satisfied") is False,
        "two-source-prefix-still-62-of-63": ready_chunks == 62
        and expected_chunks == 63
        and combiner.get("combined_rows_written") is False,
        "chunk063-completed-checkpoint-absent": not (
            ROOT / "outputs" / "yt_pr230_two_source_taste_radial_chunk063_checkpoint_2026-05-06.json"
        ).exists(),
        "forbidden-firewall-clean": not any(FORBIDDEN_FIREWALL.values()),
    }

    for name, ok in checks.items():
        report(name, bool(ok), "ok" if ok else "failed")

    result = {
        "artifact": "YT_PR230_BLOCK23_REMOTE_CANDIDATE_INTAKE_CHECKPOINT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_head": local_head,
        "git_head_subject": head_subject,
        "pr_ref": PR_REF,
        "pr_ref_head": pr_head,
        "origin_main_head": main_head,
        "actual_current_surface_status": (
            "open / block23 remote-candidate intake checkpoint; current PR head "
            "and fetched remote candidate refs contain no admissible canonical "
            "O_H/source-Higgs packet, strict W/Z accepted-action response packet, "
            "or neutral H3/H4 physical-transfer packet"
        ),
        "conditional_surface_status": (
            "support if a future fetched branch or PR head supplies accepted "
            "same-surface canonical O_H plus production C_ss/C_sH/C_HH pole "
            "rows with Gram/FV/IR authority, a strict W/Z matched physical-"
            "response packet with strict non-observed g2 and delta_perp "
            "authority, or neutral H3/H4 physical-transfer authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block23 is a committed-surface and fetched-ref intake checkpoint. "
            "It found no accepted same-surface O_H/action authority, no strict "
            "C_ss/C_sH/C_HH pole-row packet, no accepted W/Z action/response "
            "packet, no matched top/W covariance, no strict non-observed g2, "
            "no delta_perp authority, and no H3/H4 physical-transfer packet."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "parents": {name: status(cert) for name, cert in parents.items()},
        "source_higgs_required_paths_local": source_local,
        "source_higgs_required_paths_pr_ref": source_pr,
        "wz_required_paths_local": wz_local,
        "wz_required_paths_pr_ref": wz_pr,
        "neutral_h3h4_required_paths_local": neutral_local,
        "neutral_h3h4_required_paths_pr_ref": neutral_pr,
        "required_path_local_presence": required_path_local_presence,
        "remote_candidate_refs": candidates,
        "remote_candidate_refs_sample": candidates[:30],
        "admissible_remote_refs_with_required_paths": admissible_candidates,
        "strict_source_higgs_packet_refs": strict_source_refs,
        "strict_wz_packet_refs": strict_wz_refs,
        "strict_neutral_h3h4_packet_refs": strict_neutral_refs,
        "current_queue_decision": (
            "yield this PR230 lane as waiting on explicit production/certificate "
            "inputs; do not rerun more current-surface shortcut gates or count "
            "chunk063 completion alone as closure"
        ),
        "live_chunk_worker": {
            "touched": False,
            "inspected_active_output": False,
            "note": "Only committed outputs and fetched git refs were inspected.",
        },
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "checks": checks,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use yt_ward_identity, H_unit, y_t_bare, observed target values, observed g2, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, g2, or delta_perp by convention",
            "does not identify taste-radial x with canonical O_H",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not promote W/Z scout or smoke rows to production response evidence",
            "does not touch or inspect live chunk-worker output",
        ],
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
