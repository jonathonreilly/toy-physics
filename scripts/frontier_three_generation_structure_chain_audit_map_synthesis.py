#!/usr/bin/env python3
"""Re-verify the three-generation structure chain audit map synthesis meta
note against the live audit ledger.

This is a navigation-map check, not a physics proof. The synthesis note
makes specific claims about the live ledger:

  - the root (`three_generation_observable_theorem_note`) is present
    and `unaudited`, with `criticality: critical` and
    `load_bearing_score >= 40.0`;
  - the transitive-closure size of the upstream chain is `7` (root
    included);
  - the audit_status distribution matches the table in §"Chain scope";
  - the 2 unaudited frontier rows are exactly the chain tip plus
    `s3_taste_cube_decomposition_note`;
  - the named open-gate boundary
    (`staggered_dirac_realization_gate_note_2026-05-03`) carries
    `audit_status=audited_clean` and `effective_status=open_gate`;
  - the synthesis itself is `claim_type: meta` with
    `proposal_allowed: false`;
  - no audit row is promoted by this synthesis.

If any of these drift (e.g. a frontier row's audit_status changes), the
runner FAILs and the synthesis needs a refresh.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
NOTE = (
    ROOT
    / "docs"
    / "THREE_GENERATION_STRUCTURE_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md"
)

CHAIN_ROOT = "three_generation_observable_theorem_note"

EXPECTED_CHAIN_SIZE = 7  # root included

EXPECTED_STATUS_COUNTS = {
    "audited_clean": 4,
    "unaudited": 3,
}

EXPECTED_EFFECTIVE_COUNTS = {
    "retained": 2,
    "retained_no_go": 1,
    "meta": 1,
    "open_gate": 1,
    "unaudited": 2,
}

# The single strict-frontier unaudited row (deps all retained-grade
# or named-open-gate).
EXPECTED_STRICT_FRONTIER = {
    "s3_taste_cube_decomposition_note",
}

# The chain tip — unaudited, one hop above the strict frontier (has
# the strict frontier row as a dep, plus the named-open-gate boundary).
EXPECTED_CHAIN_TIP = {
    "three_generation_observable_theorem_note",
}

# Cleanly-audited open_gate frontier (named open work). Not awaiting
# forward motion at this row's scope per audit verdict.
EXPECTED_OPEN_GATE_FRONTIER = {
    "staggered_dirac_realization_gate_note_2026-05-03",
}

# Retained-grade boundary rows.
EXPECTED_RETAINED_BOUNDARY = {
    "site_phase_cube_shift_intertwiner_note",
    "z2_hw1_mass_matrix_parametrization_note",
    "s3_mass_matrix_no_go_note",
}

# Meta infrastructure.
EXPECTED_META_INTERIOR = {
    "minimal_axioms_2026-05-03",
}

RETAINED_GRADES = {"retained", "retained_no_go", "retained_bounded", "meta"}


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


def is_retained_grade(es: str | None) -> bool:
    if not es:
        return False
    if es in RETAINED_GRADES:
        return True
    return es.startswith("decoration_under_")


def is_named_open_gate_or_retained(es: str | None) -> bool:
    """Frontier-style retained-or-resolved: retained-grade or named
    open-gate boundary."""
    if is_retained_grade(es):
        return True
    return es == "open_gate"


def upstream_closure(rows: dict, start_cid: str) -> set:
    visited: set = set()
    queue: deque = deque([start_cid])
    while queue:
        cid = queue.popleft()
        if cid in visited:
            continue
        visited.add(cid)
        for d in rows.get(cid, {}).get("deps", []) or []:
            if d in rows and d not in visited:
                queue.append(d)
    return visited


def main() -> int:
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1

    rows = json.loads(LEDGER.read_text())["rows"]
    note = NOTE.read_text()

    print("three-generation structure chain audit map synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification + governance ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    check(
        "synthesis declares proposal_allowed: false",
        "proposal_allowed: false" in note,
    )
    audit_clean_token = "audited" + "_clean"
    check(
        "synthesis does not declare itself audited_clean",
        audit_clean_token not in note.split("## ", 1)[0],
        "header block must not pre-empt audit verdict",
    )

    # ---- root ----
    r = rows.get(CHAIN_ROOT, {})
    check(
        f"root present: {CHAIN_ROOT}",
        bool(r),
        f"audit_status={r.get('audit_status')!r}",
    )
    check(
        f"root unaudited: {CHAIN_ROOT}",
        r.get("audit_status") == "unaudited",
        f"audit_status={r.get('audit_status')!r}",
    )
    check(
        f"root criticality=critical: {CHAIN_ROOT}",
        r.get("criticality") == "critical",
        f"criticality={r.get('criticality')!r}",
    )
    lbs = r.get("load_bearing_score") or 0.0
    check(
        f"root load_bearing_score >= 40.0: {CHAIN_ROOT}",
        lbs >= 40.0,
        f"load_bearing_score={lbs}",
    )

    # ---- chain size ----
    chain = upstream_closure(rows, CHAIN_ROOT)
    check(
        f"chain transitive-closure size = {EXPECTED_CHAIN_SIZE}",
        len(chain) == EXPECTED_CHAIN_SIZE,
        f"actual={len(chain)}",
    )

    # ---- status distribution (audit) ----
    actual_status_counts: dict = {}
    for cid in chain:
        s = rows.get(cid, {}).get("audit_status") or "unaudited"
        actual_status_counts[s] = actual_status_counts.get(s, 0) + 1
    for status, expected in EXPECTED_STATUS_COUNTS.items():
        actual = actual_status_counts.get(status, 0)
        check(
            f"chain audit_status[{status}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- effective_status distribution ----
    actual_eff_counts: dict = {}
    for cid in chain:
        s = rows.get(cid, {}).get("effective_status") or "unaudited"
        actual_eff_counts[s] = actual_eff_counts.get(s, 0) + 1
    for status, expected in EXPECTED_EFFECTIVE_COUNTS.items():
        actual = actual_eff_counts.get(status, 0)
        check(
            f"chain effective_status[{status}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- retained boundary rows ----
    for cid in EXPECTED_RETAINED_BOUNDARY:
        r = rows.get(cid, {})
        check(
            f"retained boundary present + audited_clean: {cid}",
            r.get("audit_status") == "audited_clean",
            f"audit_status={r.get('audit_status')!r}",
        )
        check(
            f"retained boundary effective is retained-grade: {cid}",
            is_retained_grade(r.get("effective_status")),
            f"effective_status={r.get('effective_status')!r}",
        )

    # ---- open-gate boundary ----
    for cid in EXPECTED_OPEN_GATE_FRONTIER:
        r = rows.get(cid, {})
        check(
            f"open-gate boundary present + audited_clean: {cid}",
            r.get("audit_status") == "audited_clean",
            f"audit_status={r.get('audit_status')!r}",
        )
        check(
            f"open-gate boundary effective_status=open_gate: {cid}",
            r.get("effective_status") == "open_gate",
            f"effective_status={r.get('effective_status')!r}",
        )

    # ---- meta interior ----
    for cid in EXPECTED_META_INTERIOR:
        r = rows.get(cid, {})
        check(
            f"meta interior present + claim_type=meta: {cid}",
            r.get("claim_type") == "meta",
            f"claim_type={r.get('claim_type')!r}",
        )

    # ---- strict frontier (deps all retained-or-named-open-gate) ----
    for cid in EXPECTED_STRICT_FRONTIER:
        r = rows.get(cid, {})
        check(
            f"strict frontier present: {cid}",
            bool(r),
        )
        check(
            f"strict frontier audit_status=unaudited: {cid}",
            r.get("audit_status") == "unaudited",
            f"audit_status={r.get('audit_status')!r}",
        )
        # Confirm its deps are all retained-grade or named-open-gate
        deps = r.get("deps", []) or []
        bad_deps = [
            d
            for d in deps
            if not is_named_open_gate_or_retained(
                rows.get(d, {}).get("effective_status")
            )
        ]
        check(
            f"strict frontier has all retained-or-named-open-gate deps: {cid}",
            not bad_deps,
            f"non_resolved_deps={bad_deps}",
        )

    # ---- chain tip (one hop above strict frontier) ----
    for cid in EXPECTED_CHAIN_TIP:
        r = rows.get(cid, {})
        check(
            f"chain tip audit_status=unaudited: {cid}",
            r.get("audit_status") == "unaudited",
            f"audit_status={r.get('audit_status')!r}",
        )
        # Confirm its deps include exactly the strict frontier rows
        # plus retained-grade or named-open-gate boundary rows.
        deps = set(r.get("deps", []) or [])
        non_resolved = {
            d
            for d in deps
            if not is_named_open_gate_or_retained(
                rows.get(d, {}).get("effective_status")
            )
        }
        check(
            f"chain tip's non-resolved deps == strict frontier: {cid}",
            non_resolved == EXPECTED_STRICT_FRONTIER,
            f"non_resolved={sorted(non_resolved)}",
        )

    # ---- frontier completeness ----
    # A strict-frontier row is one whose own one-hop deps are all
    # retained-grade or named-open-gate boundary, but whose
    # effective_status is not itself retained-grade. Exclude meta rows
    # and named-open-gate boundary rows.
    actual_strict_frontier: set = set()
    for cid in chain:
        r = rows.get(cid, {})
        es = r.get("effective_status")
        if es == "meta":
            continue
        if is_retained_grade(es):
            continue
        if es == "open_gate":
            # A named-open-gate audit_clean row is at the boundary.
            continue
        deps = r.get("deps", []) or []
        bad = [
            d
            for d in deps
            if not is_named_open_gate_or_retained(
                rows.get(d, {}).get("effective_status")
            )
        ]
        if not bad:
            actual_strict_frontier.add(cid)

    expected_strict_frontier = set(EXPECTED_STRICT_FRONTIER)
    extra = actual_strict_frontier - expected_strict_frontier
    missing = expected_strict_frontier - actual_strict_frontier
    check(
        f"chain strict-frontier matches expected ({len(expected_strict_frontier)} rows)",
        not extra and not missing,
        f"extra={sorted(extra)} missing={sorted(missing)}",
    )

    # ---- previous archived audit on root: at least one audited_clean ----
    prev = rows.get(CHAIN_ROOT, {}).get("previous_audits") or []
    has_clean = any(
        p.get("audit_status") == "audited_clean" for p in prev
    )
    check(
        "root has at least one archived audited_clean previous audit",
        has_clean,
        "narrow-scope precedent for the C^3 algebra claim",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
