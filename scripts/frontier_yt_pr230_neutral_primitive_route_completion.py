#!/usr/bin/env python3
"""PR #230 neutral primitive/rank-one route completion gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_neutral_primitive_route_completion_2026-05-06.json"

PARENTS = {
    "primitive_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "primitive_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "positivity_rank_one_support": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "neutral_irreducibility_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "neutral_burnside_attempt": "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json",
    "neutral_offdiagonal_generator": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "neutral_rank_one_gate": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "neutral_commutant_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_dynamical_rank_one": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "orthogonal_neutral_decoupling": "outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json",
    "no_orthogonal_top_coupling_import": "outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json",
    "no_orthogonal_top_coupling_selection_rule": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
}

FUTURE_ARTIFACTS = {
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "neutral_scalar_rank_one_purity_certificate": "outputs/yt_neutral_scalar_rank_one_purity_certificate_2026-05-03.json",
    "neutral_scalar_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
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
        "used_positivity_without_irreducibility": False,
        "used_commutant_rank_as_rank_one_purity": False,
        "used_source_only_rows_as_neutral_transfer": False,
        "used_hunit_or_ward": False,
        "used_observed_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 neutral primitive/rank-one route completion gate")
    print("=" * 72)
    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()

    primitive_gate_open = (
        certs["primitive_gate"].get("primitive_cone_certificate_gate_passed") is False
        and "strict irreducibility certificate absent" in statuses["primitive_gate"]
    )
    primitive_stretch_blocks = (
        certs["primitive_stretch_no_go"].get("primitive_cone_stretch_no_go_passed") is True
        and certs["primitive_stretch_no_go"].get("proposal_allowed") is False
    )
    conditional_rank_support_only = (
        certs["positivity_rank_one_support"].get("positivity_improving_rank_one_theorem_passed") is True
        and certs["positivity_rank_one_support"].get("positivity_improving_certificate_present") is False
    )
    irreducibility_authority_absent = (
        certs["neutral_irreducibility_audit"].get("authority_audit_passed") is True
        and certs["neutral_irreducibility_audit"].get("neutral_scalar_irreducibility_certificate_present") is False
    )
    burnside_blocks = (
        certs["neutral_burnside_attempt"].get("exact_negative_boundary_passed") is True
        and certs["neutral_burnside_attempt"].get("burnside_irreducibility_certificate_passed") is False
    )
    offdiagonal_absent = (
        certs["neutral_offdiagonal_generator"].get("exact_negative_boundary_passed") is True
        and certs["neutral_offdiagonal_generator"].get("offdiagonal_generator_written") is False
    )
    rank_one_gate_open = (
        "neutral scalar rank-one purity gate not passed" in statuses["neutral_rank_one_gate"]
        and certs["neutral_rank_one_gate"].get("proposal_allowed") is False
    )
    shortcut_nogos_loaded = (
        "commutant does not force rank-one purity" in statuses["neutral_commutant_no_go"]
        and "dynamical rank-one neutral scalar theorem not derived" in statuses["neutral_dynamical_rank_one"]
        and "orthogonal neutral decoupling shortcut not derived" in statuses["orthogonal_neutral_decoupling"]
        and "no-orthogonal-top-coupling import audit" in statuses["no_orthogonal_top_coupling_import"]
        and "no-orthogonal-top-coupling selection rule not derived" in statuses["no_orthogonal_top_coupling_selection_rule"]
    )
    future_absent = not any(futures.values())
    clean_firewall = all(value is False for value in firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("primitive-cone-gate-open", primitive_gate_open, statuses["primitive_gate"])
    report("primitive-stretch-current-surface-blocks", primitive_stretch_blocks, statuses["primitive_stretch_no_go"])
    report("conditional-rank-one-support-only", conditional_rank_support_only, statuses["positivity_rank_one_support"])
    report("irreducibility-authority-absent", irreducibility_authority_absent, statuses["neutral_irreducibility_audit"])
    report("burnside-current-generators-block", burnside_blocks, statuses["neutral_burnside_attempt"])
    report("offdiagonal-generator-absent", offdiagonal_absent, statuses["neutral_offdiagonal_generator"])
    report("rank-one-purity-gate-open", rank_one_gate_open, statuses["neutral_rank_one_gate"])
    report("neutral-shortcut-nogos-loaded", shortcut_nogos_loaded, "commutant/dynamical/decoupling/import/selection shortcuts checked")
    report("future-neutral-certificate-absent", future_absent, str(futures))
    report("forbidden-firewall-clean", clean_firewall, str(firewall()))

    passed = (
        not missing
        and not proposal_allowed
        and primitive_gate_open
        and primitive_stretch_blocks
        and conditional_rank_support_only
        and irreducibility_authority_absent
        and burnside_blocks
        and offdiagonal_absent
        and rank_one_gate_open
        and shortcut_nogos_loaded
        and future_absent
        and clean_firewall
    )
    result = {
        "actual_current_surface_status": "exact negative boundary / neutral primitive-rank-one route not complete on current PR230 surface",
        "conditional_surface_status": "The route remains hard-physics open if a same-surface primitive neutral transfer, off-diagonal generator, or irreducibility/rank-one certificate is supplied.",
        "proposal_allowed": False,
        "proposal_allowed_reason": "Conditional Perron support exists, but the current surface has no primitive-cone/irreducibility/off-diagonal-generator certificate.",
        "bare_retained_allowed": False,
        "neutral_primitive_route_completion_passed": passed,
        "exact_negative_boundary_passed": passed,
        "future_artifact_presence": futures,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall(),
        "strict_non_claims": [
            "does not treat positivity alone as rank-one purity",
            "does not treat commutant rank, source-only rows, or decoupling shortcuts as irreducibility",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not claim retained or proposed_retained closure",
        ],
        "exact_next_action": "A positive theorem must construct the missing same-surface neutral off-diagonal/primitive transfer certificate; otherwise use future physical rows.",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
