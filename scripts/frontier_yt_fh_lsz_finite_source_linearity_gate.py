#!/usr/bin/env python3
"""
PR #230 FH/LSZ finite-source-linearity acceptance gate.

The finite source-shift derivative no-go shows that a single symmetric source
radius does not certify dE/ds at zero.  This runner turns that obstruction into
an executable future acceptance gate for FH/LSZ production chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json"

PARENTS = {
    "finite_source_shift_derivative_no_go": "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json",
    "fh_production_protocol": "outputs/yt_fh_production_protocol_certificate_2026-05-01.json",
    "chunked_manifest": "outputs/yt_fh_lsz_chunked_production_manifest_2026-05-01.json",
    "chunk_combiner_gate": "outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json",
    "production_postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
    "finite_source_linearity_calibration_checkpoint": "outputs/yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json",
}

CURRENT_CHUNK_SHIFTS = [-0.01, 0.0, 0.01]
CALIBRATION_SHIFTS = [-0.015, -0.01, -0.005, 0.0, 0.005, 0.01, 0.015]
CAMPAIGN_HOURS = 12.0
MAX_CALIBRATION_FRACTIONAL_DEVIATION = 1.0e-3

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


def source_radii(shifts: list[float]) -> list[float]:
    return sorted({round(abs(float(s)), 12) for s in shifts if abs(float(s)) > 0.0})


def symmetric_about_zero(shifts: list[float]) -> bool:
    rounded = {round(float(s), 12) for s in shifts}
    return 0.0 in rounded and all(round(-float(s), 12) in rounded for s in rounded)


def command_for_calibration(seed: int = 2026052001) -> dict[str, Any]:
    source_shift_arg = ",".join(str(x) for x in CALIBRATION_SHIFTS)
    output = "outputs/yt_pr230_fh_lsz_finite_source_linearity_L12_T24_calib001_2026-05-02.json"
    production_output_dir = (
        "outputs/yt_direct_lattice_correlator_production_fh_lsz_linearity/"
        "L12_T24_calib001"
    )
    command = " ".join(
        [
            "python3",
            "scripts/yt_direct_lattice_correlator_production.py",
            "--volumes",
            "12x24",
            "--masses",
            "0.45,0.75,1.05",
            "--therm",
            "1000",
            "--measurements",
            "16",
            "--separation",
            "20",
            "--engine",
            "numba",
            "--production-targets",
            f"--scalar-source-shifts={source_shift_arg}",
            "--scalar-two-point-modes",
            "'0,0,0;1,0,0;0,1,0;0,0,1'",
            "--scalar-two-point-noises",
            "16",
            "--production-output-dir",
            production_output_dir,
            "--resume",
            "--seed",
            str(seed),
            "--output",
            output,
        ]
    )
    return {
        "calibration_index": 1,
        "seed": seed,
        "volume": "12x24",
        "source_shifts": CALIBRATION_SHIFTS,
        "source_radii": source_radii(CALIBRATION_SHIFTS),
        "output": output,
        "production_output_dir": production_output_dir,
        "command": command,
        "status": (
            "launch command only; not evidence until completed, accepted by "
            "finite-source-linearity, scalar-LSZ, FV/IR/model-class, and "
            "canonical-Higgs identity gates"
        ),
    }


def main() -> int:
    print("PR #230 FH/LSZ finite-source-linearity gate")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    current_radii = source_radii(CURRENT_CHUNK_SHIFTS)
    calibration_radii = source_radii(CALIBRATION_SHIFTS)
    current_source_factor = len(CURRENT_CHUNK_SHIFTS)
    calibration_source_factor = len(CALIBRATION_SHIFTS)
    source_factor_ratio = calibration_source_factor / current_source_factor
    base_chunk_hours = float(
        parents["chunked_manifest"].get("chunk_policy", {}).get("estimated_l12_chunk_hours", 0.0)
    )
    estimated_calibration_hours = base_chunk_hours * source_factor_ratio
    calibration_command = command_for_calibration()

    finite_source_no_go_loaded = (
        "finite source-shift slope not zero-source derivative certificate"
        in status(parents["finite_source_shift_derivative_no_go"])
        and parents["finite_source_shift_derivative_no_go"].get("finite_source_shift_derivative_gate_passed")
        is False
    )
    protocol_support_only = (
        "Feynman-Hellmann production protocol" in status(parents["fh_production_protocol"])
        and parents["fh_production_protocol"].get("proposal_allowed") is False
    )
    chunked_manifest_support_only = (
        "chunked production manifest" in status(parents["chunked_manifest"])
        and parents["chunked_manifest"].get("proposal_allowed") is False
    )
    combiner_not_evidence = (
        "chunk combiner gate" in status(parents["chunk_combiner_gate"])
        and parents["chunk_combiner_gate"].get("proposal_allowed") is False
    )
    postprocess_not_ready = (
        "postprocess gate" in status(parents["production_postprocess_gate"])
        and parents["production_postprocess_gate"].get("retained_proposal_gate_ready") is False
    )
    calibration_checkpoint = parents["finite_source_linearity_calibration_checkpoint"]
    calibration_fit = calibration_checkpoint.get("zero_source_fit", {})
    calibration_fractional_deviation = calibration_fit.get("max_fractional_deviation_from_intercept")
    calibration_support_passed = (
        calibration_checkpoint.get("calibration_gate_passed") is True
        and isinstance(calibration_fractional_deviation, (int, float))
        and calibration_fractional_deviation < MAX_CALIBRATION_FRACTIONAL_DEVIATION
    )

    current_gate_passed = calibration_support_passed
    future_gate_passed = False
    current_has_single_radius = len(current_radii) == 1
    calibration_has_three_radii = len(calibration_radii) >= 3
    calibration_symmetric = symmetric_about_zero(CALIBRATION_SHIFTS)
    calibration_foreground_sized = 0.0 < estimated_calibration_hours < CAMPAIGN_HOURS

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("finite-source-no-go-loaded", finite_source_no_go_loaded, status(parents["finite_source_shift_derivative_no_go"]))
    report("fh-production-protocol-support-only", protocol_support_only, status(parents["fh_production_protocol"]))
    report("chunked-manifest-support-only", chunked_manifest_support_only, status(parents["chunked_manifest"]))
    report("chunk-combiner-not-evidence", combiner_not_evidence, status(parents["chunk_combiner_gate"]))
    report("postprocess-gate-not-ready", postprocess_not_ready, status(parents["production_postprocess_gate"]))
    report("current-chunks-have-single-radius", current_has_single_radius, f"radii={current_radii}")
    report(
        "finite-source-linearity-calibration-checkpoint-loaded",
        bool(calibration_checkpoint),
        status(calibration_checkpoint),
    )
    report(
        "finite-source-linearity-calibration-support-passed",
        calibration_support_passed,
        f"max_fractional_deviation={calibration_fractional_deviation}",
    )
    report(
        "current-finite-source-linearity-gate-state-recorded",
        True,
        f"passed={current_gate_passed}; current chunks use one radius, calibration supplies multi-radius support",
    )
    report("future-calibration-symmetric", calibration_symmetric, f"shifts={CALIBRATION_SHIFTS}")
    report("future-calibration-has-three-radii", calibration_has_three_radii, f"radii={calibration_radii}")
    report(
        "future-calibration-not-foreground-sized",
        not calibration_foreground_sized,
        f"estimated_hours={estimated_calibration_hours:.6g}",
    )
    report("future-calibration-is-not-evidence-yet", not future_gate_passed, "manifest command only")

    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ finite-source-linearity gate passed as response support"
            if current_gate_passed
            else "open / FH-LSZ finite-source-linearity gate not passed"
        ),
        "verdict": (
            (
                "The current production chunks use one nonzero source radius, "
                "but the separate multi-radius calibration checkpoint is now "
                "present and supports a small finite-source extrapolation "
                "remainder.  This passes finite-source-linearity as response "
                "support only.  It does not bypass response-window acceptance, "
                "fitted/replacement response stability, scalar LSZ, FV/IR/"
                "model-class, or canonical-Higgs identity gates."
            )
            if current_gate_passed
            else (
                "The current FH/LSZ chunks use one nonzero symmetric source "
                "radius, so they cannot certify the zero-source "
                "Feynman-Hellmann derivative.  A future production-grade "
                "response gate must include multiple nonzero radii on common "
                "ensembles and fit the finite slopes S(delta) against delta^2 "
                "with a certified small remainder, or it must supply a "
                "retained analytic response-bound theorem."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-source-linearity is response support only and does not close scalar LSZ or canonical-Higgs identity.",
        "finite_source_linearity_gate_passed": current_gate_passed,
        "current_source_shifts": CURRENT_CHUNK_SHIFTS,
        "current_source_radii": current_radii,
        "acceptance_requirements": {
            "minimum_nonzero_source_radii_without_response_bound": 3,
            "same_gauge_configurations_for_all_source_shifts": True,
            "symmetric_source_shifts_required": True,
            "fit_space": "finite slopes S(delta) versus delta^2",
            "load_bearing_acceptance": (
                "intercept dE/ds|_0 accepted only with a small certified "
                "higher-order remainder or retained response-bound theorem"
            ),
            "still_required_after_linearity": [
                "same-source scalar LSZ pole derivative",
                "FV/IR/zero-mode and model-class gates",
                "canonical-Higgs source-pole identity",
                "retained-proposal certificate",
            ],
        },
        "calibration_checkpoint": {
            "path": PARENTS["finite_source_linearity_calibration_checkpoint"],
            "calibration_gate_passed": calibration_checkpoint.get("calibration_gate_passed"),
            "source_radii": calibration_checkpoint.get("source_radii"),
            "zero_source_fit": calibration_fit,
            "max_fractional_deviation_threshold": MAX_CALIBRATION_FRACTIONAL_DEVIATION,
            "calibration_support_passed": calibration_support_passed,
        },
        "future_calibration_manifest": {
            "source_shifts": CALIBRATION_SHIFTS,
            "source_radii": calibration_radii,
            "source_count_factor_over_current": source_factor_ratio,
            "base_l12_chunk_hours": base_chunk_hours,
            "estimated_l12_calibration_chunk_hours": estimated_calibration_hours,
            "foreground_window_hours": CAMPAIGN_HOURS,
            "calibration_command": calibration_command,
        },
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat current single-radius dE/ds as zero-source dE/ds",
            "does not treat finite-source-linearity as scalar LSZ or canonical-Higgs identity",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass/y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Either schedule a multi-radius finite-source-linearity calibration "
            "with at least three nonzero radii and a response-bound acceptance "
            "rule, or keep current single-radius chunks as response diagnostics "
            "while attacking scalar LSZ/canonical-Higgs identity directly."
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
