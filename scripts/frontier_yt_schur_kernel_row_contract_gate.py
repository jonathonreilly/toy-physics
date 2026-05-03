#!/usr/bin/env python3
"""
PR #230 Schur kernel row contract gate.

The Schur-complement K'(pole) theorem is useful only after the same-surface
neutral scalar kernel rows exist.  This runner defines the executable future
row contract, validates an in-memory positive witness, and records that the
current PR #230 surface has no such row file.  It is infrastructure support,
not y_t closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_schur_kernel_row_contract_gate_2026-05-03.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_schur_scalar_kernel_rows_2026-05-03.json"

PARENTS = {
    "schur_complement_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "kprime_closure_attempt": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
    "scalar_denominator_closure_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_hunit_matrix_element_readout",
    "used_yt_ward_identity",
    "used_observed_top_or_yukawa_as_selector",
    "used_alpha_lm_or_plaquette_u0",
    "used_reduced_cold_pilots_as_production_evidence",
    "set_c2_equal_one",
    "set_z_match_equal_one",
    "set_kappa_s_equal_one",
    "set_cos_theta_equal_one",
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


def load_json(rel_or_path: str | Path) -> dict[str, Any]:
    path = Path(rel_or_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def acceptance_schema() -> dict[str, Any]:
    return {
        "candidate_rows_path": display(FUTURE_ROWS),
        "status": "support-only row contract; not retained or proposed_retained closure",
        "required_top_level": {
            "phase": "production or theorem",
            "same_surface_cl3_z3": True,
            "source_coordinate": "the scalar source coordinate used by the FH/LSZ source response",
            "schur_form": "one_orthogonal_mode_v1 or precontracted_matrix_v1",
        },
        "partition_certificate": [
            "same_surface_neutral_scalar_kernel_partition_passed=true",
            "source_pole_coordinate_certified=true",
            "orthogonal_neutral_block_certified=true",
            "source_orthogonal_covariance_included=true",
        ],
        "pole_control": [
            "isolated_scalar_pole_passed=true",
            "fv_ir_zero_mode_order_certified=true",
            "finite pole_location_x",
        ],
        "schur_rows_one_orthogonal_mode_v1": [
            "A_at_pole",
            "B_at_pole",
            "C_at_pole",
            "A_prime_at_pole",
            "B_prime_at_pole",
            "C_prime_at_pole",
        ],
        "schur_rows_precontracted_matrix_v1": [
            "A_at_pole",
            "B_Cinv_B_at_pole",
            "A_prime_at_pole",
            "two_Bprime_Cinv_B_at_pole",
            "B_Cinv_Cprime_Cinv_B_at_pole",
        ],
        "computed_quantities": [
            "D_eff(pole)",
            "D_eff_prime(pole)",
            "source-pole inverse residue only; no O_sp=O_H claim",
        ],
        "claim_firewall": [f"{field}=false" for field in FORBIDDEN_FALSE_FIELDS],
    }


def compute_schur_rows(rows: dict[str, Any]) -> dict[str, Any]:
    scalar_keys = (
        "A_at_pole",
        "B_at_pole",
        "C_at_pole",
        "A_prime_at_pole",
        "B_prime_at_pole",
        "C_prime_at_pole",
    )
    contraction_keys = (
        "A_at_pole",
        "B_Cinv_B_at_pole",
        "A_prime_at_pole",
        "two_Bprime_Cinv_B_at_pole",
        "B_Cinv_Cprime_Cinv_B_at_pole",
    )
    if all(finite(rows.get(key)) for key in scalar_keys):
        a0 = float(rows["A_at_pole"])
        b0 = float(rows["B_at_pole"])
        c0 = float(rows["C_at_pole"])
        a1 = float(rows["A_prime_at_pole"])
        b1 = float(rows["B_prime_at_pole"])
        c1 = float(rows["C_prime_at_pole"])
        if c0 == 0.0:
            return {"valid_numeric_form": False, "reason": "C_at_pole is zero"}
        return {
            "valid_numeric_form": True,
            "schur_form": "one_orthogonal_mode_v1",
            "D_eff_at_pole": a0 - b0 * b0 / c0,
            "D_eff_prime_at_pole": a1 - 2.0 * b0 * b1 / c0 + (b0 * b0 * c1) / (c0 * c0),
        }
    if all(finite(rows.get(key)) for key in contraction_keys):
        return {
            "valid_numeric_form": True,
            "schur_form": "precontracted_matrix_v1",
            "D_eff_at_pole": float(rows["A_at_pole"]) - float(rows["B_Cinv_B_at_pole"]),
            "D_eff_prime_at_pole": (
                float(rows["A_prime_at_pole"])
                - float(rows["two_Bprime_Cinv_B_at_pole"])
                + float(rows["B_Cinv_Cprime_Cinv_B_at_pole"])
            ),
        }
    return {
        "valid_numeric_form": False,
        "reason": "missing one_orthogonal_mode_v1 or precontracted_matrix_v1 Schur row keys",
    }


def validate_candidate(data: dict[str, Any]) -> dict[str, Any]:
    if not data:
        return {"present": False, "valid": False, "reasons": ["Schur scalar kernel row file absent"]}

    partition = data.get("partition_certificate", {})
    pole = data.get("pole_control", {})
    firewall = data.get("firewall", data.get("forbidden_import_firewall", {}))
    rows = data.get("schur_rows", {})
    schur = compute_schur_rows(rows if isinstance(rows, dict) else {})
    tolerance = data.get("pole_residual_tolerance", 1.0e-8)
    finite_tolerance = finite(tolerance) and float(tolerance) >= 0.0
    d_eff = schur.get("D_eff_at_pole")
    d_prime = schur.get("D_eff_prime_at_pole")
    checks = {
        "phase_supported": data.get("phase") in {"production", "theorem"},
        "same_surface_cl3_z3": data.get("same_surface_cl3_z3") is True,
        "source_coordinate_named": isinstance(data.get("source_coordinate"), str)
        and bool(data.get("source_coordinate")),
        "neutral_scalar_partition_passed": partition.get(
            "same_surface_neutral_scalar_kernel_partition_passed"
        )
        is True,
        "source_pole_coordinate_certified": partition.get("source_pole_coordinate_certified") is True,
        "orthogonal_neutral_block_certified": partition.get("orthogonal_neutral_block_certified") is True,
        "source_orthogonal_covariance_included": partition.get(
            "source_orthogonal_covariance_included"
        )
        is True,
        "isolated_scalar_pole_passed": pole.get("isolated_scalar_pole_passed") is True,
        "fv_ir_zero_mode_order_certified": pole.get("fv_ir_zero_mode_order_certified") is True,
        "finite_pole_location": finite(pole.get("pole_location_x")),
        "valid_schur_numeric_form": schur.get("valid_numeric_form") is True,
        "finite_pole_residual_tolerance": finite_tolerance,
        "pole_condition_satisfied": (
            finite(d_eff) and finite_tolerance and abs(float(d_eff)) <= float(tolerance)
        ),
        "finite_nonzero_inverse_residue": finite(d_prime) and float(d_prime) != 0.0,
        "source_lsz_only_boundary": data.get("source_lsz_only_boundary") is True,
        "does_not_claim_physical_yukawa_closure": data.get("claims_physical_yukawa_closure") is False,
    }
    checks.update({f"forbidden_{field}_false": firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS})
    reasons = [key for key, ok in checks.items() if not ok]
    return {
        "present": True,
        "valid": not reasons,
        "checks": checks,
        "reasons": reasons,
        "computed_schur": schur,
    }


def synthetic_positive_candidate() -> dict[str, Any]:
    c0 = 1.35
    b0 = 0.24
    return {
        "phase": "theorem",
        "same_surface_cl3_z3": True,
        "source_coordinate": "synthetic_source_pole_coordinate",
        "schur_form": "one_orthogonal_mode_v1",
        "partition_certificate": {
            "same_surface_neutral_scalar_kernel_partition_passed": True,
            "source_pole_coordinate_certified": True,
            "orthogonal_neutral_block_certified": True,
            "source_orthogonal_covariance_included": True,
        },
        "pole_control": {
            "isolated_scalar_pole_passed": True,
            "fv_ir_zero_mode_order_certified": True,
            "pole_location_x": -0.37,
        },
        "schur_rows": {
            "A_at_pole": b0 * b0 / c0,
            "B_at_pole": b0,
            "C_at_pole": c0,
            "A_prime_at_pole": 0.31,
            "B_prime_at_pole": -0.08,
            "C_prime_at_pole": 0.22,
        },
        "pole_residual_tolerance": 1.0e-12,
        "source_lsz_only_boundary": True,
        "claims_physical_yukawa_closure": False,
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
    }


def rejection_witness() -> dict[str, Any]:
    source_only = {
        "name": "source-only C_ss pole data without partition rows",
        "candidate": {
            "phase": "production",
            "same_surface_cl3_z3": True,
            "source_coordinate": "s",
            "scalar_source_two_point_residue": 3.2,
            "source_lsz_only_boundary": True,
            "claims_physical_yukawa_closure": False,
            "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
        },
        "validation": validate_candidate(
            {
                "phase": "production",
                "same_surface_cl3_z3": True,
                "source_coordinate": "s",
                "source_lsz_only_boundary": True,
                "claims_physical_yukawa_closure": False,
                "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
            }
        ),
        "rejection": "C_ss alone does not supply A/B/C partition rows or K'(pole).",
    }
    kappa_fiat = {
        "name": "kappa_s=1 shortcut",
        "candidate": {
            "phase": "theorem",
            "same_surface_cl3_z3": True,
            "source_coordinate": "s",
            "set_kappa_s_equal_one": True,
        },
        "rejection": "setting kappa_s=1 is a forbidden normalization import.",
    }
    return {"source_only": source_only, "kappa_fiat": kappa_fiat}


def main() -> int:
    print("PR #230 Schur kernel row contract gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    candidate = load_json(FUTURE_ROWS)
    candidate_validation = validate_candidate(candidate)
    positive_validation = validate_candidate(synthetic_positive_candidate())
    witnesses = rejection_witness()

    schur_parent_loaded = (
        "Schur-complement K-prime sufficiency theorem"
        in status(parents["schur_complement_kprime_sufficiency"])
        and parents["schur_complement_kprime_sufficiency"].get("schur_sufficiency_theorem_passed") is True
    )
    kprime_still_open = "K-prime closure attempt blocked" in status(parents["kprime_closure_attempt"])
    scalar_denominator_still_open = "scalar denominator theorem closure attempt blocked" in status(
        parents["scalar_denominator_closure_attempt"]
    )
    source_identifiability_boundary_loaded = "source-functional LSZ identifiability theorem" in status(
        parents["source_functional_lsz_identifiability"]
    )
    higgs_identity_still_blocks = (
        "canonical-Higgs pole identity gate blocking" in status(parents["fh_lsz_higgs_pole_identity"])
        and parents["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
    )
    row_contract_gate_passed = candidate_validation["valid"] is True
    current_closure_gate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-sufficiency-parent-loaded", schur_parent_loaded, status(parents["schur_complement_kprime_sufficiency"]))
    report("kprime-still-open", kprime_still_open, status(parents["kprime_closure_attempt"]))
    report("scalar-denominator-still-open", scalar_denominator_still_open, status(parents["scalar_denominator_closure_attempt"]))
    report("source-identifiability-boundary-loaded", source_identifiability_boundary_loaded, status(parents["source_functional_lsz_identifiability"]))
    report("canonical-higgs-identity-still-blocks", higgs_identity_still_blocks, status(parents["fh_lsz_higgs_pole_identity"]))
    report("synthetic-positive-row-contract-accepted", positive_validation["valid"] is True, str(positive_validation.get("reasons", [])))
    report("source-only-shortcut-rejected", witnesses["source_only"]["validation"]["valid"] is False, witnesses["source_only"]["rejection"])
    if candidate_validation["present"]:
        report("current-schur-kernel-row-file-valid", candidate_validation["valid"] is True, str(candidate_validation.get("reasons", [])))
    else:
        report("current-schur-kernel-row-file-absent", True, display(FUTURE_ROWS))
    report("schur-kernel-row-contract-gate-status-recorded", True, f"gate_passed={row_contract_gate_passed}")
    report("support-not-current-closure", not current_closure_gate_passed, f"current_closure_gate_passed={current_closure_gate_passed}")

    status_text = (
        "exact-support / Schur kernel row contract passed; retained closure still not claimed"
        if row_contract_gate_passed
        else "open / Schur kernel row contract gate not passed; current rows absent"
    )
    result = {
        "actual_current_surface_status": status_text,
        "verdict": (
            "The Schur K'(pole) sufficiency theorem now has an executable "
            "future row contract.  Current PR #230 has no same-surface Schur "
            "scalar kernel row file, so the contract gate is not passed.  "
            "The gate validates an in-memory positive witness and rejects "
            "source-only C_ss or kappa_s=1 shortcuts.  Even a future passed "
            "row contract is source-pole LSZ support only until the retained "
            "route also supplies the canonical-Higgs/source identity or an "
            "allowed physical-response bridge."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current row file is absent and the canonical-Higgs identity "
            "gate remains open; the artifact is an input contract, not y_t closure."
        ),
        "bare_retained_allowed": False,
        "schur_kernel_row_contract_gate_passed": row_contract_gate_passed,
        "candidate_rows_present": candidate_validation["present"],
        "candidate_rows_valid": candidate_validation["valid"],
        "current_closure_gate_passed": current_closure_gate_passed,
        "candidate_validation": candidate_validation,
        "positive_witness_validation": positive_validation,
        "acceptance_schema": acceptance_schema(),
        "rejection_witnesses": witnesses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not infer A/B/C Schur rows from source-only C_ss data",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Produce same-surface neutral scalar Schur rows A/B/C and pole "
            "derivatives, or precontracted matrix Schur rows, with partition, "
            "pole-control, and firewall certificates; then rerun this gate and "
            "the retained-closure route certificate."
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
