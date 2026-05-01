#!/usr/bin/env python3
"""
PR #230 production resource projection.

This runner converts the existing 12^3 x 24 numba mass-bracket run into an
honest production-scale resource estimate.  It is not production evidence; it
exists to keep the remaining direct-measurement route concrete.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "outputs" / "yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_production_resource_projection_2026-05-01.json"

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


def sites(spatial_l: int, time_t: int) -> int:
    return spatial_l ** 3 * time_t


def main() -> int:
    print("PR #230 production resource projection")
    print("=" * 72)

    data = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    ensemble = data["ensembles"][0]
    benchmark_volume = (ensemble["spatial_L"], ensemble["time_L"])
    benchmark_sites = sites(*benchmark_volume)
    runtime_seconds = float(ensemble["runtime_seconds"])
    thermalization = int(ensemble["thermalization_sweeps"])
    measurements = int(ensemble["measurement_sweeps"])
    separation = int(ensemble["measurement_separation_sweeps"])
    mass_count = len(ensemble.get("mass_parameter_scan", []))
    effective_sweeps = thermalization + measurements * max(separation, 1)
    seconds_per_effective_sweep = runtime_seconds / effective_sweeps

    production_thermalization = 1000
    production_measurements = 1000
    production_separation = 20
    production_mass_count = 3
    production_sweeps = production_thermalization + production_measurements * production_separation
    mass_count_scale = production_mass_count / max(mass_count, 1)
    volumes = [(12, 24), (16, 32), (24, 48)]
    rows = []
    for spatial_l, time_t in volumes:
        site_scale = sites(spatial_l, time_t) / benchmark_sites
        conservative_seconds = seconds_per_effective_sweep * production_sweeps * site_scale
        mass_scaled_seconds = conservative_seconds * mass_count_scale
        rows.append(
            {
                "volume": f"{spatial_l}^3x{time_t}",
                "sites": sites(spatial_l, time_t),
                "site_scale_vs_benchmark": site_scale,
                "production_sweeps": production_sweeps,
                "conservative_seconds": conservative_seconds,
                "conservative_hours": conservative_seconds / 3600.0,
                "mass_scaled_seconds": mass_scaled_seconds,
                "mass_scaled_hours": mass_scaled_seconds / 3600.0,
            }
        )

    total_conservative_hours = sum(row["conservative_hours"] for row in rows)
    total_mass_scaled_hours = sum(row["mass_scaled_hours"] for row in rows)

    report("benchmark-certificate-present", BENCHMARK.exists(), str(BENCHMARK.relative_to(ROOT)))
    report("benchmark-is-reduced-scope", data.get("metadata", {}).get("phase") == "pilot", data.get("metadata", {}).get("phase", ""))
    report("benchmark-runtime-recorded", runtime_seconds > 100.0, f"runtime_seconds={runtime_seconds:.3f}")
    report("effective-sweep-rate-computed", seconds_per_effective_sweep > 0.0, f"seconds_per_effective_sweep={seconds_per_effective_sweep:.6g}")
    report("production-protocol-larger-than-benchmark", production_sweeps > effective_sweeps, f"{production_sweeps}>{effective_sweeps}")
    report("full-production-exceeds-12h-foreground", total_mass_scaled_hours > 12.0, f"mass_scaled_total_hours={total_mass_scaled_hours:.2f}")
    report("not-production-evidence", True, "projection only; strict runner still requires actual production certificate")

    result = {
        "actual_current_surface_status": "bounded support / production resource projection",
        "verdict": (
            "The existing 12^3 x 24 numba mass-bracket run provides a concrete "
            "resource baseline but not production evidence.  Linear site-count "
            "projection of the required 1000 thermalization plus 1000x20 "
            "measurement protocol gives multi-day single-worker wall-clock for "
            "the three-volume campaign.  The direct route remains viable as a "
            "planned production job, not a 12-hour foreground closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Resource projection is not measurement evidence and does not supply matching.",
        "benchmark": {
            "path": str(BENCHMARK.relative_to(ROOT)),
            "volume": f"{benchmark_volume[0]}^3x{benchmark_volume[1]}",
            "runtime_seconds": runtime_seconds,
            "thermalization_sweeps": thermalization,
            "measurement_sweeps": measurements,
            "measurement_separation_sweeps": separation,
            "mass_count": mass_count,
            "effective_sweeps": effective_sweeps,
            "seconds_per_effective_sweep": seconds_per_effective_sweep,
        },
        "production_protocol": {
            "thermalization_sweeps": production_thermalization,
            "measurement_configurations": production_measurements,
            "measurement_separation_sweeps": production_separation,
            "fermion_mass_values": production_mass_count,
            "effective_sweeps": production_sweeps,
        },
        "rows": rows,
        "total_conservative_hours": total_conservative_hours,
        "total_mass_scaled_hours": total_mass_scaled_hours,
        "strict_non_claims": [
            "not production data",
            "not a y_t derivation",
            "does not make strict runner pass",
            "does not supply lattice-to-SM matching",
            "does not use H_unit matrix-element authority",
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
