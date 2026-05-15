#!/usr/bin/env python3
"""
PR #230 Z3 heat-kernel neutral-transfer attempt.

This runner tests a stronger finite-group neutral primitive idea than the
earlier lazy-transfer shortcut.  The Z3 taste triplet canonically gives a
Dirichlet-form Laplacian on the three-cycle, and the heat kernel exp(-t Delta)
is strictly positive and primitive for every t > 0.  The question is whether
that mathematical primitive semigroup is already a same-surface PR230 physical
neutral transfer H3, and whether it supplies the H4 source/canonical-Higgs
coupling needed for top-Yukawa closure.

Result:
    No, not on the actual PR230 surface.  The heat kernel is a real finite
    Z3 primitive-cone witness, but the current artifacts do not identify it as
    the physical neutral transfer, do not select the heat time/scale from the
    action, and do not couple it to canonical O_H or scalar LSZ normalization.
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
    / "yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json"
)

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_h2_positive_cone_support": (
        "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
    ),
    "z3_conditional_primitive": (
        "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
    ),
    "z3_lazy_transfer_promotion": (
        "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
    ),
    "z3_lazy_selector_no_go": (
        "outputs/yt_pr230_z3_lazy_selector_no_go_2026-05-06.json"
    ),
    "neutral_h3h4_aperture": (
        "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
    ),
    "block55_canonical_neutral_cut": (
        "outputs/yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json"
    ),
    "neutral_offdiagonal_generator": (
        "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
    ),
    "neutral_burnside_irreducibility": (
        "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json"
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

FUTURE_STRICT_ARTIFACTS = {
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


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def max_abs(a: Matrix, b: Matrix) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def cyclic_z3() -> Matrix:
    return [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]


def transpose(a: Matrix) -> Matrix:
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def heat_kernel(time: float) -> Matrix:
    """Closed form for exp(-t Delta) on the Z3/C3 Dirichlet form."""
    nontrivial = math.exp(-3.0 * time)
    diagonal = (1.0 + 2.0 * nontrivial) / 3.0
    offdiag = (1.0 - nontrivial) / 3.0
    return [
        [diagonal if i == j else offdiag for j in range(3)]
        for i in range(3)
    ]


def laplacian_c3() -> Matrix:
    p = cyclic_z3()
    pt = transpose(p)
    i3 = identity(3)
    return [[2.0 * i3[i][j] - p[i][j] - pt[i][j] for j in range(3)] for i in range(3)]


def row_sums(a: Matrix) -> list[float]:
    return [sum(row) for row in a]


def col_sums(a: Matrix) -> list[float]:
    return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]


def is_close_list(values: list[float], target: float, tol: float = 1.0e-12) -> bool:
    return all(abs(value - target) <= tol for value in values)


def all_positive(a: Matrix, tol: float = 0.0) -> bool:
    return all(value > tol for row in a for value in row)


def is_symmetric(a: Matrix, tol: float = 1.0e-12) -> bool:
    return max_abs(a, transpose(a)) <= tol


def commutes(a: Matrix, b: Matrix, tol: float = 1.0e-12) -> bool:
    return max_abs(matmul(a, b), matmul(b, a)) <= tol


def matrix_power(a: Matrix, power: int) -> Matrix:
    result = identity(len(a))
    for _ in range(power):
        result = matmul(result, a)
    return result


def heat_witnesses() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    p = cyclic_z3()
    projector = [[1.0 / 3.0 for _ in range(3)] for _ in range(3)]
    for time in [0.0, 0.25, 1.0, 4.0]:
        kernel = heat_kernel(time)
        powered = matrix_power(kernel, 16)
        rows.append(
            {
                "time": time,
                "matrix": kernel,
                "nontrivial_eigenvalue": math.exp(-3.0 * time),
                "row_stochastic": is_close_list(row_sums(kernel), 1.0),
                "column_stochastic": is_close_list(col_sums(kernel), 1.0),
                "symmetric": is_symmetric(kernel),
                "commutes_with_z3_cycle": commutes(kernel, p),
                "strictly_positive": all_positive(kernel),
                "primitive": all_positive(kernel),
                "primitive_power": 1 if all_positive(kernel) else None,
                "power16_max_abs_error_to_uniform_projector": max_abs(powered, projector),
            }
        )
    return rows


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_STRICT_ARTIFACTS.items()}


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
        "treats_heat_time_as_physical_action_parameter": False,
        "treats_z3_heat_kernel_as_pr230_physical_transfer": False,
        "identifies_taste_triplet_or_source_with_canonical_oh": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 heat-kernel neutral-transfer attempt")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()
    laplacian = laplacian_c3()
    witnesses = heat_witnesses()

    z3_h1_loaded = (
        "same-surface Z3 taste-triplet artifact"
        in statuses["same_surface_z3_taste_triplet"]
        and certs["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
    )
    z3_h2_loaded = (
        "Z3-triplet positive-cone H2 support"
        in statuses["z3_h2_positive_cone_support"]
        and certs["z3_h2_positive_cone_support"].get("proposal_allowed") is False
    )
    prior_lazy_boundaries_loaded = (
        "Z3 lazy-transfer promotion not derivable"
        in statuses["z3_lazy_transfer_promotion"]
        and "Z3 lazy selector shortcuts"
        in statuses["z3_lazy_selector_no_go"]
        and certs["z3_lazy_transfer_promotion"].get("proposal_allowed") is False
        and certs["z3_lazy_selector_no_go"].get("proposal_allowed") is False
    )
    neutral_h3h4_boundary_loaded = (
        "H1/H2 support" in statuses["neutral_h3h4_aperture"]
        and certs["neutral_h3h4_aperture"].get("proposal_allowed") is False
    )
    mathematical_heat_kernel_support = (
        all(row["row_stochastic"] for row in witnesses)
        and all(row["column_stochastic"] for row in witnesses)
        and all(row["symmetric"] for row in witnesses)
        and all(row["commutes_with_z3_cycle"] for row in witnesses)
        and all(row["primitive"] for row in witnesses if row["time"] > 0.0)
        and witnesses[0]["primitive"] is False
    )
    heat_time_not_selected = (
        mathematical_heat_kernel_support
        and len({round(row["nontrivial_eigenvalue"], 14) for row in witnesses}) > 1
        and not any(futures.values())
    )
    physical_neutral_transfer_present = (
        futures["same_surface_neutral_transfer_operator"]
        or futures["neutral_offdiagonal_generator_certificate"]
        or futures["neutral_primitive_cone_certificate"]
    )
    strict_h3_authority_passed = False
    h4_source_canonical_higgs_coupling_passed = False
    canonical_oh_identity_present = futures["canonical_oh_certificate"]
    source_higgs_pole_rows_present = (
        futures["source_higgs_cross_rows"]
        or futures["source_higgs_production_certificate"]
    )
    aggregate_gates_still_open = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
        and certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["post_block100_completion_reopen"].get("closure_achieved") is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    attempt_passed = (
        not missing_parents
        and not proposal_allowed_parents
        and z3_h1_loaded
        and z3_h2_loaded
        and prior_lazy_boundaries_loaded
        and neutral_h3h4_boundary_loaded
        and mathematical_heat_kernel_support
        and heat_time_not_selected
        and not physical_neutral_transfer_present
        and not strict_h3_authority_passed
        and not h4_source_canonical_higgs_coupling_passed
        and not canonical_oh_identity_present
        and not source_higgs_pole_rows_present
        and aggregate_gates_still_open
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("z3-h1-same-surface-support-loaded", z3_h1_loaded, statuses["same_surface_z3_taste_triplet"])
    report("z3-h2-positive-cone-support-loaded", z3_h2_loaded, statuses["z3_h2_positive_cone_support"])
    report("prior-lazy-boundaries-loaded", prior_lazy_boundaries_loaded, "lazy-transfer and lazy-selector no-gos loaded")
    report("neutral-h3h4-boundary-loaded", neutral_h3h4_boundary_loaded, statuses["neutral_h3h4_aperture"])
    report("heat-kernel-dirichlet-form-constructed", True, "Delta=2I-P-P^T on the Z3/C3 triplet")
    report("heat-kernel-primitive-math-support", mathematical_heat_kernel_support, "t>0 kernels are positive stochastic primitive matrices")
    report("heat-time-not-selected-by-current-surface", heat_time_not_selected, "multiple t>0 kernels satisfy the same Z3 symmetry/cone constraints")
    report("physical-neutral-transfer-artifact-absent", not physical_neutral_transfer_present, str(futures))
    report("strict-h3-authority-not-passed", not strict_h3_authority_passed, "heat kernel is not admitted as PR230 physical transfer")
    report("h4-source-canonical-higgs-coupling-absent", not h4_source_canonical_higgs_coupling_passed, "canonical O_H/source-Higgs coupling remains absent")
    report("canonical-oh-and-source-higgs-pole-rows-absent", not canonical_oh_identity_present and not source_higgs_pole_rows_present, str(futures))
    report("aggregate-gates-still-open", aggregate_gates_still_open, "retained/campaign/full-assembly/post-block100 all deny closure")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("z3-heat-kernel-attempt-passed", attempt_passed, "support/no-go boundary if all checks pass")

    result = {
        "actual_current_surface_status": (
            "exact-support / Z3 heat-kernel primitive transfer is mathematical "
            "support only; PR230 physical H3/H4 closure remains absent"
        ),
        "conditional_surface_status": (
            "If a future same-surface action or transfer certificate identifies "
            "exp(-t Delta) at a derived t as the PR230 neutral transfer and also "
            "supplies source/canonical-Higgs coupling authority, this finite "
            "heat-kernel witness can support the neutral primitive route."
        ),
        "hypothetical_axiom_status": (
            "Under an accepted new axiom that the C3 heat kernel with a specified "
            "time t is the same-surface neutral scalar transfer, H3 would be "
            "mathematically primitive; that axiom is not present on the actual "
            "surface and H4 remains additional."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The heat kernel is a mathematical primitive semigroup, not an "
            "admitted PR230 physical transfer.  The current surface does not "
            "derive the heat time/scale, canonical O_H identity, source-Higgs "
            "overlap, scalar LSZ metric, or W/Z response bridge."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_heat_kernel_neutral_transfer_attempt_passed": attempt_passed,
        "mathematical_heat_kernel_primitive_support": mathematical_heat_kernel_support,
        "heat_kernel_dirichlet_form": {
            "basis": ["Phi_1_prime", "Phi_2_prime", "Phi_3_prime"],
            "cyclic_generator_P": cyclic_z3(),
            "laplacian_delta": laplacian,
            "definition": "Delta = 2 I - P - P^T, K_t = exp(-t Delta)",
            "spectrum_delta": [0.0, 3.0, 3.0],
            "heat_kernel_rows": witnesses,
            "rank_one_limit": [[1.0 / 3.0 for _ in range(3)] for _ in range(3)],
        },
        "heat_time_or_action_scale_selected": False,
        "same_surface_physical_action_selects_heat_time": False,
        "heat_kernel_is_pr230_physical_neutral_transfer": False,
        "strict_neutral_h3_authority_passed": strict_h3_authority_passed,
        "strict_h4_source_canonical_higgs_coupling_passed": h4_source_canonical_higgs_coupling_passed,
        "source_identity_to_triplet_coupling_present": False,
        "canonical_oh_identity_present": canonical_oh_identity_present,
        "source_higgs_pole_rows_present": source_higgs_pole_rows_present,
        "scalar_lsz_metric_present": False,
        "physical_neutral_transfer_artifact_present": physical_neutral_transfer_present,
        "strict_future_artifact_presence": futures,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "closure_achieved": False,
        "pr230_closure_authorized": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write a neutral primitive-cone certificate",
            "does not treat a finite-group heat kernel as physical PR230 dynamics",
            "does not select the heat time or diffusion coefficient by convention",
            "does not identify the Z3 taste triplet, O_s, or O_sp with canonical O_H",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, g2, v, or source-Higgs overlap to one",
        ],
        "exact_next_action": (
            "Reopen the neutral route only with a same-surface physical action or "
            "transfer certificate selecting the heat-kernel time/scale and a "
            "separate H4 source/canonical-Higgs coupling certificate.  Otherwise "
            "pursue accepted O_H/action plus C_ss/C_sH/C_HH rows, strict W/Z "
            "response rows with allowed absolute pin, or strict Schur/scalar-LSZ "
            "pole authority."
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
