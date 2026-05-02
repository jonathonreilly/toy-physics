#!/usr/bin/env python3
"""
PR #230 Feynman-Hellmann gauge-mass response observable gap.

The gauge-normalized response route would cancel kappa_s if a same-source
top-energy slope and W/Z mass slope measure the same canonical Higgs radial
mode.  This runner checks whether the current repo surface actually supplies
that W/Z response observable.  It does not: the production harness is a QCD
top-correlator harness with scalar-source shifts, while the EW gauge-mass
theorem starts after a canonical Higgs field has already been supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
EW_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
MISSING_GAUGE_RESPONSE = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_gauge_mass_response_observable_gap_2026-05-02.json"

CERTS = {
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "scalar_source_response_harness": "outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json",
    "fh_lsz_higgs_pole_identity": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
    "gauge_vev_source_overlap_no_go": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def sector_overlap_countermodels() -> list[dict[str, float]]:
    y_top = 0.93
    g2 = 0.65
    v = 1.0
    k_top = 1.0
    rows = []
    for k_gauge in (0.5, 1.0, 2.0):
        top_slope = k_top * y_top / math.sqrt(2.0)
        w_slope = k_gauge * g2 / 2.0
        inferred_y_assuming_common_overlap = g2 * top_slope / (math.sqrt(2.0) * w_slope)
        rows.append(
            {
                "static_v": v,
                "static_M_W": g2 * v / 2.0,
                "true_y_top": y_top,
                "top_source_overlap": k_top,
                "gauge_source_overlap": k_gauge,
                "dE_top_ds": top_slope,
                "dM_W_ds": w_slope,
                "y_inferred_if_overlaps_identified": inferred_y_assuming_common_overlap,
            }
        )
    return rows


def main() -> int:
    print("PR #230 FH gauge-mass response observable gap")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    production_text = PRODUCTION_HARNESS.read_text(encoding="utf-8") if PRODUCTION_HARNESS.exists() else ""
    ew_text = EW_NOTE.read_text(encoding="utf-8") if EW_NOTE.exists() else ""
    rows = sector_overlap_countermodels()

    has_top_scalar_response = (
        "--scalar-source-shifts" in production_text
        and "scalar_source_response_analysis" in production_text
        and "dE/ds" in production_text
    )
    production_action_is_qcd_top = (
        "Cl3Z3_SU3_Wilson_staggered" in production_text
        and "staggered_top_correlator_mass_extraction" in production_text
    )
    no_gauge_mass_response_cli = all(
        token not in production_text
        for token in ("--gauge-mass-response", "gauge_mass_response_analysis", "dM_W_ds")
    )
    ew_derivative_requires_canonical_h = (
        "Assume a neutral Higgs vacuum" in ew_text
        and "M_W = g_2 v / 2" in ew_text
        and "standard covariant derivative" in ew_text
        and "Higgs doublet" in ew_text
    )
    static_w_values = {round(row["static_M_W"], 12) for row in rows}
    inferred_values = [row["y_inferred_if_overlaps_identified"] for row in rows]
    inferred_spread = max(inferred_values) - min(inferred_values)
    gauge_response_present = MISSING_GAUGE_RESPONSE.exists()
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(certs["fh_lsz_higgs_pole_identity"])
        and certs["fh_lsz_higgs_pole_identity"].get("proposal_allowed") is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    gauge_vev_shortcut_blocked = (
        "gauge-VEV source-overlap no-go" in status(certs["gauge_vev_source_overlap_no_go"])
        and certs["gauge_vev_source_overlap_no_go"].get("proposal_allowed") is False
    )

    acceptance_schema = {
        "required_observable": "same-source W/Z mass-response slope under the scalar source used for dE_top/ds",
        "required_fields": [
            "source_coordinate",
            "source_shifts",
            "gauge_sector_action",
            "W_or_Z_correlator_mass_fits_by_shift",
            "slope_dM_W_ds_or_dM_Z_ds",
            "same_canonical_higgs_identity_certificate",
            "used_observed_WZ_masses_as_selector=false",
            "used_static_v_overlap_selector=false",
            "production_phase",
        ],
        "accepted_ratio": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
    }
    gate_passed = (
        not missing
        and not proposal_allowed
        and gauge_response_present
        and not higgs_identity_blocked
        and not source_to_higgs_blocked
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("top-scalar-response-harness-present", has_top_scalar_response, str(PRODUCTION_HARNESS.relative_to(ROOT)))
    report("current-production-action-is-qcd-top", production_action_is_qcd_top, "not an EW W/Z mass harness")
    report("gauge-mass-response-cli-absent", no_gauge_mass_response_cli, "no gauge_mass_response_analysis path")
    report("ew-tree-derivative-needs-canonical-higgs", ew_derivative_requires_canonical_h, str(EW_NOTE.relative_to(ROOT)))
    report("gauge-vev-shortcut-blocked", gauge_vev_shortcut_blocked, CERTS["gauge_vev_source_overlap_no_go"])
    report(
        "sector-overlap-countermodels-change-ratio",
        len(static_w_values) == 1 and inferred_spread > 1.0,
        f"inferred_y_values={inferred_values}",
    )
    report("acceptance-schema-names-same-source-wz-slope", "slope_dM_W_ds_or_dM_Z_ds" in str(acceptance_schema), "schema recorded")
    report("gauge-response-certificate-absent", not gauge_response_present, str(MISSING_GAUGE_RESPONSE.relative_to(ROOT)))
    report("higgs-identity-still-blocked", higgs_identity_blocked and source_to_higgs_blocked, "identity gates remain blocking")
    report("observable-gap-not-closure", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "open / FH gauge-mass response observable gap",
        "verdict": (
            "The gauge-normalized response formula identifies a useful possible "
            "bypass, but the current repo surface has no same-source W/Z "
            "mass-response observable.  The production harness measures QCD "
            "top correlators with scalar-source mass shifts, not electroweak "
            "gauge-boson mass shifts.  The EW gauge-mass theorem supplies "
            "dM_W/dh after a canonical Higgs field has already been identified; "
            "it does not measure dM_W/ds or prove that the top and gauge "
            "responses share the same source overlap.  Therefore this route "
            "remains open until a true same-source gauge-mass response harness "
            "or a canonical-Higgs identity theorem is supplied."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No same-source W/Z mass-response certificate exists, and the canonical-Higgs identity remains blocked.",
        "gauge_mass_response_observable_ready": gate_passed,
        "parent_certificates": CERTS,
        "current_harness_gap": {
            "top_scalar_response_present": has_top_scalar_response,
            "production_action_is_qcd_top": production_action_is_qcd_top,
            "gauge_mass_response_cli_absent": no_gauge_mass_response_cli,
            "missing_gauge_response_certificate": str(MISSING_GAUGE_RESPONSE.relative_to(ROOT)),
        },
        "sector_overlap_countermodels": rows,
        "acceptance_schema": acceptance_schema,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use observed W/Z masses or observed top/y_t values as proof selectors",
            "does not use static electroweak v to identify the substrate source",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "Implement a genuine same-source W/Z mass-response observable with "
            "the same scalar source used for dE_top/ds, or derive the "
            "canonical-Higgs identity; otherwise continue scalar-denominator "
            "or seed-controlled FH/LSZ production work."
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
