#!/usr/bin/env python3
"""
PR #230 two-source taste-radial C_sx/C_xx row-contract certificate.

The previous block realized the taste-radial second source as a sparse
gauge-covariant harness vertex.  This runner checks the next engineering
contract: when that vertex is used in the existing source/operator stochastic
trace path, the analysis emits explicit C_sx/C_xx aliases instead of forcing
the rows to masquerade as canonical-Higgs C_sH/C_HH evidence.

Result: bounded support only.  This runner does not launch production rows,
does not certify canonical O_H, and does not derive kappa_s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

import yt_direct_lattice_correlator_production as prod


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json"
ACTION_CERTIFICATE = ROOT / "outputs" / "yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"

PARENTS = {
    "two_source_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

STRICT_FUTURE_FILES = {
    "taste_radial_production_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in STRICT_FUTURE_FILES.items()}


def firewall_clean(cert: dict[str, Any]) -> bool:
    firewall = cert.get("forbidden_firewall", cert.get("firewall", {}))
    return isinstance(firewall, dict) and all(value is False for value in firewall.values())


def build_contract_smoke(operator_cert: dict[str, Any]) -> dict[str, Any]:
    geom = prod.Geometry(spatial_l=2, time_l=4)
    gauge = prod.GaugeField(geom)
    rng = np.random.default_rng(20260506)
    rows_by_mode: dict[str, list[dict[str, Any]]] = {"0,0,0": []}
    normal_system = prod.build_normal_equation_system(gauge, 0.75)
    for _cfg in range(2):
        smoke = prod.stochastic_source_higgs_cross_correlator(
            gauge,
            0.75,
            1.0e-8,
            500,
            [(0, 0, 0)],
            1,
            rng,
            operator_cert,
            ACTION_CERTIFICATE,
            normal_system=normal_system,
        )
        rows_by_mode["0,0,0"].append(smoke["mode_rows"]["0,0,0"])
    return prod.fit_source_higgs_cross_correlator(
        rows_by_mode,
        geom.spatial_l,
        operator_cert,
        ACTION_CERTIFICATE,
    )


def main() -> int:
    print("PR #230 two-source taste-radial C_sx/C_xx row contract")
    print("=" * 72)

    parents = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposals = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()
    action = parents["two_source_action"]
    operator_cert = action.get("operator_certificate_payload", {})
    analysis = build_contract_smoke(operator_cert) if isinstance(operator_cert, dict) else {}
    row = analysis.get("mode_rows", {}).get("0,0,0", {})

    action_loaded = (
        action.get("two_source_taste_radial_action_passed") is True
        and action.get("proposal_allowed") is False
        and "taste-radial action source vertex" in statuses["two_source_action"]
    )
    alias_metadata_ok = (
        analysis.get("two_source_taste_radial_row_aliases", {}).get("available") is True
        and analysis.get("canonical_higgs_operator_identity_passed") is False
        and analysis.get("used_as_physical_yukawa_readout") is False
    )
    alias_fields_present = all(
        key in row
        for key in (
            "C_sx_real",
            "C_sx_imag",
            "C_sx_timeseries",
            "C_xx_real",
            "C_xx_imag",
            "C_xx_timeseries",
        )
    )
    alias_fields_finite = (
        finite(row.get("C_sx_real"))
        and finite(row.get("C_sx_imag"))
        and finite(row.get("C_xx_real"))
        and finite(row.get("C_xx_imag"))
    )
    legacy_schema_preserved = all(
        key in row
        for key in (
            "C_sH_real",
            "C_sH_imag",
            "C_HH_real",
            "C_HH_imag",
            "C_sH_timeseries",
            "C_HH_timeseries",
        )
    )
    alias_exactly_maps_legacy = (
        alias_fields_present
        and legacy_schema_preserved
        and row["C_sx_real"] == row["C_sH_real"]
        and row["C_sx_imag"] == row["C_sH_imag"]
        and row["C_xx_real"] == row["C_HH_real"]
        and row["C_xx_imag"] == row["C_HH_imag"]
    )
    future_rows_absent = (
        futures["taste_radial_production_rows"] is False
        and futures["canonical_oh_certificate"] is False
        and futures["source_higgs_rows"] is False
    )
    retained_open = parents["retained_route"].get("proposal_allowed") is False
    campaign_open = parents["campaign_status"].get("proposal_allowed") is False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("two-source-action-loaded", action_loaded, statuses["two_source_action"])
    report("alias-metadata-support-only", alias_metadata_ok, str(analysis.get("two_source_taste_radial_row_aliases", {})))
    report("legacy-source-operator-schema-preserved", legacy_schema_preserved, "C_sH/C_HH fields still present")
    report("taste-radial-alias-fields-present", alias_fields_present, "C_sx/C_xx fields present")
    report("taste-radial-alias-fields-finite", alias_fields_finite, f"C_sx={row.get('C_sx_real')} C_xx={row.get('C_xx_real')}")
    report("taste-radial-alias-maps-legacy-fields", alias_exactly_maps_legacy, "aliases are explicit labels over unchanged schema values")
    report("production-row-files-still-absent", future_rows_absent, str(futures))
    report("action-firewall-clean", firewall_clean(action), str(action.get("forbidden_firewall", {})))
    report("retained-route-still-open", retained_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])

    passed = (
        not missing
        and not proposals
        and action_loaded
        and alias_metadata_ok
        and legacy_schema_preserved
        and alias_fields_present
        and alias_fields_finite
        and alias_exactly_maps_legacy
        and future_rows_absent
        and firewall_clean(action)
        and retained_open
        and campaign_open
    )

    result = {
        "actual_current_surface_status": (
            "bounded-support / two-source taste-radial C_sx/C_xx row contract; production rows absent"
        ),
        "conditional_surface_status": (
            "conditional-support if production rows are run with this schema and a separate canonical O_H/source-overlap or physical-response bridge closes"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The runner certifies only the C_sx/C_xx row schema contract for the taste-radial second source.  It does not provide production rows, pole residues, canonical O_H identity, kappa_s, or retained-route authorization."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "two_source_taste_radial_row_contract_passed": passed,
        "row_contract_schema_passed": alias_metadata_ok and alias_fields_present and alias_fields_finite,
        "operator_id": operator_cert.get("operator_id") if isinstance(operator_cert, dict) else None,
        "future_file_presence": futures,
        "contract_smoke_analysis": analysis,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat C_sx/C_xx aliases as canonical-Higgs C_sH/C_HH rows",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not provide production C_sx/C_xx rows or pole residues",
        ],
        "exact_next_action": (
            "Run production C_sx/C_xx rows using this schema, then supply a canonical O_H/source-overlap bridge or genuine physical-response bypass before retained-route gates can pass."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
