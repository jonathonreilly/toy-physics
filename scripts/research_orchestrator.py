#!/usr/bin/env python3
"""Persistent cycle/batch orchestrator for bounded research search loops.

This helper keeps a reusable JSON state file for campaigns that need to:
- run with a fixed cycle budget
- keep a fixed number of active lanes full
- replace completed lanes with new pending lanes
- preserve diagnosed closures and retained wins as first-class state

The script is intentionally generic so the repo can reuse it for different
science-search programs, not just the current Physics batch.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
from typing import Any


DEFAULT_STATE_PATH = (
    "/Users/jonreilly/.codex/state/physics_research_orchestrator_state.json"
)
ALLOWED_LANE_STATUSES = {
    "pending",
    "active",
    "retained",
    "closure",
    "paused",
    "dropped",
}
ALLOWED_CAMPAIGN_STATUSES = {"active", "stopped"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_parent(path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return int(payload.get("exit_code", 0))


def dump_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    ensure_parent(path)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp_path, path)


def load_state(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"state file does not exist: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def default_state(
    campaign_name: str,
    max_cycles: int,
    slot_count: int,
    guardrails: list[str],
) -> dict[str, Any]:
    now = utc_now()
    return {
        "version": 1,
        "campaign": {
            "name": campaign_name,
            "status": "active",
            "max_cycles": max_cycles,
            "slot_count": slot_count,
            "created_at": now,
            "updated_at": now,
            "guardrails": guardrails,
        },
        "cycle": {
            "count": 0,
            "last_opened_at": None,
            "last_closed_at": None,
            "last_owner": None,
        },
        "lanes": [],
        "history": [],
    }


def touch_updated_at(state: dict[str, Any]) -> None:
    state["campaign"]["updated_at"] = utc_now()


def require_campaign_active(state: dict[str, Any]) -> None:
    if state["campaign"]["status"] != "active":
        raise ValueError("campaign is stopped")


def require_budget(state: dict[str, Any]) -> None:
    if state["cycle"]["count"] >= state["campaign"]["max_cycles"]:
        raise ValueError("cycle budget exhausted")


def lane_sort_key(lane: dict[str, Any]) -> tuple[Any, ...]:
    return (
        int(lane.get("priority", 100)),
        lane.get("created_at") or "",
        lane.get("id") or "",
    )


def lane_by_id(state: dict[str, Any], lane_id: str) -> dict[str, Any]:
    for lane in state["lanes"]:
        if lane["id"] == lane_id:
            return lane
    raise KeyError(f"unknown lane id: {lane_id}")


def append_lane_event(lane: dict[str, Any], event: str, payload: dict[str, Any]) -> None:
    lane.setdefault("history", []).append(
        {
            "event": event,
            "at": utc_now(),
            **payload,
        }
    )


def summarize_state(state: dict[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {status: 0 for status in ALLOWED_LANE_STATUSES}
    for lane in state["lanes"]:
        counts[lane["status"]] = counts.get(lane["status"], 0) + 1

    active = sorted(
        [lane for lane in state["lanes"] if lane["status"] == "active"],
        key=lane_sort_key,
    )
    pending = sorted(
        [lane for lane in state["lanes"] if lane["status"] == "pending"],
        key=lane_sort_key,
    )
    recent = state["history"][-3:]
    return {
        "campaign": state["campaign"],
        "cycle": state["cycle"],
        "remaining_cycles": max(
            0, state["campaign"]["max_cycles"] - state["cycle"]["count"]
        ),
        "lane_counts": counts,
        "active_lanes": [
            {
                "id": lane["id"],
                "title": lane["title"],
                "priority": lane["priority"],
                "category": lane.get("category"),
                "owner": lane.get("owner"),
                "opened_in_cycle": lane.get("opened_in_cycle"),
            }
            for lane in active
        ],
        "next_pending": [
            {
                "id": lane["id"],
                "title": lane["title"],
                "priority": lane["priority"],
                "category": lane.get("category"),
            }
            for lane in pending[: state["campaign"]["slot_count"]]
        ],
        "recent_history": recent,
    }


def preview_batch(state: dict[str, Any], count: int | None = None) -> list[dict[str, Any]]:
    requested = count or state["campaign"]["slot_count"]
    active = sorted(
        [lane for lane in state["lanes"] if lane["status"] == "active"],
        key=lane_sort_key,
    )
    pending = sorted(
        [lane for lane in state["lanes"] if lane["status"] == "pending"],
        key=lane_sort_key,
    )
    selected = active[:requested]
    remaining = max(0, requested - len(selected))
    if remaining:
        selected.extend(pending[:remaining])
    return selected


def init_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    if path.exists() and not args.reset:
        return emit(
            {
                "exit_code": 2,
                "path": str(path),
                "reason": "state file already exists; pass --reset to overwrite",
                "status": "error",
            }
        )
    state = default_state(
        campaign_name=args.name,
        max_cycles=args.max_cycles,
        slot_count=args.slot_count,
        guardrails=args.guardrail or [],
    )
    dump_json(path, state)
    return emit(
        {
            "campaign": state["campaign"],
            "exit_code": 0,
            "path": str(path),
            "status": "initialized",
        }
    )


def add_lane_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    if any(lane["id"] == args.lane_id for lane in state["lanes"]):
        return emit(
            {
                "exit_code": 2,
                "lane_id": args.lane_id,
                "reason": "lane id already exists",
                "status": "error",
            }
        )
    now = utc_now()
    lane = {
        "id": args.lane_id,
        "title": args.title,
        "category": args.category,
        "priority": args.priority,
        "status": "pending",
        "prompt": args.prompt,
        "success_gate": args.success_gate,
        "guardrails": args.guardrail or [],
        "summary": "",
        "diagnosis": "",
        "artifacts": [],
        "owner": None,
        "opened_in_cycle": None,
        "created_at": now,
        "updated_at": now,
        "history": [],
    }
    append_lane_event(lane, "created", {"status": "pending"})
    state["lanes"].append(lane)
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "exit_code": 0,
            "lane": lane,
            "path": str(path),
            "status": "added",
        }
    )


def add_guardrail_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    existing = state["campaign"].setdefault("guardrails", [])
    for entry in args.guardrail:
        if entry not in existing:
            existing.append(entry)
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "exit_code": 0,
            "guardrails": existing,
            "path": str(path),
            "status": "updated",
        }
    )


def status_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    return emit(
        {
            "exit_code": 0,
            "path": str(path),
            "status": "ok",
            "summary": summarize_state(state),
        }
    )


def preview_batch_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    lanes = preview_batch(state, args.count)
    return emit(
        {
            "exit_code": 0,
            "path": str(path),
            "selected": lanes,
            "status": "ok",
        }
    )


def open_cycle_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    try:
        require_campaign_active(state)
        require_budget(state)
    except ValueError as exc:
        return emit(
            {
                "exit_code": 2,
                "path": str(path),
                "reason": str(exc),
                "status": "stop",
                "summary": summarize_state(state),
            }
        )

    cycle_index = state["cycle"]["count"] + 1
    selected = preview_batch(state, args.count)
    if not selected:
        return emit(
            {
                "exit_code": 2,
                "path": str(path),
                "reason": "no active or pending lanes available",
                "status": "idle",
                "summary": summarize_state(state),
            }
        )

    newly_activated: list[str] = []
    for lane in selected:
        if lane["status"] == "pending":
            lane["status"] = "active"
            lane["owner"] = args.owner
            lane["opened_in_cycle"] = cycle_index
            lane["updated_at"] = utc_now()
            append_lane_event(
                lane,
                "activated",
                {"owner": args.owner, "cycle": cycle_index, "status": "active"},
            )
            newly_activated.append(lane["id"])

    state["cycle"]["count"] = cycle_index
    state["cycle"]["last_opened_at"] = utc_now()
    state["cycle"]["last_owner"] = args.owner
    state["history"].append(
        {
            "cycle": cycle_index,
            "opened_at": state["cycle"]["last_opened_at"],
            "owner": args.owner,
            "selected_lane_ids": [lane["id"] for lane in selected],
            "newly_activated_lane_ids": newly_activated,
            "closed_at": None,
            "summary": "",
        }
    )
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "cycle": cycle_index,
            "exit_code": 0,
            "newly_activated_lane_ids": newly_activated,
            "path": str(path),
            "selected": selected,
            "status": "opened",
        }
    )


def update_lane_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    try:
        lane = lane_by_id(state, args.lane_id)
    except KeyError as exc:
        return emit(
            {
                "exit_code": 2,
                "path": str(path),
                "reason": str(exc),
                "status": "error",
            }
        )

    event_payload: dict[str, Any] = {}
    if args.status:
        lane["status"] = args.status
        event_payload["status"] = args.status
        if args.status != "active":
            lane["owner"] = None
    if args.owner is not None:
        lane["owner"] = args.owner or None
        event_payload["owner"] = lane["owner"]
    if args.priority is not None:
        lane["priority"] = args.priority
        event_payload["priority"] = args.priority
    if args.summary is not None:
        lane["summary"] = args.summary
        event_payload["summary"] = args.summary
    if args.diagnosis is not None:
        lane["diagnosis"] = args.diagnosis
        event_payload["diagnosis"] = args.diagnosis
    if args.artifact:
        for artifact in args.artifact:
            if artifact not in lane["artifacts"]:
                lane["artifacts"].append(artifact)
        event_payload["artifacts_added"] = args.artifact
    lane["updated_at"] = utc_now()
    append_lane_event(lane, "updated", event_payload)
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "exit_code": 0,
            "lane": lane,
            "path": str(path),
            "status": "updated",
        }
    )


def close_cycle_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    if not state["history"]:
        return emit(
            {
                "exit_code": 2,
                "path": str(path),
                "reason": "no cycle has been opened yet",
                "status": "error",
            }
        )
    latest = state["history"][-1]
    latest["closed_at"] = utc_now()
    latest["summary"] = args.summary or ""
    state["cycle"]["last_closed_at"] = latest["closed_at"]
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "cycle": latest["cycle"],
            "exit_code": 0,
            "path": str(path),
            "status": "closed",
            "summary": latest,
        }
    )


def set_campaign_status_command(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.state_path)
    state = load_state(path)
    state["campaign"]["status"] = args.status
    touch_updated_at(state)
    dump_json(path, state)
    return emit(
        {
            "campaign_status": args.status,
            "exit_code": 0,
            "path": str(path),
            "status": "updated",
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-path", default=DEFAULT_STATE_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize a new campaign state file")
    init.add_argument("--name", required=True)
    init.add_argument("--max-cycles", type=int, default=100)
    init.add_argument("--slot-count", type=int, default=5)
    init.add_argument("--guardrail", action="append")
    init.add_argument("--reset", action="store_true")
    init.set_defaults(func=init_command)

    add_lane = subparsers.add_parser("add-lane", help="add a pending lane")
    add_lane.add_argument("--lane-id", required=True)
    add_lane.add_argument("--title", required=True)
    add_lane.add_argument("--category", default="")
    add_lane.add_argument("--priority", type=int, default=100)
    add_lane.add_argument("--prompt", default="")
    add_lane.add_argument("--success-gate", default="")
    add_lane.add_argument("--guardrail", action="append")
    add_lane.set_defaults(func=add_lane_command)

    add_guardrail = subparsers.add_parser(
        "add-guardrail", help="append campaign-level guardrails"
    )
    add_guardrail.add_argument("--guardrail", action="append", required=True)
    add_guardrail.set_defaults(func=add_guardrail_command)

    status = subparsers.add_parser("status", help="summarize current campaign state")
    status.set_defaults(func=status_command)

    preview = subparsers.add_parser(
        "preview-batch", help="preview the next batch without mutating state"
    )
    preview.add_argument("--count", type=int)
    preview.set_defaults(func=preview_batch_command)

    open_cycle = subparsers.add_parser(
        "open-cycle",
        help="increment the cycle counter and activate enough lanes to fill the batch",
    )
    open_cycle.add_argument("--owner", required=True)
    open_cycle.add_argument("--count", type=int)
    open_cycle.set_defaults(func=open_cycle_command)

    update_lane = subparsers.add_parser(
        "update-lane", help="update lane status, notes, or artifact list"
    )
    update_lane.add_argument("--lane-id", required=True)
    update_lane.add_argument("--status", choices=sorted(ALLOWED_LANE_STATUSES))
    update_lane.add_argument("--owner")
    update_lane.add_argument("--priority", type=int)
    update_lane.add_argument("--summary")
    update_lane.add_argument("--diagnosis")
    update_lane.add_argument("--artifact", action="append")
    update_lane.set_defaults(func=update_lane_command)

    close_cycle = subparsers.add_parser(
        "close-cycle", help="close the most recently opened cycle"
    )
    close_cycle.add_argument("--summary", default="")
    close_cycle.set_defaults(func=close_cycle_command)

    set_status = subparsers.add_parser(
        "set-status", help="set the campaign status to active or stopped"
    )
    set_status.add_argument("--status", choices=sorted(ALLOWED_CAMPAIGN_STATUSES), required=True)
    set_status.set_defaults(func=set_campaign_status_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        return emit({"exit_code": 2, "reason": str(exc), "status": "error"})
    except Exception as exc:  # pragma: no cover - defensive CLI path
        return emit({"exit_code": 1, "reason": str(exc), "status": "error"})


if __name__ == "__main__":
    raise SystemExit(main())
