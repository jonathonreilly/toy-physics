#!/usr/bin/env python3
"""
PR #230 FH/LSZ chunked production manifest.

The checkpoint-granularity gate shows that whole-volume production cannot be
completed inside the 12-hour foreground campaign.  This runner derives a
bounded chunk manifest for the L12_T24 shard only.  It does not launch the
chunks and does not claim evidence; it gives exact production-targeted chunk
commands that can later be combined only by a separate multi-chain/postprocess
certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESOURCE = ROOT / "outputs" / "yt_fh_lsz_joint_resource_projection_2026-05-01.json"
CHECKPOINT_GATE = ROOT / "outputs" / "yt_fh_lsz_production_checkpoint_granularity_gate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_chunked_production_manifest_2026-05-01.json"

CAMPAIGN_HOURS = 12.0
FULL_THERM = 1000
FULL_MEASUREMENTS = 1000
SEPARATION = 20
CHUNK_MEASUREMENTS = 16
MASS_SPEC = "0.45,0.75,1.05"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
SCALAR_MODES = "0,0,0;1,0,0;0,1,0;0,0,1"
SCALAR_NOISES = 16

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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def shell_join(parts: list[str]) -> str:
    return " ".join(parts)


def command_for_chunk(chunk_index: int) -> dict[str, Any]:
    output = (
        "outputs/yt_pr230_fh_lsz_production_L12_T24_"
        f"chunk{chunk_index:03d}_2026-05-01.json"
    )
    production_output_dir = (
        "outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/"
        f"L12_T24_chunk{chunk_index:03d}"
    )
    seed = 2026051000 + chunk_index
    command = shell_join(
        [
            "python3",
            "scripts/yt_direct_lattice_correlator_production.py",
            "--volumes",
            "12x24",
            "--masses",
            MASS_SPEC,
            "--therm",
            str(FULL_THERM),
            "--measurements",
            str(CHUNK_MEASUREMENTS),
            "--separation",
            str(SEPARATION),
            "--engine",
            "numba",
            "--production-targets",
            f"--scalar-source-shifts={SOURCE_SHIFTS}",
            "--scalar-two-point-modes",
            f"'{SCALAR_MODES}'",
            "--scalar-two-point-noises",
            str(SCALAR_NOISES),
            "--production-output-dir",
            production_output_dir,
            "--resume",
            "--seed",
            str(seed),
            "--output",
            output,
        ]
    )
    return {
        "chunk_index": chunk_index,
        "seed": seed,
        "volume": "12x24",
        "measurements": CHUNK_MEASUREMENTS,
        "output": output,
        "production_output_dir": production_output_dir,
        "command": command,
        "status": "launch command only; not evidence until completed and combined by a postprocess certificate",
    }


def main() -> int:
    print("PR #230 FH/LSZ chunked production manifest")
    print("=" * 72)

    resource = load(RESOURCE)
    checkpoint_gate = load(CHECKPOINT_GATE)
    volume_rows = resource.get("projection", {}).get("volume_rows", [])
    by_volume = {row.get("volume"): row for row in volume_rows if isinstance(row, dict)}
    l12_hours = float(by_volume["12^3x24"]["joint_mass_scaled_hours"])
    l16_hours = float(by_volume["16^3x32"]["joint_mass_scaled_hours"])
    l24_hours = float(by_volume["24^3x48"]["joint_mass_scaled_hours"])

    full_sweeps = FULL_THERM + FULL_MEASUREMENTS * SEPARATION
    chunk_sweeps = FULL_THERM + CHUNK_MEASUREMENTS * SEPARATION
    conservative_fraction = max(CHUNK_MEASUREMENTS / FULL_MEASUREMENTS, chunk_sweeps / full_sweeps)
    l12_chunk_hours = l12_hours * conservative_fraction
    l16_min_hours = l16_hours * (FULL_THERM / full_sweeps)
    l24_min_hours = l24_hours * (FULL_THERM / full_sweeps)
    chunk_count_l12 = math.ceil(FULL_MEASUREMENTS / CHUNK_MEASUREMENTS)
    example_commands = [command_for_chunk(index) for index in range(1, 4)]

    report("resource-loaded", resource.get("proposal_allowed") is False, str(RESOURCE.relative_to(ROOT)))
    report(
        "checkpoint-gate-loaded",
        checkpoint_gate.get("proposal_allowed") is False
        and checkpoint_gate.get("resume_semantics", {}).get("foreground_launch_safe") is False,
        checkpoint_gate.get("actual_current_surface_status", ""),
    )
    report(
        "l12-chunk-fits-foreground-window",
        l12_chunk_hours < CAMPAIGN_HOURS,
        f"estimated_l12_chunk_hours={l12_chunk_hours:.6g}",
    )
    report(
        "l16-minimum-chunk-does-not-fit-foreground-window",
        l16_min_hours > CAMPAIGN_HOURS,
        f"l16_minimum_rethermalized_hours={l16_min_hours:.6g}",
    )
    report(
        "l24-minimum-chunk-does-not-fit-foreground-window",
        l24_min_hours > CAMPAIGN_HOURS,
        f"l24_minimum_rethermalized_hours={l24_min_hours:.6g}",
    )
    report(
        "l12-chunk-count-covers-target",
        chunk_count_l12 * CHUNK_MEASUREMENTS >= FULL_MEASUREMENTS,
        f"chunk_count_l12={chunk_count_l12}",
    )
    report(
        "commands-production-targeted",
        all("--production-targets" in row["command"] for row in example_commands),
        "example commands include production-targeted flag",
    )
    report(
        "commands-use-chunk-local-artifacts",
        all("--production-output-dir" in row["command"] and f"chunk{row['chunk_index']:03d}" in row["command"] for row in example_commands),
        "example commands isolate per-volume artifacts by chunk",
    )
    report(
        "commands-resumable-per-chunk",
        all("--resume" in row["command"] for row in example_commands),
        "example commands can resume the chunk-local artifact if complete",
    )
    report("not-production-evidence", True, "chunk manifest is launch planning only")

    result = {
        "actual_current_surface_status": "bounded-support / FH-LSZ chunked production manifest",
        "verdict": (
            "The L12_T24 FH/LSZ production shard can be split into "
            f"{chunk_count_l12} independent production-targeted chunks of "
            f"{CHUNK_MEASUREMENTS} saved configurations, with a conservative "
            f"per-chunk estimate of {l12_chunk_hours:.6g} hours.  This makes "
            "L12 foreground scheduling possible, but it is not closure: L16 "
            "and L24 remain above the 12-hour window even under a rethermalized "
            "minimum-chunk estimate, and all chunks require a future "
            "multi-chain combination plus scalar-pole postprocess gate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "A chunked launch manifest is not production evidence and does not derive kappa_s or the scalar pole derivative.",
        "parent_certificates": {
            "resource_projection": str(RESOURCE.relative_to(ROOT)),
            "checkpoint_granularity_gate": str(CHECKPOINT_GATE.relative_to(ROOT)),
        },
        "chunk_policy": {
            "volume": "12x24",
            "chunk_measurements": CHUNK_MEASUREMENTS,
            "target_measurements": FULL_MEASUREMENTS,
            "chunk_count": chunk_count_l12,
            "thermalization_sweeps_per_chunk": FULL_THERM,
            "separation_sweeps": SEPARATION,
            "conservative_fraction_of_full_l12": conservative_fraction,
            "estimated_l12_chunk_hours": l12_chunk_hours,
            "campaign_hours": CAMPAIGN_HOURS,
        },
        "larger_volume_foreground_status": {
            "l16_minimum_rethermalized_hours": l16_min_hours,
            "l24_minimum_rethermalized_hours": l24_min_hours,
            "requires_scheduler_or_true_checkpointing": True,
        },
        "example_commands": example_commands,
        "combination_requirements": [
            "each chunk must complete as production phase output",
            "chunks must be combined by a multi-chain FH/LSZ postprocess certificate",
            "the combination must preserve independent seeds, source shifts, scalar modes, and noise counts",
            "each chunk must use a chunk-local production-output-dir so per-volume artifacts cannot collide",
            "the scalar pole derivative and FV/IR/zero-mode control must still pass the postprocess gate",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not treat partial chunks as complete volume evidence",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed top mass, or observed y_t",
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
