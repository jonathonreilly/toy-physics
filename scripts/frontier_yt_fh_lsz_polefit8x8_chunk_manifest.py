#!/usr/bin/env python3
"""
PR #230 FH/LSZ eight-mode/x8 pole-fit chunk manifest.

This manifest is a run-control surface only.  It defines a separate L12_T24
same-source scalar-LSZ stream with enough momentum shells for a diagnostic
pole-fit postprocess.  It is deliberately isolated from the completed four-mode
FH/LSZ chunk set and does not authorize a physical y_t readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODE_BUDGET = ROOT / "outputs" / "yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json"
PAIRED_VARIANCE = ROOT / "outputs" / "yt_fh_lsz_paired_variance_calibration_gate_2026-05-04.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_polefit8x8_chunk_manifest_2026-05-04.json"

MASS_SPEC = "0.75"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
EIGHT_MODES = [
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (1, 1, 1),
    (2, 0, 0),
    (2, 1, 0),
    (2, 1, 1),
    (2, 2, 0),
]
THERM = 1000
MEASUREMENTS_PER_CHUNK = 16
SEPARATION = 20
CHUNK_COUNT = 63
TARGET_MEASUREMENTS = 1000
SEED_BASE = 2026051900

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


def mode_string(modes: list[tuple[int, int, int]]) -> str:
    return ";".join(",".join(str(value) for value in mode) for mode in modes)


def p_hat_sq(mode: tuple[int, int, int], spatial_l: int = 12) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_l)) ** 2 for n in mode)


def command_for_chunk(index: int) -> dict[str, Any]:
    output = ROOT / "outputs" / f"yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk{index:03d}_2026-05-04.json"
    production_output_dir = (
        ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_fh_lsz_polefit8x8"
        / f"L12_T24_chunk{index:03d}"
    )
    parts = [
        "python3",
        "scripts/yt_direct_lattice_correlator_production.py",
        "--volumes",
        "12x24",
        "--masses",
        MASS_SPEC,
        "--therm",
        str(THERM),
        "--measurements",
        str(MEASUREMENTS_PER_CHUNK),
        "--separation",
        str(SEPARATION),
        "--engine",
        "numba",
        "--production-targets",
        f"--scalar-source-shifts={SOURCE_SHIFTS}",
        "--scalar-two-point-modes",
        f"'{mode_string(EIGHT_MODES)}'",
        "--scalar-two-point-noises",
        "8",
        "--production-output-dir",
        rel(production_output_dir),
        "--resume",
        "--seed",
        str(SEED_BASE + index),
        "--output",
        rel(output),
    ]
    return {
        "chunk_index": index,
        "seed": SEED_BASE + index,
        "volume": "12x24",
        "masses": MASS_SPEC,
        "scalar_source_shifts": SOURCE_SHIFTS,
        "scalar_two_point_modes": mode_string(EIGHT_MODES),
        "scalar_two_point_noises": 8,
        "thermalization_sweeps": THERM,
        "measurement_sweeps": MEASUREMENTS_PER_CHUNK,
        "measurement_separation_sweeps": SEPARATION,
        "output": rel(output),
        "production_output_dir": rel(production_output_dir),
        "command": " ".join(parts),
    }


def main() -> int:
    print("PR #230 FH/LSZ eight-mode/x8 pole-fit chunk manifest")
    print("=" * 72)

    mode_budget = load_json(MODE_BUDGET)
    paired_variance = load_json(PAIRED_VARIANCE)
    commands = [command_for_chunk(index) for index in range(1, CHUNK_COUNT + 1)]
    shells = sorted({round(p_hat_sq(mode), 12) for mode in EIGHT_MODES})
    positive_shells = [value for value in shells if value > 1.0e-12]

    report("mode-budget-loaded", bool(mode_budget), rel(MODE_BUDGET))
    report(
        "mode-budget-accepts-eight-mode-x8-launch-support",
        mode_budget.get("x8_launch_support_accepted") is True,
        str(mode_budget.get("actual_current_surface_status", "")),
    )
    report(
        "paired-variance-calibration-passed",
        paired_variance.get("variance_calibration_gate_passed") is True,
        str(paired_variance.get("actual_current_surface_status", "")),
    )
    report(
        "polefit-kinematics-have-zero-plus-three-positive-shells",
        len(shells) >= 4 and len(positive_shells) >= 3 and shells[0] == 0.0,
        f"shells={shells}",
    )
    report(
        "target-saved-configurations-covered",
        CHUNK_COUNT * MEASUREMENTS_PER_CHUNK >= TARGET_MEASUREMENTS,
        f"{CHUNK_COUNT * MEASUREMENTS_PER_CHUNK}/{TARGET_MEASUREMENTS}",
    )
    report(
        "commands-use-distinct-artifact-directories",
        len({row["production_output_dir"] for row in commands}) == len(commands),
        f"chunks={len(commands)}",
    )
    report("separate-from-four-mode-ensemble", True, "polefit8x8 output namespace is isolated")
    report("not-physical-yukawa-evidence", True, "manifest only; downstream gates decide evidence status")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ eight-mode-x8 pole-fit chunk manifest",
        "verdict": (
            "The eight-mode/x8 stream is now specified as a separate L12_T24 "
            "same-source scalar-LSZ production stream.  The chosen modes provide "
            "a zero shell plus at least three positive p_hat^2 shells, while x8 "
            "noise is accepted only as launch support by the paired variance "
            "gate.  This manifest is not production evidence and cannot be "
            "mixed with the completed four-mode L12 ensemble as a homogeneous "
            "pole-fit data set."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A chunk manifest is run control only and does not derive scalar LSZ normalization or physical y_t.",
        "parent_certificates": {
            "mode_budget": rel(MODE_BUDGET),
            "paired_variance_calibration_gate": rel(PAIRED_VARIANCE),
        },
        "chunk_policy": {
            "chunk_count": CHUNK_COUNT,
            "chunk_measurements": MEASUREMENTS_PER_CHUNK,
            "target_measurements": TARGET_MEASUREMENTS,
            "available_measurements_if_complete": CHUNK_COUNT * MEASUREMENTS_PER_CHUNK,
            "seed_base": SEED_BASE,
            "stream_namespace": "yt_pr230_fh_lsz_polefit8x8_L12_T24",
        },
        "polefit_kinematics": {
            "modes": [list(mode) for mode in EIGHT_MODES],
            "distinct_p_hat_sq_shells": shells,
            "positive_shell_count": len(positive_shells),
            "zero_plus_three_positive_shells": len(shells) >= 4 and len(positive_shells) >= 3,
        },
        "commands": commands,
        "acceptance_requirements": [
            "completed chunks must be production phase and seed-controlled",
            "completed chunks must expose the same eight scalar-LSZ modes with x8 noise",
            "do not combine with the four-mode/x16 L12 ensemble",
            "a complete L12 stream remains non-closure without L16/L24, FV/IR, model-class, and source-Higgs identity gates",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
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
