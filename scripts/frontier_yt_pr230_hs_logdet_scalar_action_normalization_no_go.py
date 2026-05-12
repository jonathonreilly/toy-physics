#!/usr/bin/env python3
"""
PR #230 HS/logdet scalar-action normalization no-go.

This runner attacks the remaining action-first shortcut after the lane-1
action-premise and logdet-neutral-mixing boundaries:

    source/logdet data + formal Hubbard-Stratonovich rewrite
        => canonical same-surface O_H action/LSZ authority

The current answer is no.  A formal auxiliary-field rewrite can preserve the
integrated source functional while changing the auxiliary field normalization,
source coupling, and neutral source-Higgs overlap.  Therefore it is not an
accepted current-surface Higgs action theorem without a same-surface
four-fermion/kernel covariance, dynamic scalar carrier, canonical LSZ metric,
and strict C_ss/C_sH/C_HH pole rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_hs_logdet_scalar_action_normalization_no_go_2026-05-12.json"
)

PARENTS = {
    "lane1_action_premise": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "logdet_hessian": "outputs/yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json",
    "hs_rpa_pole_condition": "outputs/yt_hs_rpa_pole_condition_attempt_2026-05-01.json",
    "scalar_kernel_enhancement_import": "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json",
    "scalar_pole_determinant": "outputs/yt_scalar_pole_determinant_gate_2026-05-01.json",
    "scalar_ladder_eigen_derivative": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "scalar_bs_kernel_residue_degeneracy": "outputs/yt_scalar_bs_kernel_residue_degeneracy_2026-05-01.json",
    "scalar_carrier_projector_closure": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
    "canonical_oh_hard_residual": "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_higgs_or_yukawa_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "added_scalar_contact_coupling_as_axiom": False,
    "set_auxiliary_normalization_by_unit_convention": False,
    "set_source_higgs_overlap_to_one": False,
    "treated_formal_hs_field_as_physical_higgs": False,
    "treated_source_only_logdet_as_two_source_rows": False,
    "relabelled_C_sx_C_xx_as_C_sH_C_HH": False,
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


def hs_rescaling_family() -> list[dict[str, Any]]:
    """
    Gaussian HS identity for one source current J:

        exp(1/2 K J^2) = int dphi exp[-phi^2/(2K) + J phi]

    With chi = a phi, the same integrated source functional is represented as

        int dchi exp[-chi^2/(2 a^2 K) + (J/a) chi].

    The source kernel K is invariant, but the auxiliary propagator, field
    normalization, and source coupling vary.  Source-only data therefore do not
    pick a canonical Higgs LSZ normalization.
    """
    source_current = 0.4
    kernel = 1.7
    source_functional_log_weight = 0.5 * kernel * source_current**2
    rows = []
    for scale in (0.5, 1.0, 2.0):
        auxiliary_propagator = scale * scale * kernel
        source_coupling = 1.0 / scale
        rows.append(
            {
                "field_scale_a": scale,
                "source_current_J": source_current,
                "integrated_source_kernel_K": kernel,
                "source_functional_log_weight": source_functional_log_weight,
                "auxiliary_propagator": auxiliary_propagator,
                "source_coupling_to_auxiliary": source_coupling,
                "coupling_squared_times_propagator": source_coupling**2
                * auxiliary_propagator,
                "lsz_like_field_norm": math.sqrt(auxiliary_propagator),
                "readout_factor_if_auxiliary_is_called_H": source_coupling,
            }
        )
    return rows


def neutral_rotation_family() -> list[dict[str, Any]]:
    """
    If a second neutral auxiliary direction is not fixed by the same-surface
    action, source-only rows remain unchanged while the candidate Higgs overlap
    changes as cos(theta).
    """
    kernel = 1.7
    rows = []
    for theta in (0.0, math.pi / 6.0, math.pi / 3.0):
        overlap = math.cos(theta)
        rows.append(
            {
                "theta": theta,
                "source_source_residue_C_ss": kernel,
                "candidate_HH_residue_C_HH": kernel,
                "candidate_source_H_residue_C_sH": overlap * kernel,
                "gram_purity_ratio": overlap * overlap,
                "source_only_rows_unchanged": True,
                "candidate_source_higgs_overlap": overlap,
            }
        )
    return rows


def rounded_set(rows: list[dict[str, Any]], key: str) -> set[float]:
    return {round(float(row[key]), 12) for row in rows}


def main() -> int:
    print("PR #230 HS/logdet scalar-action normalization no-go")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    scale_rows = hs_rescaling_family()
    rotation_rows = neutral_rotation_family()
    source_kernel_fixed = (
        len(rounded_set(scale_rows, "source_functional_log_weight")) == 1
        and len(rounded_set(scale_rows, "coupling_squared_times_propagator")) == 1
    )
    auxiliary_normalization_varies = (
        len(rounded_set(scale_rows, "auxiliary_propagator")) == len(scale_rows)
        and len(rounded_set(scale_rows, "source_coupling_to_auxiliary"))
        == len(scale_rows)
        and len(rounded_set(scale_rows, "lsz_like_field_norm")) == len(scale_rows)
    )
    source_only_rotation_rows_fixed = (
        len(rounded_set(rotation_rows, "source_source_residue_C_ss")) == 1
        and all(row["source_only_rows_unchanged"] for row in rotation_rows)
    )
    source_higgs_overlap_varies = (
        len(rounded_set(rotation_rows, "candidate_source_H_residue_C_sH"))
        == len(rotation_rows)
        and len(rounded_set(rotation_rows, "gram_purity_ratio")) == len(rotation_rows)
        and len(rounded_set(rotation_rows, "candidate_source_higgs_overlap"))
        == len(rotation_rows)
    )

    lane1_action_blocks = (
        certs["lane1_action_premise"].get("exact_negative_boundary_passed") is True
        and certs["lane1_action_premise"].get("hs_rewrite_authority_present")
        is False
        and certs["lane1_action_premise"].get("proposal_allowed") is False
    )
    logdet_blocks_two_source_rows = (
        certs["logdet_hessian"].get("exact_negative_boundary_passed") is True
        and certs["logdet_hessian"].get("logdet_hessian_bridge_closes_pr230")
        is False
        and certs["logdet_hessian"].get("proposal_allowed") is False
    )
    hs_rpa_needs_kernel = (
        "new kernel theorem" in statuses["hs_rpa_pole_condition"]
        and certs["hs_rpa_pole_condition"].get("proposal_allowed") is False
    )
    scalar_kernel_import_absent = (
        "scalar-kernel enhancement import audit"
        in statuses["scalar_kernel_enhancement_import"]
        and certs["scalar_kernel_enhancement_import"].get("proposal_allowed")
        is False
    )
    pole_determinant_support_only = (
        "scalar pole determinant gate" in statuses["scalar_pole_determinant"]
        and certs["scalar_pole_determinant"].get("proposal_allowed") is False
    )
    ladder_derivative_support_only = (
        "scalar ladder eigen-derivative gate"
        in statuses["scalar_ladder_eigen_derivative"]
        and certs["scalar_ladder_eigen_derivative"].get("proposal_allowed")
        is False
    )
    bs_residue_degeneracy_blocks = (
        "degeneracy" in statuses["scalar_bs_kernel_residue_degeneracy"]
        and certs["scalar_bs_kernel_residue_degeneracy"].get("proposal_allowed")
        is False
    )
    carrier_projector_open = (
        "scalar carrier-projector closure attempt blocked"
        in statuses["scalar_carrier_projector_closure"]
        and certs["scalar_carrier_projector_closure"].get("proposal_allowed")
        is False
    )
    canonical_oh_residual_open = (
        "canonical O_H hard residual not closed"
        in statuses["canonical_oh_hard_residual"]
        and certs["canonical_oh_hard_residual"].get("proposal_allowed") is False
    )
    aggregate_gates_reject = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    no_go_passed = (
        not missing
        and not proposal_parents
        and source_kernel_fixed
        and auxiliary_normalization_varies
        and source_only_rotation_rows_fixed
        and source_higgs_overlap_varies
        and lane1_action_blocks
        and logdet_blocks_two_source_rows
        and hs_rpa_needs_kernel
        and scalar_kernel_import_absent
        and pole_determinant_support_only
        and ladder_derivative_support_only
        and bs_residue_degeneracy_blocks
        and carrier_projector_open
        and canonical_oh_residual_open
        and aggregate_gates_reject
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_parents,
        f"proposal_allowed={proposal_parents}",
    )
    report(
        "hs-source-functional-invariant-under-field-rescale",
        source_kernel_fixed,
        f"rows={scale_rows}",
    )
    report(
        "hs-auxiliary-normalization-varies",
        auxiliary_normalization_varies,
        f"rows={scale_rows}",
    )
    report(
        "source-only-neutral-rotation-rows-fixed",
        source_only_rotation_rows_fixed,
        f"rows={rotation_rows}",
    )
    report(
        "candidate-source-higgs-overlap-varies",
        source_higgs_overlap_varies,
        f"rows={rotation_rows}",
    )
    report("lane1-action-premise-blocks", lane1_action_blocks, statuses["lane1_action_premise"])
    report(
        "logdet-source-only-two-source-row-boundary-loaded",
        logdet_blocks_two_source_rows,
        statuses["logdet_hessian"],
    )
    report("hs-rpa-needs-kernel-theorem", hs_rpa_needs_kernel, statuses["hs_rpa_pole_condition"])
    report(
        "scalar-kernel-import-absent",
        scalar_kernel_import_absent,
        statuses["scalar_kernel_enhancement_import"],
    )
    report(
        "scalar-pole-determinant-support-only",
        pole_determinant_support_only,
        statuses["scalar_pole_determinant"],
    )
    report(
        "scalar-ladder-eigen-derivative-support-only",
        ladder_derivative_support_only,
        statuses["scalar_ladder_eigen_derivative"],
    )
    report(
        "bs-kernel-residue-degeneracy-blocks",
        bs_residue_degeneracy_blocks,
        statuses["scalar_bs_kernel_residue_degeneracy"],
    )
    report(
        "scalar-carrier-projector-open",
        carrier_projector_open,
        statuses["scalar_carrier_projector_closure"],
    )
    report(
        "canonical-oh-hard-residual-open",
        canonical_oh_residual_open,
        statuses["canonical_oh_hard_residual"],
    )
    report("aggregate-gates-reject-proposal", aggregate_gates_reject, "full/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report(
        "hs-logdet-scalar-action-normalization-no-go",
        no_go_passed,
        "auxiliary rewrite does not derive canonical O_H normalization",
    )

    result = {
        "actual_current_surface_status": (
            "support / exact negative boundary: HS-logdet auxiliary scalar "
            "action normalization does not derive canonical O_H on the current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface four-fermion/kernel "
            "covariance, dynamic scalar carrier, accepted action, canonical LSZ "
            "metric, and strict C_ss/C_sH/C_HH pole rows are supplied"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The same integrated source/logdet functional admits HS rescalings "
            "and neutral rotations that change auxiliary normalization and "
            "source-Higgs overlap.  A formal auxiliary field is therefore not "
            "canonical O_H authority without an independent same-surface action "
            "and LSZ certificate."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "hs_logdet_scalar_action_normalization_no_go_passed": no_go_passed,
        "same_surface_cl3_z3_derived": False,
        "accepted_current_surface": False,
        "canonical_oh_identity_derived": False,
        "canonical_scalar_lsz_fixed": False,
        "hs_auxiliary_rewrite_unique": False,
        "source_higgs_pole_rows_strict": False,
        "hs_rescaling_counterfamily": scale_rows,
        "neutral_rotation_counterfamily": rotation_rows,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "open_imports": [
            "same-surface four-fermion or scalar-channel kernel/covariance",
            "dynamic scalar carrier derived from Cl(3)/Z3 or explicitly adopted action extension",
            "canonical scalar LSZ/metric normalization",
            "source-Higgs overlap or Gram rows with a certified O_H operator",
            "strict C_ss/C_sH/C_HH pole rows and FV/IR/model-class authority",
        ],
        "allowed_escape_routes": [
            "derive a native Cl(3)/Z3 scalar action and LSZ metric",
            "supply a two-source same-surface determinant functional with certified canonical O_H",
            "measure strict C_ss/C_sH/C_HH pole rows after an accepted O_H theorem",
            "derive a neutral primitive transfer theorem that fixes the Higgs direction",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define y_t_bare or use H_unit/Ward matrix-element readout",
            "does not use observed top/Higgs/y_t values as selectors",
            "does not use alpha_LM, plaquette, or u0",
            "does not set auxiliary normalization, source-Higgs overlap, c2, Z_match, or kappa_s to one",
            "does not relabel support-only C_sx/C_xx rows as physical C_sH/C_HH rows",
        ],
        "exact_next_action": (
            "Do not treat HS/logdet auxiliary fields as canonical O_H.  Continue "
            "with a real native scalar/action/LSZ theorem, a certified two-source "
            "O_H determinant functional, a neutral primitive transfer theorem, "
            "or strict source-Higgs pole rows after O_H is independently supplied."
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
