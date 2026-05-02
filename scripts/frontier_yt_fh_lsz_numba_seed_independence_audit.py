#!/usr/bin/env python3
"""
PR #230 FH/LSZ numba seed-independence audit.

This runner checks whether completed FH/LSZ L12 chunks can be counted as
independent gauge evidence.  The answer for the current chunk001/chunk002
surface is negative: their metadata seeds differ, but the gauge-evolution
observables match exactly and the historical outputs do not carry the new
numba gauge-seed-control marker.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_numba_seed_independence_audit_2026-05-02.json"
CHUNKS = [
    ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunk001_2026-05-01.json",
    ROOT / "outputs" / "yt_pr230_fh_lsz_production_L12_T24_chunk002_2026-05-01.json",
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
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def selected_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def chunk_signature(path: Path) -> dict[str, Any]:
    data = load_json(path)
    metadata = data.get("metadata", {})
    run_control = metadata.get("run_control", {})
    ensemble = selected_ensemble(data)
    source = ensemble.get("scalar_source_response_analysis", {})
    mass_fit = ensemble.get("mass_fit", {})
    signature_values = {
        "plaquette_mean": ensemble.get("plaquette_mean"),
        "mass_fit_m_lat": mass_fit.get("m_lat") if isinstance(mass_fit, dict) else None,
        "source_slope_dE_ds_lat": source.get("slope_dE_ds_lat") if isinstance(source, dict) else None,
    }
    signature = {
        key: round(float(value), 15) if finite_number(value) else None
        for key, value in signature_values.items()
    }
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": bool(data),
        "phase": metadata.get("phase"),
        "metadata_seed": run_control.get("seed") if isinstance(run_control, dict) else None,
        "engine": run_control.get("engine") if isinstance(run_control, dict) else None,
        "seed_control_version": run_control.get("seed_control_version") if isinstance(run_control, dict) else None,
        "ensemble_seed_control": ensemble.get("rng_seed_control"),
        "signature": signature,
        "signature_complete": all(value is not None for value in signature.values()),
    }


def run_numba_seed_smoke() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("yt_direct_lattice_correlator_production", HARNESS)
    if spec is None or spec.loader is None:
        return {"available": False, "reason": "could not import harness"}
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if not getattr(module, "NUMBA_AVAILABLE", False):
        return {"available": False, "reason": "numba unavailable"}

    geom = module.Geometry(2, 4)

    def plaquette_after_one_sweep(seed: int) -> float:
        u = module.cold_link_array(geom)
        module.nb_seed(seed)
        module.nb_heatbath_sweep(u, module.BETA)
        return float(module.nb_plaquette(u))

    a = plaquette_after_one_sweep(111)
    b = plaquette_after_one_sweep(222)
    c = plaquette_after_one_sweep(111)
    return {
        "available": True,
        "plaquette_seed_111_a": a,
        "plaquette_seed_222": b,
        "plaquette_seed_111_b": c,
        "distinct_seeds_diverge": abs(a - b) > 1.0e-12,
        "same_seed_reproducible": abs(a - c) < 1.0e-12,
    }


def main() -> int:
    print("PR #230 FH/LSZ numba seed-independence audit")
    print("=" * 72)

    harness_source = HARNESS.read_text(encoding="utf-8")
    run_volume_body = harness_source.split("def run_volume_numba", 1)[1].split("\ndef combine_results", 1)[0]
    harness_has_seed_call = "nb_seed(volume_rng_seed)" in run_volume_body
    harness_has_seed_marker = "numba_gauge_seed_v1" in run_volume_body and "rng_seed_control" in run_volume_body

    rows = [chunk_signature(path) for path in CHUNKS]
    present = [row for row in rows if row["exists"]]
    metadata_seeds = {row.get("metadata_seed") for row in present}
    signatures = {
        tuple(row["signature"].get(key) for key in ("plaquette_mean", "mass_fit_m_lat", "source_slope_dE_ds_lat"))
        for row in present
        if row.get("signature_complete")
    }
    duplicate_gauge_signature = len(present) >= 2 and len(signatures) == 1
    missing_seed_control = [
        row["path"]
        for row in present
        if row.get("seed_control_version") != "numba_gauge_seed_v1"
        or not isinstance(row.get("ensemble_seed_control"), dict)
    ]
    old_chunks_non_independent = (
        len(present) == 2
        and len(metadata_seeds) == 2
        and duplicate_gauge_signature
        and len(missing_seed_control) == 2
    )
    smoke = run_numba_seed_smoke()

    report("two-historical-chunks-loaded", len(present) == 2, f"present={len(present)}")
    report("historical-metadata-seeds-distinct", len(metadata_seeds) == 2, f"seeds={sorted(metadata_seeds)}")
    report("historical-gauge-signatures-identical", duplicate_gauge_signature, f"signatures={sorted(signatures)}")
    report("historical-chunks-lack-seed-control-marker", len(missing_seed_control) == len(present), f"missing={missing_seed_control}")
    report("historical-chunks-not-independent-evidence", old_chunks_non_independent, "chunk001/chunk002 must be rerun or excluded")
    report("harness-now-seeds-numba-gauge-rng", harness_has_seed_call and harness_has_seed_marker, "run_volume_numba calls nb_seed(volume_rng_seed) and records marker")
    report(
        "numba-seed-smoke-diverges-and-reproduces",
        smoke.get("available") is True
        and smoke.get("distinct_seeds_diverge") is True
        and smoke.get("same_seed_reproducible") is True,
        str(smoke),
    )
    report("does-not-authorize-retained-proposal", True, "seed fix is an evidence-quality gate, not y_t closure")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ numba seed-independence audit",
        "verdict": (
            "The completed chunk001/chunk002 outputs cannot be counted as "
            "independent production evidence.  Their metadata seeds differ, "
            "but their gauge-evolution signature is identical and neither "
            "historical output carries the numba_gauge_seed_v1 seed-control "
            "marker.  The harness is now patched to seed numba gauge evolution "
            "inside run_volume_numba and to record per-volume seed-control "
            "metadata.  Current historical chunks must be rerun under the "
            "patched harness or excluded from L12 combination."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This audit demotes historical chunk evidence; it supplies no scalar pole residue, L16/L24 scaling, or physical y_t closure.",
        "historical_chunk_rows": rows,
        "historical_completed_chunks": len(present),
        "historical_independent_chunks_counted_for_evidence": 0,
        "historical_nonindependent_chunks": [row["path"] for row in present],
        "duplicate_gauge_signature_detected": duplicate_gauge_signature,
        "missing_seed_control_marker": missing_seed_control,
        "harness_seed_control": {
            "harness": str(HARNESS.relative_to(ROOT)),
            "seed_call_present": harness_has_seed_call,
            "seed_marker_present": harness_has_seed_marker,
            "seed_control_version": "numba_gauge_seed_v1",
            "numba_smoke": smoke,
        },
        "combiner_policy": (
            "The chunk combiner must reject historical chunks without the seed "
            "marker and any chunks sharing duplicate gauge-evolution signatures "
            "across distinct metadata seeds."
        ),
        "strict_non_claims": [
            "does not treat chunk001/chunk002 as independent production evidence",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0 as proof selectors",
        ],
        "exact_next_action": (
            "Let any old-code chunk finish only as a seed-invalid diagnostic; "
            "rerun replacement L12 chunks under numba_gauge_seed_v1 before "
            "counting them for combination."
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
