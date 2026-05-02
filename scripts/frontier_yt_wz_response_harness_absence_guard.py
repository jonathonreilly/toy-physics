#!/usr/bin/env python3
"""
PR #230 W/Z response harness absence guard certificate.

The same-source W/Z ratio route can cancel kappa_s only with actual W/Z mass
response data plus identity certificates.  This guard verifies that the current
production harness explicitly marks that route absent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_wz_response_harness_absence_guard_2026-05-02.json"

PARENTS = {
    "same_source_wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "fh_gauge_mass_response_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "fh_gauge_mass_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def main() -> int:
    print("PR #230 W/Z response harness absence guard")
    print("=" * 72)

    source = HARNESS.read_text(encoding="utf-8")
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    wz_gate_blocks = (
        "same-source WZ response certificate gate not passed"
        in status(parents["same_source_wz_response_gate"])
        and parents["same_source_wz_response_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    observable_gap_blocks = (
        "FH gauge-mass response observable gap" in status(parents["fh_gauge_mass_response_gap"])
        and parents["fh_gauge_mass_response_gap"].get("proposal_allowed") is False
    )
    sector_overlap_blocks = (
        "same-source sector-overlap identity obstruction" in status(parents["same_source_sector_overlap"])
        and parents["same_source_sector_overlap"].get("proposal_allowed") is False
    )
    manifest_not_evidence = (
        "same-source WZ gauge-mass response manifest" in status(parents["fh_gauge_mass_manifest"])
        and parents["fh_gauge_mass_manifest"].get("manifest_is_evidence") is False
    )
    retained_still_open = "retained closure not yet reached" in status(parents["retained_route"])

    guard_present = '"wz_mass_response"' in source
    disabled_by_default = '"enabled": False' in source and '"implementation_status": "absent_guarded"' in source
    required_objects_named = all(
        token in source
        for token in ("same-source W/Z correlator mass fits", "dM_W/ds", "covariance with dE_top/ds")
    )
    no_yukawa_readout = '"used_as_physical_yukawa_readout": False' in source
    strict_limit_present = "does not measure W/Z mass" in source and "response.  Static EW algebra" in source

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("wz-response-gate-still-blocks", wz_gate_blocks, status(parents["same_source_wz_response_gate"]))
    report("gauge-mass-observable-gap-still-blocks", observable_gap_blocks, status(parents["fh_gauge_mass_response_gap"]))
    report("sector-overlap-still-blocks", sector_overlap_blocks, status(parents["same_source_sector_overlap"]))
    report("wz-manifest-still-not-evidence", manifest_not_evidence, status(parents["fh_gauge_mass_manifest"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_route"]))
    report("harness-guard-present", guard_present, "wz_mass_response metadata block")
    report("guard-disabled-by-default", disabled_by_default, "enabled False / absent_guarded")
    report("required-wz-objects-named", required_objects_named, "W/Z fits, slopes, covariance named")
    report("not-yukawa-readout", no_yukawa_readout, "used_as_physical_yukawa_readout False")
    report("strict-limit-present", strict_limit_present, "QCD harness has no W/Z response")

    result = {
        "actual_current_surface_status": "bounded-support / WZ response harness absence guard",
        "verdict": (
            "The production certificate now explicitly records that W/Z mass "
            "response is absent from the QCD top-correlator harness.  This is a "
            "claim firewall only; it supplies no W/Z mass fits, dM_W/ds, dM_Z/ds, "
            "covariance, sector-overlap identity, canonical-Higgs identity, or "
            "retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The guard marks missing W/Z evidence; it is not evidence.",
        "harness_file": str(HARNESS.relative_to(ROOT)),
        "guard_fields": {
            "wz_mass_response": guard_present,
            "enabled_false": disabled_by_default,
            "required_objects_named": required_objects_named,
            "used_as_physical_yukawa_readout_false": no_yukawa_readout,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not implement W/Z correlator mass fits or source-response slopes",
            "does not treat static EW algebra as dM_W/ds",
            "does not use observed W/Z masses, observed y_t, H_unit, yt_ward_identity, alpha_LM, plaquette, u0, or reduced pilots as proof selectors",
        ],
        "exact_next_action": (
            "Implement actual W/Z response observables with identity certificates, "
            "implement same-surface O_H/C_sH/C_HH rows, derive a source-Higgs "
            "identity theorem, or process FH/LSZ chunks."
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
