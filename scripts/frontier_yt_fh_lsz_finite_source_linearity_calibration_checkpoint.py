#!/usr/bin/env python3
"""
PR #230 FH/LSZ finite-source-linearity calibration checkpoint.

This runner consumes the multi-radius source-shift calibration output when it
exists.  The calibration tests whether the finite symmetric slopes
S(delta) = [E(+delta)-E(-delta)]/(2 delta) have a controlled intercept as
delta -> 0.  It is a response-window acceptance diagnostic only; it never
turns source-coordinate response into physical y_t evidence.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_finite_source_linearity_L12_T24_calib001_2026-05-02.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_fh_lsz_finite_source_linearity_calibration_checkpoint_2026-05-03.json"

PARENTS = {
    "finite_source_linearity_gate": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "finite_source_shift_derivative_no_go": "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json",
    "response_window_acceptance": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
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


def round_float(value: float, digits: int = 12) -> float:
    rounded = round(float(value), digits)
    return 0.0 if rounded == -0.0 else rounded


def source_radii(shifts: list[float]) -> list[float]:
    return sorted({round_float(abs(x)) for x in shifts if abs(x) > 0.0})


def symmetric_shift_set(shifts: list[float]) -> bool:
    rounded = {round_float(x) for x in shifts}
    return 0.0 in rounded and all(round_float(-x) in rounded for x in rounded)


def selected_ensemble(cert: dict[str, Any]) -> dict[str, Any]:
    ensembles = cert.get("ensembles", [])
    if isinstance(ensembles, list) and ensembles:
        row = ensembles[0]
        return row if isinstance(row, dict) else {}
    return {}


def energy_fits_by_shift(ensemble: dict[str, Any]) -> dict[float, dict[str, Any]]:
    source = ensemble.get("scalar_source_response_analysis", {})
    fits = source.get("energy_fits", [])
    rows: dict[float, dict[str, Any]] = {}
    if not isinstance(fits, list):
        return rows
    for fit in fits:
        if not isinstance(fit, dict):
            continue
        shift = fit.get("source_shift_lat")
        if finite(shift):
            rows[round_float(float(shift))] = fit
    return rows


def slope_rows(fits: dict[float, dict[str, Any]]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for radius in source_radii(list(fits)):
        plus = fits.get(radius)
        minus = fits.get(round_float(-radius))
        if not plus or not minus:
            continue
        e_plus = plus.get("energy_lat")
        e_minus = minus.get("energy_lat")
        err_plus = plus.get("energy_lat_err")
        err_minus = minus.get("energy_lat_err")
        if not all(finite(x) for x in (e_plus, e_minus, err_plus, err_minus)):
            continue
        slope = (float(e_plus) - float(e_minus)) / (2.0 * radius)
        slope_err = math.sqrt(float(err_plus) ** 2 + float(err_minus) ** 2) / (2.0 * radius)
        rows.append(
            {
                "source_radius": radius,
                "radius_sq": radius * radius,
                "symmetric_slope": slope,
                "symmetric_slope_error": slope_err,
            }
        )
    return rows


def weighted_linear_fit(rows: list[dict[str, float]]) -> dict[str, Any]:
    if len(rows) < 3:
        return {"available": False, "reason": "fewer than three nonzero source radii"}
    x = np.asarray([row["radius_sq"] for row in rows], dtype=float)
    y = np.asarray([row["symmetric_slope"] for row in rows], dtype=float)
    err = np.asarray([max(row["symmetric_slope_error"], 1.0e-12) for row in rows], dtype=float)
    weights = 1.0 / (err * err)
    design = np.vstack([np.ones_like(x), x]).T
    lhs = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * y)
    beta = np.linalg.solve(lhs, rhs)
    residual = y - design @ beta
    dof = max(1, len(rows) - 2)
    chi2 = float(np.sum(weights * residual * residual))
    cov = np.linalg.inv(lhs)
    intercept_err = math.sqrt(max(float(cov[0, 0]), 0.0))
    slope_err = math.sqrt(max(float(cov[1, 1]), 0.0))
    return {
        "available": True,
        "fit_model": "S(delta) = intercept + curvature * delta^2",
        "intercept_dE_ds_zero_source": float(beta[0]),
        "intercept_error": intercept_err,
        "curvature": float(beta[1]),
        "curvature_error": slope_err,
        "chi2": chi2,
        "dof": dof,
        "chi2_dof": chi2 / dof,
        "max_fractional_deviation_from_intercept": float(
            max(abs((row["symmetric_slope"] - beta[0]) / beta[0]) for row in rows)
        )
        if abs(float(beta[0])) > 1.0e-12
        else None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 FH/LSZ finite-source-linearity calibration checkpoint")
    print("=" * 78)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    cert = load_json(args.input)
    output_present = bool(cert)
    ensemble = selected_ensemble(cert)
    fits = energy_fits_by_shift(ensemble)
    shifts = sorted(fits)
    radii = source_radii(shifts)
    slopes = slope_rows(fits)
    fit = weighted_linear_fit(slopes)

    phase = str(cert.get("metadata", {}).get("phase", ""))
    run_control = cert.get("metadata", {}).get("run_control", {})
    selected_policy = ensemble.get("fh_lsz_measurement_policy", {})
    multi_radius_complete = output_present and len(radii) >= 3 and len(slopes) >= 3
    symmetric = symmetric_shift_set(shifts) if shifts else False
    common_ensemble = (
        output_present
        and ensemble.get("measurement_sweeps") == 16
        and run_control.get("volumes") == "12x24"
        and run_control.get("seed") == 2026052001
    )
    forbidden_readout = (
        cert.get("metadata", {}).get("uses_prior_ward_chain") is False
        and cert.get("metadata", {}).get("uses_composite_matrix_element_route") is False
        and selected_policy.get("used_as_physical_yukawa_readout") is False
    )
    fit_available = fit.get("available") is True

    parent_gate_open = (
        "finite-source-linearity gate not passed" in status(parents["finite_source_linearity_gate"])
        and parents["finite_source_linearity_gate"].get("proposal_allowed") is False
    )
    derivative_no_go_loaded = (
        "finite source-shift slope not zero-source derivative certificate"
        in status(parents["finite_source_shift_derivative_no_go"])
    )
    response_window_still_open = (
        "response-window acceptance gate not passed" in status(parents["response_window_acceptance"])
        and parents["response_window_acceptance"].get("response_window_acceptance_gate_passed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("parent-finite-source-gate-open", parent_gate_open, status(parents["finite_source_linearity_gate"]))
    report("finite-source-derivative-no-go-loaded", derivative_no_go_loaded, status(parents["finite_source_shift_derivative_no_go"]))
    report("response-window-gate-still-open", response_window_still_open, status(parents["response_window_acceptance"]))
    report("calibration-output-state-recorded", True, f"present={output_present}, input={args.input.relative_to(ROOT)}")
    if output_present:
        report("production-phase", phase == "production", phase)
        report("source-shifts-symmetric", symmetric, f"shifts={shifts}")
        report("at-least-three-source-radii", len(radii) >= 3, f"radii={radii}")
        report("common-ensemble-run-control", common_ensemble, f"run_control={run_control}")
        report("symmetric-slope-rows-present", len(slopes) >= 3, f"rows={len(slopes)}")
        report("zero-source-intercept-fit-available", fit_available, json.dumps(fit, sort_keys=True))
        report("forbidden-readout-routes-absent", forbidden_readout, "metadata firewalls keep calibration non-readout")
    else:
        report("calibration-output-awaiting", True, "multi-radius run not complete yet")

    calibration_gate_passed = output_present and multi_radius_complete and symmetric and common_ensemble and fit_available
    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ finite-source-linearity calibration checkpoint"
            if calibration_gate_passed
            else "open / FH-LSZ finite-source-linearity calibration awaiting output"
        ),
        "verdict": (
            "The multi-radius calibration output is present and supports a "
            "finite zero-source intercept fit for the source-coordinate FH "
            "response.  This is bounded response-window support only: it does "
            "not supply scalar LSZ pole control, FV/IR/model-class closure, or "
            "canonical-Higgs/source-overlap identity."
            if calibration_gate_passed
            else (
                "The multi-radius finite-source-linearity calibration is not "
                "complete on the current surface.  The current source-only "
                "chunks still use one nonzero source radius and cannot certify "
                "the zero-source Feynman-Hellmann derivative."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-source-linearity is response support only and does not close scalar LSZ or canonical-Higgs identity.",
        "calibration_gate_passed": calibration_gate_passed,
        "calibration_output": str(args.input.relative_to(ROOT)) if args.input.is_relative_to(ROOT) else str(args.input),
        "calibration_output_present": output_present,
        "source_shifts": shifts,
        "source_radii": radii,
        "symmetric_slope_rows": slopes,
        "zero_source_fit": fit,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat source-coordinate dE/ds as physical dE/dh",
            "does not set kappa_s = 1",
            "does not supply scalar LSZ pole derivative, FV/IR, model-class, or canonical-Higgs identity",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "When the calibration output completes, rerun this checkpoint and "
            "then rerun the response-window acceptance, retained-route, and "
            "campaign-status certificates.  Even a passing calibration must be "
            "followed by scalar-pole and canonical-Higgs identity gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {args.output.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
