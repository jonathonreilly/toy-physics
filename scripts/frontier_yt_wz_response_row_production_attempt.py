#!/usr/bin/env python3
"""
PR #230 W/Z response row production attempt.

This runner tries the next concrete W/Z item after the row-contract gate:
can the current PR #230 repo surface produce the required same-source W/Z
measurement rows now?  It does not synthesize rows.  It scans the current
top-correlator production harness, EW gauge-mass algebra, W/Z manifest,
builder/gate certificates, and the future row path.  If raw W/Z correlator
mass fits are absent, it records the exact production blocker and deliberately
does not write the future measurement-row file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_response_row_production_attempt_2026-05-03.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
EW_GAUGE_MASS_RUNNER = ROOT / "scripts" / "frontier_ew_higgs_gauge_mass_diagonalization.py"
EW_GAUGE_MASS_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"

PARENTS = {
    "wz_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "wz_repo_import_audit": "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json",
    "wz_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "wz_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "wz_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "wz_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 W/Z response row production attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    harness_text = read_text(PRODUCTION_HARNESS)
    ew_runner_text = read_text(EW_GAUGE_MASS_RUNNER)
    ew_note_text = read_text(EW_GAUGE_MASS_NOTE)

    future_rows_present = FUTURE_ROWS.exists()
    harness_has_wz_smoke_schema_path = all(
        token in harness_text
        for token in (
            "--wz-mass-response-smoke",
            "smoke_schema_enabled_not_ew_production",
            "synthetic_scout_contract_not_EW_field",
        )
    )
    harness_absent_guarded = (
        '"wz_mass_response"' in harness_text
        and "absent_guarded" in harness_text
        and "Static EW algebra, smoke" in harness_text
        and "physics evidence" in harness_text
    )
    harness_has_raw_wz_correlator_path = any(
        token in harness_text
        for token in (
            "wz_correlator_measurement",
            "gauge_mass_response_analysis",
            "fit_wz_mass_correlator",
            "wz_effective_mass_plateau",
        )
    ) or (
        "--wz-source-shifts" in harness_text
        and not harness_has_wz_smoke_schema_path
    )
    ew_is_static_algebra = (
        "Object-level verifier for the EW Higgs gauge-mass diagonalization theorem" in ew_runner_text
        and "does not use numerical electroweak pole masses" in ew_runner_text
        and "M_W = g_2 v / 2" in ew_note_text
    )
    contract_ready_but_not_evidence = (
        "WZ response measurement-row contract gate" in status(certs["wz_row_contract"])
        and certs["wz_row_contract"].get("wz_measurement_row_contract_gate_passed") is False
    )
    repo_import_blocks_hidden_harness = (
        certs["wz_repo_import_audit"].get("repo_wz_response_harness_found") is False
        and certs["wz_repo_import_audit"].get("exact_negative_boundary_passed") is True
    )
    builder_rows_absent = (
        "same-source WZ response rows absent" in status(certs["wz_builder"])
        and certs["wz_builder"].get("input_present") is False
        and certs["wz_builder"].get("candidate_written") is False
    )
    same_source_gate_not_passed = (
        "same-source WZ response certificate gate not passed" in status(certs["wz_gate"])
        and certs["wz_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    identity_blockers_active = (
        "same-source sector-overlap identity obstruction" in status(certs["sector_overlap"])
        and "FH gauge-response mixed-scalar obstruction" in status(certs["mixed_scalar"])
    )
    can_write_rows = (
        not missing
        and not proposal_allowed
        and future_rows_present
        and harness_has_raw_wz_correlator_path
        and not builder_rows_absent
        and not same_source_gate_not_passed
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("future-measurement-row-file-absent", not future_rows_present, display(FUTURE_ROWS))
    report("top-production-harness-wz-absent-guarded", harness_absent_guarded, display(PRODUCTION_HARNESS))
    report("top-production-harness-lacks-raw-wz-correlator-path", not harness_has_raw_wz_correlator_path, "no W/Z mass-fit CLI or analysis path")
    report("ew-gauge-mass-runner-is-static-algebra-only", ew_is_static_algebra, display(EW_GAUGE_MASS_RUNNER))
    report("row-contract-ready-but-not-evidence", contract_ready_but_not_evidence, status(certs["wz_row_contract"]))
    report("repo-import-audit-blocks-hidden-harness", repo_import_blocks_hidden_harness, status(certs["wz_repo_import_audit"]))
    report("builder-still-records-rows-absent", builder_rows_absent, status(certs["wz_builder"]))
    report("same-source-wz-gate-still-not-passed", same_source_gate_not_passed, status(certs["wz_gate"]))
    report("identity-blockers-still-active", identity_blockers_active, "sector-overlap and mixed-scalar gates remain active")
    report("does-not-write-future-row-file", not can_write_rows and not future_rows_present, display(FUTURE_ROWS))

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ response row production attempt on current surface",
        "verdict": (
            "The current PR #230 surface cannot produce same-source W/Z "
            "measurement rows. The top production harness explicitly marks "
            "W/Z mass response absent; no raw W/Z correlator mass-fit path or "
            "gauge_mass_response_analysis output exists; the EW gauge-mass "
            "runner is static tree-level algebra after canonical H is supplied; "
            "and the builder/gate still see no measurement rows. The future row "
            "file is deliberately not written."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No raw W/Z correlator mass fits, sector-overlap identity, or canonical-Higgs identity are present.",
        "production_attempt_closes_pr230": False,
        "measurement_rows_written": False,
        "future_rows_path": display(FUTURE_ROWS),
        "raw_wz_correlator_path_present": harness_has_raw_wz_correlator_path,
        "current_surface_inputs": {
            "production_harness": display(PRODUCTION_HARNESS),
            "ew_gauge_mass_runner": display(EW_GAUGE_MASS_RUNNER),
            "parent_certificates": PARENTS,
        },
        "blocked_requirements": [
            "same-source W/Z correlator mass fits by source shift",
            "fitted dM_W/ds or dM_Z/ds with covariance against dE_top/ds",
            "same-source sector-overlap identity",
            "canonical-Higgs pole identity",
            "retained-route gate or proposal gate",
        ],
        "strict_non_claims": [
            "does not write or synthesize W/Z measurement rows",
            "does not treat static EW gauge-mass algebra as dM_W/ds",
            "does not use observed W/Z, observed top, observed y_t, or observed g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, u0, c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Implement a genuine EW gauge/Higgs same-source correlator harness "
            "or return to certified O_H/C_sH/C_HH pole rows, Schur rows, or "
            "honest production evidence. Do not attempt to convert static EW "
            "algebra or QCD-only top chunks into W/Z response rows."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
