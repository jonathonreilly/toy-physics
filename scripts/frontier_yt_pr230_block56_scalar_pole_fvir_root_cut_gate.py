#!/usr/bin/env python3
"""
PR #230 Block56 scalar-pole/FVIR root cut gate.

Block54 reduced physical readout authorization to scalar pole/FVIR authority
plus canonical-Higgs/neutral-transfer authority.  Block55 cut the second root.
This gate attacks the remaining scalar pole/model-class/FV/IR root on the
current PR230 surface.

It does not assert a permanent no-go against scalar LSZ.  It checks a sharper
current-surface claim: the existing FH-LSZ, Stieltjes, contact, holonomic,
finite-volume, and source-Higgs row artifacts do not supply the strict scalar
authority needed for positive PR230 closure.  A future closure must provide a
same-surface scalar denominator/contact theorem plus threshold/FVIR/pole
control, or bypass scalar-source normalization through strict physical rows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block56_scalar_pole_fvir_root_cut_gate_2026-05-12.json"
)

PARENTS = {
    "block54_response_readout_reduction": "outputs/yt_pr230_block54_response_readout_reduction_gate_2026-05-12.json",
    "block55_canonical_neutral_primitive_cut": "outputs/yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json",
    "strict_scalar_lsz_moment_fv": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "fh_lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "fh_lsz_model_class_semantic_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
    "stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pade_stieltjes_bounds": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "polefit8x8_stieltjes_proxy": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "complete_bernstein_inverse": "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json",
    "scalar_lsz_holonomic_exact": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
    "scalar_lsz_carleman_tauberian": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
    "polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
    "polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
    "pole_saturation_threshold": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "threshold_authority_import_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "finite_volume_pole_saturation": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "soft_continuum_threshold": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_finite_shell_pslq_selector": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "treated_contact_subtraction_as_chosen": False,
    "treated_fv_discreteness_as_pole_saturation": False,
    "treated_source_higgs_contract_as_rows": False,
    "claimed_effective_or_proposed_retained": False,
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


def yes(cert: dict[str, Any], key: str) -> bool:
    return cert.get(key) is True


def no(cert: dict[str, Any], key: str) -> bool:
    return cert.get(key) is False


def current_scalar_authority_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_scalar_object",
            "current_satisfied": False,
            "required": (
                "same-surface scalar two-point/denominator object with a fixed "
                "source scheme and contact subtraction"
            ),
        },
        {
            "id": "positive_stieltjes_or_exact_denominator",
            "current_satisfied": False,
            "required": (
                "strict Stieltjes/moment certificate with all-order/tail "
                "control, or an exact microscopic denominator theorem"
            ),
        },
        {
            "id": "isolated_pole_residue_interval",
            "current_satisfied": False,
            "required": (
                "isolated scalar pole with a positive tight residue interval; "
                "finite-shell fit intervals with zero lower bound do not qualify"
            ),
        },
        {
            "id": "threshold_and_fv_ir",
            "current_satisfied": False,
            "required": (
                "continuum threshold/gap plus multivolume FV/IR/zero-mode "
                "limiting-order authority"
            ),
        },
        {
            "id": "canonical_readout_or_physical_bypass",
            "current_satisfied": False,
            "required": (
                "canonical O_H/source-overlap bridge with strict C_ss/C_sH/C_HH "
                "rows, or a physical W/Z/source-Higgs bypass carrying the same "
                "pole/FVIR authority"
            ),
        },
        {
            "id": "forbidden_import_firewall",
            "current_satisfied": True,
            "required": (
                "no H_unit, Ward, y_t_bare, alpha_LM/plaquette/u0, observed "
                "selector, unit kappa/c2/Z_match, or contact/FV shortcut"
            ),
        },
    ]


def main() -> int:
    print("PR #230 Block56 scalar-pole/FVIR root cut gate")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    block54_scalar_root_survives = (
        yes(certs["block54_response_readout_reduction"], "response_readout_root_reduction_passed")
        and no(certs["block54_response_readout_reduction"], "proposal_allowed")
        and "scalar pole/model-class/FV/IR authority"
        in certs["block54_response_readout_reduction"].get(
            "remaining_roots_after_reduction", []
        )
    )
    block55_not_scalar_closure = (
        yes(certs["block55_canonical_neutral_primitive_cut"], "block55_canonical_neutral_primitive_cut_passed")
        and no(certs["block55_canonical_neutral_primitive_cut"], "proposal_allowed")
        and no(certs["block55_canonical_neutral_primitive_cut"], "canonical_neutral_root_closed")
    )

    raw_scalar_rows_not_strict_lsz = (
        yes(certs["strict_scalar_lsz_moment_fv"], "strict_scalar_lsz_moment_fv_authority_gate_passed")
        and no(certs["strict_scalar_lsz_moment_fv"], "strict_scalar_lsz_moment_fv_authority_present")
        and yes(certs["strict_scalar_lsz_moment_fv"], "current_raw_c_ss_proxy_fails_stieltjes_monotonicity")
        and no(certs["strict_scalar_lsz_moment_fv"], "multivolume_fv_ir_authority_present")
        and no(certs["strict_scalar_lsz_moment_fv"], "isolated_pole_model_class_authority_present")
        and no(certs["strict_scalar_lsz_moment_fv"], "threshold_gap_authority_present")
    )
    model_class_not_authority = (
        "model-class gate blocks" in statuses["fh_lsz_model_class"]
        and no(certs["fh_lsz_model_class"], "proposal_allowed")
        and "model-class semantic firewall passed"
        in statuses["fh_lsz_model_class_semantic_firewall"]
        and no(certs["fh_lsz_model_class_semantic_firewall"], "proposal_allowed")
    )
    stieltjes_moment_not_certificate = (
        "Stieltjes moment-certificate gate" in statuses["stieltjes_moment_certificate"]
        and no(certs["stieltjes_moment_certificate"], "proposal_allowed")
        and no(certs["stieltjes_moment_certificate"], "moment_certificate_gate_passed")
        and "Pade-Stieltjes bounds gate" in statuses["pade_stieltjes_bounds"]
        and no(certs["pade_stieltjes_bounds"], "proposal_allowed")
        and no(certs["pade_stieltjes_bounds"], "pade_stieltjes_bounds_gate_passed")
    )
    current_proxy_not_positive_spectral = (
        no(certs["polefit8x8_stieltjes_proxy"], "proposal_allowed")
        and no(certs["polefit8x8_stieltjes_proxy"], "stieltjes_proxy_certificate_passed")
        and no(certs["complete_bernstein_inverse"], "proposal_allowed")
        and no(certs["complete_bernstein_inverse"], "complete_bernstein_inverse_certificate_passed")
    )

    holonomic_counterfamily = certs["scalar_lsz_holonomic_exact"].get(
        "counterfamily", {}
    )
    holonomic_finite_shell_ambiguous = (
        no(certs["scalar_lsz_holonomic_exact"], "proposal_allowed")
        and no(certs["scalar_lsz_holonomic_exact"], "holonomic_exact_authority_passed")
        and holonomic_counterfamily.get("same_finite_shell_values") is True
        and holonomic_counterfamily.get("residues_differ") is True
        and holonomic_counterfamily.get("stieltjes_or_threshold_authority_supplied")
        is False
    )
    carleman_counterfamily = certs["scalar_lsz_carleman_tauberian"].get(
        "finite_prefix_counterfamily", {}
    )
    finite_prefix_not_determinate = (
        no(certs["scalar_lsz_carleman_tauberian"], "proposal_allowed")
        and no(certs["scalar_lsz_carleman_tauberian"], "carleman_tauberian_determinacy_passed")
        and carleman_counterfamily.get("finite_prefix_stieltjes_counterfamily_passed")
        is True
        and carleman_counterfamily.get("same_finite_prefix") is True
        and carleman_counterfamily.get("pole_residue_changes") is True
    )

    contact_subtraction_not_identified = (
        "contact-subtraction identifiability obstruction"
        in statuses["contact_subtraction_identifiability"]
        and no(certs["contact_subtraction_identifiability"], "proposal_allowed")
        and yes(
            certs["contact_subtraction_identifiability"],
            "contact_subtraction_identifiability_obstruction_passed",
        )
        and no(
            certs["contact_subtraction_identifiability"],
            "contact_subtraction_certificate_present",
        )
        and no(
            certs["contact_subtraction_identifiability"],
            "stieltjes_certificate_from_contact_subtraction_passed",
        )
    )
    affine_contact_shortcut_closed = (
        "affine contact complete-monotonicity no-go"
        in statuses["affine_contact_complete_monotonicity"]
        and no(certs["affine_contact_complete_monotonicity"], "proposal_allowed")
        and yes(
            certs["affine_contact_complete_monotonicity"],
            "affine_contact_complete_monotonicity_no_go_passed",
        )
    )
    polynomial_contact_shortcut_closed = (
        "finite-shell polynomial contact non-identifiability no-go"
        in statuses["polynomial_contact_finite_shell"]
        and no(certs["polynomial_contact_finite_shell"], "proposal_allowed")
        and yes(
            certs["polynomial_contact_finite_shell"],
            "polynomial_contact_finite_shell_no_go_passed",
        )
        and "polynomial contact repair not scalar-LSZ authority"
        in statuses["polynomial_contact_repair"]
        and no(certs["polynomial_contact_repair"], "proposal_allowed")
        and yes(certs["polynomial_contact_repair"], "polynomial_contact_repair_no_go_passed")
        and no(
            certs["polynomial_contact_repair"],
            "stieltjes_certificate_from_polynomial_contact_passed",
        )
    )

    threshold_fv_ir_not_authority = (
        no(certs["pole_saturation_threshold"], "proposal_allowed")
        and no(certs["pole_saturation_threshold"], "pole_saturation_threshold_gate_passed")
        and no(certs["threshold_authority_import_audit"], "proposal_allowed")
        and "threshold-authority import audit"
        in statuses["threshold_authority_import_audit"]
        and no(certs["finite_volume_pole_saturation"], "proposal_allowed")
        and "finite-volume pole-saturation obstruction"
        in statuses["finite_volume_pole_saturation"]
        and no(certs["soft_continuum_threshold"], "proposal_allowed")
    )
    source_higgs_strict_rows_absent = (
        "direct source-Higgs pole-row contract" in statuses["source_higgs_direct_pole_row_contract"]
        and no(certs["source_higgs_direct_pole_row_contract"], "proposal_allowed")
        and "strict rows absent"
        in statuses["source_higgs_pole_row_acceptance_contract"]
        and yes(
            certs["source_higgs_pole_row_acceptance_contract"],
            "source_higgs_pole_row_acceptance_contract_passed",
        )
        and no(certs["source_higgs_pole_row_acceptance_contract"], "proposal_allowed")
    )
    aggregate_still_open = (
        no(certs["full_positive_assembly"], "proposal_allowed")
        and no(certs["campaign_status"], "proposal_allowed")
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    scalar_pole_fvir_root_closed = False
    block56_scalar_pole_fvir_root_cut_passed = (
        not missing
        and not proposal_parents
        and block54_scalar_root_survives
        and block55_not_scalar_closure
        and raw_scalar_rows_not_strict_lsz
        and model_class_not_authority
        and stieltjes_moment_not_certificate
        and current_proxy_not_positive_spectral
        and holonomic_finite_shell_ambiguous
        and finite_prefix_not_determinate
        and contact_subtraction_not_identified
        and affine_contact_shortcut_closed
        and polynomial_contact_shortcut_closed
        and threshold_fv_ir_not_authority
        and source_higgs_strict_rows_absent
        and aggregate_still_open
        and firewall_clean
    )

    obstruction_matrix = [
        {
            "root": "raw C_ss as scalar-LSZ object",
            "current_result": "blocked",
            "reason": "raw proxy is positive but violates required non-increasing Stieltjes behavior and has no FV/IR or threshold authority",
            "parent": PARENTS["strict_scalar_lsz_moment_fv"],
        },
        {
            "root": "finite-shell exact/holonomic continuation",
            "current_result": "blocked",
            "reason": "same finite shell values admit holonomic rational continuations with different pole residues",
            "parent": PARENTS["scalar_lsz_holonomic_exact"],
        },
        {
            "root": "finite moment/Stieltjes prefix",
            "current_result": "blocked",
            "reason": "positive measures can share the checked finite prefix while changing the pole atom and higher tail",
            "parent": PARENTS["scalar_lsz_carleman_tauberian"],
        },
        {
            "root": "contact-subtracted scalar object",
            "current_result": "blocked",
            "reason": "current finite rows do not identify a unique same-surface contact subtraction; affine and polynomial repairs are non-authority",
            "parent": PARENTS["contact_subtraction_identifiability"],
        },
        {
            "root": "pole saturation / threshold / FVIR",
            "current_result": "blocked",
            "reason": "near-pole continuum and finite-volume level families keep the residue lower bound at zero without a uniform gap or denominator theorem",
            "parent": PARENTS["finite_volume_pole_saturation"],
        },
        {
            "root": "strict source-Higgs bypass",
            "current_result": "blocked",
            "reason": "only contracts and reduced/noncanonical smoke exist; strict C_ss/C_sH/C_HH production pole rows are absent",
            "parent": PARENTS["source_higgs_direct_pole_row_contract"],
        },
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_parents,
        f"proposal_allowed={proposal_parents}",
    )
    report("block54-scalar-root-survives", block54_scalar_root_survives, statuses["block54_response_readout_reduction"])
    report("block55-not-scalar-closure", block55_not_scalar_closure, statuses["block55_canonical_neutral_primitive_cut"])
    report("raw-scalar-rows-not-strict-lsz", raw_scalar_rows_not_strict_lsz, statuses["strict_scalar_lsz_moment_fv"])
    report("model-class-not-authority", model_class_not_authority, statuses["fh_lsz_model_class"])
    report("stieltjes-moment-not-certificate", stieltjes_moment_not_certificate, statuses["stieltjes_moment_certificate"])
    report("current-proxy-not-positive-spectral", current_proxy_not_positive_spectral, statuses["polefit8x8_stieltjes_proxy"])
    report("holonomic-finite-shell-ambiguous", holonomic_finite_shell_ambiguous, str(holonomic_counterfamily.get("construction")))
    report("finite-prefix-not-determinate", finite_prefix_not_determinate, str(carleman_counterfamily.get("construction")))
    report("contact-subtraction-not-identified", contact_subtraction_not_identified, statuses["contact_subtraction_identifiability"])
    report("affine-contact-shortcut-closed", affine_contact_shortcut_closed, statuses["affine_contact_complete_monotonicity"])
    report("polynomial-contact-shortcut-closed", polynomial_contact_shortcut_closed, statuses["polynomial_contact_finite_shell"])
    report("threshold-fv-ir-not-authority", threshold_fv_ir_not_authority, statuses["finite_volume_pole_saturation"])
    report("source-higgs-strict-rows-absent", source_higgs_strict_rows_absent, statuses["source_higgs_direct_pole_row_contract"])
    report("aggregate-still-open", aggregate_still_open, statuses["full_positive_assembly"])
    report("forbidden-import-firewall-clean", firewall_clean, "no forbidden proof input used")
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact-support / Block56 scalar-pole-FVIR root cut; current "
            "scalar/FH-LSZ artifacts do not close scalar pole/model-class/FV/IR authority"
        ),
        "verdict": (
            "The remaining scalar authority root is now cut on the current "
            "surface.  Existing FH-LSZ rows, finite-shell fits, Stieltjes/Pade "
            "checks, contact-subtraction repairs, holonomic continuations, and "
            "finite-volume discreteness do not provide strict scalar-LSZ pole "
            "authority.  The positive route remains open only through a "
            "same-surface scalar denominator/contact theorem with threshold and "
            "FVIR control, or through strict physical source-Higgs/WZ rows that "
            "bypass scalar-source normalization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No current artifact supplies a same-surface scalar object, "
            "contact subtraction, strict positive spectral/moment certificate, "
            "isolated-pole residue interval, threshold/FVIR authority, or strict "
            "C_ss/C_sH/C_HH physical rows."
        ),
        "bare_retained_allowed": False,
        "block56_scalar_pole_fvir_root_cut_passed": block56_scalar_pole_fvir_root_cut_passed,
        "scalar_pole_fvir_root_closed": scalar_pole_fvir_root_closed,
        "current_scalar_authority_contract": current_scalar_authority_contract(),
        "remaining_scalar_authority_obligations": [
            "same-surface scalar denominator/contact/subtraction theorem",
            "strict positive Stieltjes or exact denominator certificate with all-order/tail control",
            "isolated scalar pole plus tight positive residue interval",
            "continuum threshold/gap and multivolume FV/IR limiting-order authority",
            "canonical O_H/source-overlap bridge with strict rows, or a physical W/Z/source-Higgs bypass",
        ],
        "obstruction_matrix": obstruction_matrix,
        "counterfamily_witnesses": {
            "holonomic_same_samples_different_residue": holonomic_counterfamily,
            "finite_prefix_same_moments_different_residue": carleman_counterfamily,
        },
        "condition_checks": {
            "block54_scalar_root_survives": block54_scalar_root_survives,
            "block55_not_scalar_closure": block55_not_scalar_closure,
            "raw_scalar_rows_not_strict_lsz": raw_scalar_rows_not_strict_lsz,
            "model_class_not_authority": model_class_not_authority,
            "stieltjes_moment_not_certificate": stieltjes_moment_not_certificate,
            "current_proxy_not_positive_spectral": current_proxy_not_positive_spectral,
            "holonomic_finite_shell_ambiguous": holonomic_finite_shell_ambiguous,
            "finite_prefix_not_determinate": finite_prefix_not_determinate,
            "contact_subtraction_not_identified": contact_subtraction_not_identified,
            "affine_contact_shortcut_closed": affine_contact_shortcut_closed,
            "polynomial_contact_shortcut_closed": polynomial_contact_shortcut_closed,
            "threshold_fv_ir_not_authority": threshold_fv_ir_not_authority,
            "source_higgs_strict_rows_absent": source_higgs_strict_rows_absent,
            "aggregate_still_open": aggregate_still_open,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not claim a permanent no-go against scalar LSZ",
            "does not define y_t through a matrix element or y_t_bare",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, or Z_match=1",
            "does not treat finite-shell, holonomic, contact-repaired, FV-discrete, or source-Higgs contract artifacts as physical y_t readouts",
        ],
        "exact_next_action": (
            "Pursue a genuinely new same-surface scalar denominator/contact "
            "theorem with threshold/FVIR control, or bypass scalar-source "
            "normalization with strict source-Higgs/WZ physical rows.  If no "
            "such artifact lands, wait for chunk outputs only as support and "
            "keep PR230 draft/open."
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
