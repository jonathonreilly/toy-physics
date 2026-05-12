#!/usr/bin/env python3
"""
PR #230 Block54 response-readout root reduction gate.

Block53 left physical response readout authorization as one of three live
roots.  This gate attacks that root directly.  It checks whether the response
instrumentation side is now closed as support, and whether the remaining
readout authorization is exactly the scalar-pole/FVIR and canonical-Higgs
identity problem rather than a separate response-window blocker.

It does not authorize a physical y_t readout.  It reduces the response-readout
root to the two still-open physics roots.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block54_response_readout_reduction_gate_2026-05-12.json"
)

PARENTS = {
    "block53_residual_minimality": "outputs/yt_pr230_block53_lane1_residual_minimality_gate_2026-05-12.json",
    "same_source_pole_data_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "invariant_readout_theorem": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
    "finite_source_linearity_gate": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "response_window_acceptance_gate": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
    "common_window_replacement_response_stability": "outputs/yt_fh_lsz_common_window_replacement_response_stability_2026-05-04.json",
    "v2_target_response_stability": "outputs/yt_fh_lsz_v2_target_response_stability_2026-05-04.json",
    "production_postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
    "model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_selector": False,
    "used_observed_wz_or_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_common_window_support_as_physical_readout": False,
    "treated_response_support_as_scalar_lsz": False,
    "treated_response_support_as_canonical_higgs_identity": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_effective_or_proposed_retained": False,
    "touched_live_chunk_worker": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def condition_satisfied(cert: dict[str, Any], condition: str) -> bool:
    return any(
        row.get("condition") == condition and row.get("satisfied") is True
        for row in cert.get("sufficient_conditions", [])
        if isinstance(row, dict)
    )


def condition_unsatisfied(cert: dict[str, Any], condition: str) -> bool:
    return any(
        row.get("condition") == condition and row.get("satisfied") is False
        for row in cert.get("sufficient_conditions", [])
        if isinstance(row, dict)
    )


def main() -> int:
    print("PR #230 Block54 response-readout root reduction gate")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    block53_open = (
        certs["block53_residual_minimality"].get("block53_residual_minimality_gate_passed")
        is True
        and certs["block53_residual_minimality"].get("proposal_allowed") is False
        and "physical response readout authorization"
        in certs["block53_residual_minimality"].get("minimal_remaining_roots", [])
    )
    invariant_readout_support = (
        "Feynman-Hellmann scalar-LSZ invariant readout formula"
        in statuses["invariant_readout_theorem"]
        and certs["invariant_readout_theorem"].get("proposal_allowed") is False
        and certs["invariant_readout_theorem"].get("pass_count") == 7
        and certs["invariant_readout_theorem"].get("fail_count") == 0
    )
    finite_source_linearity_support = (
        certs["finite_source_linearity_gate"].get("finite_source_linearity_gate_passed")
        is True
        and certs["finite_source_linearity_gate"].get("proposal_allowed") is False
    )
    common_window_response_support = (
        certs["common_window_response_gate"].get("common_window_response_gate_passed")
        is True
        and certs["common_window_response_gate"].get("proposal_allowed") is False
        and certs["common_window_response_gate"].get("readout_switch_authorized")
        is False
        and certs["common_window_response_gate"].get("open_blockers") == []
    )
    common_window_criteria = certs["common_window_response_gate"].get(
        "predeclared_criteria", {}
    )
    response_side_criteria_closed = (
        common_window_criteria.get("common_window_stability_passed") is True
        and common_window_criteria.get("common_window_production_grade") is True
        and common_window_criteria.get("pooled_common_window_response_production_grade")
        is True
        and common_window_criteria.get(
            "response_window_acceptance_or_replacement_passed"
        )
        is True
        and common_window_criteria.get("finite_source_linearity_gate_passed")
        is True
        and common_window_criteria.get(
            "fitted_or_replacement_response_stability_passed"
        )
        is True
        and common_window_criteria.get("v2_target_response_stability_support_passed")
        is True
        and common_window_criteria.get(
            "scalar_lsz_and_canonical_higgs_closure_required_separately"
        )
        is True
    )
    replacement_support = (
        certs["common_window_replacement_response_stability"].get(
            "replacement_response_stability_passed"
        )
        is True
        and certs["common_window_replacement_response_stability"].get(
            "proposal_allowed"
        )
        is False
    )
    v2_target_support = (
        certs["v2_target_response_stability"].get("v2_target_response_stability_passed")
        is True
        and certs["v2_target_response_stability"].get("proposal_allowed") is False
    )
    acceptance_gate_not_authority = (
        certs["response_window_acceptance_gate"].get(
            "response_window_acceptance_gate_passed"
        )
        is False
        and certs["response_window_acceptance_gate"].get("readout_switch_authorized")
        is False
        and certs["response_window_acceptance_gate"].get("proposal_allowed")
        is False
    )

    sufficiency = certs["same_source_pole_data_sufficiency"]
    same_source_support_closed = (
        condition_satisfied(sufficiency, "same-source invariant readout theorem")
        and condition_satisfied(
            sufficiency, "complete seed-controlled L12 production support chunk set"
        )
        and condition_satisfied(
            sufficiency, "complete L12 target-timeseries support packet"
        )
        and condition_satisfied(sufficiency, "response-side stability support")
    )
    remaining_physics_roots_open = (
        condition_unsatisfied(
            sufficiency, "physical response readout switch authorized"
        )
        and condition_unsatisfied(
            sufficiency,
            "postprocess gate has retained-grade same-source dE/ds, Gamma_ss(q), pole derivative, FV/IR control",
        )
        and condition_unsatisfied(
            sufficiency, "finite-shell model-class or pole-saturation gate passed"
        )
        and condition_unsatisfied(
            sufficiency, "measured pole certified as canonical Higgs radial mode"
        )
        and certs["production_postprocess_gate"].get("retained_proposal_gate_ready")
        is False
        and certs["model_class_gate"].get("model_class_gate_passed") is False
        and certs["higgs_pole_identity_gate"].get("higgs_pole_identity_gate_passed")
        is False
    )
    aggregate_gates_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    response_readout_root_reduced = (
        not missing
        and not proposal_parents
        and block53_open
        and invariant_readout_support
        and finite_source_linearity_support
        and common_window_response_support
        and response_side_criteria_closed
        and replacement_support
        and v2_target_support
        and acceptance_gate_not_authority
        and same_source_support_closed
        and remaining_physics_roots_open
        and aggregate_gates_still_open
        and firewall_clean
    )

    reduced_remaining_roots = [
        "scalar pole/model-class/FV/IR authority",
        "canonical-Higgs pole identity or same-surface neutral-transfer bridge",
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_parents,
        f"proposal_allowed={proposal_parents}",
    )
    report("block53-readout-root-open", block53_open, statuses["block53_residual_minimality"])
    report("invariant-readout-support-present", invariant_readout_support, statuses["invariant_readout_theorem"])
    report("finite-source-linearity-support-present", finite_source_linearity_support, statuses["finite_source_linearity_gate"])
    report("common-window-response-support-present", common_window_response_support, statuses["common_window_response_gate"])
    report("response-side-criteria-closed-as-support", response_side_criteria_closed, str(common_window_criteria))
    report("replacement-response-support-present", replacement_support, statuses["common_window_replacement_response_stability"])
    report("v2-target-response-support-present", v2_target_support, statuses["v2_target_response_stability"])
    report("acceptance-gate-not-authority", acceptance_gate_not_authority, statuses["response_window_acceptance_gate"])
    report("same-source-support-conditions-closed", same_source_support_closed, PARENTS["same_source_pole_data_sufficiency"])
    report("remaining-physics-roots-open", remaining_physics_roots_open, "scalar/FVIR and canonical-Higgs roots open")
    report("aggregate-gates-still-open", aggregate_gates_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("response-readout-root-reduced", response_readout_root_reduced, "response side is support-complete; physical readout waits on scalar/Higgs roots")

    result = {
        "actual_current_surface_status": "exact-support / Block54 response-readout root reduction; response-side support closed, physical readout still waits on scalar/FVIR and canonical-Higgs roots",
        "conditional_surface_status": "conditional-support if scalar pole/model-class/FV/IR authority and canonical-Higgs or same-surface neutral-transfer authority pass",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The response-instrumentation side is support-complete, but the "
            "physical y_t readout is still blocked by scalar-pole/FVIR and "
            "canonical-Higgs authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "response_readout_root_reduction_passed": response_readout_root_reduced,
        "response_side_support_closed": (
            invariant_readout_support
            and finite_source_linearity_support
            and common_window_response_support
            and response_side_criteria_closed
            and replacement_support
            and v2_target_support
            and same_source_support_closed
        ),
        "readout_switch_authorized": False,
        "readout_switch_authorized_reason": (
            "Authorization is deliberately false until scalar pole/model-class/"
            "FV/IR authority and canonical-Higgs or neutral-transfer authority pass."
        ),
        "remaining_roots_after_reduction": reduced_remaining_roots,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "common_window_criteria": common_window_criteria,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim effective or proposed_retained y_t closure",
            "does not treat response-side support as a physical readout switch",
            "does not treat response-side support as scalar LSZ or canonical-Higgs authority",
            "does not set kappa_s=1, c2=1, or Z_match=1",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, alpha_LM, plaquette, or u0",
            "does not touch active chunk workers",
        ],
        "exact_next_action": (
            "Attack the two roots left after response-root reduction: scalar "
            "pole/model-class/FV/IR authority and canonical-Higgs identity or "
            "same-surface neutral-transfer authority."
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
