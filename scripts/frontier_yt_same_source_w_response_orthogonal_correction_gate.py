#!/usr/bin/env python3
"""
PR #230 same-source W-response orthogonal-correction gate.

The same-source W response cancels scalar-source normalization, but it reads
the canonical Higgs Yukawa plus any orthogonal neutral top-coupling correction.
This gate makes the subtraction contract explicit and rejects the current
surface until a real correction/null/purity certificate exists.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json"
FUTURE_CORRECTION = ROOT / "outputs" / "yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json"

PARENTS = {
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "neutral_scalar_top_coupling_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
    "non_source_rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_gram_purity_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def symbolic_formula() -> dict[str, Any]:
    y_h, y_x, k_h, k_x, g_2, lam = sp.symbols("y_h y_x k_h k_x g_2 lam", nonzero=True)
    sqrt2 = sp.sqrt(2)
    r_t = (y_h * k_h + y_x * k_x) / sqrt2
    r_w = g_2 * k_h / 2
    raw_w_readout = sp.simplify(g_2 * r_t / (sqrt2 * r_w))
    delta_perp = sp.simplify(y_x * k_x / k_h)
    corrected_readout = sp.simplify(raw_w_readout - delta_perp)
    scale_residual = sp.simplify(
        corrected_readout.subs({k_h: lam * k_h, k_x: lam * k_x}) - corrected_readout
    )
    return {
        "raw_w_readout": str(raw_w_readout),
        "orthogonal_correction": str(delta_perp),
        "corrected_readout": str(corrected_readout),
        "corrected_equals_y_h": corrected_readout == y_h,
        "source_rescaling_residual_zero": scale_residual == 0,
    }


def positive_witness() -> dict[str, Any]:
    g2 = 0.648
    y_h = 0.917
    y_x = -0.32
    k_h = 0.73
    k_x = 0.21
    r_t = (y_h * k_h + y_x * k_x) / math.sqrt(2.0)
    r_w = g2 * k_h / 2.0
    raw_readout = g2 * r_t / (math.sqrt(2.0) * r_w)
    delta = y_x * k_x / k_h
    corrected = raw_readout - delta
    return {
        "input_parameters": {
            "g2": g2,
            "physical_y_h": y_h,
            "orthogonal_top_coupling_y_x": y_x,
            "kappa_h": k_h,
            "kappa_x": k_x,
        },
        "measured_responses": {
            "R_t": r_t,
            "R_W": r_w,
            "raw_same_source_w_readout": raw_readout,
            "orthogonal_correction_delta_perp": delta,
            "corrected_y_h": corrected,
            "absolute_recovery_error": abs(corrected - y_h),
        },
    }


def validate_correction_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["future correction certificate absent"]}

    method = candidate.get("correction_method")
    firewall = candidate.get("firewall", {})
    provenance = candidate.get("provenance", {})
    allowed_method = method in {
        "orthogonal_top_null_theorem",
        "tomography_correction_row",
        "source_higgs_gram_purity",
        "neutral_rank_one_theorem",
    }
    checks = {
        "production_or_exact_support_phase": candidate.get("phase") in {"production", "exact-support"},
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "allowed_correction_method": allowed_method,
        "finite_delta_perp": finite(candidate.get("orthogonal_correction_delta_perp")),
        "method_certificate_present": isinstance(provenance.get("method_certificate"), str)
        and bool(provenance.get("method_certificate")),
        "rank_or_null_authority_passed": provenance.get("rank_or_null_authority_passed") is True,
        "no_delta_zero_without_certificate": firewall.get("used_delta_perp_zero_without_certificate") is False,
        "no_observed_yt_backsolve": firewall.get("used_observed_y_t_to_backsolve_delta") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_or_zmatch_by_fiat": firewall.get("used_c2_or_zmatch_equal_one") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def rejection_witnesses() -> dict[str, Any]:
    zero_by_default = {
        "phase": "exact-support",
        "same_source_coordinate": True,
        "correction_method": "tomography_correction_row",
        "orthogonal_correction_delta_perp": 0.0,
        "provenance": {"method_certificate": "", "rank_or_null_authority_passed": False},
        "firewall": {
            "used_delta_perp_zero_without_certificate": True,
            "used_observed_y_t_to_backsolve_delta": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    observed_backsolve = {
        "phase": "production",
        "same_source_coordinate": True,
        "correction_method": "tomography_correction_row",
        "orthogonal_correction_delta_perp": 0.08,
        "provenance": {"method_certificate": "observed target fit", "rank_or_null_authority_passed": True},
        "firewall": {
            "used_delta_perp_zero_without_certificate": False,
            "used_observed_y_t_to_backsolve_delta": True,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    mismatched_source = {
        "phase": "production",
        "same_source_coordinate": False,
        "correction_method": "tomography_correction_row",
        "orthogonal_correction_delta_perp": -0.04,
        "provenance": {"method_certificate": "future rows", "rank_or_null_authority_passed": True},
        "firewall": {
            "used_delta_perp_zero_without_certificate": False,
            "used_observed_y_t_to_backsolve_delta": False,
            "used_H_unit_or_Ward_authority": False,
            "used_alpha_lm_plaquette_or_u0": False,
            "used_c2_or_zmatch_equal_one": False,
        },
    }
    return {
        "zero_by_default": validate_correction_certificate(zero_by_default),
        "observed_backsolve": validate_correction_certificate(observed_backsolve),
        "mismatched_source": validate_correction_certificate(mismatched_source),
    }


def main() -> int:
    print("PR #230 same-source W-response orthogonal-correction gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    formula = symbolic_formula()
    witness = positive_witness()
    future_candidate = load_json(FUTURE_CORRECTION)
    future_validation = validate_correction_certificate(future_candidate)
    rejections = rejection_witnesses()

    decomposition_ok = (
        parents["same_source_w_response_decomposition"].get(
            "same_source_w_response_decomposition_theorem_passed"
        )
        is True
        and parents["same_source_w_response_decomposition"].get("proposal_allowed") is False
    )
    tomography_open = (
        "neutral scalar top-coupling tomography gate not passed"
        in status(parents["neutral_scalar_top_coupling_tomography"])
        and parents["neutral_scalar_top_coupling_tomography"].get("gate_passed") is False
    )
    rank_repair_support = (
        "non-source response rank-repair sufficiency theorem"
        in status(parents["non_source_rank_repair"])
        and parents["non_source_rank_repair"].get("rank_repair_sufficiency_theorem_passed") is True
    )
    gram_absent = (
        parents["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed") is False
        and parents["source_higgs_gram_purity_postprocess"].get("osp_higgs_gram_purity_gate_passed") is False
    )
    orthogonal_null_absent = (
        parents["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    wz_rows_absent = (
        parents["same_source_wz_response_gate"].get("same_source_wz_response_certificate_gate_passed")
        is False
        and "WZ response measurement-row contract gate"
        in status(parents["wz_response_measurement_row_contract"])
    )
    corrected_witness_ok = witness["measured_responses"]["absolute_recovery_error"] < 1.0e-14
    rejection_checks = {
        name: validation["valid"] is False and validation["present"] is True
        for name, validation in rejections.items()
    }
    current_gate_passed = future_validation["valid"] is True
    theorem_passed = (
        not missing
        and not proposal_allowed
        and decomposition_ok
        and formula["corrected_equals_y_h"]
        and formula["source_rescaling_residual_zero"]
        and corrected_witness_ok
        and all(rejection_checks.values())
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-source-w-decomposition-available", decomposition_ok, status(parents["same_source_w_response_decomposition"]))
    report("exact-corrected-readout-derived", formula["corrected_equals_y_h"], formula["corrected_readout"])
    report("source-rescaling-cancels-after-correction", formula["source_rescaling_residual_zero"], "kappa_h,kappa_x -> lambda kappa_h,lambda kappa_x")
    report("positive-witness-recovers-yh", corrected_witness_ok, f"error={witness['measured_responses']['absolute_recovery_error']:.3g}")
    report("source-only-tomography-still-open", tomography_open, status(parents["neutral_scalar_top_coupling_tomography"]))
    report("rank-repair-support-present", rank_repair_support, status(parents["non_source_rank_repair"]))
    report("gram-purity-correction-absent", gram_absent, "source-Higgs Gram purity rows absent")
    report("orthogonal-null-theorem-absent", orthogonal_null_absent, status(parents["no_orthogonal_top_coupling_selection"]))
    report("wz-response-rows-still-absent", wz_rows_absent, status(parents["same_source_wz_response_gate"]))
    report("future-correction-certificate-absent", not future_validation["present"], str(FUTURE_CORRECTION.relative_to(ROOT)))
    report("zero-delta-without-certificate-rejected", rejection_checks["zero_by_default"], str(rejections["zero_by_default"]["failed_checks"]))
    report("observed-backsolve-rejected", rejection_checks["observed_backsolve"], str(rejections["observed_backsolve"]["failed_checks"]))
    report("mismatched-source-correction-rejected", rejection_checks["mismatched_source"], str(rejections["mismatched_source"]["failed_checks"]))
    report("orthogonal-correction-theorem-passed", theorem_passed, f"theorem_passed={theorem_passed}")
    report("current-correction-gate-not-passed", not current_gate_passed, f"gate_passed={current_gate_passed}")

    result = {
        "actual_current_surface_status": "open / same-source W-response orthogonal-correction gate not passed",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The exact subtraction formula is derived, but no same-source W "
            "response rows or orthogonal-correction/null/purity certificate is present."
        ),
        "bare_retained_allowed": False,
        "orthogonal_correction_theorem_passed": theorem_passed,
        "orthogonal_correction_gate_passed": current_gate_passed,
        "current_closure_gate_passed": False,
        "symbolic_formula": formula,
        "positive_witness": witness,
        "future_correction_certificate": str(FUTURE_CORRECTION.relative_to(ROOT)),
        "future_correction_validation": future_validation,
        "rejection_witnesses": rejections,
        "current_missing_inputs": [
            "same-source W response rows",
            "orthogonal top-coupling null theorem or measured delta_perp correction",
            "source-Higgs Gram-purity correction row",
            "matching/running bridge with certified physical input",
            "retained-route gate authorization",
        ],
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set the orthogonal correction to zero without a certificate",
            "does not use observed y_t or observed top mass to backsolve the correction",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, c2=1, or Z_match=1",
            "does not treat same-source W response alone as physical y_t",
        ],
        "exact_next_action": (
            "Produce a same-source W response row plus one correction authority: "
            "orthogonal-top null theorem, tomography delta_perp row, source-Higgs "
            "Gram-purity row, or neutral rank-one theorem."
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
