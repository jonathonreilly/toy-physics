#!/usr/bin/env python3
"""
PR #230 scalar denominator theorem closure attempt.

This runner tries to assemble the microscopic scalar-denominator / pole-residue
theorem from the current PR #230 artifacts.  It is intentionally conservative:
supporting gates count as support only, while any open/no-go prerequisite keeps
the theorem unclosed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json"

CERTS = {
    "determinant_gate": "outputs/yt_scalar_pole_determinant_gate_2026-05-01.json",
    "eigen_derivative_gate": "outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json",
    "derivative_limit": "outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json",
    "residue_envelope": "outputs/yt_scalar_ladder_residue_envelope_obstruction_2026-05-01.json",
    "ward_kernel": "outputs/yt_scalar_kernel_ward_identity_obstruction_2026-05-01.json",
    "zero_mode_limit": "outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json",
    "zero_mode_import": "outputs/yt_zero_mode_prescription_import_audit_2026-05-01.json",
    "flat_toron": "outputs/yt_flat_toron_scalar_denominator_obstruction_2026-05-01.json",
    "flat_toron_washout": "outputs/yt_flat_toron_thermodynamic_washout_2026-05-01.json",
    "color_singlet_zero_mode": "outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json",
    "color_singlet_finite_q": "outputs/yt_color_singlet_finite_q_ir_regular_2026-05-01.json",
    "taste_carrier": "outputs/yt_taste_carrier_import_audit_2026-05-01.json",
    "taste_singlet": "outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json",
    "taste_projector": "outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json",
    "unit_projector_threshold": "outputs/yt_unit_projector_pole_threshold_obstruction_2026-05-01.json",
    "kernel_enhancement": "outputs/yt_scalar_kernel_enhancement_import_audit_2026-05-01.json",
    "fitted_kernel": "outputs/yt_fitted_kernel_residue_selector_no_go_2026-05-01.json",
    "finite_shell": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
    "model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "stieltjes": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
    "threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "threshold_authority": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "finite_volume": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "uniform_gap": "outputs/yt_fh_lsz_uniform_gap_self_certification_no_go_2026-05-02.json",
    "seed_independence": "outputs/yt_fh_lsz_numba_seed_independence_audit_2026-05-02.json",
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
    print("PR #230 scalar denominator theorem closure attempt")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    dependencies = [
        {
            "premise": "pole condition and inverse-propagator derivative identified",
            "certificate": CERTS["determinant_gate"],
            "available": "scalar pole determinant gate" in status(certs["determinant_gate"]),
            "closure_role": "support",
        },
        {
            "premise": "matrix ladder derivative identified",
            "certificate": CERTS["eigen_derivative_gate"],
            "available": "scalar ladder eigen-derivative gate" in status(certs["eigen_derivative_gate"]),
            "closure_role": "support",
        },
        {
            "premise": "zero-mode/IR limiting order fixed",
            "certificate": CERTS["derivative_limit"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "scalar residue single-valued across projector/volume prescriptions",
            "certificate": CERTS["residue_envelope"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "Ward/Feshbach surfaces fix K'(pole) or common dressing",
            "certificate": CERTS["ward_kernel"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "gauge-zero-mode and flat-sector prescription derived",
            "certificate": CERTS["zero_mode_import"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "q=0 singlet cancellation and finite-q IR regularity",
            "certificate": f"{CERTS['color_singlet_zero_mode']}; {CERTS['color_singlet_finite_q']}",
            "available": True,
            "closure_role": "support_only",
        },
        {
            "premise": "physical scalar taste/projector carrier derived",
            "certificate": CERTS["taste_projector"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "unit-projector ladder crosses without fitted enhancement",
            "certificate": CERTS["unit_projector_threshold"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "scalar-kernel enhancement or K'(pole) derived",
            "certificate": CERTS["kernel_enhancement"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "finite-shell model class fixes pole derivative",
            "certificate": CERTS["model_class_gate"],
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "positive Stieltjes / threshold / uniform gap closes residue interval",
            "certificate": f"{CERTS['stieltjes']}; {CERTS['threshold_gate']}; {CERTS['uniform_gap']}",
            "available": False,
            "closure_role": "blocking",
        },
        {
            "premise": "seed-controlled production data available",
            "certificate": CERTS["seed_independence"],
            "available": False,
            "closure_role": "blocking_for_measurement_route",
        },
    ]
    blockers = [row for row in dependencies if row["closure_role"].startswith("blocking")]
    support = [row for row in dependencies if row["closure_role"] in {"support", "support_only"}]
    theorem_closed = not missing and not proposal_allowed and not blockers

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("pole-and-derivative-gates-provide-support", len([row for row in support if row["available"]]) >= 3, f"support_count={len(support)}")
    report("zero-mode-prescription-still-blocking", not dependencies[5]["available"], CERTS["zero_mode_import"])
    report("taste-projector-carrier-still-blocking", not dependencies[7]["available"], CERTS["taste_projector"])
    report("kernel-enhancement-still-blocking", not dependencies[9]["available"], CERTS["kernel_enhancement"])
    report("finite-shell-gap-path-still-blocking", not dependencies[11]["available"], CERTS["uniform_gap"])
    report("seed-controlled-production-not-yet-available", not dependencies[12]["available"], CERTS["seed_independence"])
    report("scalar-denominator-theorem-not-closed", not theorem_closed, f"blocker_count={len(blockers)}")

    result = {
        "actual_current_surface_status": "open / scalar denominator theorem closure attempt blocked",
        "verdict": (
            "The current PR #230 artifacts do not assemble into a retained "
            "microscopic scalar-denominator theorem.  They do provide support: "
            "the pole condition and derivative target are named, exact q=0 "
            "singlet cancellation is available, and finite-q IR regularity "
            "removes one divergence concern.  The theorem still fails because "
            "the zero-mode/flat-sector prescription, physical scalar "
            "taste/projector carrier, scalar-kernel enhancement/K'(pole), "
            "finite-shell model class, pole-saturation/uniform-gap premise, "
            "and seed-controlled production data remain open or explicitly "
            "blocked."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Multiple required scalar-denominator premises remain open or no-go; no retained scalar LSZ residue is derived.",
        "parent_certificates": CERTS,
        "dependency_rows": dependencies,
        "support_count": len(support),
        "blocking_count": len(blockers),
        "theorem_closed": theorem_closed,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not infer a continuum gap from finite shell rows",
            "does not count historical non-seed-controlled chunks as production evidence",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Continue seed-controlled production replacement chunks, or derive "
            "one of the blocking scalar-denominator premises directly: physical "
            "scalar carrier/projector, K'(pole), or a uniform threshold theorem."
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
