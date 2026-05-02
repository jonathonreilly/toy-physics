#!/usr/bin/env python3
"""
PR #230 source-Higgs cross-correlator production manifest.

The purity route now has three separate blockers: C_sH is absent, O_H is not
realized, and H_unit is not a certified substitute.  This runner records the
minimum production schema that would make the route evaluable without using a
forbidden normalization import.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_manifest_2026-05-02.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
FUTURE_CERTIFICATE = ROOT / "outputs" / "yt_source_higgs_cross_correlator_production_certificate_2026-05-02.json"

CERTS = {
    "source_pole_purity_cross_correlator": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "source_higgs_cross_correlator_import": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_higgs_operator_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "hunit_candidate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
    "neutral_scalar_rank_one_purity": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "higgs_identity_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
}

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


def load_json(rel_or_path: str | Path) -> dict[str, Any]:
    path = Path(rel_or_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def manifest_schema() -> dict[str, Any]:
    return {
        "observable": "same-ensemble source-Higgs pole cross-correlator",
        "goal": "evaluate Res(C_sH)^2 = Res(C_ss) Res(C_HH) at the isolated scalar pole",
        "required_operator_inputs": {
            "O_s": "the exact PR #230 scalar source already used for dE_top/ds and C_ss",
            "O_H": "same-surface canonical-Higgs radial operator, not static EW algebra and not H_unit by fiat",
            "normalization": "canonical kinetic/LSZ certificate for O_H",
        },
        "required_measurements": [
            "C_ss(q) time series at zero and at least three positive momentum shells",
            "C_HH(q) time series using the same gauge/source ensemble and momentum shells",
            "C_sH(q) cross time series with paired source/Higgs samples",
            "jackknife/bootstrap covariance across C_ss, C_sH, C_HH, and dE_top/ds",
            "isolated-pole fit or accepted model-class/pole-saturation certificate",
            "finite-volume/IR/zero-mode control for the scalar pole derivative",
        ],
        "minimum_certificate_fields": {
            "phase": "production",
            "same_ensemble": True,
            "same_source_coordinate": True,
            "canonical_higgs_operator_identity_passed": True,
            "hunit_used_as_operator": False,
            "observed_targets_used_as_selectors": False,
            "residue_matrix": ["Res_C_ss", "Res_C_sH", "Res_C_HH", "covariance"],
            "gram_purity": ["rho_sH", "rho_sH_error", "purity_gate_passed"],
            "claim_gate": "proposal_allowed only after retained-route certificate passes",
        },
        "rejection_rules": [
            "source-only C_ss does not determine C_sH or C_HH",
            "H_unit matrix-element readout is not O_H",
            "EW gauge-mass algebra after canonical H is supplied is not O_H",
            "a manifest or reduced smoke is not production evidence",
            "no retained/proposed_retained wording until retained-route gate passes",
        ],
    }


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "reasons": ["future C_sH production certificate absent"]}

    matrix = candidate.get("residue_matrix", {})
    required = {
        "production_phase": candidate.get("phase") == "production",
        "same_ensemble": candidate.get("same_ensemble") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "canonical_higgs_identity": candidate.get("canonical_higgs_operator_identity_passed") is True,
        "not_hunit_by_fiat": candidate.get("hunit_used_as_operator") is False,
        "no_observed_selectors": candidate.get("observed_targets_used_as_selectors") is False,
        "has_res_c_ss": isinstance(matrix.get("Res_C_ss"), (int, float)),
        "has_res_c_sh": isinstance(matrix.get("Res_C_sH"), (int, float)),
        "has_res_c_hh": isinstance(matrix.get("Res_C_HH"), (int, float)),
        "purity_gate_passed": candidate.get("gram_purity", {}).get("purity_gate_passed") is True,
        "retained_route_gate_passed": candidate.get("retained_route_gate_passed") is True,
    }
    return {
        "present": True,
        "valid": all(required.values()),
        "checks": required,
        "reasons": [key for key, ok in required.items() if not ok],
    }


def main() -> int:
    print("PR #230 source-Higgs cross-correlator production manifest")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    harness_text = PRODUCTION_HARNESS.read_text(encoding="utf-8") if PRODUCTION_HARNESS.exists() else ""
    schema = manifest_schema()
    future_validation = validate_future_certificate(load_json(FUTURE_CERTIFICATE))

    purity_gate_blocks = (
        "source-pole purity cross-correlator gate not passed"
        in status(certs["source_pole_purity_cross_correlator"])
        and certs["source_pole_purity_cross_correlator"].get("source_pole_purity_gate_passed") is False
    )
    import_blocks = (
        "source-Higgs cross-correlator import audit"
        in status(certs["source_higgs_cross_correlator_import"])
        and certs["source_higgs_cross_correlator_import"].get(
            "source_higgs_cross_correlator_authority_found"
        )
        is False
    )
    gram_blocks = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    operator_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in status(certs["canonical_higgs_operator_realization"])
        and certs["canonical_higgs_operator_realization"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
    )
    hunit_blocks = (
        "H_unit not canonical-Higgs operator realization" in status(certs["hunit_candidate"])
        and certs["hunit_candidate"].get("hunit_canonical_higgs_operator_gate_passed") is False
    )
    rank_one_blocks = (
        "neutral scalar rank-one purity gate not passed"
        in status(certs["neutral_scalar_rank_one_purity"])
        and certs["neutral_scalar_rank_one_purity"].get("neutral_scalar_rank_one_purity_gate_passed")
        is False
    )
    latest_identity_blocks = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_identity_blocker"])
        and certs["higgs_identity_blocker"].get("identity_closed") is False
    )
    harness_has_c_ss = "scalar_two_point_lsz_analysis" in harness_text
    harness_has_csh = any(
        token in harness_text
        for token in ("source_higgs_cross", "C_sH", "canonical_higgs_operator", "C_HH")
    )
    manifest_is_evidence = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("purity-cross-correlator-gate-blocks", purity_gate_blocks, status(certs["source_pole_purity_cross_correlator"]))
    report("csh-import-audit-blocks", import_blocks, status(certs["source_higgs_cross_correlator_import"]))
    report("gram-purity-gate-blocks", gram_blocks, status(certs["source_higgs_gram_purity"]))
    report("canonical-operator-gate-blocks", operator_blocks, status(certs["canonical_higgs_operator_realization"]))
    report("hunit-candidate-gate-blocks", hunit_blocks, status(certs["hunit_candidate"]))
    report("rank-one-purity-gate-blocks", rank_one_blocks, status(certs["neutral_scalar_rank_one_purity"]))
    report("latest-higgs-identity-blocker-open", latest_identity_blocks, status(certs["higgs_identity_blocker"]))
    report("harness-has-css-not-csh", harness_has_c_ss and not harness_has_csh, str(PRODUCTION_HARNESS.relative_to(ROOT)))
    report("future-csh-certificate-absent", future_validation["present"] is False, str(FUTURE_CERTIFICATE.relative_to(ROOT)))
    report("manifest-records-minimum-schema", "minimum_certificate_fields" in schema, "schema recorded")
    report("manifest-is-not-evidence", not manifest_is_evidence, "planning/support only")

    result = {
        "actual_current_surface_status": "bounded-support / source-Higgs cross-correlator production manifest",
        "verdict": (
            "The source-Higgs cross-correlator route now has a concrete "
            "production schema.  It remains support only: the current harness "
            "emits same-source C_ss support but no same-surface O_H, C_sH, or "
            "C_HH rows, and no future C_sH production certificate exists.  "
            "The H_unit and EW-algebra substitutes are blocked, and the "
            "rank-one/purity/Higgs-identity gates remain open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is a manifest; no O_H/C_sH/C_HH production certificate or retained purity gate exists.",
        "manifest_is_evidence": manifest_is_evidence,
        "future_certificate_validation": future_validation,
        "parent_certificates": CERTS,
        "manifest": schema,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use H_unit as O_H",
            "does not use static EW algebra, observed W/Z masses, observed top mass, observed y_t, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not set kappa_s = 1, cos(theta)=1, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Implement O_H/C_sH/C_HH measurement rows with the manifest schema, "
            "or continue W/Z response, rank-one purity theorem, or seed-controlled "
            "FH/LSZ chunk processing."
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
