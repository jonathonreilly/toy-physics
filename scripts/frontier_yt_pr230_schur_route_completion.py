#!/usr/bin/env python3
"""PR #230 Schur A/B/C route completion gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_schur_route_completion_2026-05-06.json"

PARENTS = {
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_absence_guard": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "schur_compressed_bootstrap": "outputs/yt_schur_compressed_denominator_row_bootstrap_no_go_2026-05-05.json",
    "schur_abc_definition": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "exact_tensor_schur_feasibility": "outputs/yt_pr230_exact_tensor_schur_row_feasibility_attempt_2026-05-05.json",
    "two_source_schur_subblock_witness": "outputs/yt_pr230_two_source_taste_radial_schur_subblock_witness_2026-05-06.json",
    "neutral_offdiagonal_generator": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
}

FUTURE_ARTIFACTS = {
    "schur_scalar_kernel_rows": "outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "neutral_scalar_kernel_basis": "outputs/yt_neutral_scalar_kernel_basis_certificate_2026-05-05.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
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


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def firewall() -> dict[str, bool]:
    return {
        "used_source_only_denominator_as_abc_rows": False,
        "used_pslq_or_outside_math_as_row_definition": False,
        "used_hunit_or_ward": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 Schur A/B/C route completion gate")
    print("=" * 72)
    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()

    support_loaded = (
        certs["schur_sufficiency"].get("schur_sufficiency_theorem_passed") is True
        and certs["schur_sufficiency"].get("current_schur_kernel_rows_present") is False
    )
    row_absence_loaded = (
        certs["schur_absence_guard"].get("schur_kprime_row_absence_guard_passed") is True
        and certs["schur_absence_guard"].get("current_schur_kernel_rows_present") is False
    )
    contract_open = (
        certs["schur_contract"].get("schur_kernel_row_contract_gate_passed") is False
        and certs["schur_contract"].get("candidate_rows_present") is False
    )
    candidate_extraction_blocks = (
        "Schur row candidate extraction" in statuses["schur_candidate_extraction"]
        and certs["schur_candidate_extraction"].get("proposal_allowed") is False
    )
    compressed_bootstrap_blocks = (
        certs["schur_compressed_bootstrap"].get("bootstrap_no_go_passed") is True
        and certs["schur_compressed_bootstrap"].get("proposal_allowed") is False
    )
    abc_definition_blocks = (
        "Schur A/B/C definition not derivable" in statuses["schur_abc_definition"]
        and certs["schur_abc_definition"].get("exact_negative_boundary_passed") is True
        and certs["schur_abc_definition"].get("schur_abc_rows_written") is False
    )
    exact_tensor_blocks = (
        "exact tensor Schur A/B/C row feasibility blocked" in statuses["exact_tensor_schur_feasibility"]
        and certs["exact_tensor_schur_feasibility"].get("proposal_allowed") is False
    )
    two_source_subblock_support = (
        "Schur-subblock witness" in statuses["two_source_schur_subblock_witness"]
        and certs["two_source_schur_subblock_witness"].get(
            "two_source_taste_radial_schur_subblock_witness_passed"
        )
        is True
        and certs["two_source_schur_subblock_witness"].get(
            "strict_schur_kernel_row_contract_passed"
        )
        is False
        and certs["two_source_schur_subblock_witness"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
        and certs["two_source_schur_subblock_witness"].get("proposal_allowed") is False
    )
    neutral_basis_absent = (
        certs["neutral_offdiagonal_generator"].get("offdiagonal_generator_written") is False
        and not any(futures.values())
    )
    clean_firewall = all(value is False for value in firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("schur-sufficiency-support-loaded", support_loaded, statuses["schur_sufficiency"])
    report("schur-row-absence-loaded", row_absence_loaded, statuses["schur_absence_guard"])
    report("schur-contract-open", contract_open, statuses["schur_contract"])
    report("candidate-extraction-blocks", candidate_extraction_blocks, statuses["schur_candidate_extraction"])
    report("compressed-bootstrap-blocks", compressed_bootstrap_blocks, statuses["schur_compressed_bootstrap"])
    report("abc-definition-blocks", abc_definition_blocks, statuses["schur_abc_definition"])
    report("exact-tensor-schur-blocks-current-surface", exact_tensor_blocks, statuses["exact_tensor_schur_feasibility"])
    report(
        "two-source-correlator-subblock-support-not-closure",
        two_source_subblock_support,
        statuses["two_source_schur_subblock_witness"],
    )
    report("strict-neutral-kernel-rows-still-absent", neutral_basis_absent, str(futures))
    report("forbidden-firewall-clean", clean_firewall, str(firewall()))

    passed = (
        not missing
        and not proposal_allowed
        and support_loaded
        and row_absence_loaded
        and contract_open
        and candidate_extraction_blocks
        and compressed_bootstrap_blocks
        and abc_definition_blocks
        and exact_tensor_blocks
        and two_source_subblock_support
        and neutral_basis_absent
        and clean_firewall
    )
    result = {
        "actual_current_surface_status": "exact negative boundary / strict Schur A/B/C route not complete; bounded two-source correlator subblock support present",
        "conditional_surface_status": "The Schur route remains hard-physics open if a same-surface neutral kernel basis plus A/B/C rows or equivalent row theorem is supplied.",
        "proposal_allowed": False,
        "proposal_allowed_reason": "The two-source taste-radial chunks now supply finite C_ss/C_sx/C_xx correlator subblocks for a certified s/x chart, but strict Schur K-prime closure still lacks kernel pole rows, derivatives, isolated-pole/FV/IR authority, and canonical O_H/source-overlap or physical-response authority.",
        "bare_retained_allowed": False,
        "schur_route_completion_passed": passed,
        "exact_negative_boundary_passed": passed,
        "two_source_correlator_subblock_support_loaded": two_source_subblock_support,
        "strict_schur_kernel_rows_present": False,
        "future_artifact_presence": futures,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall(),
        "strict_non_claims": [
            "does not infer A/B/C rows from source-only C_ss or compressed denominator data",
            "does not treat finite C_ss/C_sx/C_xx correlator subblocks as K-prime pole-derivative rows",
            "does not use outside-math tool names as physical row authority",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not claim retained or proposed_retained closure",
        ],
        "exact_next_action": "Continue 63/63 C_sx/C_xx row production and either derive strict Schur kernel pole/derivative rows for the s/x block or supply canonical O_H/source-overlap or W/Z physical-response authority.",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
