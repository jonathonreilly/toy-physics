#!/usr/bin/env python3
"""
PR #230 finite source-shift derivative no-go.

The current FH/LSZ production chunks use one symmetric scalar-source radius:

    s in {-0.01, 0, +0.01}

This runner tests whether that three-point finite-difference slope alone
certifies the zero-source Feynman-Hellmann derivative dE/ds|_0.  It does not:
odd cubic response terms can leave all three measured energies unchanged while
moving the true derivative at zero.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_finite_source_shift_derivative_no_go_2026-05-02.json"

PARENTS = {
    "source_response_harness": "outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json",
    "fh_production_protocol": "outputs/yt_fh_production_protocol_certificate_2026-05-01.json",
    "chunk_combiner_gate": "outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json",
    "ready_chunk_response": "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json",
    "same_source_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
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


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def build_finite_shift_family() -> dict[str, Any]:
    delta = 0.01
    measured_symmetric_slope = 0.4
    e0 = 1.25
    rows = []
    for cubic in (-2000.0, -1000.0, 0.0, 1000.0, 2000.0):
        # E(s)=E0 + a s + c s^3.  The three measured values at -delta,0,+delta
        # are fixed if a + c delta^2 is fixed.
        true_derivative = measured_symmetric_slope - cubic * delta * delta
        energies = {
            "-delta": e0 - measured_symmetric_slope * delta,
            "0": e0,
            "+delta": e0 + measured_symmetric_slope * delta,
        }
        finite_slope = (energies["+delta"] - energies["-delta"]) / (2.0 * delta)
        rows.append(
            {
                "cubic_response_coefficient": cubic,
                "true_zero_source_derivative": true_derivative,
                "finite_symmetric_slope": finite_slope,
                "energy_samples": energies,
            }
        )
    energy_triplets = {
        (
            round(row["energy_samples"]["-delta"], 15),
            round(row["energy_samples"]["0"], 15),
            round(row["energy_samples"]["+delta"], 15),
        )
        for row in rows
    }
    finite_slopes = {round(row["finite_symmetric_slope"], 15) for row in rows}
    derivatives = [row["true_zero_source_derivative"] for row in rows]
    return {
        "source_radius_delta": delta,
        "measured_symmetric_slope": measured_symmetric_slope,
        "rows": rows,
        "checks": {
            "energy_triplet_count": len(energy_triplets),
            "finite_slope_count": len(finite_slopes),
            "true_derivative_span": max(derivatives) - min(derivatives),
            "true_derivative_values": derivatives,
        },
    }


def main() -> int:
    print("PR #230 finite source-shift derivative no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = build_finite_shift_family()
    checks = family["checks"]

    harness_support_only = (
        "scalar source response harness" in status(parents["source_response_harness"])
        and parents["source_response_harness"].get("proposal_allowed") is False
    )
    protocol_support_only = (
        "Feynman-Hellmann production protocol" in status(parents["fh_production_protocol"])
        and parents["fh_production_protocol"].get("proposal_allowed") is False
    )
    combiner_not_evidence = (
        "chunk combiner gate" in status(parents["chunk_combiner_gate"])
        and parents["chunk_combiner_gate"].get("proposal_allowed") is False
    )
    response_stability_not_passed = (
        "ready chunk response-stability diagnostic" in status(parents["ready_chunk_response"])
        and parents["ready_chunk_response"].get("stability_summary", {}).get("stability_passed") is False
    )
    sufficiency_not_passed = (
        "same-source pole-data sufficiency gate not passed" in status(parents["same_source_sufficiency"])
        and parents["same_source_sufficiency"].get("gate_passed") is False
    )
    postprocess_not_ready = (
        "postprocess gate" in status(parents["postprocess_gate"])
        and parents["postprocess_gate"].get("retained_proposal_gate_ready") is False
    )
    derivative_gate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-response-harness-is-support-only", harness_support_only, status(parents["source_response_harness"]))
    report("fh-production-protocol-is-support-only", protocol_support_only, status(parents["fh_production_protocol"]))
    report("chunk-combiner-not-production-evidence-yet", combiner_not_evidence, status(parents["chunk_combiner_gate"]))
    report("response-stability-not-passed", response_stability_not_passed, status(parents["ready_chunk_response"]))
    report("same-source-sufficiency-gate-not-passed", sufficiency_not_passed, status(parents["same_source_sufficiency"]))
    report("postprocess-gate-not-ready", postprocess_not_ready, status(parents["postprocess_gate"]))
    report("finite-energy-triplet-held-fixed", checks["energy_triplet_count"] == 1, f"triplet_count={checks['energy_triplet_count']}")
    report("finite-symmetric-slope-held-fixed", checks["finite_slope_count"] == 1, f"slope_count={checks['finite_slope_count']}")
    report("zero-source-derivative-varies", checks["true_derivative_span"] >= 0.35, f"derivatives={checks['true_derivative_values']}")
    report("finite-source-shift-derivative-gate-not-passed", not derivative_gate_passed, "single finite radius does not certify derivative")

    result = {
        "actual_current_surface_status": "exact negative boundary / finite source-shift slope not zero-source derivative certificate",
        "verdict": (
            "A three-point symmetric source response at one finite radius does "
            "not certify the zero-source Feynman-Hellmann derivative.  The "
            "family E(s)=E0+a s+c s^3 keeps E(-delta), E(0), E(+delta), and "
            "the finite symmetric slope fixed while changing dE/ds|_0 through "
            "the cubic coefficient.  Current chunks with shifts [-0.01,0,+0.01] "
            "therefore provide production diagnostics only until a finite-"
            "source-linearity gate, multiple source radii, or an analytic "
            "response-bound certificate is supplied, in addition to the scalar "
            "LSZ and Higgs-identity gates."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A single finite source-shift radius leaves the zero-source derivative underdetermined by odd nonlinear response terms.",
        "finite_source_shift_derivative_gate_passed": derivative_gate_passed,
        "parent_certificates": PARENTS,
        "finite_shift_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat finite source-shift slopes as physical dE/dh",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Add a finite-source-linearity acceptance gate with at least two "
            "source radii or a retained analyticity/response-bound theorem; "
            "otherwise keep single-radius dE/ds slopes as diagnostics until "
            "same-source LSZ, FV/IR, and Higgs-identity gates pass."
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
