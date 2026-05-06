#!/usr/bin/env python3
"""
PR #230 same-surface Z3 taste-triplet artifact.

This runner attacks the first missing premise in the Z3 primitive route:
whether the PR230 Cl(3)/Z^3 taste surface contains an exact cyclic action on
the three trace-zero taste-scalar axes.

Result:
    Yes, as an exact same-surface symmetry artifact.  The tensor-factor cycle
    U sends S_0 -> S_1 -> S_2 -> S_0 and fixes the source identity I_8.

Boundary:
    This is not yet a physical neutral transfer operator.  A symmetry
    automorphism can instantiate the Z3 triplet basis, but it does not supply
    the lazy positive transfer, same-source action, off-diagonal generator,
    canonical O_H identity, or C_sH/C_HH rows required for PR230 closure.
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
    / "yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
)

TEXTS = {
    "taste_scalar_isotropy": "docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md",
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
}

PARENTS = {
    "z3_triplet_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "source_coordinate_transport": (
        "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
    ),
    "kinetic_taste_mixing": (
        "outputs/yt_pr230_kinetic_taste_mixing_bridge_attempt_2026-05-06.json"
    ),
    "one_higgs_taste_axis": (
        "outputs/yt_pr230_one_higgs_taste_axis_completeness_attempt_2026-05-06.json"
    ),
    "neutral_primitive_route": (
        "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def hs_inner(a: np.ndarray, b: np.ndarray) -> complex:
    return complex(np.trace(a.conj().T @ b))


def normalized_overlap(a: np.ndarray, b: np.ndarray) -> float:
    denom = math.sqrt(max(float(hs_inner(a, a).real * hs_inner(b, b).real), 0.0))
    if denom <= 1.0e-30:
        return float("nan")
    return float((hs_inner(a, b) / denom).real)


def find_axis_image(matrix: np.ndarray, axes: list[np.ndarray]) -> int | None:
    for i, axis in enumerate(axes):
        if float(np.max(np.abs(matrix - axis))) < 1.0e-14:
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
        "treats_symmetry_automorphism_as_physical_transfer": False,
        "sets_source_higgs_overlap_to_one": False,
        "sets_kappa_s_c2_or_zmatch_to_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 same-surface Z3 taste-triplet artifact")
    print("=" * 72)

    texts = {name: read_rel(rel) for name, rel in TEXTS.items()}
    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    future_presence = strict_future_presence()

    identity = np.eye(8, dtype=complex)
    axes = taste_axes()
    cycle = tensor_cycle_operator()
    cycle2 = cycle @ cycle
    cycle3 = cycle2 @ cycle
    unitarity_error = float(np.max(np.abs(cycle.conj().T @ cycle - identity)))
    cycle3_error = float(np.max(np.abs(cycle3 - identity)))
    axis_images = []
    for axis in axes:
        image = cycle @ axis @ cycle.conj().T
        axis_images.append(find_axis_image(image, axes))

    traces = [float(np.trace(axis).real) for axis in axes]
    squares_error = [float(np.max(np.abs(axis @ axis - identity))) for axis in axes]
    hs_gram = [
        [float(hs_inner(axes[i], axes[j]).real) for j in range(3)]
        for i in range(3)
    ]
    source_fixed_error = float(np.max(np.abs(cycle @ identity @ cycle.conj().T - identity)))
    source_axis_overlaps = [normalized_overlap(identity, axis) for axis in axes]

    p_triplet = np.zeros((3, 3), dtype=int)
    for source_index, target_index in enumerate(axis_images):
        if target_index is not None:
            p_triplet[target_index, source_index] = 1
    p3_triplet = p_triplet @ p_triplet @ p_triplet
    pure_p_has_zero_in_all_first_six = all(
        np.any(np.linalg.matrix_power(p_triplet, power) == 0) for power in range(1, 7)
    )
    lazy = 0.5 * (np.eye(3) + p_triplet)
    lazy2 = lazy @ lazy
    lazy2_positive = bool(np.all(lazy2 > 0.0))

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
    z3_conditional_loaded = (
        "Z3-triplet primitive-cone theorem" in statuses["z3_triplet_conditional_primitive"]
        and parents["z3_triplet_conditional_primitive"].get("proposal_allowed") is False
    )
    source_transport_still_blocks = (
        "source-coordinate transport not derivable" in statuses["source_coordinate_transport"]
        and parents["source_coordinate_transport"].get("proposal_allowed") is False
    )
    kinetic_still_blocks = (
        "current staggered kinetic taste symmetry" in statuses["kinetic_taste_mixing"]
        and parents["kinetic_taste_mixing"].get("kinetic_taste_mixing_bridge_closes_pr230")
        is False
    )
    one_higgs_still_blocks = (
        "one-Higgs taste-axis completeness not derived" in statuses["one_higgs_taste_axis"]
        and parents["one_higgs_taste_axis"].get("one_higgs_taste_axis_completeness_derived")
        is False
    )
    neutral_route_open = (
        "neutral primitive-rank-one route not complete" in statuses["neutral_primitive_route"]
        and parents["neutral_primitive_route"].get("proposal_allowed") is False
    )
    aggregate_open = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    z3_same_surface_triplet_artifact_passed = (
        not missing_texts
        and not missing_parents
        and not proposal_allowed
        and taste_text_support
        and substrate_text_support
        and unitarity_error < 1.0e-14
        and cycle3_error < 1.0e-14
        and axis_images == [1, 2, 0]
        and max(abs(value) for value in traces) < 1.0e-14
        and max(squares_error) < 1.0e-14
        and source_fixed_error < 1.0e-14
        and max(abs(value) for value in source_axis_overlaps) < 1.0e-14
        and np.array_equal(p3_triplet, np.eye(3, dtype=int))
        and pure_p_has_zero_in_all_first_six
        and lazy2_positive
        and z3_conditional_loaded
        and source_transport_still_blocks
        and kinetic_still_blocks
        and one_higgs_still_blocks
        and neutral_route_open
        and aggregate_open
        and clean_firewall
    )

    physical_transfer_supplied = (
        future_presence["same_surface_neutral_transfer"]
        or future_presence["neutral_offdiagonal_generator_certificate"]
        or future_presence["neutral_primitive_cone_certificate"]
    )
    pr230_closure_authorized = (
        z3_same_surface_triplet_artifact_passed
        and physical_transfer_supplied
        and future_presence["canonical_oh_certificate"]
        and future_presence["source_higgs_rows"]
        and False
    )

    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-theorem-support-loaded", taste_text_support, TEXTS["taste_scalar_isotropy"])
    report("substrate-support-loaded", substrate_text_support, TEXTS["minimal_axioms"])
    report("cycle-unitary", unitarity_error < 1.0e-14, f"error={unitarity_error:.3e}")
    report("cycle-cubed-identity", cycle3_error < 1.0e-14, f"error={cycle3_error:.3e}")
    report("cycle-maps-taste-triplet", axis_images == [1, 2, 0], f"axis_images={axis_images}")
    report("taste-axes-trace-zero", max(abs(value) for value in traces) < 1.0e-14, str(traces))
    report("taste-axes-involutions", max(squares_error) < 1.0e-14, str(squares_error))
    report("taste-axis-gram-diagonal", hs_gram == [[8.0, 0.0, 0.0], [0.0, 8.0, 0.0], [0.0, 0.0, 8.0]], str(hs_gram))
    report("source-identity-fixed", source_fixed_error < 1.0e-14, f"error={source_fixed_error:.3e}")
    report("source-axis-overlap-zero", max(abs(value) for value in source_axis_overlaps) < 1.0e-14, str(source_axis_overlaps))
    report("triplet-permutation-cubed-identity", np.array_equal(p3_triplet, np.eye(3, dtype=int)), p_triplet.tolist())
    report("pure-cycle-not-primitive", pure_p_has_zero_in_all_first_six, "P powers keep zeros")
    report("lazy-cycle-would-be-primitive", lazy2_positive, lazy2.tolist())
    report("z3-conditional-parent-loaded", z3_conditional_loaded, statuses["z3_triplet_conditional_primitive"])
    report("source-transport-still-blocks-closure", source_transport_still_blocks, statuses["source_coordinate_transport"])
    report("kinetic-mixing-still-blocks-closure", kinetic_still_blocks, statuses["kinetic_taste_mixing"])
    report("one-higgs-axis-still-blocks-closure", one_higgs_still_blocks, statuses["one_higgs_taste_axis"])
    report("neutral-route-still-open", neutral_route_open, statuses["neutral_primitive_route"])
    report("aggregate-still-open", aggregate_open, "assembly/retained proposal_allowed false")
    report("physical-transfer-not-supplied", not physical_transfer_supplied, str(future_presence))
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))
    report("same-surface-z3-artifact-passed", z3_same_surface_triplet_artifact_passed, "H1 support for Z3 primitive route")
    report("pr230-closure-not-authorized", pr230_closure_authorized is False, "symmetry artifact is not physical transfer")

    result = {
        "actual_current_surface_status": (
            "exact-support / same-surface Z3 taste-triplet artifact; physical "
            "neutral transfer still absent"
        ),
        "conditional_surface_status": (
            "This supplies the same-surface cyclic triplet action premise for "
            "the Z3 primitive route.  It becomes primitive/rank-one support "
            "only after a same-surface lazy positive transfer or equivalent "
            "off-diagonal neutral generator is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The artifact is an exact symmetry/operator-basis certificate, not "
            "a physical PR230 transfer, canonical O_H identity, or source-Higgs "
            "row packet."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "same_surface_z3_triplet_artifact_passed": z3_same_surface_triplet_artifact_passed,
        "pr230_closure_authorized": pr230_closure_authorized,
        "supplies_conditional_premises": {
            "H1_same_surface_z3_cyclic_action_on_triplet": z3_same_surface_triplet_artifact_passed,
            "H2_positive_cone_equal_magnitude_support": False,
            "H3_lazy_positive_physical_transfer": False,
            "H4_transfer_couples_to_pr230_source_canonical_higgs_sector": False,
        },
        "operator_witness": {
            "axis_labels": ["S0=sigma_xII", "S1=Isigma_xI", "S2=IIsigma_x"],
            "axis_images_under_U_cycle": axis_images,
            "unitarity_error": unitarity_error,
            "cycle3_error": cycle3_error,
            "axis_traces": traces,
            "axis_square_errors": squares_error,
            "axis_hilbert_schmidt_gram": hs_gram,
            "source_identity_fixed_error": source_fixed_error,
            "source_axis_overlaps": source_axis_overlaps,
            "triplet_permutation_matrix": p_triplet.tolist(),
            "pure_cycle_not_primitive": pure_p_has_zero_in_all_first_six,
            "lazy_cycle_L": lazy.tolist(),
            "lazy_cycle_L2": lazy2.tolist(),
            "lazy_cycle_L2_strictly_positive": lazy2_positive,
        },
        "parent_statuses": statuses,
        "strict_future_artifact_presence": future_presence,
        "remaining_same_surface_artifacts_needed": [
            "same-surface neutral transfer operator or off-diagonal neutral generator",
            "positive/lazy aperiodic self term as physical dynamics, not only symmetry averaging",
            "strict neutral primitive-cone certificate",
            "canonical O_H identity or source-Higgs C_sH/C_HH pole rows",
            "retained-route and full-positive assembly approval",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat a symmetry automorphism as a physical transfer operator",
            "does not identify source I_8 with trace-zero taste axes",
            "does not define O_H, y_t, or y_t_bare",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set source-Higgs overlap, kappa_s, c2, or Z_match to one",
        ],
        "forbidden_firewall": forbidden_firewall(),
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
