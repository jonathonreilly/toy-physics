#!/usr/bin/env python3
"""
PR #230 source-Higgs time-kernel production manifest.

The source-Higgs time-kernel harness and GEVP contract are now implemented,
but only reduced smoke rows exist.  This runner defines the non-colliding
production row manifest needed by the clean O_H/C_sH/C_HH route and records
why it is still support-only on the current surface: canonical O_H or an
equivalent physical neutral/WZ identity is absent, and active static row
workers must not be collided with.
"""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json"
)
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
ACTION_CERT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
CHUNK_OUTPUT_ROOT = ROOT / "outputs" / "yt_pr230_source_higgs_time_kernel_rows"
PRODUCTION_OUTPUT_ROOT = (
    ROOT / "outputs" / "yt_direct_lattice_correlator_production_source_higgs_time_kernel_rows"
)
STATIC_ROW_OUTPUT_ROOT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_rows"
STATIC_PRODUCTION_ROOT = (
    ROOT / "outputs" / "yt_direct_lattice_correlator_production_two_source_taste_radial_rows"
)

PARENTS = {
    "time_kernel_harness": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
    "time_kernel_gevp_contract": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "direct_source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "canonical_oh_hard_residual": "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json",
    "taste_radial_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

CHUNK_COUNT = 63
SEED_BASE = 2026058000
MASS_SPEC = "0.45,0.75,1.05"
SOURCE_SHIFTS = "-0.01,0.0,0.01"
MOMENTUM_MODES = "0,0,0;1,0,0;0,1,0;0,0,1"
SCALAR_TWO_POINT_NOISES = 16
SOURCE_HIGGS_CROSS_NOISES = 16
TIME_KERNEL_NOISES = 16
TIME_KERNEL_MAX_TAU = 4
TIME_KERNEL_ORIGIN_COUNT = 4
THERM = 1000
MEASUREMENTS = 16
SEPARATION = 20
MAX_CONCURRENT_RECOMMENDED = 2

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


def load_json(rel_path: str | Path) -> dict[str, Any]:
    path = Path(rel_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def chunk_seed(index: int) -> int:
    return SEED_BASE + index


def chunk_output(index: int) -> Path:
    return CHUNK_OUTPUT_ROOT / f"yt_pr230_source_higgs_time_kernel_rows_L12_T24_chunk{index:03d}_2026-05-07.json"


def chunk_production_dir(index: int) -> Path:
    return PRODUCTION_OUTPUT_ROOT / f"L12_T24_chunk{index:03d}"


def production_command(index: int) -> list[str]:
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
        MOMENTUM_MODES,
        "--scalar-two-point-noises",
        str(SCALAR_TWO_POINT_NOISES),
        "--source-higgs-cross-modes",
        MOMENTUM_MODES,
        "--source-higgs-cross-noises",
        str(SOURCE_HIGGS_CROSS_NOISES),
        "--source-higgs-time-kernel-modes",
        MOMENTUM_MODES,
        "--source-higgs-time-kernel-noises",
        str(TIME_KERNEL_NOISES),
        "--source-higgs-time-kernel-max-tau",
        str(TIME_KERNEL_MAX_TAU),
        "--source-higgs-time-kernel-origin-count",
        str(TIME_KERNEL_ORIGIN_COUNT),
        "--source-higgs-operator-certificate",
        rel(ACTION_CERT),
        "--production-output-dir",
        rel(chunk_production_dir(index)),
        "--seed",
        str(chunk_seed(index)),
        "--output",
        rel(chunk_output(index)),
    ]


def command_option_equals(command: list[str], option: str, expected: str) -> bool:
    try:
        index = command.index(option)
    except ValueError:
        return False
    return index + 1 < len(command) and command[index + 1] == expected


def active_production_rows() -> list[dict[str, Any]]:
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
        if "yt_pr230_" not in line and "yt_direct_lattice_correlator_production_" not in line:
            continue
        parts = line.strip().split(maxsplit=1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            pid = -1
        command = parts[1] if len(parts) > 1 else line.strip()
        try:
            argv = shlex.split(command)
        except ValueError:
            argv = []
        if not any(token.endswith("yt_direct_lattice_correlator_production.py") for token in argv):
            continue
        chunk = None
        for index in range(1, CHUNK_COUNT + 1):
            if f"chunk{index:03d}" in command:
                chunk = index
                break
        rows.append({"pid": pid, "chunk_index": chunk, "command": command})
    return rows


def chunk_state(index: int) -> dict[str, Any]:
    out = chunk_output(index)
    pdir = chunk_production_dir(index)
    return {
        "chunk_index": index,
        "seed": chunk_seed(index),
        "output": rel(out),
        "output_present": out.exists(),
        "production_output_dir": rel(pdir),
        "production_output_dir_present": pdir.exists(),
        "command": production_command(index) if not out.exists() else None,
    }


def main() -> int:
    print("PR #230 source-Higgs time-kernel production manifest")
    print("=" * 72)

    harness_text = HARNESS.read_text(encoding="utf-8") if HARNESS.exists() else ""
    parent_certs = {name: load_json(path) for name, path in PARENTS.items()}
    parent_statuses = {name: status(cert) for name, cert in parent_certs.items()}
    missing_parents = [name for name, cert in parent_certs.items() if not cert]
    action = load_json(ACTION_CERT)
    active_rows = active_production_rows()
    chunks = [chunk_state(index) for index in range(1, CHUNK_COUNT + 1)]
    commands = [row["command"] for row in chunks if isinstance(row.get("command"), list)]

    harness_has_cli = all(
        token in harness_text
        for token in (
            "--source-higgs-time-kernel-modes",
            "--source-higgs-time-kernel-noises",
            "--source-higgs-time-kernel-max-tau",
            "--source-higgs-time-kernel-origin-count",
            "source_higgs_time_kernel_analysis",
            "source_higgs_time_kernel_v1",
        )
    )
    parents_firewalled = all(cert.get("proposal_allowed") is False for cert in parent_certs.values())
    time_kernel_support_loaded = (
        "support-only" in parent_statuses["time_kernel_harness"]
        and "smoke rows are not physics closure" in parent_statuses["time_kernel_gevp_contract"]
    )
    canonical_oh_absent = (
        "not closed" in parent_statuses["canonical_oh_hard_residual"]
        and parent_certs["source_higgs_readiness"].get("proposal_allowed") is False
    )
    action_is_taste_radial_not_oh = (
        action.get("proposal_allowed") is False
        and action.get("canonical_higgs_operator_identity_passed") is False
    )
    active_static_chunks = [
        row
        for row in active_rows
        if "yt_pr230_two_source_taste_radial_rows" in row.get("command", "")
        or "yt_direct_lattice_correlator_production_two_source_taste_radial_rows" in row.get("command", "")
    ]
    active_time_kernel_chunks = [
        row
        for row in active_rows
        if "yt_pr230_source_higgs_time_kernel_rows" in row.get("command", "")
        or "yt_direct_lattice_correlator_production_source_higgs_time_kernel_rows" in row.get("command", "")
    ]
    outputs_distinct = len({row["output"] for row in chunks}) == CHUNK_COUNT
    dirs_distinct = len({row["production_output_dir"] for row in chunks}) == CHUNK_COUNT
    no_resume = all("--resume" not in command for command in commands)
    static_output_collision = any(
        row["output"].startswith(rel(STATIC_ROW_OUTPUT_ROOT))
        or row["production_output_dir"].startswith(rel(STATIC_PRODUCTION_ROOT))
        for row in chunks
    )
    seed_range_disjoint_from_static_and_higher_shell = min(chunk_seed(1), chunk_seed(CHUNK_COUNT)) >= 2026058001
    all_commands_enable_time_kernel = all(
        command_option_equals(command, "--source-higgs-time-kernel-modes", MOMENTUM_MODES)
        and command_option_equals(
            command, "--source-higgs-time-kernel-noises", str(TIME_KERNEL_NOISES)
        )
        and command_option_equals(
            command, "--source-higgs-time-kernel-max-tau", str(TIME_KERNEL_MAX_TAU)
        )
        and command_option_equals(
            command,
            "--source-higgs-time-kernel-origin-count",
            str(TIME_KERNEL_ORIGIN_COUNT),
        )
        for command in commands
    )
    closure_launch_authorized_now = False
    support_launch_authorized_now = False
    launch_blockers = []
    if canonical_oh_absent:
        launch_blockers.append("canonical O_H / physical neutral identity absent")
    if action_is_taste_radial_not_oh:
        launch_blockers.append("current operator certificate is taste-radial support, not canonical O_H")
    if active_static_chunks:
        launch_blockers.append("active static taste-radial workers already own the two-worker cap")
    if active_time_kernel_chunks:
        launch_blockers.append("time-kernel workers already active")

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parents-remain-firewalled", parents_firewalled, ", ".join(parent_statuses.values()))
    report("harness-time-kernel-cli-present", harness_has_cli, "source_higgs_time_kernel_v1 CLI and output path")
    report("time-kernel-support-loaded", time_kernel_support_loaded, parent_statuses["time_kernel_gevp_contract"])
    report("canonical-oh-or-physical-identity-absent", canonical_oh_absent, parent_statuses["canonical_oh_hard_residual"])
    report("current-operator-is-not-canonical-oh", action_is_taste_radial_not_oh, status(action))
    report("commands-have-no-resume", no_resume, f"commands={len(commands)}")
    report("commands-use-distinct-outputs", outputs_distinct, rel(CHUNK_OUTPUT_ROOT))
    report("commands-use-distinct-production-dirs", dirs_distinct, rel(PRODUCTION_OUTPUT_ROOT))
    report("commands-avoid-static-row-paths", not static_output_collision, "time-kernel paths do not overlap active static row paths")
    report("seed-range-disjoint", seed_range_disjoint_from_static_and_higher_shell, f"{chunk_seed(1)}..{chunk_seed(CHUNK_COUNT)}")
    report("commands-enable-time-kernel", all_commands_enable_time_kernel, f"modes={MOMENTUM_MODES} max_tau={TIME_KERNEL_MAX_TAU}")
    report("no-time-kernel-workers-active", not active_time_kernel_chunks, f"active={active_time_kernel_chunks}")
    report(
        "active-static-worker-state-recorded",
        True,
        f"active={[(r.get('chunk_index'), r.get('pid')) for r in active_static_chunks]}",
    )
    report("closure-launch-not-authorized", not closure_launch_authorized_now, "manifest is not O_H/closure evidence")
    report("support-launch-not-authorized-now", not support_launch_authorized_now, "; ".join(launch_blockers))

    result = {
        "actual_current_surface_status": (
            "bounded-support / source-Higgs time-kernel production manifest; "
            "canonical O_H or physical neutral identity absent and no rows launched"
        ),
        "conditional_surface_status": (
            "conditional-support after a same-surface canonical O_H certificate "
            "or physical neutral/WZ identity lands; production C_ss/C_sH/C_HH(t) "
            "rows, OS/GEVP pole extraction, FV/IR/threshold control, and "
            "source-overlap normalization would still be required"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This runner writes a production manifest and collision/metadata "
            "firewall only.  The current operator certificate is taste-radial, "
            "not canonical O_H; active static row workers are already running; "
            "and no production time-kernel rows, pole extraction, FV/IR, "
            "threshold, covariance, or source-overlap authority exists."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "artifact": "yt_pr230_source_higgs_time_kernel_production_manifest",
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "operator_certificate": rel(ACTION_CERT),
        "operator_certificate_is_canonical_oh": False,
        "time_kernel_schema_version": "source_higgs_time_kernel_v1",
        "chunk_count": CHUNK_COUNT,
        "recommended_max_concurrent": MAX_CONCURRENT_RECOMMENDED,
        "closure_launch_authorized_now": closure_launch_authorized_now,
        "support_launch_authorized_now": support_launch_authorized_now,
        "launch_blockers": launch_blockers,
        "active_process_rows": active_rows,
        "chunk_commands": chunks,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not launch or count time-kernel rows as evidence",
            "does not identify taste-radial x with canonical O_H",
            "does not relabel C_sx/C_xx(t) as canonical C_sH/C_HH(t)",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette/u0, or value recognition as proof authority",
        ],
        "exact_next_action": (
            "Wait for the active static taste-radial chunks to finish and be packaged.  "
            "For this manifest to become closure-relevant, first supply a same-surface "
            "canonical O_H certificate or physical neutral/WZ identity; then launch "
            "time-kernel chunks on the non-colliding paths, run OS/GEVP pole extraction, "
            "FV/IR/threshold and source-overlap gates, full assembly, retained-route, "
            "campaign, and completion-audit runners."
        ),
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
