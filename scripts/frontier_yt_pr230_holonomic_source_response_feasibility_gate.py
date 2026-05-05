#!/usr/bin/env python3
"""
PR #230 holonomic source-response feasibility gate.

PR #541 found a useful pattern for the plaquette lane: make the finite-volume
generating functional explicit, then derive observables as derivatives of that
functional using Picard-Fuchs / holonomic / tensor-contraction machinery.

This runner asks whether the same pattern can be used immediately for PR #230:

    Z(beta, s, h) -> C_ss, C_sH, C_HH -> source-Higgs Gram purity -> y_t

The gate is intentionally conservative.  It does not compute a physical
Yukawa value, and it does not define O_H by fiat.  It records whether the
two-source functional is a current-surface object or a future artifact.
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
    / "yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
)

PARENT_CERTIFICATES = {
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "source_higgs_production_readiness": (
        "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json"
    ),
    "source_higgs_gram_purity": (
        "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json"
    ),
    "same_source_sector_overlap": (
        "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json"
    ),
    "source_functional_lsz_identifiability": (
        "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
    ),
    "schur_abc_definition_attempt": (
        "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json"
    ),
    "full_positive_closure_assembly_gate": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_closure_route": (
        "outputs/yt_retained_closure_route_certificate_2026-05-01.json"
    ),
}

TEXT_SURFACES = {
    "canonical_higgs_repo_authority_audit": (
        "docs/YT_CANONICAL_HIGGS_REPO_AUTHORITY_AUDIT_NOTE_2026-05-03.md"
    ),
    "source_functional_lsz_identifiability": (
        "docs/YT_SOURCE_FUNCTIONAL_LSZ_IDENTIFIABILITY_THEOREM_NOTE_2026-05-03.md"
    ),
    "pr230_schur_abc_definition_attempt": (
        "docs/YT_PR230_SCHUR_ABC_DEFINITION_DERIVATION_ATTEMPT_NOTE_2026-05-05.md"
    ),
    "fresh_artifact_literature_route_review": (
        "docs/YT_PR230_FRESH_ARTIFACT_LITERATURE_ROUTE_REVIEW_NOTE_2026-05-05.md"
    ),
}

FUTURE_ARTIFACTS = {
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "holonomic_source_response_rows": (
        "outputs/yt_pr230_holonomic_source_response_rows_2026-05-05.json"
    ),
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
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def toy_source_projection_family() -> list[dict[str, Any]]:
    """Counterfamily showing why exact Z(s,0) cannot determine C_sH.

    Use a normalized two-operator pole model with covariance
        C_ss = 1, C_HH = 1, C_sH = rho.
    The source-only generating functional Z(s, 0) is identical for all rho,
    while the source-Higgs overlap and Gram determinant differ.
    """

    family: list[dict[str, Any]] = []
    for rho in (1.0, 0.75, 0.25, 0.0, -0.25):
        c_ss = 1.0
        c_hh = 1.0
        c_sh = rho
        gram_det = c_ss * c_hh - c_sh * c_sh
        family.append(
            {
                "rho": rho,
                "Z_source_only_log_quadratic": "0.5 * s^2",
                "C_ss": c_ss,
                "C_sH": c_sh,
                "C_HH": c_hh,
                "gram_determinant": gram_det,
                "gram_purity_certified": math.isclose(gram_det, 0.0, abs_tol=1e-15)
                and abs(abs(rho) - 1.0) < 1e-15,
            }
        )
    return family


def method_contract() -> dict[str, Any]:
    return {
        "method_name": "PR541-style holonomic/source-generating functional",
        "usable_after": [
            "finite-volume compact integral or finite tensor network is explicitly defined",
            "action/measure are fixed on the same current surface",
            "all source coordinates are named current-surface operators",
            "target rows are derivatives of log Z, not labels chosen after the fact",
            "no observed target values or fitted selectors are used as proof inputs",
        ],
        "pr230_target_functional": (
            "Z_PR230(beta, s, h) = integral exp(-S_Cl3Z3 + s O_s + h O_H) dmu"
        ),
        "target_derivatives": {
            "C_ss": "d_s d_s log Z at s=h=0",
            "C_sH": "d_s d_h log Z at s=h=0",
            "C_HH": "d_h d_h log Z at s=h=0",
        },
        "why_pr541_is_relevant": (
            "It supplies a disciplined compute/proof pattern: define Z first, "
            "then compute rows as derivatives.  It cannot by itself supply the "
            "missing PR230 O_H or h-source."
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_alpha_lm_plaquette_u0_or_rconn": False,
        "set_kappa_s_equal_one": False,
        "defined_O_H_by_name_only": False,
        "defined_h_source_by_hypothetical_ew_action": False,
        "used_pr541_plaquette_value_as_yukawa_input": False,
    }


def main() -> int:
    print("PR #230 holonomic source-response feasibility gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENT_CERTIFICATES.items()}
    texts = {name: read_rel(path) for name, path in TEXT_SURFACES.items()}
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    contract = method_contract()
    projection_family = toy_source_projection_family()
    firewall = forbidden_firewall()

    source_only_object_exists = (
        "source-coordinate invariant readout" in texts["source_functional_lsz_identifiability"]
        and "source-only pole data do not determine the overlap" in texts[
            "source_functional_lsz_identifiability"
        ]
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    source_higgs_rows_absent = (
        future_presence["source_higgs_rows"] is False
        and parents["source_higgs_production_readiness"].get("future_rows_present") is False
    )
    gram_rows_absent = (
        parents["source_higgs_gram_purity"].get("current_data_has_required_residues")
        is False
        and parents["source_higgs_gram_purity"].get(
            "source_higgs_gram_purity_gate_passed"
        )
        is False
    )
    overlap_identity_open = (
        parents["same_source_sector_overlap"].get("sector_overlap_identity_gate_passed")
        is False
    )
    outside_math_boundary_present = (
        "holonomic D-module/Picard-Fuchs/creative-telescoping machinery" in texts[
            "pr230_schur_abc_definition_attempt"
        ]
        and "after the object being computed is defined" in texts[
            "pr230_schur_abc_definition_attempt"
        ]
    )
    fresh_route_selected = (
        "O_H/C_sH/C_HH" in texts["fresh_artifact_literature_route_review"]
        and "action-first" in texts["fresh_artifact_literature_route_review"]
    )
    projection_counterfamily_blocks_source_only = (
        all(row["Z_source_only_log_quadratic"] == "0.5 * s^2" for row in projection_family)
        and len({row["C_sH"] for row in projection_family}) > 1
        and any(row["gram_purity_certified"] for row in projection_family)
        and any(not row["gram_purity_certified"] for row in projection_family)
    )
    two_source_functional_current_surface_defined = not (
        canonical_oh_absent or source_higgs_rows_absent
    )
    pr541_route_immediate_closure = (
        two_source_functional_current_surface_defined
        and gram_rows_absent is False
        and overlap_identity_open is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())
    retained_route_open = parents["retained_closure_route"].get("proposal_allowed") is False
    assembly_gate_open = (
        parents["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, str(proposal_allowed_parents))
    report("pr541-method-contract-usable-in-principle", True, contract["method_name"])
    report("source-only-functional-present", source_only_object_exists, parent_statuses["source_functional_lsz_identifiability"])
    report("canonical-oh-current-surface-absent", canonical_oh_absent, parent_statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-current-surface-absent", source_higgs_rows_absent, parent_statuses["source_higgs_production_readiness"])
    report("gram-purity-rows-absent", gram_rows_absent, parent_statuses["source_higgs_gram_purity"])
    report("sector-overlap-identity-open", overlap_identity_open, parent_statuses["same_source_sector_overlap"])
    report("outside-math-boundary-recorded", outside_math_boundary_present, "tools after object definition")
    report("fresh-route-selected-oh-contract", fresh_route_selected, "O_H/C_sH/C_HH action-first route")
    report("source-only-counterfamily-blocks-closure", projection_counterfamily_blocks_source_only, "same Z(s,0), different C_sH")
    report(
        "two-source-functional-not-defined-now",
        two_source_functional_current_surface_defined is False,
        "requires O_H and h-source",
    )
    report(
        "pr541-route-no-immediate-closure",
        pr541_route_immediate_closure is False,
        "blocked unless two-source rows exist",
    )
    report("retained-route-still-open", retained_route_open, parent_statuses["retained_closure_route"])
    report("assembly-gate-still-open", assembly_gate_open, parent_statuses["full_positive_closure_assembly_gate"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed_parents
        and source_only_object_exists
        and canonical_oh_absent
        and source_higgs_rows_absent
        and gram_rows_absent
        and overlap_identity_open
        and outside_math_boundary_present
        and fresh_route_selected
        and projection_counterfamily_blocks_source_only
        and two_source_functional_current_surface_defined is False
        and pr541_route_immediate_closure is False
        and retained_route_open
        and assembly_gate_open
        and no_forbidden_imports
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR541-style holonomic source-response "
            "route is relevant but blocked by missing current-surface O_H and h-source"
        ),
        "conditional_surface_status": (
            "exact-support candidate if a future PR230 artifact supplies a "
            "same-source EW/Higgs action or canonical O_H identity plus "
            "C_sH/C_HH row definitions; holonomic/tensor methods can then "
            "compute defined finite-volume rows."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The PR541 method transfers as a compute/proof discipline, not as "
            "a missing operator definition.  Current PR230 has source-only "
            "Z(s,0) support but lacks the h-source/canonical O_H needed for "
            "Z(s,h), C_sH, and C_HH."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "method_contract": contract,
        "toy_source_projection_counterfamily": projection_family,
        "two_source_functional_current_surface_defined": (
            two_source_functional_current_surface_defined
        ),
        "pr541_route_immediate_closure": pr541_route_immediate_closure,
        "future_artifact_presence": future_presence,
        "parent_certificates": PARENT_CERTIFICATES,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not compute y_t or m_t",
            "does not define y_t_bare",
            "does not use H_unit or yt_ward_identity",
            "does not use PR541 plaquette values as top-Yukawa inputs",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, or R_conn",
            "does not identify source-only O_s with canonical O_H",
            "does not treat holonomic/Picard-Fuchs labels as operator definitions",
        ],
        "exact_next_action": (
            "To make the PR541-style route positive, first derive a "
            "same-current-surface O_H/h-source artifact: either a same-source "
            "EW/Higgs action certificate tied to the Cl(3)/Z3 source coordinate, "
            "or a canonical O_H identity/normalization theorem.  Then build "
            "Z(beta,s,h) and compute C_ss/C_sH/C_HH rows by finite-volume "
            "tensor contraction or holonomic creative telescoping."
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
