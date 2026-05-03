#!/usr/bin/env python3
"""
PR #230 legacy Schur bridge import audit.

The repo already contains a YT Schur normal-form / stability /
microscopic-admissibility stack.  This audit checks whether that older stack is
the missing PR #230 physical top-Yukawa closure.  It is not: the stack is a
bounded UV-transport/coarse-operator support lane, uses the older alpha_LM /
plaquette / y_t = g3/sqrt(6) transport setup, and does not supply the new
same-surface Schur A/B/C kernel rows, source-Higgs pole rows, or W/Z response
rows required by PR #230.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_legacy_schur_bridge_import_audit_2026-05-03.json"
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

LEGACY_CLAIMS = {
    "yt_exact_schur_normal_form_uniqueness_note": {
        "runner": "scripts/frontier_yt_exact_schur_normal_form_uniqueness.py",
        "note": "docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md",
    },
    "yt_schur_stability_gap_note": {
        "runner": "scripts/frontier_yt_schur_stability_gap.py",
        "note": "docs/YT_SCHUR_STABILITY_GAP_NOTE.md",
    },
    "yt_microscopic_schur_class_admissibility_note": {
        "runner": "scripts/frontier_yt_microscopic_schur_class_admissibility.py",
        "note": "docs/YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md",
    },
}

PARENTS = {
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_row_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
}

FORBIDDEN_AS_PR230_INPUT_TOKENS = [
    "ALPHA_LM",
    "PLAQ",
    "U0",
    "YT_PL = G3_PL / np.sqrt(6.0)",
    "V_DERIVED",
]

REQUIRED_PR230_EVIDENCE_TOKENS = [
    "schur_kprime_kernel_rows",
    "A_at_pole",
    "B_at_pole",
    "C_at_pole",
    "C_sH",
    "C_HH",
    "wz_mass_response",
]

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_text(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def ledger_rows() -> dict[str, Any]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = data.get("rows", {})
    return rows if isinstance(rows, dict) else {}


def main() -> int:
    print("PR #230 legacy Schur bridge import audit")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    rows = ledger_rows()

    legacy_rows: dict[str, dict[str, Any]] = {}
    source_audits: dict[str, Any] = {}
    missing_legacy = []
    for claim_id, files in LEGACY_CLAIMS.items():
        row = rows.get(claim_id)
        if not isinstance(row, dict):
            missing_legacy.append(claim_id)
            row = {}
        legacy_rows[claim_id] = {
            "current_status_raw": row.get("current_status_raw"),
            "audit_status": row.get("audit_status"),
            "effective_status": row.get("effective_status"),
            "runner_path": row.get("runner_path"),
            "verdict_rationale": row.get("verdict_rationale"),
        }
        runner_text = load_text(files["runner"])
        note_text = load_text(files["note"])
        source_audits[claim_id] = {
            "runner": files["runner"],
            "note": files["note"],
            "forbidden_as_pr230_input_tokens_present": [
                token for token in FORBIDDEN_AS_PR230_INPUT_TOKENS if token in runner_text
            ],
            "pr230_evidence_tokens_present": [
                token for token in REQUIRED_PR230_EVIDENCE_TOKENS if token in runner_text
            ],
            "note_says_bounded_support": "bounded" in note_text.lower()
            or "support" in note_text.lower(),
            "note_says_retained_closure": "retained closure" in note_text.lower(),
        }

    legacy_statuses_not_clean = all(
        legacy_rows[claim_id].get("effective_status") not in {"audited_clean", "retained"}
        and legacy_rows[claim_id].get("audit_status") != "audited_clean"
        for claim_id in LEGACY_CLAIMS
    )
    exact_normal_form_conditional = (
        legacy_rows["yt_exact_schur_normal_form_uniqueness_note"].get("audit_status")
        == "audited_conditional"
    )
    support_or_bounded_notes = all(
        source_audits[claim_id]["note_says_bounded_support"] for claim_id in LEGACY_CLAIMS
    )
    legacy_uses_old_transport_tokens = bool(
        source_audits["yt_exact_schur_normal_form_uniqueness_note"][
            "forbidden_as_pr230_input_tokens_present"
        ]
    )
    no_pr230_evidence_rows = all(
        not source_audits[claim_id]["pr230_evidence_tokens_present"]
        for claim_id in (
            "yt_exact_schur_normal_form_uniqueness_note",
            "yt_schur_stability_gap_note",
            "yt_microscopic_schur_class_admissibility_note",
        )
    )
    schur_row_guard_blocks = (
        "Schur K-prime row absence guard" in status(parents["schur_row_absence_guard"])
        and parents["schur_row_absence_guard"].get("current_schur_kernel_rows_present") is False
    )
    schur_sufficiency_not_closure = (
        "Schur-complement K-prime sufficiency theorem" in status(parents["schur_kprime_sufficiency"])
        and parents["schur_kprime_sufficiency"].get("current_closure_gate_passed") is False
    )
    retained_still_open = "retained closure not yet reached" in status(parents["retained_route"])

    legacy_import_closes_pr230 = False
    exact_negative_boundary_passed = (
        not missing_parents
        and not proposal_allowed
        and not missing_legacy
        and legacy_statuses_not_clean
        and exact_normal_form_conditional
        and support_or_bounded_notes
        and legacy_uses_old_transport_tokens
        and no_pr230_evidence_rows
        and schur_row_guard_blocks
        and schur_sufficiency_not_closure
        and retained_still_open
        and not legacy_import_closes_pr230
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("legacy-ledger-rows-present", not missing_legacy, f"missing={missing_legacy}")
    report("legacy-statuses-not-clean", legacy_statuses_not_clean, str(legacy_rows))
    report("exact-normal-form-is-audited-conditional", exact_normal_form_conditional, legacy_rows["yt_exact_schur_normal_form_uniqueness_note"].get("audit_status"))
    report("legacy-notes-are-support-bounded", support_or_bounded_notes, "bounded/support note language")
    report("legacy-stack-uses-old-transport-tokens", legacy_uses_old_transport_tokens, str(source_audits["yt_exact_schur_normal_form_uniqueness_note"]["forbidden_as_pr230_input_tokens_present"]))
    report("legacy-stack-does-not-emit-pr230-evidence-rows", no_pr230_evidence_rows, "no A/B/C, C_sH/C_HH, or W/Z row tokens in legacy runners")
    report("schur-row-guard-blocks-current-import", schur_row_guard_blocks, status(parents["schur_row_absence_guard"]))
    report("schur-sufficiency-is-not-closure", schur_sufficiency_not_closure, status(parents["schur_kprime_sufficiency"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_route"]))
    report("legacy-schur-import-does-not-close-pr230", not legacy_import_closes_pr230, f"legacy_import_closes_pr230={legacy_import_closes_pr230}")
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "legacy Schur bridge is not PR230 closure")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / legacy Schur bridge stack is not PR230 y_t closure"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The legacy Schur bridge stack is bounded/conditional support for "
            "the older UV-transport bridge and does not supply PR230 physical "
            "observable rows."
        ),
        "bare_retained_allowed": False,
        "legacy_schur_import_closes_pr230": legacy_import_closes_pr230,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "legacy_rows": legacy_rows,
        "source_audits": source_audits,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not import alpha_LM, plaquette, u0, or y_t=g3/sqrt(6) transport as PR230 evidence",
            "does not treat Schur normal-form/stability/admissibility support as Schur A/B/C kernel rows",
            "does not use H_unit, yt_ward_identity, observed targets, or reduced pilots",
        ],
        "exact_next_action": (
            "Continue with actual PR230 positive evidence: explicit same-surface "
            "Schur A/B/C rows, certified O_H/C_sH/C_HH pole rows, or same-source "
            "W/Z response rows with identity certificates."
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
