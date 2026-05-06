#!/usr/bin/env python3
"""
PR #230 source-coordinate transport gate.

This runner tests the remaining pure source-coordinate route in the cleanest
O_H/C_sH/C_HH contract: can the PR230 uniform additive mass source be
transported, by an allowed same-surface coordinate change, into a canonical
trace-zero taste/Higgs axis?

Current answer: no.  A scalar reparametrization of the existing one-dimensional
source line keeps the tangent proportional to I_8.  A Cl/taste automorphism
fixes I_8.  A map with a nonzero trace-zero taste-axis tangent is a new source
surface, and a map with zero linear tangent cannot supply the LSZ/canonical
linear normalization.  This is a current-surface boundary, not a global
prohibition on future source-Higgs rows or a future two-source action.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_source_coordinate_transport_gate_2026-05-06.json"

FUTURE_TRANSPORT_CERTIFICATE = (
    ROOT / "outputs" / "yt_pr230_source_coordinate_transport_certificate_2026-05-06.json"
)
FUTURE_CANONICAL_OH_CERTIFICATE = (
    ROOT / "outputs" / "yt_canonical_higgs_operator_certificate_2026-05-03.json"
)
FUTURE_SOURCE_HIGGS_ROWS = (
    ROOT / "outputs" / "yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
)

PARENTS = {
    "taste_condensate_oh_bridge_audit": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
    "genuine_source_pole_artifact_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "source_reparametrization_gauge_no_go": "outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "source_pole_mixing_obstruction": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "oh_bridge_candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
    "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def shift_ops() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def norm(a: np.ndarray) -> float:
    return math.sqrt(max(float(hs_inner(a, a).real), 0.0))


def normalized_overlap(a: np.ndarray, b: np.ndarray) -> float:
    denom = norm(a) * norm(b)
    if denom <= 0.0:
        return float("nan")
    return float((hs_inner(a, b) / denom).real)


def projection_norm(target: np.ndarray, basis: list[np.ndarray]) -> float:
    gram = np.asarray([[hs_inner(a, b) for b in basis] for a in basis], dtype=complex)
    rhs = np.asarray([hs_inner(b, target) for b in basis], dtype=complex)
    coeffs = np.linalg.solve(gram, rhs)
    projected = sum(coeff * basis_i for coeff, basis_i in zip(coeffs, basis))
    return norm(projected)


def transport_candidate_rows(identity: np.ndarray, axes: list[np.ndarray]) -> list[dict[str, Any]]:
    axis = axes[0]
    rows = []
    for scale in (0.25, 1.0, 4.0):
        tangent = scale * identity
        rows.append(
            {
                "candidate": f"analytic scalar reparametrization with f'(0)={scale}",
                "allowed_current_surface_coordinate_change": True,
                "adds_new_source_axis": False,
                "invertible_linear_tangent": True,
                "tangent_trace": float(np.trace(tangent).real),
                "taste_axis_overlap": normalized_overlap(tangent, axis),
                "taste_span_projection_relative_norm": projection_norm(tangent, axes) / norm(tangent),
                "can_be_canonical_oh_transport": False,
                "failure_reason": "tangent remains proportional to the uniform identity source",
            }
        )

    tangent = identity
    rows.append(
        {
            "candidate": "Cl/taste automorphism or conjugation of uniform source",
            "allowed_current_surface_coordinate_change": True,
            "adds_new_source_axis": False,
            "invertible_linear_tangent": True,
            "tangent_trace": float(np.trace(tangent).real),
            "taste_axis_overlap": normalized_overlap(tangent, axis),
            "taste_span_projection_relative_norm": projection_norm(tangent, axes) / norm(tangent),
            "can_be_canonical_oh_transport": False,
            "failure_reason": "identity is central and trace/spectrum are invariant",
        }
    )

    tangent = axis
    rows.append(
        {
            "candidate": "linear injection into trace-zero taste/Higgs axis",
            "allowed_current_surface_coordinate_change": False,
            "adds_new_source_axis": True,
            "invertible_linear_tangent": True,
            "tangent_trace": float(np.trace(tangent).real),
            "taste_axis_overlap": normalized_overlap(tangent, axis),
            "taste_span_projection_relative_norm": projection_norm(tangent, axes) / norm(tangent),
            "can_be_canonical_oh_transport": False,
            "failure_reason": "this is the desired O_H source, but it is a new source coupling not present in PR230",
        }
    )

    tangent = identity
    second_derivative_axis = axis
    rows.append(
        {
            "candidate": "nonlinear extension s I + c s^2 S_1",
            "allowed_current_surface_coordinate_change": False,
            "adds_new_source_axis": True,
            "invertible_linear_tangent": True,
            "tangent_trace": float(np.trace(tangent).real),
            "second_derivative_trace_zero_axis_norm": norm(second_derivative_axis),
            "taste_axis_overlap": normalized_overlap(tangent, axis),
            "taste_span_projection_relative_norm": projection_norm(tangent, axes) / norm(tangent),
            "can_be_canonical_oh_transport": False,
            "failure_reason": "linear LSZ tangent is still I; the taste axis appears only in a new higher-order source extension",
        }
    )

    tangent = np.zeros_like(identity)
    rows.append(
        {
            "candidate": "singular or zero-Jacobian map onto taste axis",
            "allowed_current_surface_coordinate_change": False,
            "adds_new_source_axis": True,
            "invertible_linear_tangent": False,
            "tangent_trace": float(np.trace(tangent).real),
            "taste_axis_overlap": None,
            "taste_span_projection_relative_norm": None,
            "can_be_canonical_oh_transport": False,
            "failure_reason": "zero/noninvertible tangent cannot supply a canonical linear LSZ normalization",
        }
    )
    return rows


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "failed_checks": ["source-coordinate transport certificate absent"],
        }
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "pr230_source_coordinate_transport",
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "maps_uniform_source_to_canonical_oh": candidate.get("maps_uniform_source_to_canonical_oh") is True,
        "invertible_linear_lsz_jacobian": isinstance(candidate.get("linear_lsz_jacobian"), (int, float))
        and math.isfinite(float(candidate.get("linear_lsz_jacobian")))
        and abs(float(candidate.get("linear_lsz_jacobian"))) > 0.0,
        "canonical_oh_certificate": isinstance(candidate.get("canonical_oh_certificate"), str)
        and bool(candidate.get("canonical_oh_certificate")),
        "no_hunit": firewall.get("used_hunit_matrix_element_readout") is False,
        "no_ward": firewall.get("used_yt_ward_identity") is False,
        "no_observed": firewall.get("used_observed_targets_as_selectors") is False,
        "no_alpha_plaquette_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_kappa_by_fiat": firewall.get("set_kappa_s_equal_one") is False,
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def main() -> int:
    print("PR #230 source-coordinate transport gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}

    identity = np.eye(8, dtype=complex)
    axes = shift_ops()
    axis_traces = [float(np.trace(axis).real) for axis in axes]
    identity_axis_overlaps = [normalized_overlap(identity, axis) for axis in axes]
    identity_projection_relative_norm = projection_norm(identity, axes) / norm(identity)
    rows = transport_candidate_rows(identity, axes)
    candidate = load_rel(display(FUTURE_TRANSPORT_CERTIFICATE))
    future_validation = validate_future_certificate(candidate)

    taste_bridge_blocks = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in statuses["taste_condensate_oh_bridge_audit"]
        and parents["taste_condensate_oh_bridge_audit"].get("proposal_allowed") is False
        and parents["taste_condensate_oh_bridge_audit"].get("algebra", {}).get(
            "uniform_source_relative_projection_onto_taste_axis_span"
        )
        == 0.0
    )
    source_pole_support_only = (
        parents["genuine_source_pole_artifact_intake"].get("artifact_is_genuine_current_surface_support")
        is True
        and parents["genuine_source_pole_artifact_intake"].get("artifact_is_physics_closure")
        is False
        and parents["genuine_source_pole_artifact_intake"].get("canonical_higgs_operator_identity_passed")
        is False
    )
    source_reparam_no_go_loaded = (
        "source reparametrization gauge" in statuses["source_reparametrization_gauge_no_go"]
        and parents["source_reparametrization_gauge_no_go"].get("proposal_allowed") is False
    )
    source_lsz_identifiability_blocks = (
        "source-functional LSZ identifiability theorem" in statuses["source_functional_lsz_identifiability"]
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    mixing_obstruction_loaded = (
        "source-pole canonical-Higgs mixing obstruction" in statuses["source_pole_mixing_obstruction"]
        and parents["source_pole_mixing_obstruction"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not FUTURE_CANONICAL_OH_CERTIFICATE.exists()
    )
    source_higgs_rows_absent = (
        parents["source_higgs_readiness"].get("future_rows_present") is False
        and not FUTURE_SOURCE_HIGGS_ROWS.exists()
    )
    builder_contract_open = (
        parents["source_higgs_builder"].get("input_present") is False
        and parents["source_higgs_builder"].get("proposal_allowed") is False
    )
    postprocessor_open = (
        parents["source_higgs_postprocessor"].get("candidate_present") is False
        and parents["source_higgs_postprocessor"].get("proposal_allowed") is False
    )
    candidate_portfolio_open = (
        parents["oh_bridge_candidate_portfolio"].get("candidate_portfolio_passed") is True
        and parents["oh_bridge_candidate_portfolio"].get("proposal_allowed") is False
    )
    negative_review_preserves_reopen = (
        parents["negative_route_applicability_review"].get("future_reopen_paths_preserved") is True
        and parents["negative_route_applicability_review"].get("proposal_allowed") is False
    )
    retained_route_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False

    trace_zero_axes = all(abs(trace) < 1.0e-14 for trace in axis_traces)
    identity_orthogonal = all(abs(overlap) < 1.0e-14 for overlap in identity_axis_overlaps)
    identity_not_in_axis_span = abs(identity_projection_relative_norm) < 1.0e-14
    allowed_candidates_fail = all(
        (not row["allowed_current_surface_coordinate_change"])
        or row["can_be_canonical_oh_transport"] is False
        for row in rows
    )
    desired_axis_requires_new_source = any(
        row["candidate"] == "linear injection into trace-zero taste/Higgs axis"
        and row["adds_new_source_axis"] is True
        and isinstance(row["taste_axis_overlap"], float)
        and abs(row["taste_axis_overlap"] - 1.0) < 1.0e-14
        for row in rows
    )
    future_certificate_absent = not FUTURE_TRANSPORT_CERTIFICATE.exists()

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-bridge-blocks-current-shortcut", taste_bridge_blocks, statuses["taste_condensate_oh_bridge_audit"])
    report("source-pole-support-only", source_pole_support_only, statuses["genuine_source_pole_artifact_intake"])
    report("source-reparametrization-no-go-loaded", source_reparam_no_go_loaded, statuses["source_reparametrization_gauge_no_go"])
    report("source-functional-lsz-identifiability-blocks", source_lsz_identifiability_blocks, statuses["source_functional_lsz_identifiability"])
    report("source-pole-mixing-obstruction-loaded", mixing_obstruction_loaded, statuses["source_pole_mixing_obstruction"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, display(FUTURE_CANONICAL_OH_CERTIFICATE))
    report("source-higgs-rows-absent", source_higgs_rows_absent, display(FUTURE_SOURCE_HIGGS_ROWS))
    report("source-higgs-builder-contract-open", builder_contract_open, statuses["source_higgs_builder"])
    report("source-higgs-postprocessor-open", postprocessor_open, statuses["source_higgs_postprocessor"])
    report("candidate-portfolio-open", candidate_portfolio_open, statuses["oh_bridge_candidate_portfolio"])
    report("negative-review-preserves-reopen", negative_review_preserves_reopen, statuses["negative_route_applicability_review"])
    report("taste-axes-trace-zero", trace_zero_axes, f"Tr(S_i)={axis_traces}")
    report("uniform-source-orthogonal-to-taste-axes", identity_orthogonal, f"rho(I,S_i)={identity_axis_overlaps}")
    report("uniform-source-not-in-taste-axis-span", identity_not_in_axis_span, f"relative_projection={identity_projection_relative_norm:.3e}")
    report("allowed-current-surface-transports-do-not-produce-oh", allowed_candidates_fail, "see transport_candidate_rows")
    report("desired-axis-injection-requires-new-source", desired_axis_requires_new_source, "linear S_1 injection is not the PR230 source line")
    report("future-transport-certificate-absent", future_certificate_absent, display(FUTURE_TRANSPORT_CERTIFICATE))
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])

    gate_passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / source-coordinate transport to canonical O_H not derivable on current PR230 surface"
        ),
        "conditional_surface_status": (
            "The route reopens if a future same-surface source-coordinate "
            "transport certificate supplies an invertible linear LSZ Jacobian "
            "from the PR230 source to a certified canonical O_H, or if direct "
            "O_H/C_sH/C_HH pole rows or an equivalent physical-response bridge land."
        ),
        "hypothetical_axiom_status": (
            "Adding a new trace-zero taste/Higgs source axis would define a new "
            "two-source surface; it is not derived by reparametrizing the current "
            "one-dimensional uniform mass source."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Allowed current-surface coordinate changes preserve the identity-source "
            "linear tangent.  The desired trace-zero Higgs/taste tangent requires a "
            "new source axis or a singular/non-LSZ map."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "source_coordinate_transport_gate_passed": gate_passed,
        "future_transport_certificate": display(FUTURE_TRANSPORT_CERTIFICATE),
        "future_transport_certificate_present": FUTURE_TRANSPORT_CERTIFICATE.exists(),
        "future_transport_certificate_validation": future_validation,
        "future_canonical_oh_certificate_present": FUTURE_CANONICAL_OH_CERTIFICATE.exists(),
        "future_source_higgs_rows_present": FUTURE_SOURCE_HIGGS_ROWS.exists(),
        "algebra": {
            "source_operator": "I_8 uniform additive scalar mass source",
            "taste_axis_operator": "S_i = sigma_x on one taste tensor factor",
            "Tr_S_i": axis_traces,
            "rho_I_S_i": identity_axis_overlaps,
            "I_projection_relative_norm_onto_span_S_i": identity_projection_relative_norm,
        },
        "transport_candidate_rows": rows,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not write a source-coordinate transport certificate",
            "does not write canonical O_H or source-Higgs pole rows",
            "does not identify O_sp with O_H",
            "does not add a trace-zero Higgs source axis and call it current-surface derivation",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Do not spend another block on scalar reparametrization of the uniform "
            "source as O_H.  The next positive artifact must be direct canonical "
            "O_H/C_sH/C_HH rows, a genuine two-source source-transport certificate, "
            "strict W/Z response rows with g2/covariance authority, Schur A/B/C "
            "rows, or a neutral primitive/off-diagonal-generator certificate."
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
