#!/usr/bin/env python3
"""
PR #230 same-source W/Z gauge-mass response manifest.

This runner records the concrete physical-response observable that would
cancel kappa_s in a Feynman-Hellmann ratio.  It is a manifest and acceptance
gate only: the current production harness still has no W/Z mass-response path.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_manifest_2026-05-02.json"
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
GAUGE_RESPONSE_CERT = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"

CERTS = {
    "gauge_normalized_route": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "higgs_pole_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "source_response_harness": "outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def build_manifest() -> dict[str, Any]:
    return {
        "observable": "same-source electroweak gauge-boson mass response",
        "ratio_formula": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
        "source_coordinate": "the same scalar source s used in the top dE_top/ds FH run",
        "required_measurements": [
            "top correlator energies E_top(s=-delta,0,+delta) on common gauge/source ensembles",
            "W-boson correlator masses M_W(s=-delta,0,+delta) under the same scalar source",
            "optional Z-boson correlator masses M_Z(s=-delta,0,+delta) as neutral-sector cross-check",
            "correlated symmetric slopes dE_top/ds and dM_W/ds with jackknife/bootstrap covariance",
            "retained g2 normalization or explicitly certified electroweak coupling normalization",
            "same-source canonical-Higgs identity or direct sector-overlap certificate",
        ],
        "implementation_gaps": [
            "production harness is QCD top-only",
            "no SU(2)xU(1) gauge-boson correlator path is implemented",
            "no gauge_mass_response_analysis JSON field is emitted",
            "no same-source W/Z response certificate exists",
            "Higgs-pole identity and sector-overlap gates remain blocking",
        ],
        "evidence_rejection_rules": [
            "observed W/Z masses cannot be used as proof selectors",
            "static electroweak v cannot identify the substrate source",
            "reduced/cold pilots cannot count as production evidence",
            "same-source labels do not prove equal top/gauge overlap",
            "no retained or proposed_retained wording until the retained-route gate passes",
        ],
        "minimum_output_schema": {
            "phase": "production",
            "source_shifts": ["-delta", "0", "+delta"],
            "top_response": ["slope_dE_top_ds", "slope_dE_top_ds_err"],
            "gauge_response": ["slope_dM_W_ds", "slope_dM_W_ds_err"],
            "correlation": ["cov_dE_dMW", "jackknife_blocks"],
            "identity_certificates": [
                "same_source_sector_overlap_identity_certificate",
                "canonical_higgs_pole_identity_certificate",
            ],
            "claim_gate": "proposal_allowed only after retained-route certificate passes",
        },
    }


def main() -> int:
    print("PR #230 same-source W/Z gauge-mass response manifest")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    production_text = PRODUCTION_HARNESS.read_text(encoding="utf-8") if PRODUCTION_HARNESS.exists() else ""
    manifest = build_manifest()

    route_support = (
        "FH gauge-normalized response route" in status(certs["gauge_normalized_route"])
        and certs["gauge_normalized_route"].get("proposal_allowed") is False
    )
    observable_gap_blocks = (
        "FH gauge-mass response observable gap" in status(certs["observable_gap"])
        and certs["observable_gap"].get("gauge_mass_response_observable_ready") is False
    )
    sector_overlap_blocks = (
        "same-source sector-overlap identity obstruction" in status(certs["sector_overlap"])
        and certs["sector_overlap"].get("proposal_allowed") is False
    )
    higgs_identity_blocks = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_pole_blocker"])
        and certs["higgs_pole_blocker"].get("identity_closed") is False
    )
    top_source_harness_exists = (
        "scalar source response harness" in status(certs["source_response_harness"])
        and "--scalar-source-shifts" in production_text
        and "scalar_source_response_analysis" in production_text
    )
    gauge_response_code_absent = all(
        token not in production_text
        for token in ("gauge_mass_response_analysis", "slope_dM_W_ds", "--gauge-mass-response")
    )
    gauge_response_cert_absent = not GAUGE_RESPONSE_CERT.exists()
    manifest_is_evidence = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("gauge-normalized-route-support-present", route_support, status(certs["gauge_normalized_route"]))
    report("top-source-response-harness-present", top_source_harness_exists, str(PRODUCTION_HARNESS.relative_to(ROOT)))
    report("gauge-response-observable-gap-blocks", observable_gap_blocks, status(certs["observable_gap"]))
    report("sector-overlap-still-blocks", sector_overlap_blocks, status(certs["sector_overlap"]))
    report("higgs-identity-still-blocks", higgs_identity_blocks, status(certs["higgs_pole_blocker"]))
    report("gauge-response-code-absent", gauge_response_code_absent, "no W/Z response implementation in production harness")
    report("gauge-response-certificate-absent", gauge_response_cert_absent, str(GAUGE_RESPONSE_CERT.relative_to(ROOT)))
    report("manifest-records-minimum-schema", "minimum_output_schema" in manifest, "schema recorded")
    report("manifest-is-not-evidence", not manifest_is_evidence, "planning/support only")

    result = {
        "actual_current_surface_status": "bounded-support / same-source WZ gauge-mass response manifest",
        "verdict": (
            "The same-source W/Z mass-response route has a concrete production "
            "observable and acceptance schema, but it remains planning support. "
            "The current production harness can measure top dE/ds under scalar "
            "source shifts, but it has no electroweak W/Z correlator response "
            "path and no same-source gauge-response certificate.  The sector-"
            "overlap and Higgs-pole identity gates remain blocking."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The W/Z response harness and identity certificates are absent; this manifest is not evidence.",
        "manifest_is_evidence": manifest_is_evidence,
        "gauge_response_certificate_present": not gauge_response_cert_absent,
        "parent_certificates": CERTS,
        "manifest": manifest,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed W/Z masses, observed top mass, or observed y_t",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit or yt_ward_identity as authority",
            "does not treat a manifest as production evidence",
        ],
        "exact_next_action": (
            "Either implement the W/Z response harness named here together with "
            "sector-overlap and Higgs-pole identity certificates, or continue "
            "the scalar-denominator/production FH-LSZ route."
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
