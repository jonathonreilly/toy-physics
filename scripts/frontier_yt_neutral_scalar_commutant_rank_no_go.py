#!/usr/bin/env python3
"""
PR #230 neutral-scalar commutant rank no-go.

This block tests the strongest symmetry-only version of the rank-one purity
route: do the current listed neutral scalar labels/D17 support force a
one-dimensional response space?  If the same labels allow a rank-two commutant,
then source-pole purity still needs a dynamical theorem or C_sH/C_HH data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"

CERTS = {
    "neutral_scalar_rank_one_purity": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "d17_source_pole_identity": "outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json",
    "hunit_candidate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
    "source_higgs_cross_correlator_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "higgs_identity_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def rank_two_commutant_family() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon, source_higgs_overlap in ((0.2, 0.5), (0.6, 0.8), (1.0, 0.95)):
        response = [[1.0, 0.0], [0.0, epsilon]]
        source_vector = [1.0, 0.0]
        canonical_h_vector = [source_higgs_overlap, (1.0 - source_higgs_overlap * source_higgs_overlap) ** 0.5]
        rows.append(
            {
                "neutral_labels_identical": True,
                "commutant_dimension": 4,
                "response_matrix": response,
                "matrix_rank": 2 if epsilon > 0 else 1,
                "source_vector": source_vector,
                "canonical_higgs_vector": canonical_h_vector,
                "source_only_residue": response[0][0],
                "source_higgs_overlap": canonical_h_vector[0],
                "rank_one_purity": epsilon == 0.0,
            }
        )
    return rows


def main() -> int:
    print("PR #230 neutral-scalar commutant rank no-go")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    rank_one_gate_blocks = (
        "neutral scalar rank-one purity gate not passed"
        in status(certs["neutral_scalar_rank_one_purity"])
        and certs["neutral_scalar_rank_one_purity"].get("neutral_scalar_rank_one_purity_gate_passed")
        is False
    )
    no_selection_rule_blocks = (
        "no-orthogonal-top-coupling selection rule not derived"
        in status(certs["no_orthogonal_top_coupling_selection"])
        and certs["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    d17_blocks = (
        "D17 source-pole identity closure attempt blocked" in status(certs["d17_source_pole_identity"])
        and certs["d17_source_pole_identity"].get("theorem_closed") is False
    )
    hunit_blocks = (
        "H_unit not canonical-Higgs operator realization" in status(certs["hunit_candidate"])
        and certs["hunit_candidate"].get("hunit_canonical_higgs_operator_gate_passed") is False
    )
    manifest_not_evidence = (
        "source-Higgs cross-correlator production manifest"
        in status(certs["source_higgs_cross_correlator_manifest"])
        and certs["source_higgs_cross_correlator_manifest"].get("manifest_is_evidence") is False
    )
    gram_blocks = (
        "source-Higgs Gram purity gate not passed" in status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    latest_identity_blocks = (
        "latest Higgs-pole identity blocker certificate" in status(certs["higgs_identity_blocker"])
        and certs["higgs_identity_blocker"].get("identity_closed") is False
    )

    rows = rank_two_commutant_family()
    ranks = {int(row["matrix_rank"]) for row in rows}
    source_residues = {float(row["source_only_residue"]) for row in rows}
    overlaps = {round(float(row["source_higgs_overlap"]), 12) for row in rows}
    commutant_dimensions = {int(row["commutant_dimension"]) for row in rows}
    rank_one_theorem_derived = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("rank-one-purity-gate-still-blocks", rank_one_gate_blocks, status(certs["neutral_scalar_rank_one_purity"]))
    report("no-orthogonal-selection-rule-still-blocks", no_selection_rule_blocks, status(certs["no_orthogonal_top_coupling_selection"]))
    report("d17-source-pole-identity-still-blocks", d17_blocks, status(certs["d17_source_pole_identity"]))
    report("hunit-candidate-still-blocks", hunit_blocks, status(certs["hunit_candidate"]))
    report("csh-manifest-not-evidence", manifest_not_evidence, status(certs["source_higgs_cross_correlator_manifest"]))
    report("gram-purity-gate-still-blocks", gram_blocks, status(certs["source_higgs_gram_purity"]))
    report("latest-higgs-identity-still-blocks", latest_identity_blocks, status(certs["higgs_identity_blocker"]))
    report("rank-two-commutant-family-exists", 2 in ranks, f"ranks={sorted(ranks)}")
    report("source-only-residue-can-stay-fixed", len(source_residues) == 1, f"source_residues={sorted(source_residues)}")
    report("source-higgs-overlap-underdetermined", len(overlaps) > 1, f"overlaps={sorted(overlaps)}")
    report("commutant-not-one-dimensional", commutant_dimensions == {4}, f"commutant_dimensions={sorted(commutant_dimensions)}")
    report("rank-one-theorem-not-derived", not rank_one_theorem_derived, "symmetry labels alone do not force epsilon=0")

    result = {
        "actual_current_surface_status": "exact negative boundary / neutral scalar commutant does not force rank-one purity",
        "verdict": (
            "Current neutral scalar labels/D17 support do not force the response "
            "space to be rank one.  With two neutral scalars carrying identical "
            "listed labels, the symmetry commutant contains a rank-two positive "
            "response family.  Source-only C_ss data can remain fixed while the "
            "canonical-Higgs overlap is not certified by symmetry alone.  A "
            "rank-one result still requires a dynamical theorem, C_sH/C_HH "
            "Gram purity data, or another accepted Higgs-identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The current symmetry/D17 surface does not derive the rank-one neutral scalar response theorem.",
        "rank_one_theorem_derived": rank_one_theorem_derived,
        "parent_certificates": CERTS,
        "rank_two_commutant_family": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set cos(theta)=1 or kappa_s=1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat D17 carrier support as rank-one dynamics",
        ],
        "exact_next_action": (
            "Derive a dynamical rank-one neutral scalar theorem, measure C_sH/C_HH "
            "Gram purity, implement W/Z response with identity certificates, or "
            "process seed-controlled FH/LSZ chunks."
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
