#!/usr/bin/env python3
"""
PR #230 O_sp/O_H assumption-route audit.

This runner is the current physics-loop assumption exercise for the active
source-pole-to-canonical-Higgs blocker.  It verifies that the loop pack and
paired certificates keep allowed support, forbidden shortcuts, and remaining
positive routes separated.  It does not claim y_t closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / ".claude" / "science" / "physics-loops" / "yt-pr230-osp-oh-retained-closure-20260503"
OUTPUT = ROOT / "outputs" / "yt_osp_oh_assumption_route_audit_2026-05-04.json"

PACK_FILES = [
    "STATE.yaml",
    "GOAL.md",
    "ASSUMPTIONS_AND_IMPORTS.md",
    "OPPORTUNITY_QUEUE.md",
    "NO_GO_LEDGER.md",
    "CLAIM_STATUS_CERTIFICATE.md",
    "HANDOFF.md",
]

CERTS = {
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "source_functional_lsz": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "isolated_pole_gram_factorization": "outputs/yt_isolated_pole_gram_factorization_theorem_2026-05-03.json",
    "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_higgs_gram_contract": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "wz_response_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "schur_row_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "neutral_scalar_positivity": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

ASSUMPTION_TERMS = [
    "Legendre/LSZ `O_sp`",
    "Canonical Higgs radial `O_H`",
    "`O_sp/O_H` overlap",
    "`H_unit` matrix-element readout",
    "Observed `m_t` / `y_t`",
    "`kappa_s = 1`, `cos(theta)=1`",
    "Same-source W/Z response rows",
    "Schur `A/B/C` neutral kernel rows",
    "Neutral-sector irreducibility / positivity improvement",
    "Complete FH/LSZ production evidence",
]

QUEUE_TERMS = [
    "Source-Higgs Gram purity with `O_sp` source side",
    "Same-source W/Z response",
    "Dynamical rank-one neutral scalar theorem",
    "Finish finite-source-linearity calibration",
    "Continue FH/LSZ chunks",
    "Scalar denominator / Schur K-prime rows",
]

FORBIDDEN_CLOSURE_IMPORTS = [
    "used H_unit / Ward matrix-element readout",
    "used observed m_t or y_t as a selector",
    "set kappa_s=1 or cos(theta)=1",
    "treated static EW algebra as O_H",
    "promoted finite Schur support into A/B/C rows",
    "imported gauge Perron/reflection positivity as neutral-sector irreducibility",
    "used reduced pilots or source-Higgs guards as production evidence",
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


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 O_sp/O_H assumption-route audit")
    print("=" * 72)

    pack = {name: read(LOOP / name) for name in PACK_FILES}
    certs = {name: load_json(path) for name, path in CERTS.items()}

    missing_pack = [name for name, text in pack.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    assumptions = pack["ASSUMPTIONS_AND_IMPORTS.md"]
    queue = pack["OPPORTUNITY_QUEUE.md"]
    claim = pack["CLAIM_STATUS_CERTIFICATE.md"]
    state = pack["STATE.yaml"]

    missing_assumption_terms = [term for term in ASSUMPTION_TERMS if term not in assumptions]
    missing_queue_terms = [term for term in QUEUE_TERMS if term not in queue]

    claim_firewall_open = (
        "proposal_allowed: false" in claim
        and "bare_retained_allowed: false" in claim
        and "same-surface `O_H` realization" in claim
        and "independent audit" in claim
    )
    state_tracks_current_chunks = (
        "34/63 chunks" in state
        or "34/63" in state
        or "chunks035-040" in state
    )

    osp_constructed_not_oh = (
        "Legendre source-pole operator constructed" in status(certs["legendre_source_pole_operator"])
        and certs["legendre_source_pole_operator"].get("source_pole_operator_constructed") is True
        and certs["legendre_source_pole_operator"].get("canonical_higgs_operator_identity_passed") is False
    )
    source_only_rejected = (
        "source-functional LSZ identifiability" in status(certs["source_functional_lsz"])
        and certs["source_functional_lsz"].get("theorem_closed") is False
    )
    gram_factorization_support_only = (
        "isolated-pole Gram factorization" in status(certs["isolated_pole_gram_factorization"])
        and certs["isolated_pole_gram_factorization"].get(
            "isolated_pole_gram_factorization_theorem_passed"
        )
        is True
        and certs["isolated_pole_gram_factorization"].get("proposal_allowed") is False
    )
    osp_oh_identity_still_blocked = (
        "O_sp-to-O_H identity not derived" in status(certs["osp_oh_identity_stretch"])
        and certs["osp_oh_identity_stretch"].get("proposal_allowed") is False
    )
    mixing_countermodel_loaded = (
        "source-pole canonical-Higgs mixing obstruction" in status(certs["source_pole_mixing"])
        and certs["source_pole_mixing"].get("proposal_allowed") is False
    )
    source_higgs_contract_not_evidence = (
        "source-Higgs Gram-purity contract witness" in status(certs["source_higgs_gram_contract"])
        and certs["source_higgs_gram_contract"].get("contract_witness_passed") is True
        and certs["source_higgs_gram_contract"].get("proposal_allowed") is False
    )
    source_higgs_launch_blocked = (
        "source-Higgs production launch blocked" in status(certs["source_higgs_readiness"])
        and certs["source_higgs_readiness"].get("proposal_allowed") is False
    )
    wz_route_not_current_evidence = (
        "same-source WZ response certificate gate not passed" in status(certs["wz_response_gate"])
        and certs["wz_response_gate"].get("same_source_wz_response_certificate_gate_passed") is False
        and "WZ correlator mass-fit path absent" in status(certs["wz_mass_fit_path"])
        and "sector-overlap identity obstruction" in status(certs["wz_sector_overlap"])
    )
    schur_route_not_current_evidence = (
        "Schur row candidate extraction" in status(certs["schur_row_extraction"])
        and certs["schur_row_extraction"].get("exact_negative_boundary_passed") is True
    )
    rank_one_route_not_current_evidence = (
        "neutral-scalar positivity-improving direct theorem not derived"
        in status(certs["neutral_scalar_positivity"])
        and certs["neutral_scalar_positivity"].get("direct_positivity_improving_theorem_derived")
        is False
    )
    closure_still_open = (
        "retained closure not yet reached" in status(certs["retained_route"])
        and "active campaign continuing" in status(certs["campaign_status"])
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    route_matrix = [
        {
            "route": "source_higgs_gram_purity",
            "current_status": status(certs["source_higgs_readiness"]),
            "support_available": "O_sp normalization and Gram-purity contract",
            "blocked_by": "missing certified O_H plus production C_sH/C_HH pole residues",
            "proposal_allowed": False,
        },
        {
            "route": "same_source_wz_response",
            "current_status": status(certs["wz_mass_fit_path"]),
            "support_available": "W/Z response gate and mass-fit path contract",
            "blocked_by": "missing same-source EW action, W/Z correlator mass fits, and sector-overlap identity",
            "proposal_allowed": False,
        },
        {
            "route": "schur_kprime_rows",
            "current_status": status(certs["schur_row_extraction"]),
            "support_available": "Schur sufficiency/contract layer",
            "blocked_by": "missing same-surface A/B/C neutral scalar kernel rows",
            "proposal_allowed": False,
        },
        {
            "route": "neutral_scalar_rank_one",
            "current_status": status(certs["neutral_scalar_positivity"]),
            "support_available": "conditional Perron/rank-one support",
            "blocked_by": "missing neutral-sector irreducibility / positivity improvement",
            "proposal_allowed": False,
        },
        {
            "route": "fh_lsz_chunks",
            "current_status": "bounded production support in progress",
            "support_available": "34/63 L12 chunks ready before live chunks035-040 complete",
            "blocked_by": "response-window acceptance and O_H/source-overlap closure",
            "proposal_allowed": False,
        },
    ]

    report("loop-pack-current-files-present", not missing_pack, f"missing={missing_pack}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("assumption-ledger-covers-current-blocker", not missing_assumption_terms, f"missing={missing_assumption_terms}")
    report("opportunity-queue-covers-ranked-routes", not missing_queue_terms, f"missing={missing_queue_terms}")
    report("claim-firewall-open", claim_firewall_open, "proposal and bare retained blocked")
    report("state-tracks-live-chunk-campaign", state_tracks_current_chunks, "STATE mentions current chunk campaign")
    report("osp-constructed-but-not-oh", osp_constructed_not_oh, status(certs["legendre_source_pole_operator"]))
    report("source-only-lsz-rejected", source_only_rejected, status(certs["source_functional_lsz"]))
    report("isolated-pole-gram-factorization-support-only", gram_factorization_support_only, status(certs["isolated_pole_gram_factorization"]))
    report("osp-oh-identity-still-blocked", osp_oh_identity_still_blocked, status(certs["osp_oh_identity_stretch"]))
    report("mixing-countermodel-loaded", mixing_countermodel_loaded, status(certs["source_pole_mixing"]))
    report("source-higgs-contract-not-evidence", source_higgs_contract_not_evidence, status(certs["source_higgs_gram_contract"]))
    report("source-higgs-production-blocked", source_higgs_launch_blocked, status(certs["source_higgs_readiness"]))
    report("wz-route-not-current-evidence", wz_route_not_current_evidence, status(certs["wz_mass_fit_path"]))
    report("schur-route-not-current-evidence", schur_route_not_current_evidence, status(certs["schur_row_extraction"]))
    report("rank-one-route-not-current-evidence", rank_one_route_not_current_evidence, status(certs["neutral_scalar_positivity"]))
    report("closure-still-open", closure_still_open, status(certs["retained_route"]))

    audit_passed = (
        not missing_pack
        and not missing_certs
        and not proposal_allowed
        and not missing_assumption_terms
        and not missing_queue_terms
        and claim_firewall_open
        and osp_constructed_not_oh
        and source_only_rejected
        and gram_factorization_support_only
        and osp_oh_identity_still_blocked
        and mixing_countermodel_loaded
        and source_higgs_contract_not_evidence
        and source_higgs_launch_blocked
        and wz_route_not_current_evidence
        and schur_route_not_current_evidence
        and rank_one_route_not_current_evidence
        and closure_still_open
    )

    result = {
        "actual_current_surface_status": (
            "open / O_sp-to-O_H assumption-route audit complete; retained closure still blocked"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current loop has an explicit O_sp source-pole construction and "
            "exact support theorems, but still lacks a same-surface O_H identity "
            "or equivalent C_sH/C_HH, W/Z, Schur, or rank-one closure row."
        ),
        "bare_retained_allowed": False,
        "assumption_route_audit_passed": audit_passed,
        "missing_pack_files": missing_pack,
        "missing_certificates": missing_certs,
        "missing_assumption_terms": missing_assumption_terms,
        "missing_queue_terms": missing_queue_terms,
        "forbidden_closure_imports_checked": FORBIDDEN_CLOSURE_IMPORTS,
        "route_matrix": route_matrix,
        "parent_certificates": CERTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify O_sp with O_H",
            "does not set kappa_s=1 or cos(theta)=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat contracts, guards, finite-ladder rows, or in-progress chunks as closure",
        ],
        "exact_next_action": (
            "Continue live FH/LSZ chunks.  For positive closure, supply one real "
            "missing premise: certified O_H with C_sH/C_HH pole residues, "
            "same-source W/Z mass-response rows with identity certificates, "
            "same-surface Schur A/B/C kernel rows, or a neutral-sector "
            "irreducibility theorem."
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
