#!/usr/bin/env python3
"""
PR #230 retained-closure route certificate.

This runner answers the operational question: what is the shortest honest path
from the current PR #230 state to retained top-Yukawa closure?  It does not
claim closure.  It verifies that all non-MC shortcuts currently tested are
blocked or conditional, then records the only remaining closure routes.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_retained_closure_route_certificate_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load_json(path: str) -> dict:
    full = ROOT / path
    if not full.exists():
        return {}
    return json.loads(full.read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 retained-closure route certificate")
    print("=" * 72)

    required_certificates = {
        "global_proof_audit": "outputs/yt_pr230_global_proof_audit_2026-05-01.json",
        "direct_cutoff_obstruction": "outputs/yt_top_mass_cutoff_obstruction_2026-05-01.json",
        "beta_lambda_no_go": "outputs/yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json",
        "queue_exhaustion": "outputs/yt_pr230_queue_exhaustion_certificate_2026-05-01.json",
        "ward_repair_audit": "outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json",
        "scalar_pole_residue_no_go": "outputs/yt_scalar_pole_residue_current_surface_no_go_2026-05-01.json",
        "key_blocker_closure_attempt": "outputs/yt_key_blocker_closure_attempt_2026-05-01.json",
        "lsz_normalization_cancellation": "outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json",
        "feshbach_response_boundary": "outputs/yt_feshbach_operator_response_boundary_2026-05-01.json",
        "interacting_kinetic_sensitivity": "outputs/yt_interacting_kinetic_background_sensitivity_2026-05-01.json",
        "fh_lsz_invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
        "scalar_ladder_derivative_limit": "outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
        "cl3_source_unit": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
        "fh_lsz_production_manifest": "outputs/yt_fh_lsz_production_manifest_2026-05-01.json",
        "joint_resource_projection": "outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json",
    }
    certificates = {name: load_json(path) for name, path in required_certificates.items()}

    direct_certificates = [
        "outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_certificate_2026-04-30.json",
        "outputs/yt_direct_lattice_correlator_pilot_plus_certificate_2026-05-01.json",
        "outputs/yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json",
    ]
    direct_meta = []
    for path in direct_certificates:
        data = load_json(path)
        metadata = data.get("metadata", {})
        direct_meta.append(
            {
                "path": path,
                "exists": bool(data),
                "phase": metadata.get("phase") or data.get("phase"),
                "strict_pass": data.get("strict_pass") or data.get("strict_validation", {}).get("pass"),
            }
        )

    missing = [name for name, data in certificates.items() if not data]
    no_hidden_proof = certificates["global_proof_audit"].get("retained_y_t_rows") == {}
    direct_strict_pass = any(item.get("phase") == "production" and item.get("strict_pass") is True for item in direct_meta)
    ward_open = certificates["ward_repair_audit"].get("closure_allowed") is False
    scalar_residue_blocked = (
        certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status")
        == "exact negative boundary / retained closure unavailable on current analytic surface"
    )
    key_blocker_open = (
        certificates["key_blocker_closure_attempt"].get("actual_current_surface_status")
        == "open / key blocker not closed"
    )
    key_blocker_has_no_retained_authority = (
        certificates["key_blocker_closure_attempt"].get("retained_authorities") == []
    )
    lsz_norm_conditional = (
        certificates["lsz_normalization_cancellation"].get("actual_current_surface_status")
        == "conditional-support / scalar LSZ normalization cancellation"
        and certificates["lsz_normalization_cancellation"].get("proposal_allowed") is False
    )
    feshbach_boundary_not_common_dressing = (
        certificates["feshbach_response_boundary"].get("actual_current_surface_status")
        == "exact support / Feshbach response boundary"
        and certificates["feshbach_response_boundary"].get("proposal_allowed") is False
    )
    invariant_readout_not_closure = (
        "invariant readout" in certificates["fh_lsz_invariant_readout"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_invariant_readout"].get("proposal_allowed") is False
    )
    derivative_limit_blocks_ladder = (
        "limiting-order obstruction" in certificates["scalar_ladder_derivative_limit"].get("actual_current_surface_status", "")
        and certificates["scalar_ladder_derivative_limit"].get("proposal_allowed") is False
    )
    cl3_source_unit_blocks_kappa = (
        "source-unit normalization no-go" in certificates["cl3_source_unit"].get("actual_current_surface_status", "")
        and certificates["cl3_source_unit"].get("proposal_allowed") is False
    )
    production_manifest_not_evidence = (
        "production manifest" in certificates["fh_lsz_production_manifest"].get("actual_current_surface_status", "")
        and certificates["fh_lsz_production_manifest"].get("proposal_allowed") is False
    )
    joint_resource_multiday = (
        float(certificates["joint_resource_projection"].get("projection", {}).get("joint_mass_scaled_hours", 0.0)) > 1000.0
        and certificates["joint_resource_projection"].get("proposal_allowed") is False
    )
    interacting_kinetic_still_open = (
        certificates["interacting_kinetic_sensitivity"].get("actual_current_surface_status")
        == "bounded-support / interacting kinetic background sensitivity"
        and certificates["interacting_kinetic_sensitivity"].get("proposal_allowed") is False
    )
    beta_blocked = "no-go" in certificates["beta_lambda_no_go"].get("actual_current_surface_status", "")
    queue_text = (
        certificates["queue_exhaustion"].get("actual_current_surface_status", "")
        + " "
        + certificates["queue_exhaustion"].get("verdict", "")
    ).lower()
    queue_open = "queue exhausted" in queue_text and "no retained" in queue_text

    report("required-certificates-present", not missing, f"missing={missing}")
    report("no-hidden-retained-yt-proof", no_hidden_proof, "global audit retained_y_t_rows empty")
    report("direct-strict-production-not-yet-passed", not direct_strict_pass, f"direct_meta={direct_meta}")
    report("ward-repair-still-open", ward_open, f"closure_allowed={certificates['ward_repair_audit'].get('closure_allowed')}")
    report("scalar-pole-residue-blocked-on-current-surface", scalar_residue_blocked, certificates["scalar_pole_residue_no_go"].get("actual_current_surface_status", ""))
    report(
        "key-blocker-closure-attempt-open",
        key_blocker_open,
        certificates["key_blocker_closure_attempt"].get("actual_current_surface_status", ""),
    )
    report(
        "key-blocker-no-retained-authority",
        key_blocker_has_no_retained_authority,
        "no retained authority supplies pole residue plus common dressing",
    )
    report(
        "lsz-normalization-cancellation-not-closure",
        lsz_norm_conditional,
        certificates["lsz_normalization_cancellation"].get("actual_current_surface_status", ""),
    )
    report(
        "feshbach-response-boundary-not-common-dressing",
        feshbach_boundary_not_common_dressing,
        certificates["feshbach_response_boundary"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-invariant-readout-not-closure",
        invariant_readout_not_closure,
        certificates["fh_lsz_invariant_readout"].get("actual_current_surface_status", ""),
    )
    report(
        "scalar-ladder-derivative-limit-blocks-lsz",
        derivative_limit_blocks_ladder,
        certificates["scalar_ladder_derivative_limit"].get("actual_current_surface_status", ""),
    )
    report(
        "cl3-source-unit-does-not-fix-kappa",
        cl3_source_unit_blocks_kappa,
        certificates["cl3_source_unit"].get("actual_current_surface_status", ""),
    )
    report(
        "fh-lsz-production-manifest-not-evidence",
        production_manifest_not_evidence,
        certificates["fh_lsz_production_manifest"].get("actual_current_surface_status", ""),
    )
    report(
        "joint-fh-lsz-resource-is-multiday",
        joint_resource_multiday,
        f"hours={certificates['joint_resource_projection'].get('projection', {}).get('joint_mass_scaled_hours')}",
    )
    report(
        "interacting-kinetic-route-still-needs-ensemble-or-theorem",
        interacting_kinetic_still_open,
        certificates["interacting_kinetic_sensitivity"].get("actual_current_surface_status", ""),
    )
    report("planck-beta-route-blocked-on-current-surface", beta_blocked, certificates["beta_lambda_no_go"].get("actual_current_surface_status", ""))
    report("prior-route-queue-exhausted", queue_open, "queue exhaustion certificate says no full retained closure")

    closure_routes = [
        {
            "route": "direct_or_joint_physical_measurement",
            "retained_closure_condition": (
                "run strict production correlator or joint FH/LSZ evidence on a "
                "physically suitable scale/heavy-quark treatment, derive or "
                "measure the scalar pole derivative and any interacting "
                "kinetic/matching bridge, produce production certificates, and "
                "pass a retained-proposal gate"
            ),
            "why_shortest": "It bypasses Ward/H_unit and scalar-pole analytic normalization.",
            "current_blocker": "existing certificates are reduced-scope/pilot or manifests; the joint route projects to multi-day single-worker compute",
        },
        {
            "route": "analytic_scalar_residue",
            "retained_closure_condition": (
                "derive scalar source two-point pole residue, scalar carrier map, "
                "and common scalar/gauge dressing from retained dynamics, then "
                "re-run the Ward physical-readout repair audit"
            ),
            "why_shortest": "It directly repairs the audit's physical-readout objection.",
            "current_blocker": "source scaling and Feshbach projection are controlled, but the interacting scalar denominator/residue and common dressing are still not derived",
        },
        {
            "route": "new_selector_or_axiom",
            "retained_closure_condition": (
                "derive beta_lambda(M_Pl)=0 or explicitly add a new selector/premise; "
                "the latter is not retained closure under the current one-axiom surface"
            ),
            "why_shortest": "It can reproduce numerical y_t if the selector is accepted.",
            "current_blocker": "all current stationarity shortcuts are no-go/conditional",
        },
    ]

    result = {
        "actual_current_surface_status": "open / retained closure not yet reached",
        "verdict": (
            "The current PR #230 surface has no retained top-Yukawa closure.  "
            "All tested non-MC shortcuts are blocked or conditional.  The shortest "
            "honest retained routes are: strict direct or joint FH/LSZ physical "
            "measurement, a new scalar pole-residue/common-dressing theorem, or "
            "a newly derived Planck stationarity selector.  Newer support shows "
            "source-scaling, Feshbach projection, same-source invariant readout, "
            "and substrate source units are not the hard blockers.  The hard "
            "blockers are production pole/matching evidence or the microscopic "
            "interacting scalar denominator, zero-mode/IR limiting order, pole "
            "residue, and common dressing.  These cannot be assumed."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No route currently satisfies retained-proposal conditions.",
        "direct_certificates": direct_meta,
        "required_certificates": required_certificates,
        "closure_routes": closure_routes,
        "exact_next_action": (
            "Do not run more small pilot MC for closure.  Either run the strict "
            "production physical-response manifest and follow it with pole/LSZ "
            "and matching analysis, or derive the microscopic interacting scalar "
            "denominator/residue theorem from the retained action."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
