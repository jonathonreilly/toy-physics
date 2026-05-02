#!/usr/bin/env python3
"""
PR #230 same-source W/Z response certificate gate.

The gauge-normalized response route is only useful if the W/Z side is a real
same-source mass-response measurement, not static electroweak algebra with the
symbol h renamed to the PR source s.  This gate defines the required future
certificate and rejects current shortcuts.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_wz_response_certificate_gate_2026-05-02.json"
FUTURE_WZ_CERTIFICATE = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"

CERTS = {
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "fh_gauge_mass_response_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "same_source_sector_overlap_identity": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "fh_gauge_response_mixed_scalar": "outputs/yt_fh_gauge_response_mixed_scalar_obstruction_2026-05-02.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "higgs_pole_identity_latest_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
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


def load(rel_or_path: str | Path) -> dict[str, Any]:
    path = Path(rel_or_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def acceptance_schema() -> dict[str, Any]:
    return {
        "certificate_path": str(FUTURE_WZ_CERTIFICATE.relative_to(ROOT)),
        "required_status": "bounded-support or exact-support until retained-route gate passes",
        "required_fields": {
            "phase": "production",
            "source_coordinate": "same scalar source s used for dE_top/ds",
            "source_shifts": ["negative", "zero", "positive"],
            "gauge_sector_action": "explicit SU(2)xU(1) or retained equivalent",
            "mass_fits": [
                "W_or_Z_correlator_mass_fits_by_source_shift",
                "fit_windows_or_effective_mass_method",
                "jackknife_or_bootstrap_blocks",
            ],
            "response": [
                "slope_dM_W_ds or slope_dM_Z_ds",
                "slope_error",
                "covariance_with_top_slope",
            ],
            "identity_certificates": [
                "same_source_sector_overlap_identity_passed",
                "canonical_higgs_pole_identity_passed",
                "retained_route_or_proposal_gate_passed before proposed_retained wording",
            ],
            "firewall": [
                "used_observed_WZ_masses_as_selector=false",
                "used_static_v_overlap_selector=false",
                "used_H_unit_or_Ward_authority=false",
            ],
        },
        "accepted_ratio": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
    }


def validate_future_wz_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {"present": False, "valid": False, "reasons": ["future W/Z response certificate absent"]}

    response = candidate.get("gauge_response", {})
    identity = candidate.get("identity_certificates", {})
    firewall = candidate.get("firewall", {})
    checks = {
        "production_phase": candidate.get("phase") == "production",
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "three_source_shifts": len(candidate.get("source_shifts", [])) >= 3,
        "wz_mass_fits_from_correlators": candidate.get("wz_mass_fits_from_correlators") is True,
        "finite_w_slope": finite_number(response.get("slope_dM_W_ds"))
        or finite_number(response.get("slope_dM_Z_ds")),
        "finite_w_slope_error": finite_number(response.get("slope_error")),
        "has_top_wz_covariance": finite_number(response.get("cov_dE_top_dM_W")),
        "sector_overlap_identity_passed": identity.get("same_source_sector_overlap_identity_passed") is True,
        "canonical_higgs_identity_passed": identity.get("canonical_higgs_pole_identity_passed") is True,
        "retained_route_gate_passed": identity.get("retained_route_or_proposal_gate_passed") is True,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_static_v_selector": firewall.get("used_static_v_overlap_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "reasons": [key for key, ok in checks.items() if not ok],
    }


def rejection_witnesses() -> dict[str, Any]:
    static_algebra = {
        "name": "static EW algebra is not source response",
        "candidate": {
            "phase": "support",
            "derivative": "dM_W/dh = g2 / 2",
            "source_coordinate": "canonical_h_not_PR_source_s",
            "wz_mass_fits_from_correlators": False,
            "used_static_v_overlap_selector": True,
        },
        "rejection": "supplies dM_W/dh after canonical H is assumed, not dM_W/ds",
    }
    slope_without_identity = {
        "name": "slopes without sector identity still read y_t * k_top/k_gauge",
        "candidate": {
            "phase": "production",
            "same_source_coordinate": True,
            "source_shifts": [-0.01, 0.0, 0.01],
            "wz_mass_fits_from_correlators": True,
            "gauge_response": {
                "slope_dM_W_ds": 0.65,
                "slope_error": 0.01,
                "cov_dE_top_dM_W": 0.0,
            },
            "identity_certificates": {
                "same_source_sector_overlap_identity_passed": False,
                "canonical_higgs_pole_identity_passed": False,
            },
            "firewall": {
                "used_observed_WZ_masses_as_selector": False,
                "used_static_v_overlap_selector": False,
                "used_H_unit_or_Ward_authority": False,
            },
        },
        "rejection": "real W/Z slopes are support only until sector-overlap and Higgs identity pass",
    }
    return {"static_algebra": static_algebra, "slope_without_identity": slope_without_identity}


def main() -> int:
    print("PR #230 same-source W/Z response certificate gate")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_candidate = load(FUTURE_WZ_CERTIFICATE)
    future_validation = validate_future_wz_certificate(future_candidate)
    witnesses = rejection_witnesses()

    manifest_support_only = (
        "same-source WZ gauge-mass response manifest"
        in status(certs["fh_gauge_mass_response_manifest"])
        and certs["fh_gauge_mass_response_manifest"].get("manifest_is_evidence") is False
    )
    observable_gap_blocks = (
        "FH gauge-mass response observable gap"
        in status(certs["fh_gauge_mass_response_observable_gap"])
        and certs["fh_gauge_mass_response_observable_gap"].get("gauge_mass_response_observable_ready")
        is False
    )
    sector_overlap_blocks = (
        "same-source sector-overlap identity obstruction"
        in status(certs["same_source_sector_overlap_identity"])
        and certs["same_source_sector_overlap_identity"].get("sector_overlap_identity_gate_passed") is False
    )
    mixed_scalar_blocks = (
        "FH gauge-response mixed-scalar obstruction"
        in status(certs["fh_gauge_response_mixed_scalar"])
        and certs["fh_gauge_response_mixed_scalar"].get("proposal_allowed") is False
    )
    higgs_identity_blocks = (
        "canonical-Higgs pole identity gate blocking" in status(certs["fh_lsz_higgs_pole_identity"])
        and certs["fh_lsz_higgs_pole_identity"].get("higgs_pole_identity_gate_passed") is False
        and certs["higgs_pole_identity_latest_blocker"].get("identity_closed") is False
    )
    gram_gate_blocks = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity_gate"])
        and certs["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed") is False
    )
    gate_passed = (
        not missing
        and not proposal_allowed
        and future_validation["valid"] is True
        and not sector_overlap_blocks
        and not higgs_identity_blocks
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("manifest-is-support-only", manifest_support_only, status(certs["fh_gauge_mass_response_manifest"]))
    report("observable-gap-currently-blocks", observable_gap_blocks, status(certs["fh_gauge_mass_response_observable_gap"]))
    report("sector-overlap-currently-blocks", sector_overlap_blocks, status(certs["same_source_sector_overlap_identity"]))
    report("mixed-scalar-currently-blocks", mixed_scalar_blocks, status(certs["fh_gauge_response_mixed_scalar"]))
    report("canonical-higgs-identity-currently-blocks", higgs_identity_blocks, "Higgs identity gates not passed")
    report("gram-purity-gate-currently-blocks", gram_gate_blocks, status(certs["source_higgs_gram_purity_gate"]))
    report("future-wz-response-certificate-absent", not future_validation["present"], str(FUTURE_WZ_CERTIFICATE.relative_to(ROOT)))
    report("static-ew-algebra-rejected", True, witnesses["static_algebra"]["rejection"])
    report("slopes-without-identity-rejected", True, witnesses["slope_without_identity"]["rejection"])
    report("same-source-wz-certificate-gate-not-passed", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / same-source WZ response certificate gate not passed",
        "verdict": (
            "The future same-source W/Z response route now has an executable "
            "certificate gate.  Current PR #230 does not pass it: no W/Z "
            "mass-response certificate exists, static EW gauge-mass algebra "
            "is not a dM_W/ds measurement, and even real same-source W/Z "
            "slopes would remain support-only until sector-overlap and "
            "canonical-Higgs identity certificates pass."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No valid same-source W/Z response certificate exists, and identity gates remain open.",
        "same_source_wz_response_certificate_gate_passed": gate_passed,
        "future_certificate_validation": future_validation,
        "acceptance_schema": acceptance_schema(),
        "rejection_witnesses": witnesses,
        "parent_certificates": CERTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat static dM_W/dh or observed W/Z masses as dM_W/ds evidence",
            "does not set kappa_s = 1 or k_top = k_gauge",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Implement a real same-source electroweak W/Z mass-response "
            "harness that emits the certificate schema, or derive the "
            "sector-overlap/canonical-Higgs identity; otherwise continue "
            "seed-controlled FH/LSZ production and scalar-pole purity work."
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
