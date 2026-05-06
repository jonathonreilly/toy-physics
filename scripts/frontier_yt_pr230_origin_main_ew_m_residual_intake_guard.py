#!/usr/bin/env python3
"""
PR #230 origin/main EW M-residual intake guard.

origin/main contains a stretch-attempt script for EW color-channel
bookkeeping under CMT mean-field language.  This runner checks whether that
packet supplies a PR230 same-surface action-first or W/Z-response closure
artifact.  Expected verdict: no.  The packet explicitly says it does not close
the M rule without an explicit framework EW Wilson-line construction, and it
uses u0/CMT bookkeeping that is forbidden as load-bearing PR230 y_t authority.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json"
)

REMOTE_MAIN = "origin/main"
REMOTE_PR = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
REMOTE_SCRIPT = "scripts/yt_ew_m_residual_channel_check.py"

PARENTS = {
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
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


def git(args: list[str]) -> str:
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_mass_or_yukawa_as_selector": False,
        "uses_alpha_lm_plaquette_or_u0_as_pr230_proof_input": False,
        "uses_reduced_cold_pilots_as_production_evidence": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "sets_kappa_s_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 origin/main EW M-residual intake guard")
    print("=" * 72)

    local_head = git(["rev-parse", "HEAD"])
    remote_main_head = git(["rev-parse", REMOTE_MAIN])
    remote_pr_head = git(["rev-parse", REMOTE_PR])
    remote_script_exists = git_ok(["cat-file", "-e", f"{REMOTE_MAIN}:{REMOTE_SCRIPT}"])
    remote_text = git(["show", f"{REMOTE_MAIN}:{REMOTE_SCRIPT}"])
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()

    explicit_nonclosure = (
        "does NOT close M" in remote_text
        and "requires explicit framework EW" in remote_text
        and "Wilson-line construction" in remote_text
    )
    cmt_u0_present = (
        "CMT" in remote_text
        and "u_0" in remote_text
        and "mean-field" in remote_text
    )
    channel_bookkeeping_only = all(
        phrase in remote_text
        for phrase in (
            "Fierz channel decomposition",
            "adjoint channel",
            "singlet channel",
            "channel-fraction count",
        )
    )
    admits_missing_ew_current = (
        "Define the framework's lattice EW current as a Wilson-line bilinear"
        in remote_text
        and "currently implicit" in remote_text
        and "needs explicit formula" in remote_text
    )
    pr230_surface_absent = all(
        phrase not in remote_text
        for phrase in (
            "PR230",
            "m_bare + s",
            "C_sH",
            "C_HH",
            "O_H",
            "canonical Higgs",
            "delta_perp",
            "matched covariance",
            "same-source W/Z",
            "source-Higgs pole",
        )
    )
    output_schema_absent = (
        "json" not in remote_text.lower()
        and "OUTPUT" not in remote_text
        and "actual_current_surface_status" not in remote_text
    )
    aggregate_gates_open = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    action_first_still_blocked = (
        "action-first O_H/C_sH/C_HH route not complete"
        in parent_statuses["action_first_route_completion"]
        and parents["action_first_route_completion"].get("proposal_allowed") is False
        and parents["action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
    )
    wz_route_still_blocked = (
        "WZ same-source response route not complete"
        in parent_statuses["wz_response_route_completion"]
        and parents["wz_response_route_completion"].get("proposal_allowed") is False
        and parents["wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
    )
    same_source_action_still_absent = (
        "same-source EW action not defined"
        in parent_statuses["same_source_ew_action_gate"]
        and parents["same_source_ew_action_gate"].get("proposal_allowed") is False
        and parents["same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
    )
    wz_certificate_still_absent = (
        "same-source WZ response certificate gate not passed"
        in parent_statuses["same_source_wz_response_certificate_gate"]
        and parents["same_source_wz_response_certificate_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )
    no_future_artifacts_present = not any(futures.values())
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    ew_m_residual_closes_pr230 = (
        remote_script_exists
        and not explicit_nonclosure
        and not cmt_u0_present
        and not pr230_surface_absent
        and not no_future_artifacts_present
        and aggregate_gates_open is False
        and clean_firewall
    )
    intake_guard_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and remote_script_exists
        and bool(remote_text)
        and explicit_nonclosure
        and cmt_u0_present
        and channel_bookkeeping_only
        and admits_missing_ew_current
        and pr230_surface_absent
        and output_schema_absent
        and aggregate_gates_open
        and action_first_still_blocked
        and wz_route_still_blocked
        and same_source_action_still_absent
        and wz_certificate_still_absent
        and no_future_artifacts_present
        and ew_m_residual_closes_pr230 is False
        and clean_firewall
    )

    report("remote-script-readable", remote_script_exists and bool(remote_text), REMOTE_SCRIPT)
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, str(proposal_allowed_parents))
    report("explicit-nonclosure-disclaimer", explicit_nonclosure, "does NOT close M / EW Wilson-line construction required")
    report("cmt-u0-bookkeeping-present", cmt_u0_present, "packet uses CMT/u0/mean-field language")
    report("channel-bookkeeping-only", channel_bookkeeping_only, "Fierz singlet/adjoint decomposition")
    report("missing-ew-current-admitted", admits_missing_ew_current, "EW current formula remains implicit")
    report("pr230-same-surface-artifacts-absent", pr230_surface_absent, "no PR230 O_H/C_sH/C_HH/WZ rows")
    report("output-certificate-schema-absent", output_schema_absent, "remote script is print-only stretch attempt")
    report("aggregate-gates-still-open", aggregate_gates_open, "assembly/retained/campaign proposal_allowed=false")
    report("action-first-route-still-blocked", action_first_still_blocked, parent_statuses["action_first_route_completion"])
    report("wz-route-still-blocked", wz_route_still_blocked, parent_statuses["wz_response_route_completion"])
    report("same-source-ew-action-still-absent", same_source_action_still_absent, parent_statuses["same_source_ew_action_gate"])
    report("same-source-wz-certificate-still-absent", wz_certificate_still_absent, parent_statuses["same_source_wz_response_certificate_gate"])
    report("future-pr230-artifacts-absent", no_future_artifacts_present, str(futures))
    report("origin-main-ew-m-residual-does-not-close-pr230", ew_m_residual_closes_pr230 is False, "context-only packet")
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("intake-guard-passed", intake_guard_passed, "CMT/Fierz packet recorded as non-closure")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / origin/main EW M-residual CMT packet is "
            "context-only channel bookkeeping, not PR230 same-source EW/WZ or "
            "O_H closure"
        ),
        "conditional_surface_status": (
            "The packet may inform a future W/Z route only after a same-surface "
            "framework EW Wilson-line current/action is explicitly constructed "
            "and production W/Z response rows, matched covariance, delta_perp, "
            "and strict non-observed g2 authority are supplied without using "
            "u0/CMT as PR230 y_t proof input."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The remote script explicitly disclaims closure of M and names the "
            "missing EW Wilson-line construction.  It verifies Fierz/CMT "
            "channel bookkeeping only, mentions u0/mean-field factors, emits no "
            "PR230 same-source action, no W/Z response rows, no canonical O_H "
            "certificate, and no C_sH/C_HH pole rows.  Current aggregate gates "
            "still deny proposal wording."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "origin_main_ew_m_residual_intake_guard_passed": intake_guard_passed,
        "origin_main_ew_m_residual_closes_pr230": ew_m_residual_closes_pr230,
        "packet_classification": {
            "remote_script_exists": remote_script_exists,
            "explicit_nonclosure": explicit_nonclosure,
            "cmt_u0_present": cmt_u0_present,
            "channel_bookkeeping_only": channel_bookkeeping_only,
            "admits_missing_ew_current": admits_missing_ew_current,
            "pr230_surface_absent": pr230_surface_absent,
            "output_schema_absent": output_schema_absent,
        },
        "branch_state": {
            "local_head": local_head,
            "remote_pr_head": remote_pr_head,
            "remote_main_head": remote_main_head,
        },
        "parent_statuses": parent_statuses,
        "future_artifact_presence": futures,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use CMT/u0/mean-field bookkeeping as PR230 proof authority",
            "does not treat Fierz channel decomposition as same-source EW action",
            "does not treat implicit EW Wilson-line current language as production W/Z response rows",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Reopen via a genuine same-source EW/WZ artifact only after an "
            "explicit framework EW Wilson-line action/current, production W/Z "
            "mass-fit response rows, matched top/W covariance, strict g2 "
            "authority, and delta_perp control are present; otherwise continue "
            "with canonical O_H/C_sH/C_HH, two-source transport, Schur A/B/C, "
            "strict scalar-LSZ, or neutral primitive-cone routes."
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
