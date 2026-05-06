#!/usr/bin/env python3
"""
PR #230 source-coordinate transport completion attempt.

The current O_H bridge portfolio ranks source-coordinate transport as the
sharpest pure-algebra lane: can the PR230 uniform additive mass source
``m_bare + s`` be transported to the trace-zero taste/Higgs radial source
without adding a new source axiom, H_unit readout, or observed target?

This runner works that lane to the current-surface boundary.  It proves that
the allowed current algebraic moves do not supply the transport:

* unit-preserving algebra automorphisms fix the identity source;
* unitary/similarity transport preserves trace and spectrum;
* Hilbert-Schmidt projection of I_8 onto the taste-axis span is zero;
* any taste-equivariant map from an invariant scalar source to a sign-vector
  taste axis has zero tangent.

A future non-shortcut route can still reopen this lane with an explicit
same-surface source-transport certificate, a certified symmetry-breaking
axis/tangent, or production C_sH/C_HH rows for a separately certified O_H.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
FUTURE_TRANSPORT_CERT = (
    ROOT / "outputs" / "yt_pr230_source_to_taste_axis_transport_certificate_2026-05-06.json"
)

PARENTS = {
    "taste_condensate_oh_bridge": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
    "cl3_automorphism_source_identity": "outputs/yt_cl3_automorphism_source_identity_no_go_2026-05-02.json",
    "cl3_source_unit": "outputs/yt_cl3_source_unit_normalization_no_go_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "source_functional_lsz": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_sector_pattern_transfer": "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json",
    "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
    "candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
}

TEXTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "production_harness": "scripts/yt_direct_lattice_correlator_production.py",
    "candidate_portfolio_note": "docs/YT_PR230_OH_BRIDGE_FIRST_PRINCIPLES_CANDIDATE_PORTFOLIO_NOTE_2026-05-06.md",
}

FUTURE_REOPEN_FILES = {
    "source_to_taste_axis_transport_certificate": str(FUTURE_TRANSPORT_CERT.relative_to(ROOT)),
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "neutral_primitive_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def pauli_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return i2, sx, sz, np.zeros((2, 2), dtype=complex)


def taste_axes() -> list[np.ndarray]:
    i2, sx, _sz, _zero = pauli_basis()
    return [
        np.kron(sx, np.kron(i2, i2)),
        np.kron(i2, np.kron(sx, i2)),
        np.kron(i2, np.kron(i2, sx)),
    ]


def taste_flip_generators() -> list[np.ndarray]:
    i2, _sx, sz, _zero = pauli_basis()
    return [
        np.kron(sz, np.kron(i2, i2)),
        np.kron(i2, np.kron(sz, i2)),
        np.kron(i2, np.kron(i2, sz)),
    ]


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def norm(a: np.ndarray) -> float:
    return math.sqrt(float(hs_inner(a, a).real))


def normalized_overlap(a: np.ndarray, b: np.ndarray) -> float:
    denom = norm(a) * norm(b)
    if denom == 0.0:
        return float("nan")
    return float((hs_inner(a, b) / denom).real)


def projection_norm(target: np.ndarray, basis: list[np.ndarray]) -> float:
    gram = np.asarray([[hs_inner(a, b) for b in basis] for a in basis], dtype=complex)
    rhs = np.asarray([hs_inner(b, target) for b in basis], dtype=complex)
    coeffs = np.linalg.solve(gram, rhs)
    projected = sum(coeff * item for coeff, item in zip(coeffs, basis))
    return norm(projected)


def eig_signature(matrix: np.ndarray) -> list[float]:
    vals = np.linalg.eigvalsh(matrix)
    return [float(round(value.real, 12)) for value in vals]


def conjugation_action(u: np.ndarray, a: np.ndarray) -> np.ndarray:
    return u @ a @ u.conj().T


def validate_future_transport(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "failed_checks": ["source-to-taste-axis transport certificate absent"],
        }
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    certificates = (
        candidate.get("certificates", {}) if isinstance(candidate.get("certificates"), dict) else {}
    )
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "source_to_taste_axis_transport",
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "source_coordinate": candidate.get("source_coordinate") == "m_bare+s",
        "target_operator_kind_allowed": candidate.get("target_operator_kind")
        in {"canonical_taste_axis_higgs", "canonical_higgs_operator"},
        "transport_kind_allowed": candidate.get("transport_kind")
        in {"symmetry_breaking_tangent", "nonlinear_jacobian_theorem", "production_row_measured"},
        "finite_nonzero_jacobian": isinstance(candidate.get("jacobian"), (int, float))
        and math.isfinite(float(candidate.get("jacobian")))
        and abs(float(candidate.get("jacobian"))) > 0.0,
        "axis_selection_or_rows_reference": isinstance(
            certificates.get("axis_selection_or_row_certificate"), str
        )
        and bool(certificates.get("axis_selection_or_row_certificate")),
        "canonical_normalization_reference": isinstance(
            certificates.get("canonical_normalization_certificate"), str
        )
        and bool(certificates.get("canonical_normalization_certificate")),
        "no_hunit": firewall.get("used_hunit_matrix_element_readout") is False,
        "no_ward": firewall.get("used_yt_ward_identity") is False,
        "no_observed_selector": firewall.get("used_observed_targets") is False,
        "no_alpha_lm": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_kappa_by_fiat": firewall.get("set_kappa_s_equal_one") is False,
        "no_source_axis_by_fiat": firewall.get("selected_taste_axis_by_fiat") is False,
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "set_kappa_s_equal_one": False,
        "selected_taste_axis_by_fiat": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 source-coordinate transport completion attempt")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    missing_texts = [name for name, text in texts.items() if not text]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}

    identity = np.eye(8, dtype=complex)
    axes = taste_axes()
    flips = taste_flip_generators()
    future_candidate = load_json(FUTURE_TRANSPORT_CERT)
    future_validation = validate_future_transport(future_candidate)
    future_presence = {name: (ROOT / rel).exists() for name, rel in FUTURE_REOPEN_FILES.items()}

    traces = [float(np.trace(axis).real) for axis in axes]
    source_axis_overlaps = [normalized_overlap(identity, axis) for axis in axes]
    source_projection = projection_norm(identity, axes)
    relative_source_projection = source_projection / norm(identity)
    central_commutators = [float(np.max(np.abs(identity @ axis - axis @ identity))) for axis in axes]
    flip_sign_errors = []
    flip_identity_errors = []
    for i, flip in enumerate(flips):
        flip_identity_errors.append(float(np.max(np.abs(conjugation_action(flip, identity) - identity))))
        flip_sign_errors.append(float(np.max(np.abs(conjugation_action(flip, axes[i]) + axes[i]))))
    identity_spectrum = eig_signature(identity)
    axis_spectra = [eig_signature(axis) for axis in axes]

    source_is_uniform_mass = (
        "same uniform additive lattice scalar source s entering m_bare + s"
        in texts["production_harness"]
        or "m_bare + s" in texts["production_harness"]
    )
    target_axes_loaded = (
        "H(phi) = sum_i phi_i S_i" in texts["taste_scalar_isotropy"]
        and "orthogonal taste directions" in texts["taste_scalar_isotropy"]
    )
    portfolio_text_lower = texts["candidate_portfolio_note"].lower()
    current_portfolio_selects_transport = (
        "source-coordinate transport" in portfolio_text_lower
        and "uniform mass source" in portfolio_text_lower
    )
    taste_parent_blocks_shortcut = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in parent_statuses["taste_condensate_oh_bridge"]
        and parents["taste_condensate_oh_bridge"].get("proposal_allowed") is False
        and parents["taste_condensate_oh_bridge"].get("taste_condensate_oh_bridge_audit_passed") is True
    )
    automorphism_parent_blocks_finite_orbit = (
        "Cl3 automorphism data not source-Higgs identity"
        in parent_statuses["cl3_automorphism_source_identity"]
        and parents["cl3_automorphism_source_identity"].get("proposal_allowed") is False
    )
    source_unit_parent_blocks_kappa_one = (
        parents["cl3_source_unit"].get("proposal_allowed") is False
    )
    lsz_parent_blocks_source_only = (
        parents["source_to_higgs_lsz"].get("proposal_allowed") is False
        and parents["source_functional_lsz"].get("proposal_allowed") is False
    )
    canonical_parent_blocks_oh = (
        parents["canonical_oh_premise_stretch"].get("proposal_allowed") is False
        and parents["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed") is True
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    source_pattern_support_not_closure = (
        parents["source_sector_pattern_transfer"].get("bounded_support_passed") is True
        and parents["source_sector_pattern_transfer"].get("direct_closure_available") is False
    )
    negative_review_preserves_reopen = (
        parents["negative_route_applicability_review"].get("future_reopen_paths_preserved") is True
        and parents["negative_route_applicability_review"].get("no_retained_negative_overclaim") is True
    )
    identity_fixed_by_unit_preserving_maps = (
        all(err < 1.0e-14 for err in central_commutators)
        and len(set(identity_spectrum)) == 1
        and all(spectrum != identity_spectrum for spectrum in axis_spectra)
    )
    trace_spectrum_transport_impossible = (
        np.trace(identity).real == 8.0
        and all(abs(trace) < 1.0e-14 for trace in traces)
        and all(axis_spectrum.count(-1.0) == 4 and axis_spectrum.count(1.0) == 4 for axis_spectrum in axis_spectra)
    )
    linear_projection_zero = (
        all(abs(overlap) < 1.0e-14 for overlap in source_axis_overlaps)
        and abs(relative_source_projection) < 1.0e-14
    )
    equivariant_scalar_to_vector_tangent_zero = (
        all(err < 1.0e-14 for err in flip_identity_errors)
        and all(err < 1.0e-14 for err in flip_sign_errors)
    )
    hypothetical_non_equivariant_map_not_authority = not future_validation["present"]
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("pr230-source-is-uniform-additive-mass", source_is_uniform_mass, "m_bare+s")
    report("taste-axis-target-loaded", target_axes_loaded, TEXTS["taste_scalar_isotropy"])
    report("portfolio-selects-source-coordinate-lane", current_portfolio_selects_transport, TEXTS["candidate_portfolio_note"])
    report("taste-parent-blocks-current-shortcut", taste_parent_blocks_shortcut, parent_statuses["taste_condensate_oh_bridge"])
    report("automorphism-parent-blocks-finite-orbit", automorphism_parent_blocks_finite_orbit, parent_statuses["cl3_automorphism_source_identity"])
    report("source-unit-parent-blocks-kappa-one", source_unit_parent_blocks_kappa_one, parent_statuses["cl3_source_unit"])
    report("source-lsz-parents-block-source-only", lsz_parent_blocks_source_only, "source-to-Higgs and source-functional LSZ gates remain open")
    report("canonical-oh-parent-blocks-current-oh", canonical_parent_blocks_oh, parent_statuses["canonical_oh_premise_stretch"])
    report("source-pattern-transfer-support-not-closure", source_pattern_support_not_closure, parent_statuses["source_sector_pattern_transfer"])
    report("negative-review-preserves-reopen", negative_review_preserves_reopen, parent_statuses["negative_route_applicability_review"])
    report("unit-preserving-maps-fix-identity-source", identity_fixed_by_unit_preserving_maps, f"I spectrum={identity_spectrum[:2]}... axis spectrum={axis_spectra[0]}")
    report("trace-spectrum-transport-impossible", trace_spectrum_transport_impossible, f"Tr(I)=8 Tr(S_i)={traces}")
    report("hilbert-schmidt-projection-zero", linear_projection_zero, f"overlaps={source_axis_overlaps} rel_projection={relative_source_projection:.3e}")
    report("equivariant-scalar-to-vector-tangent-zero", equivariant_scalar_to_vector_tangent_zero, "taste flips fix I and send S_i -> -S_i")
    report("future-transport-certificate-absent", not future_validation["present"], str(FUTURE_TRANSPORT_CERT.relative_to(ROOT)))
    report("non-equivariant-map-would-be-new-authority", hypothetical_non_equivariant_map_not_authority, "axis choice/Jacobian not certified")
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    exact_negative_boundary_passed = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed
        and source_is_uniform_mass
        and target_axes_loaded
        and current_portfolio_selects_transport
        and taste_parent_blocks_shortcut
        and automorphism_parent_blocks_finite_orbit
        and source_unit_parent_blocks_kappa_one
        and lsz_parent_blocks_source_only
        and canonical_parent_blocks_oh
        and source_pattern_support_not_closure
        and negative_review_preserves_reopen
        and identity_fixed_by_unit_preserving_maps
        and trace_spectrum_transport_impossible
        and linear_projection_zero
        and equivariant_scalar_to_vector_tangent_zero
        and hypothetical_non_equivariant_map_not_authority
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / source-coordinate transport not derivable from current PR230 surface"
        ),
        "conditional_surface_status": (
            "The route can reopen with a non-shortcut same-surface transport "
            "certificate, a certified symmetry-breaking tangent/axis, production "
            "C_sH/C_HH rows for a canonical O_H, or an equivalent neutral "
            "primitive/rank-one theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The PR230 source is the central taste-singlet identity direction, "
            "while the Higgs/taste axes are trace-zero sign-vector directions. "
            "Current unit-preserving, trace-preserving, and taste-equivariant "
            "maps cannot transport I_8 into S_i; a non-equivariant map would be "
            "a new uncertified source choice."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "source_coordinate_transport_completion_passed": exact_negative_boundary_passed,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "future_transport_certificate": str(FUTURE_TRANSPORT_CERT.relative_to(ROOT)),
        "future_transport_certificate_present": future_validation["present"],
        "future_transport_certificate_valid": future_validation["valid"],
        "future_transport_certificate_validation": future_validation,
        "future_reopen_file_presence": future_presence,
        "algebra": {
            "source_operator": "I_8 uniform additive scalar mass source",
            "target_operators": "S_i = sigma_x on taste tensor factor i",
            "Tr_I": float(np.trace(identity).real),
            "Tr_S_i": traces,
            "identity_spectrum": identity_spectrum,
            "taste_axis_spectra": axis_spectra,
            "source_axis_overlaps": source_axis_overlaps,
            "source_projection_norm_onto_taste_axis_span": source_projection,
            "source_relative_projection_onto_taste_axis_span": relative_source_projection,
            "flip_identity_errors": flip_identity_errors,
            "flip_sign_errors_for_target_axes": flip_sign_errors,
        },
        "rejected_current_surface_maps": [
            {
                "map_class": "unit-preserving algebra automorphism",
                "rejection": "unital algebra maps send identity to identity, not to trace-zero S_i",
            },
            {
                "map_class": "unitary or similarity transport",
                "rejection": "trace and spectrum are preserved; I_8 and S_i have different trace and spectrum",
            },
            {
                "map_class": "linear Hilbert-Schmidt projection",
                "rejection": "I_8 has zero projection onto span{S_i}",
            },
            {
                "map_class": "taste-equivariant scalar-to-vector source map",
                "rejection": "taste flips fix the scalar source and negate target axes, forcing zero tangent",
            },
            {
                "map_class": "non-equivariant axis selection",
                "rejection": "would introduce a new source-axis/Jacobian certificate, currently absent",
            },
        ],
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not rule out future same-surface source-coordinate transport after a new certificate",
            "does not demote the retained/conditional Higgs/taste structural stack",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1 or choose a taste axis by fiat",
        ],
        "exact_next_action": (
            "Treat the source-coordinate lane as closed on the current surface. "
            "Move next to the action-first O_H/C_sH/C_HH route or to a genuine "
            "neutral primitive/rank-one theorem unless a new transport "
            "certificate appears."
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
