#!/usr/bin/env python3
"""
PR #230 same-source EW action certificate builder.

The W/Z response bypass and the source-Higgs Gram-purity lane both need more
than static electroweak algebra: they need a same-surface electroweak
gauge/Higgs action block whose scalar source coordinate is the same coordinate
used by the top FH/LSZ source response.  This runner defines and validates that
future certificate contract.  It does not synthesize the action and does not
claim y_t closure when the certificate is absent.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_2026-05-04.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json"

PARENTS = {
    "wz_response_harness_implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
    "wz_correlator_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "same_source_wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_hunit_matrix_element_readout",
    "used_hunit_as_operator",
    "used_yt_ward_identity",
    "used_observed_masses_or_couplings_as_selectors",
    "used_static_ew_algebra_as_measurement",
    "used_alpha_lm_or_plaquette_u0",
    "set_kappa_s_equal_one",
    "set_cos_theta_equal_one",
    "set_c2_equal_one",
    "set_z_match_equal_one",
)

SHORTCUT_REFERENCE_TOKENS = (
    "EW_HIGGS_GAUGE_MASS",
    "SM_ONE_HIGGS",
    "HUNIT",
    "H_UNIT",
    "WARD",
    "OBSERVED",
    "PDG",
    "ALPHA_LM",
    "PLAQUETTE",
    "U0",
    "GATE",
    "GUARD",
    "FIREWALL",
    "CHECKPOINT",
    "CONTRACT",
    "BUILDER",
    "HARNESS",
    "MANIFEST",
    "ABSENCE",
    "ABSENT",
    "OBSTRUCTION",
    "IMPORT_AUDIT",
    "PRODUCTION_ATTEMPT",
    "IMPLEMENTATION_PLAN",
    "MASS_FIT_PATH_GATE",
    "YT_DIRECT_LATTICE_CORRELATOR_PRODUCTION",
)

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def path_ref_ok(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    path = ROOT / str(value)
    return path.exists() and str(value).startswith(("docs/", "outputs/", "scripts/"))


def nonshortcut_path_ref_ok(value: Any) -> bool:
    if not path_ref_ok(value):
        return False
    upper = str(value).upper()
    return not any(token in upper for token in SHORTCUT_REFERENCE_TOKENS)


def validate_action_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "reasons": ["same-source EW action certificate absent"],
            "checks": {},
        }

    fields = candidate.get("fields", {}) if isinstance(candidate.get("fields", {}), dict) else {}
    action = candidate.get("action_terms", {}) if isinstance(candidate.get("action_terms", {}), dict) else {}
    source = candidate.get("source_coupling", {}) if isinstance(candidate.get("source_coupling", {}), dict) else {}
    observables = candidate.get("observables", {}) if isinstance(candidate.get("observables", {}), dict) else {}
    certificates = candidate.get("certificates", {}) if isinstance(candidate.get("certificates", {}), dict) else {}
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall", {}), dict) else {}

    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "same_source_ew_action",
        "phase_supported": candidate.get("phase") in {"theorem", "production_design", "production"},
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "source_coordinate_named": nonempty_string(candidate.get("source_coordinate")),
        "su2_link_field_present": fields.get("su2_link_field") is True,
        "u1_link_field_present": fields.get("u1_link_field") is True,
        "dynamic_higgs_doublet_present": fields.get("dynamic_higgs_doublet") is True,
        "higgs_radial_mode_named": nonempty_string(fields.get("higgs_radial_mode")),
        "su2_wilson_action_present": action.get("su2_wilson_action") is True,
        "u1_gauge_action_present": action.get("u1_gauge_action") is True,
        "gauge_covariant_higgs_kinetic_present": action.get("gauge_covariant_higgs_kinetic") is True,
        "higgs_potential_present": action.get("higgs_potential") is True,
        "source_couples_to_centered_phi_dagger_phi": source.get("couples_to")
        == "centered_phi_dagger_phi",
        "source_operator_centered": source.get("operator_centered") is True,
        "source_matches_top_fh_lsz_coordinate": source.get("matches_top_fh_lsz_source_coordinate") is True,
        "higgs_mass_source_action_bridge_reference": path_ref_ok(
            certificates.get("higgs_mass_source_action_bridge")
        ),
        "higgs_mass_source_action_bridge_kind_allowed": certificates.get(
            "higgs_mass_source_action_bridge_kind"
        )
        == "higgs_mass_source_action_bridge",
        "wz_correlator_observables_defined": observables.get("wz_two_point_correlators") is True,
        "wz_mass_fit_method_defined": nonempty_string(observables.get("wz_mass_fit_method")),
        "canonical_higgs_certificate_reference": path_ref_ok(certificates.get("canonical_higgs_operator_certificate")),
        "canonical_higgs_certificate_not_shortcut": nonshortcut_path_ref_ok(certificates.get("canonical_higgs_operator_certificate")),
        "canonical_higgs_certificate_kind_allowed": certificates.get("canonical_higgs_operator_certificate_kind")
        in {"same_surface_canonical_higgs_operator_certificate", "canonical_higgs_identity_theorem"},
        "sector_overlap_certificate_reference": path_ref_ok(certificates.get("same_source_sector_overlap_certificate")),
        "sector_overlap_certificate_not_shortcut": nonshortcut_path_ref_ok(certificates.get("same_source_sector_overlap_certificate")),
        "sector_overlap_certificate_kind_allowed": certificates.get("same_source_sector_overlap_certificate_kind")
        in {"same_source_sector_overlap_identity", "same_surface_sector_overlap_theorem"},
        "wz_mass_fit_path_certificate_reference": path_ref_ok(certificates.get("wz_correlator_mass_fit_path_certificate")),
        "wz_mass_fit_path_certificate_not_shortcut": nonshortcut_path_ref_ok(certificates.get("wz_correlator_mass_fit_path_certificate")),
        "wz_mass_fit_path_certificate_kind_allowed": certificates.get("wz_correlator_mass_fit_path_certificate_kind")
        in {"production_wz_correlator_mass_fit_path", "same_source_wz_mass_fit_theorem"},
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    checks.update({f"forbidden_{field}_false": firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS})
    reasons = [key for key, ok in checks.items() if not ok]
    return {
        "present": True,
        "valid": not reasons,
        "checks": checks,
        "reasons": reasons,
    }


def acceptance_schema() -> dict[str, Any]:
    return {
        "candidate_path": display(DEFAULT_INPUT),
        "required_top_level": {
            "certificate_kind": "same_source_ew_action",
            "phase": "theorem | production_design | production",
            "same_surface_cl3_z3": True,
            "same_source_coordinate": True,
            "source_coordinate": "same scalar source coordinate used by top FH/LSZ",
        },
        "required_fields": {
            "su2_link_field": True,
            "u1_link_field": True,
            "dynamic_higgs_doublet": True,
            "higgs_radial_mode": "canonical radial mode identifier",
        },
        "required_action_terms": [
            "SU(2) gauge action",
            "U(1) gauge action",
            "gauge-covariant Higgs kinetic term",
            "Higgs potential",
            "source coupled to centered Phi^dagger Phi on the same scalar source coordinate",
        ],
        "required_observables": [
            "W/Z two-point correlators under source shifts",
            "W/Z mass-fit method",
            "same-source top/WZ covariance surface in later measurement rows",
        ],
        "required_certificates": [
            "canonical Higgs operator certificate with non-shortcut reference and allowed kind",
            "Higgs mass-source action bridge reference with allowed kind",
            "same-source sector-overlap certificate with non-shortcut reference and allowed kind",
            "W/Z correlator mass-fit path certificate with non-shortcut reference and allowed kind",
        ],
        "claim_firewall": [f"{field}=false" for field in FORBIDDEN_FALSE_FIELDS],
    }


def shortcut_rejections() -> list[dict[str, str]]:
    return [
        {
            "candidate": "EW gauge-mass diagonalization after H is supplied",
            "rejection": "static dM_W/dh is not a same-source lattice dM_W/ds measurement",
        },
        {
            "candidate": "native SU(2)/hypercharge structural notes",
            "rejection": "structural gauge support is not a production EW gauge/Higgs action block",
        },
        {
            "candidate": "current QCD top FH/LSZ harness",
            "rejection": "the harness guards W/Z rows as absent and has no dynamic EW fields",
        },
        {
            "candidate": "source-Higgs diagonal-vertex shell",
            "rejection": "instrumentation is default-off and lacks accepted O_H identity/normalization",
        },
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 same-source EW action certificate builder")
    print("=" * 72)

    parents = {name: load_rel(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    candidate = load_json(args.input)
    validation = validate_action_certificate(candidate)
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    canonical_higgs_open = (
        parents["canonical_higgs_operator_certificate_gate"].get("candidate_valid") is not True
    )
    sector_overlap_open = (
        "same-source sector-overlap identity obstruction" in parent_statuses["same_source_sector_overlap_identity"]
        and parents["same_source_sector_overlap_identity"].get("sector_overlap_identity_gate_passed") is False
    )
    wz_mass_path_open = (
        "WZ correlator mass-fit path absent" in parent_statuses["wz_correlator_mass_fit_path_gate"]
        and parents["wz_correlator_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
    )
    gram_purity_open = (
        "source-Higgs Gram purity gate not passed" in parent_statuses["source_higgs_gram_purity_gate"]
        and parents["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed") is False
    )
    mass_source_bridge_loaded = (
        "Higgs mass-source action bridge"
        in parent_statuses["higgs_mass_source_action_bridge"]
        and parents["higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and parents["higgs_mass_source_action_bridge"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("higgs-mass-source-action-bridge-loaded", mass_source_bridge_loaded, parent_statuses["higgs_mass_source_action_bridge"])
    report("candidate-state-recorded", True, f"present={validation['present']}")
    if validation["present"]:
        report("candidate-schema-valid", validation["valid"] is True, f"reasons={validation['reasons']}")
    else:
        report("candidate-certificate-absent", True, display(args.input))
    report("canonical-higgs-certificate-still-open", canonical_higgs_open, parent_statuses["canonical_higgs_operator_certificate_gate"])
    report("sector-overlap-still-open", sector_overlap_open, parent_statuses["same_source_sector_overlap_identity"])
    report("wz-mass-fit-path-still-open", wz_mass_path_open, parent_statuses["wz_correlator_mass_fit_path_gate"])
    report("source-higgs-gram-purity-still-open", gram_purity_open, parent_statuses["source_higgs_gram_purity_gate"])
    report("static-ew-algebra-rejected", True, "static dM_W/dh is not dM_W/ds")
    report("same-source-ew-action-certificate-validity-recorded", True, f"valid={validation['valid']}")

    status_text = (
        "bounded-support / same-source EW action certificate candidate valid"
        if validation["valid"]
        else "open / same-source EW action certificate absent"
    )
    result = {
        "actual_current_surface_status": status_text,
        "verdict": (
            "A same-source EW action certificate candidate satisfies the schema. "
            "This remains support only until W/Z rows, sector-overlap, canonical-Higgs "
            "identity, source-Higgs/Gram or W/Z response gates, and retained-route "
            "certificates pass."
            if validation["valid"]
            else (
                "No same-source EW action certificate is present.  Current PR #230 "
                "still has static EW gauge-mass algebra and structural gauge support, "
                "but no dynamic SU(2)xU(1)/Higgs action block with the same scalar "
                "source coordinate used by the top FH/LSZ measurement and coupled "
                "to centered Phi^dagger Phi."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This builder validates an action-surface prerequisite only; it does not authorize retained/proposed-retained y_t wording.",
        "bare_retained_allowed": False,
        "input": display(args.input),
        "input_present": validation["present"],
        "same_source_ew_action_certificate_valid": validation["valid"],
        "candidate_validation": validation,
        "acceptance_schema": acceptance_schema(),
        "shortcut_rejections": shortcut_rejections(),
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not synthesize EW action data or W/Z rows",
            "does not treat static EW algebra as a same-source measurement",
            "does not define O_H by fiat",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Supply a real same-source EW action certificate satisfying this schema, "
            "with the scalar source coupled to centered Phi^dagger Phi and the "
            "Higgs mass-source action bridge attached, then implement W/Z "
            "correlator mass-fit rows or source-Higgs C_sH/C_HH rows with "
            "identity certificates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(args.output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
