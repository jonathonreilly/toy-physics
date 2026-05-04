#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode/x8 pole-fit diagnostic postprocessor.

This consumes only the separate polefit8x8 combined support surface.  It may
produce a finite-shell diagnostic fit, but finite-shell fits remain blocked as
retained evidence by the model-class/FV/IR/source-Higgs gates.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_polefit8x8_L12_T24_chunked_combined_2026-05-04.json"
COMBINER = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json"
MODEL_CLASS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json"

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def extract_mode_rows(data: dict[str, Any]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    raw = data.get("combined_lsz_summary", {}).get("mode_rows")
    iterable = raw.values() if isinstance(raw, dict) else raw if isinstance(raw, list) else []
    for row in iterable:
        if not isinstance(row, dict):
            continue
        p_hat_sq = row.get("p_hat_sq")
        gamma = row.get("Gamma_ss_real_proxy") or row.get("Gamma_ss_real") or row.get("Gamma_ss_real_mean")
        gamma_err = row.get("Gamma_ss_real_stderr")
        if finite(p_hat_sq) and finite(gamma):
            rows.append(
                {
                    "p_hat_sq": float(p_hat_sq),
                    "Gamma_ss_real": float(gamma),
                    "Gamma_ss_real_err": float(gamma_err) if finite(gamma_err) else float("nan"),
                }
            )
    return sorted(rows, key=lambda row: row["p_hat_sq"])


def weighted_linear_fit(rows: list[dict[str, float]]) -> dict[str, Any]:
    xs = np.asarray([row["p_hat_sq"] for row in rows], dtype=float)
    ys = np.asarray([row["Gamma_ss_real"] for row in rows], dtype=float)
    errs = np.asarray([row["Gamma_ss_real_err"] for row in rows], dtype=float)
    weights = np.ones_like(xs)
    mask = np.isfinite(errs) & (errs > 0.0)
    weights[mask] = 1.0 / np.square(errs[mask])
    design = np.vstack([np.ones_like(xs), xs]).T
    normal = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * ys)
    coeff = np.linalg.solve(normal, rhs)
    intercept = float(coeff[0])
    slope = float(coeff[1])
    pole_x = -intercept / slope if slope != 0.0 else float("nan")
    residuals = ys - design @ coeff
    chi2 = float(np.sum(weights * residuals * residuals))
    dof = max(len(xs) - 2, 0)
    return {
        "fit_kind": "diagnostic_weighted_linear_Gamma_vs_p_hat_sq",
        "intercept": intercept,
        "slope_dGamma_dp_hat_sq": slope,
        "pole_p_hat_sq": float(pole_x),
        "chi2": chi2,
        "dof": dof,
        "input_rows": rows,
        "strict_limit": "finite-shell diagnostic only; model-class/FV/IR/source-Higgs gates remain load-bearing",
    }


def main() -> int:
    print("PR #230 FH/LSZ eight-mode/x8 pole-fit diagnostic postprocessor")
    print("=" * 72)

    data = load_json(INPUT)
    combiner = load_json(COMBINER)
    model_class = load_json(MODEL_CLASS_GATE)
    rows = extract_mode_rows(data)
    shells = {round(row["p_hat_sq"], 12) for row in rows}
    positive_shells = {value for value in shells if value > 1.0e-12}
    has_zero = any(abs(row["p_hat_sq"]) < 1.0e-12 for row in rows)
    diagnostic_fit_ready = bool(data) and has_zero and len(positive_shells) >= 3
    fit = weighted_linear_fit(rows) if diagnostic_fit_ready else {}
    saved_configs = int(data.get("metadata", {}).get("saved_configurations", 0)) if data else 0
    complete_l12 = data.get("metadata", {}).get("complete_l12_target") is True if data else False
    model_class_blocks = "blocks finite-shell fit" in str(model_class.get("actual_current_surface_status", ""))

    report("combiner-loaded", bool(combiner), rel(COMBINER))
    report("combined-input-state-recorded", True, f"input_exists={bool(data)} saved_configs={saved_configs}")
    report("zero-plus-three-positive-shell-diagnostic-ready-or-awaiting-data", not data or diagnostic_fit_ready, f"rows={len(rows)} positive_shells={len(positive_shells)}")
    report("model-class-gate-still-blocks-retained-use", model_class_blocks, str(model_class.get("actual_current_surface_status", "")))
    report("does-not-authorize-retained-proposal", True, "diagnostic postprocess is support-only")

    status = (
        "bounded-support / FH-LSZ eight-mode-x8 finite-shell pole diagnostic"
        if diagnostic_fit_ready
        else "open / FH-LSZ eight-mode-x8 pole diagnostic awaiting combined rows"
    )
    result = {
        "actual_current_surface_status": status,
        "verdict": (
            "The eight-mode/x8 postprocessor consumes only the separate polefit8x8 "
            "combined support surface.  It can form a finite-shell diagnostic "
            "Gamma_ss(p_hat^2) fit when the zero shell and at least three positive "
            "shells are present.  This remains support-only because finite-shell "
            "identifiability, model-class, FV/IR, and canonical-Higgs/source-overlap "
            "authority remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-shell diagnostic fits do not provide retained scalar LSZ normalization.",
        "input": rel(INPUT),
        "parent_certificates": {
            "polefit8x8_combiner": rel(COMBINER),
            "model_class_gate": rel(MODEL_CLASS_GATE),
        },
        "readiness": {
            "input_exists": bool(data),
            "mode_rows": len(rows),
            "distinct_shells": len(shells),
            "positive_shells": len(positive_shells),
            "has_zero_shell": has_zero,
            "diagnostic_fit_ready": diagnostic_fit_ready,
            "saved_configurations": saved_configs,
            "complete_l12_target": complete_l12,
            "model_class_blocks_retained_use": model_class_blocks,
        },
        "diagnostic_fit_if_ready": fit,
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not mix eight-mode/x8 and four-mode/x16 chunks as one homogeneous ensemble",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
