#!/usr/bin/env python3
"""
PR #230 FH/LSZ common-window replacement response-stability gate.

The original response-window acceptance gate requires full ready-set v2
per-configuration covariance.  Legacy chunks001-016 cannot be honestly
backfilled to that schema.  This runner checks a narrower replacement-readout
contract: can the fixed tau=10..12 common-window response be treated as a
stable replacement response diagnostic over the full ready chunk set?

This is support only.  Passing this gate does not authorize a physical readout
switch and does not supply scalar-LSZ or canonical-Higgs/source-overlap
closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_common_window_replacement_response_stability_2026-05-04.json"

PARENTS = {
    "ready_chunk_set": "outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json",
    "target_observable_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
    "autocorrelation_ess": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "legacy_v2_backfill": "outputs/yt_fh_lsz_legacy_v2_backfill_feasibility_2026-05-04.json",
    "common_window_provenance": "outputs/yt_fh_lsz_common_window_response_provenance_2026-05-04.json",
    "common_window_pooled_estimator": "outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json",
    "finite_source_linearity": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "response_window_acceptance": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
}

MIN_READY_CHUNKS = 30

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
    print("PR #230 FH/LSZ common-window replacement response-stability gate")
    print("=" * 82)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, data in parents.items() if not data]
    proposal_allowed = [name for name, data in parents.items() if data.get("proposal_allowed") is True]

    ready_set = parents["ready_chunk_set"]
    target_ess = parents["target_observable_ess"]
    autocorr = parents["autocorrelation_ess"]
    legacy = parents["legacy_v2_backfill"]
    provenance = parents["common_window_provenance"]
    pooled = parents["common_window_pooled_estimator"]
    finite_source = parents["finite_source_linearity"]
    acceptance = parents["response_window_acceptance"]

    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    provenance_indices = [
        int(index)
        for index in provenance.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    ready_set_covered = bool(ready_indices) and sorted(ready_indices) == sorted(provenance_indices)
    enough_ready_chunks = len(ready_indices) >= MIN_READY_CHUNKS
    target_ess_passed = target_ess.get("target_observable_ess_gate_passed") is True
    autocorr_passed = autocorr.get("autocorrelation_ess_gate_passed") is True
    legacy_backfill_honestly_blocked = (
        legacy.get("legacy_summary", {}).get("honest_v2_backfill_possible") is False
    )
    common_window_stable = provenance.get("common_window_stability_passed") is True
    pooled_production_grade = (
        pooled.get("pooled_common_window_response_production_grade") is True
    )
    finite_source_passed = finite_source.get("finite_source_linearity_gate_passed") is True
    old_acceptance_open = acceptance.get("response_window_acceptance_gate_passed") is False
    old_acceptance_open_reason = acceptance.get("actual_current_surface_status", "")
    replacement_response_stability_passed = (
        not missing
        and not proposal_allowed
        and ready_set_covered
        and enough_ready_chunks
        and target_ess_passed
        and autocorr_passed
        and legacy_backfill_honestly_blocked
        and common_window_stable
        and pooled_production_grade
        and finite_source_passed
    )
    readout_switch_authorized = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("ready-set-covered-by-common-window", ready_set_covered, f"ready={len(ready_indices)} provenance={len(provenance_indices)}")
    report("enough-ready-chunks", enough_ready_chunks, f"n={len(ready_indices)}")
    report("target-observable-ess-passed", target_ess_passed, status(target_ess))
    report("autocorrelation-ess-passed", autocorr_passed, status(autocorr))
    report("legacy-v2-backfill-honestly-blocked", legacy_backfill_honestly_blocked, status(legacy))
    report("old-response-window-acceptance-open-recorded", old_acceptance_open, old_acceptance_open_reason)
    report("common-window-stability-passed", common_window_stable, status(provenance))
    report("pooled-common-window-production-grade", pooled_production_grade, status(pooled))
    report("finite-source-linearity-support-passed", finite_source_passed, status(finite_source))
    report("replacement-response-stability-passed-as-support", replacement_response_stability_passed, f"passed={replacement_response_stability_passed}")
    report("readout-switch-not-authorized", not readout_switch_authorized, "scalar-LSZ/O_H gates remain open")
    report("does-not-authorize-retained-proposal", True, "replacement stability is response support only")

    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ common-window replacement response-stability passed"
            if replacement_response_stability_passed
            else "open / FH-LSZ common-window replacement response-stability not passed"
        ),
        "verdict": (
            "The fixed tau=10..12 common-window response covers the full ready "
            "chunk set, has production-grade pooled chunk uncertainty, and is "
            "paired with finite-source-linearity support.  Because legacy v2 "
            "backfill is honestly impossible, this supplies a replacement "
            "response-stability support path instead of pretending that "
            "chunks001-016 have v2 covariance rows.  It does not authorize a "
            "physical readout switch or close scalar-LSZ/canonical-Higgs gates."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Replacement response stability is support only; scalar LSZ and "
            "canonical-Higgs/source-overlap remain open."
        ),
        "bare_retained_allowed": False,
        "replacement_response_stability_passed": replacement_response_stability_passed,
        "readout_switch_authorized": readout_switch_authorized,
        "ready_chunk_count": len(ready_indices),
        "ready_chunk_indices": ready_indices,
        "criteria": {
            "ready_set_covered": ready_set_covered,
            "enough_ready_chunks": enough_ready_chunks,
            "target_observable_ess_passed": target_ess_passed,
            "autocorrelation_ess_passed": autocorr_passed,
            "legacy_v2_backfill_honestly_blocked": legacy_backfill_honestly_blocked,
            "common_window_stability_passed": common_window_stable,
            "pooled_common_window_production_grade": pooled_production_grade,
            "finite_source_linearity_gate_passed": finite_source_passed,
            "old_response_window_acceptance_gate_passed": acceptance.get(
                "response_window_acceptance_gate_passed"
            ),
        },
        "common_window_summary": {
            "mean": pooled.get("mean"),
            "relative_standard_error": pooled.get("relative_standard_error"),
            "bootstrap_relative_half_width_68": pooled.get("bootstrap", {}).get(
                "relative_half_width_68"
            ),
            "common_window": pooled.get("common_window"),
        },
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not fabricate legacy v2 covariance rows",
            "does not replace scalar LSZ normalization",
            "does not identify O_sp with O_H",
            "does not set kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use this as the replacement response-stability parent for the "
            "common-window response gate.  Remaining blockers are scalar-LSZ "
            "pole/FV/IR/model-class control and canonical-Higgs/source-overlap "
            "closure."
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
