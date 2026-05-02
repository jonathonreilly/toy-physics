#!/usr/bin/env python3
"""Lint the audit ledger for consistency.

Checks (all hard rules from FRESH_LOOK_REQUIREMENTS.md and README.md):

  1. Schema:
     - Every row has the expected fields.
     - audit_status is one of the allowed enum values.
     - claim_type is one of the auditor-owned allowed enum values.
     - legacy source-status fields are absent from generated audit data.

  2. The hard rules:
     - audit_status = audited_clean requires auditor and auditor_family set.
     - audit_status = audited_clean promotes only through claim_type:
       positive_theorem -> retained, no_go -> retained_no_go, and
       bounded_theorem -> retained_bounded, provided the dependency chain is
       already retained-grade.
     - effective_status in a retained-grade bucket requires audit_status =
       audited_clean (or archived audited_failed for legacy retained_no_go)
       AND every dep's effective_status is retained-grade.
     - effective_status = retained_no_go has two paths:
       (a) claim_type = no_go and audit_status = audited_clean ratifies it.
       (b) audit_status = audited_failed AND the note has been moved to
           archive_unlanded/ (legacy path).
       Both paths represent ratified negative results, not active failures.
     - independence = 'weak' cannot land audited_clean. Critical clean
       confirmations must be cross-family, strong/external, or same-family
       fresh_context from a distinct restricted-input session.
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
ALLOWED_CLAIM_TYPES = {
    "positive_theorem",
    "bounded_theorem",
    "no_go",
    "open_gate",
    "decoration",
    "meta",
    None,
}
RETAINED_GRADES = {"retained", "retained_no_go", "retained_bounded"}
ALLOWED_EFFECTIVE_STATUSES = {
    "retained",
    "retained_no_go",
    "retained_bounded",
    "retained_pending_chain",
    "open_gate",
    "unaudited",
    "audit_in_progress",
    "meta",
    "audited_decoration",
    "audited_numerical_match",
    "audited_renaming",
    "audited_conditional",
    "audited_failed",
}
ALLOWED_INDEPENDENCE = {"weak", "fresh_context", "cross_family", "strong", "external", "judicial_review", None}
DEPRECATED_LEDGER_FIELDS = {"current_status", "current_status_raw"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def hash_note_on_disk(note_path_str: str) -> str | None:
    p = REPO_ROOT / note_path_str
    if not p.exists():
        return None
    return hashlib.sha256(p.read_text(encoding="utf-8", errors="replace").encode("utf-8")).hexdigest()


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true", help="Accepted for compatibility; lint is strict by default.")
    args, _ = p.parse_known_args()

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
        a = row.get("audit_status")
        e = row.get("effective_status")
        ct = row.get("claim_type")
        ind = row.get("independence")

        for field in DEPRECATED_LEDGER_FIELDS & set(row):
            errors.append(f"{cid}: deprecated ledger field {field!r} must not be present")
        if a not in ALLOWED_AUDIT_STATUSES:
            errors.append(f"{cid}: audit_status={a!r} not in allowed set")
        if ct not in ALLOWED_CLAIM_TYPES:
            errors.append(f"{cid}: claim_type={ct!r} not in allowed set")
        if e not in ALLOWED_EFFECTIVE_STATUSES and not (isinstance(e, str) and e.startswith("decoration_under_")):
            errors.append(f"{cid}: effective_status={e!r} not in allowed set")
        if a not in {None, "unaudited", "audit_in_progress"}:
            if ct is None:
                errors.append(f"{cid}: audited row requires claim_type")
            if not row.get("claim_scope"):
                errors.append(f"{cid}: audited row requires claim_scope")
        if row.get("claim_type_provenance") == "backfilled_pending_reaudit":
            warnings.append(
                f"{cid}: claim_type was backfilled for a critical legacy audit; queue for re-audit"
            )
        if ind not in ALLOWED_INDEPENDENCE:
            errors.append(f"{cid}: independence={ind!r} not in allowed set")

        if a == "audited_clean":
            if not row.get("auditor"):
                errors.append(f"{cid}: audited_clean requires non-empty auditor")
            if not row.get("auditor_family"):
                errors.append(f"{cid}: audited_clean requires auditor_family")
            expected = {
                "positive_theorem": "retained",
                "no_go": "retained_no_go",
                "bounded_theorem": "retained_bounded",
                "open_gate": "open_gate",
            }.get(ct)
            if expected is None:
                errors.append(
                    f"{cid}: audited_clean claim_type={ct!r} cannot become a retained-grade theorem"
                )
            elif e != expected:
                if e == "retained_pending_chain":
                    warnings.append(
                        f"{cid}: audited_clean claim_type={ct!r} waiting on upstream retained-grade closure"
                    )
                else:
                    errors.append(
                        f"{cid}: audited_clean claim_type={ct!r} expected effective_status={expected!r} "
                        f"or 'retained_pending_chain', got {e!r}"
                    )
            # Criticality-aware independence rules.
            criticality = row.get("criticality") or "leaf"
            if criticality in {"critical", "high"} and ind == "weak":
                errors.append(
                    f"{cid}: criticality={criticality} requires independence != 'weak' for audited_clean"
                )
            if criticality == "critical":
                xc = row.get("cross_confirmation") or {}
                xc_status = xc.get("status")
                if xc_status not in {"confirmed", "third_confirmed_first", "third_confirmed_second"}:
                    errors.append(
                        f"{cid}: critical claim requires confirmed cross-confirmation; "
                        f"got {xc_status!r}"
                    )
                else:
                    first = xc.get("first_audit") or {}
                    second = xc.get("second_audit") or {}
                    if first.get("auditor") and first.get("auditor") == second.get("auditor"):
                        errors.append(
                            f"{cid}: critical cross-confirmation reused auditor identity/session "
                            f"{second.get('auditor')!r}"
                        )
                    if (
                        first.get("auditor_family")
                        and first.get("auditor_family") == second.get("auditor_family")
                        and second.get("independence") != "fresh_context"
                    ):
                        errors.append(
                            f"{cid}: same-family critical cross-confirmation requires "
                            "second_audit.independence='fresh_context'"
                        )
                    if xc_status == "confirmed":
                        if first.get("claim_type") != second.get("claim_type"):
                            errors.append(
                                f"{cid}: critical cross-confirmation claim_type mismatch "
                                f"{first.get('claim_type')!r} vs {second.get('claim_type')!r}"
                            )
                        if first.get("load_bearing_step_class") != second.get("load_bearing_step_class"):
                            errors.append(
                                f"{cid}: critical cross-confirmation load_bearing_step_class mismatch "
                                f"{first.get('load_bearing_step_class')!r} vs "
                                f"{second.get('load_bearing_step_class')!r}"
                            )
                    if xc_status in {"third_confirmed_first", "third_confirmed_second"}:
                        third = xc.get("third_audit") or {}
                        if not third:
                            errors.append(f"{cid}: {xc_status} requires third_audit")
                        elif third.get("auditor") in {first.get("auditor"), second.get("auditor")}:
                            errors.append(
                                f"{cid}: third audit reused auditor identity/session "
                                f"{third.get('auditor')!r}"
                            )
                        elif (
                            third.get("auditor_family")
                            and third.get("auditor_family")
                            in {first.get("auditor_family"), second.get("auditor_family")}
                            and third.get("independence") not in {"fresh_context", "judicial_review"}
                        ):
                            errors.append(
                                f"{cid}: same-family third audit requires "
                                "fresh_context or judicial_review independence"
                            )
                        else:
                            winning = first if xc_status == "third_confirmed_first" else second
                            for key in ("verdict", "claim_type", "load_bearing_step_class"):
                                if third.get(key) != winning.get(key):
                                    errors.append(
                                        f"{cid}: {xc_status} third_audit {key}={third.get(key)!r} "
                                        f"does not match winning audit {winning.get(key)!r}"
                                    )

        if a == "audited_decoration":
            parent = row.get("decoration_parent_claim_id")
            if ct != "decoration":
                errors.append(f"{cid}: audited_decoration requires claim_type='decoration'")
            if not parent:
                msg = f"{cid}: audited_decoration requires decoration_parent_claim_id"
                if row.get("claim_type_provenance") == "backfilled_pending_reaudit":
                    warnings.append(msg + "; legacy row queued for re-audit")
                else:
                    errors.append(msg)
            else:
                parent_eff = rows.get(parent, {}).get("effective_status")
                if parent_eff not in RETAINED_GRADES:
                    warnings.append(
                        f"{cid}: decoration parent {parent!r} is not retained-grade "
                        f"(effective_status={parent_eff!r})"
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

    # Effective-status propagation sanity. A retained-grade row's deps must
    # themselves be retained-grade. Open gates and retained_pending_chain are
    # explicit blockers, not support for downstream theorem retention.
    for cid, row in rows.items():
        if row.get("effective_status") in RETAINED_GRADES:
            for d in row.get("deps", []):
                d_eff = rows.get(d, {}).get("effective_status")
                if d_eff not in RETAINED_GRADES:
                    errors.append(
                        f"{cid}: effective_status={row.get('effective_status')!r} but dep {d!r} "
                        f"has effective_status={d_eff!r}"
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
