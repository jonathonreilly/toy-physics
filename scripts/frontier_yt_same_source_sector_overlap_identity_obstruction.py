#!/usr/bin/env python3
"""
PR #230 same-source sector-overlap identity obstruction.

The gauge-normalized FH route cancels a common scalar-source rescaling only if
the top-energy and gauge-mass responses are known to probe the same canonical
Higgs radial mode with the same source overlap.  This runner records the
remaining identity gate explicitly: a single lattice source coordinate does not
by itself prove k_top = k_gauge.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json"

CERTS = {
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "fh_gauge_mass_response_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "source_reparametrization_gauge_no_go": "outputs/yt_source_reparametrization_gauge_no_go_2026-05-01.json",
    "higgs_pole_identity_gate": "outputs/yt_fh_lsz_higgs_pole_identity_gate_2026-05-02.json",
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


def sector_overlap_family() -> list[dict[str, float]]:
    y_true = 0.93
    g2 = 0.65
    v = 1.0
    rows: list[dict[str, float]] = []
    for common_scale in (0.5, 1.0, 2.0):
        for rho in (0.5, 1.0, 2.0):
            k_gauge = common_scale
            k_top = common_scale * rho
            top_slope = k_top * y_true / math.sqrt(2.0)
            w_slope = k_gauge * g2 / 2.0
            inferred_y = g2 * top_slope / (math.sqrt(2.0) * w_slope)
            rows.append(
                {
                    "common_source_scale": common_scale,
                    "rho_top_over_gauge": rho,
                    "static_v": v,
                    "static_M_W": g2 * v / 2.0,
                    "true_y_t": y_true,
                    "top_source_overlap": k_top,
                    "gauge_source_overlap": k_gauge,
                    "dE_top_ds": top_slope,
                    "dM_W_ds": w_slope,
                    "y_inferred_if_k_top_eq_k_gauge": inferred_y,
                }
            )
    return rows


def main() -> int:
    print("PR #230 same-source sector-overlap identity obstruction")
    print("=" * 72)

    certs = {name: load(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    rows = sector_overlap_family()
    by_common_scale: dict[float, list[float]] = {}
    by_rho: dict[float, list[float]] = {}
    for row in rows:
        by_common_scale.setdefault(row["common_source_scale"], []).append(
            row["y_inferred_if_k_top_eq_k_gauge"]
        )
        by_rho.setdefault(row["rho_top_over_gauge"], []).append(
            row["y_inferred_if_k_top_eq_k_gauge"]
        )

    common_scale_spreads = {
        scale: max(values) - min(values) for scale, values in by_common_scale.items()
    }
    rho_spreads = {rho: max(values) - min(values) for rho, values in by_rho.items()}
    inferred_values = [row["y_inferred_if_k_top_eq_k_gauge"] for row in rows]
    static_w_values = {round(row["static_M_W"], 12) for row in rows}

    gauge_route_support_only = (
        "FH gauge-normalized response route" in status(certs["fh_gauge_normalized_response"])
        and certs["fh_gauge_normalized_response"].get("proposal_allowed") is False
        and certs["fh_gauge_normalized_response"].get("gauge_normalized_response_gate_passed") is False
    )
    gauge_observable_absent = (
        "FH gauge-mass response observable gap"
        in status(certs["fh_gauge_mass_response_observable_gap"])
        and certs["fh_gauge_mass_response_observable_gap"].get("gauge_mass_response_observable_ready")
        is False
    )
    source_reparam_blocks_source_only = (
        "source reparametrization" in status(certs["source_reparametrization_gauge_no_go"])
        and certs["source_reparametrization_gauge_no_go"].get("proposal_allowed") is False
    )
    higgs_identity_blocked = (
        "canonical-Higgs pole identity gate blocking" in status(certs["higgs_pole_identity_gate"])
        and certs["higgs_pole_identity_gate"].get("higgs_pole_identity_gate_passed") is False
    )
    source_to_higgs_blocked = (
        "source-to-Higgs LSZ closure attempt blocked" in status(certs["source_to_higgs_lsz"])
        and certs["source_to_higgs_lsz"].get("proposal_allowed") is False
    )
    static_vev_shortcut_blocked = (
        "gauge-VEV source-overlap no-go" in status(certs["gauge_vev_source_overlap_no_go"])
        and certs["gauge_vev_source_overlap_no_go"].get("proposal_allowed") is False
    )

    common_rescaling_cancels_for_fixed_rho = all(spread < 1.0e-12 for spread in rho_spreads.values())
    sector_overlap_changes_readout = (
        len(static_w_values) == 1
        and max(inferred_values) - min(inferred_values) > 1.0
        and any(spread > 0.1 for spread in common_scale_spreads.values())
    )
    sector_overlap_identity_gate_passed = False

    report("all-parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("gauge-normalized-route-is-support-only", gauge_route_support_only, status(certs["fh_gauge_normalized_response"]))
    report("gauge-observable-gap-present", gauge_observable_absent, status(certs["fh_gauge_mass_response_observable_gap"]))
    report("source-reparametrization-blocks-source-only-closure", source_reparam_blocks_source_only, status(certs["source_reparametrization_gauge_no_go"]))
    report("common-source-rescaling-cancels-at-fixed-rho", common_rescaling_cancels_for_fixed_rho, f"rho_spreads={rho_spreads}")
    report("sector-overlap-ratio-changes-readout", sector_overlap_changes_readout, f"inferred_y_values={inferred_values}")
    report("static-vev-shortcut-still-blocked", static_vev_shortcut_blocked, status(certs["gauge_vev_source_overlap_no_go"]))
    report("canonical-higgs-identity-still-blocked", higgs_identity_blocked and source_to_higgs_blocked, "identity gates remain blocking")
    report("sector-overlap-identity-not-derived", not sector_overlap_identity_gate_passed, "k_top = k_gauge absent")
    report("same-source-sector-overlap-route-not-closure", True, "no retained proposal allowed")

    result = {
        "actual_current_surface_status": "exact negative boundary / same-source sector-overlap identity obstruction",
        "verdict": (
            "The same-source gauge-normalized FH ratio cancels a common source "
            "coordinate rescaling, but it still requires a sector-overlap "
            "identity: k_top must equal k_gauge for the lattice source's "
            "projection onto the canonical Higgs radial mode.  The current "
            "surface does not derive that identity.  Families with the same "
            "static electroweak point and same source coordinate can preserve "
            "common rescaling covariance while changing rho = k_top/k_gauge; "
            "the inferred y_t from the gauge-normalized formula then changes "
            "by rho.  Thus a same-source label is not enough.  Closure needs "
            "either a canonical-Higgs source identity theorem or a production "
            "observable that directly certifies the shared sector overlap."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The equality k_top = k_gauge is not derived, and no same-source W/Z response certificate exists.",
        "sector_overlap_identity_gate_passed": sector_overlap_identity_gate_passed,
        "formula": {
            "top_response": "dE_top/ds = k_top * y_t / sqrt(2)",
            "w_response": "dM_W/ds = k_gauge * g2 / 2",
            "ratio_readout": "y_readout = y_t * (k_top / k_gauge)",
            "closure_requirement": "derive k_top/k_gauge = 1 or measure an equivalent physical-response identity",
        },
        "sector_overlap_family": rows,
        "parent_certificates": CERTS,
        "open_identity_gates": [
            "canonical-Higgs pole identity",
            "source-to-Higgs LSZ normalization",
            "same-source W/Z mass-response observable",
            "sector-overlap equality k_top = k_gauge",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set k_top = k_gauge",
            "does not use static electroweak v or observed W/Z masses as proof selectors",
            "does not use observed top mass, observed y_t, H_unit, yt_ward_identity, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Either derive the canonical-Higgs source identity that enforces "
            "k_top = k_gauge, implement a genuine same-source W/Z response "
            "harness that certifies the shared sector overlap, or continue "
            "seed-controlled FH/LSZ production toward a direct scalar pole "
            "residue measurement."
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
