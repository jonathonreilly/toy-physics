#!/usr/bin/env python3
"""
PR #230 minimal-axioms Yukawa-summary firewall.

The current minimal-axioms memo summarizes the historical top-Yukawa lane and
still contains old "derived y_t" language.  This runner checks that PR #230
does not treat that summary memo as independent top-Yukawa authority.  The
memo can be cited as framework/input context only; the audited Ward/H_unit
failure remains the operative y_t boundary.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_minimal_axioms_yukawa_summary_firewall_2026-05-05.json"
)

TEXTS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "yt_ward_identity": "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md",
}

PARENTS = {
    "audit_ledger": "docs/audit/data/audit_ledger.json",
    "assumption_stress": "outputs/yt_pr230_assumption_import_stress_2026-05-01.json",
    "oh_source_higgs_authority_rescan": "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def read_rel(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def ledger_row(ledger: dict[str, Any], claim_id: str) -> dict[str, Any]:
    rows = ledger.get("rows", {})
    row = rows.get(claim_id, {})
    return row if isinstance(row, dict) else {}


def forbidden_summary_rows() -> list[dict[str, Any]]:
    return [
        {
            "memo_claim": "retained exact lattice-scale y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)",
            "why_not_pr230_authority": "routes through the audited Ward/H_unit structural-identification lane",
            "allowed_use": "historical context only",
        },
        {
            "memo_claim": "derived y_t(v) = 0.9176",
            "why_not_pr230_authority": "depends on the old top-Yukawa chain and downstream running/matching",
            "allowed_use": "comparator or stale summary only, not a proof input",
        },
        {
            "memo_claim": "derived m_t(pole) = 172.57 GeV",
            "why_not_pr230_authority": "depends on the old top-Yukawa chain and downstream running/matching",
            "allowed_use": "comparator or stale summary only, not a proof input",
        },
    ]


def firewall() -> dict[str, bool]:
    return {
        "uses_minimal_axioms_yukawa_summary_as_authority": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_hunit_matrix_element_readout": False,
        "uses_observed_top_or_yukawa_targets": False,
        "uses_alpha_lm_plaquette_u0_or_rconn": False,
        "defines_yt_bare": False,
        "sets_kappa_s_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 minimal-axioms Yukawa-summary firewall")
    print("=" * 72)

    texts = {name: read_rel(path) for name, path in TEXTS.items()}
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_texts = [name for name, text in texts.items() if not text]
    missing_parents = [name for name, cert in parents.items() if not cert]

    ledger = parents["audit_ledger"]
    minimal_row = ledger_row(ledger, "minimal_axioms_2026-04-11")
    ward_row = ledger_row(ledger, "yt_ward_identity_derivation_theorem")
    assumption = parents["assumption_stress"]
    rescan = parents["oh_source_higgs_authority_rescan"]
    assembly = parents["full_positive_assembly"]
    retained = parents["retained_route"]

    minimal_contains_old_yt_summary = (
        "retained exact lattice-scale `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`"
        in texts["minimal_axioms"]
        and "derived `y_t(v) = 0.9176`" in texts["minimal_axioms"]
        and "derived `m_t(pole) = 172.57 GeV`" in texts["minimal_axioms"]
    )
    minimal_audit_not_clean = (
        minimal_row.get("claim_id") == "minimal_axioms_2026-04-11"
        and minimal_row.get("effective_status") != "audited_clean"
        and minimal_row.get("audit_status") != "audited_clean"
    )
    minimal_rationale_forbids_propagation = (
        "the note may be cited as conditional/supporting local structure"
        in str(minimal_row.get("verdict_rationale", ""))
        and "no retained or promoted audit status propagates"
        in str(minimal_row.get("verdict_rationale", ""))
    )
    ward_audit_renaming = (
        ward_row.get("claim_id") == "yt_ward_identity_derivation_theorem"
        and ward_row.get("effective_status") == "audited_renaming"
        and "H_unit matrix element" in str(ward_row.get("verdict_rationale", ""))
    )
    ward_note_demoted = (
        "audit_status=audited_renaming" in texts["yt_ward_identity"]
        and "not a first-principles derivation" in texts["yt_ward_identity"]
    )
    assumption_already_bans_ward = (
        assumption.get("proposal_allowed") is False
        and "yt_ward_identity" in str(assumption.get("verdict", ""))
        and "H_unit" in str(assumption.get("verdict", ""))
    )
    current_oh_rescan_still_absent = (
        rescan.get("proposal_allowed") is False
        and rescan.get("oh_source_higgs_authority_found") is False
        and rescan.get("canonical_oh_absent") is True
        and rescan.get("source_higgs_rows_absent") is True
    )
    aggregate_gates_open = (
        assembly.get("proposal_allowed") is False
        and retained.get("proposal_allowed") is False
    )
    clean_firewall = all(value is False for value in firewall().values())
    exact_negative_boundary_passed = (
        not missing_texts
        and not missing_parents
        and minimal_contains_old_yt_summary
        and minimal_audit_not_clean
        and minimal_rationale_forbids_propagation
        and ward_audit_renaming
        and ward_note_demoted
        and assumption_already_bans_ward
        and current_oh_rescan_still_absent
        and aggregate_gates_open
        and clean_firewall
    )

    report("text-surfaces-present", not missing_texts, f"missing={missing_texts}")
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("minimal-axioms-contains-old-yukawa-summary", minimal_contains_old_yt_summary, TEXTS["minimal_axioms"])
    report("minimal-axioms-audit-not-clean", minimal_audit_not_clean, str({k: minimal_row.get(k) for k in ("audit_status", "effective_status")}))
    report("minimal-axioms-rationale-forbids-propagation", minimal_rationale_forbids_propagation, str(minimal_row.get("verdict_rationale", ""))[:220])
    report("yt-ward-audit-renaming-loaded", ward_audit_renaming, str({k: ward_row.get(k) for k in ("audit_status", "effective_status")}))
    report("yt-ward-note-demoted", ward_note_demoted, TEXTS["yt_ward_identity"])
    report("assumption-stress-already-bans-ward-hunit", assumption_already_bans_ward, assumption.get("actual_current_surface_status", ""))
    report("current-oh-source-higgs-authority-still-absent", current_oh_rescan_still_absent, rescan.get("actual_current_surface_status", ""))
    report("aggregate-gates-still-open", aggregate_gates_open, "proposal_allowed=false")
    report("minimal-axioms-yukawa-summary-not-used", clean_firewall, str(firewall()))
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "summary memo is context only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / minimal-axioms Yukawa summary is not PR230 proof authority"
        ),
        "verdict": (
            "MINIMAL_AXIOMS_2026-04-11 remains useful framework context, but "
            "its historical y_t and m_t summary cannot be imported as a PR230 "
            "closure proof.  The memo's own audit row is not clean, and the "
            "load-bearing y_t lane it summarizes is the audited_renaming "
            "Ward/H_unit matrix-element identification.  PR230 still needs a "
            "same-surface O_H/source-Higgs bridge, W/Z response bridge, Schur "
            "rows, neutral irreducibility theorem, or strict scalar-LSZ plus "
            "overlap authority."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A framework summary memo is not an independent derivation and "
            "the summarized y_t chain is explicitly audit-demoted."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "minimal_axioms_audit_status": {
            "audit_status": minimal_row.get("audit_status"),
            "effective_status": minimal_row.get("effective_status"),
            "verdict_rationale_excerpt": str(minimal_row.get("verdict_rationale", ""))[:500],
        },
        "yt_ward_audit_status": {
            "audit_status": ward_row.get("audit_status"),
            "effective_status": ward_row.get("effective_status"),
            "verdict_rationale_excerpt": str(ward_row.get("verdict_rationale", ""))[:500],
        },
        "forbidden_summary_rows": forbidden_summary_rows(),
        "forbidden_firewall": firewall(),
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not use MINIMAL_AXIOMS y_t/m_t summary as proof input",
            "does not use H_unit or yt_ward_identity as y_t authority",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, R_conn, kappa_s=1, c2=1, or Z_match=1",
            "does not edit MINIMAL_AXIOMS or promote/demote any audit ledger row",
        ],
        "exact_next_action": (
            "Continue only with genuine bridge artifacts: canonical O_H and "
            "C_sH/C_HH rows, same-source W/Z rows with covariance and g2, "
            "Schur A/B/C rows, neutral primitive/irreducibility, or strict "
            "scalar-LSZ plus overlap authority."
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
