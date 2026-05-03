#!/usr/bin/env python3
"""
PR #230 FH/LSZ target-observable ESS certificate.

The autocorrelation gate must not use plaquette ESS as a proxy for the
load-bearing FH/LSZ target observables.  This runner reads the actual
per-configuration same-source target rows from the ready chunk set and records
a chunk-blocked initial-positive ESS diagnostic for dE/ds and C_ss/Gamma_ss.
It is an acceptance-boundary certificate, not retained physics evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READY_SET = ROOT / "outputs" / "yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json"

MIN_TARGET_ESS_PER_VOLUME = 200.0
MIN_READY_CHUNKS_FOR_GATE = 8

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
    if isinstance(ensembles, list) and len(ensembles) == 1 and isinstance(ensembles[0], dict):
        return ensembles[0]
    return {}


def chunk_path(index: int) -> Path:
    return ROOT / "outputs" / f"yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"


def autocorrelation_tau_int(values: list[float], max_lag: int = 8) -> dict[str, Any]:
    n = len(values)
    if n < 8:
        return {"available": False, "n": n, "reason": "too few target rows"}
    mu = mean(values)
    centered = [x - mu for x in values]
    var = sum(x * x for x in centered) / n
    if var <= 0.0:
        return {"available": False, "n": n, "reason": "zero target variance"}
    tau = 0.5
    rho_values: list[float] = []
    window_lag = 0
    for lag in range(1, min(max_lag, n // 2) + 1):
        cov = sum(centered[i] * centered[i + lag] for i in range(n - lag)) / (n - lag)
        rho = cov / var
        rho_values.append(float(rho))
        window_lag = lag
        if rho <= 0.0:
            break
        tau += rho
    ess = n / max(2.0 * tau, 1.0)
    return {
        "available": True,
        "n": n,
        "tau_int_initial_positive": float(tau),
        "ess_initial_positive": float(ess),
        "window_lag": int(window_lag),
        "rho_first_lags": rho_values[:8],
    }


def block_summary(blocks: list[list[float]]) -> dict[str, Any]:
    finite_blocks = [[float(x) for x in block if finite(x)] for block in blocks]
    finite_blocks = [block for block in finite_blocks if block]
    chunk_rows = []
    total_ess = 0.0
    min_chunk_ess: float | None = None
    for index, block in enumerate(finite_blocks, start=1):
        tau = autocorrelation_tau_int(block)
        ess = tau.get("ess_initial_positive") if tau.get("available") else 0.0
        ess_float = float(ess) if finite(ess) else 0.0
        total_ess += ess_float
        min_chunk_ess = ess_float if min_chunk_ess is None else min(min_chunk_ess, ess_float)
        chunk_rows.append(
            {
                "block_index": index,
                "n": len(block),
                "mean": float(mean(block)),
                "tau_int": tau,
            }
        )
    all_values = [value for block in finite_blocks for value in block]
    block_means = [mean(block) for block in finite_blocks]
    block_mean = mean(block_means) if block_means else float("nan")
    if len(block_means) > 1:
        block_var = sum((x - block_mean) ** 2 for x in block_means) / (len(block_means) - 1)
        block_stderr = math.sqrt(block_var / len(block_means))
    else:
        block_stderr = float("nan")
    return {
        "available": bool(finite_blocks),
        "block_count": len(finite_blocks),
        "raw_sample_count": len(all_values),
        "total_ess_initial_positive": float(total_ess),
        "min_chunk_ess_initial_positive": float(min_chunk_ess) if min_chunk_ess is not None else None,
        "mean": float(mean(all_values)) if all_values else float("nan"),
        "chunk_block_mean": float(block_mean),
        "chunk_block_stderr": float(block_stderr),
        "chunk_rows": chunk_rows,
    }


def collect_chunk_targets(index: int) -> dict[str, Any]:
    data = load_json(chunk_path(index))
    ensemble = first_ensemble(data)
    metadata = data.get("metadata", {})
    source = ensemble.get("scalar_source_response_analysis", {})
    lsz = ensemble.get("scalar_two_point_lsz_analysis", {})
    source_slopes = [
        float(row["slope_effective_energy_tau1"])
        for row in source.get("per_configuration_slopes", [])
        if isinstance(row, dict)
        and row.get("finite") is True
        and finite(row.get("slope_effective_energy_tau1"))
    ]
    lsz_modes: dict[str, dict[str, list[float]]] = {}
    mode_rows = lsz.get("mode_rows", {})
    if isinstance(mode_rows, dict):
        for mode, row in mode_rows.items():
            if not isinstance(row, dict):
                continue
            c_rows = row.get("C_ss_timeseries", [])
            if not isinstance(c_rows, list):
                continue
            c_values = [
                float(item["C_ss_real"])
                for item in c_rows
                if isinstance(item, dict) and finite(item.get("C_ss_real"))
            ]
            gamma_values = [
                float(item["Gamma_ss_real"])
                for item in c_rows
                if isinstance(item, dict) and finite(item.get("Gamma_ss_real"))
            ]
            lsz_modes[str(mode)] = {
                "C_ss_real": c_values,
                "Gamma_ss_real": gamma_values,
            }
    return {
        "chunk_index": index,
        "path": str(chunk_path(index).relative_to(ROOT)),
        "phase": metadata.get("phase"),
        "source_slope_tau1": source_slopes,
        "lsz_modes": lsz_modes,
    }


def main() -> int:
    print("PR #230 FH/LSZ target-observable ESS certificate")
    print("=" * 72)

    ready_set = load_json(READY_SET)
    ready_indices = [
        int(index)
        for index in ready_set.get("ready_chunk_indices", [])
        if isinstance(index, int) or (isinstance(index, str) and index.isdigit())
    ]
    chunks = [collect_chunk_targets(index) for index in ready_indices]
    source_blocks = [chunk["source_slope_tau1"] for chunk in chunks]
    source_summary = block_summary(source_blocks)

    modes = sorted(
        {
            mode
            for chunk in chunks
            for mode in chunk.get("lsz_modes", {})
        }
    )
    lsz_summaries: dict[str, dict[str, Any]] = {}
    for mode in modes:
        lsz_summaries[mode] = {
            "C_ss_real": block_summary(
                [chunk.get("lsz_modes", {}).get(mode, {}).get("C_ss_real", []) for chunk in chunks]
            ),
            "Gamma_ss_real": block_summary(
                [chunk.get("lsz_modes", {}).get(mode, {}).get("Gamma_ss_real", []) for chunk in chunks]
            ),
        }

    observable_ess = [source_summary.get("total_ess_initial_positive", 0.0)]
    for mode_summary in lsz_summaries.values():
        observable_ess.append(mode_summary["C_ss_real"].get("total_ess_initial_positive", 0.0))
        observable_ess.append(mode_summary["Gamma_ss_real"].get("total_ess_initial_positive", 0.0))
    finite_ess = [float(value) for value in observable_ess if finite(value)]
    min_target_ess = min(finite_ess) if finite_ess else 0.0
    ready_count_reaches_threshold = len(ready_indices) >= MIN_READY_CHUNKS_FOR_GATE
    target_rows_complete = (
        bool(chunks)
        and bool(modes)
        and all(len(block) > 0 for block in source_blocks)
        and all(
            len(chunk.get("lsz_modes", {}).get(mode, {}).get("C_ss_real", [])) > 0
            and len(chunk.get("lsz_modes", {}).get(mode, {}).get("Gamma_ss_real", [])) > 0
            for chunk in chunks
            for mode in modes
        )
    )
    target_observable_ess_gate_passed = (
        ready_count_reaches_threshold
        and target_rows_complete
        and min_target_ess >= MIN_TARGET_ESS_PER_VOLUME
    )
    ess_per_chunk = min_target_ess / max(len(ready_indices), 1)
    additional_chunks_estimate = (
        math.ceil((MIN_TARGET_ESS_PER_VOLUME - min_target_ess) / ess_per_chunk)
        if ess_per_chunk > 0.0 and min_target_ess < MIN_TARGET_ESS_PER_VOLUME
        else 0
    )
    ess_labels = [("source_slope_tau1", source_summary.get("total_ess_initial_positive", 0.0))]
    for mode, mode_summary in lsz_summaries.items():
        ess_labels.append(
            (f"scalar_lsz_mode_{mode}_C_ss_real", mode_summary["C_ss_real"].get("total_ess_initial_positive", 0.0))
        )
        ess_labels.append(
            (
                f"scalar_lsz_mode_{mode}_Gamma_ss_real",
                mode_summary["Gamma_ss_real"].get("total_ess_initial_positive", 0.0),
            )
        )
    limiting_observable = min(
        ((label, float(value)) for label, value in ess_labels if finite(value)),
        key=lambda item: item[1],
        default=("none", 0.0),
    )[0]

    report("ready-set-loaded", bool(ready_set), str(READY_SET.relative_to(ROOT)))
    report(
        "ready-chunk-count-state-recorded",
        True,
        f"ready_chunks={ready_indices}, threshold={MIN_READY_CHUNKS_FOR_GATE}",
    )
    report(
        "source-response-target-rows-present",
        all(len(block) > 0 for block in source_blocks),
        f"rows_per_chunk={[len(block) for block in source_blocks]}",
    )
    report(
        "scalar-lsz-target-rows-present",
        bool(modes)
        and all(
            len(chunk.get("lsz_modes", {}).get(mode, {}).get("C_ss_real", [])) > 0
            for chunk in chunks
            for mode in modes
        ),
        f"modes={modes}",
    )
    report(
        "target-observable-ess-state-recorded",
        True,
        f"min_target_ess={min_target_ess:.6g}, threshold={MIN_TARGET_ESS_PER_VOLUME}",
    )
    if target_observable_ess_gate_passed:
        report("target-observable-ess-gate-passed", True, "target ESS threshold reached")
    else:
        report(
            "target-observable-ess-gate-not-passed",
            True,
            f"limiting ESS below threshold; estimated additional chunks={additional_chunks_estimate}",
        )
    report(
        "does-not-use-plaquette-ess-proxy",
        True,
        "only same-source dE/ds and C_ss/Gamma_ss target rows are load-bearing",
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        "target ESS is an acceptance boundary, not scalar LSZ or canonical-Higgs closure",
    )

    status = (
        "bounded-support / FH-LSZ target-observable ESS certificate passed"
        if target_observable_ess_gate_passed
        else "open / FH-LSZ target-observable ESS certificate not passed"
    )
    result = {
        "actual_current_surface_status": status,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Target ESS does not identify the scalar source with the canonical Higgs "
            "and does not supply pole derivative/model-class/FV/IR closure."
        ),
        "target_observable_ess_gate_passed": target_observable_ess_gate_passed,
        "minimum_target_ess_per_volume": MIN_TARGET_ESS_PER_VOLUME,
        "minimum_ready_chunks_for_gate": MIN_READY_CHUNKS_FOR_GATE,
        "ready_chunk_indices": ready_indices,
        "ready_chunk_count": len(ready_indices),
        "target_rows_complete": target_rows_complete,
        "limiting_target_ess": min_target_ess,
        "limiting_target_ess_observable": limiting_observable,
        "additional_chunks_estimate_at_current_rate": int(additional_chunks_estimate),
        "source_response_summary": source_summary,
        "scalar_lsz_summaries": lsz_summaries,
        "chunk_rows": [
            {
                "chunk_index": chunk["chunk_index"],
                "path": chunk["path"],
                "phase": chunk["phase"],
                "source_slope_rows": len(chunk["source_slope_tau1"]),
                "scalar_lsz_modes": sorted(chunk["lsz_modes"]),
            }
            for chunk in chunks
        ],
        "strict_non_claims": [
            "does not treat plaquette ESS as target FH/LSZ ESS",
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not identify the source pole with the canonical Higgs radial mode",
        ],
        "exact_next_action": (
            "Rerun the autocorrelation ESS gate; target-observable ESS is no longer the active blocker."
            if target_observable_ess_gate_passed
            else (
                "Continue optimized target-timeseries chunks until the limiting "
                "same-source dE/ds target ESS reaches the predeclared threshold, "
                "then rerun this certificate and the autocorrelation ESS gate."
            )
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
