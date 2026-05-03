#!/usr/bin/env python3
"""
PR #230 FH/LSZ target-timeseries replacement queue certificate.

The autocorrelation/ESS gate currently has enough ready chunks to evaluate a
target-observable ESS gate, but some ready chunks can predate target-timeseries
serialization. This runner derives the exact replacement queue from the current
autocorrelation certificate instead of treating more new chunks as a complete
ESS repair.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUTOCORR = ROOT / "outputs" / "yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json"
COMBINER = ROOT / "outputs" / "yt_fh_lsz_chunk_combiner_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json"

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


def chunk_command(index: int) -> str:
    seed = 2026051000 + index
    return (
        "python3 scripts/yt_direct_lattice_correlator_production.py "
        "--volumes 12x24 --masses 0.45,0.75,1.05 --therm 1000 "
        "--measurements 16 --separation 20 --engine numba --production-targets "
        "--scalar-source-shifts=-0.01,0.0,0.01 "
        "--scalar-two-point-modes '0,0,0;1,0,0;0,1,0;0,0,1' "
        "--scalar-two-point-noises 16 "
        f"--production-output-dir outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk{index:03d} "
        "--resume "
        f"--seed {seed} "
        f"--output outputs/yt_pr230_fh_lsz_production_L12_T24_chunk{index:03d}_2026-05-01.json"
    )


def main() -> int:
    print("PR #230 FH/LSZ target-timeseries replacement queue")
    print("=" * 72)

    autocorr = load_json(AUTOCORR)
    combiner = load_json(COMBINER)
    summary = autocorr.get("target_timeseries_summary", {}) if isinstance(autocorr, dict) else {}
    combiner_summary = combiner.get("chunk_summary", {}) if isinstance(combiner, dict) else {}
    ready_indices = [
        int(index)
        for index in autocorr.get("ready_chunk_indices", [])
        if isinstance(index, int)
    ]
    incomplete_indices = [
        int(index)
        for index in summary.get("incomplete_indices", [])
        if isinstance(index, int)
    ]
    complete_indices = [
        int(index)
        for index in summary.get("complete_indices", [])
        if isinstance(index, int)
    ]
    replacement_queue = sorted(index for index in incomplete_indices if index in ready_indices)
    next_replacement = replacement_queue[0] if replacement_queue else None
    commands = {f"chunk{index:03d}": chunk_command(index) for index in replacement_queue}

    report("autocorr-certificate-present", bool(autocorr), str(AUTOCORR.relative_to(ROOT)))
    report("combiner-certificate-present", bool(combiner), str(COMBINER.relative_to(ROOT)))
    report(
        "ready-set-threshold-reached",
        autocorr.get("ready_count_reaches_threshold") is True and len(ready_indices) >= 8,
        f"ready_indices={ready_indices}",
    )
    report(
        "target-timeseries-incomplete-for-ready-set",
        summary.get("complete_for_all_ready_chunks") is False and bool(incomplete_indices),
        f"summary={summary}",
    )
    report(
        "replacement-queue-derived-from-ready-set",
        replacement_queue == incomplete_indices and all(index in ready_indices for index in replacement_queue),
        f"replacement_queue={replacement_queue}",
    )
    report(
        "new-chunks-alone-do-not-repair-current-target-ess",
        bool(replacement_queue) and min(replacement_queue) < max(complete_indices or [0]),
        f"complete={complete_indices}, incomplete={incomplete_indices}",
    )
    report(
        "replacement-keeps-production-target-schema",
        bool(commands)
        and all("--production-targets" in cmd and "--scalar-two-point-noises 16" in cmd for cmd in commands.values()),
        f"commands={list(commands)[:3]}...",
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        "replacement queue is scheduling support; no new production output is certified",
    )

    complete_label = ", ".join(f"chunk{index:03d}" for index in complete_indices) or "none"
    replacement_label = ", ".join(f"chunk{index:03d}" for index in replacement_queue) or "none"
    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ target-timeseries replacement queue",
        "verdict": (
            "The ready L12 set has reached the minimum size for target ESS checks, "
            f"with target-series complete for {complete_label} and still missing for "
            f"{replacement_label}. Therefore later new chunks can increase the "
            "target-series subset, but cannot make complete_for_all_ready_chunks true "
            "while the replacement queue remains nonempty."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The queue only identifies replacement work. It supplies no new target "
            "ESS, response stability, scalar-pole derivative, FV/IR, or canonical-Higgs identity certificate."
        ),
        "autocorrelation_certificate": str(AUTOCORR.relative_to(ROOT)),
        "combiner_certificate": str(COMBINER.relative_to(ROOT)),
        "combiner_summary": combiner_summary,
        "target_timeseries_summary": summary,
        "ready_indices": ready_indices,
        "complete_target_timeseries_indices": complete_indices,
        "replacement_queue": replacement_queue,
        "next_replacement_chunk": next_replacement,
        "replacement_commands": commands,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat plaquette ESS as target ESS",
            "does not treat replacement commands as production evidence",
            "does not set kappa_s = 1 or identify the source pole as canonical Higgs",
        ],
        "exact_next_action": (
            f"Rerun chunk{next_replacement:03d} with target-timeseries serialization if "
            "completing the current ready-set target ESS gate is prioritized; otherwise "
            "continue new target-series chunks toward the full L12 set. Do not claim "
            "complete target ESS while the replacement queue is nonempty."
            if next_replacement is not None
            else "Rerun the autocorrelation/ESS gate; no replacement queue is currently open."
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
