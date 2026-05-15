#!/usr/bin/env python3
"""
PR #230 post-Block100 completion/reopen audit.

This runner maps the active objective, "resume positive closure on PR #230",
to concrete branch artifacts after the final higher-shell chunk packet and the
Block100 W/Z explicit-v firewall.  It is not a closure proof.  It verifies
that chunk production is complete, then checks whether any current or fetched
remote surface supplies a named same-surface artifact that could reopen a clean
positive-closure route.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_post_block100_completion_reopen_audit_2026-05-15.json"

PARENTS = {
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "assumption_import_stress": "outputs/yt_pr230_assumption_import_stress_2026-05-01.json",
    "wz_v_authority_firewall": "outputs/yt_pr230_wz_v_authority_firewall_2026-05-15.json",
    "higher_shell_complete_packet": "outputs/yt_pr230_schur_higher_shell_complete_packet_monotonicity_gate_2026-05-15.json",
    "higher_shell_wave_launcher": "outputs/yt_pr230_schur_higher_shell_wave_launcher_2026-05-12.json",
    "chunk063_checkpoint": "outputs/yt_pr230_schur_higher_shell_chunk063_checkpoint_2026-05-12.json",
    "source_higgs_bridge_aperture": "outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "wz_physical_response_packet": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "neutral_h3h4_aperture": "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
}

STRICT_REOPEN_ARTIFACTS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_coordinate_transport_certificate": "outputs/yt_pr230_source_coordinate_transport_certificate_2026-05-06.json",
    "source_higgs_cross_correlator_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "same_surface_neutral_transfer_operator": "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json",
    "electroweak_v_authority_certificate": "outputs/yt_electroweak_v_authority_certificate_2026-05-12.json",
    "fh_lsz_carleman_tauberian_certificate": "outputs/yt_fh_lsz_carleman_tauberian_certificate_2026-05-05.json",
}

REMOTE_REOPEN_PATTERNS = [
    re.compile(r"outputs/yt_canonical_higgs_operator_certificate_2026-05-03\.json$"),
    re.compile(r"outputs/yt_electroweak_v_authority_certificate_2026-05-12\.json$"),
    re.compile(r"outputs/yt_source_higgs_cross_correlator_(measurement_rows|production_certificate)_2026-05-03\.json$"),
    re.compile(r"outputs/yt_top_wz_matched_response_rows_2026-05-04\.json$"),
    re.compile(r"outputs/yt_schur_abc_kernel_rows_2026-05-05\.json$"),
    re.compile(r"outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05\.json$"),
    re.compile(r"outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06\.json$"),
    re.compile(r"outputs/yt_pr230_source_coordinate_transport_certificate_2026-05-06\.json$"),
    re.compile(r"outputs/yt_pr230_.*(source_higgs.*production|wz.*production|wz.*response_rows|neutral.*h3|neutral.*h4).*\.json$"),
]

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def git_lines(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def remote_reopen_hits() -> list[dict[str, str]]:
    refs = git_lines(["for-each-ref", "--format=%(refname:short)", "refs/remotes/origin"])
    hits: list[dict[str, str]] = []
    for ref in refs:
        files = git_lines(["ls-tree", "-r", "--name-only", ref])
        for path in files:
            if any(pattern.search(path) for pattern in REMOTE_REOPEN_PATTERNS):
                hits.append({"ref": ref, "path": path})
    return hits


def main() -> int:
    print("PR #230 post-Block100 completion/reopen audit")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    parent_failures = {
        name: cert.get("fail_count")
        for name, cert in certs.items()
        if cert and cert.get("fail_count") not in (0, None)
    }

    retained = certs["retained_route"]
    campaign = certs["campaign_status"]
    assembly = certs["full_positive_assembly"]
    assumptions = certs["assumption_import_stress"]
    wz_v = certs["wz_v_authority_firewall"]
    complete_packet = certs["higher_shell_complete_packet"]
    launcher = certs["higher_shell_wave_launcher"]
    chunk063 = certs["chunk063_checkpoint"]

    completed_chunks = launcher.get("completed_chunk_indices", [])
    active_chunks = launcher.get("active_chunk_indices", [])
    planned_chunks = launcher.get("planned_launch_chunk_indices", [])
    chunks_complete = (
        completed_chunks == list(range(1, 64))
        and active_chunks == []
        and planned_chunks == []
        and launcher.get("active_process_count") == 0
    )
    chunk063_passed = chunk063.get("fail_count") == 0 and chunk063.get("pass_count", 0) > 0

    current_reopen_artifacts = {
        name: (ROOT / path).exists() for name, path in STRICT_REOPEN_ARTIFACTS.items()
    }
    current_strict_artifacts_absent = not any(current_reopen_artifacts.values())
    remote_hits = remote_reopen_hits()
    current_pr_ref = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
    remote_hits_outside_pr230 = [hit for hit in remote_hits if hit["ref"] != current_pr_ref]
    remote_strict_artifacts_absent = not remote_hits_outside_pr230

    retained_denies_proposal = retained.get("proposal_allowed") is False
    campaign_denies_proposal = campaign.get("proposal_allowed") is False
    assembly_rejects_current_surface = assembly.get("proposal_allowed") is False
    assumptions_preserve_firewall = assumptions.get("proposal_allowed") is False
    wz_v_blocks = (
        wz_v.get("proposal_allowed") is False
        and wz_v.get("wz_v_authority_firewall_passed") is True
        and wz_v.get("v_authority_gate_passed") is False
    )
    finite_packet_blocks = (
        complete_packet.get("proposal_allowed") is False
        and complete_packet.get("higher_shell_complete_packet_monotonicity_gate_passed")
        is True
        and complete_packet.get("strict_schur_or_scalar_lsz_authority_passed") is False
    )
    closure_achieved = False
    fresh_artifact_admitted = False

    missing_requirements = [
        "canonical O_H / accepted same-surface EW-Higgs action authority",
        "strict physical Euclidean C_ss/C_sH/C_HH pole rows with Gram/FV/IR authority",
        "strict scalar-LSZ moment/threshold/FV authority or Schur pole-derivative rows",
        "accepted same-source W/Z action plus production W/Z/top rows and matched covariance",
        "allowed W/Z absolute pin: strict non-observed g2, strict non-forbidden v, or canonical source-response normalization",
        "same-surface neutral H3/H4 primitive/off-diagonal transfer plus source/canonical-Higgs coupling authority",
        "matching/running bridge after a physical source-overlap or W/Z response bridge",
        "retained-route and campaign proposal authorization",
    ]

    prompt_to_artifact_checklist = [
        {
            "requirement": "last higher-shell chunk campaign is finished",
            "evidence": PARENTS["higher_shell_wave_launcher"],
            "covered": chunks_complete,
        },
        {
            "requirement": "chunk063 completed-mode checkpoint exists and passes",
            "evidence": PARENTS["chunk063_checkpoint"],
            "covered": chunk063_passed,
        },
        {
            "requirement": "full retained/proposed-retained top-Yukawa closure",
            "evidence": PARENTS["retained_route"],
            "covered": False,
            "blocker": status(retained),
        },
        {
            "requirement": "full positive closure assembly gate accepts the current surface",
            "evidence": PARENTS["full_positive_assembly"],
            "covered": False,
            "blocker": status(assembly),
        },
        {
            "requirement": "source-Higgs route has canonical O_H plus strict C_sH/C_HH rows",
            "evidence": STRICT_REOPEN_ARTIFACTS,
            "covered": False,
            "blocker": "named strict source-Higgs artifacts are absent",
        },
        {
            "requirement": "W/Z response route has accepted action, rows, covariance, and allowed absolute pin",
            "evidence": PARENTS["wz_physical_response_packet"],
            "covered": False,
            "blocker": "W/Z packet intake and Block100 explicit-v firewall both block current surface",
        },
        {
            "requirement": "neutral primitive route has H3/H4 physical-transfer authority",
            "evidence": PARENTS["neutral_h3h4_aperture"],
            "covered": False,
            "blocker": "neutral H3/H4 certificate is absent",
        },
        {
            "requirement": "no fresh strict closure artifact is available on fetched remote refs",
            "evidence": "local git refs/remotes/origin scan",
            "covered": remote_strict_artifacts_absent,
        },
        {
            "requirement": "claim firewall remains active",
            "evidence": [
                PARENTS["wz_v_authority_firewall"],
                PARENTS["retained_route"],
                PARENTS["campaign_status"],
            ],
            "covered": (not closure_achieved)
            and wz_v_blocks
            and retained_denies_proposal
            and campaign_denies_proposal,
        },
    ]

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, str(parent_failures))
    report(
        "higher-shell-chunks-complete",
        chunks_complete,
        f"completed_count={len(completed_chunks)} active={active_chunks} planned={planned_chunks}",
    )
    report("chunk063-checkpoint-passed", chunk063_passed, PARENTS["chunk063_checkpoint"])
    report("retained-route-denies-proposal", retained_denies_proposal, status(retained))
    report("campaign-denies-proposal", campaign_denies_proposal, status(campaign))
    report("assembly-rejects-current-surface", assembly_rejects_current_surface, status(assembly))
    report("post-block100-audit-denies-closure", not closure_achieved, "closure_achieved=False")
    report("assumption-stress-preserves-firewall", assumptions_preserve_firewall, status(assumptions))
    report("wz-v-firewall-blocks-package-v", wz_v_blocks, status(wz_v))
    report("finite-packet-monotonicity-blocks-shortcut", finite_packet_blocks, status(complete_packet))
    report(
        "current-strict-reopen-artifacts-absent",
        current_strict_artifacts_absent,
        str(current_reopen_artifacts),
    )
    report(
        "remote-strict-reopen-artifacts-absent",
        remote_strict_artifacts_absent,
        str(remote_hits_outside_pr230[:20]),
    )
    report("closure-not-achieved", not closure_achieved, "required positive-closure roots remain absent")
    report("fresh-artifact-not-admitted", not fresh_artifact_admitted, "no current/fetched strict reopen artifact")

    result = {
        "objective": "resume positive closure on PR #230",
        "actual_current_surface_status": (
            "open / post-Block100 completion-reopen audit: positive closure not achieved "
            "and no current/fetched strict reopen artifact is admitted"
        ),
        "conditional_surface_status": (
            "reopen if a strict same-surface O_H/C_sH/C_HH packet, strict W/Z "
            "response packet with allowed absolute pin, strict Schur/scalar-LSZ pole "
            "authority, or neutral H3/H4 primitive-transfer certificate appears"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The final chunk packet is complete, but all retained/proposed-retained "
            "closure gates still reject the current surface and no fresh strict "
            "same-surface artifact is present on the branch or fetched remote refs."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "completion_reopen_audit_passed": FAIL_COUNT == 0,
        "closure_achieved": closure_achieved,
        "fresh_artifact_admitted": fresh_artifact_admitted,
        "prompt_to_artifact_checklist": prompt_to_artifact_checklist,
        "missing_requirements": missing_requirements,
        "parent_statuses": {name: status(cert) for name, cert in certs.items()},
        "chunk_status": {
            "completed_chunk_indices": completed_chunks,
            "active_chunk_indices": active_chunks,
            "planned_launch_chunk_indices": planned_chunks,
            "active_process_count": launcher.get("active_process_count"),
            "chunks_complete": chunks_complete,
        },
        "current_reopen_artifacts": current_reopen_artifacts,
        "remote_reopen_scan": {
            "patterns": [pattern.pattern for pattern in REMOTE_REOPEN_PATTERNS],
            "hits": remote_hits,
            "hits_outside_current_pr230_ref": remote_hits_outside_pr230,
        },
        "strict_non_claims": {
            "claimed_retained_or_proposed_retained": False,
            "used_hunit_matrix_element_readout": False,
            "used_yt_ward_identity": False,
            "used_observed_top_mass_or_yt_selector": False,
            "used_alpha_lm_plaquette_or_u0_as_authority": False,
            "used_package_v_as_authority": False,
            "set_kappa_s_c2_zmatch_or_g2_to_one": False,
            "treated_completed_chunks_as_closure": False,
            "treated_remote_path_names_as_closure_without_certificate": False,
        },
        "exact_next_action": (
            "Stop replaying completed finite-chunk and package-v routes. The next "
            "productive physics action must create one named strict artifact: "
            "accepted same-surface O_H/action plus C_ss/C_sH/C_HH pole rows, "
            "a strict W/Z response packet with allowed absolute pin, strict Schur/"
            "scalar-LSZ pole authority, or neutral H3/H4 primitive-transfer authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
