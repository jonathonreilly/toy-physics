#!/usr/bin/env python3
"""
PR #230 taste-radial canonical-O_H selector gate.

The two-source taste-radial chart/action artifacts give a real same-surface
source axis.  This runner checks the next non-chunk question: can that axis be
identified with canonical O_H from the current Cl(3)/Z^3 taste symmetries
alone?

Result: exact support plus an exact boundary.  The degree-one Z3-invariant
taste-radial direction is unique inside span{S0,S1,S2}.  But the full
Z3-invariant trace-zero taste algebra has higher-degree alternatives with the
same basic symmetry/source-orthogonality filters.  A same-surface action,
canonical-Higgs certificate, or production response bridge is still required.
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
    / "yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json"
)

PARENTS = {
    "two_source_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
    "two_source_row_manifest": "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json",
    "source_coordinate_transport_completion": "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "taste_radial_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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
        raise ValueError("cannot normalize zero matrix")
    return a / n


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def matrix_rank_from_basis(basis: list[np.ndarray], tol: float = 1.0e-12) -> int:
    rows = [b.reshape(-1) for b in basis]
    return int(np.linalg.matrix_rank(np.vstack(rows), tol=tol))


def eigenspace_dimension(matrix: np.ndarray, eigenvalue: complex, tol: float = 1.0e-12) -> int:
    shifted = matrix - eigenvalue * np.eye(matrix.shape[0], dtype=complex)
    return int(matrix.shape[0] - np.linalg.matrix_rank(shifted, tol=tol))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_or_plaquette": False,
        "used_taste_radial_axis_as_canonical_oh": False,
        "used_degree_one_premise_as_derived": False,
        "set_kappa_s_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def candidate_summary(name: str, op: np.ndarray, source: np.ndarray, u: np.ndarray) -> dict[str, Any]:
    return {
        "name": name,
        "trace": float(np.trace(op).real),
        "norm": hs_norm(op),
        "source_overlap": float(hs_inner(source, op).real),
        "z3_invariance_error": max_abs(u @ op @ u.conj().T - op),
        "hermiticity_error": max_abs(op - op.conj().T),
        "spectrum": [float(v) for v in np.sort(np.linalg.eigvalsh(op).real)],
    }


def main() -> int:
    print("PR #230 taste-radial canonical-O_H selector gate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()

    source = np.eye(8, dtype=complex)
    axes = taste_axes()
    s0, s1, s2 = axes
    e1 = s0 + s1 + s2
    e2 = s0 @ s1 + s1 @ s2 + s2 @ s0
    e3 = s0 @ s1 @ s2
    h1 = normalize(e1)
    h2 = normalize(e2)
    h3 = normalize(e3)
    invariant_basis = [h1, h2, h3]
    u = cyclic_tensor_permutation()

    # The cyclic action on the degree-one source-axis coefficient vector sends
    # (a0,a1,a2) to (a1,a2,a0); its +1 eigenspace is the radial line.
    degree_one_cycle = np.array(
        [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]],
        dtype=complex,
    )
    degree_one_invariant_dim = eigenspace_dimension(degree_one_cycle, 1.0)
    degree_one_radial_unique = degree_one_invariant_dim == 1

    invariant_rank = matrix_rank_from_basis(invariant_basis)
    invariant_gram = [
        [float(hs_inner(invariant_basis[i], invariant_basis[j]).real) for j in range(3)]
        for i in range(3)
    ]
    invariant_filters = [
        candidate_summary("degree1_radial_E1", h1, source, u),
        candidate_summary("degree2_pair_E2", h2, source, u),
        candidate_summary("degree3_triple_E3", h3, source, u),
        candidate_summary("mixed_E1_E2", normalize(h1 + h2), source, u),
    ]
    all_invariants_pass_basic_filters = all(
        abs(c["trace"]) < 1.0e-12
        and abs(c["norm"] - 1.0) < 1.0e-12
        and abs(c["source_overlap"]) < 1.0e-12
        and c["z3_invariance_error"] < 1.0e-12
        and c["hermiticity_error"] < 1.0e-12
        for c in invariant_filters
    )
    full_invariant_selector_nonunique = invariant_rank == 3 and all_invariants_pass_basic_filters
    spectra_distinguish_candidates = (
        invariant_filters[0]["spectrum"] != invariant_filters[1]["spectrum"]
        and invariant_filters[0]["spectrum"] != invariant_filters[2]["spectrum"]
    )

    chart_support = (
        parents["two_source_chart"].get("two_source_taste_radial_chart_support_passed")
        is True
        and parents["two_source_chart"].get("proposal_allowed") is False
    )
    action_support = (
        parents["two_source_action"].get("two_source_taste_radial_action_passed") is True
        and parents["two_source_action"].get("proposal_allowed") is False
        and parents["two_source_action"].get("operator_certificate_payload", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    row_contract_support = (
        parents["two_source_row_contract"].get("two_source_taste_radial_row_contract_passed")
        is True
        and parents["two_source_row_contract"].get("proposal_allowed") is False
    )
    row_manifest_support = (
        parents["two_source_row_manifest"].get("manifest_passed") is True
        and parents["two_source_row_manifest"].get("dry_run_only") is True
        and parents["two_source_row_manifest"].get("proposal_allowed") is False
    )
    one_source_still_blocked = (
        parents["source_coordinate_transport_completion"].get(
            "source_coordinate_transport_completion_passed"
        )
        is True
        and parents["source_coordinate_transport_completion"].get("proposal_allowed")
        is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and futures["canonical_oh_certificate"] is False
    )
    production_rows_absent = (
        futures["taste_radial_rows"] is False and futures["source_higgs_rows"] is False
    )
    source_higgs_not_ready = (
        parents["source_higgs_readiness"].get("source_higgs_launch_ready") is False
        and parents["source_higgs_builder"].get("input_present") is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    degree_one_premise_status = (
        "conditional-support: if a same-surface EW/Higgs action proves the "
        "canonical scalar is the degree-one radial fluctuation in span{S0,S1,S2}, "
        "then the taste-radial source is the unique Z3-invariant target"
    )
    symmetry_only_status = (
        "exact negative boundary: Z3, trace-zero, source-orthogonality, "
        "Hermiticity, and Hilbert-Schmidt normalization leave a 3D invariant "
        "taste algebra and do not select canonical O_H"
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("two-source-chart-support-loaded", chart_support, statuses["two_source_chart"])
    report("two-source-action-support-loaded", action_support, statuses["two_source_action"])
    report("two-source-row-contract-support-loaded", row_contract_support, statuses["two_source_row_contract"])
    report("two-source-row-manifest-support-loaded", row_manifest_support, statuses["two_source_row_manifest"])
    report("one-source-route-still-blocked", one_source_still_blocked, statuses["source_coordinate_transport_completion"])
    report("degree-one-z3-radial-unique", degree_one_radial_unique, f"invariant_dim={degree_one_invariant_dim}")
    report("full-z3-tracezero-invariant-subspace-nonunique", full_invariant_selector_nonunique, f"rank={invariant_rank}")
    report("basic-filters-do-not-select-e1", all_invariants_pass_basic_filters, str(invariant_filters))
    report("candidate-spectra-differ", spectra_distinguish_candidates, str([c["spectrum"] for c in invariant_filters[:3]]))
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("production-rows-absent", production_rows_absent, str(futures))
    report("source-higgs-launch-still-not-ready", source_higgs_not_ready, statuses["source_higgs_readiness"])
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))

    gate_passed = (
        not missing
        and not proposal_allowed
        and chart_support
        and action_support
        and row_contract_support
        and row_manifest_support
        and one_source_still_blocked
        and degree_one_radial_unique
        and full_invariant_selector_nonunique
        and all_invariants_pass_basic_filters
        and spectra_distinguish_candidates
        and canonical_oh_absent
        and production_rows_absent
        and source_higgs_not_ready
        and retained_open
        and campaign_open
        and firewall_clean
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / degree-one taste-radial uniqueness with exact "
            "negative boundary for symmetry-only canonical O_H selection"
        ),
        "conditional_surface_status": (
            "conditional-support if a same-surface EW/Higgs action or canonical "
            "operator theorem proves canonical O_H is the degree-one radial "
            "fluctuation in span{S0,S1,S2}"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The degree-one Z3-invariant taste-radial direction is unique only "
            "after importing or deriving the degree-one radial-Higgs premise. "
            "The current Cl(3)/Z^3 taste symmetry filters leave E1, E2, E3, and "
            "their mixtures admissible, so the taste-radial source cannot be "
            "identified with canonical O_H by symmetry notation alone.  "
            "Production C_sx/C_xx rows, a canonical-O_H certificate, or a "
            "same-source physical-response bypass remain required."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "parent_statuses": statuses,
        "future_file_presence": futures,
        "degree_one_premise_status": degree_one_premise_status,
        "symmetry_only_status": symmetry_only_status,
        "degree_one_z3_invariant_dimension": degree_one_invariant_dim,
        "degree_one_radial_unique": degree_one_radial_unique,
        "z3_tracezero_invariant_basis": ["E1=S0+S1+S2", "E2=S0S1+S1S2+S2S0", "E3=S0S1S2"],
        "z3_tracezero_invariant_rank": invariant_rank,
        "z3_tracezero_invariant_gram": invariant_gram,
        "full_invariant_selector_nonunique": full_invariant_selector_nonunique,
        "candidate_summaries": invariant_filters,
        "spectra_distinguish_candidates": spectra_distinguish_candidates,
        "canonical_oh_selector_absent": canonical_oh_absent,
        "production_rows_absent": production_rows_absent,
        "forbidden_firewall": forbidden_firewall(),
        "taste_radial_canonical_oh_selector_gate_passed": gate_passed,
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
