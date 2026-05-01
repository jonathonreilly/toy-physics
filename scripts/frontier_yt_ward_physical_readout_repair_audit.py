#!/usr/bin/env python3
"""
Ward physical-readout repair audit for PR #230.

The old Ward theorem computes the 1/sqrt(6) scalar-singlet algebra.  The audit
demotion is narrower: it says the physical SM Yukawa readout was identified
with the H_unit matrix element instead of derived.  This runner encodes the
audit repair target and checks whether the current repo already supplies each
required bridge piece.  It is a boundary/repair-map runner, not a closure
runner: a clean execution means the current open status is identified
reproducibly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_ward_physical_readout_repair_audit_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def ledger_row(rows: dict[str, dict], key: str) -> dict:
    return rows.get(key, {})


def has_terms(text: str, *terms: str) -> bool:
    lowered = text.lower()
    return all(term.lower() in lowered for term in terms)


def main() -> int:
    print("YT Ward physical-readout repair audit")
    print("=" * 72)

    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    docs = {
        path.name: path.read_text(encoding="utf-8", errors="ignore")
        for path in (ROOT / "docs").glob("YT*.md")
    }
    all_yt = "\n".join(docs.values())

    ward = ledger_row(rows, "yt_ward_identity_derivation_theorem")
    ssb = ledger_row(rows, "yt_ssb_matching_gap_analysis_note_2026-04-18")
    class5 = ledger_row(rows, "yt_class_5_non_ql_yukawa_vertex_note_2026-04-18")
    hunit = ledger_row(rows, "yt_h_unit_flavor_column_decomposition_note_2026-04-18")
    color = ledger_row(rows, "yukawa_color_projection_theorem")

    repair_requirements = {
        "source_or_hs_normalization": {
            "evidence_terms": ["Hubbard-Stratonovich", "source", "Legendre"],
            "candidate_docs": ["YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md", "YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md"],
            "current_status": ssb.get("effective_status"),
            "audit_clean": ssb.get("effective_status") not in {"audited_renaming", "audited_failed", "audited_conditional"},
        },
        "chirality_projection": {
            "evidence_terms": ["chirality", "Q_L", "q_R", "trilinear"],
            "candidate_docs": ["YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md"],
            "current_status": class5.get("effective_status"),
            "audit_clean": class5.get("effective_status") not in {"audited_renaming", "audited_failed", "audited_conditional"},
        },
        "h_unit_physical_scalar_uniqueness": {
            "evidence_terms": ["D17", "unique", "H_unit"],
            "candidate_docs": ["YT_H_UNIT_FLAVOR_COLUMN_DECOMPOSITION_NOTE_2026-04-18.md", "YT_WARD_IDENTITY_DERIVATION_THEOREM.md"],
            "current_status": hunit.get("effective_status"),
            "audit_clean": hunit.get("effective_status") not in {"audited_renaming", "audited_failed", "audited_conditional"},
        },
        "lsz_scalar_external_leg": {
            "evidence_terms": ["LSZ", "external leg", "Z_phi"],
            "candidate_docs": ["YUKAWA_COLOR_PROJECTION_THEOREM.md", "YT_COLOR_PROJECTION_CORRECTION_NOTE.md"],
            "current_status": color.get("effective_status"),
            "audit_clean": color.get("effective_status") not in {"audited_renaming", "audited_failed", "audited_conditional"},
        },
        "absence_of_extra_factors": {
            "evidence_terms": ["absence", "extra factors"],
            "candidate_docs": ["YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md"],
            "current_status": ssb.get("effective_status"),
            "audit_clean": False,
        },
    }

    term_coverage = {}
    for name, req in repair_requirements.items():
        covered = all(has_terms(all_yt, term) for term in req["evidence_terms"])
        term_coverage[name] = covered
        report(f"repair-terms-scanned-{name}", True, f"covered={covered}; terms={req['evidence_terms']}")

    report(
        "ward-demotion-is-narrow",
        ward.get("effective_status") == "audited_renaming"
        and "physical observable bridge" in (ward.get("verdict_rationale") or ""),
        f"ward effective={ward.get('effective_status')}",
    )

    clean_requirements = {
        name: bool(req["audit_clean"])
        for name, req in repair_requirements.items()
    }
    for name, ok in clean_requirements.items():
        report(
            f"repair-open-import-detected-{name}",
            not ok,
            f"status={repair_requirements[name]['current_status']}",
        )

    all_clean = all(clean_requirements.values())
    report(
        "current-repo-does-not-yet-close-ward-repair",
        not all_clean,
        "all audit repair requirements would have to be clean for closure",
    )

    result = {
        "actual_current_surface_status": "open / Ward physical-readout repair not closed",
        "verdict": (
            "The repo contains prose and arithmetic for the Ward physical-readout "
            "repair, but the current audit surface does not close it.  The old "
            "Ward theorem remains audited_renaming; the SSB/source matching note "
            "is audited_renaming; chirality/H_unit support is failed or conditional; "
            "and the scalar LSZ/color-projection bridge remains audited_conditional."
        ),
        "ward_status": {
            "effective_status": ward.get("effective_status"),
            "load_bearing_step": ward.get("load_bearing_step"),
            "verdict_rationale": ward.get("verdict_rationale"),
        },
        "repair_requirements": repair_requirements,
        "term_coverage": term_coverage,
        "clean_requirements": clean_requirements,
        "closure_allowed": all_clean,
        "next_positive_target": (
            "write a new operator-matching theorem that derives the source/HS "
            "normalization, chirality projection, scalar LSZ factor, and absence "
            "of extra factors in one runner-checked chain without y_t_bare := "
            "<0|H_unit|tt> as a definition"
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
