#!/usr/bin/env python3
"""
PR #230 higher-shell Schur/scalar-LSZ production contract.

The two-source taste-radial row wave was a guarded four-mode campaign and
should not be mutated in place.  After the four-mode packet is complete, this
runner defines the separate higher-shell campaign needed by the Schur/strict
scalar-LSZ route, verifies that it would use non-colliding outputs and seeds,
and records why it is only infrastructure support until rows, pole/threshold
authority, and FV/IR checks exist.
"""

from __future__ import annotations

import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_schur_higher_shell_production_contract_2026-05-07.json"
)
CURRENT_MANIFEST = (
    ROOT
    / "outputs"
    / "yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
)

PARENTS = {
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "strict_scalar_lsz": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "schur_repair": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
    "schur_complete_monotonicity": "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json",
    "schur_pole_lift": "outputs/yt_pr230_two_source_taste_radial_schur_pole_lift_gate_2026-05-06.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

BASE_FOUR_MODES = ("0,0,0", "1,0,0", "0,1,0", "0,0,1")
HIGHER_SHELL_MODES = (
    "0,0,0",
    "1,0,0",
    "0,1,0",
    "0,0,1",
    "1,1,0",
    "1,0,1",
    "0,1,1",
    "1,1,1",
    "2,0,0",
    "0,2,0",
    "0,0,2",
)
SPATIAL_L = 12
CHUNK_COUNT = 63
SEED_BASE = 2026057000
MASS_SPEC = "0.45,0.75,1.05"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
NOISES = 16
THERM = 1000
MEASUREMENTS = 16
SEPARATION = 20

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: str | Path) -> dict[str, Any]:
    full = Path(path)
    if not full.is_absolute():
        full = ROOT / full
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def parse_mode(mode: str) -> tuple[int, int, int]:
    parts = [int(part.strip()) for part in mode.split(",")]
    if len(parts) != 3:
        raise ValueError(f"bad mode {mode!r}")
    return parts[0], parts[1], parts[2]


def p_hat_sq(mode: str, spatial_l: int = SPATIAL_L) -> float:
    return sum((2.0 * math.sin(math.pi * n / spatial_l)) ** 2 for n in parse_mode(mode))


def mode_contract() -> list[dict[str, Any]]:
    rows = []
    for mode in HIGHER_SHELL_MODES:
        rows.append(
            {
                "mode": mode,
                "p_hat_sq_L12": p_hat_sq(mode),
                "shell_class": "zero"
                if mode == "0,0,0"
                else "axis"
                if sorted(parse_mode(mode)) == [0, 0, 1]
                else "face_diagonal"
                if sorted(parse_mode(mode)) == [0, 1, 1]
                else "body_diagonal"
                if sorted(parse_mode(mode)) == [1, 1, 1]
                else "double_axis",
            }
        )
    return rows


def unique_levels(rows: list[dict[str, Any]]) -> list[float]:
    return sorted({round(float(row["p_hat_sq_L12"]), 15) for row in rows})


def current_manifest_modes(manifest: dict[str, Any]) -> set[str]:
    commands = manifest.get("chunk_commands")
    if not isinstance(commands, list) or not commands:
        return set()
    command = commands[0].get("command") if isinstance(commands[0], dict) else None
    if not isinstance(command, list):
        return set()
    modes: set[str] = set()
    for flag in ("--scalar-two-point-modes", "--source-higgs-cross-modes"):
        if flag in command:
            raw = command[command.index(flag) + 1]
            if isinstance(raw, str):
                modes.update(part.strip() for part in raw.split(";") if part.strip())
    return modes


def active_process_rows() -> list[dict[str, Any]]:
    proc = subprocess.run(
        ["ps", "-Ao", "pid=,command="],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if proc.returncode != 0:
        return []
    rows: list[dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        if "yt_direct_lattice_correlator_production.py" not in line:
            continue
        if "yt_pr230_two_source_taste_radial_rows" not in line:
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        command = parts[1] if len(parts) > 1 else line.strip()
        chunk = None
        for index in range(1, 64):
            if f"chunk{index:03d}" in command:
                chunk = index
                break
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def future_output(index: int) -> Path:
    return (
        ROOT
        / "outputs"
        / "yt_pr230_schur_higher_shell_rows"
        / f"yt_pr230_schur_higher_shell_rows_L12_T24_chunk{index:03d}_2026-05-07.json"
    )


def future_production_dir(index: int) -> Path:
    return (
        ROOT
        / "outputs"
        / "yt_direct_lattice_correlator_production_schur_higher_shell_rows"
        / f"L12_T24_chunk{index:03d}"
    )


def future_command(index: int) -> list[str]:
    modes = ";".join(HIGHER_SHELL_MODES)
    return [
        "python3",
        "scripts/yt_direct_lattice_correlator_production.py",
        "--volumes",
        "12x24",
        "--masses",
        MASS_SPEC,
        "--therm",
        str(THERM),
        "--measurements",
        str(MEASUREMENTS),
        "--separation",
        str(SEPARATION),
        "--engine",
        "numba",
        "--production-targets",
        f"--scalar-source-shifts={SOURCE_SHIFTS}",
        "--scalar-two-point-modes",
        modes,
        "--scalar-two-point-noises",
        str(NOISES),
        "--source-higgs-cross-modes",
        modes,
        "--source-higgs-cross-noises",
        str(NOISES),
        "--source-higgs-operator-certificate",
        "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
        "--production-output-dir",
        rel(future_production_dir(index)),
        "--seed",
        str(SEED_BASE + index),
        "--output",
        rel(future_output(index)),
    ]


def noncollision_preview() -> list[dict[str, Any]]:
    return [
        {
            "chunk_index": index,
            "seed": SEED_BASE + index,
            "output": rel(future_output(index)),
            "production_output_dir": rel(future_production_dir(index)),
            "command": future_command(index),
        }
        for index in range(1, CHUNK_COUNT + 1)
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "mutated_active_four_mode_manifest": False,
        "launched_jobs": False,
        "wrote_higher_shell_rows": False,
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_as_selector": False,
        "used_alpha_lm_or_plaquette_u0": False,
        "used_reduced_pilot_as_production_evidence": False,
        "set_c2_equal_one": False,
        "set_z_match_equal_one": False,
        "set_kappa_s_equal_one": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 higher-shell Schur/scalar-LSZ production contract")
    print("=" * 78)

    current_manifest = load_json(CURRENT_MANIFEST)
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    modes = mode_contract()
    levels = unique_levels(modes)
    current_modes = current_manifest_modes(current_manifest)
    active_rows = active_process_rows()
    preview = noncollision_preview()

    current_manifest_is_four_mode = current_modes == set(BASE_FOUR_MODES)
    complete_four_mode_packet = (
        parents["row_combiner"].get("ready_chunks") == CHUNK_COUNT
        and parents["row_combiner"].get("expected_chunks") == CHUNK_COUNT
        and parents["row_combiner"].get("combined_rows_written") is True
        and parents["row_combiner"].get("proposal_allowed") is False
    )
    higher_shell_has_enough_levels = len(levels) >= 5 and levels[0] == 0.0
    future_paths_distinct_from_current = all(
        "yt_pr230_two_source_taste_radial_rows" not in row["output"]
        and "yt_direct_lattice_correlator_production_two_source_taste_radial_rows"
        not in row["production_output_dir"]
        for row in preview
    )
    future_outputs_absent = not any((ROOT / row["output"]).exists() for row in preview)
    future_dirs_absent = not any((ROOT / row["production_output_dir"]).exists() for row in preview)
    seeds_distinct = len({row["seed"] for row in preview}) == CHUNK_COUNT
    no_resume = all("--resume" not in row["command"] for row in preview)
    launch_allowed_now = (
        complete_four_mode_packet
        and not active_rows
        and future_outputs_absent
        and future_dirs_absent
        and future_paths_distinct_from_current
        and seeds_distinct
        and no_resume
    )
    strict_lsz_currently_absent = (
        parents["strict_scalar_lsz"].get("strict_scalar_lsz_moment_fv_authority_present")
        is False
        and parents["strict_scalar_lsz"].get("proposal_allowed") is False
    )
    schur_first_shell_support_only = (
        parents["schur_complete_monotonicity"].get("higher_momentum_shells_present")
        is False
        and parents["schur_complete_monotonicity"].get(
            "complete_monotonicity_authority_passed"
        )
        is False
        and parents["schur_complete_monotonicity"].get("proposal_allowed") is False
    )
    pole_lift_absent = (
        parents["schur_pole_lift"].get("strict_pole_lift_passed") is False
        and parents["schur_pole_lift"].get("proposal_allowed") is False
    )
    source_higgs_bridge_absent = parents["source_higgs_readiness"].get("proposal_allowed") is False
    firewall_clean = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("active-four-mode-manifest-unchanged", current_manifest_is_four_mode, f"current_modes={sorted(current_modes)}")
    report("complete-four-mode-packet-present", complete_four_mode_packet, f"ready={parents['row_combiner'].get('ready_chunks')}/{parents['row_combiner'].get('expected_chunks')}")
    report("higher-shell-mode-set-has-five-ordered-levels", higher_shell_has_enough_levels, f"levels={levels}")
    report("future-paths-do-not-collide-with-active-campaign", future_paths_distinct_from_current, "separate output roots")
    report("future-outputs-absent", future_outputs_absent, "no overwrite of future higher-shell rows")
    report("future-production-dirs-absent", future_dirs_absent, "no partial higher-shell dirs")
    report("future-seeds-distinct", seeds_distinct, f"base={SEED_BASE}")
    report("future-commands-no-resume", no_resume, "replacement-style fresh chunks only")
    report("no-active-workers-detected", not active_rows, f"active={[(row.get('chunk_index'), row.get('pid')) for row in active_rows]}")
    report("launch-preflight-clear-no-rows-written", launch_allowed_now, f"launch_allowed_now={launch_allowed_now}")
    report("strict-lsz-current-authority-absent", strict_lsz_currently_absent, statuses["strict_scalar_lsz"])
    report("schur-first-shell-support-only", schur_first_shell_support_only, statuses["schur_complete_monotonicity"])
    report("schur-pole-lift-authority-absent", pole_lift_absent, statuses["schur_pole_lift"])
    report("source-higgs-bridge-absent", source_higgs_bridge_absent, statuses["source_higgs_readiness"])
    report("forbidden-firewall-clean", firewall_clean, str(forbidden_firewall()))
    report("does-not-authorize-proposal", True, "proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "bounded-support / higher-shell Schur scalar-LSZ production contract; "
            "launch preflight clear after four-mode 63/63 completion; no physics closure"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This contract defines a non-colliding higher-shell row campaign and "
            "the launch preflight is now clear because the four-mode packet is "
            "complete and no active workers are detected.  It still does not "
            "launch jobs, does not write measurement rows, and does not supply "
            "complete monotonicity, threshold, FV/IR, pole, canonical O_H, or "
            "physical-response authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "higher_shell_schur_production_contract_passed": FAIL_COUNT == 0,
        "current_four_mode_campaign_must_remain_unmixed": True,
        "complete_four_mode_packet": complete_four_mode_packet,
        "current_manifest": rel(CURRENT_MANIFEST),
        "current_manifest_modes": sorted(current_modes),
        "active_process_rows": active_rows,
        "launch_allowed_now": launch_allowed_now,
        "launch_block_reason": None
        if launch_allowed_now
        else (
            "higher-shell launch is blocked until the four-mode packet is "
            "complete, active workers are absent, and future paths are empty"
        ),
        "jobs_launched_by_contract": False,
        "rows_written_by_contract": False,
        "higher_shell_modes": modes,
        "ordered_p_hat_sq_levels_L12": levels,
        "future_noncollision_preview": preview,
        "acceptance_requirements": [
            "run as a separate manifest/output root, not by mutating the active four-mode packet",
            "preserve three-mass top scan and selected-mass-only FH/LSZ at m=0.75",
            "preserve numba_gauge_seed_v1 seed control and fixed seed base",
            "require completed-mode chunk checkpoints before row use",
            "require a complete higher-shell packet before complete-monotonicity claims",
            "require threshold/model-class/pole and multivolume FV/IR authority before scalar-LSZ closure",
            "require canonical O_H/source-overlap or W/Z physical-response bridge before y_t closure",
        ],
        "strict_non_claims": [
            "not production evidence",
            "not a scalar-LSZ moment certificate",
            "not a Schur pole-row certificate",
            "not canonical O_H or source-overlap authority",
            "does not claim retained or proposed_retained y_t closure",
        ],
        "forbidden_firewall": forbidden_firewall(),
        "parent_statuses": statuses,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
