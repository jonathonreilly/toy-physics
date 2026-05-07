#!/usr/bin/env python3
"""
PR #230 degree-one radial-tangent O_H theorem.

This runner isolates the cleanest action-first O_H bridge that is honestly
available from the current Cl(3)/Z^3 taste surface.  It proves an exact
finite-dimensional theorem: if a future same-surface EW/Higgs action supplies
a canonical Higgs operator whose infinitesimal radial tangent is linear in the
three PR230 taste axes and Z3-covariant, then the tangent axis is unique and is
the taste-radial source already implemented by the two-source harness.

The theorem does not derive the future action, canonical kinetic/LSZ
normalization, or C_ss/C_sH/C_HH pole rows.  It is support for the clean
source-Higgs route, not top-Yukawa closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json"
)

PARENTS = {
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "taste_radial_selector": "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json",
    "degree_one_premise": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "fms_composite_oh": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "used_reduced_pilot_as_production_evidence": False,
    "used_degree_one_premise_as_current_oh_proof": False,
    "treated_taste_radial_source_as_canonical_oh": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def pauli_x() -> np.ndarray:
    return np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def taste_axes() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = pauli_x()
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def cyclic_tensor_permutation() -> np.ndarray:
    """Matrix for U|a,b,c> = |c,a,b> in the binary tensor basis."""
    u = np.zeros((8, 8), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                src = 4 * a + 2 * b + c
                dst = 4 * c + 2 * a + b
                u[dst, src] = 1.0
    return u


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def hs_norm(a: np.ndarray) -> float:
    return math.sqrt(max(float(hs_inner(a, a).real), 0.0))


def normalize(a: np.ndarray) -> np.ndarray:
    n = hs_norm(a)
    if n == 0.0:
        raise ValueError("cannot normalize zero operator")
    return a / n


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def eigenspace_dimension(matrix: np.ndarray, eigenvalue: complex, tol: float = 1.0e-12) -> int:
    shifted = matrix - eigenvalue * np.eye(matrix.shape[0], dtype=complex)
    return int(matrix.shape[0] - np.linalg.matrix_rank(shifted, tol=tol))


def matrix_rank_from_basis(basis: list[np.ndarray], tol: float = 1.0e-12) -> int:
    rows = [b.reshape(-1) for b in basis]
    return int(np.linalg.matrix_rank(np.vstack(rows), tol=tol))


def spectral_summary(op: np.ndarray) -> list[float]:
    return [float(x) for x in np.sort(np.linalg.eigvalsh(op).real)]


def main() -> int:
    print("PR #230 degree-one radial-tangent O_H theorem")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    s0, s1, s2 = taste_axes()
    axes = [s0, s1, s2]
    source_identity = np.eye(8, dtype=complex)
    u = cyclic_tensor_permutation()

    z3_action_errors = {
        "U3_minus_I": max_abs(np.linalg.matrix_power(u, 3) - source_identity),
        "US0Udag_minus_S1": max_abs(u @ s0 @ u.conj().T - s1),
        "US1Udag_minus_S2": max_abs(u @ s1 @ u.conj().T - s2),
        "US2Udag_minus_S0": max_abs(u @ s2 @ u.conj().T - s0),
    }

    # Coefficient action on a0*S0+a1*S1+a2*S2 induced by U S_i U^-1.
    coeff_cycle = np.array(
        [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=complex,
    )
    invariant_dim = eigenspace_dimension(coeff_cycle, 1.0)
    radial_coeff = np.array([1.0, 1.0, 1.0], dtype=complex) / math.sqrt(3.0)
    radial_source_norm_matched = (s0 + s1 + s2) / math.sqrt(3.0)
    radial_hs_unit = normalize(s0 + s1 + s2)
    parent_axis_matches = (
        certs["two_source_action"].get("two_source_taste_radial_action_passed") is True
        and certs["two_source_action"].get("operator_id")
        == "pr230_taste_radial_hypercube_flip_source_v1"
        and certs["two_source_action"].get("canonical_higgs_operator_identity_passed")
        is False
    )

    e1 = s0 + s1 + s2
    e2 = s0 @ s1 + s1 @ s2 + s2 @ s0
    e3 = s0 @ s1 @ s2
    invariant_basis = [normalize(e1), normalize(e2), normalize(e3)]
    invariant_rank = matrix_rank_from_basis(invariant_basis)
    higher_degree_ambiguity = (
        certs["taste_radial_selector"].get("full_invariant_selector_nonunique") is True
        and invariant_rank == 3
    )
    degree_one_current_premise_absent = (
        certs["degree_one_premise"].get("degree_one_premise_authorized_on_current_surface")
        is False
        and "degree-one Higgs-action premise not derived"
        in statuses["degree_one_premise"]
    )
    fms_still_conditional = (
        certs["fms_composite_oh"].get("proposal_allowed") is False
        and "conditional-support" in statuses["fms_composite_oh"]
    )
    pole_rows_absent = (
        certs["source_higgs_pole_row_contract"].get("rows_present") is False
        and certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_gate"].get("candidate_present") is False
        and certs["canonical_higgs_gate"].get("candidate_valid") is False
    )
    aggregate_denies_proposal = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    theorem_passed = (
        not missing
        and not proposal_allowed
        and all(err < 1.0e-12 for err in z3_action_errors.values())
        and invariant_dim == 1
        and abs(hs_norm(radial_source_norm_matched) - hs_norm(source_identity)) < 1.0e-12
        and abs(float(np.trace(radial_source_norm_matched).real)) < 1.0e-12
        and abs(float(hs_inner(source_identity, radial_source_norm_matched).real)) < 1.0e-12
        and parent_axis_matches
        and higher_degree_ambiguity
        and degree_one_current_premise_absent
        and fms_still_conditional
        and pole_rows_absent
        and canonical_oh_absent
        and aggregate_denies_proposal
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-surface-z3-action-exact", all(err < 1.0e-12 for err in z3_action_errors.values()), str(z3_action_errors))
    report("degree-one-z3-invariant-line-unique", invariant_dim == 1, f"dim={invariant_dim}")
    report("radial-coefficients-fixed", np.allclose(radial_coeff, [1 / math.sqrt(3.0)] * 3), str(radial_coeff.real.tolist()))
    report("radial-axis-source-norm-matched", abs(hs_norm(radial_source_norm_matched) - hs_norm(source_identity)) < 1.0e-12, f"norm={hs_norm(radial_source_norm_matched)}")
    report("radial-axis-source-orthogonal", abs(float(hs_inner(source_identity, radial_source_norm_matched).real)) < 1.0e-12, "Tr(I*R)=0")
    report("two-source-action-axis-matches-theorem", parent_axis_matches, statuses["two_source_action"])
    report("higher-degree-ambiguity-preserved", higher_degree_ambiguity, f"invariant_rank={invariant_rank}")
    report("degree-one-current-premise-absent", degree_one_current_premise_absent, statuses["degree_one_premise"])
    report("fms-action-bridge-still-conditional", fms_still_conditional, statuses["fms_composite_oh"])
    report("canonical-oh-and-pole-rows-absent", canonical_oh_absent and pole_rows_absent, f"oh_absent={canonical_oh_absent} rows_absent={pole_rows_absent}")
    report("retained-and-campaign-deny-proposal", aggregate_denies_proposal, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    result = {
        "actual_current_surface_status": (
            "exact-support / degree-one radial-tangent O_H uniqueness theorem; "
            "same-surface action/LSZ premise and pole rows absent"
        ),
        "conditional_surface_status": (
            "exact-support for O_H axis selection if a future same-surface EW/Higgs "
            "action proves canonical O_H is a linear Z3-covariant radial tangent "
            "in span{S0,S1,S2} and supplies canonical kinetic/LSZ normalization"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem selects the degree-one tangent axis under a named future "
            "action premise, but the current surface lacks the action premise, "
            "canonical O_H certificate, C_ss/C_sH/C_HH pole rows, and retained-route approval."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "degree_one_radial_tangent_oh_theorem_passed": theorem_passed,
        "degree_one_tangent_unique": invariant_dim == 1,
        "same_surface_linear_tangent_premise_derived": False,
        "canonical_oh_identity_derived": False,
        "source_higgs_pole_rows_present": False,
        "z3_action_errors": z3_action_errors,
        "radial_axis": {
            "coefficient_basis": ["S0", "S1", "S2"],
            "coefficients_source_norm_matched": radial_coeff.real.tolist(),
            "operator": "(S0 + S1 + S2) / sqrt(3)",
            "hilbert_schmidt_norm": hs_norm(radial_source_norm_matched),
            "trace": float(np.trace(radial_source_norm_matched).real),
            "source_identity_overlap": float(hs_inner(source_identity, radial_source_norm_matched).real),
            "spectrum": spectral_summary(radial_source_norm_matched),
            "hilbert_schmidt_unit_operator": "(S0 + S1 + S2) / sqrt(24)",
            "hilbert_schmidt_unit_norm": hs_norm(radial_hs_unit),
        },
        "higher_degree_boundary": {
            "z3_tracezero_invariant_rank": invariant_rank,
            "basis": ["E1=S0+S1+S2", "E2=S0S1+S1S2+S2S0", "E3=S0S1S2"],
            "boundary": (
                "Z3 symmetry over the full commuting trace-zero taste algebra is "
                "nonunique; the degree-one tangent premise is load-bearing."
            ),
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not identify the current taste-radial source with canonical O_H on the actual surface",
            "does not derive the same-surface EW/Higgs action or canonical kinetic/LSZ normalization",
            "does not supply C_ss/C_sH/C_HH pole rows",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
        ],
        "exact_next_action": (
            "Use this theorem as the action-first O_H axis selector only after "
            "deriving the same-surface EW/Higgs action and canonical LSZ "
            "normalization; then run source-Higgs pole rows and Gram/FV/IR gates."
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
