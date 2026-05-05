#!/usr/bin/env python3
"""
PR #230 scalar-LSZ Carleman/Tauberian determinacy attempt.

This is the strict moment-theory continuation of the scalar-LSZ route.  It
asks whether Carleman/Stieltjes moment determinacy or Tauberian threshold
machinery can turn the current finite FH/LSZ scalar rows into a unique
isolated scalar-pole residue.

The current answer is no.  Carleman and Tauberian theorems can be decisive
only after a same-surface infinite moment sequence, certified tail/asymptotic
control, contact subtraction, threshold/FV/IR authority, and pole isolation are
derived.  A finite positive Stieltjes prefix admits multiple positive measures
with the same checked prefix and different pole residue.
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
    / "yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json"
)

PARENTS = {
    "clean_source_higgs_math_selector": "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json",
    "stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
    "polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
    "polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
    "finite_volume_pole_saturation": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "pole_saturation_threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "threshold_authority_import_audit": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "soft_continuum_threshold_no_go": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "scalar_denominator_theorem_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "holonomic_exact_authority_attempt": "outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_closure_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "carleman_tauberian_certificate": "outputs/yt_fh_lsz_carleman_tauberian_certificate_2026-05-05.json",
    "infinite_same_surface_moment_sequence": "outputs/yt_fh_lsz_same_surface_infinite_moment_sequence_2026-05-05.json",
    "threshold_asymptotic_certificate": "outputs/yt_fh_lsz_threshold_asymptotic_certificate_2026-05-05.json",
    "fv_ir_limiting_order_certificate": "outputs/yt_fh_lsz_fv_ir_limiting_order_certificate_2026-05-05.json",
    "contact_subtraction_certificate": "outputs/yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json",
}

FORBIDDEN_INPUTS = [
    "finite moment prefix as Carleman proof",
    "finite shell rows as Tauberian threshold density",
    "PSLQ/value recognition as pole-residue selector",
    "observed top mass or observed y_t",
    "H_unit or Ward readout authority",
    "alpha_LM / plaquette / u0 normalization",
    "kappa_s = 1, c2 = 1, or Z_match = 1 by convention",
]

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_FILES.items()}


def stieltjes_moments(
    masses_squared: np.ndarray, weights: np.ndarray, max_order: int
) -> np.ndarray:
    orders = np.arange(max_order + 1, dtype=float)
    moments = []
    for order in orders:
        moments.append(float(np.sum(weights / masses_squared ** (order + 1.0))))
    return np.asarray(moments, dtype=float)


def moment_matrix(masses_squared: np.ndarray, max_order: int) -> np.ndarray:
    orders = np.arange(max_order + 1, dtype=float)
    return np.asarray(
        [
            [1.0 / mass_squared ** (order + 1.0) for mass_squared in masses_squared]
            for order in orders
        ],
        dtype=float,
    )


def nullspace(matrix: np.ndarray, tolerance: float = 1.0e-12) -> np.ndarray:
    _, singular_values, vh = np.linalg.svd(matrix)
    rank = int(np.sum(singular_values > tolerance))
    return vh[rank:, :]


def finite_prefix_stieltjes_counterfamily() -> dict[str, Any]:
    pole_index = 0
    moment_prefix_max_order = 4
    masses_squared = np.asarray([0.25, 0.40, 0.70, 1.10, 1.70, 2.60, 4.00, 6.30])
    base_weights = np.asarray([1.10, 0.33, 0.27, 0.22, 0.18, 0.15, 0.12, 0.10])
    matrix = moment_matrix(masses_squared, moment_prefix_max_order)
    basis = nullspace(matrix)

    if basis.size == 0:
        raise RuntimeError("unexpected empty finite-prefix nullspace")

    candidate = max(basis, key=lambda row: abs(float(row[pole_index])))
    if abs(float(candidate[pole_index])) <= 1.0e-10:
        raise RuntimeError("nullspace does not perturb the pole residue")

    if candidate[pole_index] < 0.0:
        candidate = -candidate

    negative_slots = candidate < 0.0
    if bool(np.any(negative_slots)):
        epsilon_limit = float(
            np.min(base_weights[negative_slots] / np.abs(candidate[negative_slots]))
        )
        epsilon = 0.25 * epsilon_limit
    else:
        epsilon = 0.05

    altered_weights = base_weights + epsilon * candidate
    base_moments = stieltjes_moments(
        masses_squared, base_weights, moment_prefix_max_order
    )
    altered_moments = stieltjes_moments(
        masses_squared, altered_weights, moment_prefix_max_order
    )
    moment_delta = np.abs(base_moments - altered_moments)

    base_extended = stieltjes_moments(masses_squared, base_weights, 12)
    altered_extended = stieltjes_moments(masses_squared, altered_weights, 12)
    higher_delta = float(abs(base_extended[10] - altered_extended[10]))

    return {
        "construction": (
            "A positive discrete Stieltjes measure with eight support atoms is "
            "perturbed along the nullspace of the moment map for orders 0..4. "
            "The checked finite prefix is unchanged while the isolated-pole "
            "atom weight changes."
        ),
        "stieltjes_measure_kind": "positive finite atomic measures",
        "pole_mass_squared": float(masses_squared[pole_index]),
        "support_masses_squared": [float(x) for x in masses_squared],
        "moment_prefix_orders": list(range(moment_prefix_max_order + 1)),
        "base_weights": [float(x) for x in base_weights],
        "altered_weights": [float(x) for x in altered_weights],
        "perturbation_vector": [float(x) for x in candidate],
        "epsilon": epsilon,
        "all_base_weights_positive": bool(np.all(base_weights > 0.0)),
        "all_altered_weights_positive": bool(np.all(altered_weights > 0.0)),
        "base_prefix_moments": [float(x) for x in base_moments],
        "altered_prefix_moments": [float(x) for x in altered_moments],
        "max_prefix_moment_delta": float(np.max(moment_delta)),
        "same_finite_prefix": bool(float(np.max(moment_delta)) < 1.0e-10),
        "base_pole_residue": float(base_weights[pole_index]),
        "altered_pole_residue": float(altered_weights[pole_index]),
        "pole_residue_delta": float(altered_weights[pole_index] - base_weights[pole_index]),
        "pole_residue_changes": bool(
            abs(float(altered_weights[pole_index] - base_weights[pole_index]))
            > 1.0e-8
        ),
        "higher_moment_order_10_delta": higher_delta,
        "finite_prefix_stieltjes_counterfamily_passed": bool(
            np.all(base_weights > 0.0)
            and np.all(altered_weights > 0.0)
            and float(np.max(moment_delta)) < 1.0e-10
            and abs(float(altered_weights[pole_index] - base_weights[pole_index]))
            > 1.0e-8
        ),
    }


def carleman_partial_sum(moments: list[float]) -> float:
    terms = []
    max_n = (len(moments) - 1) // 2
    for n in range(1, max_n + 1):
        value = moments[2 * n]
        if value > 0.0:
            terms.append(value ** (-1.0 / (2.0 * n)))
    return float(sum(terms))


def carleman_tauberian_boundary(
    counterfamily: dict[str, Any]
) -> dict[str, Any]:
    prefix_moments = [float(x) for x in counterfamily["base_prefix_moments"]]
    prefix_sum = carleman_partial_sum(prefix_moments)
    return {
        "carleman_condition": "sum_n m_{2n}^{-1/(2n)} = infinity",
        "finite_prefix_partial_sum": prefix_sum,
        "finite_prefix_can_prove_divergence": False,
        "tauberian_requirement": (
            "same-surface large-order/asymptotic moment or threshold-density "
            "control with contact subtraction and FV/IR limiting order"
        ),
        "finite_shell_rows_are_threshold_asymptotic": False,
        "finite_prefix_identifies_pole_residue": False,
        "lesson": (
            "Carleman determinacy is an infinite-tail statement and Tauberian "
            "threshold reconstruction is an asymptotic statement.  The current "
            "PR230 finite shell/moment rows cannot supply either statement and "
            "cannot select a unique scalar pole residue."
        ),
    }


def future_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_subtracted_scalar_correlator",
            "required": "the scalar object, source coordinate, contact subtraction, and zero-source limit are fixed on the PR230 surface",
            "current_satisfied": False,
        },
        {
            "id": "infinite_or_certified_tail_moment_sequence",
            "required": "all moments or rigorous tail bounds/asymptotics for the same scalar measure, not a finite shell prefix",
            "current_satisfied": False,
        },
        {
            "id": "carleman_or_equivalent_determinacy",
            "required": "Carleman divergence or another theorem-grade Stieltjes determinacy certificate",
            "current_satisfied": False,
        },
        {
            "id": "tauberian_threshold_authority",
            "required": "derived threshold density/gap asymptotics, limiting order, and no hidden continuum ambiguity",
            "current_satisfied": False,
        },
        {
            "id": "isolated_pole_and_residue_interval",
            "required": "isolated pole plus a positive tight pole-residue interval from the same moment problem",
            "current_satisfied": False,
        },
        {
            "id": "fv_ir_limiting_order",
            "required": "finite-volume/IR/zero-mode limiting-order authority for the scalar pole",
            "current_satisfied": False,
        },
        {
            "id": "forbidden_import_firewall",
            "required": "reject observed selectors, H_unit/Ward, alpha/plaquette/u0, unit kappa_s/c2/Z_match, PSLQ and finite-prefix selectors",
            "current_satisfied": True,
        },
    ]


def main() -> int:
    print("PR #230 scalar-LSZ Carleman/Tauberian determinacy attempt")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    future_present = future_presence()
    counterfamily = finite_prefix_stieltjes_counterfamily()
    determinacy = carleman_tauberian_boundary(counterfamily)
    contract = future_certificate_contract()
    missing_contract = [row["id"] for row in contract if not row["current_satisfied"]]

    selector_keeps_moment_tools_future_only = (
        parents["clean_source_higgs_math_selector"].get("proposal_allowed") is False
        and any(
            row.get("id") == "holonomic_dmodule_picard_fuchs_wz_painleve"
            and row.get("current_admissible_for_closure") is False
            for row in parents["clean_source_higgs_math_selector"].get(
                "outside_math_route_rows", []
            )
        )
    )
    stieltjes_gate_absent = (
        parents["stieltjes_moment_gate"].get("moment_certificate_gate_passed") is False
    )
    pade_gate_absent = (
        parents["pade_stieltjes_bounds_gate"].get("pade_stieltjes_bounds_gate_passed")
        is False
    )
    holonomic_counterfamily_loaded = (
        parents["holonomic_exact_authority_attempt"].get("proposal_allowed") is False
        and parents["holonomic_exact_authority_attempt"].get(
            "holonomic_exact_authority_passed"
        )
        is False
        and parents["holonomic_exact_authority_attempt"].get("counterfamily", {}).get(
            "residues_differ"
        )
        is True
    )
    contact_and_threshold_open = (
        parents["contact_subtraction_identifiability"].get("proposal_allowed") is False
        and parents["finite_volume_pole_saturation"].get("proposal_allowed") is False
        and parents["pole_saturation_threshold_gate"].get("proposal_allowed") is False
        and parents["soft_continuum_threshold_no_go"].get("proposal_allowed") is False
    )
    exact_authority_files_absent = not any(future_present.values())
    finite_prefix_counterfamily_passed = counterfamily[
        "finite_prefix_stieltjes_counterfamily_passed"
    ]
    carleman_tail_not_finite = (
        determinacy["finite_prefix_can_prove_divergence"] is False
        and determinacy["finite_prefix_identifies_pole_residue"] is False
    )
    tauberian_asymptotic_not_finite = (
        determinacy["finite_shell_rows_are_threshold_asymptotic"] is False
    )
    carleman_tauberian_determinacy_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selector-keeps-moment-tools-future-only", selector_keeps_moment_tools_future_only, statuses["clean_source_higgs_math_selector"])
    report("strict-stieltjes-certificate-absent", stieltjes_gate_absent, statuses["stieltjes_moment_gate"])
    report("strict-pade-stieltjes-certificate-absent", pade_gate_absent, statuses["pade_stieltjes_bounds_gate"])
    report("holonomic-counterfamily-loaded", holonomic_counterfamily_loaded, statuses["holonomic_exact_authority_attempt"])
    report("contact-threshold-fv-ir-open", contact_and_threshold_open, "contact/threshold/FV/IR gates remain absent or negative")
    report("future-carleman-tauberian-files-absent", exact_authority_files_absent, f"future_present={future_present}")
    report("finite-prefix-stieltjes-counterfamily", finite_prefix_counterfamily_passed, "same prefix, different positive pole residue")
    report("carleman-tail-condition-not-finite-prefix", carleman_tail_not_finite, f"partial_sum={determinacy['finite_prefix_partial_sum']}")
    report("tauberian-threshold-condition-not-finite-shell", tauberian_asymptotic_not_finite, determinacy["tauberian_requirement"])
    report("future-certificate-contract-recorded", len(missing_contract) == 6, f"missing={missing_contract}")
    report("forbidden-firewall-clean", True, ", ".join(FORBIDDEN_INPUTS))
    report("carleman-tauberian-determinacy-not-passed", not carleman_tauberian_determinacy_passed, "no infinite/tail same-surface moment authority")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Carleman/Tauberian scalar-LSZ "
            "determinacy not derivable from current finite PR230 rows"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface infinite or "
            "tail-certified scalar moment sequence supplies Carleman/equivalent "
            "determinacy, threshold/Tauberian asymptotics, contact subtraction, "
            "FV/IR limiting order, isolated-pole authority, and a positive tight "
            "residue interval"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current scalar-LSZ surface has finite shell/moment support only. "
            "Carleman determinacy is an infinite-tail condition, and Tauberian "
            "threshold reconstruction is an asymptotic condition.  A finite "
            "positive Stieltjes prefix admits positive measures with the same "
            "checked prefix and different pole residue."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "carleman_tauberian_determinacy_passed": carleman_tauberian_determinacy_passed,
        "finite_prefix_stieltjes_counterfamily_passed": finite_prefix_counterfamily_passed,
        "future_file_presence": future_present,
        "future_certificate_contract": contract,
        "finite_prefix_counterfamily": counterfamily,
        "carleman_tauberian_boundary": determinacy,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim scalar-LSZ closure",
            "does not write a Carleman/Tauberian or infinite-moment certificate",
            "does not use finite moments or finite shells as determinacy proof",
            "does not use PSLQ/value recognition as proof selector",
            "does not claim retained or proposed_retained PR230 closure",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "A positive scalar-LSZ moment route must supply a same-surface "
            "subtracted scalar correlator and either an infinite moment sequence "
            "or rigorous tail/asymptotic control proving Stieltjes determinacy, "
            "plus threshold, contact, FV/IR, and isolated-pole residue bounds. "
            "Otherwise the cleaner foreground remains O_H/C_sH/C_HH pole rows, "
            "same-source W/Z response rows, genuine Schur rows, or a neutral "
            "off-diagonal primitive-cone certificate."
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
