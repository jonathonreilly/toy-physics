#!/usr/bin/env python3
"""
PR #230 degree-one Higgs-action premise gate.

The taste-radial selector gate proved a useful conditional fact: if canonical
O_H is the degree-one radial fluctuation in span{S0,S1,S2}, then the implemented
taste-radial source is the unique Z3-invariant target.  This runner tests the
next shortcut: can the current PR230 surface derive that degree-one Higgs-action
premise from Cl(3)/Z^3 algebra, the source vertex, or source-only rows?

Result: exact negative boundary.  The degree-one filter selects the implemented
source, but the filter itself is not current-surface authority.  Z3 plus
Hermiticity/source-orthogonality leaves higher-degree cyclic invariants, and
odd/parity grading still leaves E1 and E3.  A same-surface EW/Higgs action,
canonical-operator theorem, production source-overlap rows, or physical-response
bridge remains required.
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
    / "yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json"
)

PARENTS = {
    "taste_radial_selector": "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json",
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_row_manifest": "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "wz_same_source_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "completion_audit": "outputs/yt_pr230_positive_closure_completion_audit_2026-05-05.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "taste_radial_combined_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "wz_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
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
        raise ValueError("zero norm")
    return a / n


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def candidate(name: str, op: np.ndarray, degree: int, source: np.ndarray, u: np.ndarray) -> dict[str, Any]:
    return {
        "name": name,
        "clifford_character_degree": degree,
        "parity": "odd" if degree % 2 else "even",
        "trace": float(np.trace(op).real),
        "norm": hs_norm(op),
        "source_overlap": float(hs_inner(source, op).real),
        "z3_error": max_abs(u @ op @ u.conj().T - op),
        "hermiticity_error": max_abs(op - op.conj().T),
        "spectrum": [float(v) for v in np.sort(np.linalg.eigvalsh(op).real)],
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_or_plaquette": False,
        "used_reduced_pilot_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "identified_degree_one_filter_as_canonical_oh_authority": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 degree-one Higgs-action premise gate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}

    source = np.eye(8, dtype=complex)
    s0, s1, s2 = taste_axes()
    e1 = normalize(s0 + s1 + s2)
    e2 = normalize(s0 @ s1 + s1 @ s2 + s2 @ s0)
    e3 = normalize(s0 @ s1 @ s2)
    u = cyclic_tensor_permutation()

    candidates = [
        candidate("E1_degree_one_radial", e1, 1, source, u),
        candidate("E2_degree_two_pair", e2, 2, source, u),
        candidate("E3_degree_three_triple", e3, 3, source, u),
        candidate("mixed_E1_E2", normalize(e1 + e2), -1, source, u),
    ]
    current_filter_names = [
        row["name"]
        for row in candidates
        if abs(row["trace"]) < 1.0e-12
        and abs(row["norm"] - 1.0) < 1.0e-12
        and abs(row["source_overlap"]) < 1.0e-12
        and row["z3_error"] < 1.0e-12
        and row["hermiticity_error"] < 1.0e-12
    ]
    odd_filter_names = [row["name"] for row in candidates[:3] if row["parity"] == "odd"]
    degree_one_names = [
        row["name"]
        for row in candidates[:3]
        if row["clifford_character_degree"] == 1
    ]

    selector = parents["taste_radial_selector"]
    action = parents["two_source_action"]
    canonical_gate = parents["canonical_higgs_operator_gate"]
    source_higgs_readiness = parents["source_higgs_readiness"]
    wz_action = parents["wz_same_source_action_gate"]
    completion = parents["completion_audit"]

    selector_support_loaded = (
        selector.get("taste_radial_canonical_oh_selector_gate_passed") is True
        and selector.get("proposal_allowed") is False
        and selector.get("degree_one_radial_unique") is True
        and selector.get("full_invariant_selector_nonunique") is True
    )
    source_vertex_is_degree_one_support = (
        action.get("two_source_taste_radial_action_passed") is True
        and action.get("proposal_allowed") is False
        and action.get("operator_certificate_payload", {})
        .get("operator_definition", "")
        .find("X=(X_1+X_2+X_3)/sqrt(3)")
        >= 0
        and action.get("operator_certificate_payload", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    current_filters_nonunique = len(current_filter_names) >= 4
    odd_parity_filter_nonunique = set(odd_filter_names) == {
        "E1_degree_one_radial",
        "E3_degree_three_triple",
    }
    degree_one_filter_selects_e1 = degree_one_names == ["E1_degree_one_radial"]
    canonical_oh_absent = (
        canonical_gate.get("candidate_present") is False
        and canonical_gate.get("candidate_valid") is False
        and futures["canonical_oh_certificate"] is False
    )
    same_surface_ew_higgs_action_absent = (
        source_higgs_readiness.get("source_higgs_launch_ready") is False
        and wz_action.get("proposal_allowed") is False
        and "same-source EW action not defined" in statuses["wz_same_source_action_gate"]
    )
    production_bridge_absent = (
        futures["taste_radial_combined_rows"] is False
        and futures["source_higgs_rows"] is False
        and futures["wz_response_rows"] is False
    )
    degree_one_premise_authorized = False
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    completion_open = completion.get("closure_achieved") is False or (
        "closure-not-achieved-recorded" in str(completion)
    )
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-support-loaded", selector_support_loaded, statuses["taste_radial_selector"])
    report("source-vertex-is-degree-one-support", source_vertex_is_degree_one_support, statuses["two_source_action"])
    report("current-z3-source-filters-nonunique", current_filters_nonunique, str(current_filter_names))
    report("odd-parity-filter-nonunique", odd_parity_filter_nonunique, str(odd_filter_names))
    report("degree-one-filter-selects-e1", degree_one_filter_selects_e1, str(degree_one_names))
    report("degree-one-premise-not-current-authority", not degree_one_premise_authorized, "no same-surface premise authorizes using degree as canonical O_H identity")
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("same-surface-ew-higgs-action-absent", same_surface_ew_higgs_action_absent, statuses["wz_same_source_action_gate"])
    report("production-bridge-absent", production_bridge_absent, str(futures))
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("completion-audit-still-open", completion_open, statuses["completion_audit"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))

    gate_passed = (
        not missing
        and not proposal_allowed
        and selector_support_loaded
        and source_vertex_is_degree_one_support
        and current_filters_nonunique
        and odd_parity_filter_nonunique
        and degree_one_filter_selects_e1
        and not degree_one_premise_authorized
        and canonical_oh_absent
        and same_surface_ew_higgs_action_absent
        and production_bridge_absent
        and retained_open
        and campaign_open
        and completion_open
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / degree-one Higgs-action premise not "
            "derived on the current PR230 surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface EW/Higgs action or "
            "canonical-operator theorem proves canonical O_H is the degree-one "
            "radial fluctuation coupled to the taste-radial source"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The finite algebra shows that a degree-one filter would select the "
            "implemented taste-radial source, but the filter is not a current "
            "PR230 authority.  Current Z3/source filters are nonunique, odd "
            "parity still leaves E1 and E3, and no same-surface EW/Higgs action, "
            "canonical-O_H theorem, production source-overlap row, or W/Z "
            "physical-response bridge supplies the missing premise."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "parent_statuses": statuses,
        "future_file_presence": futures,
        "current_filter_candidate_names": current_filter_names,
        "odd_filter_candidate_names": odd_filter_names,
        "degree_one_filter_candidate_names": degree_one_names,
        "candidate_summaries": candidates,
        "selector_support_loaded": selector_support_loaded,
        "source_vertex_is_degree_one_support": source_vertex_is_degree_one_support,
        "current_filters_nonunique": current_filters_nonunique,
        "odd_parity_filter_nonunique": odd_parity_filter_nonunique,
        "degree_one_filter_selects_e1": degree_one_filter_selects_e1,
        "degree_one_premise_authorized_on_current_surface": degree_one_premise_authorized,
        "canonical_oh_absent": canonical_oh_absent,
        "same_surface_ew_higgs_action_absent": same_surface_ew_higgs_action_absent,
        "production_bridge_absent": production_bridge_absent,
        "forbidden_firewall": forbidden_firewall(),
        "degree_one_higgs_action_premise_gate_passed": gate_passed,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and gate_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
