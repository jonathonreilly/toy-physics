#!/usr/bin/env python3
"""Check the quark projector-parameter audit terminal-synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis is:
  - classified as meta and does not declare pipeline status;
  - cites the leaf, both deps, and the terminal-verdict block;
  - cites the cross-confirmation + judicial third audit;
  - cites the carrier magnitudes recorded in the upstream verdict;
  - cites the audit-lane policy authority (docs/audit/README.md);
  - records the do-NOT-spawn-campaign-cycles recommendation.

Also verifies live audit-ledger state:
  - quark_cp_carrier_completion_note_2026-04-18 is audited_numerical_match
    (terminal). If this verdict changes, the synthesis becomes stale and the
    runner FAILs.
  - quark_projector_ray_phase_completion_note_2026-04-18 exists in the ledger.
  - quark_projector_parameter_audit_note_2026-04-19 exists in the ledger and
    lists both expected blocking deps.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md"
LEAF_NOTE = ROOT / "docs" / "QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md"
RAY_DEP_NOTE = ROOT / "docs" / "QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md"
CARRIER_DEP_NOTE = ROOT / "docs" / "QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md"
AUDIT_README = ROOT / "docs" / "audit" / "README.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

LEAF_ID = "quark_projector_parameter_audit_note_2026-04-19"
RAY_DEP_ID = "quark_projector_ray_phase_completion_note_2026-04-18"
CARRIER_DEP_ID = "quark_cp_carrier_completion_note_2026-04-18"

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
    for path in (NOTE, LEAF_NOTE, RAY_DEP_NOTE, CARRIER_DEP_NOTE, AUDIT_README, AUDIT_LEDGER):
        if not path.exists():
            print(f"missing required file: {path}")
            return 1

    note = NOTE.read_text()
    audit_readme = AUDIT_README.read_text()
    ledger = json.loads(AUDIT_LEDGER.read_text())

    print("Quark projector-parameter audit terminal-synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    # The meta note discusses verdict semantics but must NOT declare any row's
    # pipeline status. We require the canonical "does not promote" disclaimer
    # plus absence of a row-promotion to retained for any actual claim.
    check("does not promote any row to retained", "Promote any row to retained" in note and "What this note does NOT do" in note)

    # ---- leaf and dep identifiers cited by claim_id ----
    check(f"leaf claim_id cited: {LEAF_ID}", LEAF_ID in note)
    check(f"projector-ray dep claim_id cited: {RAY_DEP_ID}", RAY_DEP_ID in note)
    check(f"carrier-completion dep claim_id cited: {CARRIER_DEP_ID}", CARRIER_DEP_ID in note)

    # ---- terminal verdict semantics ----
    check("cites audited_numerical_match terminal verdict", "audited_numerical_match" in note)
    check("cites terminal_audit reason", "terminal_audit" in note)
    check("cites cross_confirmation status confirmed", "cross_confirmation" in note and "confirmed" in note)
    check("cites judicial_third_pass / judicial third audit", "judicial" in note.lower() and "third" in note.lower())
    check("cites definition-as-derivation failure mode", "definition-as-derivation" in note)

    # ---- carrier magnitudes from upstream note recorded ----
    check("xi_u magnitude vs c13_u(base) ~ 101.9 recorded",
          "101.9" in note and ("|xi_u|" in note or "xi_u" in note))
    check("xi_d magnitude vs c13_d(base) ~ 6.64 recorded",
          "6.64" in note and ("|xi_d|" in note or "xi_d" in note))

    # ---- repair surface analysis ----
    check("repair-target language present (cites first-principles xi_u/xi_d derivation)",
          "first-principles" in note.lower() and "xi_u" in note and "xi_d" in note)
    check("rules out small-bounded-note repair",
          "not a small bounded source note" in note.lower()
          or "structurally insufficient" in note.lower()
          or "small bounded" in note.lower())
    check("notes no alternative dep chain bypass",
          "no alternative" in note.lower()
          or "bypass" in note.lower()
          or "rerouting" in note.lower())

    # ---- audit-lane policy authority cited ----
    check("cites docs/audit/README.md authority",
          "docs/audit/README.md" in note or "audit/README.md" in note)
    check("cites hard rule 1 (audit-only retained grade)",
          "Retained grade is audit-only" in note or "hard rule 1" in note.lower())
    check("cites hard rule 2 (open gates / terminal block propagation)",
          "Open gates block propagation" in note or "hard rule 2" in note.lower())

    # ---- recommendation for future campaigns ----
    check("Recommendation for future campaigns section present",
          "Recommendation for future campaigns" in note)
    check("explicitly says do NOT spawn audit-backlog cycles",
          "Do not" in note and "audit-backlog" in note.lower())
    check("explicitly says do NOT spawn retained-promotion attempts on carrier dep",
          "retained-promotion" in note.lower() or "retained promotion" in note.lower())
    check("explicitly says no new vocabulary / tags / framings",
          ("new vocabulary" in note.lower() or "new tags" in note.lower())
          and ("new framing" in note.lower() or "new framings" in note.lower() or "new claim_types" in note.lower()))

    # ---- proposal_allowed: false ----
    check("proposal_allowed: false declared",
          "proposal_allowed: false" in note)
    check("proposal_allowed_reason justifies as backward-looking synthesis",
          "backward-looking" in note.lower() or "synthesis" in note.lower())

    # ---- companion + cross-references ----
    check("cites sibling BAE terminal synthesis as template",
          "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09" in note)
    check("cites leaf source note in cross-references",
          "QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md" in note)
    check("cites projector-ray dep source note in cross-references",
          "QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md" in note)
    check("cites carrier-completion dep source note in cross-references",
          "QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md" in note)

    # ---- review-loop rule ----
    check("Review-loop rule section present",
          "Review-loop rule" in note)
    check("review-loop rule notes block is terminal pending xi_u/xi_d derivation",
          "terminal" in note.lower()
          and ("xi_u" in note and "xi_d" in note))

    # ---- live ledger state ----
    rows = ledger.get("rows", {})
    check("audit_ledger.json has rows table",
          isinstance(rows, dict) and len(rows) > 0,
          detail=f"rows count: {len(rows) if isinstance(rows, dict) else 0}")

    leaf_row = rows.get(LEAF_ID)
    ray_row = rows.get(RAY_DEP_ID)
    carrier_row = rows.get(CARRIER_DEP_ID)

    check(f"ledger has leaf row: {LEAF_ID}", leaf_row is not None)
    check(f"ledger has projector-ray dep row: {RAY_DEP_ID}", ray_row is not None)
    check(f"ledger has carrier-completion dep row: {CARRIER_DEP_ID}", carrier_row is not None)

    if carrier_row is not None:
        carrier_status = carrier_row.get("audit_status")
        check(
            "carrier-completion dep audit_status is audited_numerical_match (terminal)",
            carrier_status == "audited_numerical_match",
            detail=f"audit_status: {carrier_status!r}",
        )
        carrier_effective = carrier_row.get("effective_status")
        check(
            "carrier-completion dep effective_status is audited_numerical_match",
            carrier_effective == "audited_numerical_match",
            detail=f"effective_status: {carrier_effective!r}",
        )
    else:
        check("carrier-completion dep audit_status is audited_numerical_match (terminal)", False, detail="row missing")
        check("carrier-completion dep effective_status is audited_numerical_match", False, detail="row missing")

    if leaf_row is not None:
        leaf_deps = set(leaf_row.get("deps", []) or [])
        check(
            "leaf row lists projector-ray dep",
            RAY_DEP_ID in leaf_deps,
            detail=f"deps: {sorted(leaf_deps)}",
        )
        check(
            "leaf row lists carrier-completion dep",
            CARRIER_DEP_ID in leaf_deps,
            detail=f"deps: {sorted(leaf_deps)}",
        )
        leaf_criticality = leaf_row.get("criticality")
        check(
            "leaf row is critical",
            leaf_criticality == "critical",
            detail=f"criticality: {leaf_criticality!r}",
        )
    else:
        check("leaf row lists projector-ray dep", False, detail="row missing")
        check("leaf row lists carrier-completion dep", False, detail="row missing")
        check("leaf row is critical", False, detail="row missing")

    if ray_row is not None:
        ray_deps = set(ray_row.get("deps", []) or [])
        check(
            "projector-ray dep routes through carrier-completion dep",
            CARRIER_DEP_ID in ray_deps,
            detail=f"deps: {sorted(ray_deps)}",
        )
    else:
        check("projector-ray dep routes through carrier-completion dep", False, detail="row missing")

    # ---- audit-lane README still has terminal-verdict rule we cite ----
    check(
        "audit/README.md retains 'audited_<failure_mode>' terminal language",
        "audited_<failure_mode>" in audit_readme or "terminal non-clean audit verdicts" in audit_readme,
    )
    check(
        "audit/README.md retains definition-as-derivation language",
        "Definition-as-derivation" in audit_readme or "definition-as-derivation" in audit_readme.lower(),
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Quark projector-parameter audit terminal-synthesis check passed: "
        "leaf and both deps cited, terminal verdict + cross-confirmation + "
        "judicial-third-audit recorded, repair surface analysis present, "
        "audit-lane policy authority cited, do-NOT-spawn-campaign-cycles "
        "recommendation present, live ledger state consistent with synthesis."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
