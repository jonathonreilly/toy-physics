#!/usr/bin/env python3
"""
PR #230 Z3 lazy-selector no-go.

The same-surface Z3 taste artifact supplies a cyclic action P.  The previous
promotion attempt shows that the lazy matrix L=(I+P)/2 is not instantiated as
PR230 dynamics.  This runner checks the adjacent shortcut: can common
"natural" criteria such as stochasticity, aperiodicity, entropy maximization,
spectral-gap maximization, or reversibility select the missing lazy transfer?

Verdict:
    No, not as retained-grade PR230 authority.  Some external optimization
    criteria choose eps=1/2 inside the compatible family
    T_eps = eps I + (1-eps) P, but importing those criteria is itself the
    load-bearing physical-selection step.  Other natural criteria either leave
    a continuum of choices or select a different reversible transfer.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_z3_lazy_selector_no_go_2026-05-06.json"

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_lazy_transfer_promotion_attempt": (
        "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
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
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
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


def transpose(a: Matrix) -> Matrix:
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def all_positive(a: Matrix) -> bool:
    return all(value > 0 for row in a for value in row)


def row_sums(a: Matrix) -> list[Fraction]:
    return [sum(row) for row in a]


def col_sums(a: Matrix) -> list[Fraction]:
    return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]


def is_stochastic(a: Matrix) -> bool:
    return row_sums(a) == [Fraction(1)] * len(a)


def is_doubly_stochastic(a: Matrix) -> bool:
    return is_stochastic(a) and col_sums(a) == [Fraction(1)] * len(a)


def to_strings(a: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def entropy(probs: list[Fraction]) -> float:
    result = 0.0
    for p in probs:
        if p > 0:
            value = float(p)
            result -= value * math.log(value)
    return result


def transfer_eps(eps: Fraction) -> Matrix:
    p = cyclic_z3()
    return matadd(matscale(eps, eye(3)), matscale(Fraction(1) - eps, p))


def reversible_transfer(bidirectional: Fraction) -> Matrix:
    # R_b=(1-2b)I+bP+bP^2, valid for 0 <= b <= 1/2.
    p = cyclic_z3()
    p2 = matmul(p, p)
    return matadd(
        matscale(Fraction(1) - 2 * bidirectional, eye(3)),
        matadd(matscale(bidirectional, p), matscale(bidirectional, p2)),
    )


def primitive_power(a: Matrix, max_power: int = 12) -> int | None:
    for power in range(1, max_power + 1):
        if all_positive(matpow(a, power)):
            return power
    return None


def directed_family_rows() -> list[dict[str, Any]]:
    p = cyclic_z3()
    rows: list[dict[str, Any]] = []
    for eps in [
        Fraction(0),
        Fraction(1, 8),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
        Fraction(2, 3),
        Fraction(3, 4),
        Fraction(7, 8),
        Fraction(1),
    ]:
        t = transfer_eps(eps)
        primitive_at = primitive_power(t)
        second_eigen_modulus_squared = Fraction(1) - 3 * eps * (Fraction(1) - eps)
        rows.append(
            {
                "eps": str(eps),
                "matrix": to_strings(t),
                "row_entropy": entropy([eps, Fraction(0), Fraction(1) - eps]),
                "second_eigen_modulus_squared": str(second_eigen_modulus_squared),
                "row_stochastic": is_stochastic(t),
                "column_stochastic": col_sums(t) == [Fraction(1)] * 3,
                "doubly_stochastic": is_doubly_stochastic(t),
                "commutes_with_z3_cycle": matmul(t, p) == matmul(p, t),
                "primitive": primitive_at is not None,
                "primitive_power": primitive_at,
                "reversible_with_uniform_measure": t == transpose(t),
            }
        )
    return rows


def reversible_family_rows() -> list[dict[str, Any]]:
    p = cyclic_z3()
    rows: list[dict[str, Any]] = []
    for b in [
        Fraction(0),
        Fraction(1, 8),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
    ]:
        r = reversible_transfer(b)
        primitive_at = primitive_power(r)
        diag = Fraction(1) - 2 * b
        rows.append(
            {
                "b": str(b),
                "matrix": to_strings(r),
                "row_distribution": [str(diag), str(b), str(b)],
                "row_entropy": entropy([diag, b, b]),
                "second_eigenvalue": str(Fraction(1) - 3 * b),
                "row_stochastic": is_stochastic(r),
                "doubly_stochastic": is_doubly_stochastic(r),
                "commutes_with_z3_cycle": matmul(r, p) == matmul(p, r),
                "reversible_with_uniform_measure": r == transpose(r),
                "primitive": primitive_at is not None,
                "primitive_power": primitive_at,
            }
        )
    return rows


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
        "imports_entropy_or_spectral_gap_objective_as_pr230_dynamics": False,
        "imports_markov_lazy_averaging_convention_as_pr230_dynamics": False,
        "sets_lazy_coefficient_by_definition": False,
        "sets_kappa_s_equal_one": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 lazy-selector no-go")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()

    p = cyclic_z3()
    lazy = transfer_eps(Fraction(1, 2))
    directed_rows = directed_family_rows()
    reversible_rows = reversible_family_rows()

    parent_cycle_valid = (
        "same-surface Z3 taste-triplet artifact" in statuses["same_surface_z3_taste_triplet"]
        and certs["same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certs["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
        and certs["same_surface_z3_taste_triplet"].get("pr230_closure_authorized")
        is False
    )
    promotion_boundary_valid = (
        "Z3 lazy-transfer promotion not derivable"
        in statuses["z3_lazy_transfer_promotion_attempt"]
        and certs["z3_lazy_transfer_promotion_attempt"].get(
            "z3_lazy_transfer_promotion_attempt_passed"
        )
        is True
        and certs["z3_lazy_transfer_promotion_attempt"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and certs["z3_lazy_transfer_promotion_attempt"].get("proposal_allowed")
        is False
    )
    conditional_theorem_only = (
        "Z3-triplet primitive-cone theorem"
        in statuses["z3_triplet_conditional_primitive"]
        and certs["z3_triplet_conditional_primitive"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and certs["z3_triplet_conditional_primitive"].get("proposal_allowed") is False
        and "H3" in certs["z3_triplet_conditional_primitive"].get(
            "remaining_unsupplied_conditional_premises", []
        )
    )
    generation_action_still_absent = (
        "Z3 generation-action lift" in statuses["z3_generation_action_lift"]
        and certs["z3_generation_action_lift"].get("same_surface_h1_derived") is False
        and certs["z3_generation_action_lift"].get("proposal_allowed") is False
    )
    neutral_route_still_open = (
        "neutral primitive-rank-one route not complete"
        in statuses["neutral_primitive_route_completion"]
        and certs["neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
        and certs["neutral_primitive_route_completion"].get("proposal_allowed")
        is False
    )
    offdiagonal_absent = (
        certs["neutral_offdiagonal_generator"].get("offdiagonal_generator_written")
        is False
        and certs["neutral_offdiagonal_generator"].get("proposal_allowed") is False
    )
    aggregate_gates_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_future_transfer_artifact = not any(futures.values())

    all_directed_preserve_parent_constraints = all(
        row["row_stochastic"]
        and row["doubly_stochastic"]
        and row["commutes_with_z3_cycle"]
        for row in directed_rows
    )
    directed_primitive_continuum = (
        all(row["primitive"] for row in directed_rows if row["eps"] not in {"0", "1"})
        and not next(row for row in directed_rows if row["eps"] == "0")["primitive"]
        and not next(row for row in directed_rows if row["eps"] == "1")["primitive"]
    )
    aperiodicity_does_not_select_eps = directed_primitive_continuum
    stochasticity_does_not_select_eps = (
        len({row["eps"] for row in directed_rows if row["doubly_stochastic"]}) > 2
    )

    max_entropy_directed_eps = max(
        directed_rows, key=lambda row: row["row_entropy"]
    )["eps"]
    max_gap_directed_eps = min(
        directed_rows, key=lambda row: Fraction(row["second_eigen_modulus_squared"])
    )["eps"]
    external_directed_selectors_pick_lazy = (
        max_entropy_directed_eps == "1/2" and max_gap_directed_eps == "1/2"
    )
    external_selector_not_parent_authority = (
        external_directed_selectors_pick_lazy
        and not certs["same_surface_z3_taste_triplet"].get(
            "entropy_maximization_action_principle_present", False
        )
        and not certs["same_surface_z3_taste_triplet"].get(
            "spectral_gap_optimization_action_principle_present", False
        )
    )

    directed_reversibility_selects_identity_not_lazy = (
        next(row for row in directed_rows if row["eps"] == "1")[
            "reversible_with_uniform_measure"
        ]
        is True
        and all(
            row["reversible_with_uniform_measure"] is False
            for row in directed_rows
            if row["eps"] != "1"
        )
        and lazy != eye(3)
    )

    reversible_family_preserves_parent_constraints = all(
        row["row_stochastic"]
        and row["doubly_stochastic"]
        and row["commutes_with_z3_cycle"]
        and row["reversible_with_uniform_measure"]
        for row in reversible_rows
    )
    reversible_family_not_directed_lazy = all(
        reversible_transfer(Fraction(row["b"])) != lazy for row in reversible_rows
    )
    max_entropy_reversible_b = max(
        reversible_rows, key=lambda row: row["row_entropy"]
    )["b"]
    max_gap_reversible_b = min(
        reversible_rows, key=lambda row: abs(float(Fraction(row["second_eigenvalue"])))
    )["b"]
    reversible_selectors_pick_uniform_not_lazy = (
        max_entropy_reversible_b == "1/3" and max_gap_reversible_b == "1/3"
    )

    markov_lazy_convention_is_definition = (
        lazy == transfer_eps(Fraction(1, 2))
        and external_selector_not_parent_authority
        and promotion_boundary_valid
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    selectors = {
        "z3_commuting_doubly_stochastic": {
            "status": "insufficient",
            "reason": "the whole directed T_eps family satisfies it",
            "selected_eps": None,
        },
        "aperiodicity_or_primitivity": {
            "status": "insufficient",
            "reason": "every 0 < eps < 1 in the directed family is primitive",
            "selected_eps": None,
        },
        "max_row_entropy_on_directed_family": {
            "status": "external_selector",
            "reason": "selects eps=1/2 only after importing entropy maximization",
            "selected_eps": max_entropy_directed_eps,
        },
        "max_spectral_gap_on_directed_family": {
            "status": "external_selector",
            "reason": "selects eps=1/2 only after importing gap optimization",
            "selected_eps": max_gap_directed_eps,
        },
        "uniform_detailed_balance_on_directed_family": {
            "status": "wrong_target",
            "reason": "selects reversible identity at eps=1, not primitive lazy transfer",
            "selected_eps": "1",
        },
        "reversible_z3_family": {
            "status": "different_continuum",
            "reason": "R_b gives symmetric transfers; entropy/gap pick uniform b=1/3, not L",
            "selected_b": max_entropy_reversible_b,
        },
        "markov_lazy_average_convention": {
            "status": "definition_not_derivation",
            "reason": "L=(I+P)/2 is a chosen convention unless a same-surface action supplies it",
            "selected_eps": "1/2",
        },
    }

    selector_no_go_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and parent_cycle_valid
        and promotion_boundary_valid
        and conditional_theorem_only
        and generation_action_still_absent
        and neutral_route_still_open
        and offdiagonal_absent
        and aggregate_gates_still_open
        and no_future_transfer_artifact
        and all_directed_preserve_parent_constraints
        and stochasticity_does_not_select_eps
        and aperiodicity_does_not_select_eps
        and external_directed_selectors_pick_lazy
        and external_selector_not_parent_authority
        and directed_reversibility_selects_identity_not_lazy
        and reversible_family_preserves_parent_constraints
        and reversible_family_not_directed_lazy
        and reversible_selectors_pick_uniform_not_lazy
        and markov_lazy_convention_is_definition
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("parent-cycle-valid", parent_cycle_valid, statuses["same_surface_z3_taste_triplet"])
    report("promotion-boundary-valid", promotion_boundary_valid, statuses["z3_lazy_transfer_promotion_attempt"])
    report("conditional-theorem-only", conditional_theorem_only, statuses["z3_triplet_conditional_primitive"])
    report("generation-action-still-absent", generation_action_still_absent, statuses["z3_generation_action_lift"])
    report("neutral-route-still-open", neutral_route_still_open, statuses["neutral_primitive_route_completion"])
    report("offdiagonal-generator-absent", offdiagonal_absent, statuses["neutral_offdiagonal_generator"])
    report("aggregate-gates-still-open", aggregate_gates_still_open, "assembly/retained/campaign proposal_allowed=false")
    report("no-future-transfer-artifact", no_future_transfer_artifact, str(futures))
    report("directed-family-preserves-parent-constraints", all_directed_preserve_parent_constraints, "T_eps commutes with P and is doubly stochastic")
    report("stochasticity-does-not-select-eps", stochasticity_does_not_select_eps, "many eps values satisfy stochastic constraints")
    report("aperiodicity-does-not-select-eps", aperiodicity_does_not_select_eps, "all sampled 0<eps<1 are primitive")
    report("external-directed-selectors-pick-lazy", external_directed_selectors_pick_lazy, f"entropy={max_entropy_directed_eps}, gap={max_gap_directed_eps}")
    report("external-selector-not-parent-authority", external_selector_not_parent_authority, "no same-surface entropy/gap action principle")
    report("directed-reversibility-selects-identity-not-lazy", directed_reversibility_selects_identity_not_lazy, "uniform detailed balance rejects directed lazy L")
    report("reversible-family-preserves-parent-constraints", reversible_family_preserves_parent_constraints, "R_b symmetric Z3 family")
    report("reversible-family-not-directed-lazy", reversible_family_not_directed_lazy, "R_b never equals L on sampled family")
    report("reversible-selectors-pick-uniform-not-lazy", reversible_selectors_pick_uniform_not_lazy, f"entropy={max_entropy_reversible_b}, gap={max_gap_reversible_b}")
    report("markov-lazy-convention-is-definition", markov_lazy_convention_is_definition, "L=(I+P)/2 still needs a physical same-surface row")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("z3-lazy-selector-no-go-passed", selector_no_go_passed, "exact negative boundary if all checks pass")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Z3 lazy selector shortcuts do not derive "
            "the PR230 physical neutral transfer"
        ),
        "conditional_surface_status": (
            "If a future same-surface action principle or transfer row supplies "
            "the lazy coefficient, the conditional primitive theorem can use it. "
            "The selector criteria tested here do not supply that action."
        ),
        "hypothetical_axiom_status": (
            "Adding entropy maximization, spectral-gap maximization, or Markov "
            "lazy averaging as a new axiom can select a transfer, but that is "
            "not retained-grade closure on the current PR230 surface."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Every successful selection of eps=1/2 imports an external "
            "optimization or convention; current same-surface artifacts provide "
            "only the Z3 symmetry action, not the physical transfer row."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_lazy_selector_no_go_passed": selector_no_go_passed,
        "exact_negative_boundary_passed": selector_no_go_passed,
        "parent_cycle_valid": parent_cycle_valid,
        "promotion_boundary_valid": promotion_boundary_valid,
        "conditional_theorem_only": conditional_theorem_only,
        "generation_action_still_absent": generation_action_still_absent,
        "neutral_route_still_open": neutral_route_still_open,
        "offdiagonal_generator_absent": offdiagonal_absent,
        "aggregate_gates_still_open": aggregate_gates_still_open,
        "physical_lazy_transfer_instantiated": False,
        "no_future_transfer_artifact": no_future_transfer_artifact,
        "directed_transfer_family": directed_rows,
        "reversible_transfer_family": reversible_rows,
        "selectors": selectors,
        "external_directed_selectors_pick_lazy": external_directed_selectors_pick_lazy,
        "external_selector_not_parent_authority": external_selector_not_parent_authority,
        "directed_reversibility_selects_identity_not_lazy": directed_reversibility_selects_identity_not_lazy,
        "reversible_selectors_pick_uniform_not_lazy": reversible_selectors_pick_uniform_not_lazy,
        "markov_lazy_convention_is_definition": markov_lazy_convention_is_definition,
        "pr230_closure_authorized": False,
        "writes_strict_future_certificate": False,
        "strict_future_artifact_presence": futures,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not define y_t through a matrix element or bare coupling",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat entropy or spectral-gap optimization as PR230 dynamics",
            "does not treat Markov lazy averaging as a same-surface action row",
            "does not set kappa_s, c2, Z_match, or a source-Higgs overlap to one",
        ],
        "exact_next_action": (
            "Supply a same-surface neutral transfer/action row or an equivalent "
            "off-diagonal-generator / primitive-cone certificate, or bypass "
            "this Z3 route through canonical O_H/C_sH/C_HH, same-source W/Z "
            "response, Schur A/B/C rows, or scalar-LSZ authority."
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
