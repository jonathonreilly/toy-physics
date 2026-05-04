#!/usr/bin/env python3
"""
PR #230 one-Higgs completeness orthogonal-null gate.

SM one-Higgs gauge selection does not identify the PR230 source pole with
O_H.  A narrower conditional theorem is still useful: if a future same-source
EW action certificate proves one-Higgs field completeness on the PR230 surface,
then the orthogonal neutral top-coupling correction in the W-response route is
zero.  The current surface does not supply that completeness certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json"
FUTURE_COMPLETENESS = ROOT / "outputs" / "yt_one_higgs_completeness_certificate_2026-05-04.json"

PARENTS = {
    "sm_one_higgs_oh_import_boundary": "outputs/yt_sm_one_higgs_oh_import_boundary_2026-05-03.json",
    "wz_same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_same_source_ew_action_semantic_firewall": "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
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


def symbolic_null() -> dict[str, Any]:
    y_h, y_x, k_h, k_x, g_2 = sp.symbols("y_h y_x k_h k_x g_2", nonzero=True)
    sqrt2 = sp.sqrt(2)
    r_t = (y_h * k_h + y_x * k_x) / sqrt2
    r_w = g_2 * k_h / 2
    raw = sp.simplify(g_2 * r_t / (sqrt2 * r_w))
    delta = sp.simplify(y_x * k_x / k_h)
    one_higgs_null_by_empty_orthogonal_sector = sp.simplify(delta.subs({k_x: 0}))
    readout_under_completeness = sp.simplify(raw.subs({k_x: 0}))
    return {
        "raw_readout": str(raw),
        "delta_perp": str(delta),
        "delta_perp_under_one_higgs_completeness": str(one_higgs_null_by_empty_orthogonal_sector),
        "readout_under_one_higgs_completeness": str(readout_under_completeness),
        "delta_null": one_higgs_null_by_empty_orthogonal_sector == 0,
        "readout_equals_y_h": readout_under_completeness == y_h,
    }


def validate_completeness_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "failed_checks": ["future one-Higgs completeness certificate absent"]}

    firewall = candidate.get("firewall", {})
    checks = {
        "phase_is_theorem_or_production_design": candidate.get("phase") in {"theorem", "production_design", "production"},
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "same_source_ew_action_certificate_present": isinstance(candidate.get("same_source_ew_action_certificate"), str)
        and bool(candidate.get("same_source_ew_action_certificate")),
        "proof_kind_allowed": candidate.get("proof_kind")
        in {"same_surface_one_higgs_field_completeness", "neutral_scalar_irrep_exhaustion"},
        "neutral_top_coupled_scalar_basis_dimension_one": candidate.get(
            "neutral_top_coupled_scalar_basis_dimension"
        )
        == 1,
        "extra_top_coupled_neutral_scalars_absent": candidate.get(
            "extra_top_coupled_neutral_scalars_absent"
        )
        is True,
        "higgs_doublet_is_unique_top_yukawa_scalar": candidate.get(
            "higgs_doublet_is_unique_top_yukawa_scalar"
        )
        is True,
        "orthogonal_delta_perp_certified_zero": candidate.get("orthogonal_delta_perp_certified_zero") is True,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_observed_selector": firewall.get("used_observed_targets_as_selector") is False,
        "no_source_pole_identity_by_fiat": firewall.get("set_O_sp_equal_O_H_by_fiat") is False,
        "no_cos_theta_by_fiat": firewall.get("set_cos_theta_equal_one") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def counterexample_without_completeness() -> dict[str, Any]:
    # Same one-Higgs operator pattern for H, plus an allowed current-surface
    # orthogonal neutral scalar that has not been excluded by a same-surface
    # completeness theorem.  This is the existing no-go shape, restated at the
    # correction term.
    k_h = 1.0
    k_x = 0.35
    y_x_values = [-0.2, 0.0, 0.2]
    rows = []
    for y_x in y_x_values:
        rows.append(
            {
                "kappa_h": k_h,
                "kappa_x": k_x,
                "orthogonal_top_coupling_y_x": y_x,
                "delta_perp": y_x * k_x / k_h,
            }
        )
    deltas = [row["delta_perp"] for row in rows]
    return {
        "rows": rows,
        "delta_span": max(deltas) - min(deltas),
        "completeness_needed": True,
    }


def main() -> int:
    print("PR #230 one-Higgs completeness orthogonal-null gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    formula = symbolic_null()
    future_candidate = load_json(FUTURE_COMPLETENESS)
    validation = validate_completeness_certificate(future_candidate)
    counterexample = counterexample_without_completeness()

    sm_one_higgs_not_oh = (
        parents["sm_one_higgs_oh_import_boundary"].get("sm_one_higgs_import_closes_pr230") is False
        and "SM one-Higgs gauge selection is not PR230 O_H identity"
        in status(parents["sm_one_higgs_oh_import_boundary"])
    )
    ew_action_absent = (
        parents["wz_same_source_ew_action_builder"].get("same_source_ew_action_certificate_valid") is False
        and parents["wz_same_source_ew_action_builder"].get("input_present") is False
    )
    ew_action_firewall_support = (
        "same-source EW action semantic firewall passed"
        in status(parents["wz_same_source_ew_action_semantic_firewall"])
        and parents["wz_same_source_ew_action_semantic_firewall"].get("proposal_allowed") is False
    )
    no_current_null = (
        parents["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    correction_gate_open = (
        parents["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False
        and parents["same_source_w_response_orthogonal_correction"].get(
            "orthogonal_correction_theorem_passed"
        )
        is True
    )
    counterexample_varies = counterexample["delta_span"] > 0.0
    gate_passed = validation["valid"] is True
    theorem_passed = (
        not missing
        and not proposal_allowed
        and sm_one_higgs_not_oh
        and ew_action_firewall_support
        and formula["delta_null"]
        and formula["readout_equals_y_h"]
        and counterexample_varies
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("sm-one-higgs-alone-not-oh", sm_one_higgs_not_oh, status(parents["sm_one_higgs_oh_import_boundary"]))
    report("same-source-ew-action-absent", ew_action_absent, status(parents["wz_same_source_ew_action_builder"]))
    report("same-source-ew-action-firewall-support", ew_action_firewall_support, status(parents["wz_same_source_ew_action_semantic_firewall"]))
    report("current-selection-rule-null-absent", no_current_null, status(parents["no_orthogonal_top_coupling_selection"]))
    report("w-correction-gate-open", correction_gate_open, status(parents["same_source_w_response_orthogonal_correction"]))
    report("one-higgs-completeness-null-derived", formula["delta_null"], formula["delta_perp_under_one_higgs_completeness"])
    report("one-higgs-completeness-readout-equals-yh", formula["readout_equals_y_h"], formula["readout_under_one_higgs_completeness"])
    report("without-completeness-counterexample-varies", counterexample_varies, f"delta_span={counterexample['delta_span']:.6g}")
    report("future-completeness-certificate-absent", not validation["present"], str(FUTURE_COMPLETENESS.relative_to(ROOT)))
    report("one-higgs-completeness-theorem-passed", theorem_passed, f"theorem_passed={theorem_passed}")
    report("current-completeness-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "conditional-support / one-Higgs completeness orthogonal-null theorem; premise absent",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The conditional null theorem is exact, but the current PR230 surface "
            "does not supply a same-source one-Higgs field-completeness certificate."
        ),
        "bare_retained_allowed": False,
        "one_higgs_completeness_orthogonal_null_theorem_passed": theorem_passed,
        "one_higgs_completeness_gate_passed": gate_passed,
        "current_closure_gate_passed": False,
        "symbolic_formula": formula,
        "future_completeness_certificate": str(FUTURE_COMPLETENESS.relative_to(ROOT)),
        "future_completeness_validation": validation,
        "counterexample_without_completeness": counterexample,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat SM one-Higgs gauge selection alone as O_sp=O_H",
            "does not set orthogonal top coupling or delta_perp to zero on the current surface",
            "does not use H_unit, yt_ward_identity, observed selectors, alpha_LM, plaquette/u0, c2=1, Z_match=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            "Supply a same-source EW action certificate with one-Higgs field "
            "completeness, or measure delta_perp by tomography/Gram rows."
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
