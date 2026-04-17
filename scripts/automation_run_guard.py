#!/usr/bin/env python3
"""Detect duplicate unresolved automation runs before shared-state work begins."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
from typing import Any


DEFAULT_DB_PATH = "/Users/jonreilly/.codex/sqlite/codex-dev.db"
DEFAULT_THREAD_ENV = "CODEX_THREAD_ID"


def current_thread_id(explicit_thread_id: str | None) -> str | None:
    if explicit_thread_id:
        return explicit_thread_id
    return os.environ.get(DEFAULT_THREAD_ENV)


def format_local_time(milliseconds: int) -> str:
    timestamp = dt.datetime.fromtimestamp(milliseconds / 1000, tz=dt.timezone.utc)
    return timestamp.astimezone().isoformat()


def fetch_in_progress_runs(db_path: str, automation_id: str) -> list[dict[str, Any]]:
    query = """
        SELECT thread_id, status, read_at, inbox_title, created_at, updated_at
        FROM automation_runs
        WHERE automation_id = ? AND status = 'IN_PROGRESS'
        ORDER BY created_at ASC, thread_id ASC
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, (automation_id,)).fetchall()
    return [dict(row) for row in rows]


def summarize_run(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "thread_id": row["thread_id"],
        "created_at": format_local_time(row["created_at"]),
        "updated_at": format_local_time(row["updated_at"]),
        "inbox_title": row.get("inbox_title"),
        "read_at": format_local_time(row["read_at"]) if row.get("read_at") else None,
    }


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return int(payload["exit_code"])


def preflight(args: argparse.Namespace) -> int:
    thread_id = current_thread_id(args.thread_id)
    if not thread_id:
        return emit(
            {
                "automation_id": args.automation_id,
                "current_thread_id": None,
                "exit_code": 3,
                "reason": f"missing current thread id; set {DEFAULT_THREAD_ENV} or pass --thread-id",
                "status": "error",
            }
        )

    rows = fetch_in_progress_runs(args.db_path, args.automation_id)
    runs = [summarize_run(row) for row in rows]
    latest = runs[-1] if runs else None
    current = next((run for run in runs if run["thread_id"] == thread_id), None)

    if not current:
        return emit(
            {
                "automation_id": args.automation_id,
                "current_thread_id": thread_id,
                "eligible_thread_id": latest["thread_id"] if latest else None,
                "exit_code": 3,
                "in_progress": runs,
                "in_progress_count": len(runs),
                "reason": "current thread is not present in automation_runs",
                "status": "error",
            }
        )

    if latest and latest["thread_id"] != thread_id:
        return emit(
            {
                "automation_id": args.automation_id,
                "current_thread_id": thread_id,
                "current_thread": current,
                "eligible_thread_id": latest["thread_id"],
                "exit_code": 2,
                "in_progress": runs,
                "in_progress_count": len(runs),
                "policy": "newest_in_progress_wins",
                "reason": "a newer unresolved run already exists for this automation",
                "status": "skip",
            }
        )

    return emit(
        {
            "automation_id": args.automation_id,
            "current_thread_id": thread_id,
            "current_thread": current,
            "eligible_thread_id": thread_id,
            "exit_code": 0,
            "in_progress": runs,
            "in_progress_count": len(runs),
            "policy": "newest_in_progress_wins",
            "reason": "current thread is the newest unresolved run",
            "status": "proceed",
        }
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guard against duplicate automation runs")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--automation-id", required=True)
    preflight_parser.add_argument("--thread-id")
    preflight_parser.set_defaults(command="preflight")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "preflight":
        return preflight(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
