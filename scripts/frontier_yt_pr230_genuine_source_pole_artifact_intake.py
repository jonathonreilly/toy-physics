#!/usr/bin/env python3
"""
PR #230 genuine source-pole artifact intake.

The refreshed campaign target is to find a genuine artifact inside one of the
remaining closure contracts.  This runner certifies the strongest current
artifact in the cleanest contract: the Legendre/LSZ-normalized same-source
operator O_sp.  It is real source-side support, not physical y_t closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json"
)

PARENTS = {
    "source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_contract_witness": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "fresh_artifact_review": "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json",
    "oh_source_higgs_rescan": "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

LITERATURE_CONTEXT = [
    {
        "id": "fms_gauge_invariant_higgs_operator_language",
        "source": "https://doi.org/10.1103/PhysRevD.101.056006",
        "role": "context for gauge-invariant composite Higgs operators after a gauge-Higgs action is supplied",
        "not_used_as": "PR230 source-to-Higgs identity or kappa_s selector",
    },
    {
        "id": "fh_qft_source_response_method",
        "source": "https://doi.org/10.1103/PhysRevD.96.014504",
        "role": "context for source-response measurements from two-point functions",
        "not_used_as": "canonical-Higgs normalization or source-pole purity authority",
    },
]

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
    return str(cert.get("actual_current_surface_status") or cert.get("verdict", ""))


def finite_close(value: Any, target: float, tol: float = 1.0e-12) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value)) and abs(float(value) - target) <= tol


def firewall_clean(candidate: dict[str, Any]) -> bool:
    firewall = candidate.get("firewall", {})
    if not isinstance(firewall, dict):
        return False
    return all(
        firewall.get(key) is False
        for key in (
            "used_alpha_lm_or_plaquette",
            "used_hunit_matrix_element_readout",
            "used_observed_targets_as_selectors",
            "used_yt_ward_identity",
        )
    )


def rescaling_invariant(source: dict[str, Any]) -> bool:
    rows = source.get("source_rescaling_rows", [])
    return bool(rows) and all(
        finite_close(row.get("matrix_element_O_source_pole"), 1.0)
        and finite_close(row.get("source_pole_residue"), 1.0)
        for row in rows
        if isinstance(row, dict)
    )


def contact_invariant(source: dict[str, Any]) -> bool:
    rows = source.get("contact_term_rows", [])
    return bool(rows) and all(
        finite_close(row.get("Res_C_source_pole_operator"), 1.0)
        for row in rows
        if isinstance(row, dict)
    )


def main() -> int:
    print("PR #230 genuine source-pole artifact intake")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    source = certs["source_pole_operator"]
    candidate = source.get("operator_candidate", {})
    if not isinstance(candidate, dict):
        candidate = {}

    artifact_constructed = (
        source.get("source_pole_operator_constructed") is True
        and candidate.get("source_pole_operator_constructed") is True
        and candidate.get("source_pole_residue_normalized_to_one") is True
    )
    source_side_only = (
        source.get("canonical_higgs_operator_identity_passed") is False
        and candidate.get("canonical_higgs_operator_identity_passed") is False
    )
    same_surface_source = (
        candidate.get("same_surface_cl3z3") is True
        and candidate.get("same_source_coordinate") is True
        and candidate.get("source_coordinate")
        == "uniform additive lattice scalar source s entering the Dirac mass as m_bare + s"
    )
    current_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["oh_source_higgs_rescan"].get("canonical_oh_absent") is True
    )
    csh_chh_absent = (
        certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_builder"].get("candidate_written") is False
        and certs["oh_source_higgs_rescan"].get("source_higgs_rows_absent") is True
    )
    gram_waits = (
        certs["source_higgs_postprocessor"].get("osp_higgs_gram_purity_gate_passed")
        is False
        and certs["source_higgs_contract_witness"].get("contract_witness_passed")
        is True
    )
    no_closure = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    artifact_genuine = (
        artifact_constructed
        and source_side_only
        and same_surface_source
        and rescaling_invariant(source)
        and contact_invariant(source)
        and firewall_clean(candidate)
    )
    closure_ready = artifact_genuine and not current_oh_absent and not csh_chh_absent

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("source-pole-operator-constructed", artifact_constructed, candidate.get("operator_id", ""))
    report("same-surface-same-source-coordinate", same_surface_source, candidate.get("source_coordinate", ""))
    report("source-rescaling-invariant", rescaling_invariant(source), f"rows={len(source.get('source_rescaling_rows', []))}")
    report("contact-term-invariant", contact_invariant(source), f"rows={len(source.get('contact_term_rows', []))}")
    report("forbidden-firewall-clean", firewall_clean(candidate), json.dumps(candidate.get("firewall", {}), sort_keys=True))
    report("canonical-oh-identity-open", source_side_only, status(source))
    report("canonical-oh-current-certificate-absent", current_oh_absent, status(certs["canonical_higgs_operator_gate"]))
    report("csh-chh-pole-rows-absent", csh_chh_absent, status(certs["source_higgs_builder"]))
    report("gram-purity-waits-for-real-rows", gram_waits, status(certs["source_higgs_postprocessor"]))
    report("genuine-source-side-artifact-intaken", artifact_genuine, "O_sp is real source-side support only")
    report("artifact-not-closure", not closure_ready, "O_sp-Higgs overlap remains open")
    report("aggregate-closure-still-barred", no_closure, "full/retained/campaign proposal_allowed=false")

    result = {
        "actual_current_surface_status": (
            "exact-support / genuine same-source O_sp source-pole artifact intake; canonical O_H bridge open"
        ),
        "verdict": (
            "The current PR230 surface contains one genuine artifact in the "
            "source-Higgs contract: the Legendre/LSZ-normalized source-pole "
            "operator O_sp.  It is same-surface, same-source, invariant under "
            "source-coordinate rescaling, insensitive to analytic source contact "
            "terms, and passes the forbidden-import firewall.  It is not "
            "physical top-Yukawa closure because O_sp = O_H, C_spH/C_HH pole "
            "rows, Gram purity, scalar-LSZ production authority, and aggregate "
            "retained-route authorization remain absent."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "O_sp is source-side support only; canonical O_H identity and O_sp-Higgs overlap rows are still missing.",
        "artifact_contract": "O_H/C_sH/C_HH source-Higgs pole rows",
        "genuine_artifact": {
            "artifact_id": candidate.get("operator_id"),
            "artifact_path": PARENTS["source_pole_operator"],
            "artifact_is_genuine_current_surface_support": artifact_genuine,
            "artifact_is_physics_closure": False,
            "proof_role": "source-side LSZ pole normalization only",
        },
        "artifact_is_genuine_current_surface_support": artifact_genuine,
        "artifact_is_physics_closure": False,
        "canonical_higgs_operator_identity_passed": False,
        "same_surface_source_coordinate": same_surface_source,
        "source_rescaling_invariant": rescaling_invariant(source),
        "contact_term_invariant": contact_invariant(source),
        "forbidden_firewall": candidate.get("firewall", {}),
        "current_closure_blockers": {
            "canonical_oh_certificate_absent": current_oh_absent,
            "csp_higgs_or_csh_chh_pole_rows_absent": csh_chh_absent,
            "osp_higgs_gram_purity_not_passed": gram_waits,
            "aggregate_proposal_allowed": False,
        },
        "cleanest_next_artifact": {
            "name": "O_sp-Higgs pole-residue Gram rows",
            "required_rows": [
                "Res_C_sp_sp = 1 from O_sp",
                "Res_C_spH",
                "Res_C_HH",
            ],
            "acceptance_condition": "Res_C_spH^2 = Res_C_sp_sp * Res_C_HH with same-surface O_H identity/normalization and FV/IR/model-class authority",
            "why_cleanest": "O_sp has already removed source-unit gauge freedom, so the next measurement is exactly the remaining source-to-canonical-Higgs overlap.",
        },
        "literature_context": LITERATURE_CONTEXT,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify O_sp with O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat literature, PSLQ, D-modules, GNS, or FMS terminology as proof selectors",
        ],
        "parent_certificates": PARENTS,
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
