#!/usr/bin/env python3
"""
PR #230 FH/LSZ scalar-pole fit postprocessor scaffold.

This runner is production-facing support, not evidence.  It defines the strict
data shape needed to fit Gamma_ss(p^2), locate an isolated scalar pole, and
extract dGamma_ss/dp^2 for the same source used in dE_top/ds.  With the current
repo surface the combined production input is absent, so the runner exits as
an open gate and does not authorize retained/proposed-retained wording.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json"
CHUNK_GATE = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
KINEMATICS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_postprocessor_2026-05-01.json"

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def extract_mode_rows(data: dict[str, Any]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    candidates: list[Any] = []
    if isinstance(data.get("combined_lsz_summary"), dict):
        candidates.append(data["combined_lsz_summary"].get("mode_rows"))
    if isinstance(data.get("scalar_two_point_lsz_analysis"), dict):
        candidates.append(data["scalar_two_point_lsz_analysis"].get("mode_rows"))
    for candidate in candidates:
        if isinstance(candidate, dict):
            iterator = candidate.values()
        elif isinstance(candidate, list):
            iterator = candidate
        else:
            continue
        for row in iterator:
            if not isinstance(row, dict):
                continue
            p_hat_sq = row.get("p_hat_sq")
            gamma = row.get("Gamma_ss_real") or row.get("Gamma_ss_real_mean") or row.get("Gamma_ss_real_proxy")
            gamma_err = row.get("Gamma_ss_real_err") or row.get("Gamma_ss_real_stderr")
            if finite(p_hat_sq) and finite(gamma):
                rows.append(
                    {
                        "p_hat_sq": float(p_hat_sq),
                        "Gamma_ss_real": float(gamma),
                        "Gamma_ss_real_err": float(gamma_err) if finite(gamma_err) else float("nan"),
                    }
                )
        if rows:
            break
    return rows


def distinct_shell_count(rows: list[dict[str, float]]) -> int:
    return len({round(row["p_hat_sq"], 12) for row in rows})


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
        "fit_kind": "weighted_linear_Gamma_vs_p_hat_sq",
        "intercept": intercept,
        "slope_dGamma_dp_hat_sq": slope,
        "pole_p_hat_sq": float(pole_x),
        "chi2": chi2,
        "dof": dof,
        "input_rows": rows,
    }


def main() -> int:
    print("PR #230 FH/LSZ scalar-pole fit postprocessor scaffold")
    print("=" * 72)

    data = load_json(DEFAULT_INPUT)
    chunk_gate = load_json(CHUNK_GATE)
    kinematics_gate = load_json(KINEMATICS_GATE)
    mode_rows = extract_mode_rows(data)
    shells = distinct_shell_count(mode_rows)
    has_zero = any(abs(row["p_hat_sq"]) < 1e-12 for row in mode_rows)
    has_three_positive_shells = len({round(row["p_hat_sq"], 12) for row in mode_rows if row["p_hat_sq"] > 1e-12}) >= 3
    fit_ready = bool(data) and has_zero and has_three_positive_shells and shells >= 4
    fit_result = weighted_linear_fit(mode_rows) if fit_ready else {}
    isolated_pole_ready = fit_ready and fit_result.get("pole_p_hat_sq", 1.0) < 0.0

    report("chunk-combiner-gate-loaded", bool(chunk_gate), str(CHUNK_GATE.relative_to(ROOT)))
    report("kinematics-gate-loaded", bool(kinematics_gate), str(KINEMATICS_GATE.relative_to(ROOT)))
    report("combined-production-input-absent-or-nonready", not fit_ready, f"input={DEFAULT_INPUT.relative_to(ROOT)}, rows={len(mode_rows)}, shells={shells}")
    report("requires-zero-plus-three-positive-shells", not fit_ready or (has_zero and has_three_positive_shells), f"has_zero={has_zero}, positive_shells={has_three_positive_shells}")
    report("does-not-authorize-retained-proposal", True, "postprocessor scaffold is not production evidence")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ scalar-pole fit postprocessor scaffold",
        "verdict": (
            "The runner defines a concrete postprocess path for future combined "
            "same-source FH/LSZ production output: require a zero mode plus at "
            "least three positive momentum shells, fit Gamma_ss versus p_hat^2, "
            "and use only an isolated negative-p_hat^2 pole with finite slope as "
            "a candidate dGamma_ss/dp^2 input.  The current combined production "
            "input is absent/nonready, so no pole derivative or retained proposal "
            "is authorized."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No combined production same-source pole-fit data are present.",
        "input": str(DEFAULT_INPUT.relative_to(ROOT)),
        "parent_certificates": {
            "chunk_combiner_gate": str(CHUNK_GATE.relative_to(ROOT)),
            "kinematics_gate": str(KINEMATICS_GATE.relative_to(ROOT)),
        },
        "readiness": {
            "input_exists": bool(data),
            "mode_rows": len(mode_rows),
            "distinct_shells": shells,
            "has_zero_shell": has_zero,
            "has_three_positive_shells": has_three_positive_shells,
            "fit_ready": fit_ready,
            "isolated_negative_pole_ready": isolated_pole_ready,
        },
        "fit_result_if_ready": fit_result,
        "strict_non_claims": [
            "not production evidence until input exists and passes combiner/postprocess gates",
            "does not set kappa_s = 1",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
        ],
        "exact_next_action": (
            "After chunk outputs are combined, rerun this postprocessor on the combined same-source Gamma_ss(q) rows; until then continue analytic LSZ work or production scheduling."
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
