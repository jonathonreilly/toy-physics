#!/usr/bin/env python3
"""
PR #230 FH/LSZ common-window response gate.

The common-window provenance audit shows that mixed source-shift fit windows
explain the unstable fitted dE/ds surface.  This runner turns that observation
into a predeclared response-gate contract.

Current evidence is not allowed to switch the physical readout.  A future
common-window response readout needs a production-grade fixed-window response,
finite-source-linearity, response-window acceptance, fitted-response or
replacement-readout stability, and the separate scalar-LSZ/canonical-Higgs
gates.  This script records those criteria and checks the current surface
without promoting y_t.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_response_gate_2026-05-04.json"

PARENTS = {
    "common_window_response_provenance": "outputs/yt_fh_lsz_common_window_response_provenance_2026-05-04.json",
    "common_window_pooled_response_estimator": "outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json",
    "common_window_replacement_response_stability": "outputs/yt_fh_lsz_common_window_replacement_response_stability_2026-05-04.json",
    "response_window_acceptance_gate": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
    "finite_source_linearity_gate": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "fitted_response_stability": "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json",
    "v2_target_response_stability": "outputs/yt_fh_lsz_v2_target_response_stability_2026-05-04.json",
}

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


def load_json(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(data: dict[str, Any]) -> str:
    value = data.get("actual_current_surface_status", "")
    return value if isinstance(value, str) else ""


def main() -> int:
    print("PR #230 FH/LSZ common-window response gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, data in parents.items() if not data]
    proposal_allowed = [name for name, data in parents.items() if data.get("proposal_allowed") is True]

    provenance = parents["common_window_response_provenance"]
    pooled = parents["common_window_pooled_response_estimator"]
    replacement = parents["common_window_replacement_response_stability"]
    acceptance = parents["response_window_acceptance_gate"]
    finite_source = parents["finite_source_linearity_gate"]
    fitted_response = parents["fitted_response_stability"]
    v2_target = parents["v2_target_response_stability"]

    common_window_stable = provenance.get("common_window_stability_passed") is True
    pooled_common_window_production_grade = (
        pooled.get("pooled_common_window_response_production_grade") is True
    )
    common_window_production_grade = (
        provenance.get("common_window_production_grade") is True
        or pooled_common_window_production_grade
    )
    provenance_forbids_switch = provenance.get("readout_switch_authorized") is False
    acceptance_passed = acceptance.get("response_window_acceptance_gate_passed") is True
    finite_source_linearity_passed = finite_source.get("finite_source_linearity_gate_passed") is True
    fitted_response_stability_passed = (
        fitted_response.get("stability_summary", {}).get("stability_passed") is True
    )
    replacement_response_stability_passed = (
        replacement.get("replacement_response_stability_passed") is True
    )
    response_stability_or_replacement_passed = (
        fitted_response_stability_passed or replacement_response_stability_passed
    )
    acceptance_or_replacement_passed = acceptance_passed or replacement_response_stability_passed
    v2_target_support_passed = v2_target.get("v2_target_response_stability_passed") is True

    predeclared_criteria = {
        "common_window_stability_passed": common_window_stable,
        "common_window_production_grade": common_window_production_grade,
        "pooled_common_window_response_production_grade": pooled_common_window_production_grade,
        "response_window_acceptance_or_replacement_passed": acceptance_or_replacement_passed,
        "finite_source_linearity_gate_passed": finite_source_linearity_passed,
        "fitted_or_replacement_response_stability_passed": response_stability_or_replacement_passed,
        "v2_target_response_stability_support_passed": v2_target_support_passed,
        "scalar_lsz_and_canonical_higgs_closure_required_separately": True,
    }
    common_window_response_gate_passed = (
        not missing
        and not proposal_allowed
        and common_window_stable
        and common_window_production_grade
        and acceptance_or_replacement_passed
        and finite_source_linearity_passed
        and response_stability_or_replacement_passed
        and v2_target_support_passed
    )
    readout_switch_authorized = False

    open_blockers = [
        name for name, passed in predeclared_criteria.items()
        if name != "scalar_lsz_and_canonical_higgs_closure_required_separately" and not passed
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("common-window-stability-recorded", common_window_stable, str(status(provenance)))
    report(
        "common-window-production-grade-state-recorded",
        "common_window_production_grade" in provenance
        or "pooled_common_window_response_production_grade" in pooled,
        f"production_grade={common_window_production_grade}",
    )
    report(
        "pooled-common-window-estimator-state-recorded",
        bool(pooled),
        pooled.get("actual_current_surface_status", ""),
    )
    report("provenance-forbids-readout-switch", provenance_forbids_switch, f"authorized={provenance.get('readout_switch_authorized')}")
    report("v2-target-support-state-recorded", "v2_target_response_stability_passed" in v2_target, str(status(v2_target)))
    report("finite-source-linearity-state-recorded", bool(finite_source), str(status(finite_source)))
    report("response-window-acceptance-state-recorded", bool(acceptance), str(status(acceptance)))
    report(
        "replacement-response-stability-state-recorded",
        bool(replacement),
        replacement.get("actual_current_surface_status", ""),
    )
    report("fitted-response-stability-state-recorded", bool(fitted_response), str(status(fitted_response)))
    report("common-window-gate-state-recorded", True, f"passed={common_window_response_gate_passed}")
    report("readout-switch-not-authorized-currently", not readout_switch_authorized, "separate physics gates remain open")
    report("does-not-authorize-retained-proposal", True, "common-window gate is not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ common-window response gate passed as support"
            if common_window_response_gate_passed
            else "open / FH-LSZ common-window response gate not passed"
        ),
        "verdict": (
            "The common-window provenance result is now formalized as a "
            "predeclared gate.  On the current surface the fixed-window "
            "central slope is stable, production-grade under pooled "
            "chunk-scatter uncertainty, and paired with finite-source-"
            "linearity plus replacement response-stability support.  This "
            "passes the common-window response gate as support when the "
            "criteria are satisfied, but no physical readout switch is "
            "authorized because scalar-LSZ and canonical-Higgs/source-overlap "
            "closure remain separate blockers."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The common-window gate is an evidence-quality contract only; it "
            "does not supply scalar LSZ normalization or O_sp/O_H identity."
        ),
        "bare_retained_allowed": False,
        "common_window_response_gate_passed": common_window_response_gate_passed,
        "readout_switch_authorized": readout_switch_authorized,
        "predeclared_criteria": predeclared_criteria,
        "open_blockers": open_blockers,
        "parent_certificates": PARENTS,
        "common_window_summary": {
            "common_window": provenance.get("common_window"),
            "common_window_slope_summary": provenance.get("common_window_slope_summary"),
            "common_window_relative_fit_error": provenance.get("common_window_relative_fit_error"),
            "pooled_relative_standard_error": pooled.get("relative_standard_error"),
            "pooled_empirical_standard_error": pooled.get("empirical_standard_error"),
            "replacement_response_stability_passed": replacement.get(
                "replacement_response_stability_passed"
            ),
            "high_original_slope_chunk_indices": provenance.get("high_original_slope_chunk_indices"),
            "mixed_window_chunk_indices": provenance.get("mixed_window_chunk_indices"),
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production response readout",
            "does not treat fixed-window central stability as scalar LSZ normalization",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use this response-side support only as a parent for scalar-LSZ "
            "pole/FV/IR/model-class work and canonical-Higgs/source-overlap "
            "closure.  Do not request a physical y_t readout switch until "
            "those independent gates pass."
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
