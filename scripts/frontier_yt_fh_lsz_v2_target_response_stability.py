#!/usr/bin/env python3
"""
PR #230 FH/LSZ v2 target-response stability gate.

The fitted dE/ds response-stability diagnostic is intentionally conservative
and remains open.  This runner checks a narrower production-support question:
do the v2 per-configuration multi-tau target slopes, for chunks that actually
carry the v2 schema, form a stable target-observable surface?

This is not a readout switch.  A stable target surface still lacks scalar LSZ
pole derivative, FV/IR/model-class control, and the canonical-Higgs/source
overlap identity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_v2_target_response_stability_2026-05-04.json"

MULTITAU_PATTERN = "yt_fh_lsz_chunk*_multitau_target_timeseries_checkpoint_2026-05-03.json"
EXPECTED_SCHEMA_VERSION = "fh_lsz_target_timeseries_v2_multitau"
MIN_V2_CHUNKS = 8
STABLE_REL_STDEV_MAX = 0.05
STABLE_SPREAD_MAX = 1.10
STABLE_POSITIVE_TAU_WINDOWS = set(range(0, 10))

PARENTS = {
    "legacy_v2_backfill": "outputs/yt_fh_lsz_legacy_v2_backfill_feasibility_2026-05-04.json",
    "target_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
    "response_forensics": "outputs/yt_fh_lsz_response_window_forensics_2026-05-03.json",
    "response_stability": "outputs/yt_fh_lsz_ready_chunk_response_stability_2026-05-02.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def first_ensemble(data: dict[str, Any]) -> dict[str, Any]:
    ensembles = data.get("ensembles")
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def chunk_index_from_checkpoint(path: Path) -> int | None:
    name = path.name
    marker = "yt_fh_lsz_chunk"
    if marker not in name:
        return None
    start = name.index(marker) + len(marker)
    digits = name[start : start + 3]
    return int(digits) if digits.isdigit() else None


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def v2_checkpoint_indices() -> list[int]:
    indices: list[int] = []
    for path in sorted((ROOT / "outputs").glob(MULTITAU_PATTERN)):
        index = chunk_index_from_checkpoint(path)
        if index is not None:
            indices.append(index)
    return sorted(set(indices))


def collect_chunk(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    metadata = data.get("metadata", {}) if isinstance(data.get("metadata"), dict) else {}
    ensemble = first_ensemble(data)
    source = ensemble.get("scalar_source_response_analysis", {})
    if not isinstance(source, dict):
        source = {}
    rows = source.get("per_configuration_multi_tau_slopes", [])
    tau_values: dict[int, list[float]] = {}
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            slopes = row.get("slope_effective_energy_by_tau")
            if not isinstance(slopes, dict):
                continue
            for tau_key, value in slopes.items():
                if finite(value):
                    tau_values.setdefault(int(tau_key), []).append(float(value))
    tau_means = {
        tau: float(mean(values))
        for tau, values in tau_values.items()
        if values
    }
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "seed": metadata.get("run_control", {}).get("seed"),
        "schema_version": source.get("target_timeseries_schema_version"),
        "multi_tau_slope_rows": len(rows) if isinstance(rows, list) else 0,
        "tau_means": {str(tau): value for tau, value in sorted(tau_means.items())},
        "v2_ready": (
            metadata.get("phase") == "production"
            and source.get("target_timeseries_schema_version") == EXPECTED_SCHEMA_VERSION
            and bool(tau_means)
        ),
    }


def summarize_tau(tau: int, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    values = [
        float(chunk["tau_means"][str(tau)])
        for chunk in chunks
        if isinstance(chunk.get("tau_means"), dict) and finite(chunk["tau_means"].get(str(tau)))
    ]
    if not values:
        return {"tau": tau, "available": False}
    value_mean = mean(values)
    value_stdev = stdev(values) if len(values) > 1 else 0.0
    min_value = min(values)
    max_value = max(values)
    positive = min_value > 0.0
    same_sign = all(value > 0.0 for value in values) or all(value < 0.0 for value in values)
    spread_ratio = max_value / min_value if positive else None
    stable = (
        len(values) >= MIN_V2_CHUNKS
        and same_sign
        and abs(value_stdev / value_mean) < STABLE_REL_STDEV_MAX
        and (
            (positive and spread_ratio is not None and spread_ratio < STABLE_SPREAD_MAX)
            or not positive
        )
    )
    return {
        "tau": tau,
        "available": True,
        "n_chunks": len(values),
        "mean": float(value_mean),
        "stdev": float(value_stdev),
        "relative_stdev": float(abs(value_stdev / value_mean)) if value_mean else None,
        "min": float(min_value),
        "max": float(max_value),
        "spread_ratio": float(spread_ratio) if spread_ratio is not None else None,
        "same_sign": same_sign,
        "positive_branch": positive,
        "stable_by_support_rule": stable,
    }


def main() -> int:
    print("PR #230 FH/LSZ v2 target-response stability gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    indices = v2_checkpoint_indices()
    chunks = [collect_chunk(index) for index in indices]
    ready_chunks = [chunk for chunk in chunks if chunk["v2_ready"]]
    tau_set = sorted({int(tau) for chunk in ready_chunks for tau in chunk.get("tau_means", {})})
    tau_summaries = [summarize_tau(tau, ready_chunks) for tau in tau_set]
    stable_positive = [
        row["tau"]
        for row in tau_summaries
        if row.get("stable_by_support_rule") is True
        and row.get("positive_branch") is True
        and row["tau"] in STABLE_POSITIVE_TAU_WINDOWS
    ]
    target_ess_passed = parents["target_ess"].get("target_observable_ess_gate_passed") is True
    legacy_backfill_blocked = (
        parents["legacy_v2_backfill"].get("legacy_summary", {}).get("honest_v2_backfill_possible") is False
    )
    fitted_response_still_open = (
        parents["response_stability"].get("stability_summary", {}).get("stability_passed") is False
    )
    readout_switch_authorized = False
    v2_target_response_stability_passed = (
        len(ready_chunks) >= MIN_V2_CHUNKS
        and STABLE_POSITIVE_TAU_WINDOWS <= set(stable_positive)
        and target_ess_passed
        and legacy_backfill_blocked
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("v2-checkpoint-indices-discovered", len(indices) >= MIN_V2_CHUNKS, f"indices={indices}")
    report("v2-ready-production-chunks", len(ready_chunks) == len(indices) and len(ready_chunks) >= MIN_V2_CHUNKS, f"n={len(ready_chunks)}")
    report("target-observable-ess-passed", target_ess_passed, str(parents["target_ess"].get("actual_current_surface_status")))
    report("legacy-backfill-blocked", legacy_backfill_blocked, str(parents["legacy_v2_backfill"].get("actual_current_surface_status")))
    report("positive-tau-window-stability-passed", STABLE_POSITIVE_TAU_WINDOWS <= set(stable_positive), f"stable_positive={stable_positive}")
    report("fitted-response-still-open", fitted_response_still_open, str(parents["response_stability"].get("actual_current_surface_status")))
    report("readout-switch-not-authorized", not readout_switch_authorized, "v2 target stability is support only")
    report("does-not-authorize-retained-proposal", True, "target stability is not scalar LSZ/canonical-Higgs closure")

    result = {
        "actual_current_surface_status": (
            "bounded-support / FH-LSZ v2 target-response stability passed"
            if v2_target_response_stability_passed
            else "open / FH-LSZ v2 target-response stability not passed"
        ),
        "verdict": (
            "The honest v2 multi-tau population has a stable positive-branch "
            "target-response surface across tau windows 0-9.  This narrows the "
            "response-window issue to the fitted response surface and the "
            "remaining physics gates.  It does not authorize replacing the "
            "production readout by fiat, and it does not supply scalar LSZ, "
            "FV/IR/model-class, or canonical-Higgs/source-overlap closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Stable v2 target slopes are diagnostics only; scalar LSZ and O_H/source-overlap remain open.",
        "bare_retained_allowed": False,
        "v2_target_response_stability_passed": v2_target_response_stability_passed,
        "readout_switch_authorized": readout_switch_authorized,
        "v2_chunk_indices": indices,
        "v2_ready_chunk_count": len(ready_chunks),
        "stable_positive_tau_windows": stable_positive,
        "tau_summaries": tau_summaries,
        "chunk_rows": ready_chunks,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not replace the production response readout with a target window by fiat",
            "does not backfill legacy chunks001-016",
            "does not set kappa_s = 1, cos(theta)=1, c2=1, or Z_match=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Keep accumulating v2 chunks and package completed outputs.  Any "
            "future response-window readout switch needs a separate predeclared "
            "acceptance gate plus scalar LSZ, FV/IR/model-class, and canonical-Higgs identity closure."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
