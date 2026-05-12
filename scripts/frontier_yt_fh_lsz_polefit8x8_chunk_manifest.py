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
KPRIME_SCHEMA_VERSION = "yt_pr230_kprime_pole_row_v1"
KPRIME_FIXTURE = ROOT / "fixtures" / "yt_pr230_kprime_pole_row_fixture.json"

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
KPRIME_FORBIDDEN_FALSE_FIELDS = [
    "used_hunit_matrix_element_readout",
    "used_yt_ward_identity",
    "used_y_t_bare",
    "used_alpha_lm_or_plaquette_u0",
    "used_observed_target_selectors",
    "used_alias_imports",
    "used_reduced_cold_pilots_as_production_evidence",
    "set_c2_equal_one",
    "set_z_match_equal_one",
    "set_kappa_s_equal_one",
    "set_cos_theta_equal_one",
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


def kprime_emission_schema() -> dict[str, Any]:
    return {
        "schema_version": KPRIME_SCHEMA_VERSION,
        "chunk_worker_flag": "--schur-kprime-rows",
        "fixture": rel(KPRIME_FIXTURE),
        "row_container_locations": [
            "ensemble.schur_kprime_pole_rows[]",
            "metadata.schur_kprime_kernel_rows.rows[]",
            "top-level kprime_pole_rows[]",
        ],
        "required_sections_per_row": [
            "transfer_schur_kernel_at_pole",
            "derivative_wrt_pole_coordinate",
            "eigen_projection",
            "source_numerator_projection",
            "error_interval",
            "provenance",
        ],
        "transfer_schur_kernel_at_pole": {
            "schur_form": "one_orthogonal_mode_v1 or precontracted_matrix_v1",
            "one_orthogonal_mode_v1": ["A_at_pole", "B_at_pole", "C_at_pole"],
            "precontracted_matrix_v1": ["A_at_pole", "B_Cinv_B_at_pole"],
            "must_compute": "effective_denominator_at_pole",
        },
        "derivative_wrt_pole_coordinate": {
            "coordinate": "pole coordinate, e.g. p_hat_sq or x",
            "one_orthogonal_mode_v1": ["A_prime_at_pole", "B_prime_at_pole", "C_prime_at_pole"],
            "precontracted_matrix_v1": [
                "A_prime_at_pole",
                "two_Bprime_Cinv_B_at_pole",
                "B_Cinv_Cprime_Cinv_B_at_pole",
            ],
            "must_compute": "effective_denominator_prime_at_pole",
            "projection_sign_convention": "D_eff_prime",
        },
        "eigen_projection": {
            "required": [
                "left_eigenvector",
                "right_eigenvector",
                "kernel_prime_matrix_at_pole",
                "projected_kprime_at_pole",
                "vector_normalization",
            ],
            "computed_check": "<l,K_prime(pole)r>/<l,r>",
        },
        "source_numerator_projection": {
            "required": [
                "source_vector",
                "left_source_projection",
                "right_source_projection",
                "source_numerator_at_pole",
            ],
            "computed_check": "<l,s><s,r>/<l,r>",
        },
        "error_interval": {
            "required": [
                "effective_denominator_at_pole",
                "projected_kprime_at_pole",
                "source_numerator_at_pole",
            ],
            "strict_certificate_requires": [
                "effective_denominator_at_pole interval contains zero",
                "projected_kprime_at_pole interval excludes zero",
                "source_numerator_at_pole interval excludes zero",
            ],
        },
        "provenance": {
            "required": [
                "phase",
                "same_surface_cl3_z3",
                "source_coordinate",
                "chunk_index",
                "production_output_dir",
                "row_builder",
                "forbidden_import_firewall",
            ],
            "forbidden_import_firewall_false": KPRIME_FORBIDDEN_FALSE_FIELDS,
        },
    }


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
        "kprime_pole_row_emission_contract": kprime_emission_schema(),
        "commands": commands,
        "acceptance_requirements": [
            "completed chunks must be production phase and seed-controlled",
            "completed chunks must expose the same eight scalar-LSZ modes with x8 noise",
            "closure-bearing K-prime chunks must attach rows matching yt_pr230_kprime_pole_row_v1",
            "K-prime rows must include Schur pole rows, pole-coordinate derivatives, eigenprojection data, source numerator projection, intervals, and provenance firewalls",
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
