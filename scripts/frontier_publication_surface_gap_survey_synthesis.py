#!/usr/bin/env python3
"""Re-verify the publication-surface gap survey synthesis meta note
against the live audit ledger plus the live publication tables.

This is a navigation-map check, not a physics proof. The synthesis
note makes specific claims about the live state:

  - the union of the eight publication tables references a specific
    set of 631 distinct claim_ids;
  - the effective-status distribution across those rows matches the
    table in section "Effective-status distribution across
    publication-referenced rows";
  - each top-15 high-lbs blocked publication row is currently
    non-retained-grade per the live ledger;
  - the seven in-flight PRs have specific OPEN/CLOSED states at
    write time, and the four expected-OPEN PRs (#955, #969, #988,
    #1000) are still OPEN;
  - PR #955 + PR #969's descendant-closures intersect the
    publication-relevant blocked set with cardinality 154, leaving
    374 publication-relevant blocked rows not addressed by any
    in-flight PR.

If any of these drift, the runner FAILs and the synthesis needs a
refresh.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
NOTE = ROOT / "docs" / "PUBLICATION_SURFACE_GAP_SURVEY_SYNTHESIS_META_NOTE_2026-05-10.md"
PUB_DIR = ROOT / "docs" / "publication" / "ci3_z3"

PUB_FILES = (
    "CLAIMS_TABLE_EFFECTIVE_STATUS.md",
    "PUBLICATION_MATRIX_EFFECTIVE_STATUS.md",
    "RESULTS_INDEX_EFFECTIVE_STATUS.md",
    "QUANTITATIVE_SUMMARY_TABLE_EFFECTIVE_STATUS.md",
    "USABLE_DERIVED_VALUES_INDEX_EFFECTIVE_STATUS.md",
    "DERIVATION_ATLAS_EFFECTIVE_STATUS.md",
    "DERIVATION_VALIDATION_MAP_EFFECTIVE_STATUS.md",
    "FULL_CLAIM_LEDGER_EFFECTIVE_STATUS.md",
)

EXPECTED_PUB_REF_TOTAL = 631

EXPECTED_STATUS_COUNTS = {
    "unaudited": 408,
    "audited_conditional": 97,
    "retained_bounded": 33,
    "retained_no_go": 26,
    "retained": 23,
    "audited_numerical_match": 9,
    "audited_renaming": 8,
    "audited_failed": 5,
    "meta": 4,
    "open_gate": 1,
}
# decoration_under_* flattens to 4 in the synthesis table.
EXPECTED_DECORATION_UNDER_TOTAL = 4

EXPECTED_RETAINED_GRADE_TOTAL = 86  # retained + retained_bounded + retained_no_go + decoration_*
EXPECTED_BLOCKED_TOTAL = 506        # unaudited + audited_conditional + open_gate + retained_pending_chain + audit_in_progress
EXPECTED_TERMINAL_NONCLEAN = 22     # audited_numerical_match + audited_renaming + audited_failed
EXPECTED_META = 4

# Top-15 high-lbs non-retained publication rows, in the order quoted
# in the synthesis. We record the lbs to one decimal place; the runner
# checks the lbs is within 0.05 of expected and the effective_status
# matches.
EXPECTED_TOP_BLOCKED = [
    ("three_generation_observable_theorem_note", "unaudited", 42.34),
    ("staggered_dirac_realization_gate_note_2026-05-03", "open_gate", 41.26),
    ("observable_principle_from_axiom_note", "audited_conditional", 39.00),
    ("alpha_s_derived_note", "unaudited", 35.83),
    ("ckm_cp_phase_structural_identity_theorem_note_2026-04-24", "unaudited", 31.83),
    ("yt_ward_identity_derivation_theorem", "unaudited", 31.83),
    ("wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24", "unaudited", 31.33),
    ("anomaly_forces_time_theorem", "unaudited", 30.95),
    ("three_generation_structure_note", "unaudited", 28.05),
    ("left_handed_charge_matching_note", "unaudited", 27.98),
    ("ckm_magnitudes_structural_counts_theorem_note_2026-04-25", "unaudited", 27.29),
    ("ckm_atlas_axiom_closure_note", "unaudited", 26.43),
    ("standard_model_hypercharge_uniqueness_theorem_note_2026-04-24", "unaudited", 26.43),
    ("one_generation_matter_closure_note", "unaudited", 25.03),
    ("plaquette_self_consistency_note", "unaudited", 23.83),
]

# In-flight PR table at write time. The synthesis says these four are
# OPEN; the runner FAILs if any of them is closed/merged at check
# time. The other three are recorded as CLOSED but not required to
# stay closed.
EXPECTED_OPEN_PRS = (955, 969, 988, 1000)
EXPECTED_CLOSED_PRS = (959, 960, 984)

# PR roots that actually unblock leaves (per PR bodies):
# PR #955: re-points Wilson target citation; once it merges + the
#         next Codex audit pass picks up the Wilson target, that
#         row + its publication-relevant descendants flow toward
#         retained.
# PR #969: reclassifies alpha_lm decoration -> positive_theorem;
#         once it merges + audit lands clean, alpha_lm + descendants
#         flow toward retained.
# PR #988 (chain map) and PR #1000 (narrow split) do not directly
# unblock existing publication rows.
PR_UNBLOCK_ROOTS = {
    955: "koide_circulant_wilson_target_note_2026-04-18",
    969: "alpha_lm_geometric_mean_identity_theorem_note_2026-04-24",
}

EXPECTED_ADDRESSED_TOTAL = 154   # addressed by PR #955 + PR #969
EXPECTED_GAP_TOTAL = 374         # NOT addressed by any in-flight PR
EXPECTED_BLOCKED_BASELINE = 528  # publication-relevant blocked total (any criticality)

RETAINED_GRADES = {"retained", "retained_bounded", "retained_no_go"}


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


def parse_publication_refs() -> dict[str, set[str]]:
    """Parse the eight publication tables and extract every cited
    `[audit:STATUS]` annotation. Returns claim_id -> set of source
    files.
    """
    pattern = re.compile(r"([A-Za-z0-9_\-]+\.md)\)\xa0\[audit:(\w+)\]")
    pattern2 = re.compile(r"([A-Za-z0-9_\-]+\.md)\)&nbsp;\[audit:(\w+)\]")
    note_files: dict[str, set[str]] = defaultdict(set)
    for f in PUB_FILES:
        p = PUB_DIR / f
        if not p.exists():
            continue
        text = p.read_text()
        for note, status in pattern.findall(text) + pattern2.findall(text):
            cid = note.replace(".md", "").lower()
            note_files[cid].add(f)
    return note_files


def descendants_set(rows: dict[str, dict], root_cid: str) -> set[str]:
    """Compute the set of claim_ids that depend (transitively) on
    root_cid via the deps[] graph.
    """
    dependents: dict[str, set[str]] = defaultdict(set)
    for cid, r in rows.items():
        for d in r.get("deps", []):
            dependents[d].add(cid)
    visited: set[str] = set()
    queue: deque[str] = deque([root_cid])
    while queue:
        x = queue.popleft()
        for d in dependents[x]:
            if d not in visited:
                visited.add(d)
                queue.append(d)
    return visited


def gh_pr_state(pr_number: int) -> str | None:
    """Return the GitHub PR state ("OPEN" / "CLOSED" / "MERGED") via
    `gh pr view`. Returns None on error.
    """
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--json", "state"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return json.loads(result.stdout).get("state")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            json.JSONDecodeError, FileNotFoundError):
        return None


def main() -> int:
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1

    rows = json.loads(LEDGER.read_text())["rows"]
    note = NOTE.read_text()

    print("publication-surface gap survey synthesis check")
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

    # ---- publication tables exist + parse ----
    for f in PUB_FILES:
        p = PUB_DIR / f
        check(f"publication table present: {f}", p.exists())

    note_files = parse_publication_refs()
    check(
        f"manuscript-relevant claim_id total = {EXPECTED_PUB_REF_TOTAL}",
        len(note_files) == EXPECTED_PUB_REF_TOTAL,
        f"actual={len(note_files)}",
    )

    # ---- ledger-resolved subset ----
    in_ledger = {cid for cid in note_files if cid in rows}

    status_counts: Counter = Counter()
    decoration_under_count = 0
    for cid in in_ledger:
        es = rows[cid].get("effective_status") or "unaudited"
        if es.startswith("decoration_under_"):
            decoration_under_count += 1
        else:
            status_counts[es] += 1

    for status, expected in EXPECTED_STATUS_COUNTS.items():
        actual = status_counts.get(status, 0)
        check(
            f"effective_status[{status}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )
    check(
        f"effective_status[decoration_under_*] = {EXPECTED_DECORATION_UNDER_TOTAL}",
        decoration_under_count == EXPECTED_DECORATION_UNDER_TOTAL,
        f"actual={decoration_under_count}",
    )

    # ---- bucket totals ----
    retained_grade_total = (
        status_counts.get("retained", 0)
        + status_counts.get("retained_bounded", 0)
        + status_counts.get("retained_no_go", 0)
        + decoration_under_count
    )
    check(
        f"retained-grade total = {EXPECTED_RETAINED_GRADE_TOTAL}",
        retained_grade_total == EXPECTED_RETAINED_GRADE_TOTAL,
        f"actual={retained_grade_total}",
    )
    blocked_total = (
        status_counts.get("unaudited", 0)
        + status_counts.get("audited_conditional", 0)
        + status_counts.get("audit_in_progress", 0)
        + status_counts.get("retained_pending_chain", 0)
        + status_counts.get("open_gate", 0)
    )
    check(
        f"blocked total = {EXPECTED_BLOCKED_TOTAL}",
        blocked_total == EXPECTED_BLOCKED_TOTAL,
        f"actual={blocked_total}",
    )
    terminal_total = (
        status_counts.get("audited_numerical_match", 0)
        + status_counts.get("audited_renaming", 0)
        + status_counts.get("audited_failed", 0)
    )
    check(
        f"terminal-non-clean total = {EXPECTED_TERMINAL_NONCLEAN}",
        terminal_total == EXPECTED_TERMINAL_NONCLEAN,
        f"actual={terminal_total}",
    )
    check(
        f"meta total = {EXPECTED_META}",
        status_counts.get("meta", 0) == EXPECTED_META,
        f"actual={status_counts.get('meta', 0)}",
    )

    # ---- top-15 named blocked publication rows ----
    for cid, expected_es, expected_lbs in EXPECTED_TOP_BLOCKED:
        r = rows.get(cid, {})
        check(
            f"named top-blocked row in publication: {cid}",
            cid in note_files,
            f"in_pub_set={cid in note_files}",
        )
        check(
            f"named top-blocked row in ledger: {cid}",
            bool(r),
        )
        es = r.get("effective_status")
        check(
            f"named top-blocked row effective_status={expected_es}: {cid}",
            es == expected_es,
            f"actual={es!r}",
        )
        check(
            f"named top-blocked row not retained-grade: {cid}",
            not is_retained_grade(es),
            f"effective_status={es!r}",
        )
        actual_lbs = r.get("load_bearing_score") or 0.0
        check(
            f"named top-blocked row load_bearing_score~={expected_lbs}: {cid}",
            abs(actual_lbs - expected_lbs) < 0.05,
            f"actual={actual_lbs:.3f}",
        )

    # ---- in-flight PR states ----
    for pr in EXPECTED_OPEN_PRS:
        state = gh_pr_state(pr)
        check(
            f"in-flight PR #{pr} is currently OPEN",
            state == "OPEN",
            f"state={state!r}",
        )
    for pr in EXPECTED_CLOSED_PRS:
        state = gh_pr_state(pr)
        check(
            f"recorded-CLOSED PR #{pr} is currently CLOSED",
            state == "CLOSED",
            f"state={state!r}",
        )

    # ---- addressed-vs.-gap split (descendant-closure intersection) ----
    blocked_pub_relevant: set[str] = set()
    for cid in in_ledger:
        r = rows[cid]
        es = r.get("effective_status")
        if is_retained_grade(es) or es == "meta":
            continue
        blocked_pub_relevant.add(cid)
    check(
        f"publication-relevant blocked baseline = {EXPECTED_BLOCKED_BASELINE}",
        len(blocked_pub_relevant) == EXPECTED_BLOCKED_BASELINE,
        f"actual={len(blocked_pub_relevant)}",
    )

    addressed: set[str] = set()
    for pr_num, root_cid in PR_UNBLOCK_ROOTS.items():
        check(
            f"PR #{pr_num} unblock root in ledger: {root_cid}",
            root_cid in rows,
        )
        if root_cid not in rows:
            continue
        descs = descendants_set(rows, root_cid)
        if root_cid in blocked_pub_relevant:
            addressed.add(root_cid)
        addressed |= descs & blocked_pub_relevant
    check(
        f"addressed by PR #955 + PR #969 = {EXPECTED_ADDRESSED_TOTAL}",
        len(addressed) == EXPECTED_ADDRESSED_TOTAL,
        f"actual={len(addressed)}",
    )

    gap = blocked_pub_relevant - addressed
    check(
        f"actual publication gap (NOT addressed) = {EXPECTED_GAP_TOTAL}",
        len(gap) == EXPECTED_GAP_TOTAL,
        f"actual={len(gap)}",
    )

    # ---- consistency: addressed + gap = baseline ----
    check(
        "addressed + gap = blocked baseline",
        len(addressed) + len(gap) == len(blocked_pub_relevant),
        f"addressed={len(addressed)} gap={len(gap)} baseline={len(blocked_pub_relevant)}",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
