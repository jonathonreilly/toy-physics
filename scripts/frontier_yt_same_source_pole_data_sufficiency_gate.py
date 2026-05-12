#!/usr/bin/env python3
"""
PR #230 same-source pole-data sufficiency gate.

This runner records the positive-side closure theorem for the FH/LSZ route:
same-source top response plus same-source scalar pole derivative is enough to
remove the source-coordinate normalization freedom, but only after the source
pole is independently certified as the canonical Higgs radial mode and the
finite-volume/model-class gates pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_pole_data_sufficiency_gate_2026-05-02.json"

PARENTS = {
    "invariant_readout": "outputs/yt_fh_lsz_invariant_readout_theorem_2026-05-01.json",
    "postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
    "ready_chunk_set": "outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json",
    "ready_chunk_response": "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json",
    "full_target_timeseries": "outputs/yt_fh_lsz_target_timeseries_full_set_checkpoint_2026-05-12.json",
    "common_window_response_gate": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "higgs_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "cl3_automorphism": "outputs/yt_cl3_automorphism_source_identity_no_go_2026-05-02.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def algebra_rows() -> list[dict[str, float]]:
    base_slope = 0.18
    base_dprime = 5.0
    rows = []
    for c in [0.25, 0.5, 1.0, 2.0, 4.0]:
        # O_s -> c O_s makes dE/ds -> c dE/ds and D'_ss -> D'_ss / c^2.
        rows.append(
            {
                "source_rescaling_c": c,
                "dE_ds": c * base_slope,
                "dGamma_dp2": base_dprime / (c * c),
                "readout": c * base_slope * math.sqrt(base_dprime / (c * c)),
                "forbidden_kappa_one_readout": c * base_slope,
            }
        )
    return rows


def main() -> int:
    print("PR #230 same-source pole-data sufficiency gate")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    rows = algebra_rows()
    readouts = [row["readout"] for row in rows]
    forbidden = [row["forbidden_kappa_one_readout"] for row in rows]
    readout_spread = max(readouts) - min(readouts)
    forbidden_spread = max(forbidden) - min(forbidden)

    ready_summary = parents["ready_chunk_set"].get("chunk_summary", {})
    ready_chunks = int(ready_summary.get("ready_chunks", 0))
    expected_chunks = int(ready_summary.get("expected_chunks", 1))
    l12_chunk_set_complete = expected_chunks > 0 and ready_chunks >= expected_chunks
    full_timeseries_summary = parents["full_target_timeseries"].get("chunk_summary", {})
    full_target_timeseries_complete = (
        expected_chunks > 0
        and int(full_timeseries_summary.get("expected_chunks", 0)) == expected_chunks
        and int(full_timeseries_summary.get("ready_chunks", -1)) >= expected_chunks
        and int(full_timeseries_summary.get("missing_chunks", -1)) == 0
        and parents["full_target_timeseries"].get("proposal_allowed") is False
    )
    stability = parents["ready_chunk_response"].get("stability_summary", {})
    raw_response_stability_passed = stability.get("stability_passed") is True
    common_window_gate = parents["common_window_response_gate"]
    common_window_response_support_passed = (
        common_window_gate.get("common_window_response_gate_passed") is True
        and common_window_gate.get("proposal_allowed") is False
    )
    response_side_stability_support_passed = (
        raw_response_stability_passed or common_window_response_support_passed
    )
    physical_response_readout_switch_authorized = (
        common_window_gate.get("readout_switch_authorized") is True
        or raw_response_stability_passed
    )
    postprocess_ready = parents["postprocess_gate"].get("retained_proposal_gate_ready") is True
    postprocess_l12_support_ready = parents["postprocess_gate"].get("l12_postprocess_support_ready") is True
    model_gate_passed = parents["model_class_gate"].get("model_class_gate_passed") is True
    higgs_identity_passed = parents["higgs_identity_gate"].get("higgs_pole_identity_gate_passed") is True

    sufficient_conditions = [
        {
            "condition": "same-source invariant readout theorem",
            "satisfied": parents["invariant_readout"].get("proposal_allowed") is False
            and "invariant readout" in parents["invariant_readout"].get("actual_current_surface_status", ""),
            "certificate": PARENTS["invariant_readout"],
        },
        {
            "condition": "complete seed-controlled L12 production support chunk set",
            "satisfied": l12_chunk_set_complete,
            "certificate": PARENTS["ready_chunk_set"],
            "current": f"{ready_chunks}/{expected_chunks}",
        },
        {
            "condition": "complete L12 target-timeseries support packet",
            "satisfied": full_target_timeseries_complete,
            "certificate": PARENTS["full_target_timeseries"],
            "current": full_timeseries_summary,
        },
        {
            "condition": "response-side stability support",
            "satisfied": response_side_stability_support_passed,
            "certificate": PARENTS["ready_chunk_response"],
            "current": {
                "raw_fitted_response_stability": stability,
                "common_window_response_gate_passed": common_window_response_support_passed,
                "common_window_certificate": PARENTS["common_window_response_gate"],
            },
        },
        {
            "condition": "physical response readout switch authorized",
            "satisfied": physical_response_readout_switch_authorized,
            "certificate": PARENTS["common_window_response_gate"],
            "current": {
                "readout_switch_authorized": common_window_gate.get("readout_switch_authorized"),
                "common_window_status": common_window_gate.get("actual_current_surface_status"),
            },
        },
        {
            "condition": "postprocess gate has retained-grade same-source dE/ds, Gamma_ss(q), pole derivative, FV/IR control",
            "satisfied": postprocess_ready,
            "certificate": PARENTS["postprocess_gate"],
            "l12_support_ready": postprocess_l12_support_ready,
        },
        {
            "condition": "finite-shell model-class or pole-saturation gate passed",
            "satisfied": model_gate_passed,
            "certificate": PARENTS["model_class_gate"],
        },
        {
            "condition": "measured pole certified as canonical Higgs radial mode",
            "satisfied": higgs_identity_passed,
            "certificate": PARENTS["higgs_identity_gate"],
        },
    ]
    gate_passed = not missing and not proposal_allowed and all(row["satisfied"] for row in sufficient_conditions)

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("same-source-algebra-invariant", readout_spread < 1.0e-12, f"readout_spread={readout_spread:.3e}")
    report("kappa-one-shortcut-rejected", forbidden_spread > 0.5, f"forbidden_spread={forbidden_spread:.6g}")
    report("invariant-readout-theorem-available", sufficient_conditions[0]["satisfied"], PARENTS["invariant_readout"])
    report("production-support-chunk-set-complete", sufficient_conditions[1]["satisfied"], f"{ready_chunks}/{expected_chunks}")
    report("full-target-timeseries-support-complete", sufficient_conditions[2]["satisfied"], str(full_timeseries_summary))
    report("response-side-stability-support-passed", sufficient_conditions[3]["satisfied"], str(sufficient_conditions[3]["current"]))
    report("physical-response-readout-switch-not-authorized", not sufficient_conditions[4]["satisfied"], str(sufficient_conditions[4]["current"]))
    report("postprocess-retained-gate-not-ready", not sufficient_conditions[5]["satisfied"], PARENTS["postprocess_gate"])
    report("model-class-gate-not-passed", not sufficient_conditions[6]["satisfied"], PARENTS["model_class_gate"])
    report("higgs-identity-gate-not-passed", not sufficient_conditions[7]["satisfied"], PARENTS["higgs_identity_gate"])
    report("same-source-pole-data-sufficiency-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / same-source pole-data sufficiency gate not passed",
        "verdict": (
            "The exact positive-side FH/LSZ route is now explicit: same-source "
            "production dE_top/ds and same-source scalar D'(pole) remove the "
            "source-coordinate normalization freedom by the invariant product "
            "(dE/ds)*sqrt(D'_ss).  This does not set kappa_s=1.  Retained "
            "the closure route now has complete L12 same-source production "
            "support and response-side stability support through the predeclared "
            "common-window gate.  The physical readout switch is still not "
            "authorized, and closure still requires a retained-grade pole/"
            "model-class/FV/IR postprocess plus an independent certificate that "
            "the measured source pole is the canonical Higgs radial mode.  Those "
            "closure gates are not passed on the current PR #230 surface."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The sufficiency theorem, complete L12 support packet, and common-window response stability are support only; physical readout authorization, model-class/FV/IR, and Higgs-identity gates remain open.",
        "same_source_algebra_rows": rows,
        "sufficient_conditions": sufficient_conditions,
        "gate_passed": gate_passed,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use L12-only chunks as closure evidence",
            "does not treat common-window response support as a physical y_t readout switch",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Do not relitigate chunk completeness or response-side support "
            "stability.  Attack physical readout authorization, retained-grade "
            "scalar pole/model-class/FV/IR authority, or the independent "
            "Higgs-identity gate."
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
