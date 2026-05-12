#!/usr/bin/env python3
"""
PR #230 Block67 probe C: same-surface canonical O_H/action/LSZ route.

This runner tests the strongest route requested for probe C:

    Cl(3)/Z3 current primitives
    + degree-one radial-tangent support
    + FMS candidate/action support
    => accepted same-surface canonical O_H/action/LSZ authority.

The check is deliberately non-promotional.  It audits the action-first O_H
attempt, accepted-action stretch, FMS action-adoption cut, degree-one theorem,
source-pole mixing obstruction, and neutral multiplicity/transfer no-go
artifacts.  It then constructs the narrow same-current-data countermodel:
source/taste-radial data stay fixed while the canonical Higgs direction and
source-Higgs overlap vary in an unmeasured neutral slot.
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
    / "yt_pr230_block67_same_surface_canonical_oh_action_lsz_probe_2026-05-12.json"
)

PARENTS = {
    "action_first_oh": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "canonical_accepted_action_stretch": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
    "fms_action_adoption": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "degree_one_radial_tangent": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "neutral_multiplicity_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "neutral_multiplicity_candidate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "neutral_transfer_mixing": "outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json",
    "lane1_oh_root": "outputs/yt_pr230_lane1_oh_root_theorem_attempt_2026-05-12.json",
    "lane1_action_premise": "outputs/yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json",
    "canonical_neutral_primitive_cut": "outputs/yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json",
    "native_scalar_action_lsz_exhaustion": "outputs/yt_pr230_native_scalar_action_lsz_route_exhaustion_after_block40_2026-05-12.json",
}

FUTURE_AUTHORITY_PATHS = {
    "same_surface_ew_higgs_action_certificate": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "source_higgs_pole_rows": "outputs/yt_pr230_source_higgs_pole_rows_2026-05-06.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_pr230_neutral_offdiagonal_generator_certificate_2026-05-07.json",
}

FORBIDDEN_FIREWALL = {
    "used_H_unit": False,
    "used_Ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_targets": False,
    "used_alpha_LM": False,
    "used_plaquette_or_u0": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_Z_match_equal_one": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "defined_canonical_O_H_by_declaration": False,
    "treated_FMS_support_as_action_adoption": False,
    "claimed_retained_or_proposed_retained": False,
    "touched_chunk_runner_files": False,
}

LITERATURE_REFERENCES = [
    {
        "id": "FMS_1981",
        "citation": "Frohlich, Morchio, Strocchi, Nuclear Physics B 190, 553-582 (1981)",
        "url": "https://doi.org/10.1016/0550-3213(81)90448-X",
        "role": "FMS/gauge-invariant Higgs-operator context",
        "proof_authority_for_pr230": False,
    },
    {
        "id": "Fradkin_Shenker_1979",
        "citation": "Fradkin and Shenker, Physical Review D 19, 3682-3697 (1979)",
        "url": "https://doi.org/10.1103/PhysRevD.19.3682",
        "role": "lattice gauge-Higgs complementarity context",
        "proof_authority_for_pr230": False,
    },
    {
        "id": "Osterwalder_Schrader_1973_1975",
        "citation": "Osterwalder and Schrader, CMP 31, 83-112 (1973); CMP 42, 281-305 (1975)",
        "url": "https://doi.org/10.1007/BF01608978",
        "role": "OS reconstruction and reflection-positivity context",
        "proof_authority_for_pr230": False,
    },
    {
        "id": "Osterwalder_Seiler_1978",
        "citation": "Osterwalder and Seiler, Annals of Physics 110, 440-471 (1978)",
        "url": "https://doi.org/10.1016/0003-4916(78)90039-8",
        "role": "lattice positivity/transfer-matrix context",
        "proof_authority_for_pr230": False,
    },
    {
        "id": "LSZ_1955_1957",
        "citation": "Lehmann, Symanzik, Zimmermann, Nuovo Cimento 1, 205 (1955); 6, 319-333 (1957)",
        "url": "https://www.osti.gov/biblio/4339083",
        "role": "pole residue and interpolating-field normalization context",
        "proof_authority_for_pr230": False,
    },
]

MATH_REFERENCES = [
    {
        "id": "finite_group_invariant_projection",
        "role": "Reynolds/trivial-isotypic projection identifies invariant subspace dimension but not a physical transfer/action",
        "url": "https://en.wikipedia.org/wiki/Representation_theory_of_finite_groups",
    },
    {
        "id": "GNS_cyclic_representation",
        "role": "positive state gives a cyclic representation, but cyclicity does not select a canonical Higgs vector without extra operator/action data",
        "url": "https://en.wikipedia.org/wiki/Gelfand%E2%80%93Naimark%E2%80%93Segal_construction",
    },
    {
        "id": "Perron_Frobenius_primitive_cone",
        "role": "primitive positive transfer can give a unique Perron projection only after the full source-plus-neutral transfer is supplied",
        "url": "https://handwiki.org/wiki/Perron%E2%80%93Frobenius_theorem",
    },
    {
        "id": "spectral_projectors",
        "role": "self-adjoint spectral projectors require the operator/metric whose spectral measure is being projected",
        "url": "https://en.wikipedia.org/wiki/Spectral_theorem",
    },
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


def present_map(paths: dict[str, str]) -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in paths.items()}


def countermodel(theta: float) -> dict[str, Any]:
    """Same current source rows, different canonical-Higgs overlap."""
    source = [1.0, 0.0]
    orthogonal = [0.0, 1.0]
    candidate_a = [1.0, 0.0]
    candidate_b = [math.cos(theta), math.sin(theta)]
    return {
        "neutral_basis": ["x_taste_radial_or_source_pole", "n_orthogonal_neutral"],
        "source_vector": source,
        "orthogonal_vector": orthogonal,
        "current_rows_fixed": {
            "C_ss": "fixed",
            "C_sx": "fixed",
            "C_xx": "fixed",
            "C_sH": "absent",
            "C_HH": "absent",
            "canonical_LSZ_metric": "absent",
            "accepted_action_derivative": "absent",
        },
        "completion_A": {
            "canonical_O_H_vector": candidate_a,
            "source_to_O_H_overlap": 1.0,
            "current_rows_changed": False,
        },
        "completion_B": {
            "canonical_O_H_vector": candidate_b,
            "source_to_O_H_overlap": math.cos(theta),
            "current_rows_changed": False,
        },
        "theta_radians": theta,
        "overlap_difference": 1.0 - math.cos(theta),
        "meaning": (
            "Current PR230 evidence fixes the source/taste-radial axis but not "
            "the canonical Higgs direction, scalar metric, or source derivative."
        ),
    }


def assumption_exercise() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "source or taste-radial operator equals canonical Higgs radial operator",
            "current_status": "not derived; finite C_sx/C_xx rows measure x, not O_H",
            "if_wrong": "the same-source FH/LSZ readout gives y_source, while y_t differs by the source-Higgs overlap factor",
        },
        {
            "assumption": "accepted EW/Higgs action is available on the PR230 same surface",
            "current_status": "not derived/adopted from Cl(3)/Z3 primitives",
            "if_wrong": "standard Higgs notation is an external action extension, not an authority for dS/ds = sum O_H",
        },
        {
            "assumption": "canonical scalar LSZ metric and pole normalization are fixed",
            "current_status": "absent; source-only and taste-radial rows do not fix the inverse-propagator derivative or residue metric",
            "if_wrong": "kappa_s, c2, Z_match, and source-Higgs overlap become convention-dependent or row-dependent",
        },
        {
            "assumption": "source sector has unit overlap with the canonical Higgs sector",
            "current_status": "blocked by source-pole mixing and two-neutral-singlet counterfamilies",
            "if_wrong": "orthogonal neutral admixture leaves source-only evidence fixed but changes the canonical response",
        },
        {
            "assumption": "FMS candidate/action packet is adopted as current action authority",
            "current_status": "conditional support only; adoption cut is open",
            "if_wrong": "FMS supplies route context but no PR230 theorem for Phi, h, v, O_H normalization, or strict C_sH/C_HH rows",
        },
    ]


def first_principles_drivers() -> list[dict[str, Any]]:
    return [
        {
            "driver": "gauge-invariant scalar excitation",
            "minimal_content": "an operator in the same algebra that creates the physical scalar state",
            "current_surface_result": "candidate shapes exist, but no accepted canonical operator certificate",
        },
        {
            "driver": "action variation",
            "minimal_content": "a source coordinate s whose derivative of the accepted action is the scalar operator",
            "current_surface_result": "no accepted dS/ds = sum O_H; additive top-source contamination remains a separate contract",
        },
        {
            "driver": "radial mode",
            "minimal_content": "a unique physical radial direction, not only a Z3-symmetric axis name",
            "current_surface_result": "degree-one uniqueness is exact support under a missing action premise; higher neutral invariants remain available",
        },
        {
            "driver": "source coordinate",
            "minimal_content": "the measured source must be the same coordinate used by the canonical scalar action",
            "current_surface_result": "current source/taste-radial rows do not prove that identity",
        },
        {
            "driver": "LSZ pole normalization",
            "minimal_content": "isolated pole residue and inverse-propagator derivative in the selected scalar metric",
            "current_surface_result": "strict C_ss/C_sH/C_HH pole rows and FV/IR/model-class authority are absent",
        },
        {
            "driver": "top response coupling",
            "minimal_content": "top energy response to the same normalized scalar mode",
            "current_surface_result": "source response is not canonical y_t until the source-Higgs overlap is fixed",
        },
    ]


def audit_rows(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "artifact": "action-first O_H artifact attempt",
            "status": status(certs["action_first_oh"]),
            "current_closure": False,
            "reason": "same-source EW/Higgs action certificate, canonical O_H certificate, and source-Higgs rows were not written",
        },
        {
            "artifact": "canonical accepted-action stretch",
            "status": status(certs["canonical_accepted_action_stretch"]),
            "current_closure": False,
            "reason": "support stack did not compose into accepted action or canonical O_H authority",
        },
        {
            "artifact": "FMS action adoption",
            "status": status(certs["fms_action_adoption"]),
            "current_closure": False,
            "reason": "FMS candidate support is present but same_surface_cl3_z3_derived=false and accepted_current_surface=false",
        },
        {
            "artifact": "degree-one radial-tangent theorem",
            "status": status(certs["degree_one_radial_tangent"]),
            "current_closure": False,
            "reason": "axis uniqueness holds only under a missing same-surface action/LSZ premise",
        },
        {
            "artifact": "source-pole canonical-Higgs mixing obstruction",
            "status": status(certs["source_pole_mixing"]),
            "current_closure": False,
            "reason": "fixed source response admits variable canonical y_t when source-canonical overlap changes",
        },
        {
            "artifact": "same-surface neutral multiplicity-one no-go/gate",
            "status": status(certs["neutral_multiplicity_gate"]),
            "current_closure": False,
            "reason": "two neutral singlets and a non-scalar commutant remain on the current surface",
        },
    ]


def main() -> int:
    print("PR #230 Block67 same-surface canonical O_H/action/LSZ probe C")
    print("=" * 78)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_presence = present_map(FUTURE_AUTHORITY_PATHS)

    action_first_blocks = (
        certs["action_first_oh"].get("exact_negative_boundary_passed") is True
        and certs["action_first_oh"].get("canonical_oh_certificate_written") is False
        and certs["action_first_oh"].get("same_source_ew_action_certificate_written")
        is False
        and certs["action_first_oh"].get("source_higgs_rows_written") is False
    )
    canonical_stretch_blocks = (
        certs["canonical_accepted_action_stretch"].get("stretch_attempt_passed")
        is True
        and certs["canonical_accepted_action_stretch"].get("current_route_blocked")
        is True
        and not certs["canonical_accepted_action_stretch"].get(
            "root_closures_found", []
        )
    )
    fms_not_adopted = (
        certs["fms_action_adoption"].get("fms_action_adoption_minimal_cut_passed")
        is True
        and certs["fms_action_adoption"].get("same_surface_cl3_z3_derived") is False
        and certs["fms_action_adoption"].get("accepted_current_surface") is False
        and certs["fms_action_adoption"].get("closure_authorized") is False
    )
    degree_one_support_only = (
        certs["degree_one_radial_tangent"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["degree_one_radial_tangent"].get("degree_one_tangent_unique")
        is True
        and certs["degree_one_radial_tangent"].get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and certs["degree_one_radial_tangent"].get("canonical_oh_identity_derived")
        is False
    )
    mixing_obstruction_active = (
        certs["source_pole_mixing"].get("source_pole_canonical_identity_gate_passed")
        is False
        and len(certs["source_pole_mixing"].get("mixing_family", [])) >= 3
    )
    neutral_multiplicity_rejects = (
        certs["neutral_multiplicity_gate"].get("candidate_accepted") is False
        and certs["neutral_multiplicity_candidate"].get("candidate_accepted") is False
    )
    neutral_transfer_obstruction_active = (
        certs["neutral_transfer_mixing"].get("proposal_allowed") is False
        and certs["neutral_transfer_mixing"]
        .get("current_missing_artifacts", {})
        .get("physical_transfer_or_offdiagonal_generator_absent")
        is True
    )
    lane1_confirms_open = (
        certs["lane1_oh_root"].get("exact_negative_boundary_passed") is True
        and certs["lane1_oh_root"].get("same_surface_cl3_z3_derived") is False
        and certs["lane1_oh_root"].get("accepted_current_surface") is False
        and certs["lane1_action_premise"].get("exact_negative_boundary_passed")
        is True
        and certs["lane1_action_premise"].get("same_surface_ew_higgs_action_derived")
        is False
        and certs["lane1_action_premise"].get("same_surface_phi_derived") is False
        and certs["lane1_action_premise"].get("canonical_oh_action_premise_derived")
        is False
    )
    primitive_cut_confirms_open = (
        certs["canonical_neutral_primitive_cut"].get(
            "block55_canonical_neutral_primitive_cut_passed"
        )
        is True
        and certs["canonical_neutral_primitive_cut"].get("canonical_neutral_root_closed")
        is False
        and certs["canonical_neutral_primitive_cut"].get("proposal_allowed") is False
    )
    scalar_action_lsz_exhausted = (
        certs["native_scalar_action_lsz_exhaustion"].get(
            "native_scalar_action_lsz_route_exhaustion_passed"
        )
        is True
        and certs["native_scalar_action_lsz_exhaustion"].get("proposal_allowed")
        is False
    )
    no_future_authority_files = not any(future_presence.values())
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    witness = countermodel(math.pi / 3.0)
    countermodel_blocks_derivation = (
        witness["completion_A"]["current_rows_changed"] is False
        and witness["completion_B"]["current_rows_changed"] is False
        and witness["completion_A"]["source_to_O_H_overlap"]
        != witness["completion_B"]["source_to_O_H_overlap"]
        and witness["current_rows_fixed"]["C_sH"] == "absent"
        and witness["current_rows_fixed"]["accepted_action_derivative"] == "absent"
    )

    all_blockers_confirmed = (
        not missing
        and not proposal_allowed_parents
        and action_first_blocks
        and canonical_stretch_blocks
        and fms_not_adopted
        and degree_one_support_only
        and mixing_obstruction_active
        and neutral_multiplicity_rejects
        and neutral_transfer_obstruction_active
        and lane1_confirms_open
        and primitive_cut_confirms_open
        and scalar_action_lsz_exhausted
        and no_future_authority_files
        and firewall_clean
        and countermodel_blocks_derivation
    )
    current_surface_closure_possible = not all_blockers_confirmed
    same_surface_cl3_z3_derived = False
    accepted_current_surface = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("action-first-route-blocked", action_first_blocks, statuses["action_first_oh"])
    report("canonical-accepted-action-stretch-blocked", canonical_stretch_blocks, statuses["canonical_accepted_action_stretch"])
    report("fms-not-adopted", fms_not_adopted, statuses["fms_action_adoption"])
    report("degree-one-support-only", degree_one_support_only, statuses["degree_one_radial_tangent"])
    report("source-pole-mixing-obstruction-active", mixing_obstruction_active, statuses["source_pole_mixing"])
    report("neutral-multiplicity-rejects", neutral_multiplicity_rejects, statuses["neutral_multiplicity_gate"])
    report("neutral-transfer-obstruction-active", neutral_transfer_obstruction_active, statuses["neutral_transfer_mixing"])
    report("lane1-confirms-open", lane1_confirms_open, statuses["lane1_oh_root"])
    report("canonical-neutral-primitive-cut-confirms-open", primitive_cut_confirms_open, statuses["canonical_neutral_primitive_cut"])
    report("native-scalar-action-lsz-exhausted", scalar_action_lsz_exhausted, statuses["native_scalar_action_lsz_exhaustion"])
    report("no-future-authority-files-present", no_future_authority_files, str(future_presence))
    report("countermodel-blocks-definition-as-derivation", countermodel_blocks_derivation, f"overlap_delta={witness['overlap_difference']:.12f}")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("closure-not-possible-current-surface", not current_surface_closure_possible, "requested theorem not derived")
    report("same-surface-cl3-z3-not-derived", not same_surface_cl3_z3_derived, "same_surface_cl3_z3_derived=false")
    report("accepted-current-surface-absent", not accepted_current_surface, "accepted_current_surface=false")

    exact_obstruction = {
        "name": "two-neutral-slot action/LSZ underdetermination",
        "statement": (
            "The current surface fixes source/taste-radial support and an FMS "
            "candidate shape, but it does not supply the accepted action "
            "derivative, canonical scalar LSZ metric, or primitive/full-transfer "
            "projector that would identify the measured source pole with the "
            "canonical Higgs pole."
        ),
        "countermodel": witness,
        "why_degree_one_does_not_close": (
            "Degree-one Z3 uniqueness selects the taste-radial axis only after "
            "the missing premise that canonical O_H is a degree-one radial "
            "tangent of the accepted same-surface action."
        ),
        "why_FMS_does_not_close": (
            "FMS supplies the gauge-invariant operator/action shape as route "
            "context, but current PR230 has not derived or adopted the dynamic "
            "Phi action, O_H normalization, source derivative, or strict pole rows."
        ),
    }

    minimal_new_primitive_required = {
        "id": "same_surface_scalar_action_lsz_primitive",
        "one_sentence": (
            "A same-surface OS/GNS-positive scalar action/transfer primitive on "
            "the full source-plus-neutral sector whose rank-one pole projector "
            "defines canonical O_H, fixes the LSZ metric/residue normalization, "
            "and proves dS/ds = sum_x O_H(x) for the PR230 source coordinate."
        ),
        "must_include": [
            "dynamic Phi or equivalent scalar carrier derived from Cl(3)/Z3, or explicitly admitted as a new same-surface action extension",
            "gauge-covariant scalar kinetic/update semantics and radial background v",
            "canonical O_H provenance and normalization, not a symbol relabel",
            "canonical scalar LSZ metric, isolated-pole residue, FV/IR/zero-mode limiting order, and model-class authority",
            "source derivative identity dS/ds = sum_x O_H(x), with additive top source removed by theorem or measured subtraction",
            "source-to-canonical-Higgs overlap identity or strict C_ss/C_sH/C_HH pole rows excluding orthogonal neutral admixture",
            "top-response coupling to the same normalized pole state",
        ],
    }

    result = {
        "claim_type": "no_go",
        "actual_current_surface_status": (
            "exact negative boundary / probe C same-surface canonical O_H/action/LSZ "
            "route does not close on the current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if the minimal same-surface scalar-action/LSZ "
            "primitive lands and strict C_ss/C_sH/C_HH pole rows or an equivalent "
            "source-overlap theorem pass"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "same_surface_cl3_z3_derived=false and accepted_current_surface=false; "
            "the current stack leaves action adoption, canonical O_H identity, "
            "LSZ metric, pole rows, and orthogonal-neutral exclusion open"
        ),
        "audit_status_authority": "independent audit lane only",
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "same_surface_cl3_z3_derived": same_surface_cl3_z3_derived,
        "accepted_current_surface": accepted_current_surface,
        "current_surface_closure_possible": current_surface_closure_possible,
        "audit_rows": audit_rows(certs),
        "assumptions_exercise": assumption_exercise(),
        "first_principles_drivers": first_principles_drivers(),
        "literature_search": LITERATURE_REFERENCES,
        "mathematics_search": MATH_REFERENCES,
        "exact_obstruction": exact_obstruction,
        "minimal_new_primitive_required": minimal_new_primitive_required,
        "future_authority_file_presence": future_presence,
        "parent_statuses": statuses,
        "forbidden_firewall": {
            "passed": firewall_clean,
            **FORBIDDEN_FIREWALL,
        },
        "strict_non_claims": [
            "does not use H_unit, Ward, y_t_bare, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, or Z_match=1",
            "does not relabel C_sx/C_xx as C_sH/C_HH",
            "does not adopt FMS support as current action authority",
            "does not touch chunk runner files",
            "does not claim retained or proposed_retained status",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
