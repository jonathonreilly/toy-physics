#!/usr/bin/env python3
"""
PR #230 Block70 Schur/Feshbach K-prime residue theorem.

This runner is a finite-dimensional exact-support witness for the theorem
needed by the Schur/K-prime route:

    Res C_ab = (a r) (l b) / (l K'(x_pole) r)

for the Laurent coefficient of a connected two-point row obtained from the
inverse same-surface scalar kernel K(x), after analytic contact terms are
separated.  It validates the equivalent one-source-coordinate Schur/Feshbach
row and checks invariance under both general similarity basis changes and
block-preserving orthogonal-sector reparametrizations.

It does not provide physical PR230 Schur rows and does not claim closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_block70_schur_feshbach_kprime_residue_theorem_2026-05-12.json"

PARENTS = {
    "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_kernel_row_contract_gate": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_certificate_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
}

FORBIDDEN_PROOF_INPUTS = (
    "H_unit",
    "yt_ward_identity",
    "y_t_bare",
    "alpha_LM",
    "plaquette",
    "u0",
    "observed target selector",
    "alias import",
)

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


def as_float(value: np.ndarray | float) -> float:
    return float(np.asarray(value).reshape(()))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def make_kernel_family() -> dict[str, Any]:
    x_pole = 0.37
    c0 = np.asarray(
        [
            [1.70, 0.20, -0.10],
            [0.05, 1.35, 0.18],
            [0.12, -0.08, 1.55],
        ],
        dtype=float,
    )
    b0 = np.asarray([[0.21, -0.17, 0.09]], dtype=float)
    d0 = np.asarray([[-0.11], [0.26], [0.14]], dtype=float)
    c0_inv = np.linalg.inv(c0)
    a0 = b0 @ c0_inv @ d0

    c1 = np.asarray(
        [
            [0.06, -0.03, 0.02],
            [0.01, -0.04, 0.05],
            [-0.02, 0.03, 0.07],
        ],
        dtype=float,
    )
    b1 = np.asarray([[0.04, -0.02, 0.03]], dtype=float)
    d1 = np.asarray([[0.07], [-0.04], [0.02]], dtype=float)
    a1 = np.asarray([[0.43]], dtype=float)

    c2 = np.asarray(
        [
            [0.010, 0.004, -0.003],
            [-0.002, 0.008, 0.001],
            [0.003, -0.005, 0.006],
        ],
        dtype=float,
    )
    b2 = np.asarray([[0.004, 0.002, -0.003]], dtype=float)
    d2 = np.asarray([[0.003], [-0.002], [0.005]], dtype=float)
    a2 = np.asarray([[0.011]], dtype=float)

    k0 = np.block([[a0, b0], [d0, c0]])
    k1 = np.block([[a1, b1], [d1, c1]])
    k2 = np.block([[a2, b2], [d2, c2]])
    source_covector = np.asarray([[1.0, 0.0, 0.0, 0.0]], dtype=float)
    source_vector = np.asarray([[1.0], [0.0], [0.0], [0.0]], dtype=float)
    higgs_vector = np.asarray([[0.37], [-0.22], [0.31], [0.18]], dtype=float)
    higgs_covector = np.asarray([[0.42, -0.19, 0.27, 0.16]], dtype=float)

    return {
        "x_pole": x_pole,
        "K0": k0,
        "K1": k1,
        "K2": k2,
        "source_covector": source_covector,
        "source_vector": source_vector,
        "higgs_vector": higgs_vector,
        "higgs_covector": higgs_covector,
    }


def kernel_at(family: dict[str, Any], x: float) -> np.ndarray:
    dx = x - float(family["x_pole"])
    return family["K0"] + dx * family["K1"] + dx * dx * family["K2"]


def contact_term(family: dict[str, Any], x: float) -> float:
    dx = x - float(family["x_pole"])
    return 0.31 - 0.17 * dx + 0.04 * dx * dx


def schur_row_from_blocks(k0: np.ndarray, k1: np.ndarray) -> dict[str, Any]:
    a0 = k0[:1, :1]
    b0 = k0[:1, 1:]
    d0 = k0[1:, :1]
    c0 = k0[1:, 1:]
    a1 = k1[:1, :1]
    b1 = k1[:1, 1:]
    d1 = k1[1:, :1]
    c1 = k1[1:, 1:]
    c0_inv = np.linalg.inv(c0)
    s0 = as_float(a0 - b0 @ c0_inv @ d0)
    s1 = as_float(a1 - b1 @ c0_inv @ d0 - b0 @ c0_inv @ d1 + b0 @ c0_inv @ c1 @ c0_inv @ d0)
    r = np.vstack([np.asarray([[1.0]]), -c0_inv @ d0])
    l = np.hstack([np.asarray([[1.0]]), -b0 @ c0_inv])
    return {
        "A_at_pole": as_float(a0),
        "B_at_pole": b0.reshape(-1).tolist(),
        "D_at_pole": d0.reshape(-1).tolist(),
        "C_at_pole": c0.tolist(),
        "D_eff_at_pole": s0,
        "D_eff_prime_at_pole": s1,
        "right_null_vector": r,
        "left_null_covector": l,
    }


def residue_formula(
    k1: np.ndarray,
    left_probe: np.ndarray,
    right_probe: np.ndarray,
    left_null: np.ndarray,
    right_null: np.ndarray,
) -> dict[str, float]:
    denominator = as_float(left_null @ k1 @ right_null)
    left_projection = as_float(left_probe @ right_null)
    right_projection = as_float(left_null @ right_probe)
    numerator = left_projection * right_projection
    return {
        "left_projection": left_projection,
        "right_projection": right_projection,
        "source_projection_numerator": numerator,
        "kprime_denominator": denominator,
        "residue": numerator / denominator,
    }


def residue_limit_rows(
    family: dict[str, Any],
    left_probe: np.ndarray,
    right_probe: np.ndarray,
    predicted: float,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    x_pole = float(family["x_pole"])
    for eps in (1.0e-3, 5.0e-4, 1.0e-4, 5.0e-5, 1.0e-5):
        x = x_pole + eps
        inverse_kernel = np.linalg.inv(kernel_at(family, x))
        pole_plus_contact = as_float(left_probe @ inverse_kernel @ right_probe) + contact_term(family, x)
        pole_only = as_float(left_probe @ inverse_kernel @ right_probe)
        estimate_with_contact = eps * pole_plus_contact
        estimate_without_contact = eps * pole_only
        rows.append(
            {
                "epsilon": eps,
                "estimate_with_contact": estimate_with_contact,
                "estimate_without_contact": estimate_without_contact,
                "abs_error_with_contact": abs(estimate_with_contact - predicted),
                "abs_error_without_contact": abs(estimate_without_contact - predicted),
                "epsilon_times_contact": eps * contact_term(family, x),
            }
        )
    return rows


def general_basis_witness(family: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    transform = np.asarray(
        [
            [1.2, 0.1, -0.2, 0.05],
            [0.0, 0.9, 0.15, -0.10],
            [0.2, -0.05, 1.1, 0.08],
            [-0.1, 0.12, 0.04, 0.95],
        ],
        dtype=float,
    )
    inv_t = np.linalg.inv(transform)
    k1_t = inv_t @ family["K1"] @ transform
    r_t = inv_t @ base["right_null_vector"]
    l_t = base["left_null_covector"] @ transform
    s_t = family["source_covector"] @ transform
    h_t = inv_t @ family["higgs_vector"]
    transformed = residue_formula(k1_t, s_t, h_t, l_t, r_t)
    return {
        "transform": transform.tolist(),
        "transformed_residue": transformed,
        "abs_residue_error": abs(transformed["residue"] - base["source_higgs_residue"]["residue"]),
        "abs_denominator_error": abs(transformed["kprime_denominator"] - base["source_higgs_residue"]["kprime_denominator"]),
        "abs_numerator_error": abs(
            transformed["source_projection_numerator"]
            - base["source_higgs_residue"]["source_projection_numerator"]
        ),
    }


def block_preserving_witness(family: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    u = np.asarray(
        [
            [1.10, 0.20, -0.10],
            [-0.05, 0.95, 0.12],
            [0.08, -0.04, 1.05],
        ],
        dtype=float,
    )
    transform = np.eye(4)
    transform[1:, 1:] = u
    inv_t = np.linalg.inv(transform)
    k0_t = inv_t @ family["K0"] @ transform
    k1_t = inv_t @ family["K1"] @ transform
    row_t = schur_row_from_blocks(k0_t, k1_t)
    return {
        "orthogonal_block_transform": u.tolist(),
        "D_eff_at_pole": row_t["D_eff_at_pole"],
        "D_eff_prime_at_pole": row_t["D_eff_prime_at_pole"],
        "abs_schur_derivative_error": abs(
            row_t["D_eff_prime_at_pole"] - base["schur_row"]["D_eff_prime_at_pole"]
        ),
        "abs_schur_pole_error": abs(row_t["D_eff_at_pole"] - base["schur_row"]["D_eff_at_pole"]),
    }


def forbidden_import_firewall(proof_inputs: list[str]) -> dict[str, Any]:
    joined = "\n".join(proof_inputs).lower()
    hits = [item for item in FORBIDDEN_PROOF_INPUTS if item.lower() in joined]
    flags = {
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_y_t_bare": False,
        "used_alpha_lm": False,
        "used_plaquette_or_u0": False,
        "used_observed_target_selectors": False,
        "used_alias_imports": False,
    }
    return {
        "proof_inputs": proof_inputs,
        "forbidden_string_hits_in_proof_inputs": hits,
        "flags": flags,
        "firewall_passed": not hits and all(value is False for value in flags.values()),
    }


def parent_summary(certs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        name: {
            "path": PARENTS[name],
            "actual_current_surface_status": status(cert),
            "proposal_allowed": cert.get("proposal_allowed"),
            "bare_retained_allowed": cert.get("bare_retained_allowed"),
        }
        for name, cert in certs.items()
    }


def main() -> int:
    print("PR #230 Block70 Schur/Feshbach K-prime residue theorem")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]

    family = make_kernel_family()
    schur_row = schur_row_from_blocks(family["K0"], family["K1"])
    right_null = schur_row["right_null_vector"]
    left_null = schur_row["left_null_covector"]
    null_residual_right = float(np.linalg.norm(family["K0"] @ right_null))
    null_residual_left = float(np.linalg.norm(left_null @ family["K0"]))
    singular_values = np.linalg.svd(family["K0"], compute_uv=False)
    c_block_det = float(np.linalg.det(family["K0"][1:, 1:]))

    source_higgs_residue = residue_formula(
        family["K1"],
        family["source_covector"],
        family["higgs_vector"],
        left_null,
        right_null,
    )
    source_source_residue = residue_formula(
        family["K1"],
        family["source_covector"],
        family["source_vector"],
        left_null,
        right_null,
    )
    higgs_higgs_residue = residue_formula(
        family["K1"],
        family["higgs_covector"],
        family["higgs_vector"],
        left_null,
        right_null,
    )

    limit_rows = residue_limit_rows(
        family,
        family["source_covector"],
        family["higgs_vector"],
        source_higgs_residue["residue"],
    )

    base = {
        "schur_row": schur_row,
        "right_null_vector": right_null,
        "left_null_covector": left_null,
        "source_higgs_residue": source_higgs_residue,
    }
    general_basis = general_basis_witness(family, base)
    block_basis = block_preserving_witness(family, base)
    proof_inputs = [
        "same-surface analytic scalar kernel family K(x) on the Cl(3)/Z3 source surface",
        "strict Schur/Feshbach block partition with C(pole) invertible",
        "simple isolated zero eigenvalue at x_pole",
        "left/right null vectors and K-prime derivative row",
        "analytic contact terms separated before taking residues",
    ]
    firewall = forbidden_import_firewall(proof_inputs)

    schur_equals_lr = abs(
        schur_row["D_eff_prime_at_pole"] - source_higgs_residue["kprime_denominator"]
    )
    latest_limit_error = limit_rows[-1]["abs_error_with_contact"]
    source_residue_positive = source_source_residue["residue"] > 0.0

    schur_parent_loaded = (
        parents["schur_complement_kprime_sufficiency"].get("schur_sufficiency_theorem_passed")
        is True
        and parents["schur_complement_kprime_sufficiency"].get("proposal_allowed") is False
    )
    row_contract_open = (
        parents["schur_kernel_row_contract_gate"].get("schur_kernel_row_contract_gate_passed")
        is False
        and parents["schur_kernel_row_contract_gate"].get("proposal_allowed") is False
    )
    builder_rows_absent = (
        parents["source_higgs_certificate_builder"].get("input_present") is False
        and parents["source_higgs_certificate_builder"].get("proposal_allowed") is False
    )
    assembly_open = (
        parents["full_positive_closure_assembly_gate"].get("proposal_allowed") is False
        and parents["full_positive_closure_assembly_gate"].get("current_evaluation", {}).get("assembly_passed")
        is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("schur-sufficiency-parent-loaded", schur_parent_loaded, status(parents["schur_complement_kprime_sufficiency"]))
    report("schur-row-contract-still-open", row_contract_open, status(parents["schur_kernel_row_contract_gate"]))
    report("source-higgs-builder-rows-absent", builder_rows_absent, status(parents["source_higgs_certificate_builder"]))
    report("assembly-gate-still-open", assembly_open, status(parents["full_positive_closure_assembly_gate"]))
    report("orthogonal-block-invertible", abs(c_block_det) > 1.0e-6, f"det(C)={c_block_det:.12g}")
    report("simple-zero-eigenvalue", singular_values[0] > 1.0e-2 and singular_values[-1] < 1.0e-12, f"singular_values={singular_values.tolist()}")
    report("left-right-null-vectors-valid", max(null_residual_left, null_residual_right) < 1.0e-12, f"left={null_residual_left:.3e} right={null_residual_right:.3e}")
    report("nonzero-kprime-denominator", abs(source_higgs_residue["kprime_denominator"]) > 1.0e-8, f"den={source_higgs_residue['kprime_denominator']:.12g}")
    report("schur-derivative-equals-left-right-kprime-row", schur_equals_lr < 1.0e-12, f"error={schur_equals_lr:.3e}")
    report("source-source-lsz-residue-positive-in-witness", source_residue_positive, f"Res_ss={source_source_residue['residue']:.12g}")
    report("laurent-limit-matches-residue-with-contact-separated", latest_limit_error < 1.0e-5, f"error={latest_limit_error:.3e}")
    report("general-basis-invariance", general_basis["abs_residue_error"] < 1.0e-12, f"error={general_basis['abs_residue_error']:.3e}")
    report("block-preserving-schur-row-invariance", block_basis["abs_schur_derivative_error"] < 1.0e-12, f"error={block_basis['abs_schur_derivative_error']:.3e}")
    report("forbidden-import-firewall", firewall["firewall_passed"], str(firewall))

    theorem_formula = {
        "variable": "x = p^2 - p_pole^2, or the repo row's declared scalar-pole variable",
        "connected_row_convention": "C_ab(x) = a K(x)^(-1) b + analytic contact",
        "residue_definition": "Res C_ab = lim_{x -> x_pole} (x - x_pole) C_ab(x)",
        "formula": "Res C_ab = (a r) (l b) / (l K_prime(x_pole) r)",
        "sign_note": (
            "If a row defines the denominator as p_pole^2 - p^2 or uses "
            "C = -K^{-1}, the recorded row must carry that sign convention; "
            "with the convention above no extra minus sign appears."
        ),
        "one_source_schur_formula": (
            "For K=[[A,B],[D,C]], D_eff=A-B C^{-1}D and "
            "Res C_sH = (h_s - B C^{-1} h_Q) / D_eff_prime at the pole."
        ),
    }

    result = {
        "actual_current_surface_status": (
            "exact-support / Block70 Schur-Feshbach K-prime residue theorem; physical rows absent"
        ),
        "conditional_surface_status": (
            "If future same-surface Cl(3)/Z3 rows certify an analytic scalar "
            "kernel, simple isolated pole, left/right null vectors, K-prime "
            "row, source/Higgs projections, and contact separation, then the "
            "source-Higgs pole residue is fixed by the theorem formula."
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This theorem reduces the residue to concrete same-surface rows, "
            "but those physical Schur/Feshbach rows and the canonical-Higgs "
            "bridge are not present on the current PR230 surface."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "theorem_formula": theorem_formula,
        "minimal_hypotheses": [
            "same-surface Cl(3)/Z3 scalar kernel family K(x)",
            "analytic K(x) in the pole variable near x_pole",
            "analytic contact terms separated from the pole part",
            "simple isolated zero eigenvalue K(x_pole) r = 0, l K(x_pole) = 0",
            "nonzero derivative row l K_prime(x_pole) r",
            "source and Higgs probe projections supplied in the same basis and convention",
            "declared pole-variable and inverse-kernel sign convention",
        ],
        "certificate_field_map": {
            "same_surface": ["same_surface_cl3_z3", "phase"],
            "analytic_kernel": ["kernel_family_variable", "schur_form", "partition_certificate"],
            "simple_isolated_pole": ["pole_control.isolated_scalar_pole_passed", "pole_control.pole_location_x"],
            "left_right_vectors": ["left_null_covector", "right_null_vector", "left_right_normalization_convention"],
            "kprime_row": ["K_prime_at_pole or D_eff_prime_at_pole", "kprime_denominator"],
            "source_higgs_projection": ["source_projection_numerator", "source_coordinate", "canonical_higgs_operator.operator_id"],
            "contact_separation": ["analytic_contact_terms_separated", "pole_residue_rows"],
            "lsz_convention": ["Dprime_ss_at_pole", "Res_C_ss", "selected_source_side_normalization"],
            "forbidden_import_firewall": list(firewall["flags"].keys()),
        },
        "toy_witness": {
            "x_pole": family["x_pole"],
            "K0": family["K0"].tolist(),
            "K1": family["K1"].tolist(),
            "K2": family["K2"].tolist(),
            "singular_values_K0": singular_values.tolist(),
            "schur_row": {
                key: (value.tolist() if isinstance(value, np.ndarray) else value)
                for key, value in schur_row.items()
            },
            "source_higgs_residue": source_higgs_residue,
            "source_source_residue": source_source_residue,
            "higgs_higgs_residue": higgs_higgs_residue,
            "laurent_limit_rows": limit_rows,
            "general_basis_witness": general_basis,
            "block_preserving_schur_witness": block_basis,
        },
        "parent_certificates": parent_summary(parents),
        "forbidden_import_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not assert that current PR230 physical Schur rows exist",
            "does not identify O_sp with O_H",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, observed target selectors, or alias imports as load-bearing inputs",
        ],
        "exact_next_action": (
            "Produce same-surface physical Schur/Feshbach rows carrying the "
            "mapped certificate fields, or produce source-Higgs C_sH/C_HH "
            "pole rows; then rerun the builder, Gram-purity postprocessor, "
            "assembly gate, and campaign status gate."
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
