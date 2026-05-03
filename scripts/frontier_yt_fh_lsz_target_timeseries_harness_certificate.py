#!/usr/bin/env python3
"""
PR #230 FH/LSZ target time-series harness certificate.

This runner verifies that the direct lattice production harness now serializes
the per-configuration target observables needed by the autocorrelation/ESS
gate.  It certifies instrumentation only; reduced smoke output is not
production evidence and does not determine kappa_s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "outputs" / "yt_direct_lattice_correlator_target_timeseries_smoke_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json"

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


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and ensembles and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def source_timeseries_summary(ensemble: dict[str, Any]) -> dict[str, Any]:
    source = ensemble.get("scalar_source_response_analysis", {})
    if not isinstance(source, dict):
        source = {}
    slopes = source.get("per_configuration_slopes", [])
    energies = source.get("per_configuration_effective_energies", [])
    finite_slopes = [
        float(row.get("slope_effective_energy_tau1"))
        for row in slopes
        if isinstance(row, dict) and finite(row.get("slope_effective_energy_tau1"))
    ]
    radii = sorted(
        {
            float(row.get("source_radius"))
            for row in slopes
            if isinstance(row, dict) and finite(row.get("source_radius"))
        }
    )
    return {
        "present": isinstance(slopes, list)
        and len(slopes) > 0
        and isinstance(energies, list)
        and len(energies) > 0,
        "slope_rows": len(slopes) if isinstance(slopes, list) else 0,
        "effective_energy_rows": len(energies) if isinstance(energies, list) else 0,
        "finite_slope_rows": len(finite_slopes),
        "source_radii": radii,
        "target_timeseries_rule": source.get("target_timeseries_rule"),
        "strict_limit": source.get("strict_limit"),
    }


def scalar_two_point_timeseries_summary(ensemble: dict[str, Any]) -> dict[str, Any]:
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    if not isinstance(lsz, dict):
        lsz = {}
    rows = lsz.get("mode_rows", {})
    mode_summaries = {}
    complete = bool(rows)
    total_rows = 0
    if isinstance(rows, dict):
        for key, row in rows.items():
            series = row.get("C_ss_timeseries", []) if isinstance(row, dict) else []
            finite_c = [
                item
                for item in series
                if isinstance(item, dict) and finite(item.get("C_ss_real")) and finite(item.get("Gamma_ss_real"))
            ]
            mode_summaries[key] = {
                "rows": len(series) if isinstance(series, list) else 0,
                "finite_real_gamma_rows": len(finite_c),
            }
            complete = complete and isinstance(series, list) and len(series) > 0
            total_rows += len(series) if isinstance(series, list) else 0
    else:
        complete = False
    return {
        "present": complete,
        "mode_count": len(mode_summaries),
        "total_timeseries_rows": total_rows,
        "mode_summaries": mode_summaries,
        "strict_limit": lsz.get("strict_limit"),
    }


def main() -> int:
    print("PR #230 FH/LSZ target time-series harness certificate")
    print("=" * 72)

    data = load_json(SMOKE)
    metadata = data.get("metadata", {})
    ensemble = first_ensemble(data)
    scalar_source_meta = metadata.get("scalar_source_response", {})
    scalar_lsz_meta = metadata.get("scalar_two_point_lsz", {})
    run_control = metadata.get("run_control", {})
    policy = metadata.get("fh_lsz_measurement_policy", {})
    rng_seed_control = ensemble.get("rng_seed_control", {})
    source_summary = source_timeseries_summary(ensemble)
    lsz_summary = scalar_two_point_timeseries_summary(ensemble)

    phase = metadata.get("phase")
    source_enabled = scalar_source_meta.get("enabled") is True
    lsz_enabled = scalar_lsz_meta.get("enabled") is True
    no_physical_readout = (
        scalar_source_meta.get("used_as_physical_yukawa_readout") is False
        and scalar_lsz_meta.get("used_as_physical_yukawa_readout") is False
    )
    no_higgs_normalization = (
        scalar_source_meta.get("physical_higgs_normalization") == "not_derived"
        and scalar_lsz_meta.get("physical_higgs_normalization") == "not_derived"
    )
    seed_control_ok = rng_seed_control.get("seed_control_version") == "numba_gauge_seed_v1"
    selected_mass_policy_ok = (
        policy.get("policy") == "selected_mass_only_for_scalar_fh_lsz"
        and scalar_source_meta.get("selected_mass_only") is True
        and scalar_lsz_meta.get("selected_mass_only") is True
        and run_control.get("fh_lsz_selected_mass_only") is True
        and run_control.get("normal_equation_cache_enabled") is True
    )

    report("smoke-output-loaded", bool(data), str(SMOKE.relative_to(ROOT)))
    report("phase-is-reduced-scope", phase == "reduced_scope", f"phase={phase}")
    report("scalar-source-response-enabled", source_enabled, str(scalar_source_meta))
    report("scalar-two-point-lsz-enabled", lsz_enabled, str(scalar_lsz_meta))
    report("source-target-timeseries-present", source_summary["present"], str(source_summary))
    report("scalar-lsz-target-timeseries-present", lsz_summary["present"], str(lsz_summary))
    report("numba-seed-control-present", seed_control_ok, str(rng_seed_control))
    report("selected-mass-normal-cache-metadata-present", selected_mass_policy_ok, str(policy))
    report("no-physical-yukawa-readout", no_physical_readout, "metadata uses instrumentation only")
    report("physical-higgs-normalization-not-derived", no_higgs_normalization, "kappa_s remains open")
    report("reduced-smoke-is-not-production-evidence", phase == "reduced_scope", "smoke run is infrastructure only")
    report("does-not-authorize-retained-proposal", True, "target time series are not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ target time-series harness extension",
        "verdict": (
            "The direct lattice harness now serializes per-configuration "
            "same-source target time series for the source-response effective "
            "energy slopes and scalar two-point C_ss/Gamma_ss modes.  This "
            "removes the instrumentation blocker for future autocorrelation "
            "and ESS checks, but the reduced smoke output is not production "
            "evidence and it does not derive kappa_s or the canonical-Higgs "
            "source identity."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Instrumentation support is not a retained or proposed-retained closure certificate.",
        "target_timeseries_harness_supported": bool(source_summary["present"] and lsz_summary["present"]),
        "smoke_certificate": str(SMOKE.relative_to(ROOT)),
        "source_timeseries_summary": source_summary,
        "scalar_two_point_timeseries_summary": lsz_summary,
        "rng_seed_control": rng_seed_control,
        "fh_lsz_measurement_policy": policy,
        "required_next_gate": (
            "Rerun production chunks with the extended harness, then apply "
            "target-observable autocorrelation/ESS, finite-source-linearity, "
            "scalar-pole/FV/IR/model-class, and canonical-Higgs identity gates."
        ),
        "strict_non_claims": [
            "does not use reduced smoke output as production evidence",
            "does not treat target time series as physical dE/dh",
            "does not derive kappa_s",
            "does not set kappa_s = 1",
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
