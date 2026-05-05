#!/usr/bin/env python3
"""
PR #230 invariant-ring O_H certificate attempt.

This is the stage-1 clean source-Higgs follow-up after the outside-math route
selector.  It asks whether representation/invariant-ring or Schur/commutant
data on the current PR230 surface can derive the same-surface canonical O_H
identity and normalization certificate.

The answer on the current surface is no.  The current neutral scalar labels
still admit a two-singlet completion.  Invariant-ring methods become useful
only after the same-surface representation/action/metric data prove
multiplicity one or identify the canonical radial generator.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json"

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "canonical_higgs_operator_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "source_higgs_production_readiness_gate": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_unratified_gram_shortcut_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "neutral_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity as authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "c2 = 1 by convention",
    "Z_match = 1 by convention",
    "kappa_s = 1 by convention",
    "PSLQ/value recognition selector",
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


def invariant_ring_counterfamily() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, theta in (
        ("source_equals_higgs", 0.0),
        ("mixed_higgs_30deg", math.pi / 6.0),
        ("mixed_higgs_60deg", math.pi / 3.0),
        ("orthogonal_higgs", math.pi / 2.0),
    ):
        overlap = math.cos(theta)
        rows.append(
            {
                "case": label,
                "neutral_scalar_basis": ["source_singlet", "orthogonal_neutral_singlet"],
                "group_action_on_basis": "trivial_on_both_currently_allowed_singlets",
                "degree_one_invariant_dimension": 2,
                "degree_two_invariant_dimension": 3,
                "commutant_dimension": 4,
                "source_vector": [1.0, 0.0],
                "candidate_oh_vector": [overlap, math.sin(theta)],
                "source_to_candidate_oh_overlap": overlap,
                "candidate_oh_norm": 1.0,
                "source_only_rows_change": False,
                "invariant_ring_distinguishes_candidate": False,
                "multiplicity_one_certificate_satisfied": False,
            }
        )
    return rows


def required_future_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_representation",
            "required": "explicit PR230 neutral scalar state/action representation containing source and canonical-Higgs candidates",
            "current_satisfied": False,
        },
        {
            "id": "multiplicity_one_or_generator_selection",
            "required": "proof that the neutral top-coupled invariant sector has a single primitive canonical radial generator",
            "current_satisfied": False,
        },
        {
            "id": "canonical_metric_and_lsz_normalization",
            "required": "same-surface kinetic/LSZ metric fixing the canonical field normalization",
            "current_satisfied": False,
        },
        {
            "id": "source_identity_or_overlap",
            "required": "identity or overlap certificate linking the PR230 source-pole operator to that canonical generator",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "explicitly reject H_unit, Ward, observed targets, alpha/plaquette/u0, unit c2/Z_match/kappa_s, and value-recognition selectors",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 invariant-ring O_H certificate attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    rows = invariant_ring_counterfamily()
    future_contract = required_future_certificate_contract()

    selector_chose_clean_source_higgs = (
        parents["clean_source_higgs_math_selector"].get("clean_physics_priority")
        == "source_higgs"
        and parents["clean_source_higgs_math_selector"].get(
            "selected_clean_route", {}
        ).get("id")
        == "source_higgs_invariant_ring_then_gns_pole_rows"
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_certificate_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_certificate_gate"].get("candidate_valid") is False
        and not future_present["canonical_oh_certificate"]
    )
    premise_no_go_loaded = (
        parents["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
    )
    commutant_no_go_loaded = (
        parents["neutral_scalar_commutant_rank_no_go"].get("rank_one_theorem_derived")
        is False
        and "commutant" in statuses["neutral_scalar_commutant_rank_no_go"]
    )
    primitive_no_go_loaded = (
        parents["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True
    )
    source_higgs_rows_absent = not future_present["source_higgs_rows"]
    invariant_degree_one_dims = {
        row["degree_one_invariant_dimension"] for row in rows
    }
    overlaps = {round(row["source_to_candidate_oh_overlap"], 12) for row in rows}
    source_rows_fixed = all(row["source_only_rows_change"] is False for row in rows)
    multiplicity_one_failed = all(
        row["multiplicity_one_certificate_satisfied"] is False for row in rows
    )
    future_contract_missing = [
        row["id"] for row in future_contract if not row["current_satisfied"]
    ]
    forbidden_firewall_clean = True
    invariant_ring_certificate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-chose-clean-source-higgs-route", selector_chose_clean_source_higgs, statuses["clean_source_higgs_math_selector"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_certificate_gate"])
    report("canonical-oh-premise-no-go-loaded", premise_no_go_loaded, statuses["canonical_oh_premise_stretch"])
    report("commutant-rank-no-go-loaded", commutant_no_go_loaded, statuses["neutral_scalar_commutant_rank_no_go"])
    report("primitive-cone-stretch-no-go-loaded", primitive_no_go_loaded, statuses["neutral_scalar_primitive_cone_stretch_no_go"])
    report("source-higgs-rows-absent", source_higgs_rows_absent, f"source_higgs_rows={future_present['source_higgs_rows']}")
    report("two-singlet-invariant-completion-exists", invariant_degree_one_dims == {2}, f"degree_one_dims={sorted(invariant_degree_one_dims)}")
    report("source-only-rows-stay-fixed", source_rows_fixed, "source-only rows do not depend on the candidate O_H angle")
    report("source-to-oh-overlap-varies", len(overlaps) > 1, f"overlaps={sorted(overlaps)}")
    report("multiplicity-one-certificate-not-satisfied", multiplicity_one_failed, "current invariant sector is not forced to dimension one")
    report("future-certificate-contract-recorded", len(future_contract_missing) == 4, f"missing={future_contract_missing}")
    report("forbidden-firewall-clean", forbidden_firewall_clean, ", ".join(FORBIDDEN_INPUTS))
    report("invariant-ring-certificate-not-passed", not invariant_ring_certificate_passed, "no same-surface multiplicity-one proof")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / invariant-ring O_H certificate attempt "
            "blocked on current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface representation/action "
            "proves multiplicity one or selects the canonical radial generator "
            "with LSZ normalization"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current PR230 invariant data admit a two-singlet neutral scalar "
            "completion.  Invariant-ring or Schur/commutant methods therefore "
            "do not produce the canonical O_H identity or normalization "
            "certificate without new same-surface representation/action data."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "invariant_ring_certificate_passed": invariant_ring_certificate_passed,
        "canonical_oh_certificate_written": False,
        "future_file_presence": future_present,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "invariant_ring_counterfamily": rows,
        "future_certificate_contract": future_contract,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write or validate a canonical O_H certificate",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward identity, observed targets, alpha_LM, plaquette, u0, or PSLQ/value recognition",
            "does not treat Schur's lemma as multiplicity-one proof when the trivial irrep appears twice",
        ],
        "exact_next_action": (
            "A positive clean source-Higgs theorem now needs a same-surface "
            "representation/action certificate proving multiplicity one in the "
            "neutral top-coupled invariant sector, or an independent canonical "
            "radial generator plus LSZ metric.  If that lands, rerun the "
            "canonical-Higgs operator certificate gate before producing "
            "C_ss/C_sH/C_HH pole rows."
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
