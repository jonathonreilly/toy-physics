#!/usr/bin/env python3
"""
PR #230 FH/LSZ paired x8/x16 variance calibration manifest.

The eight-mode x8 launch class needs same-source variance evidence before it
can be used as production-facing pole-fit data.  This runner does not launch
production.  It emits exact paired commands for an L12 calibration chunk whose
only physics-relevant difference is the scalar-LSZ noise count.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODE_BUDGET = ROOT / "outputs" / "yt_fh_lsz_pole_fit_mode_budget_2026-05-01.json"
VARIANCE_GATE = ROOT / "outputs" / "yt_fh_lsz_eight_mode_noise_variance_gate_2026-05-01.json"
DIAGNOSTICS = ROOT / "outputs" / "yt_fh_lsz_noise_subsample_diagnostics_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_variance_calibration_manifest_2026-05-01.json"

MASS_SPEC = "0.75"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
EIGHT_MODES = "0,0,0;1,0,0;1,1,0;1,1,1;2,0,0;2,1,0;2,1,1;2,2,0"
THERM = 1000
MEASUREMENTS = 16
SEPARATION = 20
SEED = 2026051801

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


def shell_join(parts: list[str]) -> str:
    return " ".join(parts)


def calibration_command(noises: int) -> dict[str, Any]:
    label = f"x{noises}"
    output = f"outputs/yt_pr230_fh_lsz_variance_calibration_L12_T24_{label}_2026-05-01.json"
    production_output_dir = (
        "outputs/yt_direct_lattice_correlator_production_fh_lsz_variance_calibration/"
        f"L12_T24_{label}"
    )
    command = shell_join(
        [
            "python3",
            "scripts/yt_direct_lattice_correlator_production.py",
            "--volumes",
            "12x24",
            "--masses",
            MASS_SPEC,
            "--therm",
            str(THERM),
            "--measurements",
            str(MEASUREMENTS),
            "--separation",
            str(SEPARATION),
            "--engine",
            "numba",
            "--production-targets",
            f"--scalar-source-shifts={SOURCE_SHIFTS}",
            "--scalar-two-point-modes",
            f"'{EIGHT_MODES}'",
            "--scalar-two-point-noises",
            str(noises),
            "--production-output-dir",
            production_output_dir,
            "--resume",
            "--seed",
            str(SEED),
            "--output",
            output,
        ]
    )
    return {
        "label": label,
        "scalar_two_point_noises": noises,
        "volume": "12x24",
        "masses": MASS_SPEC,
        "scalar_source_shifts": SOURCE_SHIFTS,
        "scalar_two_point_modes": EIGHT_MODES,
        "thermalization_sweeps": THERM,
        "measurement_sweeps": MEASUREMENTS,
        "measurement_separation_sweeps": SEPARATION,
        "seed": SEED,
        "output": output,
        "production_output_dir": production_output_dir,
        "command": command,
    }


def main() -> int:
    print("PR #230 FH/LSZ paired x8/x16 variance calibration manifest")
    print("=" * 72)

    mode_budget = load_json(MODE_BUDGET)
    variance_gate = load_json(VARIANCE_GATE)
    diagnostics = load_json(DIAGNOSTICS)
    x8 = calibration_command(8)
    x16 = calibration_command(16)
    commands = [x8, x16]
    differing_keys = [
        key
        for key in x8
        if key in x16 and x8[key] != x16[key] and key not in {"label", "scalar_two_point_noises", "output", "production_output_dir", "command"}
    ]

    report("mode-budget-loaded", bool(mode_budget), str(MODE_BUDGET.relative_to(ROOT)))
    report(
        "variance-gate-still-open",
        variance_gate.get("variance_gate_passed") is False,
        variance_gate.get("actual_current_surface_status", ""),
    )
    report(
        "diagnostics-available",
        diagnostics.get("proposal_allowed") is False
        and "noise-subsample diagnostics" in diagnostics.get("actual_current_surface_status", ""),
        diagnostics.get("actual_current_surface_status", ""),
    )
    report(
        "paired-commands-use-eight-modes",
        all(row["scalar_two_point_modes"] == EIGHT_MODES for row in commands),
        "both commands use the pole-fit eight-mode set",
    )
    report(
        "paired-commands-use-x8-and-x16-noises",
        [row["scalar_two_point_noises"] for row in commands] == [8, 16],
        f"noises={[row['scalar_two_point_noises'] for row in commands]}",
    )
    report(
        "gauge-stream-controls-match",
        not differing_keys,
        f"differing_controls={differing_keys}",
    )
    report(
        "artifact-directories-distinct",
        x8["production_output_dir"] != x16["production_output_dir"],
        f"dirs={[row['production_output_dir'] for row in commands]}",
    )
    report(
        "commands-production-targeted",
        all("--production-targets" in row["command"] for row in commands),
        "both commands request production-targeted metadata",
    )
    report("not-production-evidence", True, "manifest only; no calibration outputs are present")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ variance calibration manifest",
        "verdict": (
            "A paired L12 x8/x16 variance calibration can now be launched with "
            "matched volume, mass, source shifts, eight scalar-LSZ modes, seed, "
            "thermalization, and measurement schedule, while using distinct "
            "artifact directories and outputs.  This is a manifest only.  It "
            "does not supply production variance evidence, does not pass the "
            "eight-mode variance gate, and does not derive scalar LSZ "
            "normalization."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A calibration launch manifest is not completed same-source production data.",
        "parent_certificates": {
            "mode_budget": str(MODE_BUDGET.relative_to(ROOT)),
            "variance_gate": str(VARIANCE_GATE.relative_to(ROOT)),
            "noise_subsample_diagnostics": str(DIAGNOSTICS.relative_to(ROOT)),
        },
        "calibration_policy": {
            "purpose": "paired x8/x16 scalar-LSZ variance calibration",
            "matched_controls": [
                "volume",
                "masses",
                "source shifts",
                "scalar-LSZ modes",
                "seed",
                "thermalization sweeps",
                "measurement count",
                "measurement separation",
            ],
            "allowed_differences": [
                "scalar_two_point_noises",
                "output path",
                "production_output_dir",
            ],
            "same_gauge_stream_assumption": (
                "same seed and same gauge-update controls are required so the "
                "gauge stream is matched; completed certificates must still "
                "record run_control and pass the combiner/postprocess gates"
            ),
        },
        "commands": commands,
        "acceptance_requirements": [
            "both x8 and x16 calibration outputs must complete as production phase",
            "both must expose metadata.run_control matching this manifest",
            "both must expose noise_subsample_stability for each scalar-LSZ mode",
            "compare same-mode C_ss(q), Gamma_ss(q), and pole-derivative stability before accepting x8",
            "do not use either calibration as physical y_t evidence without the retained gates",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a kappa_s derivation",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
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
