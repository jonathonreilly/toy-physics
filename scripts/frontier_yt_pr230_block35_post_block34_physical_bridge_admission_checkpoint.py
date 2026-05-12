#!/usr/bin/env python3
"""
PR #230 block35 post-block34 physical-bridge admission checkpoint.

Block30 reduced the PR230 blocker to a missing same-surface physical map from
the PR230 source coordinate to canonical scalar/Higgs response.  The remote
branch then packaged chunk063, clarified no-go scope boundaries, refreshed the
complete-packet promotion contract, refreshed the OS transfer alias firewall,
and refreshed complete additive-top support.  This checkpoint consumes those
committed support-only inputs and checks whether the next campaign step is
actually admitted: source-Higgs with accepted O_H/action and strict pole rows,
strict W/Z matched physical response, or neutral H3/H4 physical-transfer
authority.

It intentionally does not inspect live chunk-worker output and does not rerun a
shortcut absence gate over untracked files.  It checks committed PR-head paths
only, records the precise missing production/certificate inputs, and yields the
lane unless one of those inputs is present.
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
    / "yt_pr230_block35_post_block34_physical_bridge_admission_checkpoint_2026-05-11.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
BLOCK29_HEAD = "22c2f326ca79f709a7b72f84961a0f6749779648"
BLOCK30_HEAD = "f7f42f27c16fd80db9b2c990294c7eb3c186423a"
BLOCK30_SUBJECT = "Record PR230 block30 full-approach bridge review"
BLOCK31_CHUNK_HEAD = "8a63348cc9fe71dac07a2eb0d1b39efe9227dfa6"
BLOCK31_CHUNK_SUBJECT = "Package PR230 two-source chunk063"
BLOCK31_SCOPE_HEAD = "20233ff2efa146386b0c7d07b1db24deae4b9a91"
BLOCK31_SCOPE_SUBJECT = "Clarify PR230 no-go scope boundaries"
BLOCK32_PROMOTION_HEAD = "4c4e91445254a4709ec93e268cf2415d7046cdeb"
BLOCK32_PROMOTION_SUBJECT = "Refresh PR230 complete-packet promotion contract"
BLOCK33_OS_TRANSFER_HEAD = "05feeafc01e475b38bc5a150278bd1eaddecbd88"
BLOCK33_OS_TRANSFER_SUBJECT = "Refresh PR230 OS transfer alias firewall"
BLOCK34_ADDITIVE_TOP_HEAD = "da3d6d8e3d022ad81d9f3f19d62ae8e9e87d8ebc"
BLOCK34_ADDITIVE_TOP_SUBJECT = "Refresh PR230 complete additive-top support"
BLOCK35_SUBJECT = "Record PR230 block35 physical bridge admission checkpoint"

PARENTS = {
    "block30_full_approach_review": "outputs/yt_pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review_2026-05-11.json",
    "block29_wz_pivot_admission": "outputs/yt_pr230_block29_post_block28_wz_pivot_admission_checkpoint_2026-05-11.json",
    "block28_degree_one_oh_support": "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json",
    "fms_oh_candidate_action": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "wz_accepted_action_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_physical_response_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
    "two_source_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "two_source_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "taste_radial_source_higgs_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "additive_top_subtraction_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

CHUNK063_SUPPORT_PATHS = {
    "chunk063_checkpoint": "outputs/yt_pr230_two_source_taste_radial_chunk063_checkpoint_2026-05-06.json",
    "chunk063_rows": "outputs/yt_pr230_two_source_taste_radial_rows/yt_pr230_two_source_taste_radial_rows_L12_T24_chunk063_2026-05-06.json",
    "combined_taste_radial_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
}

PROMOTION_CONTRACT_SUPPORT_PATHS = {
    "promotion_contract_certificate": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "promotion_contract_runner": "scripts/frontier_yt_pr230_taste_radial_to_source_higgs_promotion_contract.py",
    "promotion_contract_note": "docs/YT_PR230_TASTE_RADIAL_TO_SOURCE_HIGGS_PROMOTION_CONTRACT_NOTE_2026-05-07.md",
}

OS_TRANSFER_SUPPORT_PATHS = {
    "os_transfer_kernel_gate_certificate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "os_transfer_kernel_gate_runner": "scripts/frontier_yt_pr230_os_transfer_kernel_artifact_gate.py",
    "os_transfer_kernel_gate_note": "docs/YT_PR230_OS_TRANSFER_KERNEL_ARTIFACT_GATE_NOTE_2026-05-07.md",
}

ADDITIVE_TOP_SUPPORT_PATHS = {
    "additive_top_jacobian_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "additive_top_jacobian_runner": "scripts/frontier_yt_pr230_additive_top_jacobian_row_builder.py",
    "additive_top_jacobian_note": "docs/YT_PR230_ADDITIVE_TOP_JACOBIAN_ROW_BUILDER_NOTE_2026-05-07.md",
    "additive_top_subtraction_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "additive_top_subtraction_runner": "scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py",
    "additive_top_subtraction_note": "docs/YT_PR230_ADDITIVE_TOP_SUBTRACTION_ROW_CONTRACT_NOTE_2026-05-07.md",
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


def missing_roots(presence: dict[str, bool]) -> list[str]:
    return sorted(name for name, is_present in presence.items() if not is_present)


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


def commit_subject(line: str) -> str:
    return line.split("\t", 1)[1] if "\t" in line else line


def main() -> int:
    print("PR #230 block35 post-block34 physical-bridge admission checkpoint")
    print("=" * 82)

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
    inspection_ref = "HEAD^" if local_subject == BLOCK35_SUBJECT else "HEAD"
    inspection_head = run_git(["rev-parse", inspection_ref])
    inspection_subject = run_git(["log", "-1", "--format=%s", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])

    commits_since_block29 = commits(BLOCK29_HEAD, inspection_ref)
    commits_since_block30 = commits(BLOCK30_HEAD, inspection_ref)
    source_presence = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_presence = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_presence = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)
    chunk063_presence = present_at_ref(inspection_ref, CHUNK063_SUPPORT_PATHS)
    promotion_presence = present_at_ref(inspection_ref, PROMOTION_CONTRACT_SUPPORT_PATHS)
    os_transfer_presence = present_at_ref(inspection_ref, OS_TRANSFER_SUPPORT_PATHS)
    additive_top_presence = present_at_ref(inspection_ref, ADDITIVE_TOP_SUPPORT_PATHS)

    block30_parent_clean = (
        parents["block30_full_approach_review"].get("proposal_allowed") is False
        and parents["block30_full_approach_review"].get("bare_retained_allowed") is False
        and parents["block30_full_approach_review"].get("fails") == 0
        and "same-surface physical map from the PR230 source coordinate"
        in str(
            parents["block30_full_approach_review"]
            .get("elon_exercise", {})
            .get("irreducible_missing_object")
        )
    )
    post_block30_subjects = {commit_subject(line) for line in commits_since_block30}
    post_block30_support_only_inputs = post_block30_subjects == {
        BLOCK31_CHUNK_SUBJECT,
        BLOCK31_SCOPE_SUBJECT,
        BLOCK32_PROMOTION_SUBJECT,
        BLOCK33_OS_TRANSFER_SUBJECT,
        BLOCK34_ADDITIVE_TOP_SUBJECT,
    }
    chunk063_support_committed = all_present(chunk063_presence)
    promotion_contract_committed = all_present(promotion_presence)
    os_transfer_support_committed = all_present(os_transfer_presence)
    additive_top_support_committed = all_present(additive_top_presence)
    source_admitted = source_higgs_admitted(source_presence)
    wz_admitted = all_present(wz_presence)
    neutral_admitted = all_present(neutral_presence)
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    no_route_admitted = not (source_admitted or wz_admitted or neutral_admitted)

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("block30-parent-clean", block30_parent_clean, status(parents["block30_full_approach_review"]))
    report("post-block30-inputs-support-only", post_block30_support_only_inputs, str(commits_since_block30))
    report("chunk063-package-committed-support-only", chunk063_support_committed, str(chunk063_presence))
    report("promotion-contract-committed-support-only", promotion_contract_committed, str(promotion_presence))
    report("os-transfer-alias-firewall-committed-support-only", os_transfer_support_committed, str(os_transfer_presence))
    report("additive-top-support-committed-support-only", additive_top_support_committed, str(additive_top_presence))
    report("source-higgs-physical-bridge-not-admitted", not source_admitted, str(source_presence))
    report("wz-physical-response-not-admitted", not wz_admitted, str(wz_presence))
    report("neutral-h3h4-not-admitted", not neutral_admitted, str(neutral_presence))
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("no-route-admitted-without-explicit-input", no_route_admitted, "ranked queue requires new physical bridge input")

    result = {
        "actual_current_surface_status": (
            "open / block35 post-block34 physical-bridge admission checkpoint; "
            "chunk063, no-go-scope, promotion-contract, OS-transfer-alias "
            "firewall, and additive-top commits are support only and no physical "
            "bridge is admitted"
        ),
        "conditional_surface_status": (
            "support if a future accepted same-surface O_H/action plus strict "
            "C_ss/C_sH/C_HH rows lands, or if a strict W/Z physical-response "
            "packet or neutral H3/H4 physical-transfer authority lands"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block35 is an admission/yield checkpoint after the committed chunk063 "
            "package, no-go scope clarification, and complete-packet promotion "
            "contract, OS transfer alias firewall, and additive-top support "
            "refreshes.  The PR head still has no accepted same-surface "
            "O_H/action, strict source-Higgs pole rows, strict W/Z matched "
            "response packet, or neutral H3/H4 physical-transfer certificate."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "block35_post_block34_physical_bridge_admission_checkpoint_passed": FAIL_COUNT == 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspection_head": inspection_head,
        "inspection_subject": inspection_subject,
        "pr_ref": PR_REF,
        "pr_head": pr_head,
        "block30_head": BLOCK30_HEAD,
        "block31_chunk_head": BLOCK31_CHUNK_HEAD,
        "block31_scope_head": BLOCK31_SCOPE_HEAD,
        "block32_promotion_head": BLOCK32_PROMOTION_HEAD,
        "block33_os_transfer_head": BLOCK33_OS_TRANSFER_HEAD,
        "block34_additive_top_head": BLOCK34_ADDITIVE_TOP_HEAD,
        "commits_since_block29_input": commits_since_block29,
        "commits_since_block30_head": commits_since_block30,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "chunk063_support": {
            "committed": chunk063_support_committed,
            "support_paths": CHUNK063_SUPPORT_PATHS,
            "committed_path_presence": chunk063_presence,
            "decision": (
                "support only; chunk063 completes the taste-radial C_sx/C_xx packet "
                "but does not certify x=O_H or C_sH/C_HH pole rows"
            ),
        },
        "promotion_contract_support": {
            "committed": promotion_contract_committed,
            "support_paths": PROMOTION_CONTRACT_SUPPORT_PATHS,
            "committed_path_presence": promotion_presence,
            "decision": (
                "support only; the complete-packet promotion contract preserves "
                "the requirement for accepted x=O_H/canonical-Higgs authority "
                "and strict C_ss/C_sH/C_HH pole rows"
            ),
        },
        "os_transfer_alias_firewall_support": {
            "committed": os_transfer_support_committed,
            "support_paths": OS_TRANSFER_SUPPORT_PATHS,
            "committed_path_presence": os_transfer_presence,
            "decision": (
                "support only; the OS transfer kernel gate blocks equal-time "
                "C_ss/C_sx/C_xx rows from being treated as a same-surface "
                "transfer kernel or pole residue"
            ),
        },
        "additive_top_support": {
            "committed": additive_top_support_committed,
            "support_paths": ADDITIVE_TOP_SUPPORT_PATHS,
            "committed_path_presence": additive_top_presence,
            "decision": (
                "support only; additive-top rows and subtraction contract still "
                "require accepted action, W/Z response rows, strict g2, and "
                "matched covariance before a physical response can be admitted"
            ),
        },
        "source_higgs_bridge": {
            "admitted": source_admitted,
            "required_paths": SOURCE_HIGGS_REQUIRED_PATHS,
            "committed_path_presence": source_presence,
            "missing_roots": missing_roots(source_presence),
            "decision": (
                "not admitted; reopen only with accepted O_H/action, canonical "
                "operator authority, strict C_ss/C_sH/C_HH pole rows, and "
                "Gram/FV/IR authority"
            ),
        },
        "wz_physical_response_bridge": {
            "admitted": wz_admitted,
            "required_paths": WZ_REQUIRED_PATHS,
            "committed_path_presence": wz_presence,
            "missing_roots": missing_roots(wz_presence),
            "decision": (
                "not admitted; continue only with accepted action, production "
                "W/Z rows, same-source top rows, matched covariance, strict "
                "non-observed g2, delta_perp, and final W-response rows"
            ),
        },
        "neutral_h3h4_bridge": {
            "admitted": neutral_admitted,
            "required_paths": NEUTRAL_H3H4_REQUIRED_PATHS,
            "committed_path_presence": neutral_presence,
            "missing_roots": missing_roots(neutral_presence),
            "decision": (
                "not admitted; reopen only with same-surface physical transfer "
                "and source/canonical-Higgs coupling authority"
            ),
        },
        "campaign_decision": {
            "rank1_source_higgs": "waiting on explicit physical bridge input",
            "rank2_wz": "waiting on explicit accepted-action physical-response packet",
            "rank3_neutral_h3h4": "waiting on physical transfer/coupling certificate",
            "yield_for_supervisor": True,
            "next_exact_action": (
                "Supply one committed physical bridge artifact: accepted same-surface "
                "O_H/action plus strict C_ss/C_sH/C_HH rows, strict W/Z matched "
                "physical response, or neutral H3/H4 physical-transfer authority."
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
            "block30-parent-clean": block30_parent_clean,
            "post-block30-inputs-support-only": post_block30_support_only_inputs,
            "chunk063-package-committed-support-only": chunk063_support_committed,
            "promotion-contract-committed-support-only": promotion_contract_committed,
            "os-transfer-alias-firewall-committed-support-only": os_transfer_support_committed,
            "additive-top-support-committed-support-only": additive_top_support_committed,
            "source-higgs-physical-bridge-not-admitted": not source_admitted,
            "wz-physical-response-not-admitted": not wz_admitted,
            "neutral-h3h4-not-admitted": not neutral_admitted,
            "forbidden-firewall-clean": firewall_clean,
            "no-route-admitted-without-explicit-input": no_route_admitted,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not treat block30 route review as physical bridge evidence",
            "does not treat chunk063 completion, the promotion contract, the OS transfer alias firewall, or additive-top support as physical bridge evidence",
            "does not inspect live or untracked chunk-worker output",
            "does not treat C_sx/C_xx rows as C_sH/C_HH before x=O_H is certified",
            "does not use Ward, H_unit, y_t_bare, observed targets, observed g2, alpha_LM, plaquette, u0, or unit conventions",
        ],
        "passes": PASS_COUNT,
        "fails": FAIL_COUNT,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
