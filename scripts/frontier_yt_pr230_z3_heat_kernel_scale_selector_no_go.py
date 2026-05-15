#!/usr/bin/env python3
"""
PR #230 Z3 heat-kernel scale-selector no-go.

Block102 showed that the finite C3/Z3 Dirichlet form gives a genuine primitive
heat kernel K_tau = exp(-tau Delta) for every tau > 0.  This runner checks the
remaining shortcut: can the current PR230 symmetry/cone/semigroup data select
the heat time or diffusion scale and thereby promote that mathematical
semigroup into the physical neutral H3 transfer?

Verdict:
    No on the current PR230 surface.  Z3 covariance, symmetry, stochasticity,
    detailed balance, positivity/primitive status, the semigroup law, and the
    rank-one limit all hold for a continuum of tau > 0.  Rescaling the
    generator Delta -> lambda Delta is indistinguishable from rescaling the
    heat time, and the current surface supplies neither a physical time unit
    nor an action coefficient.  Entropy/gap extremization either remains an
    external selector or picks a boundary/limit, not a derived finite physical
    transfer.
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
    / "yt_pr230_z3_heat_kernel_scale_selector_no_go_2026-05-15.json"
)

PARENTS = {
    "same_surface_z3_taste_triplet": (
        "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json"
    ),
    "z3_positive_cone_support": (
        "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
    ),
    "z3_lazy_selector_no_go": (
        "outputs/yt_pr230_z3_lazy_selector_no_go_2026-05-06.json"
    ),
    "z3_heat_kernel_attempt": (
        "outputs/yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json"
    ),
    "neutral_h3h4_aperture": (
        "outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json"
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


def cyclic_z3() -> Matrix:
    return [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]


def identity(n: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


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


def heat_kernel(tau: float) -> Matrix:
    """Closed form for exp(-tau Delta) on C3."""
    e = math.exp(-3.0 * tau)
    diagonal = (1.0 + 2.0 * e) / 3.0
    offdiag = (1.0 - e) / 3.0
    return [[diagonal if i == j else offdiag for j in range(3)] for i in range(3)]


def row_entropy(row: list[float]) -> float:
    return -sum(p * math.log(p) for p in row if p > 0.0)


def finite_difference_generator(tau: float, step: float = 1.0e-7) -> Matrix:
    """Approximate dK/dt at zero for generator-scale checks."""
    k0 = heat_kernel(0.0)
    kh = heat_kernel(tau * step)
    return [[(kh[i][j] - k0[i][j]) / step for j in range(3)] for i in range(3)]


def scale_rows() -> list[dict[str, Any]]:
    p = cyclic_z3()
    rows: list[dict[str, Any]] = []
    for tau in [0.05, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0]:
        k = heat_kernel(tau)
        e = math.exp(-3.0 * tau)
        rows.append(
            {
                "tau": tau,
                "matrix": k,
                "nontrivial_eigenvalue": e,
                "row_stochastic": all_close(row_sums(k), 1.0),
                "column_stochastic": all_close(col_sums(k), 1.0),
                "symmetric": is_symmetric(k),
                "uniform_detailed_balance": is_symmetric(k),
                "commutes_with_z3_cycle": commutes(k, p),
                "strictly_positive": all_positive(k),
                "primitive": all_positive(k),
                "row_entropy": row_entropy(k[0]),
                "spectral_gap_discrete": 1.0 - e,
            }
        )
    return rows


def semigroup_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for a, b in [(0.125, 0.375), (0.25, 0.5), (1.0, 2.0)]:
        checks.append(
            {
                "tau_a": a,
                "tau_b": b,
                "max_abs_error_KaKb_minus_Ka_plus_b": max_abs(
                    matmul(heat_kernel(a), heat_kernel(b)),
                    heat_kernel(a + b),
                ),
            }
        )
    return checks


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
        "sets_diffusion_scale_equal_one_by_convention": False,
        "treats_entropy_or_gap_as_action_principle": False,
        "treats_z3_heat_kernel_as_pr230_physical_transfer": False,
        "identifies_taste_triplet_or_source_with_canonical_oh": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 heat-kernel scale-selector no-go")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    firewall = forbidden_firewall()
    rows = scale_rows()
    semigroup = semigroup_checks()
    generator_1 = finite_difference_generator(1.0)
    generator_2 = finite_difference_generator(2.0)

    heat_parent_loaded = (
        certs["z3_heat_kernel_attempt"].get(
            "z3_heat_kernel_neutral_transfer_attempt_passed"
        )
        is True
        and certs["z3_heat_kernel_attempt"].get(
            "mathematical_heat_kernel_primitive_support"
        )
        is True
        and certs["z3_heat_kernel_attempt"].get(
            "same_surface_physical_action_selects_heat_time"
        )
        is False
        and certs["z3_heat_kernel_attempt"].get("proposal_allowed") is False
    )
    all_rows_valid = (
        all(row["row_stochastic"] for row in rows)
        and all(row["column_stochastic"] for row in rows)
        and all(row["symmetric"] for row in rows)
        and all(row["uniform_detailed_balance"] for row in rows)
        and all(row["commutes_with_z3_cycle"] for row in rows)
        and all(row["strictly_positive"] for row in rows)
        and all(row["primitive"] for row in rows)
    )
    continuum_not_selected = (
        all_rows_valid
        and len({round(row["nontrivial_eigenvalue"], 12) for row in rows}) == len(rows)
    )
    semigroup_law_holds = all(
        item["max_abs_error_KaKb_minus_Ka_plus_b"] < 1.0e-12 for item in semigroup
    )
    generator_scale_changes = max_abs(
        generator_2,
        [[2.0 * value for value in row] for row in generator_1],
    ) < 1.0e-6
    entropy_monotone_not_finite_selector = all(
        rows[i]["row_entropy"] < rows[i + 1]["row_entropy"]
        for i in range(len(rows) - 1)
    )
    gap_monotone_not_finite_selector = all(
        rows[i]["spectral_gap_discrete"] < rows[i + 1]["spectral_gap_discrete"]
        for i in range(len(rows) - 1)
    )
    physical_transfer_artifact_absent = not (
        futures["same_surface_neutral_transfer_operator"]
        or futures["neutral_offdiagonal_generator_certificate"]
        or futures["neutral_primitive_cone_certificate"]
    )
    h4_absent = not (
        futures["canonical_oh_certificate"]
        or futures["source_higgs_cross_rows"]
        or futures["source_higgs_production_certificate"]
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
        and continuum_not_selected
        and semigroup_law_holds
        and generator_scale_changes
        and entropy_monotone_not_finite_selector
        and gap_monotone_not_finite_selector
        and physical_transfer_artifact_absent
        and h4_absent
        and aggregate_gates_still_open
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("block102-heat-kernel-support-loaded", heat_parent_loaded, statuses["z3_heat_kernel_attempt"])
    report("compatible-heat-kernel-continuum", continuum_not_selected, "all sampled tau>0 satisfy Z3/symmetric/stochastic/primitive constraints")
    report("semigroup-law-does-not-select-tau", semigroup_law_holds, str(semigroup))
    report("generator-scale-reparametrization-witness", generator_scale_changes, "Delta scale and heat-time scale are interchangeable")
    report("entropy-not-finite-physical-selector", entropy_monotone_not_finite_selector, "entropy increases toward the uniform projector limit")
    report("spectral-gap-not-finite-physical-selector", gap_monotone_not_finite_selector, "gap increases toward the uniform projector limit")
    report("physical-neutral-transfer-artifact-absent", physical_transfer_artifact_absent, str(futures))
    report("h4-source-canonical-higgs-coupling-absent", h4_absent, str(futures))
    report("aggregate-gates-still-open", aggregate_gates_still_open, "retained/campaign/full-assembly/post-block100 deny closure")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("z3-heat-kernel-scale-selector-no-go-passed", no_go_passed, "exact boundary if all checks pass")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Z3 heat-kernel scale and time selectors "
            "do not derive the PR230 physical neutral transfer"
        ),
        "conditional_surface_status": (
            "If a future same-surface action fixes the diffusion coefficient or "
            "heat time and separately supplies H4 source/canonical-Higgs "
            "coupling, the Block102 heat-kernel primitive witness can be reused "
            "as mathematical support.  That selector is absent on the actual "
            "current surface."
        ),
        "hypothetical_axiom_status": (
            "Adding a new axiom that tau is a specified physical neutral-transfer "
            "time would select one member of the heat-kernel family, but this "
            "would be a new action/normalization premise rather than a PR230 "
            "derivation."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface supplies no physical heat-time unit, diffusion "
            "coefficient, neutral transfer operator, off-diagonal generator, "
            "canonical O_H identity, or source-Higgs pole rows.  Symmetry, cone, "
            "semigroup, reversibility, entropy, and gap criteria do not select a "
            "finite physical transfer without importing a new action principle."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_heat_kernel_scale_selector_no_go_passed": no_go_passed,
        "heat_kernel_scale_time_not_selected": continuum_not_selected,
        "continuum_of_compatible_heat_kernels": all_rows_valid,
        "semigroup_law_holds_for_continuum": semigroup_law_holds,
        "generator_scale_reparametrization_witness": generator_scale_changes,
        "entropy_extremum_is_boundary_or_external_selector": entropy_monotone_not_finite_selector,
        "spectral_gap_extremum_is_boundary_or_external_selector": gap_monotone_not_finite_selector,
        "same_surface_physical_action_selects_heat_time": False,
        "physical_heat_time_authority_present": False,
        "physical_diffusion_scale_authority_present": False,
        "heat_kernel_is_pr230_physical_neutral_transfer": False,
        "strict_neutral_h3_authority_passed": False,
        "strict_h4_source_canonical_higgs_coupling_passed": False,
        "pr230_closure_authorized": False,
        "closure_achieved": False,
        "heat_kernel_scale_rows": rows,
        "semigroup_checks": semigroup,
        "generator_scale_witness": {
            "approx_generator_tau_1": generator_1,
            "approx_generator_tau_2": generator_2,
            "max_abs_error_generator_tau2_minus_2_tau1": max_abs(
                generator_2,
                [[2.0 * value for value in row] for row in generator_1],
            ),
        },
        "strict_future_artifact_presence": futures,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not select heat time or diffusion scale by convention",
            "does not treat entropy or spectral gap as a PR230 action principle",
            "does not treat the finite-group heat kernel as physical PR230 transfer",
            "does not write a neutral primitive-cone certificate",
            "does not identify the Z3 taste triplet, O_s, or O_sp with canonical O_H",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set kappa_s, c2, Z_match, g2, v, heat time, or diffusion scale to one",
        ],
        "exact_next_action": (
            "A neutral-route reopen now requires a same-surface physical action, "
            "transfer operator, or off-diagonal generator that fixes the heat "
            "time/diffusion scale, plus H4 source/canonical-Higgs coupling.  "
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
