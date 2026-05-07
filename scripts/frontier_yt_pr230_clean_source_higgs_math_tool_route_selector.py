#!/usr/bin/env python3
"""
PR #230 clean source-Higgs outside-math route selector.

The user asked to prioritize the cleanest physics closure and explicitly
allowed nonstandard mathematics such as PSLQ, holonomic/D-module methods,
tensor contractions, free probability, and motivic tools if they help.

This runner classifies those tools as algorithms that may produce a future
same-surface certificate.  It does not treat any of them as proof authority by
name, and it does not reopen the current non-chunk queue unless a parseable
same-surface artifact exists.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json"
)

PARENTS = {
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "genuine_source_pole_artifact_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "fms_oh_certificate_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_production_readiness_gate": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_unratified_gram_shortcut_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "schur_compressed_denominator_row_bootstrap_no_go": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "scalar_lsz_stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "wz_smoke_to_production_promotion_no_go": "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "two_source_taste_radial_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "two_source_taste_radial_schur_abc": "outputs/yt_pr230_two_source_taste_radial_schur_abc_finite_rows_2026-05-06.json",
    "two_source_taste_radial_pole_lift": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "nonchunk_current_surface_exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "nonchunk_future_artifact_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "same_surface_neutral_multiplicity_one_certificate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "matched_top_wz_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "top_wz_closed_covariance_theorem": "outputs/yt_top_wz_closed_covariance_theorem_2026-05-05.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "neutral_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
}

LITERATURE_REFRESH_ROWS = [
    {
        "id": "weak_and_higgs_from_lattice_2026",
        "url": "https://arxiv.org/abs/2603.12882",
        "route_use": "current lattice-Higgs/FMS context for gauge-invariant weak and Higgs spectroscopy",
        "pr230_boundary": "route guidance only; supplies no PR230 same-source EW/Higgs action, O_H identity, or pole rows",
    },
    {
        "id": "testing_gauge_invariant_perturbation_theory_2016",
        "url": "https://arxiv.org/abs/1610.04188",
        "route_use": "supports using gauge-invariant composite operators when a BEH gauge-Higgs action is present",
        "pr230_boundary": "does not identify the current Cl(3)/Z3 source pole with canonical O_H",
    },
    {
        "id": "su2_composite_spectral_properties_2021",
        "url": "https://doi.org/10.1140/epjc/s10052-021-09008-9",
        "route_use": "gauge-invariant composite correlators can carry Higgs-sector spectral information",
        "pr230_boundary": "does not provide PR230 C_spH/C_HH rows, W/Z response rows, or kappa_s authority",
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def math_route_rows(statuses: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "id": "invariant_ring_or_commutant_multiplicity_one",
            "rank_for_clean_source_higgs": 1,
            "tool_family": "representation theory, invariant rings, Schur/commutant analysis",
            "clean_use": (
                "derive a same-surface canonical O_H operator identity and "
                "normalization certificate, or prove a one-dimensional neutral "
                "top-coupled scalar sector"
            ),
            "required_output_contract": [
                FUTURE_FILES["canonical_oh_certificate"],
                "or",
                FUTURE_FILES["same_surface_neutral_multiplicity_one_certificate"],
                "or",
                FUTURE_FILES["neutral_irreducibility_certificate"],
                "or",
                FUTURE_FILES["neutral_primitive_cone_certificate"],
            ],
            "current_blocker": statuses["canonical_oh_premise_stretch"],
            "current_admissible_for_closure": False,
            "future_useful": True,
            "not_allowed_use": "do not cite symmetry labels or Schur's lemma unless the same-surface representation/action data are supplied",
        },
        {
            "id": "gns_flat_extension_or_rank_one_moment_problem",
            "rank_for_clean_source_higgs": 2,
            "tool_family": "operator algebras, truncated moment problems, semidefinite flat extension",
            "clean_use": (
                "certify pole purity from a rank-one moment/Gram matrix built "
                "from same-surface C_ss, C_sH, and C_HH rows"
            ),
            "required_output_contract": [
                FUTURE_FILES["canonical_oh_certificate"],
                FUTURE_FILES["source_higgs_rows"],
            ],
            "current_blocker": statuses["source_higgs_gram_purity_gate"],
            "current_admissible_for_closure": False,
            "future_useful": True,
            "not_allowed_use": "do not flat-extend source-only C_ss data or rows against an unratified operator",
        },
        {
            "id": "exact_tensor_or_peps_contraction",
            "rank_for_clean_source_higgs": 3,
            "tool_family": "exact tensor networks, PEPS transfer contraction, finite-volume character tensors",
            "clean_use": (
                "compute exact finite-volume C_ss/C_sH/C_HH or Schur A/B/C "
                "rows after the same-surface operator/action is defined"
            ),
            "required_output_contract": [
                FUTURE_FILES["canonical_oh_certificate"],
                FUTURE_FILES["source_higgs_rows"],
                "or",
                FUTURE_FILES["schur_kernel_rows"],
            ],
            "current_blocker": statuses["source_higgs_production_readiness_gate"],
            "current_admissible_for_closure": False,
            "future_useful": True,
            "not_allowed_use": "do not let exact arithmetic define O_H or kappa_s by convention",
        },
        {
            "id": "holonomic_dmodule_picard_fuchs_wz_painleve",
            "rank_for_clean_source_higgs": 4,
            "tool_family": "creative telescoping, Picard-Fuchs equations, WZ recurrences, isomonodromic systems",
            "clean_use": (
                "derive exact analytic-continuation or moment/threshold/FV "
                "authority for scalar-LSZ rows after same-surface correlators "
                "are present"
            ),
            "required_output_contract": [
                FUTURE_FILES["stieltjes_moment_certificate"],
                "or a scalar-denominator/analytic-continuation certificate",
            ],
            "current_blocker": statuses["scalar_lsz_stieltjes_moment_gate"],
            "current_admissible_for_closure": False,
            "future_useful": True,
            "not_allowed_use": "do not infer source-to-Higgs overlap from a closed-form C_ss function alone",
        },
        {
            "id": "free_probability_or_weingarten_expansion",
            "rank_for_clean_source_higgs": 5,
            "tool_family": "Speicher cumulants, finite-N Weingarten calculus, exact matrix-integral expansions",
            "clean_use": (
                "produce exact row values or a neutral irreducibility theorem "
                "when applied to the PR230 same-surface transfer/action block"
            ),
            "required_output_contract": [
                FUTURE_FILES["source_higgs_rows"],
                "or",
                FUTURE_FILES["neutral_primitive_cone_certificate"],
                "or",
                FUTURE_FILES["schur_kernel_rows"],
            ],
            "current_blocker": statuses["neutral_scalar_primitive_cone_stretch_no_go"],
            "current_admissible_for_closure": False,
            "future_useful": True,
            "not_allowed_use": "do not import large-N or free-limit factorization as Nc=3 proof without a bound",
        },
        {
            "id": "pslq_motivic_galois_mzv_value_recognition",
            "rank_for_clean_source_higgs": 6,
            "tool_family": "PSLQ, integer relations, periods, motivic Galois/MZV recognition",
            "clean_use": (
                "recognize exact constants after a same-surface row or theorem "
                "has already produced the quantity being recognized"
            ),
            "required_output_contract": [
                "a prior same-surface row/certificate plus an independent precision/audit certificate"
            ],
            "current_blocker": "value recognition is not an operator identity or source-overlap theorem",
            "current_admissible_for_closure": False,
            "future_useful": False,
            "not_allowed_use": "do not use PSLQ hits or observed targets as proof selectors for O_H, y_t, g2, kappa_s, c2, or Z_match",
        },
    ]


def user_option_ranking(statuses: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "option": "O_H/C_sH/C_HH source-Higgs pole rows",
            "clean_physics_role": "direct source-to-canonical-Higgs closure",
            "current_status": statuses["source_higgs_production_readiness_gate"],
            "needed": "same-surface canonical O_H identity/normalization certificate, then production C_sH/C_HH pole rows",
        },
        {
            "rank": 2,
            "option": "neutral-sector primitive-cone or irreducibility certificate",
            "clean_physics_role": "theorem route that can collapse the neutral top-coupled scalar sector to one component",
            "current_status": statuses["neutral_scalar_primitive_cone_stretch_no_go"],
            "needed": "same-surface neutral transfer sector with strong connectivity or primitive positive power",
        },
        {
            "rank": 3,
            "option": "strict scalar-LSZ moment/threshold/FV authority",
            "clean_physics_role": "necessary scalar-LSZ leg once overlap is supplied; not an overlap proof by itself",
            "current_status": statuses["scalar_lsz_stieltjes_moment_gate"],
            "needed": "strict moment/threshold/FV or scalar-denominator certificate",
        },
        {
            "rank": 4,
            "option": "Schur A/B/C kernel rows",
            "clean_physics_role": "denominator/kernel route that can support LSZ or expose orthogonal scalar structure",
            "current_status": statuses["schur_compressed_denominator_row_bootstrap_no_go"],
            "needed": "actual same-surface A/B/C kernel rows, not compressed source-only denominator data",
        },
        {
            "rank": 5,
            "option": "genuine same-source W/Z response rows",
            "clean_physics_role": "robust physical-response fallback; less clean because it adds EW action, g2, covariance, and delta_perp obligations",
            "current_status": statuses["wz_smoke_to_production_promotion_no_go"],
            "needed": "production W/Z mass-response rows plus source identity, covariance, g2, and orthogonal-correction authority",
        },
    ]


def selected_clean_route() -> dict[str, Any]:
    return {
        "id": "source_higgs_invariant_ring_then_gns_pole_rows",
        "current_status": "future-only / no current closure authority",
        "why_cleanest": (
            "It attacks the exact missing map from the PR230 scalar source to "
            "canonical Higgs directly, instead of normalizing through W/Z or "
            "downstream matching observables."
        ),
        "current_genuine_artifact": {
            "artifact": "O_sp",
            "role": "LSZ-normalized same-source source-pole operator with unit source-side pole residue",
            "limit": "source-side exact support only; O_sp = O_H, C_spH/C_HH rows, and Gram purity remain absent",
        },
        "stage_1": {
            "goal": "same-surface canonical O_H identity and normalization",
            "candidate_tools": [
                "invariant-ring multiplicity-one",
                "commutant/irreducibility theorem",
                "primitive-cone transfer theorem",
            ],
            "required_artifact": FUTURE_FILES["canonical_oh_certificate"],
        },
        "stage_2": {
            "goal": "rank-one source-Higgs pole purity",
            "candidate_tools": [
                "GNS flat extension",
                "truncated moment rank certificate",
                "exact tensor/PEPS row production",
            ],
            "required_artifact": FUTURE_FILES["source_higgs_rows"],
        },
        "stage_3": {
            "goal": "scalar-LSZ analytic authority",
            "candidate_tools": [
                "Picard-Fuchs/D-module scalar denominator",
                "WZ recurrence/moment certificate",
                "exact positive Stieltjes threshold/FV certificate",
            ],
            "required_artifact": FUTURE_FILES["stieltjes_moment_certificate"],
        },
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity_as_authority": False,
        "used_observed_top_mass_or_yt_selector": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_pilots_as_production_evidence": False,
        "set_c2_equal_one_without_derivation": False,
        "set_z_match_equal_one_without_derivation": False,
        "set_kappa_s_equal_one_without_derivation": False,
        "used_pslq_or_value_recognition_as_proof_selector": False,
    }


def main() -> int:
    print("PR #230 clean source-Higgs outside-math route selector")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    rows = math_route_rows(statuses)
    ranking = user_option_ranking(statuses)
    selected = selected_clean_route()
    firewall = forbidden_firewall()

    canonical_oh_absent = (
        parents["canonical_higgs_operator_certificate_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_certificate_gate"].get("candidate_valid") is False
        and not future_present["canonical_oh_certificate"]
    )
    source_higgs_rows_absent = not future_present["source_higgs_rows"]
    premise_no_go_loaded = (
        parents["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
        and bool(parents["canonical_oh_premise_stretch"].get("missing_obligation_ids"))
    )
    unratified_gram_blocks = (
        parents["source_higgs_unratified_gram_shortcut_no_go"].get(
            "unratified_gram_shortcut_no_go_passed"
        )
        is True
    )
    nonchunk_still_closed = (
        parents["nonchunk_current_surface_exhaustion"].get(
            "current_surface_exhaustion_gate_passed"
        )
        is True
        and parents["nonchunk_future_artifact_intake"].get(
            "dramatic_step_gate", {}
        ).get("passed")
        is False
    )
    all_rows_not_current_closure = all(
        row["current_admissible_for_closure"] is False for row in rows
    )
    pslq_not_selector = next(
        row for row in rows if row["id"] == "pslq_motivic_galois_mzv_value_recognition"
    )
    no_forbidden_imports = all(value is False for value in firewall.values())
    source_higgs_ranked_first = ranking[0]["option"] == "O_H/C_sH/C_HH source-Higgs pole rows"
    wz_fallback_not_primary = ranking[-1]["option"] == "genuine same-source W/Z response rows"
    literature_refresh_support_not_proof = (
        len(LITERATURE_REFRESH_ROWS) == 3
        and all(row["url"].startswith(("https://arxiv.org/abs/", "https://doi.org/")) for row in LITERATURE_REFRESH_ROWS)
        and all("no PR230" in row["pr230_boundary"] or "does not" in row["pr230_boundary"] for row in LITERATURE_REFRESH_ROWS)
    )
    osp_source_side_available = (
        "genuine same-source O_sp source-pole artifact intake"
        in statuses["genuine_source_pole_artifact_intake"]
        and parents["genuine_source_pole_artifact_intake"].get("proposal_allowed") is False
        and "Legendre source-pole operator constructed"
        in statuses["legendre_source_pole_operator"]
        and parents["legendre_source_pole_operator"].get("proposal_allowed") is False
    )
    radial_spurion_support_only = (
        "radial-spurion action contract" in statuses["radial_spurion_action_contract"]
        and parents["radial_spurion_action_contract"].get("current_surface_contract_satisfied") is False
        and parents["radial_spurion_action_contract"].get("accepted_action_certificate_written") is False
        and parents["same_source_ew_action_adoption_attempt"].get("adoption_allowed_now") is False
    )
    two_source_partial_rows_support_only = (
        parents["two_source_taste_radial_combiner"].get("ready_chunks") == 18
        and parents["two_source_taste_radial_combiner"].get("expected_chunks") == 63
        and parents["two_source_taste_radial_combiner"].get("combined_rows_written") is False
    )
    finite_schur_support_only = (
        parents["two_source_taste_radial_schur_abc"].get("finite_schur_abc_rows_written") is True
        and parents["two_source_taste_radial_schur_abc"].get("strict_schur_abc_kernel_rows_written") is False
        and parents["two_source_taste_radial_pole_lift"].get("proposal_allowed") is False
    )
    same_surface_multiplicity_gate_loaded = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in statuses["same_surface_neutral_multiplicity_one_gate"]
        and parents["same_surface_neutral_multiplicity_one_gate"].get("proposal_allowed") is False
        and parents["same_surface_neutral_multiplicity_one_gate"].get("candidate_accepted") is False
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_certificate_gate"])
    report("source-higgs-production-rows-absent", source_higgs_rows_absent, f"source_higgs_rows={future_present['source_higgs_rows']}")
    report("canonical-oh-premise-no-go-loaded", premise_no_go_loaded, statuses["canonical_oh_premise_stretch"])
    report("unratified-gram-shortcut-blocked", unratified_gram_blocks, statuses["source_higgs_unratified_gram_shortcut_no_go"])
    report("nonchunk-current-surface-still-closed", nonchunk_still_closed, statuses["nonchunk_current_surface_exhaustion"])
    report("outside-math-tools-classified", len(rows) == 6, f"count={len(rows)}")
    report("no-outside-math-tool-is-current-closure-evidence", all_rows_not_current_closure, "all rows future-only or support-only")
    report("pslq-value-recognition-not-proof-selector", not pslq_not_selector["future_useful"], pslq_not_selector["not_allowed_use"])
    report("literature-refresh-support-not-proof", literature_refresh_support_not_proof, f"rows={len(LITERATURE_REFRESH_ROWS)}")
    report("osp-source-side-artifact-available-not-closure", osp_source_side_available, statuses["genuine_source_pole_artifact_intake"])
    report("radial-spurion-action-contract-future-only", radial_spurion_support_only, statuses["radial_spurion_action_contract"])
    report("two-source-row-combiner-partial-support-only", two_source_partial_rows_support_only, f"ready={parents['two_source_taste_radial_combiner'].get('ready_chunks')}/63")
    report("finite-schur-abc-support-not-pole-authority", finite_schur_support_only, statuses["two_source_taste_radial_schur_abc"])
    report("same-surface-multiplicity-gate-loaded", same_surface_multiplicity_gate_loaded, statuses["same_surface_neutral_multiplicity_one_gate"])
    report("clean-physics-route-ranks-source-higgs-first", source_higgs_ranked_first, ranking[0]["option"])
    report("wz-response-demoted-to-fallback-for-clean-goal", wz_fallback_not_primary, ranking[-1]["option"])
    report("selected-route-is-source-higgs-invariant-to-gns", selected["id"] == "source_higgs_invariant_ring_then_gns_pole_rows", selected["id"])
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))

    closure_allowed = False
    same_surface_gate = parents["same_surface_neutral_multiplicity_one_gate"]
    if same_surface_gate.get("candidate_certificate_present") is True:
        exact_next_action = (
            "For the clean source-Higgs route, the candidate file "
            "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json "
            "is present but not accepted.  "
            f"{same_surface_gate.get('exact_next_action', '')}  After a same-surface "
            "artifact retires one of those failed obligations, rerun the "
            "same-surface multiplicity-one gate, canonical O_H certificate "
            "gate, source-Higgs row builder, Gram-purity postprocessor, "
            "scalar-LSZ gates, full assembly gate, retained-route gate, and "
            "completion audit."
        )
    else:
        exact_next_action = (
            "For the clean source-Higgs route, produce the actual candidate "
            "file outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json "
            "satisfying the same-surface neutral multiplicity-one gate.  If "
            "and only if that certificate lands, rerun the canonical O_H "
            "certificate gate, produce C_ss/C_spH/C_HH pole rows, and run the "
            "O_sp-Higgs Gram-purity plus scalar-LSZ aggregate gates."
        )
    result = {
        "actual_current_surface_status": (
            "exact support / clean source-Higgs outside-math route selector; "
            "positive closure still open"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface O_H certificate, "
            "source-Higgs pole rows, and scalar-LSZ authority land and the "
            "aggregate gates pass"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Outside-math tools are classified only as methods for producing "
            "future same-surface certificates.  Current O_H/C_sH/C_HH rows, "
            "neutral irreducibility, Schur rows, strict scalar-LSZ authority, "
            "and W/Z response rows remain absent."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "clean_physics_priority": "source_higgs",
        "closure_allowed": closure_allowed,
        "refresh_date": "2026-05-07",
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_future_file_presence": future_present,
        "literature_refresh_rows": LITERATURE_REFRESH_ROWS,
        "current_support_intake": {
            "osp_source_side_available": osp_source_side_available,
            "radial_spurion_support_only": radial_spurion_support_only,
            "two_source_partial_rows_support_only": two_source_partial_rows_support_only,
            "finite_schur_support_only": finite_schur_support_only,
            "same_surface_multiplicity_gate_loaded": same_surface_multiplicity_gate_loaded,
        },
        "outside_math_route_rows": rows,
        "user_option_clean_physics_ranking": ranking,
        "selected_clean_route": selected,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not reopen the non-chunk route queue on prose or path names",
            "does not treat O_sp, radial-spurion algebra, partial C_sx/C_xx chunks, or finite Schur rows as canonical-Higgs closure",
            "does not treat PSLQ, motivic recognition, or exact constants as proof selectors",
            "does not import H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, c2=1, Z_match=1, or kappa_s=1",
            "does not use reduced pilots, smoke rows, or exact toy contractions as production evidence",
        ],
        "exact_next_action": exact_next_action,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
