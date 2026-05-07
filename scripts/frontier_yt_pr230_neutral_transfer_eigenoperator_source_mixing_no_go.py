#!/usr/bin/env python3
"""
PR #230 neutral transfer/eigenoperator source-mixing no-go.

This runner attacks the same-surface neutral transfer/eigenoperator route from
the current Cl(3)/Z3 taste primitives.  The exact obstruction is not that the
Z3 triplet algebra is empty: it has a cyclic triplet, a positive-cone support
row, and a conditional primitive lazy transfer.  The obstruction is that the
current same-surface data do not supply the source-to-radial off-diagonal
transfer/action entry or an equivalent pole-overlap row.

The witness has two parts:

1. In the current symmetric taste-polynomial Z3-invariant neutral sector, the
   source identity and the taste-radial axis are orthogonal invariant basis
   vectors.  Z3/eigenoperator data alone allow both zero and nonzero
   source-radial mixing.  The mixing coefficient is an independent
   action/transfer datum.
2. The lazy triplet transfer is primitive on the triplet, but the extension
   that leaves the PR230 source block isolated is reducible.  A primitive
   full source-plus-triplet transfer requires an added source-triplet coupling
   eta; eta is not derived by the current artifacts.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json"
)

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_positive_cone_support": (
        "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
    ),
    "z3_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "z3_lazy_transfer_promotion": (
        "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
    ),
    "z3_lazy_selector_no_go": "outputs/yt_pr230_z3_lazy_selector_no_go_2026-05-06.json",
    "neutral_multiplicity_candidate": (
        "outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json"
    ),
    "source_coordinate_transport": (
        "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
    ),
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_pole_row_contract": (
        "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json"
    ),
    "os_transfer_kernel_gate": (
        "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_ARTIFACTS = {
    "same_surface_neutral_transfer_operator": (
        "outputs/yt_pr230_same_surface_neutral_transfer_operator_2026-05-06.json"
    ),
    "neutral_offdiagonal_generator_certificate": (
        "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json"
    ),
    "neutral_primitive_cone_certificate": (
        "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
    ),
    "canonical_oh_certificate": (
        "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json"
    ),
    "source_higgs_measurement_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "accepted_same_source_ew_action": (
        "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json"
    ),
}

PASS_COUNT = 0
FAIL_COUNT = 0

FMatrix = list[list[Fraction]]


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


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def taste_axes() -> list[np.ndarray]:
    i2 = np.eye(2, dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    return [kron3(sx, i2, i2), kron3(i2, sx, i2), kron3(i2, i2, sx)]


def tensor_cycle_operator() -> np.ndarray:
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


def hs_norm(a: np.ndarray) -> float:
    return math.sqrt(max(float(hs_inner(a, a).real), 0.0))


def normalize(a: np.ndarray) -> np.ndarray:
    return a / hs_norm(a)


def invariant_basis() -> dict[str, np.ndarray]:
    identity = np.eye(8, dtype=complex)
    s0, s1, s2 = taste_axes()
    return {
        "source_identity": normalize(identity),
        "degree1_taste_radial": normalize(s0 + s1 + s2),
        "degree2_taste_radial": normalize(s0 @ s1 + s1 @ s2 + s2 @ s0),
        "degree3_taste_radial": normalize(s0 @ s1 @ s2),
    }


def max_abs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def matmul(a: FMatrix, b: FMatrix) -> FMatrix:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def eye(n: int) -> FMatrix:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def matpow(a: FMatrix, power: int) -> FMatrix:
    result = eye(len(a))
    for _ in range(power):
        result = matmul(result, a)
    return result


def all_positive(a: FMatrix) -> bool:
    return all(value > 0 for row in a for value in row)


def primitive_power(a: FMatrix, max_power: int = 16) -> int | None:
    for power in range(1, max_power + 1):
        if all_positive(matpow(a, power)):
            return power
    return None


def to_strings(a: FMatrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in a]


def cyclic_z3_triplet() -> FMatrix:
    return [
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]


def lazy_triplet() -> FMatrix:
    p = cyclic_z3_triplet()
    return [
        [
            Fraction(1, 2) * (Fraction(1 if i == j else 0) + p[i][j])
            for j in range(3)
        ]
        for i in range(3)
    ]


def source_plus_triplet_transfer(eta: Fraction) -> FMatrix:
    """Z3-compatible row-stochastic transfer on source plus triplet."""

    lazy = lazy_triplet()
    rows: FMatrix = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    rows[0][0] = Fraction(1) - 3 * eta
    for j in range(1, 4):
        rows[0][j] = eta
    for i in range(1, 4):
        rows[i][0] = eta
        for j in range(1, 4):
            rows[i][j] = (Fraction(1) - eta) * lazy[i - 1][j - 1]
    return rows


def row_sums(a: FMatrix) -> list[Fraction]:
    return [sum(row) for row in a]


def symmetric_kernel(eta: Fraction) -> list[list[Fraction]]:
    # Positive self-adjoint source/radial action Hessian witness.
    return [[Fraction(2), eta], [eta, Fraction(3)]]


def determinant_2x2(a: list[list[Fraction]]) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def eigen_residual_of_radial(kernel: list[list[Fraction]]) -> Fraction:
    # Residual of e_radial as an eigenvector in the source-radial 2x2 block.
    # K * [0, 1]^T has source component K_01; this must vanish for exact
    # radial eigenoperator status.
    return kernel[0][1]


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_H_unit": False,
        "uses_yt_ward_identity": False,
        "uses_observed_top_mass_or_yukawa": False,
        "uses_observed_wz_or_g2_values": False,
        "uses_alpha_lm_plaquette_u0": False,
        "uses_reduced_pilots_as_proof": False,
        "sets_kappa_s_to_one": False,
        "sets_c2_or_zmatch_to_one": False,
        "renames_C_sx_C_xx_as_C_sH_C_HH": False,
        "imports_entropy_gap_or_markov_laziness_as_physics": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 neutral transfer/eigenoperator source-mixing no-go")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()

    basis = invariant_basis()
    basis_names = list(basis)
    gram = [
        [float(hs_inner(basis[a], basis[b]).real) for b in basis_names]
        for a in basis_names
    ]
    max_orthonormal_error = max(
        abs(gram[i][j] - (1.0 if i == j else 0.0))
        for i in range(len(gram))
        for j in range(len(gram))
    )
    cycle = tensor_cycle_operator()
    cycle_errors = {
        name: max_abs(cycle @ op @ cycle.conj().T - op)
        for name, op in basis.items()
    }
    source_radial_overlap = float(
        hs_inner(basis["source_identity"], basis["degree1_taste_radial"]).real
    )

    diagonal_kernel = symmetric_kernel(Fraction(0))
    mixed_kernel = symmetric_kernel(Fraction(1, 2))
    diagonal_det = determinant_2x2(diagonal_kernel)
    mixed_det = determinant_2x2(mixed_kernel)
    diagonal_radial_residual = eigen_residual_of_radial(diagonal_kernel)
    mixed_radial_residual = eigen_residual_of_radial(mixed_kernel)

    source_radii = []
    for eta in (Fraction(0), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
        transfer = source_plus_triplet_transfer(eta)
        source_radii.append(
            {
                "eta": str(eta),
                "row_sums": [str(value) for value in row_sums(transfer)],
                "primitive_power": primitive_power(transfer),
                "source_to_each_triplet_weight": str(eta),
                "matrix": to_strings(transfer),
            }
        )

    lazy = lazy_triplet()
    lazy_triplet_primitive_power = primitive_power(lazy)
    source_isolated_transfer = source_plus_triplet_transfer(Fraction(0))
    source_isolated_primitive_power = primitive_power(source_isolated_transfer)
    eta_positive_transfer = source_plus_triplet_transfer(Fraction(1, 10))
    eta_positive_primitive_power = primitive_power(eta_positive_transfer)

    current_transfer_artifact_absent = not any(
        futures[name]
        for name in (
            "same_surface_neutral_transfer_operator",
            "neutral_offdiagonal_generator_certificate",
            "neutral_primitive_cone_certificate",
        )
    )
    oh_rows_absent = not any(
        futures[name]
        for name in ("canonical_oh_certificate", "source_higgs_measurement_rows")
    )
    accepted_ew_action_absent = not futures["accepted_same_source_ew_action"]
    clean_firewall = all(value is False for value in firewall.values())

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("invariant-sector-orthonormal", max_orthonormal_error < 1.0e-12, f"max_error={max_orthonormal_error:.3e}")
    report("z3-fixes-four-invariant-basis-vectors", max(cycle_errors.values()) < 1.0e-12, str(cycle_errors))
    report("source-radial-orthogonal", abs(source_radial_overlap) < 1.0e-12, f"overlap={source_radial_overlap:.3e}")
    report("diagonal-kernel-positive", diagonal_det > 0, f"det={diagonal_det}")
    report("diagonal-kernel-radial-eigenoperator", diagonal_radial_residual == 0, f"residual={diagonal_radial_residual}")
    report("diagonal-kernel-no-source-radial-bridge", diagonal_kernel[0][1] == 0, f"K_sr={diagonal_kernel[0][1]}")
    report("mixed-kernel-positive", mixed_det > 0, f"det={mixed_det}")
    report("mixed-kernel-has-arbitrary-source-radial-entry", mixed_kernel[0][1] != 0, f"K_sr={mixed_kernel[0][1]}")
    report("mixed-kernel-radial-not-eigenoperator", mixed_radial_residual != 0, f"residual={mixed_radial_residual}")
    report("lazy-triplet-primitive", lazy_triplet_primitive_power is not None, f"power={lazy_triplet_primitive_power}")
    report("source-plus-lazy-with-eta-zero-reducible", source_isolated_primitive_power is None, "source block isolated")
    report("source-plus-lazy-with-eta-positive-primitive", eta_positive_primitive_power is not None, f"power={eta_positive_primitive_power}")
    report("eta-not-supplied-by-current-artifacts", current_transfer_artifact_absent, str(futures))
    report("canonical-oh-and-source-higgs-rows-absent", oh_rows_absent, str(futures))
    report("accepted-ew-action-absent", accepted_ew_action_absent, str(futures))
    report("forbidden-import-firewall-clean", clean_firewall, str(firewall))

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / current same-surface Z3 eigenoperator "
            "data do not certify a physical neutral scalar transfer or O_H bridge"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface neutral action/transfer "
            "supplies the source-radial off-diagonal generator or measured "
            "C_spH/C_HH pole rows with canonical LSZ/FV/IR authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The exact Cl(3)/Z3 invariant sector contains an orthogonal source "
            "identity and taste-radial axis.  Symmetry/eigenoperator data allow "
            "both a diagonal positive kernel with zero source-radial bridge and "
            "a mixed positive kernel with arbitrary source-radial bridge.  "
            "The lazy triplet transfer is primitive only inside the triplet; "
            "the source-plus-triplet transfer is reducible unless a new eta "
            "coupling is supplied.  Current PR230 artifacts supply no physical "
            "neutral transfer/operator, off-diagonal generator, canonical O_H "
            "certificate, source-Higgs pole rows, or accepted same-source EW action."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "invariant_operator_basis": {
            "basis": basis_names,
            "gram": gram,
            "max_orthonormal_error": max_orthonormal_error,
            "z3_cycle_errors": cycle_errors,
            "source_radial_hilbert_schmidt_overlap": source_radial_overlap,
            "z3_trivial_sector_dimension_exhibited": 4,
        },
        "eigenoperator_fork": {
            "diagonal_positive_kernel": {
                "basis": ["source_identity", "degree1_taste_radial"],
                "matrix": [[str(value) for value in row] for row in diagonal_kernel],
                "determinant": str(diagonal_det),
                "radial_is_eigenoperator": diagonal_radial_residual == 0,
                "source_radial_bridge_entry": str(diagonal_kernel[0][1]),
                "bridge_present": False,
            },
            "mixed_positive_kernel": {
                "basis": ["source_identity", "degree1_taste_radial"],
                "matrix": [[str(value) for value in row] for row in mixed_kernel],
                "determinant": str(mixed_det),
                "radial_is_eigenoperator": mixed_radial_residual == 0,
                "source_radial_bridge_entry": str(mixed_kernel[0][1]),
                "bridge_present": True,
            },
            "conclusion": (
                "Eigenoperator purity and source-radial bridge coupling are not "
                "forced by current same-surface Z3 data.  The off-diagonal "
                "source-radial entry is an independent transfer/action datum."
            ),
        },
        "primitive_transfer_witness": {
            "triplet_lazy_transfer": to_strings(lazy),
            "triplet_lazy_primitive_power": lazy_triplet_primitive_power,
            "source_plus_triplet_eta_rows": source_radii,
            "eta_zero_reducible": source_isolated_primitive_power is None,
            "eta_positive_example_primitive_power": eta_positive_primitive_power,
            "conclusion": (
                "Triplet primitivity does not imply full source-Higgs primitivity. "
                "A source-triplet eta coupling is needed and is not selected by "
                "the current same-surface artifacts."
            ),
        },
        "current_missing_artifacts": {
            **futures,
            "physical_transfer_or_offdiagonal_generator_absent": current_transfer_artifact_absent,
            "canonical_oh_or_source_higgs_rows_absent": oh_rows_absent,
            "accepted_same_source_ew_action_absent": accepted_ew_action_absent,
        },
        "parent_statuses": statuses,
        "forbidden_import_firewall": {"passed": clean_firewall, **firewall},
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not identify taste-radial x with canonical O_H",
            "does not rename C_sx/C_xx as C_sH/C_HH",
            "does not set kappa_s, c2, Z_match, or g2 to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not import entropy, spectral gap, or Markov laziness as physical transfer",
        ],
        "verification": {
            "pass_count": PASS_COUNT,
            "fail_count": FAIL_COUNT,
        },
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
