#!/usr/bin/env python3
"""
PR #230 FH/LSZ production checkpoint granularity gate.

The joint FH/LSZ route is executable only as multi-day production compute.
This runner checks whether the current manifest plus harness resume behavior
is a safe foreground launch surface for the 12-hour campaign.

It is not.  The manifest uses --resume, but the harness currently resumes only
completed per-volume artifacts.  The smallest joint shard is projected well
past the campaign window, and there is no mid-volume configuration checkpoint
that can turn a partial 12-hour run into production evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "outputs" / "yt_fh_lsz_production_manifest_2026-05-01.json"
RESOURCE = ROOT / "outputs" / "yt_fh_lsz_joint_resource_projection_2026-05-01.json"
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_production_checkpoint_granularity_gate_2026-05-01.json"

CAMPAIGN_HOURS = 12.0

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


def main() -> int:
    print("PR #230 FH/LSZ production checkpoint granularity gate")
    print("=" * 72)

    manifest = load(MANIFEST)
    resource = load(RESOURCE)
    harness_text = HARNESS.read_text(encoding="utf-8")
    commands = manifest.get("commands", [])
    volume_rows = resource.get("projection", {}).get("volume_rows", [])
    expected_output_paths = [ROOT / row["output"] for row in commands if isinstance(row, dict)]
    absent_outputs = [str(path.relative_to(ROOT)) for path in expected_output_paths if not path.exists()]

    joint_hours = [
        float(row["joint_mass_scaled_hours"])
        for row in volume_rows
        if isinstance(row, dict) and "joint_mass_scaled_hours" in row
    ]
    smallest_joint_hours = min(joint_hours) if joint_hours else float("inf")
    total_joint_hours = float(resource.get("projection", {}).get("joint_mass_scaled_hours", float("inf")))

    resume_loads_whole_volume = (
        "if args.resume and artifact_path.exists()" in harness_text
        and "ensemble = load_volume_artifact" in harness_text
    )
    writes_after_completed_volume = (
        harness_text.find("ensemble = run_volume(args, spatial_l, time_l, masses, rng)")
        < harness_text.find("written = write_volume_artifact(args.production_output_dir, ensemble)")
        and harness_text.find("written = write_volume_artifact(args.production_output_dir, ensemble)") > 0
    )
    mid_volume_checkpoint_present = (
        "checkpoint" in harness_text.lower()
        or "partial" in harness_text.lower()
        or "cfg_checkpoint" in harness_text
    )
    foreground_launch_safe = (
        smallest_joint_hours <= CAMPAIGN_HOURS
        or (resume_loads_whole_volume and writes_after_completed_volume and mid_volume_checkpoint_present)
    )

    report("manifest-loaded", manifest.get("proposal_allowed") is False, str(MANIFEST.relative_to(ROOT)))
    report("three-shard-manifest", len(commands) == 3, f"commands={len(commands)}")
    report("resource-projection-loaded", resource.get("proposal_allowed") is False, str(RESOURCE.relative_to(ROOT)))
    report(
        "smallest-shard-exceeds-campaign-window",
        smallest_joint_hours > CAMPAIGN_HOURS,
        f"smallest_joint_mass_scaled_hours={smallest_joint_hours:.6g}, campaign_hours={CAMPAIGN_HOURS}",
    )
    report(
        "resume-loads-whole-volume-artifacts",
        resume_loads_whole_volume,
        "resume checks only completed ensemble_measurement.json artifacts",
    )
    report(
        "volume-artifact-written-after-run-volume",
        writes_after_completed_volume,
        "write_volume_artifact is called after run_volume returns",
    )
    report(
        "no-mid-volume-checkpoint-detected",
        not mid_volume_checkpoint_present,
        "no checkpoint/partial-output code path detected in production harness",
    )
    report(
        "expected-production-outputs-absent",
        len(absent_outputs) == len(commands),
        f"absent={absent_outputs}",
    )
    report(
        "foreground-launch-not-safe-evidence-route",
        not foreground_launch_safe,
        "12-hour foreground launch would not produce safely checkpointed production evidence",
    )

    result = {
        "actual_current_surface_status": (
            "open / FH-LSZ production checkpoint granularity gate blocks foreground launch"
        ),
        "verdict": (
            "The joint FH/LSZ manifest is production-targeted and resumable at "
            "the whole-volume artifact level, but the current harness writes "
            "the resumable artifact only after run_volume completes.  The "
            f"smallest projected joint shard is {smallest_joint_hours:.6g} "
            "single-worker hours, far beyond the 12-hour campaign window.  "
            "A foreground launch would therefore be a partial run with no "
            "production certificate and no mid-volume checkpointed evidence."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No safely checkpointed production FH/LSZ output exists, and foreground launch cannot complete the smallest shard.",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "resource_projection": str(RESOURCE.relative_to(ROOT)),
        "harness": str(HARNESS.relative_to(ROOT)),
        "campaign_hours": CAMPAIGN_HOURS,
        "smallest_joint_mass_scaled_hours": smallest_joint_hours,
        "total_joint_mass_scaled_hours": total_joint_hours,
        "expected_outputs_absent": absent_outputs,
        "resume_semantics": {
            "loads_whole_volume_artifacts": resume_loads_whole_volume,
            "writes_artifact_after_run_volume_returns": writes_after_completed_volume,
            "mid_volume_checkpoint_detected": mid_volume_checkpoint_present,
            "foreground_launch_safe": foreground_launch_safe,
        },
        "required_before_foreground_production_launch": [
            "add per-configuration or bounded-chunk checkpoint/resume support including gauge/RNG and accumulated FH/LSZ measurements",
            "or run the manifest under an external scheduler with a walltime budget exceeding the smallest shard",
            "then run the FH/LSZ production postprocess gate on completed production outputs",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not retained or proposed_retained y_t closure",
            "does not treat a partial run as production output",
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
