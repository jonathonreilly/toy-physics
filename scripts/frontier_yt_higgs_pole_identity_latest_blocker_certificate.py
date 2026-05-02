#!/usr/bin/env python3
"""
PR #230 latest Higgs-pole identity blocker certificate.

This runner consolidates the current source-pole/canonical-Higgs blockers after
the D17 identity attempt, no-orthogonal-top-coupling import audit, and
source-overlap spectral sum-rule no-go.  It is a claim gate, not a closure
proof.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json"

CERTS = {
    "higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "fh_gauge_response_mixing": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
    "source_overlap_sum_rule": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "scalar_denominator": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "kprime": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def build_same_readout_witness() -> dict[str, Any]:
    """Construct source-pole models with identical measured source readout."""

    measured_source_pole_top_coupling = 1.0
    rows = []
    for cos_theta, physical_y_h in ((1.0, 1.0), (0.8, 0.70), (0.6, 1.20)):
        sin_theta = math.sqrt(max(1.0 - cos_theta * cos_theta, 0.0))
        if sin_theta == 0.0:
            y_orthogonal = 0.0
        else:
            y_orthogonal = (measured_source_pole_top_coupling - physical_y_h * cos_theta) / sin_theta
        readout = physical_y_h * cos_theta + y_orthogonal * sin_theta
        rows.append(
            {
                "cos_source_pole_to_canonical_higgs": cos_theta,
                "sin_orthogonal_component": sin_theta,
                "physical_y_h": physical_y_h,
                "orthogonal_scalar_top_coupling": y_orthogonal,
                "measured_source_pole_top_coupling": readout,
            }
        )
    readouts = [row["measured_source_pole_top_coupling"] for row in rows]
    physical_y = [row["physical_y_h"] for row in rows]
    return {
        "fixed_measured_source_pole_top_coupling": measured_source_pole_top_coupling,
        "models": rows,
        "checks": {
            "max_readout_spread": max(readouts) - min(readouts),
            "physical_y_span": max(physical_y) - min(physical_y),
            "model_count": len(rows),
        },
    }


def main() -> int:
    print("PR #230 latest Higgs-pole identity blocker certificate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    witness = build_same_readout_witness()
    checks = witness["checks"]

    higgs_gate_blocks = (
        "canonical-Higgs pole identity gate blocking" in status(certs["higgs_pole_identity_gate"])
        and certs["higgs_pole_identity_gate"].get("higgs_pole_identity_gate_passed") is False
    )
    source_bridge_blocks = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    d17_blocks = (
        "D17 source-pole identity closure attempt blocked" in status(certs["d17_source_pole_identity"])
        and certs["d17_source_pole_identity"].get("theorem_closed") is False
    )
    mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction" in status(certs["source_pole_mixing"])
        and certs["source_pole_mixing"].get("proposal_allowed") is False
    )
    gauge_response_mixing_blocks = (
        "FH gauge-response mixed-scalar obstruction" in status(certs["fh_gauge_response_mixing"])
        and certs["fh_gauge_response_mixing"].get("proposal_allowed") is False
    )
    no_orthogonal_not_found = (
        "no-orthogonal-top-coupling import audit" in status(certs["no_orthogonal_top_coupling"])
        and certs["no_orthogonal_top_coupling"].get("no_orthogonal_top_coupling_theorem_found") is False
    )
    source_overlap_blocks = (
        "source-overlap spectral sum-rule no-go" in status(certs["source_overlap_sum_rule"])
        and certs["source_overlap_sum_rule"].get("proposal_allowed") is False
    )
    sector_overlap_blocks = (
        "same-source sector-overlap identity obstruction" in status(certs["same_source_sector_overlap"])
        and certs["same_source_sector_overlap"].get("proposal_allowed") is False
    )
    denominator_blocks = (
        "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator"])
        and "K-prime closure attempt blocked" in status(certs["kprime"])
    )
    identity_closed = (
        not missing
        and not proposal_allowed
        and not any(
            [
                higgs_gate_blocks,
                source_bridge_blocks,
                d17_blocks,
                mixing_blocks,
                gauge_response_mixing_blocks,
                no_orthogonal_not_found,
                source_overlap_blocks,
                sector_overlap_blocks,
                denominator_blocks,
            ]
        )
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("higgs-pole-identity-gate-blocks", higgs_gate_blocks, status(certs["higgs_pole_identity_gate"]))
    report("source-bridge-closure-attempt-blocks", source_bridge_blocks, status(certs["source_to_higgs_lsz"]))
    report("d17-identity-upgrade-blocks", d17_blocks, status(certs["d17_source_pole_identity"]))
    report("source-pole-mixing-blocks", mixing_blocks, status(certs["source_pole_mixing"]))
    report("gauge-response-mixing-blocks", gauge_response_mixing_blocks, status(certs["fh_gauge_response_mixing"]))
    report("no-orthogonal-top-coupling-theorem-absent", no_orthogonal_not_found, status(certs["no_orthogonal_top_coupling"]))
    report("source-overlap-sum-rule-blocks", source_overlap_blocks, status(certs["source_overlap_sum_rule"]))
    report("sector-overlap-identity-blocks", sector_overlap_blocks, status(certs["same_source_sector_overlap"]))
    report("denominator-and-kprime-still-block", denominator_blocks, "source residue and D'(pole) remain open")
    report("same-readout-witness-fixed", checks["max_readout_spread"] < 1.0e-12, f"spread={checks['max_readout_spread']:.3e}")
    report("physical-y-varies-under-same-readout", checks["physical_y_span"] >= 0.5, f"span={checks['physical_y_span']:.6g}")
    report("higgs-pole-identity-not-closed", not identity_closed, f"identity_closed={identity_closed}")

    result = {
        "actual_current_surface_status": "open / latest Higgs-pole identity blocker certificate",
        "verdict": (
            "The latest PR #230 surface still does not certify that the measured "
            "same-source scalar pole is the canonical Higgs radial mode used by "
            "v.  D17 carrier uniqueness, no-retained-2HDM support, and finite "
            "source-overlap sum rules do not fix source pole residue, pole "
            "purity, no-orthogonal-top-coupling, the sector-overlap identity, "
            "or D'(pole).  The witness family keeps the measured source-pole "
            "top coupling fixed while varying the physical canonical-Higgs "
            "Yukawa, so retained closure still needs a genuine Higgs-pole "
            "identity theorem or production pole data plus an independent "
            "identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The source-pole/canonical-Higgs identity, no-orthogonal response premise, and scalar denominator derivative remain open.",
        "identity_closed": identity_closed,
        "parent_certificates": CERTS,
        "same_readout_witness": witness,
        "blocking_requirements": [
            "source-pole purity: cos(theta)=1 or an equivalent retained identity",
            "no orthogonal top-coupled scalar response, or direct measurement of that component",
            "same-source sector-overlap identity if using gauge-normalized response",
            "source-pole residue and D'(pole) from scalar LSZ/canonical normalization",
            "production pole data accepted by model-class/FV/IR/Higgs-identity gates",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set cos(theta) = 1",
            "does not set an orthogonal scalar top coupling to zero",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Either derive the source-pole-to-canonical-Higgs identity including "
            "source residue and D'(pole), or let seed-controlled production "
            "chunks accumulate and process them through the combiner, pole-fit, "
            "model-class, FV/IR, and Higgs-identity gates."
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
