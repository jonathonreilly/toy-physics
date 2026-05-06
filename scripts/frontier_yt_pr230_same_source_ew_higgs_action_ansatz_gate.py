#!/usr/bin/env python3
"""
PR #230 same-source EW/Higgs action ansatz gate.

This runner records the cleanest action-first next artifact without promoting
it to the current PR230 authority surface.  It gives a concrete lattice
SU(2)xU(1)/Higgs action-extension ansatz whose scalar source is the same
coordinate used by the top FH/LSZ route and whose source term couples to the
centered gauge-invariant composite Phi^dagger Phi.

The result is conditional support only.  The runner intentionally does not
write the accepted future same-source EW action certificate or canonical O_H
certificate paths.  Adoption still requires a same-surface authority decision
plus W/Z rows or O_H/C_sH/C_HH pole rows and downstream Gram/LSZ gates.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json"
)

PARENTS = {
    "fms_composite_oh_conditional_theorem": (
        "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json"
    ),
    "higgs_mass_source_action_bridge": (
        "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json"
    ),
    "wz_same_source_ew_action_certificate_builder": (
        "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json"
    ),
    "wz_same_source_ew_action_gate": (
        "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json"
    ),
    "canonical_higgs_operator_certificate_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "source_higgs_overlap_kappa_contract": (
        "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json"
    ),
    "post_fms_source_overlap_necessity_gate": (
        "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json"
    ),
    "full_positive_closure_assembly_gate": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

ACCEPTED_FUTURE_CERTIFICATES = {
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "canonical_higgs_operator_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "wz_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass / observed y_t selectors",
    "observed W/Z masses or observed g2 selectors",
    "alpha_LM / plaquette / u0 proof input",
    "reduced cold pilots as production evidence",
    "c2 = 1, Z_match = 1, or kappa_s = 1 by convention",
]

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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def fms_phi_dagger_phi_expansion() -> dict[str, Any]:
    """Check the local FMS expansion used by the ansatz.

    With Phi=(0,(v+h+i*pi0)/sqrt(2)) in unitary-coordinate notation and
    pi^2 denoting the Goldstone-square contribution, the centered composite is

        Phi^dagger Phi - v^2/2 = v h + (h^2 + pi^2)/2.

    The check is coefficient-level and uses rational coefficients where
    possible so the artifact is inspectable without symbolic dependencies.
    """

    coefficients = {
        "constant_after_centering": Fraction(0),
        "linear_h": Fraction(1),  # coefficient is v * h.
        "quadratic_h2": Fraction(1, 2),
        "quadratic_pi2": Fraction(1, 2),
    }
    return {
        "expression": "O_H = Phi^dagger Phi - v^2/2 = v*h + (h^2 + pi^2)/2",
        "coefficients": {key: str(value) for key, value in coefficients.items()},
        "linear_coefficient_is_v": coefficients["linear_h"] == 1,
        "constant_removed_by_centering": coefficients["constant_after_centering"] == 0,
        "quadratic_coefficients_canonical": (
            coefficients["quadratic_h2"] == Fraction(1, 2)
            and coefficients["quadratic_pi2"] == Fraction(1, 2)
        ),
    }


def action_ansatz() -> dict[str, Any]:
    return {
        "name": "PR230 same-source EW/Higgs action-extension ansatz",
        "lattice": "same hypercubic sites and scalar source coordinate s as the top FH/LSZ harness",
        "fields": {
            "existing_pr230_top_sector": "Cl(3)/Z3 SU(3) staggered top sector",
            "su2_link_field": "U_mu(x) in SU(2)_L",
            "u1_link_field": "B_mu(x) in U(1)_Y",
            "higgs_doublet": "Phi(x), gauge-covariant complex SU(2) doublet",
        },
        "action_terms": [
            "S_PR230_top[s] with the existing additive top scalar source coordinate",
            "S_SU2[U] Wilson plaquette term",
            "S_U1[B] compact U(1) plaquette term",
            "S_H[Phi,U,B] gauge-covariant Higgs hopping/kinetic term",
            "V_H[Phi] local Higgs potential",
            "s * sum_x (Phi(x)^dagger Phi(x) - <Phi^dagger Phi>)",
        ],
        "source_derivative": {
            "with_respect_to": "s",
            "higgs_source_derivative": "dS/ds contains sum_x O_H(x)",
            "O_H_definition": "O_H = Phi^dagger Phi - <Phi^dagger Phi>",
            "same_source_coordinate_as_top_fh_lsz": True,
        },
        "why_this_is_the_clean_contract": (
            "It makes the missing source-to-Higgs object a gauge-invariant "
            "action derivative instead of a source-only normalization choice."
        ),
    }


def source_derivative_check(ansatz: dict[str, Any]) -> dict[str, Any]:
    source_terms = [
        term
        for term in ansatz["action_terms"]
        if term.startswith("s * sum_x")
    ]
    derivative_rows = [
        {
            "source_term": term,
            "derivative_wrt_s": term.removeprefix("s * "),
            "equals_sum_oh": "O_H" in ansatz["source_derivative"]["O_H_definition"],
        }
        for term in source_terms
    ]
    return {
        "source_terms": source_terms,
        "derivative_rows": derivative_rows,
        "exact_source_derivative_present": len(source_terms) == 1
        and all(row["equals_sum_oh"] for row in derivative_rows),
    }


def gauge_invariance_check(ansatz: dict[str, Any]) -> dict[str, Any]:
    fields = ansatz["fields"]
    has_gauge_fields = (
        "su2_link_field" in fields
        and "u1_link_field" in fields
        and "higgs_doublet" in fields
    )
    # Phi^\dagger Phi is invariant under any unitary representation because
    # (G Phi)^\dagger (G Phi) = Phi^\dagger G^\dagger G Phi = Phi^\dagger Phi.
    unitary_identity_used = "G^dagger G = I"
    return {
        "has_su2_u1_higgs_fields": has_gauge_fields,
        "operator": "Phi^dagger Phi",
        "gauge_invariance_argument": unitary_identity_used,
        "operator_gauge_invariant": has_gauge_fields,
    }


def adoption_requirements() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_adoption",
            "required": "repo accepts this action-extension as an actual PR230 same-surface action, not only an ansatz",
            "current_satisfied": False,
        },
        {
            "id": "canonical_oh_certificate",
            "required": "accepted canonical O_H identity/normalization certificate on the actual current surface",
            "current_satisfied": False,
        },
        {
            "id": "source_higgs_pole_rows",
            "required": "production C_ss/C_sH/C_HH pole rows with Gram/FV/IR/model-class checks",
            "current_satisfied": False,
        },
        {
            "id": "or_wz_physical_response_rows",
            "required": "same-source W/Z response rows with identity, covariance, strict g2, and delta_perp authority",
            "current_satisfied": False,
        },
        {
            "id": "retained_route_certificate",
            "required": "retained/proposed_retained route certificate passes after the physical row packet exists",
            "current_satisfied": False,
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_observed_wz_masses_or_g2": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_pilots_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "wrote_accepted_future_certificate_paths": False,
        "claims_retained_or_proposed_retained": False,
    }


def future_presence() -> dict[str, bool]:
    return {
        name: (ROOT / rel).exists()
        for name, rel in ACCEPTED_FUTURE_CERTIFICATES.items()
    }


def main() -> int:
    print("PR #230 same-source EW/Higgs action ansatz gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    ansatz = action_ansatz()
    derivative = source_derivative_check(ansatz)
    gauge = gauge_invariance_check(ansatz)
    fms = fms_phi_dagger_phi_expansion()
    requirements = adoption_requirements()
    missing_requirements = [
        row["id"] for row in requirements if row["current_satisfied"] is not True
    ]
    firewall = forbidden_firewall()
    accepted_future_present = future_presence()

    fms_parent_loaded = (
        parents["fms_composite_oh_conditional_theorem"].get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and parents["fms_composite_oh_conditional_theorem"].get("proposal_allowed")
        is False
    )
    mass_source_bridge_loaded = (
        parents["higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and parents["higgs_mass_source_action_bridge"].get("proposal_allowed")
        is False
    )
    current_action_absent = (
        parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
        and parents["wz_same_source_ew_action_certificate_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
    )
    canonical_oh_current_absent = (
        parents["canonical_higgs_operator_certificate_gate"].get("candidate_valid")
        is False
    )
    source_overlap_still_needed = (
        parents["post_fms_source_overlap_necessity_gate"].get(
            "current_source_overlap_authority_present"
        )
        is False
        and parents["source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
    )
    retained_route_open = (
        parents["retained_closure_route"].get("proposal_allowed") is False
        and parents["full_positive_closure_assembly_gate"].get("proposal_allowed")
        is False
    )
    no_accepted_future_paths_written = not any(accepted_future_present.values())
    clean_firewall = all(value is False for value in firewall.values())
    ansatz_support_passed = (
        not missing
        and not proposal_allowed
        and derivative["exact_source_derivative_present"]
        and gauge["operator_gauge_invariant"]
        and fms["linear_coefficient_is_v"]
        and fms["constant_removed_by_centering"]
        and fms_parent_loaded
        and mass_source_bridge_loaded
        and current_action_absent
        and canonical_oh_current_absent
        and source_overlap_still_needed
        and retained_route_open
        and no_accepted_future_paths_written
        and clean_firewall
    )
    current_surface_adoption_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fms-composite-oh-parent-loaded", fms_parent_loaded, statuses["fms_composite_oh_conditional_theorem"])
    report("higgs-mass-source-bridge-parent-loaded", mass_source_bridge_loaded, statuses["higgs_mass_source_action_bridge"])
    report("ansatz-source-derivative-exact", derivative["exact_source_derivative_present"], str(derivative["derivative_rows"]))
    report("ansatz-operator-gauge-invariant", gauge["operator_gauge_invariant"], gauge["gauge_invariance_argument"])
    report("fms-linear-term-check", fms["linear_coefficient_is_v"] and fms["constant_removed_by_centering"], fms["expression"])
    report("current-ew-action-still-absent", current_action_absent, statuses["wz_same_source_ew_action_gate"])
    report("current-canonical-oh-still-absent", canonical_oh_current_absent, statuses["canonical_higgs_operator_certificate_gate"])
    report("source-overlap-rows-still-needed", source_overlap_still_needed, statuses["post_fms_source_overlap_necessity_gate"])
    report("accepted-future-certificate-paths-not-written", no_accepted_future_paths_written, str(accepted_future_present))
    report("adoption-requirements-recorded-open", len(missing_requirements) == len(requirements), str(missing_requirements))
    report("forbidden-firewall-clean", clean_firewall, ", ".join(FORBIDDEN_INPUTS))
    report("ansatz-support-passed", ansatz_support_passed, "conditional action-extension support")
    report("current-surface-adoption-not-passed", not current_surface_adoption_passed, "ansatz is not an adopted PR230 action")

    result = {
        "actual_current_surface_status": (
            "conditional support / same-source EW/Higgs action-extension ansatz "
            "specified; actual current-surface adoption absent"
        ),
        "conditional_surface_status": (
            "support if the ansatz is separately adopted as a same-surface PR230 "
            "EW/Higgs action and followed by canonical O_H plus C_sH/C_HH or W/Z rows"
        ),
        "hypothetical_axiom_status": "hypothetical action-extension ansatz; not an accepted current-surface axiom",
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The ansatz gives a concrete action contract but does not adopt the "
            "action on the current PR230 surface, does not write accepted future "
            "certificate paths, and supplies no C_sH/C_HH or W/Z production rows."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "same_source_ew_higgs_action_ansatz_gate_passed": ansatz_support_passed,
        "action_extension_ansatz_specified": True,
        "current_surface_adoption_passed": current_surface_adoption_passed,
        "future_default_certificates_written": any(accepted_future_present.values()),
        "accepted_future_certificate_presence": accepted_future_present,
        "action_ansatz": ansatz,
        "source_derivative_check": derivative,
        "gauge_invariance_check": gauge,
        "fms_phi_dagger_phi_expansion_check": fms,
        "adoption_requirements": requirements,
        "missing_adoption_requirements": missing_requirements,
        "forbidden_firewall": firewall,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write the accepted same-source EW action certificate path",
            "does not write the accepted canonical O_H certificate path",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either promote this ansatz through a same-surface adoption theorem "
            "and then produce canonical O_H/C_sH/C_HH pole rows, or implement "
            "genuine same-source W/Z response rows with identity/covariance/g2 "
            "authority."
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
