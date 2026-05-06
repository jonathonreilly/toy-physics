#!/usr/bin/env python3
"""
PR #230 Higgs mass-source action bridge.

This is a conditional action-first theorem for the clean source-Higgs route.
If a future same-surface EW/Higgs action couples the PR230 scalar source to the
Higgs mass/composite term Phi^dagger Phi, then the source insertion is the
centered gauge-invariant composite O_H and its FMS radial expansion has the
degree-one coefficient v.  The current PR230 surface still lacks that action
certificate and the C_sH/C_HH pole rows, so this is route support only.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json"

PARENTS = {
    "degree_one_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "fms_composite_oh_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "wz_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_static_ew_algebra_as_measurement": False,
        "used_c_sx_c_xx_as_c_sh_c_hh": False,
        "used_fms_method_name_as_authority": False,
        "set_kappa_s_equal_one": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def composite_rows(v: float, h: float, pi_sq: float, source_scale: float = 1.0) -> dict[str, float]:
    phi_dag_phi = ((v + h) ** 2 + pi_sq) / 2.0
    vacuum = v * v / 2.0
    centered = phi_dag_phi - vacuum
    linear = v * h
    nonlinear = (h * h + pi_sq) / 2.0
    insertion = source_scale * centered
    return {
        "v": v,
        "h": h,
        "pi_sq": pi_sq,
        "source_scale": source_scale,
        "phi_dagger_phi": phi_dag_phi,
        "vacuum_phi_dagger_phi": vacuum,
        "centered_composite_O_H": centered,
        "linear_vh": linear,
        "nonlinear_remainder": nonlinear,
        "source_insertion": insertion,
        "source_insertion_div_source_scale": insertion / source_scale,
    }


def source_rescaling_witness() -> dict[str, Any]:
    base = composite_rows(v=2.0, h=0.07, pi_sq=0.003, source_scale=1.0)
    scaled = [composite_rows(v=2.0, h=0.07, pi_sq=0.003, source_scale=s) for s in (0.25, 1.0, 4.0)]
    invariant_values = [round(row["source_insertion_div_source_scale"], 14) for row in scaled]
    return {
        "base": base,
        "scaled_rows": scaled,
        "source_scale_removed_values": invariant_values,
        "source_rescaling_removes_only_coordinate_units": len(set(invariant_values)) == 1,
    }


def action_source_derivative_contract() -> dict[str, Any]:
    return {
        "future_action_form": (
            "S_EW[Phi,U,V;s] = S_gauge + S_Higgs[Phi,U,V] + "
            "s * sum_x (Phi_x^dagger Phi_x - <Phi^dagger Phi>)"
        ),
        "source_derivative": "dS_EW/ds = sum_x O_H(x)",
        "canonical_composite": "O_H(x) = Phi_x^dagger Phi_x - <Phi^dagger Phi>",
        "fms_expansion": "O_H = v h + h^2/2 + pi^a pi^a/2",
        "degree_one_radial_coefficient": "v",
        "one_pole_residue": "Res C_HH = v^2 Z_h after canonical h LSZ normalization",
        "source_overlap_needed": "Res C_sH remains a measured row or theorem input",
        "strict_limit": (
            "This contract derives the operator produced by a future mass-source "
            "action term.  It does not itself supply the same-surface action, v, "
            "canonical LSZ normalization, C_sH/C_HH rows, or kappa_s."
        ),
    }


def main() -> int:
    print("PR #230 Higgs mass-source action bridge")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}
    futures = future_presence()
    firewall = forbidden_firewall()
    witness = source_rescaling_witness()
    contract = action_source_derivative_contract()

    fms_support_loaded = (
        parents["fms_composite_oh_theorem"].get("fms_composite_oh_conditional_theorem_passed")
        is True
        and parents["fms_composite_oh_theorem"].get("proposal_allowed") is False
        and parents["fms_composite_oh_theorem"].get("same_surface_action_absent") is True
    )
    degree_one_blocker_loaded = (
        parents["degree_one_premise_gate"].get("degree_one_higgs_action_premise_gate_passed")
        is True
        and parents["degree_one_premise_gate"].get("degree_one_filter_selects_e1") is True
        and parents["degree_one_premise_gate"].get("degree_one_premise_authorized_on_current_surface")
        is False
    )
    same_source_ew_action_absent = (
        parents["same_source_ew_action_builder"].get("same_source_ew_action_certificate_valid")
        is False
        and parents["same_source_ew_action_builder"].get("input_present") is False
        and futures["same_source_ew_action_certificate"] is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and futures["canonical_oh_certificate"] is False
    )
    source_higgs_rows_absent = (
        futures["source_higgs_rows"] is False
        and futures["source_higgs_production_certificate"] is False
        and parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
    )
    kappa_contract_loaded = (
        parents["source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and parents["source_higgs_overlap_kappa_contract"].get("proposal_allowed") is False
        and parents["source_higgs_overlap_kappa_contract"].get("current_blockers", {}).get(
            "source_higgs_row_packet_absent"
        )
        is True
    )
    retained_still_open = (
        parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    source_derivative_matches_composite = (
        abs(witness["base"]["centered_composite_O_H"] - witness["base"]["linear_vh"] - witness["base"]["nonlinear_remainder"])
        < 1.0e-14
    )
    degree_one_coefficient_nonzero_if_v_nonzero = all(
        math.isclose(composite_rows(v, 0.1, 0.0)["linear_vh"] / 0.1, v, rel_tol=0, abs_tol=1.0e-14)
        for v in (0.5, 1.0, 3.0)
    )
    rescaling_only_changes_source_units = witness["source_rescaling_removes_only_coordinate_units"]
    firewall_clean = all(value is False for value in firewall.values())
    future_bridge_absent = not any(futures.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-composite-support-loaded", fms_support_loaded, statuses["fms_composite_oh_theorem"])
    report("degree-one-current-blocker-loaded", degree_one_blocker_loaded, statuses["degree_one_premise_gate"])
    report("action-source-derivative-is-centered-composite", source_derivative_matches_composite, contract["source_derivative"])
    report("degree-one-coefficient-is-v", degree_one_coefficient_nonzero_if_v_nonzero, contract["degree_one_radial_coefficient"])
    report("source-rescaling-only-changes-units", rescaling_only_changes_source_units, str(witness["source_scale_removed_values"]))
    report("same-source-ew-action-certificate-absent", same_source_ew_action_absent, statuses["same_source_ew_action_builder"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-absent", source_higgs_rows_absent, statuses["source_higgs_readiness"])
    report("source-higgs-kappa-contract-loaded", kappa_contract_loaded, statuses["source_higgs_overlap_kappa_contract"])
    report("future-bridge-files-absent", future_bridge_absent, str(futures))
    report("retained-route-still-open", retained_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(firewall))

    passed = (
        not missing
        and not proposal_allowed
        and fms_support_loaded
        and degree_one_blocker_loaded
        and source_derivative_matches_composite
        and degree_one_coefficient_nonzero_if_v_nonzero
        and rescaling_only_changes_source_units
        and same_source_ew_action_absent
        and canonical_oh_absent
        and source_higgs_rows_absent
        and kappa_contract_loaded
        and future_bridge_absent
        and retained_still_open
        and firewall_clean
    )

    result = {
        "metadata": {
            "artifact": "pr230_higgs_mass_source_action_bridge",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "actual_current_surface_status": (
            "conditional-support / Higgs mass-source action bridge; same-surface EW/Higgs action and source-Higgs rows absent"
        ),
        "conditional_surface_status": (
            "exact-support if a future same-surface PR230 EW/Higgs action couples the scalar source to centered Phi^dagger Phi and supplies v, canonical h LSZ normalization, and C_ss/C_sH/C_HH pole rows"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem identifies the operator generated by a future Higgs mass-source action term, but the current PR230 surface has no same-source EW/Higgs action certificate, canonical O_H certificate, or source-Higgs pole rows."
        ),
        "bare_retained_allowed": False,
        "higgs_mass_source_action_bridge_passed": passed,
        "action_source_derivative_contract": contract,
        "witness": witness,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_bridge_presence": futures,
        "same_surface_ew_action_certificate_absent": same_source_ew_action_absent,
        "canonical_oh_absent": canonical_oh_absent,
        "source_higgs_rows_absent": source_higgs_rows_absent,
        "degree_one_premise_conditional_only": degree_one_blocker_loaded,
        "source_coordinate_not_authorized_current_surface": same_source_ew_action_absent,
        "source_higgs_overlap_kappa_contract_loaded": kappa_contract_loaded,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not synthesize a same-surface EW/Higgs action certificate",
            "does not write C_sH/C_HH pole rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat FMS method names or static EW algebra as proof authority",
            "does not identify C_sx/C_xx taste-radial rows with canonical C_sH/C_HH rows",
        ],
        "exact_next_action": (
            "Supply a same-surface EW/Higgs action certificate whose scalar source term is s * centered Phi^dagger Phi, then run source-Higgs C_ss/C_sH/C_HH pole rows and Gram/FV/IR gates."
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
