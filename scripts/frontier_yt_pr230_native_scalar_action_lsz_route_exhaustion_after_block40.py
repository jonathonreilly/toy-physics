#!/usr/bin/env python3
"""
PR #230 native scalar/action/LSZ route exhaustion after Block40.

Block40 closed the last concrete native-scalar shortcut in the active queue:
the formal HS/logdet auxiliary-field normalization route.  This runner checks
whether any current same-surface native scalar/action/LSZ route remains
admissible without a genuinely new primitive.

It does not claim a permanent no-go against scalar/action physics.  It records
the current-surface route boundary: the existing minimal action, FMS support,
HS/logdet rewrites, Legendre transforms, source-reparametrization identities,
effective-potential Hessians, scalar-LSZ bookkeeping, and exact-math finite
shell attempts all leave at least one load-bearing import open.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40_2026-05-12.json"
)

PARENTS = {
    "lane1_action_premise": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "hs_logdet_scalar_action_normalization": "outputs/yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json",
    "legendre_kappa_gauge_freedom": "outputs/yt_legendre_kappa_gauge_freedom_2026-05-01.json",
    "source_reparametrization_gauge": "outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json",
    "scalar_lsz_normalization_cancellation": "outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "effective_potential_hessian_source_overlap": "outputs/yt_effective_potential_hessian_source_overlap_no_go_2026-05-02.json",
    "canonical_scalar_normalization_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "source_to_higgs_lsz_closure": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "scalar_carrier_projector_closure": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
    "scalar_lsz_holonomic_exact_authority": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
    "scalar_lsz_carleman_tauberian_determinacy": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "strict_scalar_lsz_moment_fv_authority": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_higgs_yukawa_or_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "set_kappa_c2_zmatch_or_overlap_to_one": False,
    "relabelled_C_sx_C_xx_as_C_sH_C_HH": False,
    "treated_support_only_fms_as_adopted_action": False,
    "treated_hs_logdet_auxiliary_as_canonical_higgs": False,
    "treated_legendre_transform_as_metric_fixing": False,
    "treated_effective_potential_hessian_as_source_overlap": False,
    "treated_finite_shell_exact_math_as_pole_lsz_authority": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def route_table(statuses: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "route": "minimal Cl(3)/Z3 action premise",
            "current_surface_result": statuses["lane1_action_premise"],
            "closes_current_surface": False,
            "remaining_import": "dynamic Phi/action/canonical O_H/scalar LSZ not derived",
        },
        {
            "route": "FMS candidate/action packet",
            "current_surface_result": statuses["fms_oh_candidate_action_packet"],
            "closes_current_surface": False,
            "remaining_import": "candidate support only; no adopted same-surface EW/Higgs action or strict rows",
        },
        {
            "route": "FMS action-adoption minimal cut",
            "current_surface_result": statuses["fms_action_adoption_minimal_cut"],
            "closes_current_surface": False,
            "remaining_import": "minimal adoption cut still lacks action, LSZ metric, source identity, and pole rows",
        },
        {
            "route": "HS/logdet auxiliary scalar",
            "current_surface_result": statuses["hs_logdet_scalar_action_normalization"],
            "closes_current_surface": False,
            "remaining_import": "auxiliary normalization and source-Higgs overlap vary under rescaling/rotation",
        },
        {
            "route": "Legendre effective action",
            "current_surface_result": statuses["legendre_kappa_gauge_freedom"],
            "closes_current_surface": False,
            "remaining_import": "Legendre transform is covariant under source/operator rescaling",
        },
        {
            "route": "source reparametrization invariant response",
            "current_surface_result": statuses["source_reparametrization_gauge"],
            "closes_current_surface": False,
            "remaining_import": "source normalization remains gauge freedom",
        },
        {
            "route": "scalar LSZ normalization cancellation",
            "current_surface_result": statuses["scalar_lsz_normalization_cancellation"],
            "closes_current_surface": False,
            "remaining_import": "bookkeeping cancellation only; interacting kernel and pole derivative open",
        },
        {
            "route": "source-functional LSZ pole",
            "current_surface_result": statuses["source_functional_lsz_identifiability"],
            "closes_current_surface": False,
            "remaining_import": "source-pole coupling does not determine overlap with canonical Higgs mode",
        },
        {
            "route": "effective-potential Hessian / SSB algebra",
            "current_surface_result": statuses["effective_potential_hessian_source_overlap"],
            "closes_current_surface": False,
            "remaining_import": "Hessian eigenvalues do not fix the microscopic source direction",
        },
        {
            "route": "existing canonical scalar normalization surfaces",
            "current_surface_result": statuses["canonical_scalar_normalization_import"],
            "closes_current_surface": False,
            "remaining_import": "EW/Higgs surfaces assume or structure canonical H; they do not derive PR230 source normalization",
        },
        {
            "route": "source-to-Higgs LSZ closure attempt",
            "current_surface_result": statuses["source_to_higgs_lsz_closure"],
            "closes_current_surface": False,
            "remaining_import": "named source-to-canonical-Higgs LSZ theorem remains open",
        },
        {
            "route": "scalar carrier/projector closure",
            "current_surface_result": statuses["scalar_carrier_projector_closure"],
            "closes_current_surface": False,
            "remaining_import": "physical scalar carrier/projector and K'(pole) remain open",
        },
        {
            "route": "finite-shell exact math / holonomic LSZ",
            "current_surface_result": statuses["scalar_lsz_holonomic_exact_authority"],
            "closes_current_surface": False,
            "remaining_import": "finite shell data do not identify physical denominator or LSZ residue",
        },
        {
            "route": "Carleman/Tauberian scalar LSZ determinacy",
            "current_surface_result": statuses["scalar_lsz_carleman_tauberian_determinacy"],
            "closes_current_surface": False,
            "remaining_import": "strict moment/FV/IR authority remains absent",
        },
        {
            "route": "strict scalar LSZ moment/FV authority gate",
            "current_surface_result": statuses["strict_scalar_lsz_moment_fv_authority"],
            "closes_current_surface": False,
            "remaining_import": "strict scalar moment/FV authority is not present on current surface",
        },
    ]


def main() -> int:
    print("PR #230 native scalar/action/LSZ route exhaustion after Block40")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    routes = route_table(statuses)
    route_closures = [row for row in routes if row["closes_current_surface"]]

    lane1_action_blocks = (
        certs["lane1_action_premise"].get("exact_negative_boundary_passed") is True
        and certs["lane1_action_premise"].get("proposal_allowed") is False
    )
    fms_support_only = (
        certs["fms_oh_candidate_action_packet"].get("same_surface_cl3_z3_derived")
        is False
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface")
        is False
        and certs["fms_action_adoption_minimal_cut"].get("accepted_current_surface")
        is False
    )
    hs_logdet_blocks = (
        certs["hs_logdet_scalar_action_normalization"].get(
            "hs_logdet_scalar_action_normalization_no_go_passed"
        )
        is True
        and certs["hs_logdet_scalar_action_normalization"].get(
            "canonical_scalar_lsz_fixed"
        )
        is False
    )
    legendre_blocks = (
        "Legendre normalization freedom" in statuses["legendre_kappa_gauge_freedom"]
        and certs["legendre_kappa_gauge_freedom"].get("proposal_allowed") is False
    )
    source_reparam_blocks = (
        "source reparametrization gauge" in statuses["source_reparametrization_gauge"]
        and certs["source_reparametrization_gauge"].get("proposal_allowed") is False
    )
    scalar_lsz_bookkeeping_only = (
        "conditional-support" in statuses["scalar_lsz_normalization_cancellation"]
        and certs["scalar_lsz_normalization_cancellation"].get("proposal_allowed")
        is False
    )
    source_functional_overlap_blocks = (
        "source-functional LSZ identifiability theorem"
        in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    effective_potential_blocks = (
        "effective-potential Hessian not source-overlap identity"
        in statuses["effective_potential_hessian_source_overlap"]
        and certs["effective_potential_hessian_source_overlap"].get(
            "proposal_allowed"
        )
        is False
    )
    canonical_scalar_import_blocks = (
        "canonical scalar normalization import audit"
        in statuses["canonical_scalar_normalization_import"]
        and certs["canonical_scalar_normalization_import"].get("proposal_allowed")
        is False
    )
    source_to_higgs_lsz_open = (
        "source-to-Higgs LSZ closure attempt blocked"
        in statuses["source_to_higgs_lsz_closure"]
        and certs["source_to_higgs_lsz_closure"].get("proposal_allowed") is False
    )
    scalar_carrier_projector_open = (
        "scalar carrier-projector closure attempt blocked"
        in statuses["scalar_carrier_projector_closure"]
        and certs["scalar_carrier_projector_closure"].get("proposal_allowed")
        is False
    )
    exact_math_finite_shell_blocks = (
        "scalar-LSZ holonomic exact-authority not"
        in statuses["scalar_lsz_holonomic_exact_authority"]
        and certs["scalar_lsz_holonomic_exact_authority"].get("proposal_allowed")
        is False
        and "Carleman/Tauberian scalar-LSZ determinacy not"
        in statuses["scalar_lsz_carleman_tauberian_determinacy"]
        and certs["scalar_lsz_carleman_tauberian_determinacy"].get(
            "proposal_allowed"
        )
        is False
        and "strict scalar-LSZ moment/FV authority"
        in statuses["strict_scalar_lsz_moment_fv_authority"]
        and certs["strict_scalar_lsz_moment_fv_authority"].get("proposal_allowed")
        is False
    )
    aggregate_gates_reject = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_route_closes = not route_closures
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    route_exhaustion_passed = (
        not missing
        and not proposal_parents
        and lane1_action_blocks
        and fms_support_only
        and hs_logdet_blocks
        and legendre_blocks
        and source_reparam_blocks
        and scalar_lsz_bookkeeping_only
        and source_functional_overlap_blocks
        and effective_potential_blocks
        and canonical_scalar_import_blocks
        and source_to_higgs_lsz_open
        and scalar_carrier_projector_open
        and exact_math_finite_shell_blocks
        and aggregate_gates_reject
        and no_route_closes
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("lane1-action-premise-blocks", lane1_action_blocks, statuses["lane1_action_premise"])
    report("fms-support-only", fms_support_only, statuses["fms_oh_candidate_action_packet"])
    report("hs-logdet-blocks", hs_logdet_blocks, statuses["hs_logdet_scalar_action_normalization"])
    report("legendre-normalization-blocks", legendre_blocks, statuses["legendre_kappa_gauge_freedom"])
    report("source-reparametrization-blocks", source_reparam_blocks, statuses["source_reparametrization_gauge"])
    report("scalar-lsz-bookkeeping-only", scalar_lsz_bookkeeping_only, statuses["scalar_lsz_normalization_cancellation"])
    report("source-functional-overlap-blocks", source_functional_overlap_blocks, statuses["source_functional_lsz_identifiability"])
    report("effective-potential-hessian-blocks", effective_potential_blocks, statuses["effective_potential_hessian_source_overlap"])
    report("canonical-scalar-import-blocks", canonical_scalar_import_blocks, statuses["canonical_scalar_normalization_import"])
    report("source-to-higgs-lsz-open", source_to_higgs_lsz_open, statuses["source_to_higgs_lsz_closure"])
    report("scalar-carrier-projector-open", scalar_carrier_projector_open, statuses["scalar_carrier_projector_closure"])
    report("finite-shell-exact-math-blocks", exact_math_finite_shell_blocks, statuses["scalar_lsz_holonomic_exact_authority"])
    report("aggregate-gates-reject-proposal", aggregate_gates_reject, "full/campaign proposal_allowed=false")
    report("no-native-scalar-action-lsz-route-closes", no_route_closes, f"closures={route_closures}")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report(
        "native-scalar-action-lsz-route-exhaustion-passed",
        route_exhaustion_passed,
        "current native scalar/action/LSZ queue requires a new primitive",
    )

    result = {
        "actual_current_surface_status": (
            "support / exact negative boundary: native scalar/action/LSZ "
            "current-surface route exhausted after Block40 without a new primitive"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface scalar-channel "
            "kernel/covariance, dynamic scalar carrier, accepted action, scalar "
            "LSZ metric, strict C_ss/C_sH/C_HH pole rows, strict W/Z absolute "
            "authority, or neutral-transfer primitive lands"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Every current native scalar/action/LSZ candidate is blocked, "
            "support-only, or conditional.  No route supplies dynamic Phi/action, "
            "canonical O_H identity, scalar LSZ metric, source-Higgs overlap, "
            "or strict pole rows on the current PR230 surface."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "native_scalar_action_lsz_route_exhaustion_passed": route_exhaustion_passed,
        "no_current_native_scalar_action_lsz_route_closes": no_route_closes,
        "route_table": routes,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "remaining_positive_routes": [
            "genuinely new same-surface scalar/action/LSZ primitive with fixed kernel/covariance and scalar metric",
            "strict W/Z physical-response packet with non-observed absolute g2/v authority",
            "same-surface neutral transfer or primitive-cone theorem that fixes the physical Higgs direction",
            "strict source-Higgs C_ss/C_sH/C_HH pole rows after canonical O_H is independently supplied",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not declare a permanent no-go against future scalar/action physics",
            "does not use H_unit, Ward, y_t_bare, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, source-Higgs overlap, or auxiliary normalization to one",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
        ],
        "exact_next_action": (
            "Demote the native scalar/action/LSZ route to closed on the current "
            "surface unless a new primitive appears.  Pivot the campaign to "
            "strict W/Z absolute-authority evidence or same-surface neutral "
            "transfer/primitive-cone theorem work."
        ),
        "summary": {"pass": PASS_COUNT, "fail": FAIL_COUNT},
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
