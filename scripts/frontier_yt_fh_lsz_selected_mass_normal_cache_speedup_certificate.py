#!/usr/bin/env python3
"""
PR #230 FH/LSZ selected-mass normal-cache speedup certificate.

This runner certifies performance/infrastructure support only.  It models the
solve/build work removed by the target-timeseries replacement harness
optimization and checks that the production harness carries explicit metadata
for selected-mass-only scalar FH/LSZ and per-configuration normal-equation
caching.  It is not physics evidence and does not authorize retained wording.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_selected_mass_normal_cache_speedup_certificate_2026-05-03.json"

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


def replacement_model(
    mass_points: int = 3,
    selected_mass_points: int = 1,
    colors: int = 3,
    scalar_source_shifts: int = 3,
    scalar_two_point_modes: int = 4,
    scalar_two_point_noises: int = 16,
) -> dict[str, Any]:
    nonzero_source_shifts = max(scalar_source_shifts - 1, 0)
    base_scan_solves = mass_points * colors
    source_shift_solves_old = mass_points * nonzero_source_shifts * colors
    source_shift_solves_new = selected_mass_points * nonzero_source_shifts * colors
    lsz_solves_per_mass = scalar_two_point_modes * scalar_two_point_noises * 2
    lsz_solves_old = mass_points * lsz_solves_per_mass
    lsz_solves_new = selected_mass_points * lsz_solves_per_mass
    old_solves = base_scan_solves + source_shift_solves_old + lsz_solves_old
    new_solves = base_scan_solves + source_shift_solves_new + lsz_solves_new
    old_normal_builds = old_solves
    new_normal_builds = mass_points + selected_mass_points * nonzero_source_shifts
    return {
        "configuration": {
            "mass_points": mass_points,
            "selected_mass_points": selected_mass_points,
            "colors": colors,
            "scalar_source_shifts": scalar_source_shifts,
            "scalar_two_point_modes": scalar_two_point_modes,
            "scalar_two_point_noises": scalar_two_point_noises,
        },
        "old_model": {
            "base_scan_solves": base_scan_solves,
            "source_shift_solves": source_shift_solves_old,
            "scalar_two_point_solves": lsz_solves_old,
            "total_rhs_solves_per_configuration": old_solves,
            "normal_equation_builds_per_configuration": old_normal_builds,
        },
        "optimized_model": {
            "base_scan_solves": base_scan_solves,
            "source_shift_solves": source_shift_solves_new,
            "scalar_two_point_solves": lsz_solves_new,
            "total_rhs_solves_per_configuration": new_solves,
            "normal_equation_builds_per_configuration": new_normal_builds,
        },
        "speedup_estimate": {
            "rhs_solve_reduction_factor": old_solves / new_solves,
            "rhs_solves_removed_per_configuration": old_solves - new_solves,
            "normal_build_reduction_factor": old_normal_builds / new_normal_builds,
            "normal_builds_removed_per_configuration": old_normal_builds - new_normal_builds,
        },
    }


def main() -> int:
    print("PR #230 FH/LSZ selected-mass normal-cache speedup certificate")
    print("=" * 78)

    source = HARNESS.read_text(encoding="utf-8")
    model = replacement_model()
    speed = model["speedup_estimate"]
    markers = {
        "normal-equation-system": "class NormalEquationSystem" in source,
        "cached-solver": "solve_vector_normal_eq_cached" in source,
        "per-config-normal-cache": "normal_cache: dict[str, NormalEquationSystem]" in source,
        "selected-mass-policy": "selected_mass_only_for_scalar_fh_lsz" in source,
        "selected-mass-gate": "abs(float(mass) - selected_mass) <= 1.0e-15" in source,
        "metadata-selected-mass-only": "fh_lsz_selected_mass_only" in source,
        "metadata-normal-cache": "normal_equation_cache_enabled" in source,
        "claim-firewall": "used_as_physical_yukawa_readout" in source
        and "physical_higgs_normalization" in source,
    }

    report("harness-present", HARNESS.exists(), str(HARNESS.relative_to(ROOT)))
    for tag, ok in markers.items():
        report(tag, ok, f"marker={ok}")
    report(
        "rhs-solve-model-speedup",
        float(speed["rhs_solve_reduction_factor"]) > 2.0,
        f"old={model['old_model']['total_rhs_solves_per_configuration']} new={model['optimized_model']['total_rhs_solves_per_configuration']} factor={speed['rhs_solve_reduction_factor']:.3f}",
    )
    report(
        "normal-build-model-speedup",
        float(speed["normal_build_reduction_factor"]) > 10.0,
        f"old={model['old_model']['normal_equation_builds_per_configuration']} new={model['optimized_model']['normal_equation_builds_per_configuration']} factor={speed['normal_build_reduction_factor']:.3f}",
    )
    report("does-not-authorize-retained-proposal", True, "performance support only")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ selected-mass normal-cache speedup",
        "verdict": (
            "The harness now preserves the three-mass top-correlator scan while "
            "restricting expensive scalar source-response and scalar two-point "
            "LSZ solves to the selected middle mass.  It also caches D, "
            "D^dagger, and D^dagger D per saved gauge configuration and "
            "mass/source-shift value.  This is infrastructure support only and "
            "does not make source-only FH/LSZ a physical y_t readout."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Speedup and metadata hardening do not derive kappa_s or canonical-Higgs/source-overlap.",
        "model": model,
        "source_markers": markers,
        "strict_non_claims": [
            "does not derive kappa_s",
            "does not set kappa_s = 1",
            "does not use H_unit or yt_ward_identity",
            "does not use alpha_LM, plaquette/u0, observed m_t, or observed y_t as proof authority",
            "does not claim retained or proposed_retained y_t closure",
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
