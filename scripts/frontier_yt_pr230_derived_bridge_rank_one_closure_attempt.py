#!/usr/bin/env python3
"""
PR #230 derived-bridge rank-one closure attempt.

Target bridge:

    O_s / O_sp source pole  ->  canonical Higgs radial O_H

This runner attacks the derivation-preferred route: prove that the neutral
scalar response sector is rank one by a primitive-cone / positivity-improving
transfer theorem.  If that worked, source-only scalar-pole data could become
sufficient.  The runner asks whether current PR230 artifacts already satisfy
the exact contract, and records the remaining blockers without importing the
old Ward/H_unit route or observed values.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json"
)

PARENTS = {
    "missing_bridge_assumptions": (
        "outputs/yt_pr230_missing_bridge_literature_assumption_exercises_2026-05-05.json"
    ),
    "primitive_cone_gate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
    ),
    "primitive_cone_stretch_no_go": (
        "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json"
    ),
    "positivity_rank_one_support": (
        "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
    ),
    "positivity_direct_attempt": (
        "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"
    ),
    "irreducibility_authority_audit": (
        "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json"
    ),
    "burnside_attempt": (
        "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json"
    ),
    "offdiagonal_generator_attempt": (
        "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
    ),
    "canonical_higgs_operator_gate": (
        "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json"
    ),
    "source_functional_lsz_identifiability": (
        "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
    ),
    "source_higgs_gram_gate": (
        "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json"
    ),
    "full_positive_closure_assembly_gate": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_closure_route": (
        "outputs/yt_retained_closure_route_certificate_2026-05-01.json"
    ),
}

FUTURE_FILES = {
    "primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
    "neutral_irreducibility_certificate": (
        "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json"
    ),
    "neutral_offdiagonal_generator_certificate": (
        "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json"
    ),
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def positive_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_neutral_basis",
            "needed": "current PR230 Cl(3)/Z3 neutral scalar basis, including source and orthogonal sectors",
        },
        {
            "id": "nonnegative_neutral_transfer",
            "needed": "same-surface neutral transfer matrix with nonnegative entries on a certified cone",
        },
        {
            "id": "primitive_cone",
            "needed": "directed positive-entry graph strongly connected and some finite transfer power strictly positive",
        },
        {
            "id": "isolated_lowest_neutral_pole",
            "needed": "nondegenerate lowest isolated neutral scalar pole with FV/IR/threshold controls",
        },
        {
            "id": "positive_source_overlap",
            "needed": "O_sp/source pole overlaps the unique neutral pole with nonzero residue",
        },
        {
            "id": "canonical_higgs_authority",
            "needed": "canonical O_H exists on the same surface or is bypassed by a theorem that all neutral scalar probes couple to the unique pole",
        },
        {
            "id": "orthogonal_neutral_null",
            "needed": "no surviving orthogonal neutral top-coupled direction after rank-one theorem",
        },
        {
            "id": "forbidden_import_firewall",
            "needed": "reject H_unit/Ward, observed targets, alpha_LM/plaquette/u0, and unit-overlap shortcuts",
        },
    ]


def determinant_or_reflection_positivity_boundary() -> dict[str, Any]:
    return {
        "candidate": "measure/reflection/determinant positivity",
        "usable_support": [
            "positive Euclidean measure",
            "positive spectral representation",
            "fermion determinant positivity if the staggered+Wilson bridge is later accepted",
        ],
        "why_not_bridge": (
            "Positivity preservation is weaker than positivity improvement.  "
            "A block-diagonal positive neutral transfer keeps all source-only "
            "C_ss rows while preserving an orthogonal neutral scalar direction."
        ),
        "counterexample_shape": {
            "neutral_transfer_matrix": [[0.91, 0.0], [0.0, 0.88]],
            "nonnegative": True,
            "strongly_connected": False,
            "primitive_power_positive": False,
            "source_only_rows_can_match": True,
        },
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_alpha_lm_plaquette_u0_or_rconn": False,
        "set_kappa_s_equal_one": False,
        "treated_reflection_positivity_as_improvement": False,
        "treated_determinant_positivity_as_neutral_rank_one": False,
        "treated_synthetic_primitive_matrix_as_evidence": False,
    }


def main() -> int:
    print("PR #230 derived-bridge rank-one closure attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}
    firewall = forbidden_firewall()

    primitive_contract_present = (
        certs["primitive_cone_gate"].get("primitive_cone_certificate_gate_passed")
        is False
        and certs["primitive_cone_gate"].get("proposal_allowed") is False
    )
    primitive_certificate_absent = (
        future_presence["primitive_cone_certificate"] is False
        and certs["primitive_cone_gate"].get("future_certificate_checks", {}) == {}
    )
    primitive_stretch_blocks_source_only = (
        certs["primitive_cone_stretch_no_go"].get("primitive_cone_stretch_no_go_passed")
        is True
        and certs["primitive_cone_stretch_no_go"].get(
            "source_invisible_reducible_counterfamily", {}
        ).get("all_preserve_source_rows")
        is True
    )
    conditional_rank_one_theorem_available = (
        certs["positivity_rank_one_support"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and certs["positivity_rank_one_support"].get("proposal_allowed") is False
    )
    direct_positivity_not_derived = (
        certs["positivity_direct_attempt"].get("direct_positivity_improving_theorem_derived")
        is False
        and certs["positivity_direct_attempt"].get("exact_negative_boundary_passed")
        is True
    )
    irreducibility_absent = (
        certs["irreducibility_authority_audit"].get(
            "neutral_scalar_irreducibility_certificate_present"
        )
        is False
        and certs["irreducibility_authority_audit"].get(
            "neutral_scalar_irreducibility_theorem_passed"
        )
        is False
    )
    burnside_blocks = (
        certs["burnside_attempt"].get("burnside_irreducibility_certificate_passed")
        is False
        and certs["burnside_attempt"].get("exact_negative_boundary_passed") is True
    )
    offdiag_generator_absent = (
        certs["offdiagonal_generator_attempt"].get("offdiagonal_generator_derived")
        is not True
        and "neutral off-diagonal generator not derivable"
        in statuses["offdiagonal_generator_attempt"]
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and future_presence["canonical_oh_certificate"] is False
    )
    source_only_lsz_insufficient = (
        "source-functional LSZ identifiability" in statuses["source_functional_lsz_identifiability"]
        and certs["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    source_higgs_rows_absent = (
        future_presence["source_higgs_rows"] is False
        and certs["source_higgs_gram_gate"].get("current_data_has_required_residues")
        is False
    )
    retained_route_open = certs["retained_closure_route"].get("proposal_allowed") is False
    assembly_gate_open = (
        certs["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    # Strongest-current-surface derived-bridge closure condition.
    derived_bridge_closure_passed = (
        primitive_certificate_absent is False
        and direct_positivity_not_derived is False
        and irreducibility_absent is False
        and canonical_oh_absent is False
        and source_only_lsz_insufficient is False
        and source_higgs_rows_absent is False
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, str(proposal_allowed))
    report("primitive-contract-present", primitive_contract_present, statuses["primitive_cone_gate"])
    report("primitive-certificate-absent", primitive_certificate_absent, str(future_presence))
    report("primitive-stretch-blocks-source-only", primitive_stretch_blocks_source_only, statuses["primitive_cone_stretch_no_go"])
    report("conditional-rank-one-theorem-available", conditional_rank_one_theorem_available, statuses["positivity_rank_one_support"])
    report("direct-positivity-not-derived", direct_positivity_not_derived, statuses["positivity_direct_attempt"])
    report("irreducibility-authority-absent", irreducibility_absent, statuses["irreducibility_authority_audit"])
    report("burnside-route-blocked-currently", burnside_blocks, statuses["burnside_attempt"])
    report("offdiagonal-generator-absent", offdiag_generator_absent, statuses["offdiagonal_generator_attempt"])
    report("canonical-oh-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-only-lsz-insufficient", source_only_lsz_insufficient, statuses["source_functional_lsz_identifiability"])
    report("source-higgs-rows-absent", source_higgs_rows_absent, statuses["source_higgs_gram_gate"])
    report("derived-bridge-closure-not-passed", derived_bridge_closure_passed is False, "strict positive contract not satisfied")
    report("retained-route-still-open", retained_route_open, statuses["retained_closure_route"])
    report("assembly-gate-still-open", assembly_gate_open, statuses["full_positive_closure_assembly_gate"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    exact_negative_boundary_passed = (
        not missing_parents
        and not proposal_allowed
        and primitive_contract_present
        and primitive_certificate_absent
        and primitive_stretch_blocks_source_only
        and conditional_rank_one_theorem_available
        and direct_positivity_not_derived
        and irreducibility_absent
        and burnside_blocks
        and offdiag_generator_absent
        and canonical_oh_absent
        and source_only_lsz_insufficient
        and source_higgs_rows_absent
        and derived_bridge_closure_passed is False
        and retained_route_open
        and assembly_gate_open
        and no_forbidden_imports
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / derived rank-one bridge not closed on current PR230 surface"
        ),
        "conditional_surface_status": (
            "If a future current-surface certificate supplies a primitive "
            "positivity-improving neutral scalar transfer sector with an "
            "isolated lowest pole plus canonical-Higgs/source overlap authority, "
            "the existing Perron/rank-one support theorem could bridge O_sp to "
            "the physical Higgs readout."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface has conditional rank-one support and a clear "
            "primitive-cone contract, but no strict primitive-cone certificate, "
            "no neutral off-diagonal generator, no irreducibility theorem, no "
            "canonical O_H certificate, and no C_sH/C_HH rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "derived_bridge_closure_passed": derived_bridge_closure_passed,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "positive_contract": positive_contract(),
        "determinant_or_reflection_positivity_boundary": (
            determinant_or_reflection_positivity_boundary()
        ),
        "future_artifact_presence": future_presence,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define y_t_bare",
            "does not identify O_sp with O_H",
            "does not treat positivity preservation, reflection positivity, or determinant positivity as positivity improvement",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, R_conn, or unit-overlap shortcuts",
            "does not treat synthetic primitive matrices as PR230 evidence",
        ],
        "exact_next_action": (
            "Make the derived bridge positive by deriving one real current-surface "
            "neutral off-diagonal generator or primitive-cone certificate.  The "
            "certificate must define the neutral basis and transfer matrix, prove "
            "strong connectivity/positive primitive power, certify pole isolation, "
            "and supply source plus canonical-Higgs overlap authority.  Otherwise "
            "return to measured O_H/C_sH/C_HH or W/Z response rows."
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
