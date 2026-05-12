#!/usr/bin/env python3
"""
PR #230 origin/main YT_WARD Step 3 open-gate intake guard.

origin/main now contains an independently audited-clean YT_WARD Step 3
coefficient-bookkeeping diagnostic.  Its effective status is open_gate: it
reduces the proposed same-1PI equality to a gate equation, while explicitly
leaving the same-amputated-1PI bridge unproved.

This runner checks whether that upstream audit movement changes PR230's
current O_H/source-Higgs closure state.  Expected verdict: no.  The audited
Step 3 row is useful provenance for the Ward/g_bare lane, but it is not a
canonical-Higgs operator certificate, not C_sH/C_HH source-Higgs evidence, and
not scalar LSZ/pole normalization authority for PR230.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_origin_main_yt_ward_step3_open_gate_intake_guard_2026-05-12.json"
)

REMOTE_MAIN = "origin/main"
WARD_STEP3_NOTE = "docs/YT_WARD_STEP3_SAME_1PI_CONSTRUCTION_NARROW_THEOREM_NOTE_2026-05-10.md"
WARD_STEP3_RUNNER = "scripts/yt_ward_step3_same_1pi_construction_2026_05_10.py"
AUDIT_LEDGER = "docs/audit/data/audit_ledger.json"
CLAIM_ID = "yt_ward_step3_same_1pi_construction_narrow_theorem_note_2026-05-10"

PARENTS = {
    "same_1pi_scalar_pole_boundary": "outputs/yt_same_1pi_scalar_pole_boundary_2026-05-01.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def git(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return ""


def git_path_exists(ref: str, rel: str) -> bool:
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{rel}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def read_remote(rel: str) -> str:
    return git(["show", f"{REMOTE_MAIN}:{rel}"])


def load_remote_json(rel: str) -> dict[str, Any]:
    text = read_remote(rel)
    if not text:
        return {}
    data = json.loads(text)
    return data if isinstance(data, dict) else {}


def load_local_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def forbidden_firewall() -> dict[str, bool]:
    return {
        "treated_yt_ward_step3_as_pr230_oh_certificate": False,
        "treated_hunit_projection_as_canonical_oh": False,
        "treated_same_1pi_coefficient_as_scalar_lsz_normalization": False,
        "treated_open_gate_as_retained_closure": False,
        "used_yt_ward_identity_as_load_bearing_pr230_input": False,
        "used_y_t_bare_or_hunit_matrix_element_readout": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 origin/main YT_WARD Step 3 open-gate intake guard")
    print("=" * 82)

    note_text = read_remote(WARD_STEP3_NOTE)
    runner_text = read_remote(WARD_STEP3_RUNNER)
    ledger = load_remote_json(AUDIT_LEDGER)
    rows = ledger.get("rows", {}) if isinstance(ledger, dict) else {}
    row = rows.get(CLAIM_ID, {})
    certs = {name: load_local_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    failing_parents = [
        name for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    firewall = forbidden_firewall()

    remote_paths_present = (
        git_path_exists(REMOTE_MAIN, WARD_STEP3_NOTE)
        and git_path_exists(REMOTE_MAIN, WARD_STEP3_RUNNER)
        and git_path_exists(REMOTE_MAIN, AUDIT_LEDGER)
    )
    note_scope_is_open_gate = (
        "**Type:** open_gate" in note_text
        and "same-1PI bridge remains" in note_text
        and "itself prove that the OGE representation" in note_text
        and "Does **not** derive `g_bare = 1`" in note_text
        and "Does **not** prove the Standard Model top-Yukawa observable" in note_text
    )
    runner_scope_is_diagnostic = (
        "intentionally does not assert" in runner_text
        and "same Green's function" in runner_text
        and "same-1PI bridge remains" in runner_text
        and "TOTAL: PASS=" in runner_text
        and "FAIL" in runner_text
    )
    audit_row_is_clean_open_gate = (
        row.get("audit_status") == "audited_clean"
        and row.get("effective_status") == "open_gate"
        and row.get("claim_type") == "open_gate"
        and row.get("note_path") == WARD_STEP3_NOTE
        and row.get("runner_path") == WARD_STEP3_RUNNER
        and "same-1PI bridge" in str(row.get("open_dependency_paths", []))
    )
    audit_row_not_positive_yt = (
        "does not claim to derive g_bare=1" in row.get("chain_closure_explanation", "")
        or "does not derive g_bare=1" in row.get("notes_for_re_audit_if_any", "")
        or "proving the Standard Model top-Yukawa observable" in row.get(
            "notes_for_re_audit_if_any", ""
        )
    )
    same_1pi_boundary_still_blocks_pr230 = (
        "same-1PI not PR230 closure" in statuses["same_1pi_scalar_pole_boundary"]
        and certs["same_1pi_scalar_pole_boundary"].get("proposal_allowed") is False
        and "scalar LSZ" in certs["same_1pi_scalar_pole_boundary"].get(
            "proposal_allowed_reason", ""
        )
    )
    canonical_oh_absent = (
        "canonical-Higgs operator certificate absent"
        in statuses["canonical_higgs_operator_gate"]
        and certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    source_higgs_rows_absent = (
        "source-Higgs production launch blocked by missing O_H certificate"
        in statuses["source_higgs_readiness"]
        and certs["source_higgs_readiness"].get("operator_certificate_present") is False
        and certs["source_higgs_readiness"].get("future_rows_present") is False
        and certs["source_higgs_readiness"].get("proposal_allowed") is False
    )
    gram_postprocess_waits = (
        "awaiting production certificate"
        in statuses["source_higgs_gram_postprocess"]
        and certs["source_higgs_gram_postprocess"].get("candidate_present") is False
        and certs["source_higgs_gram_postprocess"].get(
            "source_higgs_gram_purity_gate_passed"
        )
        is False
    )
    aggregate_gates_still_open = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in firewall.values())

    guard_passed = all(
        [
            remote_paths_present,
            note_scope_is_open_gate,
            runner_scope_is_diagnostic,
            audit_row_is_clean_open_gate,
            audit_row_not_positive_yt,
            not missing_parents,
            not failing_parents,
            not proposal_parents,
            same_1pi_boundary_still_blocks_pr230,
            canonical_oh_absent,
            source_higgs_rows_absent,
            gram_postprocess_waits,
            aggregate_gates_still_open,
            firewall_clean,
        ]
    )

    report("origin-main-ward-step3-surfaces-present", remote_paths_present, WARD_STEP3_NOTE)
    report("ward-step3-note-scope-is-open-gate", note_scope_is_open_gate, "same-1PI bridge remains open")
    report("ward-step3-runner-scope-is-diagnostic", runner_scope_is_diagnostic, WARD_STEP3_RUNNER)
    report("audit-row-is-clean-open-gate", audit_row_is_clean_open_gate, f"{row.get('audit_status')} / {row.get('effective_status')}")
    report("audit-row-not-positive-yt", audit_row_not_positive_yt, row.get("notes_for_re_audit_if_any", ""))
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not failing_parents, f"failing={failing_parents}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("same-1pi-boundary-still-blocks-pr230", same_1pi_boundary_still_blocks_pr230, statuses["same_1pi_scalar_pole_boundary"])
    report("canonical-oh-certificate-still-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-rows-still-absent", source_higgs_rows_absent, statuses["source_higgs_readiness"])
    report("gram-postprocess-still-waits", gram_postprocess_waits, statuses["source_higgs_gram_postprocess"])
    report("aggregate-gates-still-open", aggregate_gates_still_open, statuses["full_positive_assembly"])
    report("forbidden-firewall-clean", firewall_clean, str(firewall))
    report("origin-main-ward-step3-open-gate-not-pr230-closure", guard_passed, "audited open_gate does not supply O_H/C_sH/C_HH")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / origin/main audited YT_WARD Step 3 row is "
            "an open_gate coefficient diagnostic, not PR230 O_H/source-Higgs closure"
        ),
        "conditional_surface_status": (
            "conditional-support only if a future Wick-level same-1PI bridge is "
            "combined with independent scalar pole/LSZ normalization and a "
            "canonical O_H/source-Higgs row authority accepted by PR230 gates"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The upstream row is audited_clean only as an open_gate.  It records "
            "coefficient bookkeeping and an unproved same-1PI bridge, while PR230 "
            "still lacks canonical O_H, C_sH/C_HH rows, scalar LSZ/pole "
            "normalization, and retained-route authorization."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "origin_main_yt_ward_step3_open_gate_intake_guard_passed": guard_passed,
        "origin_main": {
            "ref": REMOTE_MAIN,
            "note_path": WARD_STEP3_NOTE,
            "runner_path": WARD_STEP3_RUNNER,
            "claim_id": CLAIM_ID,
            "audit_status": row.get("audit_status"),
            "effective_status": row.get("effective_status"),
            "claim_type": row.get("claim_type"),
            "open_dependency_paths": row.get("open_dependency_paths"),
            "chain_closure_explanation": row.get("chain_closure_explanation"),
            "notes_for_re_audit_if_any": row.get("notes_for_re_audit_if_any"),
        },
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "open_imports": [
            "Wick-level same-1PI bridge, if using the Ward route at all",
            "independent scalar pole/LSZ normalization",
            "canonical O_H identity/normalization certificate",
            "production C_ss/C_sH/C_HH(tau) source-Higgs pole rows",
            "source-Higgs Gram/FV/IR/model-class authority",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not treat an audited open_gate as a positive theorem",
            "does not use YT_WARD Step 3 as load-bearing PR230 authority",
            "does not treat H_unit projection as canonical O_H",
            "does not define y_t_bare or y_t through a matrix element",
            "does not use observed top/y_t targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Keep PR230 on the existing positive routes: derive canonical O_H, "
            "measure/derive C_sH/C_HH pole rows with Gram purity, or supply an "
            "independent neutral-transfer/WZ physical-response bridge.  Do not "
            "use the origin/main Ward Step 3 audit-clean open_gate as closure."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and guard_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
