#!/usr/bin/env python3
"""
PR #230 source-Higgs harness absence guard certificate.

This is an instrumentation firewall, not evidence.  It verifies that the
production certificate now explicitly marks the source-Higgs cross-correlator
route as absent unless a same-surface canonical-Higgs operator and C_sH/C_HH
rows are implemented.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
OUTPUT = ROOT / "outputs" / "yt_source_higgs_harness_absence_guard_2026-05-02.json"

PARENTS = {
    "source_higgs_cross_correlator_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_higgs_operator_realization_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "hunit_candidate_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
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
    print("PR #230 source-Higgs harness absence guard")
    print("=" * 72)

    source = HARNESS.read_text(encoding="utf-8")
    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]

    manifest_not_evidence = (
        "source-Higgs cross-correlator production manifest"
        in status(parents["source_higgs_cross_correlator_manifest"])
        and parents["source_higgs_cross_correlator_manifest"].get("manifest_is_evidence") is False
    )
    gram_gate_blocks = (
        "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity_gate"])
        and parents["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed") is False
    )
    canonical_operator_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in status(parents["canonical_higgs_operator_realization_gate"])
        and parents["canonical_higgs_operator_realization_gate"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False
    )
    hunit_blocks = (
        "H_unit not canonical-Higgs operator realization" in status(parents["hunit_candidate_gate"])
        and parents["hunit_candidate_gate"].get("hunit_canonical_higgs_operator_gate_passed") is False
    )
    retained_still_open = "retained closure not yet reached" in status(parents["retained_route"])

    guard_present = '"source_higgs_cross_correlator"' in source
    disabled_by_default = '"enabled": False' in source and '"implementation_status": "absent_guarded"' in source
    required_objects_named = all(token in source for token in ("C_sH(q)", "C_HH(q)", "O_H or radial canonical-Higgs"))
    no_yukawa_readout = '"used_as_physical_yukawa_readout": False' in source
    absent_operator_named = '"canonical_higgs_operator_realization": "absent"' in source
    strict_limit_present = "must not be treated as source-Higgs Gram purity" in source

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("manifest-still-not-evidence", manifest_not_evidence, status(parents["source_higgs_cross_correlator_manifest"]))
    report("gram-purity-gate-still-blocks", gram_gate_blocks, status(parents["source_higgs_gram_purity_gate"]))
    report("canonical-operator-still-missing", canonical_operator_blocks, status(parents["canonical_higgs_operator_realization_gate"]))
    report("hunit-still-rejected", hunit_blocks, status(parents["hunit_candidate_gate"]))
    report("retained-route-still-open", retained_still_open, status(parents["retained_route"]))
    report("harness-guard-present", guard_present, "source_higgs_cross_correlator metadata block")
    report("guard-disabled-by-default", disabled_by_default, "enabled False / absent_guarded")
    report("required-cross-objects-named", required_objects_named, "O_H, C_sH, C_HH named")
    report("not-yukawa-readout", no_yukawa_readout, "used_as_physical_yukawa_readout False")
    report("canonical-operator-absent", absent_operator_named, "canonical_higgs_operator_realization absent")
    report("strict-limit-present", strict_limit_present, "C_ss/source-response cannot be Gram purity")

    result = {
        "actual_current_surface_status": "bounded-support / source-Higgs harness absence guard",
        "verdict": (
            "The production certificate now explicitly records that the "
            "source-Higgs cross-correlator route is absent unless a same-surface "
            "canonical-Higgs operator plus C_sH/C_HH/covariance rows are "
            "implemented.  This is an instrumentation guard only; it supplies no "
            "O_H, C_sH, C_HH, pole residue, Gram-purity data, or retained closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The guard marks missing source-Higgs evidence; it is not evidence.",
        "harness_file": str(HARNESS.relative_to(ROOT)),
        "guard_fields": {
            "source_higgs_cross_correlator": guard_present,
            "enabled_false": disabled_by_default,
            "required_objects_named": required_objects_named,
            "used_as_physical_yukawa_readout_false": no_yukawa_readout,
            "canonical_higgs_operator_absent": absent_operator_named,
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not implement O_H, C_sH, or C_HH measurements",
            "does not treat C_ss/source response as source-Higgs Gram purity",
            "does not use H_unit, observed values, yt_ward_identity, alpha_LM, plaquette, u0, or reduced pilots as proof selectors",
        ],
        "exact_next_action": (
            "Implement an actual same-surface O_H observable and C_sH/C_HH rows, "
            "derive a source-Higgs identity theorem, implement W/Z response with "
            "identity certificates, or process FH/LSZ chunks."
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
