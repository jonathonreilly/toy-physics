#!/usr/bin/env python3
"""
PR #230 source-Higgs Gram-purity contract witness.

This runner tests the executable acceptance surface for the selected
source-Higgs route without writing any production row file.  It builds in-memory
candidate certificates and verifies that the postprocessor would accept a
fully firewalled pure O_sp-Higgs pole-residue matrix, reject a mixed residue
matrix, reject a forbidden-import candidate, and reject a candidate that lacks
the retained-route gate.

The witness is contract support only.  It is not production evidence and does
not authorize retained/proposed_retained y_t closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from frontier_yt_source_higgs_gram_purity_postprocessor import (
    compute_gate,
    validate_candidate,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_gram_purity_contract_witness_2026-05-03.json"

PARENTS = {
    "gram_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "canonical_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def base_candidate() -> dict[str, Any]:
    return {
        "phase": "production",
        "same_ensemble": True,
        "same_source_coordinate": True,
        "source_coordinate": "uniform_scalar_source_s",
        "selected_source_side_normalization": "legendre_lsz_source_pole_operator_v1",
        "source_pole_operator": {
            "source_pole_operator_constructed": True,
            "source_pole_residue_normalized_to_one": True,
            "canonical_higgs_operator_identity_passed": False,
        },
        "canonical_higgs_operator_identity_passed": True,
        "canonical_higgs_operator": {
            "operator_id": "future_same_surface_O_H",
            "identity_certificate": "future/O_H_identity_certificate.json",
            "normalization_certificate": "future/O_H_normalization_certificate.json",
        },
        "hunit_used_as_operator": False,
        "firewall": {
            "used_observed_targets_as_selectors": False,
            "used_yt_ward_identity": False,
            "used_alpha_lm_or_plaquette": False,
            "used_hunit_matrix_element_readout": False,
            "used_static_ew_algebra_as_operator": False,
        },
        "retained_route_gate_passed": True,
        "residue_matrix": {
            "Res_C_ss": 4.0,
            "Res_C_sH": 6.0,
            "Res_C_HH": 9.0,
            "Res_C_ss_err": 0.0,
            "Res_C_sH_err": 0.0,
            "Res_C_HH_err": 0.0,
        },
    }


def candidate_rows() -> list[dict[str, Any]]:
    pure = base_candidate()
    mixed = base_candidate()
    mixed["residue_matrix"] = {
        "Res_C_ss": 4.0,
        "Res_C_sH": 3.0,
        "Res_C_HH": 9.0,
        "Res_C_ss_err": 0.0,
        "Res_C_sH_err": 0.0,
        "Res_C_HH_err": 0.0,
    }
    forbidden = base_candidate()
    forbidden["firewall"] = dict(forbidden["firewall"])
    forbidden["firewall"]["used_yt_ward_identity"] = True
    no_retained_gate = base_candidate()
    no_retained_gate["retained_route_gate_passed"] = False
    return [
        {"name": "pure_firewalled_future_candidate", "candidate": pure, "expect_gate": True},
        {"name": "mixed_orthogonal_component_candidate", "candidate": mixed, "expect_gate": False},
        {"name": "forbidden_ward_import_candidate", "candidate": forbidden, "expect_gate": False},
        {"name": "no_retained_route_gate_candidate", "candidate": no_retained_gate, "expect_gate": False},
    ]


def evaluate(row: dict[str, Any]) -> dict[str, Any]:
    candidate = row["candidate"]
    checks = validate_candidate(candidate)
    missing = [key for key, ok in checks.items() if not ok]
    gate = compute_gate(candidate, tolerance=1.0e-9, sigma=3.0)
    passed = bool(gate["purity_gate_passed"]) and not missing
    return {
        "name": row["name"],
        "expect_gate": row["expect_gate"],
        "candidate_missing_or_failed_checks": missing,
        "gram_purity": gate,
        "postprocessor_would_pass": passed,
        "expectation_met": passed is row["expect_gate"],
    }


def main() -> int:
    print("PR #230 source-Higgs Gram-purity contract witness")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    evaluations = [evaluate(row) for row in candidate_rows()]
    expectations_met = all(row["expectation_met"] for row in evaluations)
    pure_eval = evaluations[0]
    mixed_eval = evaluations[1]
    forbidden_eval = evaluations[2]
    no_retained_eval = evaluations[3]

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("postprocessor-current-surface-open", "awaiting production certificate" in status(parents["gram_postprocessor"]), status(parents["gram_postprocessor"]))
    report("rank-repair-current-rows-absent", "current rows absent" in status(parents["rank_repair"]), status(parents["rank_repair"]))
    report("builder-current-rows-absent", "rows absent" in status(parents["source_higgs_builder"]), status(parents["source_higgs_builder"]))
    report("canonical-operator-current-certificate-absent", "certificate absent" in status(parents["canonical_operator_gate"]), status(parents["canonical_operator_gate"]))
    report("retained-route-current-surface-open", "retained closure not yet reached" in status(parents["retained_route"]), status(parents["retained_route"]))
    report("pure-future-candidate-would-pass", pure_eval["postprocessor_would_pass"], json.dumps(pure_eval["gram_purity"], sort_keys=True))
    report("mixed-candidate-rejected", not mixed_eval["postprocessor_would_pass"], json.dumps(mixed_eval["gram_purity"], sort_keys=True))
    report("forbidden-import-candidate-rejected", not forbidden_eval["postprocessor_would_pass"], f"missing={forbidden_eval['candidate_missing_or_failed_checks']}")
    report("no-retained-route-gate-candidate-rejected", not no_retained_eval["postprocessor_would_pass"], f"missing={no_retained_eval['candidate_missing_or_failed_checks']}")
    report("contract-expectations-met", expectations_met, f"rows={len(evaluations)}")

    result = {
        "actual_current_surface_status": "exact-support / source-Higgs Gram-purity contract witness; current rows absent",
        "verdict": (
            "The source-Higgs Gram-purity acceptance surface is executable: a "
            "fully firewalled future candidate with pure O_sp-Higgs pole "
            "residues would pass the postprocessor, while a mixed orthogonal "
            "candidate, a forbidden Ward-import candidate, and a candidate "
            "without retained-route authorization are rejected.  This is a "
            "contract witness only.  The current PR230 surface still lacks the "
            "production O_H/C_sH/C_HH pole rows and the retained-route gate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is an in-memory contract witness, not production source-Higgs evidence.",
        "contract_witness_passed": expectations_met,
        "evaluations": evaluations,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write production source-Higgs rows",
            "does not define O_H by fiat",
            "does not treat H_unit, static EW algebra, or observed targets as O_H",
            "does not use yt_ward_identity, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Supply a real same-surface canonical-Higgs operator certificate "
            "and production C_sH/C_HH pole residues, then rerun the builder, "
            "postprocessor, and retained-route certificate."
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
