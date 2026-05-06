#!/usr/bin/env python3
"""
PR #230 Z3-triplet positive-cone support certificate.

The conditional Z3 primitive theorem left H2 open: the three bilinear channels
must sit in one positive cone with nonzero equal-magnitude support.  This
runner proves the narrow same-surface algebraic part of H2 for the PR230 taste
triplet.

For the trace-zero taste axes S_i, the projectors Q_i^+=(I+S_i)/2 are positive
semidefinite, nonzero, equal-rank/equal-norm, and cycled by the same tensor
cycle U that supplied H1.  This is an exact cone-support artifact.  It is not
a physical neutral transfer, not a lazy/self-edge dynamics certificate, and
not a canonical-Higgs/source-overlap certificate.
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
    / "yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
)

TEXTS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
}

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_triplet_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "z3_lazy_transfer_promotion": (
        "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
    ),
    "neutral_primitive_route": (
        "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def taste_axes() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [kron3(sx, i2, i2), kron3(i2, sx, i2), kron3(i2, i2, sx)]


def tensor_cycle_operator() -> np.ndarray:
    """Unitary permutation U: |a,b,c> -> |c,a,b> on (C^2)^3."""

    out = np.zeros((8, 8), dtype=complex)
    for index in range(8):
        a = (index >> 2) & 1
        b = (index >> 1) & 1
        c = index & 1
        target = (c << 2) | (a << 1) | b
        out[target, index] = 1.0
    return out


def projector(axis: np.ndarray, sign: int = 1) -> np.ndarray:
    return 0.5 * (np.eye(8, dtype=complex) + sign * axis)


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def hs_norm(a: np.ndarray) -> float:
    return math.sqrt(max(float(hs_inner(a, a).real), 0.0))


def eigvals(matrix: np.ndarray) -> list[float]:
    return [float(round(value.real, 12)) for value in np.linalg.eigvalsh(matrix)]


def find_projector_image(matrix: np.ndarray, rows: list[np.ndarray]) -> int | None:
    for i, row in enumerate(rows):
        if float(np.max(np.abs(matrix - row))) < 1.0e-14:
            return i
    return None


def strict_future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "uses_reduced_pilots_as_production_evidence": False,
        "treats_positive_projector_cone_as_physical_transfer": False,
        "treats_symmetry_automorphism_as_dynamics": False,
        "sets_source_higgs_overlap_to_one": False,
        "sets_kappa_s_c2_or_zmatch_to_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3-triplet positive-cone support certificate")
    print("=" * 72)

    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    certs = {name: load_rel(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = strict_future_presence()

    identity = np.eye(8, dtype=complex)
    axes = taste_axes()
    cycle = tensor_cycle_operator()
    q_plus = [projector(axis, 1) for axis in axes]
    q_minus = [projector(axis, -1) for axis in axes]

    plus_hermitian_errors = [float(np.max(np.abs(q - q.conj().T))) for q in q_plus]
    plus_idempotent_errors = [float(np.max(np.abs(q @ q - q))) for q in q_plus]
    plus_eigs = [eigvals(q) for q in q_plus]
    plus_traces = [float(np.trace(q).real) for q in q_plus]
    plus_ranks = [int(np.linalg.matrix_rank(q, tol=1.0e-12)) for q in q_plus]
    plus_hs_norms = [hs_norm(q) for q in q_plus]
    plus_cycle_images = [
        find_projector_image(cycle @ q @ cycle.conj().T, q_plus) for q in q_plus
    ]
    minus_cycle_images = [
        find_projector_image(cycle @ q @ cycle.conj().T, q_minus) for q in q_minus
    ]
    plus_axis_reconstruction_errors = [
        float(np.max(np.abs((2.0 * q_plus[i] - identity) - axes[i]))) for i in range(3)
    ]
    axis_norms = [hs_norm(axis) for axis in axes]
    axis_traces = [float(np.trace(axis).real) for axis in axes]
    positive_cone_barycenter = sum(q_plus) / 3.0
    barycenter_eigs = eigvals(positive_cone_barycenter)
    barycenter_positive = min(barycenter_eigs) >= -1.0e-12
    z3_uniform_support = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0]

    taste_text_support = (
        "H(phi) = sum_i phi_i S_i" in texts["taste_scalar_isotropy"]
        and "S_i^2 = I" in texts["taste_scalar_isotropy"]
        and "orthogonal taste directions" in texts["taste_scalar_isotropy"]
    )
    substrate_text_support = (
        "physical local algebra is `Cl(3)`" in texts["minimal_axioms"]
        and "`Z^3`" in texts["minimal_axioms"]
        and "staggered-Dirac partition" in texts["minimal_axioms"]
    )
    h1_loaded = (
        "same-surface Z3 taste-triplet artifact" in statuses["same_surface_z3_taste_triplet"]
        and certs["same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certs["same_surface_z3_taste_triplet"].get("pr230_closure_authorized")
        is False
    )
    conditional_parent_waits_for_h2 = (
        "Z3-triplet primitive-cone theorem"
        in statuses["z3_triplet_conditional_primitive"]
        and "H2"
        in certs["z3_triplet_conditional_primitive"].get(
            "remaining_unsupplied_conditional_premises", []
        )
        and certs["z3_triplet_conditional_primitive"].get("proposal_allowed") is False
    )
    h3_still_absent = (
        "Z3 lazy-transfer promotion not derivable"
        in statuses["z3_lazy_transfer_promotion"]
        and certs["z3_lazy_transfer_promotion"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and futures["same_surface_neutral_transfer"] is False
    )
    neutral_route_still_open = (
        "neutral primitive-rank-one route not complete"
        in statuses["neutral_primitive_route"]
        and certs["neutral_primitive_route"].get("proposal_allowed") is False
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    plus_projectors_psd = all(
        min(eigs) >= -1.0e-12 and max(eigs) <= 1.0 + 1.0e-12 for eigs in plus_eigs
    )
    equal_nonzero_support = (
        plus_traces == [4.0, 4.0, 4.0]
        and plus_ranks == [4, 4, 4]
        and all(abs(value - 2.0) < 1.0e-12 for value in plus_hs_norms)
        and all(abs(value - math.sqrt(8.0)) < 1.0e-12 for value in axis_norms)
        and all(abs(value) < 1.0e-12 for value in axis_traces)
    )
    z3_cycles_cone_generators = plus_cycle_images == [1, 2, 0] and minus_cycle_images == [1, 2, 0]
    cone_support_passed = (
        not missing_texts
        and not missing_parents
        and not proposal_allowed_parents
        and taste_text_support
        and substrate_text_support
        and h1_loaded
        and conditional_parent_waits_for_h2
        and max(plus_hermitian_errors) < 1.0e-14
        and max(plus_idempotent_errors) < 1.0e-14
        and plus_projectors_psd
        and equal_nonzero_support
        and z3_cycles_cone_generators
        and max(plus_axis_reconstruction_errors) < 1.0e-14
        and barycenter_positive
        and h3_still_absent
        and neutral_route_still_open
        and aggregate_still_open
        and all(value is False for value in forbidden_firewall().values())
    )

    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("taste-theorem-support-loaded", taste_text_support, TEXTS["taste_scalar_isotropy"])
    report("substrate-support-loaded", substrate_text_support, TEXTS["minimal_axioms"])
    report("h1-same-surface-z3-triplet-loaded", h1_loaded, statuses["same_surface_z3_taste_triplet"])
    report("conditional-parent-waits-for-h2", conditional_parent_waits_for_h2, statuses["z3_triplet_conditional_primitive"])
    report("projectors-hermitian", max(plus_hermitian_errors) < 1.0e-14, str(plus_hermitian_errors))
    report("projectors-idempotent", max(plus_idempotent_errors) < 1.0e-14, str(plus_idempotent_errors))
    report("projectors-positive-semidefinite", plus_projectors_psd, str(plus_eigs))
    report("equal-nonzero-cone-support", equal_nonzero_support, f"traces={plus_traces} ranks={plus_ranks} norms={plus_hs_norms}")
    report("z3-cycles-positive-cone-generators", z3_cycles_cone_generators, f"plus={plus_cycle_images} minus={minus_cycle_images}")
    report("axes-reconstruct-from-positive-projectors", max(plus_axis_reconstruction_errors) < 1.0e-14, str(plus_axis_reconstruction_errors))
    report("uniform-barycenter-positive", barycenter_positive, str(barycenter_eigs))
    report("h3-physical-transfer-still-absent", h3_still_absent, statuses["z3_lazy_transfer_promotion"])
    report("neutral-route-still-open", neutral_route_still_open, statuses["neutral_primitive_route"])
    report("aggregate-still-open", aggregate_still_open, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", all(value is False for value in forbidden_firewall().values()), str(forbidden_firewall()))
    report("h2-positive-cone-support-passed", cone_support_passed, "algebraic H2 support only")

    result = {
        "actual_current_surface_status": (
            "exact-support / Z3-triplet positive-cone H2 support; physical "
            "neutral transfer still absent"
        ),
        "conditional_surface_status": (
            "This supplies the algebraic H2 cone-support premise for the "
            "conditional Z3 primitive route. H3 and H4 remain absent: no "
            "same-surface physical lazy transfer/off-diagonal generator and no "
            "coupling to the PR230 source/canonical-Higgs sector are derived."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The certificate proves equal nonzero PSD cone support for the "
            "same-surface triplet, but does not instantiate physical dynamics, "
            "canonical O_H, source-Higgs rows, or retained-route closure."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_triplet_positive_cone_h2_support_passed": cone_support_passed,
        "pr230_closure_authorized": False,
        "supplies_conditional_premises": {
            "H1_same_surface_z3_cyclic_action_on_triplet": h1_loaded,
            "H2_positive_cone_equal_magnitude_support": cone_support_passed,
            "H3_lazy_positive_physical_transfer": False,
            "H4_transfer_couples_to_pr230_source_canonical_higgs_sector": False,
        },
        "operator_witness": {
            "axis_labels": ["S0=sigma_xII", "S1=Isigma_xI", "S2=IIsigma_x"],
            "positive_projectors": "Q_i_plus=(I+S_i)/2",
            "negative_projectors": "Q_i_minus=(I-S_i)/2",
            "projector_traces": plus_traces,
            "projector_ranks": plus_ranks,
            "projector_hilbert_schmidt_norms": plus_hs_norms,
            "projector_eigenvalues": plus_eigs,
            "axis_traces": axis_traces,
            "axis_hilbert_schmidt_norms": axis_norms,
            "z3_cycle_images_Q_plus": plus_cycle_images,
            "z3_cycle_images_Q_minus": minus_cycle_images,
            "axis_reconstruction_max_errors": plus_axis_reconstruction_errors,
            "uniform_positive_cone_support": z3_uniform_support,
            "positive_cone_barycenter_eigenvalues": barycenter_eigs,
        },
        "remaining_unsupplied_conditional_premises": ["H3", "H4"],
        "strict_future_artifact_presence": futures,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write a neutral primitive-cone certificate",
            "does not treat PSD cone support as a physical transfer operator",
            "does not treat symmetry averaging as dynamics",
            "does not identify O_s, O_sp, or taste projectors with canonical O_H",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, or reduced pilots",
            "does not set source-Higgs overlap, kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "Derive or measure H3/H4: a same-surface physical lazy neutral "
            "transfer/off-diagonal generator coupled to the PR230 source or "
            "canonical-Higgs sector. Otherwise continue with O_H/C_sH/C_HH, "
            "W/Z response, Schur rows, or completed row production."
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
