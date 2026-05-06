#!/usr/bin/env python3
"""
PR #230 K'(pole) closure attempt.

This runner checks whether the current determinant, ladder-derivative,
Ward/Feshbach, carrier/projector, and threshold artifacts now close the
interacting scalar-kernel derivative required by the same-source FH/LSZ
readout.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_kprime_closure_attempt_2026-05-02.json"

CERTS = {
    "determinant_gate": "outputs/yt_scalar_pole_determinant_gate_2026-05-01.json",
    "eigen_derivative_gate": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "total_momentum_derivative_scout": "outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json",
    "derivative_limit": "outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
    "residue_envelope": "outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
    "ward_identity": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
    "kernel_enhancement_import": "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json",
    "fitted_kernel_selector": "outputs/yt_fitted_kernel_residue_selector_no_go_2026-05-01.json",
    "carrier_projector": "outputs/yt_scalar_carrier_projector_closure_attempt_2026-05-02.json",
    "scalar_denominator_closure": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "soft_continuum_threshold": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
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


def main() -> int:
    print("PR #230 K'(pole) closure attempt")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    support_rows = [
        {
            "premise": "determinant formula names K'(pole)",
            "certificate": CERTS["determinant_gate"],
            "available": "scalar pole determinant gate" in status(certs["determinant_gate"]),
        },
        {
            "premise": "matrix eigen-derivative gate identifies d lambda/dp^2",
            "certificate": CERTS["eigen_derivative_gate"],
            "available": "scalar ladder eigen-derivative gate" in status(certs["eigen_derivative_gate"]),
        },
        {
            "premise": "finite total-momentum derivative scout is executable",
            "certificate": CERTS["total_momentum_derivative_scout"],
            "available": "total-momentum derivative scout" in status(certs["total_momentum_derivative_scout"]),
        },
    ]
    blockers = [
        {
            "premise": "finite derivative has a retained zero-mode/IR/volume limiting order",
            "certificate": CERTS["derivative_limit"],
            "blocked": "derivative limiting-order obstruction" in status(certs["derivative_limit"]),
        },
        {
            "premise": "residue proxy is single-valued across zero-mode/projector/volume surfaces",
            "certificate": CERTS["residue_envelope"],
            "blocked": "residue-envelope obstruction" in status(certs["residue_envelope"]),
        },
        {
            "premise": "Ward/Feshbach surfaces fix K'(pole) or common dressing",
            "certificate": CERTS["ward_identity"],
            "blocked": "Ward-identity obstruction" in status(certs["ward_identity"]),
        },
        {
            "premise": "scalar-kernel enhancement or K'(pole) is imported from a retained authority",
            "certificate": CERTS["kernel_enhancement_import"],
            "blocked": "scalar-kernel enhancement import audit" in status(certs["kernel_enhancement_import"]),
        },
        {
            "premise": "fitted kernel multiplier is a physical K'(pole) theorem",
            "certificate": CERTS["fitted_kernel_selector"],
            "blocked": "fitted scalar-kernel residue selector no-go" in status(certs["fitted_kernel_selector"]),
        },
        {
            "premise": "physical scalar carrier/projector is fixed before differentiating",
            "certificate": CERTS["carrier_projector"],
            "blocked": "scalar carrier-projector closure attempt blocked" in status(certs["carrier_projector"]),
        },
        {
            "premise": "threshold/denominator stack supplies missing K'(pole) control",
            "certificate": f"{CERTS['scalar_denominator_closure']}; {CERTS['soft_continuum_threshold']}",
            "blocked": (
                "scalar denominator theorem closure attempt blocked" in status(certs["scalar_denominator_closure"])
                and "soft-continuum threshold no-go" in status(certs["soft_continuum_threshold"])
            ),
        },
    ]
    support_available = [row for row in support_rows if row["available"]]
    blocked_rows = [row for row in blockers if row["blocked"]]
    explicit_positive_kprime_inputs = (
        certs["determinant_gate"].get("scalar_pole_determinant_gate_passed") is True
        and certs["eigen_derivative_gate"].get("scalar_ladder_eigen_derivative_gate_passed") is True
        and certs["scalar_denominator_closure"].get("scalar_denominator_theorem_closed") is True
        and certs["carrier_projector"].get("current_closure_gate_passed") is True
    )
    kprime_closed = (
        explicit_positive_kprime_inputs
        and not missing
        and not proposal_allowed
        and len(blocked_rows) == 0
    )

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("support-premises-available", len(support_available) == len(support_rows), f"support={len(support_available)}/{len(support_rows)}")
    report("derivative-limit-still-blocking", blockers[0]["blocked"], CERTS["derivative_limit"])
    report("residue-envelope-still-blocking", blockers[1]["blocked"], CERTS["residue_envelope"])
    report("ward-feshbach-kprime-still-blocking", blockers[2]["blocked"], CERTS["ward_identity"])
    report("kernel-enhancement-still-blocking", blockers[3]["blocked"], CERTS["kernel_enhancement_import"])
    report("carrier-projector-still-blocking", blockers[5]["blocked"], CERTS["carrier_projector"])
    report("explicit-positive-kprime-inputs-required", not explicit_positive_kprime_inputs, "no positive K'(pole) certificate present")
    report("kprime-theorem-not-closed", not kprime_closed, f"blocker_count={len(blocked_rows)}")

    result = {
        "actual_current_surface_status": "open / K-prime closure attempt blocked",
        "verdict": (
            "The current PR #230 surface names and computes finite proxies for "
            "the required scalar denominator derivative, but it does not close "
            "K'(pole).  The determinant and eigen-derivative gates identify "
            "the load-bearing object, and the total-momentum derivative scout "
            "is executable support.  The derivative remains blocked by "
            "zero-mode/IR/volume limiting order, residue-envelope dependence, "
            "Ward/Feshbach non-identification, missing scalar-kernel "
            "enhancement authority, fitted-kernel selector no-go, open "
            "carrier/projector normalization, and the still-open denominator "
            "threshold stack."
        ),
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "investigation_route_closed": False,
        "certification_scope": "current_surface_blocker_only",
        "proposal_allowed_reason": "K'(pole) is named but not derived or measured on a retained current surface.",
        "parent_certificates": CERTS,
        "support_rows": support_rows,
        "blocker_rows": blockers,
        "support_count": len(support_available),
        "blocking_count": len(blocked_rows),
        "explicit_positive_kprime_inputs_present": explicit_positive_kprime_inputs,
        "current_closure_gate_passed": kprime_closed,
        "kprime_closed": kprime_closed,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not treat a finite derivative scout as a retained continuum derivative",
            "does not fit a scalar-kernel multiplier as proof",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Continue seed-controlled FH/LSZ production replacement chunks, or "
            "derive K'(pole) together with the physical scalar carrier/projector "
            "and zero-mode/IR/volume limiting prescription."
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
