#!/usr/bin/env python3
"""
PR #230 Z3 heat-kernel source-coupling/H4 no-go.

Blocks102-103 established that the finite C3/Z3 heat kernel is a genuine
primitive triplet semigroup, but that the current PR230 surface does not select
its physical heat time or diffusion scale.  This runner checks the remaining
H4 shortcut: can the same heat-kernel data supply the source/canonical-Higgs
coupling needed to connect the PR230 source singlet to the neutral triplet?

Verdict:
    No on the current PR230 surface.  The block-diagonal source plus triplet
    heat-kernel extension keeps all triplet heat-kernel facts but is reducible
    and has no source/triplet coupling.  A symmetric stochastic full transfer
    becomes primitive after adding a positive source-triplet coupling eta, but
    eta is independent same-surface action/transfer data.  Current PR230
    artifacts do not derive or measure eta and do not supply canonical O_H or
    C_sH/C_HH pole rows.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_z3_heat_kernel_source_coupling_no_go_2026-05-15.json"
)

PARENTS = {
    "z3_heat_kernel_attempt": (
        "outputs/yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json"
    ),
    "z3_heat_kernel_scale_selector_no_go": (
        "outputs/yt_pr230_z3_heat_kernel_scale_selector_no_go_2026-05-15.json"
    ),
    "neutral_source_mixing_no_go": (
        "outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json"
    ),
    "neutral_h3h4_aperture": (
        "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
    ),
    "same_surface_neutral_multiplicity_gate": (
        "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json"
    ),
    "post_block100_completion_reopen": (
        "outputs/yt_pr230_post_block100_completion_reopen_audit_2026-05-15.json"
    ),
    "full_positive_assembly": (
        "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
    ),
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_ARTIFACTS = {
    "same_surface_source_triplet_coupling": (
        "outputs/yt_pr230_same_surface_source_triplet_coupling_2026-05-15.json"
    ),
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
    "source_higgs_cross_rows": (
        "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json"
    ),
    "source_higgs_production_certificate": (
        "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
    ),
    "wz_response_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[float]]


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


def cyclic_z3_triplet() -> Matrix:
    return [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]


def cyclic_z3_source_plus_triplet() -> Matrix:
    # Basis: source singlet s, then triplet states 0,1,2.
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
    ]


def heat_kernel(tau: float) -> Matrix:
    e = math.exp(-3.0 * tau)
    diagonal = (1.0 + 2.0 * e) / 3.0
    offdiag = (1.0 - e) / 3.0
    return [[diagonal if i == j else offdiag for j in range(3)] for i in range(3)]


def block_diagonal_source_extension(tau: float) -> Matrix:
    k = heat_kernel(tau)
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, k[0][0], k[0][1], k[0][2]],
        [0.0, k[1][0], k[1][1], k[1][2]],
        [0.0, k[2][0], k[2][1], k[2][2]],
    ]


def coupled_source_extension(tau: float, eta: float) -> Matrix:
    """Symmetric stochastic source-triplet coupling family.

    eta is the missing source-triplet coupling.  Valid for 0 <= eta <= 1/3.
    """
    k = heat_kernel(tau)
    triplet_scale = 1.0 - eta
    return [
        [1.0 - 3.0 * eta, eta, eta, eta],
        [eta, triplet_scale * k[0][0], triplet_scale * k[0][1], triplet_scale * k[0][2]],
        [eta, triplet_scale * k[1][0], triplet_scale * k[1][1], triplet_scale * k[1][2]],
        [eta, triplet_scale * k[2][0], triplet_scale * k[2][1], triplet_scale * k[2][2]],
    ]


def transpose(a: Matrix) -> Matrix:
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def max_abs(a: Matrix, b: Matrix) -> float:
    return max(
        abs(a[i][j] - b[i][j])
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def row_sums(a: Matrix) -> list[float]:
    return [sum(row) for row in a]


def col_sums(a: Matrix) -> list[float]:
    return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]


def all_close(values: list[float], target: float, tol: float = 1.0e-12) -> bool:
    return all(abs(value - target) <= tol for value in values)


def all_positive(a: Matrix, tol: float = 0.0) -> bool:
    return all(value > tol for row in a for value in row)


def is_symmetric(a: Matrix, tol: float = 1.0e-12) -> bool:
    return max_abs(a, transpose(a)) <= tol


def commutes(a: Matrix, b: Matrix, tol: float = 1.0e-12) -> bool:
    return max_abs(matmul(a, b), matmul(b, a)) <= tol


def primitive_power(a: Matrix, max_power: int = 8) -> int | None:
    current = a
    for power in range(1, max_power + 1):
        if all_positive(current):
            return power
        current = matmul(current, a)
    return None


def matrix_summary(a: Matrix) -> dict[str, Any]:
    z3 = cyclic_z3_source_plus_triplet()
    power = primitive_power(a)
    return {
        "matrix": a,
        "row_stochastic": all_close(row_sums(a), 1.0),
        "column_stochastic": all_close(col_sums(a), 1.0),
        "symmetric": is_symmetric(a),
        "commutes_with_source_plus_triplet_z3": commutes(a, z3),
        "strictly_positive": all_positive(a),
        "primitive": power is not None,
        "primitive_power": power,
        "source_triplet_entries": [a[0][1], a[0][2], a[0][3]],
    }


def eta_rows(tau: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for eta in [0.0, 0.02, 0.05, 0.1, 0.2, 1.0 / 3.0]:
        matrix = coupled_source_extension(tau, eta)
        summary = matrix_summary(matrix)
        summary["eta"] = eta
        rows.append(summary)
    return rows


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_mass_or_yukawa_as_selector": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "uses_reduced_cold_pilots_as_production_evidence": False,
        "sets_kappa_s_equal_one": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "sets_heat_time_equal_one_by_convention": False,
        "sets_source_triplet_eta_by_convention": False,
        "identifies_taste_triplet_or_source_with_canonical_oh": False,
        "treats_z3_heat_kernel_as_pr230_physical_transfer": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 heat-kernel source-coupling/H4 no-go")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()
    tau = 1.0
    block_extension = matrix_summary(block_diagonal_source_extension(tau))
    coupled_rows = eta_rows(tau)

    heat_parent_loaded = (
        certs["z3_heat_kernel_attempt"].get(
            "z3_heat_kernel_neutral_transfer_attempt_passed"
        )
        is True
        and certs["z3_heat_kernel_attempt"].get(
            "mathematical_heat_kernel_primitive_support"
        )
        is True
        and certs["z3_heat_kernel_attempt"].get("proposal_allowed") is False
    )
    scale_parent_loaded = (
        certs["z3_heat_kernel_scale_selector_no_go"].get(
            "z3_heat_kernel_scale_selector_no_go_passed"
        )
        is True
        and certs["z3_heat_kernel_scale_selector_no_go"].get(
            "heat_kernel_scale_time_not_selected"
        )
        is True
        and certs["z3_heat_kernel_scale_selector_no_go"].get("proposal_allowed")
        is False
    )
    source_mixing_parent_loaded = (
        "do not certify a physical neutral scalar transfer or O_H bridge"
        in statuses["neutral_source_mixing_no_go"]
        and certs["neutral_source_mixing_no_go"].get("proposal_allowed") is False
        and "arbitrary source-radial bridge"
        in str(certs["neutral_source_mixing_no_go"].get("proposal_allowed_reason", ""))
    )
    block_extension_is_reducible = (
        block_extension["row_stochastic"]
        and block_extension["column_stochastic"]
        and block_extension["symmetric"]
        and block_extension["commutes_with_source_plus_triplet_z3"]
        and not block_extension["strictly_positive"]
        and not block_extension["primitive"]
        and block_extension["source_triplet_entries"] == [0.0, 0.0, 0.0]
    )
    positive_eta_can_make_primitive = all(
        row["primitive"] and row["strictly_positive"]
        for row in coupled_rows
        if 0.0 < row["eta"] < 1.0 / 3.0
    )
    eta_continuum_not_selected = (
        positive_eta_can_make_primitive
        and len(
            {
                tuple(round(value, 12) for value in row["source_triplet_entries"])
                for row in coupled_rows
                if 0.0 < row["eta"] < 1.0 / 3.0
            }
        )
        > 1
    )
    h4_artifact_absent = not (
        futures["same_surface_source_triplet_coupling"]
        or futures["canonical_oh_certificate"]
        or futures["source_higgs_cross_rows"]
        or futures["source_higgs_production_certificate"]
        or futures["wz_response_rows"]
    )
    physical_neutral_transfer_absent = not (
        futures["same_surface_neutral_transfer_operator"]
        or futures["neutral_offdiagonal_generator_certificate"]
        or futures["neutral_primitive_cone_certificate"]
    )
    aggregate_gates_still_open = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
        and certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["post_block100_completion_reopen"].get("closure_achieved")
        is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    no_go_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and heat_parent_loaded
        and scale_parent_loaded
        and source_mixing_parent_loaded
        and block_extension_is_reducible
        and positive_eta_can_make_primitive
        and eta_continuum_not_selected
        and h4_artifact_absent
        and physical_neutral_transfer_absent
        and aggregate_gates_still_open
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("block102-heat-kernel-support-loaded", heat_parent_loaded, statuses["z3_heat_kernel_attempt"])
    report("block103-scale-selector-loaded", scale_parent_loaded, statuses["z3_heat_kernel_scale_selector_no_go"])
    report("source-mixing-parent-loaded", source_mixing_parent_loaded, statuses["neutral_source_mixing_no_go"])
    report("block-diagonal-source-extension-reducible", block_extension_is_reducible, str(block_extension))
    report("positive-eta-can-make-full-transfer-primitive", positive_eta_can_make_primitive, "sampled 0<eta<1/3 rows are strictly positive")
    report("eta-continuum-not-selected", eta_continuum_not_selected, "multiple eta values satisfy the same formal positivity constraints")
    report("h4-source-canonical-higgs-artifact-absent", h4_artifact_absent, str(futures))
    report("physical-neutral-transfer-artifact-absent", physical_neutral_transfer_absent, str(futures))
    report("aggregate-gates-still-open", aggregate_gates_still_open, "retained/campaign/full-assembly/post-block100 deny closure")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("z3-heat-kernel-source-coupling-no-go-passed", no_go_passed, "exact boundary if all checks pass")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Z3 heat-kernel source-coupling data do "
            "not supply PR230 H4 source/canonical-Higgs coupling"
        ),
        "conditional_surface_status": (
            "If a future same-surface action, transfer operator, or "
            "off-diagonal generator fixes the source-triplet coupling eta and "
            "also supplies canonical O_H/source-Higgs pole authority, the "
            "Block102 heat-kernel primitive support can be reused.  Eta is "
            "absent on the actual current surface."
        ),
        "hypothetical_axiom_status": (
            "Adding eta>0 as a new physical source-triplet coupling axiom can "
            "make the finite source-plus-triplet matrix primitive, but this is "
            "a new action/transfer premise and not a derivation from current "
            "PR230 artifacts."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The heat-kernel triplet primitive does not couple the PR230 source "
            "singlet to canonical O_H.  A positive source-triplet eta is "
            "independent data; current artifacts do not derive or measure eta "
            "and do not provide C_sH/C_HH pole rows, canonical O_H, W/Z "
            "response, or scalar LSZ authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_heat_kernel_source_coupling_no_go_passed": no_go_passed,
        "block_diagonal_source_extension_is_reducible": block_extension_is_reducible,
        "source_triplet_eta_required": True,
        "source_triplet_eta_selected_by_current_surface": False,
        "positive_eta_can_make_full_transfer_primitive": positive_eta_can_make_primitive,
        "eta_continuum_not_selected": eta_continuum_not_selected,
        "h4_source_canonical_higgs_coupling_passed": False,
        "strict_neutral_h3_authority_passed": False,
        "physical_neutral_transfer_artifact_present": not physical_neutral_transfer_absent,
        "h4_artifact_present": not h4_artifact_absent,
        "canonical_oh_identity_present": futures["canonical_oh_certificate"],
        "source_higgs_pole_rows_present": (
            futures["source_higgs_cross_rows"]
            or futures["source_higgs_production_certificate"]
        ),
        "wz_response_rows_present": futures["wz_response_rows"],
        "pr230_closure_authorized": False,
        "closure_achieved": False,
        "block_diagonal_source_extension": block_extension,
        "coupled_eta_witness_rows": coupled_rows,
        "strict_future_artifact_presence": futures,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not set source-triplet eta by convention",
            "does not treat eta>0 existence as a PR230 physical action",
            "does not identify source singlet, taste triplet, O_s, or O_sp with canonical O_H",
            "does not relabel C_sx/C_xx rows as C_sH/C_HH rows",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, g2, v, heat time, diffusion scale, or source-Higgs overlap to one",
        ],
        "exact_next_action": (
            "Reopen the neutral route only with a same-surface source-triplet "
            "coupling/action row, off-diagonal generator, or primitive-cone "
            "certificate that fixes eta and H4 source/canonical-Higgs coupling. "
            "Otherwise pursue accepted O_H/action with strict C_ss/C_sH/C_HH "
            "pole rows, strict W/Z response with an allowed absolute pin, or "
            "strict Schur/scalar-LSZ pole authority."
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
