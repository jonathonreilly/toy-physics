#!/usr/bin/env python3
"""
PR #230 delta_perp tomography correction builder.

The same-source W-response readout needs

    y_h = g_2 R_t/(sqrt(2) R_W) - delta_perp,
    delta_perp = sum_i y_i kappa_i / kappa_h

over neutral scalar directions orthogonal to the canonical Higgs radial mode.
This runner defines the small production-row certificate that can supply that
correction.  Scout mode proves the algebra and firewalls on synthetic rows.
Strict mode requires a real same-surface tomography certificate and fails
honestly while that input is absent.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_delta_perp_tomography_rows_2026-05-04.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_delta_perp_tomography_correction_builder_2026-05-04.json"
FUTURE_CORRECTION = (
    ROOT / "outputs" / "yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json"
)

PARENTS = {
    "neutral_scalar_top_coupling_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
    "non_source_response_rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "same_source_w_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_H_unit_or_Ward_authority",
    "used_yt_ward_identity",
    "used_y_t_bare",
    "used_observed_y_t_or_m_t_as_selector",
    "used_observed_WZ_masses_as_selector",
    "used_alpha_lm_plaquette_or_u0",
    "set_delta_perp_zero_without_certificate",
    "set_kappa_s_equal_one",
    "set_c2_equal_one",
    "set_z_match_equal_one",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def vector(value: Any) -> list[float]:
    if not isinstance(value, list):
        return []
    if not all(finite(item) for item in value):
        return []
    return [float(item) for item in value]


def matrix_rank(rows: Any, *, tol: float = 1.0e-10) -> int:
    if not isinstance(rows, list) or not rows:
        return 0
    mat = [vector(row) for row in rows]
    if not mat or any(not row for row in mat):
        return 0
    ncols = len(mat[0])
    if any(len(row) != ncols for row in mat):
        return 0

    # Small Gaussian elimination avoids adding a numpy dependency to this
    # certificate runner.
    work = [row[:] for row in mat]
    rank = 0
    col = 0
    while rank < len(work) and col < ncols:
        pivot = max(range(rank, len(work)), key=lambda idx: abs(work[idx][col]))
        if abs(work[pivot][col]) <= tol:
            col += 1
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][col]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row_index in range(len(work)):
            if row_index == rank:
                continue
            factor = work[row_index][col]
            work[row_index] = [
                value - factor * pivot_component
                for value, pivot_component in zip(work[row_index], work[rank])
            ]
        rank += 1
        col += 1
    return rank


def compute_delta(candidate: dict[str, Any]) -> dict[str, Any]:
    kappa = vector(candidate.get("source_overlap_vector"))
    sigma_kappa = vector(candidate.get("source_overlap_sigma"))
    y = vector(candidate.get("top_coupling_vector"))
    sigma_y = vector(candidate.get("top_coupling_sigma"))
    canonical_index = int(candidate.get("canonical_higgs_index", 0))
    n = len(kappa)
    if not (n and len(y) == n and len(sigma_kappa) == n and len(sigma_y) == n):
        return {"valid": False, "reason": "vectors absent or length-mismatched"}
    if canonical_index < 0 or canonical_index >= n:
        return {"valid": False, "reason": "canonical index out of range"}
    k_h = kappa[canonical_index]
    if abs(k_h) <= 1.0e-14:
        return {"valid": False, "reason": "canonical kappa_h is zero"}

    orthogonal_indices = [index for index in range(n) if index != canonical_index]
    numerator = sum(y[index] * kappa[index] for index in orthogonal_indices)
    delta = numerator / k_h

    variance = 0.0
    for index in orthogonal_indices:
        grad_y = kappa[index] / k_h
        grad_kappa = y[index] / k_h
        variance += grad_y * grad_y * sigma_y[index] * sigma_y[index]
        variance += grad_kappa * grad_kappa * sigma_kappa[index] * sigma_kappa[index]
    grad_kh = -delta / k_h
    variance += grad_kh * grad_kh * sigma_kappa[canonical_index] * sigma_kappa[canonical_index]

    return {
        "valid": True,
        "canonical_higgs_index": canonical_index,
        "orthogonal_indices": orthogonal_indices,
        "kappa_h": k_h,
        "orthogonal_numerator": numerator,
        "orthogonal_correction_delta_perp": delta,
        "sigma_delta_perp": math.sqrt(max(variance, 0.0)),
    }


def validate_firewall(candidate: dict[str, Any]) -> dict[str, Any]:
    firewall = candidate.get("firewall", {})
    checks = {field: firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS}
    return {
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [field for field, ok in checks.items() if not ok],
    }


def validate_candidate(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["delta_perp tomography rows absent"]}

    basis = candidate.get("neutral_scalar_basis", [])
    kappa = vector(candidate.get("source_overlap_vector"))
    y = vector(candidate.get("top_coupling_vector"))
    response_rows = candidate.get("response_matrix_rows", [])
    rank = matrix_rank(response_rows)
    delta = compute_delta(candidate)
    firewall = validate_firewall(candidate)
    identity = candidate.get("identity_certificates", {})
    n = len(basis) if isinstance(basis, list) else 0
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "delta_perp_tomography_rows",
        "phase_allowed": candidate.get("phase") in {"scout", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "basis_dimension_at_least_two": n >= 2,
        "vectors_match_basis": bool(kappa) and bool(y) and len(kappa) == n and len(y) == n,
        "response_matrix_full_rank": rank >= n and n >= 2,
        "delta_computable": delta.get("valid") is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_identity_passed") is True,
        "orthogonal_basis_identity_passed": identity.get("orthogonal_basis_identity_passed") is True,
        "same_source_sector_overlap_passed": identity.get("same_source_sector_overlap_passed") is True,
        "no_observed_selector_or_forbidden_import": firewall["valid"],
        "proposal_not_authorized_by_input": candidate.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "basis_dimension": n,
        "response_matrix_rank": rank,
        "delta_perp": delta,
        "firewall_validation": firewall,
    }


def correction_certificate(candidate: dict[str, Any], validation: dict[str, Any], method_ref: str) -> dict[str, Any]:
    delta = validation.get("delta_perp", {})
    firewall = candidate.get("firewall", {})
    return {
        "phase": candidate.get("phase"),
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "correction_method": "tomography_correction_row",
        "orthogonal_correction_delta_perp": delta.get("orthogonal_correction_delta_perp"),
        "sigma_delta_perp": delta.get("sigma_delta_perp"),
        "provenance": {
            "method_certificate": method_ref,
            "rank_or_null_authority_passed": validation.get("valid") is True,
            "response_matrix_rank": validation.get("response_matrix_rank"),
            "basis_dimension": validation.get("basis_dimension"),
        },
        "firewall": {
            "used_delta_perp_zero_without_certificate": firewall.get("set_delta_perp_zero_without_certificate"),
            "used_observed_y_t_to_backsolve_delta": firewall.get("used_observed_y_t_or_m_t_as_selector"),
            "used_H_unit_or_Ward_authority": firewall.get("used_H_unit_or_Ward_authority")
            or firewall.get("used_yt_ward_identity"),
            "used_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0"),
            "used_c2_or_zmatch_equal_one": firewall.get("set_c2_equal_one")
            or firewall.get("set_z_match_equal_one"),
        },
    }


def synthetic_scout_candidate() -> dict[str, Any]:
    return {
        "certificate_kind": "delta_perp_tomography_rows",
        "phase": "scout",
        "same_surface_cl3_z3": True,
        "same_source_coordinate": True,
        "neutral_scalar_basis": ["O_H", "O_chi_1", "O_chi_2"],
        "canonical_higgs_index": 0,
        "source_overlap_vector": [0.72, 0.11, -0.06],
        "source_overlap_sigma": [0.004, 0.003, 0.002],
        "top_coupling_vector": [0.9176, -0.28, 0.14],
        "top_coupling_sigma": [0.006, 0.025, 0.020],
        "response_matrix_rows": [
            [0.72, 0.11, -0.06],
            [1.00, 0.00, 0.00],
            [0.00, 1.00, 0.00],
        ],
        "identity_certificates": {
            "canonical_higgs_identity_passed": True,
            "orthogonal_basis_identity_passed": True,
            "same_source_sector_overlap_passed": True,
        },
        "proposal_allowed": False,
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
    }


def rejection_witnesses() -> dict[str, Any]:
    base = synthetic_scout_candidate()

    source_only = json.loads(json.dumps(base))
    source_only["response_matrix_rows"] = [source_only["source_overlap_vector"]]

    no_identity = json.loads(json.dumps(base))
    no_identity["identity_certificates"]["canonical_higgs_identity_passed"] = False

    observed_selector = json.loads(json.dumps(base))
    observed_selector["firewall"]["used_observed_y_t_or_m_t_as_selector"] = True

    mismatched_source = json.loads(json.dumps(base))
    mismatched_source["same_source_coordinate"] = False

    zero_kappa_h = json.loads(json.dumps(base))
    zero_kappa_h["source_overlap_vector"][0] = 0.0

    return {
        "source-only-rank-deficient": validate_candidate(source_only, require_production=False),
        "canonical-identity-absent": validate_candidate(no_identity, require_production=False),
        "observed-selector": validate_candidate(observed_selector, require_production=False),
        "mismatched-source": validate_candidate(mismatched_source, require_production=False),
        "zero-kappa-h": validate_candidate(zero_kappa_h, require_production=False),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scout", action="store_true", help="run synthetic tomography correction scout")
    parser.add_argument("--strict", action="store_true", help="require production tomography rows")
    parser.add_argument(
        "--emit-correction-certificate",
        action="store_true",
        help="write the future orthogonal-correction certificate when validation is strict-production valid",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    print("PR #230 delta_perp tomography correction builder")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    parent_statuses = {name: status(cert) for name, cert in parents.items()}
    candidate = synthetic_scout_candidate() if args.scout else load_json(args.input)
    validation = validate_candidate(candidate, require_production=args.strict)
    correction = correction_certificate(candidate, validation, display(args.input)) if validation["present"] else {}
    rejections = rejection_witnesses()
    rejections_ok = all(result["valid"] is False for result in rejections.values())

    scout_delta_ok = False
    if args.scout and validation["valid"]:
        delta = validation["delta_perp"]
        expected = ((-0.28 * 0.11) + (0.14 * -0.06)) / 0.72
        scout_delta_ok = abs(delta["orthogonal_correction_delta_perp"] - expected) < 1.0e-14

    strict_gate_passed = args.strict and validation["valid"]
    if args.emit_correction_certificate and strict_gate_passed:
        FUTURE_CORRECTION.parent.mkdir(parents=True, exist_ok=True)
        FUTURE_CORRECTION.write_text(
            json.dumps(correction, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("source-only-tomography-currently-blocked", "tomography gate not passed" in parent_statuses["neutral_scalar_top_coupling_tomography"], parent_statuses["neutral_scalar_top_coupling_tomography"])
    report("rank-repair-sufficiency-available", "rank-repair sufficiency theorem" in parent_statuses["non_source_response_rank_repair"], parent_statuses["non_source_response_rank_repair"])
    report("w-orthogonal-correction-gate-open", "orthogonal-correction gate not passed" in parent_statuses["same_source_w_response_orthogonal_correction"], parent_statuses["same_source_w_response_orthogonal_correction"])
    report("lightweight-w-readout-open", "lightweight same-source W-response readout" in parent_statuses["same_source_w_lightweight_readout"], parent_statuses["same_source_w_lightweight_readout"])
    if args.strict:
        report("strict-candidate-present", validation["present"], display(args.input))
        report("strict-candidate-valid", validation["valid"], f"failed={validation.get('failed_checks', [])}")
    elif args.scout:
        report("scout-candidate-built", validation["present"], "synthetic tomography rows")
        report("scout-candidate-valid", validation["valid"], f"failed={validation.get('failed_checks', [])}")
        report("scout-delta-matches-direct-arithmetic", scout_delta_ok, str(validation.get("delta_perp", {})))
    else:
        report("future-tomography-row-certificate-absent", not validation["present"], display(args.input))
        report("current-mode-valid-if-present", (not validation["present"]) or validation["valid"], f"failed={validation.get('failed_checks', [])}")
    report("adversarial-tomography-shortcuts-rejected", rejections_ok, str({name: row["failed_checks"] for name, row in rejections.items()}))
    report("strict-production-correction-not-claimed", not strict_gate_passed if not args.strict else strict_gate_passed, f"strict_gate_passed={strict_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "scout-pass / delta_perp tomography correction builder"
            if args.scout and validation["valid"] and scout_delta_ok
            else "strict-pass / delta_perp tomography correction production rows"
            if strict_gate_passed
            else "open / delta_perp tomography correction production rows absent"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This builder supplies a correction-row contract only.  Production "
            "proposal still requires real same-surface tomography rows, W rows, "
            "matching/running, and retained-route authorization."
        ),
        "bare_retained_allowed": False,
        "delta_perp_tomography_builder_passed": validation["valid"] and rejections_ok,
        "strict_delta_perp_tomography_gate_passed": strict_gate_passed,
        "input_certificate": display(args.input),
        "future_orthogonal_correction_certificate": display(FUTURE_CORRECTION),
        "validation": validation,
        "correction_certificate_candidate": correction,
        "rejection_witnesses": rejections,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not create production tomography rows in scout/current mode",
            "does not set delta_perp to zero",
            "does not backsolve delta_perp from observed y_t or m_t",
            "does not use H_unit, yt_ward_identity, y_t_bare, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            f"Supply {display(DEFAULT_INPUT)} with full-rank neutral-scalar "
            "tomography rows, then rerun this builder in strict mode and emit "
            f"{display(FUTURE_CORRECTION)} for the W-response correction gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(args.output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
