#!/usr/bin/env python3
"""
PR #230 neutral-scalar dynamical rank-one closure attempt.

The commutant no-go blocks symmetry-only rank-one purity.  This runner tests
the next stronger route: do the current dynamical certificates force the
neutral scalar response space itself to be rank one?  The answer is no on the
current surface.  A positive two-pole neutral scalar family keeps the
source-created pole mass and residue fixed while the canonical-Higgs overlap
varies.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"

CERTS = {
    "neutral_scalar_commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_scalar_rank_one_purity_gate": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "source_pole_canonical_higgs_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "no_orthogonal_top_coupling_selection": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
    "source_higgs_gram_purity": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_higgs_operator_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "latest_higgs_identity_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
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


def cert_status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def two_pole_dynamic_family() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_pole_mass_sq = 0.25
    source_pole_residue = 1.0
    source_pole_yukawa_readout = 1.0
    for orthogonal_mass_sq, overlap in ((1.4, 0.5), (2.0, 0.8), (3.2, 0.95)):
        rows.append(
            {
                "kernel_basis": ["source_pole", "orthogonal_neutral"],
                "quadratic_kernel": [[source_pole_mass_sq, 0.0], [0.0, orthogonal_mass_sq]],
                "kernel_positive_definite": source_pole_mass_sq > 0.0 and orthogonal_mass_sq > 0.0,
                "neutral_response_rank": 2,
                "source_vector": [1.0, 0.0],
                "source_pole_mass_sq": source_pole_mass_sq,
                "source_pole_residue": source_pole_residue,
                "orthogonal_pole_mass_sq": orthogonal_mass_sq,
                "orthogonal_pole_finite": orthogonal_mass_sq < float("inf"),
                "canonical_higgs_overlap_with_source_pole": overlap,
                "canonical_higgs_vector_in_source_basis": [overlap, (1.0 - overlap * overlap) ** 0.5],
                "source_pole_yukawa_readout": source_pole_yukawa_readout,
                "canonical_higgs_yukawa_example": source_pole_yukawa_readout * overlap,
            }
        )
    return rows


def main() -> int:
    print("PR #230 neutral-scalar dynamical rank-one closure attempt")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    commutant_blocks = (
        "neutral scalar commutant does not force rank-one purity"
        in cert_status(certs["neutral_scalar_commutant_rank_no_go"])
        and certs["neutral_scalar_commutant_rank_no_go"].get("rank_one_theorem_derived") is False
    )
    rank_one_gate_blocks = (
        "neutral scalar rank-one purity gate not passed"
        in cert_status(certs["neutral_scalar_rank_one_purity_gate"])
        and certs["neutral_scalar_rank_one_purity_gate"].get("neutral_scalar_rank_one_purity_gate_passed")
        is False
    )
    source_mixing_blocks = (
        "source-pole canonical-Higgs mixing obstruction"
        in cert_status(certs["source_pole_canonical_higgs_mixing"])
        and certs["source_pole_canonical_higgs_mixing"].get("proposal_allowed") is False
    )
    no_selection_blocks = (
        "no-orthogonal-top-coupling selection rule not derived"
        in cert_status(certs["no_orthogonal_top_coupling_selection"])
        and certs["no_orthogonal_top_coupling_selection"].get(
            "no_orthogonal_top_coupling_selection_rule_gate_passed"
        )
        is False
    )
    gram_blocks = (
        "source-Higgs Gram purity gate not passed" in cert_status(certs["source_higgs_gram_purity"])
        and certs["source_higgs_gram_purity"].get("source_higgs_gram_purity_gate_passed") is False
    )
    canonical_operator_blocks = (
        "canonical-Higgs operator realization gate not passed"
        in cert_status(certs["canonical_higgs_operator_realization"])
        and certs["canonical_higgs_operator_realization"].get("canonical_higgs_operator_realization_gate_passed")
        is False
    )
    latest_identity_blocks = (
        "latest Higgs-pole identity blocker certificate" in cert_status(certs["latest_higgs_identity_blocker"])
        and certs["latest_higgs_identity_blocker"].get("identity_closed") is False
    )

    rows = two_pole_dynamic_family()
    ranks = {int(row["neutral_response_rank"]) for row in rows}
    kernel_positive = all(bool(row["kernel_positive_definite"]) for row in rows)
    source_masses = {float(row["source_pole_mass_sq"]) for row in rows}
    source_residues = {float(row["source_pole_residue"]) for row in rows}
    orthogonal_masses = {float(row["orthogonal_pole_mass_sq"]) for row in rows}
    overlaps = {round(float(row["canonical_higgs_overlap_with_source_pole"]), 12) for row in rows}
    y_examples = {round(float(row["canonical_higgs_yukawa_example"]), 12) for row in rows}
    rank_one_dynamical_theorem_derived = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("commutant-rank-no-go-still-blocks", commutant_blocks, cert_status(certs["neutral_scalar_commutant_rank_no_go"]))
    report("rank-one-purity-gate-still-blocks", rank_one_gate_blocks, cert_status(certs["neutral_scalar_rank_one_purity_gate"]))
    report("source-pole-mixing-still-blocks", source_mixing_blocks, cert_status(certs["source_pole_canonical_higgs_mixing"]))
    report("no-orthogonal-selection-still-blocks", no_selection_blocks, cert_status(certs["no_orthogonal_top_coupling_selection"]))
    report("gram-purity-gate-still-blocks", gram_blocks, cert_status(certs["source_higgs_gram_purity"]))
    report("canonical-higgs-operator-still-missing", canonical_operator_blocks, cert_status(certs["canonical_higgs_operator_realization"]))
    report("latest-higgs-identity-still-blocks", latest_identity_blocks, cert_status(certs["latest_higgs_identity_blocker"]))
    report("rank-two-dynamic-family-exists", ranks == {2}, f"ranks={sorted(ranks)}")
    report("quadratic-kernels-positive", kernel_positive, "all source-basis kernels positive definite")
    report("orthogonal-pole-finite", all(mass > 0.0 for mass in orthogonal_masses), f"orthogonal_masses={sorted(orthogonal_masses)}")
    report("source-pole-mass-fixed", len(source_masses) == 1, f"source_masses={sorted(source_masses)}")
    report("source-pole-residue-fixed", len(source_residues) == 1, f"source_residues={sorted(source_residues)}")
    report("canonical-higgs-overlap-varies", len(overlaps) > 1, f"overlaps={sorted(overlaps)}")
    report("canonical-yukawa-example-varies", len(y_examples) > 1, f"y_examples={sorted(y_examples)}")
    report(
        "rank-one-dynamical-theorem-not-derived",
        not rank_one_dynamical_theorem_derived,
        "current certificates do not remove the finite orthogonal neutral pole",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / dynamical rank-one neutral scalar theorem not derived"
        ),
        "verdict": (
            "The current PR #230 surface does not derive a dynamical rank-one "
            "neutral scalar response theorem.  A positive two-pole neutral "
            "scalar family keeps the source-created pole mass and residue fixed "
            "while a finite orthogonal neutral pole remains and the canonical-Higgs "
            "overlap varies.  Therefore source-pole purity still needs a "
            "dynamical rank-one theorem, same-surface C_sH/C_HH Gram-purity data, "
            "or an equivalent accepted Higgs-identity certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Open Higgs-pole identity and source-Higgs purity imports remain.",
        "rank_one_dynamical_theorem_derived": rank_one_dynamical_theorem_derived,
        "dynamic_counterfamily": rows,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s=1, cos(theta)=1, c2=1, or Z_match=1",
            "does not use H_unit matrix-element readout or yt_ward_identity authority",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, or reduced cold pilots as proof selectors",
            "does not treat finite orthogonal mass as decoupling without a derived decoupling theorem",
        ],
        "exact_next_action": (
            "Measure same-surface C_sH/C_HH Gram purity, derive a genuine "
            "dynamical rank-one theorem, implement W/Z response with identity "
            "certificates, or process seed-controlled FH/LSZ chunks."
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
