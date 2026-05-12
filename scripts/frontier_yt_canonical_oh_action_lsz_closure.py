#!/usr/bin/env python3
"""
PR #230 canonical O_H action/LSZ closure attempt.

This runner tries the narrow action-first route: derive a same-surface
canonical-Higgs radial operator O_H from the accepted Cl(3)/Z3 action and LSZ
normalization primitives.  It does not use source-only rows, H_unit, Ward
identity, observed targets, alpha_LM, plaquette/u0, or alias imports as
closure inputs.

If the action/LSZ premise is absent, it writes the exact source-Higgs interface
needed by the production row owner, rather than widening the route inventory.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_canonical_oh_action_lsz_closure_2026-05-12.json"
INTERFACE_OUTPUT = (
    ROOT / "outputs" / "yt_canonical_oh_action_lsz_source_higgs_interface_2026-05-12.json"
)

PARENTS = {
    "legendre_source_pole": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_operator_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_repo_authority": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "canonical_scalar_import": "outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json",
    "fms_construction": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "osp_oh_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "osp_oh_assumption_audit": "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json",
    "source_higgs_contract": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "same_source_ew_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "sm_one_higgs_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

TEXTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
    "ew_higgs_gauge_mass": "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
}

FORBIDDEN_IMPORT_FLAGS = {
    "uses_h_unit": False,
    "uses_yt_ward_identity": False,
    "uses_y_t_bare": False,
    "uses_alpha_lm": False,
    "uses_plaquette_or_u0": False,
    "uses_observed_target_selectors": False,
    "uses_alias_imports": False,
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def find_radial_tangent_gate() -> list[str]:
    candidates: list[str] = []
    for path in (ROOT / "scripts").glob("frontier_yt_*"):
        name = path.name.lower()
        if ("radial" in name and "tangent" in name) or "degree_one_radial" in name:
            candidates.append(display(path))
    return sorted(candidates)


def rotation_counterfamily() -> list[dict[str, Any]]:
    rows = []
    for theta in (0.0, math.pi / 8.0, math.pi / 4.0, math.pi / 3.0):
        c = math.cos(theta)
        s = math.sin(theta)
        rows.append(
            {
                "theta": theta,
                "cos_theta": c,
                "sin_theta": s,
                "Res_C_sp_sp": 1.0,
                "Res_C_HH": 1.0,
                "Res_C_sp_H": c,
                "source_higgs_gram_delta": 1.0 - c * c,
                "interpretation": (
                    "LSZ unit residues for O_sp and O_H do not force the "
                    "overlap to be +/-1 unless an action identity or pole "
                    "Gram-purity row removes the orthogonal component."
                ),
            }
        )
    return rows


def agent4_interface() -> dict[str, Any]:
    return {
        "interface_kind": "canonical_oh_action_lsz_source_higgs_input_contract",
        "ready_for_source_higgs_rows": False,
        "blocked_reason": "accepted action/LSZ O_H certificate is absent on the current PR230 surface",
        "operator_certificate_required": {
            "certificate_kind": "canonical_higgs_operator",
            "same_surface_cl3z3": True,
            "same_source_coordinate": True,
            "source_coordinate": "same uniform additive lattice scalar source s entering m_bare + s",
            "operator_id": "nonempty stable id for the canonical Higgs radial operator",
            "operator_definition": "action-derived O_H or gauge-invariant radial FMS operator, not a diagonal vertex by fiat",
            "accepted_action_certificate": "outputs/...json or docs/...md proving the same-surface EW/Higgs action",
            "action_surface_id": "same_surface_cl3_z3_ew_higgs_action",
            "action_field_id": "dynamic Higgs doublet/radial mode field id on that action",
            "canonical_higgs_operator_identity_passed": True,
            "identity_certificate": "non-shortcut proof reference",
            "identity_certificate_kind": "canonical_higgs_identity_theorem",
            "canonical_higgs_operator_normalization_passed": True,
            "normalization_certificate": "non-shortcut proof reference",
            "normalization_certificate_kind": "canonical_higgs_lsz_normalization",
            "source_overlap_closure_mode": "source_higgs_gram_purity",
            "forbidden_shortcut_audit_passed": True,
            "hunit_used_as_operator": False,
            "static_ew_algebra_used_as_operator": False,
            "diagonal_vertex": {
                "kind": "site_color_diagonal_values | constant_site_color_diagonal | staggered_parity_site_color_diagonal",
                "normalization": "must be derived from the action/LSZ certificate, not fitted to a target",
            },
            "canonical_normalization": {
                "kinetic_term_convention": "Euclidean scalar kinetic term normalized as 1/2 (partial h_R)^2 for the radial field",
                "field_rescaling": "h_R = Z_H^{-1/2} h_bare after the action certificate fixes Z_H",
                "vev_convention": "<H> = (0, v/sqrt(2)) in the EW normalization, with O_H the radial fluctuation",
                "sign_convention": "O_H sign may be chosen, but only an overall sign is free after the identity certificate",
                "pole_residue_target": "unit residue for the canonically normalized h_R field; composite O_H residues must be measured and normalized by the certificate",
            },
            "lsz_residue_convention": {
                "euclidean_pole_variable": "x = p^2 - p_star^2",
                "connected_two_point_residue": "Res_C_AB = lim_{x->0} x C_AB(p)",
                "source_pole_operator": "O_sp = sqrt(dGamma_ss/dx|pole) O_s, so Res(C_sp,sp)=1",
                "canonical_higgs_operator": "O_H is accepted only after its action certificate and C_HH pole residue convention are both supplied",
                "gram_purity_test": "Res(C_sH)^2 = Res(C_ss) Res(C_HH), equivalently Delta=0 and |rho_sH|=1",
            },
            "firewall": {
                "used_observed_targets_as_selectors": False,
                "used_yt_ward_identity": False,
                "used_alpha_lm_or_plaquette": False,
                "used_hunit_matrix_element_readout": False,
                "used_y_t_bare": False,
                "used_alias_imports": False,
            },
        },
        "measurement_rows_required_after_certificate": {
            "production_phase_metadata": True,
            "same_ensemble": True,
            "same_source_coordinate": True,
            "operator_certificate_ref": "the accepted certificate above",
            "correlators": ["C_ss", "C_sH", "C_HH"],
            "pole_residue_rows": [
                {
                    "pole_id": "common isolated scalar pole id",
                    "p2_pole_or_mass_lattice": "required with uncertainty",
                    "Res_C_ss": "required",
                    "Res_C_sH": "required",
                    "Res_C_HH": "required",
                    "residue_covariance": "required for strict row use",
                    "isolated_pole_or_model_class_certificate": "required",
                    "finite_volume_ir_zero_mode_threshold_certificates": "required",
                }
            ],
            "strict_row_compatibility": {
                "C_ss": "same-source scalar two-point pole residue",
                "C_sH": "same-ensemble cross pole residue between O_s/O_sp side and certified O_H",
                "C_HH": "certified O_H self pole residue",
                "strict_limit": "finite-mode rows alone are not pole residues",
            },
        },
        "forbidden_shortcuts": [
            "H_unit",
            "yt_ward_identity",
            "y_t_bare",
            "alpha_LM",
            "plaquette/u0",
            "observed target selectors",
            "static EW algebra as operator identity",
            "source-only O_sp schema padding",
            "alias imports",
        ],
        "exact_missing_primitive": (
            "A same-surface accepted EW/Higgs action and LSZ pinning theorem "
            "that proves the PR230 source-pole direction is the canonical Higgs "
            "radial direction, or equivalently supplies the accepted O_H "
            "certificate consumed by C_ss/C_sH/C_HH production rows."
        ),
    }


def main() -> int:
    print("PR #230 canonical O_H action/LSZ closure attempt")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    missing_certs = [name for name, cert in certs.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    radial_tangent_gates = find_radial_tangent_gate()
    minimal = texts["minimal_axioms"]
    harness = texts["production_harness"]
    ew_note = texts["ew_higgs_gauge_mass"]
    sm_note = texts["sm_one_higgs"]

    amin_allowed = {
        "cl3_local_algebra": "Cl(3)" in minimal,
        "z3_spatial_substrate": "Z^3" in minimal or "Z3" in minimal,
        "staggered_dirac_partition": "staggered-Dirac" in minimal or "staggered" in minimal,
        "uniform_scalar_source": "same uniform additive lattice scalar source" in harness,
        "legendre_lsz_source_pole": certs["legendre_source_pole"].get("source_pole_operator_constructed") is True,
    }
    forbidden_import_audit_passed = all(value is False for value in FORBIDDEN_IMPORT_FLAGS.values())

    current_action_surface = {
        "qcd_staggered_top_harness_present": "SU(3) Wilson" in harness and "staggered" in harness,
        "source_higgs_measurement_shell_present": all(
            token in harness
            for token in (
                "--source-higgs-operator-certificate",
                "C_ss/C_sH/C_HH",
                "stochastic_source_higgs_cross_correlator",
            )
        ),
        "source_higgs_shell_requires_certificate": (
            "--source-higgs-operator-certificate is required for C_sH/C_HH rows" in harness
        ),
        "dynamic_ew_higgs_action_in_harness": all(
            token in harness for token in ("SU(2)xU(1)", "Higgs doublet", "W_mu", "B_mu")
        ),
        "ew_note_assumes_h_after_supplied": "Assume a neutral Higgs vacuum" in ew_note,
        "sm_one_higgs_leaves_yukawa_values_free": "does not select the numerical entries" in sm_note,
    }

    same_surface_action_missing = (
        "same-source EW action not defined" in status(certs["same_source_ew_action"])
        and certs["same_source_ew_action"].get("same_source_ew_action_ready") is False
        and not current_action_surface["dynamic_ew_higgs_action_in_harness"]
    )
    canonical_operator_absent = (
        "canonical-Higgs operator certificate absent" in status(certs["canonical_operator_gate"])
        and certs["canonical_operator_gate"].get("candidate_valid") is False
    )
    canonical_realization_open = (
        "canonical-Higgs operator realization gate not passed"
        in status(certs["canonical_operator_realization"])
        and certs["canonical_operator_realization"].get("canonical_higgs_operator_realization_gate_passed")
        is False
    )
    repo_hidden_oh_absent = certs["canonical_repo_authority"].get("repo_authority_found") is False
    fms_packet_blocks_current_surface = (
        certs["fms_construction"].get("fms_oh_certificate_available") is False
        and "FMS O_H certificate construction blocked" in status(certs["fms_construction"])
    )
    contract_is_support_only = (
        "source-Higgs Gram-purity contract witness" in status(certs["source_higgs_contract"])
        and certs["source_higgs_contract"].get("proposal_allowed") is False
    )
    source_higgs_launch_blocked = (
        certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and certs["source_higgs_readiness"].get("operator_certificate_present") is False
    )
    assembly_rejects_current = (
        certs["assembly"].get("current_evaluation", {}).get("assembly_passed") is False
        and certs["assembly"].get("proposal_allowed") is False
    )
    campaign_status_open = certs["campaign_status"].get("proposal_allowed") is False

    rotation_rows = rotation_counterfamily()
    rotation_freedom_killed = all(
        math.isclose(abs(row["Res_C_sp_H"]), 1.0, abs_tol=1.0e-12) for row in rotation_rows
    )

    same_surface_cl3_z3_derived = (
        all(amin_allowed.values())
        and not same_surface_action_missing
        and not canonical_operator_absent
        and not canonical_realization_open
        and not fms_packet_blocks_current_surface
        and rotation_freedom_killed
    )
    accepted_current_surface = same_surface_cl3_z3_derived and assembly_rejects_current is False
    closure_succeeds = same_surface_cl3_z3_derived and accepted_current_surface

    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("a-min-allowed-premises-present", all(amin_allowed.values()), json.dumps(amin_allowed, sort_keys=True))
    report("forbidden-import-audit-passed", forbidden_import_audit_passed, json.dumps(FORBIDDEN_IMPORT_FLAGS, sort_keys=True))
    report("degree-one-radial-tangent-gate-availability-recorded", True, f"available={radial_tangent_gates}")
    report("qcd-action-surface-present", current_action_surface["qcd_staggered_top_harness_present"], "current production action")
    report("source-higgs-shell-requires-certificate", current_action_surface["source_higgs_shell_requires_certificate"], "instrumentation guard")
    report("same-surface-ew-higgs-action-missing", same_surface_action_missing, status(certs["same_source_ew_action"]))
    report("canonical-operator-certificate-absent", canonical_operator_absent, status(certs["canonical_operator_gate"]))
    report("canonical-operator-realization-open", canonical_realization_open, status(certs["canonical_operator_realization"]))
    report("repo-hidden-oh-absent", repo_hidden_oh_absent, status(certs["canonical_repo_authority"]))
    report("fms-packet-blocks-current-surface", fms_packet_blocks_current_surface, status(certs["fms_construction"]))
    report("source-higgs-contract-support-only", contract_is_support_only, status(certs["source_higgs_contract"]))
    report("source-higgs-launch-blocked-until-oh", source_higgs_launch_blocked, status(certs["source_higgs_readiness"]))
    report("rotation-freedom-not-killed-by-lsz-alone", not rotation_freedom_killed, "counterfamily has Delta>0 for theta != 0")
    report("assembly-rejects-current-surface", assembly_rejects_current, status(certs["assembly"]))
    report("campaign-status-remains-open", campaign_status_open, status(certs["campaign_status"]))
    report("same-surface-cl3-z3-derived-is-false", same_surface_cl3_z3_derived is False, f"value={same_surface_cl3_z3_derived}")
    report("accepted-current-surface-is-false", accepted_current_surface is False, f"value={accepted_current_surface}")

    interface = agent4_interface()
    interface["parent_certificates"] = PARENTS
    interface["radial_tangent_gates_available"] = radial_tangent_gates
    interface["strict_rows_compatible"] = True
    interface["proposal_allowed"] = False
    interface["proposal_allowed_reason"] = (
        "This interface is a row contract only. It becomes launch-ready only "
        "after the accepted action/LSZ O_H certificate exists."
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / canonical O_H action-LSZ closure primitive absent",
        "conditional_surface_status": (
            "exact support for Agent 4 source-Higgs rows after a future accepted "
            "same-surface EW/Higgs action and O_H LSZ-pinning certificate is supplied"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The accepted action currently contains the QCD/staggered top "
            "source surface and a guarded source-Higgs measurement shell, but "
            "not a same-surface dynamic EW/Higgs action or O_H identity/"
            "normalization certificate. LSZ normalization of O_sp does not "
            "remove the O_H = cos(theta) O_sp + sin(theta) O_chi freedom."
        ),
        "bare_retained_allowed": False,
        "same_surface_cl3_z3_derived": same_surface_cl3_z3_derived,
        "accepted_current_surface": accepted_current_surface,
        "canonical_normalization_fields": interface["operator_certificate_required"]["canonical_normalization"],
        "lsz_residue_convention": interface["operator_certificate_required"]["lsz_residue_convention"],
        "forbidden_import_flags": FORBIDDEN_IMPORT_FLAGS,
        "strict_rows_compatible": True,
        "strict_rows_compatibility": interface["measurement_rows_required_after_certificate"]["strict_row_compatibility"],
        "closure_succeeds": closure_succeeds,
        "a_min_allowed_premises": amin_allowed,
        "current_action_surface": current_action_surface,
        "action_first_lsz_checks": {
            "same_surface_action_missing": same_surface_action_missing,
            "canonical_operator_absent": canonical_operator_absent,
            "canonical_realization_open": canonical_realization_open,
            "repo_hidden_oh_absent": repo_hidden_oh_absent,
            "fms_packet_blocks_current_surface": fms_packet_blocks_current_surface,
            "source_higgs_contract_support_only": contract_is_support_only,
            "source_higgs_launch_blocked": source_higgs_launch_blocked,
            "rotation_freedom_killed_by_lsz_alone": rotation_freedom_killed,
        },
        "rotation_counterfamily": rotation_rows,
        "narrow_obstruction": (
            "The PR230 accepted action has no dynamic same-surface Higgs "
            "doublet/radial field and no action-derived LSZ identity equating "
            "the source-pole operator O_sp with the canonical Higgs radial "
            "operator O_H. Therefore canonical O_H authority is not certified."
        ),
        "exact_missing_primitive": interface["exact_missing_primitive"],
        "agent4_source_higgs_interface": display(INTERFACE_OUTPUT),
        "parent_certificates": PARENTS,
        "radial_tangent_gates_available": radial_tangent_gates,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not launch or duplicate live chunk execution",
            "does not define O_H by fiat",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed targets, or alias imports",
            "does not treat source-only O_sp, FMS literature, static EW algebra, or finite C_ss/C_sH/C_HH rows as O_H authority",
        ],
        "exact_next_action": (
            "Agent 4 can proceed only after the interface certificate is made "
            "real: supply a same-surface accepted EW/Higgs action plus the "
            "canonical O_H identity/normalization certificate, then run "
            "source-Higgs C_ss/C_sH/C_HH production rows and the existing "
            "builder/postprocessor gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    INTERFACE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    INTERFACE_OUTPUT.write_text(json.dumps(interface, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"Wrote source-Higgs interface: {display(INTERFACE_OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
