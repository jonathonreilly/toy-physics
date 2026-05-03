#!/usr/bin/env python3
"""
PR #230 repo-wide W/Z response harness import audit.

The same-source W/Z response route would be a physical-observable bypass if
the repo already had production W/Z correlator mass fits under the same scalar
source used for dE_top/ds.  This runner checks that possibility directly.

It does not manufacture W/Z rows and does not treat static electroweak algebra
as a source response.  Algebra/running/gauge-scope scripts are classified as
support unless they emit actual same-source W/Z mass-response measurement rows
with covariance and identity certificates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_response_repo_harness_import_audit_2026-05-03.json"

REQUIRED_OUTPUTS = {
    "measurement_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "candidate_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
}

CANDIDATES = [
    {
        "id": "yt_direct_lattice_correlator_production",
        "paths": ["scripts/yt_direct_lattice_correlator_production.py"],
        "classification": "QCD top-correlator harness with W/Z absent guard",
        "positive_reuse": "same-source top dE_top/ds rows and metadata guard",
        "missing_or_blocking": [
            "no W/Z gauge-boson correlator mass fits",
            "no gauge_mass_response_analysis output field",
            "W/Z metadata is absent_guarded and not evidence",
        ],
    },
    {
        "id": "ew_higgs_gauge_mass_diagonalization",
        "paths": [
            "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
            "scripts/frontier_ew_higgs_gauge_mass_diagonalization.py",
        ],
        "classification": "object-level EW algebra after canonical H is supplied",
        "positive_reuse": "tree-level W/Z mass dictionary once H is known",
        "missing_or_blocking": [
            "does not measure dM_W/ds under PR230 scalar source",
            "does not emit W/Z correlator mass fits",
            "does not prove source-sector overlap",
        ],
    },
    {
        "id": "fh_gauge_mass_response_manifest",
        "paths": [
            "scripts/frontier_yt_fh_gauge_mass_response_manifest.py",
            "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
        ],
        "classification": "acceptance manifest only",
        "positive_reuse": "minimum W/Z response schema and rejection rules",
        "missing_or_blocking": [
            "manifest_is_evidence=false",
            "no measurement rows or candidate certificate",
        ],
    },
    {
        "id": "fh_gauge_mass_response_observable_gap",
        "paths": [
            "scripts/frontier_yt_fh_gauge_mass_response_observable_gap.py",
            "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
        ],
        "classification": "current-surface observable gap",
        "positive_reuse": "sector-overlap countermodels and acceptance schema",
        "missing_or_blocking": [
            "gauge_mass_response_observable_ready=false",
            "W/Z response certificate absent",
        ],
    },
    {
        "id": "fh_gauge_mass_response_certificate_builder",
        "paths": [
            "scripts/frontier_yt_fh_gauge_mass_response_certificate_builder.py",
            "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
        ],
        "classification": "future-row certificate builder",
        "positive_reuse": "validates future measurement row schema",
        "missing_or_blocking": [
            "input_present=false",
            "candidate_written=false",
        ],
    },
    {
        "id": "same_source_wz_response_certificate_gate",
        "paths": [
            "scripts/frontier_yt_same_source_wz_response_certificate_gate.py",
            "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
        ],
        "classification": "future W/Z response acceptance gate",
        "positive_reuse": "rejects static EW algebra and slope-only W/Z rows",
        "missing_or_blocking": [
            "gate not passed",
            "future W/Z response certificate absent",
        ],
    },
    {
        "id": "wz_response_harness_absence_guard",
        "paths": [
            "scripts/frontier_yt_wz_response_harness_absence_guard.py",
            "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
        ],
        "classification": "explicit absence guard",
        "positive_reuse": "claim firewall in production certificates",
        "missing_or_blocking": [
            "guard marks missing evidence; it is not W/Z response evidence",
        ],
    },
    {
        "id": "ew_coupling_support_scan",
        "paths": ["scripts/frontier_yt_ew_coupling_derivation.py"],
        "classification": "EW running/coupling support scan",
        "positive_reuse": "possible g2 context after separate audit",
        "missing_or_blocking": [
            "does not measure W/Z mass response",
            "contains observed comparators and taste-threshold support inputs",
        ],
    },
    {
        "id": "native_gauge_scope",
        "paths": ["scripts/frontier_native_gauge_scope.py"],
        "classification": "native SU(2) Clifford-bivector scope theorem",
        "positive_reuse": "weak-gauge algebra context",
        "missing_or_blocking": [
            "does not implement electroweak gauge-boson correlators",
            "does not couple the PR230 scalar source to W/Z masses",
        ],
    },
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


def read_rel(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def candidate_status(candidate: dict[str, Any]) -> dict[str, Any]:
    texts = {rel: read_rel(rel) for rel in candidate["paths"]}
    combined = "\n".join(texts.values())
    json_payloads = {
        rel: load_json(rel) for rel in candidate["paths"] if rel.endswith(".json")
    }
    real_cli_tokens = [
        "--gauge-mass-response",
        "--wz-mass-response",
        "gauge_mass_response_analysis",
    ]
    real_row_tokens = [
        "slope_dM_W_ds",
        "slope_dM_Z_ds",
        "wz_mass_fits_from_correlators",
        "cov_dE_top_dM_W",
        "cov_dE_top_dM_Z",
    ]
    guard_only = "absent_guarded" in combined and "used_as_physical_yukawa_readout" in combined
    emits_real_rows = any(token in combined for token in real_cli_tokens) and all(
        token in combined for token in ("slope_dM_W_ds", "wz_mass_fits_from_correlators")
    )
    output_claims_evidence = any(
        payload.get("input_present") is True
        or payload.get("candidate_written") is True
        or payload.get("same_source_wz_response_certificate_gate_passed") is True
        or payload.get("manifest_is_evidence") is True
        for payload in json_payloads.values()
    )
    return {
        "id": candidate["id"],
        "paths": candidate["paths"],
        "path_presence": {rel: bool(texts[rel]) for rel in candidate["paths"]},
        "classification": candidate["classification"],
        "positive_reuse": candidate["positive_reuse"],
        "missing_or_blocking": candidate["missing_or_blocking"],
        "signals": {
            "has_real_cli_token": any(token in combined for token in real_cli_tokens),
            "has_real_row_token": any(token in combined for token in real_row_tokens),
            "has_all_required_row_tokens": all(token in combined for token in real_row_tokens[:4]),
            "guard_only": guard_only,
            "output_claims_evidence": output_claims_evidence,
        },
        "usable_as_wz_response_harness": emits_real_rows and output_claims_evidence,
    }


def main() -> int:
    print("PR #230 repo-wide W/Z response harness import audit")
    print("=" * 72)

    rows = [candidate_status(candidate) for candidate in CANDIDATES]
    missing_candidate_paths = [
        f"{row['id']}:{path}"
        for row in rows
        for path, present in row["path_presence"].items()
        if not present
    ]
    required_output_presence = {
        name: (ROOT / path).exists() for name, path in REQUIRED_OUTPUTS.items()
    }
    usable = [row["id"] for row in rows if row["usable_as_wz_response_harness"]]
    production_harness = next(row for row in rows if row["id"] == "yt_direct_lattice_correlator_production")
    ew_algebra = next(row for row in rows if row["id"] == "ew_higgs_gauge_mass_diagonalization")
    builder = next(row for row in rows if row["id"] == "fh_gauge_mass_response_certificate_builder")
    gate = next(row for row in rows if row["id"] == "same_source_wz_response_certificate_gate")
    guard = next(row for row in rows if row["id"] == "wz_response_harness_absence_guard")

    exact_negative_boundary_passed = (
        not missing_candidate_paths
        and not any(required_output_presence.values())
        and not usable
        and production_harness["signals"]["guard_only"]
        and not production_harness["signals"]["output_claims_evidence"]
    )

    report("candidate-files-present", not missing_candidate_paths, f"missing={missing_candidate_paths}")
    report("measurement-row-output-absent", not required_output_presence["measurement_rows"], REQUIRED_OUTPUTS["measurement_rows"])
    report("candidate-certificate-output-absent", not required_output_presence["candidate_certificate"], REQUIRED_OUTPUTS["candidate_certificate"])
    report("production-harness-is-guard-only", production_harness["signals"]["guard_only"], "wz_mass_response absent_guarded")
    report("ew-algebra-not-source-response", not ew_algebra["usable_as_wz_response_harness"], ew_algebra["classification"])
    report("builder-has-no-input-rows", not builder["signals"]["output_claims_evidence"], builder["classification"])
    report("gate-does-not-pass", not gate["signals"]["output_claims_evidence"], gate["classification"])
    report("absence-guard-is-not-evidence", guard["signals"]["guard_only"], guard["classification"])
    report("no-usable-wz-response-harness-found", not usable, f"usable={usable}")
    report("exact-negative-boundary-passed", exact_negative_boundary_passed, "no hidden W/Z response implementation")

    result = {
        "actual_current_surface_status": "exact negative boundary / repo-wide WZ response harness import audit",
        "verdict": (
            "No existing repo artifact supplies the same-source W/Z mass-response "
            "measurement required by PR #230.  The production harness has only "
            "a W/Z absent guard; EW gauge-mass algebra starts after canonical H "
            "is supplied; EW coupling/native-gauge scripts provide algebra or "
            "running context; and the W/Z builder/gate have no measurement rows. "
            "Therefore the W/Z route remains a future physical-observable route, "
            "not a hidden current closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No same-source W/Z response measurement rows or candidate certificate exist.",
        "wz_response_repo_import_closes_pr230": False,
        "repo_wz_response_harness_found": False,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "required_outputs": REQUIRED_OUTPUTS,
        "required_output_presence": required_output_presence,
        "candidate_surfaces": rows,
        "positive_reuse": [
            "Use the production harness for same-source top dE_top/ds rows.",
            "Use EW gauge-mass algebra only after canonical H/source overlap is certified.",
            "Use the W/Z builder and gate once real measurement rows exist.",
            "Use native SU(2) and EW coupling scripts only as separate gauge-context support.",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat static EW algebra as dM_W/ds",
            "does not use observed W/Z masses, observed top mass, or observed y_t as selectors",
            "does not set k_top = k_gauge, kappa_s = 1, c2 = 1, or Z_match = 1",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette, or u0 as W/Z response authority",
        ],
        "exact_next_action": (
            "Implement actual same-source W/Z response measurement rows in a "
            "dedicated EW gauge/Higgs harness, or return to source-Higgs "
            "C_sH/C_HH pole rows / production FH-LSZ evidence."
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
