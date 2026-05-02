#!/usr/bin/env python3
"""
PR #230 source-pole purity cross-correlator gate.

The canonical-Higgs identity can be closed by proving that the measured source
pole is pure canonical Higgs radial mode.  Source-only C_ss data do not prove
that.  This runner records the missing cross-correlator/response observable and
constructs a two-model witness where C_ss and source response are fixed while
the canonical-Higgs overlap changes.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_pole_purity_cross_correlator_gate_2026-05-02.json"

PARENTS = {
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "target_timeseries_higgs_identity": "outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json",
    "no_orthogonal_top_coupling_selection_rule": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "fh_gauge_mass_response_manifest": "outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json",
    "fh_gauge_mass_response_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "target_timeseries_harness": "outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json",
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


def purity_witness() -> dict[str, Any]:
    residue_ss = 1.0
    source_response = 1.0
    overlap_a = 1.0
    overlap_b = 0.60
    source_higgs_cross_a = overlap_a * math.sqrt(residue_ss)
    source_higgs_cross_b = overlap_b * math.sqrt(residue_ss)
    return {
        "shared_source_only_data": {
            "C_ss_pole_residue": residue_ss,
            "source_response": source_response,
            "source_inverse_propagator_derivative": 2.5,
        },
        "model_A_pure": {
            "source_pole_higgs_overlap": overlap_a,
            "C_sH_pole_cross_residue": source_higgs_cross_a,
            "purity": "pure canonical Higgs",
        },
        "model_B_mixed": {
            "source_pole_higgs_overlap": overlap_b,
            "C_sH_pole_cross_residue": source_higgs_cross_b,
            "purity": "mixed with orthogonal scalar",
        },
        "checks": {
            "source_only_data_equal": True,
            "cross_correlator_distinguishes_models": abs(source_higgs_cross_a - source_higgs_cross_b) > 1.0e-12,
            "canonical_overlap_differs": abs(overlap_a - overlap_b) > 1.0e-12,
            "purity_requires_cross_data_or_theorem": True,
        },
    }


def harness_cross_observable_status() -> dict[str, bool]:
    harness = (ROOT / "scripts" / "yt_direct_lattice_correlator_production.py").read_text(encoding="utf-8")
    key = '"source_higgs_cross_correlator"'
    start = harness.find(key)
    block = ""
    if start >= 0:
        end = harness.find("},", start)
        block = harness[start : end + 2] if end >= 0 else harness[start:]
    guard_present = bool(block)
    guarded_absence = (
        '"enabled": False' in block
        and '"implementation_status": "absent_guarded"' in block
        and '"canonical_higgs_operator_realization": "absent"' in block
    )
    required_objects_named = all(token in block for token in ("C_sH(q)", "C_HH(q)", "O_H or radial canonical-Higgs"))
    real_measurement_path = (
        '"enabled": True' in block
        and '"absent_guarded"' not in block
        and '"canonical_higgs_operator_realization": "absent"' not in block
    )
    return {
        "guard_present": guard_present,
        "guarded_absence": guarded_absence,
        "required_objects_named": required_objects_named,
        "real_measurement_path": real_measurement_path,
    }


def main() -> int:
    print("PR #230 source-pole purity cross-correlator gate")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = purity_witness()
    checks = witness["checks"]
    harness_cross_status = harness_cross_observable_status()

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "source-pole-mixing-obstruction-loaded",
        "source-pole canonical-Higgs mixing" in status(parents["source_pole_mixing"])
        and parents["source_pole_mixing"].get("proposal_allowed") is False,
        status(parents["source_pole_mixing"]),
    )
    report(
        "target-timeseries-not-higgs-identity",
        "target time series not canonical-Higgs identity" in status(parents["target_timeseries_higgs_identity"])
        and parents["target_timeseries_higgs_identity"].get("proposal_allowed") is False,
        status(parents["target_timeseries_higgs_identity"]),
    )
    report(
        "no-orthogonal-coupling-selection-rule-blocked",
        "no-orthogonal-top-coupling selection rule not derived"
        in status(parents["no_orthogonal_top_coupling_selection_rule"])
        and parents["no_orthogonal_top_coupling_selection_rule"].get("proposal_allowed") is False,
        status(parents["no_orthogonal_top_coupling_selection_rule"]),
    )
    report(
        "gauge-response-manifest-not-current-evidence",
        parents["fh_gauge_mass_response_manifest"].get("proposal_allowed") is False,
        status(parents["fh_gauge_mass_response_manifest"]),
    )
    report(
        "current-harness-lacks-cross-observable",
        not harness_cross_status["real_measurement_path"],
        f"guarded_absence={harness_cross_status['guarded_absence']}",
    )
    report(
        "source-higgs-guard-not-evidence",
        harness_cross_status["guard_present"] and harness_cross_status["guarded_absence"],
        "metadata guard names required objects but keeps enabled false",
    )
    report("source-only-data-equal-in-witness", checks["source_only_data_equal"], str(checks))
    report("cross-correlator-distinguishes-models", checks["cross_correlator_distinguishes_models"], str(checks))
    report("canonical-overlap-differs", checks["canonical_overlap_differs"], str(checks))
    report("source-pole-purity-gate-not-passed", checks["purity_requires_cross_data_or_theorem"], str(checks))

    result = {
        "actual_current_surface_status": "open / source-pole purity cross-correlator gate not passed",
        "verdict": (
            "Source-only pole data can determine C_ss and a same-source response, "
            "but not the overlap of the source pole with the canonical Higgs "
            "radial mode.  The witness keeps the source-only data fixed while "
            "changing the canonical-Higgs overlap; a C_sH cross-correlator, "
            "same-source W/Z response, or retained source-pole purity theorem "
            "would distinguish the cases.  The current QCD top harness and "
            "certificates do not provide such an observable."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No cross-correlator, W/Z response, or retained source-pole purity theorem exists.",
        "source_pole_purity_gate_passed": False,
        "parents": PARENTS,
        "current_harness_source_higgs_status": harness_cross_status,
        "current_harness_has_cross_observable": harness_cross_status["real_measurement_path"],
        "witness": witness,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat C_ss as source-pole purity",
            "does not set kappa_s = 1",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Add or derive a source-Higgs cross-correlator/purity theorem, or "
            "implement an independent canonical-Higgs response observable such "
            "as same-source W/Z mass slopes."
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
