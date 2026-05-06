#!/usr/bin/env python3
"""
PR #230 origin/main composite-Higgs intake guard.

origin/main contains a composite-Higgs stretch-attempt packet.  This runner
checks whether that packet supplies a PR230 same-surface canonical-Higgs
operator or source-Higgs pole rows.  Expected verdict: no.  The packet is
cross-lane conditional context with three named residual obstructions; it is
not a PR230 O_H/C_sH/C_HH artifact and it does not authorize closure wording.
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
    / "yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json"
)

REMOTE_MAIN = "origin/main"
REMOTE_PR = "origin/claude/yt-direct-lattice-correlator-2026-04-30"

COMPOSITE_PATHS = {
    "note": "docs/COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md",
    "runner": "scripts/frontier_composite_higgs_mechanism.py",
    "state": ".claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/STATE.yaml",
    "handoff": ".claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/HANDOFF.md",
    "claim_status": ".claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/CLAIM_STATUS_CERTIFICATE.md",
    "assumptions": ".claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/ASSUMPTIONS_AND_IMPORTS.md",
}

FUTURE_PR230_ARTIFACTS = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_coordinate_transport_certificate": "outputs/yt_pr230_source_coordinate_transport_certificate_2026-05-06.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "carleman_tauberian_certificate": "outputs/yt_fh_lsz_carleman_tauberian_certificate_2026-05-05.json",
}

PARENTS = {
    "cross_lane_oh_authority_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_coordinate_transport_gate": "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json",
    "positive_closure_completion_audit": "outputs/yt_pr230_positive_closure_completion_audit_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def git_path_exists(ref: str, rel: str) -> bool:
    return git_ok(["cat-file", "-e", f"{ref}:{rel}"])


def read_candidate(rel: str) -> tuple[str, str]:
    path = ROOT / rel
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace"), "local"
    text = git(["show", f"{REMOTE_MAIN}:{rel}"])
    if text:
        return text, REMOTE_MAIN
    return "", "missing"


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present_paths(ref: str | None = None) -> list[str]:
    present = []
    for rel in FUTURE_PR230_ARTIFACTS.values():
        if ref is None:
            if (ROOT / rel).exists():
                present.append(rel)
        elif git_path_exists(ref, rel):
            present.append(rel)
    return sorted(present)


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_mass_or_yukawa_as_selector": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "uses_reduced_cold_pilots_as_production_evidence": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "sets_kappa_s_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 origin/main composite-Higgs intake guard")
    print("=" * 72)

    texts = {name: read_candidate(rel) for name, rel in COMPOSITE_PATHS.items()}
    candidate_text = "\n\n".join(text for text, _source in texts.values())
    sources = {name: source for name, (_text, source) in texts.items()}
    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    remote_main_head = git(["rev-parse", REMOTE_MAIN])
    remote_pr_head = git(["rev-parse", REMOTE_PR])
    local_head = git(["rev-parse", "HEAD"])
    composite_pack_present = all(source != "missing" for source in sources.values())
    stretch_attempt_classified = (
        "stretch_attempt" in candidate_text
        or "STRETCH ATTEMPT" in candidate_text
        or "stretch attempt" in candidate_text.lower()
    )
    not_closing_derivation_disclaimed = (
        "NOT a closing derivation" in candidate_text
        or "not a closing derivation" in candidate_text.lower()
    )
    residual_obstructions_named = all(
        phrase in candidate_text
        for phrase in (
            "NO1",
            "Z3 acts on quark-bilinear generation index",
            "NO2",
            "equal magnitude",
            "NO3",
            "strong-coupling magnitude",
        )
    )
    runner_pass_recorded = (
        "TOTAL: PASS=80, FAIL=0" in candidate_text
        or "PASS=80, FAIL=0" in candidate_text
    )
    claim_status_open = (
        "open_gate" in candidate_text
        and (
            "proposal_allowed: false" in candidate_text
            or "retained_grade_claim_proposed: false" in candidate_text
        )
        and (
            "No retained-grade claim proposed" in candidate_text
            or "not a retained claim" in candidate_text.lower()
            or "NOT retained" in candidate_text
        )
    )
    admitted_or_hypothetical_premises = all(
        phrase in candidate_text
        for phrase in (
            "branch-local HYPOTHESIS",
            "Z3 acts on",
            "equal magnitude",
            "NJL mean-field factorization",
        )
    )
    pr230_same_surface_rows_absent = (
        "C_sH" not in candidate_text
        and "C_HH" not in candidate_text
        and "source-Higgs pole" not in candidate_text
    )
    pr230_uniform_source_absent = (
        "PR230" not in candidate_text
        and "uniform additive mass source" not in candidate_text
        and "m_bare + s" not in candidate_text
    )
    cross_lane_oh_audit_still_blocks = (
        "cross-lane O_H authority audit" in statuses["cross_lane_oh_authority_audit"]
        and certs["cross_lane_oh_authority_audit"].get("proposal_allowed") is False
        and certs["cross_lane_oh_authority_audit"].get("repo_cross_lane_authority_found")
        is False
        and certs["cross_lane_oh_authority_audit"].get(
            "cross_lane_oh_authority_audit_passed"
        )
        is True
    )
    canonical_oh_gate_still_absent = (
        "canonical-Higgs operator certificate absent"
        in statuses["canonical_higgs_operator_gate"]
        and certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    source_transport_still_blocked = (
        "source-coordinate transport to canonical O_H not derivable"
        in statuses["source_coordinate_transport_gate"]
        and certs["source_coordinate_transport_gate"].get("proposal_allowed") is False
        and certs["source_coordinate_transport_gate"].get(
            "source_coordinate_transport_gate_passed"
        )
        is True
        and certs["source_coordinate_transport_gate"].get(
            "future_transport_certificate_present"
        )
        is False
    )
    aggregate_gates_open = (
        certs["positive_closure_completion_audit"].get("closure_achieved") is False
        and certs["positive_closure_completion_audit"].get("proposal_allowed") is False
        and certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    future_presence = {
        "local": present_paths(),
        "remote_pr": present_paths(REMOTE_PR),
        "remote_main": present_paths(REMOTE_MAIN),
    }
    no_future_pr230_artifact_present = not any(future_presence.values())
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    origin_main_composite_higgs_closes_pr230 = (
        composite_pack_present
        and not admitted_or_hypothetical_premises
        and not pr230_same_surface_rows_absent
        and not pr230_uniform_source_absent
        and canonical_oh_gate_still_absent is False
        and no_future_pr230_artifact_present is False
        and clean_firewall
    )
    intake_guard_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and composite_pack_present
        and stretch_attempt_classified
        and not_closing_derivation_disclaimed
        and residual_obstructions_named
        and runner_pass_recorded
        and claim_status_open
        and admitted_or_hypothetical_premises
        and pr230_same_surface_rows_absent
        and pr230_uniform_source_absent
        and cross_lane_oh_audit_still_blocks
        and canonical_oh_gate_still_absent
        and source_transport_still_blocked
        and aggregate_gates_open
        and no_future_pr230_artifact_present
        and origin_main_composite_higgs_closes_pr230 is False
        and clean_firewall
    )

    report("composite-pack-readable", composite_pack_present, str(sources))
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, str(proposal_allowed_parents))
    report("stretch-attempt-classified", stretch_attempt_classified, "origin/main packet is a stretch attempt")
    report("not-a-closing-derivation-disclaimed", not_closing_derivation_disclaimed, "explicit non-closure disclaimer")
    report("three-residual-obstructions-named", residual_obstructions_named, "NO1/NO2/NO3")
    report("runner-pass-recorded", runner_pass_recorded, "TOTAL PASS=80 FAIL=0")
    report("claim-status-open", claim_status_open, "open_gate / proposal_allowed=false")
    report("hypotheses-load-bearing", admitted_or_hypothetical_premises, "H1/H2 plus NJL context")
    report("pr230-source-higgs-rows-absent-from-packet", pr230_same_surface_rows_absent, "no C_sH/C_HH rows")
    report("pr230-uniform-source-absent-from-packet", pr230_uniform_source_absent, "no m_bare+s source transport")
    report("cross-lane-oh-audit-still-blocks", cross_lane_oh_audit_still_blocks, statuses["cross_lane_oh_authority_audit"])
    report("canonical-oh-gate-still-absent", canonical_oh_gate_still_absent, statuses["canonical_higgs_operator_gate"])
    report("source-transport-still-blocked", source_transport_still_blocked, statuses["source_coordinate_transport_gate"])
    report("aggregate-gates-still-open", aggregate_gates_open, "completion/assembly/retained/campaign proposal_allowed=false")
    report("future-pr230-artifacts-absent", no_future_pr230_artifact_present, str(future_presence))
    report("origin-main-composite-higgs-does-not-close-pr230", origin_main_composite_higgs_closes_pr230 is False, "conditional cross-lane packet")
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("intake-guard-passed", intake_guard_passed, "cross-lane context recorded as non-closure")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / origin/main composite-Higgs stretch "
            "packet is conditional cross-lane context, not PR230 same-surface "
            "O_H/C_sH/C_HH closure"
        ),
        "conditional_surface_status": (
            "The composite-Higgs packet may become relevant only if its Z3 "
            "extension, equal-condensate, and strong-coupling premises are "
            "derived and then connected to a PR230 same-source canonical O_H "
            "operator or production C_sH/C_HH rows."
        ),
        "hypothetical_axiom_status": (
            "H1 Z3 quark-bilinear generation action and H2 equal condensate "
            "magnitudes are branch-local hypotheses in the origin/main packet."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The origin/main composite-Higgs packet is an open_gate stretch "
            "attempt with three named residual obstructions.  It supplies no "
            "PR230 uniform-source transport, no same-surface canonical O_H "
            "identity/normalization certificate, and no C_sH/C_HH pole rows.  "
            "All aggregate PR230 proposal gates still deny closure."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "origin_main_composite_higgs_intake_guard_passed": intake_guard_passed,
        "origin_main_composite_higgs_closes_pr230": origin_main_composite_higgs_closes_pr230,
        "composite_sources": sources,
        "branch_state": {
            "local_head": local_head,
            "remote_pr_head": remote_pr_head,
            "remote_main_head": remote_main_head,
        },
        "parent_statuses": statuses,
        "future_pr230_artifact_presence": future_presence,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat a composite-Higgs mechanism candidate as PR230 O_H authority",
            "does not import branch-local Z3/equal-condensate hypotheses into PR230",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Reopen positive closure only after a real same-surface PR230 "
            "artifact lands: canonical O_H plus O_sp/C_sH/C_HH pole rows, "
            "a genuine source-coordinate transport certificate, same-source "
            "W/Z rows with strict g2/covariance/identity authority, Schur "
            "A/B/C kernel rows, a neutral primitive/off-diagonal certificate, "
            "or strict scalar-LSZ/FV/IR authority."
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
