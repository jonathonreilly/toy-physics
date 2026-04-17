#!/usr/bin/env python3
"""Cooperative repo lock for manual work and automations.

This script coordinates background workers so long-running science steps do not
overlap with each other or with a manual Codex session.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import pathlib
import sys
from typing import Any


DEFAULT_LOCK_PATH = "/Users/jonreilly/Projects/Physics/logs/physics_worker_lock.json"
DEFAULT_META_LOCK_PATH = "/Users/jonreilly/Projects/Physics/logs/.physics_worker_lock.guard"
DEFAULT_HOLDER_ENV = "CODEX_THREAD_ID"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_iso8601(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def dump_json(path: str, payload: dict[str, Any]) -> None:
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp_path, path)


def load_lock(path: str) -> dict[str, Any] | None:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def lock_is_live(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False
    expires_at = parse_iso8601(payload.get("expires_at"))
    if not expires_at:
        return False
    return expires_at > utc_now()


def resolve_holder_id(explicit_holder_id: str | None) -> str | None:
    if explicit_holder_id:
        return explicit_holder_id
    return os.environ.get(DEFAULT_HOLDER_ENV)


def build_payload(
    owner: str,
    purpose: str,
    ttl_hours: float,
    holder_id: str | None,
) -> dict[str, Any]:
    now = utc_now()
    expires_at = now + dt.timedelta(hours=ttl_hours)
    payload = {
        "owner": owner,
        "purpose": purpose,
        "pid": os.getpid(),
        "started_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    if holder_id:
        payload["holder_id"] = holder_id
    return payload


def holder_matches(payload: dict[str, Any] | None, owner: str, holder_id: str | None) -> bool:
    if not payload or payload.get("owner") != owner:
        return False

    payload_holder_id = payload.get("holder_id")
    if payload_holder_id or holder_id:
        return payload_holder_id == holder_id
    return True


def print_payload(status: str, payload: dict[str, Any] | None) -> None:
    result = {"status": status, "lock": payload}
    print(json.dumps(result, indent=2, sort_keys=True))


def run_with_guard(args: argparse.Namespace) -> int:
    pathlib.Path(os.path.dirname(args.meta_lock_path)).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.dirname(args.lock_path)).mkdir(parents=True, exist_ok=True)
    with open(args.meta_lock_path, "a+", encoding="utf-8") as guard:
        fcntl.flock(guard.fileno(), fcntl.LOCK_EX)
        return dispatch_locked(args)


def dispatch_locked(args: argparse.Namespace) -> int:
    payload = load_lock(args.lock_path)
    live = lock_is_live(payload)
    holder_id = resolve_holder_id(getattr(args, "holder_id", None))

    if args.command == "status":
        print_payload("held" if live else "free", payload if live else None)
        return 0

    if args.command == "acquire":
        if live and payload and not holder_matches(payload, args.owner, holder_id):
            print_payload("held", payload)
            return 2
        new_payload = build_payload(args.owner, args.purpose, args.ttl_hours, holder_id)
        dump_json(args.lock_path, new_payload)
        print_payload("acquired", new_payload)
        return 0

    if args.command == "refresh":
        if not live or not holder_matches(payload, args.owner, holder_id):
            print_payload("not-owned", payload if live else None)
            return 2
        refreshed = build_payload(
            args.owner,
            payload.get("purpose", args.purpose),
            args.ttl_hours,
            holder_id,
        )
        dump_json(args.lock_path, refreshed)
        print_payload("refreshed", refreshed)
        return 0

    if args.command == "release":
        if not payload:
            print_payload("free", None)
            return 0
        if not holder_matches(payload, args.owner, holder_id):
            print_payload("not-owned", payload)
            return 2
        os.remove(args.lock_path)
        print_payload("released", None)
        return 0

    raise ValueError(f"unknown command {args.command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cooperative worker lock")
    parser.add_argument("--lock-path", default=DEFAULT_LOCK_PATH)
    parser.add_argument("--meta-lock-path", default=DEFAULT_META_LOCK_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status")
    status.set_defaults(command="status")

    for name in ("acquire", "refresh"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--owner", required=True)
        sub.add_argument("--purpose", default="")
        sub.add_argument("--ttl-hours", type=float, required=True)
        sub.add_argument("--holder-id")
        sub.set_defaults(command=name)

    release = subparsers.add_parser("release")
    release.add_argument("--owner", required=True)
    release.add_argument("--holder-id")
    release.set_defaults(command="release")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run_with_guard(args)
    except Exception as exc:  # pragma: no cover - defensive CLI path
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
