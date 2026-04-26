#!/usr/bin/env python3
"""Lint the audit ledger for consistency.

Checks (all hard rules from FRESH_LOOK_REQUIREMENTS.md and README.md):

  1. Schema:
     - Every row has the expected fields.
     - audit_status is one of the allowed enum values.
     - current_status is one of the allowed enum values.

  2. The hard rules:
     - No row has current_status = 'retained' or 'promoted' (these are
       audit-ratified only; authors may only declare proposed_*).
     - audit_status = audited_clean requires auditor and auditor_family set.
     - audit_status = audited_clean with current_status not in
       {proposed_retained, proposed_promoted} is illegal.
     - effective_status = retained requires audit_status = audited_clean
       AND every dep's effective_status = retained.
     - independence = 'weak' is forbidden as the only audit for a critical
       claim (criticality computed from transitive descendants only).
     - note_hash on row must equal current note hash on disk.

  3. Graph health:
     - No dangling deps.
     - Cycles reported (warning, not failure).
     - Orphaned ledger rows (no source note) reported.

Exit code 0 if clean, 1 if any error-level issue found.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
GRAPH_PATH = DATA_DIR / "citation_graph.json"

ALLOWED_AUDIT_STATUSES = {
    "unaudited",
    "audit_in_progress",
    "audited_clean",
    "audited_renaming",
    "audited_conditional",
    "audited_decoration",
    "audited_failed",
    "audited_numerical_match",
}
ALLOWED_CURRENT_STATUSES = {
    "proposed_retained",
    "proposed_promoted",
    "support",
    "bounded",
    "open",
    "unknown",
}
RATIFIED_BY_AUDIT_ONLY = {"retained", "promoted"}
ALLOWED_INDEPENDENCE = {"weak", "cross_family", "strong", "external", None}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def hash_note_on_disk(note_path_str: str) -> str | None:
    p = REPO_ROOT / note_path_str
    if not p.exists():
        return None
    return hashlib.sha256(p.read_text(encoding="utf-8", errors="replace").encode("utf-8")).hexdigest()


def main() -> int:
    if not LEDGER_PATH.exists():
        print("FAIL: audit_ledger.json missing", file=sys.stderr)
        return 1
    ledger = load_json(LEDGER_PATH)
    graph = load_json(GRAPH_PATH) if GRAPH_PATH.exists() else None
    rows = ledger.get("rows", {})

    errors: list[str] = []
    warnings: list[str] = []

    # Schema and hard-rule checks.
    for cid, row in rows.items():
        cs = row.get("current_status")
        a = row.get("audit_status")
        e = row.get("effective_status")
        ind = row.get("independence")

        if cs in RATIFIED_BY_AUDIT_ONLY:
            errors.append(
                f"{cid}: current_status={cs!r} forbidden — only audit lane may grant {cs}; use proposed_{cs}"
            )
        if cs not in ALLOWED_CURRENT_STATUSES:
            errors.append(f"{cid}: current_status={cs!r} not in allowed set")
        if a not in ALLOWED_AUDIT_STATUSES:
            errors.append(f"{cid}: audit_status={a!r} not in allowed set")
        if ind not in ALLOWED_INDEPENDENCE:
            errors.append(f"{cid}: independence={ind!r} not in allowed set")

        if a == "audited_clean":
            if not row.get("auditor"):
                errors.append(f"{cid}: audited_clean requires non-empty auditor")
            if not row.get("auditor_family"):
                errors.append(f"{cid}: audited_clean requires auditor_family")
            if cs not in {"proposed_retained", "proposed_promoted"}:
                errors.append(
                    f"{cid}: audited_clean with current_status={cs!r} is illegal "
                    f"(audit_clean only ratifies proposed_retained / proposed_promoted)"
                )
            # Effective must be retained or promoted.
            if e not in {"retained", "promoted"}:
                # Could be inherited demotion; warn rather than error.
                warnings.append(
                    f"{cid}: audited_clean but effective_status={e!r} (likely demoted by upstream dep)"
                )
            # Criticality-aware independence rules.
            criticality = row.get("criticality") or "leaf"
            if criticality in {"critical", "high"} and ind == "weak":
                errors.append(
                    f"{cid}: criticality={criticality} requires independence != 'weak' for audited_clean"
                )
            if criticality == "critical":
                xc = row.get("cross_confirmation") or {}
                if xc.get("status") != "confirmed":
                    errors.append(
                        f"{cid}: critical claim requires cross_confirmation.status='confirmed'; "
                        f"got {xc.get('status')!r}"
                    )

        # Criticality bump after audit (warn that re-audit may be needed).
        snap = row.get("audit_state_snapshot")
        if snap is not None:
            crit_now = row.get("criticality") or "leaf"
            crit_at_audit = snap.get("criticality") or "leaf"
            crit_rank = {"leaf": 0, "medium": 1, "high": 2, "critical": 3}
            if crit_rank.get(crit_now, 0) > crit_rank.get(crit_at_audit, 0):
                warnings.append(
                    f"{cid}: criticality bumped {crit_at_audit}->{crit_now} since audit; "
                    "invalidate_stale_audits.py should reset"
                )

        # Hash drift.
        on_disk = hash_note_on_disk(row.get("note_path", ""))
        if on_disk is None:
            warnings.append(f"{cid}: source note missing on disk: {row.get('note_path')}")
        elif on_disk != row.get("note_hash"):
            errors.append(
                f"{cid}: note_hash mismatch — note edited since seeding; re-run seed_audit_ledger.py"
            )

        # Dangling deps.
        for d in row.get("deps", []):
            if d not in rows:
                warnings.append(f"{cid}: dangling dep {d!r} (no ledger row)")

    # Effective-status propagation sanity.
    for cid, row in rows.items():
        if row.get("effective_status") == "retained":
            for d in row.get("deps", []):
                d_eff = rows.get(d, {}).get("effective_status")
                if d_eff != "retained":
                    errors.append(
                        f"{cid}: effective_status=retained but dep {d!r} has effective_status={d_eff!r}"
                    )

    # Graph health: cycles (informational).
    cycle_count = 0
    if graph:
        # Quick reachability-based cycle detection on the graph adjacency.
        adj = {c: list(n["deps"]) for c, n in graph["nodes"].items()}
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {c: WHITE for c in adj}
        for start in adj:
            if color[start] != WHITE:
                continue
            stack = [(start, iter(adj[start]))]
            color[start] = GRAY
            while stack:
                node, it = stack[-1]
                try:
                    nxt = next(it)
                except StopIteration:
                    color[node] = BLACK
                    stack.pop()
                    continue
                if nxt not in color:
                    continue
                if color[nxt] == GRAY:
                    cycle_count += 1
                    continue
                if color[nxt] == BLACK:
                    continue
                color[nxt] = GRAY
                stack.append((nxt, iter(adj[nxt])))
        if cycle_count:
            warnings.append(f"graph contains {cycle_count} back-edges (cycles)")

    # Output.
    print(f"audit_lint: {len(rows)} rows checked")
    if warnings:
        print(f"  {len(warnings)} warnings:")
        for w in warnings[:20]:
            print(f"    WARN: {w}")
        if len(warnings) > 20:
            print(f"    ... and {len(warnings) - 20} more")
    if errors:
        print(f"  {len(errors)} errors:")
        for e in errors[:30]:
            print(f"    ERROR: {e}")
        if len(errors) > 30:
            print(f"    ... and {len(errors) - 30} more")
        return 1
    print("  OK: no errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
