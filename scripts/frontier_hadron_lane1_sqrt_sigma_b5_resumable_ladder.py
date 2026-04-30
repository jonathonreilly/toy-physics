#!/usr/bin/env python3
"""Resumable B5 Wilson/Creutz ladder runner for Lane 1 sqrt(sigma).

Cycle 6 of the hadron sqrt(sigma) loop.  The default smoke profile is
intentionally tiny and only validates checkpoint / JSONL plumbing.  The
production profile targets the first B5-closing compute class identified
by Cycle 4: L=8,12,16.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Any

import numpy as np

from frontier_hadron_lane1_sqrt_sigma_b5_lowstat_scout import (
    BETA,
    make_lattice,
    measure_plaquette,
    measure_wilson_average,
    metropolis_sweep,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSONL = ROOT / "outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_2026-04-30.jsonl"
DEFAULT_CHECKPOINT_DIR = ROOT / "outputs/frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder_checkpoints"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def state_cycle_at_least(state: str, cycle: int) -> bool:
    match = re.search(r"cycles_completed:\s*(\d+)", state)
    return bool(match) and int(match.group(1)) >= cycle


@dataclass(frozen=True)
class RunnerConfig:
    profile: str
    volumes: tuple[int, ...]
    therm_sweeps: int
    measurements: int
    skip_sweeps: int
    max_seconds: float
    seed: int
    jsonl_path: Path
    checkpoint_dir: Path
    fresh: bool


@dataclass(frozen=True)
class VolumeSummary:
    L: int
    sweeps_completed: int
    measurements_completed: int
    accepted: int
    proposals: int
    checkpoint_path: Path
    status: str


def profile_defaults(profile: str) -> dict[str, Any]:
    profiles = {
        "smoke": {
            "volumes": (4,),
            "therm_sweeps": 1,
            "measurements": 1,
            "skip_sweeps": 1,
            "max_seconds": 30.0,
        },
        "scout": {
            "volumes": (4, 6, 8),
            "therm_sweeps": 6,
            "measurements": 4,
            "skip_sweeps": 1,
            "max_seconds": 240.0,
        },
        "production": {
            "volumes": (8, 12, 16),
            "therm_sweeps": 200,
            "measurements": 1000,
            "skip_sweeps": 10,
            "max_seconds": 3600.0,
        },
    }
    return profiles[profile]


def parse_volumes(text: str) -> tuple[int, ...]:
    values = tuple(int(item.strip()) for item in text.split(",") if item.strip())
    if not values or any(value < 4 for value in values):
        raise argparse.ArgumentTypeError("volumes must be comma-separated integers >= 4")
    return values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("smoke", "scout", "production"), default="smoke")
    parser.add_argument("--volumes", type=parse_volumes)
    parser.add_argument("--therm-sweeps", type=int)
    parser.add_argument("--measurements", type=int)
    parser.add_argument("--skip-sweeps", type=int)
    parser.add_argument("--max-seconds", type=float)
    parser.add_argument("--seed", type=int, default=20260430)
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--checkpoint-dir", type=Path, default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--fresh", action="store_true", help="remove this runner's output/checkpoints before running")
    return parser


def resolve_config(args: argparse.Namespace) -> RunnerConfig:
    defaults = profile_defaults(args.profile)
    return RunnerConfig(
        profile=args.profile,
        volumes=args.volumes or defaults["volumes"],
        therm_sweeps=args.therm_sweeps if args.therm_sweeps is not None else defaults["therm_sweeps"],
        measurements=args.measurements if args.measurements is not None else defaults["measurements"],
        skip_sweeps=args.skip_sweeps if args.skip_sweeps is not None else defaults["skip_sweeps"],
        max_seconds=args.max_seconds if args.max_seconds is not None else defaults["max_seconds"],
        seed=args.seed,
        jsonl_path=args.jsonl,
        checkpoint_dir=args.checkpoint_dir,
        fresh=args.fresh,
    )


def links_to_array(links: dict[tuple[int, ...], list[np.ndarray]], L: int) -> np.ndarray:
    arr = np.empty((L, L, L, L, 4, 3, 3), dtype=np.complex128)
    for coords in np.ndindex(*([L] * 4)):
        arr[coords] = np.stack(links[coords])
    return arr


def array_to_links(arr: np.ndarray) -> dict[tuple[int, ...], list[np.ndarray]]:
    L = arr.shape[0]
    links: dict[tuple[int, ...], list[np.ndarray]] = {}
    for coords in np.ndindex(*([L] * 4)):
        links[coords] = [arr[coords][mu].copy() for mu in range(4)]
    return links


def checkpoint_path(checkpoint_dir: Path, L: int) -> Path:
    return checkpoint_dir / f"state_L{L}.npz"


def load_or_initialize_state(
    L: int, seed: int, checkpoint_dir: Path
) -> tuple[dict[tuple[int, ...], list[np.ndarray]], np.random.Generator, int, int, int, int]:
    path = checkpoint_path(checkpoint_dir, L)
    if not path.exists():
        return make_lattice(L), np.random.default_rng(seed + L), 0, 0, 0, 0

    data = np.load(path, allow_pickle=False)
    links = array_to_links(data["links"])
    rng = np.random.default_rng()
    rng.bit_generator.state = json.loads(str(data["rng_state"].item()))
    return (
        links,
        rng,
        int(data["sweeps_completed"]),
        int(data["measurements_completed"]),
        int(data["accepted"]),
        int(data["proposals"]),
    )


def save_state(
    L: int,
    checkpoint_dir: Path,
    links: dict[tuple[int, ...], list[np.ndarray]],
    rng: np.random.Generator,
    sweeps_completed: int,
    measurements_completed: int,
    accepted: int,
    proposals: int,
) -> Path:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    path = checkpoint_path(checkpoint_dir, L)
    np.savez(
        path,
        links=links_to_array(links, L),
        rng_state=np.array(json.dumps(rng.bit_generator.state)),
        sweeps_completed=np.array(sweeps_completed, dtype=np.int64),
        measurements_completed=np.array(measurements_completed, dtype=np.int64),
        accepted=np.array(accepted, dtype=np.int64),
        proposals=np.array(proposals, dtype=np.int64),
    )
    return path


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, allow_nan=False))
        handle.write("\n")


def measurement_record(
    config: RunnerConfig,
    L: int,
    sweeps_completed: int,
    measurements_completed: int,
    accepted: int,
    proposals: int,
    links: dict[tuple[int, ...], list[np.ndarray]],
) -> dict[str, Any]:
    stride = max(1, L // 4)
    plaquette = float(measure_plaquette(links, L))
    w11 = float(measure_wilson_average(links, L, 1, 1, stride))
    w12 = float(measure_wilson_average(links, L, 1, 2, stride))
    w22 = float(measure_wilson_average(links, L, 2, 2, stride))
    chi22 = None
    if w11 > 1e-12 and w12 > 1e-12 and w22 > 1e-12:
        chi22 = float(-math.log(abs(w22 * w11) / abs(w12 * w12)))

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "profile": config.profile,
        "beta": BETA,
        "L": L,
        "stride": stride,
        "seed": config.seed,
        "sweeps_completed": sweeps_completed,
        "measurement_index": measurements_completed,
        "therm_sweeps_target": config.therm_sweeps,
        "measurements_target": config.measurements,
        "skip_sweeps": config.skip_sweeps,
        "plaquette": plaquette,
        "W11": w11,
        "W12": w12,
        "W22": w22,
        "chi22": chi22,
        "acceptance": accepted / proposals if proposals else None,
    }


def run_volume(config: RunnerConfig, L: int, deadline: float) -> VolumeSummary:
    links, rng, sweeps_completed, measurements_completed, accepted, proposals = load_or_initialize_state(
        L, config.seed, config.checkpoint_dir
    )
    status = "complete"

    while sweeps_completed < config.therm_sweeps and time.monotonic() < deadline:
        a, t = metropolis_sweep(links, L, rng)
        accepted += a
        proposals += t
        sweeps_completed += 1
        save_state(L, config.checkpoint_dir, links, rng, sweeps_completed, measurements_completed, accepted, proposals)

    while measurements_completed < config.measurements and time.monotonic() < deadline:
        for _ in range(config.skip_sweeps):
            if time.monotonic() >= deadline:
                break
            a, t = metropolis_sweep(links, L, rng)
            accepted += a
            proposals += t
            sweeps_completed += 1

        if time.monotonic() >= deadline:
            status = "checkpointed"
            break

        record = measurement_record(
            config, L, sweeps_completed, measurements_completed, accepted, proposals, links
        )
        append_jsonl(config.jsonl_path, record)
        measurements_completed += 1
        save_state(L, config.checkpoint_dir, links, rng, sweeps_completed, measurements_completed, accepted, proposals)

    if measurements_completed < config.measurements:
        status = "checkpointed"
        save_state(L, config.checkpoint_dir, links, rng, sweeps_completed, measurements_completed, accepted, proposals)

    return VolumeSummary(
        L=L,
        sweeps_completed=sweeps_completed,
        measurements_completed=measurements_completed,
        accepted=accepted,
        proposals=proposals,
        checkpoint_path=checkpoint_path(config.checkpoint_dir, L),
        status=status,
    )


def reset_outputs(config: RunnerConfig) -> None:
    if config.jsonl_path.exists():
        config.jsonl_path.unlink()
    if config.checkpoint_dir.exists():
        shutil.rmtree(config.checkpoint_dir)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_ladder(config: RunnerConfig) -> list[VolumeSummary]:
    if config.fresh:
        reset_outputs(config)

    deadline = time.monotonic() + config.max_seconds
    summaries: list[VolumeSummary] = []
    for L in config.volumes:
        if time.monotonic() >= deadline:
            break
        summary = run_volume(config, L, deadline)
        summaries.append(summary)
        print(
            f"  L={summary.L}: sweeps={summary.sweeps_completed}, "
            f"measurements={summary.measurements_completed}/{config.measurements}, "
            f"acc={summary.accepted / summary.proposals if summary.proposals else 0.0:.3f}, "
            f"status={summary.status}"
        )
    return summaries


def part1_config_checks(config: RunnerConfig) -> None:
    section("Part 1: runner configuration checks")
    production = profile_defaults("production")
    print(f"  profile={config.profile}")
    print(f"  volumes={','.join(str(v) for v in config.volumes)}")
    print(f"  therm={config.therm_sweeps}, measurements={config.measurements}, skip={config.skip_sweeps}")
    print(f"  max_seconds={config.max_seconds}")

    check(
        "production profile targets the first B5-closing volume class",
        production["volumes"] == (8, 12, 16),
    )
    check(
        "runner has wall-clock and checkpoint controls",
        config.max_seconds > 0 and str(config.checkpoint_dir) and str(config.jsonl_path),
    )
    check(
        "smoke profile stays below B5 closure scale",
        profile_defaults("smoke")["volumes"] == (4,),
    )


def part2_run_and_checkpoint(config: RunnerConfig) -> None:
    section("Part 2: resumable ladder smoke run")
    summaries = run_ladder(config)
    records = read_jsonl(config.jsonl_path)
    required = {
        "timestamp_utc",
        "profile",
        "beta",
        "L",
        "sweeps_completed",
        "measurement_index",
        "plaquette",
        "W11",
        "W12",
        "W22",
        "chi22",
        "acceptance",
    }

    check("runner produced at least one JSONL measurement", len(records) >= 1)
    check("JSONL measurement schema is complete", bool(records) and required.issubset(records[-1]))
    check(
        "latest measurement has finite primary observables",
        bool(records)
        and all(math.isfinite(float(records[-1][key])) for key in ["plaquette", "W11", "W12", "W22", "acceptance"]),
    )
    check(
        "state checkpoint was written for each started volume",
        bool(summaries) and all(summary.checkpoint_path.exists() for summary in summaries),
    )
    reloaded = False
    if summaries:
        last = summaries[-1]
        _, _, sweeps, measurements, accepted, proposals = load_or_initialize_state(
            last.L, config.seed, config.checkpoint_dir
        )
        reloaded = (
            sweeps == last.sweeps_completed
            and measurements == last.measurements_completed
            and accepted == last.accepted
            and proposals == last.proposals
        )
    check("checkpoint can be reloaded for resume", reloaded)
    checkpointable_progress = bool(summaries) and all(
        summary.measurements_completed >= 1
        or summary.sweeps_completed >= config.therm_sweeps
        or (summary.status == "checkpointed" and summary.sweeps_completed >= 1)
        for summary in summaries
    )
    measurement_progress = any(summary.measurements_completed >= 1 for summary in summaries)
    thermalization_progress = any(
        summary.status == "checkpointed" and summary.sweeps_completed >= 1 for summary in summaries
    )
    check(
        "resume counters advanced",
        checkpointable_progress and (measurement_progress or thermalization_progress),
    )


def part3_artifact_checks() -> None:
    section("Part 3: artifact checks")
    note = read("docs/HADRON_LANE1_SQRT_SIGMA_B5_RESUMABLE_LADDER_NOTE_2026-04-30.md")
    handoff = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/HANDOFF.md")
    certificate = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/CLAIM_STATUS_CERTIFICATE.md")
    state = read(".claude/science/physics-loops/hadron-sqrt-sigma-b2-20260430/STATE.yaml")

    check(
        "note labels the runner as append-only/resumable but not B5 closure",
        "append-only JSONL" in note and "wall-clock stop/resume" in note and "not B5 closure" in note,
    )
    check(
        "branch-local handoff includes the resumable ladder runner",
        "HADRON_LANE1_SQRT_SIGMA_B5_RESUMABLE_LADDER_NOTE_2026-04-30.md" in handoff
        and "frontier_hadron_lane1_sqrt_sigma_b5_resumable_ladder.py" in handoff,
    )
    check(
        "claim-status certificate keeps B5 open rather than retained",
        "actual_current_surface_status: bounded-support" in certificate
        and "bare_retained_allowed: false" in certificate,
    )
    check(
        "loop state advanced to cycle 6",
        state_cycle_at_least(state, 6) and "cycle-6-complete" in state,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = resolve_config(args)

    print("=" * 88)
    print("LANE 1 SQRT(SIGMA) B5 RESUMABLE WILSON/CREUTZ LADDER")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is there now a resumable compute path for the B5 production ladder?")
    print()
    print("Answer:")
    print("  Yes as executable infrastructure; no as B5 closure until production")
    print("  L=8,12,16 statistics and uncertainties are actually accumulated.")

    part1_config_checks(config)
    part2_run_and_checkpoint(config)
    part3_artifact_checks()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
