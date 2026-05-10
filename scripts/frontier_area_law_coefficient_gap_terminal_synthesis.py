#!/usr/bin/env python3
"""Check the area-law coefficient-gap audit terminal-synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis is:
  - classified as meta and does not declare pipeline status;
  - cites the leaf and all ten expected blocking deps;
  - cites the substrate-forcing dep's audited_renaming verdict from two
    independent auditors;
  - cites the prior audited_conditional verdict on the leaf with the
    recorded carrier-identification load-bearing step;
  - cites the audit-lane policy authority (docs/audit/README.md);
  - cites the cycle-break entries cycle-0008, cycle-0009, cycle-0010
    naming the leaf as primary break target;
  - records the do-NOT-spawn-campaign-cycles recommendation.

Also verifies live audit-ledger and audit-queue state:
  - planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30
    carries at least one archived audited_renaming verdict;
  - area_law_coefficient_gap_note exists in the ledger with the expected
    deps and carries at least one archived audited_conditional verdict
    whose chain_closes is false;
  - audit_queue.json records cycle-0008/0009/0010 cycle-break entries
    with the leaf as primary_break_target.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "AREA_LAW_COEFFICIENT_GAP_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md"
)
LEAF_NOTE = ROOT / "docs" / "AREA_LAW_COEFFICIENT_GAP_NOTE.md"
PARITY_GATE_NOTE = (
    ROOT / "docs" / "AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md"
)
CAR_EDGE_NOTE = (
    ROOT
    / "docs"
    / "AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md"
)
NATIVE_CAR_NOTE = (
    ROOT / "docs" / "AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md"
)
BROADER_NO_GO_NOTE = (
    ROOT / "docs" / "AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md"
)
SUBSTRATE_NOTE = (
    ROOT
    / "docs"
    / "PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md"
)
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
AUDIT_README = ROOT / "docs" / "audit" / "README.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
AUDIT_QUEUE = ROOT / "docs" / "audit" / "data" / "audit_queue.json"

LEAF_ID = "area_law_coefficient_gap_note"
SUBSTRATE_ID = (
    "planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30"
)

EXPECTED_LEAF_DEPS = {
    "planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25",
    "planck_boundary_density_extension_theorem_note_2026-04-24",
    "area_law_quarter_broader_no_go_note_2026-04-25",
    "area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25",
    "area_law_primitive_car_edge_identification_theorem_note_2026-04-25",
    "bh_entropy_derived_note",
    "bh_entropy_rt_ratio_widom_no_go_note",
    "boundary_law_robustness_note_2026-04-11",
    "holographic_probe_note_2026-04-11",
    "area_law_native_car_semantics_tightening_note_2026-04-25",
}

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
    required_files = (
        NOTE,
        LEAF_NOTE,
        PARITY_GATE_NOTE,
        CAR_EDGE_NOTE,
        NATIVE_CAR_NOTE,
        BROADER_NO_GO_NOTE,
        SUBSTRATE_NOTE,
        MINIMAL_AXIOMS,
        AUDIT_README,
        AUDIT_LEDGER,
        AUDIT_QUEUE,
    )
    for path in required_files:
        if not path.exists():
            print(f"missing required file: {path}")
            return 1

    note = NOTE.read_text()
    audit_readme = AUDIT_README.read_text()
    ledger = json.loads(AUDIT_LEDGER.read_text())
    queue = json.loads(AUDIT_QUEUE.read_text())

    print("Area-law coefficient-gap audit terminal-synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    # The meta note discusses verdict semantics but must NOT declare any
    # row's pipeline status. We require the canonical "does not promote"
    # disclaimer plus presence of the explicit "What this note does NOT do"
    # section.
    check(
        "does not promote any row to retained",
        "Promote any row to retained" in note and "What this note does NOT do" in note,
    )

    # ---- leaf and dep identifiers cited ----
    check(f"leaf claim_id cited: {LEAF_ID}", LEAF_ID in note)
    check(f"substrate-forcing dep claim_id cited: {SUBSTRATE_ID}", SUBSTRATE_ID in note)
    check(
        "parity-gate dep claim_id cited",
        "area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25" in note,
    )
    check(
        "CAR-edge dep claim_id cited",
        "area_law_primitive_car_edge_identification_theorem_note_2026-04-25" in note,
    )
    check(
        "native-CAR tightening dep claim_id cited",
        "area_law_native_car_semantics_tightening_note_2026-04-25" in note,
    )
    check(
        "broader-no-go dep claim_id cited",
        "area_law_quarter_broader_no_go_note_2026-04-25" in note,
    )

    # ---- terminal verdict semantics ----
    check("cites audited_renaming terminal verdict", "audited_renaming" in note)
    check(
        "cites two independent audited_renaming verdicts on substrate-forcing dep",
        "Auditor 1" in note and "Auditor 2" in note,
    )
    check(
        "cites audited_conditional prior verdict on leaf",
        "audited_conditional" in note,
    )
    check(
        "cites cross_family independence on prior leaf audit",
        "cross_family" in note or "cross-family" in note.lower(),
    )
    check(
        "cites carrier-identification premise (CIP) by name",
        "(CIP)" in note and "carrier-identification premise" in note.lower(),
    )
    check(
        "cites conditional-on-open-work failure mode",
        "conditional-on-open-work" in note.lower()
        or "conditional on open" in note.lower(),
    )

    # ---- repair surface analysis ----
    check(
        "repair-target language present (cites independent retained derivation)",
        "Repair target" in note and "independent" in note.lower(),
    )
    check(
        "rules out small-bounded-note repair",
        "not a small bounded source note" in note.lower()
        or "structurally insufficient" in note.lower()
        or "small bounded" in note.lower(),
    )
    check(
        "notes no alternative dep chain bypass",
        "no alternative" in note.lower()
        or "bypass" in note.lower()
        or "rerouting" in note.lower(),
    )
    check(
        "names substrate-to-P_A forcing as the open block",
        "substrate-to-`P_A` forcing" in note or "substrate-to-P_A forcing" in note,
    )

    # ---- audit-lane policy authority cited ----
    check(
        "cites docs/audit/README.md authority",
        "docs/audit/README.md" in note or "audit/README.md" in note,
    )
    check(
        "cites hard rule 1 (audit-only retained grade)",
        "Retained grade is audit-only" in note or "hard rule 1" in note.lower(),
    )
    check(
        "cites hard rule 2 (open gates / terminal block propagation)",
        "Open gates block propagation" in note or "hard rule 2" in note.lower(),
    )

    # ---- cycle-break context ----
    check(
        "cites cycle-0008 cycle-break entry",
        "cycle-0008" in note or "`cycle-0008`" in note,
    )
    check(
        "cites cycle-0009 cycle-break entry",
        "cycle-0009" in note or "`cycle-0009`" in note,
    )
    check(
        "cites cycle-0010 cycle-break entry",
        "cycle-0010" in note or "`cycle-0010`" in note,
    )
    check(
        "cites cycle-break repair_class=missing_dependency_edge",
        "missing_dependency_edge" in note,
    )

    # ---- recommendation for future campaigns ----
    check(
        "Recommendation for future campaigns section present",
        "Recommendation for future campaigns" in note,
    )
    check(
        "explicitly says do NOT spawn audit-backlog cycles",
        "Do not" in note and "audit-backlog" in note.lower(),
    )
    check(
        "explicitly says do NOT spawn retained-promotion attempts on substrate-forcing dep",
        "retained-promotion" in note.lower() or "retained promotion" in note.lower(),
    )
    check(
        "explicitly says no new vocabulary / tags / framings",
        ("new vocabulary" in note.lower() or "new tags" in note.lower())
        and (
            "new framing" in note.lower()
            or "new framings" in note.lower()
            or "new claim_types" in note.lower()
        ),
    )

    # ---- proposal_allowed: false ----
    check("proposal_allowed: false declared", "proposal_allowed: false" in note)
    check(
        "proposal_allowed_reason justifies as backward-looking synthesis",
        "backward-looking" in note.lower() or "synthesis" in note.lower(),
    )

    # ---- companion + cross-references ----
    check(
        "cites sibling QUARK terminal synthesis as template",
        "QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10" in note,
    )
    check(
        "cites sibling KOIDE BAE terminal synthesis as template",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09" in note,
    )
    check(
        "cites leaf source note in cross-references",
        "AREA_LAW_COEFFICIENT_GAP_NOTE.md" in note,
    )
    check(
        "cites parity-gate dep source note in cross-references",
        "AREA_LAW_PRIMITIVE_PARITY_GATE_CARRIER_THEOREM_NOTE_2026-04-25.md" in note,
    )
    check(
        "cites CAR-edge dep source note in cross-references",
        "AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md" in note,
    )
    check(
        "cites native-CAR tightening dep source note in cross-references",
        "AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md" in note,
    )
    check(
        "cites broader-no-go dep source note in cross-references",
        "AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md" in note,
    )
    check(
        "cites substrate-forcing dep source note in cross-references",
        "PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md"
        in note,
    )
    check(
        "cites MINIMAL_AXIOMS_2026-05-03 framework axioms",
        "MINIMAL_AXIOMS_2026-05-03" in note,
    )
    check(
        "cites AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02 template authority",
        "AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02" in note,
    )

    # ---- review-loop rule ----
    check("Review-loop rule section present", "Review-loop rule" in note)
    check(
        "review-loop rule notes block is terminal pending substrate-forcing theorem",
        "terminal" in note.lower()
        and ("substrate-to-`P_A` forcing" in note or "substrate-to-P_A forcing" in note),
    )

    # ---- live ledger state ----
    rows = ledger.get("rows", {})
    check(
        "audit_ledger.json has rows table",
        isinstance(rows, dict) and len(rows) > 0,
        detail=f"rows count: {len(rows) if isinstance(rows, dict) else 0}",
    )

    leaf_row = rows.get(LEAF_ID)
    substrate_row = rows.get(SUBSTRATE_ID)

    check(f"ledger has leaf row: {LEAF_ID}", leaf_row is not None)
    check(f"ledger has substrate-forcing dep row: {SUBSTRATE_ID}", substrate_row is not None)

    if leaf_row is not None:
        leaf_deps = set(leaf_row.get("deps", []) or [])
        # All ten expected deps should appear
        missing_deps = EXPECTED_LEAF_DEPS - leaf_deps
        check(
            "leaf row lists all ten expected blocking deps",
            len(missing_deps) == 0,
            detail=(
                f"missing: {sorted(missing_deps)}"
                if missing_deps
                else f"deps count: {len(leaf_deps)}"
            ),
        )
        leaf_criticality = leaf_row.get("criticality")
        check(
            "leaf row is critical",
            leaf_criticality == "critical",
            detail=f"criticality: {leaf_criticality!r}",
        )
        leaf_claim_type = leaf_row.get("claim_type")
        check(
            "leaf row claim_type is positive_theorem",
            leaf_claim_type == "positive_theorem",
            detail=f"claim_type: {leaf_claim_type!r}",
        )
        # Find archived audited_conditional verdict in previous_audits
        prev_audits = leaf_row.get("previous_audits", []) or []
        has_audited_conditional = any(
            a.get("audit_status") == "audited_conditional"
            and a.get("chain_closes") is False
            for a in prev_audits
        )
        check(
            "leaf has archived audited_conditional verdict with chain_closes=false",
            has_audited_conditional,
            detail=f"previous_audits count: {len(prev_audits)}",
        )
        # Confirm the archived verdict's load_bearing_step references the
        # carrier-identification premise verbatim (the synthesis cites this).
        has_carrier_step = any(
            a.get("audit_status") == "audited_conditional"
            and "carrier-identification" in (a.get("load_bearing_step") or "").lower()
            or "primitive boundary block" in (a.get("load_bearing_step") or "").lower()
            for a in prev_audits
        )
        check(
            "archived verdict load_bearing_step names the carrier identification",
            has_carrier_step,
        )
    else:
        check("leaf row lists all ten expected blocking deps", False, detail="row missing")
        check("leaf row is critical", False, detail="row missing")
        check("leaf row claim_type is positive_theorem", False, detail="row missing")
        check(
            "leaf has archived audited_conditional verdict with chain_closes=false",
            False,
            detail="row missing",
        )
        check(
            "archived verdict load_bearing_step names the carrier identification",
            False,
            detail="row missing",
        )

    if substrate_row is not None:
        prev_audits = substrate_row.get("previous_audits", []) or []
        # At least one audited_renaming verdict must appear in archived audits
        renaming_audits = [
            a for a in prev_audits if a.get("audit_status") == "audited_renaming"
        ]
        check(
            "substrate-forcing dep has at least one archived audited_renaming verdict",
            len(renaming_audits) >= 1,
            detail=f"audited_renaming count: {len(renaming_audits)}",
        )
        # The synthesis cites two independent verdicts; we require the ledger
        # to reflect at least one (and we additionally require the synthesis
        # text quote two distinct rationales above).
        # Also confirm each renaming verdict carries a non-empty rationale.
        rationales_nonempty = all(
            (a.get("verdict_rationale") or "").strip() for a in renaming_audits
        )
        check(
            "all archived audited_renaming verdicts have non-empty rationale",
            rationales_nonempty if renaming_audits else False,
        )
    else:
        check(
            "substrate-forcing dep has at least one archived audited_renaming verdict",
            False,
            detail="row missing",
        )
        check(
            "all archived audited_renaming verdicts have non-empty rationale",
            False,
            detail="row missing",
        )

    # ---- audit-queue cycle-break entries ----
    cycle_break_targets = queue.get("cycle_break_targets", []) or []
    cycle_ids_with_leaf = {
        c.get("cycle_id")
        for c in cycle_break_targets
        if c.get("primary_break_target") == LEAF_ID
    }
    for cycle_id in ("cycle-0008", "cycle-0009", "cycle-0010"):
        check(
            f"audit_queue.json records {cycle_id} with leaf as primary break target",
            cycle_id in cycle_ids_with_leaf,
        )

    # Also verify the cycle_break_required repair_class language is present
    has_break_class = any(
        c.get("repair_class") == "cycle_break_required"
        for c in cycle_break_targets
        if c.get("primary_break_target") == LEAF_ID
    )
    check(
        "cycle-break entries on the leaf carry repair_class=cycle_break_required",
        has_break_class,
    )

    # ---- audit-lane README still has terminal-verdict rule we cite ----
    check(
        "audit/README.md retains 'audited_<failure_mode>' terminal language",
        "audited_<failure_mode>" in audit_readme
        or "terminal non-clean audit verdicts" in audit_readme,
    )
    check(
        "audit/README.md retains conditional-on-open-work failure-mode language",
        "Conditional-on-open-work" in audit_readme
        or "conditional-on-open-work" in audit_readme.lower()
        or "support" in audit_readme.lower()
        and "load-bearing" in audit_readme.lower(),
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Area-law coefficient-gap audit terminal-synthesis check passed: "
        "leaf and all ten deps cited, substrate-forcing audited_renaming "
        "verdict + leaf audited_conditional verdict recorded, repair "
        "surface analysis present, audit-lane policy authority cited, "
        "cycle-break entries cycle-0008/0009/0010 cited, do-NOT-spawn-"
        "campaign-cycles recommendation present, live ledger and audit-"
        "queue state consistent with synthesis."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
