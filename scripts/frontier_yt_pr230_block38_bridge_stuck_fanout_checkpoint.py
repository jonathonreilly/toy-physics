#!/usr/bin/env python3
"""
PR #230 block38 source-Higgs / WZ bridge stuck-fanout checkpoint.

Block37 yielded the lane because no fresh production/certificate input had
landed.  The current PR head also contains the block42/block43 timeseries
boundaries plus the block44 Euclidean source-Higgs row absence boundary, which
still do not provide accepted source-Higgs, W/Z, or neutral transfer roots.
This block does not re-run the same absence gate.  It
consumes five orthogonal, already executable attack frames around the two
prioritized routes:

1. degree-one O_H action premise,
2. same-source EW action adoption,
3. same-surface neutral multiplicity-one intake,
4. taste-condensate O_H bridge,
5. strict W/Z absolute-authority response.

The checkpoint records that all five frames are support-only or exact negative
boundaries on the current PR230 surface.  The next admissible move is still a
real source-Higgs or W/Z physical bridge artifact, not another shortcut cycle.
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
    / "yt_pr230_block38_bridge_stuck_fanout_checkpoint_2026-05-12.json"
)

PR_REF = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
EXPECTED_INSPECTION_HEAD = "6db4d9bcb3c77f2de7acf6adbef6e2105fc6cab1"
EXPECTED_INSPECTION_LABEL = "current PR head after block42/block43/block44 boundaries"
BLOCK38_SUBJECT = "Record PR230 block38 bridge stuck fanout checkpoint"

PARENTS = {
    "block37_supervisor_yield": "outputs/yt_pr230_block37_post_block36_supervisor_yield_checkpoint_2026-05-12.json",
    "degree_one_higgs_action_premise": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "same_source_ew_action_adoption": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "same_surface_neutral_multiplicity_one": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "taste_condensate_oh_bridge": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
    "wz_absolute_authority": "outputs/yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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
    print("PR #230 block38 source-Higgs / WZ bridge stuck-fanout checkpoint")
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
    inspection_ref = "HEAD^" if local_subject == BLOCK38_SUBJECT else "HEAD"
    inspection_head = run_git(["rev-parse", inspection_ref])
    pr_head = run_git(["rev-parse", "--verify", PR_REF])

    source_presence = present_at_ref(inspection_ref, SOURCE_HIGGS_REQUIRED_PATHS)
    wz_presence = present_at_ref(inspection_ref, WZ_REQUIRED_PATHS)
    neutral_presence = present_at_ref(inspection_ref, NEUTRAL_H3H4_REQUIRED_PATHS)

    block37 = parents["block37_supervisor_yield"]
    degree_one = parents["degree_one_higgs_action_premise"]
    ew_adoption = parents["same_source_ew_action_adoption"]
    neutral_mult = parents["same_surface_neutral_multiplicity_one"]
    taste_bridge = parents["taste_condensate_oh_bridge"]
    wz_absolute = parents["wz_absolute_authority"]

    block37_yield_clean = (
        block37.get("block37_post_block36_supervisor_yield_checkpoint_passed")
        is True
        and block37.get("proposal_allowed") is False
        and block37.get("campaign_decision", {}).get("yield_for_supervisor") is True
        and block37.get("checks", {}).get("no-ranked-route-admitted") is True
        and block37.get("checks", {}).get("forbidden-firewall-clean") is True
    )
    degree_one_frame_blocked = (
        degree_one.get("degree_one_higgs_action_premise_gate_passed") is True
        and degree_one.get("degree_one_filter_selects_e1") is True
        and degree_one.get("degree_one_premise_authorized_on_current_surface")
        is False
        and degree_one.get("canonical_oh_absent") is True
        and degree_one.get("same_surface_ew_higgs_action_absent") is True
    )
    ew_action_frame_blocked = (
        ew_adoption.get("same_source_ew_action_adoption_attempt_passed") is True
        and ew_adoption.get("adoption_allowed_now") is False
        and ew_adoption.get("schema_side_satisfied") is False
        and ew_adoption.get("accepted_action_certificate_present") is False
    )
    neutral_frame_blocked = (
        neutral_mult.get("candidate_accepted") is False
        and neutral_mult.get("proposal_allowed") is False
        and neutral_mult.get("future_file_presence", {}).get(
            "canonical_higgs_operator_certificate"
        )
        is False
        and neutral_mult.get("future_file_presence", {}).get(
            "source_higgs_measurement_rows"
        )
        is False
    )
    taste_frame_blocked = (
        taste_bridge.get("taste_condensate_oh_bridge_audit_passed") is True
        and taste_bridge.get("proposal_allowed") is False
        and taste_bridge.get("algebra", {}).get(
            "uniform_source_relative_projection_onto_taste_axis_span"
        )
        == 0.0
        and taste_bridge.get("future_file_presence", {}).get(
            "canonical_oh_certificate"
        )
        is False
    )
    wz_frame_blocked = (
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
    fanout_all_blocked = all(
        [
            degree_one_frame_blocked,
            ew_action_frame_blocked,
            neutral_frame_blocked,
            taste_frame_blocked,
            wz_frame_blocked,
        ]
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    yield_for_supervisor = (
        not missing_parents
        and not failing_parents
        and not proposal_parents
        and inspection_head == EXPECTED_INSPECTION_HEAD
        and block37_yield_clean
        and fanout_all_blocked
        and no_route_admitted
        and firewall_clean
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("inspection-ref-is-current-pr-head", inspection_head == EXPECTED_INSPECTION_HEAD, f"{inspection_ref}={inspection_head}; expected={EXPECTED_INSPECTION_LABEL}")
    report("block37-yield-clean", block37_yield_clean, status(block37))
    report("degree-one-oh-premise-frame-blocked", degree_one_frame_blocked, status(degree_one))
    report("same-source-ew-action-adoption-frame-blocked", ew_action_frame_blocked, status(ew_adoption))
    report("same-surface-neutral-multiplicity-frame-blocked", neutral_frame_blocked, status(neutral_mult))
    report("taste-condensate-oh-bridge-frame-blocked", taste_frame_blocked, status(taste_bridge))
    report("wz-absolute-authority-frame-blocked", wz_frame_blocked, status(wz_absolute))
    report("source-higgs-required-roots-still-absent", not source_admitted, str(source_presence))
    report("wz-required-roots-still-absent", not wz_admitted, str(wz_presence))
    report("neutral-h3h4-required-roots-still-absent", not neutral_admitted, str(neutral_presence))
    report("five-frame-stuck-fanout-all-blocked", fanout_all_blocked, "all prioritized O_H/source-Higgs/WZ frames remain support-only or exact boundaries")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("yield-for-supervisor", yield_for_supervisor, "waiting on explicit source-Higgs or W/Z physical bridge inputs")

    result = {
        "actual_current_surface_status": (
            "open / block38 bridge stuck-fanout checkpoint; five prioritized "
            "O_H/source-Higgs/WZ attack frames are blocked on the current "
            "surface and no ranked route is admitted without a fresh physical "
            "bridge artifact"
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
            "Block38 is a stuck-fanout checkpoint.  It consumes existing "
            "source-Higgs and W/Z route attempts and records that each frame is "
            "support-only or an exact current-surface boundary.  No accepted "
            "action, canonical O_H certificate, source-Higgs pole-row packet, "
            "strict W/Z packet, or neutral H3/H4 certificate is present."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "block38_bridge_stuck_fanout_checkpoint_passed": FAIL_COUNT == 0,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "local_head": local_head,
        "local_subject": local_subject,
        "inspection_ref": inspection_ref,
        "inspection_head": inspection_head,
        "expected_inspection_head": EXPECTED_INSPECTION_HEAD,
        "expected_inspection_label": EXPECTED_INSPECTION_LABEL,
        "pr_ref": PR_REF,
        "pr_head": pr_head,
        "fanout_frames": [
            {
                "id": "degree_one_oh_action_premise",
                "status": status(degree_one),
                "blocked": degree_one_frame_blocked,
                "remaining_import": "accepted same-surface action premise or canonical O_H certificate",
            },
            {
                "id": "same_source_ew_action_adoption",
                "status": status(ew_adoption),
                "blocked": ew_action_frame_blocked,
                "remaining_import": "canonical-Higgs, sector-overlap, W/Z mass-fit, and accepted action certificate inputs",
            },
            {
                "id": "same_surface_neutral_multiplicity_one",
                "status": status(neutral_mult),
                "blocked": neutral_frame_blocked,
                "remaining_import": "same-surface physical neutral transfer plus source/canonical-Higgs overlap authority",
            },
            {
                "id": "taste_condensate_oh_bridge",
                "status": status(taste_bridge),
                "blocked": taste_frame_blocked,
                "remaining_import": "source-coordinate transport certificate or canonical O_H plus C_sH/C_HH rows",
            },
            {
                "id": "wz_absolute_authority_response",
                "status": status(wz_absolute),
                "blocked": wz_frame_blocked,
                "remaining_import": "strict W/Z physical-response packet with absolute g2/v authority and matched covariance",
            },
        ],
        "source_higgs_route": {
            "rank": 1,
            "admitted": source_admitted,
            "required_paths": SOURCE_HIGGS_REQUIRED_PATHS,
            "committed_path_presence": source_presence,
            "missing_roots": missing_roots(source_presence),
            "decision": (
                "yield until accepted same-surface O_H/action plus strict "
                "C_ss/C_sH/C_HH pole rows and Gram/FV/IR authority exist"
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
                "yield until accepted action, production W/Z rows, same-source "
                "top rows, matched covariance, strict non-observed g2, "
                "delta_perp, and final W-response rows exist"
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
            "fanout_all_blocked": fanout_all_blocked,
            "no_ranked_route_admitted": no_route_admitted,
            "yield_for_supervisor": yield_for_supervisor,
            "next_exact_action": (
                "Supply one explicit missing artifact: accepted same-surface "
                "O_H/action plus strict C_ss/C_sH/C_HH rows, or a strict W/Z "
                "physical-response packet with accepted action, production "
                "rows, same-source top rows, matched covariance, strict "
                "non-observed g2, delta_perp, and final W-response rows."
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
            "block37-yield-clean": block37_yield_clean,
            "degree-one-oh-premise-frame-blocked": degree_one_frame_blocked,
            "same-source-ew-action-adoption-frame-blocked": ew_action_frame_blocked,
            "same-surface-neutral-multiplicity-frame-blocked": neutral_frame_blocked,
            "taste-condensate-oh-bridge-frame-blocked": taste_frame_blocked,
            "wz-absolute-authority-frame-blocked": wz_frame_blocked,
            "source-higgs-required-roots-still-absent": not source_admitted,
            "wz-required-roots-still-absent": not wz_admitted,
            "neutral-h3h4-required-roots-still-absent": not neutral_admitted,
            "five-frame-stuck-fanout-all-blocked": fanout_all_blocked,
            "forbidden-firewall-clean": firewall_clean,
            "yield-for-supervisor": yield_for_supervisor,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not rerun block37 as new evidence",
            "does not treat block42/block43/block44 boundaries as source-Higgs, W/Z, or neutral-transfer closure",
            "does not promote degree-one taste-radial uniqueness to canonical O_H without a same-surface action premise",
            "does not treat the same-source EW action ansatz as an accepted action certificate",
            "does not treat neutral multiplicity-one intake as accepted O_H authority",
            "does not treat the Higgs/taste condensate stack as PR230 O_H authority",
            "does not treat W/Z scout, smoke, ratio, or response-only rows as a strict W/Z packet",
            "does not relabel C_sx/C_xx as C_sH/C_HH before x=O_H is certified",
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
