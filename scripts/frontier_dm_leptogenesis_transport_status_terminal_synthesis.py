#!/usr/bin/env python3
"""Check the DM leptogenesis transport status terminal synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis:
  - is classified as meta and does not declare pipeline status;
  - cites the leaf and its eight one-hop deps;
  - records the five `terminal_audit`-flagged upstreams with the
    audit_status values claimed in the synthesis;
  - cross-references the parallel BAE terminal-synthesis template;
  - is consistent with the live audit ledger
    (`docs/audit/data/audit_ledger.json`); any drift in the cited
    upstream verdicts means the synthesis is stale and should be
    re-audited (FAIL).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md"
LEAF = ROOT / "docs" / "DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md"
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
BAE_TEMPLATE = ROOT / "docs" / "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md"

LEAF_ID = "dm_leptogenesis_transport_status_note_2026-04-16"

# The five terminal-flagged upstreams documented in this synthesis. Each
# row's expected (audit_status, effective_status_reason) pair must match
# the live ledger; if any cell drifts, the synthesis is stale and the
# runner FAILs that check.
TERMINAL_UPSTREAMS: list[tuple[str, str, str]] = [
    (
        "dm_leptogenesis_transport_decomposition_theorem_note_2026-04-16",
        "audited_renaming",
        "terminal_audit",
    ),
    (
        "dm_leptogenesis_transport_integral_theorem_note_2026-04-16",
        "audited_numerical_match",
        "terminal_audit",
    ),
    (
        "dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16",
        "audited_numerical_match",
        "terminal_audit",
    ),
    (
        "dm_leptogenesis_hrad_theorem_note_2026-04-16",
        "audited_conditional",
        "terminal_audit",
    ),
    (
        "dm_leptogenesis_equilibrium_conversion_theorem_note_2026-04-16",
        "audited_conditional",
        "terminal_audit",
    ),
]

# All eight load-bearing deps the leaf cites in its "Citations" section.
EXPECTED_LEAF_DEPS: list[str] = [
    "dm_leptogenesis_exact_kernel_closure_note_2026-04-15",
    "dm_leptogenesis_hrad_theorem_note_2026-04-16",
    "dm_leptogenesis_equilibrium_conversion_theorem_note_2026-04-16",
    "dm_leptogenesis_transport_decomposition_theorem_note_2026-04-16",
    "dm_leptogenesis_transport_integral_theorem_note_2026-04-16",
    "dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16",
    "dm_leptogenesis_ne_projected_source_triplet_sign_theorem_note_2026-04-16",
    "dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16",
]

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1
    if not LEAF.exists():
        print(f"missing leaf note: {LEAF}")
        return 1
    if not LEDGER.exists():
        print(f"missing audit ledger: {LEDGER}")
        return 1

    note = NOTE.read_text(encoding="utf-8")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    print("DM leptogenesis transport status terminal synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    check(
        "does not declare pipeline status (no effective_status, no audited_clean)",
        effective_token not in note and audit_clean_token not in note,
    )
    check("synthesis carries authority disclaimer", "Authority disclaimer" in note)
    check(
        "synthesis explicitly disclaims new derivation / new vocabulary",
        "no theorem promotion" in note.lower()
        or "does not propose" in note.lower()
        or "is not a new derivation" in note.lower(),
    )

    # ---- leaf reference ----
    check(
        "synthesis cites the leaf by markdown link",
        "DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md" in note,
    )
    check("leaf row exists in ledger", LEAF_ID in rows)
    if LEAF_ID in rows:
        leaf_row = rows[LEAF_ID]
        check(
            "leaf criticality=critical",
            leaf_row.get("criticality") == "critical",
            detail=f"got {leaf_row.get('criticality')}",
        )
        leaf_deps = set(leaf_row.get("deps") or [])
        for dep in EXPECTED_LEAF_DEPS:
            check(
                f"leaf registers dep: {dep}",
                dep in leaf_deps,
            )

    # ---- terminal upstream verdicts ----
    for dep_id, expected_status, expected_reason in TERMINAL_UPSTREAMS:
        if dep_id not in rows:
            check(f"upstream row exists: {dep_id}", False, "missing from ledger")
            continue
        r = rows[dep_id]
        check(
            f"{dep_id} audit_status == {expected_status}",
            r.get("audit_status") == expected_status,
            detail=f"got {r.get('audit_status')}",
        )
        check(
            f"{dep_id} effective_status_reason == {expected_reason}",
            r.get("effective_status_reason") == expected_reason,
            detail=f"got {r.get('effective_status_reason')}",
        )
        # Also verify the synthesis cites this upstream by its filename
        # (lowercase claim_id maps to the uppercase filename without the
        # `.md`; we check the canonical uppercase filename).
        expected_filename = dep_id.upper() + ".MD"
        # The note uses `.md` not `.MD`; match case-insensitively.
        check(
            f"synthesis links upstream: {dep_id}",
            expected_filename.lower() in note.lower(),
        )

    # ---- terminal-verdict language ----
    check(
        "synthesis uses repo-canonical 'audited_renaming'",
        "audited_renaming" in note,
    )
    check(
        "synthesis uses repo-canonical 'audited_numerical_match'",
        "audited_numerical_match" in note,
    )
    check(
        "synthesis uses repo-canonical 'audited_conditional'",
        "audited_conditional" in note,
    )
    check(
        "synthesis uses repo-canonical 'terminal_audit' reason",
        "terminal_audit" in note,
    )

    # ---- proposal_allowed status block ----
    check(
        "status block: proposal_allowed: false",
        "proposal_allowed: false" in note,
    )
    check(
        "status block: proposal_allowed_reason cites synthesis-not-derivation",
        "proposal_allowed_reason" in note
        and ("synthesis" in note.lower())
        and ("not a new derivation" in note.lower()),
    )

    # ---- recommendation section present ----
    check(
        "recommendation: do not run audit-backlog campaigns on this leaf",
        "audit-backlog" in note.lower()
        and ("do **not**" in note.lower() or "do not" in note.lower()),
    )
    check(
        "recommendation: do not run retained-promotion campaigns on this leaf",
        "retained-promotion" in note.lower(),
    )

    # ---- cross-reference to parallel BAE template ----
    check(
        "synthesis cross-references BAE terminal-synthesis template",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09" in note,
    )
    check(
        "BAE template file exists on disk",
        BAE_TEMPLATE.exists(),
    )

    # ---- review-loop rule ----
    check(
        "review-loop rule for future campaigns present",
        "Review-loop rule" in note or "review-loop rule" in note.lower(),
    )
    check(
        "review-loop rule notes block is terminal at audit-lane layer",
        "terminal at the\n   audit-lane" in note or "terminal at the audit-lane" in note,
    )

    # ---- count summary ----
    terminal_count = sum(
        1
        for dep_id, _, _ in TERMINAL_UPSTREAMS
        if dep_id in rows
        and rows[dep_id].get("effective_status_reason") == "terminal_audit"
    )
    check(
        "five terminal-flagged upstreams confirmed in ledger",
        terminal_count == 5,
        detail=f"counted {terminal_count}/5",
    )
    check(
        "synthesis cites 'five of eight' load-bearing deps as terminal",
        ("five of eight" in note.lower())
        or ("5 of 8" in note),
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "DM leptogenesis transport status terminal synthesis check passed: "
        "five terminal-flagged upstreams match live ledger, "
        "synthesis is meta, "
        "no theorem promotion, no new vocabulary, "
        "recommendation against audit-backlog / retained-promotion campaigns recorded."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
