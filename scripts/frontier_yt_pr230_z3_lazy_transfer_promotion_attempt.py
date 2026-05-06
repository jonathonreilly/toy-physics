#!/usr/bin/env python3
"""
PR #230 Z3 lazy-transfer promotion attempt.

This runner asks whether the new same-surface Z3 taste-triplet artifact can be
promoted into the missing neutral primitive/lazy-transfer certificate.

Result:
    No, not on the current PR230 surface.  The exact cyclic action P is present
    and the lazy matrix L=(I+P)/2 is primitive as mathematics, but current
    artifacts encode only a symmetry automorphism.  They do not encode a
    physical same-surface transfer, action row, lazy self term, or off-diagonal
    neutral generator that instantiates L as dynamics.
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
    / "yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
)

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_triplet_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "z3_generation_action_lift": (
        "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json"
    ),
    "neutral_primitive_route_completion": (
        "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
    ),
    "neutral_offdiagonal_generator": (
        "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
    ),
    "neutral_primitive_cone_gate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_ARTIFACTS = {
    "same_surface_neutral_transfer": (
        "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json"
    ),
    "neutral_offdiagonal_generator_certificate": (
        "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json"
    ),
    "neutral_primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
    "same_source_ew_action_certificate": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[Fraction]]


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


def eye(n: int) -> Matrix:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def cyclic_z3() -> Matrix:
    return [
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def matadd(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matscale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * value for value in row] for row in a]


def matpow(a: Matrix, power: int) -> Matrix:
    result = eye(len(a))
    for _ in range(power):
        result = matmul(result, a)
    return result


def all_positive(a: Matrix) -> bool:
    return all(value > 0 for row in a for value in row)


def has_zero(a: Matrix) -> bool:
    return any(value == 0 for row in a for value in row)


def to_strings(a: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_mass_or_yukawa_as_selector": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "uses_reduced_pilots_as_production_evidence": False,
        "treats_symmetry_automorphism_as_physical_transfer": False,
        "imports_external_markov_lazy_averaging_as_dynamics": False,
        "sets_kappa_s_equal_one": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 lazy-transfer promotion attempt")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()

    ident = eye(3)
    p = cyclic_z3()
    p2 = matmul(p, p)
    p3 = matmul(p2, p)
    lazy = matscale(Fraction(1, 2), matadd(ident, p))
    lazy2 = matmul(lazy, lazy)
    pure_cycle_nonprimitive = all(has_zero(matpow(p, k)) for k in range(1, 7))
    lazy_primitive_as_math = all_positive(lazy2)
    lazy_differs_from_parent_symmetry = lazy != p

    same_surface_cycle_supplied = (
        "same-surface Z3 taste-triplet artifact" in statuses["same_surface_z3_taste_triplet"]
        and certs["same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certs["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
        and certs["same_surface_z3_taste_triplet"].get("pr230_closure_authorized")
        is False
    )
    conditional_lazy_theorem_loaded = (
        "Z3-triplet primitive-cone theorem"
        in statuses["z3_triplet_conditional_primitive"]
        and certs["z3_triplet_conditional_primitive"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and certs["z3_triplet_conditional_primitive"].get("proposal_allowed") is False
        and certs["z3_triplet_conditional_primitive"].get("pr230_closure_authorized")
        is False
        and "H3" in certs["z3_triplet_conditional_primitive"].get(
            "remaining_unsupplied_conditional_premises", []
        )
    )
    generation_action_not_derived = (
        "Z3 generation-action lift" in statuses["z3_generation_action_lift"]
        and certs["z3_generation_action_lift"].get("proposal_allowed") is False
        and certs["z3_generation_action_lift"].get("same_surface_h1_derived") is False
    )
    neutral_route_still_open = (
        "neutral primitive-rank-one route not complete"
        in statuses["neutral_primitive_route_completion"]
        and certs["neutral_primitive_route_completion"].get("proposal_allowed") is False
        and certs["neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
    )
    offdiagonal_absent = (
        certs["neutral_offdiagonal_generator"].get("offdiagonal_generator_written")
        is False
        and certs["neutral_offdiagonal_generator"].get("proposal_allowed") is False
    )
    primitive_gate_absent = (
        certs["neutral_primitive_cone_gate"].get(
            "strict_primitive_cone_certificate_present"
        )
        is not True
    )
    physical_lazy_transfer_present = (
        futures["same_surface_neutral_transfer"]
        or futures["neutral_offdiagonal_generator_certificate"]
        or futures["neutral_primitive_cone_certificate"]
        or certs["same_surface_z3_taste_triplet"].get(
            "treats_symmetry_automorphism_as_physical_transfer"
        )
        is True
    )
    parent_encodes_only_symmetry = (
        same_surface_cycle_supplied
        and certs["same_surface_z3_taste_triplet"].get("forbidden_firewall", {}).get(
            "treats_symmetry_automorphism_as_physical_transfer"
        )
        is False
        and not physical_lazy_transfer_present
    )
    countermodel_identifiability_gap = (
        parent_encodes_only_symmetry
        and pure_cycle_nonprimitive
        and lazy_primitive_as_math
        and lazy_differs_from_parent_symmetry
    )
    aggregate_gates_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    promotion_attempt_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and same_surface_cycle_supplied
        and conditional_lazy_theorem_loaded
        and generation_action_not_derived
        and neutral_route_still_open
        and offdiagonal_absent
        and primitive_gate_absent
        and parent_encodes_only_symmetry
        and countermodel_identifiability_gap
        and aggregate_gates_still_open
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("same-surface-cycle-supplied", same_surface_cycle_supplied, statuses["same_surface_z3_taste_triplet"])
    report("conditional-lazy-theorem-loaded", conditional_lazy_theorem_loaded, statuses["z3_triplet_conditional_primitive"])
    report("generation-action-still-not-derived", generation_action_not_derived, statuses["z3_generation_action_lift"])
    report("pure-cycle-not-primitive", pure_cycle_nonprimitive, "P powers keep zeros")
    report("lazy-matrix-primitive-as-math", lazy_primitive_as_math, "L^2 has strictly positive entries")
    report("lazy-differs-from-parent-symmetry", lazy_differs_from_parent_symmetry, "L introduces a self/identity edge not encoded by P")
    report("neutral-route-still-open", neutral_route_still_open, statuses["neutral_primitive_route_completion"])
    report("offdiagonal-generator-absent", offdiagonal_absent, statuses["neutral_offdiagonal_generator"])
    report("primitive-cone-certificate-absent", primitive_gate_absent, statuses["neutral_primitive_cone_gate"])
    report("physical-lazy-transfer-not-present", not physical_lazy_transfer_present, str(futures))
    report("parent-encodes-only-symmetry", parent_encodes_only_symmetry, "same-surface artifact says symmetry automorphism, not transfer")
    report("countermodel-identifiability-gap", countermodel_identifiability_gap, "same P is compatible with nonprimitive P dynamics or primitive L dynamics")
    report("aggregate-gates-still-open", aggregate_gates_still_open, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("lazy-transfer-promotion-attempt-passed", promotion_attempt_passed, "exact negative boundary if all checks pass")

    countermodels = {
        "encoded_parent_data_common_to_both": [
            "same-surface cyclic triplet action P",
            "P fixes the PR230 source identity I_8",
            "no same-surface neutral-transfer output file",
            "no off-diagonal neutral-generator certificate",
            "no strict primitive-cone certificate",
        ],
        "model_A_pure_cycle_dynamics": {
            "physical_transfer": "P",
            "primitive": False,
            "reason": "P^k has zeros for every tested k and P^3=I, so the chain is periodic.",
        },
        "model_B_lazy_cycle_dynamics": {
            "physical_transfer": "L=(I+P)/2",
            "primitive": True,
            "reason": "L^2=(I+2P+P^2)/4 is strictly positive.",
        },
        "identifiability_conclusion": (
            "The current parent artifacts specify the symmetry P but do not "
            "select model A versus model B as physical PR230 dynamics.  "
            "Promoting B would import an unproved lazy/self-transfer term."
        ),
    }

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Z3 lazy-transfer promotion not derivable "
            "from current same-surface cyclic action"
        ),
        "conditional_surface_status": (
            "If a future same-surface neutral transfer, action row, or "
            "off-diagonal generator instantiates L=(I+P)/2 or an equivalent "
            "aperiodic positive transfer, the conditional Z3 primitive theorem "
            "can become neutral primitive support.  That premise is absent now."
        ),
        "hypothetical_axiom_status": (
            "Under an accepted new same-surface lazy-transfer axiom this would "
            "supply the finite primitive-cone step; no closure is authorized "
            "on the actual current surface."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The proof would require importing the lazy self term or treating "
            "a symmetry automorphism as dynamics.  Current PR230 artifacts do "
            "neither."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_lazy_transfer_promotion_attempt_passed": promotion_attempt_passed,
        "exact_negative_boundary_passed": promotion_attempt_passed,
        "same_surface_cycle_supplied": same_surface_cycle_supplied,
        "conditional_lazy_theorem_loaded": conditional_lazy_theorem_loaded,
        "lazy_matrix_primitive_as_math": lazy_primitive_as_math,
        "physical_lazy_transfer_instantiated": physical_lazy_transfer_present,
        "parent_encodes_only_symmetry": parent_encodes_only_symmetry,
        "countermodel_identifiability_gap": countermodel_identifiability_gap,
        "pr230_closure_authorized": False,
        "writes_strict_future_certificate": False,
        "strict_future_artifact_presence": futures,
        "primitive_witness": {
            "cyclic_generator_P": to_strings(p),
            "P2": to_strings(p2),
            "P3_equals_identity": p3 == ident,
            "pure_cyclic_generator_is_not_primitive": pure_cycle_nonprimitive,
            "lazy_transfer_L": to_strings(lazy),
            "L2": to_strings(lazy2),
            "L2_is_strictly_positive": lazy_primitive_as_math,
            "L_differs_from_P": lazy_differs_from_parent_symmetry,
            "load_bearing_new_term": "the identity/self edge with coefficient 1/2 in L",
        },
        "countermodels": countermodels,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write a neutral primitive-cone certificate",
            "does not treat symmetry averaging as a physical same-surface transfer",
            "does not identify O_sp, O_s, or the taste triplet with canonical O_H",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, or a source-Higgs overlap to one",
        ],
        "exact_next_action": (
            "Supply outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json "
            "or an equivalent strict off-diagonal-generator / primitive-cone "
            "certificate, or bypass this route with O_H/C_sH/C_HH, same-source "
            "W/Z response, Schur A/B/C rows, or scalar-LSZ authority."
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
