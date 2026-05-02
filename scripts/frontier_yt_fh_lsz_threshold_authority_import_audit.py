#!/usr/bin/env python3
"""
PR #230 FH/LSZ threshold-authority import audit.

The pole-saturation threshold gate names a possible repair: provide a
continuum-threshold / pole-saturation certificate that makes the scalar pole
residue interval tight.  This runner checks the current PR #230 surface for
that authority and keeps the claim firewall explicit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"
MODEL_CLASS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
CHUNK_COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
RETAINED_ROUTE = ROOT / "outputs" / "yt_retained_closure_route_certificate_2026-05-01.json"
THRESHOLD_CERT = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_certificate_2026-05-02.json"
SCALAR_DENOMINATOR_CERT = ROOT / "outputs" / "yt_scalar_denominator_pole_residue_theorem_2026-05-02.json"
COMBINED_L12 = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json"

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
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 FH/LSZ threshold-authority import audit")
    print("=" * 72)

    threshold_gate = load_json(THRESHOLD_GATE)
    model_gate = load_json(MODEL_CLASS_GATE)
    combiner = load_json(CHUNK_COMBINER)
    retained_route = load_json(RETAINED_ROUTE)
    threshold_cert = load_json(THRESHOLD_CERT)
    scalar_denominator = load_json(SCALAR_DENOMINATOR_CERT)
    combined_l12 = load_json(COMBINED_L12)

    combiner_summary = combiner.get("chunk_summary", {})
    ready_chunks = int(combiner_summary.get("ready_chunks", 0))
    expected_chunks = int(combiner_summary.get("expected_chunks", 1))
    proposal_list = retained_route.get("proposal_allowed_certificates", [])

    report("threshold-gate-loaded", bool(threshold_gate), str(THRESHOLD_GATE.relative_to(ROOT)))
    report(
        "threshold-gate-not-passed",
        threshold_gate.get("pole_saturation_threshold_gate_passed") is False,
        str(threshold_gate.get("actual_current_surface_status")),
    )
    report("model-class-gate-still-blocking", model_gate.get("model_class_gate_passed") is False, str(model_gate.get("actual_current_surface_status")))
    report("threshold-certificate-absent", not threshold_cert, str(THRESHOLD_CERT.relative_to(ROOT)))
    report("scalar-denominator-certificate-absent", not scalar_denominator, str(SCALAR_DENOMINATOR_CERT.relative_to(ROOT)))
    report("combined-l12-production-absent", not combined_l12 and ready_chunks < expected_chunks, f"ready={ready_chunks}/{expected_chunks}")
    report("retained-route-authorizes-no-proposal", not proposal_list, f"proposal_allowed={proposal_list}")
    report("does-not-authorize-retained-proposal", True, "audit found no current threshold authority")

    missing_authorities = [
        str(THRESHOLD_CERT.relative_to(ROOT)),
        str(SCALAR_DENOMINATOR_CERT.relative_to(ROOT)),
        str(COMBINED_L12.relative_to(ROOT)),
    ]
    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ threshold-authority import audit",
        "verdict": (
            "No current PR #230 artifact supplies the continuum-threshold, "
            "pole-saturation, or scalar-denominator authority required by the "
            "new residue-interval gate.  The model-class gate remains blocking, "
            "the threshold certificate is absent, the scalar denominator theorem "
            "certificate is absent, and chunked production has no combined L12 "
            "output.  The threshold input therefore cannot be imported silently."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The pole-saturation/threshold authority named by the gate is absent on the current surface.",
        "missing_authorities": missing_authorities,
        "parents": {
            "threshold_gate": str(THRESHOLD_GATE.relative_to(ROOT)),
            "model_class_gate": str(MODEL_CLASS_GATE.relative_to(ROOT)),
            "chunk_combiner": str(CHUNK_COMBINER.relative_to(ROOT)),
            "retained_route": str(RETAINED_ROUTE.relative_to(ROOT)),
        },
        "strict_non_claims": [
            "does not use a threshold or pole-saturation premise by assumption",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either derive the scalar denominator/pole-saturation theorem, "
            "produce a threshold certificate that passes the interval gate, or "
            "continue production chunks toward combined L12 plus postprocess."
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
