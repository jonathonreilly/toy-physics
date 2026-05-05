#!/usr/bin/env python3
"""
PR #230 neutral-scalar Burnside irreducibility attempt.

This is the outside-math version of the neutral-sector primitive-cone route.
It asks whether the current same-surface neutral scalar generator data are
already sufficient for a Burnside/double-commutant certificate: the generated
operator algebra must be the full matrix algebra on the neutral scalar sector,
or an equivalent primitive positive transfer power must be certified.

The current surface does not close.  The certified source-only generator set is
block diagonal in a source/orthogonal neutral completion, so its algebra is not
full and its commutant is not scalar-only.  Burnside becomes useful only after a
same-surface off-diagonal neutral generator, primitive transfer matrix, or
equivalent source-orthogonal row is supplied.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "invariant_ring_oh_attempt": "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json",
    "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_irreducibility_authority_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "neutral_scalar_primitive_cone_certificate_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_scalar_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "neutral_scalar_positivity_improving_direct_closure": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
    "positivity_improving_neutral_scalar_rank_one": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "burnside_irreducibility_certificate": "outputs/yt_neutral_scalar_burnside_irreducibility_certificate_2026-05-05.json",
    "neutral_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "matched_top_wz_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
}

FORBIDDEN_INPUTS = [
    "H_unit matrix-element readout",
    "yt_ward_identity authority",
    "observed top mass or observed y_t selector",
    "alpha_LM / plaquette / u0 proof input",
    "reduced pilots as production evidence",
    "c2 = 1, Z_match = 1, or kappa_s = 1 by convention",
    "PSLQ/value recognition as generator selector",
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


def matrix_rank(mats: list[np.ndarray], tol: float = 1.0e-10) -> int:
    if not mats:
        return 0
    flattened = np.stack([mat.reshape(-1) for mat in mats], axis=1)
    return int(np.linalg.matrix_rank(flattened, tol=tol))


def independent_append(basis: list[np.ndarray], candidate: np.ndarray) -> bool:
    old_rank = matrix_rank(basis)
    new_rank = matrix_rank([*basis, candidate])
    if new_rank > old_rank:
        basis.append(candidate)
        return True
    return False


def generated_algebra(generators: list[np.ndarray]) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for generator in generators:
        independent_append(basis, np.asarray(generator, dtype=float))

    changed = True
    while changed:
        changed = False
        current = list(basis)
        for left in current:
            for right in current:
                if independent_append(basis, left @ right):
                    changed = True
    return basis


def commutant_dimension(generators: list[np.ndarray], tol: float = 1.0e-10) -> int:
    n = generators[0].shape[0]
    variables = []
    for row in range(n):
        for col in range(n):
            unit = np.zeros((n, n), dtype=float)
            unit[row, col] = 1.0
            variables.append(unit)

    columns = []
    for variable in variables:
        column_blocks = []
        for generator in generators:
            column_blocks.append((variable @ generator - generator @ variable).reshape(-1))
        columns.append(np.concatenate(column_blocks))
    equation_matrix = np.stack(columns, axis=1)
    rank = int(np.linalg.matrix_rank(equation_matrix, tol=tol))
    return n * n - rank


def strongly_connected(matrix: np.ndarray, tolerance: float = 1.0e-12) -> bool:
    n = matrix.shape[0]
    graph = [[j for j in range(n) if matrix[i, j] > tolerance] for i in range(n)]
    reverse = [[i for i in range(n) if matrix[i, j] > tolerance] for j in range(n)]

    def reachable(adjacency: list[list[int]]) -> set[int]:
        seen = {0}
        queue: deque[int] = deque([0])
        while queue:
            node = queue.popleft()
            for child in adjacency[node]:
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen

    return len(reachable(graph)) == n and len(reachable(reverse)) == n


def primitive_power_positive(matrix: np.ndarray, tolerance: float = 1.0e-12) -> dict[str, Any]:
    n = matrix.shape[0]
    power = np.array(matrix, dtype=float)
    max_power = max(1, n * n - 2 * n + 2)
    for exponent in range(1, max_power + 1):
        if bool(np.all(power > tolerance)):
            return {"positive": True, "first_positive_power": exponent}
        power = power @ matrix
    return {"positive": False, "first_positive_power": None}


def burnside_witnesses() -> dict[str, Any]:
    identity = np.eye(2)
    source_projector = np.asarray([[1.0, 0.0], [0.0, 0.0]])
    current_transfer = np.asarray([[0.82, 0.0], [0.0, 0.61]])
    future_mixing_transfer = np.asarray([[0.62, 0.18], [0.11, 0.71]])

    current_generators = [identity, source_projector, current_transfer]
    future_generators = [identity, source_projector, future_mixing_transfer]

    current_algebra = generated_algebra(current_generators)
    future_algebra = generated_algebra(future_generators)
    current_primitive = primitive_power_positive(current_transfer)
    future_primitive = primitive_power_positive(future_mixing_transfer)

    shells = [0.0, 0.2679491924311227, 0.5358983848622454, 1.0]
    source_rows = [
        {"p_hat_sq": shell, "C_ss": 1.0 / (shell + 0.25)}
        for shell in shells
    ]

    return {
        "basis": ["source_created_neutral", "orthogonal_neutral"],
        "current_source_only_generators": {
            "names": ["I", "P_source", "T_source_only_block_diagonal"],
            "algebra_dimension": matrix_rank(current_algebra),
            "full_matrix_algebra_dimension": 4,
            "commutant_dimension": commutant_dimension(current_generators),
            "scalar_commutant_dimension": 1,
            "burnside_irreducible": matrix_rank(current_algebra) == 4
            and commutant_dimension(current_generators) == 1,
            "strongly_connected": strongly_connected(current_transfer),
            "primitive_power": current_primitive,
            "source_rows": source_rows,
            "missing_generator": (
                "same-surface off-diagonal source/orthogonal neutral transfer "
                "or row coupling"
            ),
        },
        "future_mixed_generator_example": {
            "names": ["I", "P_source", "T_with_source_orthogonal_mixing"],
            "algebra_dimension": matrix_rank(future_algebra),
            "full_matrix_algebra_dimension": 4,
            "commutant_dimension": commutant_dimension(future_generators),
            "scalar_commutant_dimension": 1,
            "burnside_irreducible": matrix_rank(future_algebra) == 4
            and commutant_dimension(future_generators) == 1,
            "strongly_connected": strongly_connected(future_mixing_transfer),
            "primitive_power": future_primitive,
            "interpretation": (
                "This is an acceptance-shape example only.  It is not a PR230 "
                "measurement or theorem until the off-diagonal generator is "
                "derived on the same surface."
            ),
        },
    }


def future_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_generator_set",
            "required": "explicit PR230 neutral scalar generator set after gauge, fermion, scalar-source, and canonical-Higgs construction",
            "current_satisfied": False,
        },
        {
            "id": "full_matrix_algebra_or_scalar_commutant",
            "required": "Burnside certificate that the generated algebra is M_n or the commutant is scalar-only",
            "current_satisfied": False,
        },
        {
            "id": "primitive_positive_transfer",
            "required": "equivalent nonnegative transfer matrix with a positive finite power on the same neutral cone",
            "current_satisfied": False,
        },
        {
            "id": "source_and_canonical_higgs_overlap",
            "required": "nonzero certified source and canonical-Higgs overlaps with the unique lowest isolated pole",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "reject H_unit, Ward, observed selectors, alpha/plaquette/u0, reduced pilots, unit c2/Z_match/kappa_s, and PSLQ selectors",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 neutral-scalar Burnside irreducibility attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in parents.items()}
    future_present = future_presence()
    witnesses = burnside_witnesses()
    current = witnesses["current_source_only_generators"]
    future = witnesses["future_mixed_generator_example"]
    contract = future_certificate_contract()
    missing_contract = [row["id"] for row in contract if not row["current_satisfied"]]

    selector_loaded = (
        parents["clean_source_higgs_math_selector"].get("clean_physics_priority")
        == "source_higgs"
    )
    invariant_ring_blocks = (
        "invariant-ring O_H certificate attempt blocked"
        in statuses["invariant_ring_oh_attempt"]
        and parents["invariant_ring_oh_attempt"].get("invariant_ring_certificate_passed")
        is False
    )
    commutant_no_go_loaded = (
        "neutral scalar commutant does not force rank-one purity"
        in statuses["neutral_scalar_commutant_rank_no_go"]
        and parents["neutral_scalar_commutant_rank_no_go"].get("rank_one_theorem_derived")
        is False
    )
    authority_absent = (
        parents["neutral_scalar_irreducibility_authority_audit"].get(
            "neutral_scalar_irreducibility_certificate_present"
        )
        is False
    )
    primitive_gate_absent = (
        parents["neutral_scalar_primitive_cone_certificate_gate"].get(
            "primitive_cone_certificate_gate_passed"
        )
        is False
    )
    primitive_stretch_blocks = (
        parents["neutral_scalar_primitive_cone_stretch_no_go"].get(
            "primitive_cone_stretch_no_go_passed"
        )
        is True
    )
    direct_positivity_blocks = (
        parents["neutral_scalar_positivity_improving_direct_closure"].get(
            "direct_positivity_improving_theorem_derived"
        )
        is False
    )
    conditional_perron_loaded = (
        parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and parents["positivity_improving_neutral_scalar_rank_one"].get(
            "positivity_improving_certificate_present"
        )
        is False
    )
    current_algebra_not_full = (
        current["algebra_dimension"] < current["full_matrix_algebra_dimension"]
        and current["commutant_dimension"] > current["scalar_commutant_dimension"]
    )
    current_not_primitive = (
        current["strongly_connected"] is False
        and current["primitive_power"]["positive"] is False
    )
    future_shape_is_decisive = (
        future["algebra_dimension"] == future["full_matrix_algebra_dimension"]
        and future["commutant_dimension"] == future["scalar_commutant_dimension"]
        and future["burnside_irreducible"] is True
        and future["primitive_power"]["positive"] is True
    )
    future_authority_absent = not any(future_present.values())
    forbidden_firewall_clean = True
    burnside_irreducibility_certificate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("clean-source-higgs-selector-loaded", selector_loaded, statuses["clean_source_higgs_math_selector"])
    report("invariant-ring-oh-attempt-blocks", invariant_ring_blocks, statuses["invariant_ring_oh_attempt"])
    report("commutant-rank-no-go-loaded", commutant_no_go_loaded, statuses["neutral_scalar_commutant_rank_no_go"])
    report("irreducibility-authority-absent", authority_absent, statuses["neutral_scalar_irreducibility_authority_audit"])
    report("primitive-cone-gate-absent", primitive_gate_absent, statuses["neutral_scalar_primitive_cone_certificate_gate"])
    report("primitive-cone-stretch-blocks", primitive_stretch_blocks, statuses["neutral_scalar_primitive_cone_stretch_no_go"])
    report("direct-positivity-theorem-not-derived", direct_positivity_blocks, statuses["neutral_scalar_positivity_improving_direct_closure"])
    report("conditional-perron-support-loaded", conditional_perron_loaded, statuses["positivity_improving_neutral_scalar_rank_one"])
    report("current-burnside-algebra-not-full", current_algebra_not_full, f"dim={current['algebra_dimension']}, commutant={current['commutant_dimension']}")
    report("current-transfer-not-primitive", current_not_primitive, f"primitive={current['primitive_power']}")
    report("future-offdiagonal-shape-would-be-decisive", future_shape_is_decisive, f"dim={future['algebra_dimension']}, commutant={future['commutant_dimension']}")
    report("future-burnside-authority-absent", future_authority_absent, f"future_present={future_present}")
    report("future-certificate-contract-recorded", len(missing_contract) == 4, f"missing={missing_contract}")
    report("forbidden-firewall-clean", forbidden_firewall_clean, ", ".join(FORBIDDEN_INPUTS))
    report("burnside-irreducibility-certificate-not-passed", not burnside_irreducibility_certificate_passed, "no same-surface off-diagonal generator")

    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and selector_loaded
        and invariant_ring_blocks
        and commutant_no_go_loaded
        and authority_absent
        and primitive_gate_absent
        and primitive_stretch_blocks
        and direct_positivity_blocks
        and conditional_perron_loaded
        and current_algebra_not_full
        and current_not_primitive
        and future_shape_is_decisive
        and future_authority_absent
        and forbidden_firewall_clean
        and not burnside_irreducibility_certificate_passed
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Burnside neutral irreducibility attempt "
            "blocked by non-full current generator algebra"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface neutral generator set "
            "generates the full matrix algebra or a primitive positive transfer "
            "power, with certified source and canonical-Higgs overlaps"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current PR230 neutral generator set is block diagonal in a "
            "source/orthogonal completion.  Burnside/double-commutant methods "
            "therefore do not prove neutral-sector irreducibility until a "
            "same-surface off-diagonal generator, primitive transfer matrix, "
            "or equivalent non-source row is supplied."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "burnside_irreducibility_certificate_passed": burnside_irreducibility_certificate_passed,
        "burnside_certificate_written": False,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_file_presence": future_present,
        "burnside_witnesses": witnesses,
        "future_certificate_contract": contract,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write a neutral irreducibility or primitive-cone certificate",
            "does not treat source-only C_ss rows as off-diagonal generator data",
            "does not import H_unit, Ward, observed targets, alpha_LM, plaquette, u0, reduced pilots, c2=1, Z_match=1, kappa_s=1, or PSLQ selectors",
            "does not use the future mixed-generator example as PR230 evidence",
        ],
        "exact_next_action": (
            "To make the neutral Burnside route positive, supply a same-surface "
            "neutral scalar generator set with source/orthogonal mixing and "
            "prove that its generated algebra is full M_n, or supply an "
            "equivalent primitive-cone certificate.  Otherwise return to "
            "certified O_H/C_sH/C_HH rows, W/Z response rows, Schur A/B/C rows, "
            "or strict scalar-LSZ moment/threshold/FV authority."
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
