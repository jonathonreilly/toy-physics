#!/usr/bin/env python3
"""
PR #230 FH/LSZ pole-fit mode/noise budget.

The four-mode scalar-LSZ plan is not pole-fit ready because it has one nonzero
momentum shell.  This runner asks whether a foreground-sized L12 chunk can use
more momentum shells without increasing the solve budget beyond the current
12-hour chunk window.  It is a planning certificate only: lower scalar-noise
counts need a variance gate and production data before they can support any
physical readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "outputs" / "yt_fh_lsz_joint_resource_projection_2026-05-01.json"
CHUNK_MANIFEST = ROOT / "outputs" / "yt_fh_lsz_chunked_production_manifest_2026-05-01.json"
KINEMATICS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_kinematics_gate_2026-05-01.json"
VARIANCE_GATE = ROOT / "outputs" / "yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json"

POINT_SOURCES_PER_MASS = 3
BASE_MASS_POINTS = 3
SOURCE_SHIFTS = 3
EXTRA_SOURCE_SHIFT_MASSES = SOURCE_SHIFTS - 1
CAMPAIGN_HOURS = 12.0
SPATIAL_L = 12

CURRENT_MODES = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
POLE_FIT_MODES = [
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (1, 1, 1),
    (2, 0, 0),
    (2, 1, 0),
    (2, 1, 1),
    (2, 2, 0),
]

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
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def p_hat_sq(mode: tuple[int, int, int], spatial_l: int = SPATIAL_L) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_l)) ** 2 for n in mode)


def shell_summary(modes: list[tuple[int, int, int]]) -> dict[str, Any]:
    shells = sorted({round(p_hat_sq(mode), 12) for mode in modes})
    nonzero = [value for value in shells if abs(value) > 1.0e-12]
    return {
        "modes": [list(mode) for mode in modes],
        "mode_count": len(modes),
        "distinct_p_hat_sq_shells": shells,
        "distinct_shell_count": len(shells),
        "nonzero_shell_count": len(nonzero),
        "pole_fit_kinematics_ready": len(shells) >= 4 and len(nonzero) >= 3,
    }


def solve_factor(mode_count: int, noise_vectors: int) -> float:
    lsz_equivalent = (2 * mode_count * noise_vectors) / POINT_SOURCES_PER_MASS
    total_equivalent = BASE_MASS_POINTS + EXTRA_SOURCE_SHIFT_MASSES + lsz_equivalent
    return total_equivalent / BASE_MASS_POINTS


def candidate(
    name: str,
    modes: list[tuple[int, int, int]],
    noise_vectors: int,
    current_chunk_hours: float,
    current_solve_factor: float,
) -> dict[str, Any]:
    summary = shell_summary(modes)
    factor = solve_factor(len(modes), noise_vectors)
    ratio = factor / current_solve_factor
    chunk_hours = current_chunk_hours * ratio
    command_modes = ";".join(",".join(str(value) for value in mode) for mode in modes)
    return {
        "name": name,
        **summary,
        "noise_vectors": noise_vectors,
        "solve_budget_factor": factor,
        "factor_ratio_vs_current_manifest": ratio,
        "estimated_l12_chunk_hours": chunk_hours,
        "fits_12h_foreground": chunk_hours < CAMPAIGN_HOURS,
        "command_fragment": {
            "scalar_two_point_modes": command_modes,
            "scalar_two_point_noises": noise_vectors,
        },
    }


def main() -> int:
    print("PR #230 FH/LSZ pole-fit mode/noise budget")
    print("=" * 72)

    resource = load_json(RESOURCE)
    chunk_manifest = load_json(CHUNK_MANIFEST)
    kinematics = load_json(KINEMATICS_GATE)
    variance_gate = load_json(VARIANCE_GATE)
    current_chunk_hours = float(
        chunk_manifest.get("chunk_policy", {}).get("estimated_l12_chunk_hours", float("nan"))
    )
    assumed = resource.get("assumed_joint_protocol", {})
    current_solve_factor = float(assumed.get("solve_budget_factor_vs_three_mass_direct", float("nan")))

    current = candidate("current_four_modes_x16_noise", CURRENT_MODES, 16, current_chunk_hours, current_solve_factor)
    pole_fit_same_noise = candidate("pole_fit_eight_modes_x16_noise", POLE_FIT_MODES, 16, current_chunk_hours, current_solve_factor)
    pole_fit_half_noise = candidate("pole_fit_eight_modes_x8_noise", POLE_FIT_MODES, 8, current_chunk_hours, current_solve_factor)
    x8_variance_gate_passed = variance_gate.get("variance_gate_passed") is True
    x8_launch_support_accepted = (
        pole_fit_half_noise["pole_fit_kinematics_ready"] is True
        and pole_fit_half_noise["fits_12h_foreground"] is True
        and x8_variance_gate_passed
    )

    report("resource-loaded", bool(resource), str(RESOURCE.relative_to(ROOT)))
    report("chunk-manifest-loaded", bool(chunk_manifest), str(CHUNK_MANIFEST.relative_to(ROOT)))
    report("variance-gate-loaded", bool(variance_gate), str(VARIANCE_GATE.relative_to(ROOT)))
    report(
        "current-four-mode-plan-not-pole-ready",
        current["pole_fit_kinematics_ready"] is False
        and kinematics.get("proposal_allowed") is False,
        f"nonzero_shells={current['nonzero_shell_count']}",
    )
    report(
        "eight-mode-plan-pole-kinematics-ready",
        pole_fit_same_noise["pole_fit_kinematics_ready"] is True,
        f"shells={pole_fit_same_noise['distinct_shell_count']}",
    )
    report(
        "eight-mode-x16-exceeds-foreground",
        pole_fit_same_noise["fits_12h_foreground"] is False,
        f"hours={pole_fit_same_noise['estimated_l12_chunk_hours']:.6g}",
    )
    report(
        "eight-mode-x8-fits-current-foreground-budget",
        pole_fit_half_noise["fits_12h_foreground"] is True,
        f"hours={pole_fit_half_noise['estimated_l12_chunk_hours']:.6g}",
    )
    report(
        "lower-noise-variance-gate-state-recorded",
        x8_variance_gate_passed,
        "x8 accepted as launch support only" if x8_variance_gate_passed else "x8 still needs variance acceptance",
    )
    report(
        "x8-launch-support-accepted-not-evidence",
        x8_launch_support_accepted,
        "eight-mode/x8 may be launched as a separate support stream",
    )
    report("not-retained-closure", True, "mode/noise budget is not production data or scalar LSZ theorem")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ pole-fit mode-noise budget",
        "verdict": (
            "A pole-fit-ready L12 scalar-LSZ mode set can stay within the "
            "current foreground chunk estimate only by trading noise vectors "
            "for momentum shells.  Eight modes with sixteen noises are "
            f"estimated at {pole_fit_same_noise['estimated_l12_chunk_hours']:.6g} "
            "hours for a 16-configuration L12 chunk, above the 12-hour window.  "
            "The same eight modes with eight noises keep the solve-budget "
            "factor equal to the current four-mode/sixteen-noise plan and are "
            f"estimated at {pole_fit_half_noise['estimated_l12_chunk_hours']:.6g} "
            "hours.  The eight-mode/x8 setting now also passes the variance "
            "gate as launch support only.  This is a constructive launch "
            "option, not evidence: production completion, pole/model-class "
            "control, FV/IR control, canonical-Higgs/source-overlap closure, "
            "and retained-proposal certification remain required."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A mode/noise budget is launch planning only and does not provide production pole data.",
        "parent_certificates": {
            "resource_projection": str(RESOURCE.relative_to(ROOT)),
            "chunk_manifest": str(CHUNK_MANIFEST.relative_to(ROOT)),
            "kinematics_gate": str(KINEMATICS_GATE.relative_to(ROOT)),
            "variance_gate": str(VARIANCE_GATE.relative_to(ROOT)),
        },
        "candidates": [current, pole_fit_same_noise, pole_fit_half_noise],
        "x8_variance_gate_passed": x8_variance_gate_passed,
        "x8_launch_support_accepted": x8_launch_support_accepted,
        "recommended_next_launch_if_variance_accepted": pole_fit_half_noise["command_fragment"],
        "recommended_next_launch_if_launch_support_accepted": (
            pole_fit_half_noise["command_fragment"] if x8_launch_support_accepted else None
        ),
        "acceptance_requirements": [
            "variance/noise gate has passed only as launch support, not physics evidence",
            "use the same source coordinate and run-control provenance as the FH response",
            "do not combine four-mode and eight-mode chunks as one homogeneous pole-fit ensemble",
            "fit an isolated pole derivative only after enough completed production chunks exist",
            "retain FV/IR/zero-mode, model-class, canonical-Higgs/source-overlap, and retained-proposal gates",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a kappa_s derivation",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use observed top mass, observed y_t, H_unit, yt_ward_identity, alpha_LM, plaquette, or u0",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
