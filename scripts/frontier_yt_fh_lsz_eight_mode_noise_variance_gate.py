#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode noise variance gate.

The mode/noise budget found an eight-mode/eight-noise L12 chunk shape that
fits the current foreground estimate.  This runner asks the narrower question:
is the noise reduction from sixteen to eight vectors already justified by
same-source variance evidence?  It is an acceptance gate, not a production
launcher and not retained closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODE_BUDGET = ROOT / "outputs" / "yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json"
COMBINER_GATE = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
JOINT_SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json"
CHUNK001 = ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunk001_2026-05-01.json"
EXPECTED_CALIBRATION = (
    ROOT
    / "outputs"
    / "yt_pr230_fh_lsz_production_L12_T24_eightmode_x8_variance_calibration_2026-05-01.json"
)
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json"

EXPECTED_EIGHT_MODE_KEYS = {
    "0,0,0",
    "1,0,0",
    "1,1,0",
    "1,1,1",
    "2,0,0",
    "2,1,0",
    "2,1,1",
    "2,2,0",
}
MIN_CALIBRATION_CONFIGS = 16
REFERENCE_NOISES = 16
CANDIDATE_NOISES = 8

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


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if not isinstance(ensembles, list) or len(ensembles) != 1:
        return {}
    first = ensembles[0]
    return first if isinstance(first, dict) else {}


def scalar_lsz_metadata(data: dict[str, Any]) -> dict[str, Any]:
    metadata = data.get("metadata", {})
    scalar_meta = metadata.get("scalar_two_point_lsz")
    return scalar_meta if isinstance(scalar_meta, dict) else {}


def scalar_lsz_rows(data: dict[str, Any]) -> dict[str, Any]:
    ensemble = selected_ensemble(data)
    analysis = ensemble.get("scalar_two_point_lsz_analysis")
    if not isinstance(analysis, dict):
        return {}
    rows = analysis.get("mode_rows")
    return rows if isinstance(rows, dict) else {}


def candidate_from_output(name: str, path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not data:
        return {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "exists": False,
            "variance_calibration_ready": False,
            "issues": ["output absent"],
        }

    metadata = data.get("metadata", {})
    ensemble = selected_ensemble(data)
    scalar_meta = scalar_lsz_metadata(data)
    rows = scalar_lsz_rows(data)
    analysis = selected_ensemble(data).get("scalar_two_point_lsz_analysis", {})
    mode_keys = set(rows)
    config_counts = [
        int(row.get("configuration_count", 0))
        for row in rows.values()
        if isinstance(row, dict)
    ]
    issues: list[str] = []

    if metadata.get("phase") != "production":
        issues.append(f"phase={metadata.get('phase')!r}, expected production")
    if scalar_meta.get("noise_vectors_per_configuration") != CANDIDATE_NOISES:
        issues.append(
            "noise_vectors_per_configuration="
            f"{scalar_meta.get('noise_vectors_per_configuration')!r}, expected {CANDIDATE_NOISES}"
        )
    missing_modes = sorted(EXPECTED_EIGHT_MODE_KEYS - mode_keys)
    if missing_modes:
        issues.append(f"missing eight-mode rows {missing_modes}")
    min_configs = min(config_counts) if config_counts else 0
    if min_configs < MIN_CALIBRATION_CONFIGS:
        issues.append(f"configuration_count_min={min_configs}, expected >= {MIN_CALIBRATION_CONFIGS}")
    if not any(
        isinstance(row, dict) and float(row.get("C_ss_real_config_stderr", 0.0)) > 0.0
        for row in rows.values()
    ):
        issues.append("no positive configuration stderr for C_ss_real")
    if (
        "noise_subsample_stability" not in ensemble
        and "noise_subsample_stability" not in scalar_meta
        and not (isinstance(analysis, dict) and "noise_subsample_stability" in analysis)
    ):
        issues.append("no noise_subsample_stability field")

    return {
        "name": name,
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "phase": metadata.get("phase"),
        "dims": ensemble.get("dims"),
        "noise_vectors_per_configuration": scalar_meta.get("noise_vectors_per_configuration"),
        "mode_count": len(mode_keys),
        "mode_keys": sorted(mode_keys),
        "configuration_count_min": min_configs,
        "variance_calibration_ready": not issues,
        "issues": issues,
    }


def find_candidate(mode_budget: dict[str, Any], name: str) -> dict[str, Any]:
    for candidate in mode_budget.get("candidates", []):
        if candidate.get("name") == name:
            return candidate
    return {}


def main() -> int:
    print("PR #230 FH/LSZ eight-mode noise variance gate")
    print("=" * 72)

    mode_budget = load_json(MODE_BUDGET)
    combiner = load_json(COMBINER_GATE)
    x8_candidate = find_candidate(mode_budget, "pole_fit_eight_modes_x8_noise")
    inflation = math.sqrt(REFERENCE_NOISES / CANDIDATE_NOISES)

    current_surfaces = [
        candidate_from_output("reduced_joint_smoke", JOINT_SMOKE),
        candidate_from_output("foreground_chunk001", CHUNK001),
        candidate_from_output("expected_eightmode_x8_calibration", EXPECTED_CALIBRATION),
    ]
    ready_surfaces = [row for row in current_surfaces if row.get("variance_calibration_ready") is True]
    reduced_smoke = current_surfaces[0]
    chunk001 = current_surfaces[1]

    report("mode-budget-loaded", bool(mode_budget), str(MODE_BUDGET.relative_to(ROOT)))
    report("combiner-gate-loaded", bool(combiner), str(COMBINER_GATE.relative_to(ROOT)))
    report(
        "eight-mode-x8-candidate-present",
        bool(x8_candidate),
        f"modes={x8_candidate.get('mode_count')} noises={x8_candidate.get('noise_vectors')}",
    )
    report(
        "eight-mode-x8-has-pole-fit-kinematics",
        x8_candidate.get("pole_fit_kinematics_ready") is True,
        f"shells={x8_candidate.get('distinct_shell_count')}",
    )
    report(
        "eight-mode-x8-fits-foreground-estimate",
        x8_candidate.get("fits_12h_foreground") is True,
        f"hours={x8_candidate.get('estimated_l12_chunk_hours')}",
    )
    report(
        "noise-reduction-has-known-stderr-inflation",
        inflation > 1.0,
        f"x8 stochastic stderr multiplier vs x16 is {inflation:.6g}",
    )
    report(
        "reduced-smoke-disqualified",
        reduced_smoke.get("variance_calibration_ready") is False
        and "phase='reduced_scope', expected production" in reduced_smoke.get("issues", []),
        "; ".join(reduced_smoke.get("issues", [])[:3]),
    )
    report(
        "chunk001-not-eight-mode-x8-calibration",
        chunk001.get("variance_calibration_ready") is False,
        "; ".join(chunk001.get("issues", [])[:3]),
    )
    report(
        "variance-gate-not-passed",
        not ready_surfaces,
        f"ready_calibration_surfaces={len(ready_surfaces)}",
    )
    report("not-retained-closure", True, "variance gating is launch control, not a scalar LSZ theorem")

    result = {
        "actual_current_surface_status": "open / FH-LSZ eight-mode noise variance gate not passed",
        "verdict": (
            "The eight-mode/eight-noise L12 chunk shape is pole-fit-kinematics "
            "ready and fits the current foreground estimate, but lowering the "
            "stochastic scalar-LSZ noise count from 16 to 8 increases the "
            f"noise-only standard error by sqrt(2) = {inflation:.6g}.  The "
            "current repo surface has no same-source production calibration "
            "showing that this inflation leaves C_ss(q), Gamma_ss(q), and the "
            "pole-derivative fit stable.  The reduced smoke output is wrong "
            "phase, wrong volume, two modes, two noises, and one configuration.  "
            "The foreground chunk001 surface is absent or four-mode/x16 and is "
            "not an eight-mode/x8 variance calibration.  Therefore the x8 "
            "option remains planning support only; it is not production "
            "evidence and cannot be used for a retained or proposed-retained "
            "top-Yukawa claim."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No production same-source eight-mode/x8 variance calibration or theorem is present.",
        "variance_gate_passed": False,
        "eight_mode_x8_launch_allowed_as_retained_evidence": False,
        "stochastic_standard_error_multiplier_vs_x16": inflation,
        "parent_certificates": {
            "mode_budget": str(MODE_BUDGET.relative_to(ROOT)),
            "chunk_combiner_gate": str(COMBINER_GATE.relative_to(ROOT)),
        },
        "candidate_from_mode_budget": x8_candidate,
        "current_surfaces": current_surfaces,
        "acceptance_requirements": [
            "production phase output on the same additive scalar source coordinate as dE_top/ds",
            "eight specified scalar-LSZ modes with eight noise vectors per configuration",
            "at least 16 saved configurations for a calibration chunk",
            "positive finite configuration stderr or explicit noise-subsample stability for C_ss(q)",
            "paired x16 reference or a derived stochastic variance bound for the same modes",
            "stable Gamma_ss(q) and pole-derivative fit under x8 versus x16 noise choices",
            "no use of reduced cold pilots as production evidence",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a kappa_s derivation",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit matrix-element readout",
            "does not use yt_ward_identity as authority",
            "does not use observed top mass or observed y_t",
            "does not use alpha_LM, plaquette, or u0 as proof input",
        ],
        "exact_next_action": (
            "Keep the running four-mode/x16 chunk as non-evidence until the "
            "combiner gate can inspect completed output.  For a pole-fit-ready "
            "foreground campaign, either add a paired eight-mode x8/x16 "
            "calibration chunk with noise-subsample diagnostics, or stay with "
            "the x16 noise plan and schedule beyond the 12-hour foreground "
            "window."
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
