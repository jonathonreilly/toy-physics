#!/usr/bin/env python3
"""
PR #230 W/Z response harness implementation plan gate.

The same-source W/Z response lane can bypass the scalar-source normalization
only if it measures a real W/Z mass response under the same source coordinate
used for the top Feynman-Hellmann row.  Existing certificates already block
static EW algebra and the QCD-only production harness.  This runner turns that
blocked fallback into an executable engineering plan without manufacturing any
measurement rows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_response_harness_implementation_plan_2026-05-04.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"

PARENTS = {
    "wz_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "wz_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
    "wz_repo_import_audit": "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json",
    "wz_absence_guard": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "wz_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "wz_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "wz_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
    "rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def implementation_plan() -> list[dict[str, Any]]:
    return [
        {
            "id": "ew_same_source_action",
            "deliverable": "Define the same-source EW gauge/Higgs action block used by the W/Z response run.",
            "required_rows_or_certificates": [
                "SU(2)xU(1) or retained-equivalent gauge-sector action on the Cl(3)/Z3 substrate",
                "scalar source s coupled to the canonical Higgs radial direction, not to H_unit",
                "same-source-coordinate certificate tying this source to the top FH source",
                "firewall certificate excluding observed W/Z/top/y_t selectors and Ward/H_unit authority",
            ],
            "claim_status_after_done": "setup support only",
        },
        {
            "id": "wz_correlator_mass_fits",
            "deliverable": "Measure W/Z correlators at negative, zero, and positive source shifts.",
            "required_rows_or_certificates": [
                "W_or_Z_correlator_mass_fits_by_source_shift",
                "fit windows or effective-mass plateaus with jackknife/bootstrap errors",
                "production phase and seed/run-control metadata",
                "finite-volume and fit-window systematic rows",
            ],
            "claim_status_after_done": "measurement support only",
        },
        {
            "id": "top_wz_covariance",
            "deliverable": "Fit dE_top/ds and dM_W/ds or dM_Z/ds on matched configurations.",
            "required_rows_or_certificates": [
                "slope_dM_W_ds or slope_dM_Z_ds with slope_error",
                "cov_dE_top_dM_W or cov_dE_top_dM_Z",
                "source-shift covariance matrix",
                "no use of static dM_W/dh as dM_W/ds",
            ],
            "claim_status_after_done": "response support only",
        },
        {
            "id": "sector_identity",
            "deliverable": "Prove the measured W/Z response and top response are on the same canonical-Higgs pole sector.",
            "required_rows_or_certificates": [
                "same_source_sector_overlap_identity_passed",
                "canonical_higgs_pole_identity_passed",
                "orthogonal neutral top-coupling null direction removed or measured",
                "retained-route/proposal gate still false until all checks pass",
            ],
            "claim_status_after_done": "identity support; not closure until gate passes",
        },
        {
            "id": "builder_gate_integration",
            "deliverable": "Write the future W/Z measurement row file and feed the existing builder/gate stack.",
            "required_rows_or_certificates": [
                "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
                "frontier_yt_fh_gauge_mass_response_certificate_builder.py pass",
                "frontier_yt_same_source_wz_response_certificate_gate.py pass",
                "frontier_yt_retained_closure_route_certificate.py decides claim status",
            ],
            "claim_status_after_done": "audit-decided; no branch-local retained wording",
        },
    ]


def shortcut_rejections() -> list[dict[str, str]]:
    return [
        {
            "shortcut": "static EW gauge-mass algebra",
            "reason": "It supplies dM_W/dh after canonical H is assumed, not measured dM_W/ds under the PR230 source.",
        },
        {
            "shortcut": "QCD top-correlator harness W/Z absent guard",
            "reason": "The guard records missing W/Z rows; it is not a W/Z correlator or mass-response measurement.",
        },
        {
            "shortcut": "generic W/Z slope without sector identity",
            "reason": "The ratio still reads y_t times an unknown top/gauge source-overlap factor.",
        },
        {
            "shortcut": "observed W/Z, top, y_t, or g2 selectors",
            "reason": "External values are comparators only and cannot select the source overlap.",
        },
        {
            "shortcut": "H_unit or yt_ward_identity",
            "reason": "This re-enters the audited matrix-element renaming trap.",
        },
    ]


def main() -> int:
    print("PR #230 W/Z response harness implementation plan gate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    harness_text = PRODUCTION_HARNESS.read_text(encoding="utf-8") if PRODUCTION_HARNESS.exists() else ""
    plan = implementation_plan()
    rejections = shortcut_rejections()

    row_contract_ready = (
        "WZ response measurement-row contract gate" in status(certs["wz_row_contract"])
        and certs["wz_row_contract"].get("wz_measurement_row_contract_gate_passed") is False
    )
    production_attempt_negative = (
        "WZ response row production attempt" in status(certs["wz_row_production_attempt"])
        and certs["wz_row_production_attempt"].get("measurement_rows_written") is False
    )
    repo_audit_negative = (
        certs["wz_repo_import_audit"].get("repo_wz_response_harness_found") is False
        and certs["wz_repo_import_audit"].get("exact_negative_boundary_passed") is True
    )
    absence_guard_status = status(certs["wz_absence_guard"])
    absence_guard_present = (
        (
            "W/Z response harness absence guard" in absence_guard_status
            or "WZ response harness absence guard" in absence_guard_status
        )
        and certs["wz_absence_guard"].get("proposal_allowed") is False
    )
    builder_rows_absent = (
        "same-source WZ response rows absent" in status(certs["wz_builder"])
        and certs["wz_builder"].get("input_present") is False
    )
    gate_open = (
        "same-source WZ response certificate gate not passed" in status(certs["wz_gate"])
        and certs["wz_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    identity_blockers_present = (
        "same-source sector-overlap identity obstruction" in status(certs["sector_overlap"])
        and "FH gauge-response mixed-scalar obstruction" in status(certs["mixed_scalar"])
    )
    rank_repair_requires_wz_identity = (
        "non-source response rank-repair sufficiency theorem" in status(certs["rank_repair"])
        and certs["rank_repair"].get("current_closure_gate_passed") is False
    )
    retained_route_open = (
        "closure not yet reached" in status(certs["retained_route"])
        and certs["retained_route"].get("proposal_allowed") is False
    )
    qcd_harness_has_wz_absent_guard = (
        '"wz_mass_response"' in harness_text
        and '"implementation_status": "absent_guarded"' in harness_text
    )
    qcd_harness_has_real_wz_cli = any(
        token in harness_text
        for token in (
            "--wz-source-shifts",
            "fit_wz_mass_correlator",
            "gauge_mass_response_analysis",
            "wz_correlator_measurement",
        )
    )
    future_rows_written = FUTURE_ROWS.exists()
    plan_complete = len(plan) == 5 and all(row["required_rows_or_certificates"] for row in plan)

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("wz-row-contract-ready-as-future-gate", row_contract_ready, status(certs["wz_row_contract"]))
    report("current-row-production-attempt-negative", production_attempt_negative, status(certs["wz_row_production_attempt"]))
    report("repo-audit-finds-no-hidden-wz-harness", repo_audit_negative, status(certs["wz_repo_import_audit"]))
    report("absence-guard-present-not-evidence", absence_guard_present, status(certs["wz_absence_guard"]))
    report("builder-rows-absent", builder_rows_absent, status(certs["wz_builder"]))
    report("same-source-wz-gate-open", gate_open, status(certs["wz_gate"]))
    report("identity-blockers-present", identity_blockers_present, "sector-overlap and mixed-scalar blockers active")
    report("rank-repair-requires-identity", rank_repair_requires_wz_identity, status(certs["rank_repair"]))
    report("retained-route-still-open", retained_route_open, status(certs["retained_route"]))
    report("qcd-harness-has-wz-absent-guard", qcd_harness_has_wz_absent_guard, display(PRODUCTION_HARNESS))
    report("qcd-harness-has-no-real-wz-cli", not qcd_harness_has_real_wz_cli, "no W/Z mass-response CLI path")
    report("future-row-file-not-written", not future_rows_written, display(FUTURE_ROWS))
    report("implementation-plan-complete", plan_complete, f"work_units={len(plan)}")

    result = {
        "actual_current_surface_status": "bounded-support / WZ response harness implementation plan",
        "verdict": (
            "The W/Z fallback route is now reduced to concrete engineering "
            "work units.  Current PR230 still has no same-source W/Z mass "
            "response rows: the QCD top harness only emits an absent guard, the "
            "repo-wide audit finds no hidden W/Z harness, and the builder/gate "
            "remain open.  The plan names the required EW action, W/Z correlator "
            "mass fits, matched top/WZ covariance, sector-identity certificates, "
            "and builder integration.  It does not write measurement rows or "
            "authorize retained/proposed-retained wording."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Implementation planning is support only; no production W/Z rows or identity certificates exist.",
        "bare_retained_allowed": False,
        "future_rows_path": display(FUTURE_ROWS),
        "future_rows_written": future_rows_written,
        "qcd_harness_has_wz_absent_guard": qcd_harness_has_wz_absent_guard,
        "qcd_harness_has_real_wz_cli": qcd_harness_has_real_wz_cli,
        "implementation_work_units": plan,
        "shortcut_rejections": rejections,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write or synthesize W/Z measurement rows",
            "does not treat static EW gauge-mass algebra as dM_W/ds",
            "does not treat the QCD harness absent guard as evidence",
            "does not set kappa_s = 1, k_top = k_gauge, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Choose whether to actually implement the EW same-source W/Z "
            "correlator harness as a new production workstream.  Until then, "
            "continue FH/LSZ chunks and the source-Higgs/Schur/rank-one routes."
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
