#!/usr/bin/env python3
"""
PR #230 Feynman-Hellmann gauge-normalized response route.

This runner checks a physical-response bypass for the scalar source
normalization: measure the top energy slope and an electroweak gauge-boson
mass slope with respect to the same scalar source.  If the source is certified
to move the same canonical Higgs radial mode in both sectors, the ratio
dE_top/ds divided by dM_W/ds cancels kappa_s.

The result is route support only.  PR #230 does not currently have a
same-source W/Z mass-response harness, production data, or the source-to-Higgs
identity certificate needed to use the ratio as physical y_t evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_gauge_normalized_response_route_2026-05-02.json"
MISSING_GAUGE_RESPONSE = ROOT / "outputs" / "yt_fh_gauge_mass_response_certificate_2026-05-02.json"

CERTS = {
    "feynman_hellmann_source_response": "outputs/yt_feynman_hellmann_source_response_route_2026-05-01.json",
    "scalar_source_response_harness": "outputs/yt_scalar_source_response_harness_certificate_2026-05-01.json",
    "fh_production_protocol": "outputs/yt_fh_production_protocol_certificate_2026-05-01.json",
    "higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
    "gauge_vev_source_overlap_no_go": "outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json",
    "source_to_higgs_lsz": "outputs/yt_source_to_higgs_lsz_closure_attempt_2026-05-01.json",
}

EW_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"

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


def main() -> int:
    print("PR #230 Feynman-Hellmann gauge-normalized response route")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    ew_text = EW_NOTE.read_text(encoding="utf-8") if EW_NOTE.exists() else ""

    y_true = 0.93
    g2 = 0.65
    source_scales = [0.25, 0.5, 1.0, 2.0, 4.0]
    rows = []
    for kappa_s in source_scales:
        top_slope = kappa_s * y_true / math.sqrt(2.0)
        w_slope = kappa_s * g2 / 2.0
        ratio = top_slope / w_slope
        y_from_ratio = g2 * ratio / math.sqrt(2.0)
        rows.append(
            {
                "kappa_s": kappa_s,
                "dE_top_ds": top_slope,
                "dM_W_ds": w_slope,
                "ratio_dE_over_dMW": ratio,
                "y_reconstructed_from_ratio": y_from_ratio,
                "forbidden_kappa_one_top_slope_readout": top_slope,
            }
        )
    y_values = [row["y_reconstructed_from_ratio"] for row in rows]
    forbidden = [row["forbidden_kappa_one_top_slope_readout"] for row in rows]
    y_spread = max(y_values) - min(y_values)
    forbidden_spread = max(forbidden) - min(forbidden)

    fh_route_available = "Feynman-Hellmann" in status(certs["feynman_hellmann_source_response"])
    scalar_harness_available = "scalar source response harness" in status(certs["scalar_source_response_harness"])
    protocol_available = "Feynman-Hellmann production protocol" in status(certs["fh_production_protocol"])
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(certs["higgs_pole_identity_gate"])
        and certs["higgs_pole_identity_gate"].get("proposal_allowed") is False
    )
    gauge_vev_static_shortcut_blocked = (
        "gauge-VEV source-overlap no-go" in status(certs["gauge_vev_source_overlap_no_go"])
        and certs["gauge_vev_source_overlap_no_go"].get("proposal_allowed") is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    ew_supplies_tree_derivative = (
        "M_W^2 = g^2 v^2 / 4" in ew_text
        and "M_W = g_2 v / 2" in ew_text
    )
    gauge_response_present = MISSING_GAUGE_RESPONSE.exists()

    acceptance_requirements = [
        "same-source production dE_top/ds",
        "same-source production dM_W/ds or dM_Z/ds under the same scalar source",
        "retained electroweak coupling normalization for g2 or the neutral-sector equivalent",
        "certificate that the scalar source moves the same canonical Higgs radial mode in top and gauge sectors",
        "no use of observed top mass, observed y_t, observed W/Z mass, H_unit, or Ward authority as proof selectors",
    ]
    gate_passed = (
        not missing
        and not proposal_allowed
        and gauge_response_present
        and not higgs_identity_blocked
        and not source_to_higgs_blocked
    )

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("fh-source-response-route-available", fh_route_available, CERTS["feynman_hellmann_source_response"])
    report("scalar-source-response-harness-available", scalar_harness_available, CERTS["scalar_source_response_harness"])
    report("fh-production-protocol-available", protocol_available, CERTS["fh_production_protocol"])
    report("ew-tree-gauge-derivative-available", ew_supplies_tree_derivative, str(EW_NOTE.relative_to(ROOT)))
    report("ratio-cancels-kappa-s", y_spread < 1.0e-12, f"y_spread={y_spread:.3e}")
    report("kappa-one-top-slope-shortcut-varies", forbidden_spread > 1.0, f"spread={forbidden_spread:.6g}")
    report("static-gauge-vev-shortcut-remains-blocked", gauge_vev_static_shortcut_blocked, CERTS["gauge_vev_source_overlap_no_go"])
    report("same-source-higgs-identity-still-blocked", higgs_identity_blocked and source_to_higgs_blocked, "identity gate blocks route")
    report("gauge-mass-response-output-absent", not gauge_response_present, str(MISSING_GAUGE_RESPONSE.relative_to(ROOT)))
    report("gauge-normalized-route-not-closure", not gate_passed, f"gate_passed={gate_passed}")

    result = {
        "actual_current_surface_status": "bounded-support / FH gauge-normalized response route",
        "verdict": (
            "A same-source gauge-normalized Feynman-Hellmann ratio can cancel "
            "the scalar source normalization: if the source moves the same "
            "canonical Higgs radial mode, then (dE_top/ds)/(dM_W/ds) equals "
            "sqrt(2) y_t/g2.  This identifies a physical-response bypass for "
            "kappa_s that does not use observed top mass or set kappa_s = 1.  "
            "It is not PR #230 closure because no same-source W/Z mass-response "
            "observable or production certificate exists, and the current "
            "Higgs-pole/source-to-Higgs identity gates remain blocked."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The same-source gauge-mass response data and canonical-Higgs identity certificate are absent.",
        "gauge_normalized_response_gate_passed": gate_passed,
        "formula": {
            "top_response": "dE_top/ds = kappa_s * y_t / sqrt(2)",
            "w_response": "dM_W/ds = kappa_s * g2 / 2",
            "ratio": "y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)",
        },
        "rows": rows,
        "acceptance_requirements": acceptance_requirements,
        "parent_certificates": CERTS,
        "missing_gauge_response_certificate": str(MISSING_GAUGE_RESPONSE.relative_to(ROOT)),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use observed top mass, observed y_t, or observed W/Z mass",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Add a same-source electroweak gauge-mass response observable or "
            "derive the canonical-Higgs identity; then combine it with "
            "production dE_top/ds and retained g2 normalization."
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
