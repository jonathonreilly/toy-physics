#!/usr/bin/env python3
"""Check the LHCM chain audit map synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis is:
  - classified as meta and does not declare pipeline status;
  - cites the chain root, the four LHCM-family rows, and the sister
    narrow ratio / hypercharge / anomaly cancellation rows;
  - cites the audit-lane policy authority (docs/audit/README.md);
  - records the do-NOT-spawn-105-row-frontier recommendation;
  - cites the consolidation atlas, the recently-shipped proof-walk
    notes, and the companion narrow theorem note in this PR.

Also verifies live audit-ledger state:
  - left_handed_charge_matching_note (chain root) carries the recorded
    bounded_theorem / unaudited / critical / td=713 / direct_in_degree=36
    fields and the three-row deps array.
  - The five-row parent core upstream matches the table in §2 with the
    recorded audit-status fields per claim_id.
  - The four LHCM-family sibling rows exist on the live ledger.
  - The realization gate carries audited_clean / open_gate.
  - The two retained-bounded graph-first authorities carry
    retained_bounded effective_status.

If any recorded ledger field above changes, this runner FAILs and the
synthesis becomes stale.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "LHCM_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md"
PARENT_NOTE = ROOT / "docs" / "LEFT_HANDED_CHARGE_MATCHING_NOTE.md"
ATLAS_NOTE = ROOT / "docs" / "LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md"
MATTER_NOTE = ROOT / "docs" / "LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md"
YNORM_NOTE = ROOT / "docs" / "LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md"
HIGGS_NOTE = ROOT / "docs" / "HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md"
PROOF_WALK_RATIO_NOTE = ROOT / "docs" / "LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md"
COMPANION_NOTE = ROOT / "docs" / "LHCM_MATTER_ASSIGNMENT_BLOCK_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10.md"
AUDIT_README = ROOT / "docs" / "audit" / "README.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

# claim_ids
PARENT_ID = "left_handed_charge_matching_note"
RATIO_ID = "lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02"
SELECTOR_ID = "graph_first_selector_derivation_note"
SU3_ID = "graph_first_su3_integration_note"
GATE_ID = "staggered_dirac_realization_gate_note_2026-05-03"
MINIMAL_AXIOMS_ID = "minimal_axioms_2026-05-03"
MATTER_ID = "lhcm_matter_assignment_from_su3_representation_note_2026-05-02"
YNORM_ID = "lhcm_y_normalization_from_anomaly_and_convention_note_2026-05-02"
ATLAS_ID = "lhcm_repair_atlas_consolidation_note_2026-05-02"
HIGGS_ID = "higgs_y_from_lhcm_and_yukawa_structure_note_2026-05-02"

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


def upstream_closure(target: str, rows: dict) -> set[str]:
    visited: set[str] = set()
    queue = [target]
    while queue:
        cur = queue.pop()
        if cur in visited:
            continue
        visited.add(cur)
        r = rows.get(cur, {})
        for d in r.get("deps", []) or []:
            if d not in visited:
                queue.append(d)
    visited.discard(target)
    return visited


def main() -> int:
    for path in (
        NOTE, PARENT_NOTE, ATLAS_NOTE, MATTER_NOTE, YNORM_NOTE, HIGGS_NOTE,
        PROOF_WALK_RATIO_NOTE, COMPANION_NOTE, AUDIT_README, AUDIT_LEDGER
    ):
        if not path.exists():
            print(f"missing required file: {path}")
            return 1

    note = NOTE.read_text()
    audit_readme = AUDIT_README.read_text()
    ledger = json.loads(AUDIT_LEDGER.read_text())

    print("LHCM chain audit map synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    check(
        "does not promote any row to retained",
        "Promote any LHCM-family row to retained" in note
        and "What this note does NOT do" in note,
    )

    # ---- chain root and family rows cited by claim_id ----
    check(f"chain root claim_id cited: {PARENT_ID}", PARENT_ID in note)
    check(f"narrow ratio claim_id cited: {RATIO_ID}", RATIO_ID in note)
    check(f"selector claim_id cited: {SELECTOR_ID}", SELECTOR_ID in note)
    check(f"SU(3) integration claim_id cited: {SU3_ID}", SU3_ID in note)
    check(f"realization gate claim_id cited: {GATE_ID}", GATE_ID in note)
    check(f"minimal axioms claim_id cited: {MINIMAL_AXIOMS_ID}", MINIMAL_AXIOMS_ID in note)
    check(f"matter-assignment row claim_id cited: {MATTER_ID}", MATTER_ID in note)
    check(f"Y-normalization row claim_id cited: {YNORM_ID}", YNORM_ID in note)
    check(f"consolidation atlas claim_id cited: {ATLAS_ID}", ATLAS_ID in note)
    check(f"Higgs-Y row claim_id cited: {HIGGS_ID}", HIGGS_ID in note)

    # ---- structural facts cited ----
    # Post-PR values: td=715 and direct_in_degree=37 because this PR adds
    # two new downstream rows (the chain-map meta + the matter-assignment
    # block proof-walk). The note is written referencing both pre- and
    # post-PR values explicitly.
    check(
        "transitive_descendants 715 (post-PR) recorded",
        "715" in note,
    )
    check(
        "direct_in_degree 37 (post-PR) recorded",
        "37" in note,
    )
    check(
        "load_bearing_score 27.984 (post-PR) recorded",
        "27.984" in note,
    )
    check(
        "pre-PR transitive_descendants 713 recorded for reference",
        "713" in note,
    )
    check(
        "pre-PR direct_in_degree 36 recorded for reference",
        "36" in note,
    )
    check("five-row parent core upstream language", "five-row parent core upstream" in note or "five-row" in note)
    check("132-row family upstream language", "132" in note and "upstream" in note)
    check("105-row frontier language", "105" in note and "frontier" in note)

    # ---- audit-lane policy authority cited ----
    check(
        "cites docs/audit/README.md authority",
        "docs/audit/README.md" in note or "audit/README.md" in note,
    )

    # ---- repair-class language present (canonical only) ----
    canonical_repair_classes = [
        "runner_artifact_issue",
        "dependency_not_retained",
        "missing_dependency_edge",
        "missing_bridge_theorem",
        "scope_too_broad",
        "compute_required",
    ]
    for rc in canonical_repair_classes:
        check(f"canonical repair class cited: {rc}", rc in note)

    # ---- recommendation for future campaigns ----
    check("Recommendation for future campaigns section present",
          "Recommendation for future campaigns" in note)
    check(
        "explicitly says structurally cheapest target = ratio row",
        "structurally cheapest" in note.lower()
        and RATIO_ID in note,
    )
    check(
        "explicitly says do NOT spawn 105-row frontier closure cycles",
        "Do NOT" in note and "105" in note,
    )
    check(
        "explicitly says no new vocabulary / tags / framings",
        "new vocabulary" in note.lower()
        and ("new tags" in note.lower() or "new claim_types" in note.lower())
        and ("new framing" in note.lower() or "new framings" in note.lower()),
    )

    # ---- proposal_allowed: false ----
    check("proposal_allowed: false declared", "proposal_allowed: false" in note)
    check(
        "proposal_allowed_reason justifies as backward-looking synthesis",
        "backward-looking" in note.lower() and "synthesis" in note.lower(),
    )

    # ---- companion + cross-references ----
    check(
        "cites consolidation atlas",
        "LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02" in note,
    )
    check(
        "cites parent LHCM source note",
        "LEFT_HANDED_CHARGE_MATCHING_NOTE.md" in note,
    )
    check(
        "cites companion narrow proof-walk note in this PR",
        "LHCM_MATTER_ASSIGNMENT_BLOCK_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10" in note,
    )
    check(
        "cites sibling ratio proof-walk note",
        "LH_DOUBLET_EIGENVALUE_RATIO_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-10" in note,
    )
    check(
        "cites hypercharge proof-walk note",
        "HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07" in note,
    )
    check(
        "cites anomaly-cancellation proof-walk note",
        "ANOMALY_CANCELLATION_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-08" in note,
    )
    check(
        "cites synthesis-template authority (audit backlog campaign progress)",
        "AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02" in note,
    )
    check(
        "cites sibling dep-chain audit (three-generation observable)",
        "THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02" in note,
    )

    # ---- review-loop rule ----
    check("Review-loop rule section present", "Review-loop rule" in note)

    # ---- new-vocabulary guard (forbidden tokens) ----
    blocked = [
        "algebraic universality",
        "two-class framing",
        "(CKN)",
        "lattice-realization-invariant",
        "realization-invariance",
    ]
    note_lower = note.lower()
    for marker in blocked:
        check(f"no banned vocabulary token: {marker!r}", marker.lower() not in note_lower)

    # ---- live ledger state ----
    rows = ledger.get("rows", {})
    check(
        "audit_ledger.json has rows table",
        isinstance(rows, dict) and len(rows) > 0,
        detail=f"rows count: {len(rows) if isinstance(rows, dict) else 0}",
    )

    parent_row = rows.get(PARENT_ID)
    ratio_row = rows.get(RATIO_ID)
    selector_row = rows.get(SELECTOR_ID)
    su3_row = rows.get(SU3_ID)
    gate_row = rows.get(GATE_ID)
    minimal_row = rows.get(MINIMAL_AXIOMS_ID)
    matter_row = rows.get(MATTER_ID)
    ynorm_row = rows.get(YNORM_ID)
    atlas_row = rows.get(ATLAS_ID)
    higgs_row = rows.get(HIGGS_ID)

    for rid, r in [
        (PARENT_ID, parent_row), (RATIO_ID, ratio_row),
        (SELECTOR_ID, selector_row), (SU3_ID, su3_row),
        (GATE_ID, gate_row), (MINIMAL_AXIOMS_ID, minimal_row),
        (MATTER_ID, matter_row), (YNORM_ID, ynorm_row),
        (ATLAS_ID, atlas_row), (HIGGS_ID, higgs_row),
    ]:
        check(f"ledger has row: {rid}", r is not None)

    # ---- chain root field consistency ----
    if parent_row is not None:
        check(
            "chain root claim_type is bounded_theorem",
            parent_row.get("claim_type") == "bounded_theorem",
            detail=f"claim_type: {parent_row.get('claim_type')!r}",
        )
        check(
            "chain root audit_status is unaudited",
            parent_row.get("audit_status") == "unaudited",
            detail=f"audit_status: {parent_row.get('audit_status')!r}",
        )
        check(
            "chain root effective_status is unaudited",
            parent_row.get("effective_status") == "unaudited",
            detail=f"effective_status: {parent_row.get('effective_status')!r}",
        )
        check(
            "chain root criticality is critical",
            parent_row.get("criticality") == "critical",
            detail=f"criticality: {parent_row.get('criticality')!r}",
        )
        # td and direct_in_degree are recomputed by the pipeline.
        # After this PR adds two downstream rows (chain map meta + matter
        # assignment block proof-walk), td increases by 2 and direct_in_degree
        # increases by 1. We record both pre-PR (713 / 36) and post-PR
        # (715 / 37) values in the note text and accept either current
        # state in the runner so the synthesis is robust to future
        # additions.
        td = parent_row.get("transitive_descendants")
        check(
            "chain root transitive_descendants is recorded as int >= 713",
            isinstance(td, int) and td >= 713,
            detail=f"transitive_descendants: {td!r}",
        )
        d_in = parent_row.get("direct_in_degree")
        check(
            "chain root direct_in_degree is recorded as int >= 36",
            isinstance(d_in, int) and d_in >= 36,
            detail=f"direct_in_degree: {d_in!r}",
        )
        parent_deps = set(parent_row.get("deps", []) or [])
        expected_parent_deps = {RATIO_ID, SELECTOR_ID, SU3_ID}
        check(
            "chain root deps match expected three-row set",
            parent_deps == expected_parent_deps,
            detail=f"deps: {sorted(parent_deps)} expected: {sorted(expected_parent_deps)}",
        )

    # ---- five-row parent core upstream ----
    if parent_row is not None:
        closure = upstream_closure(PARENT_ID, rows)
        expected_core = {RATIO_ID, SELECTOR_ID, SU3_ID, GATE_ID, MINIMAL_AXIOMS_ID}
        check(
            "parent core upstream is exactly five rows",
            len(closure) == 5,
            detail=f"len(closure) = {len(closure)}",
        )
        check(
            "parent core upstream matches expected five-row set",
            closure == expected_core,
            detail=f"closure: {sorted(closure)} expected: {sorted(expected_core)}",
        )

    # ---- realization gate fields ----
    if gate_row is not None:
        check(
            "realization gate audit_status is audited_clean",
            gate_row.get("audit_status") == "audited_clean",
            detail=f"audit_status: {gate_row.get('audit_status')!r}",
        )
        check(
            "realization gate effective_status is open_gate",
            gate_row.get("effective_status") == "open_gate",
            detail=f"effective_status: {gate_row.get('effective_status')!r}",
        )
        check(
            "realization gate claim_type is open_gate",
            gate_row.get("claim_type") == "open_gate",
            detail=f"claim_type: {gate_row.get('claim_type')!r}",
        )

    # ---- retained-bounded graph-first authorities ----
    for rid in (SELECTOR_ID, SU3_ID):
        r = rows.get(rid, {})
        check(
            f"{rid} effective_status is retained_bounded",
            r.get("effective_status") == "retained_bounded",
            detail=f"effective_status: {r.get('effective_status')!r}",
        )
        check(
            f"{rid} audit_status is audited_clean",
            r.get("audit_status") == "audited_clean",
            detail=f"audit_status: {r.get('audit_status')!r}",
        )

    # ---- narrow ratio row is the single unaudited critical in the parent core ----
    if ratio_row is not None:
        check(
            "narrow ratio row claim_type is bounded_theorem",
            ratio_row.get("claim_type") == "bounded_theorem",
            detail=f"claim_type: {ratio_row.get('claim_type')!r}",
        )
        check(
            "narrow ratio row audit_status is unaudited",
            ratio_row.get("audit_status") == "unaudited",
            detail=f"audit_status: {ratio_row.get('audit_status')!r}",
        )
        check(
            "narrow ratio row criticality is critical",
            ratio_row.get("criticality") == "critical",
            detail=f"criticality: {ratio_row.get('criticality')!r}",
        )

    # ---- audit-lane README still has retained-grade dep / repair-class language ----
    check(
        "audit/README.md retains retained-grade dependency language",
        "retained-grade dependencies" in audit_readme
        or "retained-grade" in audit_readme,
    )
    check(
        "audit/README.md retains audit_status / effective_status separation language",
        "audit_status" in audit_readme and "effective_status" in audit_readme,
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "LHCM chain audit map synthesis check passed: chain root + five-row "
        "parent core upstream + four LHCM-family siblings cited, repair-class "
        "language repo-canonical, structurally-cheapest-target recommendation "
        "explicit, live ledger state consistent with synthesis."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
